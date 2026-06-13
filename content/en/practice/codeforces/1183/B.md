---
title: "CF 1183B - Equalize Prices"
description: "We are given several independent scenarios. In each one, there is a list of product prices, and we are allowed to adjust each price by at most k in either direction, but we are not allowed to adjust it more than once."
date: "2026-06-13T11:39:02+07:00"
tags: ["codeforces", "competitive-programming", "math"]
categories: ["algorithms"]
codeforces_contest: 1183
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 570 (Div. 3)"
rating: 900
weight: 1183
solve_time_s: 580
verified: false
draft: false
---

[CF 1183B - Equalize Prices](https://codeforces.com/problemset/problem/1183/B)

**Rating:** 900  
**Tags:** math  
**Solve time:** 9m 40s  
**Verified:** no  

## Solution
## Problem Understanding

We are given several independent scenarios. In each one, there is a list of product prices, and we are allowed to adjust each price by at most `k` in either direction, but we are not allowed to adjust it more than once. After these adjustments, we want all products to end up with exactly the same integer price `B`.

The condition for a chosen value `B` is simple but strict: every original price `a_i` must be able to move to `B` without exceeding the allowed change, meaning the absolute difference `|a_i - B|` must not exceed `k`. If even one product cannot reach `B`, then that value of `B` is invalid.

Among all valid integer values of `B`, we need to find the maximum one. If no integer satisfies the condition for all elements, we output `-1`.

Each query is independent, so the process restarts with a new array every time.

The constraints are small: `n ≤ 100`, `q ≤ 100`. This immediately rules out any need for advanced data structures or optimization beyond linear or log-linear work per query. Even an O(n^2) approach per query would pass comfortably.

A subtle edge case appears when the intervals defined by different elements do not overlap at all. For example, if we have `a = [1, 100]` and `k = 10`, then valid ranges are `[−9, 11]` and `[90, 110]`, which do not intersect, so no valid `B` exists.

Another edge case is when the intersection is valid but the maximum boundary is not intuitive. For example, if all intervals overlap heavily, the answer is simply the rightmost point of the intersection.

## Approaches

A brute-force approach would try every possible integer `B` from `1` up to `max(a_i) + k`, and check whether every element satisfies `|a_i - B| ≤ k`. For each candidate `B`, we scan the array, so the complexity becomes O(M·n), where M is the range of possible values. Since `a_i` can be up to `10^8`, M can also be large, making this approach completely infeasible in the worst case.

The key observation is that each element `a_i` does not allow arbitrary values of `B`, but instead restricts it to an interval `[a_i - k, a_i + k]`. The condition “all products can become equal to B” is equivalent to requiring that B lies in the intersection of all these intervals. Once we interpret the problem this way, it reduces to a standard interval intersection problem.

The intersection of many intervals is itself an interval `[L, R]`, where `L` is the maximum of all left endpoints and `R` is the minimum of all right endpoints. If `L > R`, the intersection is empty and no solution exists. Otherwise, every integer in `[L, R]` is valid, and since we want the maximum possible `B`, we simply choose `R`.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n · max(a_i + k)) | O(1) | Too slow |
| Optimal | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

1. For each query, read the array of prices and the value `k`.

We process each scenario independently, so no state is shared.
2. For each price `a_i`, compute the interval of valid final values: `[a_i - k, a_i + k]`.

This directly encodes the constraint `|a_i - B| ≤ k`.
3. Maintain two variables: `L` initialized to a very small number, and `R` initialized to a very large number.

These represent the intersection of all intervals processed so far.
4. For each interval `[l, r]`, update:

`L = max(L, l)` and `R = min(R, r)`.

This keeps only values of `B` that are valid for all elements seen so far.
5. After processing all elements, check whether `L > R`.

If this happens, no integer lies in the intersection, so the answer is `-1`.
6. Otherwise, output `R`, since it is the largest integer that satisfies all constraints.

### Why it works

Each element independently restricts `B` to a closed interval of valid values. A value of `B` is valid for the whole array only if it satisfies every element’s constraint simultaneously, which is exactly the definition of belonging to the intersection of all intervals. The algorithm maintains this intersection incrementally, and at no step does it discard any value that could still satisfy all processed constraints. Therefore, if a value survives to the end, it is valid for all elements, and if the intersection becomes empty, no valid value exists.

## Python Solution

```python
import sys
input = sys.stdin.readline

q = int(input())
for _ in range(q):
    n, k = map(int, input().split())
    a = list(map(int, input().split()))

    L = -10**18
    R = 10**18

    for x in a:
        L = max(L, x - k)
        R = min(R, x + k)

    if L > R:
        print(-1)
    else:
        print(R)
```

The solution converts each price into an allowable interval and keeps intersecting them. The only subtle implementation detail is choosing sufficiently large initial bounds for `L` and `R`, since prices can go up to `10^8` and `k` up to `10^8`, so the resulting interval can extend beyond the original range.

## Worked Examples

### Example 1

Input:

```
n = 5, k = 1
a = [1, 1, 2, 3, 1]
```

We compute intervals:

| Step | a_i | Interval | L | R |
| --- | --- | --- | --- | --- |
| 1 | 1 | [0, 2] | 0 | 2 |
| 2 | 1 | [0, 2] | 0 | 2 |
| 3 | 2 | [1, 3] | 1 | 2 |
| 4 | 3 | [2, 4] | 2 | 2 |
| 5 | 1 | [0, 2] | 2 | 2 |

Final intersection is `[2, 2]`, so answer is `2`.

This confirms that the algorithm correctly tracks shrinking overlap and handles multiple constraints converging to a single point.

### Example 2

Input:

```
n = 2, k = 2
a = [1, 6]
```

| Step | a_i | Interval | L | R |
| --- | --- | --- | --- | --- |
| 1 | 1 | [-1, 3] | -1 | 3 |
| 2 | 6 | [4, 8] | 4 | 3 |

At this point `L > R`, so the intersection is empty and we output `-1`.

This demonstrates the failure case where two feasible ranges do not overlap at all.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) per query | Each element contributes one interval update |
| Space | O(1) | Only two running bounds are stored |

The constraints allow up to 10,000 total elements across all queries, so a linear scan per query is easily fast enough within the time limit.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    q = int(input())
    out = []
    for _ in range(q):
        n, k = map(int, input().split())
        a = list(map(int, input().split()))

        L = -10**18
        R = 10**18

        for x in a:
            L = max(L, x - k)
            R = min(R, x + k)

        out.append(str(-1 if L > R else R))

    return "\n".join(out)

# provided samples
assert run("""4
5 1
1 1 2 3 1
4 2
6 4 8 5
2 2
1 6
3 5
5 2 5
""") == """2
6
-1
7"""

# custom cases
assert run("""1
1 10
5
""") == "15", "single element expands range"

assert run("""1
2 0
5 5
""") == "5", "zero movement edge"

assert run("""1
3 1
1 10 20
""") == "-1", "disjoint intervals"

assert run("""1
4 5
10 10 10 10
""") == "15", "all equal values"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single element | 15 | interval expansion correctness |
| zero movement | 5 | k = 0 behavior |
| disjoint intervals | -1 | empty intersection |
| all equal | 15 | stable intersection growth |

## Edge Cases

One important edge case is when `k = 0`. In this case, every interval collapses to `[a_i, a_i]`, so the only possible solution is if all elements are already equal. The algorithm handles this naturally because the intersection will only survive if all values match exactly.

Another edge case is when `n = 1`. The answer is simply `a_1 + k`, since the single interval is `[a_1 - k, a_1 + k]` and we choose the maximum valid value.

A more subtle case happens when values are large and `k` is also large, potentially pushing bounds outside the original input range. The use of wide integer bounds in the implementation ensures no overflow or clipping affects correctness, since Python integers are unbounded and the logic only depends on comparisons.

Finally, cases where the intersection shrinks to a single point early are handled correctly because the algorithm continuously tightens both ends, never losing a valid candidate that could still satisfy all constraints.
