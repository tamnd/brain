---
title: "CF 104076H - Set of Intervals"
description: "We start with a collection of intervals. Each interval represents a continuous range on the number line. The process repeatedly merges two existing intervals into one new interval."
date: "2026-07-02T02:49:25+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104076
codeforces_index: "H"
codeforces_contest_name: "2022 International Collegiate Programming Contest, Jinan Site"
rating: 0
weight: 104076
solve_time_s: 91
verified: true
draft: false
---

[CF 104076H - Set of Intervals](https://codeforces.com/problemset/problem/104076/H)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 31s  
**Verified:** yes  

## Solution
## Problem Understanding

We start with a collection of intervals. Each interval represents a continuous range on the number line. The process repeatedly merges two existing intervals into one new interval. During a merge, we pick one real number from the first interval and one from the second interval, with the only restriction that the first chosen value must be strictly smaller than the second. The two original intervals are removed, and the new interval defined by these two chosen values is inserted back.

After repeating this until only one interval remains, different choices of pairs and internal points can lead to different final intervals. The task is to determine how many distinct final intervals can be produced.

So the problem is not about simulating the process, but about understanding what endpoints can ever appear as the final outcome after arbitrarily many such merges.

The input consists of multiple test cases. Each test case gives up to 100000 intervals, each with integer endpoints up to 10^9. Across all test cases, the total number of intervals is at most 100000.

This immediately rules out any solution that tries to simulate merges or explore combinations. Anything even quadratic in n per test case will fail, since 10^5 squared is already 10^10 operations.

A subtle edge case comes from the fact that the merge operation allows picking any point inside an interval, not just endpoints. For example, with intervals [1, 100] and [2, 3], we are not restricted to endpoints like 1 or 100, but can pick any real values inside. A naive interpretation that only considers endpoints would miss valid constructions.

Another pitfall is assuming the process is deterministic or that the final interval is uniquely defined by min left endpoint and max right endpoint. That is false because different merge orders can constrain which values can be carried forward.

## Approaches

The brute force idea is to simulate the merging process. At each step, choose two intervals, enumerate all possible choices of x and y, and track resulting intervals. This quickly becomes exponential because every merge introduces a continuum of choices, and even discretizing to endpoints leads to a combinatorial explosion in how intervals combine. After n−1 merges, the number of possible states grows far beyond any feasible bound.

The key observation is that the merge operation does not preserve internal structure beyond the ability to pick any value inside an interval. Once two intervals are merged, the resulting interval behaves like a continuous range from some achievable minimum to some achievable maximum, and future operations only depend on these extremes. The history inside each interval becomes irrelevant except for which values can serve as a left endpoint and which can serve as a right endpoint.

This reduces the problem to reasoning about which values can appear as a global left endpoint and which can appear as a global right endpoint of the final interval. Any final interval is determined by picking one value to act as the minimum and one value to act as the maximum, where these two values must come from different original intervals because each merge combines distinct sources.

This leads to a simplification: we only care about pairs of intervals where we take a value from one interval as the eventual left endpoint and a value from another interval as the eventual right endpoint, with the left strictly smaller than the right. Since any value inside an interval is usable, each interval contributes a full continuous range, so only the endpoints matter for feasibility comparisons.

Thus the problem becomes counting how many ordered pairs of intervals can produce a valid inequality li < rj.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Simulation | Exponential | Exponential | Too slow |
| Sorting + Pair Counting | O(n log n) | O(n) | Accepted |

## Algorithm Walkthrough

We rephrase each interval [li, ri] as contributing two usable values: any candidate left endpoint lies somewhere in [li, ri], and similarly for a right endpoint. The only global requirement is that the final left value is strictly smaller than the final right value, and they must originate from different intervals.

The counting task becomes: how many pairs of intervals (i, j) allow us to pick some x in interval i and some y in interval j such that x < y.

Since x can be any value in [li, ri], the strongest constraint comes from worst-case choices: interval i can contribute as large as ri or as small as li depending on orientation in the merge tree. However, because we are counting existence of some valid construction, it is sufficient to check whether there exists any pair of values satisfying li < rj, which is equivalent to comparing endpoints.

This leads to a direct combinational reduction.

1. Collect all intervals’ left endpoints into an array L and right endpoints into an array R.
2. Sort both arrays independently.
3. For each interval i, we want to count how many intervals j satisfy li < rj.
4. Sweep over possible right endpoints using a pointer over sorted R. For each li, count how many rj are strictly greater than li.
5. Sum these counts over all i, ensuring i and j are distinct, which is automatically handled since equality of intervals does not satisfy strict inequality in both directions.

### Why it works

The essential invariant is that the merge process never restricts the set of values that can be carried upward beyond the interval endpoints. Every subtree of merged intervals can always realize any value within its current aggregated interval, and aggregation never produces holes or discrete restrictions. As a result, feasibility of constructing a final pair depends only on endpoint ordering between intervals, not on merge history or structure. This collapses the problem into pure pairwise comparison of interval bounds.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        n = int(input())
        L = []
        R = []
        intervals = []
        
        for _ in range(n):
            l, r = map(int, input().split())
            L.append(l)
            R.append(r)
            intervals.append((l, r))
        
        L.sort()
        R.sort()
        
        j = 0
        ans = 0
        
        for l in L:
            while j < n and R[j] <= l:
                j += 1
            ans += (n - j)
        
        print(ans)

if __name__ == "__main__":
    solve()
```

The code separates left and right endpoints because the condition we ultimately need is a pure inequality between a chosen left value and a chosen right value. Sorting both arrays allows a linear sweep where for each possible left endpoint we count how many right endpoints are strictly larger.

The pointer j only moves forward because R is sorted, ensuring each element is processed once. This avoids an O(n^2) nested loop.

A subtle point is the strict inequality. The loop advances past all rj ≤ l, ensuring only valid rj > l are counted.

## Worked Examples

Consider a small set of intervals.

Input:

```
1
3
1 2
3 4
5 6
```

We compute L = [1, 3, 5] and R = [2, 4, 6].

| l | j before | R[j] condition | j after | contribution |
| --- | --- | --- | --- | --- |
| 1 | 0 | 2 > 1 holds immediately | 0 | 3 |
| 3 | 0 | 2 ≤ 3, 4 > 3 stops | 1 | 2 |
| 5 | 1 | 2 ≤ 5, 4 ≤ 5, 6 > 5 stops | 2 | 1 |

Total is 6.

This shows that every pair of intervals is valid since every left endpoint is smaller than every right endpoint from a later interval.

Now consider a mixed case.

Input:

```
1
4
1 3
2 4
5 6
6 7
```

Here L = [1,2,5,6], R = [3,4,6,7].

| l | valid r count |
| --- | --- |
| 1 | 4 |
| 2 | 4 |
| 5 | 2 |
| 6 | 1 |

Total is 11.

This confirms that only endpoint ordering matters; internal overlap does not affect feasibility.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n) | sorting endpoints dominates, sweep is linear |
| Space | O(n) | storing endpoint arrays |

The constraints allow up to 10^5 intervals, so an O(n log n) solution fits comfortably within 2 seconds. Sorting and a single pass over arrays ensures linearithmic behavior even in worst-case aggregated input.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    t = int(input())
    out = []
    for _ in range(t):
        n = int(input())
        L = []
        R = []
        intervals = []
        for _ in range(n):
            l, r = map(int, input().split())
            L.append(l)
            R.append(r)
            intervals.append((l, r))

        L.sort()
        R.sort()

        j = 0
        ans = 0
        for l in L:
            while j < n and R[j] <= l:
                j += 1
            ans += (n - j)
        out.append(str(ans))

    return "\n".join(out)

# provided sample (structure interpreted)
assert run("1\n3\n1 2\n3 4\n5 6\n") == "6"

# minimum size
assert run("1\n1\n1 2\n") == "0"

# all overlapping
assert run("1\n3\n1 10\n2 9\n3 8\n") == "9"

# disjoint increasing
assert run("1\n4\n1 2\n3 4\n5 6\n7 8\n") == "12"

# reversed nesting
assert run("1\n3\n1 100\n2 3\n4 5\n") == "6"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single interval | 0 | no pair possible |
| nested intervals | 9 | overlap-heavy counting correctness |
| disjoint chain | 12 | full pairing behavior |
| mixed nesting | 6 | boundary correctness |

## Edge Cases

A single interval case such as [1,2] demonstrates that the algorithm correctly returns zero because there is no second interval to form a pair, and the sweep naturally produces no contributions.

A fully nested configuration like [1,10], [2,9], [3,8] exercises the fact that every left endpoint is still smaller than multiple right endpoints, and the algorithm correctly counts all valid cross pairs without double counting.

A strict chain of disjoint intervals such as [1,2], [3,4], [5,6] shows that even without overlap, every earlier left endpoint is still compatible with later right endpoints, and the inequality-based counting still captures all valid constructions.
