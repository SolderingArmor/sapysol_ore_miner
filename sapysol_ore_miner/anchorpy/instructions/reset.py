# ================================================================================
#
from  __future__ import annotations
import  typing
from    solders.pubkey      import Pubkey
from    spl.token.constants import TOKEN_PROGRAM_ID
from    solders.instruction import Instruction, AccountMeta
from  ..program_id          import PROGRAM_ID
from ...constants           import *
from    sapysol             import MakePubkey

# ================================================================================
#
def reset(signer:     Pubkey,
          program_id: Pubkey = PROGRAM_ID,
          remaining_accounts: typing.Optional[typing.List[AccountMeta]] = None) -> Instruction:

    keys: list[AccountMeta] = [
        AccountMeta(pubkey=MakePubkey(signer), is_signer=True,  is_writable=False),
        AccountMeta(pubkey=BUS_ADDRESSES[0],   is_signer=False, is_writable=True ),
        AccountMeta(pubkey=BUS_ADDRESSES[1],   is_signer=False, is_writable=True ),
        AccountMeta(pubkey=BUS_ADDRESSES[2],   is_signer=False, is_writable=True ),
        AccountMeta(pubkey=BUS_ADDRESSES[3],   is_signer=False, is_writable=True ),
        AccountMeta(pubkey=BUS_ADDRESSES[4],   is_signer=False, is_writable=True ),
        AccountMeta(pubkey=BUS_ADDRESSES[5],   is_signer=False, is_writable=True ),
        AccountMeta(pubkey=BUS_ADDRESSES[6],   is_signer=False, is_writable=True ),
        AccountMeta(pubkey=BUS_ADDRESSES[7],   is_signer=False, is_writable=True ),
        AccountMeta(pubkey=ORE_MINT_ADDRESS,   is_signer=False, is_writable=True ),
        AccountMeta(pubkey=TREASURY_ADDRESS,   is_signer=False, is_writable=True ),
        AccountMeta(pubkey=TREASURY_TOKEN_ATA, is_signer=False, is_writable=True ),
        AccountMeta(pubkey=TOKEN_PROGRAM_ID,   is_signer=False, is_writable=False),
    ]
    if remaining_accounts is not None:
        keys += remaining_accounts
    identifier   = b"\x00"
    encoded_args = b""
    data         = identifier + encoded_args
    return Instruction(program_id, data, keys)

# ================================================================================
#
