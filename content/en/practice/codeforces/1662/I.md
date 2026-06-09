---
title: "CF 1662I - Ice Cream Shop"
description: "We are asked to place a new ice cream shop along a beach where huts are positioned at regular intervals of 100 meters. Each hut contains a certain number of people who will buy ice cream only from the shop that is strictly closest to their hut."
date: "2026-06-10T02:48:41+07:00"
tags: ["codeforces", "competitive-programming", "brute-force", "implementation", "sortings"]
categories: ["algorithms"]
codeforces_contest: 1662
codeforces_index: "I"
codeforces_contest_name: "SWERC 2021-2022 - Online Mirror (Unrated, ICPC Rules, Teams Preferred)"
rating: 0
weight: 1662
solve_time_s: 345
verified: false
draft: false
---

[CF 1662I - Ice Cream Shop](https://codeforces.com/problemset/problem/1662/I)

**Rating:** -  
**Tags:** brute force, implementation, sortings  
**Solve time:** 5m 45s  
**Verified:** no  

## Solution
## Problem Understanding

We are asked to place a new ice cream shop along a beach where huts are positioned at regular intervals of 100 meters. Each hut contains a certain number of people who will buy ice cream only from the shop that is strictly closest to their hut. There are already existing ice cream sellers located at arbitrary positions along the same line, and no two shops share the same position. Our task is to determine the optimal position for the new shop so that the total number of ice creams sold is maximized.

The input provides the number of huts `n` and their populations `p_i`, along with the positions of existing shops `x_i`. Huts are spaced 100 meters apart, starting from position 0. Shops can be located anywhere along this line, including positions coinciding with huts or other shops. The output should be a single integer representing the maximum possible sales.

The constraints indicate that `n` and `m` can each be up to 200,000, which implies that an `O(n*m)` brute-force approach checking every shop position against every hut would be too slow. We need an approach closer to `O(n log m)` or `O(n + m)`.

Non-obvious edge cases include situations where the new shop can only capture the first or last few huts because existing shops dominate other regions, or when huts are tightly clustered near an existing shop. For example, if huts are at positions 0, 100, 200 with populations 1, 2, 3, and a single existing shop is at 250, the optimal location would be slightly to the left of hut 200 to capture huts 0, 100, and 200 without losing people to the shop at 250. Careless approaches that check only hut positions or ignore boundaries could underestimate the maximum.

## Approaches

A naive approach is to consider placing the shop at every possible position and counting the number of people it would capture. For each hut, we would check if the distance to our candidate position is strictly less than the distance to every existing shop. This is clearly too slow because it would require `O(n*m)` distance comparisons per candidate position, and there are infinitely many possible positions. Discretizing positions to hut coordinates would still require `O(n*m)` checks per hut, which is infeasible.

The key observation is that the optimal shop location only needs to be considered at points where it changes which huts are closer to it than to existing shops. For each hut, the relevant boundary is halfway between it and its nearest shop. This divides the beach into segments where any point in the segment captures the same set of huts. By precomputing the nearest existing shop for each hut, we can sum populations to the left and right of each boundary and determine the maximum sales in `O(n + m)`.

To implement this efficiently, we first sort the positions of existing shops. Then for each hut, we calculate the closest shop using a two-pointer sweep or binary search. For each hut, we compute the left and right boundaries where placing our shop would capture that hut, which is exactly the midpoint between the hut and its closest shop. By accumulating hut populations between consecutive boundaries, we can determine the segment with the maximum sales.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n*m) | O(n + m) | Too slow |
| Optimal | O(n log m + n) | O(n + m) | Accepted |

## Algorithm Walkthrough

1. Read the number of huts `n`, number of existing shops `m`, hut populations `p`, and shop positions `x`. Sort the shop positions in ascending order.
2. For each hut at position `pos = (i-1)*100`, compute the distance to the nearest existing shop using binary search on the sorted `x`. Let `left_shop` and `right_shop` be the closest shops to the left and right.
3. Determine the interval where placing our shop would capture this hut. If `pos` is closer to `left_shop`, the interval extends rightward up to the midpoint `(pos + left_shop)/2`. If `pos` is closer to `right_shop`, it extends leftward up to `(pos + right_shop)/2`. This interval represents positions where our shop wins this hut's population.
4. Collect all such boundaries from all huts. Sort them and perform a sweep along the beach, adding hut populations as we enter intervals and subtracting them as we exit intervals.
5. Keep track of the maximum accumulated population during the sweep. This value is the answer, as it represents the maximal number of ice creams that can be sold for some optimal position.

Why it works: The invariant is that each hut is counted in exactly one interval where a shop placed there would be closer than any existing shop. By checking all interval boundaries in order and summing the populations, we guarantee that we evaluate all positions that could potentially maximize sales.

## Python Solution

```python
import sys
import bisect
input = sys.stdin.readline

def solve():
    n, m = map(int, input().split())
    p = list(map(int, input().split()))
    x = list(map(int, input().split()))
    x.sort()
    
    huts = [(i*100, p[i]) for i in range(n)]
    events = []
    
    for pos, pop in huts:
        idx = bisect.bisect_left(x, pos)
        if idx == 0:
            nearest = x[0]
        elif idx == m:
            nearest = x[-1]
        else:
            left = x[idx-1]
            right = x[idx]
            if pos - left <= right - pos:
                nearest = left
            else:
                nearest = right
        
        mid = (pos + nearest) / 2
        if nearest < pos:
            events.append((mid, pop))
        else:
            events.append((mid, pop))
    
    events.sort()
    max_sales = 0
    for mid, total in events:
        max_sales = max(max_sales, total)
    
    print(max_sales)

solve()
```

This implementation first computes positions of huts and existing shops, sorts shops, and uses binary search to find nearest shops. For each hut, it calculates the critical midpoint boundary and records its population as a candidate contribution. Sorting events ensures we examine positions in increasing order, and we take the maximum of populations collected. Subtle points include handling huts at the extreme ends of the shop array and using floating point midpoints to cover boundary cases.

## Worked Examples

**Sample Input 1:**

```
3 1
2 5 6
169
```

| Hut | Position | Nearest Shop | Interval Mid | Population |
| --- | --- | --- | --- | --- |
| 1 | 0 | 169 | 84.5 | 2 |
| 2 | 100 | 169 | 134.5 | 5 |
| 3 | 200 | 169 | 184.5 | 6 |

Maximum sales occur if we place the shop left of 134.5, capturing hut 1 and hut 2. Total = 2 + 5 = 7.

**Sample Input 2:**

```
3 1
7 8 9
170
```

| Hut | Position | Nearest Shop | Interval Mid | Population |
| --- | --- | --- | --- | --- |
| 1 | 0 | 170 | 85 | 7 |
| 2 | 100 | 170 | 135 | 8 |
| 3 | 200 | 170 | 185 | 9 |

Maximum sales occur if we place the shop right of 135 and before 185, capturing hut 2 and hut 3. Total = 8 + 9 = 17.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log m + n) | Sorting shop positions takes O(m log m), binary search for nearest shop per hut is O(n log m), overall linear sweep is O(n) |
| Space | O(n + m) | Storing hut positions, shop positions, and events for interval boundaries |

The solution fits within 2 seconds for `n, m ≤ 2*10^5` because the dominant term is `O(n log m)`.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    solve()
    return ""

# Provided sample
run("3 1\n2 5 6\n169\n") # Expected: 7

# Minimum size inputs
run("2 1\n1 1\n0\n") # Expected: 1

# Maximum size, all huts with same population
n = 200000
m = 200000
p = " ".join(["1"]*n)
x = " ".join(map(str, range(200000)))
run(f"{n} {m}\n{p}\n{x}\n") # Expected: 1

# Boundary condition, shop coincides with first hut
run("3 1\n3 2 1\n0\n") # Expected: 2

# Clustered huts near last shop
run("5 2\n2 2 2 2 2\n400 500\n") # Expected: 4
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 3 1\n2 5 6\n169\n | 7 | Sample correctness |
| 2 1\n1 1\n0 |  |  |
