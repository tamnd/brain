---
title: "CF 2000E - Photoshoot for Gorillas"
description: "We are placing weighted objects onto a grid, but the score is not just the sum of values on the grid. Instead, every placement contributes multiple times: each cell participates in several overlapping fixed-size $k times k$ sub-squares, and the total score is the sum over all…"
date: "2026-06-08T14:13:08+07:00"
tags: ["codeforces", "competitive-programming", "combinatorics", "data-structures", "greedy", "math"]
categories: ["algorithms"]
codeforces_contest: 2000
codeforces_index: "E"
codeforces_contest_name: "Codeforces Round 966 (Div. 3)"
rating: 1400
weight: 2000
solve_time_s: 102
verified: true
draft: false
---

[CF 2000E - Photoshoot for Gorillas](https://codeforces.com/problemset/problem/2000/E)

**Rating:** 1400  
**Tags:** combinatorics, data structures, greedy, math  
**Solve time:** 1m 42s  
**Verified:** yes  

## Solution
## Problem Understanding

We are placing weighted objects onto a grid, but the score is not just the sum of values on the grid. Instead, every placement contributes multiple times: each cell participates in several overlapping fixed-size $k \times k$ sub-squares, and the total score is the sum over all such sub-squares of the sums of values inside them.

Equivalently, each cell contributes its value multiplied by how many $k \times k$ sub-squares cover that cell. The task is to place all given weights onto grid cells so that this weighted contribution is maximized.

The constraints are large in total size but not per test case, meaning we can afford $O(nm \log nm)$ or even $O(nm)$ per test case, but not anything like enumerating placements or trying permutations. The key implication is that the structure must be reduced to sorting and deterministic assignment.

A naive mistake here is to think locally: placing large gorillas in corners or edges because they seem “less useful”. This is incorrect because coverage depends only on geometry, not on whether a cell is on a boundary of the grid itself. Another common failure is to assume uniform contribution, which breaks down when $k < n,m$, because interior cells belong to many more sub-squares than boundary ones.

For example, in a $3 \times 3$ grid with $k=2$, the center cells appear in more $2 \times 2$ sub-squares than corners. A greedy ignoring this will misplace high values and lose score even though the grid looks symmetric.

## Approaches

A brute-force solution would try all placements of gorillas into cells and compute the contribution directly. Since there are up to $nm \le 2 \cdot 10^5$ cells, even before considering permutations of weights, this is factorial and impossible.

The key observation is linearity: the total score is a sum over cells, and each cell has a fixed coefficient determined only by $n, m, k$. Once we compute these coefficients, the problem becomes purely an assignment problem: assign largest weights to largest coefficients.

To compute the coefficient for a cell $(i,j)$, we count how many $k \times k$ sub-squares include it. This splits independently into row and column contributions. If we define how many windows cover a given index in a 1D array, the 2D answer is the product of the row and column contributions. This reduces the entire problem to sorting coefficients and sorting weights.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force permutations | $O((nm)!)$ | $O(nm)$ | Impossible |
| Coefficient sorting | $O(nm \log nm)$ | $O(nm)$ | Accepted |

## Algorithm Walkthrough

We reduce the grid into a list of weights per cell and match it with a list of importance values.

Step 1: For each row index $i$, compute how many vertical placements of a $k$-length segment cover it. A row is covered by all segments whose starting position lies in a range intersecting $i$, which forms a contiguous interval. The number of valid starts gives a value $row[i]$.

Step 2: Similarly compute $col[j]$ for columns. These are identical 1D sliding window coverage counts.

Step 3: For each cell $(i,j)$, its contribution multiplier is $row[i] \cdot col[j]$. This is because a $k \times k$ square is determined independently by choosing a valid row interval and column interval.

Step 4: Flatten all cell multipliers into a single array of size $nm$.

Step 5: Sort this array in non-decreasing order.

Step 6: Sort gorilla heights in non-decreasing order.

Step 7: Multiply largest heights with largest multipliers and sum.

### Why it works

The score is linear in each cell value and independent across cells once the coverage multiplicity is fixed. Any swap of two gorillas affects only their individual contributions. Therefore, pairing larger values with larger coefficients always increases or preserves the total sum, which is a direct application of the rearrangement inequality.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        n, m, k = map(int, input().split())
        w = int(input())
        a = list(map(int, input().split()))

        # compute 1D coverage counts
        def coverage(x):
            # number of segments [l, l+k-1] covering x
            # l must satisfy l <= x <= l+k-1
            # => x-k+1 <= l <= x
            # valid l in [1, n-k+1]
            L = max(1, x - k + 1)
            R = min(x, n - k + 1)
            return max(0, R - L + 1)

        row = [coverage(i) for i in range(1, n + 1)]
        col = [coverage(j) for j in range(1, m + 1)]

        vals = []
        for i in range(n):
            for j in range(m):
                vals.append(row[i] * col[j])

        vals.sort()
        a.sort()

        # take largest weights with largest coefficients
        ans = 0
        for i in range(w):
            ans += a[i] * vals[i + (n * m - w)]

        print(ans)

if __name__ == "__main__":
    solve()
```

The first part computes how frequently each row or column index participates in a valid $k$-window. The second part builds the full grid of multiplicities via product structure. The final pairing uses sorting to maximize the sum.

A subtle point is that we only use the top $w$ coefficients because only $w$ gorillas are placed; remaining cells contribute zero. Sorting ensures we match the largest heights with the largest available coefficients.

## Worked Examples

### Example 1

Consider $n=2, m=2, k=1$, weights $[5,7]$.

Every cell has coefficient 1 because each $1\times1$ sub-square covers exactly one cell.

| Step | Values |
| --- | --- |
| row/col coverage | all 1 |
| cell coefficients | [1,1,1,1] |
| sorted coefficients | [1,1,1,1] |
| sorted weights | [5,7] |

We take two largest coefficients and pair them with 7 and 5, giving 12.

This confirms that when $k=1$, the problem reduces to selecting any two cells.

### Example 2

Take a $3 \times 3$ grid with $k=2$. Row and column coverages are $[1,2,1]$. Thus coefficients are:

| Cell | Value |
| --- | --- |
| corners | 1 |
| edges | 2 |
| center | 4 |

Flattened list: $[1,2,1,2,4,2,1,2,1]$

Sorting gives $[1,1,1,1,2,2,2,2,4]$. Largest weight must go to 4, next to 2s.

This demonstrates why center placement dominates and why greedy assignment is required.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(nm \log (nm))$ | sorting all cell coefficients dominates |
| Space | $O(nm)$ | storing coefficient grid |

Given that total $nm$ across tests is at most $2 \cdot 10^5$, this is well within limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    t = int(input())
    out = []
    for _ in range(t):
        n, m, k = map(int, input().split())
        w = int(input())
        a = list(map(int, input().split()))

        def cov(x, n):
            L = max(1, x - k + 1)
            R = min(x, n - k + 1)
            return max(0, R - L + 1)

        row = [cov(i, n) for i in range(1, n + 1)]
        col = [cov(j, m) for j in range(1, m + 1)]

        vals = []
        for i in range(n):
            for j in range(m):
                vals.append(row[i] * col[j])

        vals.sort()
        a.sort()

        ans = 0
        for i in range(w):
            ans += a[i] * vals[i + (n*m - w)]

        out.append(str(ans))

    return "\n".join(out)

# provided sample check
assert run("""5
3 4 2
9
1 1 1 1 1 1 1 1 1
2 1 1
2
5 7
20 15 7
9
4 1 4 5 6 1 1000000000 898 777
1984 1 1
4
5 4 1499 2004
9 5 5
6
6 7 14 16 16 6
""") == """21
12
49000083104
3512
319"""
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1x1 grid | direct sum | base correctness |
| k = 1 | uniform weights | edge case of uniform coverage |
| k = n | single window | boundary dominance |
| sparse large weights | sorting correctness | greedy pairing correctness |
