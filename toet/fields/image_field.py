from reportlab.platypus import Image
from reportlab.platypus import Flowable

from .field import Field

class MyFlowable(Flowable):
    """
     A Custom Flowable
     """
    def __init__(self, img,width, height=0):
        Flowable.__init__(self)
        self.width = width
        self.height = height
        self.img = img

    #def wrap(self, *args):
    #    return (self.width, self.height)

    def draw(self):
        self.canv.drawImage(self.img, 0, 0, height=self.height, width=self.width)


class ImageField(Field):
    """
    Reportlab Image Wrapper
    """
    def __init__(self, path='', width=None, height=None):
        self.path = path
        self.width = width
        self.height = height

    def render(self):
        return Image(self.path, width=self.width, height=self.height)


class LowImageField(Field):
    """
    Reportlab Image Wrapper
    """

    def __init__(self, path='', width=None, height=None):
        self.path = path
        self.width = width
        self.height = height

    def render(self):
        return MyFlowable(self.path, width=self.width, height=self.height)

