import sublime
import Vinimum.vinimum as vinimum

class Command:
    def __init__(self, view):
        self.view = view

    def run(self):
        pass

# i
class InsertCommand(Command):
    def run(self):
        vinimum.enter_sublime_mode()

# I
class InsertBOLCommand(Command):
    def run(self):
        vinimum.enter_sublime_mode()
        self.view.run_command("move_to", {"to": "bol"})

# a
class AppendCommand(Command):
    def run(self):
        vinimum.enter_sublime_mode()
        self.view.run_command("move", {"by": "characters", "forward": True})

# A
class AppendEOLCommand(Command):
    def run(self):
        vinimum.enter_sublime_mode()
        self.view.run_command("move_to", {"to": "eol"})

# o
class NewLineAfterCommand(Command):
    def run(self):
        vinimum.enter_sublime_mode()
        self.view.run_command("run_macro_file", {"file": "res://Packages/Default/Add Line.sublime-macro"})

# O
class NewLineBeforeCommand(Command):
    def run(self):
        vinimum.enter_sublime_mode()
        self.view.run_command("run_macro_file", {"file": "res://Packages/Default/Add Line Before.sublime-macro"})

# x
class RemoveCharacterCommand(Command):
    def run(self):
        self.view.run_command("right_delete")

commands = {
    "i": InsertCommand,
    "I": InsertBOLCommand,
    "a": AppendCommand,
    "A": AppendEOLCommand,
    "o": NewLineAfterCommand,
    "O": NewLineBeforeCommand,
    "x": RemoveCharacterCommand,
}
