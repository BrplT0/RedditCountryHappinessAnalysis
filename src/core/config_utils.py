import configparser
import os

_config = None

def load_config(path=None):
    global _config
    if _config is None:
        config = configparser.ConfigParser()
        if path is None:
            base_dir = os.path.dirname(os.path.abspath(__file__))
            path = os.path.join(base_dir, "..", "..", "data", "config", "config.ini")

        path = os.path.abspath(path)
        if not os.path.exists(path):
            raise FileNotFoundError(f"Config not found: {path}")

        config.read(path)
        _config = config

    return _config

def get_config(section, key, fallback=None, type=str, path=None):
    config = load_config(path)
    if type == int:
        return config.getint(section, key, fallback=fallback)
    elif type == bool:
        return config.getboolean(section, key, fallback=fallback)
    elif type == float:
        return config.getfloat(section, key, fallback=fallback)
    else:
        return config.get(section, key, fallback=fallback)
