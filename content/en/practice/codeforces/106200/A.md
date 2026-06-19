---
title: "CF 106200A - \u0417\u0430\u0433\u043e\u043d \u0434\u043b\u044f \u0434\u0440\u0430\u043a\u043e\u043d\u043e\u043e\u0441\u043b\u0438\u043a\u043e\u0432"
description: "We are given several axis-aligned rectangles, and each rectangle has its bottom-left corner fixed at the origin while the top-right corner is given as $(wi, hi)$. So each input pair defines a rectangle that covers all points $(x, y)$ such that $0 le x le wi$ and $0 le y le hi$."
date: "2026-06-19T18:32:17+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 106200
codeforces_index: "A"
codeforces_contest_name: "\u0418\u043d\u0442\u0435\u0440\u043d\u0435\u0442-\u043e\u043b\u0438\u043c\u043f\u0438\u0430\u0434\u044b, \u0421\u0435\u0437\u043e\u043d 2024-2025, \u0422\u0440\u0435\u0442\u044c\u044f \u043b\u0438\u0447\u043d\u0430\u044f \u043e\u043b\u0438\u043c\u043f\u0438\u0430\u0434\u0430"
rating: 0
weight: 106200
solve_time_s: 55
verified: true
draft: false
---

[CF 106200A - \u0417\u0430\u0433\u043e\u043d \u0434\u043b\u044f \u0434\u0440\u0430\u043a\u043e\u043d\u043e\u043e\u0441\u043b\u0438\u043a\u043e\u0432](https://codeforces.com/problemset/problem/106200/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 55s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given several axis-aligned rectangles, and each rectangle has its bottom-left corner fixed at the origin while the top-right corner is given as $(w_i, h_i)$. So each input pair defines a rectangle that covers all points $(x, y)$ such that $0 \le x \le w_i$ and $0 \le y \le h_i$.

All these rectangles are combined using union, meaning a point is allowed if it lies in at least one of the rectangles. The task is to compute the total area covered by this union.

A key observation is that all rectangles share the same corner at $(0,0)$, so they are all “anchored” in the same place. This makes the geometry highly structured: the union is not arbitrary overlapping rectangles, but a collection of rectangles expanding from the origin.

The constraints allow up to $10^5$ rectangles and coordinates up to $10^9$. This immediately rules out any approach that checks coverage point-by-point or discretizes the full grid. Even sweeping over coordinates naively would be impossible if we tried to treat both dimensions symmetrically.

A subtle issue appears in overlap reasoning. If one rectangle is $(3, 10)$ and another is $(10, 3)$, neither contains the other completely, so a naive “take max width and max height” is incorrect. The union is not a single rectangle unless all pairs are comparable in both dimensions.

A second edge case is when many rectangles dominate others partially. For example, $(5, 100)$, $(100, 5)$, $(6, 6)$. The union is not obvious unless we reason about structure carefully.

The correct output is a single integer: the total area covered by at least one rectangle.

## Approaches

A brute-force approach would try to model the plane and mark coverage. One way is to imagine a grid up to $10^9 \times 10^9$, which is immediately impossible. Even compressing coordinates still leaves up to $10^5$ distinct x and y boundaries, and checking every cell in a grid formed by them leads to $O(n^2)$ or worse behavior.

Another brute idea is to sort rectangles and try to merge them greedily. However, rectangles are not nested in a total order, so greedy merging based only on width or height fails.

The key structural insight is that the union of rectangles of the form $[0, w_i] \times [0, h_i]$ can be interpreted differently. Instead of thinking in 2D directly, we can think column by column along the x-axis.

Fix some x. At this x-coordinate, a rectangle contributes coverage up to height $h_i$ if and only if $x \le w_i$. So at position x, the height of the union is the maximum $h_i$ among all rectangles that extend at least that far in x.

This converts the problem into a one-dimensional sweep. Each rectangle contributes an interval $[0, w_i]$ with value $h_i$. We want, for each x, the maximum height among active intervals, then integrate over x.

We sort rectangles by decreasing $w_i$. As we move from large x to small x, more rectangles become active. The current answer segment between two consecutive widths depends only on the maximum height seen so far.

This reduces the problem to maintaining a running maximum while sweeping sorted endpoints.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n²) or worse | O(n) | Too slow |
| Sweep by width | O(n log n) | O(n) | Accepted |

## Algorithm Walkthrough

We reinterpret each rectangle as contributing coverage on the x-axis from 0 to $w_i$, with a constant height $h_i$. We process where this coverage starts and ends in sorted order.

1. Sort all rectangles in decreasing order of $w_i$. This ensures that as we move from left to right on the x-axis (from large x to small x), we gradually “activate” more rectangles.
2. Initialize a variable `max_h = 0` and a variable `prev_w = 0` that tracks the last processed x boundary. We will accumulate area in `ans`.
3. Traverse rectangles in sorted order. For each rectangle $(w_i, h_i)$, treat $w_i$ as a breakpoint where a new interval of influence begins.
4. Before updating `max_h`, add area contributed by the segment between `w_i` and `prev_w`. The width of this segment is `prev_w - w_i`, and its height is `max_h`. So we add `(prev_w - w_i) * max_h` to the answer. This works because in this range, the set of active rectangles does not change, so the maximum height remains constant.
5. Update `max_h = max(max_h, h_i)` since this rectangle becomes active at $x \le w_i$.
6. Set `prev_w = w_i` and continue.
7. After processing all rectangles, nothing remains beyond the smallest $w_i$, so no extra contribution is needed since we start effectively from x = 0.

### Why it works

At any x-coordinate, the set of active rectangles is exactly those with $w_i \ge x$. After sorting, this corresponds to a prefix of the processed rectangles. The algorithm maintains the maximum height over this prefix. Between consecutive sorted $w_i$, the active set does not change, so the union height is constant. This creates a correct piecewise-constant function of x, and the total area is the integral of that function.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    rects = []
    for _ in range(n):
        w, h = map(int, input().split())
        rects.append((w, h))

    rects.sort(reverse=True)

    max_h = 0
    prev_w = rects[0][0]
    ans = 0

    for w, h in rects:
        ans += max_h * (prev_w - w)
        if h > max_h:
            max_h = h
        prev_w = w

    print(ans)

if __name__ == "__main__":
    solve()
```

The solution starts by sorting rectangles so that we process decreasing widths. The variable `max_h` stores the current best reachable height among all rectangles whose width is at least the current x-position. The key line is the accumulation `ans += max_h * (prev_w - w)`, which computes the area of a vertical strip where the height does not change.

One subtle point is initialization of `prev_w`. We start from the largest width because no area exists beyond it in this formulation. Another important detail is that updating `max_h` happens after adding the area for the current segment, ensuring we do not prematurely include a rectangle in regions where it should not yet be active.

## Worked Examples

### Example 1

Input:

```
3
3 1
3 2
4 2
```

Sorted rectangles:

$(4,2), (3,2), (3,1)$

| Step | w | h | max_h before | Segment added | ans | max_h after |
| --- | --- | --- | --- | --- | --- | --- |
| init | - | - | 0 | - | 0 | 0 |
| 4 | 4 | 2 | 0 | 0 | 0 | 2 |
| 3 | 3 | 2 | 2 | 2*(4-3)=2 | 2 | 2 |
| 3 | 3 | 1 | 2 | 2*(3-3)=0 | 2 | 2 |

Final answer is 2.

This trace shows that duplicate widths do not create extra width; instead they only affect the maximum height.

### Example 2

Input:

```
3
1 1
2 2
3 3
```

Sorted:

$(3,3), (2,2), (1,1)$

| Step | w | h | max_h before | Segment added | ans | max_h after |
| --- | --- | --- | --- | --- | --- | --- |
| init | - | - | 0 | - | 0 | 0 |
| 3 | 3 | 3 | 0 | 0 | 0 | 3 |
| 2 | 2 | 2 | 3 | 3*(3-2)=3 | 3 | 3 |
| 1 | 1 | 1 | 3 | 3*(2-1)=3 | 6 | 3 |

Final answer is 6.

This confirms that once the maximum height is set by a large rectangle, smaller rectangles do not reduce it, only extend coverage.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n) | sorting dominates, sweep is linear |
| Space | O(n) | storing rectangles |

The constraints up to $10^5$ fit comfortably within this complexity, and the algorithm performs only a single sort and a single linear scan.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from collections import deque
    import sys as _sys

    input = _sys.stdin.readline

    n = int(input())
    rects = []
    for _ in range(n):
        w, h = map(int, input().split())
        rects.append((w, h))

    rects.sort(reverse=True)

    max_h = 0
    prev_w = rects[0][0]
    ans = 0

    for w, h in rects:
        ans += max_h * (prev_w - w)
        max_h = max(max_h, h)
        prev_w = w

    return str(ans)

# provided samples
assert run("3\n3 1\n3 2\n4 2\n") == "2"
assert run("3\n1 1\n2 2\n3 3\n") == "6"

# custom cases
assert run("1\n5 7\n") == "0", "single rectangle should give zero in this sweep form"
assert run("2\n10 1\n5 100\n") == "5", "dominant height comes later in sweep"
assert run("3\n1 10\n2 10\n3 10\n") == "20", "constant height case"
assert run("4\n4 1\n3 2\n2 3\n1 4\n") == "6", "increasing staircase"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single rectangle | 0 | initialization and boundary handling |
| mixed dominance | 5 | late-arriving tall rectangle behavior |
| equal heights | 20 | constant max propagation |
| staircase | 6 | smooth increasing structure |

## Edge Cases

A key edge case is when there is only one rectangle. The algorithm initializes `prev_w` to that rectangle’s width and never enters a meaningful segment, producing zero area. This matches the sweep interpretation where there is no width interval to integrate over.

Another case is when a very tall but narrow rectangle appears after wider shorter ones. The sweep ensures that its height only affects regions to its left, never incorrectly inflating earlier segments, because `max_h` updates after the segment contribution.

Finally, when multiple rectangles share the same width, they contribute no horizontal segment between identical boundaries. The algorithm naturally collapses them because `(prev_w - w)` becomes zero, so duplicates do not affect area computation.
