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


# This example is quite similar to a previous one
# (ex2.py) but it is focused  on cells  alignment
# We'll create two TableView,  first one  with no
# body and the latter one with a body.
# We will see how to set vertical  and  orizontal
# alignment  for  each header's row  and  for the 
# whole body.
# It's no possible set alignment for a single row
# in the body, sorry.

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
                        ['one', 'two', 'three', 'four'],
                        ['one', 'two', 'three', 'four'],
                        ['one', 'two', 'three', 'four'],
                      ]
        # As you can see orizontal alignment (right)  does  not work  here
        # for TextField but it works for ImageField.
        # Only for TextField set orizontal alignment in style_header field.
        self.cell_alignment = {
                                "0": {
                                    "0": [('VALIGN',"TOP"),('ALIGN','RIGHT')],
                                    "1": [('VALIGN',"MIDDLE"),('ALIGN','RIGHT')],
                                    "2": [('VALIGN',"MIDDLE"),('ALIGN','RIGHT')], # ImageField
                                    "3": [('VALIGN',"BOTTOM"),('ALIGN','RIGHT')],
                                },
                                "1": {
                                    "0": [('VALIGN',"BOTTOM"),('ALIGN','RIGHT')],
                                    "1": [('VALIGN',"MIDDLE"),('ALIGN','RIGHT')],
                                    "2": [('VALIGN',"MIDDLE"),('ALIGN','LEFT') ], # ImageField
                                    "3": [('VALIGN',"TOP"),('ALIGN','RIGHT')],
                                },
        }
        self.style_header = {
            "one": {
                    "style": "Normal",
                    "commands": [
                                    ('fontName', 'Helvetica'),
                                    ('fontSize', 8),
                                ]
            },
            "two": {
                    "style": "Normal",
                    "commands": [
                                    ('alignment', TA_RIGHT),
                                    ('fontName', 'Helvetica'),
                                    ('fontSize', 8),
                                ]
            },
            "four": {
                    "style": "Normal",
                    "commands": [
                                    ('fontName', 'Helvetica'),
                                    ('fontSize', 8),
                                ]

            }
        }
        self.span = False
        super(ExampleView, self).__init__(self)


class ExampleModelSampleBody(Model):
    def __init__(self, **kwargs):
        super(ExampleModelSampleBody, self).__init__(**kwargs)
        self.one = TextField("One<br/><br/><br/>")
        self.two = TextField("Two")
        self.three = TextField("Three")


class ExampleViewSampleBody(TableView):
    def __init__(self, **kwargs):
        self.model = ExampleModelSampleBody(**kwargs)
        self.fields = [
                        ['one', 'two', 'three',],
                        ['one', 'two', 'three',],
                      ]
        self.cell_alignment = {
                                "0": {
                                    "0": [('VALIGN',"TOP"),('ALIGN','RIGHT')],
                                    "1": [('VALIGN',"MIDDLE"),('ALIGN','RIGHT')],
                                    "2": [('VALIGN',"BOTTOM"),('ALIGN','RIGHT')],
                                },
                                "1": {
                                    "0": [('VALIGN',"BOTTOM"),('ALIGN','RIGHT')],
                                    "1": [('VALIGN',"MIDDLE"),('ALIGN','RIGHT')],
                                    "2": [('VALIGN',"TOP"),('ALIGN','RIGHT')],
                                },
                                "*": {
                                    "1": [('VALIGN',"BOTTOM")],
                                    "2": [('VALIGN',"TOP")],
                                }
        }
        self.style_header = {
            "one": {
                    "style": "Normal",
                    "commands": [
                                    ('fontName', 'Helvetica'),
                                    ('fontSize', 8),
                                ]
            },
            "two": {
                    "style": "Normal",
                    "commands": [
                                    ('fontName', 'Helvetica'),
                                    ('fontSize', 8),
                                ]
            },
            "three": {
                    "style": "Normal",
                    "commands": [
                                    ('fontName', 'Helvetica'),
                                    ('fontSize', 8),
                                ]

            }
        }
        self.span = False
        super(ExampleViewSampleBody, self).__init__(self)


from reportlab.platypus import SimpleDocTemplate, Spacer

if __name__ == '__main__':
    pdf = Template(filename='ex7.pdf')
    data_model = {
        "_one" : "1",
        "_two" : "2",
        "_four": "4",
    }
    # a table with a multiple rows header
    # but no body.
    table = ExampleView(**data_model)
    rendered_table = table.render()
    pdf.story.add(rendered_table)

    some_space = Spacer(1, 10)
    pdf.story.add(some_space)

    # a table with same header but with a body.
    table = ExampleViewSampleBody()
    data_body = [
                    ['cell body under 1<br/><br/><br/>','cell body under 2', 'cell body under3'],
                    ['cell body under 1<br/><br/><br/>','cell body under 2', 'cell body under3'],
                    ['cell body under 1<br/><br/><br/>','cell body under 2', 'cell body under3'],
                    ['cell body under 1<br/><br/><br/>','cell body under 2', 'cell body under3'],
    ]
    # to set a body pass body data in render() call.
    rendered_table = table.render(data_body)
    pdf.story.add(rendered_table)


    pdf.build()
