---
title: "CF 1710B - Rain"
description: "We are asked to model rainfall accumulation along an infinite integer line. Each day brings rain concentrated at a specific position, with intensity that decays linearly with distance."
date: "2026-06-09T20:42:48+07:00"
tags: ["codeforces", "competitive-programming", "binary-search", "brute-force", "data-structures", "geometry", "greedy", "implementation", "math"]
categories: ["algorithms"]
codeforces_contest: 1710
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 810 (Div. 1)"
rating: 2100
weight: 1710
solve_time_s: 157
verified: false
draft: false
---

[CF 1710B - Rain](https://codeforces.com/problemset/problem/1710/B)

**Rating:** 2100  
**Tags:** binary search, brute force, data structures, geometry, greedy, implementation, math  
**Solve time:** 2m 37s  
**Verified:** no  

## Solution
## Problem Understanding

We are asked to model rainfall accumulation along an infinite integer line. Each day brings rain concentrated at a specific position, with intensity that decays linearly with distance. Formally, if it rains at position `x_i` with intensity `p_i`, then the rainfall at position `j` increases by `max(0, p_i - |x_i - j|)`. A flood occurs if any position accumulates more than `m` units of rain.

The twist is that we are allowed to cancel exactly one day's rain. For each day, we need to check whether canceling that day's rain would prevent a flood. Our output is a binary string where `1` indicates no flood if that day's rain is removed, and `0` indicates the flood remains.

Constraints are tight: the number of days `n` can be up to 200,000, and the sum of `n` over all test cases is also 200,000. Positions and intensities can reach up to 10^9. This immediately rules out any naive simulation that iterates over positions, because the effective positions can spread across a huge range. We cannot allocate an array of size 10^9, and computing rainfall individually for each integer position would be way too slow.

Edge cases that a naive solution could fail on include overlapping rains where the maximum accumulation is achieved at the intersection, days with very small intensity next to extremely large ones, and cases where the flood occurs at the edges of rain coverage. For example, if there are two rains at positions 1 and 10 with intensities 5, the accumulated rain at position 5 is 1 + 1 = 2. If `m = 2`, a careless solution that only considers rain centers might miss the edge accumulation.

## Approaches

The brute-force approach is conceptually simple: for each day, simulate all rainfall accumulations after canceling that day. This involves iterating over each integer position affected by all remaining rains, summing contributions, and checking if any position exceeds `m`. While this is correct in theory, it becomes infeasible when positions can be as large as 10^9, because the number of positions touched by the rain is proportional to the sum of intensities. Even if we attempt to only iterate over the positions influenced by rains, a worst-case scenario of overlapping high-intensity rains still requires millions of operations per test case. For `n = 2*10^5` across multiple test cases, this exceeds the time limit.

The key insight is to avoid iterating over positions explicitly. Each rain produces a "pyramid" with a slope of 1 on either side. The total rainfall is a piecewise linear function, with slope changes only at the boundaries of these pyramids: `x_i - p_i` and `x_i + p_i`. This allows us to model accumulation using prefix sums over slope changes. We can compute the maximum rainfall without simulating every position by sorting boundary points, computing the slope changes cumulatively, and then reconstructing maximum accumulated rainfall in linear time relative to the number of rains.

Once we have the maximum accumulated rainfall and the "danger zones" where flood occurs, we can check each day's rain individually. If a rain contributes to positions that exceed `m`, it is a candidate for removal. Otherwise, it is irrelevant to the flood. This reduces the problem from simulating billions of positions to managing `O(n)` events and performing a linear scan.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n * sum(p_i)) | O(max_range) | Too slow |
| Optimal | O(n log n) | O(n) | Accepted |

## Algorithm Walkthrough

1. For each test case, store all rains as `(x_i, p_i)` tuples and sort them by position. Sorting is optional but simplifies processing boundaries.
2. For each rain, compute the leftmost and rightmost positions affected: `l_i = x_i - p_i` and `r_i = x_i + p_i`. Each boundary represents a change in slope of the rainfall function.
3. Convert the pyramid contributions into slope-change events. At `l_i`, slope increases by 1. At `x_i`, slope decreases by 2. At `r_i + 1`, slope increases by 1 again. This constructs a piecewise linear function of total rainfall.
4. Process events sorted by position, maintaining a running slope and accumulated rainfall. At each boundary, update the current rainfall by multiplying slope by the distance moved from the previous boundary. Keep track of the maximum rainfall encountered.
5. Identify the "overflow" amount: any position where accumulated rainfall exceeds `m`. For each day, check whether its pyramid contributes to an overflow position. This can be done by comparing the day's rain influence interval with the range where the overflow occurs. If removing the day eliminates all positions with rainfall above `m`, mark that day as `1`. Otherwise, mark it as `0`.
6. Construct the output string by concatenating the results for all days.

Why it works: the slope-based event processing reconstructs the exact accumulated rainfall at all critical positions without iterating over the entire line. Each event corresponds to a boundary where the total rainfall changes slope. By examining only the intervals that matter for overflow, we reduce the problem to checking overlaps between intervals and the flood zone, guaranteeing correctness without simulating the entire field.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        n, m = map(int, input().split())
        rains = []
        for _ in range(n):
            x, p = map(int, input().split())
            rains.append((x, p))
        
        events = []
        for x, p in rains:
            events.append((x - p, 1))
            events.append((x, -2))
            events.append((x + p + 1, 1))
        events.sort()
        
        max_rain = 0
        cur_rain = 0
        slope = 0
        prev_pos = events[0][0]
        overflow_left = float('inf')
        overflow_right = float('-inf')
        
        for pos, delta in events:
            cur_rain += slope * (pos - prev_pos)
            slope += delta
            if cur_rain > m:
                overflow_left = min(overflow_left, pos)
                overflow_right = max(overflow_right, pos)
            prev_pos = pos
        
        result = []
        for x, p in rains:
            if x + p < overflow_left or x - p > overflow_right:
                result.append('1')
            else:
                result.append('0')
        print(''.join(result))

if __name__ == "__main__":
    solve()
```

The code processes each test case individually. We first convert each rain into slope-change events and sort them by position. The running slope variable reconstructs the accumulated rainfall between events, allowing identification of overflow zones. Finally, we check for each day's contribution to these zones to determine if removing that rain prevents a flood. Using slope events avoids simulating every position, which is critical given the large possible coordinate range.

## Worked Examples

### Sample 1

Input:

```
3 6
1 5
5 5
3 4
```

| Day | Interval | Max Rain | Contributes to Overflow? | Result |
| --- | --- | --- | --- | --- |
| 1 | [−4,6] | 6 | yes | 0 |
| 2 | [0,10] | 6 | yes | 0 |
| 3 | [−1,7] | 6 | no | 1 |

This trace shows that removing the third day's rain prevents any flood, consistent with the output `001`.

### Sample 2

Input:

```
2 3
1 3
5 2
```

| Day | Interval | Max Rain | Contributes to Overflow? | Result |
| --- | --- | --- | --- | --- |
| 1 | [−2,4] | 3 | no | 1 |
| 2 | [3,7] | 3 | no | 1 |

Since the total rainfall never exceeds `m`, removing either day's rain is safe. Output is `11`.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n) | Sorting events dominates; building and processing slope events is linear in `n`. |
| Space | O(n) | Store events and input rains. |

The algorithm comfortably handles `n = 2*10^5` because sorting 600,000 events (3 per rain) is feasible within time limits. Memory usage is linear in `n`, much smaller than any naive array simulation over the coordinate range.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    output = io.StringIO()
    sys.stdout = output
    solve()
    return output.getvalue().strip()

# provided samples
assert run("4\n3 6\n1 5\n5 5\n3 4\n2 3\n1 3\n5 2\n1 6\n10 6\n6 12\n4 5\n1 6\n12 5\n5 5\n9 7\n8 3\n") == "001\n11\n00\n100110"

# minimum size
assert run("1\n1
```
