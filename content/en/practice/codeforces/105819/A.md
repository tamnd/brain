---
title: "CF 105819A - Lily Pads"
description: "There are $N$ rows of lily pads. Every row contains exactly two pads, left and right. At any moment exactly one of them is afloat. Two frogs start before the first row and both must reach the far shore."
date: "2026-06-25T15:05:44+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105819
codeforces_index: "A"
codeforces_contest_name: "TeamsCode Spring 2025 Novice Division"
rating: 0
weight: 105819
solve_time_s: 44
verified: true
draft: false
---

[CF 105819A - Lily Pads](https://codeforces.com/problemset/problem/105819/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 44s  
**Verified:** yes  

## Solution
## Problem Understanding

There are $N$ rows of lily pads. Every row contains exactly two pads, left and right. At any moment exactly one of them is afloat.

Two frogs start before the first row and both must reach the far shore. A frog may move only forward, from row $i$ to row $i+1$, and can land only on the currently afloat pad. When a frog leaves a pad, that row flips state: the pad it left sinks and the other pad becomes afloat. Each frog earns one point whenever it lands on a right pad. We may choose the order of all jumps and want the maximum total score earned by the two frogs.

The input gives the initial afloat pad in every row. For row $i$, `L` means the left pad starts afloat and `R` means the right pad starts afloat. $N$ is at most $100$, so even a simulation would be trivial from a performance perspective. The real task is recognizing the invariant hidden in the flipping behavior.

A common mistake is to think that the jumping order can change how many right-pad landings occur in a row. Consider:

```
1
R
```

The first frog to visit the row must land on the right pad and gains a point. After it leaves, the row flips, so the second frog must land on the left pad. The total is exactly 1.

Similarly:

```
1
L
```

The first frog lands left, the row flips, and the second frog lands right. The total is again 1.

The key observation is that every row is visited exactly twice, once by each frog, and the two visits are forced to use opposite sides.

## Approaches

A brute-force viewpoint is to model the entire process. At every step we choose which frog jumps next, track which rows are occupied, and track the current afloat side of every row. This correctly explores all valid schedules, but the number of possible jump orders grows exponentially and quickly becomes impractical.

The reason the brute-force is unnecessary is that the rows are effectively independent from the scoring perspective.

Focus on a single row. The first frog that reaches the row must land on the initially afloat side. Before the second frog can use that row, the first frog must leave it, because a pad can hold only one frog. When the first frog leaves, the row flips. As a result, the second frog is forced to land on the opposite side.

That means each row contributes exactly one right-pad landing:

If the row starts as `R`, the first visit is right and the second is left.

If the row starts as `L`, the first visit is left and the second is right.

Either way, among the two landings in that row, exactly one is on the right pad.

Since there are $N$ rows and every row contributes exactly one point, the answer is always $N$.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | Exponential | Exponential | Too slow |
| Optimal | O(1) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read $N$.
2. Read the string describing the initial afloat side of each row.
3. Ignore the string's contents. The answer depends only on the number of rows.
4. Output $N$.

Why it works:

For every row, the two frogs must visit it exactly once each. The first visit uses the currently afloat side. After that frog leaves the row, the row flips, forcing the second visit to use the opposite side. The two visits always consist of one left landing and one right landing. Hence each row contributes exactly one point, regardless of the jump order or the initial side. Summing over all $N$ rows gives exactly $N$ points.

## Python Solution

```python
import sys
input = sys.stdin.readline

n = int(input())
s = input().strip()

print(n)
```

The implementation is short because the entire problem collapses to the row invariant proved above.

The input string is still read because it is part of the input format. Ignoring it is intentional. Whether a row starts as `L` or `R`, its contribution is always exactly one point.

No simulation is required. No edge cases require special handling beyond reading the input correctly.

## Worked Examples

### Example 1

Input:

```
1
R
```

| Row | Initial Side | First Landing | Second Landing | Points From Row |
| --- | --- | --- | --- | --- |
| 1 | R | R | L | 1 |

Total answer:

| N | Answer |
| --- | --- |
| 1 | 1 |

This example shows that a row beginning with the right pad afloat contributes one point immediately on the first visit.

### Example 2

Input:

```
3
LLR
```

| Row | Initial Side | First Landing | Second Landing | Points From Row |
| --- | --- | --- | --- | --- |
| 1 | L | L | R | 1 |
| 2 | L | L | R | 1 |
| 3 | R | R | L | 1 |

Total answer:

| N | Answer |
| --- | --- |
| 3 | 3 |

This demonstrates that the initial configuration does not matter. Every row contributes exactly one point.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(1) | After reading the input, the answer is simply `n` |
| Space | O(1) | Only a few variables are stored |

The constraints are tiny, but the solution is even simpler than a linear scan. The running time and memory usage are effectively constant.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys, io

def solve():
    input = sys.stdin.readline
    n = int(input())
    s = input().strip()
    print(n)

def run(inp: str) -> str:
    backup_stdin = sys.stdin
    backup_stdout = sys.stdout

    sys.stdin = io.StringIO(inp)
    out = io.StringIO()
    sys.stdout = out

    solve()

    sys.stdin = backup_stdin
    sys.stdout = backup_stdout

    return out.getvalue()

# provided sample
assert run("1\nR\n") == "1\n", "sample 1"

# custom cases
assert run("1\nL\n") == "1\n", "single row starting left"
assert run("2\nLR\n") == "2\n", "mixed configuration"
assert run("5\nRRRRR\n") == "5\n", "all right"
assert run("100\n" + "L" * 100 + "\n") == "100\n", "maximum n"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 / R` | `1` | Sample case |
| `1 / L` | `1` | Single row starting on the left |
| `2 / LR` | `2` | Mixed row states |
| `5 / RRRRR` | `5` | All rows start right |
| `100 / L...L` | `100` | Maximum constraint |

## Edge Cases

Consider:

```
1
L
```

The first frog lands on the left pad. When it leaves, the row flips. The second frog must land on the right pad. The row contributes exactly one point, so the answer is 1.

Now consider:

```
1
R
```

The first frog lands on the right pad and gains one point. After the flip, the second frog lands on the left pad. Again the row contributes exactly one point, so the answer is 1.

A larger example:

```
4
LRRL
```

Row 1 contributes one point, row 2 contributes one point, row 3 contributes one point, and row 4 contributes one point. The total is 4. The jumping order may change which frog receives a particular point, but it cannot change the total number of right-pad landings in any row. The invariant remains intact for every row independently.
