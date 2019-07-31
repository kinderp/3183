from reportlab.platypus import SimpleDocTemplate
from reportlab.platypus import Table, TableStyle
from reportlab.platypus import Paragraph, Spacer
from reportlab.platypus import Image

from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors

from reportlab.platypus.flowables import Flowable

styles = getSampleStyleSheet()

from abc import ABC, abstractmethod


class Field(ABC):
    """
    Defined here interface for field types 
    """
    @abstractmethod
    def render(self):
        pass


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


class BulletTextField(TextField):
    def __init__(self, *args, **kwargs):
        super(BulletTextField, self).__init__(*args, **kwargs)

    def render(self):
        return Paragraph(text=self.text, style=self.style, bulletText='[  ]')


class ImageField(Field):
    """
    Reportlab Image Wrapper
    """
    def __init__(self, path='', width=None, height=None):
        self.path = path
        self.width = width
        self.height = height

    def render(self):
        return Image(self.path, width=self.width, height=self.height)

class FieldFactory():

    @staticmethod
    def create(class_name, data):

        if isinstance(data, dict):
            all_type = {
                "TextField": TextField(**data),
                "BulletTextField": BulletTextField(**data),
                "ImageField": ImageField(**data) 
            }
        else:
            all_type = {
                "TextField": TextField(*data),
                "BulletTextField": BulletTextField(*data),
                "ImageField": ImageField(*data) 
            }

        return all_type[class_name]



class Model(ABC):
    """
    Defined here interface for model types 
    """
    pass

class HeaderModel(Model):
    session = TextField(text="prova")
    title = TextField(text='titolo')
    logo = ImageField('./sanofi.png', width=50, height=50)


class View(ABC):

    def __init__(self, child):
        self.child = child
        self.model = child.model
        self.fields = child.fields

    def render(self):
        objects = []
        for elem in dir(self.model):
            if elem in self.fields:
                print(elem)
                cuurent_field = getattr(self.model,elem)
                objects.insert(0,cuurent_field.render())
        return objects


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


class HeaderView(TableView):
     model = HeaderModel()
     fields = [['session', 'title', 'logo']]
     span = False

     def __init__(self):
        super(HeaderView, self).__init__(self)

     def render(self):
        return super().render()


class SessionModel(Model):
    session_type = TextField(text="Session Type: ")
    s1 = BulletTextField(text='Bullet 1')
    s2 = BulletTextField(text='Bullet 2')
    s3 = BulletTextField(text='Bullet 3')

    session_title = TextField(text='Session Title: ')
    session_id = TextField(text="Session Id: ")

    version = TextField(text="Version 1.0")
    language = TextField(text="Language: English")

    start_date = TextField("Start date: 01/01/2017")
    end_date = TextField("End date: 01/01/2017")
    duration = TextField("Duration: 1h20m")


class SessionView(TableView):
    model = SessionModel()
    fields = [
              ['session_type', 's1', 's2', 's3'],
              ['session_title', 'session_id'],
              ['version', 'language'],
              ['start_date', 'end_date', 'duration']
             ]
    span = True

    def __init__(self):
        super(SessionView, self).__init__(self)


    def render(self):
        return super().render()


class StudentModel(Model):
    course_title = TextField(text="Course Title")

    start_date = TextField("Start date: 01/07/2017")
    end_date = TextField("End date: 01/07/2017")
    start_time = TextField("Start time: 10:00")
    end_time = TextField("End time: 11:00")

    student_name = TextField("Name: ")
    student_surname = TextField("Surname: ")
    student_infos = TextField("""
                              Workday ID
                              Network ID (internal)
                              Network ID / E-mail
                              Address    (external)
                              """)

    entry_signature = TextField("""
                                Part 1
                                Date + Signature
                                """)

    exit_signature = TextField("""
                               Part 2
                               Date + Signature
                               """)

class StudentView(TableView):
    model = StudentModel()
    span = True
    fields = [
              ['course_title'],
              ['start_date', 'start_time', 'end_date', 'end_time'],
              ['student_name', 'student_surname', 'student_infos',
               'entry_signature', 'exit_signature'],
    ]

    def __init__(self):
        super(StudentView, self).__init__(self)


class InstructorModel(Model):
    instructor = TextField("Instructor: \n Mario Neri")
    internal_bullet = BulletTextField("Internal Insructor")
    external_bullet = BulletTextField("External Instructor")

    instructor_infos = TextField("""Instructor: bla bla bla
                                 Data + Siganture""")

class InstructorView(TableView):
    model = InstructorModel()
    span = True

    fields = [
        ['instructor','internal_bullet','external_bullet'],
        ['instructor_infos']
    ]

    def __init__(self):
        super(InstructorView, self).__init__(self)


class SingInTemplate(SimpleDocTemplate):
    def __init__(self, *args, **kwargs):
        self.header = HeaderView()
        self.info_session = None
        self.info_students = None
        self.info_teacher = None
        return SimpleDocTemplate(*args, **kwargs)


class Story():
    def __init__(self):
        self.workflow = []

    def add(self, item):
        if isinstance(item, list):
            self.workflow.extend(item)
        else:
            self.workflow.append(item)

    def get(self):
        return self.workflow

from reportlab.lib.pagesizes import A4

if __name__ == '__main__':
    doc = SimpleDocTemplate('test.pdf', pagasize=A4)
    story = Story()

    some_space = Spacer(1,10)

    h = HeaderView()

    rendered_fields = h.render()
    story.add(rendered_fields) 

    story.add(some_space)

    s = SessionView()
    rendered_fields = s.render()
    story.add(rendered_fields)

    story.add(some_space)

    u = StudentView()
    students_data = [
        ['Mario','Rossi','','','',''],
        ['Marco','Bianchi','','','', ''],
        ['Giuseppe','Verdi','','','', ''],
        ['','','','','', ''],
    ]
    rendered_fields = u.render(students_data)
    story.add(rendered_fields)

    story.add(some_space)

    i = InstructorView()
    rendered_fields = i.render()
    story.add(rendered_fields)

    doc.build(story.get())

