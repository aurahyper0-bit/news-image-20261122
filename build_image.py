"""Render the 22 November 2026 front page as one 1024x1024 picture.

The page is a newspaper front: a black banner, a red date line, one lead
story across the full width, three shorter stories side by side, a dark
"also today" band and a small footer. Run it with `python3
build_image.py`; it writes entry.png next to this file.
"""

from pathlib import Path

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

PAGE = 1024
EDGE = 48
PAPER = (255, 255, 255)
CARBON = (0, 0, 0)
CRIMSON = (198, 12, 12)
SLATE = (30, 30, 30)
ASH = (105, 105, 105)
MIDNIGHT = (18, 18, 46)

DEJAVU = Path("/usr/share/fonts/truetype/dejavu")


def font_for(size, bold=True):
    name = "DejaVuSans-Bold.ttf" if bold else "DejaVuSans.ttf"
    return ImageFont.truetype(str(DEJAVU / name), size)


def split_lines(draw, text, font, width):
    """Yield the lines of text wrapped to fit inside width pixels."""
    for chunk in text.split("\n"):
        words = chunk.split()
        if not words:
            yield ""
            continue
        current = words[0]
        for word in words[1:]:
            candidate = current + " " + word
            if draw.textlength(candidate, font=font) <= width:
                current = candidate
            else:
                yield current
                current = word
        yield current


class FrontPage:
    """A blank page with the fonts and helpers for the front page."""

    def __init__(self):
        self.image = Image.new("RGB", (PAGE, PAGE), PAPER)
        self.draw = ImageDraw.Draw(self.image)
        self.masthead = font_for(66)
        self.dateline = font_for(34)
        self.headline = font_for(46)
        self.column_head = font_for(27)
        self.body = font_for(27, bold=False)
        self.small_body = font_for(22, bold=False)
        self.strip_head = font_for(26)
        self.strip_body = font_for(24, bold=False)
        self.footer = font_for(20, bold=False)

    def block(self, text, font, x, y, width, colour, leading=8):
        """Draw wrapped text at (x, y); return the y below the last line."""
        for line in split_lines(self.draw, text, font, width):
            self.draw.text((x, y), line, font=font, fill=colour)
            y += font.size + leading
        return y

    def banner(self):
        self.draw.rectangle([0, 0, PAGE, 96], fill=CARBON)
        self.draw.text((PAGE / 2, 48), "WORLD NEWS", font=self.masthead,
                       fill=PAPER, anchor="mm")

    def date_line(self):
        self.draw.text((PAGE / 2, 128), "SUNDAY, 22 NOVEMBER 2026",
                       font=self.dateline, fill=CRIMSON, anchor="mm")
        self.draw.line([EDGE, 160, PAGE - EDGE, 160], fill=CARBON, width=3)

    def lead(self):
        self.draw.text((EDGE, 182), "US ENVOYS HEAD FOR MOSCOW",
                       font=self.headline, fill=CARBON)
        self.draw.text((EDGE, 238), "AFTER ABU DHABI TALKS",
                       font=self.headline, fill=CARBON)
        lead = (
            "US negotiators Jared Kushner and Steve Witkoff wrapped up two days "
            "of trilateral talks in Abu Dhabi on Sunday and flew to Moscow to "
            "brief Vladimir Putin. Russia revived demands NATO pull back to its "
            "1997 lines, and leaked data put its military dead above 400,000."
        )
        self.block(lead, self.body, EDGE, 306, PAGE - 2 * EDGE, SLATE,
                   leading=6)
        self.draw.line([EDGE, 452, PAGE - EDGE, 452], fill=CARBON, width=2)

    def columns(self):
        width = 304
        starts = [EDGE, 360, 672]
        items = [
            ("TWO MORE TANKERS HIT NEAR HORMUZ",
             "Two outbound tankers were struck near Oman\u2019s Khasab on "
             "Saturday. One, the Torkel, was left burning."),
            ("SPARTA II ABLAZE AFTER DRONE STRIKE",
             "A Russian-linked cargo ship was hit by drones in the Gulf of "
             "Finland, caught fire and drifted into Finnish waters. All 16 "
             "crew were evacuated."),
            ("COP31 TALKS INTO SECOND OVERTIME DAY",
             "The Antalya climate summit ran past its deadline with no deal, "
             "as a draft dropping all mention of coal, oil and gas drew "
             "threats of a walkout."),
        ]
        top = 478
        for x, (headline, text) in zip(starts, items):
            self.draw.rectangle([x, top, x + 64, top + 5], fill=CRIMSON)
            y = self.block(headline, self.column_head, x, top + 18, width,
                           CARBON, leading=4)
            self.block(text, self.small_body, x, y + 6, width, SLATE,
                       leading=5)

    def also_today(self):
        self.draw.rectangle([0, 760, PAGE, 950], fill=MIDNIGHT)
        self.draw.text((EDGE, 782), "ALSO TODAY", font=self.strip_head,
                       fill=PAPER)
        strip = (
            "Iran says it downed two US drones over Hormuz  \u2022  France "
            "cost-of-living protests clash in Strasbourg  \u2022  S&P 500 "
            "suffers worst week since April 2025  \u2022  Quake 6.7 hits Peru, "
            "15 hurt"
        )
        self.block(strip, self.strip_body, EDGE, 822, PAGE - 2 * EDGE, PAPER,
                   leading=4)

    def foot(self):
        self.draw.text((PAGE / 2, 972),
                       "\u2014 compiled from major wire reports  \u2022  22 November 2026",
                       font=self.footer, fill=ASH, anchor="mm")

    def save(self):
        out = Path(__file__).resolve().parent / "entry.png"
        self.image.save(out, "PNG", optimize=True)
        print("wrote", out, out.stat().st_size, "bytes")


def main():
    page = FrontPage()
    page.banner()
    page.date_line()
    page.lead()
    page.columns()
    page.also_today()
    page.foot()
    page.save()


if __name__ == "__main__":
    main()
