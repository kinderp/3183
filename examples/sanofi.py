import os, sys
project_dir =  os.path.realpath(__file__).split("/examples")[0]
sys.path.append(project_dir)

from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate
from reportlab.platypus import Spacer
from reportlab.lib.styles import getSampleStyleSheet

styles = getSampleStyleSheet()

from models import Model
from views import TableView
from fields import TextField, BulletTextField, ImageField


class HeaderModel(Model):

    def __init__(self,**kwargs):
        """Init custom Model (Header)

        Parameters: 
            kwargs : { '_title': 'Titolo centrale', '_session': 'Sessione di prova'}
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

"""
class SingInTemplate(SimpleDocTemplate):
    def __init__(self, *args, **kwargs):
        self.header = HeaderView()
        self.info_session = None
        self.info_students = None
        self.info_teacher = None
        return SimpleDocTemplate(*args, **kwargs)
"""

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


def sanofi():
    doc = SimpleDocTemplate('test.pdf', pagasize=A4)
    story = Story()

    some_space = Spacer(1,10)

    data_header =  { '_title': 'Titolo centrale', '_session': 'Sessione di prova'}
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
