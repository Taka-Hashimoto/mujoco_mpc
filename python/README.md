# MuJoCo MPC Python API

This directory contains the Python API for MuJoCo MPC (MJPC).

## Quick Start with uv

[uv](https://docs.astral.sh/uv/) is the recommended way to manage Python dependencies for MJPC.

### Install uv
```sh
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### Install and run

#### Quick setup (one command)
```sh
# One-command setup (after building MJPC)
uv run python setup_uv.py
```

#### Manual setup
```sh
# Install dependencies and create virtual environment
uv sync --extra dev

# Generate protobuf files (required before first run)
uv run python generate_proto.py

# Copy agent server binaries and task assets (required for agent functionality)
uv run python copy_binaries.py

# Test the installation
uv run python mujoco_mpc/agent_test.py

# Run demos
uv run python mujoco_mpc/demos/agent/cartpole_gui.py
```

### Development workflow
```sh
# Add new dependencies
uv add numpy  # for runtime dependencies
uv add pytest --dev  # for development dependencies

# Run tests
uv run python -m pytest

# Run with specific Python version
uv python install 3.11
uv sync --python 3.11
```

## Requirements

- Python 3.10+
- Built MJPC C++ library (see main README.md)
- The following Python packages are automatically installed:
  - mujoco >= 3.1.1
  - brax
  - grpcio
  - matplotlib
  - mediapy
  - mujoco-mjx
  - protobuf

## Traditional Installation

If you prefer using pip/conda, see the main README.md for instructions. 