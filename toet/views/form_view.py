from .view import View
from ..styles import Styles
from reportlab.platypus import Spacer

class FormView(View):
    def __init__(self, child):
        self.child = child
        self.model = child.model
        self.fields = child.fields
        self.styles = child.styles

    def render(self):
        objects = []
        for rows in self.fields:
            new_row = []
            for elem in rows:
                if elem in self.styles:
                    # this elem has a style defined in self.styles
                    my_style_name = self.styles[elem]['style']
                    my_commands = self.styles[elem]['commands']
                    my_style = Styles.style(style=my_style_name,
                                           commands=my_commands)
                    new_row.append(getattr(self.model,
                                           elem).render(style=my_style))
                    if 'space' in self.styles[elem]:
                        new_row.append(Spacer(1,self.styles[elem]['space']))
                else:
                    # no style, default=Normal
                    new_row.append(getattr(self.model, elem).render())

            objects.extend(new_row)

        return objects

