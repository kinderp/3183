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

# In this example we'll create a table
# will use self.body_header to set our
# body's header to a complete customi-
# -zable value.

class ExampleModel(Model):
    def __init__(self, **kwargs):
        super(ExampleModel, self).__init__(**kwargs)
        self.one = TextField("One:<br/>{}".format(self._one))
        self.two = TextField("Two:<br/>{}".format(self._two))
        self.three = ImageField("images/Octocat.png", width=50, height=50)
        self.four = TextField("Four:<br/>{}".format(self._four))
        self.five = TextField("Five:<br/>{}".format(self._five))
        self.six = TextField("Six:<br/>{}".format(self._six))
        self.seven = TextField("Seven:<br/>{}".format(self._seven))
        self.blank = TextField(" ")
        self.ignored = TextField("This field will be ignored because in the \
                                  same row of a inner table")

        self.not_ignored = TextField("This one is in a new row, it won't be \
                                     ignored")
class ExampleView(TableView):
    def __init__(self, **kwargs):
        self.model = ExampleModel(**kwargs)
        self.fields = [
                        ['not_ignored'],
                        [
                            [
                                ['one', 'one', 'two', 'two', 'three'],
                                ['one', 'one', 'blank', 'four', 'three'],
                                ['five', 'five','six', 'six', 'seven'],
                            ],
                        ],
                        ['not_ignored', 'not_ignored'],
                      ]
        # set body_header to a complet arbitrary value
        self.body_header = ['one','two','four','five','six']
        # if you comment the line above, the number
        # of columns in the body will come back to be
        # defined by the last row in the header.

        self.style_header = {
            "one": {
                    "style": "Normal",
                    "commands": [
                                    ('alignment', TA_CENTER),
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
                                    ('alignment', TA_CENTER),
                                    ('fontName', 'Helvetica'),
                                    ('fontSize', 8),
                                ]
            },
            "five": {
                    "style": "Normal",
                    "commands": [
                                    ('alignment', TA_CENTER),
                                    ('fontName', 'Helvetica'),
                                    ('fontSize', 8),
                                ]
            },
            "six": {
                    "style": "Normal",
                    "commands": [
                                    ('alignment', TA_CENTER),
                                    ('fontName', 'Helvetica'),
                                    ('fontSize', 8),
                                ]
            },
            "seven": {
                    "style": "Normal",
                    "commands": [
                                    ('alignment', TA_CENTER),
                                    ('fontName', 'Helvetica'),
                                    ('fontSize', 8),
                                ]
            },
        }
        self.span = True
        super(ExampleView, self).__init__(self)


from reportlab.platypus import SimpleDocTemplate, Spacer

if __name__ == '__main__':
    pdf = Template(filename='ex6.pdf')
    data_model = {
        "_one"  : "1",
        "_two"  : "2",
        "_four" : "4",
        "_five" : "5",
        "_six"  : "6",
        "_seven": "7",
    }
    data_body = [
        ["crazy body's header", "crazy body's header", "crazy body's header", "crazy body's header", "crazy body's header"],
        ["crazy body's header", "crazy body's header", "crazy body's header", "crazy body's header", "crazy body's header"],
        ["crazy body's header", "crazy body's header", "crazy body's header", "crazy body's header", "crazy body's header"],
    ]
    # Create a table with an inner table in the header.
    # The last row in the heeader will define the nums
    # of columns in the body.  You can overwrite  this 
    # behaviour using self.body_header as seen in prev-
    # -ious example.
    table = ExampleView(**data_model)
    rendered_table = table.render(data_body)
    pdf.story.add(rendered_table)

    pdf.build()
