from pathlib import Path

from reportlab.lib.colors import HexColor
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.pdfgen import canvas


OUTPUT = Path(__file__).with_name("pixel_cv_concept.pdf")

# Edit this block to replace the placeholder copy.
CONTENT = {
    "name": "YOUR NAME",
    "role": "PRODUCT BUILDER / CREATIVE DEVELOPER",
    "location": "Berlin, DE",
    "email": "hello@yourname.dev",
    "intro": (
        "I build playful, useful digital products - from marketplaces and AI tools "
        "to strange game mechanics. I like turning ambitious ideas into clear experiences."
    ),
    "projects": [
        {
            "index": "01",
            "eyebrow": "MARKETPLACE",
            "title": "gas.green",
            "body": (
                "Built a marketplace that makes lower-carbon fuel choices easier to discover "
                "and act on. I worked across product thinking, flows and interface details."
            ),
            "tags": "PRODUCT  /  UX  /  FRONT END",
            "scene": "market",
        },
        {
            "index": "02",
            "eyebrow": "UE5 GAME",
            "title": "Mind over mollusc",
            "body": (
                "A game about mind-controlling a sea slug. Built in Unreal Engine 5, with the "
                "central mechanic, atmosphere and underwater world developed together."
            ),
            "tags": "UE5  /  GAMEPLAY  /  PROTOTYPING",
            "scene": "slug",
        },
        {
            "index": "03",
            "eyebrow": "B2B STARTUP",
            "title": "AI agents",
            "body": (
                "Worked on agentic tools for business teams, turning messy workflows into "
                "clear, testable product experiences across AI behavior and interface."
            ),
            "tags": "AI  /  PRODUCT  /  SYSTEMS",
            "scene": "agent",
        },
        {
            "index": "04",
            "eyebrow": "SELECTED WORK",
            "title": "Front ends + NDA",
            "body": (
                "Shipped focused front-end work and contributed to projects I cannot name yet. "
                "I can discuss my role, decisions and lessons at the right level."
            ),
            "tags": "UI  /  DELIVERY  /  COLLABORATION",
            "scene": "nda",
        },
    ],
}


PAPER = HexColor("#F4F0E6")
INK = HexColor("#18231F")
MUTED = HexColor("#5E6A63")
LINE = HexColor("#C8C9B8")
MOSS = HexColor("#A8C45A")
SEA = HexColor("#50A99C")
CORAL = HexColor("#F27E62")
GOLD = HexColor("#E8B64B")
WHITE = HexColor("#FFFDF7")


def wrap_text(text, font, size, width):
    words = text.split()
    lines = []
    current = ""
    for word in words:
        trial = word if not current else f"{current} {word}"
        if stringWidth(trial, font, size) <= width:
            current = trial
        else:
            lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def draw_paragraph(c, text, x, y, width, font="Helvetica", size=8.35, leading=11.2, color=INK):
    c.setFont(font, size)
    c.setFillColor(color)
    for line in wrap_text(text, font, size, width):
        c.drawString(x, y, line)
        y -= leading
    return y


def pixel(c, x, y, size, color):
    c.setFillColor(color)
    c.rect(round(x), round(y), size, size, stroke=0, fill=1)


def pixel_person(c, x, y, scale=3.0, shirt=SEA, facing=1, pose="stand"):
    # Coordinates are a tiny 8 x 12 sprite, expanded as crisp vector squares.
    skin = HexColor("#D99A70")
    dark = INK
    grid = [
        (2, 10, dark), (3, 10, dark), (4, 10, dark),
        (1, 9, dark), (2, 9, skin), (3, 9, skin), (4, 9, skin),
        (1, 8, dark), (2, 8, skin), (3, 8, skin), (4, 8, skin),
        (2, 7, skin), (3, 7, skin),
        (1, 6, shirt), (2, 6, shirt), (3, 6, shirt), (4, 6, shirt),
        (1, 5, shirt), (2, 5, shirt), (3, 5, shirt), (4, 5, shirt),
        (2, 4, shirt), (3, 4, shirt),
        (2, 3, dark), (3, 3, dark),
    ]
    if pose == "carry":
        grid += [(0, 6, skin), (5, 6, skin), (0, 5, skin), (5, 5, skin)]
    elif pose == "point":
        arm_x = 5 if facing == 1 else 0
        grid += [(arm_x, 6, skin), (arm_x + facing, 6, skin)]
    elif pose == "build":
        grid += [(0, 5, skin), (5, 4, skin)]
    else:
        grid += [(0, 6, skin), (5, 6, skin)]
    grid += [(1, 2, dark), (4, 2, dark), (1, 1, dark), (4, 1, dark)]
    for gx, gy, color in grid:
        px = gx if facing == 1 else 5 - gx
        pixel(c, x + px * scale, y + gy * scale, scale, color)


def draw_coin(c, x, y, scale=3):
    for gx, gy in [(1, 0), (2, 0), (0, 1), (3, 1), (0, 2), (3, 2), (1, 3), (2, 3)]:
        pixel(c, x + gx * scale, y + gy * scale, scale, INK)
    for gx, gy in [(1, 1), (2, 1), (1, 2), (2, 2)]:
        pixel(c, x + gx * scale, y + gy * scale, scale, GOLD)


def draw_leaf(c, x, y, scale=3):
    for gx, gy in [(0, 2), (1, 1), (1, 2), (2, 0), (2, 1), (2, 2), (3, 0), (3, 1)]:
        pixel(c, x + gx * scale, y + gy * scale, scale, MOSS)
    pixel(c, x + 3 * scale, y - scale, scale, INK)


def draw_slug(c, x, y, scale=3):
    dark = INK
    body = SEA
    cells = [
        (0, 1, dark), (1, 1, body), (2, 1, body), (3, 1, body),
        (4, 1, body), (5, 1, body), (6, 1, body), (7, 1, dark),
        (2, 2, body), (3, 2, body), (4, 2, body), (5, 2, body), (6, 2, body),
        (5, 3, body), (6, 3, body), (6, 4, body),
        (5, 5, dark), (7, 5, dark),
    ]
    for gx, gy, color in cells:
        pixel(c, x + gx * scale, y + gy * scale, scale, color)


def draw_robot(c, x, y, scale=3):
    cells = [
        (1, 6, INK), (2, 6, INK), (3, 6, INK), (4, 6, INK),
        (0, 5, INK), (1, 5, WHITE), (2, 5, WHITE), (3, 5, WHITE), (4, 5, WHITE), (5, 5, INK),
        (0, 4, INK), (1, 4, SEA), (2, 4, WHITE), (3, 4, SEA), (4, 4, WHITE), (5, 4, INK),
        (0, 3, INK), (1, 3, WHITE), (2, 3, WHITE), (3, 3, WHITE), (4, 3, WHITE), (5, 3, INK),
        (1, 2, INK), (2, 2, INK), (3, 2, INK), (4, 2, INK),
        (1, 1, INK), (4, 1, INK), (0, 0, INK), (5, 0, INK),
    ]
    for gx, gy, color in cells:
        pixel(c, x + gx * scale, y + gy * scale, scale, color)
    pixel(c, x + 2 * scale, y + 7 * scale, scale, INK)
    pixel(c, x + 2 * scale, y + 8 * scale, scale, CORAL)


def draw_crate(c, x, y, scale=3):
    for gx in range(7):
        for gy in range(5):
            edge = gx in (0, 6) or gy in (0, 4)
            pixel(c, x + gx * scale, y + gy * scale, scale, INK if edge else GOLD)
    for i in range(1, 5):
        pixel(c, x + i * scale, y + i * scale, scale, INK)
        pixel(c, x + (6 - i) * scale, y + i * scale, scale, INK)
    c.setFillColor(INK)
    c.setFont("Courier-Bold", 6)
    c.drawCentredString(x + 10.5, y + 6, "NDA")


def draw_scene(c, kind, x, y):
    # Scene sits in the top-right of each card.
    if kind == "market":
        c.setStrokeColor(INK)
        c.setLineWidth(1)
        c.line(x + 42, y + 2, x + 42, y + 34)
        c.line(x + 68, y + 2, x + 68, y + 34)
        c.setFillColor(MOSS)
        c.rect(x + 39, y + 24, 32, 9, stroke=1, fill=1)
        draw_person = pixel_person
        draw_person(c, x + 2, y, scale=2.4, shirt=CORAL, facing=1, pose="carry")
        draw_coin(c, x + 24, y + 12, scale=2.2)
        draw_leaf(c, x + 51, y + 10, scale=2.2)
    elif kind == "slug":
        pixel_person(c, x + 1, y, scale=2.4, shirt=GOLD, facing=1, pose="point")
        draw_slug(c, x + 43, y + 2, scale=2.8)
        c.setStrokeColor(CORAL)
        c.setLineWidth(1.6)
        c.setDash(2, 2)
        c.bezier(x + 21, y + 28, x + 38, y + 47, x + 53, y + 41, x + 60, y + 27)
        c.setDash()
        pixel(c, x + 35, y + 36, 3, CORAL)
    elif kind == "agent":
        pixel_person(c, x + 1, y, scale=2.4, shirt=MOSS, facing=1, pose="build")
        draw_robot(c, x + 49, y + 1, scale=2.7)
        c.setStrokeColor(LINE)
        c.setLineWidth(1)
        c.line(x + 25, y + 16, x + 45, y + 16)
        c.line(x + 34, y + 16, x + 34, y + 32)
        draw_coin(c, x + 29, y + 32, scale=1.5)
    elif kind == "nda":
        pixel_person(c, x + 2, y, scale=2.4, shirt=SEA, facing=1, pose="carry")
        draw_crate(c, x + 44, y + 4, scale=3)
        c.setStrokeColor(MUTED)
        c.setLineWidth(1)
        c.setDash(1, 2)
        c.line(x + 27, y + 13, x + 42, y + 13)
        c.setDash()


def draw_card(c, x, y, width, height, project):
    c.setFillColor(WHITE)
    c.setStrokeColor(LINE)
    c.setLineWidth(0.8)
    c.roundRect(x, y, width, height, 7, stroke=1, fill=1)

    c.setFillColor(INK)
    c.rect(x, y + height - 26, 27, 26, stroke=0, fill=1)
    c.setFillColor(PAPER)
    c.setFont("Courier-Bold", 8.3)
    c.drawCentredString(x + 13.5, y + height - 17, project["index"])

    c.setFillColor(MUTED)
    c.setFont("Courier-Bold", 6.7)
    c.drawString(x + 36, y + height - 17, project["eyebrow"])

    draw_scene(c, project["scene"], x + width - 94, y + height - 69)

    c.setFillColor(INK)
    c.setFont("Helvetica-Bold", 15)
    c.drawString(x + 17, y + height - 58, project["title"])

    draw_paragraph(
        c,
        project["body"],
        x + 17,
        y + height - 84,
        width - 34,
        font="Helvetica",
        size=8.1,
        leading=10.8,
        color=INK,
    )

    c.setStrokeColor(LINE)
    c.setLineWidth(0.6)
    c.line(x + 17, y + 25, x + width - 17, y + 25)
    c.setFillColor(MUTED)
    c.setFont("Courier-Bold", 6.1)
    c.drawString(x + 17, y + 12, project["tags"])

    # One intentionally "loose" pixel at the corner makes the system feel assembled.
    accent = [MOSS, CORAL, SEA, GOLD][int(project["index"]) - 1]
    pixel(c, x + width - 8, y - 3, 6, accent)


def build():
    width, height = A4
    c = canvas.Canvas(str(OUTPUT), pagesize=A4)
    c.setTitle("Pixel CV concept")
    c.setAuthor(CONTENT["name"])
    c.setSubject("One-page personal CV concept")
    c.setFillColor(PAPER)
    c.rect(0, 0, width, height, stroke=0, fill=1)

    margin = 38
    top = height - 34

    # Top status bar.
    c.setFillColor(INK)
    c.roundRect(margin, top - 16, 83, 16, 8, stroke=0, fill=1)
    c.setFillColor(PAPER)
    c.setFont("Courier-Bold", 6.6)
    c.drawCentredString(margin + 41.5, top - 11, "PLAYER PROFILE")
    c.setFillColor(MUTED)
    c.setFont("Courier", 6.5)
    status = f"{CONTENT['location']}  /  AVAILABLE FOR GOOD QUESTS"
    c.drawRightString(width - margin, top - 11, status)

    # Identity.
    c.setFillColor(INK)
    c.setFont("Helvetica-Bold", 30)
    c.drawString(margin, top - 55, CONTENT["name"])
    c.setFillColor(SEA)
    c.setFont("Courier-Bold", 9)
    c.drawString(margin + 2, top - 73, CONTENT["role"])

    # A small running crew builds the heading underline.
    crew_x = width - margin - 91
    pixel_person(c, crew_x, top - 82, scale=2.4, shirt=CORAL, facing=1, pose="carry")
    c.setFillColor(INK)
    c.rect(crew_x + 27, top - 68, 15, 4, stroke=0, fill=1)
    c.setFillColor(GOLD)
    c.rect(crew_x + 42, top - 68, 15, 4, stroke=0, fill=1)
    c.setFillColor(MOSS)
    c.rect(crew_x + 57, top - 68, 15, 4, stroke=0, fill=1)

    # Intro.
    c.setFillColor(INK)
    c.setFont("Helvetica-Bold", 8)
    c.drawString(margin, top - 104, "INTRO /")
    draw_paragraph(
        c,
        CONTENT["intro"],
        margin + 48,
        top - 104,
        width - (margin * 2) - 48,
        font="Helvetica",
        size=9.1,
        leading=12.4,
        color=INK,
    )

    # Quest path, intentionally simple and sparse.
    path_y = top - 145
    c.setStrokeColor(LINE)
    c.setLineWidth(1)
    c.line(margin, path_y, width - margin, path_y)
    c.setFillColor(INK)
    c.setFont("Courier-Bold", 6.5)
    c.drawString(margin, path_y + 6, "SELECTED QUESTS")
    for i, color in enumerate([MOSS, CORAL, SEA, GOLD]):
        px = margin + 120 + i * 36
        pixel(c, px, path_y - 3, 7, color)
        if i < 3:
            c.setStrokeColor(LINE)
            c.setDash(2, 3)
            c.line(px + 8, path_y + 0.5, px + 34, path_y + 0.5)
            c.setDash()

    # Project grid.
    gap = 12
    card_width = (width - margin * 2 - gap) / 2
    card_height = 192
    row_1_y = path_y - 17 - card_height
    row_2_y = row_1_y - gap - card_height
    positions = [
        (margin, row_1_y),
        (margin + card_width + gap, row_1_y),
        (margin, row_2_y),
        (margin + card_width + gap, row_2_y),
    ]
    for (x, y), project in zip(positions, CONTENT["projects"]):
        draw_card(c, x, y, card_width, card_height, project)

    # Footer inventory bar.
    footer_y = 38
    c.setStrokeColor(INK)
    c.setLineWidth(1.2)
    c.line(margin, footer_y + 19, width - margin, footer_y + 19)
    c.setFillColor(INK)
    c.setFont("Courier-Bold", 6.5)
    c.drawString(margin, footer_y + 7, "INVENTORY:")
    c.setFont("Courier", 6.5)
    c.drawString(margin + 55, footer_y + 7, "PRODUCT THINKING  UX/UI  PROTOTYPING  FRONT END  UE5  AI")
    c.setFont("Courier-Bold", 6.5)
    c.drawRightString(width - margin, footer_y + 7, CONTENT["email"])

    # Tiny continuation marker, like the edge of a level.
    pixel(c, width - margin - 4, 17, 4, INK)
    pixel(c, width - margin + 1, 17, 4, SEA)
    c.showPage()
    c.save()


if __name__ == "__main__":
    build()
