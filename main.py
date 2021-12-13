import os
import lib


def AndroidFiles():
    # TODO DATA
    # TODO book
    # TODO config

    if not os.path.isfile(lib.__location__.joinpath("epubstyle.css")):
        from shutil import copyfile

        copyfile(
            lib.__location__.joinpath("template", "epubstyle.css"),
            lib.__location__.joinpath("epubstyle.css"),
        )

    if not os.path.isfile(lib.__location__.joinpath("gui.kv")):
        from shutil import copyfile

        copyfile(
            lib.__location__.joinpath("template", "gui.kv"),
            lib.__location__.joinpath("gui.kv"),
        )

    if not os.path.isdir(lib.__location__.joinpath("config")):
        from shutil import copytree

        copytree(
            lib.__location__.joinpath("template", "config"),
            lib.__location__.joinpath("config"),
        )

    if not lib.config.sections():
        import firstuse

        firstuse.GenerateHTML()
        firstuse.AndroidOpenHTML()


def DesktopFiles():

    if not os.path.isdir(lib.__location__.joinpath("DATA")):
        from shutil import copytree

        copytree(
            lib.__location__.joinpath("template", "DATA"),
            lib.__location__.joinpath("DATA"),
        )

    if not os.path.isdir(lib.__location__.joinpath("book")):
        os.mkdir(lib.__location__.joinpath("book"))

    if not os.path.isfile(lib.__location__.joinpath("epubstyle.css")):
        from shutil import copyfile

        copyfile(
            lib.__location__.joinpath("template", "epubstyle.css"),
            lib.__location__.joinpath("epubstyle.css"),
        )

    if not os.path.isfile(lib.__location__.joinpath("gui.kv")):
        from shutil import copyfile

        copyfile(
            lib.__location__.joinpath("template", "gui.kv"),
            lib.__location__.joinpath("gui.kv"),
        )

    if not os.path.isdir(lib.__location__.joinpath("config")):
        from shutil import copytree

        copytree(
            lib.__location__.joinpath("template", "config"),
            lib.__location__.joinpath("config"),
        )

    if not lib.config.sections():
        import firstuse

        firstuse.GenerateHTML()
        firstuse.DesktopOpenHTML()


if __name__ == "__main__":

    if lib.user_os in ["win", "linux"]:
        DesktopFiles()

    elif lib.user_os == "android":
        AndroidFiles()

    else:
        raise Exception("Platform not supported")

    import gui

    gui.Start()

# when building exe with pyinstaller :
# python -m PyInstaller --noconsole --name package C:\Users\jerem\Desktop\kivy\start.py --add-data 'C:\Users\jerem\Desktop\kivy\template;.'

# when building with buildozer :
# buildozer debug deploy run
