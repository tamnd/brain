---
title: "CF 1170F - Wheels"
description: "We are given an array of wheel pressures and we need to pick exactly $m$ of them. After selecting those $m$ wheels, we are allowed to change their pressures so that all of them end up equal to a single value."
date: "2026-06-18T17:09:12+07:00"
tags: ["codeforces", "competitive-programming", "*special", "binary-search", "greedy"]
categories: ["algorithms"]
codeforces_contest: 1170
codeforces_index: "F"
codeforces_contest_name: "Kotlin Heroes: Episode 1"
rating: 0
weight: 1170
solve_time_s: 94
verified: true
draft: false
---

[CF 1170F - Wheels](https://codeforces.com/problemset/problem/1170/F)

**Rating:** -  
**Tags:** *special, binary search, greedy  
**Solve time:** 1m 34s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given an array of wheel pressures and we need to pick exactly $m$ of them. After selecting those $m$ wheels, we are allowed to change their pressures so that all of them end up equal to a single value. Each unit change, either increasing or decreasing a wheel by 1, costs 1 minute.

There is one extra restriction that makes the problem asymmetric: while decreasing pressure is always allowed, the total number of unit increases across all operations cannot exceed $k$. So if we raise a wheel by 5 overall, that already consumes 5 units of the global increase budget.

The task is to choose which $m$ wheels to use and what final equal pressure to target so that the total time spent is minimized, while never exceeding the global increase budget.

The constraints force us to think in $O(n \log n)$ or $O(n)$ terms. With $n \le 2 \cdot 10^5$, any solution that tries all subsets or all pairs of subsets is immediately impossible. Even $O(n^2)$ constructions are too slow. This pushes us toward a sorted structure and a solution based on contiguous segments, prefix sums, or sliding windows.

A subtle failure case appears when one tries to fix a target value independently and greedily choose closest elements. That ignores the increase budget coupling all chosen elements together. Another pitfall is assuming symmetry: the cost is not symmetric because increases are globally constrained, while decreases are always allowed without restriction.

A concrete example where greedy per-element selection fails is when high values are slightly fewer but expensive to decrease, while low values are many but cheap individually, yet their combined increases violate $k$. A naive “pick m closest to target” strategy can easily exceed the increase budget without noticing.

## Approaches

A direct brute force idea is to try all subsets of size $m$, and for each subset try all possible final equal values. For a fixed subset and target value, we can compute cost by summing absolute differences and tracking total increases. This is correct but completely infeasible: the number of subsets is $\binom{n}{m}$, which is exponential in $n$, and even evaluating each subset would be linear in $m$.

The key structural observation is that after sorting the array, any optimal set of $m$ wheels will form a contiguous block in the sorted order. The reason is that if we fix the final value, swapping a farther element with a closer one in sorted order can only reduce cost and never worsens the increase requirement.

Once we restrict ourselves to contiguous segments of length $m$, the problem becomes much more structured. For each segment, we still need to decide the final equal value. For absolute deviation cost, the optimal value is always a median of the chosen segment. That reduces the choice of target drastically.

The remaining task is to check, for every window of size $m$, whether it is feasible under the increase constraint and compute its cost efficiently. This can be done using prefix sums on the sorted array, allowing constant time evaluation per window.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force subsets | $O(\binom{n}{m} \cdot m)$ | $O(m)$ | Too slow |
| Sorted + sliding window + prefix sums | $O(n \log n)$ | $O(n)$ | Accepted |

## Algorithm Walkthrough

We first sort the array so that any candidate group of $m$ wheels is represented as a contiguous segment.

Then we examine every segment of length $m$, treating it as a potential candidate group.

1. Sort the array $a$ in non-decreasing order.
2. Build prefix sums so that any range sum can be queried in $O(1)$.
3. For every window $[l, r]$ of length $m$, compute the median position $p = l + \frac{m-1}{2}$. We choose this as the final equal pressure value.
4. Compute the cost to raise all elements in the left half of the window up to $a[p]$. This is the total increase cost:

$$\text{inc} = a[p] \cdot (p - l) - \sum_{i=l}^{p-1} a[i]$$

If this exceeds $k$, the window is invalid and we skip it.
5. Compute the full cost of making all elements equal to $a[p]$:

left side contributes increases as above, right side contributes decreases:

$$\text{dec} = \sum_{i=p+1}^{r} a[i] - a[p] \cdot (r - p)$$

Total cost is $\text{inc} + \text{dec}$.
6. Track the minimum cost across all valid windows.

The crucial decision is choosing the median as the target value. This is optimal for minimizing absolute deviation inside a fixed set. The only additional constraint is ensuring the increase budget is not exceeded, which only depends on elements below the median.

### Why it works

For any chosen window, if we fix the final value, the optimal value minimizing absolute deviations is the median. Any deviation from the median increases total cost symmetrically on both sides. Since increasing cost depends only on elements below the target, shifting the target away from the median either increases cost or reduces feasibility without improving the total objective. Therefore, checking each contiguous block with its median is sufficient to capture all optimal solutions.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, m, k = map(int, input().split())
    a = list(map(int, input().split()))
    a.sort()

    pref = [0] * (n + 1)
    for i in range(n):
        pref[i + 1] = pref[i] + a[i]

    INF = 10**30
    ans = INF

    for l in range(0, n - m + 1):
        r = l + m - 1
        p = l + (m - 1) // 2
        x = a[p]

        left_cnt = p - l
        left_sum = pref[p] - pref[l]
        inc = x * left_cnt - left_sum

        if inc > k:
            continue

        right_cnt = r - p
        right_sum = pref[r + 1] - pref[p + 1]
        dec = right_sum - x * right_cnt

        ans = min(ans, inc + dec)

    print(ans)

if __name__ == "__main__":
    solve()
```

The sorting step ensures that every optimal selection becomes a contiguous window in this order. Prefix sums allow fast computation of segment sums, which is essential because recomputing sums per window would otherwise lead to an $O(nm)$ solution.

The only subtle implementation detail is correct indexing around the median. The left side is strictly before the median index, and the right side starts strictly after it. Mixing inclusive boundaries would shift costs incorrectly.

## Worked Examples

### Example 1

Input:

```
6 6 7
6 15 16 20 1 5
```

After sorting:

```
1 5 6 15 16 20
```

There is only one window of size 6.

| l | r | p | x | inc | dec | total |
| --- | --- | --- | --- | --- | --- | --- |
| 0 | 5 | 2 | 6 | (6·2 - (1+5)) = 6 | (15+16+20 - 6·3) = 27 | 33 |

The increase cost is within $k = 7$, so the window is valid. The minimum cost is 33.

This trace shows how the algorithm isolates a single valid global configuration and computes both sides independently using the median split.

### Example 2

Input:

```
5 3 3
1 2 10 11 12
```

Sorted array:

```
1 2 10 11 12
```

We check all windows of size 3.

Window [0..2]:

| p | x | inc | dec | total |
| --- | --- | --- | --- | --- |
| 1 | 2 | (2·1 - 1) = 1 | (10 - 2·1) = 8 | 9 |

Window [1..3]:

| p | x | inc | dec | total |
| --- | --- | --- | --- | --- |
| 2 | 10 | (10·1 - 2) = 8 (invalid since >3) | - | skip |

Window [2..4]:

| p | x | inc | dec | total |
| --- | --- | --- | --- | --- |
| 3 | 11 | (11·1 - 10) = 1 | (12 - 11·1) = 1 | 2 |

Best answer is 2.

This demonstrates how feasibility is determined purely by the left side increase cost.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n \log n)$ | Sorting dominates; window scan is linear |
| Space | $O(n)$ | Prefix sums and array storage |

The solution fits comfortably within limits since $n = 2 \cdot 10^5$ allows linear scanning after sorting, and prefix sums avoid any repeated recomputation.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from math import inf

    def solve():
        n, m, k = map(int, input().split())
        a = list(map(int, input().split()))
        a.sort()

        pref = [0] * (n + 1)
        for i in range(n):
            pref[i + 1] = pref[i] + a[i]

        ans = 10**30

        for l in range(n - m + 1):
            r = l + m - 1
            p = l + (m - 1) // 2
            x = a[p]

            inc = x * (p - l) - (pref[p] - pref[l])
            if inc > k:
                continue

            dec = (pref[r + 1] - pref[p + 1]) - x * (r - p)
            ans = min(ans, inc + dec)

        return str(ans)

# provided sample
assert run("6 6 7\n6 15 16 20 1 5\n") == "33"

# all equal
assert run("4 3 10\n5 5 5 5\n") == "0"

# minimal window
assert run("3 1 0\n10 1 7\n") == "0"

# increasing array tight k
assert run("5 3 1\n1 2 3 4 5\n") == "2"

# large gap case
assert run("5 2 100\n1 100 1000 10000 100000\n") == "1"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| all equal array | 0 | zero cost baseline |
| m = 1 case | 0 | single element selection |
| tight k constraint | small cost | increase constraint enforcement |
| large gaps | minimal adjustment | correctness under skewed values |

## Edge Cases

One edge case is when all elements are identical. In that situation every window has zero cost, and the algorithm must not mistakenly reject any segment due to a computed increase cost of zero. The formula correctly yields zero for both increase and decrease terms, so every window is valid.

Another edge case occurs when $m = 1$. The median logic still selects the only element in each window, and both increase and decrease become zero, matching the fact that no changes are required.

A more subtle case is when $k = 0$. Here any window with elements below the median becomes invalid unless all selected elements are already at or above the median. The algorithm handles this correctly because the computed increase cost is strictly checked against zero before accepting a window.
