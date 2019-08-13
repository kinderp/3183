from reportlab.platypus import Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from .text_field import TextField

styles = getSampleStyleSheet()

class BulletTextField(TextField):
    def __init__(self, *args, **kwargs):
        super(BulletTextField, self).__init__(*args, **kwargs)

    def render(self):
        return Paragraph(text=self.text, style=self.style, bulletText='[  ]')

