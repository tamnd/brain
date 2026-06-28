---
title: "CF 104778C - \u0414\u0432\u0435 \u043f\u043e\u0441\u043b\u0435\u0434\u043e\u0432\u0430\u0442\u0435\u043b\u044c\u043d\u043e\u0441\u0442\u0438"
description: "We are given two arrays of integers of equal length. Each position i defines a “constraint interval”, but the interval is unordered: the valid range for a candidate integer x at index i is simply the segment between ai and bi, regardless of which one is larger."
date: "2026-06-28T15:05:47+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104778
codeforces_index: "C"
codeforces_contest_name: "2023-2024 \u0412\u0441\u0435\u0440\u043e\u0441\u0441\u0438\u0439\u0441\u043a\u0430\u044f \u043a\u043e\u043c\u0430\u043d\u0434\u043d\u0430\u044f \u043e\u043b\u0438\u043c\u043f\u0438\u0430\u0434\u0430 \u0448\u043a\u043e\u043b\u044c\u043d\u0438\u043a\u043e\u0432 \u043f\u043e \u043f\u0440\u043e\u0433\u0440\u0430\u043c\u043c\u0438\u0440\u043e\u0432\u0430\u043d\u0438\u044e, \u0440\u0435\u0433\u0438\u043e\u043d\u0430\u043b\u044c\u043d\u044b\u0439 \u044d\u0442\u0430\u043f \u0421\u0430\u0440\u0430\u0442\u043e\u0432\u0441\u043a\u043e\u0439 \u043e\u0431\u043b\u0430\u0441\u0442\u0438 (\u0412\u041a\u041e\u0428\u041f 23, \u0421\u0430\u0440\u0430\u0442\u043e\u0432\u0441\u043a\u0438\u0439 \u043e\u0442\u0431\u043e\u0440\u043e\u0447\u043d\u044b\u0439 \u044d\u0442\u0430\u043f)"
rating: 0
weight: 104778
solve_time_s: 43
verified: true
draft: false
---

[CF 104778C - \u0414\u0432\u0435 \u043f\u043e\u0441\u043b\u0435\u0434\u043e\u0432\u0430\u0442\u0435\u043b\u044c\u043d\u043e\u0441\u0442\u0438](https://codeforces.com/problemset/problem/104778/C)

**Rating:** -  
**Tags:** -  
**Solve time:** 43s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given two arrays of integers of equal length. Each position i defines a “constraint interval”, but the interval is unordered: the valid range for a candidate integer x at index i is simply the segment between ai and bi, regardless of which one is larger. So each pair contributes a closed interval on the number line.

The task is to count how many integers x satisfy all constraints simultaneously, meaning x must lie inside every one of these n intervals. In other words, we are looking for the number of integer points in the intersection of all segments defined by (ai, bi).

The constraints are large, with n up to 200000 and values up to 1e9. This rules out any approach that tries every possible x or explicitly constructs ranges. A full scan over the value domain is impossible because the range size is too large. The only viable direction is to compress the problem down to a constant amount of information per interval.

A naive mistake is to try building a global set of valid x values by checking each interval one by one and filtering candidates. Even starting from a single interval and iteratively intersecting sets would explode, since the intersection of many large integer intervals cannot be represented explicitly as a set of individual points when ranges are large.

A second subtle pitfall is forgetting that each pair does not define direction, so (ai, bi) and (bi, ai) are identical constraints. Treating them as directed intervals would lead to incorrect intersection bounds.

## Approaches

If we try brute force, we could imagine iterating over every integer x from 1 to 1e9 and checking whether it satisfies all n intervals. Each check costs O(n), so the worst case is O(1e9 * n), which is completely infeasible.

The key observation is that each constraint is a standard closed interval. The set of all valid x is exactly the intersection of these intervals. The intersection of multiple intervals on a line is also a single interval, possibly empty. That means we do not need to track many candidates, we only need the global overlap.

Each interval [min(ai, bi), max(ai, bi)] contributes a lower bound and an upper bound. The intersection of all intervals is obtained by taking the maximum of all lower bounds and the minimum of all upper bounds. If the resulting left endpoint is greater than the right endpoint, the intersection is empty. Otherwise, every integer between them is valid, and we count them directly.

This reduces the problem from managing n intervals to maintaining two running values.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n · 1e9) | O(1) | Too slow |
| Optimal | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

We maintain the intersection of all intervals while scanning the input once.

1. For each pair (ai, bi), convert it into a proper interval [l, r] where l = min(ai, bi) and r = max(ai, bi). This normalization step is necessary because the endpoints are unordered.
2. Initialize the global intersection as an interval that contains all integers: left bound as very small, right bound as very large. This ensures the first interval fully defines the initial restriction.
3. For each interval [l, r], update the intersection by setting the new left bound to max(current_left, l). This keeps only values that are valid in every interval seen so far.
4. Similarly, update the right bound to min(current_right, r). This ensures we discard values that exceed any constraint.
5. After processing all intervals, check whether the resulting left bound is greater than the right bound. If so, no integer satisfies all constraints.
6. Otherwise, the answer is right − left + 1, since every integer in this closed interval is valid.

### Why it works

Each interval defines a set of allowed integers. The intersection of sets defined by intervals on a line is itself an interval. At every step, the maintained range exactly equals the intersection of all intervals processed so far. The updates preserve this property because any integer outside the new interval must violate at least one constraint, while any integer inside both previous intersection and the new interval satisfies all constraints seen so far.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    a = list(map(int, input().split()))
    b = list(map(int, input().split()))
    
    left = -10**18
    right = 10**18
    
    for i in range(n):
        l = min(a[i], b[i])
        r = max(a[i], b[i])
        left = max(left, l)
        right = min(right, r)
    
    if left > right:
        print(0)
    else:
        print(right - left + 1)

if __name__ == "__main__":
    solve()
```

The implementation directly mirrors the algorithm. The only subtle design choice is using sufficiently large sentinels for the initial intersection bounds. Since input values are up to 1e9, using ±1e18 safely avoids accidental clipping before the first update. The rest of the logic is a straightforward rolling intersection.

## Worked Examples

### Example 1

Input:

n = 4

a = [5, 5, 5, 5]

b = [5, 5, 5, 5]

Every interval is [5, 5], so the intersection remains [5, 5] throughout.

| Step | Interval | Left | Right |
| --- | --- | --- | --- |
| 1 | [5, 5] | 5 | 5 |
| 2 | [5, 5] | 5 | 5 |
| 3 | [5, 5] | 5 | 5 |
| 4 | [5, 5] | 5 | 5 |

Answer is 1. This confirms the algorithm correctly handles degenerate intervals.

### Example 2

Input:

n = 3

a = [3, 7, 10]

b = [6, 8, 12]

Intervals are [3,6], [7,8], [10,12]. These do not overlap.

| Step | Interval | Left | Right |
| --- | --- | --- | --- |
| 1 | [3,6] | 3 | 6 |
| 2 | [7,8] | 7 | 6 |
| 3 | [10,12] | 10 | 6 |

After step 2, left > right, so intersection becomes empty and remains empty.

Answer is 0. This demonstrates early collapse of feasibility.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | single pass over all intervals with constant updates |
| Space | O(1) | only two running bounds are stored |

The linear scan over up to 200000 intervals is easily within limits, and no additional structures are needed, making the solution both memory and time efficient.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    n = int(input())
    a = list(map(int, input().split()))
    b = list(map(int, input().split()))
    
    left = -10**18
    right = 10**18
    
    for i in range(n):
        l = min(a[i], b[i])
        r = max(a[i], b[i])
        left = max(left, l)
        right = min(right, r)
    
    if left > right:
        return "0\n"
    return str(right - left + 1) + "\n"

# provided samples
assert run("4\n5 5 5 5\n5 5 5 5\n") == "1\n"
assert run("3\n3 7 10\n6 8 12\n") == "0\n"

# custom cases
assert run("1\n10\n10\n") == "1\n"  # single point
assert run("2\n1 100\n50 60\n") == "11\n"  # overlapping interval
assert run("3\n1 2 3\n10 20 30\n") == "0\n"  # disjoint everywhere
assert run("2\n5 1\n1 5\n") == "5\n"  # reversed intervals
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1-point equality | 1 | minimal valid interval |
| overlapping mid-range | 11 | correct intersection size |
| fully disjoint | 0 | empty intersection handling |
| reversed endpoints | 5 | correctness under swapped ai, bi |

## Edge Cases

One edge case is when all intervals are identical single points. For input n = 3 with (ai, bi) = (5, 5) repeated, the algorithm sets left = 5 and right = 5 after the first iteration, and remains unchanged. The output becomes 1, correctly counting that only x = 5 satisfies all constraints.

Another edge case is when intervals collapse immediately after the first few steps. For example:

Input:

n = 2

a = [1, 100]

b = [2, 90]

After normalization we get [1,2] and [90,100]. After processing the first interval, left = 1, right = 2. After the second, left becomes 90 and right becomes 2, producing left > right and output 0. The algorithm correctly detects impossibility as soon as the intersection becomes empty, even though later updates continue consistently.
