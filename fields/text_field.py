from reportlab.platypus import Paragraph
from reportlab.lib.styles import getSampleStyleSheet

from .field import Field

styles = getSampleStyleSheet()

class TextField(Field):
    """
    Reportlab Paragraph Wrapper
    """
    def __init__(self, text='', style=None):
        self.text = text
        if style:
            self.style = style
        else: 
            self.style = styles['Normal']

    def render(self):
        return Paragraph(text=self.text, style=self.style)

