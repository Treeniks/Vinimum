import sublime
from sublime import Region
from sublime_plugin import TextCommand, EventListener

import Vinimum.actions as actions
import Vinimum.commands as commands
import Vinimum.motions as motions
import Vinimum.text_objects as text_objects

from enum import Enum

class State(Enum):
    SUBLIME = 0
    COMMAND = 1

g_state = State.SUBLIME
g_command = ""
g_prev_command = ""
g_insert = ""
# this is here to get around some issues with undo and the . repeat command
# True if the current/last TextCommand was undo
g_undo = False

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
                desc += f" {g_command}"
            # the '_' is to ensure that this is the first entry in the status line
            view.set_status("_vinimum", desc)

def reset():
    global g_command, g_prev_command

    g_command = ""
    update_visuals()

def remove_selection(view):
    sel = view.sel()
    new_sel = []
    for r in sel:
        if r.b < r.a:
            new_sel.append(Region(r.b))
        else:
            new_sel.append(Region(r.b - 1))
    sel.clear()
    sel.add_all(new_sel)

def enter_command_mode(view):
    global g_state

    if g_state == State.COMMAND:
        reset()
    else:
        g_state = State.COMMAND
        if view.has_non_empty_selection_region():
            remove_selection(view)
        else:
            motions.LeftMotion(view).move()
        update_visuals()

def enter_sublime_mode():
    global g_state

    g_state = State.SUBLIME
    update_visuals()

def eval(view):
    global g_command, g_prev_command, g_insert

    i = 0
    try:
        a = g_command[i]

        to_insert = None
        if a == ".": # repeat command
            g_command = g_prev_command
            a = g_command[i]
            to_insert = g_insert

        repeat = 1
        if a.isnumeric() and not a == "0":
            repeat = 0
            while a.isnumeric():
                repeat = repeat * 10 + int(a)
                i += 1
                a = g_command[i]

        if a == "r": # r is a special command
            b = g_command[i + 1]
            for i in range(repeat):
                view.run_command("vnm_replace_character", {"character": b})
                if not i == repeat - 1:
                    motions.RightMotion(view).move()
            g_prev_command = g_command

        elif a in "fFtT": # f/F/t/T are special motions
            b = g_command[i + 1]
            motion = motions.motions[a](view, b)
            for i in range(repeat):
                motion.move()

        elif a in commands.commands: # e.g. 'i'
            command = commands.commands[a](view)
            # TODO some commands have unique behaviour upon numerical repetition
            command.run()
            if command.repeatable():
                g_prev_command = g_command
                if not to_insert:
                    g_insert = ""

        elif a in motions.motions: # e.g. 'w'
            motion = motions.motions[a](view)
            for i in range(repeat):
                motion.move()

        elif a in actions.actions: # e.g. 'd'
            action = actions.actions[a](view)
            b = g_command[i + 1]

            if b == a: # e.g. 'dd'
                for i in range(repeat):
                    action.double()

            else:
                if b.isnumeric() and not b == "0":
                    tmp = 0
                    while b.isnumeric():
                        tmp = tmp * 10 + int(b)
                        i += 1
                        b = g_command[i + 1]
                    repeat *= tmp

                if b in "fFtT": # f/F/t/T are special motions
                    c = g_command[i + 2]
                    motion = motions.motions[b](view, c)
                    action.run(lambda: motion.select(repeat))

                elif b in motions.motions: # e.g. 'dw'
                    motion = motions.motions[b](view)
                    action.run(lambda: motion.select(repeat))

                elif b in text_objects.modifiers: # e.g. 'di'
                    modifier = text_objects.modifiers[b]
                    c = g_command[i + 2]
                    if c in text_objects.text_objects: # e.g. 'diw'
                        text_object = text_objects.text_objects[c](view, modifier)
                        for i in range(repeat):
                            action.run(text_object.select)

            g_prev_command = g_command
            if not to_insert:
                g_insert = ""

        if to_insert:
            view.run_command("insert", {"characters": to_insert})
            enter_command_mode(view)

        reset()
    except IndexError:
        pass

class VnmEventListener(EventListener):
    def on_init(self, views):
        global g_state

        enter_sublime_mode()
        reset()

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
        global g_state, g_prev_command, g_insert

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

    def on_modified(self, view):
        global g_insert, g_undo

        (s, d, i) = view.command_history(0, True)

        # required to check because undoing an insert
        # will be listed as an "insert" command in the history
        if not g_undo:
            if s == "insert":
                g_insert += d["characters"]
            elif s == "left_delete":
                g_insert = g_insert[:-1]


    def on_text_command(self, view, command_name, args):
        global g_undo

        if command_name == "undo": g_undo = True
        else: g_undo = False

    def on_post_text_command(self, view, command_name, args):
        global g_prev_command, g_insert

        if command_name == "move" and not g_insert == "":
            g_insert = ""
            g_prev_command = "i"

    def on_post_window_command(self, view, command_name, args):
        # show_overlay does not get tracked
        # see https://github.com/sublimehq/sublime_text/issues/2198
        if command_name == "show_overlay" or command_name == "show_panel":
            enter_sublime_mode()

class VnmFeedInput(TextCommand):
    def run(self, edit, key: str):
        global g_command

        g_command += key
        # ? only add g_command to statusline in active view
        # ? support for longer strings?
        update_visuals()
        eval(self.view)

class VnmEnterCommandMode(TextCommand):
    def run(self, edit):
        enter_command_mode(self.view)

# see https://github.com/sublimehq/sublime_text/issues/2198
class VnmOverlayWorkaround(TextCommand):
    def run(self, edit, overlay, show_files=False, text=""):
        enter_sublime_mode()
        self.view.window().run_command("show_overlay", {"overlay": overlay, "show_files": show_files, "text": text})

class VnmResetCommandCommand(TextCommand):
    def run(self, edit):
        reset()

# assumes that the selections are points
class VnmReplaceCharacter(TextCommand):
    def run(self, edit, character):
        sel = self.view.sel()
        for r in sel:
            self.view.replace(edit, Region(r.a, r.b + 1), character)
