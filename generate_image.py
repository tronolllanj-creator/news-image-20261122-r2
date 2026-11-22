import sys
from PIL import Image, ImageDraw, ImageFont

BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
REG = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

INK = (20, 33, 61)
NAVY = (27, 42, 74)
RED = (193, 39, 45)
TEAL = (14, 124, 123)
GOLD = (217, 164, 65)
PAPER = (247, 241, 227)
WHITE = (255, 255, 255)


def load(bold, size):
    path = BOLD if bold else REG
    return ImageFont.truetype(path, size)


def wrap_text(draw, text, font, max_width):
    words = text.split()
    lines = []
    cur = ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=font) <= max_width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines if lines else [""]


def draw_wrapped(draw, xy, lines, font, fill, leading):
    x, y = xy
    for line in lines:
        draw.text((x, y), line, font=font, fill=fill)
        y += leading
    return y


def chip(draw, xy, label, color, lsize):
    f = load(True, lsize)
    w = int(draw.textlength(label, font=f)) + 14
    h = 22
    x, y = xy
    draw.rounded_rectangle((x, y, x + w, y + h), radius=5, fill=color)
    draw.text((x + 7, y + 4), label, font=f, fill=WHITE)
    return h


def icon_box(draw, x, y, s, color, style):
    draw.rectangle((x, y, x + s, y + s), outline=color, width=2)
    if style == "shield":
        cx, cy = x + s // 2, y + s // 2
        draw.line((cx, y + int(s * 0.22), cx, y + int(s * 0.72)), fill=color, width=3)
        draw.line((x + int(s * 0.25), cy, x + int(s * 0.75), cy), fill=color, width=3)
    elif style == "bolt":
        poly = [
            (x + s * 0.55, y + int(s * 0.15)),
            (x + int(s * 0.3), y + s * 0.55),
            (x + s * 0.48, y + s * 0.55),
            (x + int(s * 0.42), y + int(s * 0.85)),
            (x + int(s * 0.72), y + s * 0.42),
            (x + s * 0.55, y + s * 0.42),
        ]
        draw.polygon(poly, fill=color)
    elif style == "temp":
        cx = x + s // 2
        ly = y + int(s * 0.7)
        draw.line((cx, y + int(s * 0.3), cx, ly), fill=color, width=3)
        draw.ellipse((cx - int(s * 0.12), ly, cx + int(s * 0.12), ly + int(s * 0.24)), fill=color)
    elif style == "missile":
        cx = x + s // 2
        draw.polygon(
            [(cx, y + int(s * 0.15)), (cx - int(s * 0.16), y + int(s * 0.55)), (cx + int(s * 0.16), y + int(s * 0.55))],
            fill=color,
        )
        draw.line((cx - int(s * 0.16), y + int(s * 0.55), cx - int(s * 0.22), y + int(s * 0.8)), fill=color, width=2)
        draw.line((cx + int(s * 0.16), y + int(s * 0.55), cx + int(s * 0.22), y + int(s * 0.8)), fill=color, width=2)
    elif style == "gate":
        cx = x + s // 2
        draw.line((cx, y + int(s * 0.2), cx, y + int(s * 0.8)), fill=color, width=3)
        draw.line((x + int(s * 0.25), y + int(s * 0.3), x + int(s * 0.75), y + int(s * 0.7)), fill=color, width=2)
        draw.line((x + int(s * 0.75), y + int(s * 0.3), x + int(s * 0.25), y + int(s * 0.7)), fill=color, width=2)
    elif style == "lock":
        cx = x + s // 2
        draw.arc((cx - int(s * 0.2), y + int(s * 0.18), cx + int(s * 0.2), y + int(s * 0.56)), start=180, end=0, fill=color, width=3)
        draw.rectangle((cx - int(s * 0.28), y + int(s * 0.4), cx + int(s * 0.28), y + int(s * 0.8)), outline=color, width=2)
    elif style == "mic":
        cx = x + s // 2
        draw.ellipse((cx - int(s * 0.12), y + int(s * 0.2), cx + int(s * 0.12), y + int(s * 0.55)), outline=color, width=2)
        draw.arc((cx - int(s * 0.22), y + int(s * 0.35), cx + int(s * 0.22), y + int(s * 0.8)), start=0, end=180, fill=color, width=2)
        draw.line((cx, y + int(s * 0.8), cx, y + int(s * 0.9)), fill=color, width=2)
    elif style == "wave":
        for i in range(4):
            yy = y + int(s * (0.3 + i * 0.12))
            xx = x + int(s * 0.2)
            draw.line((xx, yy, x + int(s * 0.8), yy), fill=color, width=2)
        draw.ellipse((x + int(s * 0.5) - 3, y + int(s * 0.5) - 3, x + int(s * 0.5) + 3, y + int(s * 0.5) + 3), fill=color)
    elif style == "vote":
        draw.rectangle((x + int(s * 0.2), y + int(s * 0.35), x + int(s * 0.8), y + int(s * 0.8)), outline=color, width=2)
        draw.polygon(
            [(x + int(s * 0.35), y + int(s * 0.35)), (x + int(s * 0.55), y + int(s * 0.35)), (x + int(s * 0.5), y + int(s * 0.6))],
            fill=color,
        )
    elif style == "ball":
        cx, cy = x + s // 2, y + s // 2
        r = int(s * 0.32)
        draw.ellipse((cx - r, cy - r, cx + r, cy + r), outline=color, width=2)
        draw.line((cx - r, cy, cx + r, cy), fill=color, width=2)


def draw_variant1():
    img = Image.new("RGB", (1024, 1024), PAPER)
    d = ImageDraw.Draw(img)

    f_mast = load(True, 46)
    f_date = load(True, 34)
    f_lead = load(True, 30)
    f_leadsum = load(False, 16)
    f_chip = load(True, 13)
    f_head = load(True, 20)
    f_sub = load(False, 13)
    f_ticker = load(True, 14)
    f_foot = load(False, 14)

    MY = 24
    MW = 976
    MX = (1024 - MW) // 2

    d.rectangle((MX, MY, MX + MW, MY + 96), fill=NAVY)
    txt = "THE WORLD IN ONE IMAGE"
    d.text((MX + (MW - d.textlength(txt, font=f_mast)) // 2, MY + 14), txt, font=f_mast, fill=WHITE)
    dtxt = "SUNDAY 22 NOVEMBER 2026"
    d.text((MX + (MW - d.textlength(dtxt, font=f_date)) // 2, MY + 62), dtxt, font=f_date, fill=GOLD)
    d.rectangle((MX, MY + 97, MX + MW, MY + 100), fill=RED)

    ly0 = MY + 112
    lh = 168
    d.rectangle((MX, ly0, MX + MW, ly0 + lh), fill=INK)
    d.rectangle((MX, ly0, MX + 8, ly0 + lh), fill=RED)
    chip(d, (MX + 10, ly0 + 12), "SECURITY", RED, 13)
    _ll = wrap_text(d, "MEXICO CAPTURES CARTEL BOSS 'EL CHAPO ISIDRO' IN GUASAVE RAID; 11 DEAD", f_lead, MW - 40)
    _ly = draw_wrapped(d, (MX + 20, ly0 + 20), _ll[:2], f_lead, WHITE, 34)
    d.text((MX + 20, ly0 + 124), "Fausto Isidro Meza Flores was the FBI\'s most wanted; the clash killed 7 gunmen", font=f_leadsum, fill=(223, 227, 235))
    d.text((MX + 20, ly0 + 144), "and 4 Mexican soldiers; he was later flown to Mexico City for interrogation.", font=f_leadsum, fill=(223, 227, 235))

    py = ly0 + lh + 10
    pw = (MW - 10) // 2

    def panel(x, y, chip_label, ccolor, head, sub, istyle):
        d.rectangle((x, y, x + pw, y + 120), outline=INK, width=1, fill=(255, 251, 242))
        d.rectangle((x, y, x + 4, y + 120), fill=ccolor)
        icon_box(d, x + 14, y + 14, 34, ccolor, istyle)
        chip(d, (x + 60, y + 16), chip_label, ccolor, 12)
        hlines = wrap_text(d, head, f_head, pw - 16)
        draw_wrapped(d, (x + 14, y + 58), hlines[:2], f_head, INK, 24)
        slines = wrap_text(d, sub, f_sub, pw - 30)
        draw_wrapped(d, (x + 14, y + 96), slines[:1], f_sub, (70, 74, 88), 16)

    panel(MX, py, "CLIMATE", TEAL, "COP31 DEADLOCKED IN OVERTIME OVER FOSSIL FUELS", "Turkey talks stall with no final agreement yet reached.", "temp")
    panel(MX + pw + 10, py, "CONFLICT", RED, "RUSSIAN MISSILES STRIKE POLAND", "NATO calls it a grave violation of its airspace.", "missile")

    py3 = py + 130
    pw3 = (MW - 20) // 3

    def tile(x, y, lab, ccol, head, sub, istyle):
        d.rectangle((x, y, x + pw3, y + 130), outline=INK, width=1, fill=(255, 251, 242))
        d.rectangle((x, y, x + 4, y + 130), fill=ccol)
        icon_box(d, x + 14, y + 12, 30, ccol, istyle)
        chip(d, (x + 14, y + 48), lab, ccol, 12)
        hl = wrap_text(d, head, load(True, 16), pw3 - 24)
        draw_wrapped(d, (x + 14, y + 76), hl[:2], load(True, 16), INK, 20)
        sl = wrap_text(d, sub, load(False, 12), pw3 - 24)
        draw_wrapped(d, (x + 14, y + 116), sl[:1], load(False, 12), (70, 74, 88), 14)

    tile(MX, py3, "SECURITY", NAVY, "ESTONIA WILL CLOSE ITS BORDER WITH RUSSIA", "Moscow decries the move as a \"new Iron Curtain\".", "gate")
    tile(MX + pw3 + 10, py3, "SECURITY", GOLD, "FBI PROBES APPARENT HACK OF ITS DATA", "An investigation centres on the criminal database.", "lock")
    tile(MX + 2 * (pw3 + 10), py3, "SECURITY", RED, "DENMARK: RUSSIA PLOTTED RAPPER KILLING", "Target was a US-Ukrainian artist, the state says.", "mic")

    ty = py3 + 140
    d.rectangle((MX, ty, MX + MW, ty + 40), fill=INK)
    t = "  PERU ANDES 6.9 QUAKE, FELT IN LIMA, NO CASUALTIES   |   SOUTH AFRICA LOCAL ELECTIONS, ANC FIGHT FOR CITIES   |   AUSTRALIA BREAKS ENGLAND'S 7-MATCH T20 STREAK   |"
    tf = load(True, 14)
    d.text((MX + (MW - d.textlength(t, font=tf)) // 2, ty + 10), t, font=tf, fill=GOLD)

    ftxt = "All stories first reported 22 November 2026"
    d.line((MX, ty + 52, MX + MW, ty + 52), fill=INK, width=1)
    d.text((MX + (MW - d.textlength(ftxt, font=f_foot)) // 2, ty + 58), ftxt, font=f_foot, fill=(70, 74, 88))

    return img


def draw_variant2():
    img = Image.new("RGB", (1024, 1024), PAPER)
    d = ImageDraw.Draw(img)

    f_title = load(True, 38)
    f_date = load(True, 22)
    f_chip = load(True, 11)
    f_head = load(True, 18)
    f_sub = load(False, 12)

    bw = 976
    bx = (1024 - bw) // 2
    by = 20
    bh = 74
    d.rectangle((bx, by, bx + bw, by + bh), fill=NAVY)
    t = "THE WORLD IN ONE IMAGE"
    d.text((bx + (bw - d.textlength(t, font=f_title)) // 2, by + 8), t, font=f_title, fill=WHITE)
    dt = "SUNDAY 22 NOVEMBER 2026"
    d.text((bx + (bw - d.textlength(dt, font=f_date)) // 2, by + 46), dt, font=f_date, fill=GOLD)
    d.rectangle((bx, by + bh, bx + bw, by + bh + 4), fill=RED)

    gx = 20
    gy = 108
    gw = 984
    gh = 896
    cw = (gw - 16) // 2
    chh = (gh - 12) // 3

    stories = [
        ("SECURITY", RED, "shield", "MEXICO CAPTURES \"EL CHAPO ISIDRO\"", "Guasave raid kills 11; FBI target flown to Mexico City."),
        ("CLIMATE", TEAL, "temp", "COP31 DEADLOCKED IN OVERTIME", "Turkish talks stall over fossil fuels, no deal yet."),
        ("CONFLICT", RED, "missile", "RUSSIAN MISSILES HIT POLAND", "NATO: grave violation of its airspace."),
        ("SECURITY", NAVY, "gate", "ESTONIA CLOSES BORDER WITH RUSSIA", "Moscow calls it a \"new Iron Curtain\"."),
        ("SECURITY", GOLD, "lock", "FBI PROBES HACK OF ITS DATABASE", "Investigation of criminal database breach."),
        ("SECURITY", TEAL, "mic", "DENMARK: RUSSIA PLOTTED RAPPER KILL", "Target a US-Ukrainian artist; bridge strikes defended."),
    ]

    for i, (lab, color, style, head, sub) in enumerate(stories):
        row = i // 2
        col = i % 2
        x = gx + col * (cw + 16)
        y = gy + row * (chh + 12)
        d.rectangle((x, y, x + cw, y + chh), outline=INK, width=1, fill=WHITE)
        d.rectangle((x, y, x + 5, y + chh), fill=color)
        icon_box(d, x + cw - 40, y + 12, 28, color, style)
        chip(d, (x + 15, y + 12), lab, color, 11)
        hy = y + 46
        icon_x = x + 15
        icon_s = 34
        for li, line in enumerate(wrap_text(d, head, f_head, cw - 30)[:2]):
            d.text((icon_x, hy + li * 22), line, font=f_head, fill=INK)
            icon_y = hy + li * 22 + 6
        sx = x + 15
        sw = cw - 30
        d.line((sx, y + chh - 54, x + cw - 15, y + chh - 54), fill=(210, 204, 190), width=1)
        for li, line in enumerate(wrap_text(d, sub, f_sub, sw)[:2]):
            d.text((sx, y + chh - 48 + li * 16), line, font=f_sub, fill=(70, 74, 88))
    return img


def draw_variant3():
    img = Image.new("RGB", (1024, 1024), PAPER)
    d = ImageDraw.Draw(img)

    f_head = load(True, 38)
    f_sum = load(False, 19)
    f_chip = load(True, 13)
    f_brief = load(True, 15)
    f_briefsub = load(False, 12)
    f_ticker = load(True, 15)
    f_foot = load(False, 13)
    f_bigchip = load(True, 40)

    MX, MW = 24, 976

    d.rectangle((MX, 10, MX + MW, 66), fill=NAVY)
    dtxt = "SUNDAY 22 NOVEMBER 2026"
    d.text((MX + (MW - d.textlength(dtxt, font=f_head)) // 2, 16), dtxt, font=f_head, fill=GOLD)
    d.rectangle((MX, 66, MX + MW, 71), fill=RED)

    chip(d, (MX, 84), "SECURITY - LEAD", RED, 15)
    hh = wrap_text(d, "MEXICO CAPTURES \u201cEL CHAPO ISIDRO\u201d IN GUASAVE RAID; 11 DEAD", f_bigchip, MW)[0:2]
    hy = 120
    for line in hh:
        d.text((MX, hy), line, font=f_bigchip, fill=INK)
        hy += 46
    hy = max(hy, 120)
    for li, line in enumerate(wrap_text(d, "FBI most-wanted Fausto Isidro Meza Flores was captured in Guasave; 11 were killed in the clash.", f_sum, MW)[0:2]):
        d.text((MX, hy + li * 26), line, font=f_sum, fill=(70, 74, 88))
    d.line((MX, hy + 62, MX + MW, hy + 62), fill=RED, width=3)

    briefs = [
        ("CLIMATE", TEAL, "temp", "COP31 DEADLOCKED IN OVERTIME", "Turkish talks stall over fossil fuels, with no final agreement yet."),
        ("CONFLICT", RED, "missile", "RUSSIAN MISSILES HIT POLAND", "NATO called it a grave violation of its airspace."),
        ("SECURITY", NAVY, "gate", "ESTONIA CLOSES ITS BORDER WITH RUSSIA", "Moscow decried the move as a \u201cnew Iron Curtain\u201d."),
        ("SECURITY", GOLD, "lock", "FBI PROBES HACK OF ITS CRIMINAL DATABASE", "The bureau said it is investigating the apparent breach."),
        ("SECURITY", TEAL, "mic", "DENMARK: RUSSIA PLOTTED RAPPER KILLING", "The target was a US-Ukrainian artist, the state said."),
    ]
    brief_top = hy + 70
    brief_bottom = 862
    rh = (brief_bottom - brief_top - 4 * 14) // 5
    gap = (brief_bottom - brief_top - rh * 5) // 4
    ry = brief_top
    icon_s = 40
    for lab, col, sty, head, sub in briefs:
        d.rectangle((MX, ry, MX + MW, ry + rh), outline=(210, 204, 190), width=1, fill=(255, 251, 242))
        d.rectangle((MX, ry, MX + 6, ry + rh), fill=col)
        icon_box(d, MX + 18, ry + (rh - icon_s) // 2, icon_s, col, sty)
        chip(d, (MX + 74, ry + 10), lab, col, 13)
        hy2 = ry + 44
        d.text((MX + 74, hy2), head, font=f_brief, fill=INK)
        d.text((MX + 74, ry + rh - 20), sub, font=f_briefsub, fill=(70, 74, 88))
        ry += rh + 8

    ty = 872
    d.rectangle((MX, ty, MX + MW, ty + 92), fill=INK)
    ticker = wrap_text(d, "TICKER |  PERU ANDES 6.9 QUAKE, FELT IN LIMA, NO CASUALTIES  \u00b7  SOUTH AFRICA VOTES, ANC FIGHTS FOR CITIES  \u00b7  AUSTRALIA BREAKS ENGLAND\u2019S 7-MATCH T20 STREAK", f_ticker, MW - 30)[0:2]
    ty2 = ty + 12
    for line in ticker:
        d.text((MX + 16, ty2), line, font=f_ticker, fill=GOLD)
        ty2 += 22
    d.line((MX, ty + 58, MX + MW, ty + 58), fill=(70, 80, 100), width=1)
    ftxt = "All stories first reported 22 November 2026"
    d.text((MX + (MW - d.textlength(ftxt, font=f_foot)) // 2, ty + 66), ftxt, font=f_foot, fill=(200, 206, 220))
    return img


def main():
    variant = sys.argv[1] if len(sys.argv) > 1 else "1"
    fn = globals().get("draw_variant" + variant)
    if fn is None:
        print("unknown variant", variant)
        sys.exit(2)
    img = fn()
    assert img.size == (1024, 1024)
    out = "out_" + variant + ".png"
    img.save(out)
    n = len(open(out, "rb").read())
    print("wrote " + out + " 1024x1024 bytes " + str(n))

if __name__ == "__main__":
    main()
