# ================================================================================
#
from __future__ import annotations
import typing
from   solders.pubkey      import Pubkey
from   spl.token.constants import TOKEN_PROGRAM_ID
from   solders.instruction import Instruction, AccountMeta
from   construct           import Construct
import borsh_construct     as borsh
from ..program_id          import PROGRAM_ID

# ================================================================================
#
class ClaimAccounts(typing.TypedDict):
    signer:          Pubkey
    beneficiary:     Pubkey
    mint:            Pubkey
    proof:           Pubkey
    treasury:        Pubkey
    treasury_tokens: Pubkey

class ClaimArgs(typing.TypedDict):
    amount: int

# ================================================================================
#
layout = borsh.CStruct(
    "amount" / borsh.U64,
)

# ================================================================================
#
def claim(accounts:           ClaimAccounts,
          amount:             int,
          program_id:         Pubkey = PROGRAM_ID,
          remaining_accounts: typing.Optional[typing.List[AccountMeta]] = None) -> Instruction:

    keys: list[AccountMeta] = [
        AccountMeta(pubkey=accounts["signer"],          is_signer=True,  is_writable=False),
        AccountMeta(pubkey=accounts["beneficiary"],     is_signer=False, is_writable=True ),
        AccountMeta(pubkey=accounts["mint"],            is_signer=False, is_writable=False),
        AccountMeta(pubkey=accounts["proof"],           is_signer=False, is_writable=True ),
        AccountMeta(pubkey=accounts["treasury"],        is_signer=False, is_writable=True ),
        AccountMeta(pubkey=accounts["treasury_tokens"], is_signer=False, is_writable=True ),
        AccountMeta(pubkey=TOKEN_PROGRAM_ID,            is_signer=False, is_writable=False),
    ]
    if remaining_accounts is not None:
        keys += remaining_accounts
    identifier   = b"\x03"
    encoded_args = layout.build({
        "amount": amount,
    })
    data = identifier + encoded_args
    return Instruction(program_id, data, keys)

# ================================================================================
#
