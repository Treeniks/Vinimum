from sublime import View, Region
from Vinimum.actions import Actionable

from enum import Enum

class Modifier(Enum):
    INNER = 0
    OUTER = 1

class TextObject(Actionable):
    def __init__(self, view: View, modifier: Modifier):
        self.view = view
        self.modifier = modifier

    def select(self):
        if self.modifier == Modifier.INNER:
            return self._select_inner()
        elif self.modifier == Modifier.OUTER:
            return self._select_outer()

    def _select_inner(self):
        pass

    def _select_outer(self):
        pass

def expand_to_whitespace(view, r):
    a = r.a
    b = r.b
    while view.substr(b) in " \t":
        b += 1

    if b == r.b:
        while view.substr(a - 1) in " \t":
            a -= 1

    return Region(a, b)

class WordObject(TextObject):
    def _select_inner(self):
        self.view.run_command("expand_selection", {"to": "word"})

    def _select_outer(self):
        self.view.run_command("expand_selection", {"to": "word"})
        sel = self.view.sel()
        for r in sel:
            sel.add(expand_to_whitespace(self.view, r))


modifiers = {
    "i": Modifier.INNER,
    "a": Modifier.OUTER,
}

text_objects = {
    "w": WordObject,
}
