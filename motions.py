from sublime import View
from Vinimum.actions import Actionable

class Motion(Actionable):
    def __init__(self, view: View):
        self.view = view

    def move(self):
        pass

    def select(self):
        pass

class WordMotion(Motion):
    def move(self):
        self.view.run_command("move", {"by": "words", "forward": True})

    def select(self):
        print("word")
        # self.view.run_command("move", {"by": "words", "forward": True, "extend": True})

motions = {
    "w": WordMotion,
}
