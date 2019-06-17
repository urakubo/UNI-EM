###
###
###

from Filter2D3D.filters import Binary
from Filter2D3D.filters import Canny
from Filter2D3D.filters import Gaussian
from Filter2D3D.filters import Invert
from Filter2D3D.filters import Label
from Filter2D3D.filters import Skimg
from Filter2D3D.filters import Label3D
from Filter2D3D.filters import Skimg3D
from Filter2D3D.filters import CLAHE

class FilterInfo(object):
    def __init__(self):
        self.__info = [
            {'type': '2d', 'name': 'Binary', 'class': Binary.Binary},
            {'type': '2d', 'name': 'Canny', 'class': Canny.Canny},
            {'type': '2d', 'name': 'Gaussian', 'class': Gaussian.Gaussian},
            {'type': '2d', 'name': 'Invert', 'class': Invert.Invert},
            {'type': '2d', 'name': '2D Label', 'class': Label.Label},
            {'type': '2d', 'name': '2D Watershed', 'class': Skimg.Skimg},
            {'type': '2d', 'name': 'CLAHE', 'class': CLAHE.CLAHE},
            {'type': '3d', 'name': '3D Label', 'class': Label3D.Label3D},
            {'type': '3d', 'name': '3D Watershed', 'class': Skimg3D.Skimg3D},
            ]

    def get_2d_filter_name_list(self):
        for i in self.__info:
            if i['type'] == '2d':
                yield i['name']

    def get_3d_filter_name_list(self):
        for i in self.__info:
            if i['type'] == '3d':
                yield i['name']

    def get_class(self, name):
        for i in self.__info:
            if name == i['name']:
                return i['class']

    def get_type(self, name):
        for i in self.__info:
            if name == i['name']:
                return i['type']

