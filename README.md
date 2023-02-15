---
# biokit

[![codecov](https://codecov.io/gh/weslleylc/biokit/branch/main/graph/badge.svg?token=biokit_token_here)](https://codecov.io/gh/weslleylc/biokit)
[![CI](https://github.com/weslleylc/biokit/actions/workflows/main.yml/badge.svg)](https://github.com/weslleylc/biokit/actions/workflows/main.yml)

Awesome biokit created by weslleylc

## Install it from PyPI

```bash
pip install biokit
```

## Usage

```py
import neurokit2 as nk
from biokit.features.ecg.quality import compute_zhao

sampling_rate=1000
ecg = nk.ecg_simulate(duration=15, sampling_rate=1000, heart_rate=80)
zhao_features = compute_zhao(ecg, sampling_rate)

```

```bash
$ python -m biokit
#or
$ biokit
```

## Development

Read the [CONTRIBUTING.md](CONTRIBUTING.md) file.
