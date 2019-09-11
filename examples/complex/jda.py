import os, sys
project_dir =  os.path.realpath(__file__).split("/examples")[0]
sys.path.append(project_dir)

from toet.models import Model
from toet.views import TableView
from toet.fields import TextField, ImageField
from toet.templates import Template
from toet.settings import Setting

from reportlab.platypus import Spacer
from reportlab.lib.styles import getSampleStyleSheet
styles = getSampleStyleSheet()

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT

Setting.DOC_LEFT_MARGIN = 2
Setting.DOC_RIGHT_MARGIN = 2
Setting.DOC_TOP_MARGIN = 10
Setting.update()

PAGASIZE = Setting.PAGASIZE
DOC_WIDTH = Setting.DOC_WIDTH
DOC_HEIGHT = Setting.DOC_HEIGHT
DOC_TOP_MARGIN = Setting.DOC_TOP_MARGIN
DOC_BOTTOM_MARGIN = Setting.DOC_BOTTOM_MARGIN
DOC_RIGHT_MARGIN = Setting.DOC_RIGHT_MARGIN
DOC_LEFT_MARGIN = Setting.DOC_LEFT_MARGIN
DOC_WIDTH_REAL = Setting.DOC_WIDTH_REAL
DOC_HEIGHT_REAL = Setting.DOC_HEIGHT_REAL


class TitleModel(Model):
    def __init__(self, **kwargs):
        super(TitleModel, self).__init__(**kwargs)

        self.title = TextField("{}".format(self._title))
        self.logo = ImageField('./jda.png', width=80, height=50) 


class TitleView(TableView):
    def __init__(self, **kwargs):
        self.model = TitleModel(**kwargs)
        self.fields = [
            [
                        [   ['title', 'title','title','title', 'logo' ] ]
            ]
        ]
        self.span = True
        self.style_header = {
            "title": {
                "style": "Normal",
                "commands": [
                                ('alignment', TA_CENTER),
                                ('fontName', 'Helvetica'),
                                ('fontSize', 14)

                ]
            }
        }
        super(TitleView, self).__init__(self)


class SessionDetailsModel(Model):
    def __init__(self, **kwargs):
        """Init custom Model (SessionDetails)

        Parameters:
        kwargs: {
                    "_locator_number_value": "3183",
                    "_subject_value": "Learning",
                    "_date_value",
        }
        """
        super(SessionDetailsModel, self).__init__(**kwargs)
        self.session_details = TextField("Session details")

        self.locator_number = TextField("Locator Number:")
        self.locator_number_value = TextField("{}".format(self._locator_number_value))

        self.subject = TextField("Subject:")
        self.subject_value = TextField("{}".format(self._subject_value))

        self.date = TextField("<b>Date:</b>")
        self.date_value = TextField("{}".format(self._date_value))
        self.blank = TextField(" ")


class SessionDetailsView(TableView):
    def __init__(self, **kwargs):
        self.model = SessionDetailsModel(**kwargs)


        self.fields = [
            ['session_details', 'blank', 'blank', 'blank', 'blank'],
            ['locator_number', 'locator_number_value', 'blank', 'blank','blank'],
            ['subject', 'subject_value', 'blank', 'blank', 'blank'],
            ['date', 'date_value', 'blank', 'blank', 'blank'],
        ]

        """
        self.fields = [
            ['session_details', 'blank', 'blank', 'blank',],
            ['locator_number', 'locator_number_value', 'blank','blank'],
            ['subject', 'subject_value', 'blank', 'blank'],
            ['date', 'date_value', 'blank', 'blank'],
        ]
        """
        self.span = False
        self.style_header = {
            "session_details": {
                "style": "Normal",
                "commands": [
                                ('alignment', TA_LEFT),
                                ('fontName', 'Helvetica'),
                                ('fontSize', 10)
                ]
            },
            "locator_number": {
                "style": "Normal",
                "commands": [
                                ('alignment', TA_RIGHT),
                                ('fontName', 'Helvetica'),
                                ('fontSize', 10)
                ]
            },
            "locator_number_value": {
                "style": "Normal",
                "commands": [
                                ('alignment', TA_LEFT),
                                ('fontName', 'Helvetica'),
                                ('fontSize', 10)
                ]
            },
            "subject": {
                "style": "Normal",
                "commands": [
                                ('alignment', TA_RIGHT),
                                ('fontName', 'Helvetica'),
                                ('fontSize', 10)
                ]
            },
            "subject_value": {
                "style": "Normal",
                "commands": [
                                ('alignment', TA_LEFT),
                                ('fontName', 'Helvetica'),
                                ('fontSize', 10)
                ]
            },
            "date": {
                "style": "Normal",
                "commands": [
                                ('alignment', TA_RIGHT),
                                ('fontName', 'Helvetica'),
                                ('fontSize', 10)
                ]
            },
            "date_value": {
                "style": "Normal",
                "commands": [
                                ('alignment', TA_LEFT),
                                ('fontName', 'Helvetica'),
                                ('fontSize', 9.7)
                ]
            }



        }
        super(SessionDetailsView, self).__init__(self)


class SessionPartInfoModel(Model):
    def __init__(self, **kwargs):
        super(SessionPartInfoModel, self).__init__(**kwargs)
        self.locations = TextField("<b>Location:</b>")
        self.locations_value = TextField("{}".format(self._locations_value))
        self.instructor = TextField("<b>Instructor:</b>")
        self.instructor_value = TextField("{}<br/>{}".format(self._instructor_fullname,
                                                          self._instructor_email))
        self.blank = TextField(" ")


class SessionPartInfoView(TableView):
    def __init__(self, **kwargs):
        self.model = SessionPartInfoModel(**kwargs)

        self.fields = [
            ['locations', 'locations_value', 'blank', 'blank', 'blank'],
            ['instructor', 'instructor_value', 'blank', 'blank','blank'],
        ]
        self.span = False
        self.style_header = {
            "locations": {
                "style": "Normal",
                "commands": [
                                ('alignment', TA_RIGHT),
                                ('fontName', 'Helvetica'),
                                ('fontSize', 10)
                ]
            },
            "locations_value": {
                "style": "Normal",
                "commands": [
                                ('alignment', TA_LEFT),
                                ('fontName', 'Helvetica'),
                                ('fontSize', 10)
                ]
            },
            "instructor": {
                "style": "Normal",
                "commands": [
                                ('alignment', TA_RIGHT),
                                ('fontName', 'Helvetica'),
                                ('fontSize', 10)
                ]
            },
            "instructor_value": {
                "style": "Normal",
                "commands": [
                                ('alignment', TA_LEFT),
                                ('fontName', 'Helvetica'),
                                ('fontSize', 10)
                ]
            },

        }
        super(SessionPartInfoView, self).__init__(self)


class SessionPartInstructorSignatureModel(Model):
    def __init__(self, **kwargs):
        super(SessionPartInstructorSignatureModel, self).__init__(**kwargs)

        self.instructor_signature = TextField("Instructor Signature {}".format("_"*24))
        self.blank = TextField(" ")

        self.style_header = {
            "instructor_signature": {
                "style": "Normal",
                "commands": [
                                ('alignment', TA_LEFT),
                                ('fontName', 'Helvetica'),
                                ('fontSize', 10)
                ]
            },
        }


class SessionPartInstructorSignatureView(TableView):
    def __init__(self, **kwargs):
        self.model = SessionPartInstructorSignatureModel(**kwargs)
        self.fields = [
            [
                        [
                            ['instructor_signature', 'instructor_signature', 'blank', 'blank', 'blank'],
                        ],
            ],
        ]
        self.span = True
        super(SessionPartInstructorSignatureView, self).__init__(self)


class SessionPartAttendeeUsersModel(Model):
    def __init__(self, **kwargs):
        super(SessionPartAttendeeUsersModel, self).__init__(**kwargs)
        self.registered_attendees = TextField("Registered Attendees<br/><br/>")
        self.user_id = TextField("User ID<br/><br/>")
        self.company_name = TextField("Company Name<br/><br/>")
        self.email = TextField("Email Address<br/><br/>")
        self.signature = TextField("Signature<br/><br/>")

        self.style_header = {
            "registed_attendees": {
                "style": "Normal",
                "commands": [
                                ('alignment', TA_LEFT),
                                ('fontName', 'Helvetica'),
                                ('fontSize', 10)
                ]
            },
             "user_id": {
                "style": "Normal",
                "commands": [
                                ('alignment', TA_LEFT),
                                ('fontName', 'Helvetica'),
                                ('fontSize', 10)
                ]
            },
             "company_name": {
                "style": "Normal",
                "commands": [
                                ('alignment', TA_LEFT),
                                ('fontName', 'Helvetica'),
                                ('fontSize', 10)
                ]
            },
             "email": {
                "style": "Normal",
                "commands": [
                                ('alignment', TA_LEFT),
                                ('fontName', 'Helvetica'),
                                ('fontSize', 10)
                ]
            },
             "signature": {
                "style": "Normal",
                "commands": [
                                ('alignment', TA_LEFT),
                                ('fontName', 'Helvetica'),
                                ('fontSize', 10)
                ]
            },
          }


class SessionPartAttendeeUsersView(TableView):
    def __init__(self, **kwargs):
        self.model = SessionPartAttendeeUsersModel(**kwargs)
        self.fields = [
            ['registered_attendees', 'user_id', 'company_name', 'email', 'signature']
        ]
        self.span = False
        super(SessionPartAttendeeUsersView, self).__init__(self)


class SessionPartOtherAttendeeUsersModel(Model):
    def __init__(self, **kwargs):
        super(SessionPartOtherAttendeeUsersModel, self).__init__(**kwargs)
        self.other_attendees = TextField("Other Attendees<br/><br/>")
        self.attendee_replaced = TextField("Attendee Replaced<br/><br/>")
        self.company_name = TextField("Company Name<br/><br/>")
        self.email_address = TextField("Email Adreess<br/><br/>")
        self.signature = TextField("Signature<br/><br/>")


class SessionPartOtherAttendeeUsersView(TableView):
    def __init__(self, **kwargs):
        self.model = SessionPartOtherAttendeeUsersModel(**kwargs)
        self.fields = [
                ['other_attendees', 'attendee_replaced', 'company_name',
                 'email_address', 'signature']
        ]
        self.span = False
        super(SessionPartOtherAttendeeUsersView, self).__init__(self)



def make():
    pdf = Template(filename='jda.pdf')
    common_table_style = [
                            ('BOX', (0,0), (-1,-1), 0.1, colors.white),
                            ('INNERGRID', (0,0), (-1,-1), 0.1, colors.white),
                            ('ALIGN', (0,0), (-1,-1), 'CENTER'),
                            ('VALIGN', (0,0), (-1,-1), 'TOP'),
                        ]

    data_title = {
        "_title": "A very long long long but very long title..."
    }
    title = TitleView(**data_title)
    title.set_style([
                            ('BOX', (0,0), (-1,-1), 0.1, colors.white),
                            ('INNERGRID', (0,0), (-1,-1), 0.1, colors.white),
                            ('ALIGN', (0,0), (-1,-1), 'CENTER'),
                            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
                    ]
    )
    rendered_fields = title.render()
    pdf.story.add(rendered_fields)

    some_space = Spacer(1,10)
    pdf.story.add(some_space)

    data_session_details = {
        "_locator_number_value": "3183",
        "_subject_value": "Learning",
        "_date_value": "30/09/2019 - 03/10/2019",
    }
    sess_dets = SessionDetailsView(**data_session_details)
    sess_dets.set_style(common_table_style)
    rendered_fields = sess_dets.render()
    pdf.story.add(rendered_fields)

    some_space = Spacer(1,10)
    pdf.story.add(some_space)

    data_session_part_info = {
        "_locations_value": "Mexico City",
        "_instructor_fullname": "Mario Rossi",
        "_instructor_email": "mrossi@gmail.com"
    }
    sess_part_i = SessionPartInfoView(**data_session_part_info)
    sess_part_i.set_style(common_table_style)
    rendered_fields = sess_part_i.render()
    pdf.story.add(rendered_fields)

    sess_part_sign = SessionPartInstructorSignatureView()
    sess_part_sign.set_style(common_table_style)
    rendered_fields = sess_part_sign.render()
    pdf.story.add(rendered_fields)


    some_space = Spacer(1,10)
    pdf.story.add(some_space)

    attendee_users_table_data = []
    cell_formatted_text = """
                {family_name}<br/>
                {first_name}<br/>
                """
    cell_values = [
        {"family_name": "family name 1", "first_name": "fitst name 1"},
        {"family_name": "family name 2", "first_name": "fitst name 2"},
        {"family_name": "family name 3", "first_name": "fitst name 3"},
        {"family_name": "family name 4", "first_name": "fitst name 4"},
        {"family_name": "family name 5", "first_name": "fitst name 5"},
        {"family_name": "family name 6", "first_name": "fitst name 6"},
        {"family_name": "family name 7", "first_name": "fitst name 7"},
        {"family_name": "family name 8", "first_name": "fitst name 8"},
        {"family_name": "family name 9", "first_name": "fitst name 9"},
        {"family_name": "family name 10", "first_name": "fitst name 10"},
    ]

    for elem in cell_values:
        attendee_users_table_data.append([cell_formatted_text.format(**elem),
                                          '1234abc', 'ACME Labs',
                                          'test@test.org', ''])

    sess_part_users = SessionPartAttendeeUsersView()
    rendered_fields = sess_part_users.render(attendee_users_table_data)
    pdf.story.add(rendered_fields)

    some_space = Spacer(1,10)
    pdf.story.add(some_space)

    sess_part_other_users = SessionPartOtherAttendeeUsersView()
    other_attendee_user_tale_data = [[TextField("<br/>"),TextField("<br/>"),TextField("<br/>"),TextField("<br/>"),TextField("<br/>"),]for elem in range(0,10)]
    other_attendee_user_tale_data = [["<br/><br/>", "<br/><br/>", "<br/><br/>",
                                      "<br/><br/>",
                                      "<br/><br/>",] for elem in range(0,10)]
    rendered_fields = sess_part_other_users.render(other_attendee_user_tale_data)
    pdf.story.add(rendered_fields)
    pdf.build()

if __name__ == '__main__':
    make()
