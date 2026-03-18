# Workspace restriction
from pathlib import Path

BASE_DIR = Path("./workspace").resolve()
BASE_DIR.mkdir(exist_ok=True)

def safe_path(user_path: str) -> Path:
    """Prevent path traversal attacks"""
    resolved = (BASE_DIR / user_path).resolve()

    if not str(resolved).startswith(str(BASE_DIR)):
        raise ValueError("Access outside workspace is not allowed")

    return resolved

