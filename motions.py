from sublime import Region

class Motion():
    def __init__(self, view):
        self.view = view

    def move(self):
        pass

    def select(self, repeat=1):
        for i in range(repeat):
            self._select()

    def _select(self):
        pass

# w
class WordMotion(Motion):
    def move(self):
        self.view.run_command("move", {"by": "stops", "word_begin": True, "punct_begin": True, "empty_line": True, "forward": True})

    def _select(self):
        self.view.run_command("move", {"by": "stops", "word_begin": True, "punct_begin": True, "empty_line": True, "forward": True, "extend": True})

# W
class BigWordMotion(Motion):
    def move(self):
        self.view.run_command("move", {"by": "stops", "word_begin": True, "empty_line": True, "separators": "", "forward": True})

    def _select(self):
        self.view.run_command("move", {"by": "stops", "word_begin": True, "empty_line": True, "separators": "", "forward": True, "extend": True})

# b
class BackMotion(Motion):
    def move(self):
        self.view.run_command("move", {"by": "stops", "word_begin": True, "punct_begin": True, "empty_line": True, "forward": False})

    def _select(self):
        self.view.run_command("move", {"by": "stops", "word_begin": True, "punct_begin": True, "empty_line": True, "forward": False, "extend": True})

# B
class BigBackMotion(Motion):
    def move(self):
        self.view.run_command("move", {"by": "stops", "word_begin": True, "empty_line": True, "separators": "", "forward": False})

    def _select(self):
        self.view.run_command("move", {"by": "stops", "word_begin": True, "empty_line": True, "separators": "", "forward": False, "extend": True})

# e
class WordEndMotion(Motion):
    def move(self):
        RightMotion(self.view).move()
        self.view.run_command("move", {"by": "stops", "word_end": True, "punct_end": True, "empty_line": True, "forward": True})
        LeftMotion(self.view).move()

    def _select(self):
        RightMotion(self.view)._select()
        self.view.run_command("move", {"by": "stops", "word_end": True, "punct_end": True, "empty_line": True, "forward": True, "extend": True})

# E
class BigWordEndMotion(Motion):
    def move(self):
        RightMotion(self.view).move()
        self.view.run_command("move", {"by": "stops", "word_end": True, "empty_line": True, "separators": "", "forward": True})
        LeftMotion(self.view).move()

    def _select(self):
        RightMotion(self.view)._select()
        self.view.run_command("move", {"by": "stops", "word_end": True, "empty_line": True, "separators": "", "forward": True, "extend": True})

# j
class LeftMotion(Motion):
    def move(self):
        sel = self.view.sel()
        new_sel = []
        for r in sel:
            line = self.view.line(r)
            new_pt = r.a - 1
            if new_pt < line.a:
                new_pt = line.a
            new_sel.append(Region(new_pt))
        sel.clear()
        sel.add_all(new_sel)

    def _select(self):
        sel = self.view.sel()
        new_sel = []
        for r in sel:
            line = self.view.line(r)
            new_r = Region(r.a - 1, r.b)
            if new_r.a < line.a:
                new_r = Region(line.a, r.b)
            new_sel.append(new_r)
        sel.clear()
        sel.add_all(new_sel)

# l
class RightMotion(Motion):
    def move(self):
        sel = self.view.sel()
        new_sel = []
        for r in sel:
            line = self.view.line(r)
            new_pt = r.a + 1
            if new_pt >= line.b:
                new_pt = line.b - 1
            if line.a == line.b:
                new_pt = r.a
            new_sel.append(Region(new_pt))
        sel.clear()
        sel.add_all(new_sel)

    def _select(self):
        sel = self.view.sel()
        new_sel = []
        for r in sel:
            line = self.view.line(r)
            new_r = Region(r.a, r.b + 1)
            if new_r.b > line.b:
                new_r = Region(r.a, line.b)
            new_sel.append(new_r)
        sel.clear()
        sel.add_all(new_sel)

# k
class UpMotion(Motion):
    def move(self):
        self.view.run_command("move", {"by": "lines", "forward": False})

    def select(self, repeat=1):
        for i in range(repeat):
            self.view.run_command("move", {"by": "lines", "forward": False, "extend": True})
        self.view.run_command("expand_selection", {"to": "line"})

# j
class DownMotion(Motion):
    def move(self):
        self.view.run_command("move", {"by": "lines", "forward": True})

    def select(self, repeat=1):
        for i in range(repeat):
            self.view.run_command("move", {"by": "lines", "forward": True, "extend": True})
        self.view.run_command("expand_selection", {"to": "line"})

# {
class EmptyLineUpMotion(Motion):
    def move(self):
        self.view.run_command("move", {"by": "stops", "word_begin": False, "empty_line": True, "separators": "", "forward": False})

    def _select(self):
        self.view.run_command("move", {"by": "stops", "word_begin": False, "empty_line": True, "separators": "", "forward": False, "extend": True})

# }
class EmptyLineDownMotion(Motion):
    def move(self):
        self.view.run_command("move", {"by": "stops", "word_begin": False, "empty_line": True, "separators": "", "forward": True})

    def _select(self):
        self.view.run_command("move", {"by": "stops", "word_begin": False, "empty_line": True, "separators": "", "forward": True, "extend": True})

# _
class ToBOLMotion(Motion):
    def move(self):
        self.view.run_command("move_to", {"to": "bol"})

    def _select(self):
        self.view.run_command("move_to", {"to": "bol", "extend": True})

# 0
class ToHardBOLMotion(Motion):
    def move(self):
        self.view.run_command("move_to", {"to": "hardbol"})

    def _select(self):
        self.view.run_command("move_to", {"to": "hardbol", "extend": True})

# f
class FindInLineMotion(Motion):
    def __init__(self, view, character):
        self.view = view
        self.character = character

    def move(self):
        sel = self.view.sel()
        new_sel = []
        for r in sel:
            line = self.view.line(r)
            s = self.view.substr(Region(r.a, line.b))
            index = s.find(self.character, 1)
            if index == -1: new_sel.append(r)
            else: new_sel.append(Region(r.a + index))
        sel.clear()
        sel.add_all(new_sel)

    def _select(self):
        sel = self.view.sel()
        new_sel = []
        for r in sel:
            line = self.view.line(r)
            s = self.view.substr(Region(r.a, line.b))
            index = s.find(self.character, 1)
            if index == -1: new_sel.append(r)
            else: new_sel.append(Region(r.a, r.a + index + 1))
        sel.clear()
        sel.add_all(new_sel)

# F
class FindInLineBackwardsMotion(Motion):
    def __init__(self, view, character):
        self.view = view
        self.character = character

    def move(self):
        sel = self.view.sel()
        new_sel = []
        for r in sel:
            line = self.view.line(r)
            s = self.view.substr(Region(line.a, r.a))[::-1]
            index = s.find(self.character, 0)
            if index == -1: new_sel.append(r)
            else: new_sel.append(Region(r.a - index - 1))
        sel.clear()
        sel.add_all(new_sel)

    def _select(self):
        sel = self.view.sel()
        new_sel = []
        for r in sel:
            line = self.view.line(r)
            s = self.view.substr(Region(line.a, r.a))[::-1]
            index = s.find(self.character, 0)
            if index == -1: new_sel.append(r)
            else: new_sel.append(Region(r.a, r.a - index - 1))
        sel.clear()
        sel.add_all(new_sel)

# t
class ToInLineMotion(Motion):
    def __init__(self, view, character):
        self.view = view
        self.character = character

    def move(self):
        sel = self.view.sel()
        new_sel = []
        for r in sel:
            line = self.view.line(r)
            s = self.view.substr(Region(r.a, line.b))
            index = s.find(self.character, 1)
            if index == -1: new_sel.append(r)
            else: new_sel.append(Region(r.a + index - 1))
        sel.clear()
        sel.add_all(new_sel)

    def _select(self):
        sel = self.view.sel()
        new_sel = []
        for r in sel:
            line = self.view.line(r)
            s = self.view.substr(Region(r.a, line.b))
            index = s.find(self.character, 1)
            if index == -1: new_sel.append(r)
            else: new_sel.append(Region(r.a, r.a + index))
        sel.clear()
        sel.add_all(new_sel)

# T
class ToInLineBackwardsMotion(Motion):
    def __init__(self, view, character):
        self.view = view
        self.character = character

    def move(self):
        sel = self.view.sel()
        new_sel = []
        for r in sel:
            line = self.view.line(r)
            s = self.view.substr(Region(line.a, r.a))[::-1]
            index = s.find(self.character, 0)
            if index == -1: new_sel.append(r)
            else: new_sel.append(Region(r.a - index))
        sel.clear()
        sel.add_all(new_sel)

    def _select(self):
        sel = self.view.sel()
        new_sel = []
        for r in sel:
            line = self.view.line(r)
            s = self.view.substr(Region(line.a, r.a))[::-1]
            index = s.find(self.character, 0)
            if index == -1: new_sel.append(r)
            else: new_sel.append(Region(r.a, r.a - index))
        sel.clear()
        sel.add_all(new_sel)

motions = {
    "w": WordMotion,
    "W": BigWordMotion,
    "b": BackMotion,
    "B": BigBackMotion,
    "e": WordEndMotion,
    "E": BigWordEndMotion,
    "h": LeftMotion,
    "j": DownMotion,
    "k": UpMotion,
    "l": RightMotion,
    "{": EmptyLineUpMotion,
    "}": EmptyLineDownMotion,
    "_": ToBOLMotion,
    "0": ToHardBOLMotion,
    "f": FindInLineMotion,
    "F": FindInLineBackwardsMotion,
    "t": ToInLineMotion,
    "T": ToInLineBackwardsMotion,
}
