import subprocess
import sys
import time
from pathlib import Path

def run_backend():
    backend_dir = Path(__file__).parent / "backend"
    venv_python = backend_dir / ".venv" / "bin" / "python"

    if not venv_python.exists():
        venv_python = backend_dir / ".venv" / "Scripts" / "python.exe"

    if venv_python.exists():
        return subprocess.Popen([str(venv_python), "-m", "fastapi", "dev"], cwd=backend_dir)
    else:
        return subprocess.Popen([sys.executable, "-m", "fastapi", "dev"], cwd=backend_dir)

def run_frontend():
    frontend_dir = Path(__file__).parent / "frontend"
    return subprocess.Popen(["bun", "run", "dev"], cwd=frontend_dir)

def main():
    processes = []

    try:
        backend_process = run_backend()
        processes.append(backend_process)
        print("Backend started")

        time.sleep(2)

        frontend_process = run_frontend()
        processes.append(frontend_process)
        print("Frontend started")

        print("Both servers running. Press Ctrl+C to stop.")

        while True:
            time.sleep(1)
            for process in processes:
                if process.poll() is not None:
                    print("A process died, shutting down")
                    return

    except KeyboardInterrupt:
        print("\nShutting down...")
    finally:
        for process in processes:
            if process.poll() is None:
                process.terminate()
                try:
                    process.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    process.kill()

if __name__ == "__main__":
    main()
