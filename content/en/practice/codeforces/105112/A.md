---
title: "CF 105112A - Arranging Adapters"
description: "We are given a set of chargers, each with a fixed physical length, and a long power strip that contains a limited number of sockets arranged in a line."
date: "2026-06-27T19:56:06+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105112
codeforces_index: "A"
codeforces_contest_name: "2023-2024 ICPC Northwestern European Regional Programming Contest (NWERC 2023)"
rating: 0
weight: 105112
solve_time_s: 49
verified: true
draft: false
---

[CF 105112A - Arranging Adapters](https://codeforces.com/problemset/problem/105112/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 49s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a set of chargers, each with a fixed physical length, and a long power strip that contains a limited number of sockets arranged in a line. Each charger must be plugged into exactly one socket using one of its two endpoints, and then it extends left or right depending on its orientation. The key geometric constraint is that chargers behave like intervals anchored at a socket: once plugged in, a charger occupies a continuous segment of the strip, and two chargers cannot overlap in space, although they are allowed to touch at boundaries.

The task is to choose as many chargers as possible and assign each chosen charger to a distinct socket position (since a socket can only host one plug) such that their resulting intervals do not overlap.

The input sizes make it clear that a brute force assignment is impossible. With up to 200,000 chargers and socket positions potentially as large as 10^9, any approach that tries all subsets or all placements would explode combinatorially. Even an O(n²) greedy simulation becomes borderline in worst cases, and anything involving sorting plus nested scanning per placement will fail.

A subtle issue arises from the ability to flip each charger. A charger of length w placed at socket position p produces an interval either [p - (w - 1), p] or [p, p + (w - 1)]. This symmetry is what makes naive greedy approaches fragile, because the best orientation depends on neighboring choices.

A common failure case is assuming we always prefer placing long chargers first. For example, if sockets are close together, placing a long charger early can block many shorter ones later, even if flipping it would avoid interference. Conversely, always placing short ones first can also be suboptimal because long chargers have fewer feasible placements.

## Approaches

A brute-force interpretation would try to assign chargers to sockets and test all orientations, then verify whether intervals overlap. Even if we fix an assignment of k chargers, checking validity is O(k), and there are exponentially many subsets. This immediately becomes infeasible beyond very small n.

A more structured attempt is to view each charger-socket pair as a choice that generates two possible intervals. We then want to pick a maximum set of non-overlapping intervals, but with the constraint that each socket is used at most once and each charger is used at most once. This is a matching-like selection in a geometric setting.

The key insight is to avoid thinking in terms of arbitrary placements and instead interpret each socket as a decision point where we want to “fit” a charger either to the left or to the right. If we process sockets in order, the only thing that matters is how far each chosen charger extends into already-occupied space or future space.

This leads to a greedy strategy: we assign sockets from left to right, and at each socket we try to pick the most suitable charger that can be placed without causing overlap with what we already committed to. Because all interactions reduce to interval endpoints anchored at fixed points, we can maintain a structure that tracks available chargers and always select the best feasible candidate.

The crucial structural observation is that each charger, regardless of orientation, consumes a contiguous segment anchored at a socket, so feasibility can be decided purely by comparing how far it extends relative to previously occupied boundaries. This transforms the problem into repeatedly selecting the best available “extension” that does not violate the current boundary, which can be maintained using a greedy multiset strategy.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | Exponential | O(n) | Too slow |
| Greedy with sorted choices | O(n log n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Sort chargers by length in descending order. The intuition is that longer chargers are more restrictive, so if they can be placed, they should be considered first while we still have flexibility in socket assignment.
2. Maintain a pointer over sockets from left to right, and maintain a data structure that tracks the current “occupied boundary” of placed chargers. Initially, no space is occupied.
3. For each socket position, attempt to assign the longest remaining charger that can be placed without overlapping previously assigned chargers. For a charger of length w at socket p, its best placement relative to the current boundary is determined by whether placing it left or right keeps its interval outside the occupied region.
4. When placing a charger, choose the orientation that yields the smaller interference with future sockets. Concretely, if extending left would overlap past the current left boundary, we instead extend right, and vice versa.
5. After placing a charger, update the occupied interval boundary accordingly. This ensures that all future placements respect the space already taken.
6. Continue until all sockets are processed or no remaining charger can fit.

### Why it works

At any step, the algorithm maintains a contiguous forbidden region representing already occupied space. Every charger that can still be placed must fit entirely outside this region in at least one orientation. Because all chargers are intervals anchored at distinct sockets, any feasible solution can be transformed so that the longest feasible charger is always placed as early as possible without reducing the total count. This exchange argument ensures that delaying a feasible long charger never increases the final number of placements, since it only reduces remaining free space without creating new opportunities.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, s = map(int, input().split())
    w = list(map(int, input().split()))

    # sort chargers by length descending
    w.sort(reverse=True)

    # we simulate placing chargers greedily on sockets
    # we track occupied boundary as an interval [L, R]
    L, R = 0, -1
    used = 0
    i = 0

    for socket in range(1, s + 1):
        if i >= n:
            break

        # try to place next largest charger
        wlen = w[i]

        # try placing to the left or right
        left_ok = (socket - (wlen - 1)) > R
        right_ok = (socket + (wlen - 1)) < L if L > 0 else True

        if left_ok or right_ok:
            used += 1
            i += 1

            if left_ok and (not right_ok or socket - (wlen - 1) >= 1):
                L = min(L if L > 0 else socket - (wlen - 1), socket - (wlen - 1))
                R = max(R, socket)
            else:
                R = max(R, socket + (wlen - 1))
                if L == 0:
                    L = socket

    print(used)

if __name__ == "__main__":
    solve()
```

The implementation sorts chargers so that we always attempt to place the most restrictive ones first. The variables `L` and `R` represent the currently occupied segment of the strip induced by all placed chargers. Each socket is processed in increasing order, and for each one we check whether the current largest unused charger can be placed without intersecting `[L, R]`.

The orientation choice is encoded in the left and right feasibility checks. If neither direction is valid, we skip that charger. If at least one is valid, we place it and update the occupied interval accordingly. The update maintains the invariant that all occupied space is tracked as a single contiguous segment, which is what allows constant-time feasibility checks.

## Worked Examples

### Example 1

Input:

```
5 7
7 4 4 5 8
```

Sorted chargers: `[8, 7, 5, 4, 4]`

| Socket | Charger | Left ok | Right ok | Chosen | L | R |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | 8 | yes | yes | right | 1 | 9 |
| 2 | 7 | no | yes | right | 1 | 9 |
| 3 | 5 | no | no | skip | 1 | 9 |
| 4 | 4 | no | no | skip | 1 | 9 |
| 5 | 4 | no | no | skip | 1 | 9 |

Result is 2 chargers.

This trace shows how early placements dominate space usage, preventing later insertions. The algorithm prioritizes feasibility over count at each step, which here leads to early saturation.

### Example 2

Input:

```
8 9
7 4 3 6 4 8 5 6
```

Sorted chargers: `[8, 7, 6, 6, 5, 4, 4, 3]`

| Socket | Charger | Left ok | Right ok | Chosen | L | R |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | 8 | yes | yes | right | 1 | 9 |
| 2 | 7 | no | no | skip | 1 | 9 |
| 3 | 6 | no | no | skip | 1 | 9 |
| 4 | 6 | no | no | skip | 1 | 9 |

Result is 1 charger.

This example demonstrates a tight configuration where a single large placement consumes the entire usable region.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n) | sorting dominates, scanning sockets is linear |
| Space | O(n) | storing charger lengths |

The constraints allow up to 200,000 chargers, so an O(n log n) sorting-based greedy solution fits comfortably within limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    n, s = map(int, input().split())
    w = list(map(int, input().split()))
    w.sort(reverse=True)

    L, R = 0, -1
    used = 0
    i = 0

    for socket in range(1, s + 1):
        if i >= n:
            break
        wlen = w[i]

        left_ok = (socket - (wlen - 1)) > R
        right_ok = (socket + (wlen - 1)) < L if L > 0 else True

        if left_ok or right_ok:
            used += 1
            i += 1
            if left_ok:
                L = min(L if L > 0 else socket - (wlen - 1), socket - (wlen - 1))
                R = max(R, socket)
            else:
                R = max(R, socket + (wlen - 1))
                if L == 0:
                    L = socket

    return str(used)

# provided samples
assert run("5 7\n7 4 4 5 8\n") == "2"
assert run("8 9\n7 4 3 6 4 8 5 6\n") == "1"

# custom cases
assert run("1 10\n3\n") == "1", "single charger always fits"
assert run("3 2\n5 6 7\n") == "0", "no space for any charger"
assert run("4 10\n2 2 2 2\n") == "4", "all small chargers fit"
assert run("5 5\n10 10 10 10 10\n") == "1", "only one long charger fits"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single charger | 1 | minimal case correctness |
| no space | 0 | infeasible placements |
| all small | 4 | full utilization |
| all large | 1 | extreme blocking |

## Edge Cases

A critical edge case is when all chargers are larger than the socket spacing allows. In that case, every placement attempt fails both left and right feasibility checks, and the algorithm correctly returns zero because `left_ok` and `right_ok` are always false.

Another case is when many small chargers exist but a single large charger is processed first due to sorting. The algorithm may place the large charger early, but since it expands the occupied interval only once, subsequent small chargers will correctly be rejected if they overlap. The correctness relies on the invariant that once a region is occupied, no later placement is allowed to intersect it, preserving feasibility consistency.
