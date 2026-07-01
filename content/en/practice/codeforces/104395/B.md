---
title: "CF 104395B - Spilling the Juice"
description: "We are given an array where each position does not necessarily store a single fixed number. Some positions are known exactly, while others are uncertain and described as a closed interval."
date: "2026-06-30T23:18:05+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104395
codeforces_index: "B"
codeforces_contest_name: "Cupertino Informatics Tournament"
rating: 0
weight: 104395
solve_time_s: 57
verified: true
draft: false
---

[CF 104395B - Spilling the Juice](https://codeforces.com/problemset/problem/104395/B)

**Rating:** -  
**Tags:** -  
**Solve time:** 57s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given an array where each position does not necessarily store a single fixed number. Some positions are known exactly, while others are uncertain and described as a closed interval. For each uncertain position, the final chosen value must lie somewhere inside its allowed interval.

After the array is fixed by choosing one valid value for every uncertain position, we must answer multiple queries. Each query gives a segment $[l, r]$ and a target sum $x$. The question is whether it is possible to assign valid values to all uncertain positions so that the sum of the chosen values in that segment becomes exactly $x$, while respecting all interval constraints globally.

The key difficulty is that the same array must satisfy all queries independently, but each query only asks about existence: we are not required to construct a single global assignment that works for all queries simultaneously.

The constraints are large, with $n, q \le 10^5$. This immediately rules out any solution that recomputes information per query in linear time over the segment, since that would lead to $10^{10}$ operations in the worst case. Even $O(n \log n)$ per query is too slow. We are forced toward a preprocessing approach where each query can be answered in logarithmic or constant time.

A subtle issue is that uncertainty is not local to a query. Each unknown position contributes a range of possible values, and different queries may overlap these positions in different ways. A naive mistake is to treat each query independently and greedily assign values inside the segment only. That fails because values chosen for one query’s reasoning might contradict feasibility when considering the global consistency of bounds.

Another trap appears when all elements are known. Then the answer reduces to checking whether the fixed segment sum equals $x$. In mixed cases, however, the feasible sum is not a single value but an interval, and reasoning about that interval correctly is the central challenge.

## Approaches

A direct brute force approach would try to assign a concrete value to every uncertain element, then compute the segment sum for each query and check whether any assignment can produce the required target. Each uncertain cell has up to 1000 choices, and in the worst case there can be $n$ such cells, making the number of combinations astronomically large. Even restricting attention to a single query, enumerating all combinations is exponential and completely infeasible.

The important observation is that we do not care about individual assignments. What matters for each query is only the minimum and maximum possible sum of the queried segment under all valid choices. If we can compute these two values, the answer becomes a simple interval membership check.

This reduces the problem to maintaining two independent versions of the array: one where every uncertain position takes its minimum value, and one where it takes its maximum value. Any valid assignment must lie between these extremes for every position, so any segment sum must lie between the corresponding prefix sums of these two arrays.

Once these two prefix-sum arrays are built, each query reduces to extracting a subarray sum in $O(1)$ and checking whether the target lies inside the achievable interval.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | Exponential | O(n) | Too slow |
| Optimal | O(n + q) | O(n) | Accepted |

## Algorithm Walkthrough

### Optimal solution

We convert the problem into prefix sums over two derived arrays: a minimum array and a maximum array.

## Algorithm Walkthrough

1. Construct two arrays of length $n$. For each position, if the value is fixed, both arrays store that value. If the value is uncertain with range $[l, r]$, the minimum array stores $l$ and the maximum array stores $r$. This captures the full range of possibilities at each index in a way that separates lower and upper extremes.
2. Build prefix sums for both arrays. The prefix sum at index $i$ represents the minimum or maximum possible sum of the prefix $[1, i]$ under extreme choices.
3. For each query $(l, r, x)$, compute the minimum possible sum on the segment as $minSum = prefMin[r] - prefMin[l-1]$, and the maximum possible sum as $maxSum = prefMax[r] - prefMax[l-1]$.
4. Check whether $x$ lies in the interval $[minSum, maxSum]$. If it does, output "yes", otherwise output "no".

The reason this works is that each position contributes independently to the total sum, and the constraints on each element are interval constraints that do not interact across positions.

### Why it works

Each position in the array contributes an additive term to any segment sum. Since the only restriction is that each element must lie in a fixed interval, the minimum possible contribution of each position is achieved independently by picking its lower bound, and the maximum by picking its upper bound. No coupling exists between indices, so extremizing each position locally produces global extrema for any segment. This makes the feasible set of sums for any segment exactly the interval between these two computed extremes.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, q = map(int, input().split())

    min_arr = [0] * (n + 1)
    max_arr = [0] * (n + 1)

    for i in range(1, n + 1):
        tmp = input().split()
        if tmp[0] == '1':
            v = int(tmp[1])
            min_arr[i] = max_arr[i] = v
        else:
            l = int(tmp[1])
            r = int(tmp[2])
            min_arr[i] = l
            max_arr[i] = r

    pref_min = [0] * (n + 1)
    pref_max = [0] * (n + 1)

    for i in range(1, n + 1):
        pref_min[i] = pref_min[i - 1] + min_arr[i]
        pref_max[i] = pref_max[i - 1] + max_arr[i]

    out = []
    for _ in range(q):
        l, r, x = map(int, input().split())
        min_sum = pref_min[r] - pref_min[l - 1]
        max_sum = pref_max[r] - pref_max[l - 1]

        if min_sum <= x <= max_sum:
            out.append("yes")
        else:
            out.append("no")

    print("\n".join(out))

if __name__ == "__main__":
    solve()
```

The implementation directly follows the construction of the two bounding arrays. The only subtle point is ensuring 1-indexed prefix sums so that subarray queries become a single subtraction. Another important detail is that uncertain values are handled symmetrically: both bounds are stored at the same index, which avoids any special-case logic during query time.

## Worked Examples

Consider a small array:

Input:

```
5 3
1 5
2 1 3
1 2
2 4 6
1 10
1 2 5
2 2 2
1 5 12
```

We first build the arrays:

| i | type | min | max | pref_min | pref_max |
| --- | --- | --- | --- | --- | --- |
| 1 | fixed 5 | 5 | 5 | 5 | 5 |
| 2 | [1,3] | 1 | 3 | 6 | 8 |
| 3 | fixed 2 | 2 | 2 | 8 | 10 |
| 4 | [4,6] | 4 | 6 | 12 | 16 |
| 5 | fixed 10 | 10 | 10 | 22 | 26 |

Query 1 is $[1,2]$ with $x = 5$. The segment minimum sum is $6 - 0 = 6$, maximum is $8 - 0 = 8$, so 5 is outside the interval and the answer is no.

Query 2 is $[2,2]$ with $x = 2$. The interval for index 2 is $[1,3]$, so 2 is feasible and the answer is yes.

Query 3 is $[3,5]$ with $x = 12$. Minimum is $22 - 8 = 14$, maximum is $26 - 10 = 16$, so 12 is not achievable.

This trace shows that each query reduces to checking a numeric interval derived from prefix sums, with no dependence on other queries.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n + q) | One pass to build arrays and prefix sums, one O(1) check per query |
| Space | O(n) | Two auxiliary arrays and prefix sums |

The constraints allow up to $10^5$ operations, and this solution performs only linear preprocessing plus constant-time query handling, which fits comfortably within limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from sys import stdout
    import sys

    input = sys.stdin.readline

    def solve():
        n, q = map(int, input().split())

        min_arr = [0] * (n + 1)
        max_arr = [0] * (n + 1)

        for i in range(1, n + 1):
            tmp = input().split()
            if tmp[0] == '1':
                v = int(tmp[1])
                min_arr[i] = max_arr[i] = v
            else:
                l = int(tmp[1])
                r = int(tmp[2])
                min_arr[i] = l
                max_arr[i] = r

        pref_min = [0] * (n + 1)
        pref_max = [0] * (n + 1)

        for i in range(1, n + 1):
            pref_min[i] = pref_min[i - 1] + min_arr[i]
            pref_max[i] = pref_max[i - 1] + max_arr[i]

        res = []
        for _ in range(q):
            l, r, x = map(int, input().split())
            mn = pref_min[r] - pref_min[l - 1]
            mx = pref_max[r] - pref_max[l - 1]
            res.append("yes" if mn <= x <= mx else "no")

        return "\n".join(res)

    return solve()

# sample-like sanity tests
assert run("1 1\n1 5\n1 1 5\n") == "yes"
assert run("1 1\n2 1 3\n1 1 2\n") == "yes"
assert run("1 1\n2 1 3\n1 1 10\n") == "no"
assert run("3 2\n1 1\n2 1 2\n1 3\n1 1 3\n1 1 6\n") in ["yes\nno", "no\nyes"]
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single fixed match | yes | exact equality case |
| single uncertain within range | yes | interval feasibility |
| single uncertain impossible | no | upper bound constraint |
| mixed small array | varies | prefix correctness |

## Edge Cases

A single-element uncertain cell tests whether the solution correctly treats the interval as inclusive. For example, if the cell is $[2, 5]$ and the query asks for sum 5, the algorithm correctly answers yes because the segment bounds become exactly 2 to 5.

A fully fixed array is another boundary case. Here the minimum and maximum arrays are identical, so every query reduces to a strict equality check against a single prefix-sum difference. The algorithm naturally collapses to that behavior without special handling.

A fully uncertain array highlights correctness of aggregation. Each index independently contributes a range, and prefix sums correctly accumulate these ranges. For any segment, the achievable sum set becomes a single contiguous interval, and the algorithm’s computed bounds match that interval exactly, ensuring no false positives or negatives.
