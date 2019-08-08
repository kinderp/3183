import os, sys
project_dir =  os.path.realpath(__file__).split("/examples")[0]
test_dir = os.path.dirname(os.path.realpath(__file__))
sys.path.append(project_dir)

from models import Model
from views import TableView
from fields import TextField, BulletTextField, ImageField

from reportlab.platypus import SimpleDocTemplate, Spacer
from reportlab.lib.styles import getSampleStyleSheet
styles = getSampleStyleSheet() 

class HeaderModel(Model):
    def __init__(self,**kwargs):
        """Init custom Model (Header)

        Parameters: 
            kwargs : { '_sign_in_sheet': 'Titolo centrale' }
        """
        super(HeaderModel, self).__init__(**kwargs)
        self.sign_in_sheet = TextField(text="{}".format(self._sign_in_sheet))
        self.logo_vendor = ImageField('./sanofi.png', width=50, height=50)
        self.logo_company = ImageField('./sanofi.png', width=50, height=50)


class HeaderView(TableView):

     def __init__(self, **kwargs):
        self.model = HeaderModel(**kwargs)
        self.fields = [['logo_vendor', 'sign_in_sheet', 'logo_company']]
        self.span = False

        super(HeaderView, self).__init__(self)


class SessionModel(Model):
    def __init__(self, **kwargs):
        """Init custom Model (Session)

        Parameters:
            kwargs : { "_session": {
                            "session_part_title": "Session Part Title",
                            "session_date_time": "01/01/2017 10:00",
                            "timezone": "UTC+2",
                            "end_date_time": "01/01/2017 11:00",
                            "break": "...",
                            "session_location". "somewhere"
                        }
                     }
        """
        super(SessionModel, self).__init__(**kwargs)
        text_for_session = """
        {session_part_title}<br/>
        Starts: {session_date_time} {timezone} End: {end_date_time} {timezone} Break: {break} <br/>
        <br/>
        Session Location: {session_location}
        """
        self.session = TextField(text_for_session.format(**self._session))

        self.participants = TextField("Participants")
        self.signatures = TextField("SIGNATURES")

        self.part1 = TextField("Part 1")
        self.part2 = TextField("Part 2")

        self.observations = TextField("Observations")


class SessionView(TableView):
    def __init__(self, **kwargs):

        self.model = SessionModel(**kwargs)
        self.fields = [
              ['session'],
              [
                  [
                    ['participants', 'signatures', 'signatures', 'observations'],
                    ['participants', 'part1', 'part2', 'observations']
                  ],
              ],
        ]
        self.span = True

        super(SessionView, self).__init__(self)

class InstructorModel(Model):
     def __init__(self, **kwargs):
        """Init custom Model (Instructor)

        Parameters:
            kwargs : { "_session": {
                            "session_part_title": "Session Part Title",
                            "session_date_time": "01/01/2017 10:00",
                            "timezone": "UTC+2",
                            "end_date_time": "01/01/2017 11:00",
                            "break": "...",
                            "session_location". "somewhere"
                        }
                     }
        """
        super(InstructorModel, self).__init__(**kwargs)
        self.instructors = TextField("INSTRUCTOR(s)")
        self.signatures = TextField("SIGNATURES")
        self.part1 = TextField("Part 1")
        self.part2 = TextField("Part 2")
        self.affiliation = TextField("AFFILIATION")

class InstructorView(TableView):
    def __init__(self, **kwargs):

        self.model = InstructorModel(**kwargs)
        self.fields = [
            [
                  [
                    ['instructors', 'instructors', 'signatures', 'signatures'],
                    ['instructors', 'instructors', 'part1', 'part2']
                  ],
            ]
        ]
        self.span = True
        self.body_header = ['instructors', 'affiliation', 'part1', 'part2']

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

def sign_in_sheets():
    doc = SimpleDocTemplate('test.pdf', pagasize=A4)
    story = Story()

    some_space = Spacer(1,10)

    data_header =  { '_sign_in_sheet': 'Titolo centrale' }
    h = HeaderView(**data_header)

    rendered_fields = h.render()
    story.add(rendered_fields)

    story.add(some_space)

    data_session =  { "_session": {
                            "session_part_title": "Session Part Title",
                            "session_date_time": "01/01/2017 10:00",
                            "timezone": "UTC+2",
                            "end_date_time": "01/01/2017 11:00",
                            "break": "...",
                            "session_location": "somewhere"
                        }
                     }

    cell_formatted_text = """
                {family_name}<br/>
                {first_name}<br/>
                {username}<br/>
                {email}<br/>
                Division: {division}<br/>
                """
    cell_values = [
        {"family_name": "family name 1", "first_name": "fitst name", "username": "username", "email": "test@test.it", "division": "division"},
        {"family_name": "family name 2", "first_name": "fitst name", "username": "username", "email": "test@test.it", "division": "division"},
        {"family_name": "family name 3", "first_name": "fitst name", "username": "username", "email": "test@test.it", "division": "division"},
        {"family_name": "family name 4", "first_name": "fitst name", "username": "username", "email": "test@test.it", "division": "division"},
        {"family_name": "family name 5", "first_name": "fitst name", "username": "username", "email": "test@test.it", "division": "division"},
        {"family_name": "family name 6", "first_name": "fitst name", "username": "username", "email": "test@test.it", "division": "division"},
    ]


    s = SessionView(**data_session)

    session_data = [
    ]
    for elem in cell_values:
       session_data.append([cell_formatted_text.format(**elem), '', '', ''])

    rendered_fields = s.render(session_data)
    story.add(rendered_fields)

    story.add(some_space)

    instructor_data = [
    ]


    cell_formatted_text = """
                {family_name}<br/>
                {first_name}<br/>
                {username}<br/>
                {email}<br/>
                {phone}<br/>
                {fax}<br/>
                """
    cell_values = [
        {"family_name": "family name 1", "first_name": "fitst name", "username": "username", "email": "test@test.it", "phone": "+393331234567", "fax": "+3902123456"},
        {"family_name": "family name 1", "first_name": "fitst name", "username": "username", "email": "test@test.it", "phone": "+393331234567", "fax": "+3902123456"},
        {"family_name": "family name 1", "first_name": "fitst name", "username": "username", "email": "test@test.it", "phone": "+393331234567", "fax": "+3902123456"},
        {"family_name": "family name 1", "first_name": "fitst name", "username": "username", "email": "test@test.it", "phone": "+393331234567", "fax": "+3902123456"},
        {"family_name": "family name 1", "first_name": "fitst name", "username": "username", "email": "test@test.it", "phone": "+393331234567", "fax": "+3902123456"},
    ]

    for elem in cell_values:
       instructor_data.append([cell_formatted_text.format(**elem), '', '', ''])


    i = InstructorView()
    rendered_fields = i.render(instructor_data)


    story.add(rendered_fields)

    doc.build(story.get())

if __name__ == '__main__':
    sign_in_sheets()
