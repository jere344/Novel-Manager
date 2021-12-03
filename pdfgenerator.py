from fpdf import FPDF
import lib
from os.path import isfile


def Generate(novel):
    """Generate the novel pdf with the files in DATA/novel"""
    pdf = FPDF()
    font = lib.style.get("GLOBAL", "font")
    pdf.add_font(
        font,
        style="",
        fname=str(lib.__location__.joinpath("DATA", font)),
        uni=True,
    )
    pdf.set_font(font, size=12)
    pdf.set_margins(20, 20)

    pdf.add_page()
    pdf.image(
        lib.__location__.joinpath(
            lib.config.get(novel, "picture").replace("-resized", "")
        )
    )
    pdf.add_page()

    i = 1
    while isfile(lib.__location__.joinpath("DATA", novel, f"{novel} chapter {i}.txt")):
        with open(
            lib.__location__.joinpath("DATA", novel, f"{novel} chapter {i}.txt"),
            "r",
            encoding="utf-8",
        ) as chapter_file:

            pdf.multi_cell(0, txt=chapter_file.read())
            pdf.add_page()

        i += 1

    pdf.output(
        lib.__location__.joinpath("pdf", f"{novel} chapter 1 to {i-1}.pdf"),
    )


# Generate("the-beginning-after-the-end-web-novel-07101329")
