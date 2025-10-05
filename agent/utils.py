import re
import os
from .config import AUTO_CONFIRM, PROJECT_ROOT

DANGEROUS_PATTERNS = [
    r"\brm\s+-rf\b",
    r"\brm\s+-r\b",
    r"\bshutdown\b",
    r"\breboot\b",
    r"\binit\s+0\b",
    r"\bmkfs\b",
    r"\b:>\s*/dev\b",
    r"\bchmod\s+777\b",
    r"\bchown\b",
    r"\bkill\b",
]

def is_dangerous(cmd: str) -> bool:
    s = cmd.lower()
    for p in DANGEROUS_PATTERNS:
        if re.search(p, s):
            return True
    return False

def confirm_command(cmd: str) -> bool:
    """If AUTO_CONFIRM is True, accept; otherwise ask the user for confirmation (stdin)."""
    if AUTO_CONFIRM:
        print("⚠️ AUTO_CONFIRM is enabled: allowing potentially dangerous command.")
        return True
    if not is_dangerous(cmd):
        return True
    # For dangerous commands ask user:
    print("⚠️ دستور شناسایی شد که می‌تواند خطرناک باشد:", cmd)
    ans = input("آیا مطمئنی می‌خوای اجرا بشه؟ (yes/NO): ").strip().lower()
    return ans in ("y", "yes")

def safe_write_file(rel_path: str, content: str) -> str:
    """Write a file inside PROJECT_ROOT only. Returns the absolute path written."""
    base = os.path.abspath(PROJECT_ROOT)
    target = os.path.abspath(os.path.join(base, rel_path))
    if not target.startswith(base):
        raise ValueError("File write outside project root is not allowed.")
    parent = os.path.dirname(target)
    if parent and not os.path.exists(parent):
        os.makedirs(parent, exist_ok=True)
    with open(target, "w", encoding="utf-8") as f:
        f.write(content)
    return target
