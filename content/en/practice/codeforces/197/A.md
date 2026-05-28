---
title: "CF 197A - Plate Game"
description: "We have a rectangular table with dimensions a × b and an unlimited supply of identical circular plates with radius r. Two players alternate placing plates on the table. Every plate must lie completely inside the rectangle, and plates may touch but cannot overlap."
date: "2026-05-29T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "constructive-algorithms", "games", "math"]
categories: ["algorithms"]
codeforces_contest: 197
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 124 (Div. 2)"
rating: 1600
weight: 197
solve_time_s: 82
verified: true
draft: false
---

[CF 197A - Plate Game](https://codeforces.com/problemset/problem/197/A)

**Rating:** 1600  
**Tags:** constructive algorithms, games, math  
**Solve time:** 1m 22s  
**Verified:** yes  

## Solution
## Problem Understanding

We have a rectangular table with dimensions `a × b` and an unlimited supply of identical circular plates with radius `r`. Two players alternate placing plates on the table. Every plate must lie completely inside the rectangle, and plates may touch but cannot overlap.

The game ends when the current player cannot place another plate. Both players play optimally, and we must determine whether the first or second player wins.

The geometry is much simpler than it first appears. A plate of radius `r` fits inside the table only if its center stays at least `r` units away from every border. That means the center must lie inside a smaller rectangle of dimensions `(a - 2r) × (b - 2r)`.

The constraints are tiny, every value is at most `100`, so even brute-force geometric simulation would technically fit within the limits. The real challenge is recognizing the game structure and simplifying the geometry correctly.

The key edge case is when exactly one plate fits. For example:

```
5 5 2
```

The correct answer is `"First"` because one plate can be placed at the center and then the game ends.

A careless approach might incorrectly think more placements are possible because the remaining uncovered area is large. The actual restriction comes from circle overlap, not unused area.

Another subtle case is when no plate fits at all:

```
3 3 2
```

The diameter is `4`, larger than both table dimensions, so even a single plate cannot be placed. The correct answer is `"Second"` because the first player has no move.

A common mistake is checking `a >= r` and `b >= r` instead of requiring room for the full diameter. The correct condition is `a >= 2r` and `b >= 2r`.

There is also a boundary-touching case:

```
4 7 2
```

The plate diameter equals the table height exactly. This is still valid because touching borders is allowed. One plate fits, so the answer is `"First"`.

An implementation using strict inequalities instead of non-strict inequalities would fail here.

## Approaches

The brute-force interpretation is to model the game geometrically. One could try generating every valid plate placement, checking overlaps against previously placed circles, and recursively evaluating winning and losing states with minimax.

That approach is correct in principle because the game is finite and deterministic. The problem is that the state space explodes immediately. Even after discretizing positions, the number of configurations becomes enormous because plate centers can vary continuously. A full geometric game search is completely impractical.

The breakthrough observation is that the board can never contain more than one plate.

A plate has diameter `2r`. If two plates were placed on the table, their centers would need to be at least `2r` apart. But any valid center must remain inside the rectangle:

```
[r, a-r] × [r, b-r]
```

If both `a < 4r` or `b < 4r`, there is not enough room to separate two centers by distance `2r`.

More directly, the original Codeforces trick is even simpler. Since both plates must fit entirely inside the table, placing two non-overlapping circles of radius `r` requires at least one table dimension to be at least `4r`. Under the problem constraints and geometry, the only thing that matters is whether at least one plate fits.

If no plate fits, the first player loses immediately.

If at least one plate fits, the first player places it and wins because no second move exists.

So the game reduces to a single condition:

```
a >= 2r and b >= 2r
```

If true, print `"First"`. Otherwise print `"Second"`.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | Exponential / infinite-state | Huge | Too slow |
| Optimal | O(1) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the table dimensions `a` and `b`, along with the plate radius `r`.
2. Check whether one plate can fit on the table.

A plate fits only if its diameter `2r` does not exceed either table dimension. This gives the condition:

$a \ge 2r \text{ and } b \ge 2r$
3. If the condition is true, print `"First"`.

The first player places the only possible plate and leaves no legal move.
4. Otherwise, print `"Second"`.

No plate can be placed at all, so the first player immediately loses.

### Why it works

The entire game hinges on whether a legal first move exists. A plate of radius `r` needs a square of side `2r` just to fit inside the table. If either table dimension is smaller than `2r`, no move exists.

If a move does exist, the first player can always place one plate. After that, another plate cannot be added without overlap because there is insufficient remaining space for a second circle of the same radius. The game always lasts either zero moves or one move, so the winner is determined entirely by the existence of the first move.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    a, b, r = map(int, input().split())

    if a >= 2 * r and b >= 2 * r:
        print("First")
    else:
        print("Second")

solve()
```

The implementation directly mirrors the mathematical observation from the walkthrough.

The expression `2 * r` is the plate diameter. A plate fits only if both dimensions of the table are at least that large.

The comparison must use `>=` instead of `>`. The problem explicitly allows touching the border, so a plate whose diameter exactly matches a table dimension is still valid.

No loops or additional memory are needed because the result depends on a single geometric check.

## Worked Examples

### Sample 1

Input:

```
5 5 2
```

| Variable | Value |
| --- | --- |
| a | 5 |
| b | 5 |
| r | 2 |
| 2r | 4 |
| a >= 2r | True |
| b >= 2r | True |
| Output | First |

A circle of diameter `4` fits inside a `5 × 5` table. The first player places one plate, and no further move exists.

### Sample 2

Input:

```
3 3 2
```

| Variable | Value |
| --- | --- |
| a | 3 |
| b | 3 |
| r | 2 |
| 2r | 4 |
| a >= 2r | False |
| b >= 2r | False |
| Output | Second |

The diameter is larger than both table dimensions, so no legal placement exists. The first player loses immediately.

These traces confirm the core invariant: the game outcome depends only on whether a legal first placement exists.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(1) | Only a few arithmetic operations and comparisons |
| Space | O(1) | No extra memory is used |

The constraints are extremely small, but the constant-time solution is even stronger. The program performs a single geometric check and immediately produces the answer, easily fitting within the time and memory limits.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys, io

def solve():
    input = sys.stdin.readline

    a, b, r = map(int, input().split())

    if a >= 2 * r and b >= 2 * r:
        print("First")
    else:
        print("Second")

def run(inp: str) -> str:
    backup_stdin = sys.stdin
    backup_stdout = sys.stdout

    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    solve()

    output = sys.stdout.getvalue()

    sys.stdin = backup_stdin
    sys.stdout = backup_stdout

    return output

# provided sample
assert run("5 5 2\n") == "First\n", "sample 1"

# no plate fits
assert run("3 3 2\n") == "Second\n", "no valid move"

# exact boundary fit
assert run("4 7 2\n") == "First\n", "touching border allowed"

# minimum values
assert run("1 1 1\n") == "Second\n", "smallest table"

# large valid case
assert run("100 100 50\n") == "First\n", "maximum exact fit"

# one dimension too small
assert run("10 3 2\n") == "Second\n", "fails on one dimension only"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `3 3 2` | `Second` | No plate can fit |
| `4 7 2` | `First` | Border touching is allowed |
| `1 1 1` | `Second` | Minimum-size edge case |
| `100 100 50` | `First` | Maximum exact-fit case |
| `10 3 2` | `Second` | Both dimensions must satisfy the condition |

## Edge Cases

Consider the input:

```
4 7 2
```

The diameter is `4`. The table height is also exactly `4`, so the circle touches the top and bottom borders simultaneously.

The algorithm checks:

```
4 >= 4  -> True
7 >= 4  -> True
```

and prints `"First"`.

This confirms the implementation correctly handles non-strict inequalities.

Now consider:

```
3 3 2
```

The diameter is `4`, larger than both dimensions. The checks become:

```
3 >= 4  -> False
3 >= 4  -> False
```

The algorithm prints `"Second"` because no legal placement exists.

Finally, consider a mixed case:

```
10 3 2
```

The width is large enough, but the height is not:

```
10 >= 4 -> True
3 >= 4  -> False
```

The algorithm still prints `"Second"` because the plate must fit completely in both dimensions. A common incorrect solution checks only one dimension or uses area-based reasoning, both of which fail here.
