from .M2 import Mizhu, Manage, Kaca
from .common import add_element_method, read_config
from .configReader import ConfigReader
from .config import SERVER
from .people import *
from .utx.core import TestCase
from .utx import *
from .model import Lesson, Clazz, Courseware
from .execlUtil import *
from .util import *

add_element_method(Mizhu, "mizhu.yml")
add_element_method(Manage, "manage.yml")
add_element_method(Kaca, "kaca.yml")
