import sublime
import Vinimum.vinimum as vinimum

class Command:
    def __init__(self, view):
        self.view = view

    def run(self):
        pass

    def repeatable(self):
        return True

# i
class InsertCommand(Command):
    def run(self):
        vinimum.enter_sublime_mode()

    # technically repeatable
    # but only once proper repeat engine is in place
    # better not make it repeatable until then
    def repeatable(self):
        return False

# I
class InsertBOLCommand(Command):
    def run(self):
        vinimum.enter_sublime_mode()
        self.view.run_command("move_to", {"to": "bol"})

    # technically repeatable
    # but only once proper repeat engine is in place
    # better not make it repeatable until then
    def repeatable(self):
        return False

# a
class AppendCommand(Command):
    def run(self):
        vinimum.enter_sublime_mode()
        self.view.run_command("move", {"by": "characters", "forward": True})

    # technically repeatable
    # but only once proper repeat engine is in place
    # better not make it repeatable until then
    def repeatable(self):
        return False

# A
class AppendEOLCommand(Command):
    def run(self):
        vinimum.enter_sublime_mode()
        self.view.run_command("move_to", {"to": "eol"})

    # technically repeatable
    # but only once proper repeat engine is in place
    # better not make it repeatable until then
    def repeatable(self):
        return False

# o
class NewLineAfterCommand(Command):
    def run(self):
        vinimum.enter_sublime_mode()
        self.view.run_command("run_macro_file", {"file": "res://Packages/Default/Add Line.sublime-macro"})

    # technically repeatable
    # but only once proper repeat engine is in place
    # better not make it repeatable until then
    def repeatable(self):
        return False

# O
class NewLineBeforeCommand(Command):
    def run(self):
        vinimum.enter_sublime_mode()
        self.view.run_command("run_macro_file", {"file": "res://Packages/Default/Add Line Before.sublime-macro"})

    # technically repeatable
    # but only once proper repeat engine is in place
    # better not make it repeatable until then
    def repeatable(self):
        return False

# x
class RemoveCharacterCommand(Command):
    def run(self):
        self.view.run_command("right_delete")

# D
class DeleteToEOLCommand(Command):
    def run(self):
        self.view.run_command("run_macro_file", {"file": "res://Packages/Default/Delete to Hard EOL.sublime-macro"})

# C
class ChangeToEOLCommand(Command):
    def run(self):
        vinimum.enter_sublime_mode()
        self.view.run_command("run_macro_file", {"file": "res://Packages/Default/Delete to Hard EOL.sublime-macro"})

commands = {
    "i": InsertCommand,
    "I": InsertBOLCommand,
    "a": AppendCommand,
    "A": AppendEOLCommand,
    "o": NewLineAfterCommand,
    "O": NewLineBeforeCommand,
    "x": RemoveCharacterCommand,
    "D": DeleteToEOLCommand,
    "C": ChangeToEOLCommand,
}
