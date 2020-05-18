from .configReader import ConfigReader

config = ConfigReader.config()
SERVER = config.server


def get_server_host(key):
    front = getattr(config, key)
    if front.endswith("/"):
        return front + SERVER + "/"
    return front + "/" + SERVER + "/"
