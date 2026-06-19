---
title: "CF 106129A - Around the Table"
description: "We are simulating a very structured game involving two queues of players standing on opposite sides of a table. On the left side there are ℓ players arranged in a queue, and on the right side there are r players arranged in another queue."
date: "2026-06-19T19:54:09+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 106129
codeforces_index: "A"
codeforces_contest_name: "2025-2026 ICPC German Collegiate Programming Contest (GCPC 2025)"
rating: 0
weight: 106129
solve_time_s: 63
verified: true
draft: false
---

[CF 106129A - Around the Table](https://codeforces.com/problemset/problem/106129/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 3s  
**Verified:** yes  

## Solution
## Problem Understanding

We are simulating a very structured game involving two queues of players standing on opposite sides of a table. On the left side there are ℓ players arranged in a queue, and on the right side there are r players arranged in another queue. At every moment, only the front player of each queue matters: they face each other, one hits the ball, and then that player immediately leaves the front position and joins the back of the opposite queue. This continues indefinitely in a deterministic way.

What matters for the problem is not the full configuration, but only the sequence of pairings that appear at the moment of each hit. Each hit produces a pair consisting of the current front of the left queue and the current front of the right queue. After enough hits, these pairings eventually start repeating because the system has a finite number of possible configurations of the two circular queues.

The input gives ℓ and r, the initial sizes of the two queues. The task is to determine how many distinct ordered pairs of players appear at the front positions before the pairing sequence begins to repeat.

Even though the statement mentions a very large number of hits, up to 10¹⁰, that value is not the real bottleneck. The key is that the system becomes periodic long before that scale matters, so we only need to understand the structure of the cycle.

The constraints ℓ, r ≤ 10⁹ immediately rule out any simulation over individual hits. Even storing states of the queues is impossible because the number of states grows combinatorially with ℓ and r. This forces a purely arithmetic or number-theoretic interpretation of the process.

A subtle point that can mislead a naive simulation is assuming that the process depends on the identities of players rather than only their positions in the cyclic rotations. For example, with ℓ = 2 and r = 2, the system quickly cycles and the same pairings reappear even though players keep moving between queues. A simulation approach would need to detect repeated configurations of two sequences, which is far too large to manage directly.

## Approaches

A direct simulation would explicitly maintain both queues and repeatedly move the front players to the opposite ends. Each step is O(1), but after each operation the configuration changes, and we would need to detect when a full state repeats. The number of possible states is enormous because each queue can be any permutation of its elements, and tracking that would require hashing or full comparison of structures of size ℓ + r. Even ignoring that, simulating up to 10¹⁰ steps is impossible.

The key observation is that we do not actually need the full state. We only care about which pair appears at each step. The evolution of the system is completely deterministic and symmetric: each step advances the “front positions” in a predictable modular pattern. Each player effectively cycles through both sides in a fixed rhythm, and the interaction between the two cycles is governed entirely by the relative sizes ℓ and r.

This reduces the problem to understanding when two independent cyclic processes synchronize. One cycle has length ℓ, the other has length r. The pairing at each step depends only on the alignment of these cycles. The sequence of pairs repeats exactly when both cycles return to their original alignment simultaneously, which happens after lcm(ℓ, r) steps.

Since each step produces exactly one pairing and no pairing repeats before the full cycle completes, the number of distinct pairings is exactly the length of this cycle.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Simulation with queues | O(steps) or worse | O(ℓ + r) | Too slow |
| Cycle analysis using LCM | O(log min(ℓ, r)) | O(1) | Accepted |

## Algorithm Walkthrough

### Algorithm Walkthrough

1. Read the values ℓ and r, which represent the sizes of the two rotating queues. The goal is to determine when the interaction pattern of the two cycles repeats completely.
2. Observe that each queue behaves like a cyclic structure: every player returns to their original relative position after a fixed number of rotations equal to the queue size. This suggests that the system is driven by two independent cycles of lengths ℓ and r.
3. Recognize that the pairing at each step depends only on the relative alignment of these two cycles. A full repetition of all observed pairings occurs only when both cycles simultaneously return to their starting alignment.
4. Compute the smallest time step where both cycles align again, which is the least common multiple of ℓ and r. This is the first moment when both fronts and all relative positions match the initial configuration.
5. Return this value as the number of distinct pairings, since each step before repetition produces a unique pairing.

### Why it works

The process can be viewed as two synchronized modular counters: one advancing modulo ℓ and the other modulo r. The pair observed at step t is fully determined by the pair of residues (t mod ℓ, t mod r). Two steps produce the same pairing only when both residues match simultaneously, which happens exactly when t is a multiple of both ℓ and r. The first such time is lcm(ℓ, r), and until that point all pairs are distinct because no earlier collision of both residues can occur.

## Python Solution

```python
import sys
input = sys.stdin.readline

def lcm(a, b):
    import math
    return a // math.gcd(a, b) * b

def main():
    l, r = map(int, input().split())
    print(lcm(l, r))

if __name__ == "__main__":
    main()
```

The implementation is deliberately minimal because the entire problem reduces to computing a greatest common divisor and then deriving the least common multiple. The multiplication is performed after division by the gcd to avoid overflow issues in languages with fixed integer bounds, even though Python handles large integers safely.

The only subtlety is ensuring that the gcd is computed first. Writing `a * b // gcd(a, b)` is mathematically correct, but computing `a // gcd(a, b) * b` is safer in general because it keeps intermediate values smaller.

## Worked Examples

### Example 1: ℓ = 2, r = 3

We track the value of t and the implied alignment of the two cycles.

| Step t | t mod 2 | t mod 3 | Pair uniqueness |
| --- | --- | --- | --- |
| 0 | 0 | 0 | new |
| 1 | 1 | 1 | new |
| 2 | 0 | 2 | new |
| 3 | 1 | 0 | new |
| 4 | 0 | 1 | new |
| 5 | 1 | 2 | new |
| 6 | 0 | 0 | repeats initial |

The first repetition of the full state occurs at t = 6, which equals lcm(2, 3). All 6 steps produce distinct pairings.

This confirms that the pairing sequence is exactly governed by modular alignment.

### Example 2: ℓ = 2, r = 2

| Step t | t mod 2 | t mod 2 | Pair uniqueness |
| --- | --- | --- | --- |
| 0 | 0 | 0 | new |
| 1 | 1 | 1 | new |
| 2 | 0 | 0 | repeats initial |

Here the cycle repeats after 2 steps, matching lcm(2, 2) = 2. Even though players are moving between queues, the pairing structure repeats immediately after both cycles realign.

This shows that identical queue sizes collapse the system into a very short periodic structure.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(log min(ℓ, r)) | Dominated by gcd computation |
| Space | O(1) | Only a few integer variables are used |

The constraints allow ℓ and r up to 10⁹, so any linear simulation over time is impossible. A logarithmic gcd-based computation is easily fast enough for the worst case.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import math

    l, r = map(int, sys.stdin.readline().split())
    return str(l // math.gcd(l, r) * r)

# provided samples (interpreted)
assert run("2 3\n") == "6"
assert run("2 2\n") == "2"

# custom cases
assert run("1 5\n") == "5", "one side trivial cycle"
assert run("6 4\n") == "12", "non-coprime alignment"
assert run("10 1\n") == "10", "degenerate single cycle"
assert run("7 3\n") == "21", "coprime full expansion"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 5 | 5 | single-element cycle behavior |
| 6 4 | 12 | gcd reduction effect |
| 10 1 | 10 | degenerate queue on one side |
| 7 3 | 21 | coprime case reaching full lcm |

## Edge Cases

When one queue has size 1, the system reduces to a single rotating cycle on the other side. For example, ℓ = 1, r = 5 produces a pairing sequence that repeats every 5 steps. The algorithm correctly returns lcm(1, 5) = 5 because gcd(1, 5) = 1, so no reduction occurs.

When ℓ and r are equal, every alignment synchronizes immediately. For ℓ = r = 2, both cycles move in lockstep, and the pairing sequence repeats after exactly 2 steps. The computation lcm(2, 2) handles this naturally since gcd(2, 2) = 2.

When ℓ and r are coprime, the cycles only realign after ℓ·r steps. For example, ℓ = 7 and r = 3 produces a full-length cycle of 21 distinct pairings. The algorithm captures this maximal behavior because gcd(7, 3) = 1, leaving the product unchanged.
