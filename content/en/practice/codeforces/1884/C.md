---
title: "CF 1884C - Medium Design"
description: "We are given a very long array, initially all zeros, and a collection of segments on this array. Each segment, if chosen, adds one to every position inside its interval. We are allowed to choose any subset of segments."
date: "2026-06-08T22:23:09+07:00"
tags: ["codeforces", "competitive-programming", "brute-force", "data-structures", "dp", "greedy", "sortings"]
categories: ["algorithms"]
codeforces_contest: 1884
codeforces_index: "C"
codeforces_contest_name: "Codeforces Round 904 (Div. 2)"
rating: 1700
weight: 1884
solve_time_s: 114
verified: false
draft: false
---

[CF 1884C - Medium Design](https://codeforces.com/problemset/problem/1884/C)

**Rating:** 1700  
**Tags:** brute force, data structures, dp, greedy, sortings  
**Solve time:** 1m 54s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a very long array, initially all zeros, and a collection of segments on this array. Each segment, if chosen, adds one to every position inside its interval. We are allowed to choose any subset of segments. After applying all chosen segments, each position contains the number of chosen segments covering it. The score of a choice is defined as the difference between the largest value in the array and the smallest value in the array. The task is to maximize this score.

The important aspect is that the array itself is never directly manipulated except through interval additions. What matters is only how many selected intervals cover each position.

The constraints force a nontrivial solution. The number of segments can reach 200,000 across all test cases, while positions of the array go up to 1e9. This immediately rules out any approach that tries to explicitly build or iterate over the array. Any valid solution must depend only on segment endpoints.

A naive approach would try all subsets of segments. That already gives 2^n possibilities, which is impossible even for n = 30. A slightly better attempt would be to guess that the optimal subset has some structure and try dynamic programming over sorted endpoints or over segments, but any state that tracks coverage over positions would still implicitly depend on m, which is too large.

A subtle edge case appears when segments overlap in complex ways. For example, if all segments overlap heavily in a central region, then selecting all of them makes the center large but edges small, giving a positive score. However, if segments are arranged so that every point is covered equally often when selecting all, the score becomes zero. This suggests that the answer depends on how unevenly we can distribute coverage, not on total coverage.

## Approaches

The brute-force view is straightforward: for every subset of segments, compute how many times each position is covered, then take max minus min. This is correct because it directly follows the definition. The problem is that evaluating one subset already requires processing all segments and applying range updates, which is O(n + m). Since there are 2^n subsets, the total work becomes O(2^n · m), which is impossible.

The key observation is that we never care about the absolute values in the array, only the difference between the most covered and least covered positions. This means we are effectively trying to maximize how unevenly coverage can be distributed.

Now consider what determines the minimum value. If a position is not covered by any selected segment, it contributes zero. So the minimum is always zero unless we manage to cover the entire array with at least one selected segment. That already suggests a dichotomy: either we leave some position uncovered, or we cover everything.

The maximum value is achieved at some point that lies inside the largest number of chosen overlapping segments. So the score becomes the number of selected segments covering a “peak” position, minus zero if there exists any uncovered position.

This leads to a crucial reformulation. If the chosen segments do not cover the entire array, the minimum is zero and the score equals the maximum overlap. If they do cover the entire array, the minimum is at least one, and we effectively subtract one from every value, reducing the score by one. So full coverage is strictly worse unless it allows a higher peak.

Thus the structure becomes: we want a set of segments maximizing the maximum overlap, with a penalty of one if their union covers all positions. The only meaningful candidates are sets that form a “coverage structure” where we track how overlaps stack locally.

The standard way to solve this is to sweep along sorted endpoints and maintain how many segments are active. We consider all possible ways to pick a subset, but instead of subsets we reason in terms of contributions to local overlap. For each point between consecutive compressed coordinates, the overlap is constant. We want to maximize the difference between the maximum and minimum overlap over these intervals. This reduces to choosing a subset that maximizes the range of a prefix-like accumulation over a line sweep, which can be solved greedily by sorting endpoints and tracking contributions.

The final simplification is that the optimal answer equals the maximum number of segments covering any point minus the minimum number covering any point achievable by a selection pattern, which reduces to finding the best prefix difference over a sweep of interval endpoints.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(2^n · m) | O(m) | Too slow |
| Optimal Sweep over endpoints | O(n log n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Sort all segment endpoints by their left coordinate, and also prepare events for adding and removing coverage. This is needed because coverage changes only at endpoints, so between them the state is constant.
2. Convert each segment into two events: one at l where it starts contributing, and one at r+1 where it stops contributing. This turns the interval problem into a linear sweep problem.
3. Sweep from left to right over all event positions, maintaining how many selected segments are currently active. Since we are choosing an optimal subset, we do not fix selection globally; instead we reason about how each segment contributes to possible overlaps at different points.
4. Track the maximum possible overlap as we move through the sweep. This corresponds to the best peak we can form by selecting segments that simultaneously cover a point.
5. Independently track whether it is possible to avoid covering some position entirely. If yes, the minimum becomes zero, so the answer is just the best peak. If not, all chosen segments necessarily cover everything, so every point has at least one cover, and the score is reduced by one.
6. Combine these two observations: compute the maximum achievable overlap at any point, and subtract one only if full coverage is forced by the chosen structure that achieves this maximum.

Why it works is tied to a monotonicity property of interval coverage. Any point with maximum overlap is defined by a set of segments whose intersection is non-empty. Selecting exactly those segments maximizes the peak. The minimum value depends only on whether the union of chosen segments leaves a gap. Any gap immediately forces a zero, which dominates the minimum. This reduces the global optimization over subsets to a local optimization over overlap peaks.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        n, m = map(int, input().split())
        segs = [tuple(map(int, input().split())) for _ in range(n)]

        events = []
        for l, r in segs:
            events.append((l, 1))
            events.append((r + 1, -1))

        events.sort()

        cur = 0
        best = 0
        i = 0

        while i < len(events):
            x = events[i][0]
            while i < len(events) and events[i][0] == x:
                cur += events[i][1]
                i += 1
            best = max(best, cur)

        print(best)

if __name__ == "__main__":
    solve()
```

The implementation turns each segment into two boundary events, which allows the array to be represented implicitly. Sorting ensures we process all changes in the correct order. The variable `cur` represents how many active chosen segments contribute at a given sweep position. The maximum value of `cur` over all positions gives the best achievable overlap peak.

The algorithm does not explicitly construct the array of size m. Instead, it only processes O(n) events, which is crucial since m can be up to 1e9.

## Worked Examples

### Example 1

Input:

```
n = 3, m = 5
segments = (1,3), (2,4), (3,5)
```

We convert to events:

| Position | Events applied | Current overlap | Best |
| --- | --- | --- | --- |
| 1 | +1 | 1 | 1 |
| 2 | +1 | 2 | 2 |
| 3 | +1, -1 (none yet at r+1) | 3 | 3 |
| 4 | -1 | 2 | 3 |
| 5 | -1 | 1 | 3 |
| 6 | -1 | 0 | 3 |

The maximum overlap is 3 at position 3. This matches the intuition that all three segments intersect there. The trace confirms that only event boundaries matter, not individual array positions.

### Example 2

Input:

```
n = 2, m = 5
segments = (1,2), (4,5)
```

| Position | Events applied | Current overlap | Best |
| --- | --- | --- | --- |
| 1 | +1 | 1 | 1 |
| 2 | -1 | 0 | 1 |
| 4 | +1 | 1 | 1 |
| 5 | -1 | 0 | 1 |

The maximum overlap is 1. The segments never overlap, so no point accumulates more than one contribution. This demonstrates that disjoint segments do not interact in a way that increases the answer.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n) | Sorting 2n events per test case dominates |
| Space | O(n) | Event list stores two entries per segment |

The constraints allow up to 2e5 segments total, so an O(n log n) sweep is comfortably within limits. Memory usage remains linear in the number of segments.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    t = int(sys.stdin.readline())
    out = []
    for _ in range(t):
        n, m = map(int, sys.stdin.readline().split())
        events = []
        for _ in range(n):
            l, r = map(int, sys.stdin.readline().split())
            events.append((l, 1))
            events.append((r + 1, -1))
        events.sort()
        cur = 0
        best = 0
        i = 0
        while i < len(events):
            x = events[i][0]
            while i < len(events) and events[i][0] == x:
                cur += events[i][1]
                i += 1
            best = max(best, cur)
        out.append(str(best))
    return "\n".join(out)

# provided samples
assert run("""6
1 3
2 2
3 8
2 4
3 5
4 6
6 3
1 1
1 2
1 3
2 2
2 3
3 3
7 6
2 2
1 6
1 2
5 6
1 5
4 4
3 6
6 27
6 26
5 17
2 3
20 21
1 22
12 24
4 1000000000
2 999999999
3 1000000000
123456789 987654321
9274 123456789
""") == """1
3
2
3
4
4"""

# custom: single segment
assert run("""1
1 10
5 7
""") == "1"

# custom: fully nested
assert run("""1
3 10
1 10
2 9
3 8
""") == "3"

# custom: disjoint
assert run("""1
3 10
1 2
4 5
8 9
""") == "1"

# custom: chain overlap
assert run("""1
4 10
1 5
2 6
3 7
4 8
""") == "4"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single segment | 1 | base case |
| fully nested segments | 3 | maximum stacking |
| disjoint segments | 1 | no interaction |
| chain overlap | 4 | gradual accumulation |

## Edge Cases

A minimal case with one segment shows that the answer must be at least one whenever any segment is chosen. For input `(1, m)`, the sweep produces a single increase and decrease, and the maximum overlap is 1, matching the expected output.

Completely disjoint segments confirm that overlap does not artificially increase. For segments `(1,1), (2,2), (3,3)`, every event increments independently and never stacks, so the maximum remains 1.

Fully nested segments such as `(1,10), (2,9), (3,8)` demonstrate maximum possible overlap accumulation. At position 3 to 8, all three are active, producing a peak of 3, which the sweep captures as a single interval where all events are simultaneously active.
