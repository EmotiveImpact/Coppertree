#!/usr/bin/env python3
"""Build the three Copper Tree story and colouring books from reviewed sources."""
from pathlib import Path
from html import escape
import argparse
import json

from reportlab import rl_config
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.utils import ImageReader
from reportlab.platypus import Paragraph
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

rl_config.useA85 = 0

ROOT = Path(__file__).resolve().parents[1]
WIDTH, HEIGHT = A4
MARGIN = 43
CONTENT = WIDTH - 2 * MARGIN


def register_fonts():
    folder = Path('/usr/share/fonts/truetype/dejavu')
    for name, filename in [('Body', 'DejaVuSans.ttf'), ('Bold', 'DejaVuSans-Bold.ttf'), ('Display', 'DejaVuSerif-Bold.ttf')]:
        pdfmetrics.registerFont(TTFont(name, str(folder / filename)))


def paragraph(pdf, text, x, top, width, size=16, leading=24, font='Body', align=0):
    style = ParagraphStyle('text', fontName=font, fontSize=size, leading=leading, alignment=align, textColor='#171717')
    content = escape(text).replace('\n', '<br/>')
    item = Paragraph(content, style)
    _, height = item.wrap(width, HEIGHT)
    if top - height < 45:
        raise ValueError(f'Text crosses page footer: {text[:70]}')
    item.drawOn(pdf, x, top - height)
    return top - height


def small_label(pdf, text, y):
    pdf.setFont('Bold', 9)
    pdf.drawString(MARGIN, y, text.upper())


def footer(pdf, page):
    pdf.setStrokeColorRGB(.7, .7, .7)
    pdf.setLineWidth(.5)
    pdf.line(MARGIN, 34, WIDTH - MARGIN, 34)
    pdf.setFillColorRGB(.3, .3, .3)
    pdf.setFont('Body', 8)
    pdf.drawString(MARGIN, 22, 'COPPER TREE | Read, colour and create')
    pdf.drawRightString(WIDTH - MARGIN, 22, str(page))
    pdf.setFillColorRGB(0, 0, 0)


def fitted_image(pdf, path, x, y, width, height):
    reader = ImageReader(str(path))
    iw, ih = reader.getSize()
    scale = min(width / iw, height / ih)
    w, h = iw * scale, ih * scale
    pdf.drawImage(reader, x + (width - w) / 2, y + (height - h) / 2, width=w, height=h, mask='auto')


def draw_box(pdf, top, bottom=65):
    if top - bottom < 170:
        raise ValueError('Activity drawing area is too small')
    pdf.setLineWidth(.9)
    pdf.setStrokeColorRGB(.4, .4, .4)
    pdf.roundRect(MARGIN, bottom, CONTENT, top - bottom, 12, stroke=1, fill=0)
    pdf.setStrokeColorRGB(0, 0, 0)


def cover(pdf, book, number, image):
    small_label(pdf, f'Copper Tree / Book {number}', HEIGHT - 49)
    bottom = paragraph(pdf, book['title'], MARGIN, HEIGHT - 81, CONTENT, 29, 36, 'Display')
    bottom = paragraph(pdf, book.get('subtitle') or 'A story and colouring adventure', MARGIN, bottom - 17, CONTENT, 13, 19)
    fitted_image(pdf, image, MARGIN, 115, CONTENT, bottom - 139)
    paragraph(pdf, 'A story to share. A world to make your own.', MARGIN, 94, CONTENT, 12, 18, align=1)
    paragraph(pdf, 'Created by Emotive Impact', MARGIN, 66, CONTENT, 10, 14, align=1)
    pdf.showPage()


def welcome(pdf, number):
    small_label(pdf, 'Welcome to Copper Tree', HEIGHT - 49)
    y = paragraph(pdf, 'You are part of the adventure.', MARGIN, HEIGHT - 80, CONTENT, 27, 34, 'Display')
    y = paragraph(pdf, 'Meet six friends who live in Copper Tree. They ask questions, make things, make mistakes and help each other. There is room for you too.', MARGIN, y - 22, CONTENT, 16, 25)
    pairs = [('Amara', 'An artist with wonderfully big ideas.'), ('Kofi', 'An inventor who loves figuring things out.'), ('Zuri', 'An explorer with a question for everything.'), ('Eli', 'A playful friend who loves a good game.'), ('Nia', 'A gardener who notices the little things.'), ('Tayo', 'A dreamer who keeps looking up.')]
    y -= 30
    for name, description in pairs:
        y = paragraph(pdf, name, MARGIN, y, CONTENT, 14, 20, 'Bold')
        y = paragraph(pdf, description, MARGIN, y - 3, CONTENT, 13, 20) - 13
    y = paragraph(pdf, 'Read together or on your own. After every two story pages, there is a picture to colour. Use the drawing spaces for your own ideas. You can tell someone your answer instead of writing it.', MARGIN, y - 6, CONTENT, 13, 20)
    paragraph(pdf, 'Grown-ups: print at actual size on A4 paper. Single-sided printing is helpful for colouring. Try pencils or crayons first. Place scrap paper underneath if using felt-tip pens.', MARGIN, 115, CONTENT, 10, 15)
    footer(pdf, 2)
    pdf.showPage()


def story_page(pdf, part, index, page):
    small_label(pdf, f'The story / {index + 1:02d}', HEIGHT - 49)
    y = paragraph(pdf, part['heading'], MARGIN, HEIGHT - 79, CONTENT, 25, 32, 'Display')
    y = paragraph(pdf, part['text'], MARGIN, y - 21, CONTENT, 16, 25)
    y -= 29
    y = paragraph(pdf, 'Your turn', MARGIN, y, CONTENT, 13, 18, 'Bold')
    y = paragraph(pdf, part['activity'], MARGIN, y - 8, CONTENT, 13, 20)
    draw_box(pdf, y - 18)
    footer(pdf, page)
    pdf.showPage()


def colour_page(pdf, image, scene, page):
    small_label(pdf, f'Colour Copper Tree / Scene {scene}', HEIGHT - 49)
    fitted_image(pdf, image, 31, 62, WIDTH - 62, HEIGHT - 139)
    footer(pdf, page)
    pdf.showPage()


def closing_page(pdf, title, prompt, page):
    small_label(pdf, 'Make your mark', HEIGHT - 49)
    y = paragraph(pdf, title, MARGIN, HEIGHT - 81, CONTENT, 27, 34, 'Display')
    y = paragraph(pdf, prompt, MARGIN, y - 24, CONTENT, 16, 25)
    draw_box(pdf, y - 27)
    footer(pdf, page)
    pdf.showPage()


def build(number):
    source = ROOT / 'books' / f'book{number}.json'
    book = json.loads(source.read_text())
    if len(book['pages']) != 12:
        raise ValueError(f'{source} must contain twelve story parts')
    images = [ROOT / 'assets' / 'books' / f'book{number}' / f'scene{index}.png' for index in range(1, 7)]
    for path in images:
        if not path.is_file():
            raise FileNotFoundError(path)
    output = ROOT / 'output' / 'pdf' / f'Copper-Tree-Book-{number}.pdf'
    output.parent.mkdir(parents=True, exist_ok=True)
    pdf = canvas.Canvas(str(output), pagesize=A4, pageCompression=1)
    pdf.setTitle(book['title'])
    pdf.setAuthor('Emotive Impact')
    pdf.setSubject('Copper Tree story, colouring and drawing book for children')
    cover(pdf, book, number, images[0])
    welcome(pdf, number)
    page = 3
    for scene in range(6):
        for index in (scene * 2, scene * 2 + 1):
            story_page(pdf, book['pages'][index], index, page)
            page += 1
        colour_page(pdf, images[scene], scene + 1, page)
        page += 1
    closing_page(pdf, 'A place for you', 'Draw yourself with the Copper Tree friends. Where would you meet? What would you bring to share?', page)
    closing_page(pdf, 'What happens next?', 'Invent another adventure. Draw the first thing the friends discover. Give your adventure a name, or tell someone your story.', page + 1)
    pdf.save()
    return output


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--book', type=int, choices=(1, 2, 3))
    args = parser.parse_args()
    register_fonts()
    for number in ([args.book] if args.book else (1, 2, 3)):
        print(build(number))
