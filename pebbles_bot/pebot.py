import os
import sys
import yaml
from pathlib import Path
from .pb_main import Pebbles


def config_reader():
    """
    Reads the config file and returns a dictionary
    """
    config = os.environ.get(
        "PEBBLES_CONFIG", f"{str(Path.home())}/pebbles.yaml"
    )

    if Path(config).is_file():
        try:
            with open(config, "r") as config_file:
                return yaml.safe_load(config_file)
        except:
            print(f"Error opening {config}")
            return None
    else:
        print(f"Config file {config} not found")
        return None


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

    pebbles_config = config_reader()
    if pebbles_config:
        whitelist_ids = pebbles_config["whitelist_ids"]

    Pebbles(
        api_key=api_key,
        whitelist=whitelist_ids.split(","),
        notify=notify,
    )


if __name__ == "__main__":
    main()
