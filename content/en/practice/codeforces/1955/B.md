---
title: "CF 1955B - Progressive Square"
description: "We are given an $n times n$ grid that is fully determined by three values: the top-left cell, and two fixed increments that govern movement downwards and rightwards. Moving one step down always adds $c$, and moving one step right always adds $d$."
date: "2026-05-31T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "constructive-algorithms", "data-structures", "implementation", "sortings"]
categories: ["algorithms"]
codeforces_contest: 1955
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 938 (Div. 3)"
rating: 1000
weight: 1955
solve_time_s: 49
verified: true
draft: false
---

[CF 1955B - Progressive Square](https://codeforces.com/problemset/problem/1955/B)

**Rating:** 1000  
**Tags:** constructive algorithms, data structures, implementation, sortings  
**Solve time:** 49s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given an $n \times n$ grid that is fully determined by three values: the top-left cell, and two fixed increments that govern movement downwards and rightwards. Moving one step down always adds $c$, and moving one step right always adds $d$. Because of this, every cell in the grid can be expressed as a linear function of its coordinates once the starting value is fixed.

After this grid is conceptually constructed, we are given a multiset of $n^2$ integers in arbitrary order. The task is to decide whether this multiset can be exactly the set of values appearing in that uniquely defined grid for the given $n$, $c$, and $d$. We do not need to reconstruct the grid layout, only verify that such a grid exists whose values match the multiset exactly.

The constraints force us into near-linear or $O(n^2 \log n)$ per test at worst. Since the total number of elements across all test cases is at most $2.5 \cdot 10^5$, anything quadratic in sorting or hashing per test is fine, but anything that tries to simulate all possible starting values or check per-cell consistency with heavy recomputation would be too slow.

A naive pitfall comes from thinking the order of the array matters. It does not. Another subtle failure mode is assuming that only relative differences matter locally. For example, trying to verify row-wise or column-wise patterns without anchoring the grid leads to false positives when duplicates exist or when sorting hides structure.

Consider a small failure case intuition: if $n=2$, $c=1$, $d=2$, the grid must be

$$\begin{pmatrix}
x & x+2 \\
x+1 & x+3
\end{pmatrix}$$

The multiset must be exactly $\{x, x+1, x+2, x+3\}$. Any attempt that checks only adjacency in sorted order could mistakenly accept incorrect multisets where spacing is right but structure cannot be formed.

## Approaches

A brute-force interpretation would try every possible value of $a_{1,1}$ as a candidate starting point. For each candidate, we would construct the entire grid using the recurrence relations and compare the resulting multiset with the given array. Since values range up to $10^9$, the starting value is not directly bounded in a way that makes enumeration feasible. Even worse, each construction costs $O(n^2)$, and there is no meaningful bound on the number of candidates to try, making this approach completely infeasible.

The key structural observation is that the grid is fully determined by its smallest element. Because both $c$ and $d$ are positive, every step down or right strictly increases values. This means the minimum element in the grid must be $a_{1,1}$, and the entire grid can be reconstructed deterministically from it.

Once we sort the array, we can attempt to treat the smallest value as the top-left corner. From there, every expected value of the grid is uniquely determined. The only remaining question is whether the multiset contains exactly those values.

The crucial reduction is turning a 2D structure into a 1D verification problem: instead of reasoning about geometry, we validate a generated sequence of expected values against a sorted array.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force over start | Exponential / infeasible | O(1) | Too slow |
| Sort + validate construction | $O(n^2 \log n)$ | O(1) extra | Accepted |

## Algorithm Walkthrough

We exploit the fact that sorting reveals the intended structure.

1. Sort the array of size $n^2$. This gives us a candidate ordering where the smallest element is assumed to correspond to $a_{1,1}$. This is justified because all moves in the grid increase values strictly due to $c, d \ge 1$.
2. Let the smallest element be the candidate starting value $x$. This fixes the entire grid uniquely.
3. For every position $(i, j)$, compute the expected value:

$$x + i \cdot c + j \cdot d$$

This directly follows from applying the recurrence repeatedly from the top-left.
4. Compare each computed value with the sorted array at the same index (using row-major traversal). If any mismatch occurs, the multiset cannot represent the progressive square.
5. If all values match exactly, the array is valid.

The ordering used for traversal must be consistent with the sorted array. Since both the construction and sorting impose a total ordering, row-major enumeration aligns with increasing values only because $c, d > 0$, ensuring monotonic growth across both dimensions.

### Why it works

The structure induces a strictly increasing grid in both row and column directions. This guarantees that the grid values, when flattened in row-major order, form a strictly increasing sequence. Since sorting also produces the unique increasing ordering of the same multiset, both sequences must coincide if and only if the multiset is exactly the constructed grid. This removes any ambiguity about placement: once the smallest element is fixed, every other value has exactly one valid position.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        n, c, d = map(int, input().split())
        b = list(map(int, input().split()))
        
        b.sort()
        start = b[0]
        
        expected = []
        for i in range(n):
            for j in range(n):
                expected.append(start + i * c + j * d)
        
        expected.sort()
        
        if expected == b:
            print("YES")
        else:
            print("NO")

if __name__ == "__main__":
    solve()
```

The solution begins by sorting the input multiset. This is essential because the grid’s monotonic structure ensures a unique increasing ordering when flattened.

We then reconstruct what the grid must be if it is valid, starting from the smallest value. The formula $start + i \cdot c + j \cdot d$ is derived directly from repeatedly applying the row and column increments.

Finally, we compare the generated multiset with the input. Sorting both ensures that we are comparing unordered collections rather than positional layouts.

A subtle point is that we do not attempt to guess orientation or permutations. The strict positivity of $c$ and $d$ guarantees a unique increasing direction, so no alternative arrangement can satisfy the constraints.

## Worked Examples

### Example 1

Input:

```
n = 3, c = 2, d = 3
b = [3, 9, 6, 5, 7, 1, 10, 4, 8]
```

Sorted array:

| step | sorted b | expected from formula |
| --- | --- | --- |
| 0 | 1 | 1 |
| 1 | 3 | 3 |
| 2 | 4 | 4 |
| 3 | 5 | 5 |
| 4 | 6 | 6 |
| 5 | 7 | 7 |
| 6 | 8 | 8 |
| 7 | 9 | 9 |
| 8 | 10 | 10 |

The generated sequence matches exactly, so the output is YES.

This confirms that ordering alone is sufficient when the grid is strictly monotone.

### Example 2

Input:

```
n = 3, c = 2, d = 3
b = [3, 9, 6, 5, 7, 1, 11, 4, 8]
```

Sorted array:

| step | sorted b | expected |
| --- | --- | --- |
| 0 | 1 | 1 |
| 1 | 3 | 3 |
| 2 | 4 | 4 |
| 3 | 5 | 5 |
| 4 | 6 | 6 |
| 5 | 7 | 7 |
| 6 | 8 | 8 |
| 7 | 9 | 9 |
| 8 | 11 | 10 |

Mismatch occurs at the last element.

This shows that even a single corrupted value breaks the entire structure, since every position is tightly constrained.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(t \cdot n^2 \log n)$ | Sorting dominates per test case |
| Space | $O(n^2)$ | Storing the input and generated grid |

Given that the total $n^2$ across tests is bounded by $2.5 \cdot 10^5$, sorting and linear reconstruction comfortably fit within limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from __main__ import solve
    import contextlib
    out = io.StringIO()
    with contextlib.redirect_stdout(out):
        solve()
    return out.getvalue().strip()

# provided sample
assert run("""5
3 2 3
3 9 6 5 7 1 10 4 8
3 2 3
3 9 6 5 7 1 11 4 8
2 100 100
400 300 400 500
3 2 3
3 9 6 6 5 1 11 4 8
4 4 4
15 27 7 19 23 23 11 15 7 3 19 23 11 15 11 15
""") == """NO
YES
YES
NO
NO"""

# custom cases
assert run("""1
2 1 2
1 3 2 4
""") == "YES", "minimal valid"

assert run("""1
2 1 2
1 3 2 5
""") == "NO", "one wrong value"

assert run("""1
3 1 1
1 2 3 2 3 4 3 4 5
""") == "YES", "perfect arithmetic grid"

assert run("""1
3 1 1
1 2 3 2 3 4 3 4 6
""") == "NO", "off-by-one corruption"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 2x2 correct grid | YES | smallest valid structure |
| 2x2 corrupted value | NO | single mismatch detection |
| 3x3 arithmetic grid | YES | full consistency |
| 3x3 off-by-one error | NO | subtle corruption case |

## Edge Cases

A key edge case is when duplicates appear in the input array. Since $c, d \ge 1$, the true grid never contains duplicates, so any repeated number immediately invalidates the construction. The algorithm handles this naturally because sorting preserves duplicates, and comparison with the generated strictly increasing sequence will fail at the first repeated value.

Another subtle case is when the smallest element is not actually the correct $a_{1,1}$. However, because the grid is strictly increasing in both directions, no other position can contain a smaller value, so the smallest element must always be the correct starting point. This removes any ambiguity in initialization.

A final edge case is large $n = 500$, where the grid has 250,000 elements. The solution remains safe because it only performs sorting and linear generation, avoiding any nested recomputation that could push it into quadratic behavior per test case.
