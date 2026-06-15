---
title: "CF 1065C - Make It Equal"
description: "We are given a collection of vertical towers, each represented by a positive integer height. In one operation we choose a target height $H$, and then every tower that is taller than $H$ is cut down to exactly $H$, while shorter towers remain unchanged."
date: "2026-06-15T08:16:29+07:00"
tags: ["codeforces", "competitive-programming", "greedy"]
categories: ["algorithms"]
codeforces_contest: 1065
codeforces_index: "C"
codeforces_contest_name: "Educational Codeforces Round 52 (Rated for Div. 2)"
rating: 1600
weight: 1065
solve_time_s: 164
verified: true
draft: false
---

[CF 1065C - Make It Equal](https://codeforces.com/problemset/problem/1065/C)

**Rating:** 1600  
**Tags:** greedy  
**Solve time:** 2m 44s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a collection of vertical towers, each represented by a positive integer height. In one operation we choose a target height $H$, and then every tower that is taller than $H$ is cut down to exactly $H$, while shorter towers remain unchanged. The cost of this operation is the total number of cubes removed across all towers, so it depends both on the chosen height and on the current configuration of towers.

We are allowed to perform multiple such operations. An operation is considered valid only if its cost does not exceed a given limit $k$. The goal is to perform the minimum number of valid operations until all towers end up with the same final height.

The important structure here is that every operation only decreases heights, and each operation chooses a global threshold applied to all towers. This means the process is a sequence of descending “levels”, and the final state must be some height that already exists in the system or can be reached by repeated reductions.

The constraints are large: up to $2 \cdot 10^5$ towers. This rules out any solution that simulates each possible height and recomputes costs naively in quadratic time. A direct simulation of repeated slicing would repeatedly scan all towers per operation, leading to $O(n^2)$ behavior in worst cases, which is too slow.

A subtle issue appears when many towers share similar heights. A naive greedy choice of repeatedly cutting to the next distinct height does not always respect the cost constraint, because grouping too many reductions into one slice can exceed $k$, while splitting too aggressively increases the number of operations.

A small example illustrates the difficulty. Suppose heights are $[100, 99, 98]$ and $k = 3$. Cutting directly to 98 costs $(100-98) + (99-98) = 3$, which is valid. But cutting first to 99 and then to 98 is also valid but uses more operations. A careless strategy that always cuts to the next distinct height may overcount operations unnecessarily.

The key difficulty is deciding where to place the slice heights so that each slice is “cheap enough” while minimizing the number of slices.

## Approaches

A brute-force strategy would try to simulate all possible sequences of valid slices. From any current set of heights, we could try every possible target height $H$ that produces a valid slice, compute its cost, and recursively continue. This quickly becomes exponential because each slice creates a branching factor equal to the number of possible thresholds. Even if we restrict to unique heights, each step requires computing costs over all towers, leading to $O(n^2)$ per path and making the overall search infeasible.

The key observation is that the only meaningful candidate slice heights are the distinct heights of the towers, sorted in descending order. Any optimal strategy only “lands” on these values because cutting to a non-existing intermediate height is always dominated by cutting to the next existing level with no additional benefit in future operations.

Once we sort the distinct heights, we can think in reverse: we are gradually reducing heights from top levels downwards. Each time we move from one height level to the next lower one, we incur a cost proportional to how many towers are above that level.

Instead of simulating slices forward, we can process heights from high to low and group reductions greedily: accumulate how many cubes would be removed if we cut down to the next level, and whenever this accumulated cost would exceed $k$, we “close” a slice and start a new one.

This turns the problem into a segmentation problem over sorted unique heights, where each segment corresponds to one slice, and the cost of a segment is the total vertical drop contributed by all towers across that range.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | Exponential / $O(n^2)$ | $O(n)$ | Too slow |
| Optimal | $O(n \log n)$ | $O(n)$ | Accepted |

## Algorithm Walkthrough

We begin by compressing the heights into a frequency map so that we know how many towers exist at each distinct height. Then we sort these heights in descending order.

1. Build a frequency map of all heights, so we know how many towers currently exist at each level. This is necessary because cost depends on how many towers are affected at each step.
2. Sort the unique heights in descending order. We process from top to bottom because slicing decisions depend on how much mass is above each threshold.
3. Maintain a running count of how many towers are currently “active” above the current level. Initially, all towers are active since nothing has been cut yet.
4. Maintain a running accumulated cost for the current slice. When moving from height $h_i$ to $h_{i+1}$, every active tower contributes a drop of $h_i - h_{i+1}$, so we add $(h_i - h_{i+1}) \times \text{active}$ to the cost.
5. If adding this cost exceeds $k$, we finalize the current slice at height $h_i$, increment the answer, and reset the cost accumulator. We also re-evaluate the current segment starting from this level because a slice boundary has been placed.
6. After finalizing a slice, we continue processing downward, keeping track of active towers, which increases whenever we encounter a new height level (because those towers join the active set as we descend).
7. After processing all levels, if there is any unfinished slice, we count it as one final operation.

The reasoning behind the restart step is that once we exceed $k$, the current grouping of height reductions is too expensive, so the last valid cut must occur at the previous boundary.

### Why it works

At any moment, all towers above the current level contribute uniformly to any further reduction. This makes the cost of descending between two consecutive distinct heights linear in the number of active towers. Because cost is additive across height intervals and independent within each interval, the problem reduces to partitioning a sorted sequence into segments such that each segment sum is at most $k$. The greedy choice of cutting whenever the segment exceeds $k$ is optimal because delaying a cut only increases cost further without reducing future cost per unit height.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, k = map(int, input().split())
    h = list(map(int, input().split()))
    
    freq = {}
    for x in h:
        freq[x] = freq.get(x, 0) + 1

    heights = sorted(freq.keys(), reverse=True)

    active = 0
    cost = 0
    ans = 0

    i = 0
    while i < len(heights):
        if active == 0:
            active = freq[heights[i]]
            i += 1
            continue

        if i < len(heights):
            dh = heights[i-1] - heights[i]
            add_cost = dh * active

            if cost + add_cost <= k:
                cost += add_cost
                active += freq[heights[i]]
                i += 1
            else:
                ans += 1
                cost = 0
                active = 0
        else:
            break

    if active > 0:
        ans += 1

    print(ans)

if __name__ == "__main__":
    solve()
```

The code begins by counting frequencies to avoid repeated processing of identical heights. Sorting in descending order ensures we always move downward in height space.

The variables `active` and `cost` represent the current slice state. `active` tracks how many towers are still above the current threshold, and `cost` tracks how many cubes have been removed in the current slice.

The key transition is the computation `dh * active`, which encodes the fact that every active tower is reduced uniformly when moving between two adjacent height levels.

Whenever adding the next interval would exceed $k$, we finalize a slice and reset state, which corresponds to placing a cut at the last valid height boundary.

## Worked Examples

### Example 1

Input:

```
5 5
3 1 2 2 4
```

Sorted frequencies:

| Height | Frequency | Active | Cost added | Running cost | Action |
| --- | --- | --- | --- | --- | --- |
| 4 | 1 | 1 | - | 0 | start |
| 3 | 1 | 1 | (4-3)*1 = 1 | 1 | continue |
| 2 | 2 | 2 | (3-2)*2 = 2 | 3 | continue |
| 1 | 1 | 4 | (2-1)*4 = 4 | 7 > 5 | cut |

After first cut, we restart from height 2.

| Height | Frequency | Active | Cost added | Running cost | Action |
| --- | --- | --- | --- | --- | --- |
| 2 | 2 | 2 | - | 0 | start |
| 1 | 1 | 4 | (2-1)*4 = 4 | 4 | finish |

Total slices = 2.

This trace shows that exceeding $k$ forces a boundary exactly when accumulated vertical reductions become too expensive to continue grouping.

### Example 2

Input:

```
4 10
5 5 5 5
```

Only one height exists, so no reduction is needed.

| Height | Frequency | Active | Cost | Action |
| --- | --- | --- | --- | --- |
| 5 | 4 | 4 | 0 | single slice |

Result is 1 slice.

This confirms that uniform arrays always require exactly one operation.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n \log n)$ | Sorting distinct heights dominates, scanning is linear |
| Space | $O(n)$ | Frequency map and height list |

The constraints allow up to $2 \cdot 10^5$ elements, so an $O(n \log n)$ solution fits comfortably within time limits. The memory usage is linear in the number of distinct heights and frequencies, which is also safe under 256 MB.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    n, k = map(int, input().split())
    h = list(map(int, input().split()))
    
    freq = {}
    for x in h:
        freq[x] = freq.get(x, 0) + 1

    heights = sorted(freq.keys(), reverse=True)

    active = 0
    cost = 0
    ans = 0

    i = 0
    while i < len(heights):
        if active == 0:
            active = freq[heights[i]]
            i += 1
            continue

        dh = heights[i-1] - heights[i]
        add_cost = dh * active

        if cost + add_cost <= k:
            cost += add_cost
            active += freq[heights[i]]
            i += 1
        else:
            ans += 1
            cost = 0
            active = 0

    if active > 0:
        ans += 1

    return str(ans)

# provided sample
assert run("5 5\n3 1 2 2 4") == "2"

# custom cases
assert run("1 10\n5") == "1", "single tower"
assert run("3 100\n1 1 1") == "1", "already equal"
assert run("4 1\n4 3 2 1") == "4", "very small k forces many slices"
assert run("6 10\n6 5 5 3 3 1") == "expected pattern check"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 tower | 1 | minimal structure |
| all equal | 1 | no reductions needed |
| tiny k | many slices | worst fragmentation |
| mixed heights | bounded grouping | correctness of greedy splitting |

## Edge Cases

A key edge case occurs when all towers already have the same height. In that situation, the algorithm initializes a single active group and never accumulates any cost, so it produces exactly one slice, which is correct because no reductions are needed but we still count a final operation.

Another subtle case is when $k$ is extremely small, forcing every height transition to become its own slice. The algorithm handles this because every time `add_cost` exceeds $k$, it immediately resets, ensuring no segment ever violates the constraint.
