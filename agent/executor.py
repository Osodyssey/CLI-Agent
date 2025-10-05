import subprocess
import shlex
from typing import Tuple
from .config import SANDBOX

def run_command(cmd: str, timeout: int = 120) -> Tuple[int, str]:
    """Execute a shell command and return (returncode, output).
    If SANDBOX is True, do not execute — only print and return success code 0 with a simulated message.
    """
    print(f"⚙️ اجرای دستور: {cmd}")
    if SANDBOX:
        msg = f"[SANDBOX MODE] would run: {cmd}"
        print(msg)
        return 0, msg
    try:
        # Use shell=False where possible for safety; if the command is complex, we fallback to shell execution.
        # Here we attempt to split with shlex; if it fails, run with shell=True.
        try:
            parts = shlex.split(cmd)
            proc = subprocess.run(parts, capture_output=True, text=True, timeout=timeout)
        except Exception:
            proc = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=timeout)
        output = (proc.stdout or "") + (proc.stderr or "")
        print(output)
        return proc.returncode, output
    except Exception as e:
        return -1, str(e)
