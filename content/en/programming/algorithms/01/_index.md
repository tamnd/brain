---

title: "Chapter 1. Foundations"
description: "This chapter defines how you think about algorithms before you write any code."
tags: ["algorithms", "computer-science", "complexity", "foundations"]
weight: 1000
date: 2026-05-03T16:27:48+07:00
---

This chapter defines how you think about algorithms before you write any code. It establishes a small set of rules for describing problems, reasoning about correctness, and estimating cost. Every later technique relies on these rules, so the focus here stays on precision and repeatability.

An algorithm begins with a contract. You specify inputs, outputs, and constraints in a way that removes ambiguity. This includes data shape, value ranges, ordering guarantees, and failure modes. A clear contract lets you reason locally. Without it, later proofs and optimizations become fragile.

Correctness is treated as a construction, not a claim. You describe an invariant that holds at every step, and you show how each operation preserves it. For iterative algorithms, this takes the form of loop invariants. For recursive algorithms, it becomes a structural argument that each call reduces the problem while maintaining validity. These arguments should be short, mechanical, and checkable.

Cost is measured with simple models. Time complexity captures how running time grows with input size. Space complexity tracks memory usage. You use asymptotic notation to compare algorithms while ignoring constant factors, but you still record constants when they matter in practice. Lower bounds appear early because they tell you when further optimization is impossible.

The chapter also introduces baseline strategies. Brute force provides a reference implementation that is often correct and easy to test. Greedy methods make locally optimal choices and require a proof that local choices compose into a global solution. Divide and conquer splits problems into independent parts and recombines results. Dynamic programming stores intermediate results to avoid recomputation. These are not full techniques yet, but you begin to recognize when each pattern applies.

Edge cases receive explicit attention. Empty inputs, minimal sizes, duplicate values, and extreme ranges often break naive implementations. A disciplined approach treats edge cases as part of the specification, not as afterthoughts.

Testing complements reasoning. You design small cases that exercise invariants, boundary conditions, and failure paths. Random testing and adversarial inputs help reveal incorrect assumptions. A simple baseline algorithm often acts as an oracle for verification.

Finally, the chapter sets expectations for implementation. Pseudocode should reflect the invariant structure of the algorithm. Data representation choices should support the operations you need, not the other way around. Numerical limits, overflow, and precision are considered early to avoid hidden errors.

After this chapter, you should be able to take a problem, define it precisely, select a basic strategy, argue correctness with invariants, and estimate cost with a simple model. These steps form the standard workflow used in all subsequent chapters.
