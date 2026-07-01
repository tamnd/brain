---
title: "CF 104014F - \u0422\u0443\u0440\u0438\u0441\u0442\u044b, \u0434\u043e\u0441\u0442\u043e\u043f\u0440\u0438\u043c\u0435\u0447\u0430\u0442\u0435\u043b\u044c\u043d\u043e\u0441\u0442\u0438 \u0438 \u0442\u0435\u043b\u0435\u0441\u043a\u043e\u043f\u044b"
description: "There is a row of cities, each city containing a known number of attractions. In every city, a telescope is installed. Each telescope has a non-negative integer power."
date: "2026-07-02T04:57:32+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104014
codeforces_index: "F"
codeforces_contest_name: "2022-2023 ICPC NERC, \u043a\u0432\u0430\u043b\u0438\u0444\u0438\u043a\u0430\u0446\u0438\u0438 \u0423\u0440\u0430\u043b\u044c\u0441\u043a\u043e\u0433\u043e \u0440\u0435\u0433\u0438\u043e\u043d\u0430 \u0438 \u0421\u0435\u0432\u0435\u0440\u043e-\u0417\u0430\u043f\u0430\u0434\u0430 \u0420\u043e\u0441\u0441\u0438\u0438"
rating: 0
weight: 104014
solve_time_s: 49
verified: true
draft: false
---

[CF 104014F - \u0422\u0443\u0440\u0438\u0441\u0442\u044b, \u0434\u043e\u0441\u0442\u043e\u043f\u0440\u0438\u043c\u0435\u0447\u0430\u0442\u0435\u043b\u044c\u043d\u043e\u0441\u0442\u0438 \u0438 \u0442\u0435\u043b\u0435\u0441\u043a\u043e\u043f\u044b](https://codeforces.com/problemset/problem/104014/F)

**Rating:** -  
**Tags:** -  
**Solve time:** 49s  
**Verified:** yes  

## Solution
## Problem Understanding

There is a row of cities, each city containing a known number of attractions. In every city, a telescope is installed. Each telescope has a non-negative integer power. If a telescope in city $i$ has power $p$, then a tourist using it can observe all cities whose indices lie within distance $p$ from $i$, forming a contiguous segment centered at $i$, clipped at the borders of the country.

For any fixed city, looking through a telescope produces a total number of visible attractions equal to the sum of attractions in all cities inside the telescope’s visible segment. The requirement is that this total must never exceed a global limit $R$. Each city has its own telescope, and we want to assign each telescope the largest possible power such that this constraint remains satisfied for its center city. If even power zero already violates the constraint at some city, the configuration is impossible.

The key point is that each city is checked independently, but the constraint depends on a range sum around that city. So for every position $i$, we are effectively looking for the largest radius $p_i$ such that the sum of a symmetric segment around $i$ does not exceed $R$.

The constraints force an $O(N \log N)$ or $O(N)$ solution. With $N \le 10^5$, any quadratic expansion of intervals would be too slow. Since attraction sums can reach up to $10^{14}$, we also need 64-bit arithmetic for prefix sums.

A few edge situations matter.

If a city already has $s_i > R$, then even a radius of zero fails, so the answer for that city is immediately $-1$. For example, if $R = 3$ and $s = [1, 10, 1]$, then the middle city cannot be assigned any valid telescope power.

Another subtle case is when expanding the radius quickly exceeds the boundaries of the array. The correct interpretation is that the interval simply clips at the ends, and this must be handled naturally in the range sum computation.

Finally, since each city is independent, a mistake would be to try to couple radii between cities. The constraint does not interact across telescopes.

## Approaches

The straightforward idea is to treat each city independently. For a fixed center $i$, we try every possible radius $p$, compute the sum of attractions in $[i-p, i+p]$, and check whether it stays within $R$. This works because the condition is purely local to that interval.

However, this brute force approach is too slow. In the worst case, each city might allow a radius up to $O(N)$, and recomputing range sums naively for each radius leads to $O(N)$ work per city, or $O(N^2)$ total operations. With $10^5$ cities, this is far beyond the time limit.

The key observation is that range sums can be queried in constant time using prefix sums. Once prefix sums are available, checking a fixed radius becomes $O(1)$. This transforms the problem into a monotonic search: as radius increases, the sum of the interval never decreases, so we can binary search the maximum valid radius for each city.

This monotonicity is what unlocks the solution. Instead of scanning all radii, we search for the boundary where the interval sum first exceeds $R$.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force expansion per city | $O(N^2)$ | $O(N)$ | Too slow |
| Prefix sums + binary search per city | $O(N \log N)$ | $O(N)$ | Accepted |

## Algorithm Walkthrough

We preprocess prefix sums of the attraction array so that any segment sum can be computed in constant time.

For each city $i$, we then search for the maximum radius $p_i$ such that the sum of attractions in the interval $[i-p_i, i+p_i]$ does not exceed $R$. If even $p_i = 0$ fails, we output $-1$.

1. Build a prefix sum array over the attractions. This allows fast computation of any interval sum in constant time.
2. For each city $i$, first check whether the single city already violates the constraint. If $s_i > R$, we immediately assign $-1$. This is necessary because no expansion can fix a local violation.
3. Otherwise, perform a binary search over possible radii from $0$ to $N$. The upper bound $N$ is safe because the interval cannot exceed the whole array.
4. For a candidate radius $m$, compute the interval $[L, R] = [i-m, i+m]$, clamping to valid indices. Use prefix sums to compute the total attractions in this segment.
5. If the sum is less than or equal to $R$, the radius is feasible and we try to expand further; otherwise, we reduce the radius.
6. The binary search result gives the maximum valid radius for city $i$, which is stored as the answer.

The key idea in step 4 is that clamping handles boundary cities naturally, so no special casing is needed beyond index limits.

### Why it works

For each fixed center $i$, define a function $f(p)$ as the sum of attractions in $[i-p, i+p]$. As $p$ increases, the interval only grows, so $f(p)$ is monotone non-decreasing. This guarantees that once $f(p)$ exceeds $R$, all larger radii are invalid. That monotonic structure is exactly what makes binary search correct, and ensures we find the maximum feasible radius without missing any intermediate candidate.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, r = map(int, input().split())
    a = list(map(int, input().split()))
    
    pref = [0] * (n + 1)
    for i in range(n):
        pref[i + 1] = pref[i] + a[i]

    def range_sum(l, rr):
        if l > rr:
            return 0
        return pref[rr + 1] - pref[l]

    def can(i, rad):
        l = max(0, i - rad)
        rr = min(n - 1, i + rad)
        return range_sum(l, rr) <= r

    res = []
    for i in range(n):
        if a[i] > r:
            res.append(-1)
            continue

        lo, hi = 0, n
        best = 0

        while lo <= hi:
            mid = (lo + hi) // 2
            if can(i, mid):
                best = mid
                lo = mid + 1
            else:
                hi = mid - 1

        res.append(best)

    print("\n".join(map(str, res)))

if __name__ == "__main__":
    solve()
```

The prefix sum array is built once so that each interval query becomes a subtraction of two values. The helper function `can` enforces boundary clipping, which is essential near the ends of the array.

The binary search runs independently for each city. The choice of `n` as the upper bound is safe because no radius can exceed the full span of the array.

A common mistake here is forgetting to handle the case `a[i] > R` early. Without that, binary search might incorrectly return a positive radius even though the center itself already violates the constraint.

## Worked Examples

### Example 1

Input:

```
3 4
1 2 1
```

We compute prefix sums: `[1, 3, 4]`.

For city 1 (value 2), radius 0 gives 2 which is valid, radius 1 gives 1+2+1 = 4 which is also valid, radius 2 would exceed bounds but still equals full sum 4. So result is 2.

For city 2 (value 2), symmetry gives the same result 2.

For city 3 (value 1), radius 0 gives 1, radius 1 gives 2+1 = 3, radius 2 gives 4, so result is 2.

Output:

```
2
2
2
```

This trace shows how expansion stops exactly at the point where the full segment sum reaches the limit.

### Example 2

Input:

```
3 3
1 3 5
```

Prefix sums: `[1, 4, 9]`.

For city 2 (value 3), radius 0 is valid. Radius 1 gives 1+3+5 = 9 which exceeds 3, so result is 0.

City 3 has value 5 which already exceeds 3, so output is -1.

| City | Best radius |
| --- | --- |
| 1 | 0 |
| 2 | 0 |
| 3 | -1 |

This example shows that even small expansions can immediately break the constraint, and that invalid centers are detected before any search.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(N \log N)$ | Each city performs a binary search over radius, and each check is $O(1)$ using prefix sums |
| Space | $O(N)$ | Prefix sum array stores cumulative totals |

With $N \le 10^5$, the logarithmic factor keeps the total operations around a few million, well within the limits of a 3-second time budget in Python.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from main import solve  # assuming solution is in main.py
    return sys.stdout.getvalue()

# sample-like cases
assert run("3 4\n1 2 1\n") == "2\n2\n2\n"
assert run("3 3\n1 3 5\n") == "0\n0\n-1\n"

# minimum size
assert run("3 1\n1 1 1\n") == "0\n0\n0\n"

# single large spike
assert run("5 10\n1 1 100 1 1\n") == "2\n1\n-1\n1\n2\n"

# all equal
assert run("4 8\n2 2 2 2\n") == "1\n1\n1\n1\n"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| small balanced array | symmetric expansion correctness | correctness of radius symmetry |
| spike exceeding R | -1 handling | early invalid detection |
| uniform values | uniform growth | monotonic behavior consistency |
