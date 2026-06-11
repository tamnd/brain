---
title: "CF 1313D - Happy New Year"
description: "We are given a large line of positions from 1 to $m$, and a collection of $n$ intervals. Each interval represents a “spell” that, when used, adds one candy to every position inside its range. Each spell can be used at most once."
date: "2026-06-11T17:10:25+07:00"
tags: ["codeforces", "competitive-programming", "bitmasks", "dp", "implementation"]
categories: ["algorithms"]
codeforces_contest: 1313
codeforces_index: "D"
codeforces_contest_name: "Codeforces Round 622 (Div. 2)"
rating: 2500
weight: 1313
solve_time_s: 153
verified: false
draft: false
---

[CF 1313D - Happy New Year](https://codeforces.com/problemset/problem/1313/D)

**Rating:** 2500  
**Tags:** bitmasks, dp, implementation  
**Solve time:** 2m 33s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a large line of positions from 1 to $m$, and a collection of $n$ intervals. Each interval represents a “spell” that, when used, adds one candy to every position inside its range. Each spell can be used at most once.

After choosing a subset of spells, each position accumulates a certain number of candies equal to how many chosen intervals cover it. A position is considered “happy” if this number is odd, and “unhappy” otherwise. The goal is to choose a subset of intervals maximizing the number of positions with an odd coverage count.

A direct interpretation is that each interval toggles the parity of all positions in its range. We are trying to maximize how many points end up with parity 1 after applying a subset of these range flips.

The key difficulty comes from the constraints. The number of intervals $n$ is up to $10^5$, while the coordinate range $m$ is up to $10^9$. This immediately rules out any solution that explicitly builds an array of size $m$ or simulates each position. Any valid approach must compress the structure of the problem into the endpoints of intervals, since only those matter for changes in coverage.

A second constraint is that each position ends up with at most $k \le 8$ candies if all spells are used. This is crucial because it bounds the overlap structure locally and enables state compression ideas.

A subtle issue is that positions are independent except through interval overlaps. However, intervals interact in a global way: choosing one interval changes parity across a whole segment, which affects all other intervals overlapping it.

A naive but tempting mistake is to think greedy selection of intervals with largest “gain” works. For example, consider intervals:

```
1 5
2 6
3 7
```

Any greedy attempt to pick locally beneficial intervals fails because parity effects interact, and a locally good interval may cancel out future gains.

Another edge case is when intervals are identical or heavily overlapping. If two identical intervals are chosen, they cancel in parity, so selecting both is equivalent to selecting none. A naive approach that treats each interval independently misses this XOR structure.

## Approaches

If we ignore constraints, we could try iterating over all subsets of intervals. For each subset, we simulate coverage over all positions and count how many positions are covered an odd number of times. This is correct, since it directly matches the definition of happiness. However, this requires $2^n$ subsets, and for $n = 10^5$, this is completely infeasible. Even for $n = 40$, this becomes borderline.

A slightly more structured brute force is to compress coordinates and simulate coverage using prefix sums for each subset. This still leaves the exponential choice of subsets intact, so the bottleneck remains.

The key structural observation is that the answer depends only on the parity of coverage, and each interval contributes a bitwise toggle over a segment. This is a classic “XOR of intervals” structure.

If we sweep the line, the state at any position depends only on which active intervals are currently contributing. As we move from left to right, intervals enter and leave the active set. Since $k \le 8$, at most 8 intervals can overlap at any point in an optimal configuration sense, which suggests that the system has small effective dimension at any boundary event.

We sort interval endpoints and process events. Between consecutive endpoints, the set of active intervals is fixed. What matters is the parity of how many chosen intervals cover that segment. So the problem becomes: for each segment between consecutive compressed coordinates, decide which subset of active intervals to choose, and ensure consistency when intervals start and end.

This leads to a DP over sweep-line states where the state is the current subset of active intervals. Since at any moment the number of active intervals is at most $k \le 8$, the number of states is bounded by $2^k \le 256$. Transitions correspond to adding or removing intervals at endpoints, while optionally choosing whether each interval is included in the final subset.

We maximize total contribution over segments where a state produces a given parity.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force over subsets | $O(2^n \cdot m)$ | $O(m)$ | Too slow |
| Sweep line + DP over active subsets | $O(n \cdot 2^k)$ | $O(2^k)$ | Accepted |

## Algorithm Walkthrough

We convert the problem into a sweep over sorted interval endpoints.

1. We compress all interval endpoints into a sorted list of critical positions. Between consecutive coordinates, nothing changes, so each segment contributes independently once we fix which intervals are active.
2. We sort events by position, marking when intervals start and end. We sweep from left to right, maintaining a current set of active intervals. Each active interval corresponds to a binary choice: selected or not selected in the final subset.
3. At each segment, we consider all subsets of currently active intervals. For a fixed subset, the parity contribution on this segment is determined by how many chosen intervals are active over it. If this number is odd, every position in the segment becomes happy, so we add segment length to the score.
4. We maintain a DP array over subsets of active intervals. When we move from one event position to the next, we transition DP states by updating which intervals enter or leave the active set. Removing an interval collapses states by dropping that bit; adding introduces a new dimension and expands states by duplicating existing values across choices of the new bit.
5. At each step, we update DP with the best achievable score for each subset configuration, accumulating contributions of the current segment.

After processing all segments, the maximum value over all DP states is the answer.

### Why it works

The DP state encodes exactly which active intervals are chosen in the final solution at a given sweep position. Any valid global selection corresponds to exactly one path through these states as intervals are introduced and removed. The contribution of each segment depends only on the parity of chosen intervals covering that segment, which is fully determined by the current state. Since transitions preserve consistency of inclusion decisions across the sweep, no valid configuration is missed, and no invalid configuration is introduced.

## Python Solution

```
PythonRun
```
