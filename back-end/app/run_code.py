import docker
from docker.errors import ContainerError
import os
from pathlib import Path

def run_code(filename: str, directory_path: str = "./app/sandbox"):
    client = docker.from_env()
    code_path = Path(directory_path).resolve()

    # Check that the file exists
    target_file = code_path / filename
    if not target_file.exists():
        return f"File not found: {target_file}"

    try:
        # Run Docker container
        output = client.containers.run(
            image="python:3.10-slim",
            command=f"python3 /code/{filename}",
            volumes={str(code_path): {"bind": "/code", "mode": "ro"}},
            network_mode="none",         # no network access
            mem_limit="128m",            # memory cap
            cpu_period=100000,           # limit to 0.5 CPU
            cpu_quota=50000,
            user="1000:1000",            # run as non-root
            stderr=True,
            stdout=True,
            remove=True
        )
        return output.decode()
    except ContainerError as e:
        stderr = e.stderr
        if stderr is not None and isinstance(stderr, bytes):
            stderr = stderr.decode()
        return f"[Runtime Error]\n{stderr}"
    except Exception as e:
        return f"[System Error] {e}"
