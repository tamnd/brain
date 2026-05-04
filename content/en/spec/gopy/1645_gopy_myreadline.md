---
title: "gopy myreadline"
description: "Port of cpython/Parser/myreadline.c. Cross-platform readline shim used by the interactive REPL. Mostly a thin wrapper over the host readline library; gopy substitutes Go-native line editing."
tags: ["gopy", "spec"]
weight: 1645
---

# 1645. myreadline

## What we are porting

`Parser/myreadline.c` (~700 lines) is CPython's host-readline
shim. It owns:

* The signal-safe `PyOS_Readline` entry point that the REPL
  calls one line at a time.
* Integration with GNU readline / libedit when present.
* The fallback for when no readline library is linked (raw stdin
  with Ctrl-C handling).
* Atomicity around `PyOS_FinalizeReadline`.

This file is the smallest of the parser block and the most
divergent from CPython, because gopy does not link `libreadline`.
We substitute a Go-native line editor.

## Strategy

Two layers:

1. `parser/readline/`: the public entry point
   `Readline(prompt) (string, error)`. The REPL and the
   `FromReadline` tokenizer driver (1641) call it.
2. `parser/readline/<backend>.go`: backend selected at build time.
   `goreadline.go` is the default; we link `golang.org/x/term` for
   raw mode and pull in `chzyer/readline` (or a hand-rolled
   editor) for history and line editing.

Both layers stay free of CPython header dependencies. They just
expose the same `(prompt) -> (line, err)` shape.

## What stays compatible

User-observable behaviour to preserve:

1. Ctrl-C at the prompt raises KeyboardInterrupt without exiting
   the REPL.
2. EOF (Ctrl-D on Unix, Ctrl-Z+Enter on Windows) returns
   `io.EOF` from `Readline`.
3. The history file path (`PYTHONSTARTUP`, `~/.python_history`)
   is read and updated in the same locations CPython uses.
4. Continuation prompt is `sys.ps2` (`"... "` by default), same
   as primary `sys.ps1` (`">>> "`).
5. Tab completion hooks into the same `rlcompleter`-shaped
   Python-side callback when `readline.set_completer` is set.

## What diverges

* No GNU readline link. We use a Go-native editor.
* No libedit fallback path. Goes through the same Go editor.
* `PyOS_InputHook` (used by IDLE for Tk integration) becomes a
  Go callback registry; users targeting IDLE would still need a
  Go-native shim. Not in scope for v0.9.

## Go shape

```go
// Readline reads one line from the user, displaying prompt.
// Mirrors PyOS_Readline. Returns io.EOF on EOF.
func Readline(prompt string) (string, error)

// SetCompleter registers a tab-completion callback.
// Mirrors readline.set_completer.
func SetCompleter(fn func(text string, state int) (string, bool))

// LoadHistory reads the history file. Returns nil if the file
// does not exist.
func LoadHistory(path string) error

// SaveHistory appends the in-memory history to path.
func SaveHistory(path string) error
```

## File mapping

| C source                       | Go target                                |
|--------------------------------|------------------------------------------|
| `Parser/myreadline.c`          | `parser/readline/readline.go`            |
| (no CPython equivalent)        | `parser/readline/editor.go` (backend)    |
| (no CPython equivalent)        | `parser/readline/history.go`             |

## Checklist

Status legend: `[x]` shipped, `[ ]` pending, `[~]` partial / scaffold,
`[n]` deferred / not in scope this phase.

### Files

* [ ] `parser/readline/readline.go`: `Readline`, signal handling,
  prompt rendering.
* [ ] `parser/readline/editor.go`: terminal raw-mode driver,
  arrow-key navigation, line editing primitives.
* [ ] `parser/readline/history.go`: `LoadHistory`, `SaveHistory`,
  in-memory ring buffer.
* [ ] `parser/readline/completer.go`: `SetCompleter`, tab
  expansion plumbing.
* [ ] `parser/readline/readline_test.go`: scripted-input panel
  (no real terminal needed).

### Surface guarantees

* [ ] Ctrl-C at the prompt raises KeyboardInterrupt.
* [ ] Ctrl-D on an empty line returns `io.EOF`.
* [ ] History file path defaults to `~/.python_history`,
  overridable via `PYTHONSTARTUP`.
* [ ] `sys.ps1` / `sys.ps2` thread through unchanged.
* [ ] Tab completion calls the registered completer with the
  same `(text, state)` protocol as CPython.

### Out of scope

* IDLE / Tkinter `PyOS_InputHook`. Tracked separately if/when
  IDLE support is in scope.
* GNU readline binary compatibility. We never link `libreadline`.
* Bracketed paste mode beyond what the Go editor library
  provides.

### Cross-references

* REPL entry point: separate spec series (sysconfig / interpreter
  loop, not yet numbered).
* Tokenizer driver that consumes Readline: 1641.
