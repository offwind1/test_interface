from .configReader import ConfigReader

config = ConfigReader.config()
USER_SERVER = config.use_server
SERVER = config.server


def get_server_host(key):
    front = getattr(config, key)
    if not front.endswith("/"):
        front = front + "/"

    if USER_SERVER:
        return front + SERVER + "/"

    return front
