#!/usr/bin/env python3
"""One-command setup script for MJPC Python API with uv."""

import subprocess
import sys
from pathlib import Path


def run_command(cmd, description):
    """Run a command and handle errors."""
    print(f"\n🔧 {description}")
    print(f"Running: {' '.join(cmd)}")
    
    try:
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        if result.stdout:
            print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error: {e}")
        if e.stdout:
            print(f"stdout: {e.stdout}")
        if e.stderr:
            print(f"stderr: {e.stderr}")
        return False


def main():
    """Setup MJPC Python API for uv."""
    print("🚀 Setting up MJPC Python API with uv")
    
    # Check if we're in the python directory
    if not Path("mujoco_mpc").exists():
        print("❌ Error: Please run this script from the python/ directory")
        sys.exit(1)
    
    # Check if MJPC is built
    if not Path("../build/bin/agent_server").exists():
        print("❌ Error: MJPC not built. Please build MJPC first:")
        print("  cd .. && mkdir -p build && cd build")
        print("  cmake .. -DCMAKE_BUILD_TYPE=Release -G Ninja -DMJPC_BUILD_GRPC_SERVICE=ON")
        print("  cmake --build . --config=Release")
        sys.exit(1)
    
    steps = [
        (["uv", "sync", "--extra", "dev"], "Installing Python dependencies"),
        (["uv", "run", "python", "generate_proto.py"], "Generating protobuf files"),
        (["uv", "run", "python", "copy_binaries.py"], "Copying binaries and assets"),
    ]
    
    for cmd, description in steps:
        if not run_command(cmd, description):
            print(f"❌ Setup failed at: {description}")
            sys.exit(1)
    
    print("\n✅ Setup complete! You can now run:")
    print("  uv run python mujoco_mpc/agent_test.py")
    print("  uv run python mujoco_mpc/demos/agent/cartpole_gui.py")


if __name__ == "__main__":
    main() 