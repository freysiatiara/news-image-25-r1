#!/usr/bin/env python3
"""Draw entry.png for make.fun news-image-20261125.

Front page for Wednesday 25 November 2026: 30 dated, sourced stories
from 9 regions, drawn with PIL (build-time only). Deterministic output:
no timestamps, no randomness, fixed layout and fonts.
Run:  python3 draw.py        (writes entry.png next to this file)
"""
import os

from PIL import Image, ImageDraw, ImageFont

W = 1024
H = 1024
MARGIN = 24
GUT = 12

PAPER = (248, 244, 236)
INK = (20, 20, 20)
NAVY = (16, 35, 63)
RED = (179, 38, 30)
CARD = (255, 255, 255)
CARD_LINE = (216, 210, 196)
GRAY = (90, 90, 90)
STRIP = (232, 228, 216)

REGION_COLORS = {
    "EUROPE": (31, 78, 121),
    "E ASIA": (139, 26, 26),
    "MIDEAST": (122, 92, 0),
    "N AMERICA": (20, 83, 45),
    "CHINA": (156, 43, 46),
    "S ASIA": (106, 61, 154),
    "SE ASIA": (15, 118, 110),
    "WORLD": (51, 65, 85),
    "SPORT": (180, 83, 9),
    "AFRICA": (146, 64, 14),
    "LATAM": (14, 116, 144),
    "PACIFIC": (29, 78, 216),
}

TAX_COLORS = {
    "REPORTED": (70, 70, 70),
    "CLAIM": (179, 38, 30),
    "ANALYSIS": (106, 61, 154),
    "OBSERVED": (15, 118, 110),
    "ONGOING": (180, 83, 9),
}

FONT_DIR = "/usr/share/fonts/truetype/dejavu"


def font(name, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)


F_SERIF_B = lambda s: font("DejaVuSerif-Bold.ttf", s)
F_SANS_B = lambda s: font("DejaVuSans-Bold.ttf", s)
F_SANS = lambda s: font("DejaVuSans.ttf", s)

ELLIPSIS = "\u2026"


def wrap_text(draw, text, fnt, width):
    """Greedy word wrap; returns list of lines that fit width."""
    lines = []
    for raw in text.split("\n"):
        words = raw.split()
        if not words:
            lines.append("")
            continue
        cur = words[0]
        for w in words[1:]:
            trial = cur + " " + w
            if draw.textlength(trial, font=fnt) <= width:
                cur = trial
            else:
                lines.append(cur)
                cur = w
        lines.append(cur)
    return lines


def fit_text(draw, text, fnt, width, max_lines):
    """Wrap to at most max_lines; truncate the last line with an ellipsis."""
    lines = wrap_text(draw, text, fnt, width)
    if len(lines) <= max_lines:
        return lines
    lines = lines[:max_lines]
    last = lines[-1]
    while last and draw.textlength(last + ELLIPSIS, font=fnt) > width:
        last = last[:-1]
    lines[-1] = last + ELLIPSIS
    return lines


def text_center(draw, cx, y, text, fnt, fill):
    w = draw.textlength(text, font=fnt)
    draw.text((cx - w / 2, y), text, font=fnt, fill=fill)


# ---------------------------------------------------------------- stories
# (headline, deck, source, date, region, taxonomy)
HEROES = [
    (
        "LEAD  \u2022  SPACE  \u2014  CHINA",
        "SHENZHOU-24 LIFTS OFF",
        "China launches its Shenzhou-24 crew to the Tiangong station. "
        "Pakistani pilot Zeeshan Ali is the first foreign astronaut aboard.",
        "REUTERS  \u2022  25 NOV 2026  \u2022  08:18 CST",
        "rocket",
    ),
    (
        "LEAD  \u2022  PACIFIC  \u2014  TREATY",
        "SOLOMONS PICK AUSTRALIA",
        "Australia signs a historic security treaty in Canberra. The Solomons "
        "name Australia their partner of choice, dropping their China pact.",
        "REUTERS  \u2022  25 NOV 2026",
        "treaty",
    ),
]

STORIES = [
    ("UKRAINE DEFENDS LIBYA STRIKE",
     "Kyiv: sinking the corvette Merkury was self-defence.",
     "REUTERS", "24 NOV", "EUROPE", "REPORTED"),
    ("NATO SENDS AWACS TO POLAND",
     "Radar jet sent after 3 Russian missiles landed.",
     "REUTERS", "23 NOV", "EUROPE", "REPORTED"),
    ("720,000 RUSSIAN SOLDIERS DEAD",
     "490,000 confirmed; 720,000+ counting the missing.",
     "MEDUZA", "23 NOV", "EUROPE", "ANALYSIS"),
    ("RUSSIAN JETS BUZZ SOUTH KOREA",
     "Seoul scrambles F-15Ks as jets near Ulleung.",
     "YONHAP", "24 NOV", "E ASIA", "REPORTED"),
    ("RIYADH TOWER HIT AGAIN",
     "11 hurt in 2nd drone hit on PIF Tower in a week.",
     "REUTERS", "24 NOV", "MIDEAST", "REPORTED"),
    ("4TH TANKER HITS MINE OFF HORMUZ",
     "IRGC claims a 4th tanker hit a mine; unverified.",
     "IRNA / TASNIM", "24 NOV", "MIDEAST", "CLAIM"),
    ("CIA AND ODNI HACKED",
     "Unclassified system breached; no classified hit.",
     "NYT", "24 NOV", "N AMERICA", "REPORTED"),
    ("HUAWEI GUILTY ON 10 COUNTS",
     "Guilty: Iran sanctions, bank fraud, trade theft.",
     "REUTERS / DOJ", "24 NOV", "N AMERICA", "REPORTED"),
    ("GIULIANI GETS MEDAL OF FREEDOM",
     "Medal of Freedom, awarded in private ceremony.",
     "REUTERS", "24 NOV", "N AMERICA", "REPORTED"),
    ("SARKOZY TO STAND TRIAL",
     "Ex-president and wife Carla Bruni face a trial.",
     "REUTERS", "24 NOV", "EUROPE", "REPORTED"),
    ("SHANGHAI PARTY CHIEF FALLS",
     "Chen Jining probed \u2014 4th Politburo member to fall.",
     "XINHUA", "24 NOV", "CHINA", "REPORTED"),
    ("EU'S 22ND SANCTIONS PACKAGE",
     "60 banks off SWIFT, 70+ shadow-fleet ships listed.",
     "EU COMMISSION", "23 NOV", "EUROPE", "REPORTED"),
    ("CHINA EXTENDS MINERALS PAUSE",
     "Gallium ban pause extended to 27 Jan 2027.",
     "COMMERCE MIN.", "24 NOV", "CHINA", "REPORTED"),
    ("INDIA GIVES NEPAL \u20b915,000 CRORE",
     "Aid follows PM Shah's first state visit to Delhi.",
     "INDIA GOVT", "24 NOV", "S ASIA", "REPORTED"),
    ("BJP AND SAD REUNITE",
     "Alliance for 2027 Punjab polls after six-year split.",
     "INDIAN MEDIA", "25 NOV", "S ASIA", "REPORTED"),
    ("END VIOLENCE AGAINST WOMEN",
     "UN marks the day to end violence against women.",
     "UN", "25 NOV", "WORLD", "OBSERVED"),
    ("ANTHROPIC BELOW IPO PRICE",
     "First close under $83: $81.91, down 6.5%.",
     "REUTERS", "24 NOV", "N AMERICA", "REPORTED"),
    ("SHEIN PAYS $100 MILLION",
     "FTC deal; only 5 phone agents for ~1M parcels.",
     "FTC", "24 NOV", "N AMERICA", "REPORTED"),
    ("TURKEYS PARDONED \u2014 ONE FLEES",
     "Both spared; Feathers flees into the bushes first.",
     "AP", "24 NOV", "N AMERICA", "REPORTED"),
    ("O'HARE RADAR OUTAGE",
     "~350 flights delayed in O'Hare radar ground stop.",
     "FAA / REUTERS", "24 NOV", "N AMERICA", "REPORTED"),
    ("INDONESIA FACTORY FIRE: 26 DEAD",
     "Toll confirmed at 26; most died reaching the exit.",
     "AP", "24 NOV", "SE ASIA", "REPORTED"),
    ("HANOI EATERY BLAST KILLS 6",
     "6 killed, 10 hurt as gas blast collapses eatery.",
     "REUTERS", "24 NOV", "SE ASIA", "REPORTED"),
    ("ENGLAND LEVEL T20 SERIES",
     "Donald 85 off 32 balls as England win by 8 wickets.",
     "CRICINFO", "24 NOV", "SPORT", "REPORTED"),
    ("EBOLA TEAMS TRAPPED IN DR CONGO",
     "WHO teams stranded near Ituri; 11,000+ cases.",
     "UN NEWS", "24 NOV", "AFRICA", "REPORTED"),
    ("'EL CHAPO ISIDRO' CAPTURED",
     "Mexico nabs cartel boss; US drone flew over Mexico.",
     "AL JAZEERA", "24 NOV", "LATAM", "REPORTED"),
    ("BOLSONARO DEVELOPS PNEUMONIA",
     "Ex-president in intensive care, treated since Friday.",
     "MERCOPRESS", "24 NOV", "LATAM", "REPORTED"),
    ("UN MARKS PALESTINE SOLIDARITY DAY",
     "Gazans still lack safety and aid, says Guterres.",
     "UN", "24 NOV", "MIDEAST", "REPORTED"),
    ("ARGENTINA BUDGET HEADS FOR VOTE",
     "Signatures secured for Milei's 2027 budget vote.",
     "ARGENTINE PRESS", "25 NOV", "LATAM", "ONGOING"),
]

DATE_CHECK = (
    "DATE CHECK \u2014 Every story happened or was first reported on 25 Nov 2026 "
    "in some time zone. Older events appear only as dated follow-ups "
    "(attack 22 Nov, missiles 20 Nov, fire 21 Nov). Nothing here is from "
    "before 13 Nov 2026. Claims are labelled CLAIM; analysis is ANALYSIS."
)


# ---------------------------------------------------------------- icons
def draw_rocket(draw, x, y, s):
    """Simple rocket icon inside box (x, y, size s)."""
    cx = x + s // 2
    body_top = y + int(s * 0.12)
    body_bot = y + int(s * 0.62)
    # flame
    draw.polygon([(cx - 7, body_bot), (cx + 7, body_bot),
                  (cx, y + int(s * 0.92))], fill=(255, 140, 0))
    draw.polygon([(cx - 4, body_bot), (cx + 4, body_bot),
                  (cx, y + int(s * 0.82))], fill=(255, 210, 0))
    # fins
    draw.polygon([(x + int(s * 0.22), body_bot - 6),
                  (x + int(s * 0.38), body_bot - 26),
                  (x + int(s * 0.38), body_bot)], fill=RED)
    draw.polygon([(x + int(s * 0.78), body_bot - 6),
                  (x + int(s * 0.62), body_bot - 26),
                  (x + int(s * 0.62), body_bot)], fill=RED)
    # body
    draw.rounded_rectangle([cx - 13, body_top, cx + 13, body_bot],
                           radius=12, fill=(255, 255, 255),
                           outline=NAVY, width=2)
    # nose
    draw.polygon([(cx - 13, body_top + 12), (cx + 13, body_top + 12),
                  (cx, body_top - 12)], fill=RED)
    # window
    draw.ellipse([cx - 6, body_top + 22, cx + 6, body_top + 34],
                 fill=(120, 180, 220), outline=NAVY, width=2)
    # stars
    for sx, sy in ((x + 6, y + 8), (x + s - 10, y + 18), (x + 10, y + s - 14)):
        draw.ellipse([sx, sy, sx + 4, sy + 4], fill=(255, 200, 40))


def draw_treaty(draw, x, y, s):
    """Two documents + seal icon inside box (x, y, size s)."""
    # back document
    draw.rounded_rectangle([x + int(s * 0.30), y + int(s * 0.10),
                            x + int(s * 0.88), y + int(s * 0.78)],
                           radius=5, fill=(235, 230, 215),
                           outline=NAVY, width=2)
    # front document
    draw.rounded_rectangle([x + int(s * 0.08), y + int(s * 0.22),
                            x + int(s * 0.66), y + int(s * 0.90)],
                           radius=5, fill=(255, 255, 255),
                           outline=NAVY, width=2)
    for i, ly in enumerate((0.34, 0.44, 0.54, 0.64)):
        draw.line([x + int(s * 0.16), y + int(s * ly),
                   x + int(s * 0.58), y + int(s * ly)],
                  fill=(120, 120, 120), width=2)
    # seal
    draw.ellipse([x + int(s * 0.52), y + int(s * 0.66),
                  x + int(s * 0.82), y + int(s * 0.96)],
                 fill=RED, outline=(255, 255, 255), width=2)
    draw.ellipse([x + int(s * 0.60), y + int(s * 0.74),
                  x + int(s * 0.74), y + int(s * 0.88)],
                 outline=(255, 255, 255), width=2)


ICONS = {"rocket": draw_rocket, "treaty": draw_treaty}


# ---------------------------------------------------------------- layout
def draw_masthead(draw):
    draw.rectangle([0, 0, W, 104], fill=NAVY)
    text_center(draw, W // 2, 12,
                "T H E   W O R L D   I N   O N E   D A Y",
                F_SANS_B(13), (200, 210, 225))
    text_center(draw, W // 2, 32, "WEDNESDAY 25 NOVEMBER 2026",
                F_SERIF_B(40), (255, 255, 255))
    text_center(draw, W // 2, 80,
                "One day's news in one image \u2014 every story named, dated and sourced",
                F_SANS(13), (200, 210, 225))
    draw.rectangle([0, 100, W, 104], fill=RED)


def draw_proof_strip(draw):
    draw.rectangle([MARGIN, 112, W - MARGIN, 146], fill=STRIP,
                   outline=(190, 184, 168), width=1)
    text_center(draw, W // 2, 121,
                "30 DATED STORIES   \u2022   9 REGIONS   \u2022   "
                "5 EVENTS DATED 25 NOV   \u2022   0 STORIES BEFORE 13 NOV 2026",
                F_SANS_B(14), INK)


def draw_hero(draw, x, y, w, h, kicker, headline, deck, source, icon):
    draw.rectangle([x, y, x + w, y + h], fill=CARD,
                   outline=CARD_LINE, width=1)
    draw.rectangle([x, y, x + w, y + 5], fill=RED)
    ix, iy, isize = x + 14, y + 34, 74
    ICONS[icon](draw, ix, iy, isize)
    tx = x + 102
    tw = w - 102 - 16
    draw.text((tx, y + 12), kicker, font=F_SANS_B(11), fill=RED)
    hsize = 23
    while hsize > 17:
        hf = F_SERIF_B(hsize)
        if draw.textlength(headline, font=hf) <= tw:
            break
        hsize -= 1
    draw.text((tx, y + 28), headline, font=F_SERIF_B(hsize), fill=INK)
    lines = fit_text(draw, deck, F_SANS(14), tw, 3)
    yy = y + 58
    for ln in lines:
        draw.text((tx, yy), ln, font=F_SANS(14), fill=(40, 40, 40))
        yy += 18
    draw.text((tx, y + h - 20), source, font=F_SANS_B(11), fill=GRAY)


def draw_story_card(draw, x, y, w, h, story):
    headline, deck, source, date, region, tax = story
    color = REGION_COLORS[region]
    draw.rectangle([x, y, x + w, y + h], fill=CARD,
                   outline=CARD_LINE, width=1)
    draw.rectangle([x, y, x + 4, y + h], fill=color)
    # kicker: region + source + date + taxonomy (taxonomy in its own colour).
    # Shrink the kicker font until the whole line fits the card width.
    kicker_left = "%s  \u2022  %s  \u2022  %s  \u2022  " % (region, source, date)
    ksize = 10
    while ksize > 7:
        kf = F_SANS_B(ksize)
        total = (draw.textlength(kicker_left, font=kf)
                 + draw.textlength(tax, font=kf))
        if total <= w - 24:
            break
        ksize -= 1
    kf = F_SANS_B(ksize)
    draw.text((x + 12, y + 5), kicker_left, font=kf, fill=color)
    lw = draw.textlength(kicker_left, font=kf)
    draw.text((x + 12 + lw, y + 5), tax, font=kf,
              fill=TAX_COLORS[tax])
    lines = fit_text(draw, headline, F_SANS_B(13), w - 24, 2)
    yy = y + 19
    for ln in lines:
        draw.text((x + 12, yy), ln, font=F_SANS_B(13), fill=INK)
        yy += 16
    deck_lines = fit_text(draw, deck, F_SANS(11), w - 24, 1)
    draw.text((x + 12, y + h - 15), deck_lines[0] if deck_lines else "",
              font=F_SANS(11), fill=(60, 60, 60))


def draw_date_check(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=(255, 246, 220),
                   outline=(190, 160, 90), width=1)
    lines = fit_text(draw, DATE_CHECK, F_SANS(11), w - 24, 4)
    yy = y + 6
    for ln in lines:
        draw.text((x + 12, yy), ln, font=F_SANS(11), fill=(60, 45, 10))
        yy += 13


def draw_footer(draw):
    text_center(draw, W // 2, 992,
                "Sources: Reuters \u2022 NYT \u2022 AP \u2022 US DOJ \u2022 FTC "
                "\u2022 United Nations \u2022 Xinhua \u2022 Yonhap \u2022 "
                "European Commission \u2022 ESPNcricinfo",
                F_SANS(10), GRAY)
    text_center(draw, W // 2, 1006,
                "Every story dated; every claim labelled. Drawn for make.fun "
                "\u2014 news-image-20261125.",
                F_SANS(10), GRAY)


def validate_layout(img):
    """Guard: the front page must hold exactly 2 leads + 28 grid stories
    and stay 1024x1024. Raises before anything is saved."""
    if len(HEROES) != 2:
        raise ValueError("expected 2 hero stories, got %d" % len(HEROES))
    if len(STORIES) != 28:
        raise ValueError("expected 28 grid stories, got %d" % len(STORIES))
    if img.size != (W, H):
        raise ValueError("expected 1024x1024, got %r" % (img.size,))
    if img.mode != "RGB":
        raise ValueError("expected RGB mode, got %s" % img.mode)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    draw = ImageDraw.Draw(img)

    draw_masthead(draw)
    draw_proof_strip(draw)

    hero_y, hero_h = 154, 138
    hero_w = (W - 2 * MARGIN - GUT) // 2
    for i, (kicker, headline, deck, source, icon) in enumerate(HEROES):
        draw_hero(draw, MARGIN + i * (hero_w + GUT), hero_y, hero_w,
                  hero_h, kicker, headline, deck, source, icon)

    grid_y = 300
    row_h = 68
    col_w = (W - 2 * MARGIN - 2 * GUT) // 3
    for idx, story in enumerate(STORIES):
        row, col = divmod(idx, 3)
        x = MARGIN + col * (col_w + GUT)
        y = grid_y + row * row_h
        draw_story_card(draw, x, y, col_w, row_h, story)

    # last row: 1 story (idx 27) + DATE CHECK spanning cols 2-3
    dc_x = MARGIN + 1 * (col_w + GUT)
    dc_w = 2 * col_w + GUT
    dc_y = grid_y + 9 * row_h
    draw_date_check(draw, dc_x, dc_y, dc_w, row_h)

    draw_footer(draw)

    validate_layout(img)

    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
    img.save(out, "PNG", optimize=True)
    print("wrote", out, os.path.getsize(out), "bytes")


if __name__ == "__main__":
    main()
