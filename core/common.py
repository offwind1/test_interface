import yaml
import sys
import os
import xml.etree.cElementTree as ET

package_path = os.path.join(__file__, os.path.pardir)
config_path = os.path.join(package_path, "config.yml")


def read_yaml_file(file_path):
    """
    读取yaml格式的文档，返回一个字典
    :param file_path:
    :return:
    """
    with open(os.path.join(package_path, file_path), 'r', encoding='utf-8') as f:
        try:
            data = yaml.load(f)
            return data
        except:
            raise Exception(file_path, " 文件中的内容yaml格式不正确")
    raise Exception(file_path, " 文件路径不存在或者打不开")


def save_yaml_file(file_path, data):
    with open(file_path, "w", encoding="utf-8") as  f:
        yaml.dump(data, f, default_flow_style=False, allow_unicode=True)


config = read_yaml_file(config_path)


def get_config_attr(key):
    return config.get(key, "")


def get_server_host(key):
    front = get_config_attr(key)
    behind = get_config_attr("server")

    if front.endswith("/"):
        return front + behind + "/"

    return front + "/" + behind + "/"


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

    #
    # with open(os.path.join(package_path, filename), encoding="utf-8") as f:
    #     for line in f.readlines():
    #         line = line.strip()
    #         setattr(Kclass, line.replace("/", "_"), request_object(line))
