# Vinimum | Vim Minimum
Minimalistic Vim Emulation for Sublime Text

> This Package does not try to faithfully emulate Vim! It is a very stripped down, minimal and opinionated Vim emulation instead. If what you want is a faithful Vim experience inside Sublime Text, look at [NeoVintageous](https://github.com/NeoVintageous/NeoVintageous) instead.

## Quick Start and Usage
After installing the Plugin, add this to your `Default.sublime-keymap` *(Preferences -> Key Bindings)*:
```json
{ "keys": ["ctrl+["], "command": "vnm_enter_command_mode" },
```
This is the default recommended configuration for Vinimum. As for why this is not included by default, please read the [Philosophy](#philosophy) section.

After that, simply use `ctrl+[` to enter command mode in which you can enter *most* vim commands just as you would in vim, although not all commands are implemented yet. For a list of differences in commands between Vinimum and Vim, read the [Differences to Vim](#differences-to-vim) section. For a list of commands that are implemented, see the [List of Implemented Commands](#list-of-implemented-commands) section.

## Differences to Vim
- Normal Mode is called Command Mode, Insert Mode is called Sublime Mode. These names better reflect the philosophy of Vinimum, as Command Mode is the exception, and Sublime Mode is unaltered Sublime.
- There is no Visual Mode. Any Selection made while in Command Mode will immediately put one into Sublime Mode. `v` in Vinimum is instead an action that will select the following motion or text object. This is currently not intended to change, although there might be a setting to enable a Visual Mode in the future.
- Some Sublime commands will throw you into Sublime Mode, specifically anything that opens a panel or overlay (e.g. `ctrl+shift+p`).
- Repetition does not correctly work yet.
  - Numbers given before commands do currently not work, however this is planned for the future.
  - The `.` command currently only repeats the last command, without tracking any input given directly after. This means that, for example, when replacing a word with "hello" by typing `c i w h e l l o ctrl+[`, then a `.` command after will only repeat the `c i w` part. This might be corrected in the future.
- `j` and `k` do not go by logical lines, but instead by visual lines. I.e. in a buffer with wordwrap on, when a logical line wraps and has multiple visual lines, `j` and `k` in Command Mode will act just like the up and down arrow keys. This is intended, though there might be a setting for it in the future.
- Registers do not exist, commands like yank and paste are not implemented yet. Any copying and pasting should, at least for now, be done the Sublime way.

## Philosophy
The core idea of Vinimum is the following: if someone were to secretly install the Package on your Sublime Text, unless you would specifically look for it, you wouldn't know it's there.

Another core ideal is also that Vinimum has no intention of reaching feature parity with Vim, or even being faithful to it. This Package is supposed to provide a **thin, minimalistic emulation layer** to get the core functionality of Vim and nothing more. Vinimum is first a Sublime Package, second a Vim emulation, i.e. Sublime's philosophy will usually be preferred over Vim's philosophy.

This means the following:
1. Any keybind that would be replace a default Sublime keybind is not included by default. This also means **there is no way to get into command mode by default!**
2. While in Sublime Mode, the Package does not interfere with anything
3. Any case of ambiguation of what an input means is tried to be prevented or Sublime's default interpretation is used
4. Mouse usage is not actively hindered. When selecting text with a mouse, Vinimum will immediately go into Sublime Mode.

Because of **1**, after installing the Package, one has to add a keybind of their choice to enter Command Mode before the Package is usable. To do so, add a keybind for the command `vnm_enter_command_mode` to your `Default.sublime-keymap` *(Preferences -> Key Bindings)*:
```json
{ "keys": ["ctrl+["], "command": "vnm_enter_command_mode" },
```
The above is the recommended keybind for Vinimum. The reason why `escape` for the key should not be used is explained below in the [Why not stay more faithful to Vim?](#why-not-stay-more-faithful-to-vim) section, although obviously it can also be used if that is desired. `ctrl+[` is the default alternative to `escape` in Vim, which is why it's recommended to be used in place of `escape`.

The reason that keybind is not included by default is that it replaces the Sublime default keybind for `unindent`:
```json
{ "keys": ["ctrl+["], "command": "unindent" },
```

Since the philosophy of Vinimum is to not replace *any* of Sublime's default keybinds, the `ctrl+[` keybind cannot be included by default. The overriding of the `unindent` keybind can be combated in a few ways:
1. Set the `shift_tab_unindent` setting to `true` and use `shift+tab` instead.
2. Use a different keybind to enter command mode, for example `ctrk+'`. However, this will destroy muscle memory.
3. Remap `unindent` and `indent` one key to the right like this:
   ```json
   { "keys": ["ctrl+]"], "command": "unindent" },
   { "keys": ["ctrl+\\"], "command": "indent" },
   ```

## Why not stay more faithful to Vim?
The question could also be framed as "why did I create this plugin and not just use NeoVintageous?", thus this section is mostly my personal opinion on Vim and Vim Plugins.

1. **Ambiguation of `escape`:**\
   Vim plugins will usually remap `escape` to `enter_command_mode`. However, this creates a lot of ambiguation as `escape` is already used in some places inside Sublime. Most importantly, it is the default key to close any kind of panel, overlay, auto complete or similar. When you have an auto complete suggestion and press `escape`, it is not clear if what you want is to hide the auto complete, or go into Command Mode. This ambiguation cannot simply be solved by defining one over the other, as a user will not always want one over the other, but instead makes that decision situationally. As such, the only way to fix this is to not use `escape`.
2. **Redifinition of default keybinds:**\
   Vim plugins typically rebind keybinds like `ctrl+r` (redo in Vim, goto symbol in Sublime) to use the Vim interpretation. They either rebind the keybind globally, which destroys any keybind knowledge and muscle memory one has built for Sublime, or they rebind the keybind only while in Command Mode, making the keybind unpredictable as it has different behaviour in different contexts.

   Either version I dislike. Sublime already has a keybind for redo, it's `ctrl+shift+z`, and while one may argue that to be a worse keybind, I would also argue that the goto symbol command of Sublime is useful enough to not be overwritten. Not to mention that `ctrl+shift+z` is certainly a more widely used default for redo. A user of Vinimum can still bind `ctrl+r` to whatever they want, but Vinimum itself will not impose such keybinds by default.
3. **Compatibility with Mouse-Heavy editing of code:**\
   One of the main advantages of Vim is that it offers tools for mouse-less editing of code. That is great, however not always the way to go. Mouse-less editing is great when doing focused, uninterrupted editing of code, and I want Vim functionality for those situations.

   However, I don't always edit code by having both my hands on the keyboard and the editor in fullscreen. Sometimes, you're refactoring, or just hacking some code snippets together. Sometimes, editing code means copying code from an online resource to analyze, execute, slightly modify or learn from it. Mouse usage can slow one down during focused editing, but when editing code is secondary, having only one hand on the keyboard and the other on the mouse is not unusual. For those situations, Vim is about as bad of a choice as it gets. Being able to edit code the same way I would in vanilla Sublime is important to me. When selecting some text with the mouse that I want to delete, I don't want to have to find the `d` key with my left hand, instead I want to use my muscle memory to hit `backspace` like I did ever since using a computer for the first time.

   Vim forces me into having both hands on the keyboard. It actively hinders and discourages the use of a mouse. Howver, **I want the functionality to not need a mouse, yet not be actively hindered when using one.**
4. **Occasional strange behaviour with panels and overlays:**
   Sometimes Vim Plugins cause problems when using panels or overlays, like the Command Palette. To combat this, Vinimum immediately jumps into Sublime Mode if it detects that a panel or overlay was opened. Note that because of [an issue with `show_overlay`](https://github.com/sublimehq/sublime_text/issues/2198), this is currently solved by remapping the default keybinds for `show_overlay`. If you have custom keybinds for overlays, please look into the `Default.sublime-keymap` file of this package to see how you can rebind your custom keybinds. An issue like this does not exist for panels.

## List of Implemented Commands
The implementation of Vinimum differentiates between *commands*, *actions*, *motions*, *text_object_modifiers* and *text_objects*.

- *commands*: direct execution\
  `i`, `I`, `a`, `A`, `o`, `O`, `x`, `D`, `C`, `r`
- *actions*: followed by either itself, a *motion* or a *text_object*\
  `d`, `c`, `v`
- *motions*: define a movement from the current caret positon\
  `w`, `W`, `b`, `B`, `e`, `E`, `h`, `j`, `k`, `l`, `{`, `}`, `_`, `0`, `f`, `F`, `t`, `T`
- *text_object_modifiers*: used as a modifier for *text_objects*\
  `i` (inner), `a` (outer)
- *text_objects*: define an area\
  `w`,`(`,`[`,`{`,`'`,`"`
