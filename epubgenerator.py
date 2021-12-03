from ebooklib import epub
import os.path
import lib


def Generate(novel):
    """Generate the novel epub with the files in DATA/novel"""

    book = epub.EpubBook()
    # set metadata
    book.set_identifier("N/A")
    book.set_title(novel)
    book.set_language("en")
    book.add_author("N/A")
    pic = lib.config.get(novel, "picture").replace("-resized", "")
    book.set_cover("image.jpg", open(lib.__location__.joinpath(pic), "rb").read())

    spine = []
    i = 1
    while os.path.isfile(
        lib.__location__.joinpath("DATA", novel, f"{novel} chapter {i}.txt")
    ):
        with open(
            lib.__location__.joinpath("DATA", novel, f"{novel} chapter {i}.txt"),
            "r",
            encoding="utf-8",
        ) as file:
            chapter_text = file.read().split("\n\n")

        # Search title
        title_line = 0
        for paragraph in chapter_text:
            if "# " in paragraph:
                break
            title_line += 1

        chapter = epub.EpubHtml(
            title=chapter_text[title_line][2:], file_name=f"chap_{i}.xhtml", lang="en"
        )

        chapter.content = "".join(
            (
                "<p>",
                str("\n\n".join(chapter_text[:title_line])).replace("\n", "<br>"),
                "<h1>",  # put the title in bold
                str("\n\n".join(chapter_text[title_line])).replace("\n", "")[2:],
                "</h1>",
                str("\n\n".join(chapter_text[title_line + 1 :])).replace("\n", "<br>"),
                "</p>",
            )
        )

        book.add_item(chapter)
        spine.append(chapter)

        i += 1

    with open(lib.__location__.joinpath("epubstyle.css"), encoding="utf-8") as style:
        css = epub.EpubItem(
            uid="stylesheet",
            file_name="stylesheet.css",
            media_type="text/css",
            content=style.read(),
        )

    book.toc = tuple(spine)

    book.add_item(epub.EpubNcx())
    book.add_item(epub.EpubNav())

    book.add_item(css)
    book.spine = spine
    epub.write_epub(
        lib.__location__.joinpath("epub", f"{novel} chapter 1 to {i-1}.epub"),
        book,
        {"epub3_pages": False},
    )


Generate("the-beginning-after-the-end-web-novel-07101329")
