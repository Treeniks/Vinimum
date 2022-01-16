from sublime import Region

import Vinimum.motions as motions

from enum import Enum

class Modifier(Enum):
    INNER = 0
    OUTER = 1

class TextObject():
    def __init__(self, view, modifier):
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

# w
class WordObject(TextObject):
    def _select_inner(self):
        self.view.run_command("expand_selection", {"to": "word"})

    def _select_outer(self):
        self.view.run_command("expand_selection", {"to": "word"})
        sel = self.view.sel()
        for r in sel:
            sel.add(expand_to_whitespace(self.view, r))

class BracketsObject(TextObject):
    def __init__(self, view, modifier, character):
        super().__init__(view, modifier)
        self.character = character

    def _select_inner(self):
        self.view.run_command("expand_selection", {"to": "brackets", "brackets": self.character})

    def _select_outer(self):
        self.view.run_command("expand_selection", {"to": "brackets", "brackets": self.character})
        self.view.run_command("expand_selection", {"to": "brackets", "brackets": self.character})

# (
class RoundBracketsObject(BracketsObject):
    def __init__(self, view, modifier):
        super().__init__(view, modifier, "(")

# [
class SquareBracketsObject(BracketsObject):
    def __init__(self, view, modifier):
        super().__init__(view, modifier, "[")

# {
class CurlyBracketsObject(BracketsObject):
    def __init__(self, view, modifier):
        super().__init__(view, modifier, "{")

class QuotesObject(TextObject):
    def __init__(self, view, modifier, character):
        super().__init__(view, modifier)
        self.character = character

    def _select_inner(self):
        motion_backwards = motions.ToInLineBackwardsMotion(self.view, self.character)
        motion_forwards = motions.ToInLineMotion(self.view, self.character)

        motion_backwards.move()
        motion_forwards.select()

    def _select_outer(self):
        motion_backwards = motions.FindInLineBackwardsMotion(self.view, self.character)
        motion_forwards = motions.FindInLineMotion(self.view, self.character)

        motion_backwards.move()
        motion_forwards.select()

# '
class SingleQuotesObject(QuotesObject):
    def __init__(self, view, modifier):
        super().__init__(view, modifier, "'")

# "
class DoubleQuotesObject(QuotesObject):
    def __init__(self, view, modifier):
        super().__init__(view, modifier, '"')

modifiers = {
    "i": Modifier.INNER,
    "a": Modifier.OUTER,
}

text_objects = {
    "w": WordObject,
    "(": RoundBracketsObject,
    "[": SquareBracketsObject,
    "{": CurlyBracketsObject,
    "'": SingleQuotesObject,
    '"': DoubleQuotesObject,
}
