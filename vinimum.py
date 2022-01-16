import sublime
from sublime import Edit, View
from sublime_plugin import TextCommand, EventListener
from Vinimum.actions import actions
from Vinimum.commands import commands
from Vinimum.motions import motions
from Vinimum.text_objects import text_objects, modifiers

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

def enter_command_mode():
    global g_state

    g_state = State.COMMAND
    update_visuals()

def enter_sublime_mode():
    global g_state

    g_state = State.SUBLIME
    update_visuals()

def eval(view: View):
    global g_command

    try:
        a = g_command[0]
        if a in commands:
            command = commands[a](view)
            command.run()
        if a in motions:
            motion = motions[a](view)
            motion.move()
        elif a in actions:
            action = actions[a](view)
            b = g_command[1]
            if b in motions:
                motion = motions[b](view)
                action.run(motion)
            elif b in modifiers:
                modifier = modifiers[b]
                c = g_command[2]
                if c in text_objects:
                    text_object = text_objects[c](view, modifier)
                    action.run(text_object)
        reset()
    except IndexError:
        pass

class VnmEventListener(EventListener):
    def on_query_context(self, view, key, operator, operand, match_all):
        global g_state

        if key == "vnm.command_mode":
            if operator == sublime.OP_EQUAL:
                return (g_state == State.COMMAND) == operand
            elif operator == sublime.OP_NOT_EQUAL:
                return (g_state == State.COMMAND) != operand

class VnmFeedInput(TextCommand):
    def run(self, edit: Edit, key: str):
        global g_command

        g_command += key
        # ? only add g_command to statusline in active view
        update_visuals()
        eval(self.view)

class VnmEnterCommandMode(TextCommand):
    def run(self, edit):
        enter_command_mode()
