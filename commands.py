from sublime import View
import Vinimum.vinimum as vinimum

class Command:
    def __init__(self, view: View):
        self.view = view

    def run(self):
        pass

class InsertCommand(Action):
    def run(self):
        vinimum.enter_sublime_mode()

commands = {
    "i": InsertCommand,
}
