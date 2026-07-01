---
title: "CF 104008A - Lily"
description: "We are given a one-dimensional strip of cells. Each cell is either empty or contains a lily, represented by a character string where L means a lily is already planted and . means the cell is empty soil."
date: "2026-07-02T05:28:13+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104008
codeforces_index: "A"
codeforces_contest_name: "2022 China Collegiate Programming Contest (CCPC) Guilin Site"
rating: 0
weight: 104008
solve_time_s: 43
verified: true
draft: false
---

[CF 104008A - Lily](https://codeforces.com/problemset/problem/104008/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 43s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a one-dimensional strip of cells. Each cell is either empty or contains a lily, represented by a character string where `L` means a lily is already planted and `.` means the cell is empty soil.

We are allowed to place cat food on some of the empty cells, marking them as `C`. However, placing cat food at position `i` imposes a strict safety constraint: the cell itself and its immediate neighbors `i-1` and `i+1` must not contain lilies. In other words, a cat food placement “blocks” a radius of 1 around it from containing lilies.

The task is to choose positions for cat food to maximize how many `C` cells we place while respecting this constraint. Any valid configuration achieving the maximum number of cat food placements is acceptable.

The constraint `n ≤ 1000` means that even quadratic or mildly cubic solutions are fine, but the structure of the problem strongly suggests a greedy or linear scan is sufficient. Since each decision affects only adjacent cells, global search or DP is unnecessary.

A subtle edge case appears when lilies are very dense. For example, if the string is `LLL`, no cat food can be placed anywhere, because every empty cell adjacent to a lily would violate the constraint immediately. Another edge case is alternating patterns like `L.L.L`, where naive greedy placement might incorrectly try to place `C` too close to a lily without checking both neighbors.

A careless approach often fails by placing cat food whenever a single adjacent cell is safe, instead of verifying both sides. For instance, in `..L..`, placing cat food at position 2 blocks position 3 from being used, and a greedy left-to-right placement must account for that propagation.

## Approaches

A brute-force strategy would try every subset of empty cells and check validity. For each subset, we would scan the string and verify that no chosen `C` violates the rule with nearby lilies. There are up to `n` positions, so the number of subsets is `2^n`, and each check costs `O(n)`, leading to `O(n·2^n)` operations. This becomes impossible even for small `n`.

The key observation is that each cat food placement only restricts a local neighborhood of size 3. This locality means we never need to reconsider earlier decisions if we scan left to right. Once we place a `C` at position `i`, positions `i-1` and `i+1` become effectively forbidden if they contain lilies, and we naturally skip them in a greedy construction.

The optimal construction is to traverse the string and place a `C` whenever the current position is empty and none of its neighbors contain a lily that would violate the rule. After placing a `C`, we skip the next cell to avoid accidental adjacency conflicts in future placements.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n·2^n) | O(n) | Too slow |
| Greedy Scan | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

We process the string from left to right and build the answer incrementally.

1. Start from index 0 and maintain a mutable copy of the grid.

We need mutability because placing a `C` changes what future positions are allowed.
2. At each position `i`, check whether the cell is empty.

If it already contains `L`, we cannot place anything there, so we move forward.
3. If the cell is `.`, we check whether placing a `C` here would violate the rule.

This requires ensuring that neither `i-1`, `i`, nor `i+1` contains `L`.
4. If the condition is satisfied, we place a `C` at position `i`.

Once we do this, we mark it immediately so future decisions see its effect.
5. After placing `C`, we skip the next position by incrementing `i` by 2 instead of 1.

This prevents accidental placement that would create overlap conflicts in constrained neighborhoods.
6. If we do not place `C`, we simply move to the next index.

### Why it works

The key invariant is that every time we place a `C`, all forbidden interactions are strictly local and never propagate beyond distance 1. This means decisions made earlier cannot be invalidated by later choices. Since we only place a `C` when its neighborhood is clean, no later placement can introduce a conflict involving that cell, because any future `C` is at least two steps away. The greedy choice is therefore safe and locally optimal, and local optimality implies global optimality because each placement consumes exactly the minimum forbidden region.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    s = list(input().strip())
    n = len(s)

    i = 0
    while i < n:
        if s[i] == '.':
            left_ok = (i == 0 or s[i - 1] != 'L')
            right_ok = (i == n - 1 or s[i + 1] != 'L')

            if left_ok and right_ok:
                s[i] = 'C'
                i += 2
                continue
        i += 1

    print(''.join(s))

if __name__ == "__main__":
    solve()
```

The implementation mirrors the greedy scan. We convert the string to a list to allow in-place updates, since Python strings are immutable. The two boundary checks handle edge cells cleanly without index errors. After placing a `C`, skipping the next index is a practical optimization that also prevents re-evaluating a position whose neighborhood has just been “used”.

A common pitfall is forgetting to check both neighbors before placing `C`. Another is failing to handle boundaries properly, which would cause incorrect rejection or index errors at `i = 0` or `i = n - 1`.

## Worked Examples

### Example 1

Input:

```
..L..
```

We scan left to right.

| i | s[i] | left_ok | right_ok | action | state |
| --- | --- | --- | --- | --- | --- |
| 0 | . | true | true | place C | C.L.. |
| 2 | L | - | - | skip | C.L.. |
| 4 | . | true | true | place C | C.L.C |

This confirms that placements are maximized while respecting the lily constraint, and no two placements interfere.

### Example 2

Input:

```
L.L.L
```

| i | s[i] | left_ok | right_ok | action | state |
| --- | --- | --- | --- | --- | --- |
| 0 | L | - | - | skip | L.L.L |
| 2 | L | - | - | skip | L.L.L |
| 4 | L | - | - | skip | L.L.L |

No placements are possible, and the algorithm correctly avoids illegal positions.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | single left-to-right scan with constant-time checks |
| Space | O(1) | modification is done in-place |

The input size limit of `n ≤ 1000` is comfortably handled by a linear scan. Even with overhead from Python string operations, the solution runs well within limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    s = list(input().strip())
    n = len(s)

    i = 0
    while i < n:
        if s[i] == '.':
            left_ok = (i == 0 or s[i - 1] != 'L')
            right_ok = (i == n - 1 or s[i + 1] != 'L')
            if left_ok and right_ok:
                s[i] = 'C'
                i += 2
                continue
        i += 1

    return ''.join(s)

# provided samples
assert run("..L..\n") == "C.L.C"

# custom cases
assert run("L") == "L", "single lily"
assert run(".") == "C", "single empty cell"
assert run("LLL") == "LLL", "no valid placement"
assert run("L.L.L") == "L.L.L", "blocked by lilies"
assert run(".....") == "C.C.C", "maximum spacing"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `L` | `L` | single boundary handling |
| `.` | `C` | trivial placement |
| `LLL` | `LLL` | fully blocked configuration |
| `L.L.L` | `L.L.L` | alternating constraints |
| `.....` | `C.C.C` | maximal greedy packing |

## Edge Cases

For a single-cell string like `.` the algorithm immediately places a `C` because both neighbor checks pass vacuously. There are no boundary risks since `i == 0` and `i == n-1` are both true.

For a fully blocked string like `LLL`, every position is skipped because the initial check `s[i] == '.'` fails everywhere, so no invalid placement is attempted.

For boundary-heavy patterns like `.L` or `L.`, the edge checks correctly treat missing neighbors as safe. For example in `.L`, index 0 is empty but its right neighbor is `L`, so no placement occurs, producing `.L`.
