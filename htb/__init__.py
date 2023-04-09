from pathlib import Path

STORAGE_DIR = Path.home() / ".htb"

if not STORAGE_DIR.exists():
    STORAGE_DIR.mkdir(exist_ok=True)
