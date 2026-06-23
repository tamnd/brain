---
title: "CF 105472H - Hot Hike"
description: "We are given a sequence of daily temperatures covering a vacation of length $n$. We must choose a continuous block of exactly three consecutive days: the first day is hiking up to a lake, the second day is rest (ignored for heat considerations), and the third day is hiking back."
date: "2026-06-23T18:05:17+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105472
codeforces_index: "H"
codeforces_contest_name: "2019-2020 ACM-ICPC Nordic Collegiate Programming Contest (NCPC 2019)"
rating: 0
weight: 105472
solve_time_s: 46
verified: true
draft: false
---

[CF 105472H - Hot Hike](https://codeforces.com/problemset/problem/105472/H)

**Rating:** -  
**Tags:** -  
**Solve time:** 46s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a sequence of daily temperatures covering a vacation of length $n$. We must choose a continuous block of exactly three consecutive days: the first day is hiking up to a lake, the second day is rest (ignored for heat considerations), and the third day is hiking back. Only the two hiking days matter, and the discomfort of a trip is defined as the maximum temperature among those two hiking days.

So for every valid starting day $d$, we look at the pair of temperatures $(t_d, t_{d+2})$, and we want to minimize $\max(t_d, t_{d+2})$. The output is the best starting day and the corresponding minimized value of this maximum. If multiple starting days achieve the same minimum value, we choose the smallest starting day index.

The constraint $3 \le n \le 50$ immediately tells us that even a quadratic or cubic solution would run easily within limits. A direct scan over all possible starting days is already sufficient. There is no need for advanced data structures or optimizations.

A subtle edge case comes from tie-breaking. If two starting positions produce the same maximum hiking temperature, we must pick the earliest one. For example, if temperatures are $[10, 1, 10, 1]$, then starting at day 1 gives max $10$, and starting at day 2 gives max $10$ as well, but we must output day 1.

Another edge case is when the best solution occurs at the very end of the array. Since we access $d+2$, the last valid starting day is $n-2$. A common mistake is iterating up to $n-1$, which would index out of bounds or ignore valid candidates.

## Approaches

A brute-force approach tries every possible starting day $d$ from 1 to $n-2$. For each $d$, it computes the maximum of the two hiking-day temperatures $t_d$ and $t_{d+2}$, and keeps track of the minimum value seen so far. This is correct because every valid trip is considered exactly once.

The cost of this approach is $O(n)$, since each candidate is evaluated in constant time and there are $n-2$ candidates. Even if we extended the problem to check more complex patterns, this sliding-window enumeration remains cheap.

There is no meaningful optimization beyond this because each starting day is independent. The structure of the problem is already minimal: a fixed-size window with a simple aggregation over two endpoints. The key observation is that the middle day is irrelevant, so we never need to consider it in computation.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(n)$ | $O(1)$ | Accepted |
| Optimal | $O(n)$ | $O(1)$ | Accepted |

In fact, the “optimal” solution is just the brute-force scan with clean bookkeeping.

## Algorithm Walkthrough

We process all valid starting positions and compute the cost of each candidate trip.

1. Initialize variables to store the best answer: a large value for the minimum temperature and a placeholder for the best starting day. We use a very large initial value so that any real temperature will improve it.
2. Iterate over all starting days $d$ from 0 to $n-3$ in zero-based indexing. This ensures both $d$ and $d+2$ are valid indices.
3. For each $d$, compute the value $v = \max(t[d], t[d+2])$. This represents the worst hiking-day temperature for that trip.
4. If $v$ is strictly smaller than the best value seen so far, update both the best value and the best starting day to $d$. We also implicitly handle tie-breaking by only updating on strict improvement, which preserves the earliest index.
5. After finishing the scan, output the best starting day converted back to one-based indexing, along with the best value.

### Why it works

Each valid trip corresponds to exactly one index $d$, and the cost of that trip depends only on two fixed elements $t[d]$ and $t[d+2]$. Since we evaluate all such pairs exactly once and always retain the minimum over all candidates, the stored answer is globally optimal. Tie-breaking correctness follows from never overwriting an equal value once the first occurrence has been recorded.

## Python Solution

```python
import sys
input = sys.stdin.readline

n = int(input())
t = list(map(int, input().split()))

best_val = float('inf')
best_d = 0

for d in range(n - 2):
    val = max(t[d], t[d + 2])
    if val < best_val:
        best_val = val
        best_d = d

print(best_d + 1, best_val)
```

The core loop directly implements the enumeration of all valid starting days. The use of zero-based indexing simplifies boundary handling, since we naturally stop at $n-3$. The condition `val < best_val` enforces both minimization and correct tie-breaking, because earlier indices are never replaced by equal ones.

## Worked Examples

### Example 1

Input:

```
5
23 27 31 28 30
```

We evaluate all valid starts:

| d (0-based) | t[d] | t[d+2] | max |
| --- | --- | --- | --- |
| 0 | 23 | 31 | 31 |
| 1 | 27 | 28 | 28 |
| 2 | 31 | 30 | 31 |

The best value is 28 at $d = 1$, so output is:

```
2 28
```

This shows how skipping the middle day allows a better pairing that is not obvious from local minima alone.

### Example 2

Input:

```
4
30 20 20 30
```

| d | t[d] | t[d+2] | max |
| --- | --- | --- | --- |
| 0 | 30 | 20 | 30 |
| 1 | 20 | 30 | 30 |

Both choices give the same value 30, but we select the smallest starting index $d=0$, producing:

```
1 30
```

This confirms the tie-breaking rule is handled purely by the strict improvement condition.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n)$ | We evaluate each valid starting day once, computing a constant-time max |
| Space | $O(1)$ | Only a few variables are used regardless of input size |

With $n \le 50$, this is far below any practical limit, and even for much larger $n$, the linear scan remains optimal.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys as _sys
    from io import StringIO as _StringIO

    backup = _sys.stdin
    _sys.stdin = _StringIO(inp)

    n = int(input())
    t = list(map(int, input().split()))

    best_val = float('inf')
    best_d = 0

    for d in range(n - 2):
        val = max(t[d], t[d + 2])
        if val < best_val:
            best_val = val
            best_d = d

    _sys.stdin = backup
    return f"{best_d + 1} {best_val}"

assert run("5\n23 27 31 28 30\n") == "2 28"
assert run("4\n30 20 20 30\n") == "1 30"

# minimum size
assert run("3\n10 1 10\n") == "1 10"

# all equal
assert run("5\n5 5 5 5 5\n") == "1 5"

# decreasing
assert run("5\n40 30 20 10 0\n") == "3 20"

# increasing
assert run("5\n0 10 20 30 40\n") == "1 20"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 3-day alternating | 1 10 | minimum valid length |
| all equal | 1 5 | tie-breaking stability |
| decreasing sequence | 3 20 | best near end boundary |
| increasing sequence | 1 20 | best at start boundary |

## Edge Cases

For the minimum case $n = 3$, there is exactly one possible trip. The algorithm evaluates only $d = 0$, computing $\max(t[0], t[2])$. There is no ambiguity, and the loop executes exactly once.

For constant arrays like $[5,5,5,5,5]$, every candidate produces the same value. Because we only update on strict improvement, the first index remains selected, ensuring correct tie-breaking without any explicit comparison on indices.

For boundary-heavy cases such as strictly increasing sequences, the optimal solution is always at $d = 0$, since later positions pair with even larger values at $d+2$. The scan naturally preserves this without special handling.

For strictly decreasing sequences, the best choice shifts toward the end where both endpoints are smallest. Since the loop includes $d = n-3$, the final candidate is always considered, preventing off-by-one errors.
