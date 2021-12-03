import lib


def SetUrl(novel):
    scraper = __import__(lib.config.get(novel, "source"))
    lib.config.set(novel, "url", scraper.Url(novel))


def SetCleanName(novel):
    scraper = __import__(lib.config.get(novel, "source"))
    lib.config.set(novel, "cleanname", scraper.CleanName(novel))


def Save(config=False, chapterlist=False, style=False):
    """Save config files"""
    if config:
        with open(
            lib.__location__.joinpath("config", "config.ini"), "w", encoding="utf-8"
        ) as configfile:
            lib.config.write(configfile)

    if chapterlist:
        with open(
            lib.__location__.joinpath("config", "chapterlist.ini"),
            "w",
            encoding="utf-8",
        ) as configfile:
            lib.chapterlist.write(configfile)

    if style:
        with open(
            lib.__location__.joinpath("config", "style.ini"), "w", encoding="utf-8"
        ) as configfile:
            lib.style.write(configfile)


def SetCover(novel: str) -> str:
    """This function put the less work possible on the scraper script

    Save the cover in DATA/novel twice : one raw and the other resized.
    Return the path to the resized one

    And save the pic path in the novel section of lib.config"""
    scraper = __import__(lib.config.get(novel, "source"))
    pic = scraper.ScrapPic(novel, lib.proxies)

    relative_path = str(lib.__location__.joinpath("DATA", novel, novel))

    # Put the picture in DATA/novel
    with open(relative_path + pic[1], "wb") as file:
        file.write(pic[0])

    # create a resized image for easier loading in gui later
    from PIL import Image

    image = Image.open(relative_path + pic[1])
    image.resize((230, 330)).save(relative_path + "-resized" + pic[1])

    lib.config.set(novel, "Picture", f"DATA/{novel}/{novel}-resized{pic[1]}")


def SetChapter(novel: str, chapter_number: str):
    """This function put the less work possible on the scraper script

    write the chapter text retrieved by the scraper script in DATA/novel.
    Check beforehand if there is the title in chapterlist

    """
    scraper = __import__(lib.config.get(novel, "source"))
    info_chapter = lib.chapterlist.get(novel, chapter_number)

    ch = scraper.ScrapText(lib.proxies, info_chapter).strip()

    with open(
        lib.__location__.joinpath(
            "DATA", novel, f"{novel} chapter {chapter_number}.txt"
        ),
        "w",
        encoding="utf-8",
    ) as chapter:

        chapter.write(ch)


def SetTotalDownloaded():
    """Calculate the sum of the downloaded chapter and set the total in config"""
    total = sum(
        [
            int(lib.config.get(section, "downloadedchapter"))
            for section in lib.config.sections()[1:]
        ]
    )
    lib.config.set("*USER*", "totaldownloaded", str(total))


def SetTotalRead():
    """Calculate the sum of the read chapter and set the total in config"""
    total = sum(
        [
            int(lib.config.get(section, "chapterread"))
            for section in lib.config.sections()[1:]
        ]
    )
    lib.config.set("*USER*", "totalread", str(total))


def SetMaxChapter(novel: str):
    """just get the number of chapters from chapterlist"""

    i = 1
    while True:
        try:
            lib.chapterlist.get(novel, str(i))
        except lib.configparser.NoOptionError:
            break
        i += 1

    lib.config.set(novel, "MaxChapter", str(i - 1))


def SetDownloaded(novel: str) -> str:
    "just count the number of chapter in /DATA/novel/"
    i = 1
    from os.path import isfile

    while isfile(lib.__location__.joinpath("DATA", novel, f"{novel} chapter {i}.txt")):
        i += 1

    lib.config.set(novel, "downloadedchapter", str(i - 1))


def DeleteNovel(novel):
    from shutil import rmtree

    try:
        rmtree(str(lib.__location__.joinpath("DATA", novel)))
    except FileNotFoundError:
        pass

    lib.config.remove_section(novel)
    lib.chapterlist.remove_section(novel)


def SetSummary(novel):
    scraper = __import__(lib.config.get(novel, "source"))
    summary = scraper.ScrapSummary(novel, lib.proxies)
    lib.config.set(novel, "summary", summary)


def SetChapterList(novel: str):
    scraper = __import__(lib.config.get(novel, "source"))

    ch = scraper.ScrapChapterList(novel, lib.proxies)

    try:
        lib.chapterlist.add_section(novel)
    except lib.configparser.DuplicateSectionError:
        pass

    for element, value in ch.items():
        lib.chapterlist.set(novel, element, value[0])
