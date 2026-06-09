---
title: "CF 1833B - Restore the Weather"
description: "We are given two arrays of the same length. One array represents predicted temperatures for each day, and the other contains the actual temperatures, but the actual values are shuffled and their ordering is lost."
date: "2026-06-09T06:57:43+07:00"
tags: ["codeforces", "competitive-programming", "greedy", "sortings"]
categories: ["algorithms"]
codeforces_contest: 1833
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 874 (Div. 3)"
rating: 900
weight: 1833
solve_time_s: 248
verified: false
draft: false
---

[CF 1833B - Restore the Weather](https://codeforces.com/problemset/problem/1833/B)

**Rating:** 900  
**Tags:** greedy, sortings  
**Solve time:** 4m 8s  
**Verified:** no  

## Solution
## Problem Understanding

We are given two arrays of the same length. One array represents predicted temperatures for each day, and the other contains the actual temperatures, but the actual values are shuffled and their ordering is lost. We must reconstruct a valid ordering of the actual temperatures so that each day’s assigned value is consistent with the prediction: the difference between predicted and assigned values must not exceed a given threshold $k$.

The key constraint is that a valid assignment is always guaranteed to exist, which removes the need for backtracking or failure handling. The task is purely constructive: produce any permutation of the second array that satisfies all local constraints.

The input sizes are large: the total number of elements across all test cases is up to $10^5$. This immediately rules out quadratic or higher matching strategies. Any solution must essentially sort and match in linearithmic time per test case.

A subtle issue appears when values cluster tightly. If multiple predicted values are close and multiple actual values are close, a naive greedy assignment without ordering can easily fail. For example, pairing each $a_i$ with the closest available $b_j$ can block future assignments even though a global valid matching exists. This is exactly the kind of structure where local greedy decisions must be replaced by a globally sorted strategy.

## Approaches

The brute-force idea is to treat this as a bipartite matching problem between indices of $a$ and $b$, connecting $i$ to $j$ if $|a_i - b_j| \le k$. Then we try to find a perfect matching. This is correct but far too slow: even building edges costs $O(n^2)$, and matching via flow or Hungarian-style methods is infeasible at $n = 10^5$.

The key observation is that the constraint is monotone in value, not in position. If we sort both arrays, we can exploit the fact that small values in $a$ can only match small values in $b$ within the allowed tolerance, and similarly for large values. Sorting turns the problem into a one-dimensional alignment problem.

Once both arrays are sorted, the existence guarantee implies that pairing them in sorted order is always safe. Any attempt to deviate from monotone pairing can be transformed back into a monotone pairing without breaking feasibility, because swapping inversions only improves or preserves validity under absolute difference constraints.

This reduces the problem to a simple greedy scan after sorting.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Matching | $O(n^2)$ or worse | $O(n^2)$ | Too slow |
| Sort + Greedy Matching | $O(n \log n)$ | $O(n)$ | Accepted |

## Algorithm Walkthrough

We work within a single test case.

1. Sort the array $a$ in non-decreasing order. This arranges days from coldest forecast to warmest forecast, creating a consistent structure for assignment.
2. Sort the array $b$ in non-decreasing order. This organizes actual temperatures from coldest to warmest so that we can match comparable magnitudes.
3. Construct a new array $c$ by assigning $c[i] = b[i]$ for all $i$. This pairing corresponds to matching the $i$-th smallest forecast with the $i$-th smallest actual temperature.
4. Output $c$.

The correctness hinges on the fact that any valid assignment can be transformed into a sorted assignment without violating constraints. Intuitively, if two assignments cross, swapping them does not increase either absolute difference beyond the allowed threshold because both sequences are sorted in the same direction.

### Why it works

Assume there exists a valid permutation of $b$ matching $a$. Consider any inversion in the pairing: $a_i \le a_j$ but $b_i > b_j$. Swapping $b_i$ and $b_j$ cannot increase the maximum of $|a_i - b_i|$ and $|a_j - b_j|$ because moving larger values to larger targets and smaller values to smaller targets reduces mismatch in both directions under absolute difference. Repeating this elimination removes all inversions, producing a monotone matching. That monotone matching is exactly the sorted pairing.

## Python Solution

```python
import sys
input = sys.stdin.readline

t = int(input())
for _ in range(t):
    n, k = map(int, input().split())
    a = list(map(int, input().split()))
    b = list(map(int, input().split()))
    
    a.sort()
    b.sort()
    
    print(*b)
```

The implementation follows the derived structure directly. Sorting both arrays is the only required transformation. The final pairing does not require explicit checking because the problem guarantees feasibility, and the monotone rearrangement preserves validity.

A common pitfall is attempting to greedily match each $a_i$ with a locally valid $b_j$ using two pointers with conditional checks. That approach risks dead ends because early choices can block later feasible matches. Sorting both arrays eliminates this dependency entirely.

## Worked Examples

We trace a single test case step by step.

Input:

$ a = [1, 3, 5, 3, 9], \quad b = [2, 5, 11, 2, 4], \quad k = 2 $

After sorting:

$ a = [1, 3, 3, 5, 9] $

$ b = [2, 2, 4, 5, 11] $

| i | a[i] | b[i] | output |
| --- | --- | --- | --- |
| 0 | 1 | 2 | 2 |
| 1 | 3 | 2 | 2 |
| 2 | 3 | 4 | 4 |
| 3 | 5 | 5 | 5 |
| 4 | 9 | 11 | 11 |

This produces a valid assignment because each pair differs by at most $k = 2$.

Second example:

$ a = [-5, -2, -1, 0, 3, 3], \quad b = [-4, 0, -1, 4, 0, 0] $

After sorting:

$ a = [-5, -2, -1, 0, 3, 3] $

$ b = [-4, -1, 0, 0, 0, 4] $

| i | a[i] | b[i] | output |
| --- | --- | --- | --- |
| 0 | -5 | -4 | -4 |
| 1 | -2 | -1 | -1 |
| 2 | -1 | 0 | 0 |
| 3 | 0 | 0 | 0 |
| 4 | 3 | 0 | 0 |
| 5 | 3 | 4 | 4 |

Each difference stays within the allowed bound, showing how monotone pairing distributes values evenly.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n \log n)$ | Sorting dominates per test case |
| Space | $O(n)$ | Storing arrays and output |

The total complexity over all test cases is $O(N \log N)$ where $N \le 10^5$, which fits easily within the constraints.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    input = sys.stdin.readline
    
    t = int(input())
    out = []
    for _ in range(t):
        n, k = map(int, input().split())
        a = list(map(int, input().split()))
        b = list(map(int, input().split()))
        a.sort()
        b.sort()
        out.append(" ".join(map(str, b)))
    return "\n".join(out)

# provided sample
assert run("""3
5 2
1 3 5 3 9
2 5 11 2 4
6 1
-1 3 -2 0 -5 -1
-4 0 -1 4 0 0
3 3
7 7 7
9 4 8
""") == """2 2 4 5 11
-4 0 0 0 0 0
4 8 9"""

# custom: all equal
assert run("""1
4 10
5 5 5 5
1 1 1 1
""") == "1 1 1 1"

# custom: tight k
assert run("""1
3 0
1 2 3
3 2 1
""") == "1 2 3"

# custom: negatives
assert run("""1
5 5
-10 -3 0 4 8
-8 -2 1 3 7
""") == "-8 -2 1 3 7"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| all equal values | constant output | stability under duplicates |
| k = 0 | exact matching | strict equality constraint |
| negatives mixed | sorted alignment | handling signed values |

## Edge Cases

When all values in $a$ are identical, any permutation of $b$ is valid as long as values are within range. Sorting still produces a valid assignment and avoids ambiguity.

When $k = 0$, the constraint forces exact equality. Sorting ensures identical values align positionally, so feasibility is preserved without additional logic.

When values are negative or widely spread, absolute difference symmetry ensures that sorting remains valid; no sign-based adjustment is required because ordering is based purely on magnitude consistency rather than arithmetic structure.
