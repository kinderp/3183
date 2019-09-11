import os, sys
project_dir =  os.path.realpath(__file__).split("/examples")[0]
sys.path.append(project_dir)

from toet.models import Model
from toet.views import TableView, TableViewHeaderOrFooter, FormView
from toet.fields import TextField, BulletTextField, ImageField

from reportlab.platypus import Spacer
from reportlab.lib.styles import getSampleStyleSheet
styles = getSampleStyleSheet()

from toet.settings import Setting
from toet.templates import Template

PAGASIZE = Setting.PAGASIZE
DOC_WIDTH = Setting.DOC_WIDTH
DOC_HEIGHT = Setting.DOC_HEIGHT
DOC_TOP_MARGIN = Setting.DOC_TOP_MARGIN
DOC_BOTTOM_MARGIN = Setting.DOC_BOTTOM_MARGIN
DOC_RIGHT_MARGIN = Setting.DOC_RIGHT_MARGIN
DOC_LEFT_MARGIN = Setting.DOC_LEFT_MARGIN
DOC_WIDTH_REAL = Setting.DOC_WIDTH_REAL
DOC_HEIGHT_REAL = Setting.DOC_HEIGHT_REAL


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


class HeaderView(TableViewHeaderOrFooter):

     def __init__(self, **kwargs):
        self.model = HeaderModel(**kwargs)
        self.fields = ['logo_vendor', 'sign_in_sheet', 'logo_company']
        self.style_header = {
            "sign_in_sheet": {
                "style": "Normal",
                "commands": [
                                ('alignment', TA_CENTER),
                                ('fontName', 'Helvetica'),
                                ('fontSize', 18),
                ]
            }
        }
        super(HeaderView, self).__init__(self)


class SummaryModel(Model):

    def __init__(self, **kwargs):
        """Init custom Model (Summary)

        Parameters:
            kwargs : {
                        "_event_name": "Nome evento",
                        "_session_id": "1234abc",
                        "_vendor": "ACME Labs",
                        "_start_date": "01/01/2017",
                        "_end_date": "01/01/2017",
                        "_parts": "1",
                        "_locations": "Location1, Location2",
                        "_available_languages": ""

            }

        """
        super(SummaryModel, self).__init__(**kwargs)
        self.event_name_and_session_id = TextField("{} - {}".format(self._event_name, self._session_id))
        self.vendor = TextField("{}".format(self._vendor))
        self.start_and_end_date_parts = TextField("<b>From:</b> {} <b>to:</b>{}(<b>Parts:</b> {})".format(self._start_date,
                                                                                                        self._end_date,
                                                                                                        self._parts))
        self.locations = TextField("<b>Location(s):</b> {}".format(self._locations))
        self.available_languages = TextField("<b>Available Language(s):</b>{}".format(self._available_languages))


from reportlab.lib.enums import TA_CENTER, TA_LEFT


class SummaryView(FormView):
    def __init__(self, **kwargs):
        self.model = SummaryModel(**kwargs)
        self.fields = [
                        ['event_name_and_session_id'],
                        ['vendor'],
                        ['start_and_end_date_parts'],
                        ['locations'],
                        ['available_languages']
        ]

        self.styles = {
            'event_name_and_session_id': {
                'style': 'Normal',
                'space': 4.5,
                'commands': [
                                ('alignment', TA_CENTER),
                                ('fontName', 'Helvetica'),
                                ('fontSize', 18),
                            ]
            },
            'vendor': {
                'style': 'Normal',
                'commands': [
                                ('alignment', TA_CENTER),
                                ('fontSize', 12),
                            ],
                'space': 4.5,
            },
            'start_and_end_date_parts': {
                'style': 'Normal',
                'commands': [
                                ('alignment', TA_LEFT),
                                ('fontSize', 8),
                            ]
            },
            'locations': {
                'style': 'Normal',
                'commands': [
                                ('alignment', TA_LEFT),
                                ('fontSize', 8),
                            ]
            },
            'available_languages':{
                'style': 'Normal',
                'commands': [
                                ('alignment', TA_LEFT),
                                ('fontSize', 8),
                            ]
            }
        }

        super(SummaryView, self).__init__(self)


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

        self.participants = TextField("<b>Participants</b>")
        self.signatures = TextField("<b>SIGNATURES</b>")

        self.part1 = TextField("<i>Part 1</i>")
        self.part2 = TextField("<i>Part 2</i>")

        self.observations = TextField("<i>Observations</i>")


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
        self.style_header = {
            "participants": {
                "style": "Normal",
                "commands": [
                                ('alignment', TA_CENTER),
                                ('fontSize', 12),
                ]
            },
            "signatures": {
                "style": "Normal",
                "commands": [
                                ('alignment', TA_CENTER),
                                ('fontSize', 12),
                ]
            },
            "part1": {
                "style": "Normal",
                "commands": [
                                ('alignment', TA_CENTER),
                                ('fontSize', 12),
                ]
            },
            "part2": {
                "style": "Normal",
                "commands": [
                                ('alignment', TA_CENTER),
                                ('fontSize', 12),
                ]
            },

            "observations": {
                "style": "Normal",
                "commands": [
                                ('alignment', TA_CENTER),
                ]
            },
        }
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
        self.instructors = TextField("<b>INSTRUCTOR(s)</b>")
        self.signatures = TextField("<b>SIGNATURES</b>")
        self.part1 = TextField("<i>Part 1</i>")
        self.part2 = TextField("<i>Part 2</i>")
        self.affiliation = TextField("<i>AFFILIATION</i>")


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
        self.style_header = {
                            "instructors": {
                                            "style": "Normal",
                                            "commands": [
                                                        ('alignment', TA_CENTER),
                                                        ('fontName', 'Helvetica'),
                                                        ('fontSize', 8),
                                                        ]
                            },
                            "signatures": {
                                            "style": "Normal",
                                            "commands": [
                                                        ('alignment', TA_CENTER),
                                                        ('fontName', 'Helvetica'),
                                                        ('fontSize', 14),
                                                        ]
                            },
                            "part1": {
                                            "style": "Normal",
                                            "commands": [
                                                        ('alignment', TA_CENTER),
                                                        ('fontName', 'Helvetica'),
                                                        ('fontSize', 4),
                                                        ]
                            },
                            "part2": {
                                            "style": "Normal",
                                            "commands": [
                                                        ('alignment', TA_CENTER),
                                                        ('fontName', 'Helvetica'),
                                                        ('fontSize', 4),
                                                        ]
                            },

        }

        self.body_header = ['instructors', 'affiliation', 'part1', 'part2']

        super(InstructorView, self).__init__(self)


def make():

    some_space = Spacer(1,10)

    data_header = {
                    "_sign_in_sheet": "Titolo centrale" ,
    }
    header = HeaderView(**data_header)

    footer = {
                "left": "",
                "right": "Vendor name",
                "middle": "Session Locator"
    }

    pdf = Template(header=header, footer=footer, filename='sign-in-sheets.pdf')

    data_summary = {
                        "_event_name": "Nome evento",
                        "_session_id": "1234abc",
                        "_vendor": "ACME Labs",
                        "_start_date": "01/01/2017",
                        "_end_date": "01/01/2017",
                        "_parts": "1",
                        "_locations": "Location1, Location2",
                        "_available_languages": ""
    }

    s_ = SummaryView(**data_summary)
    rendered_fields = s_.render()
    pdf.story.add(rendered_fields)

    pdf.story.add(some_space)

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
                <b>{family_name}</b><br/>
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
        {"family_name": "family name 7", "first_name": "fitst name", "username": "username", "email": "test@test.it", "division": "division"},
        {"family_name": "family name 8", "first_name": "fitst name", "username": "username", "email": "test@test.it", "division": "division"},
        {"family_name": "family name 9", "first_name": "fitst name", "username": "username", "email": "test@test.it", "division": "division"},
        {"family_name": "family name 10", "first_name": "fitst name", "username": "username", "email": "test@test.it", "division": "division"},
    ]

    s = SessionView(**data_session)

    session_data = []

    for elem in cell_values:
       session_data.append([cell_formatted_text.format(**elem), '', '', ''])

    rendered_fields = s.render(session_data)
    pdf.story.add(rendered_fields)

    pdf.story.add(some_space)

    instructor_data = []

    cell_formatted_text = """
                <b>{family_name}</b><br/>
                {first_name}<br/>
                {username}<br/>
                {email}<br/>
                {phone}<br/>
                {fax}<br/>
                """
    cell_values = [
        {"family_name": "family name 1", "first_name": "fitst name", "username": "username", "email": "test@test.it", "phone": "+393331234567", "fax": "+3902123456"},
        {"family_name": "family name 2", "first_name": "fitst name", "username": "username", "email": "test@test.it", "phone": "+393331234567", "fax": "+3902123456"},
        {"family_name": "family name 3", "first_name": "fitst name", "username": "username", "email": "test@test.it", "phone": "+393331234567", "fax": "+3902123456"},
        {"family_name": "family name 4", "first_name": "fitst name", "username": "username", "email": "test@test.it", "phone": "+393331234567", "fax": "+3902123456"},
        {"family_name": "family name 5", "first_name": "fitst name", "username": "username", "email": "test@test.it", "phone": "+393331234567", "fax": "+3902123456"},
        {"family_name": "family name 6", "first_name": "fitst name", "username": "username", "email": "test@test.it", "phone": "+393331234567", "fax": "+3902123456"},
        {"family_name": "family name 7", "first_name": "fitst name", "username": "username", "email": "test@test.it", "phone": "+393331234567", "fax": "+3902123456"},
        {"family_name": "family name 8", "first_name": "fitst name", "username": "username", "email": "test@test.it", "phone": "+393331234567", "fax": "+3902123456"},
        {"family_name": "family name 9", "first_name": "fitst name", "username": "username", "email": "test@test.it", "phone": "+393331234567", "fax": "+3902123456"},
        {"family_name": "family name 10", "first_name": "fitst name", "username": "username", "email": "test@test.it", "phone": "+393331234567", "fax": "+3902123456"},
        {"family_name": "family name 11", "first_name": "fitst name", "username": "username", "email": "test@test.it", "phone": "+393331234567", "fax": "+3902123456"},
        {"family_name": "family name 12", "first_name": "fitst name", "username": "username", "email": "test@test.it", "phone": "+393331234567", "fax": "+3902123456"},
    ]

    for elem in cell_values:
       instructor_data.append([cell_formatted_text.format(**elem),
                               'AFFILIATION<br/> <br/ <br/> <br/> <br/> <br/> <br/>', '', ''])

    i = InstructorView()
    rendered_fields = i.render(instructor_data)

    pdf.story.add(rendered_fields)

    pdf.build()



if __name__ == '__main__':
    make()
