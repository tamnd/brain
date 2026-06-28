---
title: "CF 104790A - \\texttt{apt upgrade}"
description: "We are given a collection of software packages, each with a known download size. At some moment during an upgrade process, we observe that exactly some number of packages have already fully completed downloading, while up to a fixed number of packages can be downloading at the…"
date: "2026-06-28T13:54:58+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104790
codeforces_index: "A"
codeforces_contest_name: "2023 Benelux Algorithm Programming Contest (BAPC 23)"
rating: 0
weight: 104790
solve_time_s: 58
verified: true
draft: false
---

[CF 104790A - \\texttt{apt upgrade}](https://codeforces.com/problemset/problem/104790/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 58s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a collection of software packages, each with a known download size. At some moment during an upgrade process, we observe that exactly some number of packages have already fully completed downloading, while up to a fixed number of packages can be downloading at the same time. Downloads are parallelized, so at any time at most `k` packages are actively being downloaded, and completed packages are no longer active.

The key twist is that the progress indicator does not distinguish perfectly between “fully downloaded but not yet marked finished” and “still in progress”, so at the observation moment, some active downloads may effectively contribute their full size to the displayed progress even though they are not officially finished.

We are asked to compute the maximum possible fraction of the total download size that could have already been completed at the moment we observe exactly `m` finished packages, under the constraint that at most `k` packages are simultaneously downloading and the order of downloads is completely unknown.

In other words, we are free to choose which packages are finished, which are currently being downloaded, and which have not started yet, as long as exactly `m` are finished and at most `k` are active. We want to arrange this in a way that maximizes the total amount of downloaded data so far, including both finished packages and those currently in progress (which can be assumed to be almost complete).

The input size `n` can be up to `100000`, so any solution involving sorting is feasible, but anything quadratic or involving repeated simulation over permutations is not. A solution that tries all subsets of finished and in-progress packages would be far too slow, since that would explode combinatorially.

A subtle edge case appears when `k` is large relative to `n`. In that case, all remaining packages after choosing finished ones can still be considered in progress, meaning essentially everything can contribute to the progress total.

Another important case is when `m = 0`. Then nothing is fully finished, and only up to `k` packages can contribute their full sizes as in-progress downloads.

## Approaches

A brute-force approach would attempt to simulate all possible ways of selecting `m` finished packages and up to `k` active downloads from the remaining ones. For each configuration, we would compute the total contributed size and track the maximum. This is correct in principle, but completely infeasible because the number of ways to choose finished and active sets is combinatorial in `n`.

The key observation is that the structure of the problem does not depend on time ordering at all. We only care about how many packages are fully counted (`m`) and how many additional packages can still contribute fully because they are in progress (`k`). This means we are simply choosing a set of size `m + k` from the `n` packages that contributes fully to the observed progress.

To maximize the total progress, we should always select the largest packages for both the finished set and the in-progress set, because each package contributes its full size in both cases. There is no penalty or partial tradeoff: every selected package contributes independently and fully to the numerator of the percentage.

Thus, the optimal strategy reduces to sorting all package sizes in descending order and summing the largest `m + k` values. The denominator is the sum of all package sizes.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force (choose finished and in-progress sets) | Exponential | O(n) | Too slow |
| Sort and take top `m + k` | O(n log n) | O(n) | Accepted |

## Algorithm Walkthrough

Let the package sizes be stored in an array.

1. Compute the total sum of all package sizes. This will be the denominator of the final percentage.
2. Sort the array in descending order so that larger packages are considered first.
3. Take the first `m + k` elements from this sorted list. These represent the best possible choice of packages that can contribute fully to observed progress, either by being finished or by being in-progress but effectively counted as complete.
4. Sum these `m + k` elements to get the maximum achievable downloaded size at observation time.
5. Divide this sum by the total sum and multiply by 100 to convert it into a percentage.

The reason step 3 is valid is that we are free to assign roles to packages after the fact: the largest `m` become “finished”, and the next largest `k` become “currently downloading but effectively fully counted”.

### Why it works

At the observation moment, exactly `m` packages are in the finished state, and up to `k` can be actively downloading. Every active download can contribute up to its full size to the displayed progress, and finished packages contribute their full size as well.

This means the total counted progress is determined purely by selecting up to `m + k` packages whose full sizes are included in the total. Since there is no constraint on which specific packages must be finished, only on how many, any assignment of roles is valid. Therefore, maximizing the sum reduces to choosing the largest available package sizes.

## Python Solution

```python
import sys
input = sys.stdin.readline

n, m, k = map(int, input().split())
sizes = list(map(int, input().split()))

total = sum(sizes)
sizes.sort(reverse=True)

take = min(n, m + k)
best = sum(sizes[:take])

print((best / total) * 100)
```

The solution first reads input and computes the total size of all packages. It then sorts package sizes in descending order so that we can greedily pick the most valuable contributions first.

The variable `take` ensures we do not exceed the number of available packages when `m + k > n`. The final result is computed as a floating-point percentage. Using Python’s float division is sufficient because the required precision is only `1e-4`.

A common implementation pitfall is forgetting to clamp `m + k` by `n`, which would lead to indexing errors or incorrect sums. Another subtle issue is integer division, which must be avoided when computing percentages.

## Worked Examples

### Example 1

Input:

```
5 1 2
10 25 30 15 20
```

Sorted sizes: `[30, 25, 20, 15, 10]`

We take `m + k = 3` elements.

| Step | Chosen set | Sum |
| --- | --- | --- |
| Finished + in-progress selection | 30, 25, 20 | 75 |

Total sum is `100`, so answer is `75%`.

This shows that the best strategy is to treat the largest packages as either finished or nearly finished, maximizing contribution.

### Example 2

Input:

```
5 0 4
4 2 7 1 3
```

Sorted sizes: `[7, 4, 3, 2, 1]`

We take `m + k = 4` elements.

| Step | Chosen set | Sum |
| --- | --- | --- |
| Selected top elements | 7, 4, 3, 2 | 16 |

Total sum is `17`, so answer is `94.1176...%`.

This case demonstrates that when no packages are finished, all contribution comes from in-progress downloads, but the same greedy selection still applies.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n) | Sorting dominates, summation is linear |
| Space | O(n) | Storage for package sizes |

The constraints allow up to `100000` packages, so sorting comfortably fits within limits, and the memory usage is linear in the input size.

## Test Cases

```python
import sys, io

def solve(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    n, m, k = map(int, input().split())
    a = list(map(int, input().split()))
    total = sum(a)
    a.sort(reverse=True)
    take = min(n, m + k)
    best = sum(a[:take])
    return str((best / total) * 100)

# provided samples (second sample)
assert abs(float(solve("5 0 4\n4 2 7 1 3\n")) - 94.117647059) < 1e-6

# custom: minimum case
assert solve("1 0 1\n5\n").startswith("100")

# all equal values
assert solve("4 2 2\n10 10 10 10\n").startswith("100")

# k = 0 case
assert solve("5 2 0\n1 2 3 4 5\n").startswith("60")

# m + k > n
assert solve("3 2 5\n1 2 3\n").startswith("100")
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 0 1 / 5` | `100%` | Single element correctness |
| all equal | `100%` | symmetry and role assignment |
| `k = 0` | partial sum only | no in-progress contribution |
| `m + k > n` | full sum | clamping behavior |

## Edge Cases

When `m = 0`, the algorithm reduces to selecting the largest `k` packages. The sorted selection still applies directly, and the result is simply the sum of the top `k` sizes over the total.

When `k = 0`, no in-progress contribution exists, so only the top `m` packages are counted. The algorithm still works because `m + k = m`.

When `m + k >= n`, all packages are included in the sum, so the answer is always `100%`. The clamping step ensures we do not attempt to exceed array bounds, and the logic naturally collapses to summing everything.
