---
title: "Swift consuming / borrowing / inout & Noncopyable Types"
description: "Swift 6.x has shipped a complete move-only/noncopyable system layered on top of ARC. Parameter conventions are explicit; the law of exclusivity (Swift's variant from 2017) supplies the static aliasing discipline."
tags: ["memory-safety", "ownership"]
weight: 80
date: 2026-05-18T17:00:00+07:00
---

## §1 Provenance

- **Vendor**: Apple. Swift Evolution.
- **Foundational law**: SE-0176 *Enforce Exclusive Access to Memory* (Swift 5, 2017–2018).
- **Parameter modifiers**: SE-0377 *borrowing / consuming parameter ownership modifiers*, https://github.com/swiftlang/swift-evolution/blob/main/proposals/0377-parameter-ownership-modifiers.md .
- **Noncopyable foundation**: SE-0390 *Noncopyable structs and enums*, https://github.com/swiftlang/swift-evolution/blob/main/proposals/0390-noncopyable-structs-and-enums.md .
- **Generics**: SE-0427 *Noncopyable Generics*, https://github.com/swiftlang/swift-evolution/blob/main/proposals/0427-noncopyable-generics.md .
- **Pattern matching**: SE-0432 *Borrowing/consuming pattern matching for noncopyable types*.
- **Std lib primitives**: SE-0437.
- **2026 review item**: SE-0528 *Noncopyable Continuation*, https://github.com/swiftlang/swift-evolution/blob/main/proposals/0528-noncopyable-continuation.md .
- **Hacking with Swift summary**: https://www.hackingwithswift.com/swift/6.0/noncopyable-upgrades .

## §2 Core type discipline

Two axes:

1. **Copyability** of a type, controlled by conformance to the `Copyable` protocol. By default every Swift type conforms; opt out with `~Copyable`. A noncopyable value has unique identity and can carry a `deinit`.
2. **Parameter convention**, written as a keyword on the parameter type:
   - `borrowing T` — shared read; callee must not consume.
   - `inout T` — exclusive write; the caller's storage is mutated.
   - `consuming T` — caller transfers ownership; binding dies after the call.
   - (default for `Copyable` types: copy-in by value.)

Judgement form: SE-0176's law of exclusivity says every memory access has a duration; for that duration, no overlapping conflicting access (read+write or two writes) is permitted. For copyable types this is checked statically where possible, falls back to dynamic checks where not. For noncopyable types, the check is fully static; the rules of SE-0390 collapse with the law of exclusivity to give Rust-equivalent guarantees on those values.

Principal example — a file handle modelled as noncopyable:

```swift
struct FileHandle: ~Copyable {
    private var fd: CInt
    deinit { close(fd) }
    consuming func releaseFD() -> CInt {
        let v = fd; discard self; return v
    }
    borrowing func read(into buf: inout [UInt8]) { ... }
}
```

`consuming` methods consume `self`; `borrowing` methods share; `inout` methods take exclusive write of `self`. The compiler enforces a single owner per handle, double-close is impossible.

## §3 Memory-safety invariant

For noncopyable values:

- **No double-free** (deinit runs exactly once on a unique value).
- **No use-after-free** (consume invalidates the binding statically).
- **No data race on the value** (no shared mutable access).
- **Protocol safety**: state-machine-typed APIs (closed/open file, etc.).

For copyable values: ARC continues to do its job; the law of exclusivity prevents `inout` overlap. UAF on classes still requires `weak`/`unowned`.

## §4 Compiler implementation cost

- Swift's borrow checker is built on the existing SIL (Swift Intermediate Language) ownership SSA, which has carried `@owned`/`@guaranteed` since 2018. SE-0377 / SE-0390 add a surface-language exposure of pre-existing machinery, so the *compiler* cost was incremental.
- Error messages benefit from a decade of Swift compiler investment. Suggestions are concrete ("did you mean to mark this as `consuming`?").
- The big cost is **library migration**: every container type in the std lib has had to grow noncopyable variants (SE-0437 onwards). The migration spans Swift 6.0 → 6.x.

## §5 Production / language adoption status (May 2026)

- Swift 6.0 (Sep 2024) shipped SE-0390, SE-0377, SE-0427, SE-0432.
- Swift 6.1, 6.2 fold in SE-0437, SE-0429 partial consumption, and additional std-lib noncopyable primitives.
- SE-0528 (noncopyable continuations) is in active review during 2026.
- Apple SDK adoption: file handles, concurrency primitives, low-level IO types are being rewritten as noncopyable.
- Cross-platform Swift (Linux, Windows) ships the same compiler.
- Adoption pattern: incremental — old copyable code still works; new high-stakes APIs declare `~Copyable`.

## §6 Mochi adaptation note

Swift's design is the **most-adoption-friendly** model in this survey: pre-existing language remains correct; opt-in keywords add static guarantees. That is exactly Mochi's preferred adoption story (MEP-15 was structured the same way).

Pieces that map cleanly:

- **`borrowing` / `consuming` / `inout` parameter conventions** — verbatim. Same three keywords, same call-site implicitness, same rule that the convention is part of the function type but not the variable type.
- **`~Copyable` types** — Mochi could expose this as `nocopy struct File { … }` or `linear struct File { … }`. The check is the same as Austral's linear universe: bindings of nocopy type must be threaded through one consuming use per path. The runtime continues to copy handle Cells (a handle is 8 bytes, copy is unavoidable), but the *type checker* prevents the user-visible second use.
- **deinit on nocopy types** — already implementable: when the binding is consumed (last use), the VM calls the user's `dispose` function with the handle just before bumping `gen`.

Incompatible:

- The whole ARC interaction. Mochi is GC'd; there is no retain/release to expose.
- The dynamic exclusivity-check fallback. Mochi's bytecode does not have the SSA shape Swift needs.

Surface-syntax change MEP-41 should adopt: the keyword triple `borrowing` / `consuming` / `inout` on parameter types, and a `nocopy` (or `~Copyable`-style) modifier on `struct` declarations. The check is local and small. Diagnostic quality should be good because we are mirroring Swift's accepted vocabulary.

vm3 tie-in: a `nocopy` type's handle, when consumed, leads the VM to emit a `KILL_HANDLE` opcode that zeroes the source slot **and** bumps the gen on the slab entry one extra time so any stray copy of the Cell traps on next use. The 12-bit gen field already exists.

MEP-15 tie-in: a `consuming` parameter is an effect on the caller's binding. The effect set could grow `move: P` per consumed parameter; useful for purity diagnostics.

MEP-16 tie-in: `consuming` on `Option<T>` desugars to `take` and produces `T`. A `borrowing Option<T>` can be narrowed via `if let` without copying.

## §7 Open questions for MEP-41

1. Should Mochi's keyword be `nocopy` or `~Copyable`? Mochi's surface tends to spell out words, so `nocopy struct …` is the better fit.
2. Does Mochi need a `Copyable` protocol at all, or is the modifier sufficient?
3. How do generics interact with `nocopy`? Swift took two proposals (SE-0390 → SE-0427) to get this right; Mochi can learn from the staging.
4. Does the JIT (MEP-39) need special handling of `KILL_HANDLE`, or can it treat it as a normal store?

Sources: SE-0177, SE-0390, SE-0427, SE-0432, SE-0437, SE-0528 (links above); https://www.hackingwithswift.com/swift/6.0/noncopyable-upgrades .