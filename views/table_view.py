from reportlab.platypus import Table, TableStyle
from reportlab.lib import colors

from utils import FieldFactory

from .view import View

class TableView(View):

    def __init__(self, child):

        self.child = child
        self.model = child.model
        self.fields = child.fields
        self.span = child.span
        # style is static yet
        # TO DO: load style dynamically somewhere
        self.LIST_STYLE_HEADER = TableStyle(
            [
            ('BOX', (0,0), (-1,-1), 0.25, colors.black),
            ('INNERGRID', (0,0), (-1,-1), 0.25, colors.black),
            ('ALIGN', (0,0), (-1,-1), 'CENTER'),
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
            ]
            )

        self.LIST_STYLE = TableStyle(
            [
            ('BOX', (0,0), (-1,-1), 0.25, colors.black),
            ('INNERGRID', (0,0), (-1,-1), 0.25, colors.black),
            ('ALIGN', (0,0), (-1,-1), 'CENTER'),
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
            ]
            )

        super(TableView, self).__init__(self.child)

    def render(self, data=[]):
        # render_header return a list (objects)
        #
        # - if span == False:
        #   objects is a list with a single Table (header)
        #
        # - if span == True:
        #   objects is a list of Tables (a table for each header rows)
        objects = self.render_header()
        # if data list is empty (no body)
        # return just the header 
        if not data:
            return objects
        # render_body add a new Table (body table)
        # with data values filled 
        return self.render_body(objects, data)

    def render_body(self, header, data):
        # - append body table in header
        body_rendered_objects = []
        body_fields = self.fields[-1]
        for row in data:
            new_rendered_row = []
            for i, field in enumerate(body_fields):
                current_record = row[i]
                class_name = getattr(self.model, field).__class__.__name__
                print(class_name)
                if isinstance(current_record, dict):
                    new_body_obj = FieldFactory.create(class_name, current_record)
                    new_rendered_row.append(new_body_obj.render())
                else:
                    new_body_obj = FieldFactory.create(class_name, (current_record,))
                    new_rendered_row.append(new_body_obj.render())
            body_rendered_objects.append(new_rendered_row)

        header.append(Table(body_rendered_objects, style=self.LIST_STYLE))
        return header 

    def render_header(self):
        objects = []

        for rows in self.fields:
            new_row = []
            for elem in rows:
                if elem:
                    new_row.append(getattr(self.model, elem).render())
                else:
                    new_row.append('')

            if self.span:
                t = Table([new_row], style=self.LIST_STYLE_HEADER)
                objects.append(t)
            else:
                objects.append(new_row)

        if not self.span:
            objects = [Table(objects, style=self.LIST_STYLE_HEADER)]
        return objects

