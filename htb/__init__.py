from pathlib import Path

ROOT_DIR = Path(__file__).parent.parent
STORAGE_DIR = ROOT_DIR / "storage"

if not STORAGE_DIR.exists():
    STORAGE_DIR.mkdir(exist_ok=True)
