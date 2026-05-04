---


title: "Chapter 4. Equality and Rewriting"
description: "This chapter isolates the operational core of reasoning in Type Theory as implemented by Lean: equality and its use as a transport mechanism."
tags: ["lean", "proof-assistant", "type-theory"]
weight: 4000
date: 2026-05-04T22:58:55+07:00
---

# Chapter 4. Equality and Rewriting

This chapter isolates the operational core of reasoning in Type Theory as implemented by Lean: equality and its use as a transport mechanism. Most nontrivial proofs in Lean reduce to a controlled sequence of rewrites. The objective here is to make rewriting predictable, terminating, and compositional.

Lean exposes two layers of equality. *Definitional equality* is handled by the kernel through computation. Expressions that reduce to the same normal form are treated as equal without requiring proof. This includes beta reduction, delta unfolding, and other normalization steps. You do not invoke it directly; you design definitions so that it fires where you need it. In contrast, *propositional equality* is an explicit value of type `a = b`. It must be constructed and then consumed by rewriting. The boundary between these two layers determines when `rfl` succeeds and when a proof term is required.

The primitive proof of equality is `rfl`. It closes goals where both sides are definitionally equal after normalization. From this base, the system builds congruence, symmetry, and transitivity. Congruence lifts equality through contexts such as function application. Symmetry and transitivity allow you to orient and compose equalities. The chapter shows how these principles appear in practice through rewriting tactics and through term-level combinators.

Rewriting is the act of replacing one expression with another using a proof of equality. In tactic mode, `rw` applies a lemma in a chosen direction and location. In term mode, the same effect is achieved by applying transport along equality. The direction matters: many goals require the inverse orientation of a lemma. The chapter emphasizes explicit control of direction, scope, and order of rewrites, since uncontrolled rewriting leads to divergence or loss of structure.

A central tool is `simp`, a normalization engine built on a curated set of rewrite rules. Unlike `rw`, which performs a single directed step, `simp` performs repeated rewriting until no rule applies. Its behavior depends entirely on the simp set. The chapter develops criteria for good simp lemmas: left-hand sides that strictly decrease a measure, right-hand sides in canonical form, and absence of overlapping rules that create loops. You will see how to register, localize, and audit simp rules so that normalization remains fast and terminating.

Rewriting under binders introduces dependence. When variables appear in types, replacing a term can change the type of subsequent expressions. Lean supports dependent rewriting through specialized combinators and tactics that respect binders. The chapter shows how to move equalities across lambdas, quantifiers, and structures without breaking typing, and how to diagnose failures that arise from hidden dependencies.

Transport is the general mechanism behind rewriting. Given `h : a = b`, you can move data or proofs indexed by `a` to ones indexed by `b`. In simple cases this appears as substitution. In dependent settings it becomes explicit transport across families. Understanding this mechanism clarifies why some rewrites require auxiliary lemmas and why others are automatic.

Function equality is treated via extensionality. Two functions are equal when they agree on all inputs. Lean provides extensionality lemmas that reduce function equality to pointwise goals. This reduction is often necessary before rewriting can proceed, since rewriting acts on concrete applications rather than abstract functions.

The chapter also addresses heterogeneous equality, which relates terms whose types differ but are connected by an equality of indices. While less common in routine proofs, it appears in dependent developments and in low-level manipulations. The practical guidance is to avoid it when a homogeneous formulation is available, and to use standard bridges when it is not.

Throughout, the focus is on building a stable rewrite system for your development. You will learn to choose canonical forms, orient lemmas consistently, and separate local rewrites from global normalization. The result is a proof style where most steps are mechanical, failures are localized, and large proofs remain maintainable.
