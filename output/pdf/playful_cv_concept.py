"""Generate the one-page playful CV concept.

Edit only the CONTENT block below, then run this file with the bundled Python.
"""

from pathlib import Path

from reportlab.lib.colors import HexColor, Color
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.pdfgen.canvas import Canvas
from reportlab.platypus import Paragraph


HERE = Path(__file__).resolve().parent
BACKGROUND = HERE / "assets" / "playful-cv-background.png"
OUTPUT = HERE / "playful-cv-concept.pdf"


# ---------------------------------------------------------------------------
# EDIT YOUR TEXT HERE
# Keep each description to roughly this length so the one-page layout holds.
# ---------------------------------------------------------------------------
CONTENT = {
    "name": "YOUR NAME",
    "role": "CREATIVE SOFTWARE DEVELOPER",
    "intro": (
        "I like odd ideas, useful software, and the moment a sketch becomes "
        "something people can play with. I build products across web, games "
        "and AI - usually with curiosity switched on."
    ),
    "contact": "you@email.com   /   your-site.dev   /   Berlin, DE",
    "projects": [
        {
            "kicker": "01  PRODUCT + MARKETPLACE",
            "title": "gas.green",
            "subtitle": "A clearer marketplace for green gas",
            "body": (
                "Built a product marketplace that turns a complex energy "
                "domain into a clear, trustworthy journey - from discovery "
                "and comparison to the moment a customer is ready to act."
            ),
            "tags": ["PRODUCT", "MARKETPLACE", "WEB"],
        },
        {
            "kicker": "02  GAME + PROTOTYPING",
            "title": "Mind the sea slug",
            "subtitle": "An Unreal Engine 5 game experiment",
            "body": (
                "An experimental game about mind-controlling a sea slug. "
                "I worked where mechanics, atmosphere and player feedback "
                "meet, turning a strange premise into a readable, playful loop."
            ),
            "tags": ["UE5", "GAMEPLAY", "PROTOTYPING"],
        },
        {
            "kicker": "03  AI + B2B",
            "title": "Agents at work",
            "subtitle": "Product work for an AI agents startup",
            "body": (
                "Helped shape AI-agent experiences for business teams: "
                "translating autonomous workflows into interfaces people "
                "can understand, steer and trust."
            ),
            "tags": ["AI AGENTS", "B2B", "PRODUCT"],
        },
        {
            "kicker": "04  FRONTEND + NDA",
            "title": "Secret missions",
            "subtitle": "Focused builds, experiments and client work",
            "body": (
                "Built frontend experiments, product surfaces and supporting "
                "tools. Some projects stay behind a lock, but I can discuss "
                "the problems, decisions and outcomes at the right level."
            ),
            "tags": ["FRONTEND", "DELIVERY", "NDA"],
        },
    ],
}


INK = HexColor("#12325B")
MUTED = HexColor("#385678")
CORAL = HexColor("#F36F45")
COBALT = HexColor("#2769D8")
GREEN = HexColor("#6BAA38")
VIOLET = HexColor("#7652BA")
IVORY = HexColor("#FFF8E7")


def image_to_page(canvas: Canvas):
    """Cover A4 with the portrait artwork, centered with a tiny vertical crop."""
    page_w, page_h = A4
    image = ImageReader(str(BACKGROUND))
    image_w, image_h = image.getSize()
    scale = max(page_w / image_w, page_h / image_h)
    draw_w, draw_h = image_w * scale, image_h * scale
    x = (page_w - draw_w) / 2
    y = (page_h - draw_h) / 2
    canvas.drawImage(image, x, y, width=draw_w, height=draw_h, mask="auto")
    return image_w, image_h, scale, x, y


def px_box(box, image_h, scale, image_x, image_y):
    """Convert a top-left image-pixel box to a ReportLab point box."""
    x, y, width, height = box
    left = image_x + x * scale
    bottom = image_y + (image_h - y - height) * scale
    return left, bottom, width * scale, height * scale


def draw_paragraph(canvas, html, box, style):
    x, y, width, height = box
    paragraph = Paragraph(html, style)
    used_w, used_h = paragraph.wrap(width, height)
    paragraph.drawOn(canvas, x, y + height - used_h)
    return used_h


def draw_tags(canvas, tags, x, y, colors):
    cursor = x
    for index, tag in enumerate(tags):
        fill = colors[index % len(colors)]
        font = "Helvetica-Bold"
        size = 6.0
        padding_x = 6
        height = 13
        width = stringWidth(tag, font, size) + padding_x * 2
        canvas.setFillColor(fill)
        canvas.roundRect(cursor, y, width, height, height / 2, stroke=0, fill=1)
        canvas.setFillColor(IVORY)
        canvas.setFont(font, size)
        canvas.drawString(cursor + padding_x, y + 4.1, tag)
        cursor += width + 4


def build():
    canvas = Canvas(str(OUTPUT), pagesize=A4, pageCompression=1)
    canvas.setTitle("Playful one-page CV concept")
    canvas.setAuthor(CONTENT["name"])
    image_w, image_h, scale, image_x, image_y = image_to_page(canvas)

    header = px_box((247, 40, 555, 157), image_h, scale, image_x, image_y)
    sections = [
        px_box((66, 248, 446, 221), image_h, scale, image_x, image_y),
        px_box((66, 548, 436, 222), image_h, scale, image_x, image_y),
        px_box((66, 844, 438, 196), image_h, scale, image_x, image_y),
        px_box((70, 1140, 422, 220), image_h, scale, image_x, image_y),
    ]

    # A faint veil keeps the typography calm while preserving the paper texture.
    canvas.saveState()
    canvas.setFillColor(Color(1, 0.98, 0.91, alpha=0.68))
    hx, hy, hw, hh = header
    canvas.roundRect(hx, hy, hw, hh, 15, stroke=0, fill=1)
    for sx, sy, sw, sh in sections:
        canvas.roundRect(sx, sy, sw, sh, 12, stroke=0, fill=1)
    canvas.restoreState()

    hx, hy, hw, hh = header
    canvas.setFillColor(CORAL)
    canvas.setFont("Helvetica-Bold", 7.8)
    canvas.drawString(hx + 12, hy + hh - 18, CONTENT["role"])

    canvas.setFillColor(INK)
    canvas.setFont("Helvetica-Bold", 25)
    canvas.drawString(hx + 12, hy + hh - 43, CONTENT["name"])

    intro_style = ParagraphStyle(
        "intro",
        fontName="Helvetica",
        fontSize=7.8,
        leading=9.6,
        textColor=INK,
        alignment=TA_LEFT,
    )
    draw_paragraph(
        canvas,
        CONTENT["intro"],
        (hx + 12, hy + 29, hw - 24, 39),
        intro_style,
    )
    canvas.setFillColor(MUTED)
    canvas.setFont("Helvetica-Bold", 6.1)
    canvas.drawString(hx + 12, hy + 13, CONTENT["contact"])

    accent_sets = [
        [GREEN, CORAL, COBALT],
        [VIOLET, COBALT, CORAL],
        [COBALT, GREEN, VIOLET],
        [CORAL, COBALT, GREEN],
    ]

    for project, box, tag_colors in zip(CONTENT["projects"], sections, accent_sets):
        x, y, width, height = box
        top = y + height

        canvas.setFillColor(tag_colors[0])
        canvas.setFont("Helvetica-Bold", 6.6)
        canvas.drawString(x + 10, top - 17, project["kicker"])

        canvas.setFillColor(INK)
        canvas.setFont("Helvetica-Bold", 16.2)
        canvas.drawString(x + 10, top - 38, project["title"])

        canvas.setFillColor(MUTED)
        canvas.setFont("Helvetica-Bold", 7.1)
        canvas.drawString(x + 10, top - 52, project["subtitle"])

        body_style = ParagraphStyle(
            f"body-{project['title']}",
            fontName="Helvetica",
            fontSize=7.8,
            leading=10.2,
            textColor=INK,
            alignment=TA_LEFT,
        )
        body_height = max(42, height - 94)
        draw_paragraph(
            canvas,
            project["body"],
            (x + 10, y + 30, width - 20, body_height),
            body_style,
        )
        draw_tags(canvas, project["tags"], x + 10, y + 10, tag_colors)

    canvas.setStrokeColor(INK)
    canvas.setLineWidth(0.7)
    canvas.setDash(1.4, 2.4)
    canvas.line(45, 18, 550, 18)
    canvas.setDash()
    canvas.setFillColor(MUTED)
    canvas.setFont("Helvetica-Bold", 5.4)
    canvas.drawRightString(549, 9, "SELECTED WORK  /  ONE PAGE  /  BUILT WITH CURIOSITY")

    canvas.showPage()
    canvas.save()


if __name__ == "__main__":
    build()
