---
title: "CF 105761C - Soccer Standing Table"
description: "We are given five integers that describe a soccer team’s season statistics, but the order of these integers is scrambled. We know they correspond to matches played, wins, draws, losses, and total points, but we do not know which number is which."
date: "2026-06-21T23:50:58+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105761
codeforces_index: "C"
codeforces_contest_name: "2021 UCF Local Programming Contest"
rating: 0
weight: 105761
solve_time_s: 43
verified: true
draft: false
---

[CF 105761C - Soccer Standing Table](https://codeforces.com/problemset/problem/105761/C)

**Rating:** -  
**Tags:** -  
**Solve time:** 43s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given five integers that describe a soccer team’s season statistics, but the order of these integers is scrambled. We know they correspond to matches played, wins, draws, losses, and total points, but we do not know which number is which.

The rules of soccer scoring are fixed: a win contributes 3 points, a draw contributes 1 point, and a loss contributes 0 points. Also, every match results in exactly one of these outcomes, so the total matches played is the sum of wins, draws, and losses. The total points is computed as three times wins plus draws.

The task is to take the five numbers in unknown order and reconstruct the unique valid interpretation, then print them in the canonical order: MP, W, D, L, Pts.

Even though all values are small, up to 300, the key difficulty is that we must assign roles correctly under two constraints simultaneously: a linear constraint from match counts and another from scoring. A naive attempt that assigns roles arbitrarily will fail because multiple permutations exist, but only one satisfies both equations together.

Edge cases mostly revolve around repeated values. For example, an input like `0 0 1 1 0` contains duplicates, which makes naive greedy assignment ambiguous. Another subtle case is when draws and losses or wins and draws have identical values, which can mislead a sorting-based heuristic even though the valid solution is still unique.

Since there are only five numbers, brute force over all permutations is feasible in constant time. That is the main structural observation.

## Approaches

A direct idea is to try all possible assignments of the five numbers to the roles MP, W, D, L, and Pts. For each assignment, we check whether it satisfies two conditions: first, MP must equal W + D + L, and second, Pts must equal 3W + D. If both hold, we have found the correct interpretation.

There are only five values, so the number of permutations is 5 factorial, which is 120. For each permutation we do constant work, so this approach is extremely fast.

A more “thought-based” optimization is unnecessary here because the constraints are tiny. Even if we tried to reduce it further by reasoning about which number is largest or smallest, we would still need to verify consistency, and the permutation check is already simple and safe.

The brute-force approach works because the search space is tiny and constraints fully determine a unique mapping. The observation that only 5! assignments exist reduces what looks like a reasoning problem into a straightforward validation loop.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force permutations | O(5!) | O(1) | Accepted |
| Optimal (same as brute force) | O(120) | O(1) | Accepted |

## Algorithm Walkthrough

We treat the five input numbers as a multiset and try every possible assignment to the five roles.

1. Read the five integers into an array. These represent an unknown permutation of MP, W, D, L, and Pts.
2. Generate all permutations of these five values. Each permutation corresponds to a hypothetical assignment: the first value is MP, the second W, the third D, the fourth L, and the fifth Pts. We do not assume any ordering because the input gives no hints.
3. For each permutation, compute whether it satisfies the structural constraints of soccer statistics. We check two equations: MP must equal W + D + L, and Pts must equal 3W + D. This step is the only filtering condition, and it enforces the rules of the scoring system.
4. The problem guarantees exactly one valid assignment exists, so as soon as we find a permutation that satisfies both conditions, we output it in the required order and terminate.

The reason this is sufficient is that the constraints fully define the system. Any incorrect assignment will violate at least one equation, so it cannot pass the check.

### Why it works

Every valid soccer table row is fully determined by the two equations MP = W + D + L and Pts = 3W + D. Since we are testing all possible assignments of the input numbers into these roles, the correct configuration must appear among the permutations. The uniqueness guarantee ensures that no other permutation can satisfy both constraints simultaneously, so the first valid match we find is the only answer.

## Python Solution

```python
import sys
input = sys.stdin.readline

from itertools import permutations

nums = list(map(int, input().split()))

for mp, w, d, l, pts in permutations(nums):
    if mp == w + d + l and pts == 3 * w + d:
        print(mp, w, d, l, pts)
        break
```

The solution directly encodes the idea of exhaustive assignment checking. We rely on Python’s `itertools.permutations` to enumerate all possible role assignments.

The key detail is that we do not attempt to optimize selection order or prune aggressively. With only 120 cases, overhead is negligible. The early break ensures we stop immediately once the valid configuration is found, which aligns with the uniqueness guarantee.

One subtle point is that we treat all permutations equally, even when values repeat. This is fine because correctness depends on value assignment, not index identity. Duplicate values may produce duplicate permutations, but they do not affect correctness or performance in any meaningful way.

## Worked Examples

### Example 1

Input:

`19 11 2 4 5`

We test permutations until we find a valid mapping.

| MP | W | D | L | Pts | MP check | Pts check |
| --- | --- | --- | --- | --- | --- | --- |
| 11 | 5 | 4 | 2 | 19 | 11 ≠ 11 | 19 = 19  |

Here, MP = 11, W = 5, D = 4, L = 2, Pts = 19.

We verify MP = W + D + L → 11 = 5 + 4 + 2 = 11 and Pts = 3W + D → 19 = 15 + 4 = 19.

This confirms the correct assignment is found.

### Example 2

Input:

`0 0 1 1 0`

One valid permutation is:

| MP | W | D | L | Pts | MP check | Pts check |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | 0 | 0 | 1 | 0 | 1 = 1  | 0 = 0  |

Here MP = 1, W = 0, D = 0, L = 1, Pts = 0 satisfies both constraints exactly.

This case shows why duplicate values matter: multiple permutations exist, but only one satisfies both equations simultaneously.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(5!) | We test all permutations of five elements, each check is O(1) |
| Space | O(1) | Only constant extra variables beyond input storage |

The input size is fixed at five integers, so even a brute-force enumeration is effectively instantaneous. The solution easily fits within any time limit constraints.

## Test Cases

```python
import sys, io
from itertools import permutations

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    nums = list(map(int, sys.stdin.readline().split()))
    for mp, w, d, l, pts in permutations(nums):
        if mp == w + d + l and pts == 3 * w + d:
            return f"{mp} {w} {d} {l} {pts}"
    return ""

# provided samples
assert run("19 11 2 4 5") == "11 5 4 2 19"
assert run("2 2 6 20 10") == "10 6 2 2 20"
assert run("0 0 1 1 0") == "1 0 0 1 0"

# custom cases
assert run("3 1 1 1 4") == "3 1 1 1 4", "simple valid case"
assert run("9 3 3 3 12") == "9 3 3 3 12", "balanced draws case"
assert run("6 2 1 3 7") == "6 2 1 3 7", "mixed ordering case"
assert run("1 0 1 0 1") == "1 0 1 0 1", "edge small values"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 3 1 1 1 4 | 3 1 1 1 4 | basic valid reconstruction |
| 9 3 3 3 12 | 9 3 3 3 12 | symmetric draw-heavy case |
| 6 2 1 3 7 | 6 2 1 3 7 | shuffled roles correctness |
| 1 0 1 0 1 | 1 0 1 0 1 | minimal edge configuration |

## Edge Cases

One important edge case is when several values are identical, which increases the number of indistinguishable permutations. For input like `0 0 1 1 0`, the algorithm still works because correctness is not tied to uniqueness of values but to satisfaction of constraints. The permutation loop will eventually try `MP=1, W=0, D=0, L=1, Pts=0`, which passes both checks, and all other permutations either violate MP consistency or scoring consistency.

Another edge case is when wins are zero. For input like `1 0 0 1 0`, the valid interpretation has no scoring contribution from wins or draws except structure. The check still succeeds because MP = 0 + 0 + 1 and Pts = 0 matches exactly.

A third edge case is when draws are zero, which collapses scoring into a pure multiple of wins. For example, if input is `6 2 0 4 6`, only the correct permutation will satisfy both MP and Pts equations simultaneously. The algorithm does not treat zero specially, it simply validates equations uniformly, which avoids any special-case bugs.
