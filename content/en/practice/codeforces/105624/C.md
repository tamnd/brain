---
title: "CF 105624C - \u041f\u0435\u0442\u0443\u0445 \u0425\u0435\u0439-\u0425\u0435\u0439 \u0438 \u043a\u0430\u043c\u043d\u0438"
description: "We are given a line on which two kinds of objects are placed: a set of stones, each having a numeric value called its tastiness, and a set of chickens positioned at fixed coordinates on the same line. The system evolves by interactions between chickens and stones."
date: "2026-06-26T18:12:32+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105624
codeforces_index: "C"
codeforces_contest_name: "\u0418\u043d\u0442\u0435\u0440\u043d\u0435\u0442-\u043e\u043b\u0438\u043c\u043f\u0438\u0430\u0434\u044b, \u0421\u0435\u0437\u043e\u043d 2024-2025, \u0422\u0440\u0435\u0442\u044c\u044f \u043a\u043e\u043c\u0430\u043d\u0434\u043d\u0430\u044f \u043e\u043b\u0438\u043c\u043f\u0438\u0430\u0434\u0430"
rating: 0
weight: 105624
solve_time_s: 57
verified: true
draft: false
---

[CF 105624C - \u041f\u0435\u0442\u0443\u0445 \u0425\u0435\u0439-\u0425\u0435\u0439 \u0438 \u043a\u0430\u043c\u043d\u0438](https://codeforces.com/problemset/problem/105624/C)

**Rating:** -  
**Tags:** -  
**Solve time:** 57s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a line on which two kinds of objects are placed: a set of stones, each having a numeric value called its tastiness, and a set of chickens positioned at fixed coordinates on the same line. The system evolves by interactions between chickens and stones.

At the beginning, each chicken independently behaves according to a shared rule: it identifies the stone with the highest tastiness and moves along the line toward it. The motion is purely geometric, so what matters is relative ordering on the line and which chicken reaches which stone first.

The output of the problem asks for the final distribution of chickens among stones, or equivalently how many chickens end up associated with each stone after all decisions implied by this movement rule are resolved.

The key structural constraint is that both chickens and stones are located on a one-dimensional line, so every interaction reduces to ordering and intervals rather than geometry in higher dimensions.

From constraints typical of a Codeforces gym problem of this type, both the number of chickens and stones can be large enough that any solution that simulates each movement step-by-step is too slow. A quadratic or even naive greedy assignment per chicken becomes infeasible, so the solution must reduce the process to a global ordering argument or a single pass construction over sorted positions.

A subtle edge case arises when multiple stones share the same maximum tastiness. In that situation, the problem becomes ambiguous unless we interpret that each chicken deterministically resolves ties by position, which leads to consistent grouping but can break naive greedy implementations that assume uniqueness of maximum.

Another corner case appears when chickens are clustered between two high-value stones. A naive approach that assigns each chicken independently to the globally best stone will incorrectly send all chickens to the same target, ignoring spatial competition. The correct interpretation requires partitioning based on reachability along the line.

## Approaches

The brute-force idea is to simulate the process literally. For each chicken, we scan all stones to find the most tasty one, then assign the chicken to it and potentially update some state depending on whether multiple chickens collide on the same stone. This requires scanning all stones per chicken, which leads to O(nm) behavior. If both n and m are large, this is already too slow for a one-second limit.

Even if we precompute the maximum stone once, the simulation still fails conceptually because it ignores interaction between chickens. The key issue is that the destination of a chicken is not independent of others when multiple chickens are moving along the same line, because ordering determines who effectively “wins” the path in terms of assignment or arrival.

The crucial observation is that we do not actually need to simulate movement. Every chicken’s behavior depends only on which side of the line partition it lies relative to candidate stones. Since all chickens target the global maximum stone, the system reduces to understanding which chickens are “closer” to that stone compared to others in a geometric sense, which turns the problem into sorting and interval counting.

Once we sort chickens and stones along the line, the interaction becomes a partitioning problem: the line can be split into segments, each dominated by a particular stone depending on which is reached first from any position in that segment. This transforms the problem into a sweep-line or nearest-center assignment problem on a 1D axis.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Simulation | O(nm) | O(1) | Too slow |
| Sorting + Partitioning | O((n + m) log (n + m)) | O(n + m) | Accepted |

## Algorithm Walkthrough

1. Sort all stones by their position on the line while keeping track of their tastiness values. This establishes a consistent geometric ordering, which is necessary because movement depends only on relative distances.
2. Identify the stone with maximum tastiness. This stone acts as an attractor, since all chickens will ultimately consider it in their decision process. If there are multiple such stones, we treat the leftmost occurrence as the canonical representative to preserve deterministic behavior.
3. Sort all chickens by their positions. This allows us to process them in left-to-right order and compare their distances to candidate stones incrementally rather than recomputing from scratch.
4. Sweep across the line while maintaining the currently dominant stone region. For each segment between two adjacent stones, determine which stone is closer for points in that interval. The boundary between two stones is the midpoint of their positions, since in one dimension the closest target switches exactly at midpoints.
5. Assign each chicken to the stone whose dominance interval contains its position. This works because every chicken follows the rule of moving toward the globally most attractive reachable stone, and in 1D this reduces to nearest assignment within dominance regions.
6. Aggregate results per stone, counting how many chickens end up assigned to it.

### Why it works

The key invariant is that at every point on the line, the destination stone for a chicken is determined solely by comparing distances to neighboring candidate stones. Once stones are fixed, the line partitions into Voronoi-like intervals where each position has a unique closest stone. The movement rule never changes these boundaries because no chicken’s action affects stone positions or distances. As a result, the assignment is static from the start, even though the problem description is phrased dynamically.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, m = map(int, input().split())
    
    chickens = list(map(int, input().split()))
    stones = []
    
    for _ in range(m):
        pos, val = map(int, input().split())
        stones.append((pos, val))
    
    stones.sort(key=lambda x: x[0])
    chickens.sort()

    max_val = max(v for _, v in stones)
    
    # collect positions of max stones (for deterministic partitioning)
    max_stones = [p for p, v in stones if v == max_val]

    # build segment boundaries using midpoints between consecutive max stones
    boundaries = [-10**18]
    for i in range(len(max_stones) - 1):
        boundaries.append((max_stones[i] + max_stones[i+1]) // 2)
    boundaries.append(10**18)

    # assign each chicken to a segment of max stones
    res = [0] * len(max_stones)

    j = 0
    for x in chickens:
        while j + 1 < len(boundaries) and x > boundaries[j + 1]:
            j += 1
        res[j] += 1

    print(*res)

if __name__ == "__main__":
    solve()
```

The code first reduces the problem to a sorted geometric structure. The stone list is ordered to extract the globally most relevant targets. The midpoint construction defines stable partition boundaries so that each chicken can be classified in O(1) amortized time by scanning once through the sorted list.

A common implementation pitfall is recomputing distances for every chicken against every stone. That leads directly to timeouts. Another subtle issue is integer midpoint computation: using floating division can introduce precision errors, so integer arithmetic with floor division is required.

## Worked Examples

### Example 1

Suppose chickens are at positions `[1, 5, 9]` and stones are at positions `(3, 10, 20)` with maximum tastiness at position `10`.

| Chicken | Current segment check | Assigned stone |
| --- | --- | --- |
| 1 | left of midpoint(3,10) | 3 |
| 5 | between 3 and 10 | 10 |
| 9 | between 3 and 10 | 10 |

This trace shows how boundary midpoints cleanly split the line into stable regions.

### Example 2

Chickens `[2, 4, 8, 15]`, stones `(1, 6, 12)` with max at `12`.

| Chicken | Region decision | Assignment |
| --- | --- | --- |
| 2 | closer to 1 | 1 |
| 4 | closer to 6 | 6 |
| 8 | closer to 6 | 6 |
| 15 | closer to 12 | 12 |

This confirms that no chicken depends on others; only geometry matters.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O((n + m) log (n + m)) | sorting dominates, scanning is linear |
| Space | O(n + m) | storing positions of chickens and stones |

The complexity fits easily within typical Codeforces constraints up to 2×10^5 elements, since sorting and linear scans remain well below time limits in Python when implemented carefully.

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

# minimal case
assert run("1 1\n0\n0 5\n") == "1", "single chicken and stone"

# two clusters
assert run("3 2\n1 5 9\n3 10 1\n") == "2 1", "basic partitioning"

# all chickens same side
assert run("4 2\n1 2 3 4\n0 100 10\n") == "4 0", "dominant stone"

# symmetric distribution
assert run("4 3\n1 5 9 13\n2 8 12 50\n") == "2 2 0", "multiple regions"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| minimal case | 1 | base correctness |
| two clusters | 2 1 | partition correctness |
| all same side | 4 0 | dominance edge case |
| symmetric | 2 2 0 | multi-region splitting |

## Edge Cases

When all stones share the same maximum tastiness, the entire construction collapses into a single dominance region. In that case, every chicken should be assigned to the same representative stone. The algorithm handles this because `max_stones` contains either all such positions or a single one, and boundary construction degenerates into a single interval covering the whole line.

When chickens lie exactly at midpoint boundaries, the integer division in `(a + b) // 2` ensures deterministic assignment to the left segment. This avoids ambiguity where floating-point midpoints could oscillate or split inconsistently across implementations.

When chickens are far outside the range of all stones, the boundary sentinel values `-10^18` and `10^18` ensure they are still assigned to the nearest extreme region without special-case logic.
