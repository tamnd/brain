---
title: "CF 1669D - Colorful Stamp"
description: "We are given a line of cells that starts completely empty, and we are allowed to apply a special operation that always acts on exactly two adjacent positions. Each application recolors those two cells into different colors, one red and one blue, in either order."
date: "2026-06-10T01:56:33+07:00"
tags: ["codeforces", "competitive-programming", "implementation"]
categories: ["algorithms"]
codeforces_contest: 1669
codeforces_index: "D"
codeforces_contest_name: "Codeforces Round 784 (Div. 4)"
rating: 1100
weight: 1669
solve_time_s: 97
verified: true
draft: false
---

[CF 1669D - Colorful Stamp](https://codeforces.com/problemset/problem/1669/D)

**Rating:** 1100  
**Tags:** implementation  
**Solve time:** 1m 37s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a line of cells that starts completely empty, and we are allowed to apply a special operation that always acts on exactly two adjacent positions. Each application recolors those two cells into different colors, one red and one blue, in either order.

The final configuration is fixed in advance as a string consisting of white cells, red cells, and blue cells. White means “never colored”, while red and blue are permanent colors. The task is to determine whether there exists some sequence of adjacent two-cell stamping operations that transforms the initially all-white row into the target string.

Each stamp always affects two neighbors, so it introduces a local constraint: colors are never assigned independently per cell, but always in pairs. Because stamps can overlap and be reapplied, earlier choices can be overwritten, so the problem is not about tracking a construction sequence explicitly, but about checking whether a consistent sequence exists at all.

The constraints are large enough that any solution must run in linear time per test case. Since the total length across all test cases is at most 100,000, even an O(n) or O(n log n) solution per test case is acceptable, but anything quadratic per case would be too slow. This immediately rules out brute-force simulation of all stamping sequences, since the number of ways to apply stamps grows exponentially with the number of positions.

A few edge cases are easy to miss if reasoning locally. A single colored cell like “B” or “R” is impossible because every stamp colors two cells, so isolated single-color requirements cannot be created. Another subtle case is patterns like “WBW” or “WRW”, where a colored cell is surrounded by whites. Even though each colored cell individually looks fine, there is no way to create it without affecting a neighbor, so such configurations fail. A third important case is alternating patterns like “BRBR”, where every adjacent pair is “valid-looking”, but global consistency still matters because each stamp enforces pairing structure that must tile the entire colored region.

## Approaches

A brute-force approach would try to simulate the process: starting from all white, repeatedly choose adjacent pairs and assign them as BR or RB, exploring all possible sequences until we either reach the target string or exhaust possibilities. This is correct in principle because it mirrors the exact rules of construction.

However, each position can be part of many stamping choices, and each stamp placement branches into multiple future states. In the worst case, the number of possible sequences grows exponentially with n, since each of roughly n positions can be paired in multiple ways. Even for n around 50, this becomes infeasible.

The key observation is that we do not actually need to construct the sequence. Each stamp always produces a valid pair of adjacent non-white cells consisting of one R and one B. So in any valid final configuration, every maximal contiguous block of non-white cells must be internally “resolvable” into adjacent pairs that can cover all non-white cells. White cells act as separators that break the problem into independent segments.

Inside any segment without white cells, we are essentially asking whether we can assign each position a color such that every adjacent relationship can be explained by some overlapping BR/RB pairs. The crucial simplification is that a segment is valid if and only if it contains at least one valid starting point for a chain of alternating placements, and no segment forces a single isolated colored cell.

This reduces the problem to a greedy local check: scan the string, split it by whites, and for every contiguous block of non-white cells ensure it has at least one pair of adjacent equal-colored endpoints or at least one adjacent valid interaction that allows propagation. In practice, the known simplification becomes even stronger: any block of length 1 is invalid, and any block of length at least 2 is always constructible.

This is because within any segment of length at least 2, we can always start stamping on any adjacent pair and extend coverage outward while respecting that every stamp only enforces local adjacency constraints. There is enough flexibility due to overlap to realize any multi-cell segment, but a single cell has no partner to originate from.

So the final condition collapses to checking whether every maximal contiguous segment of non-white cells has length at least 2.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(2^n) | O(n) | Too slow |
| Segment check | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

We process each test case independently.

1. Scan the string from left to right while tracking the length of the current contiguous block of non-white cells. We increase the length whenever we see ‘R’ or ‘B’, and reset it when we see ‘W’. This is necessary because white cells break any stamping interaction.
2. Whenever we encounter a white cell or reach the end of the string, we evaluate the segment that just ended. If its length is exactly 1, we immediately know the configuration is impossible because a single cell cannot be produced by any stamp operation.
3. Continue scanning through the rest of the string, repeating the same logic for each segment.
4. After finishing the scan, if no invalid segment of length 1 was found, the configuration is possible.

The key decision point is the moment we close a segment. At that boundary, we have complete information about a maximal region that must be constructed without interruption, so we can safely validate it locally.

### Why it works

Each stamp always produces a pair of adjacent colored cells. This implies that every colored cell must belong to some adjacent pair inside its connected region of non-white cells. If a segment has length 1, there is no adjacent partner available, so no sequence of stamps can ever produce it. Conversely, any segment of length at least 2 can be constructed by starting from one pair and extending outward, since overlapping stamps allow recoloring without breaking adjacency feasibility. This makes segment length the only necessary and sufficient condition.

## Python Solution

```python
import sys
input = sys.stdin.readline

t = int(input())
for _ in range(t):
    n = int(input())
    s = input().strip()

    ok = True
    i = 0

    while i < n:
        if s[i] == 'W':
            i += 1
            continue

        j = i
        while j < n and s[j] != 'W':
            j += 1

        if j - i == 1:
            ok = False
            break

        i = j

    print("YES" if ok else "NO")
```

The solution works by explicitly identifying contiguous non-white blocks and rejecting any block of size one. The scan is linear, and each position is processed at most once.

A subtle implementation detail is ensuring the pointer `i` jumps directly to `j` after processing a block. This avoids double-counting characters and guarantees O(n) behavior. Another important point is that we only evaluate segments when they are fully closed by a white cell or the end of the string, ensuring correctness at boundaries.

## Worked Examples

### Example 1: `BRBBW`

We track segments of non-white cells.

| Step | Index | Char | Segment Length | Action |
| --- | --- | --- | --- | --- |
| 1 | 0 | B | 1 | start segment |
| 2 | 1 | R | 2 | continue |
| 3 | 2 | B | 3 | continue |
| 4 | 3 | B | 4 | continue |
| 5 | 4 | W | end | segment length 4 valid |

No invalid segment appears, so answer is YES.

This shows that long contiguous colored regions are valid as long as they are not isolated singletons.

### Example 2: `WBW`

| Step | Index | Char | Segment Length | Action |
| --- | --- | --- | --- | --- |
| 1 | 0 | W | - | reset |
| 2 | 1 | B | 1 | start segment |
| 3 | 2 | W | end | segment length 1 invalid |

This demonstrates the failure case where a single isolated colored cell cannot be formed.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Each character is visited once during segmentation |
| Space | O(1) | Only counters and indices are stored |

The total input size across all test cases is bounded by 100,000, so a linear scan per test case comfortably fits within time limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    input = sys.stdin.readline

    t = int(input())
    out = []
    for _ in range(t):
        n = int(input())
        s = input().strip()

        ok = True
        i = 0
        while i < n:
            if s[i] == 'W':
                i += 1
                continue
            j = i
            while j < n and s[j] != 'W':
                j += 1
            if j - i == 1:
                ok = False
                break
            i = j

        out.append("YES" if ok else "NO")
    return "\n".join(out)

# provided samples (partial inclusion due to length)
assert run("""1
5
BRBBW
""") == "YES"

assert run("""1
1
B
""") == "NO"

# custom cases
assert run("""1
3
WBW
""") == "NO"

assert run("""1
2
BR
""") == "YES"

assert run("""1
4
WWWW
""") == "YES"

assert run("""1
5
RBBRW
""") == "YES"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| WBW | NO | isolated single cell failure |
| BR | YES | minimal valid segment |
| WWWW | YES | empty construction |
| RBBRW | YES | multiple valid segments |

## Edge Cases

A single colored cell such as input “B” triggers immediate failure because the scan produces a segment of length one. The algorithm identifies this when the segment closes at the end of the string, correctly marking it invalid.

A pattern like “WBW” splits into two segments of length one, but even one is enough to reject the case. The scan resets at each white cell, so both segments are independently checked.

A fully white string produces no segments at all, so no invalid condition is ever triggered, and the answer remains YES, matching the fact that we can simply do nothing.
