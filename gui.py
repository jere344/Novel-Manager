from kivy.app import App
from kivy.uix.widget import Widget
from kivy.lang.builder import Builder
from kivy.core.window import Window
from kivy.properties import ObjectProperty
from kivy.uix.anchorlayout import AnchorLayout
from task import StartThread
import lib
import webbrowser


class Cover(AnchorLayout):
    button = ObjectProperty(None)


class ScraperWidget(Widget):
    Builder.load_file(str(lib.__location__.joinpath("gui.kv")))
    main = ObjectProperty(None)

    # top pannel
    grid_novel = ObjectProperty(None)

    # Middle pannel
    summary = ObjectProperty(None)
    scroll_summary = ObjectProperty(None)
    icon = ObjectProperty(None)
    label_downloaded = ObjectProperty(None)
    label_read = ObjectProperty(None)
    label_title = ObjectProperty(None)
    # Button
    button_PDF = ObjectProperty(None)
    button_epub = ObjectProperty(None)
    button_web = ObjectProperty(None)
    button_refresh = ObjectProperty(None)
    button_delete = ObjectProperty(None)
    button_download_10 = ObjectProperty(None)
    button_download_100 = ObjectProperty(None)
    button_download_all = ObjectProperty(None)
    button_add = ObjectProperty(None)
    input_url = ObjectProperty(None)
    input_source = ObjectProperty(None)

    # Bottom pannel
    label_last = ObjectProperty(None)

    def OnStart(self):
        Window.size = 540, 960
        # Window.bind(on_resize=self.Resize)
        self.flask_running = False
        self.Cover()
        self.UpdateMiddlePannel(lib.config.sections()[1])
        self.Bind()

    def Bind(self):
        """Bind buttons with their respectives actions"""
        self.button_download_10.bind(
            on_press=lambda _: StartThread("download_10", self.novel_selected)
        )
        self.button_download_100.bind(
            on_press=lambda _: StartThread("download_100", self.novel_selected)
        )
        self.button_download_all.bind(
            on_press=lambda _: StartThread("download_all", self.novel_selected)
        )
        self.button_epub.bind(
            on_press=lambda _: StartThread("epub", self.novel_selected)
        )
        self.button_PDF.bind(on_press=lambda _: StartThread("PDF", self.novel_selected))
        self.button_web.bind(on_press=lambda _: StartThread("web", self.novel_selected))
        self.button_refresh.bind(on_press=lambda _: StartThread("refresh"))
        self.button_delete.bind(
            on_press=lambda _: StartThread("delete", self.novel_selected)
        )
        self.button_add.bind(
            on_press=lambda _: StartThread(
                "add", self.input_url.text, self.input_source.text
            )
        )

        self.icon.bind(
            on_press=lambda _: webbrowser.open(
                lib.config.get(self.novel_selected, "url")
            )
        )

    def Cover(self):
        """Place the novels cover in the scrolling grid"""
        self.cover_list = []

        for name in lib.config.sections()[1:]:
            cover = Cover()
            cover.button.bind(
                on_press=lambda _, novel=name: self.UpdateMiddlePannel(novel)
            )
            cover.button.background_normal = str(
                lib.__location__.joinpath(lib.config.get(name, "picture"))
            )
            self.cover_list.append(cover)
            self.grid_novel.add_widget(cover)

    def UpdateCover(self):
        [self.grid_novel.remove_widget(cover) for cover in self.cover_list]
        from math import ceil

        self.Cover()
        self.grid_novel.height = int(
            10
            + 340
            * ceil(
                int(len(lib.config.sections()[1:]))
                / (self.grid_novel.cols if self.grid_novel.cols else 2)
            )
        )

    def UpdateMiddlePannel(self, novel: str) -> None:
        """Update middle pannel for the selected novel"""
        self.novel_selected = novel
        self.icon.background_normal = str(
            lib.__location__.joinpath(lib.config.get(novel, "picture"))
        )
        self.summary.text = lib.config.get(novel, "summary").strip()
        self.label_downloaded.text = f'Downloaded :\n{lib.config.get(novel, "downloadedchapter")} / {lib.config.get(novel, "maxchapter")}'
        self.label_read.text = f'Read :\n{lib.config.get(novel, "chapterread")} / {lib.config.get(novel, "maxchapter")}'
        self.label_title.text = lib.config.get(self.novel_selected, "cleanname")

    def SetLast(self, value):
        self.label_last.text = value


class ScraperGui(App):
    config_file = ObjectProperty(lib.config)

    def build(self):
        self.ok = ScraperWidget()
        return self.ok

    def on_start(self):
        lib.app = self.ok
        self.ok.OnStart()
        # self.ok.grid_novel.add_widget(Cover())


if __name__ == "__main__":
    import os

    if not os.path.isdir("DATA"):
        os.mkdir("DATA")

    if not os.path.isdir("epub"):
        os.mkdir("epub")

    if not os.path.isdir("pdf"):
        os.mkdir("pdf")

    if not os.path.isdir("config"):
        import shutil

        src = "templace"
        dst = "config"
        shutil.copy(src, dst)

    ScraperGui().run()
