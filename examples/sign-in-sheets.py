import os, sys
project_dir =  os.path.realpath(__file__).split("/examples")[0]
sys.path.append(project_dir)

from models import Model
from views import TableView, FormView
from fields import TextField, BulletTextField, ImageField

from reportlab.lib.pagesizes import A4
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

from reportlab.lib.units import mm
from reportlab.pdfgen import canvas

class SingInSheets:
    """

    Parameters:
        kwargs: {
            "_data_header" : { '_sign_in_sheet': 'Titolo centrale' }
            "_data_footer" : { '_vendor_name: 'Vendor Name', '_session_locator': 'Session Locator'}
        }
    """

    def __init__(self, **kwargs):
        self.data_header = kwargs['_data_header']
        self.data_footer = kwargs['_data_footer']

        self.doc = SimpleDocTemplate('test.pdf', pagasize=A4)
        self.story = self.Story()

    def build(self):
        self.doc.build(self.story.get(), onFirstPage=self._header,
                       onLaterPages=self._header, canvasmaker=self._footer())

    def _header(self, canvas, doc):
        width, height = doc.pagesize
        #data_header =  { '_sign_in_sheet': 'Titolo centrale' }
        h = HeaderView(**self.data_header)
        rendered_fields = h.render()
        for elem in rendered_fields:
            elem.wrapOn(canvas, width, height)
            elem.drawOn(canvas, 0, 790)

    def _footer(self):
        self.Footer.set_data_footer(self.data_footer)
        return self.Footer

    class Footer(canvas.Canvas):

        data_footer = None
        @classmethod
        def set_data_footer(cls, data_footer):
            cls.data_footer = data_footer

        def __init__(self, *args, **kwargs):
            """Constructor"""
            canvas.Canvas.__init__(self, *args, **kwargs)
            self.pages = []

        def showPage(self):
            """
            On a page break, add information to the list
            """
            self.pages.append(dict(self.__dict__))
            self._startPage()

        def save(self):
            """
            Add the page number to each page (page x of y)
            """
            page_count = len(self.pages)
            for page in self.pages:
                self.__dict__.update(page)
                self.draw_page_number(page_count)
                canvas.Canvas.showPage(self)

            canvas.Canvas.save(self)

        def draw_page_number(self, page_count):
            """
            Add the page number
            """
            page = "Page %s of %s" % (self._pageNumber, page_count)
            self.setFont("Helvetica", 9)
            self.drawRightString(200*mm, 20*mm,
                                 self.data_footer['_session_locator'])
            self.drawCentredString(100*mm, 20*mm,
                                   self.data_footer['_vendor_name'])
            self.drawString(10*mm, 20*mm, page)


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


#def _header(canvas, doc):
#    width, height = doc.pagesize
#    data_header =  { '_sign_in_sheet': 'Titolo centrale' }
#    h = HeaderView(**data_header)
#    rendered_fields = h.render()
#    import pdb
#    pdb.set_trace()
#    for elem in rendered_fields:
#        elem.wrapOn(canvas, width, height)
#        elem.drawOn(canvas, 0, 790)
#
#class Story():
#
#    def __init__(self):
#        self.workflow = []
#
#    def add(self, item):
#        if isinstance(item, list):
#            self.workflow.extend(item)
#        else:
#            self.workflow.append(item)
#
#    def get(self):
#        return self.workflow
#
#from reportlab.lib.units import mm
#from reportlab.pdfgen import canvas
#
#class PageNumCanvas(canvas.Canvas):
#    def __init__(self, *args, **kwargs):
#        """Constructor"""
#        canvas.Canvas.__init__(self, *args, **kwargs)
#        self.pages = []
#
#    def showPage(self):
#        """
#        On a page break, add information to the list
#        """
#        self.pages.append(dict(self.__dict__))
#        self._startPage()
#
#    def save(self):
#        """
#        Add the page number to each page (page x of y)
#        """
#        page_count = len(self.pages)
#        for page in self.pages:
#            self.__dict__.update(page)
#            self.draw_page_number(page_count)
#            canvas.Canvas.showPage(self)
#
#        canvas.Canvas.save(self)
#
#    def draw_page_number(self, page_count):
#        """
#        Add the page number
#        """
#        page = "Page %s of %s" % (self._pageNumber, page_count)
#        self.setFont("Helvetica", 9)
#        self.drawRightString(200*mm, 20*mm, page)
#        self.drawCentredString(100*mm, 20*mm, page)
#        self.drawString(10*mm, 20*mm, page)
#
#from reportlab.lib.pagesizes import landscape,letter

def make():

    some_space = Spacer(1,10)

    header_footer_data = {
            "_data_header" : { "_sign_in_sheet": "Titolo centrale" },
            "_data_footer" : { "_vendor_name": "Vendor Name",
                               "_session_locator": "Session Locator"
                             }
    }

    pdf = SingInSheets(**header_footer_data)

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
        {"family_name": "family name 1", "first_name": "fitst name", "username": "username", "email": "test@test.it", "phone": "+393331234567", "fax": "+3902123456"},
        {"family_name": "family name 1", "first_name": "fitst name", "username": "username", "email": "test@test.it", "phone": "+393331234567", "fax": "+3902123456"},
        {"family_name": "family name 1", "first_name": "fitst name", "username": "username", "email": "test@test.it", "phone": "+393331234567", "fax": "+3902123456"},
        {"family_name": "family name 1", "first_name": "fitst name", "username": "username", "email": "test@test.it", "phone": "+393331234567", "fax": "+3902123456"},
    ]

    for elem in cell_values:
       instructor_data.append([cell_formatted_text.format(**elem),
                               'AFFILIATION<br/> <br/ <br/> <br/> <br/> <br/> <br/>', '', ''])

    i = InstructorView()
    rendered_fields = i.render(instructor_data)

    pdf.story.add(rendered_fields)

    pdf.build()

def sign_in_sheets():
    doc = SimpleDocTemplate('test.pdf', pagasize=A4)
    story = Story()

    some_space = Spacer(1,10)

    data_header =  { '_sign_in_sheet': 'Titolo centrale' }
    h = HeaderView(**data_header)

    rendered_fields = h.render()
    story.add(rendered_fields)

    story.add(some_space)

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

    session_data = []

    for elem in cell_values:
       session_data.append([cell_formatted_text.format(**elem), '', '', ''])

    rendered_fields = s.render(session_data)
    story.add(rendered_fields)

    story.add(some_space)

    instructor_data = []

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

    doc.build(story.get(), onFirstPage=_header, onLaterPages=_header, canvasmaker=PageNumCanvas)



if __name__ == '__main__':
    #sign_in_sheets()
    make()
