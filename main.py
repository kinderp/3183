from reportlab.platypus import SimpleDocTemplate
from reportlab.platypus import Table, TableStyle
from reportlab.platypus import Paragraph, Spacer
from reportlab.platypus import Image

from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors

from reportlab.platypus.flowables import Flowable

styles = getSampleStyleSheet()

from abc import ABC, abstractmethod

from models import Model
from views import TableView
from fields import TextField, BulletTextField, ImageField

#class Field(ABC):
#    """
#    Defined here interface for field types 
#    """
#    @abstractmethod
#    def render(self):
#        pass
#
#
#
#class TextField(Field):
#    """
#    Reportlab Paragraph Wrapper
#    """
#    def __init__(self, text='', style=None):
#        self.text = text
#        if style:
#            self.style = style
#        else: 
#            self.style = styles['Normal']
#
#    def render(self):
#        return Paragraph(text=self.text, style=self.style)
#
#
#
#class BulletTextField(TextField):
#    def __init__(self, *args, **kwargs):
#        super(BulletTextField, self).__init__(*args, **kwargs)
#
#    def render(self):
#        return Paragraph(text=self.text, style=self.style, bulletText='[  ]')
#
#
#
#class ImageField(Field):
#    """
#    Reportlab Image Wrapper
#    """
#    def __init__(self, path='', width=None, height=None):
#        self.path = path
#        self.width = width
#        self.height = height
#
#    def render(self):
#        return Image(self.path, width=self.width, height=self.height)
#
#
#class FieldFactory():
#
#    @staticmethod
#    def create(class_name, data):
#
#        if isinstance(data, dict):
#            all_type = {
#                "TextField": TextField(**data),
#                "BulletTextField": BulletTextField(**data),
#                "ImageField": ImageField(**data) 
#            }
#        else:
#            all_type = {
#                "TextField": TextField(*data),
#                "BulletTextField": BulletTextField(*data),
#                "ImageField": ImageField(*data) 
#            }
#
#        return all_type[class_name]
#
#
#
#class Model(ABC):
#    """
#    Defined here interface for model types 
#    """
#    def __init__(self, **kwargs):
#        self.__dict__.update(kwargs)
#
#
#
#class View(ABC):
#
#    def __init__(self, child):
#        self.child = child
#        self.model = child.model
#        self.fields = child.fields
#
#    def render(self):
#        objects = []
#        for elem in dir(self.model):
#            if elem in self.fields:
#                print(elem)
#                cuurent_field = getattr(self.model,elem)
#                objects.insert(0,cuurent_field.render())
#        return objects
#
#
#
#class TableView(View):
#
#    def __init__(self, child):
#
#        self.child = child
#        self.model = child.model
#        self.fields = child.fields
#        self.span = child.span
#        # style is static yet
#        # TO DO: load style dynamically somewhere
#        self.LIST_STYLE_HEADER = TableStyle(
#            [
#            ('BOX', (0,0), (-1,-1), 0.25, colors.black),
#            ('INNERGRID', (0,0), (-1,-1), 0.25, colors.black),
#            ('ALIGN', (0,0), (-1,-1), 'CENTER'),
#            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
#            ]
#            )
#
#        self.LIST_STYLE = TableStyle(
#            [
#            ('BOX', (0,0), (-1,-1), 0.25, colors.black),
#            ('INNERGRID', (0,0), (-1,-1), 0.25, colors.black),
#            ('ALIGN', (0,0), (-1,-1), 'CENTER'),
#            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
#            ]
#            )
#
#        super(TableView, self).__init__(self.child)
#
#    def render(self, data=[]):
#        # render_header return a list (objects)
#        #
#        # - if span == False:
#        #   objects is a list with a single Table (header)
#        #
#        # - if span == True:
#        #   objects is a list of Tables (a table for each header rows)
#        objects = self.render_header()
#        # if data list is empty (no body)
#        # return just the header 
#        if not data:
#            return objects
#        # render_body add a new Table (body table)
#        # with data values filled 
#        return self.render_body(objects, data)
#
#    def render_body(self, header, data):
#        # - append body table in header
#        body_rendered_objects = []
#        body_fields = self.fields[-1]
#        for row in data:
#            new_rendered_row = []
#            for i, field in enumerate(body_fields):
#                current_record = row[i]
#                class_name = getattr(self.model, field).__class__.__name__
#                print(class_name)
#                if isinstance(current_record, dict):
#                    new_body_obj = FieldFactory.create(class_name, current_record)
#                    new_rendered_row.append(new_body_obj.render())
#                else:
#                    new_body_obj = FieldFactory.create(class_name, (current_record,))
#                    new_rendered_row.append(new_body_obj.render())
#            body_rendered_objects.append(new_rendered_row)
#
#        header.append(Table(body_rendered_objects, style=self.LIST_STYLE))
#        return header 
#
#    def render_header(self):
#        objects = []
#
#        for rows in self.fields:
#            new_row = []
#            for elem in rows:
#                if elem:
#                    new_row.append(getattr(self.model, elem).render())
#                else:
#                    new_row.append('')
#
#            if self.span:
#                t = Table([new_row], style=self.LIST_STYLE_HEADER)
#                objects.append(t)
#            else:
#                objects.append(new_row)
#
#        if not self.span:
#            objects = [Table(objects, style=self.LIST_STYLE_HEADER)]
#        return objects
#
# classes used in sanofi exapmle

class HeaderModel(Model):
    def __init__(self,**kwargs):
        """Init custom Model (Header)

        Parameters: 
            kwargs : { '_title': 'Titola centrale', '_session': 'Sessione di prova'}
        """
        super(HeaderModel, self).__init__(**kwargs)
        self.session = TextField(text="{}".format(self._session))
        self.title = TextField(text="{}".format(self._title))
        self.logo = ImageField('./sanofi.png', width=50, height=50)


class HeaderView(TableView):

     def __init__(self, **kwargs):
        self.model = HeaderModel(**kwargs)
        self.fields = [['session', 'title', 'logo']]
        self.span = False

        super(HeaderView, self).__init__(self)

     def render(self):
        return super().render()


class SessionModel(Model):
    def __init__(self, **kwargs):
        """Init custom Model (Session)

        Parameters:
            kwargs : { "_session_type": "Session One",
                       "_s1": "Bullet1",
                       "_s2": "Bullet2",
                       "_s3": "Bullet3",
                       "_session_title": "This is a session title",
                       "_session_id": "1234 session",
                       "_version": "1.0",
                       "_language": "English",
                       "_start_date": "01/01/2017",
                       "_end_date": "01/07/2017",
                       "_duration": "1h20m"
                     }
        """
        super(SessionModel, self).__init__(**kwargs)
        self.session_type = TextField(text="Session Type: {}".format(self._session_type))
        self.s1 = BulletTextField(text='{}'.format(self._s1))
        self.s2 = BulletTextField(text='{}'.format(self._s2))
        self.s3 = BulletTextField(text='{}'.format(self._s3))

        self.session_title = TextField(text='Session Title: {}'.format(self._session_title))
        self.session_id = TextField(text="Session Id: {}".format(self._session_id))

        self.version = TextField(text="Version: {}".format(self._version))
        self.language = TextField(text="Language: {}".format(self._language))

        self.start_date = TextField("Start date: {}".format(self._start_date))
        self.end_date = TextField("End date: {}".format(self._end_date))
        self.duration = TextField("Duration: {}".format(self._duration))


class SessionView(TableView):
    def __init__(self, **kwargs):

        self.model = SessionModel(**kwargs)
        self.fields = [
              ['session_type', 's1', 's2', 's3'],
              ['session_title', 'session_id'],
              ['version', 'language'],
              ['start_date', 'end_date', 'duration']
        ]
        self.span = True

        super(SessionView, self).__init__(self)


    def render(self):
        return super().render()


class StudentModel(Model):
    def __init__(self, **kwargs):
        """Init custom Model (Student)

        Parameters:
            kwargs : { "_course_title": "This is a course title",
                       "_start_date": "01/01/2017",
                       "_start_time": "10:00",
                       "_end_date": "01/01/2017",
                       "_end_time": "11:00"
                     }
        """

        super(StudentModel, self).__init__(**kwargs)
        self.course_title = TextField(text="Course Title: {}".format(self._course_title))

        self.start_date = TextField("Start date: {}".format(self._start_date))
        self.end_date = TextField("End date: {}".format(self._end_date))
        self.start_time = TextField("Start time: {}".format(self._start_time))
        self.end_time = TextField("End time: {}".format(self._end_time))

        self.student_name = TextField("Name")
        self.student_surname = TextField("Surname")
        self.student_infos = TextField("""
                              Workday ID<br/>
                              Network ID (internal)<br/>
                              Network ID / E-mail <br/>
                              Address    (external) <br/>
                              """)

        self.entry_signature = TextField("""
                                Part 1 <br/>
                                Date + Signature
                                """)

        self.exit_signature = TextField("""
                               Part 2 <br/>
                               Date + Signature
                               """)

class StudentView(TableView):

    def __init__(self, **kwargs):
        self. model = StudentModel(**kwargs)
        self.span = True
        self.fields = [
                ['course_title'],
                ['start_date', 'start_time', 'end_date', 'end_time'],
                ['student_name', 'student_surname', 'student_infos',
                 'entry_signature', 'exit_signature'],
        ]

        super(StudentView, self).__init__(self)


class InstructorModel(Model):
    def __init__(self, **kwargs):
        """Init custom Model (Instructor)

        Parameters:
            kwargs : { "_instructor": "Mario Neri",
                       "_internal_bullet": "Internal Instructor",
                       "_external_bullet": "External Instructor",
                       "_instructor_infos": "bla bla bla ..."
                     }
        """

        super(InstructorModel, self).__init__(**kwargs)
        self.instructor = TextField("Instructor: <br/> {}".format(self._instructor))
        self.internal_bullet = BulletTextField("Internal Insructor")
        self.external_bullet = BulletTextField("External Instructor")

        self.instructor_infos = TextField("""Instructor: {} <br/>
                                          Data + Siganture""".format(self._instructor_infos))

class InstructorView(TableView):
    
    def __init__(self, **kwargs):
        self.model = InstructorModel(**kwargs)
        self.span = True

        self.fields = [
            ['instructor','internal_bullet','external_bullet'],
            ['instructor_infos']
        ]

        super(InstructorView, self).__init__(self)

# class used in sing-in sheet example


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

def sanofi():
    doc = SimpleDocTemplate('test.pdf', pagasize=A4)
    story = Story()

    some_space = Spacer(1,10)

    data_header =  { '_title': 'Titola centrale', '_session': 'Sessione di prova'}
    h = HeaderView(**data_header)

    rendered_fields = h.render()
    story.add(rendered_fields) 

    story.add(some_space)

    data_session = { "_session_type": "Session One",
                       "_s1": "Bullet1",
                       "_s2": "Bullet2",
                       "_s3": "Bullet3",
                       "_session_title": "This is a session title",
                       "_session_id": "1234 session",
                       "_version": "1.0",
                       "_language": "English",
                       "_start_date": "01/01/2017",
                       "_end_date": "01/07/2017",
                       "_duration": "1h20m"
    }

    s = SessionView(**data_session)
    rendered_fields = s.render()
    story.add(rendered_fields)

    story.add(some_space)

    data_student = {"_course_title": "This is a course title",
                    "_start_date": "01/01/2017",
                    "_start_time": "10:00",
                    "_end_date": "01/01/2017",
                    "_end_time": "11:00"
    }

    u = StudentView(**data_student)
    students_data = [
        ['Mario','Rossi','','','',''],
        ['Marco','Bianchi','','','', ''],
        ['Giuseppe','Verdi','','','', ''],
        ['','','','','', ''],
    ]

    rendered_fields = u.render(students_data)
    story.add(rendered_fields)

    story.add(some_space)

    data_instructor = {"_instructor": "Mario Neri",
                       "_internal_bullet": "Internal Instructor",
                       "_external_bullet": "External Instructor",
                       "_instructor_infos": "bla bla bla ..."
                      }

    i = InstructorView(**data_instructor)
    rendered_fields = i.render()
    story.add(rendered_fields)

    doc.build(story.get())

if __name__ == '__main__':
    sanofi()
