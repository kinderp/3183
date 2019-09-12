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

# In the previous example (ex7.pdf) we set
# cell alignment in header and  body  with 
# self.span = False.
# Let's see here how to to do same but with
# self.span = True

class ExampleModel(Model):
    def __init__(self, **kwargs):
        super(ExampleModel, self).__init__(**kwargs)
        self.one = TextField("One:<br/>{}".format(self._one))
        self.two = TextField("Two:<br/>{}".format(self._two))
        self.three = ImageField("images/Octocat.png", width=50, height=50)
        self.four = TextField("Four:<br/>{}".format(self._four))


class ExampleView(TableView):
    def __init__(self, **kwargs):
        self.model = ExampleModel(**kwargs)
        self.fields = [
                        ['one', 'two'],
                        ['one', 'two', 'three', 'four'],
                        ['one'],
                        ['one', 'two', 'four', 'three'],
                        ['one', 'two', 'four'],
                      ]

        self.cell_alignment = {
                                "1":{
                                        "1": [('VALIGN','BOTTOM')],
                                        "3": [('VALIGN','TOP')]
                                },
                                "3":{
                                        "1": [('VALIGN','TOP')],
                                        "2": [('VALIGN','BOTTOM')]
                                },
                                "*": {
                                        "1": [('VALIGN','BOTTOM')],
                                        "2": [('VALIGN','TOP')],
                                }
        }

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

            }
        }
        self.span = True
        super(ExampleView, self).__init__(self)


class ExampleViewFirstRowDataBody(TableView):
    def __init__(self, **kwargs):
        self.model = ExampleModel(**kwargs)
        self.fields = [
                        ['one', 'two'],
                        ['one', 'two', 'three', 'four'],
                        ['one'],
                        ['one', 'two', 'four'],
                      ]
        self.cell_alignment = {
                                "*": {
                                        "1": [('VALIGN','BOTTOM')],
                                }
        }



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

            }
        }
        self.span = True
        self.body_header = self.fields[0]
        super(ExampleViewFirstRowDataBody, self).__init__(self)


from reportlab.platypus import SimpleDocTemplate, Spacer

if __name__ == '__main__':
    pdf = Template(filename='ex8.pdf')
    data_model = {
        "_one" : "1",
        "_two" : "2",
        "_four": "4",
    }

    data_body = [
                    ['*<br/><br/><br/>', '*', '*'],
                    ['*<br/><br/><br/>', '*', '*'],
                    ['*<br/><br/><br/>', '*', '*'],
                    ['*<br/><br/><br/>', '*', '*'],
    ]
    table = ExampleView(**data_model)
    rendered_table = table.render(data_body)
    pdf.story.add(rendered_table)

    some_space = Spacer(1, 10)
    pdf.story.add(some_space)

    first_row_data_body = [
        ['o<br/><br/>', 'o'],
        ['o<br/><br/>', 'o'],
        ['o<br/><br/>', 'o'],
    ]

    table_first_row_data_body = ExampleViewFirstRowDataBody(**data_model)
    rendered_table = table_first_row_data_body.render(first_row_data_body)
    pdf.story.add(rendered_table)

    pdf.build()
