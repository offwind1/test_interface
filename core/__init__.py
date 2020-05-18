from .M2 import Mizhu, Manage
from .common import add_element_method, read_config
from .configReader import ConfigReader
from .config import SERVER
from .people import Student, Teacher, Jigou, Admin
# from .utx.core import TestCase
from .utx import *


add_element_method(Mizhu, "mizhu.yml")
add_element_method(Manage, "manage.yml")
