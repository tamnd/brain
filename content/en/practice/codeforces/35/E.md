---
title: "CF 35E - Parade"
description: "Each skyscraper is an axis-aligned rectangle sitting on the ground. A building with parameters (h, l, r) occupies every point with l ≤ x ≤ r and 0 ≤ y ≤ h."
date: "2026-05-28T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "data-structures", "sortings"]
categories: ["algorithms"]
codeforces_contest: 35
codeforces_index: "E"
codeforces_contest_name: "Codeforces Beta Round 35 (Div. 2)"
rating: 2100
weight: 35
solve_time_s: 101
verified: true
draft: false
---
[CF 35E - Parade](https://codeforces.com/problemset/problem/35/E)

**Rating:** 2100  
**Tags:** data structures, sortings  
**Solve time:** 1m 41s  
**Verified:** yes  

## Solution
## Problem Understanding

Each skyscraper is an axis-aligned rectangle sitting on the ground. A building with parameters `(h, l, r)` occupies every point with `l ≤ x ≤ r` and `0 ≤ y ≤ h`.

We must construct a polyline that starts on the ground, moves only horizontally or vertically, and encloses all buildings together with the ground. Among all such polylines, we first minimize enclosed area. If several polylines achieve the same minimum area, we choose the one with the smallest total length.

Geometrically, this is exactly the upper skyline of the union of rectangles. The polyline climbs whenever a taller building begins, stays flat while the visible height is constant, and descends when the current tallest building disappears.

The constraints immediately rule out any quadratic approach. With `n ≤ 100000`, even `O(n^2)` with simple operations becomes around `10^10` work in the worst case, which is far beyond the time limit. We need something close to `O(n log n)`.

The buildings may overlap in arbitrary ways. Several subtle cases appear if we try to construct the skyline carelessly.

One dangerous case is when multiple events happen at the same x-coordinate.

Example:

```
3
5 0 2
3 2 4
7 2 5
```

At `x = 2`, one building ends and two others begin. The skyline must jump directly from height `5` to height `7`. A naive sweep that processes removals before insertions may incorrectly create an intermediate drop to `0` or `3`.

Another tricky case is nested buildings.

Example:

```
3
10 0 10
3 2 4
5 6 8
```

The smaller buildings never affect the outline because they are fully hidden under the taller one. A naive implementation that blindly emits segments for every building would produce redundant vertices and fail the minimum-length requirement.

Disjoint buildings are also important.

Example:

```
2
4 0 2
3 5 7
```

The correct skyline must return to ground level between the buildings:

```
0 0
0 4
2 4
2 0
5 0
5 3
7 3
7 0
```

If we accidentally merge separate components, we enclose unnecessary area and violate the primary optimization criterion.

Finally, equal heights require care.

Example:

```
2
5 0 2
5 2 4
```

The correct answer is one continuous horizontal segment at height `5`, not two separate plateaus with an unnecessary vertical edge at `x = 2`.

## Approaches

The most direct idea is to discretize the x-axis. We could collect all distinct coordinates, split the plane into elementary intervals, and compute the maximum building height covering each interval. Once the height profile is known, generating the polyline is easy.

This works conceptually because the optimal polyline is uniquely determined by the maximum visible height at every x-coordinate. Any lower curve would intersect a building, and any higher curve would increase enclosed area.

The problem with brute force is coverage testing. Suppose we compress coordinates into `m` intervals. For every interval, we check all buildings to find the maximum height. In the worst case, `m` is `2n`, so this becomes `O(nm) = O(n^2)`.

With `100000` buildings, that means roughly `10^10` comparisons.

The key observation is that the skyline only changes at building boundaries. Between two consecutive event coordinates, the set of active buildings never changes, so the visible height is constant there.

This naturally suggests a sweep line. We process all building start and end events from left to right while maintaining the tallest active building in a data structure.

When a building starts, we insert its height.

When a building ends, we remove its height.

After processing events at position `x`, the maximum active height determines the skyline immediately to the right of `x`.

A max-heap gives fast access to the current tallest building. Since Python heaps are min-heaps, we store negative heights. Removing arbitrary heights from a heap is inconvenient, so we use lazy deletion with a counter map.

The sweep processes `2n` events, and each insertion or removal costs `O(log n)`, giving total complexity `O(n log n)`.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n²) | O(n) | Too slow |
| Optimal | O(n log n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Convert every building into two events.

A building `(h, l, r)` becomes:

- start event `(l, type=0, h)`
- end event `(r, type=1, h)`

We process start events before end events at the same coordinate. This avoids temporary drops in height when one building ends exactly where another begins.
2. Sort all events by x-coordinate and event type.

After sorting, sweeping from left to right guarantees that we always know which buildings are currently active.
3. Maintain a max-heap of active heights.

Since Python only provides a min-heap, store negative heights.

Initially the heap contains `0`, representing ground level.
4. Maintain a frequency map for lazy deletion.

When a building ends, we decrement its frequency instead of removing it directly from the heap.

Before reading the current maximum, repeatedly pop heap elements whose frequency became zero.
5. Process all events with the same x-coordinate together.

This is critical. The skyline cannot change multiple times at the same x-coordinate.

For every event at position `x`:

- add heights for start events
- mark heights removed for end events
6. After processing all events at position `x`, clean the heap.

Remove stale heap entries until the top corresponds to an active height.
7. Compare the new maximum height with the previous skyline height.

If the height changed from `prev_h` to `cur_h`, the skyline must turn at `x`.

Two vertices are added:

- `(x, prev_h)`
- `(x, cur_h)`

This creates the required vertical segment.
8. Remove redundant consecutive duplicates.

Some transitions can create repeated points or unnecessary collinear vertices. Compressing them guarantees the minimum-length polyline.
9. Add the initial and final ground points automatically through the sweep transitions.

### Why it works

At every x-coordinate, the heap contains exactly the heights of buildings covering positions immediately to the right of x. The maximum among them is the minimum possible valid height of the envelope there, because any smaller value would intersect a building.

The skyline only changes when the maximum active height changes. Emitting vertices exactly at those transition points produces the unique minimum-area envelope. Any additional vertical or horizontal segment would increase total length without changing area, so the cleaned polyline also has minimum length among all minimum-area solutions.

## Python Solution

```python
import sys
import heapq
from collections import defaultdict

input = sys.stdin.readline

def solve():
    n = int(input())

    events = []

    for _ in range(n):
        h, l, r = map(int, input().split())

        # start before end at same x
        events.append((l, 0, h))
        events.append((r, 1, h))

    events.sort()

    heap = [0]
    cnt = defaultdict(int)
    cnt[0] = 1

    ans = []

    prev_h = 0

    i = 0
    m = len(events)

    while i < m:
        x = events[i][0]

        while i < m and events[i][0] == x:
            _, typ, h = events[i]

            if typ == 0:
                cnt[h] += 1
                heapq.heappush(heap, -h)
            else:
                cnt[h] -= 1

            i += 1

        while heap and cnt[-heap[0]] == 0:
            heapq.heappop(heap)

        cur_h = -heap[0]

        if cur_h != prev_h:
            ans.append((x, prev_h))
            ans.append((x, cur_h))
            prev_h = cur_h

    # remove redundant consecutive duplicates / collinear points
    res = []

    for p in ans:
        if res and res[-1] == p:
            continue

        while len(res) >= 2:
            x1, y1 = res[-2]
            x2, y2 = res[-1]
            x3, y3 = p

            if (x1 == x2 == x3) or (y1 == y2 == y3):
                res.pop()
            else:
                break

        res.append(p)

    print(len(res))
    for x, y in res:
        print(x, y)

solve()
```

The sweep line is the core of the implementation. Every building contributes one insertion event and one removal event. Sorting events gives the left-to-right traversal order.

The heap stores all candidate heights that may currently define the skyline. Since removing arbitrary elements from a heap is expensive, the code uses lazy deletion. Heights remain in the heap until they reach the top. At that moment we check whether the frequency map says they are still active.

Processing all events at the same x-coordinate together avoids incorrect intermediate transitions. Suppose a height disappears and another taller height appears at the same coordinate. If we emitted changes one event at a time, we could accidentally create zero-width zigzags.

The cleanup loop at the end removes redundant collinear vertices. Without it, equal-height plateaus or repeated vertical turns could produce non-minimal polylines.

All coordinates and heights fit safely in Python integers, so no overflow issues appear.

## Worked Examples

### Sample 1

Input:

```
2
3 0 2
4 1 3
```

Sorted events:

| x | type | h |
| --- | --- | --- |
| 0 | start | 3 |
| 1 | start | 4 |
| 2 | end | 3 |
| 3 | end | 4 |

Sweep trace:

| x | Active Heights | Current Max | Previous Max | Added Vertices |
| --- | --- | --- | --- | --- |
| 0 | {3} | 3 | 0 | (0,0), (0,3) |
| 1 | {3,4} | 4 | 3 | (1,3), (1,4) |
| 2 | {4} | 4 | 4 | none |
| 3 | {} | 0 | 4 | (3,4), (3,0) |

Final output:

```
0 0
0 3
1 3
1 4
3 4
3 0
```

This trace shows how overlapping buildings only affect the skyline when a taller building appears.

### Example 2

Input:

```
3
5 0 10
3 2 4
7 6 8
```

Sorted events:

| x | type | h |
| --- | --- | --- |
| 0 | start | 5 |
| 2 | start | 3 |
| 4 | end | 3 |
| 6 | start | 7 |
| 8 | end | 7 |
| 10 | end | 5 |

Sweep trace:

| x | Active Heights | Current Max | Previous Max | Added Vertices |
| --- | --- | --- | --- | --- |
| 0 | {5} | 5 | 0 | (0,0), (0,5) |
| 2 | {5,3} | 5 | 5 | none |
| 4 | {5} | 5 | 5 | none |
| 6 | {5,7} | 7 | 5 | (6,5), (6,7) |
| 8 | {5} | 5 | 7 | (8,7), (8,5) |
| 10 | {} | 0 | 5 | (10,5), (10,0) |

The smaller building from `2` to `4` never changes the skyline because it stays hidden beneath height `5`.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n) | Sorting events and heap operations |
| Space | O(n) | Events, heap, and frequency map |

The algorithm comfortably fits the limits. With `2n` events and logarithmic heap operations, even the worst case with `100000` buildings runs efficiently within 2 seconds.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io
from collections import defaultdict
import heapq

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    input = sys.stdin.readline

    out = io.StringIO()
    sys.stdout = out

    n = int(input())

    events = []

    for _ in range(n):
        h, l, r = map(int, input().split())
        events.append((l, 0, h))
        events.append((r, 1, h))

    events.sort()

    heap = [0]
    cnt = defaultdict(int)
    cnt[0] = 1

    ans = []

    prev_h = 0

    i = 0

    while i < len(events):
        x = events[i][0]

        while i < len(events) and events[i][0] == x:
            _, typ, h = events[i]

            if typ == 0:
                cnt[h] += 1
                heapq.heappush(heap, -h)
            else:
                cnt[h] -= 1

            i += 1

        while cnt[-heap[0]] == 0:
            heapq.heappop(heap)

        cur_h = -heap[0]

        if cur_h != prev_h:
            ans.append((x, prev_h))
            ans.append((x, cur_h))
            prev_h = cur_h

    res = []

    for p in ans:
        if res and res[-1] == p:
            continue

        while len(res) >= 2:
            x1, y1 = res[-2]
            x2, y2 = res[-1]
            x3, y3 = p

            if (x1 == x2 == x3) or (y1 == y2 == y3):
                res.pop()
            else:
                break

        res.append(p)

    print(len(res))
    for x, y in res:
        print(x, y)

    sys.stdout = sys.__stdout__

    return out.getvalue()

# provided sample
assert run(
"""2
3 0 2
4 1 3
"""
) == (
"""6
0 0
0 3
1 3
1 4
3 4
3 0
"""
), "sample 1"

# single building
assert run(
"""1
5 2 7
"""
) == (
"""4
2 0
2 5
7 5
7 0
"""
), "single rectangle"

# equal heights touching
assert run(
"""2
5 0 2
5 2 4
"""
) == (
"""4
0 0
0 5
4 5
4 0
"""
), "merge equal plateaus"

# nested buildings
assert run(
"""3
10 0 10
3 2 4
5 6 8
"""
) == (
"""4
0 0
0 10
10 10
10 0
"""
), "hidden buildings"

# disjoint buildings
assert run(
"""2
4 0 2
3 5 7
"""
) == (
"""8
0 0
0 4
2 4
2 0
5 0
5 3
7 3
7 0
"""
), "ground gap"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Single rectangle | One plateau | Minimum-size input |
| Equal heights touching | Merged segment | Removes unnecessary vertical edges |
| Nested buildings | Only tallest visible | Hidden rectangles ignored |
| Disjoint buildings | Return to ground | Correct handling of gaps |

## Edge Cases

Consider buildings sharing the same boundary:

```
3
5 0 2
3 2 4
7 2 5
```

At `x = 2`, height `5` disappears while heights `3` and `7` appear. The algorithm processes all events at `x = 2` together before reading the new maximum. The heap transitions directly from `5` to `7`, producing:

```
0 0
0 5
2 5
2 7
5 7
5 0
```

No temporary dip occurs.

Now consider nested buildings:

```
3
10 0 10
3 2 4
5 6 8
```

The heap maximum remains `10` throughout the sweep. Smaller buildings enter and leave the heap but never become the maximum, so the skyline never changes inside `[0,10]`.

For equal adjacent buildings:

```
2
5 0 2
5 2 4
```

When the first building ends and the second begins at `x = 2`, the maximum height before and after processing remains `5`. Since `cur_h == prev_h`, no new vertices are emitted. The result becomes one continuous horizontal segment.

Finally, disjoint buildings:

```
2
4 0 2
3 5 7
```

After processing `x = 2`, the heap maximum falls to `0`, so the skyline returns to ground level. At `x = 5`, it rises again to `3`. This correctly preserves empty space between buildings instead of enclosing unnecessary area.
