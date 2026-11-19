#!/usr/bin/env python3
"""News front page for Wednesday 18 November 2026.

Draws a 1024x1024 newspaper front page summing up the day's world news
and writes it to /output/entry.png.

Deterministic: all text, layout and colours are fixed in this file. No
network, no clock, no randomness, no system fonts (the DejaVu fonts the
page uses are bundled in fonts/ next to this script, so the program renders
identically wherever it runs).

Stories (as reported on 18 November 2026 by AP, Reuters, BBC, PAHO/CDC,
Nvidia and NASA JPL, via the day's news briefs):
  1. Xi Jinping and Vladimir Putin meet in Shenzhen, a day before the
     first-ever three-way summit with Donald Trump; APEC opens.
  2. U.S. jets strike an Iranian missile site on Qeshm Island; Iran fires
     drones at U.S. bases in Kuwait and Bahrain.
  3. Democrat Mary Peltola wins Alaska's Senate race; Democrats take a
     56-44 majority, their ninth flip of the midterms.
  4. The U.S. loses measles-elimination status after 26 years; 5,412 cases
     recorded in 2026, the most since 1991.
  5. Nvidia posts a record $115.8B quarter, revenue up 103% year on year,
     in its first earnings since Jensen Huang's exit.
  6. Voyager 1 reaches one light-day from Earth, about 16 billion miles,
     a distance no human-made object has crossed before.
"""

import os

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (248, 244, 232)
INK = (17, 17, 17)
RED = (163, 30, 34)
GREY = (90, 86, 78)

HERE = os.path.dirname(os.path.abspath(__file__))
FONT_DIR = os.path.join(HERE, "fonts")


def font(name, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)


SERIF_B = "DejaVuSerif-Bold.ttf"
SANS = "DejaVuSans.ttf"
SANS_B = "DejaVuSans-Bold.ttf"


def wrap(draw, text, fnt, max_width):
    """Greedy word wrap; returns a list of lines that fit max_width."""
    lines, cur = [], ""
    for word in text.split():
        trial = word if not cur else cur + " " + word
        if draw.textlength(trial, font=fnt) <= max_width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def block(draw, x, y, width, kicker, headline, deck, hsize, dsize,
          align="left", hspace=4, dspace=3):
    """Draw one story block; returns the y just below it."""
    fk = font(SANS_B, 20)
    fh = font(SERIF_B, hsize)
    fd = font(SANS, dsize)
    if kicker:
        draw.text((x, y), kicker, font=fk, fill=RED)
        y += 30
    lines = wrap(draw, headline, fh, width)
    for ln in lines:
        lx = x if align == "left" else x + (width - draw.textlength(ln, font=fh)) // 2
        draw.text((lx, y), ln, font=fh, fill=INK)
        y += hsize + hspace
    if deck:
        y += 2
        for ln in wrap(draw, deck, fd, width):
            lx = x if align == "left" else x + (width - draw.textlength(ln, font=fd)) // 2
            draw.text((lx, y), ln, font=fd, fill=INK)
            y += dsize + dspace
    return y


def rule(draw, x, y, width, thick=2):
    draw.rectangle([x, y, x + width, y + thick - 1], fill=INK)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # Double border frame.
    d.rectangle([14, 14, W - 15, H - 15], outline=INK, width=3)
    d.rectangle([24, 24, W - 25, H - 25], outline=INK, width=1)

    x, cw = 44, W - 88  # content x and width

    # Masthead.
    fm = font(SERIF_B, 96)
    title = "THE WORLD"
    d.text(((W - d.textlength(title, font=fm)) // 2, 30), title,
           font=fm, fill=INK)
    rule(d, x, 148, cw, 2)
    fd_line = font(SANS_B, 27)
    date = "WEDNESDAY, 18 NOVEMBER 2026"
    d.text(((W - d.textlength(date, font=fd_line)) // 2, 158), date,
           font=fd_line, fill=INK)
    rule(d, x, 200, cw, 5)
    rule(d, x, 208, cw, 1)

    # Lead story: Xi and Putin in Shenzhen.
    y = block(d, x, 224, cw,
              "SUMMIT  —  SHENZHEN",
              "XI AND PUTIN MEET IN SHENZHEN",
              "Leaders hold talks a day before the first-ever three-way summit "
              "with Trump, as APEC opens with trade and sanctions on the agenda.",
              54, 22, align="center")
    rule(d, x, y + 10, cw, 2)

    # Row two: Middle East | U.S. politics.
    col_w = (cw - 24) // 2
    y2 = y + 26
    left_end = block(d, x, y2, col_w,
                     "MIDDLE EAST",
                     "U.S. STRIKES IRAN SITE; IRAN HITS BACK",
                     "Iran fires drones at U.S. bases in Kuwait and Bahrain "
                     "after U.S. jets hit a missile site on Qeshm Island.",
                     34, 20)
    right_end = block(d, x + col_w + 24, y2, col_w,
                      "U.S. POLITICS",
                      "DEMOCRATS TAKE SENATE 56–44",
                      "Peltola wins Alaska, the ninth Democratic flip of the "
                      "midterms and the party's largest majority since 2009.",
                      34, 20)
    y3 = max(left_end, right_end)
    d.line([x + col_w + 12, y2, x + col_w + 12, y3 - 6], fill=GREY, width=1)
    rule(d, x, y3 + 8, cw, 2)

    # Row three: health | tech | space.
    c3 = (cw - 48) // 3
    y4 = y3 + 24
    ends = []
    ends.append(block(d, x, y4, c3,
                      "HEALTH",
                      "U.S. LOSES MEASLES-FREE STATUS",
                      "After 26 years; 5,412 cases in 2026, the most since 1991.",
                      27, 19))
    ends.append(block(d, x + c3 + 24, y4, c3,
                      "TECH",
                      "NVIDIA POSTS RECORD $115.8B QUARTER",
                      "Revenue doubles in a year; first earnings since "
                      "Huang's exit.",
                      27, 19))
    ends.append(block(d, x + 2 * (c3 + 24), y4, c3,
                      "SPACE",
                      "VOYAGER 1 REACHES ONE LIGHT-DAY",
                      "16 billion miles from Earth — no human-made object "
                      "has gone farther.",
                      27, 19))
    y5 = max(ends)
    for gx in (x + c3 + 12, x + 2 * c3 + 36):
        d.line([gx, y4, gx, y5 - 6], fill=GREY, width=1)
    rule(d, x, y5 + 12, cw, 2)

    # Footer.
    ff = font(SANS_B, 18)
    foot = "SIX TOP STORIES  ·  WEDNESDAY 18 NOVEMBER 2026  ·  THE WORLD"
    d.text(((W - d.textlength(foot, font=ff)) // 2, y5 + 22), foot,
           font=ff, fill=GREY)
    fs = font(SANS, 15)
    src = "Sources: AP  ·  Reuters  ·  BBC  ·  PAHO/CDC  ·  Nvidia  ·  NASA JPL"
    d.text(((W - d.textlength(src, font=fs)) // 2, y5 + 48), src,
           font=fs, fill=GREY)

    os.makedirs("/output", exist_ok=True)
    img.save("/output/entry.png", format="PNG")


if __name__ == "__main__":
    main()
