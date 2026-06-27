---
title: "CF 105017K - Count the squares"
description: "We are given a grid formed by unit squares, with height $N$ and width $M$. Inside this grid, we want to count how many axis-aligned squares exist, considering all possible sizes."
date: "2026-06-28T02:10:26+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105017
codeforces_index: "K"
codeforces_contest_name: "Winter Cup 4.0 Online Mirror Contest"
rating: 0
weight: 105017
solve_time_s: 41
verified: true
draft: false
---

[CF 105017K - Count the squares](https://codeforces.com/problemset/problem/105017/K)

**Rating:** -  
**Tags:** -  
**Solve time:** 41s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a grid formed by unit squares, with height $N$ and width $M$. Inside this grid, we want to count how many axis-aligned squares exist, considering all possible sizes. A square of side $k$ is valid if it fits completely inside the $N \times M$ board, and we count every distinct position where such a square can be placed.

So the task is not to find just the largest square or check existence, but to sum over all possible square sizes and all valid placements.

The input size constraints allow $N, M \le 10^6$. This immediately rules out any method that tries to enumerate squares explicitly. Even a single iteration over all grid cells is fine, but anything that attempts to consider every square individually would explode to around $O(N^2 M^2)$ in the worst case, which is far beyond feasible limits.

A common failure mode here is treating each square size independently but still iterating over all positions naively. For example, for each $k$, iterating over all $(i, j)$ and checking validity leads to $O(NM \cdot \min(N,M))$, which already becomes too large when both dimensions are large.

Another subtle issue is overflow. The number of squares grows cubically with the dimensions, roughly on the order of $N^3$, so intermediate computations must use 64-bit integers.

## Approaches

A brute-force approach is straightforward: fix a square size $k$, then slide a $k \times k$ window over the grid and count all valid positions. For a fixed $k$, there are $(N-k+1)(M-k+1)$ placements. Summing this over all $k$ from $1$ to $\min(N, M)$ gives the correct answer. This is conceptually simple and already close to the final formula.

However, computing this directly as nested loops over $k$, $i$, and $j$ degenerates into three nested loops. The total work becomes

$$\sum_{k=1}^{\min(N,M)} (N-k+1)(M-k+1),$$

which is fine mathematically but expensive if evaluated iteratively in a naive way.

The key observation is that the count for each square size is independent and follows a closed form. Instead of iterating over all placements, we directly compute how many positions exist for each size and sum them. This removes the inner loops entirely and reduces the problem to a single linear pass over possible side lengths.

We then recognize that the entire answer is just a summation over $k$, which can be computed in $O(\min(N,M))$ time.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(NM \cdot \min(N,M))$ | $O(1)$ | Too slow |
| Optimal | $O(\min(N,M))$ | $O(1)$ | Accepted |

## Algorithm Walkthrough

1. Identify the limiting dimension $L = \min(N, M)$. This is the maximum possible side length of any square. Any larger square cannot fit in the grid along at least one dimension.
2. For each possible square size $k$ from $1$ to $L$, compute the number of valid placements. A square of size $k$ can start in any row from $1$ to $N-k+1$ and any column from $1$ to $M-k+1$, so the number of positions is $(N-k+1)(M-k+1)$.
3. Accumulate this value into an answer variable. Each term contributes the number of distinct squares of that size.
4. After processing all $k$, output the accumulated sum.

The reason this direct summation works efficiently is that each square is uniquely identified by its top-left corner and side length, so there is no overlap or double counting across iterations.

### Why it works

Every valid square in the grid is uniquely determined by two choices: its side length $k$, and its top-left coordinate $(i, j)$. For a fixed $k$, valid $i$ range independently from valid $j$, and both ranges are contiguous and fully determined by the grid boundaries. The algorithm enumerates every valid pair $(k, i, j)$ exactly once through a factorized count, so no configuration is missed and none is double counted.

## Python Solution

```python
import sys
input = sys.stdin.readline

N, M = map(int, input().split())

L = min(N, M)

ans = 0
for k in range(1, L + 1):
    ans += (N - k + 1) * (M - k + 1)

print(ans)
```

The implementation directly follows the derived counting formula. The loop variable `k` represents the square side length. For each `k`, `(N - k + 1)` counts how many vertical positions the square can take, and `(M - k + 1)` counts horizontal positions. Their product gives the number of placements.

A subtle but important detail is that the loop must stop at `min(N, M)`. Continuing beyond that would produce negative contributions, which are meaningless and would corrupt the sum.

All arithmetic is done using Python integers, which naturally handle large values without overflow concerns.

## Worked Examples

### Example 1

Input:

```
2 3
```

We compute $L = 2$.

| k | N-k+1 | M-k+1 | Contribution |
| --- | --- | --- | --- |
| 1 | 2 | 3 | 6 |
| 2 | 1 | 2 | 2 |

Total sum = 8

This confirms that even a small grid already produces multiple square sizes, with size 1 dominating the count but size 2 still contributing valid placements.

### Example 2

Input:

```
4 4
```

We compute $L = 4$.

| k | N-k+1 | M-k+1 | Contribution |
| --- | --- | --- | --- |
| 1 | 4 | 4 | 16 |
| 2 | 3 | 3 | 9 |
| 3 | 2 | 2 | 4 |
| 4 | 1 | 1 | 1 |

Total sum = 30

This trace shows how larger squares contribute progressively fewer placements, forming a decreasing quadratic pattern.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(\min(N, M))$ | one loop over all possible square sizes |
| Space | $O(1)$ | only a running sum and constants |

The constraint $N, M \le 10^6$ makes a linear pass over $\min(N,M)$ acceptable. The total of $10^6$ iterations is easily within limits in Python when each iteration is a constant-time arithmetic operation.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    N, M = map(int, input().split())
    L = min(N, M)
    ans = 0
    for k in range(1, L + 1):
        ans += (N - k + 1) * (M - k + 1)
    return str(ans)

# provided samples
assert run("2 3\n") == "8"
assert run("4 4\n") == "30"

# custom cases
assert run("1 1\n") == "1", "single cell grid"
assert run("1 5\n") == "5", "only 1x1 squares possible"
assert run("2 2\n") == "5", "small symmetric grid"
assert run("3 5\n") == str(sum((3-k+1)*(5-k+1) for k in range(1,4))), "formula consistency"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 1 | 1 | minimum grid |
| 1 5 | 5 | degenerate rectangle |
| 2 2 | 5 | symmetry and small case correctness |
| 3 5 | formula-based | general correctness |

## Edge Cases

A key edge case is when one dimension is 1. For input `1 5`, only squares of size 1 exist. The algorithm sets $L = 1$, so only $k = 1$ is processed, producing $(1-1+1)(5-1+1) = 5$, which matches the fact that every cell is a valid 1×1 square.

Another edge case is the smallest possible grid `1 1`. Here $L = 1$, and the single contribution is $(1)(1) = 1$. No larger iteration occurs, so no invalid negative values are ever considered.

For square grids like `4 4`, all side lengths from 1 to 4 contribute progressively smaller counts. The algorithm naturally handles this without special casing because the factor $(N-k+1)(M-k+1)$ remains valid across the entire range.
