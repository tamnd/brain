---
title: "CF 105404F - Painting Squares"
description: "We start with an empty grid of size $n times m$, where every cell is initially white. The only way to modify the grid is to choose whole rows or whole columns and paint them completely black."
date: "2026-06-23T04:49:47+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105404
codeforces_index: "F"
codeforces_contest_name: "XXIV Spain Olympiad in Informatics, Online Qualifier 2"
rating: 0
weight: 105404
solve_time_s: 73
verified: true
draft: false
---

[CF 105404F - Painting Squares](https://codeforces.com/problemset/problem/105404/F)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 13s  
**Verified:** yes  

## Solution
## Problem Understanding

We start with an empty grid of size $n \times m$, where every cell is initially white. The only way to modify the grid is to choose whole rows or whole columns and paint them completely black. Once a row is painted, every cell in that row becomes black; the same applies to columns.

After performing any number of such operations, we want the number of remaining white cells to be exactly $k$. Each test case gives us $n$, $m$, and this target value $k$, and we must decide whether it is achievable.

A key observation about the structure of operations is that the final configuration depends only on which rows and which columns are painted, not on the order of operations. If we paint a set of rows $R$ and a set of columns $C$, then every cell in $R$ or $C$ becomes black. The remaining white cells are exactly those outside both sets, forming a clean rectangular block of size $(n - |R|) \times (m - |C|)$.

This means the final number of white cells is always of the form

$$(n - r)(m - c)$$

for some integers $0 \le r \le n$, $0 \le c \le m$.

So the problem is no longer about operations, but about whether we can represent $k$ as the area of some sub-rectangle aligned with the grid dimensions.

From constraints, $t$ can be up to 30000, so each test must be very fast, ideally $O(1)$ or $O(\sqrt{k})$ at worst. Since $n$, $m$, and $k$ can be large, anything involving simulation over the grid or enumerating operations is impossible.

A common failure case comes from reasoning in terms of “painting sequences” instead of final geometry. For example, one might incorrectly think overlaps between row and column operations change counts in a complicated way. In reality, overlap does not matter: a cell is black if either its row or column is chosen, so the result is purely multiplicative.

Another subtle mistake is treating $k$ as arbitrary while forgetting that it must equal a rectangle area inside the grid. For instance, if $n = 3$, $m = 3$, and $k = 5$, there is no way to form a $3 \times 3$ grid area of exactly 5 remaining white cells, even though 5 might seem “reachable” via partial painting intuition.

## Approaches

A brute-force perspective would simulate all choices of painted rows and columns. For each subset of rows and columns, we compute the resulting number of white cells. This immediately becomes exponential in $n + m$, since there are $2^n \cdot 2^m$ possible states. Even for small grids this explodes, and it is unusable.

The key simplification comes from recognizing that all valid final states are determined only by how many rows and columns are fully removed. If we remove $r$ rows and $c$ columns, the remaining white region is a perfect rectangle of size $(n-r) \times (m-c)$. This transforms the problem into a pure factorization check: we are asking whether there exist integers $x \le n$ and $y \le m$ such that $x \cdot y = k$.

So the task reduces to finding whether $k$ has a divisor $x$ that fits within $n$, with the corresponding quotient $y = k/x$ fitting within $m$.

We no longer need to think about operations at all, only about divisors of $k$.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force (row/column subsets) | $O(2^{n+m})$ | $O(1)$ | Too slow |
| Check divisors of $k$ | $O(\sqrt{k})$ per test | $O(1)$ | Accepted |

## Algorithm Walkthrough

1. Observe that after choosing which rows and columns to paint, the remaining white cells form a rectangle of size $(n-r) \times (m-c)$. This reduces the problem to choosing two side lengths.
2. Reformulate the task as finding integers $x, y$ such that $x \cdot y = k$, with $x \le n$ and $y \le m$. Here $x$ represents remaining unpainted rows and $y$ remaining unpainted columns.
3. Iterate over all possible divisors $x$ of $k$. For each $x$, check whether it divides $k$ cleanly. This ensures we only consider valid rectangle dimensions.
4. For each valid divisor $x$, compute $y = k / x$, then check whether $x \le n$ and $y \le m$.
5. If no such pair works, conclude that $k$ cannot be formed as a valid rectangle area inside the grid.

### Why it works

Every valid sequence of operations corresponds exactly to choosing a set of rows and columns to remove, and that choice always produces a rectangular remaining white region. Conversely, every rectangle of size $x \times y$ inside the grid can be obtained by leaving $x$ rows and $y$ columns unpainted and painting the rest. This creates a one-to-one correspondence between feasible configurations and factor pairs of $k$ constrained by the grid dimensions, so checking all divisors is both necessary and sufficient.

## Python Solution

```python
import sys
input = sys.stdin.readline

def possible(n, m, k):
    x = 1
    while x * x <= k:
        if k % x == 0:
            y = k // x
            if x <= n and y <= m:
                return True
            if y <= n and x <= m:
                return True
        x += 1
    return False

def solve():
    t = int(input())
    out = []
    for _ in range(t):
        n, m, k = map(int, input().split())
        out.append("SI" if possible(n, m, k) else "NO")
    print("\n".join(out))

if __name__ == "__main__":
    solve()
```

The function `possible` performs a divisor scan up to $\sqrt{k}$. For each divisor $x$, it checks both orientations of the rectangle, since $x$ could represent either the remaining rows or the remaining columns.

The symmetric check is necessary because we do not know in advance whether $x$ should correspond to the $n$-dimension or the $m$-dimension. Missing this swap is a common source of wrong answers.

## Worked Examples

### Example 1

Input:

```
2 50 81
```

We try to express $81$ as $x \cdot y$ with $x \le 2$, $y \le 50$.

| x | y = 81/x | x ≤ 2 | y ≤ 50 | Valid |
| --- | --- | --- | --- | --- |
| 1 | 81 | yes | no | no |
| 3 | 27 | no | yes | no |
| 9 | 9 | no | yes | no |

No factor pair fits within the grid constraints, so the answer is NO.

### Example 2

Input:

```
29 22 546
```

We search divisors of 546.

| x | y = 546/x | x ≤ 29 | y ≤ 22 | Valid |
| --- | --- | --- | --- | --- |
| 2 | 273 | yes | no | no |
| 3 | 182 | yes | no | no |
| 6 | 91 | yes | no | no |
| 7 | 78 | yes | no | no |
| 14 | 39 | yes | no | no |
| 21 | 26 | yes | no | no |
| 22 | 24.8 | no | - | no |
| 26 | 21 | yes | yes | yes |

We find a valid pair $26 \times 21 = 546$, and both fit inside $29 \times 22$, so the answer is SI.

This trace shows that we only need one valid factor pair, not all possibilities.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(t \sqrt{k})$ | Each test scans divisors of $k$ up to $\sqrt{k}$ |
| Space | $O(1)$ | Only constant variables are used |

Even though $\sqrt{k}$ can be large in theory, the operation is simple integer arithmetic, and the total number of checks remains within typical limits for 30000 test cases in practice.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    def possible(n, m, k):
        x = 1
        while x * x <= k:
            if k % x == 0:
                y = k // x
                if x <= n and y <= m:
                    return True
                if y <= n and x <= m:
                    return True
            x += 1
        return False

    t = int(input())
    out = []
    for _ in range(t):
        n, m, k = map(int, input().split())
        out.append("SI" if possible(n, m, k) else "NO")
    return "\n".join(out)

# provided samples
assert run("3\n2 50 81\n29 22 546\n27 13 168\n") == "NO\nSI\nSI"

# minimum case
assert run("1\n1 1 1\n") == "SI"

# impossible small factor case
assert run("1\n2 2 3\n") == "NO"

# perfect rectangle case
assert run("1\n10 10 25\n") == "SI"

# large asymmetric case
assert run("1\n100 2 200\n") == "SI"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1×1 grid | SI | trivial base case |
| 2×2, k=3 | NO | non-factorable area |
| 10×10, k=25 | SI | square factor handling |
| 100×2, k=200 | SI | orientation swap |

## Edge Cases

A corner case is when $k = 1$. Even though the problem states $k \ge 2$, reasoning about it clarifies correctness: only $1 \times 1$ rectangles would be valid, meaning the grid must allow at least one untouched row and column.

Another subtle case is when $k$ is prime. For example, $k = 13$ with $n = 3$, $m = 10$. The only factorization is $1 \times 13$, which fails unless one dimension can accommodate 13. The algorithm correctly rejects all other values because no divisor other than 1 exists.

A more interesting case is when both factorizations exist but only one fits. For $n = 5$, $m = 20$, $k = 50$, we have pairs $(1,50)$, $(2,25)$, $(5,10)$, $(10,5)$. Only $(5,10)$ and $(10,5)$ are relevant, and at least one satisfies constraints, so the algorithm accepts immediately once it encounters it.
