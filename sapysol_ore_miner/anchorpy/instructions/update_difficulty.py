# ================================================================================
#
from __future__ import annotations
import typing
from   solders.pubkey      import Pubkey
from   solders.instruction import Instruction, AccountMeta
from ..program_id          import PROGRAM_ID

# ================================================================================
#
# TODO: NOT IMPLEMENTED, LAYOUT/ARGS ARE WRONG
#
# ================================================================================
#
class UpdateDifficultyAccounts(typing.TypedDict):
    ore_program: Pubkey
    treasury:    Pubkey

# ================================================================================
#
def update_difficulty(accounts:   UpdateDifficultyAccounts,
                      program_id: Pubkey = PROGRAM_ID,
                      remaining_accounts: typing.Optional[typing.List[AccountMeta]] = None) -> Instruction:

    keys: list[AccountMeta] = [
        AccountMeta(pubkey=accounts["ore_program"], is_signer=False, is_writable=False),
        AccountMeta(pubkey=accounts["treasury"],    is_signer=False, is_writable=False),
    ]
    if remaining_accounts is not None:
        keys += remaining_accounts
    identifier   = b"\x66"
    encoded_args = b""
    data         = identifier + encoded_args
    return Instruction(program_id, data, keys)

# ================================================================================
#
