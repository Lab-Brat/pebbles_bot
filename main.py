from pebbels import Pebbles

if __name__ == '__main__':
    try:
        with open(f"pebbles_api", 'r') as api_key:
            bot_api = api_key.read().strip('\n')
        print("Pebbles has started!")
    except FileNotFoundError:
        print("pebbles_api key file is not in the repo")
        raise SystemExit(0)
    
    pebbles = Pebbles(bot_api)
