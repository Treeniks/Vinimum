from sublime import View, Region
from Vinimum.actions import Actionable

class Motion(Actionable):
    def __init__(self, view: View):
        self.view = view

    def move(self):
        pass

    def select(self):
        pass

class WordMotion(Motion):
    def move(self):
        self.view.run_command("move", {"by": "stops", "word_begin": True, "punct_begin": True, "empty_line": True, "forward": True})

    def select(self):
        self.view.run_command("move", {"by": "stops", "word_begin": True, "punct_begin": True, "empty_line": True, "forward": True, "extend": True})

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

    def select(self):
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

    def select(self):
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

class UpMotion(Motion):
    def move(self):
        self.view.run_command("move", {"by": "lines", "forward": False})

    def select(self):
        self.view.run_command("move", {"by": "lines", "forward": False, "extend": True})
        self.view.run_command("expand_selection", {"to": "line"})

class DownMotion(Motion):
    def move(self):
        self.view.run_command("move", {"by": "lines", "forward": True})

    def select(self):
        self.view.run_command("move", {"by": "lines", "forward": True, "extend": True})
        self.view.run_command("expand_selection", {"to": "line"})

# '{'
class EmptyLineUpMotion(Motion):
    def move(self):
        self.view.run_command("move", {"by": "stops", "word_begin": False, "empty_line": True, "separators": "", "forward": False})

    def select(self):
        self.view.run_command("move", {"by": "stops", "word_begin": False, "empty_line": True, "separators": "", "forward": False, "extend": True})

# '}'
class EmptyLineDownMotion(Motion):
    def move(self):
        self.view.run_command("move", {"by": "stops", "word_begin": False, "empty_line": True, "separators": "", "forward": True})

    def select(self):
        self.view.run_command("move", {"by": "stops", "word_begin": False, "empty_line": True, "separators": "", "forward": True, "extend": True})

motions = {
    "w": WordMotion,
    "h": LeftMotion,
    "j": DownMotion,
    "k": UpMotion,
    "l": RightMotion,
    "{": EmptyLineUpMotion,
    "}": EmptyLineDownMotion,
}
