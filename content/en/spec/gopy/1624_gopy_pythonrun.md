---
title: "gopy pythonrun"
description: "Port of cpython/Python/pythonrun.c. PyRun_SimpleString, PyRun_File, the REPL loop, and the .pyc read/write helpers that the lifecycle calls."
tags: ["gopy", "spec"]
weight: 1624
---

# 1624. Pythonrun: source-to-result entry points

## What we are porting

`Python/pythonrun.c` (~1.7k lines). Three concerns:

1. **String / file evaluation**. `PyRun_SimpleString`,
   `PyRun_AnyFile`, `PyRun_FileEx`, `PyRun_String`. The
   plumbing that takes a chunk of source, calls the parser,
   compiles, and runs through the VM.
2. **Interactive REPL**. `PyRun_InteractiveLoop` and friends.
   Reads a line, parses, compiles, runs, prints. Until EOF.
3. **`.pyc` read/write helpers**. `_PyRun_PycFile` and the
   marshal-magic check. (The marshal port itself lives in
   1623; this spec uses it.)

`pythonrun.c` is the *consumer* layer that sits on top of
parser + compile + vm. It does not own any state; it threads
the right `*state.Thread` through to each subsystem.

## Why this lands in v0.7 alongside lifecycle

`lifecycle.Main` (spec 1622) needs a target to dispatch to:

* `gopy script.py` => `pythonrun.RunFile`.
* `gopy -c "..."` => `pythonrun.RunString`.
* `gopy` (no args) => `pythonrun.InteractiveLoop`.
* `gopy -m foo` => deferred to v0.8 (import-driven).

In v0.6 cmd/gopy hand-rolled `RunString` inline. v0.7 moves
that to `pythonrun.RunString` and adds the file and REPL
arms.

## Package layout

```
gopy/pythonrun/
  runstring.go      # PyRun_SimpleString and PyRun_String
  runfile.go        # PyRun_AnyFile and PyRun_FileEx
  repl.go           # PyRun_InteractiveLoop, the prompt loop
  pyc.go            # _PyRun_PycFile (marshal magic check)
  exceptions.go     # _PyErr_Print and the SystemExit / KeyboardInterrupt
                    # hooks pythonrun owns
```

## v0.7 release blockers

* `1624-A` Port `PyRun_SimpleStringFlags`. Drives the v0.6
  `gopy -c` smoke; same fixture must keep passing once the
  call site moves into pythonrun.
  CPython: `Python/pythonrun.c:432 PyRun_SimpleStringFlags`.
* `1624-B` Port `PyRun_AnyFileExFlags` plus the closeit-on-EOF
  semantics.
  CPython: `Python/pythonrun.c:88 PyRun_AnyFileExFlags`.
* `1624-C` Port `PyRun_InteractiveLoopFlags` for the basic
  REPL. v0.7 uses `bufio.Scanner` from stdin; readline editing
  is deferred to v0.9 (spec 1645).
  CPython: `Python/pythonrun.c:128 PyRun_InteractiveLoopFlags`.
* `1624-D` Port `_PyErr_Print` so unhandled exceptions print
  the traceback CPython would.
  CPython: `Python/pythonrun.c:797 _PyErr_PrintEx`.
* `1624-E` `pythonrun_test.go` panel: 12 fixtures driven
  through RunString, plus `TestREPL` exercising a pipe-based
  stdin against canned input.

## Test gates

* `pythonrun/runstring_test.go` — the v0.6 cpython_smoke panel
  re-rooted onto `pythonrun.RunString`. Same 13 cases must
  still match python3 stdout.
* `pythonrun/repl_test.go` — feed `"1+2\nprint('done')\n"`
  through stdin, assert stdout is `"3\ndone\n"`.
* `pythonrun/runfile_test.go` — write a temp `.py` file with
  one expression, assert RunFile evaluates it and prints the
  result.

## Out of scope

* `.pyc` execution (`_PyRun_PycFile`) is wired but stubbed in
  v0.7; the marshal arm lands in v0.8.
* PEP 657 traceback positions need the full source-position
  walker; v0.7 ships file:line:col only, no caret pinning.
