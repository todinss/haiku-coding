from json import dump, load
from random import choice
from sys import stdout

from kivy.core.clipboard import Clipboard
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.properties import StringProperty
from kivy.uix.boxlayout import BoxLayout
from kivymd.app import MDApp
from kivymd.uix.button import MDFlatButton
from kivymd.uix.card import MDCardSwipe
from kivymd.uix.dialog import MDDialog
from kivymd.uix.snackbar import Snackbar


class Content(BoxLayout):
    def __init__(self, *args, **kwargs):
        super().__init__(**kwargs)
        self.container = self.ids.container
        self.height = 80

    def adding(self, dict):
        for i in reversed(dict["cronologia"]):
            haiku = list(dict["cronologia"][i].values())
            self.container.add_widget(
                SwipeToDeleteItem(
                    text=haiku[0],
                    secondary_text=haiku[1],
                    tertiary_text=haiku[2],
                    number=i)
                )

        if len(self.container.children) in [1, 2, 3]:
            self.height = 80 * len(self.container.children)
        elif len(self.container.children) >= 4:
            self.height = 80 * 4


class SwipeToDeleteItem(MDCardSwipe):
    text = StringProperty()
    secondary_text = StringProperty()
    tertiary_text = StringProperty()
    number = StringProperty()


class HaikuGenerator(MDApp):

    info_dialog = None
    contact_dialog = None
    history_dialog = None

    def build(self):
        self.title = "Basho: Un Haiku al giorno"
        with open('haiku.json', 'r', encoding="utf-8") as outfile:
            self.database = load(outfile)
        self.theme_cls.theme_style = "Light"
        self.title_color = "000000"
        self.text_color = "181818"
        self.theme_cls.primary_palette = "Amber"
        self.icon = 'icon.png'
        return Builder.load_file("Haiku.kv")

    def generate_haiku(self):
        self.root.ids["verso_1"].text = choice(self.database['verso_1'])
        self.root.ids["verso_2"].text = choice(self.database['verso_2'])
        self.root.ids["verso_3"].text = choice(self.database['verso_3'])
        self.add_to_history()

    def copy_haiku(self):
        haiku = [
            self.root.ids["verso_1"].text,
            self.root.ids["verso_2"].text,
            self.root.ids["verso_3"].text
            ]

        if haiku != ["", "", ""] and "\n".join(haiku) != Clipboard.paste():
            Clipboard.copy("\n".join(haiku))
            Snackbar(text="Elemento copiato negli appunti!").show()

    def show_info_dialog(self):
        app_info = "L'applicazione è stata sviluppata da un gruppo di studenti dell'istituto \"Gian Battista Vico\", all'indirizzo Coding, in un progetto scolastico monitorato in compresenza dalla professoressa di Italiano Luciana Soravia e il professore di coding Diomede Mazzone."
        if not self.info_dialog:
            self.info_dialog = MDDialog(
                title=f"[color={self.title_color}]Informazioni App[/color]",
                text=f"[color={self.text_color}]{app_info}[/color]",
                buttons=[
                    MDFlatButton(
                        text="ESCI",
                        text_color=self.theme_cls.primary_color,
                        on_release=self.close_info_dialog
                        )],
                auto_dismiss=True,
                size_hint=(0.8, 1)
            )
        self.info_dialog.open()

    def show_contact_dialog(self):
        app_info = "Barile Luigi:\n    barile.luigi.s03@liceoviconapoli.it\n\nPatruno Luca:\n    patruno.luca.s26@liceoviconapoli.it\n\nRipoli Luca:\n    ripoli.luca.s13@liceoviconapoli.it\n\nSenese Walter:\n    senese.walter.s30@liceoviconapoli.it\n"
        if not self.contact_dialog:
            self.contact_dialog = MDDialog(
                title=f"[color={self.title_color}]I Nostri Contatti[/color]",
                text=f"[color={self.text_color}]{app_info}[/color]",
                buttons=[
                    MDFlatButton(
                        text="ESCI",
                        text_color=self.theme_cls.primary_color,
                        on_release=self.close_contact_dialog
                        )],
                auto_dismiss=True,
                size_hint=(0.8, 1)
            )
        self.contact_dialog.open()

    def show_history_dialog(self):
        if not self.history_dialog:
            if len(list(self.database["cronologia"].keys())) != 0:
                self.history_container = Content()
                self.history_container.adding(self.database)
                self.history_dialog = MDDialog(
                    type="custom",
                    title=f"[color={self.title_color}]Cronologia[/color]",
                    content_cls=self.history_container,
                    buttons=[
                        MDFlatButton(
                            text="ESCI",
                            text_color=self.theme_cls.primary_color,
                            on_release=self.close_history_dialog
                            ),
                        MDFlatButton(
                            text="CANCELLA CRONOLOGIA",
                            text_color=self.theme_cls.primary_color,
                            on_release=self.delete_history
                            )],
                    auto_dismiss=True,
                    size_hint=(0.8, 1)
                )
            else:
                self.history_dialog = MDDialog(
                    type="custom",
                    title=f"[color={self.title_color}]Cronologia[/color]",
                    text=f"[color={self.text_color}]La cronologia è vuota[/color]",
                    buttons=[
                        MDFlatButton(
                            text="ESCI",
                            text_color=self.theme_cls.primary_color,
                            on_release=self.close_history_dialog
                            )
                        ],
                    auto_dismiss=True,
                    size_hint=(0.8, 1)
                    )
        self.history_dialog.open()

    def close_info_dialog(self, obj):
        self.info_dialog.dismiss()

    def close_contact_dialog(self, obj):
        self.contact_dialog.dismiss()

    def close_history_dialog(self, obj):
        self.history_dialog.dismiss()
        self.history_dialog = None
        self.reload_history()

        self.info_dialog = None
        self.contact_dialog = None
        self.history_dialog = None

    def add_to_history(self):
        self.database["cronologia"][
            "elem_%s" % (len(self.database["cronologia"].keys()) + 1)
            ] = {
                "verso_1": self.root.ids["verso_1"].text,
                "verso_2": self.root.ids["verso_2"].text,
                "verso_3": self.root.ids["verso_3"].text
                }
        self.dumper()
        self.history_dialog = None
        self.reload_history()

    def reload_history(self):
        new_history = {}
        for i in enumerate(self.database["cronologia"].values(), start=1):
            new_history["elem_%s" % i[0]] = i[1]
        self.database["cronologia"] = new_history
        self.dumper()

    def delete_history(self, obj):
        self.database["cronologia"] = {}
        self.dumper()
        self.close_history_dialog("")
        self.history_dialog = None
        self.reload_history()
        Snackbar(text="La cronologia è stata eliminata!").show()

    def copy_item(self, obj):
        haiku = [obj.text, obj.secondary_text, obj.tertiary_text]
        if haiku != ["", "", ""] and "\n".join(haiku) != Clipboard.paste():
            Clipboard.copy("\n".join(haiku))
            Snackbar(text="Elemento copiato negli appunti!").show()

    def delete_item(self, obj):
        del self.database['cronologia'][obj.number]
        self.dumper()
        self.history_container.container.remove_widget(obj)
        Snackbar(text="Elemento eliminato dalla cronologia!").show()
        if len(self.history_container.container.children) < 4:
            self.close_history_dialog("obj")
            self.show_history_dialog()

    def dumper(self):
        with open('haiku.json', 'w', encoding="utf-8") as outfile:
            dump(
                self.database,
                outfile,
                indent=4,
                sort_keys=True,
                ensure_ascii=False
                )


if __name__ == '__main__':
    stdout.reconfigure(encoding='utf-8')
    __version__ = "1.0"
    Window.size = (500, 500)
    Application = HaikuGenerator()
    Application.run()
