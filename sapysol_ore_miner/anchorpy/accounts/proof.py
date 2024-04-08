# ================================================================================
#
import typing
from   dataclasses              import dataclass
from   solders.pubkey           import Pubkey
from   solana.rpc.api           import Client
from   solana.rpc.commitment    import Commitment
import borsh_construct          as borsh
from   anchorpy.coder.accounts  import ACCOUNT_DISCRIMINATOR_SIZE
from   anchorpy.error           import AccountInvalidDiscriminator
from   anchorpy.utils.rpc       import get_multiple_accounts
from   anchorpy.borsh_extension import BorshPubkey
from ..program_id               import PROGRAM_ID
from   sapysol                  import FetchAccount, FetchAccounts, MakePubkey

# ================================================================================
#
class ProofJSON(typing.TypedDict):
    authority:         str
    claimable_rewards: int
    hash:              list[int]
    total_hashes:      int
    total_rewards:     int

# ================================================================================
#
@dataclass
class Proof:
    discriminator: typing.ClassVar = b"e\x00\x00\x00\x00\x00\x00\x00"
    layout: typing.ClassVar = borsh.CStruct(
        "authority"         / BorshPubkey,
        "claimable_rewards" / borsh.U64,
        "hash"              / borsh.U8[32],
        "total_hashes"      / borsh.U64,
        "total_rewards"     / borsh.U64,
    )
    authority:         Pubkey
    claimable_rewards: int
    hash:              list[int]
    total_hashes:      int
    total_rewards:     int

    # ========================================
    #
    @classmethod
    def fetch(cls,
              conn:       Client,
              address:    Pubkey,
              commitment: typing.Optional[Commitment] = None,
              program_id: Pubkey = PROGRAM_ID) -> typing.Optional["Proof"]:

        resp = FetchAccount(connection    = conn, 
                            pubkey        = address,
                            requiredOwner = program_id,
                            commitment    = commitment)
        return None if resp is None else cls.decode(resp.data)

    # ========================================
    #
    @classmethod
    def fetch_multiple(cls,
                       conn:       Client,
                       addresses:  list[Pubkey],
                       commitment: typing.Optional[Commitment] = None,
                       program_id: Pubkey = PROGRAM_ID) -> typing.List[typing.Optional["Proof"]]:

        entries = FetchAccounts(connection   = conn, 
                                pubkeys      = addresses,
                                requiredOwner= program_id,
                                commitment   = commitment)
        return [ Proof.decode(entry.data) if entry else None for entry in entries ]

    # ========================================
    #
    @classmethod
    def decode(cls, data: bytes) -> "Proof":
        if data[:ACCOUNT_DISCRIMINATOR_SIZE] != cls.discriminator:
            raise AccountInvalidDiscriminator("The discriminator for this account is invalid")
        dec = Proof.layout.parse(data[ACCOUNT_DISCRIMINATOR_SIZE:])
        return cls(authority         = dec.authority,
                   claimable_rewards = dec.claimable_rewards,
                   hash              = dec.hash,
                   total_hashes      = dec.total_hashes,
                   total_rewards     = dec.total_rewards)

    # ========================================
    #
    def to_json(self) -> ProofJSON:
        return {
            "authority":     str(self.authority),
            "claimable_rewards": self.claimable_rewards,
            "hash":              self.hash,
            "total_hashes":      self.total_hashes,
            "total_rewards":     self.total_rewards,
        }

    # ========================================
    #
    @classmethod
    def from_json(cls, obj: ProofJSON) -> "Proof":
        return cls(authority         = MakePubkey(obj["authority"]),
                   claimable_rewards = obj["claimable_rewards"],
                   hash              = obj["hash"],
                   total_hashes      = obj["total_hashes"],
                   total_rewards     = obj["total_rewards"])

# ================================================================================
#
