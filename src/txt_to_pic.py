from PIL import Image, ImageFont, ImageDraw
from pathlib import Path as pa
import textwrap

def_font = pa.cwd() / "assets" / "fonts" / "shabnam.ttf"
base_pic = pa.cwd() / "assets" / "frames" / "semi.png"

source_pic = pa.cwd() / "assets" / "exports"


def text_to_pic(
    text, writer, font=def_font, font_size=30, pic=base_pic, align="center"
):
    text_font = ImageFont.truetype(str(font), size=font_size, encoding="unic")
    writer_font = ImageFont.truetype(str(font), size=15, encoding="unic")

    text = "\n".join([textwrap.fill(line, 25) for line in text.split("\n")])

    with Image.open(base_pic) as picture:
        draw = ImageDraw.Draw(picture)
        draw.text(
            xy=gen_xy(text, align)[0],
            text=text,
            font=text_font,
            align=align,
            fill="black",
            anchor=f"{gen_xy(text, align)[1]}m",
            stroke_width=4,
            stroke_fill="white",
            direction="rtl",
        )

        draw.text(
            xy=(512 / 2, 512 - 70),
            text=writer,
            font=writer_font,
            anchor=f"mm",
            fill="black",
            stroke_width=2,
            stroke_fill="white",
            direction="rtl",
        )
        draw.text(
            xy=(512 - 80, 60),
            text="سخن بزرگان:",
            font=writer_font,
            align="right",
            fill="brown",
            anchor="rm",
            stroke_width=2,
            stroke_fill="white",
            direction="rtl",
        )
    picture.save(source_pic / "sticker.png")
    picture.save(source_pic / "sticker.webp", "webp")


def gen_xy(text, mode="center"):
    DIMEN = 512
    Y_MAR = DIMEN / 2
    X_MAR = 70

    lines = text.count("\n")
    Y_MAR -= lines * 2

    center = DIMEN / 2
    if mode == "center":
        return ((center, Y_MAR), "m")
    elif mode == "left":
        return ((X_MAR, Y_MAR), "l")
    elif mode == "right":
        return ((DIMEN - X_MAR, Y_MAR), "r")
