from reportlab.platypus import Paragraph
from reportlab.lib.styles import getSampleStyleSheet

from .field import Field

styles = getSampleStyleSheet()

class TextField(Field):
    """
    Reportlab Paragraph Wrapper
    """
    def __init__(self, text='', style=None):
        self.__text = text
        if style:
            self.__style = style
        else:
            self.__style = styles['Normal']

    @property
    def text(self):
        return self.__text

    @text.setter
    def text(self, value):
        self.___text = value


    @property
    def style(self):
        return self.__style

    @style.setter
    def style(self, value):
        self.__style = value

    def render(self, text=None, style=None):
        if text is None and style is None:
            return Paragraph(text=self.__text, style=self.__style)
        elif text is None and style is not None:
            return Paragraph(text=self.__text, style=style)
        elif text is not None and style is not None:
            return Paragraph(text=text, style=style)


