from sublime import View
import Vinimum.vinimum as vinimum

class Command:
    def __init__(self, view: View):
        self.view = view

    def run(self):
        pass

class InsertCommand(Command):
    def run(self):
        vinimum.enter_sublime_mode()

class InsertBOLCommand(Command):
    def run(self):
        vinimum.enter_sublime_mode()
        self.view.run_command("move_to", {"to": "bol"})

class AppendCommand(Command):
    def run(self):
        vinimum.enter_sublime_mode()
        self.view.run_command("move", {"by": "characters", "forward": True})

class AppendEOLCommand(Command):
    def run(self):
        vinimum.enter_sublime_mode()
        self.view.run_command("move_to", {"to": "eol"})

class NewLineAfterCommand(Command):
    def run(self):
        vinimum.enter_sublime_mode()
        self.view.run_command("run_macro_file", {"file": "res://Packages/Default/Add Line.sublime-macro"})

class NewLineBeforeCommand(Command):
    def run(self):
        vinimum.enter_sublime_mode()
        self.view.run_command("run_macro_file", {"file": "res://Packages/Default/Add Line Before.sublime-macro"})

commands = {
    "i": InsertCommand,
    "I": InsertBOLCommand,
    "a": AppendCommand,
    "A": AppendEOLCommand,
    "o": NewLineAfterCommand,
    "O": NewLineBeforeCommand,
}
