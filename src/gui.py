import kivy, os
from kivy.config import Config
Config.set('graphics', 'resizable', False)
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.core.window import Window
from kivy.uix.checkbox import CheckBox
from kivy.properties import ObjectProperty

kivy.require("1.10.1")


class DefineButtons(Widget):

    gen = ObjectProperty(None)
    aStar = ObjectProperty(None)
    aStarBot = ObjectProperty(None)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.selectedAlgorithm = ""

    def getValues(self):
        if self.gen.active:
            self.selectedAlgorithm = "GeneticAlgorithm"
        elif self.aStar.active:
            self.selectedAlgorithm = "A*"
        elif self.aStarBot.active:              # TODO
            self.selectedAlgorithm = "A*_bot"

        self.startPacman()

    def startPacman(self):
        os.system("python3 main.py " + self.selectedAlgorithm)


class PacmanApp(App):

    def build(self):
        Window.size = (600, 580)
        return DefineButtons()


if __name__ == "__main__":
    PacmanApp().run()