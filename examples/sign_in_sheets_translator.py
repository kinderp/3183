import os, sys
project_dir =  os.path.realpath(__file__).split("/examples")[0]
sys.path.append(project_dir)

from toet.models import Model
from toet.views import TableView, TableViewHeaderOrFooter, FormView
from toet.fields import TextField, BulletTextField, ImageField

from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Spacer
from reportlab.lib.styles import getSampleStyleSheet
styles = getSampleStyleSheet()

from toet.settings import PAGASIZE
from toet.settings import DOC_WIDTH, DOC_HEIGHT
from toet.settings import DOC_TOP_MARGIN, DOC_BOTTOM_MARGIN
from toet.settings import DOC_RIGHT_MARGIN, DOC_LEFT_MARGIN
from toet.settings import DOC_WIDTH_REAL, DOC_HEIGHT_REAL
from toet.utils import Translator

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

    __t = {
        "_t_from" : "From",
        "_t_to" : "To",
        "_t_parts" : "Parts",
        "_t_locations" : "Locations",
        "_t_available_languages" : "Available Languages",
    }

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
        super(SummaryModel, self)._('SummaryModel', SummaryModel.__t)
        self.event_name_and_session_id = TextField("<b>{} - {}</b>".format(self._event_name, self._session_id))
        self.vendor = TextField("<b>{}</b>".format(self._vendor))
        self.start_and_end_date_parts = TextField("<b>{}:</b> {} <b>{}:</b> {} (<b>{}:</b> {})".format(
                                                                                                        self._t_from,
                                                                                                        self._start_date,
                                                                                                        self._t_to,
                                                                                                        self._end_date,
                                                                                                        self._t_parts,
                                                                                                        self._parts
                                                                                                       )
        )

        self.locations = TextField("<b>{}:</b> {}".format(self._t_locations, self._locations))
        self.available_languages = TextField("<b>{}:</b> {}".format(self._t_available_languages, self._available_languages))


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

    __t = {
        "_t_starts" : "Starts",
        "_t_end" : "End",
        "_t_break" : "Breaks",
        "_t_sesion_location" : "Session Location",
        "_t_participants": "Participants",
        "_t_signatures": "SIGNATURES",
        "_t_part": "Part",
        "_t_observations": "Observations",
    }

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
        super(SessionModel, self)._('SessionModel', SessionModel.__t)
        #text_for_session = """
        #<b>{session_part_title}</b><br/>
        #<b>Starts:</b> {session_date_time} {timezone} <b>End:</b>
        #{end_date_time} {timezone} <b>Break:</b> {break} <br/>
        #<br/>
        #<b>Session Location:</b> {session_location}
        #"""

        text_for_session = """
        <b>{session_part_title}</b><br/>
        <b>{_t_starts}:</b> {session_date_time} {timezone} <b>{_t_end}:</b>
        {end_date_time} {timezone} <b>{_t_break}:</b> {break} <br/>
        <br/>
        <b>{_t_sesion_location}:</b> {session_location}
        """

        self._session.update(self._t)

        self.session = TextField(text_for_session.format(**self._session))

        #self.participants = TextField("<b>Participants</b>")
        #self.signatures = TextField("<b>SIGNATURES</b>")

        #self.part1 = TextField("<i>Part 1</i>")
        #self.part2 = TextField("<i>Part 2</i>")

        #self.observations = TextField("<i>Observations</i>")

        self.participants = TextField("<b>{}</b>".format(self._t_participants))
        self.signatures = TextField("<b>{}</b>".format(self._t_signatures))

        self.part1 = TextField("<i>{} 1</i>".format(self._t_part))
        self.part2 = TextField("<i>{} 2</i>".format(self._t_part))

        self.observations = TextField("<i>{}</i>".format(self._t_observations))


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

    __t = {
        "_t_instructors": "INSTRUCTORS",
        "_t_signatures": "SIGNATURES",
        "_t_part": "Part",
        "_t_affiliation": "AFFILIATION",
    }

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
        super(InstructorModel, self)._('InstructorModel', InstructorModel.__t)
        self.instructors = TextField("<b>{}</b>".format(self._t_instructors))
        self.signatures = TextField("<b>{}</b>".format(self._t_signatures))
        self.part1 = TextField("<i>{} 1</i>".format(self._t_part))
        self.part2 = TextField("<i>{} 2</i>".format(self._t_part))
        self.affiliation = TextField("<i>{}</i>".format(self._t_affiliation))


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
            "_doc_name": "test.pdf"
            "_data_header" : { '_sign_in_sheet': 'Titolo centrale' },
            "_data_footer" : { '_vendor_name: 'Vendor Name',
                               '_session_locator': 'Session Locator'},
                             },
        }
    """

    def __init__(self, **kwargs):
        self.data_header = kwargs['_data_header']
        self.data_footer = kwargs['_data_footer']
        self.doc = SimpleDocTemplate(kwargs['_doc_name'], pagasize=PAGASIZE,
                                     leftMargin=DOC_LEFT_MARGIN,
                                     rightMargin=DOC_RIGHT_MARGIN,
                                     bottomMargin=DOC_BOTTOM_MARGIN,
                                     topMargin=DOC_TOP_MARGIN)
        """
        self.doc = SimpleDocTemplate('test.pdf', pagasize=PAGASIZE,
                                     leftMargin=DOC_LEFT_MARGIN,
                                     rightMargin=DOC_RIGHT_MARGIN)
        """
        self.story = self.Story()


    def build(self):
        self.doc.build(self.story.get(), onFirstPage=self._header,
                       onLaterPages=self._header, canvasmaker=self._footer())

    def _header(self, canvas, doc):
        width, height = doc.pagesize
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

def make(doc_name, src, dest):

    # Below an example of a real time translation in rendering phase.
    # There are two functions for realtime translations:
    # (1) translate_from_web(), (2) bulk_translate_from_web().
    #
    # The latter one is always preferable for obvious
    # performance reasons and to avoid ip banning by google.
    #
    # Note obj=True, it is a useful trick:
    # if obj is set to False (default) a translate call
    # returns a dict with the same keys of the original dict
    # but with values translated in dest lang.
    # (e.g.)
    # BEFORE TRANSLATION:
    #                   dynamic__t = { '_t_affiliation' : 'AFFILIATION' }
    # AFTER TRANSLATION:
    #                   dynamic__t = { '_t_affiliation' : 'AFFILIAZOINE' }
    #
    # if obj is set to True, it will return an object where
    # attributes are the keys of the orgin dict.
    # (e.g.)
    # BEFORE TRANSLATION:
    #                   dynamic__t = { '_t_affiliation' : 'AFFILIATION' }
    # AFTER TRANSLATION:
    #                   dynamic__t._t_affiliation -> 'AFFILIAZOINE'

    dynamic__t = { '_t_affiliation' : 'AFFILIATION' }
    dynamic__t = Translator(src=src, dest=dest, disk=False,
                            write=False,
                            translation_dir=None).bulk_translate_from_web(dynamic__t,
                                                                          obj=True)
    # you can access your translated vars in this way:
    # dynamic__t._t_affiliation

    some_space = Spacer(1,10)

    data = {
            "_doc_name": doc_name,
            "_data_header" : { "_sign_in_sheet": "Titolo centrale" },
            "_data_footer" : { "_vendor_name": "Vendor Name",
                               "_session_locator": "Session Locator"
                             },
    }

    pdf = SingInSheets(**data)

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
                               '{}<br/> <br/ <br/> <br/> <br/> <br/><br/>'.format(dynamic__t._t_affiliation), '', ''])

    i = InstructorView()
    rendered_fields = i.render(instructor_data)

    pdf.story.add(rendered_fields)

    pdf.build()


if __name__ == '__main__':
    # This example uses pre generated translations vocabularies.
    # Vocabularies are translations for __t class attribute in your code.
    # See vocabularies_generator.py in examples/ dir of this project for
    # an example on how to create vocabularies files; README on this project
    # contains more detailed informations about translation process.

    # In order to set toet for translations from disk (using vocabularies) you
    # need four variables in your env
    #
    # TOET_LOAD_VOCABULARIES = 1
    # TOET_TRANSLATIONS_DIR = '/somewhere/in/your/disk'
    # TOET_SRC_LANG = 'en'
    # TOET_DEST_LANG = 'it'
    #
    # First one is obvious, second one is the dir where you have saved your
    # vocabularies. (see vocabularies_generator.py in examples/ )
    # The last two are source and destination languages of your translation
    list_langs = [
                    ('en','it'),
    ]
    for lang in list_langs:
        os.environ['TOET_LOAD_VOCABULARIES'] = "1"
        os.environ['TOET_TRANSLATIONS_DIR'] = "/home/antonio/dev/sign_in_sheet/translations"
        os.environ['TOET_SRC_LANG'] = lang[0]
        os.environ['TOET_DEST_LANG'] = lang[1]
        make("{}_{}_test.pdf".format(*lang), *lang)
