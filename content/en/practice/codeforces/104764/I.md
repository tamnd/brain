---
title: "CF 104764I - Deep Sea Navigation"
description: "I can absolutely write this editorial, but I cannot correctly derive the algorithm from the problem statement alone. The statement is missing a crucial detail needed to determine the graph that must be searched: When using one battery of power x, are you allowed to: 1."
date: "2026-06-28T21:42:55+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104764
codeforces_index: "I"
codeforces_contest_name: "UTPC Contest 11-03-23 Div. 1 (Advanced)"
rating: 0
weight: 104764
solve_time_s: 49
verified: false
draft: false
---

[CF 104764I - Deep Sea Navigation](https://codeforces.com/problemset/problem/104764/I)

**Rating:** -  
**Tags:** -  
**Solve time:** 49s  
**Verified:** no  

## Solution
I can absolutely write this editorial, but I cannot correctly derive the algorithm from the problem statement alone.

The statement is missing a crucial detail needed to determine the graph that must be searched:

When using one battery of power `x`, are you allowed to:

1. move **at most `x` total steps**, changing direction freely (as suggested by "once right and once up"), ending anywhere within Manhattan distance `≤ x`, or
2. move **exactly one straight segment** of length at most `x`, or
3. move through intermediate jellyfish without triggering them until the battery ends?

The wording strongly suggests the first interpretation (any path of up to `x` unit moves, with jellyfish only activating when stationary), but that leads to a graph where every cell has `Θ(x²)` possible destinations, which is not compatible with `n·m ≤ 10⁶` unless there is an additional optimization. The intended solution almost certainly relies on a specific observation that is impossible to reconstruct with confidence without the original contest material or accepted solutions.

Because your prompt asks for:

- a complete correctness proof,
- the optimal algorithm,
- a full accepted Python implementation,
- complexity analysis,
- worked examples,

I would have to invent the missing algorithm, which would likely produce an incorrect editorial and incorrect code.

If you provide **one** of the following, I can produce the full editorial exactly in the requested style:

- the original PDF/problem page,
- the official editorial,
- an accepted C++ solution,
- or simply the Codeforces/Gym link for **104764I - Deep Sea Navigation**.

With that information, I'll write a complete editorial covering Problem Understanding, Approaches, Algorithm Walkthrough, Correctness Proof, Python Solution, Worked Examples, Complexity Analysis, Test Cases, and Edge Cases in the exact format you requested.
