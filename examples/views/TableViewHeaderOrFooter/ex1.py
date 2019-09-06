import os, sys
project_dir =  os.path.realpath(__file__).split("/examples")[0]
sys.path.append(project_dir)

from toet.models import Model
from toet.views import TableViewHeaderOrFooter
from toet.templates import Template
from toet.fields import TextField, ImageField

from reportlab.lib.pagesizes import A4
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from reportlab.platypus import SimpleDocTemplate, Spacer, PageBreak

class HeaderModel(Model):
    def __init__(self,**kwargs):
        """Init custom Model (Header)
        Parameters: 
            kwargs : { '_title': 'My repositories', '_session': ''}
        """
        super(HeaderModel, self).__init__(**kwargs)
        self.session = TextField(text="{}".format(self._session))
        self.title = TextField(text="{}".format(self._title))
        self.logo = ImageField('{}/examples/TableView/images/Octocat.png'.format(project_dir), width=50, height=50)


class HeaderView(TableViewHeaderOrFooter):
     def __init__(self, **kwargs):
        self.model = HeaderModel(**kwargs)
        self.fields = ['session', 'title', 'logo']
        self.style_header = {
            "title": {
                "style": "Normal",
                "commands": [
                                ('alignment', TA_CENTER),
                                ('fontName', 'Helvetica'),
                                ('fontSize', 14),
                ]
            },
            "session": {
                "style": "Normal",
                "commands": [
                                ('alignment', TA_CENTER),
                                ('fontName', 'Helvetica'),
                                ('fontSize', 14),
                ]
            }

        }
        super(HeaderView, self).__init__(self)

from datetime import datetime

if __name__ == '__main__':

    header_data = {
        "_title": "<b>Github Report</b>",
        "_session": datetime.now().strftime("%m/%d/%Y - %H:%M:%S")
    }

    footer = {
                'left': '',
                'right': 'Right in the footer',
                'middle': 'Middle in the footer'
    }

    header = HeaderView(**header_data)
    pdf = Template(header=header, footer=footer)
    some_space = Spacer(1,10)

    a_new_page = PageBreak()

    pdf.story.add(some_space)
    pdf.story.add(a_new_page)
    pdf.story.add(a_new_page)

    pdf.build()
