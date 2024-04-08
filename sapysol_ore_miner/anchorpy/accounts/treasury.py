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
class TreasuryJSON(typing.TypedDict):
    admin:                 str
    bump:                  int
    difficulty:            list[int]
    last_reset_at:         int
    reward_rate:           int
    total_claimed_rewards: int

# ================================================================================
#
@dataclass
class Treasury:
    discriminator: typing.ClassVar = b"f\x00\x00\x00\x00\x00\x00\x00"
    layout: typing.ClassVar = borsh.CStruct(
        "admin"                 / BorshPubkey,
        "bump"                  / borsh.U64,
        "difficulty"            / borsh.U8[32],
        "last_reset_at"         / borsh.I64,
        "reward_rate"           / borsh.U64,
        "total_claimed_rewards" / borsh.U64,
    )
    admin:                 Pubkey
    bump:                  int
    difficulty:            list[int]
    last_reset_at:         int
    reward_rate:           int
    total_claimed_rewards: int

    # ========================================
    #
    @classmethod
    def fetch(cls,
              conn:       Client,
              address:    Pubkey,
              commitment: typing.Optional[Commitment] = None,
              program_id: Pubkey = PROGRAM_ID) -> typing.Optional["Treasury"]:

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
                       program_id: Pubkey = PROGRAM_ID) -> typing.List[typing.Optional["Treasury"]]:

        entries = FetchAccounts(connection   = conn, 
                                pubkeys      = addresses,
                                requiredOwner= program_id,
                                commitment   = commitment)
        return [ Treasury.decode(entry.data) if entry else None for entry in entries ]

    # ========================================
    #
    @classmethod
    def decode(cls, data: bytes) -> "Treasury":
        if data[:ACCOUNT_DISCRIMINATOR_SIZE] != cls.discriminator:
            raise AccountInvalidDiscriminator("The discriminator for this account is invalid")
        dec = Treasury.layout.parse(data[ACCOUNT_DISCRIMINATOR_SIZE:])
        return cls(admin                 = dec.admin,
                   bump                  = dec.bump,
                   difficulty            = dec.difficulty,
                   last_reset_at         = dec.last_reset_at,
                   reward_rate           = dec.reward_rate,
                   total_claimed_rewards = dec.total_claimed_rewards)

    # ========================================
    #
    def to_json(self) -> TreasuryJSON:
        return {
            "admin":             str(self.admin),
            "bump":                  self.bump,
            "difficulty":            self.difficulty,
            "last_reset_at":         self.last_reset_at,
            "reward_rate":           self.reward_rate,
            "total_claimed_rewards": self.total_claimed_rewards,
        }

    # ========================================
    #
    @classmethod
    def from_json(cls, obj: TreasuryJSON) -> "Treasury":
        return cls(admin      = MakePubkey(obj["admin"]),
                   bump                  = obj["bump"],
                   difficulty            = obj["difficulty"],
                   last_reset_at         = obj["last_reset_at"],
                   reward_rate           = obj["reward_rate"],
                   total_claimed_rewards = obj["total_claimed_rewards"])

# ================================================================================
#
