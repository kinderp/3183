from toet.settings import Setting

from reportlab.lib.units import mm
from reportlab.pdfgen import canvas
from reportlab.platypus import SimpleDocTemplate, Spacer


PAGASIZE = Setting.PAGASIZE
DOC_WIDTH = Setting.DOC_WIDTH
DOC_HEIGHT = Setting.DOC_HEIGHT
DOC_TOP_MARGIN = Setting.DOC_TOP_MARGIN
DOC_BOTTOM_MARGIN = Setting.DOC_BOTTOM_MARGIN
DOC_RIGHT_MARGIN = Setting.DOC_RIGHT_MARGIN
DOC_LEFT_MARGIN = Setting.DOC_LEFT_MARGIN
DOC_WIDTH_REAL = Setting.DOC_WIDTH_REAL
DOC_HEIGHT_REAL = Setting.DOC_HEIGHT_REAL


class Template:
    """
    Parameters:
        kwargs: {
            "header": HeaderView(**some_data),
            "footer" : {
                        'left': 'Left in the footer',
                        'right': 'Right in the footer',
                        'middle': 'Middle in the footer'
                        },
        }
    """

    def __init__(self, **kwargs):
        if 'header' in kwargs:
            self.header_class = kwargs['header']
        else:
            self.header_class = None

        if 'footer' in kwargs:
            self.footer = kwargs['footer']
        else:
            self.footer = None

        self.doc = SimpleDocTemplate('test.pdf', pagasize=Setting.PAGASIZE,
                                     leftMargin=Setting.DOC_LEFT_MARGIN,
                                     rightMargin=Setting.DOC_RIGHT_MARGIN,
                                     bottomMargin=Setting.DOC_BOTTOM_MARGIN,
                                     topMargin=Setting.DOC_TOP_MARGIN)
        self.story = self.Story()


    def build(self):
        if self.header_class and not self.footer:
            self.doc.build(self.story.get(), onFirstPage=self._header,
                           onLaterPages=self._header)
        elif self.header_class and self.footer:
            self.doc.build(self.story.get(), onFirstPage=self._header,
                           onLaterPages=self._header, canvasmaker=self._footer())
        else:
            self.doc.build(self.story.get())

    def _header(self, canvas, doc):
        width, height = doc.pagesize
        rendered_fields = getattr(self.header_class, 'render')()
        for elem in rendered_fields:
            elem.wrapOn(canvas, width, height)
            elem.drawOn(canvas, 0, 790)

    def _footer(self):
        self.Footer.set_data_footer(self.footer)
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

            if 'right' in self.data_footer:
                if self.data_footer['right']:
                    self.drawRightString(200*mm, 20*mm, self.data_footer['right'])
                else:
                    self.drawRightString(200*mm, 20*mm, page)
            if 'middle' in self.data_footer:
                if self.data_footer['middle']:
                    self.drawCentredString(100*mm, 20*mm, self.data_footer['middle'])
                else:
                    self.drawCentredString(100*mm, 20*mm, page)
            if 'left' in self.data_footer:
                if self.data_footer['left']:
                    self.drawString(10*mm, 20*mm, self.data_footer['left'])
                else:
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

