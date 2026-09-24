"""Build the two keynote poster drafts from reusable, editable layout source.

Requires reportlab, qrcode, Pillow. Run: python3 scripts/build_posters.py
Coordinates are in points, measured from the top of each page.
"""
from io import BytesIO
from pathlib import Path

import qrcode
from reportlab.lib.colors import HexColor
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas

ROOT = Path(__file__).resolve().parents[1]
FONTS = Path('/System/Library/Fonts/Supplemental')
for name, filename in [('Body', 'Arial.ttf'), ('Bold', 'Arial Bold.ttf'),
                       ('Title', 'Georgia Bold.ttf'), ('Italic', 'Georgia Italic.ttf')]:
    pdfmetrics.registerFont(TTFont(name, str(FONTS / filename)))

INK, PAPER, SAGE, RED = '#1e1e1e', '#f4ece3', '#626b5c', '#a94d44'
MUTED, RULE = '#62645f', '#c8c2b9'
THEME = (
    'This conference explores the relationship between '
    'the self and the modern world. We invite reflection on personal '
    'identity, agency, freedom, community, and what it means to live “the good life.” '
    'How do technological, social, political, and religious developments '
    'shape selfhood and human flourishing?'
)
BIO = ('A scholar of Kierkegaard and the existential tradition, Davenport studies '
       'free will, personal identity, autonomy, and virtue ethics. He is a past '
       'president of the Kierkegaard Society USA.')
EMAIL = 'anthony.malagon@qc.cuny.edu'
URL = 'https://beyondfunctionqc.github.io/'


class Poster:
    def __init__(self, size, width, height):
        self.width, self.height = width, height
        self.path = ROOT / 'output/pdf' / f'beyond-function-conference-poster-{size}-keynote.pdf'
        self.c = canvas.Canvas(str(self.path), pagesize=(width, height), pageCompression=1)
        self.c.setTitle(f'Beyond Function - Keynote and Call for Papers ({size})')
        self.c.setAuthor('Queens College Department of Philosophy')
        self.rect(0, 0, width, height, PAPER)

    def rect(self, x, top, w, h, color):
        self.c.setFillColor(HexColor(color))
        self.c.rect(x, self.height-top-h, w, h, fill=1, stroke=0)

    def text(self, text, x, baseline, size=10.5, font='Body', color=INK, shadow=False):
        if shadow:
            self.c.saveState()
            self.c.setFillAlpha(.22)
            self.c.setFillColor(HexColor('#151515'))
            self.c.setFont(font, size)
            self.c.drawString(x+.4, self.height-baseline-.5, text)
            self.c.restoreState()
        self.c.setFont(font, size)
        self.c.setFillColor(HexColor(color))
        self.c.drawString(x, self.height-baseline, text)

    def paragraph(self, text, x, baseline, width, size=10.5, leading=13,
                  color=INK, shadow=False):
        lines, line = [], ''
        for word in text.split():
            trial = f'{line} {word}'.strip()
            if pdfmetrics.stringWidth(trial, 'Body', size) > width:
                lines.append(line)
                line = word
            else:
                line = trial
        if line:
            lines.append(line)
        for i, line in enumerate(lines):
            self.text(line, x, baseline+i*leading, size, color=color, shadow=shadow)
        return baseline + (len(lines)-1)*leading

    def line(self, x1, x2, top, color=RULE, weight=.6):
        self.c.setStrokeColor(HexColor(color))
        self.c.setLineWidth(weight)
        self.c.line(x1, self.height-top, x2, self.height-top)

    def image(self, path, x, top, w, h):
        self.c.drawImage(str(path), x, self.height-top-h, w, h, mask='auto')

    def qr(self, x, top, size):
        code = qrcode.QRCode(border=4)
        code.add_data(URL)
        code.make(fit=True)
        qr = code.make_image(fill_color=INK, back_color=PAPER)
        data = BytesIO()
        qr.save(data, format='PNG')
        data.seek(0)
        self.c.drawImage(ImageReader(data), x, self.height-top-size, size, size)
        self.c.linkURL(URL, (x, self.height-top-size, x+size, self.height-top))

    def finish(self):
        self.c.save()
        print(self.path)


def letter():
    p = Poster('letter', 612, 792)
    p.image(ROOT/'poster-assets/artwork-letter.jpg', 0, 0, 612, 402)
    p.text('QUEENS COLLEGE PHILOSOPHY CONFERENCE', 42, 184, 8, 'Bold', '#ffffff')
    p.text('Beyond', 40, 231, 50, 'Title', '#ffffff', True)
    p.text('Function', 40, 280, 50, 'Title', '#ffffff', True)
    p.text('The Self in the Modern World', 42, 314, 18, 'Italic', '#f4ece3', True)
    end = p.paragraph(THEME, 42, 338, 528, 12.5, 14.5, '#ffffff', True)
    assert end <= 384, end

    p.rect(0, 402, 612, 64, SAGE)
    p.text('DATE AND TIME', 31, 414, 7.2, 'Bold', '#ffffff')
    p.text('NOVEMBER 12, 2026', 31, 432, 16, 'Bold', '#ffffff')
    p.text('8:30 AM - 8:30 PM', 31, 445, 10, color='#ffffff')
    p.text('LOCATION', 313, 414, 7.2, 'Bold', '#ffffff')
    p.text('QUEENS COLLEGE, CUNY', 313, 432, 16, 'Bold', '#ffffff')
    p.text('Dining Hall 120 & 122 (Q-side)', 313, 445, 10, color='#ffffff')
    p.text('65-30 Kissena Boulevard, Flushing, NY 11367', 313, 458, 10, color='#ffffff')

    # Align the portrait to the label's cap height, not its baseline.
    # The full text block has roughly equal padding above and below.
    p.image(ROOT/'assets/john-davenport.jpg', 31, 481, 72, 72)
    p.text('KEYNOTE SPEAKER', 121, 486.5, 7.5, 'Bold', RED)
    p.text('John J. Davenport', 121, 510, 22, 'Title')
    p.text('Professor of Philosophy · Fordham University', 121, 533, 10.5, 'Bold', SAGE)
    end = p.paragraph(BIO, 121, 551, 459, 10.5, 12.5)
    assert end <= 568, end
    p.line(31, 581, 582)

    p.text('CALL FOR PAPERS', 31, 599, 7.3, 'Bold', RED)
    p.text('Submit a Paper', 31, 624, 20.5, 'Title')
    p.paragraph('Students and scholars are invited. Student papers, especially from Queens College students, are encouraged.', 31, 643, 259, 10.5, 13)
    p.text('ABSTRACT', 31, 691, 7.3, 'Bold', SAGE)
    p.paragraph('300-400 words stating the thesis and its relevance to the conference theme.', 101, 691, 189, 10, 12.5)
    p.text('PAPER', 31, 730, 7.3, 'Bold', SAGE)
    p.paragraph('Approximately 3,000 words or 10 double-spaced pages.', 101, 730, 189, 10, 12.5)

    p.text('ABSTRACT SUBMISSION DEADLINE', 325, 599, 7.3, 'Bold', RED)
    p.text('October 21, 2026', 325, 624, 19, 'Title', RED)
    p.line(325, 581, 638, RED, 1)
    p.text('SEND YOUR ABSTRACT', 325, 657, 7.3, 'Bold', SAGE)
    p.text(EMAIL, 325, 675, 10, 'Bold')
    p.c.linkURL('mailto:'+EMAIL, (325, 112, 581, 130))
    p.text('Full call for papers and suggested topics:', 325, 702, 8.3, color=MUTED)
    p.text('beyondfunctionqc.github.io', 325, 718, 9.5, 'Bold')
    p.qr(519, 723, 58)
    p.text('SCAN FOR DETAILS', 325, 746, 7, color=MUTED)

    p.image(ROOT/'poster-assets/qc-logo.png', 31, 761, 87, 21.6)
    p.text('DEPARTMENT OF PHILOSOPHY', 129, 775, 6.2, 'Bold')
    p.text('Artwork: Georges Rochegrosse · Portrait: Fordham faculty profile', 31, 788, 5.7, color=MUTED)
    p.finish()


def tabloid():
    p = Poster('11x17', 792, 1224)
    p.image(ROOT/'poster-assets/artwork-11x17.jpg', 0, 0, 792, 634)
    p.text('QUEENS COLLEGE PHILOSOPHY CONFERENCE', 54, 335, 10, 'Bold', '#ffffff')
    p.text('Beyond', 52, 396, 66, 'Title', '#ffffff', True)
    p.text('Function', 52, 461, 66, 'Title', '#ffffff', True)
    p.text('The Self in the Modern World', 54, 504, 24, 'Italic', '#f4ece3', True)
    end = p.paragraph(THEME, 54, 538, 684, 16.5, 20, '#ffffff', True)
    assert end <= 610, end

    p.rect(0, 634, 792, 80, SAGE)
    p.text('DATE AND TIME', 49, 649, 9.2, 'Bold', '#ffffff')
    p.text('NOVEMBER 12, 2026', 49, 672, 20, 'Bold', '#ffffff')
    p.text('8:30 AM - 8:30 PM', 49, 688, 12.5, color='#ffffff')
    p.text('LOCATION', 414, 649, 9.2, 'Bold', '#ffffff')
    p.text('QUEENS COLLEGE, CUNY', 414, 672, 20, 'Bold', '#ffffff')
    p.text('Dining Hall 120 & 122 (Q-side)', 414, 688, 12.5, color='#ffffff')
    p.text('65-30 Kissena Boulevard, Flushing, NY 11367', 414, 704, 12.5, color='#ffffff')

    p.image(ROOT/'assets/john-davenport.jpg', 49, 735, 90, 90)
    p.text('KEYNOTE SPEAKER', 164, 742, 9.5, 'Bold', RED)
    p.text('John J. Davenport', 164, 773, 29, 'Title')
    p.text('Professor of Philosophy · Fordham University', 164, 803, 13.5, 'Bold', SAGE)
    end = p.paragraph(BIO, 164, 826, 579, 13.5, 17)
    assert end <= 851, end
    p.line(49, 743, 870)

    p.text('CALL FOR PAPERS', 49, 894, 9.5, 'Bold', RED)
    p.text('Submit a Paper', 49, 927, 27, 'Title')
    p.paragraph('Students and scholars are invited. Student papers, especially from Queens College students, are encouraged.', 49, 954, 310, 14, 18)
    p.line(49, 359, 1007)
    p.text('ABSTRACT', 49, 1033, 9.5, 'Bold', SAGE)
    p.paragraph('300-400 words stating the thesis and its relevance to the conference theme.', 143, 1033, 216, 13, 17)
    p.line(49, 359, 1100)
    p.text('PAPER', 49, 1125, 9.5, 'Bold', SAGE)
    p.paragraph('Approximately 3,000 words or 10 double-spaced pages.', 143, 1125, 216, 13, 17)

    p.text('ABSTRACT SUBMISSION DEADLINE', 424, 894, 9.5, 'Bold', RED)
    p.text('October 21, 2026', 424, 927, 25, 'Title', RED)
    p.line(424, 743, 946, RED, 1.3)
    p.text('SEND YOUR ABSTRACT', 424, 973, 9.5, 'Bold', SAGE)
    p.text(EMAIL, 424, 998, 12.5, 'Bold')
    p.c.linkURL('mailto:'+EMAIL, (424, 222, 743, 242))
    p.text('Full call for papers and suggested topics:', 424, 1036, 10.5, color=MUTED)
    p.text('beyondfunctionqc.github.io', 424, 1057, 12.5, 'Bold')
    p.qr(659, 1090, 84)
    p.text('SCAN FOR DETAILS', 424, 1124, 9, color=MUTED)

    p.image(ROOT/'poster-assets/qc-logo.png', 49, 1188, 112, 27.8)
    p.text('DEPARTMENT OF PHILOSOPHY', 177, 1206, 8, 'Bold')
    p.text('Artwork: Georges Rochegrosse · Portrait: Fordham faculty profile', 424, 1206, 6, color=MUTED)
    p.finish()


if __name__ == '__main__':
    letter()
    tabloid()
