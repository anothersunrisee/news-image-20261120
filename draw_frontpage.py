#!/usr/bin/env python3
"""news-image-20261120: dense newspaper front page, Friday 20 November 2026.
Drawn with PIL (no AI image generation): 1024x1024, masthead + 3 top stories
+ 8 medium cards + 19 numbered briefs + dot-matrix world map + sources footer.
Clean mid-century poster / Swiss editorial style: flat solid colours, cream
paper, generous margins, no painterly textures, no detailed faces."""
import math
from PIL import Image, ImageDraw, ImageFont

PAGE = 1024
EDGE = 40
INNER = PAGE - 2 * EDGE          # 944

# palette (flat, solid)
CREAM = (247, 241, 227)
INK = (26, 26, 26)
NAVY = (20, 38, 74)
RED = (193, 39, 45)
GOLD = (217, 164, 65)
TEAL = (31, 122, 109)
BLUE = (46, 95, 163)
GREEN = (62, 122, 58)
PURPLE = (106, 76, 147)
ORANGE = (198, 110, 30)
SLATE = (138, 148, 166)
GREY = (68, 68, 68)
HAIRLINE = (216, 210, 192)
SKY = (215, 227, 238)
SEA = (46, 95, 163)
DEEPTEAL = (20, 82, 74)
WHITE = (255, 255, 255)
OFFWHITE = (245, 240, 225)

FONTDIR = "/usr/share/fonts/truetype/noto/"

def load(name, size):
    return ImageFont.truetype(FONTDIR + name, size)

MASTHEAD = load("NotoSerifDisplay-Bold.ttf", 44)
KICKER = load("NotoSans-Bold.ttf", 14)
CLAIM = load("NotoSans-Bold.ttf", 14)
SECTION = load("NotoSans-Bold.ttf", 13)
HEADLINE = load("NotoSans-Bold.ttf", 17)
DEK = load("NotoSans-Regular.ttf", 12)
TAG = load("NotoSans-Bold.ttf", 10)
CARDHEAD = load("NotoSans-Bold.ttf", 13)
CARDBODY = load("NotoSans-Regular.ttf", 11)
BRIEF = load("NotoSans-Regular.ttf", 11)
BRIEFNUM = load("NotoSans-Bold.ttf", 11)
FOOT = load("NotoSans-Regular.ttf", 11)
PINNUM = load("NotoSans-Bold.ttf", 10)
LEGEND = load("NotoSans-Bold.ttf", 10)
MAPTITLE = load("NotoSans-Bold.ttf", 11)

canvas = Image.new("RGB", (PAGE, PAGE), CREAM)
pen = ImageDraw.Draw(canvas)

# ------------------------------------------------------------- text helpers
def measure(s, f):
    return pen.textlength(s, font=f)

def wrap_text(s, f, width):
    """Greedy word wrap to the given pixel width."""
    out, cur = [], ""
    for word in s.split():
        trial = (cur + " " + word).strip()
        if measure(trial, f) <= width:
            cur = trial
        else:
            if cur:
                out.append(cur)
            cur = word
    if cur:
        out.append(cur)
    return out

def spaced_center(cx, y, s, f, fill, gap=2):
    """Draw s centred on cx with letter-spacing `gap`."""
    widths = [measure(c, f) for c in s]
    total = sum(widths) + gap * (len(s) - 1)
    x = cx - total / 2
    for ch, w in zip(s, widths):
        pen.text((x, y), ch, font=f, fill=fill)
        x += w + gap

def tag(x, y, label, colour):
    """Coloured category chip; returns its width."""
    tw = measure(label, TAG)
    pad = 7
    bw, bh = tw + 2 * pad, 17
    pen.rounded_rectangle([x, y, x + bw, y + bh], radius=3, fill=colour)
    pen.text((x + pad, y + 3), label, font=TAG, fill=WHITE)
    return bw

# ------------------------------------------------------------- masthead
spaced_center(PAGE // 2, 40, "THE WORLD IN ONE DAY", KICKER, RED, gap=3)
pen.text((PAGE // 2, 56), "Friday 20 November 2026", font=MASTHEAD,
         fill=NAVY, anchor="ma")
spaced_center(PAGE // 2, 106, "30 STORIES  ·  6 CONTINENTS  ·  ONE DAY",
              CLAIM, NAVY, gap=2)
pen.rectangle([EDGE, 128, PAGE - EDGE - 1, 131], fill=NAVY)
pen.rectangle([EDGE, 134, PAGE - EDGE - 1, 135], fill=RED)

# ------------------------------------------------------------- pictograms
def burst(cx, cy, outer, inner, points=8, fill=RED):
    """Starburst polygon (explosion / flash)."""
    pts = []
    for i in range(2 * points):
        r = outer if i % 2 == 0 else inner
        a = math.pi * i / points - math.pi / 2
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    pen.polygon(pts, fill=fill)

def art_kyiv(x, y, w, h):
    """Night strike over a city: dark sky, missile streaks, blasts, bridge."""
    pen.rectangle([x, y, x + w - 1, y + h - 1], fill=NAVY)
    for sx, sy in [(0.10, 0.14), (0.34, 0.08), (0.58, 0.15), (0.88, 0.09)]:
        pen.ellipse([x + sx * w - 2, y + sy * h - 2,
                     x + sx * w + 2, y + sy * h + 2], fill=WHITE)
    # missile streaks (orange diagonals)
    for sx, sy, ln in [(0.18, 0.10, 34), (0.52, 0.06, 40), (0.78, 0.14, 30)]:
        pen.line([x + sx * w, y + sy * h, x + sx * w + ln, y + sy * h + ln],
                 fill=(232, 120, 40), width=3)
    # two explosions
    burst(x + 0.30 * w, y + 0.52 * h, 18, 8, fill=(232, 90, 40))
    pen.ellipse([x + 0.30 * w - 5, y + 0.52 * h - 5,
                 x + 0.30 * w + 5, y + 0.52 * h + 5], fill=GOLD)
    burst(x + 0.72 * w, y + 0.44 * h, 14, 6, fill=(232, 90, 40))
    # skyline silhouette
    base = y + h
    for bx, bw, bh in [(0.02, 0.09, 30), (0.12, 0.08, 44), (0.22, 0.10, 34),
                       (0.62, 0.09, 40), (0.72, 0.10, 28), (0.84, 0.11, 36)]:
        pen.rectangle([x + bx * w, base - bh, x + (bx + bw) * w, base],
                      fill=(8, 16, 36))
        for wy in range(2):
            pen.rectangle([x + (bx + 0.02) * w, base - bh + 7 + wy * 11,
                           x + (bx + 0.04) * w, base - bh + 11 + wy * 11],
                          fill=GOLD)
    # river + bridge deck at the foot
    pen.rectangle([x, y + h - 16, x + w - 1, y + h - 1], fill=SEA)
    pen.rectangle([x + 0.30 * w, y + h - 24, x + 0.70 * w, y + h - 19],
                  fill=OFFWHITE)

def art_shenzhen(x, y, w, h):
    """Trilateral declaration: three flags over a skyline, gold seal."""
    pen.rectangle([x, y, x + w - 1, y + h - 1], fill=DEEPTEAL)
    # gold sun
    pen.ellipse([x + 0.88 * w - 13, y + 0.12 * h - 13,
                 x + 0.88 * w + 13, y + 0.12 * h + 13], fill=GOLD)
    # three flag poles
    fy = y + 0.30 * h
    # China (red, one big + four small gold stars)
    fx = x + 0.12 * w
    pen.rectangle([fx - 2, fy, fx, fy + 44], fill=WHITE)
    pen.rectangle([fx, fy, fx + 48, fy + 30], fill=RED)
    pen.ellipse([fx + 6, fy + 5, fx + 14, fy + 13], fill=GOLD)
    for sx, sy in [(22, 5), (28, 9), (28, 15), (22, 19)]:
        pen.ellipse([fx + sx, fy + sy, fx + sx + 4, fy + sy + 4], fill=GOLD)
    # USA (stripes + blue canton)
    ux = x + 0.40 * w
    pen.rectangle([ux - 2, fy, ux, fy + 44], fill=WHITE)
    for i in range(7):
        col = RED if i % 2 == 0 else WHITE
        pen.rectangle([ux, fy + i * 5, ux + 48, fy + i * 5 + 5], fill=col)
    pen.rectangle([ux, fy, ux + 20, fy + 17], fill=NAVY)
    for r in range(3):
        for c in range(4):
            pen.ellipse([ux + 3 + c * 5, fy + 3 + r * 5,
                         ux + 5 + c * 5, fy + 5 + r * 5], fill=WHITE)
    # Russia (white-blue-red tricolour)
    rx = x + 0.68 * w
    pen.rectangle([rx - 2, fy, rx, fy + 44], fill=WHITE)
    pen.rectangle([rx, fy, rx + 48, fy + 10], fill=WHITE)
    pen.rectangle([rx, fy + 10, rx + 48, fy + 20], fill=BLUE)
    pen.rectangle([rx, fy + 20, rx + 48, fy + 30], fill=RED)
    # gold seal at the foot (drawn star, not a text glyph)
    pen.ellipse([x + 0.50 * w - 12, y + h - 26, x + 0.50 * w + 12, y + h - 2],
                fill=GOLD, outline=WHITE, width=1)
    burst(x + 0.50 * w, y + h - 14, 6, 2.5, points=5, fill=NAVY)
    # skyline
    base = y + h
    for bx, bw, bh in [(0.02, 0.08, 22), (0.86, 0.09, 26)]:
        pen.rectangle([x + bx * w, base - bh, x + (bx + bw) * w, base],
                      fill=NAVY)

def art_icj(x, y, w, h):
    """World Court ruling: white courthouse columns + gold scales on navy."""
    pen.rectangle([x, y, x + w - 1, y + h - 1], fill=NAVY)
    # pediment
    pen.polygon([(x + 0.08 * w, y + 0.30 * h), (x + 0.50 * w, y + 0.10 * h),
                 (x + 0.92 * w, y + 0.30 * h)], fill=OFFWHITE)
    pen.ellipse([x + 0.50 * w - 7, y + 0.16 * h - 7,
                 x + 0.50 * w + 7, y + 0.16 * h + 7], fill=GOLD)
    # columns
    for cx in (0.16, 0.38, 0.62, 0.84):
        pen.rectangle([x + cx * w - 7, y + 0.32 * h,
                       x + cx * w + 7, y + 0.78 * h], fill=OFFWHITE)
    pen.rectangle([x + 0.06 * w, y + 0.78 * h, x + 0.94 * w, y + 0.84 * h],
                  fill=OFFWHITE)
    # scales of justice (gold) centred on the steps
    sx, sy = x + 0.50 * w, y + 0.60 * h
    pen.line([sx, sy - 16, sx, sy + 12], fill=GOLD, width=3)
    pen.line([sx - 16, sy - 12, sx + 16, sy - 12], fill=GOLD, width=3)
    pen.polygon([(sx - 22, sy + 4), (sx - 10, sy + 4), (sx - 16, sy - 10)],
                fill=GOLD)
    pen.polygon([(sx + 10, sy + 4), (sx + 22, sy + 4), (sx + 16, sy - 10)],
                fill=GOLD)
    pen.rectangle([sx - 16, y + 0.84 * h, sx + 16, y + h - 1], fill=GOLD)

# ------------------------------------------------------------- top stories
TOP = [
    ("EUROPE", BLUE,
     "RUSSIA'S KYIV BARRAGE SPILLS INTO POLAND",
     "400+ drones, 110+ missiles hit Kyiv; 9 killed, 3 bridges shut. Missiles land in Poland.",
     art_kyiv),
    ("GLOBAL", NAVY,
     "U.S., CHINA, RUSSIA ISSUE JOINT PEACE DECLARATION",
     "Trump, Xi and Putin sign a joint declaration; nuclear arms limits on the table.",
     art_shenzhen),
    ("ASIA", TEAL,
     "ICJ: MYANMAR COMMITTED GENOCIDE AGAINST ROHINGYA",
     "World Court rules Myanmar's forces committed genocide against the Rohingya.",
     art_icj),
]
COLW, GUT = 304, 16
TOPY = 144
for i, (cat, col, head, sub, art) in enumerate(TOP):
    cx = EDGE + i * (COLW + GUT)
    art(cx, TOPY, COLW, 88)
    tag(cx, TOPY + 96, cat, col)
    lines = wrap_text(head, HEADLINE, COLW)
    yy = TOPY + 120
    for ln in lines[:3]:
        pen.text((cx, yy), ln, font=HEADLINE, fill=INK)
        yy += 21
    slines = wrap_text(sub, DEK, COLW)
    assert len(slines) <= 2, f"top dek too long: {sub!r} -> {slines}"
    yy = TOPY + 120 + 3 * 21 + 2
    for ln in slines[:2]:
        pen.text((cx, yy), ln, font=DEK, fill=GREY)
        yy += 15

pen.rectangle([EDGE, 368, PAGE - EDGE - 1, 369], fill=HAIRLINE)

# ------------------------------------------------------------- medium cards
pen.text((EDGE, 376), "AROUND THE WORLD", font=SECTION, fill=NAVY)
pen.rectangle([EDGE + 190, 385, PAGE - EDGE - 1, 386], fill=HAIRLINE)
MEDIUM = [
    ("HOUTHIS", RED, "Houthi missile hits Riyadh's tallest tower",
     "PIF Tower windows blown out over 7–8 floors; no injuries.", "MIDDLE EAST"),
    ("CYCLONE", ORANGE, "Cyclone Akvan makes landfall in Odisha",
     "Storm comes ashore on India's east coast after days at sea.", "ASIA"),
    ("MARKETS", NAVY, "Markets slide as AI selloff deepens",
     "S&P 500 falls a 6th straight day; Nikkei drops 5.06%.", "GLOBAL"),
    ("HORMUZ", PURPLE, "Oil tanker burns in the Strait of Hormuz",
     "U.S. blockades Iranian shipping; IEA calls it the top energy shock.", "MIDDLE EAST"),
    ("SENATE", BLUE, "Senate blocks Iran war-powers vote, 51–48",
     "Trump in no rush on Iran: 'see what happens after January 1'.", "AMERICAS"),
    ("BRUSSELS", TEAL, "UK and EU sign Brussels deals",
     "Food trade, carbon markets and youth mobility agreed.", "EUROPE"),
    ("COP31", GREEN, "COP31 draft drops all fossil fuel references",
     "Activists protest as the Antalya summit runs past deadline.", "GLOBAL"),
    ("QUAKE", RED, "Magnitude 6.7 earthquake hits central Peru",
     "Tremor strikes near Cerro de Pasco; damage assessed.", "AMERICAS"),
]
MCW, MGUT = 227, 12
for row in range(2):
    ry = 404 + row * 102
    for ci in range(4):
        m = MEDIUM[row * 4 + ci]
        mx = EDGE + ci * (MCW + MGUT)
        tag(mx, ry, m[0], m[1])
        lines = wrap_text(m[2], CARDHEAD, MCW)
        yy = ry + 24
        for ln in lines[:2]:
            pen.text((mx, yy), ln, font=CARDHEAD, fill=INK)
            yy += 16
        slines = wrap_text(m[3], CARDBODY, MCW)
        yy = ry + 24 + 2 * 16 + 3
        for ln in slines[:2]:
            pen.text((mx, yy), ln, font=CARDBODY, fill=GREY)
            yy += 14
    for ci in range(1, 4):
        vx = EDGE + ci * (MCW + MGUT) - 6
        pen.rectangle([vx, ry + 2, vx, ry + 96], fill=HAIRLINE)

pen.rectangle([EDGE, 610, PAGE - EDGE - 1, 611], fill=HAIRLINE)

# ------------------------------------------------------------- briefs
pen.text((EDGE, 618), "THE BRIEFS — 19 MORE STORIES", font=SECTION, fill=NAVY)
pen.rectangle([EDGE + 268, 627, PAGE - EDGE - 1, 628], fill=HAIRLINE)
BRIEFS = [
    "Kerch Bridge rail traffic resumes after strikes.",
    "Anthropic shares slide on day two after record $81.3bn IPO.",
    "Haiti police kill 34 suspected gang members in Martissant raid.",
    "BepiColombo spacecraft reaches Mercury after eight years.",
    "Iraqi forces enter Hezbollah stronghold Jurf al-Nasr.",
    "Political violence in Bangladesh ahead of Hasina's return.",
    "Estonia to close its Russia border from Dec 1, for at least six months.",
    "Jury convicts Rinderknecht of starting the Palisades Fire.",
    "Judge approves $7.25bn Bayer settlement over Roundup.",
    "Israeli strikes kill Palestinians in Gaza despite the ceasefire.",
    "Russia invites Europeans to Moscow; Zelensky calls Putin a killer.",
    "Trump threatens penalties for U.S. tech firms building datacenters abroad.",
    "White House fires cyber director Cairncross after tech outages.",
    "El Salvador's Bukele seeks third term after constitution change.",
    "Nigeria moves to end jail terms for attempted suicide.",
    "U.S. robbery suspects charged over alleged $22M train heist spree.",
    "Kenya begins 42-day countdown to an Ebola-free declaration.",
    "Lauren Price becomes undisputed welterweight world champion.",
    "Lionel Messi of Inter Miami tops Major League Soccer salaries.",
]
BW = 460
for i, b in enumerate(BRIEFS):
    ci = 0 if i < 10 else 1
    ri = i if i < 10 else i - 10
    bx = EDGE + ci * (BW + 24)
    by = 644 + ri * 13
    pen.text((bx, by), f"{i+1}.", font=BRIEFNUM, fill=RED)
    pen.text((bx + 22, by), b, font=BRIEF, fill=INK)

pen.rectangle([EDGE, 782, PAGE - EDGE - 1, 783], fill=HAIRLINE)

# ------------------------------------------------------------- world map
pen.text((EDGE, 788), "WHERE IT HAPPENED — SCHEMATIC MAP, NOT TO SCALE",
         font=MAPTITLE, fill=NAVY)
MAPX0, MAPY0, MAPX1, MAPY1 = EDGE, 806, PAGE - EDGE, 944
MAPW, MAPH = MAPX1 - MAPX0, MAPY1 - MAPY0
TOPLAT, BOTLAT = 76.0, -56.0

def project(lon, lat):
    px = MAPX0 + (lon + 180.0) / 360.0 * MAPW
    py = MAPY0 + (TOPLAT - lat) / (TOPLAT - BOTLAT) * MAPH
    return px, py

# simplified continent outlines (lon, lat)
LAND = [
    # North America
    [(-168, 66), (-140, 70), (-125, 72), (-110, 73), (-95, 80), (-85, 80),
     (-75, 72), (-65, 60), (-55, 52), (-60, 47), (-70, 44), (-75, 35),
     (-80, 32), (-81, 26), (-84, 30), (-90, 29), (-97, 26), (-105, 20),
     (-97, 16), (-92, 15), (-86, 13), (-83, 9), (-79, 9), (-85, 11),
     (-90, 14), (-95, 16), (-105, 20), (-110, 24), (-114, 29), (-120, 34),
     (-125, 40), (-124, 48), (-130, 55), (-145, 60), (-155, 58), (-165, 60),
     (-168, 66)],
    # South America
    [(-79, 9), (-72, 12), (-62, 10), (-52, 5), (-50, 0), (-44, -3),
     (-35, -8), (-40, -20), (-48, -28), (-52, -33), (-58, -38), (-62, -41),
     (-66, -47), (-70, -52), (-73, -50), (-73, -40), (-72, -30), (-70, -18),
     (-77, -12), (-81, -6), (-80, 0), (-79, 9)],
    # Africa
    [(-17, 15), (-10, 30), (-5, 35), (0, 36), (10, 37), (20, 32), (30, 31),
     (35, 28), (38, 22), (43, 12), (48, 11), (51, 10), (44, 0), (40, -10),
     (36, -18), (32, -26), (28, -33), (20, -35), (16, -28), (12, -18),
     (9, -1), (9, 4), (-8, 4), (-13, 8), (-17, 15)],
    # Eurasia
    [(-10, 36), (-9, 43), (-2, 48), (-5, 50), (0, 51), (5, 53), (8, 57),
     (10, 59), (18, 56), (21, 55), (24, 59), (28, 60), (30, 62), (35, 66),
     (40, 68), (50, 69), (60, 69), (70, 72), (80, 73), (90, 75), (100, 77),
     (110, 74), (120, 73), (130, 72), (140, 72), (150, 70), (160, 70),
     (170, 67), (178, 65), (178, 62), (170, 60), (162, 56), (158, 52),
     (150, 59), (142, 55), (140, 50), (135, 44), (130, 42), (127, 40),
     (126, 38), (122, 38), (120, 32), (122, 28), (118, 25), (112, 22),
     (108, 18), (105, 10), (103, 8), (100, 6), (97, 10), (94, 16), (92, 21),
     (89, 22), (86, 20), (80, 13), (77, 8), (75, 12), (72, 20), (68, 22),
     (62, 25), (57, 26), (54, 26), (50, 29), (48, 30), (44, 29), (40, 31),
     (36, 36), (30, 36), (27, 37), (23, 36), (19, 40), (15, 44), (12, 44),
     (8, 44), (3, 43), (0, 40), (-2, 37), (-6, 36), (-10, 36)],
    # Australia
    [(114, -22), (114, -30), (115, -35), (118, -35), (124, -33), (129, -32),
     (132, -32), (135, -35), (138, -35), (140, -38), (145, -38), (150, -37),
     (153, -32), (153, -27), (150, -22), (146, -19), (142, -11), (140, -17),
     (136, -12), (132, -11), (126, -14), (122, -17), (118, -20), (114, -22)],
    # United Kingdom
    [(-5, 50), (-3, 53), (-5, 56), (-3, 58), (-1, 57), (0, 53), (1, 51),
     (-3, 50)],
    # Japan
    [(130, 31), (133, 34), (137, 35), (140, 37), (141, 40), (142, 43),
     (144, 44), (142, 41), (140, 38), (137, 34), (133, 33), (130, 31)],
]
PIXEL_POLYS = [[project(lon, lat) for lon, lat in poly] for poly in LAND]

def point_in_poly(px, py, poly):
    """Ray-casting point-in-polygon test."""
    inside = False
    n = len(poly)
    j = n - 1
    for i in range(n):
        xi, yi = poly[i]
        xj, yj = poly[j]
        if ((yi > py) != (yj > py)) and \
                (px < (xj - xi) * (py - yi) / (yj - yi) + xi):
            inside = not inside
        j = i
    return inside

pen.rectangle([MAPX0, MAPY0, MAPX1 - 1, MAPY1 - 1], outline=NAVY, width=1)
STEP = 6
gx = MAPX0 + 4
while gx < MAPX1 - 2:
    gy = MAPY0 + 4
    while gy < MAPY1 - 2:
        if any(point_in_poly(gx, gy, p) for p in PIXEL_POLYS):
            pen.ellipse([gx - 1.6, gy - 1.6, gx + 1.6, gy + 1.6], fill=SLATE)
        gy += STEP
    gx += STEP

def marker(lon, lat, num):
    px, py = project(lon, lat)
    pen.ellipse([px - 9, py - 9, px + 9, py + 9], fill=RED,
                outline=WHITE, width=1)
    pen.text((px, py), str(num), font=PINNUM, fill=WHITE, anchor="mm")

marker(30.5, 50.4, 1)    # Kyiv
marker(114.1, 22.5, 2)   # Shenzhen
marker(96.0, 21.0, 3)    # Myanmar
marker(86.0, 20.0, 4)    # Cyclone Akvan / Odisha
# BepiColombo: gold star in the empty South Pacific
sx, sy = project(-155, -48)
star = []
for i in range(10):
    r = 11 if i % 2 == 0 else 4.5
    a = math.pi * i / 5 - math.pi / 2
    star.append((sx + r * math.cos(a), sy + r * math.sin(a)))
pen.polygon(star, fill=GOLD, outline=WHITE)
pen.text((sx, sy - 16), "5", font=PINNUM, fill=GOLD, anchor="mm")

# legend, bottom-right inside the map frame
legend = "1 KYIV  ·  2 SHENZHEN  ·  3 MYANMAR  ·  4 AKVAN  ·  5 BEPICOLOMBO"
lw = measure(legend, LEGEND)
lx0 = MAPX1 - lw - 16
ly0 = MAPY1 - 20
pen.rectangle([lx0, ly0, MAPX1 - 4, MAPY1 - 4], fill=CREAM,
              outline=NAVY, width=1)
pen.text((lx0 + 8, ly0 + 3), legend, font=LEGEND, fill=NAVY)

# ------------------------------------------------------------- footer
pen.text((PAGE // 2, 956),
         "Sources: Reuters · AP · AFP · BBC · Al Jazeera  —  "
         "Every story above was first reported on Friday 20 November 2026.",
         font=FOOT, fill=GREY, anchor="ma")

canvas.save("/home/hatch/workspace/makefun-test/news-image-20261120-entry/entry.png",
            optimize=True)
print("saved entry.png")
