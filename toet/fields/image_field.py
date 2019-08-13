from reportlab.platypus import Image

from .field import Field

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

