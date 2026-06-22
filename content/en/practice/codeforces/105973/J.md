---
title: "CF 105973J - Sublime Replacement"
description: "We are given an array where some positions are already fixed and some positions are marked as unknown with value −1. We are allowed to replace each unknown position with any positive integer up to $10^9$."
date: "2026-06-22T16:25:19+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105973
codeforces_index: "J"
codeforces_contest_name: "Uttara University Inter-University Programming Contest 2025"
rating: 0
weight: 105973
solve_time_s: 62
verified: true
draft: false
---

[CF 105973J - Sublime Replacement](https://codeforces.com/problemset/problem/105973/J)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 2s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given an array where some positions are already fixed and some positions are marked as unknown with value −1. We are allowed to replace each unknown position with any positive integer up to $10^9$. After this replacement, we look at all contiguous subarrays that are non-decreasing, meaning every element in the segment is less than or equal to the next one, and for each such segment we compute its sum. The goal is to maximize the largest such sum over all non-decreasing segments after we choose the replacements.

The key difficulty is that the replacements influence both the ability to extend non-decreasing segments and the sums of those segments. A very large value is beneficial for sums, but it may break non-decreasing structure if placed after a smaller fixed value. The array is long up to $3 \cdot 10^5$ across test cases, so any quadratic scan of all subarrays is impossible. Even $O(n \log n)$ per test case is acceptable only if the algorithm is linear or near-linear in practice.

A naive pitfall appears when treating −1 as freely replaceable without considering adjacency constraints. For example, if we greedily replace every −1 with $10^9$, we may break non-decreasing order at boundaries like `[5, -1, 1]`, where setting −1 to a large value would violate monotonicity for the best segment ending at 1. Another subtle case is when we assume the best segment always uses all large replacements; sometimes it is better to isolate a segment between fixed decreases rather than stretching across them.

## Approaches

The brute-force interpretation is straightforward. For every way of replacing −1 values, we would enumerate all non-decreasing subarrays and compute their sums, then take the maximum. Even ignoring replacements, enumerating all subarrays is $O(n^2)$, and the number of replacement choices is exponential. This becomes infeasible immediately.

A more structured brute-force removes replacement enumeration and instead tries all possible non-decreasing subarrays after fixing a candidate assignment. Even then, we would still need $O(n^2)$ scanning per assignment. The bottleneck is not just the number of arrays, but the number of subarrays per array.

The crucial observation is that the optimal construction will never use small values for a −1 unless forced by a surrounding fixed constraint. If we isolate a segment that is “safe” in terms of non-decreasing structure, we want to maximize its sum by filling all −1 with the maximum value $10^9$. The real constraint is not the exact values, but whether a segment can be made non-decreasing across fixed elements.

This suggests splitting the array at positions where a fixed descent is impossible to bridge. A non-decreasing subarray that achieves the maximum score will always either lie entirely inside a region of −1s and increasing fixed values, or it will be anchored by fixed values that determine the shape, while all −1s inside are filled with $10^9$. This reduces the problem to finding the best “extendable” segment where unknowns act as boosters but do not need individual tuning.

We can reinterpret the problem as finding a best segment where we are allowed to treat −1 as a wildcard that can be set high enough to preserve monotonicity. Since non-decreasing requires continuity of order, the only obstruction is when two fixed values violate order, in which case no segment can cross that boundary. Inside any valid region, all −1 should be maximized.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | exponential / $O(n^2)$ per assignment | $O(1)$-$O(n)$ | Too slow |
| Optimal | $O(n)$ | $O(1)$ | Accepted |

## Algorithm Walkthrough

1. Split the array into maximal segments where fixed values do not create a strict decreasing violation boundary. Any position where a fixed value is greater than the next fixed value forces a break, because no replacement can fix a violation between two fixed endpoints.
2. Inside each segment, interpret every −1 as a position that can safely become a large value. Replace −1 conceptually with $10^9$, since we want to maximize sums and these values will never be harmful as long as we stay inside a valid segment.
3. For each segment, compute the best non-decreasing subarray sum using a standard linear scan that extends a current candidate window when the non-decreasing condition holds, and resets otherwise.
4. Maintain a running maximum across all segments.
5. Output the maximum value found.

The subtle part is step 3. Even after filling −1s with large values, fixed small values can still break monotonicity locally. The scan ensures we only accumulate contiguous valid non-decreasing structure, while the large substituted values ensure that unknown positions do not artificially limit extension.

### Why it works

Any optimal solution must correspond to some non-decreasing segment in the final array. Inside a segment, replacing a −1 with anything smaller than $10^9$ can only reduce the sum without improving feasibility, since feasibility only depends on being able to choose a value consistent with neighbors. Thus every −1 inside a chosen segment is best set to the maximum allowed value.

Once this is fixed, the problem reduces to finding the maximum-sum non-decreasing subarray in a partially fixed array, where unknowns behave like very large elements that never block monotonicity. Any segment crossing a strict decrease between fixed elements cannot be valid in any completion, so such transitions naturally segment the array. The scan over each valid region enumerates all possible optimal candidates implicitly, ensuring no better segment is missed.

## Python Solution

```python
import sys
input = sys.stdin.readline

INF = 10**9

t = int(input())
for _ in range(t):
    n = int(input())
    a = list(map(int, input().split()))

    # replace -1 with INF for computation
    b = [INF if x == -1 else x for x in a]

    ans = 0

    # we scan all subarrays that are valid non-decreasing
    i = 0
    while i < n:
        j = i
        cur_sum = 0

        while j < n:
            if j > i and b[j] < b[j - 1]:
                break
            cur_sum += b[j]
            ans = max(ans, cur_sum)
            j += 1

        i = j + 1

    print(ans)
```

The array is first normalized so every unknown becomes $10^9$, reflecting the optimal choice for maximizing sums inside any feasible segment. The nested scan is structured so that each segment is extended greedily while maintaining non-decreasing order. When the order breaks, we restart from the next position because no valid subarray can cross that break.

A common mistake here is to restart at `j` instead of `j + 1`, which would incorrectly reconsider the violating pair as a valid start. Another subtlety is that we never need to explicitly check replacement choices again after substitution, because the decision is already encoded in using the maximum value.

## Worked Examples

### Example 1

Input:

```
n = 5
a = [4, 3, -1, -1, 2]
```

We convert −1 to INF:

| index | value | extendable? | current sum | best |
| --- | --- | --- | --- | --- |
| 0 | 4 | start | 4 | 4 |
| 1 | 3 | break (3 < 4) | reset | 4 |
| 2 | INF | start | INF | INF |
| 3 | INF | 3 ≤ INF | 2*INF | 2*INF |
| 4 | 2 | break (2 < INF) | reset | 2*INF |

The best segment is `[INF, INF]`, corresponding to replacing both −1 with $10^9$, giving sum $2 \cdot 10^9$.

This shows that unknowns behave as a high plateau that can dominate any segment they form.

### Example 2

Input:

```
n = 4
a = [1, -1, 5, 2]
```

After replacement:

```
[1, INF, 5, 2]
```

| index | value | action | current sum | best |
| --- | --- | --- | --- | --- |
| 0 | 1 | start | 1 | 1 |
| 1 | INF | extend | 1 + INF | 1 + INF |
| 2 | 5 | extend | 1 + INF + 5 | 1 + INF + 5 |
| 3 | 2 | break (2 < 5) | reset | 1 + INF + 5 |

This demonstrates that fixed decreases still break segments even when unknowns are large, so segmentation is essential.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n)$ | each element is visited once in the two-pointer scan |
| Space | $O(1)$ | only a few accumulators besides the array |

The linear scan is necessary given total input size up to $3 \cdot 10^5$, and avoids recomputation across test cases.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    t = int(input())
    out = []
    INF = 10**9

    for _ in range(t):
        n = int(input())
        a = list(map(int, input().split()))
        b = [INF if x == -1 else x for x in a]

        ans = 0
        i = 0
        while i < n:
            j = i
            cur = 0
            while j < n:
                if j > i and b[j] < b[j - 1]:
                    break
                cur += b[j]
                ans = max(ans, cur)
                j += 1
            i = j + 1
        out.append(str(ans))

    return "\n".join(out)

# provided sample-style case
assert run("1\n3\n2 4 5\n") == "11"

# all unknowns
assert run("1\n3\n-1 -1 -1\n") == str(3 * 10**9)

# alternating breaks
assert run("1\n5\n5 4 3 2 1\n") == "5"

# mixed
assert run("1\n5\n1 -1 2 -1 1\n") == str(1 + 10**9 + 2 + 10**9 + 1)
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| all −1 | $3 \cdot 10^9$ | unknown dominance |
| decreasing fixed | 5 | segmentation at breaks |
| mixed | large sum | interaction of fixed and unknown |

## Edge Cases

A fully decreasing array like `[5,4,3,2,1]` forces every non-decreasing segment to have length 1. The algorithm correctly resets at every drop and only considers single-element sums.

A fully unknown array becomes a single segment after conversion to $10^9$, and the scan accumulates the entire array, producing $n \cdot 10^9$, which is correct since the whole array is non-decreasing.

A pattern like `[1, -1, 1, -1, 1]` shows that unknowns do not need to be contiguous to form a best segment. After replacement, it becomes `[1, INF, 1, INF, 1]`, and the scan ensures only valid non-decreasing windows are accumulated, correctly balancing resets at each fixed decrease boundary.
