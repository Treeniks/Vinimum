import sublime
from sublime import Edit, View, Region
from sublime_plugin import TextCommand, EventListener

from Vinimum.actions import actions
from Vinimum.commands import commands
from Vinimum.motions import motions, LeftMotion
from Vinimum.text_objects import modifiers, text_objects

from enum import Enum

class State(Enum):
    SUBLIME = 0
    COMMAND = 1

g_state = State.SUBLIME
g_command = ""

def update_visuals():
    global g_state, g_command

    for window in sublime.windows():
        for view in window.views():
            if g_state == State.COMMAND:
                view.settings().set("inverse_caret_state", True)
                view.settings().set("command_mode", True)
                desc = "COMMAND MODE"
            else:
                view.settings().set("inverse_caret_state", False)
                view.settings().set("command_mode", False)
                desc = "SUBLIME MODE"
            if g_command:
                desc += f" - {g_command}"
            # the '_' is to ensure that this is the first entry in the status line
            view.set_status("_vinimum", desc)

def reset():
    global g_command

    g_command = ""
    update_visuals()

def enter_command_mode(view: View):
    global g_state

    g_state = State.COMMAND
    LeftMotion(view).move()
    reset()

def enter_sublime_mode():
    global g_state

    g_state = State.SUBLIME
    reset()

def eval(view: View):
    global g_command

    try:
        a = g_command[0]
        # r is a special command
        if a == "r":
            b = g_command[1]
            view.run_command("vnm_replace_character", {"character": b})
        # f/F/t/T are special motions
        elif a in "fFtT":
            b = g_command[1]
            motion = motions[a](view, b)
            motion.move()
        elif a in commands:
            # e.g. 'i'
            command = commands[a](view)
            command.run()
        elif a in motions:
            # e.g. 'w'
            motion = motions[a](view)
            motion.move()
        elif a in actions:
            # e.g. 'd'
            action = actions[a](view)
            b = g_command[1]
            if b == a:
                # e.g. 'dd'
                action.double()
            # f/F/t/T are special motions
            elif b in "fFtT":
                c = g_command[2]
                motion = motions[b](view, c)
                action.run(motion.select)
            elif b in motions:
                # e.g. 'dw'
                motion = motions[b](view)
                action.run(motion.select)
            elif b in modifiers:
                # e.g. 'di'
                modifier = modifiers[b]
                c = g_command[2]
                if c in text_objects:
                    # e.g. 'diw'
                    text_object = text_objects[c](view, modifier)
                    action.run(text_object.select)
        reset()
    except IndexError:
        pass

class VnmEventListener(EventListener):
    def on_init(self, views):
        global g_state

        enter_sublime_mode()

    def on_activated(self, view):
        global g_state

        self.on_selection_modified(view)
        reset()

    def on_load(self, view):
        global g_state

        reset()

    def on_new(self, view):
        self.on_load(view)

    def on_clone(self, view):
        self.on_load(view)

    def on_selection_modified(self, view):
        global g_state

        if view.has_non_empty_selection_region():
            enter_sublime_mode()
        elif g_state == State.COMMAND:
            sel = view.sel()
            new_sel = []
            for r in sel:
                line = view.line(r)
                if line.a != line.b and r.b == line.b:
                    new_sel.append(Region(r.b-1))
                else:
                    new_sel.append(r)
            sel.clear()
            sel.add_all(new_sel)


    def on_query_context(self, view, key, operator, operand, match_all):
        global g_state

        if key == "vnm.command_mode": val = (g_state == State.COMMAND)
        elif key == "vnm.command_in_process": val = (not g_command == "")
        else: return None

        if operator == sublime.OP_EQUAL: return val == operand
        elif operator == sublime.OP_NOT_EQUAL: return val != operand

    def on_post_window_command(self, view, command_name, args):
        # show_overlay does not get tracked
        # see https://github.com/sublimehq/sublime_text/issues/2198
        if command_name == "show_overlay" or command_name == "show_panel":
            enter_sublime_mode()

class VnmFeedInput(TextCommand):
    def run(self, edit: Edit, key: str):
        global g_command

        g_command += key
        # ? only add g_command to statusline in active view
        update_visuals()
        eval(self.view)

class VnmEnterCommandMode(TextCommand):
    def run(self, edit: Edit):
        enter_command_mode(self.view)

# see https://github.com/sublimehq/sublime_text/issues/2198
class VnmOverlayWorkaround(TextCommand):
    def run(self, edit: Edit, overlay, show_files=False, text=""):
        enter_sublime_mode()
        self.view.window().run_command("show_overlay", {"overlay": overlay, "show_files": show_files, "text": text})

class VnmResetCommandCommand(TextCommand):
    def run(self, edit: Edit):
        reset()

# assumes that the selections are points
class VnmReplaceCharacter(TextCommand):
    def run(self, edit: Edit, character):
        sel = self.view.sel()
        for r in sel:
            self.view.replace(edit, Region(r.a, r.b + 1), character)
