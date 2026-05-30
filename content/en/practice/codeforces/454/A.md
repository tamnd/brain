---
title: "CF 454A - Little Pony and Crystal Mine"
description: "We need to print an odd-sized square grid that contains a diamond shape. Every cell belonging to the diamond is represented by the character D, and every other cell is represented by . The input contains a single odd integer n."
date: "2026-05-30T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "implementation"]
categories: ["algorithms"]
codeforces_contest: 454
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 259 (Div. 2)"
rating: 800
weight: 454
solve_time_s: 87
verified: true
draft: false
---

[CF 454A - Little Pony and Crystal Mine](https://codeforces.com/problemset/problem/454/A)

**Rating:** 800  
**Tags:** implementation  
**Solve time:** 1m 27s  
**Verified:** yes  

## Solution
## Problem Understanding

We need to print an odd-sized square grid that contains a diamond shape. Every cell belonging to the diamond is represented by the character `D`, and every other cell is represented by `*`.

The input contains a single odd integer `n`. The output must consist of exactly `n` rows, each containing exactly `n` characters. The diamond is centered in the grid and expands toward the middle row, then shrinks symmetrically afterward.

The constraints are very small. The largest possible grid is only `101 × 101`, which contains 10,201 cells. Even an algorithm that examines every cell individually is easily fast enough within the one-second limit. There is no need for advanced optimization.

The main challenge is not performance but correctly constructing the diamond pattern.

One easy mistake is handling the transition between the upper and lower halves incorrectly.

For example:

Input:

```
5
```

Correct output:

```
**D**
*DDD*
DDDDD
*DDD*
**D**
```

A careless implementation might continue increasing the width after the center row or start decreasing one row too early.

Another common mistake is producing rows with the wrong total length.

For example, the first row of a size-5 crystal must be:

```
**D**
```

The row contains 2 stars, then 1 `D`, then 2 stars, for a total length of 5. Forgetting the trailing stars would produce:

```
**D
```

which is invalid because every row must contain exactly `n` characters.

The smallest valid input is also worth checking.

Input:

```
3
```

Output:

```
*D*
DDD
*D*
```

The center row already occupies the entire width, so boundary calculations must still work when the diamond reaches both edges.

## Approaches

A straightforward way to solve the problem is to examine every position `(row, column)` in the grid and decide whether that cell belongs to the diamond. Since the diamond is centered, we can compute the distance from the center row and center column and mark cells accordingly. This approach is correct because every cell is classified independently. It performs `n²` checks, which is at most 10,201 operations for the given constraints.

There is an even simpler observation. We do not actually need to decide cell-by-cell. If we know how many `D` characters belong in a row, the remaining positions must be stars.

The diamond grows by two cells per row until reaching the center:

```
1, 3, 5, ..., n
```

After the center row, it shrinks symmetrically:

```
..., 5, 3, 1
```

For each row, once the number of `D` characters is known, the number of stars on each side is:

```
(n - D_count) / 2
```

The entire row can then be built directly as:

```
stars + Ds + stars
```

This avoids thinking about individual cells and matches the geometric structure of the diamond.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n²) | O(1) | Accepted |
| Optimal | O(n²) | O(1) | Accepted |

Even though both approaches have the same asymptotic complexity, constructing rows directly is simpler and more natural for this pattern-printing task.

## Algorithm Walkthrough

1. Read the odd integer `n`.
2. Compute the middle row index as `mid = n // 2`.
3. Iterate through every row index `i` from `0` to `n - 1`.
4. Compute the distance from the center row:

```
dist = abs(i - mid)
```

Rows equally far from the center must look identical because the diamond is symmetric.
5. Determine how many `D` characters belong in this row:

```
d = n - 2 * dist
```

Every step away from the center removes one `D` from the left side and one from the right side.
6. Compute the number of stars on each side:

```
stars = (n - d) // 2
```
7. Construct the row:

```
"*" * stars + "D" * d + "*" * stars
```
8. Output the row.

### Why it works

For a row at distance `dist` from the center, the diamond becomes narrower by exactly one cell on each side. That reduces the width of the diamond by `2 × dist`, giving `n - 2 × dist` diamond cells. The remaining positions are split evenly between the left and right sides because the figure is symmetric around the center column. Every row produced by the algorithm has exactly the correct number of stars and `D` characters, so the resulting grid is precisely the required diamond.

## Python Solution

```python
import sys
input = sys.stdin.readline

n = int(input())

mid = n // 2

for i in range(n):
    dist = abs(i - mid)
    d = n - 2 * dist
    stars = (n - d) // 2
    print("*" * stars + "D" * d + "*" * stars)
```

The solution begins by locating the middle row. Every other row is described entirely by its distance from that center.

The value `d` stores the number of consecutive `D` characters in the current row. At the center row, `dist = 0`, so `d = n`, meaning the entire row consists of `D` characters. Moving one row away decreases the width by two, which matches the shape of the diamond.

The value `stars` is computed from the unused positions. Since the pattern is symmetric, half of those positions appear on the left and half on the right.

Using `abs(i - mid)` avoids separate logic for the upper and lower halves. The same formula automatically handles both sides of the diamond and eliminates many common off-by-one mistakes.

## Worked Examples

### Example 1

Input:

```
3
```

| Row `i` | `dist` | `d` | `stars` | Output Row |
| --- | --- | --- | --- | --- |
| 0 | 1 | 1 | 1 | `*D*` |
| 1 | 0 | 3 | 0 | `DDD` |
| 2 | 1 | 1 | 1 | `*D*` |

Output:

```
*D*
DDD
*D*
```

This trace shows the symmetry around the center row. Rows 0 and 2 have identical values because they are equally far from the middle.

### Example 2

Input:

```
5
```

| Row `i` | `dist` | `d` | `stars` | Output Row |
| --- | --- | --- | --- | --- |
| 0 | 2 | 1 | 2 | `**D**` |
| 1 | 1 | 3 | 1 | `*DDD*` |
| 2 | 0 | 5 | 0 | `DDDDD` |
| 3 | 1 | 3 | 1 | `*DDD*` |
| 4 | 2 | 1 | 2 | `**D**` |

Output:

```
**D**
*DDD*
DDDDD
*DDD*
**D**
```

This example demonstrates the expansion toward the center and the matching contraction afterward. The sequence of `D` counts is `1, 3, 5, 3, 1`.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n²) | Printing each of the `n²` characters once |
| Space | O(1) | Only a few integer variables are stored |

The largest possible grid contains just 10,201 characters, so generating and printing the pattern is easily within both the time and memory limits.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    n = int(sys.stdin.readline())
    mid = n // 2

    out = []
    for i in range(n):
        dist = abs(i - mid)
        d = n - 2 * dist
        stars = (n - d) // 2
        out.append("*" * stars + "D" * d + "*" * stars)

    return "\n".join(out) + "\n"

# provided sample
assert run("3\n") == "*D*\nDDD\n*D*\n", "sample 1"

# minimum valid size
assert run("3\n") == "*D*\nDDD\n*D*\n", "minimum size"

# small symmetric case
assert run("5\n") == "**D**\n*DDD*\nDDDDD\n*DDD*\n**D**\n", "size 5"

# larger odd size
assert run("7\n") == "***D***\n**DDD**\n*DDDDD*\nDDDDDDD\n*DDDDD*\n**DDD**\n***D***\n", "size 7"

# maximum size, verify dimensions
res = run("101\n").splitlines()
assert len(res) == 101
assert all(len(row) == 101 for row in res)
assert res[50] == "D" * 101
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `3` | Small diamond | Minimum valid size |
| `5` | Width sequence `1,3,5,3,1` | Expansion and contraction |
| `7` | Width sequence `1,3,5,7,5,3,1` | General symmetry |
| `101` | Center row has 101 `D`s | Maximum constraint handling |

## Edge Cases

### Smallest Valid Crystal

Input:

```
3
```

The middle row index is `1`.

For rows `0` and `2`, the distance from the center is `1`, so `d = 1` and `stars = 1`. For row `1`, the distance is `0`, so `d = 3` and `stars = 0`.

Output:

```
*D*
DDD
*D*
```

The formula works without requiring any special handling for the smallest allowed size.

### Center Row Occupies Entire Width

Input:

```
5
```

At row `2`, which is the center row:

```
dist = 0
d = 5
stars = 0
```

The produced row is:

```
DDDDD
```

No stars are added because the diamond reaches both edges. The computation naturally handles this case.

### Symmetry Between Upper and Lower Halves

Input:

```
7
```

Rows `1` and `5` both have:

```
dist = 2
d = 3
stars = 2
```

Both rows become:

```
**DDD**
```

Because the algorithm depends only on the absolute distance from the center, mirrored rows are guaranteed to be identical, which preserves the required diamond shape.
