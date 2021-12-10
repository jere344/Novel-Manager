import requirement

if __name__ == "__main__":
    import os

    if not os.path.isdir("DATA"):
        from shutil import copytree
        from pathlib import Path

        __location__ = Path(__file__).parent.resolve()

        copytree(
            __location__.joinpath("template", "DATA"), __location__.joinpath("DATA")
        )

    if not os.path.isdir("epub"):
        os.mkdir("epub")

    if not os.path.isfile("epubstyle.css"):
        from shutil import copyfile
        from pathlib import Path

        __location__ = Path(__file__).parent.resolve()
        copyfile(
            __location__.joinpath("template", "epubstyle.css"),
            __location__.joinpath("epubstyle.css"),
        )

    if not os.path.isfile("gui.kv"):
        from shutil import copyfile
        from pathlib import Path

        __location__ = Path(__file__).parent.resolve()
        copyfile(
            __location__.joinpath("template", "gui.kv"),
            __location__.joinpath("gui.kv"),
        )

    if not os.path.isdir("pdf"):
        os.mkdir("pdf")

    if not os.path.isdir("config"):
        from shutil import copytree
        from pathlib import Path

        __location__ = Path(__file__).parent.resolve()

        copytree(
            __location__.joinpath("template", "config"), __location__.joinpath("config")
        )

    import lib

    if not lib.config.sections():
        pass
        # import firstuse

    import gui

    gui.Start()

# when building exe with pyinstaller :
# python -m PyInstaller --noconsole --name package C:\Users\jerem\Desktop\kivy\start.py --add-data 'C:\Users\jerem\Desktop\kivy\template;.'

# when building with buildozer :
# buildozer debug deploy run
