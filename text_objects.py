from sublime import View
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

class Word(TextObject):
    def _select_inner(self):
        print("inner word")

    def _select_outer(self):
        print("outer word")

modifiers = {
    "i": Modifier.INNER,
    "a": Modifier.OUTER,
}

text_objects = {
    "w": Word,
}
