#!/usr/bin/env python3
"""Generate protobuf files for MJPC Python API."""

import pathlib
import shutil
import subprocess
import sys

Path = pathlib.Path


def generate_proto_files():
    """Generate agent_pb2{_grpc}.py files from agent.proto."""
    try:
        from grpc_tools import protoc
    except ImportError:
        print("Error: grpcio-tools is required. Install with: uv add grpcio-tools --dev")
        sys.exit(1)

    agent_proto_filename = "agent.proto"
    agent_proto_source_path = Path("..", "mjpc", "grpc", agent_proto_filename).resolve()
    
    if not agent_proto_source_path.exists():
        print(f"Error: {agent_proto_source_path} not found. Make sure you're in the python directory and MJPC is built.")
        sys.exit(1)
    
    # Create proto directory
    proto_dir = Path("mujoco_mpc", "proto")
    proto_dir.mkdir(parents=True, exist_ok=True)
    
    # Copy agent.proto to proto directory
    agent_proto_destination_path = proto_dir / agent_proto_filename
    shutil.copy(agent_proto_source_path, agent_proto_destination_path)
    
    # Generate __init__.py
    (proto_dir / "__init__.py").touch()
    
    protoc_command_parts = [
        __file__,
        f"-I{Path.cwd()}",
        f"--python_out={Path.cwd()}",
        f"--grpc_python_out={Path.cwd()}",
        str(agent_proto_destination_path),
    ]
    
    print("Generating protobuf files...")
    print(f"Command: {' '.join(protoc_command_parts)}")
    
    protoc_returncode = protoc.main(protoc_command_parts)
    
    if protoc_returncode != 0:
        print(f"Error: protoc failed with return code {protoc_returncode}")
        sys.exit(1)
    
    print("Successfully generated protobuf files:")
    print(f"  - {proto_dir}/agent_pb2.py")
    print(f"  - {proto_dir}/agent_pb2_grpc.py")


if __name__ == "__main__":
    generate_proto_files() 