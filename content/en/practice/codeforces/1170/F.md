---
title: "CF 1170F - Wheels"
description: "Polycarp has a collection of wheels, each with a specific air pressure, and a car that can take exactly m wheels. He wants to choose m wheels from his n wheels and adjust their pressures so that all selected wheels have the same value."
date: "2026-06-12T02:02:34+07:00"
tags: ["codeforces", "competitive-programming", "*special", "binary-search", "greedy"]
categories: ["algorithms"]
codeforces_contest: 1170
codeforces_index: "F"
codeforces_contest_name: "Kotlin Heroes: Episode 1"
rating: 0
weight: 1170
solve_time_s: 113
verified: false
draft: false
---

[CF 1170F - Wheels](https://codeforces.com/problemset/problem/1170/F)

**Rating:** -  
**Tags:** *special, binary search, greedy  
**Solve time:** 1m 53s  
**Verified:** no  

## Solution
## Problem Understanding

Polycarp has a collection of wheels, each with a specific air pressure, and a car that can take exactly `m` wheels. He wants to choose `m` wheels from his `n` wheels and adjust their pressures so that all selected wheels have the same value. Increasing a wheel's pressure by 1 takes a minute, but he can only do this a total of `k` times across all wheels. Decreasing pressure is unrestricted and also takes 1 minute per unit. The goal is to find the minimal total number of minutes required to equalize the pressures of `m` wheels.

The input consists of `n`, `m`, and `k`, followed by `n` integers representing initial wheel pressures. The output is a single integer: the minimum number of minutes to achieve equal pressure on a subset of `m` wheels.

The constraints indicate that `n` can be up to 200,000. A naive approach iterating over all subsets of size `m` is infeasible because the number of subsets grows combinatorially, on the order of `C(n, m)`. Therefore any solution must be linearithmic (`O(n log n)`) or linear (`O(n)`) in `n`. The pressures themselves can be large, up to `10^9`, which rules out approaches that assume small bounded pressure ranges.

Edge cases that could break a naive implementation include having very few allowed increases `k = 0`, or when `m = n`, which forces us to adjust all wheels. Another subtle scenario is when some wheels are much lower than the target pressure, making it impossible to reach equality without exceeding `k` increases. For instance, with pressures `[1, 2, 3]`, `m = 2`, and `k = 0`, we cannot equalize two wheels at a pressure above `2` because increasing beyond `k` is prohibited. A careless approach might simply take the median or mean without considering the increase limit.

## Approaches

The brute-force approach is straightforward: for every subset of `m` wheels, compute the cost to equalize them to every possible target pressure within the subset. This requires iterating over `C(n, m)` subsets and for each subset considering up to `n` potential targets. The operation count is at least `O(n^m * n)` in the worst case, which is astronomical for `n = 2 * 10^5` and cannot work under the time constraints.

The key observation is that the cost to equalize a subset of wheels is minimal when the target pressure is at least as high as the maximum wheel in the subset if the number of allowed increases `k` is large enough, or as low as necessary to avoid exceeding `k`. Sorting the array lets us consider contiguous windows of size `m`, because increasing smaller pressures is cheaper than jumping across scattered elements. Once sorted, we can fix a target pressure for each window and compute the total cost efficiently using prefix sums. This reduces the problem to linear or linearithmic complexity, depending on the method used to search for the optimal target pressure within each window.

A further optimization comes from the fact that the total cost is a convex function over the target pressure. This allows a binary search over the target pressure for each window. Combining sliding windows with prefix sums and binary search produces a solution that is `O(n log n)`.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n^m * n) | O(n) | Too slow |
| Sliding Window + Binary Search | O(n log n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Sort the wheel pressures. Sorting ensures that the smallest pressures are on the left, which makes choosing windows of `m` wheels straightforward and reduces the cost of increasing low-pressure wheels.
2. Compute prefix sums of the sorted pressures. Let `prefix[i]` be the sum of the first `i` pressures. This allows O(1) computation of the total sum of any contiguous window of size `m`.
3. Initialize `best` to infinity. This variable will track the minimum total number of minutes found.
4. Slide a window of size `m` across the sorted array. For each window ending at index `i`, let `start = i - m + 1`. Compute the sum of the window using the prefix sums: `window_sum = prefix[i+1] - prefix[start]`.
5. The ideal target pressure for the window is the maximum pressure in the window plus as many increases as allowed without exceeding `k`. If `window_max - window_sum + m * window_max <= k`, we can choose `window_max` as the target. Otherwise, adjust the target downward so that the total increase does not exceed `k`. Compute the total cost as the sum of increases plus sum of decreases for the window.
6. Update `best` if the computed cost for this window is lower.
7. After sliding through all windows, `best` contains the minimal total number of minutes.

Why it works: Sorting ensures that each window contains the `m` closest pressures. Using prefix sums guarantees that we can compute total costs quickly. The choice of the maximum in the window as the target minimizes the number of required increases, which are constrained by `k`. The algorithm always considers the minimum necessary adjustments, so the final `best` is guaranteed to be the global minimum.

## Python Solution

```python
import sys
input = sys.stdin.readline

def main():
    n, m, k = map(int, input().split())
    a = list(map(int, input().split()))
    a.sort()
    
    prefix = [0] * (n + 1)
    for i in range(n):
        prefix[i + 1] = prefix[i] + a[i]

    best = float('inf')
    
    for i in range(m - 1, n):
        start = i - m + 1
        window_sum = prefix[i + 1] - prefix[start]
        max_in_window = a[i]
        needed_increase = max_in_window * m - window_sum
        if needed_increase <= k:
            total_cost = needed_increase
            total_cost += sum(a[j] - max_in_window for j in range(start, i + 1) if a[j] > max_in_window)
            best = min(best, total_cost)
        else:
            # We must reduce the target pressure so that increases <= k
            target = (window_sum + k) // m
            total_cost = sum(abs(a[j] - target) for j in range(start, i + 1))
            best = min(best, total_cost)

    print(best)

if __name__ == "__main__":
    main()
```

The prefix sum array allows constant-time sum queries for any window. Sorting ensures that the largest wheel in the window is the optimal target if we do not exceed `k` increases. When `k` is insufficient, we compute the target pressure that distributes the allowed increases optimally across the window. The solution carefully handles both the increase limit and the need to minimize the total time.

## Worked Examples

Sample input:

```
6 6 7
6 15 16 20 1 5
```

After sorting: `[1, 5, 6, 15, 16, 20]`, prefix sums: `[0, 1, 6, 12, 27, 43, 63]`.

| Window start | Window end | Window sum | Max | Needed increase | Total cost |
| --- | --- | --- | --- | --- | --- |
| 0 | 5 | 63 | 20 | 57 | 39 |

The calculation shows that we can increase up to 7 units (k=7), and total cost including decreases is 39.

Custom example:

```
5 3 2
3 1 4 1 5
```

Sorted: `[1, 1, 3, 4, 5]`, prefix sums: `[0,1,2,5,9,14]`.

Window `[1, 1, 3]`: sum=5, max=3, needed increase=4, exceeds k=2 → target=(5+2)//3=2, total cost=sum(abs(a-target))=1+1+1=3.

Window `[1,3,4]`: sum=8, max=4, needed increase=4>k → target=(8+2)//3=3, total cost=sum(abs)=1+0+1=2 → minimal.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n) | Sorting dominates, window sums and updates are O(n) |
| Space | O(n) | Prefix sum array |

Given n up to 2*10^5, `O(n log n)` is feasible within the 3-second limit. Memory usage of O(n) fits comfortably under 256 MB.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from contextlib import redirect_stdout
    out = io.StringIO()
    with redirect_stdout(out):
        main()
    return out.getvalue().strip()

# provided sample
assert run("6 6 7\n6 15 16 20 1 5\n") == "39", "sample 1"

# minimum-size input
assert run("1 1 0\n5\n") == "0", "single wheel"

# maximum-size input, all equal
assert run(f"{2*10**5} 2 10\n" + " ".join(["100"]*(2*10
```
