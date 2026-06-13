---
title: "CF 1703E - Mirror Grid"
description: "We are given an $n times n$ grid whose cells contain only 0 or 1. We may flip any cell, changing 0 to 1 or 1 to 0, and each flip costs one operation. The goal is to make the grid look identical after rotating it by $90^circ$, $180^circ$, or $270^circ$."
date: "2026-06-09T21:37:55+07:00"
tags: ["codeforces", "competitive-programming", "implementation"]
categories: ["algorithms"]
codeforces_contest: 1703
codeforces_index: "E"
codeforces_contest_name: "Codeforces Round 806 (Div. 4)"
rating: 1200
weight: 1703
solve_time_s: 156
verified: false
draft: false
---

[CF 1703E - Mirror Grid](https://codeforces.com/problemset/problem/1703/E)

**Rating:** 1200  
**Tags:** implementation  
**Solve time:** 2m 36s  
**Verified:** no  

## Solution
## Problem Understanding

We are given an $n \times n$ grid whose cells contain only `0` or `1`. We may flip any cell, changing `0` to `1` or `1` to `0`, and each flip costs one operation.

The goal is to make the grid look identical after rotating it by $90^\circ$, $180^\circ$, or $270^\circ$. In other words, every rotation must produce exactly the same grid as the original.

The input consists of multiple test cases. For each test case we receive the size of the square grid and then the grid itself. We must output the minimum number of cell flips required to achieve rotational symmetry.

The constraints are small enough that examining every cell several times is completely feasible. The largest grid has $100 \times 100 = 10{,}000$ cells, and there are at most 100 test cases. An $O(n^2)$ solution per test case easily fits within the limits, while anything involving exponential search over flip combinations would be impossible.

The tricky part is understanding which cells are tied together by rotational symmetry. A careless implementation might process cells independently even though rotating the grid forces several positions to always contain the same value.

Consider this grid:

```
2
10
00
```

The four positions involved in rotation are:

```
(0,0) -> (0,1) -> (1,1) -> (1,0)
```

Their values are:

```
1 0 0 0
```

To make all four equal, one flip is enough. Flipping the lone `1` gives four zeros. Treating positions independently would miss this relationship.

Another subtle case is the center cell of an odd-sized grid:

```
3
000
010
000
```

The center cell maps to itself under every rotation. No operation is ever needed for it. A solution that tries to force every group to have size four may accidentally count extra flips.

A third common mistake is double-counting rotation groups. For example:

```
3
010
110
010
```

The corner cells form one rotational group, and the edge-middle cells form another. If we iterate through all cells and process every group repeatedly, the answer becomes four times too large.

## Approaches

A brute-force viewpoint is to consider every set of cells connected by rotation. For each set, we could try all possible final assignments and choose the cheapest one.

A rotation by $90^\circ$ sends position $(i,j)$ to:

$$(j,\ n-1-i)$$

Applying this repeatedly produces at most four distinct positions:

$$(i,j) \rightarrow (j,n-1-i) \rightarrow (n-1-i,n-1-j) \rightarrow (n-1-j,i)$$

For the final grid to remain unchanged after rotation, all cells in this orbit must contain the same value.

The brute-force idea works because each orbit is independent. Once we know the cells belonging to one orbit, we only need to decide whether they all become `0` or all become `1`. If an orbit contains $k$ ones, then:

```
cost to make all 0 = k
cost to make all 1 = size - k
```

We take the smaller value.

The only remaining challenge is avoiding repeated processing of the same orbit. Every orbit of size four appears four times if we start from every cell. Instead, we process each orbit exactly once.

The key observation is that every orbit intersects the upper-left quadrant exactly once. If we iterate only over:

```
0 <= i < n/2
0 <= j < (n+1)/2
```

then each rotational group is visited exactly once. We collect its four cells, count how many are `1`, and add the minimum number of flips needed.

This transforms the problem into a simple $O(n^2)$ scan.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force with repeated orbit processing | $O(n^2)$ but prone to double counting | $O(1)$ | Incorrect |
| Optimal orbit-based processing | $O(n^2)$ | $O(1)$ | Accepted |

## Algorithm Walkthrough

1. Read the grid.
2. Iterate through the cells in the upper-left representative region:

$$0 \le i < \frac{n}{2}$$

$$0 \le j < \frac{n+1}{2}$$

Every rotational orbit appears exactly once in this region.
3. For each selected position $(i,j)$, compute its four rotationally equivalent cells:

$$(i,j)$$

$$(j,n-1-i)$$

$$(n-1-i,n-1-j)$$

$$(n-1-j,i)$$
4. Count how many of these four cells contain `1`.
5. If the count is `ones`, then the number of zeros is `4 - ones`.
6. To make all four cells equal, either flip all ones to zero or all zeros to one. Add:

$$\min(\text{ones},\ 4-\text{ones})$$

to the answer.
7. After processing all representative cells, output the accumulated answer.

### Why it works

Rotational symmetry requires every cell to match the value of all cells obtained by repeatedly applying a $90^\circ$ rotation. These positions form an orbit. Different orbits never interact, so the optimal solution can be computed independently for each orbit and then summed.

Within one orbit, the final value must be either all zeros or all ones. The cheapest choice is whichever requires fewer flips, namely $\min(\text{ones}, \text{zeros})$. Since every orbit is processed exactly once, every required modification is counted exactly once, producing the minimum total number of operations.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())

    for _ in range(t):
        n = int(input())
        g = [input().strip() for _ in range(n)]

        ans = 0

        for i in range(n // 2):
            for j in range((n + 1) // 2):
                cells = [
                    g[i][j],
                    g[j][n - 1 - i],
                    g[n - 1 - i][n - 1 - j],
                    g[n - 1 - j][i]
                ]

                ones = sum(c == '1' for c in cells)
                ans += min(ones, 4 - ones)

        print(ans)

solve()
```

The outer loops enumerate exactly one representative from every rotational orbit. The bounds are the most delicate part of the implementation. Using `n // 2` rows and `(n + 1) // 2` columns covers all groups exactly once and naturally skips the center cell when `n` is odd.

For each representative position, the code computes the four locations obtained by successive $90^\circ$ rotations. These coordinates are derived directly from the rotation formula.

The count of ones determines the optimal cost for that orbit. If an orbit contains three ones and one zero, changing the single zero costs one operation, while changing the three ones costs three operations. Taking the minimum gives the optimal local contribution.

Since orbits are independent, summing these costs yields the global optimum.

## Worked Examples

### Example 1

Input:

```
3
010
110
010
```

The algorithm processes one orbit.

| i | j | Orbit Values | Ones | Contribution |
| --- | --- | --- | --- | --- |
| 0 | 0 | 0,0,0,1 | 1 | 1 |

Total answer:

```
1
```

The corner orbit contains one `1` and three `0`s. Making them all zero requires a single flip.

### Example 2

Input:

```
1
0
```

There are no size-four orbits.

| n | Processed Orbits | Answer |
| --- | --- | --- |
| 1 | 0 | 0 |

The center cell maps to itself under every rotation, so the grid is already rotationally symmetric.

This example demonstrates why odd-sized grids need no special handling beyond the loop bounds.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n^2)$ | Every orbit is processed once, proportional to the number of cells |
| Space | $O(1)$ | Only a few variables are stored besides the input grid |

The largest test case contains only 10,000 cells. An $O(n^2)$ traversal is extremely fast, and the constant factors are tiny because each orbit involves only four coordinate lookups.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    input = sys.stdin.readline

    t = int(input())
    out = []

    for _ in range(t):
        n = int(input())
        g = [input().strip() for _ in range(n)]

        ans = 0

        for i in range(n // 2):
            for j in range((n + 1) // 2):
                cells = [
                    g[i][j],
                    g[j][n - 1 - i],
                    g[n - 1 - i][n - 1 - j],
                    g[n - 1 - j][i]
                ]
                ones = sum(c == '1' for c in cells)
                ans += min(ones, 4 - ones)

        out.append(str(ans))

    return "\n".join(out) + "\n"

# provided sample
assert run(
"""5
3
010
110
010
1
0
5
11100
11011
01011
10011
11000
5
01000
10101
01010
00010
01001
5
11001
00000
11111
10110
01111
"""
) == "1\n0\n9\n7\n6\n"

# minimum size
assert run(
"""1
1
1
"""
) == "0\n"

# already symmetric
assert run(
"""1
2
11
11
"""
) == "0\n"

# one differing corner
assert run(
"""1
2
10
00
"""
) == "1\n"

# odd size with center ignored
assert run(
"""1
3
000
010
000
"""
) == "0\n"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1×1 grid containing `1` | 0 | Center cell maps to itself |
| 2×2 all ones | 0 | Already symmetric grid |
| 2×2 with one corner set | 1 | Single orbit correction |
| 3×3 with only center equal to `1` | 0 | Center cell should not contribute |

## Edge Cases

### Odd-sized grid with a center cell

Input:

```
1
3
000
010
000
```

The center position is `(1,1)`. Rotating the grid keeps this cell in exactly the same place. The algorithm never processes it because the representative loops only cover size-four orbits.

All other cells already form symmetric groups, so the answer remains:

```
0
```

### Orbit containing three equal values and one different value

Input:

```
1
2
10
00
```

The orbit is:

```
(0,0), (0,1), (1,1), (1,0)
```

Values:

```
1 0 0 0
```

The algorithm computes:

```
ones = 1
zeros = 3
min(1, 3) = 1
```

Output:

```
1
```

A greedy attempt to force everything to `1` would use three flips instead of one.

### Double-counting danger

Input:

```
1
3
010
110
010
```

The four corner cells form a single orbit:

```
0 0 0 1
```

A naive scan over all cells would encounter this orbit four times. The representative-region iteration visits it once, computes cost `1`, and stops. The correct answer is:

```
1
```

This confirms that every rotational group contributes exactly once to the final sum.
