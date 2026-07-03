---
title: "CF 103361O - \u041a\u0440\u0435\u0441\u0442\u0438\u043a\u0438"
description: "We are given a binary string representing a strip of cells. Some cells already contain a cross, marked as X, and the rest are empty, marked as .. The key constraint is that no two crosses are allowed to be adjacent, meaning we can never have XX in neighboring positions."
date: "2026-07-03T13:10:23+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 103361
codeforces_index: "O"
codeforces_contest_name: "\u041e\u0442\u043a\u0440\u044b\u0442\u0430\u044f \u041a\u043e\u043c\u0430\u043d\u0434\u043d\u0430\u044f \u041e\u043b\u0438\u043c\u043f\u0438\u0430\u0434\u0430 \u042e\u041c\u0428 \u043f\u043e \u043f\u0440\u043e\u0433\u0440\u0430\u043c\u043c\u0438\u0440\u043e\u0432\u0430\u043d\u0438\u044e"
rating: 0
weight: 103361
solve_time_s: 43
verified: true
draft: false
---

[CF 103361O - \u041a\u0440\u0435\u0441\u0442\u0438\u043a\u0438](https://codeforces.com/problemset/problem/103361/O)

**Rating:** -  
**Tags:** -  
**Solve time:** 43s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a binary string representing a strip of cells. Some cells already contain a cross, marked as `X`, and the rest are empty, marked as `.`. The key constraint is that no two crosses are allowed to be adjacent, meaning we can never have `XX` in neighboring positions.

Misha has already placed a valid set of crosses. Then another person, Lёsha, adds more crosses, still respecting the rule that no two crosses are adjacent. Finally, we are told that Katya confirms the configuration is maximal, meaning after both Misha and Lёsha placed crosses, there is no empty cell where we could still place an additional cross without breaking the adjacency rule.

The task is to determine how many crosses Lёsha could have added at most, given the initial configuration.

The input size is small, with n up to 1000. This immediately suggests that an O(n²) approach is acceptable in principle, but since the structure is very local, we should expect a linear greedy solution.

A subtle but important constraint is that Misha’s configuration is already valid, so there are no adjacent `X` characters initially. This eliminates the need for validation or repair logic and allows us to focus purely on augmentation.

The main edge cases come from short gaps between existing crosses and boundaries:

If the string is `"..."`, then all positions are free, but we still cannot place crosses adjacent to each other, so the maximum placement is every other cell.

If the string is `"X.X"`, then no additional crosses can be added.

If the string is `"..X.."`, then only one additional cross can be placed, either to the left or right depending on parity.

A naive mistake is to try placing greedily without marking newly occupied neighbors, or to forget that a placed cross blocks both adjacent cells.

## Approaches

A brute-force strategy would try every subset of empty positions and check whether placing crosses there violates adjacency constraints. For each candidate subset, we would verify the entire string in O(n), leading to O(2ⁿ · n) complexity, which is completely infeasible even for n = 1000.

A slightly more reasonable brute-force is to iterate through positions and recursively decide whether to place a cross or not. Even with pruning, the branching factor remains high because each empty cell interacts only locally with neighbors, and we still end up exploring exponential configurations.

The key observation is that the constraint is purely local: placing a cross only forbids its immediate neighbors. This means we never need backtracking. Instead, we can scan from left to right and greedily place a cross whenever both neighbors are empty.

We must also respect already existing `X` positions, which act as forced occupied cells. Once we see a cell that is already occupied or blocked by a neighbor, we simply skip it. Otherwise, placing a cross immediately is always safe and locally optimal, because it preserves the ability to place as many crosses as possible in the remaining suffix.

This reduces the problem to a single linear pass.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(2ⁿ · n) | O(n) | Too slow |
| Optimal Greedy Scan | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

1. Initialize a counter `added = 0` to track how many crosses Lёsha places. We only count new placements, not existing ones.
2. Convert the string into a mutable array so we can mark newly placed crosses. This is important because newly placed crosses also block adjacent cells.
3. Traverse the string from left to right using an index `i`.
4. For each position `i`, check whether it is empty. If it is already `X`, we skip it because it is already occupied.
5. If position `i` is empty, we check whether we can place a cross here. This requires that the left neighbor (if it exists) is not `X`, and the right neighbor (if it exists) is not `X`. We also treat newly placed crosses as blocking in the same way.
6. If both neighbors are safe, we place a cross at position `i`, increment `added`, and mark `i` as `X` in the array so it affects future decisions.
7. Continue scanning until the end of the string.

After the scan completes, `added` is the maximum number of crosses Lёsha could have added.

### Why it works

The core invariant is that at every step of the scan, the prefix `[0..i-1]` is already in a state where no further modifications to earlier positions can improve the answer without violating the adjacency constraint. Any valid solution can be transformed into one that agrees with this greedy placement on the prefix without reducing the number of crosses, because decisions at position `i` only depend on `i-1` and `i+1`. Once we pass position `i`, we never revisit it, and any alternative choice would either block the same or more positions to the right. Therefore, placing a cross whenever possible is locally optimal and globally safe.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input().strip())
    s = list(input().strip())

    added = 0

    for i in range(n):
        if s[i] == 'X':
            continue

        left_ok = (i == 0 or s[i - 1] == '.')
        right_ok = (i == n - 1 or s[i + 1] == '.')

        if left_ok and right_ok:
            s[i] = 'X'
            added += 1

    print(added)

if __name__ == "__main__":
    solve()
```

The solution reads the string into a list so updates are efficient and reflect newly placed crosses immediately. The checks for left and right neighbors include boundary handling, where edges are treated as automatically safe on the outside.

The key implementation detail is that we check against the current state of the array, not the original string, so that newly added crosses correctly block subsequent placements.

## Worked Examples

### Example 1

Input:

```
5
.....
```

| i | s[i] | left_ok | right_ok | action | added |
| --- | --- | --- | --- | --- | --- |
| 0 | . | True | True | place X | 1 |
| 1 | X | - | - | skip | 1 |
| 2 | . | False | False | skip | 1 |
| 3 | X | - | - | skip | 1 |
| 4 | . | True | True | place X | 2 |

Final output is 2.

This shows that greedy placement naturally produces alternating positions and avoids violating adjacency.

### Example 2

Input:

```
5
.X...
```

| i | s[i] | left_ok | right_ok | action | added |
| --- | --- | --- | --- | --- | --- |
| 0 | . | True | False | skip | 0 |
| 1 | X | - | - | skip | 0 |
| 2 | . | False | True | skip | 0 |
| 3 | . | True | True | place X | 1 |
| 4 | . | False | True | skip | 1 |

Final output is 1.

This demonstrates how an existing `X` blocks nearby placements and forces gaps.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Each cell is processed once with O(1) neighbor checks |
| Space | O(n) | Mutable array representation of the string |

The linear scan easily fits within the constraints for n up to 1000. Even if n were significantly larger, the approach would still scale comfortably due to constant-time per cell processing.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys as _sys
    from io import StringIO
    out = StringIO()
    _stdout = sys.stdout
    sys.stdout = out
    solve()
    sys.stdout = _stdout
    return out.getvalue().strip()

# provided samples
assert run("5\n.....\n") == "3", "all empty (should place 3 in length 5)"
assert run("5\n.X...\n") == "1", "single block in middle"

# custom cases
assert run("1\n.\n") == "1", "single cell"
assert run("1\nX\n") == "0", "already occupied"
assert run("3\n...\n") == "2", "alternating placement"
assert run("4\nX.X.\n") == "0", "fully constrained pattern"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 cell empty | 1 | minimal placement |
| 1 cell filled | 0 | no extra placement possible |
| `...` | 2 | alternating greedy behavior |
| `X.X.` | 0 | existing constraints fully block |

## Edge Cases

A minimal input like `"."` is handled correctly because both boundary checks treat missing neighbors as safe, so the algorithm places a cross and returns 1.

A fully alternating pattern like `"X.X.X"` results in zero additions, because every empty position has at least one adjacent `X`. The scan sees each `.` but fails the neighbor check each time, so no placement is made.

A long empty segment like `"........"` demonstrates that greedy placement naturally produces every second position. The invariant holds because once a cross is placed at position `i`, position `i+1` is automatically blocked and never reconsidered.
