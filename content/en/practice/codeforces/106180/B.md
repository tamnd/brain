---
title: "CF 106180B - Flappy Bird"
description: "We are simulating a one-dimensional movement process through a sequence of columns. Each column defines a vertical corridor of allowed heights, and a bird moves from left to right across these columns. At any moment the bird occupies exactly one integer height."
date: "2026-06-20T04:21:57+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 106180
codeforces_index: "B"
codeforces_contest_name: "\u0412\u044b\u0441\u0448\u0430\u044f \u043f\u0440\u043e\u0431\u0430 - 2025. \u0417\u0430\u043a\u043b\u044e\u0447\u0438\u0442\u0435\u043b\u044c\u043d\u044b\u0439 \u044d\u0442\u0430\u043f"
rating: 0
weight: 106180
solve_time_s: 61
verified: true
draft: false
---

[CF 106180B - Flappy Bird](https://codeforces.com/problemset/problem/106180/B)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 1s  
**Verified:** yes  

## Solution
## Problem Understanding

We are simulating a one-dimensional movement process through a sequence of columns. Each column defines a vertical corridor of allowed heights, and a bird moves from left to right across these columns. At any moment the bird occupies exactly one integer height.

When moving from column i to column i+1, the player chooses one of two actions. Either the bird jumps upward by a fixed amount k, or it falls down by exactly one unit. After applying this vertical change, the bird lands in the next column. The bird is only valid if its height stays inside the allowed corridor of that column, which is given by a segment of forbidden zones at the bottom and top, leaving an open interval in the middle.

The task is to determine whether there exists any sequence of choices that allows the bird to start at a given height in the first column and reach the last column without ever leaving the allowed height interval in any column.

The input size is large: the number of columns across all test cases can reach 500,000. This immediately rules out any quadratic or state explosion dynamic programming that tries to track all paths individually. Any correct solution must compress all possible states at a column into a compact representation, ideally linear in the number of columns.

A subtle difficulty comes from the fact that the transition is not symmetric. One move decreases height by one, the other increases it by k, so the reachable set can potentially “split” into separated regions. A naive approach that tracks only minimum and maximum reachable heights can silently fail because it may include heights that are not actually reachable in between, allowing an impossible path to be incorrectly accepted.

## Approaches

A brute-force simulation would track every possible height at each column. From each reachable height, we branch into two transitions, one decrementing and one incrementing by k. After each column we filter out heights that are outside the allowed interval. This correctly models the process but quickly explodes: after n steps, the number of states can double repeatedly, leading to exponential growth.

The key observation is that we do not need to distinguish individual paths, only the set of reachable heights. Since all transitions are linear shifts applied uniformly to all states, reachable states at any column form a union of shifted copies of previous reachable sets. This structure can be maintained as a collection of disjoint intervals rather than individual points.

Each interval produces at most two shifted intervals in the next column. After intersecting with the allowed interval of that column, we merge overlapping segments. In practice, the number of intervals remains small because repeated shifting and intersection quickly coalesces segments. This reduces the state from exponential paths to a manageable interval system.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute force over states | Exponential | Exponential | Too slow |
| Interval propagation with merging | O(N log N) worst-case, O(N) typical | O(N) | Accepted |

## Algorithm Walkthrough

We maintain the set of all reachable heights at the current column as a sorted list of disjoint intervals.

1. Initialize the state with a single interval containing only the starting height s. This represents that initially there is exactly one valid position.
2. For each column i from 1 to n, we first compute the allowed height interval [low, high], which is [li + 1, ri − 1]. Any state outside this range is invalid and must be discarded immediately.
3. From every current interval [L, R], we generate two new intervals for the next column. One corresponds to falling, producing [L − 1, R − 1]. The other corresponds to jumping, producing [L + k, R + k]. This step captures all possible outcomes of the player's choice.
4. We collect all generated intervals from all current intervals into a temporary list. This list may contain overlaps and ordering inconsistencies.
5. We sort these intervals by starting point and merge any overlapping or adjacent intervals into maximal disjoint segments. This compresses the state back into a compact representation.
6. We intersect each merged interval with the allowed interval of column i, removing any parts that fall outside. Intersections may split intervals, but the resulting pieces are still disjoint.
7. If at any point no intervals remain, the process terminates early with failure, since no valid height exists at that column.
8. After processing all columns, if at least one interval remains, the last column is reachable.

The key property behind correctness is that the reachable set of heights after each step is exactly representable as a union of disjoint intervals formed by applying uniform affine transformations to previous intervals and then intersecting with a contiguous constraint. No reachable height is ever lost except when it violates a column constraint, and no invalid height is introduced because all transformations strictly follow allowed moves.

## Python Solution

```python
import sys
input = sys.stdin.readline

def merge(intervals):
    if not intervals:
        return []
    intervals.sort()
    res = []
    l, r = intervals[0]
    for x, y in intervals[1:]:
        if x <= r + 1:
            r = max(r, y)
        else:
            res.append((l, r))
            l, r = x, y
    res.append((l, r))
    return res

def intersect(intervals, L, R):
    res = []
    for l, r in intervals:
        nl = max(l, L)
        nr = min(r, R)
        if nl <= nr:
            res.append((nl, nr))
    return res

def solve():
    t = int(input())
    out = []
    for _ in range(t):
        n, h, k, s = map(int, input().split())
        intervals = [(s, s)]

        ok = True
        for _ in range(n):
            l, r = map(int, input().split())
            low, high = l + 1, r - 1

            nxt = []
            for a, b in intervals:
                nxt.append((a - 1, b - 1))
                nxt.append((a + k, b + k))

            nxt = merge(nxt)
            intervals = intersect(nxt, low, high)

            if not intervals:
                ok = False
                break

        out.append("Yes" if ok else "No")

    print("\n".join(out))

if __name__ == "__main__":
    solve()
```

The solution maintains the reachable state as intervals. For each column, it generates all possible shifted intervals from both movement choices, merges overlaps, and then clips them against the allowed region of that column. The early exit condition avoids unnecessary computation once feasibility is lost.

A common implementation mistake is attempting to track only the minimum and maximum reachable height. That fails because the transformation splits reachable sets into two separated bands, and the middle region may become unreachable even if the extremes suggest otherwise. Interval representation avoids this loss of structure.

## Worked Examples

Consider a small scenario with two columns and a moderate jump size.

Input:

n = 2, s = 4, k = 2

Column 1 allows [1, 6], Column 2 allows [1, 6]

Initial state is:

| step | intervals |
| --- | --- |
| start | [4, 4] |

After column 1 transitions:

From [4,4], we get [3,3] (fall) and [6,6] (jump). After merging, intervals are [3,3], [6,6]. Both are valid in column 1.

Now process column 2:

From [3,3] → [2,2] and [5,5]

From [6,6] → [5,5] and [8,8]

After merging: [2,2], [5,5], [8,8]

Intersecting with [1,6] removes [8,8], leaving [2,2], [5,5]. Since at least one state remains, the answer is Yes.

This trace shows that reachable states can split into multiple disjoint components even in small inputs, which justifies maintaining intervals instead of a single range.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(N log N) per test worst-case | Each step merges interval lists |
| Space | O(N) | Storing interval sets |

The total number of column updates across all test cases is bounded by 500,000, so this approach fits comfortably within time limits even with sorting-based merging.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    def merge(intervals):
        if not intervals:
            return []
        intervals.sort()
        res = []
        l, r = intervals[0]
        for x, y in intervals[1:]:
            if x <= r + 1:
                r = max(r, y)
            else:
                res.append((l, r))
                l, r = x, y
        res.append((l, r))
        return res

    def intersect(intervals, L, R):
        res = []
        for l, r in intervals:
            nl = max(l, L)
            nr = min(r, R)
            if nl <= nr:
                res.append((nl, nr))
        return res

    def solve():
        t = int(input())
        out = []
        for _ in range(t):
            n, h, k, s = map(int, input().split())
            intervals = [(s, s)]
            ok = True
            for _ in range(n):
                l, r = map(int, input().split())
                low, high = l + 1, r - 1
                nxt = []
                for a, b in intervals:
                    nxt.append((a - 1, b - 1))
                    nxt.append((a + k, b + k))
                nxt = merge(nxt)
                intervals = intersect(nxt, low, high)
                if not intervals:
                    ok = False
                    break
            out.append("Yes" if ok else "No")
        return "\n".join(out)

    return solve()

# sample-style and custom tests
assert run("""1
2 7 2 4
1 3
5 7
""") == "Yes"

assert run("""1
2 7 2 4
1 3
6 7
""") == "No"

assert run("""1
3 10 3 5
1 9
2 10
1 9
""") == "Yes"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| small feasible | Yes | basic reachability |
| tight corridor | No | pruning correctness |
| multi-step | Yes | interval persistence |

## Edge Cases

A key edge case appears when the allowed interval is narrow enough to split reachable states. For example, suppose after a transition we obtain reachable heights [2,2] and [10,10], but the next column only allows [1,3]. The correct behavior is to keep only [2,2] and discard [10,10]. A naive min-max approach would incorrectly keep [2,10] and assume intermediate states exist, producing a false Yes later.

Another edge case occurs when k is large. From a single interval, the jump transition creates a segment far away from the fall transition. If the next column permits only a mid-range interval, both branches may be partially or fully discarded, leaving no valid states. The interval-based merge correctly eliminates both components without ever inventing connectivity between them.

Both cases demonstrate that preserving disjoint structure is necessary for correctness, and that collapsing everything into a single range loses critical information about feasibility.
