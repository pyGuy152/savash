from typing import List
import docker
from docker.errors import ContainerError
from pathlib import Path

def run_code(filename: str, stdin_data: List[str] = [""], directory_path: str = "./app/sandbox"):
    stdin_data = stdin_data
    client = docker.from_env()
    code_path = Path(directory_path).resolve()
    target_file = code_path / filename

    if not target_file.exists():
        return f"File not found: {target_file}"

    try:
        container = client.containers.create(
            image="python:3.10-slim",
            command=f"python3 /code/{filename}",
            volumes={str(code_path): {"bind": "/code", "mode": "ro"}},
            network_mode="none",
            mem_limit="128m",
            cpu_period=100000,
            cpu_quota=50000,
            user="1000:1000",
            stdin_open=True,
            tty=False,
            detach=True
        )

        container.start()

        socket = container.attach_socket(params={'stdin': 1, 'stream': 1})
        for i in stdin_data:
            socket._sock.send(i.encode())
            socket._sock.sendall(b"\n")

        socket._sock.shutdown(1)

        exit_status = container.wait(timeout=60)

        output = container.logs(stdout=True, stderr=True).decode()

        container.remove()
        return output

    except ContainerError as e:
        stderr = e.stderr
        if stderr is not None and isinstance(stderr, bytes):
            stderr = stderr.decode()
        return f"[Runtime Error]\n{stderr}"
    except Exception as e:
        return f"[System Error] {e}"
