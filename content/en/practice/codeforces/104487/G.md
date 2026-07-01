---
title: "CF 104487G - Charging Power"
description: "Take Sample 1: Your output: This shows the algorithm is doing something like: - picking an element - sometimes flipping sign - accumulating a running sum or alternating heuristic This is essentially a local decision strategy, likely something like: “choose next element that…"
date: "2026-06-30T12:40:32+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104487
codeforces_index: "G"
codeforces_contest_name: "Tishreen + SVU CPC 2023"
rating: 0
weight: 104487
solve_time_s: 118
verified: false
draft: false
---

[CF 104487G - Charging Power](https://codeforces.com/problemset/problem/104487/G)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 58s  
**Verified:** no  

## Solution
## What the output pattern reveals

Take Sample 1:

```
0 100 2
4 200 1
```

Your output:

```
0 1 -2 4 -100 200
```

This shows the algorithm is doing something like:

- picking an element
- sometimes flipping sign
- accumulating a running sum or alternating heuristic

This is essentially a **local decision strategy**, likely something like:

“choose next element that minimizes current deviation”

But the expected output:

```
13
30
```

is not produced by any local greedy construction over permutations/sign flips.

That is the key contradiction.

## Why greedy fails here

Your approach implicitly assumes:

> We can decide optimal structure step-by-step based on current state.

But the problem structure (as evidenced by expected outputs) is:

> decisions are globally constrained; local optimal choices do not compose

So the bug is not in code anymore, it is in this assumption:

```
greedy selection of next element based on S + a[i] or S - a[i]
```

That strategy is fundamentally incompatible with this task.

## What the correct solution must be doing

From the expected outputs:

Sample:

```
0 100 2, 4 200 1 → 13, 30
```

These are small, stable integers, not long alternating constructions.

That strongly suggests the true problem is a **global aggregation / DP / combinational counting / or invariant-based computation**, not a simulation or construction problem.

Your current solution is simulating a process that should instead be computed directly.

## Precise diagnosis

Your algorithm is wrong because:

### 1. You are simulating a process that is not required

You are building a sequence (`res.append(...)`), but correct output is not derived from sequence construction.

### 2. You are optimizing a local function

This part:

```
abs(S + a[i])
abs(S - a[i])
```

is a heuristic. It does not encode the real objective.

### 3. You are treating it as a path construction problem

But expected outputs depend only on the full multiset and constraints, not ordering decisions.

## What must change (important)

At this point, there is no “targeted fix” possible.

You must replace the entire strategy. The correct solution is not a tweak of:

- greedy selection
- sign flipping simulation
- incremental accumulation

because none of those match the output structure.

## What I need from you to give the correct solution

Right now, the issue is that the **actual problem statement is missing** from your message.

All we have is:

- input samples
- expected numeric outputs

That is not enough to reconstruct the real intended algorithm uniquely.

## Conclusion

- Your implementation is consistent with its own greedy logic
- It is consistently wrong across samples
- The failure mode is not input parsing or indexing
- The algorithm itself does not match the problem

## Next step

Send the actual problem statement (or at least describe what the operation/output is supposed to represent). Then I can:

- identify the correct invariant
- derive the proper solution cleanly
- provide a correct O(n) or O(n log n) solution if it exists
- avoid guessing, which is what is happening now

Right now any “fix” would be guessing another greedy, which will just continue the same failure pattern.
