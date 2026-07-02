---
title: "CF 103741D - Difference"
description: "We are given an array of length $n$. For every contiguous subarray $[l, r]$, we define a value equal to the difference between the maximum element and the minimum element inside that subarray."
date: "2026-07-02T09:04:50+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 103741
codeforces_index: "D"
codeforces_contest_name: "HUSTPC 2022"
rating: 0
weight: 103741
solve_time_s: 50
verified: true
draft: false
---

[CF 103741D - Difference](https://codeforces.com/problemset/problem/103741/D)

**Rating:** -  
**Tags:** -  
**Solve time:** 50s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given an array of length $n$. For every contiguous subarray $[l, r]$, we define a value equal to the difference between the maximum element and the minimum element inside that subarray. The task is not to compute all of these values explicitly, but to determine which value ranks $k$-th when all subarray differences are sorted in descending order.

So conceptually, every interval contributes one number: how “spread out” its values are. A constant subarray contributes zero, while a subarray that contains both a very large and a very small element contributes a large value.

The constraints are large: $n \le 5 \cdot 10^5$, which implies $O(n^2)$ subarrays in the worst case, around $10^{11}$. Any solution that enumerates intervals is immediately impossible. Even $O(n \log n)$ per interval computations are ruled out.

The key difficulty is that we are asked for an order statistic over all subarray ranges, not a single aggregate value. That typically signals that we need to count how many subarrays satisfy a condition of the form “difference at least X”, then binary search on X.

A subtle pitfall is misunderstanding monotonicity. If we fix a threshold $X$, the condition “max minus min ≥ X” behaves monotonically over subarrays: if a subarray satisfies it, any larger window containing it also satisfies it. This structure is what allows counting with two pointers and monotonic queues.

Edge cases worth keeping in mind include arrays with all equal elements, where every subarray has value zero, and arrays with extreme alternating values, where most subarrays have large differences. A naive ranking simulation would fail even for $n = 10^4$ because it would need about $5 \cdot 10^7$ intervals.

## Approaches

A direct approach would enumerate every subarray, compute its minimum and maximum, and store the result. This is correct but fundamentally quadratic in the number of intervals. With $n = 5 \cdot 10^5$, this means about $1.25 \cdot 10^{11}$ subarrays, which is far beyond any feasible computation.

The key observation is to invert the problem. Instead of trying to list all differences, we ask: for a fixed value $X$, how many subarrays satisfy

$$\max(a[l..r]) - \min(a[l..r]) \ge X?$$

If we can compute this count quickly, we can binary search over $X$. The answer we want is the largest $X$ such that at least $k$ subarrays have difference at least $X$. This works because the number of subarrays with difference at least $X$ decreases monotonically as $X$ increases.

To compute the count efficiently for a fixed $X$, we use a two-pointer sliding window with monotonic deques maintaining the current maximum and minimum. We expand the right endpoint and maintain the best left endpoint such that the window is still valid under the constraint “max − min < X”. Every time the window breaks the constraint, we move the left pointer forward.

This gives a linear scan per check.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(n^2)$ | $O(1)$ | Too slow |
| Binary search + two pointers | $O(n \log V)$ | $O(n)$ | Accepted |

Here $V$ is the range of possible differences, bounded by about $2 \cdot 10^9$.

## Algorithm Walkthrough

1. Define a function $\text{count}(X)$ that returns how many subarrays satisfy $\max - \min \ge X$. We will compute this via complement counting instead of direct counting.
2. For a fixed $X$, instead count subarrays where $\max - \min < X$. This is easier to maintain incrementally.
3. Maintain a sliding window $[l, r]$ and two monotonic deques: one decreasing for maximum values and one increasing for minimum values.
4. Expand $r$ from left to right, inserting $a[r]$ into both deques while preserving monotonicity. This ensures the front of each deque always represents the current window maximum and minimum.
5. While the current window violates $\max - \min < X$, move $l$ forward and remove outdated elements from deques. This shrinking step guarantees the window always satisfies the constraint.
6. For each $r$, all subarrays ending at $r$ and starting anywhere in $[l, r]$ are valid under the constraint, so we add $r - l + 1$ to the count of valid subarrays.
7. The total number of subarrays is $n(n+1)/2$. Subtracting valid ones gives the number of subarrays with difference at least $X$.
8. Binary search $X$ over the range of possible differences. For each mid, compute how many subarrays have difference at least mid and compare with $k$ to adjust the search.

The key idea is that instead of directly ranking subarray values, we convert the problem into a threshold counting problem, which is monotonic and efficiently checkable.

### Why it works

For any fixed $X$, the set of subarrays satisfying $\max - \min \ge X$ is monotone in the sense required for binary search: increasing $X$ can only remove valid subarrays, never add new ones. The sliding window correctly counts the complement set because within each right endpoint, the minimal left boundary enforcing validity is uniquely determined by the monotonic constraint on maximum and minimum. This guarantees each subarray is counted exactly once in the valid regime.

## Python Solution

```python
import sys
input = sys.stdin.readline

from collections import deque

def count_less_than_x(a, x):
    n = len(a)
    maxdq = deque()
    mindq = deque()
    l = 0
    res = 0

    for r in range(n):
        while maxdq and a[maxdq[-1]] <= a[r]:
            maxdq.pop()
        maxdq.append(r)

        while mindq and a[mindq[-1]] >= a[r]:
            mindq.pop()
        mindq.append(r)

        while maxdq and mindq and a[maxdq[0]] - a[mindq[0]] >= x:
            if maxdq[0] == l:
                maxdq.popleft()
            if mindq[0] == l:
                mindq.popleft()
            l += 1

        res += r - l + 1

    return res

def solve():
    n, k = map(int, input().split())
    a = list(map(int, input().split()))

    total = n * (n + 1) // 2

    lo, hi = 0, max(a) - min(a)

    ans = 0
    while lo <= hi:
        mid = (lo + hi) // 2
        # count subarrays with diff >= mid
        less = count_less_than_x(a, mid)
        ge = total - less

        if ge >= k:
            ans = mid
            lo = mid + 1
        else:
            hi = mid - 1

    print(ans)

if __name__ == "__main__":
    solve()
```

The code is structured around a helper that counts subarrays with difference less than a threshold. The sliding window maintains two monotonic deques, one tracking maximum candidates and the other tracking minimum candidates. The critical correctness point is that the window invariant always enforces a strict inequality condition, so the complement corresponds exactly to the desired threshold predicate.

The binary search is performed on possible answer values, and each check converts the condition into a counting problem. The final answer is the largest threshold that still leaves at least $k$ valid subarrays above it.

A common implementation mistake is mixing up the inequality direction inside the sliding window condition. The check must be consistent with the definition of “less than x”, otherwise the binary search monotonicity breaks and the result becomes unstable.

## Worked Examples

### Example 1

Input:

```
3 2
3 1 2
```

All subarrays:

| l | r | subarray | max-min |
| --- | --- | --- | --- |
| 1 | 1 | [3] | 0 |
| 2 | 2 | [1] | 0 |
| 3 | 3 | [2] | 0 |
| 1 | 2 | [3,1] | 2 |
| 2 | 3 | [1,2] | 1 |
| 1 | 3 | [3,1,2] | 2 |

Sorted descending differences:

```
2, 2, 1, 0, 0, 0
```

The 2nd largest is 2.

This confirms the algorithm must prioritize larger span subarrays even if they are fewer.

### Example 2

Input:

```
4 1
1 1 1 1
```

Every subarray has difference 0, so all values are identical. The k-th largest is always 0 regardless of k.

This shows the binary search must handle degenerate ranges correctly and not assume positive differences exist.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n \log V)$ | Each binary search step runs a linear two-pointer scan; the range of values is bounded by max-min |
| Space | $O(n)$ | Deques store indices of the current window |

The algorithm fits comfortably within constraints because $n = 5 \cdot 10^5$ and about 31-32 binary search iterations are needed.

## Test Cases

```python
import sys, io
from collections import deque

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    input = sys.stdin.readline

    def count_less_than_x(a, x):
        n = len(a)
        maxdq = deque()
        mindq = deque()
        l = 0
        res = 0

        for r in range(n):
            while maxdq and a[maxdq[-1]] <= a[r]:
                maxdq.pop()
            maxdq.append(r)

            while mindq and a[mindq[-1]] >= a[r]:
                mindq.pop()
            mindq.append(r)

            while maxdq and mindq and a[maxdq[0]] - a[mindq[0]] >= x:
                if maxdq[0] == l:
                    maxdq.popleft()
                if mindq[0] == l:
                    mindq.popleft()
                l += 1

            res += r - l + 1

        return res

    n, k = map(int, input().split())
    a = list(map(int, input().split()))

    total = n * (n + 1) // 2

    lo, hi = 0, max(a) - min(a)
    ans = 0

    while lo <= hi:
        mid = (lo + hi) // 2
        less = count_less_than_x(a, mid)
        ge = total - less

        if ge >= k:
            ans = mid
            lo = mid + 1
        else:
            hi = mid - 1

    return str(ans)

# provided sample
assert run("3 2\n3 1 2\n") == "2"

# custom cases
assert run("4 1\n1 1 1 1\n") == "0"
assert run("2 1\n1 100\n") == "99"
assert run("5 3\n1 2 3 4 5\n") == "3"
assert run("3 3\n5 1 5\n") == "4"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 3 2 / 3 1 2 | 2 | sample correctness and ranking logic |
| 4 1 / all equal | 0 | degenerate case |
| 2 1 / 1 100 | 99 | single interval max gap |
| 5 3 / 1..5 | 3 | distribution of subarray ranges |
| 3 3 / 5 1 5 | 4 | mixed extremes and duplicates |

## Edge Cases

For an all-equal array such as `1 1 1 1`, every subarray has difference zero. The sliding window never violates the constraint for any $X > 0$, so the binary search correctly collapses to answer 0. The count function returns all subarrays for $X = 0$, which correctly places zero as the only candidate value.

For a two-element extreme case like `1 100`, there are only three subarrays, and the maximum difference appears exactly once. The binary search immediately isolates 99 as the only non-zero threshold supported by one subarray.

For alternating patterns like `5 1 5`, large differences occur in multiple overlapping subarrays, and the monotonic queue ensures correct counting even when maximum and minimum repeatedly shift at boundaries.
