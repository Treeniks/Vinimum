from sublime import View

class Actionable:
    def select():
        pass

class Action:
    def __init__(self, view: View):
        self.view = view

    def run(self, selector):
        pass

class DeleteAction(Action):
    def run(self, selector: Actionable):
        print("delete", end=" ")
        selector.select()

actions = {
    "d": DeleteAction,
}
