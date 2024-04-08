# ================================================================================
#
from  solders.pubkey import Pubkey
from  typing         import List, Tuple
from .constants      import *

# ================================================================================
#
def DeriveProof(authority: Pubkey) -> Tuple[Pubkey, int]:
    return Pubkey.find_program_address(seeds=[b"proof", bytes(authority)], program_id=ORE_PROGRAM_ID)

def DeriveProofAddress(authority: Pubkey) -> Pubkey:
    return DeriveProof(authority)[0]

def DeriveProofBump(authority: Pubkey) -> int:
    return DeriveProof(authority)[1]

# ================================================================================
#
def DeriveBus(index: int) -> Tuple[Pubkey, int]:
    return Pubkey.find_program_address(seeds=[b"bus", bytes([index])], program_id=ORE_PROGRAM_ID)

def DeriveBusAddress(index: int) -> Pubkey:
    return DeriveBus(index)[0]

def DeriveBusBump(index: int) -> int:
    return DeriveBus(index)[1]

# ================================================================================
#
    