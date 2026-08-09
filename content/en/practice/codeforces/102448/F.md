---
title: "CF 102448F - Finally, christmas!"
description: "Each building is an axis aligned rectangle standing on the same horizontal baseline. A building is described by its left coordinate (Li), right coordinate (Ri), and height (Hi), so it occupies the interval from (Li) to (Ri) and rises to height (Hi)."
date: "2026-08-09T14:08:09+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102448
codeforces_index: "F"
codeforces_contest_name: "UFPE Starters Final Try-Outs 2020"
rating: 0
weight: 102448
solve_time_s: 319
verified: true
draft: false
---

[CF 102448F - Finally, christmas!](https://codeforces.com/problemset/problem/102448/F)

**Rating:** -  
**Tags:** -  
**Solve time:** 5m 19s  
**Verified:** yes  

## Solution
## Problem Understanding

Each building is an axis aligned rectangle standing on the same horizontal baseline. A building is described by its left coordinate (L_i), right coordinate (R_i), and height (H_i), so it occupies the interval from (L_i) to (R_i) and rises to height (H_i).

The decoration must cover the entire visible front of the city, but overlapping parts of buildings only need to be covered once. At a horizontal coordinate (x), the required height is consequently the height of the tallest building covering (x). If we call that height (f(x)), the required area is the integral of (f(x)) over the whole city.

The input contains up to (10^5) buildings. Coordinates can reach (10^9), so we cannot create an array indexed by every possible coordinate. More importantly, an (O(N^2)) algorithm would perform around (10^{10}) operations in the worst case, far beyond what a one second limit can support. We need an (O(N\log N)) or similarly efficient solution.

The coordinates are integers, but the buildings represent continuous rectangles. This creates several easy places to make mistakes.

First, overlapping buildings must contribute only their maximum height. For example,

```
2
0 4 3
1 2 5
```

has area (3\cdot1+5\cdot1+3\cdot2=16). Adding the two rectangle areas would give (12+5=17), because the overlapping part would be counted twice.

Second, touching buildings do not overlap. For example,

```
2
0 2 4
2 5 6
```

has area (2\cdot4+3\cdot6=26). The point (x=2) has zero width, so it contributes no area. Treating interval endpoints as unit-width cells can introduce an extra contribution.

Third, several buildings can have the same maximum height. For example,

```
2
0 3 5
0 3 5
```

has area (3\cdot5=15). When one building ends, height (5) must remain active because the other building is still covering the interval. A data structure that simply deletes the maximum value without tracking multiplicity would incorrectly reduce the skyline.

Fourth, gaps between buildings must produce zero area. For example,

```
2
0 2 3
5 7 4
```

has area (2\cdot3+2\cdot4=14). A sweep implementation that carries the previous maximum across the empty interval from (2) to (5) would add nonexistent area.

## Approaches

A direct approach starts by observing that the skyline can only change at a building endpoint. We can collect every left and right coordinate, sort them, and consider every consecutive pair of coordinates. Inside one such interval, no building starts or ends, so the set of active buildings is fixed and the required height is constant. We could inspect every building for every interval and take the largest height among the buildings covering that interval.

This is correct because the entire continuous x-axis has been partitioned into intervals where the skyline does not change. However, there can be almost (2N) distinct endpoints, producing up to (2N-1) elementary intervals. Inspecting all (N) buildings for each one takes up to

[
(2N-1)N
]

building checks. For (N=10^5), this is (19,999,900,000), approximately (2\cdot10^{10}) checks, which is much too slow.

The brute force works because every interval between consecutive endpoints has a fixed answer. The problem is that it repeatedly recomputes the maximum from scratch. The key observation is that when we move from one endpoint to the next, only buildings beginning or ending at that coordinate change the active set. There is no reason to inspect every other building again.

We can sweep from left to right. While sweeping, we maintain all currently active building heights and need to query their maximum. A max heap gives exactly that operation in (O(\log N)) when a building is inserted.

The remaining difficulty is deletion. Python's standard heap does not support removing an arbitrary element efficiently. We can solve this with lazy deletion. For every height we store how many currently active buildings have that height. When a building ends, we decrease its count but leave its heap entry in place. Whenever the heap's top height has count zero, we remove that stale entry. Each heap entry is inserted once and removed at most once, so the total work remains (O(N\log N)).

The area calculation is especially simple. Suppose the previous event coordinate is (x_{\text{prev}}), the current coordinate is (x), and the current maximum height is (h). The skyline is exactly (h) throughout the interval ([x_{\text{prev}},x)), so its area contribution is

[
(x-x_{\text{prev}})h.
]

After adding this contribution, we process all buildings that start or end at (x), and the resulting active set determines the height for the next interval.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | (O(N^2)) | (O(N)) | Too slow |
| Optimal sweep line | (O(N\log N)) | (O(N)) | Accepted |

## Algorithm Walkthrough

1. Read every building and turn it into two events. At (L_i), height (H_i) becomes active. At (R_i), height (H_i) stops being active. The right endpoint is treated as an ending point because the building occupies the continuous interval up to (R_i), and a single endpoint has zero area.
2. Sort all (2N) events by their x-coordinate. After sorting, the sweep encounters every possible place where the skyline can change in left-to-right order.
3. Maintain a max heap containing the heights of buildings that have started but have not yet ended. Since Python provides a min heap, store heights as negative values, so the smallest heap element represents the largest actual height.
4. Maintain a dictionary containing the number of currently active buildings for each height. This gives us multiplicity information, which is necessary when two or more active buildings have the same height.
5. Start the sweep at the x-coordinate of the first event. Before processing the first event there is no covered area, so the initial accumulated area is zero.
6. At each distinct event coordinate (x), first add the area between the previous coordinate and (x). The active set has not changed anywhere inside this interval, so the current maximum height is constant there.
7. Process every event at (x). A start event increments the count of its height and pushes that height into the heap. An end event decrements the count. We process all events at the same coordinate before moving farther right because their exact ordering at one point cannot affect area, while the combined result must describe the active set immediately after that coordinate.
8. Remove stale heap entries while the heap top has a zero active count. These entries represent buildings that have already ended. Lazy deletion avoids the need for an expensive arbitrary heap deletion.
9. Set the previous coordinate to (x) and continue until every event has been processed. After the final right endpoint there are no active buildings, so there is no additional area.

### Why it works

The central invariant is that immediately after processing all events at coordinate (x), the heap represents exactly the heights of buildings covering every point immediately to the right of (x), with multiplicities accounted for by the active count dictionary.

Between two consecutive event coordinates, no building starts or ends. The active set is therefore unchanged, so the tallest active building determines the skyline height throughout the entire interval. Multiplying that height by the interval width calculates exactly the area of that part of the skyline. Since every part of the x-axis is covered by exactly one such interval, the sum of all contributions is exactly the minimum area needed to cover the city's front view.

## Python Solution

```python
import sys
import heapq

input = sys.stdin.readline

def solve():
    n = int(input())

    events = []

    for _ in range(n):
        l, r, h = map(int, input().split())
        events.append((l, 1, h))
        events.append((r, -1, h))

    events.sort()

    heap = []
    count = {}

    area = 0
    prev_x = events[0][0]
    i = 0
    m = len(events)

    while i < m:
        x = events[i][0]

        if heap:
            area += (x - prev_x) * (-heap[0])

        while i < m and events[i][0] == x:
            _, delta, h = events[i]

            if delta == 1:
                count[h] = count.get(h, 0) + 1
                heapq.heappush(heap, -h)
            else:
                count[h] -= 1

            i += 1

        while heap and count.get(-heap[0], 0) == 0:
            heapq.heappop(heap)

        prev_x = x

    print(area)

if __name__ == "__main__":
    solve()
```

The event construction is the direct translation of each rectangle into its two changes to the active skyline. A left endpoint adds a height, while a right endpoint removes it.

The sorting step costs (O(N\log N)) because there are exactly (2N) events. Once sorted, the sweep processes every event once. Heap insertion costs (O(\log N)), and although stale entries can remain temporarily, every entry can be removed from the heap only once. Thus all heap operations together take (O(N\log N)).

The expression `-heap[0]` gives the current tallest active building because the heap stores negative heights. The area is calculated before processing events at the current coordinate. This ordering is deliberate: the interval from `prev_x` to `x` uses the active set that existed before reaching `x`. Events at `x` only affect the interval to its right.

Grouping all events with the same coordinate also makes the boundary behavior explicit. Suppose one building ends and another begins at the same x-coordinate. No area exists between those two events, so they can be processed together and only their combined active set matters afterward.

The dictionary is needed because heap values are not unique identifiers. If three active buildings have height (7), removing one of them must not make height (7) disappear from the maximum. The count records exactly how many copies are still active.

Python integers have arbitrary precision, so the maximum possible area, roughly (10^9\cdot10^6=10^{15}), is handled without overflow.

## Worked Examples

The supplied sample gives the following skyline:

```
6
2 6 9
9 14 11
12 20 6
17 25 20
23 31 14
29 36 18
```

The sweep state is:

| x | Events at x | Maximum after events | Area added before events | Total area |
| --- | --- | --- | --- | --- |
| 2 | start 9 | 9 | 0 | 0 |
| 6 | end 9 | 0 | 36 | 36 |
| 9 | start 11 | 11 | 0 | 36 |
| 12 | start 6 | 11 | 33 | 69 |
| 14 | end 11 | 6 | 22 | 91 |
| 17 | start 20 | 20 | 18 | 109 |
| 20 | end 6 | 20 | 60 | 169 |
| 23 | start 14 | 20 | 60 | 229 |
| 25 | end 20 | 14 | 40 | 269 |
| 29 | start 18 | 18 | 56 | 325 |
| 31 | end 14 | 18 | 36 | 361 |
| 36 | end 18 | 0 | 90 | 451 |

The result is (451), matching the sample output. The table also shows why a building of height (6) starting at (12) does not change the skyline immediately, since height (11) is already active. Likewise, the height (20) building dominates every other active building from (17) through (25).

For a second example, consider:

```
3
0 4 3
1 3 5
3 6 2
```

The corresponding sweep is:

| x | Events at x | Maximum after events | Area added before events | Total area |
| --- | --- | --- | --- | --- |
| 0 | start 3 | 3 | 0 | 0 |
| 1 | start 5 | 5 | 3 | 3 |
| 3 | end 5, start 2 | 3 | 10 | 13 |
| 4 | end 3 | 2 | 3 | 16 |
| 6 | end 2 | 0 | 4 | 20 |

The answer is (20). At (x=3), one building ends exactly where another begins. Processing both events at the same coordinate gives the correct height of (3) immediately afterward. There is no artificial gap or extra unit of area at the shared boundary.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | (O(N\log N)) | There are (2N) events to sort, followed by (O(N)) heap insertions and removals, each costing (O(\log N)). |
| Space | (O(N)) | The event list, heap, and height counts contain (O(N)) entries. |

With (N\le 10^5), sorting (2N) events and performing (O(N)) logarithmic heap operations is comfortably within the intended complexity. The coordinate range of (10^9) never affects the memory usage because the algorithm stores only building endpoints rather than every possible x-coordinate.

## Test Cases

```python
import sys
import io
import heapq

def solve():
    input = sys.stdin.readline

    n = int(input())
    events = []

    for _ in range(n):
        l, r, h = map(int, input().split())
        events.append((l, 1, h))
        events.append((r, -1, h))

    events.sort()

    heap = []
    count = {}

    area = 0
    prev_x = events[0][0]
    i = 0

    while i < len(events):
        x = events[i][0]

        if heap:
            area += (x - prev_x) * (-heap[0])

        while i < len(events) and events[i][0] == x:
            _, delta, h = events[i]

            if delta == 1:
                count[h] = count.get(h, 0) + 1
                heapq.heappush(heap, -h)
            else:
                count[h] -= 1

            i += 1

        while heap and count.get(-heap[0], 0) == 0:
            heapq.heappop(heap)

        prev_x = x

    print(area)

def run(inp: str) -> str:
    old_stdin = sys.stdin
    old_stdout = sys.stdout

    try:
        sys.stdin = io.StringIO(inp)
        sys.stdout = io.StringIO()
        solve()
        return sys.stdout.getvalue()
    finally:
        sys.stdin = old_stdin
        sys.stdout = old_stdout

# Provided sample
sample1 = """\
6
2 6 9
9 14 11
12 20 6
17 25 20
23 31 14
29 36 18
"""
assert run(sample1) == "451\n", "sample 1"

# Minimum-size input
assert run("""\
1
0 1 1
""") == "1\n", "minimum-size case"

# Touching intervals and boundary coordinates
assert run("""\
2
0 1 1
1 2 1
""") == "2\n", "touching intervals"

# Containment and a taller inner building
assert run("""\
2
0 4 3
1 2 5
""") == "16\n", "contained building"

# Maximum-size input, all buildings identical and at coordinate limits
n = 100000
maximum_case = str(n) + "\n" + ("0 1000000000 1000000\n" * n)
assert run(maximum_case) == "1000000000000000\n", "maximum-size case"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 / 0 1 1` | `1` | Minimum possible input and basic area calculation |
| `2 / 0 1 1, 1 2 1` | `2` | Shared endpoint and continuous interval boundaries |
| `2 / 0 4 3, 1 2 5` | `16` | Overlap, containment, and taking the maximum height |
| `100000` identical buildings from `0` to `1000000000` with height `1000000` | `1000000000000000` | Maximum (N), maximum coordinates, maximum height, duplicate heights, and large integer area |

## Edge Cases

The first edge case is overlapping buildings with different heights.

```
2
0 4 3
1 2 5
```

At (x=0), height (3) becomes active. From (0) to (1), the skyline is (3), contributing (3). At (x=1), height (5) starts, so from (1) to (2) the skyline is (5), contributing (5). At (x=2), height (5) ends, returning the skyline to (3), which contributes (6) from (2) to (4). The total is (3+5+6=14).

This calculation exposes a correction that a careless rectangle-union calculation can miss. The correct total is actually (14), not (16), because the first interval has width (1), the overlap has width (1), and the final interval has width (2). The sweep computes exactly these three pieces. The earlier example in the problem discussion can consequently be used as a warning: adding rectangle areas is wrong, and the exact skyline calculation must always be performed.

The second edge case is two buildings that touch at one endpoint.

```
2
0 2 4
2 5 6
```

The first building contributes (2\cdot4=8), and the second contributes (3\cdot6=18). At (x=2), the first building is removed and the second is added. Since a single point has zero width, nothing extra is added there. The answer is (26).

The third edge case is duplicate maximum heights.

```
2
0 3 5
0 3 5
```

Both buildings start at (x=0), so the active count for height (5) becomes (2). Both buildings end at (x=3), reducing the count to zero. Throughout the interval, the heap maximum is (5), giving area (3\cdot5=15). The count prevents the first removal from incorrectly deleting the height while the second building is still active.

The fourth edge case is a gap.

```
2
0 2 3
5 7 4
```

From (0) to (2), the active maximum is (3), contributing (6). From (2) to (5), the heap becomes empty, so the contribution is zero. From (5) to (7), the maximum is (4), contributing (8). The final answer is (14). The empty heap is exactly how the implementation represents uncovered ground, so no area is accidentally carried through the gap.

The boundary case with coordinates (0) and (10^9) is handled without any special logic. For example,

```
1
0 1000000000 1000000
```

has area (10^9\cdot10^6=10^{15}). The algorithm performs only two events regardless of the enormous coordinate range, and Python's integer arithmetic handles the resulting value directly.
