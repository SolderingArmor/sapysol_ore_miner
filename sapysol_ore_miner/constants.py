# ================================================================================
#
from solders.pubkey import Pubkey
from sapysol        import MakePubkey, GetAta
from typing         import List

# ================================================================================
#
EPOCH_DURATION: int = 60

ORE_PROGRAM_ID:     Pubkey = MakePubkey("mineRHF5r6S7HyD9SppBfVMXMavDkJsxwGesEvxZr2A" )
ORE_MINT_ADDRESS:   Pubkey = MakePubkey("oreoN2tQbHXVaZsr3pf66A48miqcBXCDJozganhEJgz" )
METADATA_ADDRESS:   Pubkey = MakePubkey("2nXZSxfjELuRatcoY64yHdFLZFi3mtesxobHmsoU3Dag")
TREASURY_ADDRESS:   Pubkey = MakePubkey("FTap9fv2GPpWGqrLj3o4c9nHH7p36ih7NbSWHnrkQYqa")
TREASURY_TOKEN_ATA: Pubkey = GetAta(owner=TREASURY_ADDRESS, tokenMint=ORE_MINT_ADDRESS)

# ================================================================================
#
BUS_COUNT: int = 8
BUS_ADDRESSES: List[Pubkey] = [
    MakePubkey("9ShaCzHhQNvH8PLfGyrJbB8MeKHrDnuPMLnUDLJ2yMvz"),
    MakePubkey("4Cq8685h9GwsaD5ppPsrtfcsk3fum8f9UP4SPpKSbj2B"),
    MakePubkey("8L1vdGdvU3cPj9tsjJrKVUoBeXYvAzJYhExjTYHZT7h7"),
    MakePubkey("JBdVURCrUiHp4kr7srYtXbB7B4CwurUt1Bfxrxw6EoRY"),
    MakePubkey("DkmVBWJ4CLKb3pPHoSwYC2wRZXKKXLD2Ued5cGNpkWmr"),
    MakePubkey("9uLpj2ZCMqN6Yo1vV6yTkP6dDiTTXmeM5K3915q5CHyh"),
    MakePubkey("EpcfjBs8eQ4unSMdowxyTE8K3vVJ3XUnEr5BEWvSX7RB"),
    MakePubkey("Ay5N9vKS2Tyo2M9u9TFt59N1XbxdW93C7UrFZW3h8sMC"),
]

# ================================================================================
#
