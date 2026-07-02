---
title: "CF 103785D - Elder Ning"
description: "We are given several closed integer intervals, each defined by a left endpoint and a right endpoint. The task is to determine how many integers lie inside every single one of these intervals at the same time. In other words, imagine each interval as a segment on the number line."
date: "2026-07-02T08:52:08+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 103785
codeforces_index: "D"
codeforces_contest_name: "CodeBrew : Freshers Contest 2022"
rating: 0
weight: 103785
solve_time_s: 46
verified: true
draft: false
---

[CF 103785D - Elder Ning](https://codeforces.com/problemset/problem/103785/D)

**Rating:** -  
**Tags:** -  
**Solve time:** 46s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given several closed integer intervals, each defined by a left endpoint and a right endpoint. The task is to determine how many integers lie inside every single one of these intervals at the same time.

In other words, imagine each interval as a segment on the number line. We are asked to find the portion of the line that is common to all segments. If such a common portion exists, we count how many integers fall inside it. If no common portion exists, the answer is zero.

The input size is small enough that we are only doing a single pass over all intervals. This immediately rules out anything quadratic or involving pairwise comparisons between intervals. A solution that inspects each interval once is sufficient.

A few edge cases matter.

If the intervals do not overlap at all, for example [1, 2] and [5, 6], then there is no integer that belongs to both, and the correct answer is 0. A naive mistake is to compute something like total union length or to forget that an empty intersection must be detected explicitly.

If all intervals share at least one point but the intersection shrinks to a single integer, such as [3, 5], [4, 6], [5, 10], the answer is 1. This is easy to mishandle if one incorrectly computes a difference without including both endpoints.

Another subtle case is when endpoints are very large or very small. The logic depends only on comparing endpoints, so integer range does not affect correctness as long as comparisons are handled properly.

## Approaches

A straightforward way to solve the problem is to think in terms of checking every integer and verifying whether it belongs to all intervals. This brute-force idea would require identifying the global minimum possible range across all intervals, and then iterating through each integer in that range to test membership in every interval.

For each candidate integer x, we would check all intervals and confirm whether L_i ≤ x ≤ R_i for every i. If yes, we count it.

This approach is correct but expensive. If interval endpoints span a large range, say up to 10^9, then even a single interval could force us to consider up to 10^9 candidate integers. For each candidate, checking all intervals adds another factor of m, making this completely infeasible.

The key observation is that membership in all intervals is equivalent to satisfying all lower bounds simultaneously and all upper bounds simultaneously. A number x is valid if it is greater than or equal to every left endpoint and less than or equal to every right endpoint. This transforms the problem from checking every point to finding a single constrained segment.

The smallest possible right bound of the intersection is the minimum of all right endpoints, because any valid point must lie inside every interval. Similarly, the largest possible left bound of the intersection is the maximum of all left endpoints. The intersection is therefore [max(L_i), min(R_i)]. Once this interval is known, the answer is simply its length if it is valid.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(R−L) · m | O(1) | Too slow |
| Optimal | O(m) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read all intervals and initialize two variables: one to track the maximum left endpoint and one to track the minimum right endpoint. These represent the tightest possible intersection bounds seen so far.
2. For each interval [l, r], update the maximum left endpoint by comparing it with l. This ensures that the final left boundary respects the strongest lower constraint among all intervals.
3. For each interval [l, r], update the minimum right endpoint by comparing it with r. This ensures that the final right boundary respects the strongest upper constraint among all intervals.
4. After processing all intervals, interpret the result interval as [L, R], where L is the maximum of all left endpoints and R is the minimum of all right endpoints. This interval represents all numbers that satisfy every constraint simultaneously.
5. If L is greater than R, the intersection is empty, so output 0.
6. Otherwise, the valid integers are all values from L to R inclusive, so output R − L + 1.

### Why it works

Each interval contributes two independent constraints: a lower bound and an upper bound. Any number that belongs to all intervals must satisfy every lower bound, which collapses into being at least the maximum of all left endpoints, and must also satisfy every upper bound, which collapses into being at most the minimum of all right endpoints. These two aggregated constraints exactly characterize the intersection. No other hidden condition exists because intervals impose only these monotonic restrictions.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    m = int(input())
    
    L = -10**18
    R = 10**18
    
    for _ in range(m):
        l, r = map(int, input().split())
        L = max(L, l)
        R = min(R, r)
    
    if L > R:
        print(0)
    else:
        print(R - L + 1)

if __name__ == "__main__":
    solve()
```

The implementation directly mirrors the idea of compressing all lower bounds into a single maximum and all upper bounds into a single minimum. The initial values for L and R are chosen wide enough to not interfere with any valid input range. Each update is constant time, ensuring a linear scan over all intervals.

The final subtraction R − L + 1 counts integers in a closed interval. The +1 is necessary because both endpoints are included.

## Worked Examples

### Example 1

Input intervals:

[1, 5], [2, 6], [4, 10]

We track L as the maximum of left endpoints and R as the minimum of right endpoints.

| Step | Interval | L (max left) | R (min right) |
| --- | --- | --- | --- |
| 1 | [1, 5] | 1 | 5 |
| 2 | [2, 6] | 2 | 5 |
| 3 | [4, 10] | 4 | 5 |

Final intersection is [4, 5], so the answer is 2.

This confirms that only values simultaneously satisfying all constraints survive, and the shrinking process correctly captures overlap.

### Example 2

Input intervals:

[1, 2], [5, 6], [3, 4]

| Step | Interval | L (max left) | R (min right) |
| --- | --- | --- | --- |
| 1 | [1, 2] | 1 | 2 |
| 2 | [5, 6] | 5 | 2 |
| 3 | [3, 4] | 5 | 2 |

Final result has L = 5 and R = 2, so L > R and the intersection is empty.

The algorithm correctly detects that no single integer can satisfy all intervals simultaneously.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(m) | Each interval is processed once with constant-time updates |
| Space | O(1) | Only two tracking variables are used |

The algorithm is optimal for the input constraints because any solution must at least read all intervals, which already requires linear time.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from contextlib import redirect_stdout
    out = io.StringIO()
    with redirect_stdout(out):
        solve()
    return out.getvalue().strip()

def solve():
    m = int(input())
    L = -10**18
    R = 10**18
    for _ in range(m):
        l, r = map(int, input().split())
        L = max(L, l)
        R = min(R, r)
    if L > R:
        print(0)
    else:
        print(R - L + 1)

# sample-style tests
assert run("3\n1 5\n2 6\n4 10\n") == "2"
assert run("3\n1 2\n5 6\n3 4\n") == "0"

# custom tests
assert run("1\n10 20\n") == "11", "single interval"
assert run("2\n1 100\n50 60\n") == "11", "nested overlap"
assert run("3\n0 0\n0 0\n0 0\n") == "1", "all equal single point"
assert run("2\n-5 -1\n-3 2\n") == "3", "negative range overlap"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 interval | 11 | single interval correctness |
| nested overlap | 11 | proper intersection shrinking |
| all zeros | 1 | single-point intersection |
| negative range | 3 | handling negatives and bounds |

## Edge Cases

One edge case is when there is only one interval. The algorithm sets L and R directly from that interval, so the answer becomes R − L + 1, which correctly counts all integers inside it.

Another edge case is when intervals are disjoint early, such as [1, 2] followed by [100, 200]. After processing the second interval, L becomes 100 while R remains 2, so L > R immediately. The algorithm correctly outputs 0 without needing further processing.

A third case is when all intervals collapse to a single shared point, such as [5, 5] repeated multiple times. L and R remain equal to 5 throughout, and the output becomes 1, reflecting exactly one valid integer.
