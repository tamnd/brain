---
title: "gopy gc, weakrefs, finalizers"
description: "v0.10 cycle GC port. Maps Python/gc.c, Python/gc_gil.c, Python/object_stack.c, Objects/weakrefobject.c onto gopy/gc and objects/weakref. Defines what '100% behavioural compatibility' means when the host runtime is Go (which already collects cycles)."
tags: ["gopy", "spec"]
weight: 1613
---

# 1613. gopy gc, weakrefs, finalizers

## Goal

Port CPython's cycle collector and weakref machinery to Go so that
the user-visible behaviour of the `gc` and `weakref` modules matches
upstream byte-for-byte. v0.3 shipped a refcount/finalizer skeleton at
`gc/gc.go`; `gc.Collect()` is currently a no-op
(`gc/gc.go:113`). v0.10 makes it real.

## Why a Python collector on top of Go's GC

Go's runtime already reclaims unreachable cycles. We do not need a
second collector to free memory. We *do* need a CPython-shaped
collector for three reasons that Go's GC cannot satisfy on its own:

1. **Finalizer ordering**. CPython runs `tp_finalize` / `__del__` on a
   tracked object as part of the cycle pass and obeys the legacy
   finalizer rules (no finalizer on objects reachable from a finalizer,
   resurrection check, exactly-once invocation).
   `runtime.SetFinalizer` in Go runs in arbitrary order at arbitrary
   times.
2. **Weakref callback timing**. PEP 442 specifies that weakrefs to
   objects in a collected cycle are cleared *before* finalizers run,
   and callbacks fire in a defined order. Go has no equivalent.
3. **The `gc` module API surface**. `gc.collect()`, `gc.get_objects()`,
   `gc.get_count()`, `gc.set_threshold()`, `gc.is_tracked()`,
   `gc.freeze()` are all CPython-shaped and the stdlib uses them.

The collector therefore runs as a *bookkeeping* pass over the tracked
set: it walks references, classifies reachability, fires weakref
callbacks and finalizers in the right order, and clears references on
collected objects so Go's GC can reclaim the memory on the next cycle.
We do *not* maintain refcounts; "is this object dead in a cycle" is
determined by walking references inside the tracked set, the same way
CPython does.

## Sources of truth

| CPython file                       | Lines | Target                     |
|------------------------------------|------:|----------------------------|
| `Python/gc.c`                      |  2057 | `gc/collector.go` plus splits |
| `Python/gc_gil.c`                  |    17 | `gc/gil.go`                |
| `Python/object_stack.c`            |    66 | `gc/objstack.go`           |
| `Objects/weakrefobject.c`          |  1134 | `objects/weakref.go`       |
| `Modules/gcmodule.c`               |   ~600 | `gc/module.go` (built-in registration) |
| `Include/internal/pycore_gc.h`     |   ~300 | type/state declarations spread across the targets |

`gc/gc.go` is the existing v0.3 skeleton (Track / Untrack /
RegisterFinalizer / Finalize / Collect-stub). v0.10 keeps the public
API of that file and grows the package.

## Package layout

```
gc/
  gc.go         Track / Untrack / RegisterFinalizer / Finalize public API (kept)
  state.go      GCState struct, generation lists, thresholds, enabled flag
  list.go       gc_list_* doubly-linked list helpers (gc.c:205-313)
  refs.go       update_refs / subtract_refs / visit_decref (gc.c:392-495)
  reachable.go  move_unreachable / visit_reachable / clear_unreachable_mask (gc.c:497-728)
  finalize.go   has_legacy_finalizer / move_legacy_finalizer_reachable / finalize_garbage (gc.c:672-1067)
  weakref.go    handle_weakrefs callback queue + clearing pass (gc.c:772-948)
  collector.go  gc_collect_main, gc_select_generation, _PyGC_Collect entry points (gc.c:1258-1696)
  module.go     gc built-in module: collect, enable, disable, get_threshold, set_threshold, get_count, get_objects, is_tracked, freeze, unfreeze
  gil.go        collector-vs-mutator interlock (gc_gil.c)
  objstack.go   _PyObjectStack helper (object_stack.c)

objects/
  weakref.go    PyWeakref / PyWeakrefRef / PyWeakrefProxy types, callback list, _PyWeakref_ClearWeakRefsExceptCallbacks
```

## Tracked-object protocol

Every container type that can participate in a cycle calls
`gc.Track(o)` from its constructor and `gc.Untrack(o)` from its clear
hook. v0.3 already wires this in for tuples, lists, dicts, sets,
generators. v0.10 extends to:

- frames (`objects.Frame`),
- coroutines / async generators,
- code objects (don't track; they have no cycle path),
- bound methods,
- partial / weakref proxy objects.

The collector visits an object's references through a per-type
`tp_traverse` slot. v0.10 adds the slot to `objects.Type` and
populates it for every tracked type. CPython: `Include/object.h:339
tp_traverse`.

## Generation lists

CPython uses three generations (`young`, `old`, `permanent`) plus a
freeze list. Each generation has a count; the collector runs
generation `n` when `count[n] > threshold[n]`. Defaults are 700 / 10 /
10. We mirror these and the same per-generation linked list layout.

CPython: `Include/internal/pycore_gc.h:122 GCState`,
`Modules/gcmodule.c gc_collect_generations`.

## Cycle algorithm (port of `gc_collect_main`)

1. `update_refs`: for each object in the candidate generation, copy
   its refcount-equivalent into `gc_refs`.
2. `subtract_refs`: for each object, walk `tp_traverse` and decrement
   `gc_refs` for every reference into the candidate set.
3. After the walk, any object whose `gc_refs` is zero is unreachable
   *unless* it is referenced from a reachable object. `move_unreachable`
   does a second pass to find the closure of reachable objects and
   moves the rest to an `unreachable` list.
4. `move_legacy_finalizers` separates objects that have legacy
   `__del__` finalizers; their dependencies are pulled back into
   reachable to preserve resurrection invariants.
5. `handle_weakrefs` clears every weakref pointing into the
   unreachable set and queues their callbacks.
6. `finalize_garbage` runs `tp_finalize` on each unreachable object.
7. After finalizers, anything still unreachable is cleared via
   `tp_clear` so Go's GC can reclaim the memory.

Refcounts: gopy doesn't keep one. `gc_refs` is computed fresh by
counting incoming edges from inside the candidate set. A node is
unreachable iff after `subtract_refs` its `gc_refs` is zero *and* no
visit_reachable walk pulls it back. This matches CPython's algorithm
without needing the runtime refcount field.

## Weakrefs (`objects/weakref.go`)

CPython: `Objects/weakrefobject.c` ports verbatim to `objects/weakref.go`.
Three observable types: `weakref.ref`, `weakref.proxy`,
`weakref.ReferenceType`. Each tracked object has an optional pointer
to a singly-linked list of weakrefs in its header; the GC walks this
list during `handle_weakrefs`.

The list head goes on `objects.Header` as a new optional field. Types
that opt into weakref support set a flag in `tp_flags`. CPython:
`Include/cpython/object.h:235 tp_weaklistoffset`.

Callbacks: a weakref with a callback survives object death long enough
to fire the callback once on a clean Python frame. CPython queues
these on `tstate.async_exc`; we use a per-thread channel.

## Module registration (`gc/module.go`)

Built-in `gc` module exposes:

| Python                  | Go                          | CPython entry                     |
|-------------------------|-----------------------------|-----------------------------------|
| `gc.collect([gen])`     | `Collect(gen int) int`      | `Modules/gcmodule.c gc_collect`   |
| `gc.enable()`           | `Enable()`                  | `gc.c PyGC_Enable`                |
| `gc.disable()`          | `Disable()`                 | `gc.c PyGC_Disable`               |
| `gc.isenabled()`        | `IsEnabled() bool`          | `gc.c PyGC_IsEnabled`             |
| `gc.get_threshold()`    | `GetThreshold() (int,int,int)` | `gcmodule.c gc_get_threshold`  |
| `gc.set_threshold(...)` | `SetThreshold(int,int,int)` | `gcmodule.c gc_set_threshold`     |
| `gc.get_count()`        | `GetCount() (int,int,int)`  | `gcmodule.c gc_get_count`         |
| `gc.get_objects([gen])` | `GetObjects(gen int) []Object` | `gc.c _PyGC_GetObjects`        |
| `gc.is_tracked(o)`      | `IsTracked(o Object) bool`  | (already in `gc.go`)              |
| `gc.freeze()` / `unfreeze()` / `get_freeze_count()` | `Freeze()` / `Unfreeze()` / `GetFreezeCount() int` | `gc.c _PyGC_Freeze`        |
| `gc.get_referrers(*objs)` | `GetReferrers(...Object) []Object` | `gc.c _PyGC_GetReferrers` |
| `gc.get_referents(*objs)` | `GetReferents(...Object) []Object` | `gcmodule.c gc_get_referents` |

Callbacks (`gc.callbacks` list) and stats (`gc.set_debug`, `gc.get_stats`)
land in v0.10 if they fit; otherwise v0.10.x.

## v0.10 checklist (1613-A through Q)

- [x] **1613-A** `gc/state.go`: GCState struct, three generation lists,
      thresholds, enabled flag, mu lock.
- [x] **1613-B** `gc/list.go`: gc_list_init / append / remove / move /
      merge / size / clear_collecting.
- [x] **1613-C** `gc/objstack.go`: `_PyObjectStack` helper.
- [~] **1613-D** `gc/gil.go`: collector entry/exit guards. CPython
      gc_gil.c reduces to `_PyGC_ClearAllFreeLists` against the
      per-type freelists; gopy has no freelists, so the port is a
      documented no-op (1613-O).
- [~] **1613-E** `Type.TpTraverse` slot + per-type callbacks. Slot
      shipped on `objects/type.go`; impls live for tuple, list, dict,
      odict, set, frozenset. Frame, generator, coroutine, async_gen,
      bound method, cell tracked separately as 1613-N.
- [x] **1613-F** `gc/refs.go`: update_refs, subtract_refs.
- [x] **1613-G** `gc/reachable.go`: move_unreachable, visit_reachable,
      clear_unreachable_mask, untrack_tuples.
- [x] **1613-H** `objects/weakref.go`: PyWeakref types, header slot,
      _PyWeakref_ClearWeakRefsExceptCallbacks.
- [x] **1613-I** `gc/weakref.go`: handle_weakrefs + callback drain.
- [~] **1613-J** `gc/finalize.go`: finalize_garbage shipped via PEP 442
      `Type.Finalize`. Pre-PEP-442 `__del__` and `gc.garbage`
      population for resurrected cycles tracked separately as 1613-P.
- [x] **1613-K** `gc/collector.go`: gc_collect_main, gc_select_generation.
- [x] **1613-L** `gc/module.go`: 18 callables (collect, enable,
      disable, isenabled, get_threshold, set_threshold, get_count,
      is_tracked, get_objects, get_referrers, get_referents, freeze,
      unfreeze, get_freeze_count, set_debug, get_debug, get_stats,
      is_finalized) registered via inittab.
- [x] **1613-M** `gc/cycle_test.go` plus the per-component test files.

Beyond the original A through M, these landed during v0.10.x:
- [x] **set_debug / get_debug** with DEBUG_* flag constants.
- [x] **gc.callbacks** invoked before and after collection.
- [x] **gc.get_stats** per-generation counters.
- [x] **gc.is_finalized** lookup.
- [x] **weakref.proxy** + CallableProxyType.
- [x] **Type.Finalize** wired through tp_finalize and the GC table.
- [x] **gc.get_referrers / gc.get_referents**.
- [x] **gc.freeze / unfreeze / get_freeze_count**.

Remaining work after v0.10.x:
- [x] **1613-N** `objects/Type.TpTraverse` impls for frame, generator,
      coroutine, async_generator (+ ASend / AThrow), bound method,
      cell. Mirrors Objects/frameobject.c frame_traverse,
      Objects/genobject.c gen_traverse, Objects/cellobject.c
      cell_traverse, Objects/classobject.c method_traverse. Note that
      Generator / Coroutine / AsyncGenerator carry no Object fields
      directly (the suspended frame lives on the body goroutine), so
      only the wrapper types (coro_wrapper, async_gen_asend,
      async_gen_athrow) get traverse impls.
- [x] **1613-O** `gc/gil.go`: stub `ClearAllFreeLists` documenting
      the no-op parity with gc_gil.c so future readers know why the
      collector skips the call.
- [x] **1613-P** populate `gc.garbage` when a finalizer resurrects an
      object or when a cycle stays alive after finalize_garbage; honor
      DEBUG_SAVEALL by appending collectable objects too. Resurrection
      detection in `gc/finalize.go:handleResurrected` re-runs deduce
      on the post-finalize list and pulls survivors back to the
      destination generation; DEBUG_SAVEALL appends the still-dead set
      to the shared gc.garbage list (`gc/collector.go:appendGarbage`).
      Mirrors gc.c:1261 handle_resurrected_objects + gc.c:1142
      delete_garbage SAVEALL branch.
- [x] **1613-Q** `weakref/` package: ports the Lib/_weakrefset.py and
      Lib/weakref.py collection classes (WeakSet,
      WeakValueDictionary, WeakKeyDictionary) as Go types layered on
      objects.Weakref. Each container's `_remove` callback is an
      objects.BuiltinFunction whose closure deletes the dead weakref's
      entry; gc.RegisterWeakref wires the callback to the cycle
      collector's handle_weakrefs path. Outstanding follow-up
      (1613-S): the closure captures the container strongly, leaking
      empty containers until items die; mirroring CPython's
      `selfref = ref(self)` trick needs a TpTraverse-aware closure
      shape.

## v0.10 release gate

`gc.collect()` reclaims a deliberately constructed reference cycle.
`weakref.ref(target)` returns `None` after the target is collected.
A class with `__del__` is finalized exactly once when its instance
becomes unreachable through a cycle. The CPython `test_gc` smoke
fixtures (subset; full suite needs the type system port) pass.

## Out of scope for v0.10 (deferred to v0.10.x or v0.11)

- Free-threaded build's separate collector path (`gc_free_threading.c`).
- `gc.callbacks` user hooks.
- `gc.set_debug` debug flags.
- `tracemalloc` integration (own spec at 1666).
- Biased reference counting (own spec at 1614, post v0.10).

## Open design questions

1. **gc_refs without refcounts**: confirmed approach is to count
   in-edges from the candidate set rather than copy `ob_refcnt`. The
   per-object `gc_refs` field lives on `objects.Header` only during a
   collection pass; cleared on entry, scratch on exit. Memory cost: 8
   bytes per tracked object during collection only (zero between).
2. **Weakref backref**: do we put the weaklist head on every
   `objects.Header`, or only on types that opt in via `tp_flags`?
   Decision: opt-in via flag, matching CPython's `tp_weaklistoffset`
   model. Saves one word per non-weakreffable object.
3. **Finalizer queue under goroutine yield**: `tp_finalize` runs
   Python code that may yield to other goroutines; we must hold the
   collection lock across the queue drain to avoid a second collector
   pass observing partially-finalized objects. Detail in 1613-J.
