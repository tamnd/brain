---
title: "CF 102482H - Single Cut of Failure"
description: "We have a rectangle representing a door. Wires are straight segments whose endpoints lie on the boundary, and every wire connects two different sides. We need to place as few new straight segments as possible so that every existing wire is crossed by at least one of our segments."
date: "2026-08-05T19:01:45+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102482
codeforces_index: "H"
codeforces_contest_name: "2018 ACM-ICPC World Finals"
rating: 0
weight: 102482
solve_time_s: 121
verified: true
draft: false
---

[CF 102482H - Single Cut of Failure](https://codeforces.com/problemset/problem/102482/H)

**Rating:** -  
**Tags:** -  
**Solve time:** 2m 1s  
**Verified:** yes  

## Solution
## Problem Understanding

We have a rectangle representing a door. Wires are straight segments whose endpoints lie on the boundary, and every wire connects two different sides. We need to place as few new straight segments as possible so that every existing wire is crossed by at least one of our segments.

The answer is surprisingly small. Two cuts are always enough: the two diagonals of the rectangle intersect every possible boundary-to-boundary wire. The real challenge is deciding whether one cut is already sufficient. The official solution observation is that the geometry can be converted into a circular interval problem, and the existence of a single cut can be checked with a linear sweep after sorting the endpoints.

The input size is the main difficulty. There can be up to one million wires, so anything involving pairs of wires is impossible. A quadratic algorithm would perform around 10^12 comparisons in the worst case, far beyond the available time. We need a method that processes each wire only a constant number of times.

The coordinates are large, up to 10^8, but they are only used to determine the cyclic order of points on the boundary. We do not need geometric intersection calculations between arbitrary segments. The structure of the rectangle is what makes the problem manageable.

A common mistake is to search for a cut by testing slopes or by trying many possible segments. The answer is not determined by metric geometry. The important information is only the order of endpoints around the rectangle.

## Approaches

A direct approach would try every possible cut and check which wires it intersects. Since a valid cut can be moved continuously without changing which wires it crosses until it reaches a wire endpoint, one could restrict the candidates to gaps between consecutive endpoints. There are O(n) such gaps, and checking one candidate against all wires costs O(n), giving O(n²) operations. With n = 10^6, this is impossible.

The useful transformation is to walk around the rectangle boundary and unwrap it into a line. Every wire becomes an interval between its two endpoint positions on this circular order. A cut also corresponds to choosing an interval on this circle. A wire is crossed exactly when the chosen interval contains exactly one of its two endpoints.

The problem becomes finding whether there exists a circular interval that contains one endpoint from every wire. This can be solved with a two-pointer sweep while maintaining how many wires currently have zero, one, or two endpoints inside the active interval.

If such an interval exists, its two boundary points give the required single cut. If it does not exist, the two rectangle diagonals are optimal because two cuts are always sufficient.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n²) | O(n) | Too slow |
| Optimal | O(n log n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Convert every wire endpoint into a single coordinate on the perimeter of the rectangle. We start at the bottom-left corner, move along the bottom side, then the right side, the top side, and finally the left side. The exact starting point does not matter, but a consistent cyclic order is required.
2. Sort all endpoint positions. Duplicate the sorted list with an added perimeter length so that circular intervals can be processed as normal intervals.
3. Maintain a sliding window on this doubled array. The left and right ends of the window represent the two endpoints of a possible cut. For every wire, maintain how many of its two endpoints are currently inside the window.
4. Move the right pointer forward while the window can still be extended without making any wire have both endpoints inside. A wire with both endpoints inside cannot be crossed by the corresponding cut.
5. Whenever every wire has exactly one endpoint inside the current window, the two boundary positions of the window describe a valid single cut.
6. If the sweep finishes without finding such a window, output the two slightly shortened diagonals of the rectangle.

The invariant is that the sliding window always represents a candidate cut interval whose right endpoint has been extended as far as possible for the current left endpoint. Every possible valid interval appears during this sweep because the left pointer visits every possible gap between endpoints, and the right pointer only moves forward around the circle.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, w, h = map(int, input().split())

    events = []
    wires = []

    per = 2 * (w + h)

    def pos(x, y):
        if y == 0:
            return x
        if x == w:
            return w + y
        if y == h:
            return w + h + (w - x)
        return w + h + w + (h - y)

    for i in range(n):
        x1, y1, x2, y2 = map(int, input().split())
        a = pos(x1, y1)
        b = pos(x2, y2)
        wires.append((a, b))
        events.append((a, i))
        events.append((b, i))

    events.sort()

    m = len(events)
    coords = [x[0] for x in events]

    index_a = [0] * n
    index_b = [0] * n
    for i, (_, w_id) in enumerate(events):
        if index_a[w_id] == 0 and index_b[w_id] == 0:
            index_a[w_id] = i
        else:
            index_b[w_id] = i

    cnt = [0] * n
    one = 0
    two = 0

    def add(idx):
        nonlocal one, two
        w_id = events[idx % m][1]
        if cnt[w_id] == 0:
            cnt[w_id] = 1
            one += 1
        elif cnt[w_id] == 1:
            cnt[w_id] = 2
            one -= 1
            two += 1

    def remove(idx):
        nonlocal one, two
        w_id = events[idx % m][1]
        if cnt[w_id] == 1:
            cnt[w_id] = 0
            one -= 1
        else:
            cnt[w_id] = 1
            two -= 1
            one += 1

    def from_pos(p):
        p %= per
        if p < w:
            return 0.0, float(p)
        p -= w
        if p < h:
            return float(w), float(p)
        p -= h
        if p < w:
            return float(w - p), float(h)
        p -= w
        return 0.0, float(h - p)

    r = 0
    while r < m:
        add(r)
        r += 1

    for l in range(m):
        while r < l + m and two == 0 and one < n:
            add(r)
            r += 1

        if one == n and two == 0:
            a = coords[l]
            b = coords[r - 1] if r - 1 < m else coords[(r - 1) % m] + per
            if b - a < per:
                mid1 = a + 0.5
                mid2 = b - 0.5
                if mid2 > per:
                    mid2 -= per
                x1, y1 = from_pos(mid1)
                x2, y2 = from_pos(mid2)
                print(1)
                print(x1, y1, x2, y2)
                return

        remove(l)

    eps = 0.001
    print(2)
    print(eps, eps, w - eps, h - eps)
    print(w - eps, eps, eps, h - eps)

if __name__ == "__main__":
    solve()
```
