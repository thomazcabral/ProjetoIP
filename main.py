from engine import Engine
from config import global_config

def main():

    engine = Engine(global_config)
    engine.run()

if __name__ == '__main__':
    main()