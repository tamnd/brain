---
title: "CF 1997B - Make Three Regions"
description: "We have a grid with only two rows. Some cells are free (.), some are blocked (x). Free cells form a graph where adjacent cells sharing a side are connected. A connected region is simply a connected component of this graph."
date: "2026-06-08T14:35:25+07:00"
tags: ["codeforces", "competitive-programming", "constructive-algorithms", "two-pointers"]
categories: ["algorithms"]
codeforces_contest: 1997
codeforces_index: "B"
codeforces_contest_name: "Educational Codeforces Round 168 (Rated for Div. 2)"
rating: 1100
weight: 1997
solve_time_s: 168
verified: true
draft: false
---

[CF 1997B - Make Three Regions](https://codeforces.com/problemset/problem/1997/B)

**Rating:** 1100  
**Tags:** constructive algorithms, two pointers  
**Solve time:** 2m 48s  
**Verified:** yes  

## Solution
## Problem Understanding

We have a grid with only two rows. Some cells are free (`.`), some are blocked (`x`).

Free cells form a graph where adjacent cells sharing a side are connected. A connected region is simply a connected component of this graph.

The input guarantees that before we do anything, the grid contains at most one connected region. In other words, all free cells are already connected, or there are no free cells at all.

For every free cell, we imagine blocking it and ask how many connected regions remain. We must count the cells whose removal produces exactly three connected regions.

The width of the grid can reach $2 \cdot 10^5$, and the sum over all test cases is also $2 \cdot 10^5$. Any solution that recomputes connected components for every candidate cell is far too expensive. Even an $O(n^2)$ algorithm would perform tens of billions of operations in the worst case.

The most dangerous mistakes come from assuming that every articulation point is valid.

Consider:

```
...
...
```

Removing the center cell of the top row does not create three regions. The bottom row still connects the left and right parts, so the graph remains connected.

Another subtle case is:

```
top:    ...
bottom: x.x
```

Removing the middle cell of the top row creates exactly three regions:

```
top:    .x.
bottom: x.x
```

The left top cell, the right top cell, and the bottom middle cell become three separate components.

A careless solution that only checks the degree of the removed cell would miss why this pattern works and why similar-looking patterns do not.

## Approaches

The brute-force idea is straightforward. For every free cell, temporarily block it, run a DFS or BFS over the remaining grid, count connected components, and check whether the answer is three.

This is correct because it directly simulates the definition of the problem.

The problem is the running time. There are $O(n)$ free cells, and each connectivity check costs $O(n)$. The total becomes $O(n^2)$, which is far too large when $n$ can be $2 \cdot 10^5$.

The key observation comes from the fact that the grid has only two rows.

Suppose removing a cell creates exactly three connected components. Since a vertex can split a graph into at most as many pieces as its degree, the removed cell must have degree three.

In a 2-row grid, degree three is possible only when:

```
same row:      . . .
other row:       .
```

The cell has a left neighbor, a right neighbor, and a vertical neighbor.

Now ask when those three neighbors become three different components after removal.

The vertical neighbor must not be able to reach either side. That means the cells adjacent to it in its own row must both be blocked:

```
same row:      . . .
other row:    x . x
```

This pattern is sufficient. After removing the center cell of the first row:

```
same row:      . x .
other row:    x . x
```

the left side, right side, and vertical cell become three separate regions.

Because the original grid contains at most one connected component, there is no alternative route around this local structure. The left and right parts cannot reconnect elsewhere.

So every valid cell is exactly the center of one of these patterns, and every such pattern is valid.

We only need to scan the columns and count them.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n²) | O(n) | Too slow |
| Optimal | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

1. For every column $i$ with $1 \le i \le n-2$, consider it as a possible center column.
2. Check whether the top cell at column $i$ is the removable cell.

We need:

```
top:    . . .
bottom: x . x
```

centered at column $i$.

Concretely:

```
top[i-1] == '.'
top[i]   == '.'
top[i+1] == '.'

bottom[i-1] == 'x'
bottom[i]   == '.'
bottom[i+1] == 'x'
```

If this pattern appears, increase the answer.
3. Perform the symmetric check with the rows swapped.

Now the removable cell is in the bottom row:

```
bottom: . . .
top:    x . x
```
4. After scanning all columns, output the count.

### Why it works

A cell can create three connected components only if it has three neighbors. In a 2-row grid, that forces the local shape

```
. . .
  .
```

around the removed cell.

For the three resulting components to be distinct, the vertical neighbor must be isolated from both left and right branches. The only way this happens is when the cells beside the vertical neighbor are blocked, producing

```
. . .
x . x
```

or its mirrored version.

Every counted pattern indeed produces exactly three components after removing the center cell. Conversely, any cell producing exactly three components must appear in one of these patterns. The scan counts all and only valid cells.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())

    for _ in range(t):
        n = int(input())
        s0 = input().strip()
        s1 = input().strip()

        ans = 0

        for i in range(1, n - 1):
            if (
                s0[i - 1] == '.' and
                s0[i] == '.' and
                s0[i + 1] == '.' and
                s1[i - 1] == 'x' and
                s1[i] == '.' and
                s1[i + 1] == 'x'
            ):
                ans += 1

            if (
                s1[i - 1] == '.' and
                s1[i] == '.' and
                s1[i + 1] == '.' and
                s0[i - 1] == 'x' and
                s0[i] == '.' and
                s0[i + 1] == 'x'
            ):
                ans += 1

        print(ans)

solve()
```

The loop starts at column `1` and ends at column `n - 2` because every valid pattern needs both a left neighbor and a right neighbor.

Each iteration performs two checks. The first assumes the removable cell is in the top row. The second assumes it is in the bottom row.

No graph construction, DFS, or component counting is required. The entire solution is driven by the structural characterization of a valid articulation cell in a 2-row grid.

The implementation uses only constant extra memory and processes each column once.

## Worked Examples

### Example 1

Input:

```
8
.......x
.x.xx...
```

The scan examines columns 2 through 7 (1-based indexing omitted here for clarity).

| Center Column | Top Pattern `...` | Bottom Pattern `x.x` | Counted |
| --- | --- | --- | --- |
| 1 | No | No | No |
| 2 | Yes | No | No |
| 3 | Yes | Yes | Yes |
| 4 | Yes | No | No |
| 5 | No | No | No |
| 6 | No | No | No |

Final answer:

```
1
```

The interesting column is the third one. Removing that top cell isolates the left branch, the right branch, and the bottom cell.

### Example 2

Input:

```
9
..x.x.x.x
x.......x
```

| Center Column | Bottom Pattern `...` | Top Pattern `x.x` | Counted |
| --- | --- | --- | --- |
| 1 | No | No | No |
| 2 | Yes | No | No |
| 3 | Yes | Yes | Yes |
| 4 | Yes | No | No |
| 5 | Yes | Yes | Yes |
| 6 | Yes | No | No |
| 7 | No | No | No |

Final answer:

```
2
```

The two valid removable cells are the bottom-row cells whose columns sit beneath the pattern `x.x` in the top row.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | One scan over the columns |
| Space | O(1) | Only a few variables are used |

Since the sum of all `n` values is at most `2 · 10^5`, a linear scan across each test case easily fits within the time limit.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    out = io.StringIO()

    input = sys.stdin.readline

    t = int(input())

    for _ in range(t):
        n = int(input())
        s0 = input().strip()
        s1 = input().strip()

        ans = 0

        for i in range(1, n - 1):
            if (
                s0[i - 1] == '.' and
                s0[i] == '.' and
                s0[i + 1] == '.' and
                s1[i - 1] == 'x' and
                s1[i] == '.' and
                s1[i + 1] == 'x'
            ):
                ans += 1

            if (
                s1[i - 1] == '.' and
                s1[i] == '.' and
                s1[i + 1] == '.' and
                s0[i - 1] == 'x' and
                s0[i] == '.' and
                s0[i + 1] == 'x'
            ):
                ans += 1

        print(ans, file=out)

    return out.getvalue()

# provided sample
assert run(
"""4
8
.......x
.x.xx...
2
..
..
3
xxx
xxx
9
..x.x.x.x
x.......x
"""
) == "1\n0\n0\n2\n"

# minimum size
assert run(
"""1
1
.
.
"""
) == "0\n"

# single valid pattern
assert run(
"""1
3
...
x.x
"""
) == "1\n"

# mirrored valid pattern
assert run(
"""1
3
x.x
...
"""
) == "1\n"

# no valid articulation
assert run(
"""1
5
.....
.....
"""
) == "0\n"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `n = 1`, both free | `0` | No center column exists |
| `... / x.x` | `1` | Smallest valid pattern |
| `x.x / ...` | `1` | Symmetric case |
| Two full rows of dots | `0` | Left and right remain connected |

## Edge Cases

Consider:

```
1
2
..
..
```

There is no column with both a left and a right neighbor. The scan range is empty, so the answer is `0`. A brute-force articulation-point intuition might incorrectly look at one of the cells and expect a split, but degree three is impossible in a width-two grid of length two.

Consider:

```
1
3
...
...
```

The center top cell has degree three, but the pattern is not valid. The bottom row provides a route connecting the left and right sides after removal. Our check rejects it because the opposite row is `...`, not `x.x`.

Consider:

```
1
3
...
x.x
```

The center top cell matches the required pattern exactly. The algorithm counts it. After removal:

```
.x.
x.x
```

the three remaining free cells are pairwise disconnected, giving exactly three connected regions.

These examples cover the main pitfalls and show why the local pattern characterization is both necessary and sufficient.
