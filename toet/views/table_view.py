import copy

from reportlab.platypus import Table, TableStyle
from reportlab.lib import colors

from ..utils import FieldFactory
from ..styles import Styles
from .view import View

from reportlab.lib.pagesizes import A4

from ..settings import Setting


class TableView(View):

    def __init__(self, child):
        self.DOC_WIDTH_REAL = Setting.DOC_WIDTH_REAL
        self.child = child
        self.model = child.model
        self.fields = child.fields
        self.span = child.span
        self.body_header = child.body_header if hasattr(child, 'body_header') else None 
        # atm style is only for header fields styiling (Textfield in a cell)
        # IS NOT table style (border backgroudn and so on)!
        self.style_header = child.style_header if hasattr(child, 'style_header') else []
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
 
    def set_style(self, _commands, header=True, body=True):
            if _commands:
                if header and body:
                    self.LIST_STYLE_HEADER = TableStyle(_commands)
                    self.LIST_STYLE = TableStyle(_commands)
                elif header and not body:
                    self.LIST_STYLE_HEADER = TableStyle(_commands)
                elif not header and body:
                    self.LIST_STYLE = TableStyle(_commands)
 
    def _get_col_widths(self,  data):
        n_cols = len(data)
        return [self.DOC_WIDTH_REAL/n_cols]*n_cols

    def _view_rule(self):
        # TODO: Put here all the logic for rendering rules
        # 1. if an inner table is present in a row
        #    it MUST be the only elem in that row
        #
        # 2. if an inner table is present in a row
        #    self.span MUST be TRUE. Inner table are supported
        #    only in span mode.
        pass

    def render(self, data=[]):
        # render_header returns a list (objects)
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
        # with data values filled in
        return self.render_body(objects, data)

    def _get_body_fields(self):
        if self.body_header:
            #return self.body_header
            last_header_row = self.body_header
        else:
            last_header_row = self.fields[-1]

        if isinstance(last_header_row[0],list):
            # last row is an innertable
            # last_header_row is a matrix
            # return last row of that matrix
            return last_header_row[0][-1], True
        else:
            # normal case
            return last_header_row, False

    def render_body(self, header, data):
        # - append body table in header
        body_rendered_objects = []
        #body_fields = self.fields[-1]
        body_fields, is_inner_table = self._get_body_fields()
        if is_inner_table:
            body_inner_table = self._render_body_inner_table(data, body_fields)
            header.append(body_inner_table)
            return header
        for row in data:
            new_rendered_row = []
            for i, field in enumerate(body_fields):
                current_record = row[i]
                class_name = getattr(self.model, field).__class__.__name__
                #print(class_name)
                if isinstance(current_record, dict):
                    new_body_obj = FieldFactory.create(class_name, current_record)
                    new_rendered_row.append(new_body_obj.render())
                else:
                    new_body_obj = FieldFactory.create(class_name, (current_record,))
                    new_rendered_row.append(new_body_obj.render())
            body_rendered_objects.append(new_rendered_row)

        col_widths = self._get_col_widths(body_rendered_objects[0])
        #header.append(Table(body_rendered_objects, style=self.LIST_STYLE))
        header.append(Table(body_rendered_objects, style=self.LIST_STYLE,
                            colWidths=col_widths))
        return header

    def render_header(self):
        objects = []
        for rows in self.fields:
            inner = False
            new_row = []
            for elem in rows:
                if elem and isinstance(elem, str):
                    # if elem in a row is a str, it is a simple elem like:
                    # TextField, ImageField ecc.
                    class_name = getattr(self.model, elem).__class__.__name__
                    if elem in self.style_header and class_name == 'TextField':
                        # atm header style con be applied only to TextField
                        # type. ( and class_name == 'TextField )

                        style_name = self.style_header[elem]['style']
                        commands = self.style_header[elem]['commands']
                        my_style = Styles.style(style=style_name,
                                                commands=commands)

                        new_row.append(getattr(self.model,
                                               elem).render(style=my_style))
                    else:
                        new_row.append(getattr(self.model, elem).render())
                elif elem and isinstance(elem, list):
                    # if elem is a list it is an inner table.
                    #
                    # Note: inner table is supported only in span
                    # mode. So self.span must be TRUE.
                    # self._view_rules() should take care of these rules.
                    inner_table = self._render_inner_table(elem)
                    # inner_table cen be added already here into objects
                    # and break the loop over row elements. 
                    # If and inner table is present,
                    # it must be the only elem in a row.
                    objects.append(inner_table)
                    inner = True
                    # break here because inner table must occupy a whole row
                    # so elem before or after an inner table (in the same row)
                    # will be ignored.
                    # e.g.
                    #
                    #   self.fields = [
                    #                   ['session'], 
                    #                   [
                    #                       'session', <<<< IGNORED
                    #                       [
                    #                           ['participants', 'signatures', 'signatures', 'observations'],
                    #                           ['participants', 'part1', 'part2', 'observations']
                    #                       ],
                    #                       'session' <<<<< IGNORED
                    #                   ],
                    #                ],
                    #

                    break
                else:
                    new_row.append('')

            if self.span and not inner:
                # this row is not an inner table
                # objects contais all the rendered elems of the row
                #t = Table([new_row], style=self.LIST_STYLE_HEADER)
                col_widths = self._get_col_widths(new_row)
                t = Table([new_row], style=self.LIST_STYLE_HEADER,
                          colWidths=col_widths)
                objects.append(t)
            elif self.span and inner:
                # nothing to do here, inner talbe has been added above
                # into objects.
                # Let leave explicit this elif just to understand better the
                # whole logic
                pass
            else:
                objects.append(new_row)

        if not self.span:
            col_widths = self._get_col_widths(objects[0])
            objects = [Table(objects, style=self.LIST_STYLE_HEADER, colWidths=col_widths)] 
            #objects = [Table(objects, style=self.LIST_STYLE_HEADER)] 
        return objects

    def _render_body_inner_table(self, data, body_fields):

        body_rendered_objects = []
        # style_command appends SPAN commands to style header
        # SPAN commands are needed to create our inner table

        style_command = copy.deepcopy(self.LIST_STYLE)
        #style_command = TableStyle([
        #    ('INNERGRID', (0,0), (-1,-1), 0.25, colors.black),
        #])

        fields = set(body_fields)

        indices = {x: [] for x in fields}
        # indices is a dict and it contains table coords (col, row) for earch fields
        # e.g. if data is like below:
        #
        # data = [
        #         ['uno', 'uno', 'due', 'due', 'due', 'tre'],
        #        ]
        #
        # indices will have this values
        #
        # {'tre':     [5], 
        #  'uno':     [0, 1], 
        #  'due':     [2. 3. 4], 
        # }
        #
        # for each elem in data indices will contain (col,row) coords

        for elem in fields:
            for i, field in enumerate(body_fields):
                if field == elem:
                    indices[elem].append(i)
        # after calculating indices, we use those ones for (sc, sr), (ec, er)
        # coords in SPAN commands
        # 
        # SPAN, (sc,sr), (ec,er)
        # indicates that the cells in columns sc - ec and rows sr - er should 
        # be combined into a super cell with contents determined by the cell 
        # (sc, sr). 
        #
        # The other cells should be present, but should contain empty strings 
        # or you may get unexpected results.

        for field in indices:
            if len(indices[field]) < 2:
                continue
            for r, row in enumerate(data):
                tmp_span_command =  ('SPAN', ( min(indices[field]), r ), (max(indices[field]), r ) )
                style_command.add(*tmp_span_command)


        # recreate data (compliant_data) with '' in the other cells (to avoid
        # unexpected results)

        n_cols = len(body_fields)
        n_rows = len(data)
        compliant_data = [['']*n_cols]*n_rows

        for r, row in enumerate(data):
            for i, field in enumerate(fields):
                min_col_index = min(indices[field])
                compliant_data[r][min_col_index] = row[i]

        # and finally rendering fields
        for row in compliant_data:
            new_rendered_row = []
            for i, field in enumerate(body_fields):
                current_record = row[i]
                if current_record == '':
                    new_rendered_row.append(current_record)
                else:
                    class_name = getattr(self.model, field).__class__.__name__
                    if isinstance(current_record, dict):
                        new_body_obj = FieldFactory.create(class_name, current_record)
                        new_rendered_row.append(new_body_obj.render())
                    else:
                        new_body_obj = FieldFactory.create(class_name, (current_record,))
                        new_rendered_row.append(new_body_obj.render())
            body_rendered_objects.append(new_rendered_row)

        col_widths = self._get_col_widths(body_fields)
        return Table(body_rendered_objects, colWidths=col_widths, style=style_command)


    def _render_inner_table(self, data):

        # style_command appends SPAN commands to style header
        # SPAN commands are needed to create our inner table

        style_command = copy.deepcopy(self.LIST_STYLE_HEADER)
        #style_command = TableStyle([
        #    ('INNERGRID', (0,0), (-1,-1), 0.25, colors.black),
        #])

        fields = set([item for row in data for item in row] )

        indices = {x: [] for x in fields}
        # indices is a dict and it contains table coords (col, row) for earch fields
        # e.g. if data is like below:
        #
        # data = [
        #         ['uno', 'due', 'due', 'tre'],
        #         ['uno', 'quattro', 'cinque', 'tre']
        #        ]
        #
        # indices will have this values
        #
        # {'tre':     [(3, 0), (3, 1)], 
        #  'uno':     [(0, 0), (0, 1)], 
        #  'quattro': [(1, 1)], 
        #  'due':     [(1, 0), (2, 0)], 
        #  'cinque':  [(2, 1)]
        # }
        #
        # for each elem in data indices will contain (col,row) coords


        for elem in fields:
            for r, row in enumerate(data):
                col_indices = [i for i, x in enumerate(row) if x == elem]
                indices[elem].extend(list(zip(col_indices, [r]*len(col_indices))))

        # after calculating indices, we use those ones for (sc, sr), (ec, er)
        # coords in SPAN commands
        # 
        # SPAN, (sc,sr), (ec,er)
        # indicates that the cells in columns sc - ec and rows sr - er should 
        # be combined into a super cell with contents determined by the cell 
        # (sc, sr). 
        #
        # The other cells should be present, but should contain empty strings 
        # or you may get unexpected results.

        min_list = [] # contains (sc,sr) coords (where no '')

        for field in indices:
            if len(indices[field]) < 2:
                min_list.append(min(indices[field]))
                continue
            tmp_span_command =  ('SPAN', min(indices[field]), max(indices[field]) )
            style_command.add(*tmp_span_command)
            min_list.append(min(indices[field]))


        # recreate data (compliant_data) with '' in the other cells (to avoid
        # unexpected results)
        compliant_data = copy.deepcopy(data) 
        for sr, row in enumerate(data):
            for sc, elem in enumerate(row):
                if (sc, sr) not in min_list:
                    compliant_data[sr][sc] = ''
                else:
                    class_name = getattr(self.model, elem).__class__.__name__
                    if elem in self.style_header and class_name == 'TextField':
                        # atm header style con be applied only to TextField
                        # type. ( and class_name == 'TextField )
                        style_name = self.style_header[elem]['style']
                        commands = self.style_header[elem]['commands']
                        my_style = Styles.style(style=style_name,
                                                commands=commands)

                        compliant_data[sr][sc] = getattr(self.model, elem).render(style=my_style)
                    else:
                        compliant_data[sr][sc] = getattr(self.model, elem).render()

        # and finally rendering fields
        col_widths = self._get_col_widths(compliant_data[0])
        #return Table(compliant_data, style=style_command)
        return Table(compliant_data, colWidths=col_widths, style=style_command)


class TableViewHeaderOrFooter(View):
    def __init__(self, child):

        self.child = child
        self.model = child.model
        self.fields = child.fields
        # IS NOT table style (border backgroudn and so on)!
        self.style_header = child.style_header if hasattr(child, 'style_header') else []
        # style is static yet
        # TO DO: load style dynamically somewhere
        self.STYLE = TableStyle(
            [
            ('BOX', (0,0), (-1,-1), 0.25, colors.black),
            ('INNERGRID', (0,0), (-1,-1), 0.25, colors.black),
            ('ALIGN', (0,0), (-1,-1), 'CENTER'),
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
            ]
            )
        super(TableViewHeaderOrFooter, self).__init__(self.child)

    def render(self):
        rendered_fields = []
        for elem in self.fields:
            class_name = getattr(self.model, elem).__class__.__name__
            if elem in self.style_header and class_name == 'TextField':
                # atm header style con be applied only to TextField
                # type. ( and class_name == 'TextField )

                style_name = self.style_header[elem]['style']
                commands = self.style_header[elem]['commands']
                my_style = Styles.style(style=style_name, commands=commands)

                rendered_fields.append(getattr(self.model, elem).render(style=my_style))
            else:
                rendered_fields.append(getattr(self.model, elem).render())

        return [Table([rendered_fields], style=self.STYLE)]
