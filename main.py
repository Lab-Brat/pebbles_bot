import yaml
from pathlib import Path
from pebbles import Pebbles

config = f"{str(Path.home())}/pebbles.yaml"


def reader():
    if Path(config).is_file():
        try:
            with open(config, "r") as config_file:
                return yaml.safe_load(config_file)
        except:
            print(f"Error opening {config}")
    else:
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


if __name__ == "__main__":
    read_yaml = reader()
    Pebbles(read_yaml["pebbles"]["api_key"], read_yaml["pebbles"]["whitelist"])
