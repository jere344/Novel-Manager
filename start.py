if __name__ == "__main__":
    import os

    if not os.path.isdir("DATA"):
        os.mkdir("DATA")

    if not os.path.isdir("epub"):
        os.mkdir("epub")

    if not os.path.isdir("pdf"):
        os.mkdir("pdf")

    if not os.path.isdir("config"):
        from shutil import copytree
        from pathlib import Path

        __location__ = Path(__file__).parent.resolve()

        copytree(__location__.joinpath("template"), __location__.joinpath("config"))

    import lib

    if not lib.config.sections():
        import firstuse

    import gui

    gui.Start()
