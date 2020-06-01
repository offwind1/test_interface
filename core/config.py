from .configReader import ConfigReader

config = ConfigReader.config()
SERVER = config.server


def get_url(reader):
    try:
        return getattr(reader, "url")
    except:
        pass


def get_use_server(reader):
    try:
        return getattr(reader, "use_server")
    except:
        pass


def get_server_host(key):
    front = getattr(config, key)
    url = get_url(front)
    use_server = get_use_server(front)
    if not url.endswith("/"):
        url = url + "/"

    if use_server:
        return url + SERVER + "/"

    return url
