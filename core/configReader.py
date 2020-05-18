from .common import read_config, CONFIG_FILE_PATH
import random


def _get_item_for_path(data, path):
    for line in path.split("."):
        if line.startswith("_") and line.replace("_", "").isdigit():
            line = line.replace("_", "")
        if line.isdigit():
            data = data[int(line)] if int(line) < len(data) else None
        else:
            data = data.get(line, None)

    return data


class ConfigReader:
    _config = None
    _readers = {}

    @classmethod
    def m2(cls, key):
        from .config import SERVER
        key = key if key.endswith("yml") else key + ".yml"
        _ = key.split(".")[0]
        if cls._readers.get(_, None) is None:
            cls._readers[_] = getattr(ConfigReader(read_config(key)), SERVER)
        return cls._readers.get(_)

    @staticmethod
    def config():
        if ConfigReader._config is None:
            ConfigReader._config = ConfigReader(read_config(CONFIG_FILE_PATH))
        return ConfigReader._config

    def __init__(self, data, item=""):
        self._data = data
        self._key = item

    def __getattr__(self, item):
        if item == "random":
            return self._random()
        elif item == "format":
            return self._format()

        _ = self._get_item(item)
        return self._get_inner_(_, item)

    def _random(self):
        list = self._get_item("list")
        return self._get_inner_(random.choice(list), "list")

    def _format(self):
        """
        使用格式化方式 生成对应属性
        :return:
        """
        format_list = self._get_item("format")
        data = {}
        for dict in format_list:
            if "name" not in dict:
                self._raise_Exception("format.name")

            data[dict["name"]] = self._analysis_format_value(dict)
        return self._get_inner_(data, "format")

    def _analysis_format_value(self, format_data):
        """
        解析format的值
      - name: account
        value: robot%04d
        start: 0
        end: 200
        带有 end 字段的，将会进行 格式化调用

      - name: password
        value: 111111
        不带有 end字段的，直接返回 value
        """
        if "value" in format_data:
            if "end" in format_data:
                start = format_data["start"] if "start" in format_data else 0
                end = format_data["end"]
                return format_data["value"] % random.randrange(start, end)
            else:
                return format_data["value"]
        self._raise_Exception("format.value")

    def _get_item(self, item):
        _ = _get_item_for_path(self._data, item)
        if _ is None:
            # raise Exception("路径 {} 不存在".format(self._key + "." + item))
            self._raise_Exception(item)
        return _

    def _raise_Exception(self, item):
        raise Exception("路径 {} 不存在".format(self._key + "." + item))

    def _get_inner_(self, data, item):
        if isinstance(data, str) or isinstance(data, int):
            return data
        else:
            return ConfigReader(data, self._key + "." + item)
