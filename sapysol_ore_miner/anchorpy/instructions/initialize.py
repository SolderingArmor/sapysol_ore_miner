# ================================================================================
#
from __future__ import annotations
import typing
from   solders.pubkey         import Pubkey
from   solders.system_program import ID as SYS_PROGRAM_ID
from   solders.sysvar         import RENT
from   construct              import Construct
import borsh_construct        as borsh
from   spl.token.constants    import TOKEN_PROGRAM_ID, ASSOCIATED_TOKEN_PROGRAM_ID
from   solders.instruction    import Instruction, AccountMeta
from ..program_id             import PROGRAM_ID

# ================================================================================
#
# TODO: NOT IMPLEMENTED, LAYOUT/ARGS ARE WRONG
#
# ================================================================================
#
class InitializeAccounts(typing.TypedDict):
    ore_program:     Pubkey
    admin:           Pubkey
    bus0:            Pubkey
    bus1:            Pubkey
    bus2:            Pubkey
    bus3:            Pubkey
    bus4:            Pubkey
    bus5:            Pubkey
    bus6:            Pubkey
    bus7:            Pubkey
    mint:            Pubkey
    treasury:        Pubkey
    treasury_tokens: Pubkey

# ================================================================================
#
class InitializeArgs(typing.TypedDict):
    hash:  bytes
    nonce: int

# ================================================================================
#
layout = borsh.CStruct(
    "bus_0_bump"    / borsh.U8,
    "bus_1_bump"    / borsh.U8,
    "bus_2_bump"    / borsh.U8,
    "bus_3_bump"    / borsh.U8,
    "bus_4_bump"    / borsh.U8,
    "bus_5_bump"    / borsh.U8,
    "bus_6_bump"    / borsh.U8,
    "bus_7_bump"    / borsh.U8,
    "metadata_bump" / borsh.U8,
    "mint_bump"     / borsh.U8,
    "treasury_bump" / borsh.U8,
)
# ================================================================================
#
def initialize(accounts:           InitializeAccounts,
               program_id:         Pubkey = PROGRAM_ID,
               remaining_accounts: typing.Optional[typing.List[AccountMeta]] = None) -> Instruction:

    keys: list[AccountMeta] = [
        AccountMeta(pubkey=accounts["ore_program"],     is_signer=False, is_writable=False),
        AccountMeta(pubkey=accounts["admin"],           is_signer=True,  is_writable=False),
        AccountMeta(pubkey=accounts["bus0"],            is_signer=False, is_writable=True ),
        AccountMeta(pubkey=accounts["bus1"],            is_signer=False, is_writable=True ),
        AccountMeta(pubkey=accounts["bus2"],            is_signer=False, is_writable=True ),
        AccountMeta(pubkey=accounts["bus3"],            is_signer=False, is_writable=True ),
        AccountMeta(pubkey=accounts["bus4"],            is_signer=False, is_writable=True ),
        AccountMeta(pubkey=accounts["bus5"],            is_signer=False, is_writable=True ),
        AccountMeta(pubkey=accounts["bus6"],            is_signer=False, is_writable=True ),
        AccountMeta(pubkey=accounts["bus7"],            is_signer=False, is_writable=True ),
        AccountMeta(pubkey=accounts["mint"],            is_signer=False, is_writable=False),
        AccountMeta(pubkey=accounts["treasury"],        is_signer=False, is_writable=False),
        AccountMeta(pubkey=accounts["treasury_tokens"], is_signer=False, is_writable=True ),
        AccountMeta(pubkey=SYS_PROGRAM_ID,              is_signer=False, is_writable=False),
        AccountMeta(pubkey=TOKEN_PROGRAM_ID,            is_signer=False, is_writable=False),
        AccountMeta(pubkey=ASSOCIATED_TOKEN_PROGRAM_ID, is_signer=False, is_writable=False),
        AccountMeta(pubkey=RENT,                        is_signer=False, is_writable=False),
    ]
    if remaining_accounts is not None:
        keys += remaining_accounts
    identifier   = b"\x64"
    encoded_args = b""
    data         = identifier + encoded_args
    return Instruction(program_id, data, keys)

# ================================================================================
#
