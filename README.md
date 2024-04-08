# sapysol_ore_miner

`sapysol` Ore miner implementation. Based on [ore](https://github.com/HardhatChad/ore) and [ore-cli](https://github.com/HardhatChad/ore-cli), written from scratch.

What currently works: `register`, `mine`.

WARNING! `claim` currently implemented but not tested!

WARNING! `mine` works with `keccak-256` single thread solving! But you can run unlimited threads of different miners (with different private keys). For that please update `config.json`, check sample in `config.json.sample`

# Installation

```sh
pip install sapysol
```

Note: Requires Python >= 3.11.

# Usage

```py
# ORE mining
from sapysol import *
from sapysol_ore_miner.miner_manager import MinerManager
import time

manager: MinerManager = MinerManager()
manager.StartMiners("config.json")

while True:
    time.sleep(0.1)
```

TODO

# Contributing

TODO

# Tests

TODO

# Contact

[Telegram](https://t.me/sapysol)

Donations: `SAxxD7JGPQWqDihYDfD6mFp7JWz5xGrf9RXmE4BJWTS`

# Disclaimer

### Intended Purpose and Use
The Content is provided solely for educational, informational, and general purposes. It is not intended for use in making any business, investment, or legal decisions. Although every effort has been made to keep the information up-to-date and accurate, no representations or warranties, express or implied, are made regarding the completeness, accuracy, reliability, suitability, or availability of the Content.

### Opinions and Views
The views and opinions expressed herein are those of Anton Platonov and do not necessarily reflect the official policy, position, or views of any other agency, organization, employer, or company. These views are subject to change, revision, and rethinking at any time.

### Third-Party Content and Intellectual Property
Some Content may include or link to third-party materials. The User agrees to respect all applicable intellectual property laws, including copyrights and trademarks, when engaging with this Content.

### Amendments
Chintan Gurjar reserves the right to update or change this disclaimer at any time without notice. Continued use of the Content following modifications to this disclaimer will constitute acceptance of the revised terms.