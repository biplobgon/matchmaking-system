from __future__ import annotations

from pathlib import Path
from urllib.request import urlretrieve

from matchmaking_system.data import DATA_URL, RAW_DATA_PATH


def main() -> None:
    RAW_DATA_PATH.parent.mkdir(parents=True, exist_ok=True)
    if RAW_DATA_PATH.exists():
        print(f"Dataset already exists: {RAW_DATA_PATH}")
        return

    print(f"Downloading {DATA_URL}")
    urlretrieve(DATA_URL, RAW_DATA_PATH)
    print(f"Wrote {Path(RAW_DATA_PATH).resolve()}")


if __name__ == "__main__":
    main()
