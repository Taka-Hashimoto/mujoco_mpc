#!/usr/bin/env python3
"""Copy agent server binaries and task assets for MJPC Python API."""

import pathlib
import shutil
import sys

Path = pathlib.Path


def copy_binaries():
    """Copy agent_server and ui_agent_server binaries."""
    build_dir = Path("../build/bin")
    
    if not build_dir.exists():
        print(f"Error: {build_dir.resolve()} not found. Please build MJPC first.")
        sys.exit(1)
    
    mjpc_dir = Path("mujoco_mpc/mjpc")
    mjpc_dir.mkdir(parents=True, exist_ok=True)
    
    binaries = ["agent_server", "ui_agent_server"]
    
    for binary_name in binaries:
        source_path = build_dir / binary_name
        if not source_path.exists():
            print(f"Error: {source_path} not found. Please build MJPC with gRPC service enabled.")
            sys.exit(1)
        
        destination_path = mjpc_dir / binary_name
        print(f"Copying {source_path} -> {destination_path}")
        shutil.copy(source_path, destination_path)
        
        # Make executable
        destination_path.chmod(0o755)
    
    print("Successfully copied server binaries.")


def copy_task_assets():
    """Copy task assets."""
    mjpc_tasks_path = Path("../build/mjpc/tasks")
    
    if not mjpc_tasks_path.exists():
        print(f"Error: {mjpc_tasks_path.resolve()} not found. Please build MJPC first.")
        sys.exit(1)
    
    # Find all asset files
    source_paths = (
        tuple(mjpc_tasks_path.rglob("*.xml"))
        + tuple(mjpc_tasks_path.rglob("*.png"))
        + tuple(mjpc_tasks_path.rglob("*.stl"))
        + tuple(mjpc_tasks_path.rglob("*.obj"))
    )
    
    if not source_paths:
        print(f"Warning: No task assets found in {mjpc_tasks_path}")
        return
    
    destination_dir = Path("mujoco_mpc/mjpc/tasks")
    
    print(f"Copying {len(source_paths)} task assets...")
    
    for source_path in source_paths:
        relative_path = source_path.relative_to(mjpc_tasks_path)
        destination_path = destination_dir / relative_path
        destination_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy(source_path, destination_path)
    
    print(f"Successfully copied task assets to {destination_dir}")


if __name__ == "__main__":
    copy_binaries()
    copy_task_assets() 