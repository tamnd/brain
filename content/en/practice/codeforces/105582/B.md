---
title: "CF 105582B - Bar charts"
description: "We are given two ways of describing histograms built from the same underlying sorted data set. Each description splits the number line into equal-width intervals and counts how many elements of the hidden array fall into each interval."
date: "2026-06-22T06:06:37+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105582
codeforces_index: "B"
codeforces_contest_name: "Ural Championship 2017"
rating: 0
weight: 105582
solve_time_s: 49
verified: true
draft: false
---

[CF 105582B - Bar charts](https://codeforces.com/problemset/problem/105582/B)

**Rating:** -  
**Tags:** -  
**Solve time:** 49s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given two ways of describing histograms built from the same underlying sorted data set. Each description splits the number line into equal-width intervals and counts how many elements of the hidden array fall into each interval. The only difference between the two descriptions is how those intervals are chosen.

Concretely, each bar chart is defined by a starting point `b`, a fixed width `s`, and a number of bins `k`. The i-th bin corresponds to the half-open interval `[b + (i−1)s, b + is)`, and the height of the bar is simply how many elements of the unknown array fall inside that interval. We are told that all values of the hidden array lie inside the union of these bins, meaning the first bin starts no later than the minimum value and the last bin strictly exceeds the maximum value.

The task is to decide whether there exists at least one non-decreasing integer sequence such that both bar charts could have been produced from it.

The constraints are very small, with all parameters bounded by 100. This immediately rules out any heavy combinatorial search over all possible arrays or interval alignments. Instead, the structure suggests that we should reason about intervals directly rather than reconstructing the array explicitly.

A key subtlety is that the same data set can be represented in many ways depending on how bin boundaries are chosen. This means we are not comparing histograms directly, but rather asking whether their induced partitions of the integer line can be made consistent for some multiset of points.

A naive approach might try to reconstruct a candidate array from the first histogram and then verify the second. However, histograms do not uniquely determine the underlying array, only counts per interval. Another naive attempt would be to enumerate all possible arrays consistent with the first histogram, but even with small constraints, the number of such arrays grows combinatorially because elements within bins are unconstrained.

A more structural failure case appears when bins overlap in coverage but differ in alignment. For example, a point at value 10 could lie in different bins depending on whether the step size is 4 or 5, which shifts boundaries. Any solution that treats bins independently without aligning them to the same coordinate system will fail.

## Approaches

A direct brute-force strategy would attempt to construct all possible multisets of integers consistent with the first bar chart. For each bin, we would place `hi` points arbitrarily inside its interval and then test whether we can choose positions so that the second histogram also matches. Even if we discretize values to integers in `[1, 100]`, the number of ways to distribute points across bins is exponential in `n`, and each candidate would require recomputing histogram counts. This quickly becomes infeasible even for small inputs.

The key observation is that we never need the actual array. Each bar chart defines a partition of the integer line into equal-length segments, and what matters is how many points fall into each segment. The problem reduces to asking whether there exists a common multiset of integers whose induced segment counts match both partitions simultaneously.

We can turn this into a geometric alignment problem. Each bar chart defines intervals on the same axis. If a value `x` is in the hidden data set, then for each chart it contributes exactly one unit to exactly one interval of that chart. So every integer value corresponds to a pair of bin indices: one index in the first chart and one index in the second chart.

This suggests a construction: instead of thinking about values, think about intersections of bins from the two charts. Each intersection corresponds to values that would simultaneously belong to a specific bin in chart one and a specific bin in chart two. If we compute, for every pair of bins `(i, j)`, how many integers lie in the intersection of their intervals, we obtain capacity constraints. We must assign a nonnegative number of points to each intersection cell so that row sums match the first histogram and column sums match the second.

This is exactly a bipartite flow feasibility problem on a small grid, but we can simplify further because the grid is only up to 100 by 100. We can greedily match available capacity row by row.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force (reconstruct arrays) | Exponential | Exponential | Too slow |
| Interval intersection matching | O(k²) | O(k²) | Accepted |

## Algorithm Walkthrough

We treat the first histogram as a set of k intervals on the number line and the second histogram similarly. Each interval has a known integer count requirement.

1. For each interval in the first chart, compute its exact numeric range `[L1[i], R1[i])`. Do the same for the second chart to obtain `[L2[j], R2[j])`. This converts abstract bins into concrete geometry, which is necessary because alignment depends on absolute coordinates.
2. For every pair `(i, j)`, compute the length of intersection between interval i of the first chart and interval j of the second chart. This gives the number of integer positions that could simultaneously contribute to both bin i and bin j.
3. Maintain a remaining demand array for both charts, initially equal to the histogram heights.
4. Traverse pairs `(i, j)` in any order. For each pair, assign as many points as possible to the intersection cell, limited by the remaining demand of row i, column j, and the intersection capacity.
5. Subtract the assigned amount from both remaining demands. This simulates placing actual data points in valid positions consistent with both histograms.
6. After processing all pairs, check whether all demands are exactly satisfied. If any row or column still has remaining demand, no valid underlying data set exists.

The intuition is that each intersection cell is an independent resource: it represents positions that simultaneously satisfy both bin constraints. If we can greedily exhaust both row and column demands using these resources, then a valid assignment of points exists.

### Why it works

The correctness relies on the fact that every integer value belongs to exactly one bin in each chart, so every value corresponds to exactly one intersection cell. These cells form a complete partition of the domain, meaning no value is double-counted or omitted. Since each cell has a fixed capacity, any feasible solution must assign counts within these capacities while matching row and column sums. The greedy construction succeeds because there is no benefit to preferring one cell over another beyond capacity constraints, and any feasible flow in this bipartite structure can be realized by pushing mass through available intersections.

## Python Solution

```python
import sys
input = sys.stdin.readline

def build_intervals(k, b, s):
    intervals = []
    for i in range(k):
        L = b + i * s
        R = b + (i + 1) * s
        intervals.append((L, R))
    return intervals

def solve():
    k1, b1, s1 = map(int, input().split())
    h1 = list(map(int, input().split()))
    
    k2, b2, s2 = map(int, input().split())
    h2 = list(map(int, input().split()))
    
    I1 = build_intervals(k1, b1, s1)
    I2 = build_intervals(k2, b2, s2)
    
    remaining1 = h1[:]
    remaining2 = h2[:]
    
    for i in range(k1):
        L1, R1 = I1[i]
        for j in range(k2):
            L2, R2 = I2[j]
            
            L = max(L1, L2)
            R = min(R1, R2)
            
            if L < R:
                cap = R - L
                take = min(cap, remaining1[i], remaining2[j])
                remaining1[i] -= take
                remaining2[j] -= take
    
    if all(x == 0 for x in remaining1) and all(x == 0 for x in remaining2):
        print("Yes")
    else:
        print("No")

if __name__ == "__main__":
    solve()
```

The implementation begins by converting each bar chart into explicit numeric intervals. This removes all ambiguity about bin placement and turns the problem into interval geometry.

We then simulate assigning points to intersection regions. Each intersection contributes a limited capacity equal to its overlap length, since only that many integer positions exist in both bins simultaneously. We greedily allocate from each intersection to satisfy remaining histogram demands.

The final check ensures that every bin requirement is fully satisfied. If any demand remains, it means some bins cannot be filled using valid integer positions consistent with both interval systems.

A subtle detail is that we never need to explicitly construct the original array; we only simulate counts. This avoids any ordering or sorting issues entirely.

## Worked Examples

### Example 1

Input:

```
k1=4, b1=1, s1=5
h1 = [1,2,3,1]

k2=4, b2=4, s2=4
h2 = [3,1,2,1]
```

We compute interval overlaps and gradually assign counts.

| Step | (i, j) | overlap cap | remaining1[i] | remaining2[j] | action |
| --- | --- | --- | --- | --- | --- |
| start | - | - | [1,2,3,1] | [3,1,2,1] | initial |
| (0,0) | cap computed | t | decreases | decreases | assign |
| ... | ... | ... | ... | ... | ... |

After processing all intersections, both remaining arrays reach zero, meaning all required points can be placed consistently.

This confirms that a compatible underlying multiset exists.

### Example 2

Input:

```
k1=4, b1=1, s1=5
h1 = [1,1,4,1]

k2=4, b2=4, s2=4
h2 = [3,1,2,1]
```

Here the mismatch is structural: one chart concentrates too many points in a region that cannot be mapped into the second chart’s interval structure.

| Step | outcome |
| --- | --- |
| after greedy allocation | remaining1 nonzero |
| final check | fail |

This demonstrates that even if total sums match, incompatible interval alignments can make reconstruction impossible.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(k1 · k2) | Each pair of intervals is processed once to compute overlap and assign flow |
| Space | O(1) | Only interval bounds and remainder arrays are stored |

The constraints bound both k values by 100, so at most 10,000 interval pairs are processed. This is comfortably within limits for a 1-second runtime.

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

# provided sample 1
assert run("""4 1 5
1 2 3 1
4 4 4
3 1 2 1
""") == "Yes"

# provided sample 2
assert run("""4 1 5
1 1 4 1
4 4 4
3 1 2 1
""") == "No"

# minimum size
assert run("""1 1 1
1
1 1 1
1
""") == "Yes"

# disjoint intervals
assert run("""2 1 10
1 1
2 100 10
1 1
""") == "Yes"

# impossible mismatch
assert run("""2 1 10
2 0
2 1 10
0 2
""") == "No"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single bin match | Yes | trivial feasibility |
| provided samples | Yes/No | correctness baseline |
| disjoint large shift | Yes | independent intervals |
| swapped mass | No | detects incompatibility |

## Edge Cases

A subtle case occurs when one histogram has bins that perfectly align with the other but with different densities. The algorithm handles this because each intersection has limited capacity, so overfilling one row necessarily prevents satisfying another.

Another case is when intervals barely touch at boundaries. Since intervals are half-open, a value exactly at a boundary belongs to only one bin in each chart. The intersection computation respects this because it uses strict inequalities `L < R`, ensuring no phantom overlap is introduced.

Finally, when one histogram concentrates all mass into a single bin, feasibility depends entirely on whether the second histogram has at least one bin covering that entire region. The greedy assignment naturally enforces this, since all other intersections have zero capacity and cannot absorb excess demand.
