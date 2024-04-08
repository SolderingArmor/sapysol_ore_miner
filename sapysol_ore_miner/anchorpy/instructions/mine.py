# ================================================================================
#
from  __future__ import annotations
import  typing
from    solders.pubkey         import Pubkey
from    solders.instruction    import Instruction, AccountMeta
from    sapysol                import MakePubkey
from    construct              import Construct
import  borsh_construct        as borsh
from    sapysol.ix             import get_associated_token_address
from    sapysol.helpers        import SYSVAR_SLOT_HASHES_PUBKEY
from  ..program_id             import PROGRAM_ID
from ...constants import *

# ================================================================================
#
class MineArgs(typing.TypedDict):
    hash:  bytes
    nonce: int

# ================================================================================
#
layout = borsh.CStruct(
    "hash"  / borsh.U8[32],
    "nonce" / borsh.U64,
)

# ================================================================================
#
def mine(signer: Pubkey,
         bus:    Pubkey,
         proof:  Pubkey,
         args:   MineArgs,
         program_id:  Pubkey = PROGRAM_ID,
         treasury_id: Pubkey = TREASURY_ADDRESS,
         remaining_accounts: typing.Optional[typing.List[AccountMeta]] = None,
) -> Instruction:
    keys: list[AccountMeta] = [
        AccountMeta(pubkey=signer,                    is_signer=True, is_writable=False),
        AccountMeta(pubkey=bus,                       is_signer=False, is_writable=True),
        AccountMeta(pubkey=proof,                     is_signer=False, is_writable=True),
        AccountMeta(pubkey=treasury_id,               is_signer=False, is_writable=False),
        AccountMeta(pubkey=SYSVAR_SLOT_HASHES_PUBKEY, is_signer=False, is_writable=False),
    ]
    if remaining_accounts is not None:
        keys += remaining_accounts
    identifier = b"\x02"
    #encoded_args = hash + nonce.to_bytes(8, "little")
    encoded_args = layout.build({
        "hash":  args["hash"],
        "nonce": args["nonce"],
    })
    data = identifier + encoded_args
    return Instruction(program_id, data, keys)

# ================================================================================
#
