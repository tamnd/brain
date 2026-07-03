---
title: "CF 103361H - \u041d\u043e\u0436\u043d\u0438\u0446\u044b"
description: "We are given a rectangle of size $m times n$, and we want to completely tile it using smaller rectangles of fixed size $1 times k$."
date: "2026-07-03T13:07:14+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 103361
codeforces_index: "H"
codeforces_contest_name: "\u041e\u0442\u043a\u0440\u044b\u0442\u0430\u044f \u041a\u043e\u043c\u0430\u043d\u0434\u043d\u0430\u044f \u041e\u043b\u0438\u043c\u043f\u0438\u0430\u0434\u0430 \u042e\u041c\u0428 \u043f\u043e \u043f\u0440\u043e\u0433\u0440\u0430\u043c\u043c\u0438\u0440\u043e\u0432\u0430\u043d\u0438\u044e"
rating: 0
weight: 103361
solve_time_s: 48
verified: true
draft: false
---

[CF 103361H - \u041d\u043e\u0436\u043d\u0438\u0446\u044b](https://codeforces.com/problemset/problem/103361/H)

**Rating:** -  
**Tags:** -  
**Solve time:** 48s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a rectangle of size $m \times n$, and we want to completely tile it using smaller rectangles of fixed size $1 \times k$. Each tile can be placed in either orientation, meaning it can be used as $1 \times k$ or $k \times 1$, and we are allowed to cut the big rectangle into such pieces without overlap or gaps. The task is to decide whether such a perfect tiling exists.

The input consists of three integers $m$, $n$, and $k$, each up to $10^9$. Since there is only one test case and all operations are constant time arithmetic checks, any solution must run in constant time.

The key structural constraint is that every tile always covers exactly $k$ unit squares. That immediately implies that the area $m \cdot n$ must be divisible by $k$. However, divisibility alone is not sufficient because the geometry of fitting long thin rectangles into a grid imposes additional constraints about alignment along rows and columns.

A subtle edge case appears when $k = 1$. In this case, every cell is already a valid tile, so any rectangle is trivially tileable. Another edge case occurs when one dimension is already 1, because then we are effectively working with a 1D segment.

A naive mistake is to only check area divisibility. For example, $m = 2, n = 3, k = 4$ gives area 6, which is not divisible by 4, so it is correctly impossible. But consider $m = 2, n = 3, k = 2$: area is 6, divisible by 2, and indeed it works. The real challenge is distinguishing cases where divisibility holds but placement is impossible, such as $m = 6, n = 6, k = 4$, where area is 36 divisible by 4 but tiling is impossible due to mismatch in achievable strip configurations.

## Approaches

A brute-force approach would try to simulate placing $1 \times k$ or $k \times 1$ tiles inside the grid, backtracking over all placements. Each placement reduces the available space, and we would recursively attempt to fill the remaining region. The number of states grows extremely fast because at each step there are many possible placements, and even for modest grids this quickly becomes exponential in $m \cdot n$. This is only useful as a correctness reference.

The key observation is that the rectangle is uniform, and the tiles are also uniform, so any valid tiling must respect global arithmetic constraints rather than local search structure. Each tile contributes exactly $k$ cells, so total area must be divisible by $k$. Beyond that, the only structural limitation comes from whether we can align strips of length $k$ along either dimension.

If we try to tile using horizontal $1 \times k$ strips, we need $n$ to be divisible by $k$. Similarly, if we tile using vertical $k \times 1$ strips, we need $m$ to be divisible by $k$. However, we are allowed to mix orientations, so we are not restricted to a single global orientation. The remaining non-trivial case is when neither dimension alone is divisible by $k$. In that case, both directions must be combined in a way that respects integer grid boundaries, which turns out to be possible only when both $m$ and $n$ are even multiples of something compatible with $k$, and the only obstruction arises when $k$ cannot be decomposed across both dimensions cleanly.

A more precise way to see the structure is to think in terms of partitioning the rectangle into blocks of size $k$. Any such block must lie entirely inside rows or columns aligned in multiples of $k$ unless it straddles both directions, which forces consistency conditions on $m \bmod k$ and $n \bmod k$. The final simplification is that the tiling is possible if and only if at least one of the dimensions can be fully partitioned into segments of length $k$, i.e., $m \bmod k = 0$ or $n \bmod k = 0$. If neither dimension is divisible by $k$, any attempt to mix orientations creates unavoidable leftover fragments that cannot be completed.

So the decision reduces to checking two simple conditions: area divisibility and at least one dimension divisible by $k$. The area condition is actually implied once one dimension is divisible, so the final check becomes straightforward.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Tiling Search | exponential | O(mn) | Too slow |
| Arithmetic + divisibility reasoning | O(1) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the values $m$, $n$, and $k$. These define the grid and tile shape.
2. If $k = 1$, immediately output "YES". Every cell is already a valid $1 \times 1$ tile, so the rectangle is always tileable.
3. Check whether $m \cdot n$ is divisible by $k$. If not, output "NO". This is necessary because each tile covers exactly $k$ cells, so total area must be an integer multiple of tile area.
4. Check whether at least one of $m$ or $n$ is divisible by $k$. If yes, output "YES". In this case, we can partition the rectangle into strips aligned with that dimension, each strip forming a valid tiling using rotated or unrotated tiles.
5. If neither dimension is divisible by $k$, output "NO". In this situation, any attempt to place $k$-length rectangles will eventually leave a remainder strip that cannot be completed.

### Why it works

Every tile always consumes exactly $k$ unit cells, so the total number of cells must be divisible by $k$. That gives a global necessary condition. The second constraint comes from alignment: without at least one dimension divisible by $k$, any decomposition into length-$k$ segments must cross boundaries in a way that leaves incompatible residual strips. If one dimension is divisible by $k$, we can partition along that dimension first, reducing the problem to independent $k$-by-1 or 1-by-$k$ strips, each trivially tileable. These two conditions together fully characterize when a perfect tiling exists.

## Python Solution

```python
import sys
input = sys.stdin.readline

m, n, k = map(int, input().split())

if k == 1:
    print("YES")
elif (m * n) % k != 0:
    print("NO")
elif m % k == 0 or n % k == 0:
    print("YES")
else:
    print("NO")
```

The code follows the decision process directly. The first condition isolates the degenerate case where tiles are single cells. The second enforces the global area constraint. The final check captures whether a clean strip decomposition exists in at least one direction, which is the structural requirement for avoiding leftover fragments.

A subtle point is the order: checking $k = 1$ first avoids unnecessary multiplication and potential overflow concerns in languages with fixed integer size, even though Python handles large integers safely.

## Worked Examples

### Example 1: $2, 3, 2$

We evaluate the conditions step by step.

| Step | m | n | k | m·n % k | m % k | n % k | Decision |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Start | 2 | 3 | 2 | - | - | - | compute |
| Area check | 2 | 3 | 2 | 6 % 2 = 0 | - | - | pass |
| Divisible dimension | 2 | 3 | 2 | - | 0 | 1 | YES |

Since $m$ is divisible by $k$, we can split the grid into vertical strips of size $2 \times 1$, each of which can be filled with rotated tiles of size $2 \times 1$. This confirms feasibility.

### Example 2: $6, 6, 4$

| Step | m | n | k | m·n % k | m % k | n % k | Decision |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Start | 6 | 6 | 4 | - | - | - | compute |
| Area check | 6 | 6 | 4 | 36 % 4 = 0 | - | - | pass |
| Divisible dimension | 6 | 6 | 4 | - | 2 | 2 | NO |

Even though total area is divisible by 4, neither dimension aligns with multiples of 4, so any placement of $1 \times 4$ or $4 \times 1$ tiles eventually creates leftover regions of width or height 2 that cannot be tiled.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(1) | Only a constant number of arithmetic operations and modulo checks |
| Space | O(1) | No additional data structures are used |

The solution fits easily within the constraints since it performs only constant-time arithmetic regardless of input magnitude.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    m, n, k = map(int, input().split())

    if k == 1:
        return "YES"
    elif (m * n) % k != 0:
        return "NO"
    elif m % k == 0 or n % k == 0:
        return "YES"
    else:
        return "NO"

# provided samples
assert run("2 3 2") == "YES"
assert run("2 3 3") == "YES"

# custom cases
assert run("1 1 2") == "NO"
assert run("4 4 2") == "YES"
assert run("6 6 4") == "NO"
assert run("5 5 1") == "YES"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 1 2 | NO | impossible due to area mismatch |
| 4 4 2 | YES | clean tiling with both dimensions even |
| 6 6 4 | NO | divisibility not sufficient |
| 5 5 1 | YES | trivial k = 1 case |

## Edge Cases

The case $k = 1$ behaves differently from all other inputs because it removes geometric constraints entirely. For input $1\ 1\ 1$, the algorithm immediately returns YES, matching the fact that the rectangle is already tiled.

When $m \cdot n$ is not divisible by $k$, such as $3\ 3\ 2$, the algorithm correctly returns NO before any structural reasoning. The execution stops at the area check, preventing any incorrect acceptance.

When neither dimension is divisible by $k$, such as $6\ 6\ 4$, the algorithm reaches the final condition and correctly returns NO. Even though 36 is divisible by 4, the absence of a clean strip decomposition forces leftover regions that cannot be covered.

When one dimension is exactly equal to $k$, such as $4\ 7\ 4$, the algorithm returns YES because $m \bmod k = 0$, and the grid can be partitioned into vertical strips of size $4 \times 1$, each tileable independently.
