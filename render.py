#!/usr/bin/env python3
"""Draw entry.png for make.fun news-image-20261124.

A one-day newspaper front page for Tuesday 24 November 2026: Nvidia
reinstates Jensen Huang, a U.S. jury convicts Huawei, mines hit tankers in
the Strait of Hormuz, Ukraine strikes Russian ships, a Turkish military
helicopter crashes, and Britain warns of Russian sabotage. Everything is
drawn with PIL shapes and DejaVu fonts, so the text stays crisp; the
render is deterministic (same script, same bytes).
"""
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (248, 245, 238)
INK = (22, 26, 32)
TEAL = (14, 59, 59)
RED = (172, 32, 32)
GREEN = (34, 120, 66)
GREY = (96, 96, 96)
CARD = (255, 255, 255)
EDGE = (205, 198, 180)
FAINT = (236, 231, 220)

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def F(path, size):
    return ImageFont.truetype(path, size)


def wrap(d, text, fnt, max_w):
    """Greedy word wrap returning a list of lines that fit max_w."""
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if d.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def para(d, x, y, text, fnt, fill, max_w, leading=5):
    for line in wrap(d, text, fnt, max_w):
        d.text((x, y), line, font=fnt, fill=fill)
        y += fnt.size + leading
    return y


def centred(d, cx, y, text, fnt, fill):
    w = d.textlength(text, font=fnt)
    d.text((cx - w / 2, y), text, font=fnt, fill=fill)
    return y + fnt.size


img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img)

# ---------- masthead ----------
d.rectangle([0, 0, W, 130], fill=TEAL)
d.rectangle([0, 130, W, 136], fill=RED)
centred(d, W // 2, 16, "THE WORLD IN ONE DAY", F(SERIF_B, 56), (255, 255, 255))
centred(d, W // 2, 86, "TUESDAY  ·  24 NOVEMBER 2026", F(SANS_B, 30), (232, 214, 160))

# ---------- lead story: Nvidia ----------
y = 158
d.text((40, y), "TOP STORY", font=F(SANS_B, 24), fill=RED)
y += 36
y = para(d, 40, y, "HUANG IS BACK AT NVIDIA", F(SERIF_B, 42), INK, 600, leading=2)
y += 6
deck = ("The board reinstates Jensen Huang as chief executive less than two "
        "weeks after he resigned, after Donald Trump pressed for his return. "
        "Nvidia shares jump about 30% and Wall Street rebounds with them.")
y = para(d, 40, y, deck, F(SANS, 24), INK, 600, leading=4)

# rising-bars chart icon, right of the lead story
bx, by = 700, 190
bars = [(0, 46), (34, 34), (68, 56), (102, 22), (136, 40), (170, 8)]
for i, (dx, bh) in enumerate(bars):
    d.rectangle([bx + dx, by + 120 - bh, bx + dx + 26, by + 120], fill=GREEN)
d.line([bx - 12, by + 132, bx + 208, by + 132], fill=INK, width=3)
d.line([(bx - 6, by + 96), (bx + 52, by + 62), (bx + 108, by + 74),
        (bx + 168, by + 30), (bx + 200, by + 12)], fill=RED, width=6)
d.polygon([(bx + 200, by + 12), (bx + 178, by + 8), (bx + 196, by + 34)], fill=RED)
d.text((bx - 4, by + 146), "WALL STREET RALLIES", font=F(SANS_B, 21), fill=GREY)

d.line([40, 446, 984, 446], fill=INK, width=3)
d.line([40, 452, 984, 452], fill=INK, width=1)

# ---------- story cards, 2 x 2 ----------
def icon_gavel(d, x, y, c):
    d.rectangle([x + 6, y + 44, x + 66, y + 58], fill=c)
    d.rectangle([x + 30, y + 58, x + 42, y + 66], fill=c)
    d.line([x + 36, y + 8, x + 36, y + 66], fill=c, width=5)
    d.rectangle([x + 14, y, x + 58, y + 12], fill=c)


def icon_mine(d, x, y, c):
    # tanker hull with a spiked mine above it
    d.ellipse([x + 18, y, x + 54, y + 36], fill=c)
    for dx, dy in ((-6, 18), (42, -6), (42, 42), (66, 18)):
        d.line([x + 36, y + 18, x + dx + 18, y + dy], fill=c, width=4)
    d.polygon([(x + 2, y + 44), (x + 70, y + 44), (x + 60, y + 62),
               (x + 12, y + 62)], fill=c)
    d.line([x, y + 68, x + 72, y + 68], fill=c, width=4)


def icon_drone(d, x, y, c):
    d.line([x + 10, y + 10, x + 62, y + 62], fill=c, width=5)
    d.line([x + 62, y + 10, x + 10, y + 62], fill=c, width=5)
    for cx, cy in ((10, 10), (62, 10), (10, 62), (62, 62)):
        d.ellipse([x + cx - 10, y + cy - 10, x + cx + 10, y + cy + 10],
                  outline=c, width=4)
    d.rectangle([x + 28, y + 28, x + 44, y + 44], fill=c)


def icon_heli(d, x, y, c):
    d.line([x + 4, y + 12, x + 68, y + 12], fill=c, width=5)
    d.ellipse([x + 14, y + 26, x + 52, y + 52], fill=c)
    d.polygon([(x + 52, y + 32), (x + 70, y + 40), (x + 52, y + 46)], fill=c)
    d.line([x + 30, y + 52, x + 30, y + 66], fill=c, width=5)
    d.line([x + 20, y + 66, x + 42, y + 66], fill=c, width=5)


def icon_shield(d, x, y, c):
    d.polygon([(x + 6, y + 6), (x + 66, y + 6), (x + 66, y + 34),
               (x + 36, y + 68), (x + 6, y + 34)], outline=c, width=5)
    d.text((x + 26, y + 18), "!", font=F(SANS_B, 34), fill=c)


icons = {"gavel": icon_gavel, "mine": icon_mine, "drone": icon_drone,
         "heli": icon_heli, "shield": icon_shield}

cards = [
    ("HUAWEI FOUND GUILTY", RED,
     "A U.S. jury convicts the Chinese tech giant of stealing trade secrets "
     "and bank fraud, but clears it of racketeering.", "gavel"),
    ("MINES IN THE HORMUZ STRAIT", RED,
     "Four tankers hit mines and catch fire; Iran's Revolutionary Guard says "
     "it attacked a container ship and refuses talks.", "mine"),
    ("UKRAINE HITS RUSSIAN SHIPS", TEAL,
     "Sea drones strike a Russian cargo ship in the Gulf of Finland and a "
     "warship off Libya, Kyiv confirms.", "drone"),
    ("BRITAIN WARNS OF SABOTAGE", TEAL,
     "The defence ministry and MI5 issue a rare public alert: firms that "
     "supply Ukraine face a higher Russian sabotage risk.", "shield"),
]

gx, gy = 40, 478
cw, chh = 462, 196
for i, (head, color, body, kind) in enumerate(cards):
    x = gx + (i % 2) * (cw + 20)
    yy = gy + (i // 2) * (chh + 16)
    d.rectangle([x, yy, x + cw, yy + chh], fill=CARD, outline=EDGE, width=2)
    d.rectangle([x, yy, x + 10, yy + chh], fill=color)  # left colour bar
    icons[kind](d, x + 26, yy + 22, color)
    hx = x + 112
    para(d, hx, yy + 22, head, F(SANS_B, 23), INK, cw - 128, leading=2)
    d.line([x + 26, yy + 96, x + cw - 16, yy + 96], fill=FAINT, width=2)
    para(d, x + 26, yy + 106, body, F(SANS, 20), (52, 52, 52), cw - 42, leading=3)

# ---------- second lead strip: helicopter crash ----------
hy = 906
d.rectangle([40, hy, 984, hy + 2], fill=INK)
para(d, 40, hy + 12,
     "ALSO:  Turkish helicopter crash kills five  ·  Senegal regain the AFCON title  ·  "
     "5.6 quake hits Nepal  ·  COP31 talks collapse",
     F(SANS_B, 21), INK, 944, leading=2)
centred(d, W // 2, 978,
        "Sources: Reuters · AP · Daily Summary Of · 10 Things  —  24 November 2026",
        F(SANS, 19), GREY)

img.save("entry.png", optimize=True)
print("saved entry.png", img.size)
