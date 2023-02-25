from pebbles import Pebbles

def reader(file):
    try:
        with open(file) as f:
            return f.read().split('\n')
    except FileNotFoundError:
        print(f"{file} was not found")


if __name__ == '__main__':
    bot_api = reader('pebbles_api')[0]
    whitelist = reader('pebbles_whitelist')
    
    Pebbles(bot_api, whitelist)
