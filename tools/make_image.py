"""Draws entry.png: a one-page front page of the world news of Thursday 19 November 2026.

Run once on a machine with Pillow (the entry itself needs nothing):
    python tools/make_image.py
main.py copies the committed entry.png to /output at grading time.
Every picture here is drawn from simple shapes in this file.
"""
import math
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

S = 2                      # draw at 2x, then downsample for clean edges
W = H = 1024
FONTS = Path("C:/Windows/Fonts")

PAPER = "#F4F0E6"
INK = "#1A1A1F"
NAVY = "#14233F"
RED = "#B8322A"
MUTED = "#5A5A63"
RULE = "#CFC7B4"
SEA = "#D7E6EE"
LAND = "#E9DFC8"

REGION = {
    "ASIA": "#C0612B", "MIDDLE EAST": "#8C3B2E", "EUROPE": "#2F5DA8",
    "AFRICA": "#2E7D32", "AMERICAS": "#6A3D9A", "WORLDWIDE": "#3F4A55",
}


def font(name, size):
    return ImageFont.truetype(str(FONTS / name), round(size * S))


def s(*v):
    return [x * S for x in v]


img = Image.new("RGB", (W * S, H * S), PAPER)
d = ImageDraw.Draw(img)


def wrap(text, fnt, width, dr=None):
    dr = dr or d
    lines, cur = [], ""
    for w in text.split():
        trial = (cur + " " + w).strip()
        if dr.textlength(trial, font=fnt) <= width * S:
            cur = trial
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def text_block(x, y, text, name, size, width, max_lines, fill=INK, leading=1.16, min_size=10):
    """Wrap text into width, shrinking the font until it fits max_lines; returns the next y."""
    while True:
        fnt = font(name, size)
        lines = wrap(text, fnt, width)
        if len(lines) <= max_lines or size <= min_size:
            break
        size -= 0.5
    for i, line in enumerate(lines):
        d.text((x * S, (y + i * size * leading) * S), line, font=fnt, fill=fill)
    return y + len(lines) * size * leading


def star(cx, cy, r, fill):
    pts = []
    for k in range(10):
        a = -math.pi / 2 + k * math.pi / 5
        rr = r if k % 2 == 0 else r * 0.42
        pts += [(cx + rr * math.cos(a)) * S, (cy + rr * math.sin(a)) * S]
    d.polygon(pts, fill=fill)


# ---------------- flags ----------------
def flag_us(x, y, w, h):
    for i in range(7):
        d.rectangle(s(x, y + i * h / 7, x + w, y + (i + 0.5) * h / 7), fill="#B22234")
        d.rectangle(s(x, y + (i + 0.5) * h / 7, x + w, y + (i + 1) * h / 7), fill="white")
    d.rectangle(s(x, y, x + w * 0.42, y + h * 0.54), fill="#3C3B6E")


def flag_cn(x, y, w, h):
    d.rectangle(s(x, y, x + w, y + h), fill="#DE2910")
    star(x + w * 0.17, y + h * 0.27, h * 0.17, "#FFDE00")
    for dx, dy in [(0.33, 0.1), (0.4, 0.22), (0.4, 0.38), (0.33, 0.5)]:
        star(x + w * dx, y + h * dy, h * 0.06, "#FFDE00")


def flag_ru(x, y, w, h):
    for i, c in enumerate(["white", "#0039A6", "#D52B1E"]):
        d.rectangle(s(x, y + i * h / 3, x + w, y + (i + 1) * h / 3), fill=c)
    d.rectangle(s(x, y, x + w, y + h), outline="#BDBDBD", width=S)


# ---------------- icons: drawn in a 90x90 box, pasted at any size ----------------
def icon_tower_missile(x, y):
    d.polygon(s(x + 30, y + 86, x + 58, y + 86, x + 54, y + 14, x + 34, y + 22), fill="#4C5A6B")
    for r in range(6):
        d.line(s(x + 36, y + 30 + r * 9, x + 52, y + 30 + r * 9), fill="#9FB3C8", width=2 * S)
    d.line(s(x + 2, y + 6, x + 32, y + 24), fill="#8A8A8A", width=3 * S)
    d.ellipse(s(x + 40, y + 10, x + 72, y + 36), fill="#F39C12")
    d.ellipse(s(x + 48, y + 16, x + 64, y + 30), fill="#FDE68A")


def icon_tanker_fire(x, y):
    d.rectangle(s(x, y + 70, x + 90, y + 90), fill="#2E86AB")
    d.polygon(s(x + 4, y + 58, x + 86, y + 58, x + 78, y + 76, x + 12, y + 76), fill="#2B2B2B")
    d.rectangle(s(x + 62, y + 44, x + 76, y + 58), fill="#E8E8E8")
    d.polygon(s(x + 22, y + 58, x + 30, y + 22, x + 36, y + 40, x + 42, y + 12, x + 50, y + 58), fill="#E4572E")
    d.polygon(s(x + 28, y + 58, x + 34, y + 36, x + 40, y + 46, x + 44, y + 58), fill="#FFC857")
    d.ellipse(s(x + 26, y + 0, x + 46, y + 12), fill="#7A7A7A")


def icon_expel(x, y):
    d.rectangle(s(x + 6, y + 10, x + 46, y + 86), fill="#6D4C41")
    d.rectangle(s(x + 12, y + 16, x + 40, y + 86), fill="#F3EFE6")
    d.rounded_rectangle(s(x + 48, y + 46, x + 82, y + 76), radius=4 * S, fill="#2E7D32")
    d.rectangle(s(x + 58, y + 40, x + 72, y + 46), outline="#2E7D32", width=2 * S)
    d.line(s(x + 22, y + 32, x + 76, y + 32), fill=RED, width=4 * S)
    d.polygon(s(x + 86, y + 32, x + 74, y + 24, x + 74, y + 40), fill=RED)


def icon_strike_building(x, y):
    d.rectangle(s(x + 10, y + 46, x + 80, y + 88), fill="#7D6B57")
    for c in range(4):
        d.rectangle(s(x + 18 + c * 16, y + 56, x + 26 + c * 16, y + 66), fill="#3B3226")
    d.polygon(s(x + 30, y + 46, x + 40, y + 20, x + 46, y + 34, x + 56, y + 6, x + 62, y + 30, x + 70, y + 46), fill="#E4572E")
    d.polygon(s(x + 40, y + 46, x + 47, y + 30, x + 54, y + 38, x + 60, y + 46), fill="#FFC857")
    d.line(s(x + 4, y + 8, x + 26, y + 22), fill="#555555", width=3 * S)


def icon_empty_chair(x, y):
    c = "#5B3A8A"
    d.rounded_rectangle(s(x + 24, y + 6, x + 66, y + 48), radius=6 * S, fill=c)
    d.rectangle(s(x + 18, y + 48, x + 72, y + 60), fill=c)
    d.rectangle(s(x + 22, y + 60, x + 28, y + 88), fill=c)
    d.rectangle(s(x + 62, y + 60, x + 68, y + 88), fill=c)
    d.line(s(x + 30, y + 16, x + 60, y + 40), fill="white", width=4 * S)
    d.line(s(x + 60, y + 16, x + 30, y + 40), fill="white", width=4 * S)


def icon_gavel_podium(x, y):
    d.rectangle(s(x + 20, y + 50, x + 70, y + 88), fill="#2F5DA8")
    d.rectangle(s(x + 14, y + 44, x + 76, y + 52), fill="#1F3F75")
    for i, c in enumerate(["#C6363C", "#0C4076", "#FFFFFF"]):
        d.rectangle(s(x + 32, y + 58 + i * 7, x + 58, y + 65 + i * 7), fill=c)
    d.line(s(x + 30, y + 10, x + 58, y + 36), fill="#6D4C41", width=5 * S)
    d.rounded_rectangle(s(x + 46, y + 4, x + 70, y + 20), radius=3 * S, fill="#4E342E")


def icon_ballot(x, y):
    d.rectangle(s(x + 10, y + 40, x + 80, y + 88), fill="#1F4E8C")
    d.rectangle(s(x + 28, y + 40, x + 62, y + 46), fill="#0E2C52")
    d.polygon(s(x + 30, y + 4, x + 64, y + 10, x + 58, y + 44, x + 24, y + 38), fill="white", outline="#999999")
    d.line(s(x + 34, y + 24, x + 42, y + 32, x + 56, y + 14), fill="#2E7D32", width=4 * S)
    d.text(s(x + 45, y + 66), "3rd", font=font("arialbd.ttf", 18), fill="white", anchor="mm")


def icon_shield(x, y):
    d.polygon(s(x + 45, y + 4, x + 80, y + 16, x + 76, y + 56, x + 45, y + 88, x + 14, y + 56, x + 10, y + 16), fill="#1F3F75")
    d.polygon(s(x + 45, y + 14, x + 70, y + 22, x + 67, y + 52, x + 45, y + 76, x + 23, y + 52, x + 20, y + 22), fill="#3E6DB5")
    d.text(s(x + 45, y + 44), "POLICE", font=font("arialbd.ttf", 12), fill="white", anchor="mm")


def icon_house_fire(x, y):
    d.polygon(s(x + 8, y + 46, x + 45, y + 14, x + 82, y + 46), fill="#7B3F00")
    d.rectangle(s(x + 16, y + 46, x + 74, y + 88), fill="#B07A4A")
    d.rectangle(s(x + 38, y + 62, x + 52, y + 88), fill="#3B2412")
    d.polygon(s(x + 52, y + 46, x + 60, y + 6, x + 68, y + 26, x + 76, y + 2, x + 86, y + 46), fill="#E4572E")
    d.polygon(s(x + 58, y + 46, x + 64, y + 22, x + 72, y + 32, x + 80, y + 46), fill="#FFC857")


def icon_cyclone(x, y):
    cx, cy = x + 45, y + 45
    for k in range(3):
        a0 = k * 120
        pts = []
        for t in range(0, 34):
            a = math.radians(a0 + t * 6)
            r = 6 + t * 1.1
            pts += [(cx + r * math.cos(a)) * S, (cy + r * math.sin(a)) * S]
        d.line(pts, fill="#2E86AB", width=6 * S)
    d.ellipse(s(cx - 7, cy - 7, cx + 7, cy + 7), fill="#1B4F72")


def icon_gamepad(x, y):
    d.rounded_rectangle(s(x + 6, y + 30, x + 84, y + 74), radius=20 * S, fill="#3F2A56")
    d.rectangle(s(x + 18, y + 48, x + 36, y + 54), fill="white")
    d.rectangle(s(x + 24, y + 42, x + 30, y + 60), fill="white")
    for cx, cy, c in [(62, 46, "#FF6B9A"), (72, 54, "#FFD166"), (62, 60, "#06D6A0")]:
        d.ellipse(s(x + cx - 4, y + cy - 4, x + cx + 4, y + cy + 4), fill=c)
    d.text(s(x + 45, y + 16), "VI", font=font("georgiab.ttf", 22), fill="#E0457B", anchor="mm")


def icon_ipo_chart(x, y):
    d.rectangle(s(x + 6, y + 6, x + 84, y + 84), fill="#13233F")
    for i, h in enumerate([16, 24, 22, 36, 58]):
        d.rectangle(s(x + 14 + i * 14, y + 76 - h, x + 24 + i * 14, y + 76), fill="#3DDC97" if i == 4 else "#5B7CA8")
    d.line(s(x + 14, y + 52, x + 34, y + 44, x + 52, y + 46, x + 76, y + 16), fill="#FFD166", width=3 * S)
    d.text(s(x + 14, y + 10), "IPO", font=font("arialbd.ttf", 14), fill="white")


def icon_jet(x, y):
    c = "#4A5A3A"
    d.polygon(s(x + 6, y + 40, x + 70, y + 34, x + 86, y + 40, x + 70, y + 46), fill=c)
    d.polygon(s(x + 36, y + 37, x + 50, y + 10, x + 58, y + 10, x + 54, y + 37), fill=c)
    d.polygon(s(x + 36, y + 43, x + 50, y + 70, x + 58, y + 70, x + 54, y + 43), fill=c)
    d.ellipse(s(x + 18, y + 70, x + 70, y + 90), fill="#8A8A8A")


def paste_icon(fn, x, y, size):
    """Draw a 90x90 icon on its own layer and paste it scaled to size at (x, y)."""
    global d
    layer = Image.new("RGBA", (90 * S, 90 * S), (0, 0, 0, 0))
    saved, d = d, ImageDraw.Draw(layer)
    fn(0, 0)
    d = saved
    layer = layer.resize((round(size * S), round(size * S)), Image.LANCZOS)
    img.paste(layer, (round(x * S), round(y * S)), layer)


# ---------------- the three lead illustrations ----------------
def scene_summit(x, y, w, h):
    d.rectangle(s(x, y, x + w, y + h), fill="#1F3A68")
    d.rectangle(s(x, y, x + w, y + 22), fill="#C9A227")
    d.text(s(x + 8, y + 11), "APEC · SHENZHEN", font=font("arialbd.ttf", 13), fill=NAVY, anchor="lm")
    d.text(s(x + w - 8, y + 11), "FIRST US–CHINA–RUSSIA SUMMIT", font=font("arialbd.ttf", 13), fill=NAVY, anchor="rm")
    d.rectangle(s(x + 20, y + h - 34, x + w - 20, y + h - 14), fill="#8B5E3C")
    d.rectangle(s(x + 20, y + h - 14, x + w - 20, y + h - 8), fill="#5E3B22")
    for i, (painter, name) in enumerate([(flag_us, "USA"), (flag_cn, "CHINA"), (flag_ru, "RUSSIA")]):
        cx = x + w * (0.2 + 0.3 * i)
        d.line(s(cx - 34, y + h - 34, cx - 34, y + 34), fill="#B8B8B8", width=2 * S)
        painter(cx - 33, y + 34, 50, 32)
        # a seat marker and nameplate, no faces
        d.ellipse(s(cx - 14, y + 68, cx + 14, y + 96), fill="#3B5A8C")
        d.rounded_rectangle(s(cx - 24, y + 92, cx + 24, y + h - 34), radius=8 * S, fill="#3B5A8C")
        d.rectangle(s(cx - 28, y + h - 30, cx + 28, y + h - 16), fill="white")
        d.text(s(cx, y + h - 23), name, font=font("arialbd.ttf", 11), fill=INK, anchor="mm")


def scene_court(x, y, w, h):
    d.rectangle(s(x, y, x + w, y + h), fill="#DCE8F0")
    bx, by, bw = x + 20, y + 30, w - 120
    d.polygon(s(bx - 6, by + 22, bx + bw / 2, by, bx + bw + 6, by + 22), fill="#9C5B3B")
    d.rectangle(s(bx, by + 22, bx + bw, by + h - 40), fill="#B5704A")
    for c in range(6):
        d.rectangle(s(bx + 10 + c * (bw - 20) / 6, by + 34, bx + 20 + c * (bw - 20) / 6, by + h - 46), fill="#F1E3CF")
    d.rectangle(s(bx + bw / 2 - 6, by - 26, bx + bw / 2 + 6, by + 4), fill="#7A4630")
    d.rectangle(s(x, y + h - 30, x + w, y + h), fill="#7E9A6A")
    paste_icon(icon_scales, x + w - 104, y + 18, 96)


def icon_scales(x, y):
    c = "#5B1A22"
    d.line(s(x + 45, y + 10, x + 45, y + 78), fill=c, width=4 * S)
    d.line(s(x + 12, y + 22, x + 78, y + 22), fill=c, width=4 * S)
    d.polygon(s(x + 30, y + 84, x + 60, y + 84, x + 45, y + 72), fill=c)
    for cx in (x + 18, x + 72):
        d.line(s(cx, y + 22, cx - 12, y + 48), fill=c, width=2 * S)
        d.line(s(cx, y + 22, cx + 12, y + 48), fill=c, width=2 * S)
        d.chord(s(cx - 15, y + 38, cx + 15, y + 60), 0, 180, fill=c)
    d.ellipse(s(x + 40, y + 5, x + 50, y + 15), fill="#E2B33C")


def scene_bridge(x, y, w, h):
    d.rectangle(s(x, y, x + w, y + h), fill="#2B3A55")
    d.rectangle(s(x, y + h - 40, x + w, y + h), fill="#2E6F8E")
    deck = y + h - 62
    d.rectangle(s(x, deck, x + w, deck + 8), fill="#9AA5B1")
    for i in range(7):
        px = x + 16 + i * (w - 32) / 6
        d.rectangle(s(px - 3, deck + 8, px + 3, y + h - 30), fill="#9AA5B1")
    for i in range(3):
        ax = x + 10 + i * (w - 20) / 3
        d.arc(s(ax, deck - 40, ax + (w - 20) / 3, deck + 40), 180, 360, fill="#C9D1DA", width=3 * S)
    bx = x + w * 0.62
    d.polygon(s(bx - 26, deck, bx - 10, deck - 34, bx, deck - 16, bx + 10, deck - 44, bx + 26, deck), fill="#E4572E")
    d.polygon(s(bx - 14, deck, bx - 4, deck - 20, bx + 6, deck - 10, bx + 14, deck), fill="#FFC857")
    for k, r in enumerate([10, 13, 15]):
        d.ellipse(s(bx - 2 + k * 12 - r, deck - 50 - k * 6 - r, bx - 2 + k * 12 + r, deck - 50 - k * 6 + r), fill="#5C6470")
    d.rectangle(s(x + 8, y + 8, x + 118, y + 26), fill="#14233F")
    d.text(s(x + 63, y + 17), "KERCH BRIDGE", font=font("arialbd.ttf", 12), fill="white", anchor="mm")


# ---------------- simple world map (equirectangular, hand-placed outlines) ----------------
CONTINENTS = [
    [(-168, 66), (-140, 70), (-100, 72), (-80, 70), (-62, 60), (-55, 50), (-70, 43), (-76, 35), (-81, 25), (-97, 26),
     (-97, 18), (-88, 15), (-80, 8), (-85, 11), (-92, 15), (-105, 20), (-112, 30), (-117, 33), (-124, 40), (-125, 48),
     (-135, 58), (-150, 60), (-165, 60)],
    [(-55, 60), (-44, 60), (-20, 70), (-20, 80), (-60, 82), (-72, 77)],
    [(-80, 8), (-72, 12), (-60, 10), (-50, 0), (-35, -6), (-40, -22), (-48, -28), (-58, -38), (-65, -55), (-72, -50),
     (-73, -40), (-71, -20), (-81, -5)],
    [(-10, 36), (-9, 43), (-2, 44), (-5, 48), (2, 51), (8, 54), (5, 58), (12, 65), (25, 71), (40, 68), (45, 55),
     (40, 45), (28, 41), (22, 37), (15, 38), (12, 44), (3, 42)],
    [(-6, 50), (2, 51), (0, 54), (-3, 58), (-6, 57)],
    [(-17, 15), (-17, 21), (-10, 30), (-5, 36), (10, 37), (20, 32), (32, 31), (35, 28), (43, 12), (51, 12), (40, -5),
     (40, -15), (35, -25), (20, -35), (15, -28), (12, -15), (9, -1), (9, 4), (-8, 4), (-15, 10)],
    [(44, -25), (50, -15), (49, -12), (43, -17)],
    [(28, 41), (36, 36), (35, 30), (44, 13), (55, 22), (57, 26), (62, 25), (67, 24), (73, 17), (77, 8), (80, 15),
     (88, 22), (92, 21), (98, 16), (100, 7), (104, 1), (109, 12), (108, 21), (118, 24), (122, 30), (121, 40),
     (130, 43), (142, 50), (141, 60), (160, 61), (180, 66), (180, 72), (140, 73), (100, 78), (70, 73), (60, 70),
     (45, 55), (40, 45)],
    [(130, 31), (136, 34), (141, 36), (142, 40), (141, 45), (139, 40), (133, 34)],
    [(95, 5), (106, -6), (102, -5)],
    [(109, 1), (117, 7), (119, 0), (116, -4), (110, -3)],
    [(114, -22), (122, -17), (130, -12), (137, -12), (142, -11), (146, -19), (153, -26), (150, -37), (141, -38),
     (130, -32), (116, -35), (114, -27)],
]


def draw_map(x, y, w, h, pins):
    def P(lon, lat):
        return (x + (lon + 180) / 360 * w, y + (82 - lat) / (82 + 56) * h)

    d.rectangle(s(x, y, x + w, y + h), fill=SEA)
    for poly in CONTINENTS:
        pts = []
        for lon, lat in poly:
            px, py = P(lon, lat)
            pts += [px * S, py * S]
        d.polygon(pts, fill=LAND, outline="#B9AD91")
    for n, lon, lat, colour in pins:
        px, py = P(lon, lat)
        d.ellipse(s(px - 7, py - 7, px + 7, py + 7), fill=colour, outline="white", width=S)
        d.text(s(px, py), str(n), font=font("arialbd.ttf", 9), fill="white", anchor="mm")
    d.rectangle(s(x, y, x + w, y + h), outline=RULE, width=S)


# =====================================================================
# header
d.text(s(16, 10), "THE WORLD IN ONE DAY", font=font("arialbd.ttf", 14), fill=RED)
d.text(s(W - 16, 10), "15 STORIES IN PICTURES · 16 MORE BELOW · ALL FROM THIS ONE DAY",
       font=font("arialbd.ttf", 12), fill=INK, anchor="ra")
d.line(s(16, 28, W - 16, 28), fill=INK, width=2 * S)
d.text(s(14, 34), "Thursday 19 November 2026", font=font("georgiab.ttf", 57), fill=INK)
bx = W - 112
d.rectangle(s(bx, 36, W - 16, 104), fill="white", outline=RED, width=2 * S)
d.rectangle(s(bx, 36, W - 16, 54), fill=RED)
d.text(s(bx + 48, 45), "NOV 2026", font=font("arialbd.ttf", 12), fill="white", anchor="mm")
d.text(s(bx + 48, 76), "19", font=font("georgiab.ttf", 34), fill=INK, anchor="mm")
d.text(s(bx + 48, 97), "THURSDAY", font=font("arialbd.ttf", 10), fill=RED, anchor="mm")
d.text(s(16, 100), "Trump, Xi and Putin share one table · World Court finds genocide in Myanmar · "
       "Ukraine hits the Kerch Bridge again", font=font("georgia.ttf", 15), fill=RED)
d.line(s(16, 122, W - 16, 122), fill=INK, width=S)

# numbers strip
NUMBERS = [
    ("3", "leaders at one table"),
    ("1st", "state the ICJ finds guilty of genocide"),
    ("730,000", "Rohingya driven out in 2017"),
    ("3rd", "Kerch Bridge strike this week"),
    ("$107bn", "Anthropic's record IPO"),
    ("13 yrs", "since GTA V, now GTA VI"),
]
cw = (W - 32) / len(NUMBERS)
for i, (big, small) in enumerate(NUMBERS):
    x = 16 + i * cw
    if i:
        d.line(s(x, 128, x, 172), fill=RULE, width=S)
    d.text(s(x + 8, 125), big, font=font("georgiab.ttf", 22), fill=RED)
    text_block(x + 8, 154, small, "arial.ttf", 11, cw - 12, 1, min_size=9)
d.line(s(16, 176, W - 16, 176), fill=INK, width=S)

# lead stories
LEAD = [
    (16, 384, scene_summit, "SHENZHEN · SUMMIT", "ASIA",
     "Trump, Xi and Putin hold first three-way summit",
     "At APEC the US, Chinese and Russian leaders sign a four-point “Declaration toward Peace”: "
     "on nuclear risk, oil supply, UN reform and limits on the ICC."),
    (408, 304, scene_court, "THE HAGUE · JUSTICE", "EUROPE",
     "World Court: Myanmar committed genocide",
     "Ruling on Gambia's case, the ICJ finds the 2017 campaign against the Rohingya was genocide "
     "and calls for refugees' return and restitution."),
    (720, 288, scene_bridge, "CRIMEA · WAR", "EUROPE",
     "Ukraine hits Crimea bridge for third time this week",
     "Rail traffic over the Kerch Bridge halts. Russian strikes kill one in Kyiv and damage two "
     "embassies; Putin rules out ceasefire talks."),
]
for n, (x, w, scene, tag, region, head, body) in enumerate(LEAD, start=1):
    y = 182
    d.rectangle(s(x, y, x + w, 446), fill="white", outline=RULE, width=S)
    scene(x + 1, y + 1, w - 2, 128)
    ty = y + 136
    d.ellipse(s(x + 8, ty, x + 24, ty + 16), fill=REGION[region])
    d.text(s(x + 16, ty + 8), str(n), font=font("arialbd.ttf", 11), fill="white", anchor="mm")
    d.text(s(x + 30, ty + 8), tag, font=font("arialbd.ttf", 11), fill=REGION[region], anchor="lm")
    yy = text_block(x + 8, ty + 20, head, "georgiab.ttf", 24 if n == 1 else 20, w - 16, 2, leading=1.08)
    text_block(x + 8, yy + 4, body, "arial.ttf", 12.5, w - 16, 4, fill="#33333A", leading=1.2)

# grid of twelve more stories
GRID = [
    (icon_tower_missile, "RIYADH · WAR", "MIDDLE EAST", "Houthi missiles damage Riyadh's PIF Tower; no injuries"),
    (icon_tanker_fire, "HORMUZ · SHIPPING", "MIDDLE EAST", "Oil tanker catches fire after hitting a naval mine"),
    (icon_expel, "MOGADISHU · DIPLOMACY", "AFRICA", "Somalia expels UAE ambassador over sovereignty"),
    (icon_strike_building, "NYALA · SUDAN WAR", "AFRICA", "Army jets hit RSF intelligence HQ in Darfur"),
    (icon_empty_chair, "ULAANBAATAR · POLITICS", "ASIA", "Mongolia's president Khürelsükh resigns; vote due in 4 months"),
    (icon_house_fire, "GOPALGANJ · UNREST", "ASIA", "Arson in Bangladesh; 97 border-guard platoons deployed"),
    (icon_cyclone, "BAY OF BENGAL · STORM", "ASIA", "Cyclone Akvan nears India's east coast; landfall due Friday"),
    (icon_gavel_podium, "BELGRADE · POLITICS", "EUROPE", "Serbia's new parliament elects Čupić speaker and interim president"),
    (icon_ballot, "EL SALVADOR · VOTE", "AMERICAS", "Bukele files to run for a third term in 2027"),
    (icon_shield, "PORT-AU-PRINCE · GANGS", "AMERICAS", "Haitian police push into Martissant; 34 gang members killed, police say"),
    (icon_ipo_chart, "NEW YORK · MARKETS", "AMERICAS", "Anthropic shares start trading after record IPO"),
    (icon_gamepad, "WORLDWIDE · GAMES", "WORLDWIDE", "Grand Theft Auto VI goes on sale on PS5 and Xbox"),
]
GW, GH, GG = 158, 146, 8.8
for i, (icon, tag, region, head) in enumerate(GRID):
    col, row = i % 6, i // 6
    x, y = 16 + col * (GW + GG), 454 + row * (GH + 8)
    n = i + 4
    colour = REGION[region]
    d.rectangle(s(x, y, x + GW, y + GH), fill="white", outline=RULE, width=S)
    d.rectangle(s(x + 1, y + 1, x + GW - 1, y + 58), fill="#EEE8DA")
    paste_icon(icon, x + GW / 2 - 27, y + 3, 54)
    d.ellipse(s(x + 6, y + 63, x + 20, y + 77), fill=colour)
    d.text(s(x + 13, y + 70), str(n), font=font("arialbd.ttf", 9), fill="white", anchor="mm")
    text_block(x + 24, y + 64, tag, "arialbd.ttf", 9.5, GW - 28, 1, fill=colour)
    text_block(x + 7, y + 82, head, "arialbd.ttf", 13.5, GW - 13, 4, leading=1.13)

# bottom: map and the rest of the day
BY = 762
d.text(s(16, BY), "WHERE IT HAPPENED", font=font("arialbd.ttf", 12), fill=INK)
d.text(s(150, BY + 1), "numbers match the stories", font=font("arial.ttf", 10), fill=MUTED)
PINS = [
    (1, 114.1, 22.5, REGION["ASIA"]), (2, 4.3, 52.1, REGION["EUROPE"]), (3, 36.5, 45.3, REGION["EUROPE"]),
    (4, 46.7, 24.7, REGION["MIDDLE EAST"]), (5, 56.5, 26.5, REGION["MIDDLE EAST"]),
    (6, 45.3, 2.0, REGION["AFRICA"]), (7, 24.9, 12.0, REGION["AFRICA"]),
    (8, 106.9, 47.9, REGION["ASIA"]), (9, 89.8, 23.0, REGION["ASIA"]), (10, 84.0, 16.0, REGION["ASIA"]),
    (11, 20.5, 44.8, REGION["EUROPE"]), (12, -89.2, 13.7, REGION["AMERICAS"]),
    (13, -72.3, 18.5, REGION["AMERICAS"]), (14, -74.0, 40.7, REGION["AMERICAS"]),
]
draw_map(16, BY + 18, 346, 180, PINS)

ALSO = [
    ("Kyiv", "Russian strikes hit Austrian and Dutch embassies"),
    ("Gaza", "Israeli troops leave Nuseirat after a one-day raid"),
    ("Bekaa", "Israeli jets strike a Hezbollah underground site"),
    ("Sanaa", "Houthis say Saudi-led strikes killed 10 in two days"),
    ("Taiz", "UNICEF: water output nearly halved, 800,000 cut off"),
    ("Baghdad", "Deal ends standoff with Kataib Hezbollah militia"),
    ("Israel", "Court extends Gaza doctor Abu Safiya's detention"),
    ("Tehran", "Iran calls US chemical-weapons claims “fraudulent”"),
    ("Shenzhen", "Philippines and Chile sign a free-trade pact"),
    ("Shenzhen", "Trump leaves China without meeting Kim Jong Un"),
    ("Antalya", "COP31 nears its Friday deadline, oil wording disputed"),
    ("London", "UK and EU close in on a “reset” deal, FT reports"),
    ("Bogotá", "Unions call a national strike; marches in cities"),
    ("Dakar", "Senegal's budget passed by decree for an IMF deal"),
    ("Peshawar", "Pakistan army says 22 militants killed in raids"),
    ("Riyadh", "Saudi oil exports at their highest since the war began"),
]
LX0 = 374
d.text(s(LX0, BY), "ALSO ON THURSDAY 19 NOVEMBER", font=font("arialbd.ttf", 12), fill=INK)
d.line(s(LX0, BY + 16, W - 16, BY + 16), fill=INK, width=S)
colw = (W - 16 - LX0) / 2
for i, (place, what) in enumerate(ALSO):
    col, row = i // 8, i % 8
    x, y = LX0 + col * (colw + 4), BY + 22 + row * 22.4
    pf = font("arialbd.ttf", 12)
    d.text(s(x, y), place, font=pf, fill=INK)
    pw = d.textlength(place + " ", font=pf) / S
    text_block(x + pw, y + 0.5, what, "arial.ttf", 11.5, colw - pw - 6, 1, fill="#33333A")

# date check
DY = 966
d.rectangle(s(16, DY, W - 16, DY + 38), fill="white", outline=RED, width=S)
d.text(s(24, DY + 5), "DATE CHECK", font=font("arialbd.ttf", 11), fill=RED)
text_block(104, DY + 4.5, "Every story above happened, or was first reported, on Thursday 19 November 2026.",
           "arial.ttf", 11, W - 140, 1)
text_block(24, DY + 20.5, "Left out as other days' news: 18 Nov, US–Venezuela military ties restored; Israeli push "
           "past Gaza's Yellow Line; Jeffries nominated. 16 Nov, first COP31 draft. 20 Nov, Akvan's landfall.",
           "arial.ttf", 10.5, W - 48, 1, fill="#33333A")
d.text(s(W / 2, 1014), "Sources: AFP, AP, Reuters, Al Jazeera, BBC, Democracy Now, Sudan Tribune, FT · "
       "claims are attributed, not stated as fact · pictures and map drawn in code",
       font=font("arial.ttf", 10), fill=MUTED, anchor="mm")

out = img.resize((W, H), Image.LANCZOS)
dest = Path(__file__).resolve().parent.parent / "entry.png"
out.save(dest, optimize=True)
print(dest, dest.stat().st_size, "bytes")
