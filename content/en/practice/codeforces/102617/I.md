---
title: "CF 102617I - Ice Cream"
description: "There is a line of huts, each hut containing some number of people. The huts are equally spaced, and the input gives the population of every hut. Existing ice cream shops are also placed on the same line at given coordinates. We need to choose the coordinate of one new shop."
date: "2026-08-01T07:14:26+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102617
codeforces_index: "I"
codeforces_contest_name: "mBIT Rookie November 2019"
rating: 0
weight: 102617
solve_time_s: 61
verified: true
draft: false
---

[CF 102617I - Ice Cream](https://codeforces.com/problemset/problem/102617/I)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 1s  
**Verified:** yes  

## Solution
## Problem Understanding

There is a line of huts, each hut containing some number of people. The huts are equally spaced, and the input gives the population of every hut. Existing ice cream shops are also placed on the same line at given coordinates.

We need to choose the coordinate of one new shop. A person buys from the new shop only if the new shop is strictly closer to their hut than every existing shop. The goal is to find the maximum total population of huts that can be captured by choosing the best possible position for the new shop.

The number of huts and existing shops can both reach 200,000. That immediately rules out checking every possible position and comparing it against all huts, because there are infinitely many possible real coordinates for the new shop. Even checking every pair of huts and shops would be too slow. We need a solution close to linear or sorting based, around $O(n \log n)$.

The key difficulty is the word "strictly". If the new shop is exactly the same distance from a hut as an existing shop, that person does not count. A solution that treats the intervals as closed intervals will overestimate the answer.

For example:

```
Input
2 1
5 7
100

Output
7
```

The huts are at positions 0 and 100, and the existing shop is at 100. The second hut has distance 0 to an existing shop, so it can never be won. Only the first hut can be captured. A careless implementation that allows ties may incorrectly count both huts.

Another edge case is when several huts have the same best possible region.

```
Input
3 1
2 5 6
169

Output
7
```

The first hut and second hut can both be captured by placing the new shop near the left side. The third hut cannot. A solution that only checks locations next to existing shops can miss the best point, because the optimal location can be anywhere inside a continuous interval.

## Approaches

A direct approach would be to try every meaningful position for the new shop. Between two consecutive existing shops, the set of people who prefer the new shop does not change continuously except when crossing a point where some hut becomes tied. We could generate many candidate points, test every candidate against every hut, and keep the maximum.

This works conceptually because the answer must come from one of the regions created by distance comparisons. However, the number of candidates can be large, and checking each candidate against all huts leads to far more than the allowed operations. In the worst case this becomes quadratic or worse.

The useful observation is to reverse the point of view. Instead of asking which huts a chosen shop location can capture, ask where a chosen hut allows the new shop to be placed.

Suppose a hut is at coordinate $c_i$. Let $d_i$ be the distance from this hut to its closest existing shop. The new shop wins this hut exactly when:

$$|x-c_i| < d_i$$

which means:

$$c_i-d_i < x < c_i+d_i$$

So every hut contributes an open interval of positions where the new shop would capture that hut. The problem becomes finding the maximum total weight of overlapping open intervals.

This is a weighted sweep line problem. We create an event when an interval starts and another when it ends. The only subtlety is handling open intervals correctly. At the same coordinate, intervals ending there disappear before intervals starting there become active, because neither includes the boundary itself. After processing all events at a coordinate, the current sum represents the coverage immediately after that coordinate.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(n^2)$ or worse | $O(n)$ | Too slow |
| Optimal | $O((n+m)\log m)$ | $O(n+m)$ | Accepted |

## Algorithm Walkthrough

1. Sort the coordinates of all existing ice cream shops. For every hut, we need to know its nearest shop, and in a sorted list this can be found with binary search.
2. For every hut, find the distance to the closest existing shop. If the hut coordinate is $c$ and the distance is $d$, the new shop can capture this hut only inside the open interval $(c-d,c+d)$.
3. Ignore huts where $d=0$. Their interval has zero length because an existing shop already sits exactly at the hut position.
4. Add a start event at $c-d$ and an end event at $c+d$. The weight of the event is the number of people in that hut.
5. Sort all event coordinates. For every coordinate, remove intervals ending there first, then add intervals starting there. After all events at that coordinate are processed, the current weight is the number of people captured in the following open segment.
6. Track the maximum current weight seen during the sweep.

Why it works:

Each hut contributes exactly the set of all positions where a new shop would beat every existing shop for that hut. The total number of people captured by a chosen position is exactly the sum of weights of all intervals containing that position. The sweep line maintains this sum for every possible region between consecutive event coordinates. Since the value can only change at event coordinates, checking every such region finds the optimal location.

## Python Solution

```python
import sys
import bisect

input = sys.stdin.readline

def solve():
    n, m = map(int, input().split())
    people = list(map(int, input().split()))
    shops = list(map(int, input().split()))
    shops.sort()

    events = []

    for i in range(n):
        pos = i * 100
        idx = bisect.bisect_left(shops, pos)

        best = 10**18
        if idx < m:
            best = min(best, abs(shops[idx] - pos))
        if idx > 0:
            best = min(best, abs(shops[idx - 1] - pos))

        if best > 0:
            events.append((pos - best, 1, people[i]))
            events.append((pos + best, -1, people[i]))

    events.sort()

    ans = 0
    cur = 0
    i = 0
    while i < len(events):
        x = events[i]

        while i < len(events) and events[i][0] == x[0] and events[i][1] == -1:
            cur -= events[i][2]
            i += 1

        j = i
        while j < len(events) and events[j][0] == x[0]:
            j += 1

        while i < j:
            cur += events[i][2]
            i += 1

        ans = max(ans, cur)

    print(ans)

if __name__ == "__main__":
    solve()
```

The shop coordinates are sorted first because nearest-neighbor queries on a line can then be answered with binary search. The hut coordinates do not need to be stored separately because hut $i$ is always at coordinate $100i$ when using zero-based indexing.

The interval generation is the core transformation. The distance to the closest existing shop determines exactly how far the new shop can move away while still being preferred. Since the interval is open, a zero distance creates no valid positions and is skipped.

The sweep ordering is the part most likely to cause an off-by-one mistake. End events must be applied before start events at the same coordinate. If starts were processed first, two touching intervals such as $(-1,0)$ and $(0,1)$ would incorrectly appear to overlap at coordinate zero.

Python integers are arbitrary precision, so the large possible population sums do not require any special handling.

## Worked Examples

For the first sample:

```
3 1
2 5 6
169
```

The huts are at coordinates 0, 100, and 200. The closest shop distances are 169, 69, and 31.

| Event coordinate | Removed weight | Added weight | Current people |
| --- | --- | --- | --- |
| -169 | 0 | 2 | 2 |
| 31 | 5 | 0 | 2 |
| 31 | 0 | 5 | 7 |
| 131 | 5 | 0 | 2 |
| 169 | 2 | 0 | 0 |

The maximum value is 7, meaning the new shop can capture the first two huts.

For the second sample:

```
4 2
1 2 7 8
35 157
```

The nearest shops determine the following intervals.

| Hut | Coordinate | Distance to closest shop | Interval | Weight |
| --- | --- | --- | --- | --- |
| 1 | 0 | 35 | (-35,35) | 1 |
| 2 | 100 | 57 | (43,157) | 2 |
| 3 | 200 | 43 | (157,243) | 7 |
| 4 | 300 | 143 | (157,443) | 8 |

The maximum overlap happens just after coordinate 157, where the last two huts are both available.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O((n+m)\log m)$ | Sorting shops and sorting interval events dominate the runtime |
| Space | $O(n+m)$ | Stores the generated events and sorted shop positions |

With 200,000 huts and shops, sorting about 400,000 events is easily within typical contest limits.

## Test Cases

```python
import sys, io, bisect

def run(inp: str) -> str:
    old = sys.stdin
    sys.stdin = io.StringIO(inp)

    def solve():
        import sys, bisect
        input = sys.stdin.readline
        n, m = map(int, input().split())
        people = list(map(int, input().split()))
        shops = sorted(map(int, input().split()))

        events = []
        for i, p in enumerate(people):
            pos = i * 100
            k = bisect.bisect_left(shops, pos)
            d = 10**18
            if k < m:
                d = min(d, abs(shops[k] - pos))
            if k:
                d = min(d, abs(shops[k-1] - pos))
            if d:
                events.append((pos-d, 1, p))
                events.append((pos+d, -1, p))

        events.sort()
        cur = ans = 0
        i = 0
        while i < len(events):
            x = events[i][0]
            while i < len(events) and events[i][0] == x and events[i][1] == -1:
                cur -= events[i][2]
                i += 1
            while i < len(events) and events[i][0] == x:
                cur += events[i][2]
                i += 1
            ans = max(ans, cur)

        return str(ans) + "\n"

    out = solve()
    sys.stdin = old
    return out

assert run("""3 1
2 5 6
169
""") == "7\n", "sample 1"

assert run("""4 2
1 2 7 8
35 157
""") == "15\n", "sample 2"

assert run("""2 1
5 7
100
""") == "5\n", "existing shop on hut"

assert run("""3 2
1 1 1
0 200
""") == "1\n", "two boundary shops"

assert run("""5 1
10 10 10 10 10
1000
""") == "50\n", "all huts captured"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Existing shop on hut | 5 | Handles zero-length intervals |
| Two boundary shops | 1 | Checks strict comparison and touching intervals |
| All equal populations | 50 | Checks large sums and overlapping intervals |

## Edge Cases

When an existing shop is exactly at a hut, the distance to the nearest shop is zero. The interval becomes empty, and the algorithm ignores it. For example:

```
2 1
5 7
100
```

The second hut cannot be captured because its distance to the existing shop is already zero. The sweep only receives the interval from the first hut and returns 5.

When two intervals touch at a boundary, the algorithm must not count both simultaneously. For example, one hut might allow positions in $(-10,0)$ while another allows positions in $(0,10)$. The coordinate zero itself satisfies neither interval, so the answer cannot include both weights. Processing end events before start events preserves this rule.

When many huts can be captured by the same region, the sweep accumulates their weights naturally. In the first sample, the intervals of the first two huts overlap, so their populations combine into the final answer of 7.
