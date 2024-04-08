# ================================================================================
#
import typing
from   dataclasses             import dataclass
from   solders.pubkey          import Pubkey
from   solana.rpc.api          import Client
from   solana.rpc.commitment   import Commitment
import borsh_construct         as borsh
from   anchorpy.coder.accounts import ACCOUNT_DISCRIMINATOR_SIZE
from   anchorpy.error          import AccountInvalidDiscriminator
from   anchorpy.utils.rpc      import get_multiple_accounts
from ..program_id              import PROGRAM_ID
from   sapysol                 import FetchAccount, FetchAccounts

# ================================================================================
#
class BusJSON(typing.TypedDict):
    id:      int
    rewards: int

# ================================================================================
#
@dataclass
class Bus:
    discriminator: typing.ClassVar = b"d\x00\x00\x00\x00\x00\x00\x00"
    layout: typing.ClassVar = borsh.CStruct(
        "id"      / borsh.U64,
        "rewards" / borsh.U64
    )
    id:      int
    rewards: int

    # ========================================
    #
    @classmethod
    def fetch(cls,
              conn:       Client,
              address:    Pubkey,
              commitment: typing.Optional[Commitment] = None,
              program_id: Pubkey = PROGRAM_ID) -> typing.Optional["Bus"]:

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
                       program_id: Pubkey = PROGRAM_ID) -> typing.List[typing.Optional["Bus"]]:

        entries = FetchAccounts(connection   = conn, 
                                pubkeys      = addresses,
                                requiredOwner= program_id,
                                commitment   = commitment)
        return [ Bus.decode(entry.data) if entry else None for entry in entries ]

    # ========================================
    #
    @classmethod
    def decode(cls, data: bytes) -> "Bus":
        if data[:ACCOUNT_DISCRIMINATOR_SIZE] != cls.discriminator:
            raise AccountInvalidDiscriminator("The discriminator for this account is invalid")
        dec = Bus.layout.parse(data[ACCOUNT_DISCRIMINATOR_SIZE:])
        return cls(id=dec.id, rewards=dec.rewards)

    # ========================================
    #
    def to_json(self) -> BusJSON:
        return {
            "id":      self.id,
            "rewards": self.rewards,
        }

    # ========================================
    #
    @classmethod
    def from_json(cls, obj: BusJSON) -> "Bus":
        return cls(id=obj["id"], rewards=obj["rewards"])

# ================================================================================
#
