import Vinimum.vinimum as vinimum

class Action:
    def __init__(self, view):
        self.view = view

    def run(self, select):
        pass

    def double(self):
        pass

# d
class DeleteAction(Action):
    def run(self, select):
        select()
        if self.view.has_non_empty_selection_region():
            self.view.run_command("left_delete")

    def double(self):
        self.run(lambda: self.view.run_command("expand_selection", {"to": "line"}))

# c
class ChangeAction(Action):
    def run(self, select):
        select()
        if self.view.has_non_empty_selection_region():
            self.view.run_command("left_delete")
        vinimum.enter_sublime_mode()

    def __select(self):
        sel = self.view.sel()
        new_sel = [self.view.line(r) for r in sel]
        sel.clear()
        sel.add_all(new_sel)

    def double(self):
        self.run(self.__select)
        self.view.run_command("reindent")

# v
# while Vinimum doesn't have a full Visual Mode
# this v action can be used to select a motion or text object
class VisualAction(Action):
    def run(self, select):
        select()

    def double(self):
        self.view.run_command("expand_selection", {"to": "line"})

actions = {
    "d": DeleteAction,
    "c": ChangeAction,
    "v": VisualAction,
}
