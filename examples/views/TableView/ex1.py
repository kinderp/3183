import os, sys
project_dir =  os.path.realpath(__file__).split("/examples")[0]
sys.path.append(project_dir)

from toet.models import Model
from toet.views import TableView
from toet.fields import TextField
from toet.fields import ImageField
from toet.templates import Template
from toet.settings import Setting

from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from reportlab.platypus import Spacer

# In this first example about 'TableView' we will
# learn how to create a table's header.
# TableView is a table with steroids and it has a
# header with multiple rows and naturally a body.
# Let's see how to create a TableView with an header
# with just a single row.
# We'll learn how to modify doc's margins, using
# toet.settings.Setting class, for a better layout.


class ExampleModel(Model):
    def __init__(self, **kwargs):
        super(ExampleModel, self).__init__(**kwargs)
        self.one = TextField("One:<br/>{}".format(self._one))
        self.two = TextField("Two:<br/><b>{}</b>".format(self._two))
        self.three = ImageField("images/Octocat.png", width=50, height=50)
        self.four = TextField("Four:<br/>{}".format(self._four))


class ExampleView(TableView):
    def __init__(self, **kwargs):
        self.model = ExampleModel(**kwargs)
        self.fields = [
                        ['one', 'two', 'three', 'four']
                      ]
        self.style_header = {
            "one": {
                    "style": "Normal",
                    "commands": [
                                    ('alignment', TA_LEFT),
                                    ('fontName', 'Helvetica'),
                                    ('fontSize', 8),
                                ]
            },
            "two": {
                    "style": "Normal",
                    "commands": [
                                    ('alignment', TA_CENTER),
                                    ('fontName', 'Helvetica'),
                                    ('fontSize', 8),
                                ]
            },
            "four": {
                    "style": "Normal",
                    "commands": [
                                    ('alignment', TA_RIGHT),
                                    ('fontName', 'Helvetica'),
                                    ('fontSize', 8),
                                ]

            }
        }
        self.span = False
        super(ExampleView, self).__init__(self)

from reportlab.platypus import SimpleDocTemplate, Spacer

if __name__ == '__main__':
    pdf = Template()
    data_model = {
        "_one" : "Left aligned",
        "_two" : "Centered and bold",
        "_four": "Right aligned and <i>italic</i>",
    }
    table = ExampleView(**data_model)
    rendered_table = table.render()
    pdf.story.add(rendered_table)

    some_space = Spacer(1, 10)
    pdf.story.add(some_space)

    # In Setting do exist some variables that control
    # docs' margins. If you change those ones (see below)
    # all the elements (a table in this case) in your docs
    # will be affected.

    Setting.DOC_TOP_MARGIN = Setting.DOC_TOP_MARGIN - 20
    Setting.DOC_LEFT_MARGIN = Setting.DOC_LEFT_MARGIN - 50
    Setting.DOC_RIGHT_MARGIN = Setting.DOC_RIGHT_MARGIN - 50
    # Be careful to call update() method to apply margins'
    # changes.
    Setting.update()

    larger_table = ExampleView(**data_model)
    pdf.story.add(larger_table.render())
    pdf.build()

