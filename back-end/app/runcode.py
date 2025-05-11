from fastapi import APIRouter
from pydantic import BaseModel
import uuid
import os
import subprocess

router = APIRouter()

class codeiiiii(BaseModel):
    code: str

@router.post("/run")
async def run_code(code: codeiiiii):

    # Step 1: Write code to a temporary file
    code_id = str(uuid.uuid4())
    temp_dir = f"./temp/{code_id}"
    os.makedirs(temp_dir, exist_ok=True)
    code_path = f"{temp_dir}/code.py"
    with open(code_path, "w") as f:
        f.write(code.code)

    # Step 2: Build a Docker image from that code
    dockerfile_path = f"{temp_dir}/Dockerfile"
    with open(dockerfile_path, "w") as f:
        f.write(f"""
FROM python:3.11-slim
WORKDIR /app
COPY code.py /app/code.py
CMD ["python", "code.py"]
""")

    tag = f"code-runner-{code_id}"
    try:
        subprocess.run(["docker", "build", "-t", tag, temp_dir], check=True)

        # Step 3: Run the container and capture output
        result = subprocess.run(["docker", "run", "--rm", tag], capture_output=True, text=True, timeout=10)

        return {"output": result.stdout or result.stderr}
    except subprocess.CalledProcessError as e:
        return {"error": f"Build or run failed: {e.stderr}"}
    except subprocess.TimeoutExpired:
        return {"error": "Execution timed out"}
    finally:
        subprocess.run(["docker", "rmi", tag])
        os.remove(code_path)
        os.remove(dockerfile_path)
        os.rmdir(temp_dir)
