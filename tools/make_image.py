"""Draws entry.png: one image summing up the world news of Thursday 19 November 2026.

Run once on a machine with Pillow (not needed by the entry itself):
    python tools/make_image.py
The committed entry.png is what main.py copies to /output at grading time.
"""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

S = 2                      # draw at 2x, then downsample for clean edges
W = H = 1024
FONTS = Path("C:/Windows/Fonts")

PAPER = "#F3EFE6"
INK = "#1B1B1F"
NAVY = "#13233F"
GOLD = "#E2B33C"
MUTED = "#5A5A63"


def font(name, size):
    return ImageFont.truetype(str(FONTS / name), size * S)


def s(*v):
    return [x * S for x in v]


img = Image.new("RGB", (W * S, H * S), PAPER)
d = ImageDraw.Draw(img)


def wrap(text, fnt, width):
    words, lines, cur = text.split(), [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if d.textlength(trial, font=fnt) <= width * S:
            cur = trial
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def text_block(x, y, text, name, size, width, max_lines, fill=INK, leading=1.18):
    """Wrap text into width; shrink the font until it fits max_lines."""
    while True:
        fnt = font(name, size)
        lines = wrap(text, fnt, width)
        if len(lines) <= max_lines or size <= 12:
            break
        size -= 1
    for i, line in enumerate(lines):
        d.text((x * S, (y + i * size * leading) * S), line, font=fnt, fill=fill)
    return y + len(lines) * size * leading


# ---------- flags (simplified, for the summit table) ----------
def flag_us(x, y, w, h):
    for i in range(7):
        d.rectangle(s(x, y + i * h / 7, x + w, y + (i + 0.5) * h / 7), fill="#B22234")
        d.rectangle(s(x, y + (i + 0.5) * h / 7, x + w, y + (i + 1) * h / 7), fill="white")
    d.rectangle(s(x, y, x + w * 0.42, y + h * 0.54), fill="#3C3B6E")
    for r in range(3):
        for c in range(4):
            cx, cy = x + 4 + c * w * 0.1, y + 5 + r * h * 0.16
            d.ellipse(s(cx - 1.2, cy - 1.2, cx + 1.2, cy + 1.2), fill="white")


def star(cx, cy, r, fill):
    import math
    pts = []
    for k in range(10):
        a = -math.pi / 2 + k * math.pi / 5
        rr = r if k % 2 == 0 else r * 0.42
        pts += [(cx + rr * math.cos(a)) * S, (cy + rr * math.sin(a)) * S]
    d.polygon(pts, fill=fill)


def flag_cn(x, y, w, h):
    d.rectangle(s(x, y, x + w, y + h), fill="#DE2910")
    star(x + w * 0.17, y + h * 0.27, h * 0.17, "#FFDE00")
    for dx, dy in [(0.33, 0.1), (0.4, 0.22), (0.4, 0.38), (0.33, 0.5)]:
        star(x + w * dx, y + h * dy, h * 0.06, "#FFDE00")


def flag_ru(x, y, w, h):
    for i, c in enumerate(["white", "#0039A6", "#D52B1E"]):
        d.rectangle(s(x, y + i * h / 3, x + w, y + (i + 1) * h / 3), fill=c)
    d.rectangle(s(x, y, x + w, y + h), outline="#C8C8C8", width=S)


def pole_flag(px, base_y, painter, label):
    d.line(s(px, base_y, px, base_y - 120), fill="#6B6B6B", width=3 * S)
    d.ellipse(s(px - 4, base_y - 126, px + 4, base_y - 118), fill=GOLD)
    painter(px + 2, base_y - 118, 66, 42)
    d.text(s(px + 35, base_y - 66), label, font=font("arialbd.ttf", 14), fill=INK, anchor="mt")


# ---------- small icons, each in a 90x90 box at (x, y) ----------
def icon_scales(x, y):
    c = "#7A1F2B"
    d.line(s(x + 45, y + 10, x + 45, y + 78), fill=c, width=4 * S)
    d.line(s(x + 12, y + 22, x + 78, y + 22), fill=c, width=4 * S)
    d.polygon(s(x + 30, y + 82, x + 60, y + 82, x + 45, y + 72), fill=c)
    for cx in (x + 18, x + 72):
        d.line(s(cx, y + 22, cx - 12, y + 48), fill=c, width=2 * S)
        d.line(s(cx, y + 22, cx + 12, y + 48), fill=c, width=2 * S)
        d.chord(s(cx - 15, y + 38, cx + 15, y + 60), 0, 180, fill=c)
    d.ellipse(s(x + 40, y + 5, x + 50, y + 15), fill=GOLD)


def icon_tower_missile(x, y):
    d.polygon(s(x + 30, y + 86, x + 58, y + 86, x + 54, y + 14, x + 34, y + 22), fill="#4C5A6B")
    for r in range(6):
        d.line(s(x + 36, y + 30 + r * 9, x + 52, y + 30 + r * 9), fill="#9FB3C8", width=2 * S)
    d.line(s(x + 2, y + 6, x + 32, y + 24), fill="#8A8A8A", width=3 * S)
    d.polygon(s(x + 28, y + 18, x + 38, y + 28, x + 26, y + 28), fill="#C0392B")
    d.ellipse(s(x + 44, y + 12, x + 72, y + 34), fill="#F39C12")
    d.ellipse(s(x + 50, y + 16, x + 66, y + 30), fill="#FDE68A")


def icon_tanker_fire(x, y):
    d.rectangle(s(x, y + 70, x + 90, y + 90), fill="#2E86AB")
    d.polygon(s(x + 4, y + 58, x + 86, y + 58, x + 78, y + 76, x + 12, y + 76), fill="#2B2B2B")
    d.rectangle(s(x + 62, y + 44, x + 76, y + 58), fill="#E8E8E8")
    d.polygon(s(x + 22, y + 58, x + 30, y + 22, x + 36, y + 40, x + 42, y + 12, x + 50, y + 58), fill="#E4572E")
    d.polygon(s(x + 28, y + 58, x + 34, y + 36, x + 40, y + 46, x + 44, y + 58), fill="#FFC857")
    d.ellipse(s(x + 26, y + 2, x + 46, y + 14), fill="#7A7A7A")


def icon_bridge(x, y):
    d.rectangle(s(x, y + 72, x + 90, y + 90), fill="#2E86AB")
    d.rectangle(s(x, y + 44, x + 90, y + 52), fill="#555555")
    for px in (x + 14, x + 45, x + 76):
        d.rectangle(s(px - 3, y + 52, px + 3, y + 76), fill="#555555")
    d.arc(s(x + 14, y + 14, x + 76, y + 74), 180, 360, fill="#555555", width=4 * S)
    d.line(s(x + 36, y + 30, x + 54, y + 50), fill="#C0392B", width=5 * S)
    d.line(s(x + 54, y + 30, x + 36, y + 50), fill="#C0392B", width=5 * S)


def icon_expel(x, y):
    d.rectangle(s(x + 6, y + 10, x + 46, y + 86), fill="#6D4C41")
    d.rectangle(s(x + 12, y + 16, x + 40, y + 86), fill="#F3EFE6")
    d.rounded_rectangle(s(x + 48, y + 46, x + 82, y + 76), radius=4 * S, fill="#2E7D32")
    d.rectangle(s(x + 58, y + 40, x + 72, y + 46), outline="#2E7D32", width=2 * S)
    d.line(s(x + 22, y + 34, x + 76, y + 34), fill="#C0392B", width=4 * S)
    d.polygon(s(x + 86, y + 34, x + 74, y + 26, x + 74, y + 42), fill="#C0392B")


def icon_empty_chair(x, y):
    c = "#5B3A8A"
    d.rounded_rectangle(s(x + 24, y + 6, x + 66, y + 48), radius=6 * S, fill=c)
    d.rectangle(s(x + 18, y + 48, x + 72, y + 60), fill=c)
    d.rectangle(s(x + 22, y + 60, x + 28, y + 88), fill=c)
    d.rectangle(s(x + 62, y + 60, x + 68, y + 88), fill=c)
    d.text(s(x + 45, y + 27), "EXIT", font=font("arialbd.ttf", 13), fill="white", anchor="mm")


def icon_ballot(x, y):
    d.rectangle(s(x + 10, y + 40, x + 80, y + 88), fill="#1F4E8C")
    d.rectangle(s(x + 28, y + 40, x + 62, y + 46), fill="#0E2C52")
    d.polygon(s(x + 30, y + 4, x + 64, y + 10, x + 58, y + 44, x + 24, y + 38), fill="white", outline="#999999")
    d.line(s(x + 34, y + 24, x + 42, y + 32, x + 56, y + 14), fill="#2E7D32", width=4 * S)
    d.text(s(x + 45, y + 66), "2027", font=font("arialbd.ttf", 16), fill="white", anchor="mm")


def icon_house_fire(x, y):
    d.polygon(s(x + 8, y + 46, x + 45, y + 14, x + 82, y + 46), fill="#7B3F00")
    d.rectangle(s(x + 16, y + 46, x + 74, y + 88), fill="#B07A4A")
    d.rectangle(s(x + 38, y + 62, x + 52, y + 88), fill="#3B2412")
    d.polygon(s(x + 52, y + 46, x + 60, y + 6, x + 68, y + 26, x + 76, y + 2, x + 86, y + 46), fill="#E4572E")
    d.polygon(s(x + 58, y + 46, x + 64, y + 22, x + 72, y + 32, x + 80, y + 46), fill="#FFC857")


def icon_trade(x, y):
    d.rounded_rectangle(s(x + 4, y + 16, x + 52, y + 46), radius=4 * S, fill="#0038A8")
    d.polygon(s(x + 4, y + 16, x + 24, y + 31, x + 4, y + 46), fill="white")
    d.rectangle(s(x + 4, y + 31, x + 52, y + 46), fill="#CE1126")
    d.polygon(s(x + 4, y + 16, x + 24, y + 31, x + 4, y + 46), fill="white")
    d.rectangle(s(x + 38, y + 50, x + 86, y + 80), fill="white", outline="#999999")
    d.rectangle(s(x + 38, y + 65, x + 86, y + 80), fill="#D52B1E")
    d.rectangle(s(x + 38, y + 50, x + 54, y + 65), fill="#0039A6")
    star(x + 46, y + 57.5, 5, "white")
    d.line(s(x + 58, y + 26, x + 82, y + 26, x + 82, y + 44), fill=INK, width=3 * S)
    d.polygon(s(x + 82, y + 48, x + 76, y + 40, x + 88, y + 40), fill=INK)
    d.line(s(x + 32, y + 72, x + 10, y + 72, x + 10, y + 52), fill=INK, width=3 * S)
    d.polygon(s(x + 10, y + 48, x + 4, y + 56, x + 16, y + 56), fill=INK)


# ---------- header ----------
d.rectangle(s(0, 0, W, 116), fill=NAVY)
d.text(s(28, 16), "THE WORLD IN ONE PAGE", font=font("arialbd.ttf", 20), fill=GOLD)
d.text(s(26, 40), "Thursday 19 November 2026", font=font("georgiab.ttf", 52), fill="white")
d.text(s(W - 28, 22), "WORLD NEWS", font=font("arialbd.ttf", 18), fill="#AFC2E0", anchor="ra")
d.text(s(W - 28, 46), "11 stories", font=font("arial.ttf", 18), fill="#AFC2E0", anchor="ra")
d.text(s(W - 28, 70), "of the day", font=font("arial.ttf", 18), fill="#AFC2E0", anchor="ra")

# ---------- lead story ----------
LX, LY, LW, LH = 24, 130, 976, 300
d.rounded_rectangle(s(LX, LY, LX + LW, LY + LH), radius=10 * S, fill="white", outline="#D8D2C4", width=S)
d.rounded_rectangle(s(LX + 16, LY + 14, LX + 146, LY + 42), radius=4 * S, fill="#C0392B")
d.text(s(LX + 81, LY + 28), "TOP STORY", font=font("arialbd.ttf", 16), fill="white", anchor="mm")
# summit table with the three flags
TX = LX + 30
d.ellipse(s(TX + 10, LY + 200, TX + 370, LY + 262), fill="#8B5E3C")
d.ellipse(s(TX + 22, LY + 204, TX + 358, LY + 250), fill="#A9744F")
pole_flag(TX + 40, LY + 214, flag_us, "UNITED STATES")
pole_flag(TX + 150, LY + 200, flag_cn, "CHINA")
pole_flag(TX + 260, LY + 214, flag_ru, "RUSSIA")
d.text(s(TX + 190, LY + 272), "APEC SUMMIT · SHENZHEN, CHINA", font=font("arialbd.ttf", 15), fill=MUTED, anchor="mt")
# lead text
RX = LX + 430
y = text_block(RX, LY + 22, "Trump, Xi and Putin hold their first three-way summit",
               "georgiab.ttf", 40, 520, 3, leading=1.12)
y = text_block(RX, y + 10, "At the APEC meeting in Shenzhen the US, Chinese and Russian leaders "
               "issue a joint declaration on nuclear war, oil supply and UN reform.",
               "arial.ttf", 21, 520, 4, fill="#33333A")
d.text(s(RX, LY + LH - 34), "Also at APEC: the Philippines and Chile sign a free-trade pact",
       font=font("arialbd.ttf", 16), fill="#1F4E8C")

# ---------- grid of the day's other stories ----------
STORIES = [
    ("UN COURT · THE HAGUE", "#7A1F2B", icon_scales,
     "ICJ rules Myanmar committed genocide against the Rohingya"),
    ("SAUDI ARABIA · YEMEN", "#C0612B", icon_tower_missile,
     "Houthi missiles hit Riyadh's PIF Tower; no injuries"),
    ("STRAIT OF HORMUZ", "#1F7A8C", icon_tanker_fire,
     "Oil tanker catches fire after hitting a naval mine"),
    ("UKRAINE · CRIMEA", "#2F5DA8", icon_bridge,
     "Kerch Bridge shut again after Ukrainian attacks; trains held"),
    ("SOMALIA · UAE", "#2E7D32", icon_expel,
     "Somalia expels the UAE ambassador over sovereignty"),
    ("MONGOLIA", "#5B3A8A", icon_empty_chair,
     "President Khurelsukh resigns amid corruption scandal"),
    ("EL SALVADOR", "#1F4E8C", icon_ballot,
     "Bukele files to run for a third term in 2027"),
    ("BANGLADESH", "#8C4A1F", icon_house_fire,
     "Arson and looting in Gopalganj; border guards deployed"),
    ("LEBANON · ISRAEL", "#4A5A3A", None,
     "Israel strikes Hezbollah site in the Bekaa valley"),
]


def icon_jet(x, y):
    c = "#4A5A3A"
    d.polygon(s(x + 6, y + 40, x + 70, y + 34, x + 86, y + 40, x + 70, y + 46), fill=c)
    d.polygon(s(x + 36, y + 37, x + 50, y + 10, x + 58, y + 10, x + 54, y + 37), fill=c)
    d.polygon(s(x + 36, y + 43, x + 50, y + 70, x + 58, y + 70, x + 54, y + 43), fill=c)
    d.polygon(s(x + 8, y + 40, x + 12, y + 26, x + 18, y + 26, x + 20, y + 40), fill=c)
    d.ellipse(s(x + 18, y + 68, x + 70, y + 90), fill="#8A8A8A")
    d.ellipse(s(x + 30, y + 64, x + 58, y + 82), fill="#B0B0B0")


GX, GY, CW, CH, GAP = 24, 442, 320, 168, 8
for i, (tag, colour, icon, headline) in enumerate(STORIES):
    col, row = i % 3, i // 3
    x, y = GX + col * (CW + GAP), GY + row * (CH + GAP)
    d.rounded_rectangle(s(x, y, x + CW, y + CH), radius=8 * S, fill="white", outline="#D8D2C4", width=S)
    d.rounded_rectangle(s(x, y, x + CW, y + 28), radius=8 * S, fill=colour)
    d.rectangle(s(x, y + 18, x + CW, y + 28), fill=colour)
    d.text(s(x + 12, y + 14), tag, font=font("arialbd.ttf", 15), fill="white", anchor="lm")
    (icon or icon_jet)(x + 12, y + 50)
    text_block(x + 114, y + 40, headline, "arialbd.ttf", 21, 196, 5, leading=1.15)

# ---------- footer ----------
d.text(s(28, 1004), "Events of 19 Nov 2026 as reported by AFP, AP, Al Jazeera and BBC  ·  "
       "illustrations drawn for this page", font=font("arial.ttf", 14), fill=MUTED, anchor="lm")

out = img.resize((W, H), Image.LANCZOS)
dest = Path(__file__).resolve().parent.parent / "entry.png"
out.save(dest, optimize=True)
print(dest, dest.stat().st_size, "bytes")
