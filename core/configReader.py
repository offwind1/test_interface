from core.util.common import read_config, CONFIG_FILE_PATH
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


#配置文件读取类
class ConfigReader:
    _config = None
    _readers = {} # 全局缓存 避免反复读取

    @classmethod
    def m2(cls, key):
        """
        读取对应的 账号配置
        :param key: 配置文件名称
        :return:
        """
        from .config import SERVER

        key = key if key.endswith("yml") else key + ".yml"
        _ = key.split(".")[0]

        if cls._readers.get(_, None) is None:
            # 根据 SERVER 标签读取对应的测试或者正式的配置
            # 并将其记录到缓存中
            cls._readers[_] = getattr(ConfigReader(read_config(key)), SERVER)
        #从缓存中读取配置文件内容返回
        return cls._readers.get(_)

    @staticmethod
    def config():
        """
        读取默认的 服务器 配置
        :return:
        """
        if ConfigReader._config is None:
            ConfigReader._config = ConfigReader(read_config(CONFIG_FILE_PATH))
        return ConfigReader._config

    def __init__(self, data, item=""):
        self._data = data # 字典
        self._key = item # 属性标签

    def __getattr__(self, item):
        if item == "random":
            # 运行random函数时，转接到_random函数
            return self._random()
        elif item == "format":
            # 运行format函数时，转接到_format函数
            return self._format()
        elif "%" in item:
            return self.__getattribute__(item)

        _ = self._get_item(item)
        return self._get_inner_(_, item)

    def __iter__(self):
        return iter(self._data)

    def _random(self):
        """
        随机读取list下的值
        :return:
        """
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
        # 获取配置对象
        _ = _get_item_for_path(self._data, item)
        if _ is None:
            # raise Exception("路径 {} 不存在".format(self._key + "." + item))
            self._raise_Exception(item)
        return _

    def _raise_Exception(self, item):
        raise Exception("路径 {} 不存在".format(self._key + "." + item))

    def _get_inner_(self, data, item):
        # 若data还是字典对象，再包装成ConfigReader对象返回
        if isinstance(data, str) or isinstance(data, int):
            return data
        else:
            return ConfigReader(data, self._key + "." + item)
