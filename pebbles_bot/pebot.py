import sys
import yaml
from pathlib import Path
from .pb_main import Pebbles

config = f"{str(Path.home())}/.pebbles/pebbles.yaml"


def reader():
    if Path(config).is_file():
        try:
            with open(config, "r") as config_file:
                return yaml.safe_load(config_file)
        except:
            print(f"Error opening {config}")
    else:
        Path(f"{str(Path.home())}/.pebbles").mkdir(parents=True, exist_ok=True)
        with open(config, "w") as config_file:
            yaml.dump(
                {"pebbles": {"api_key": "API_KEY", "whitelist": ["USER_ID"]}},
                config_file,
                default_flow_style=False,
            )
        print(
            f"Configuration file template created at {config}\n"
            f"please edit it and consult README for details"
        )


def main():
    read_yaml = reader()
    if read_yaml:
        if len(sys.argv) == 1:
            notify = False
        elif sys.argv[1] == "--notify":
            notify = sys.stdin.read()
        Pebbles(
            read_yaml["pebbles"]["api_key"],
            read_yaml["pebbles"]["whitelist"],
            notify=notify,
        )
    else:
        print("Relaunch the bot after editing the configuration file.")


if __name__ == "__main__":
    main()
