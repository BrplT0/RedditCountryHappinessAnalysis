import configparser
import os

_config = None

def load_config(path="../../data/config/config.ini"):
    global _config
    if _config is None:
        config = configparser.ConfigParser()
        if not os.path.exists(path):
            raise FileNotFoundError(f"Config not found: {path}")
        config.read(path)
        _config = config
    return _config

def get_config(section, key, fallback=None, type=str):
    """
    Read a config value.
    section: name of the [section]
    key: setting key
    fallback: default value if the key is not found
    type: str, int, bool, or float for type conversion
    """
    config = load_config()
    if type == int:
        return config.getint(section, key, fallback=fallback)
    elif type == bool:
        return config.getboolean(section, key, fallback=fallback)
    elif type == float:
        return config.getfloat(section, key, fallback=fallback)
    else:
        return config.get(section, key, fallback=fallback)