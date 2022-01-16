from sublime import View
import Vinimum.vinimum as vinimum

class Actionable:
    def select():
        pass

class Action:
    def __init__(self, view: View):
        self.view = view

    def run(self, selector: Actionable):
        pass

class DeleteAction(Action):
    def run(self, selector: Actionable):
        print("delete", end=" ")
        selector.select()
        if self.view.has_non_empty_selection_region():
            self.view.run_command("left_delete")

class ChangeAction(Action):
    def run(self, selector: Actionable):
        print("change", end=" ")
        selector.select()
        if self.view.has_non_empty_selection_region():
            self.view.run_command("left_delete")
        vinimum.enter_sublime_mode()

actions = {
    "d": DeleteAction,
    "c": ChangeAction,
}
