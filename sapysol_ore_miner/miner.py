# ================================================================================
#
from   solana.rpc.api        import Client
from   solders.pubkey        import Pubkey
from   solders.keypair       import Keypair
from   solana.exceptions     import SolanaRpcException
from  .anchorpy.instructions import *
from  .anchorpy.accounts     import *
from  .derive                import *
from   sapysol.sysvar.clock  import SysvarClock, SYSVAR_CLOCK_PUBKEY
from   sapysol               import MakeKeypair, MakePubkey, EnsurePathExists, FetchAccount, FetchAccounts, SapysolTx
from   sapysol.ix            import *
from   sapysol.tx            import *
from   concurrent.futures    import ProcessPoolExecutor
from   pathlib               import Path
from   typing                import Tuple
import random
import json
import sha3
import os

# ================================================================================
#
class _MinerAccounts:
    def __init__(self, connection: Client, signer: Keypair):
        self.CONNECTION:    Client      = connection
        self.SIGNER:        Keypair     = MakeKeypair(signer)
        self.PROOF_PUBKEY:  Pubkey      = DeriveProofAddress(authority=self.SIGNER.pubkey())
        self.PROOF:         Proof       = None
        self.TREASURY:      Treasury    = None 
        self.CLOCK:         SysvarClock = None
        self.BUSES:         List[Bus]   = None
        self.LAST_NONCE:    int         = 0

    # ========================================
    #
    def UpdateNonce(self, nonce: int) -> None:
        EnsurePathExists(".cache")
        filePath = os.path.join(".cache", f"{str(self.SIGNER.pubkey())}.json")
        with open(filePath, "w") as f:
            json.dump({"nonce": nonce}, f)
        self.LAST_NONCE: int = nonce

    # ========================================
    #
    def GetNonce(self) -> int:
        try:
            filePath = os.path.join(".cache", f"{str(self.SIGNER.pubkey())}.json")
            with open(filePath) as f:
                self.LAST_NONCE = json.loads(f.read())["nonce"]
        except:
            pass
        return self.LAST_NONCE

    # ========================================
    #
    # Do less calls to RPC, fetch all accounts in one run.
    def FetchState(self):
        accounts = FetchAccounts(connection=self.CONNECTION, 
                                    pubkeys   = [self.PROOF_PUBKEY,
                                                TREASURY_ADDRESS,
                                                SYSVAR_CLOCK_PUBKEY,
                                                *BUS_ADDRESSES])
        self.PROOF:    Proof       = Proof.decode      (accounts[0].data)
        self.TREASURY: Treasury    = Treasury.decode   (accounts[1].data)
        self.CLOCK:    SysvarClock = SysvarClock.decode(accounts[2].data)
        self.BUSES:    List[Bus]   = [ Bus.decode(entry.data) if entry else None for entry in accounts[3:] ]


class Miner:
    # ========================================
    #
    def __init__(self, connection: Client, signer: Keypair, priorityFee: int=20_000, connectionOverride=None):
        self.CONNECTION:    Client         =  connection
        self.CONN_OVERRIDE                 =  connectionOverride if connectionOverride else connection
        self.PRIORITY_FEE:  int            =  priorityFee
        self.SIGNER:        Keypair        =  MakeKeypair(signer)
        self.ACCOUNTS:      _MinerAccounts = _MinerAccounts(connection=connection, signer=signer)

    # ========================================
    #
    def Register(self) -> bool:
        proofAddress = DeriveProofAddress(authority=self.SIGNER.pubkey())
        accountInfo  = FetchAccount(connection=self.CONNECTION, pubkey=proofAddress)
        if accountInfo:
            print(f"Miner {str(self.SIGNER.pubkey()):>44}: is already registered.")
            return True

        print(f"Registering miner {str(self.SIGNER.pubkey())}...")
        accounts = RegisterAccounts(ore_program = ORE_PROGRAM_ID,
                                    signer      = self.SIGNER.pubkey(),
                                    proof       = proofAddress)
        registerIx = register(accounts=accounts, seed=DeriveProofBump(authority=self.SIGNER.pubkey()))

        tx = SapysolTx(connection=self.CONNECTION, payer=self.SIGNER)
        tx.FromInstructionsLegacy([registerIx])
        tx.Sign()
        result = tx.SendAndWait()
        if result == SapysolTxStatus.SUCCESS:
            logging.info(f"Miner registration successful!")
            return True

        logging.info(f"Miner registration failed or timed out! Please check transaction logs")
        return False

    # ========================================
    #
    def FindHash(self, seed: bytes, difficulty: bytes) -> Tuple[bytes, int]:
        nonce    = self.ACCOUNTS.GetNonce()
        maxNonce = 2**64
        while True:
            k = sha3.keccak_256()
            k.update(bytes(seed) + bytes(self.SIGNER.pubkey()) + nonce.to_bytes(8, "little"))
            digest = k.digest()
            if digest < difficulty:
                return digest, nonce
            #nonce += 1
            nonce = random.randint(0, maxNonce)

    # ========================================
    #
    def TryResetEpoch(self) -> bool:
        threshold = self.ACCOUNTS.TREASURY.last_reset_at + EPOCH_DURATION
        if self.ACCOUNTS.CLOCK.unix_timestamp < threshold:
            return False

        ixList = []
        ixList.append(ComputeBudgetIx())
        ixList.append(ComputePriceIx(self.PRIORITY_FEE))
        ixList.append(reset(signer=self.SIGNER.pubkey()))

        tx: SapysolTx = SapysolTx(connection=self.CONNECTION, payer=self.SIGNER)
        tx.FromInstructionsLegacy(ixList).Sign()
        logging.info(f"Trying to reset epoch...")
        result = tx.SendAndWait(self.CONN_OVERRIDE)
        # We actually don't care about the result
        return True

    # ========================================
    #
    def MineSingleTry(self):
        self.ACCOUNTS.FetchState()
        currentHash       = bytes(self.ACCOUNTS.PROOF.hash)
        currentDifficulty = self.ACCOUNTS.TREASURY.difficulty

        logging.info(f"Miner {str(self.SIGNER.pubkey()):>44}: rewards: {self.ACCOUNTS.PROOF.claimable_rewards / 1_000_000_000}")
        logging.info(f"Miner {str(self.SIGNER.pubkey()):>44}: mining next block...")
        hash, nonce = self.FindHash(seed=bytes(currentHash), difficulty=bytes(currentDifficulty))
        self.ACCOUNTS.UpdateNonce(nonce=nonce)
        logging.info(f"Miner {str(self.SIGNER.pubkey()):>44}: Found hash with nonce: {nonce}")

        # Refetch because mining could take a lot of time
        self.ACCOUNTS.FetchState()

        # Check if epoch reset is needed
        if self.TryResetEpoch():
            return

        bus, busAddress = self.GetCorrectBus(rewardRate=self.ACCOUNTS.TREASURY.reward_rate)
        busRewards: float = bus.rewards / 1_000_000_000
        logging.info(f"Miner {str(self.SIGNER.pubkey()):>44}: sending on bus {str(busAddress)} (with {busRewards} ORE)")

        try:
            ixMine = mine(signer = self.SIGNER.pubkey(), 
                          bus    = busAddress, 
                          proof  = self.ACCOUNTS.PROOF_PUBKEY, 
                          args   = MineArgs(hash=hash, nonce=nonce))
            ixList = []
            ixList.append(ComputeBudgetIx())
            ixList.append(ComputePriceIx(self.PRIORITY_FEE))
            ixList.append(ixMine)

            tx: SapysolTx = SapysolTx(connection=self.CONNECTION, payer=self.SIGNER)
            tx.FromInstructionsLegacy(ixList).Sign()
            result = tx.SendAndWait(self.CONN_OVERRIDE)

            # Reset nonce only if it is a success
            if result == SapysolTxStatus.SUCCESS:
                self.ACCOUNTS.UpdateNonce(nonce=0)

            # No matter what result is we recorded last (successfull) nonce and will retry
            # with refetching all accounts. See, because Solana is congested we can get TIMEOUT
            # but transaction may actually succeed. By returning here we ensure that we retry the 
            # nonce at least once.

        except KeyboardInterrupt:
            quit()
        except SolanaRpcException:
            print("RPC Exception...")
        except:
            pass

    # ========================================
    #
    def Mine(self):
        while True:
            try:
                result = self.Register()
                if result == True:
                    break
            except KeyboardInterrupt:
                quit()
            except:
                raise
        while True:
            try:
                self.MineSingleTry()
            except KeyboardInterrupt:
                quit()
            except SolanaRpcException:
                print("RPC Exception...")
            except:
                raise

    # ========================================
    #
    def GetRewards(self) -> None:
        pass

    # ========================================
    #
    def GetBalance(self) -> None:
        pass

    # ========================================
    #
    def Claim(self) -> None:
        minerAta = GetOrCreateAtaIx(connection = self.CONNECTION,
                                    tokenMint  = ORE_MINT_ADDRESS,
                                    owner      = self.SIGNER.pubkey())
        claimAccounts: ClaimAccounts = ClaimAccounts(signer          = self.SIGNER.pubkey(),
                                                     beneficiary     = minerAta.pubkey,
                                                     mint            = ORE_MINT_ADDRESS,
                                                     proof           = self.ACCOUNTS.PROOF_PUBKEY,
                                                     treasury        = TREASURY_ADDRESS,
                                                     treasury_tokens = TREASURY_TOKEN_ATA)

        self.ACCOUNTS.FetchState()
        while True:
            self.ACCOUNTS.FetchState()
            if self.ACCOUNTS.PROOF.claimable_rewards <= 0:
                break

            try:
                ixClaim = claim(signer = self.SIGNER.pubkey(), 
                            accounts = claimAccounts,
                            amount   = self.ACCOUNTS.PROOF.claimable_rewards)
                ixList: List[Instruction] = []
                ixList.append(ComputeBudgetIx())
                ixList.append(ComputePriceIx(self.PRIORITY_FEE))
                if minerAta.ix:
                    ixList.append(minerAta.ix)
                ixList.append(ixClaim)

                tx: SapysolTx = SapysolTx(connection=self.CONNECTION, payer=self.SIGNER)
                tx.FromInstructionsLegacy(ixList).Sign()
                result = tx.SendAndWait(self.CONN_OVERRIDE)

            except KeyboardInterrupt:
                quit()
            except SolanaRpcException:
                print("RPC Exception...")
            except:
                pass

    # ========================================
    #
    def GetCorrectBus(self, rewardRate: int):
        # Buses were already fetched
        for i in range(len(self.ACCOUNTS.BUSES)):
            if self.ACCOUNTS.BUSES[i].rewards > (rewardRate * 4):
                return self.ACCOUNTS.BUSES[i], BUS_ADDRESSES[i]

# ================================================================================
#
