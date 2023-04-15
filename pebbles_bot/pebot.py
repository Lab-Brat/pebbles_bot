import sys
import yaml
import os
from pathlib import Path
from .pb_main import Pebbles


def main():
    api_key = os.environ.get("PEBBLES_API_KEY")
    whitelist_ids = os.environ.get("PEBBLES_USER_WHITELIST")

    if not api_key:
        print("Pebbles API key not found")
        sys.exit(0)

    if not whitelist_ids:
        print("Pebbles user whitelist not found")
        sys.exit(0)

    if len(sys.argv) == 1:
        notify = False
    elif "--notify" in sys.argv:
        notify = sys.stdin.read()

    Pebbles(
        api_key=api_key,
        whitelist=whitelist_ids.split(","),
        notify=notify,
    )


if __name__ == "__main__":
    main()
