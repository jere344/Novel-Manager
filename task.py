import lib
import webbrowser
from threading import Thread
import misc


def StartThread(task: str, novel=None, source=None) -> None:
    """Call for the good function in a different thread"""
    list_task = {
        "download_10": lambda: Download10(novel),
        "download_100": lambda: Download100(novel),
        "download_all": lambda: Downloadall(novel),
        "epub": lambda: GenerateEpub(novel),
        "PDF": lambda: GeneratePDF(novel),
        "web": lambda: WebReader(novel),
        "refresh": lambda: Refresh(),
        "delete": lambda: Delete(novel),
        "add": lambda: AddNovel(novel, source),
    }

    t = Thread(target=list_task[task])
    t.daemon = True
    t.start()


def Download10(novel):
    """Call for download 10 times"""
    lib.app.SetLast("downloaded started")
    if int(lib.config.get(novel, "downloadedchapter")) == int(
        lib.config.get(novel, "maxchapter")
    ):
        lib.app.SetLast("No chapter left")
        return None

    for i in range(
        int(lib.config.get(novel, "downloadedchapter")) + 1,
        min(
            [
                int(lib.config.get(novel, "downloadedchapter")) + 11,
                int(lib.config.get(novel, "maxchapter")),
            ]
        ),
    ):

        misc.SetChapter(novel, str(i))
        lib.app.SetLast(f"chapter {i} downloaded")

    lib.app.SetLast("chapters downloaded")
    misc.SetDownloaded(novel)
    misc.Save(config=True)
    Refresh(text=False)


def Download100(novel):
    """Call for download 10 times"""
    lib.app.SetLast("downloaded started")
    if int(lib.config.get(novel, "downloadedchapter")) == int(
        lib.config.get(novel, "maxchapter")
    ):
        lib.app.SetLast("No chapter left")
        return None

    for i in range(
        int(lib.config.get(novel, "downloadedchapter")) + 1,
        min(
            [
                int(lib.config.get(novel, "downloadedchapter")) + 101,
                int(lib.config.get(novel, "maxchapter")),
            ]
        ),
    ):

        misc.SetChapter(novel, str(i))
        lib.app.SetLast(f"chapter {i} downloaded")

    lib.app.SetLast("chapters downloaded")
    misc.SetDownloaded(novel)
    misc.Save(config=True)
    Refresh(text=False)


def Downloadall(novel):
    """Call for download for every chapter left"""
    lib.app.SetLast("downloaded started")
    if int(lib.config.get(novel, "downloadedchapter")) == int(
        lib.config.get(novel, "maxchapter")
    ):
        lib.app.SetLast("No chapter left")
        return None

    lib.app.SetLast("downloaded started")
    for i in range(
        int(lib.config.get(novel, "downloadedchapter")) + 1,
        int(lib.config.get(novel, "maxchapter")),
    ):
        misc.SetChapter(novel, str(i))
        lib.app.SetLast(f"chapter {i} downloaded")

    lib.app.SetLast("chapters downloaded")
    misc.SetDownloaded(novel)
    misc.Save(config=True)
    Refresh(text=False)


def GenerateEpub(novel):
    """Call for epub generation"""
    lib.app.SetLast("epub generation started")
    import epubgenerator

    epubgenerator.Generate(novel)
    lib.app.SetLast("epub generated")


def GeneratePDF(novel):
    """Call for pdf generation"""
    lib.app.SetLast("pdf generation started")
    import pdfgenerator

    pdfgenerator.Generate(novel)
    lib.app.SetLast("pdf generated")


def WebReader(novel):
    """launch flask and open the selected novel in browser"""
    import flaskapp

    webbrowser.open(
        f"http://localhost:5000/{novel}/{lib.config.get(novel, 'chapterread')}"
    )
    lib.app.SetLast("web Reader launched")
    if not lib.app.flask_running:
        lib.app.flask_running = True
        flaskapp.app.run()


def Refresh(text=True):
    """Refresh UI and number of downloaded"""
    if text:
        lib.app.SetLast("refreshing")
    for novel in lib.config.sections():
        misc.SetDownloaded(novel)

    # misc.SetTotalDownloaded()
    # misc.SetTotalRead()
    misc.Save(config=True)
    lib.app.UpdateMiddlePannel(lib.app.novel_selected)
    if text:
        lib.app.SetLast("refreshed")


def Delete(novel):
    """Delete the selected novel"""
    lib.app.SetLast(f"deleting")
    misc.DeleteNovel(novel)
    misc.Save(config=True, chapterlist=True)
    lib.app.UpdateCover()
    lib.app.UpdateMiddlePannel(lib.config.sections()[0])
    lib.app.SetLast(f"deleted")


def AddNovel(novel, source):
    """Add the novel in the textinput from the source in spinner"""
    lib.app.SetLast(f"Adding novel")
    import os.path

    # try:

    if not os.path.isdir(lib.__location__.joinpath("DATA/", novel)):
        os.mkdir(lib.__location__.joinpath("DATA/", novel))

    # If exist do nothing else ignore error and add section
    try:
        lib.config[novel]
    except KeyError:
        lib.config.add_section(novel)

    lib.config.set(novel, "DownloadedChapter", "0")
    lib.config.set(novel, "ChapterRead", "0")
    lib.config.set(novel, "Source", source)

    misc.SetUrl(novel)
    misc.SetChapterList(novel)
    lib.app.SetLast(f"Chapter scraped")
    misc.SetCover(novel)
    lib.app.SetLast(f"Cover scraped")
    misc.SetMaxChapter(novel)
    misc.SetCleanName(novel)
    misc.SetSummary(novel)
    lib.app.SetLast(f"summary scraped")

    misc.Save(config=True, chapterlist=True)

    lib.app.UpdateCover()
    lib.app.SetLast(f"novel added")

    # except:
    #     lib.app.SetLast("Error while downloading, deleting novel")
    #     try:
    #         misc.DeleteNovel(novel)
    #     except:
    #         lib.app.SetLast("deletion done")
    #     lib.app.SetLast("deletion failed")
