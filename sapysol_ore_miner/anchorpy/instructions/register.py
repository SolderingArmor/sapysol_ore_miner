# ================================================================================
#
from __future__ import annotations
import typing
from   solders.pubkey         import Pubkey
from   solders.system_program import ID as SYS_PROGRAM_ID
from   solders.instruction    import Instruction, AccountMeta
from ..program_id             import PROGRAM_ID

# ================================================================================
#
class RegisterAccounts(typing.TypedDict):
    ore_program: Pubkey
    signer:      Pubkey
    proof:       Pubkey

# ================================================================================
#
def register(accounts:   RegisterAccounts,
             seed:       int,
             program_id: Pubkey = PROGRAM_ID,
             remaining_accounts: typing.Optional[typing.List[AccountMeta]] = None) -> Instruction:

    keys: list[AccountMeta] = [
        AccountMeta(pubkey=accounts["ore_program"], is_signer=False, is_writable=False),
        AccountMeta(pubkey=accounts["signer"],      is_signer=True,  is_writable=False),
        AccountMeta(pubkey=accounts["proof"],       is_signer=False, is_writable=True ),
        AccountMeta(pubkey=SYS_PROGRAM_ID,          is_signer=False, is_writable=False),
    ]
    if remaining_accounts is not None:
        keys += remaining_accounts
    identifier   = b"\x01"
    encoded_args = seed.to_bytes()
    data         = identifier + encoded_args
    return Instruction(program_id, data, keys)

# ================================================================================
#
