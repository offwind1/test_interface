import yaml
import sys
import os
import xml.etree.cElementTree as ET

PACKAGE_PATH = os.path.join(__file__, os.path.pardir)
MAIN_PATH = os.path.join(PACKAGE_PATH, os.path.pardir)

CONFIG_PATH = os.path.join(MAIN_PATH, "config")
CONFIG_FILE_PATH = os.path.join(CONFIG_PATH, "config.yml")

def read_yaml_file(file_path):
    """
    读取yaml格式的文档，返回一个字典
    :param file_path:
    :return:
    """
    with open(os.path.join(PACKAGE_PATH, file_path), 'r', encoding='utf-8') as f:
        try:
            data = yaml.load(f)
            return data
        except:
            raise Exception(file_path, " 文件中的内容yaml格式不正确")
    raise Exception(file_path, " 文件路径不存在或者打不开")


def save_yaml_file(file_path, data):
    with open(file_path, "w", encoding="utf-8") as  f:
        yaml.dump(data, f, default_flow_style=False, allow_unicode=True)


def parse_xml(path):
    """
        解析xml，返回root
    """
    if not os.path.exists(path):
        raise Exception("路径:{} 的文件不存在".format(path))

    return ET.parse(path).getroot()


def add_element_method(Kclass, filename):
    """为类添加方法"""

    def request_object(api, name=None):
        def _object():
            obj = Kclass(api=api, name=name)
            # obj.api = api
            return obj

        return _object

    for dict in read_yaml_file(filename):
        line = dict["url"]
        name = dict["name"]
        setattr(Kclass, line.replace("/", "_"), request_object(line, name))

def read_config(key):
    path = os.path.join(CONFIG_PATH, key)
    return read_yaml_file(path)
