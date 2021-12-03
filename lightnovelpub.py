from bs4 import BeautifulSoup, NavigableString
import cloudscraper


def CleanName(novel: str):
    """
    return the name cleaned.

    >>>CleanName('release-that-witch-19072354')
    >>>'Release That Witch'
    """
    novel = novel.split("-")
    if novel[-1].isnumeric():
        novel.pop()
    return " ".join(novel).title()


def ScrapPic(novel: str, proxies: dict) -> tuple:
    """return (picture_data, format of the picture)"""

    url = "https://www.lightnovelpub.com/novel/" + novel
    # Cloudscraper avoid lightnovelpub cloudflare protection
    # Equivalent to request
    scraper = cloudscraper.create_scraper(
        browser={
            "browser": "firefox",
            "platform": "windows",
            "desktop": True,
            "mobile": False,
        },
        delay=10,
    )
    source = scraper.get(url, proxies=proxies).text
    # find the url of the cover in website : in a <div class="fixed-img"> find the "data-src" of a <img>
    url_pic = (
        BeautifulSoup(source, "lxml")
        .find("div", class_="fixed-img")
        .find("img")["data-src"]
    )

    # Download the cover
    pic_data = scraper.get(url_pic, proxies=proxies)
    pic_data = pic_data.content

    # The picture and the format
    # The last 4 character of the url are the format : .jpg, .png ... Could use split() if some other format are use but never saw them in lightnovelpub
    return pic_data, url_pic[-4:]


def ScrapText(proxies: dict, info_chapter: str) -> str:
    """return the text of the chapter cleaned. MUST have a title announced by a '# '"""
    info_chapter = tuple(info_chapter.split("/split/"))
    url = info_chapter[2]
    scraper = cloudscraper.create_scraper(
        browser={
            "browser": "firefox",
            "platform": "windows",
            "desktop": True,
            "mobile": False,
        },
        delay=10,
    )
    source = scraper.get(url, proxies=proxies).text
    soup = BeautifulSoup(source, "lxml").find("div", id="chapter-container")

    for br in soup.find_all("br"):
        br.replace_with("\n" + br.text)
    for hr in soup.find_all("hr"):
        hr.replace_with("\n\n\n\n" + hr.text)
    for h3 in soup.find_all("</h3>"):
        h3.replace_with("\n\n")

    ch = ""
    title_missing = True
    # Check if there's the full title in chapterlist or just Chapter x
    if "Chapter" in info_chapter[1]:
        if len(info_chapter[1].strip()) > 12:
            ch = f"# {info_chapter[0].strip()}: {info_chapter[1].strip()} \n\n"
            title_missing = False
    else:
        if len(info_chapter[1].strip()) > 4:
            ch = f"# Chapter {info_chapter[0].strip()}: {info_chapter[1].strip()} \n\n"
            title_missing = False

    for paragraph in soup:
        if isinstance(paragraph, NavigableString):
            continue

        texte = paragraph.get_text(separator="\n")
        if "lightno" in texte:
            continue

        # If the title is not missing no need to write it again
        # If title is missing and is in the text put '# ' before it.
        if "Chapter " in texte:
            if title_missing:
                ch += texte.replace("Chapter ", "# Chapter ", 1)
                title_missing = False
            continue
        ch += texte + "\n\n"

    # if the title is still missing just add chapter x
    if title_missing:
        if "Chapter" in info_chapter[1]:
            ch = f"# {info_chapter[0].strip()}. {info_chapter[1].strip()} \n\n" + ch
        else:
            ch = (
                f"# Chapter {info_chapter[0].strip()}. {info_chapter[1].strip()} \n\n"
                + ch
            )

    return ch


def ScrapSummary(novel: str, proxies: dict) -> str:
    """return the summary"""

    url = "https://www.lightnovelpub.com/novel/" + novel
    scraper = cloudscraper.create_scraper(
        browser={
            "browser": "firefox",
            "platform": "windows",
            "desktop": True,
            "mobile": False,
        },
        delay=10,
    )

    source = scraper.get(url, proxies=proxies).text
    soup = BeautifulSoup(source, "lxml").find("div", class_="content")

    br = False
    for br in soup.find_all("br"):
        br.replace_with("\n" + br.text)
        br = True

    return (
        soup.text.replace("\n", "\n\n").strip().replace("%", "%%")
        if not br
        else soup.text.strip().replace("%", "%%")
    )


def ScrapChapterList(novel: str, proxies: dict) -> dict:
    """return a dict of :
    "ID  : chapter/split/title/split/url"
    ID is for sorting, only int, begin at 1
    chapter is the official number of the chapter (can be 0, 25, 43.5 ...)
    It's better if the title can contain the true title, but if not possible just put f"Chapter {chapter}"
    url will be use to download the chapter so must point directly to it"""

    # try to add section ; pass if aldready exist
    fixed_url = f"https://www.lightnovelpub.com/novel/{novel}/Chapters/page-"

    ch = {}
    page = 1

    while True:
        url = fixed_url + str(page)
        scraper = cloudscraper.create_scraper(
            browser={
                "browser": "firefox",
                "platform": "windows",
                "desktop": True,
                "mobile": False,
            },
            delay=10,
        )
        source = scraper.get(url, proxies=proxies).text
        # Every chapter of the page are in <ul class="chapter-list">
        list = BeautifulSoup(source, "lxml").find("ul", class_="chapter-list")

        i = 0

        # Element is one chapter
        for element in list:
            # Sometimes there is a NavigableString in the middle wich throw error
            if isinstance(element, NavigableString):
                continue

            a = element.text.split("\n\n")
            url = "https://www.lightnovelpub.com" + element.find("a")["href"]
            nmbchapter = element["data-orderno"]

            # % is a special characters in configparser %% is the string
            ch[nmbchapter] = (
                f"{a[1].replace('(lightnovelpub.com)', '')}/split/{a[2]}/split/{url}".replace(
                    "%", "%%"
                ),
            )

            i += 1

        # If the list of chapter go to 100 it mean that the page is full and there is probably another page after
        if i == 100:
            page += 1
        else:
            # If if finish at for exemple chapter 524 there is no page 6 (page 6 = chapter 600-700)
            break

    return ch


def Url(novel):
    return "https://www.lightnovelpub.com/novel/" + novel
