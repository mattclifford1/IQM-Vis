# IQM-Vis — Claude Code Guide

## Project Overview

IQM-Vis (Image Quality Metric Visualisation) is a Python package providing an extendable PyQt6 UI for assessing the effect of image transformations on Image Quality Metrics (IQMs). Version 1.0.2, published in the SoftwareX Journal (https://doi.org/10.1016/j.softx.2025.102225).

## Tech Stack

- Python 3.9+ (including 3.13)
- PyQt6 — UI framework
- PyTorch — deep learning metrics
- OpenCV — image processing
- Pillow — image I/O
- scikit-image — image quality metrics

## Dev Environment Setup

```bash
# Install PDM (once)
pip install pdm

# Install all deps (creates venv, installs package in editable mode)
pdm install -G :all

# Or install specific groups only
pdm install -G test    # testing tools only
pdm install -G docs    # docs tools only
```

## Running Tests

```bash
# Default (configured in pyproject.toml)
pdm run pytest

# Faster with parallel processes
pdm run pytest --numprocesses=auto

# Tests + update coverage/test badges
./dev_resources/scripts/pytest_and_badges.sh
```

**Platform notes:**
- GUI tests require a display — no headless CI support
- Windows: run test files individually (`--forked` is unsupported)
- Linux: use XOrg display server, not Wayland

## Building Docs

```bash
# Requires pandoc: conda install pandoc
./dev_resources/scripts/make_docs.sh
```

Docs are built locally and committed to the repo. The CI workflow deploys pre-built docs to gh-pages — always build docs locally before pushing if you've changed them.

## Key Architecture

| Path | Purpose |
|------|---------|
| `IQM_Vis/ui_wrapper.py` | Public API entry point (`make_UI`, `dataset_holder`) |
| `IQM_Vis/UI/` | PyQt6 UI components |
| `IQM_Vis/metrics/` | Metric implementations (non-perceptual, perceptual, DL-based) |
| `IQM_Vis/transforms/` | Image transformation functions |
| `IQM_Vis/data_handlers/` | `dataset_holder` class |
| `IQM_Vis/utils/` | Image, save, plot, GUI utilities |
| `IQM_Vis/examples/` | Runnable example scripts |
| `tests/` | pytest test suite |
| `dev_resources/` | Dev scripts, requirements, docs source, pics |

## CI/CD

- `.github/workflows/deploy-package-to-PyPi.yml` — auto-publishes to PyPI when version is bumped on a push to main
- `.github/workflows/publish-documentation.yml` — deploys pre-built docs to gh-pages

## Versioning

Bump `IQM_Vis/version.py` to trigger a PyPI release on next push to main.

## Adding Custom Metrics

Implement a callable with signature:
```python
def my_metric(image_reference, image_comparison, **kwargs):
    ...
    return score  # float
```

Register in the metrics dict: `metrics = {'my_metric': my_metric}`

## Adding Custom Transforms

Implement a callable with signature:
```python
def my_transform(image, parameter):
    ...
    return transformed_image
```

Register in the transforms dict: `transformations = {'my_trans': {'function': my_transform, 'min': -1.0, 'max': 1.0}}`


## coding style
always wise clear and consise code.

## documentation
always document features in the relevant README.md files and in code docstrings. Use type hints for clarity.