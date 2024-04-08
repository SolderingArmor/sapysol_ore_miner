#!/usr/bin/python
# =============================================================================
# 
from solana.rpc.api          import Client
from sapysol_ore_miner.miner import Miner
from sapysol                 import * 
from threading               import Thread
from typing                  import List
import json

# ================================================================================
#
class MinerManagerConfig:
    def __init__(self, configPath: str):
        self.CONFIG_PATH:   str       = configPath
        self.CONFIG:        dict      = None
        with open(configPath) as f:
            self.CONFIG = json.loads(f.read())

        self.CONNECTION:    str       = self.CONFIG["connection"]
        self.CONN_OVERRIDE: List[str] = self.CONFIG["connection_override"]
        if len(self.CONN_OVERRIDE) == 0:
            self.CONN_OVERRIDE = None
        self.PRIORITY_FEE:  int       = self.CONFIG["priority_fee"]

    def GetMiners(self) -> List[Miner]:
        result: List[Miner] = []
        for minerParams in self.CONFIG["miners"]:
            paramSigner       = MakeKeypair(minerParams["signer"])
            paramConnection   = minerParams["connection"]          if "connection"          in minerParams else self.CONNECTION
            paramConnOverride = minerParams["connection_override"] if "connection_override" in minerParams else self.CONN_OVERRIDE
            paramPriorityFee  = minerParams["priority_fee"]        if "priority_fee"        in minerParams else self.PRIORITY_FEE
            miner = Miner(connection         = Client(paramConnection),
                          signer             = paramSigner,
                          priorityFee        = paramPriorityFee,
                          connectionOverride = paramConnOverride)
            result.append(miner)
        return result

# ================================================================================
#
class MinerManager:
    def __init__(self):
        self.CONFIG:      MinerManagerConfig = None
        self.MINERS_LIST: List[Miner] = []
        self.THREADS:     List[Thread]

    def StartMiners(self, configPath: str):
        self.CONFIG: MinerManagerConfig = MinerManagerConfig(configPath=configPath)
        miner: Miner
        for miner in self.CONFIG.GetMiners():
            self.MINERS_LIST.append(miner)

        for miner in self.MINERS_LIST:
            thr = Thread(target=miner.Mine())
            thr.start()
            self.THREADS.append(thr)

# ================================================================================
#
