import kivy, os
from kivy.config import Config
from kivy.uix.floatlayout import FloatLayout

Config.set('graphics', 'resizable', False)
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.core.window import Window
from kivy.uix.checkbox import CheckBox
from kivy.properties import ObjectProperty
from kivy.uix.popup import Popup

kivy.require("1.10.1")


class DefineButtons(Widget):
    humanA = ObjectProperty(None)
    rl = ObjectProperty(None)
    treeA = ObjectProperty(None)
    greedyA = ObjectProperty(None)
    humanG = ObjectProperty(None)
    treeG = ObjectProperty(None)
    greedyG = ObjectProperty(None)
    # dfs = ObjectProperty(None)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.selectedAlgorithm = ""
        self.playerAlgorithm = ""

    def getValues(self):
        if self.humanA.active:
            self.selectedAlgorithm = "A*"
            self.playerAlgorithm = "human"
        elif self.rl.active:
            self.selectedAlgorithm = "A*"
            self.playerAlgorithm = "rl"
        elif self.treeA.active:
            self.selectedAlgorithm = "A*"
            self.playerAlgorithm = "tree"
        elif self.greedyA.active:
            self.selectedAlgorithm = "A*"
            self.playerAlgorithm = "greedy"
        elif self.humanG.active:
            self.selectedAlgorithm = "GeneticAlgorithm"
            self.playerAlgorithm = "human"
        elif self.treeG.active:
            self.selectedAlgorithm = "GeneticAlgorithm"
            self.playerAlgorithm = "tree"
        elif self.greedyG.active:
            self.selectedAlgorithm = "GeneticAlgorithm"
            self.playerAlgorithm = "greedy"
        # elif self.dfs.active:
        #     self.selectedAlgorithm = "DFS"
        #     self.playerAlgorithm = "human"

        self.startPacman()

    def startPacman(self):
        os.system("python3 main.py " + self.selectedAlgorithm + " " + self.playerAlgorithm)

    def helpBtnPressed(self):
        showHelpWindow()

class Help(FloatLayout):
    pass

def showHelpWindow():
    show = Help()
    helpWindow = Popup(title="Help", content=show, size_hint=(None, None), size=(400, 400))
    helpWindow.open()


class PacmanApp(App):

    def build(self):
        Window.size = (600, 580)
        return DefineButtons()


if __name__ == "__main__":
    PacmanApp().run()