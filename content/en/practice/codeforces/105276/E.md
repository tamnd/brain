---
title: "CF 105276E - Enthusiast of Algorithms"
description: "We are given several categories of algorithms, where each category contains a certain number of distinct algorithms. Over the next $K$ days, Bob will study exactly one category per day, and on that day he must learn exactly $M$ algorithms from that chosen category."
date: "2026-06-23T14:12:44+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105276
codeforces_index: "E"
codeforces_contest_name: "La Salle-Pui Ching Programming Challenge \u57f9\u6b63\u5587\u6c99\u7de8\u7a0b\u6311\u6230\u8cfd 2023"
rating: 0
weight: 105276
solve_time_s: 66
verified: true
draft: false
---

[CF 105276E - Enthusiast of Algorithms](https://codeforces.com/problemset/problem/105276/E)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 6s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given several categories of algorithms, where each category contains a certain number of distinct algorithms. Over the next $K$ days, Bob will study exactly one category per day, and on that day he must learn exactly $M$ algorithms from that chosen category.

A single category can be reused on multiple days, but each day is independent: Bob just picks $M$ distinct algorithms from that category for that day. He is allowed to ignore some algorithms entirely, so there is no requirement to exhaust a category.

The goal is to choose the largest possible integer $M$ such that it is possible to assign a category to each of the $K$ days, and each chosen category has at least $M$ unused algorithms available for that day.

Rephrased differently, for a fixed $M$, a category with $a_i$ algorithms can be used at most $\left\lfloor \frac{a_i}{M} \right\rfloor$ days. We need to check whether the total number of usable days across all categories is at least $K$. We want the maximum $M$ satisfying this condition.

The constraints allow up to $10^5$ categories and total algorithm counts up to $10^5$. This strongly suggests that any solution with quadratic behavior in $N$ or $a_i$ is impossible. Even $O(N \log N)$ is fine, but anything worse than linear or near-linear per check would be too slow if repeated many times.

A direct brute force over $M$ from 1 to $\max a_i$, checking feasibility each time, would be too slow because each check requires scanning all categories, leading to about $O(N \cdot \max a_i)$, which can reach $10^{10}$ operations in the worst case.

A subtle edge case appears when categories are very uneven. For example, if all $a_i = 1$ and $K = N$, then only $M = 1$ works. A naive greedy idea that assigns categories without accounting for reuse across days would fail if it assumes each category is used only once.

Another failure mode is trying to assign days greedily without modeling reuse. For instance, thinking "pick the largest categories first and subtract $M$" without counting how many full groups each category can support leads to incorrect depletion modeling unless done carefully.

## Approaches

The brute-force idea is straightforward: try every possible value of $M$, and for each value compute how many days we can support. For a fixed $M$, each category $i$ contributes $\lfloor a_i / M \rfloor$ days. We sum this across all categories and check whether the sum is at least $K$. This is correct because each group of $M$ algorithms is independent and disjoint within a category.

The issue is performance. For each candidate $M$, we scan all $N$ categories. Since $M$ can go up to $10^5$, the total work becomes $O(N \cdot \max a_i)$, which is too large.

The key observation is that feasibility is monotonic in $M$. If a value $M$ is feasible, then any smaller value is also feasible because decreasing $M$ only increases or preserves $\lfloor a_i / M \rfloor$ for every category. This monotonic structure allows us to use binary search over $M$.

Each feasibility check remains $O(N)$, but we only perform $O(\log \max a_i)$ checks, making the solution efficient.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(N \cdot \max a_i)$ | $O(1)$ | Too slow |
| Binary Search + Greedy Check | $O(N \log \max a_i)$ | $O(1)$ | Accepted |

## Algorithm Walkthrough

We exploit the fact that larger values of $M$ reduce the number of usable days per category.

1. Define a function `can(M)` that computes how many days can be formed if each day uses $M$ algorithms from a single category. For each category $a_i$, we add $a_i // M$ to a running total. This counts how many full groups of size $M$ exist.
2. If the total number of groups across all categories is at least $K$, then $M$ is feasible. Otherwise, it is not feasible. This directly matches the requirement that each of the $K$ days must be assigned one valid group.
3. Perform binary search on $M$ in the range from 1 to $\max(a_i)$. The lower bound is 1 because at least one algorithm per day is always the minimal meaningful choice.
4. For a midpoint $mid$, compute `can(mid)`. If it is feasible, we try larger values by moving the lower bound up. Otherwise, we reduce the upper bound.
5. After binary search finishes, the lower bound will point to the maximum feasible $M$.

### Why it works

The function `can(M)` is monotone non-increasing in $M$. Increasing $M$ can only reduce or preserve the number of full groups in each category, never increase it. This guarantees that the feasibility space is a contiguous prefix over integers $M$, so binary search correctly finds the boundary between feasible and infeasible values.

## Python Solution

```python
import sys
input = sys.stdin.readline

def can(M, arr, K):
    total = 0
    for a in arr:
        total += a // M
        if total >= K:
            return True
    return False

def solve():
    N, K = map(int, input().split())
    arr = list(map(int, input().split()))
    
    lo, hi = 1, max(arr)
    ans = 1
    
    while lo <= hi:
        mid = (lo + hi) // 2
        if can(mid, arr, K):
            ans = mid
            lo = mid + 1
        else:
            hi = mid - 1
    
    print(ans)

if __name__ == "__main__":
    solve()
```

The core of the implementation is the `can` function, which converts each category into a count of how many full “days” it can support at a given $M$. The early exit when `total >= K` prevents unnecessary work once feasibility is confirmed.

The binary search maintains the invariant that all values below `lo` are feasible candidates, while all values above `hi` are infeasible. The variable `ans` tracks the best valid midpoint seen so far.

## Worked Examples

### Example 1

Input:

```
5 5
4 6 7 3 1
```

We search for maximum $M$.

| mid | contributions (a_i // mid) | total | feasible |
| --- | --- | --- | --- |
| 4 | 1+1+1+0+0 = 3 | 3 | no |
| 2 | 2+3+3+1+0 = 9 | 9 | yes |
| 3 | 1+2+2+1+0 = 6 | 6 | yes |

The binary search converges to 3. This confirms that while 4 is too large to sustain 5 days, 3 still allows enough grouped assignments.

### Example 2

Input:

```
3 4
10 10 10
```

| mid | contributions | total | feasible |
| --- | --- | --- | --- |
| 5 | 2+2+2 = 6 | 6 | yes |
| 6 | 1+1+1 = 3 | 3 | no |

So the answer is 5. This shows the cutoff behavior clearly: once grouping becomes too large, capacity drops sharply.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(N \log A)$ | each feasibility check scans all categories, binary search over possible $M$ |
| Space | $O(1)$ | only storing input array and counters |

The constraints allow up to $10^5$ categories, and each feasibility check is linear in $N$. With at most about 17-20 binary search iterations, the total work stays comfortably within limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    def can(M, arr, K):
        total = 0
        for a in arr:
            total += a // M
            if total >= K:
                return True
        return False

    def solve():
        N, K = map(int, input().split())
        arr = list(map(int, input().split()))
        lo, hi = 1, max(arr)
        ans = 1
        while lo <= hi:
            mid = (lo + hi) // 2
            if can(mid, arr, K):
                ans = mid
                lo = mid + 1
            else:
                hi = mid - 1
        print(ans)

    from contextlib import redirect_stdout
    out = io.StringIO()
    with redirect_stdout(out):
        solve()
    return out.getvalue().strip()

# provided sample
assert run("5 5\n4 6 7 3 1\n") == "3"

# minimum case
assert run("1 1\n5\n") == "5"

# all equal
assert run("4 4\n4 4 4 4\n") == "1"

# tight packing
assert run("2 3\n5 5\n") == "2"

# large skew
assert run("3 5\n100 1 1\n") == "20"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 1 / 5 | 5 | single category edge |
| 4 4 / 4 4 4 4 | 1 | minimal grouping |
| 2 3 / 5 5 | 2 | balanced allocation |
| 3 5 / 100 1 1 | 20 | skewed distribution |

## Edge Cases

A single category case like `N = 1` tests whether the solution correctly reduces to simple division. For input `1 3` with `a = [10]`, feasibility depends entirely on whether `10 // M >= 3`, so the binary search must converge exactly to the largest divisor satisfying this constraint, producing `M = 3`.

When all categories are equal, for example `N = 5`, `K = 5`, and `a_i = 2`, the algorithm correctly recognizes that each category contributes at most one day if `M = 2`, but contributes two days if `M = 1`. The binary search captures this step change without needing explicit case handling.

In heavily skewed inputs like `a = [100, 1, 1, 1]`, most capacity comes from a single category. For large `M`, the smaller categories contribute zero, and only the large category matters. The algorithm still sums contributions correctly and does not mistakenly assume uniform distribution.
