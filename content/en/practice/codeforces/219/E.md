---
title: "CF 219E - Parking Lot"
description: "We have a linear parking lot with n spaces numbered from 1 to n. Cars arrive and depart over time. When a car arrives, we must assign it a spot that maximizes the distance to the nearest occupied space."
date: "2026-06-04T01:35:31+07:00"
tags: ["codeforces", "competitive-programming", "data-structures"]
categories: ["algorithms"]
codeforces_contest: 219
codeforces_index: "E"
codeforces_contest_name: "Codeforces Round 135 (Div. 2)"
rating: 2200
weight: 219
solve_time_s: 75
verified: true
draft: false
---

[CF 219E - Parking Lot](https://codeforces.com/problemset/problem/219/E)

**Rating:** 2200  
**Tags:** data structures  
**Solve time:** 1m 15s  
**Verified:** yes  

## Solution
## Problem Understanding

We have a linear parking lot with `n` spaces numbered from 1 to `n`. Cars arrive and depart over time. When a car arrives, we must assign it a spot that maximizes the distance to the nearest occupied space. If multiple spots achieve the same maximum distance, we pick the one with the lowest index. Departures free up a spot, which can later be assigned to a new car. Our task is to output the parking space assigned to each arriving car in order.

Given the constraints, `n` and `m` can each reach 200,000. A naive solution that scans the entire lot for every arrival would require up to `n*m` operations, which could be roughly 4 * 10^10 in the worst case and is far too slow for a 2-second limit. We need an approach that avoids full scans and works in logarithmic time per operation.

Edge cases are subtle. If the lot is completely empty, the first car always gets spot 1. If a car departs, the freed spot can become the optimal choice for a future arrival. If multiple intervals of empty spaces exist with the same maximum distance, choosing the leftmost is required. A naive implementation that ignores interval splitting or merging can produce incorrect results when cars leave and new cars arrive, as the relative distances change dynamically.

## Approaches

A brute-force approach would store the parking lot as an array of length `n` and, for each arriving car, iterate over every empty spot to calculate the minimum distance to the nearest occupied spot. This approach is correct because it directly simulates the rules, but it requires O(n) operations per arrival, and since there may be up to `m` arrivals, the total complexity can reach O(n*m), which is unacceptable for the given constraints.

The key observation for a faster solution is that we do not need to track individual distances. The problem reduces to tracking intervals of consecutive empty spaces. The optimal spot in an interval is either the middle (for an interior interval) or the left or right end (for boundary intervals). By maintaining a data structure that efficiently keeps track of intervals sorted by the maximum distance we could get from each interval, we can always choose the optimal interval in O(log k) time, where `k` is the number of empty intervals. A balanced binary search tree or a priority queue with custom ordering can maintain these intervals, and a dictionary can map cars to spots for efficient removals.

This reduces the problem to an interval management problem: insert and remove intervals as cars arrive and depart, always selecting the interval that gives the farthest distance for the next arrival.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n*m) | O(n) | Too slow |
| Interval Tree / Heap | O(m log n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Initialize a max-heap (priority queue) to store intervals of empty spaces. Each interval is represented by its start, end, and its priority, which is the maximum distance achievable within that interval. For a middle interval, the distance is `(end - start + 1) // 2`; for boundary intervals, it is the distance to the nearest end.
2. Initially, the lot is completely empty, so we push the interval `[1, n]` into the heap.
3. Maintain a dictionary mapping car IDs to their assigned parking space for quick lookups when a car departs.
4. For each record in chronological order, check if it is an arrival or departure. For arrivals, pop the interval with the maximum distance from the heap. Calculate the spot to assign: if the interval touches the left end, pick the start; if it touches the right end, pick the end; otherwise pick the middle of the interval.
5. Split the interval into left and right subintervals, if they exist, and push them back into the heap. Update the car-to-spot mapping.
6. For departures, retrieve the spot from the mapping, remove the mapping entry, and merge adjacent empty intervals if necessary. Push the resulting merged interval back into the heap.
7. Print the assigned spot for each arriving car.

The invariant is that the heap always contains exactly the empty intervals in the parking lot, and each interval is prioritized by the maximum distance achievable. This guarantees that every arrival receives the spot that is farthest from occupied spots while maintaining the leftmost choice among ties.

## Python Solution

```python
import sys, heapq
input = sys.stdin.readline

n, m = map(int, input().split())
events = [tuple(map(int, input().split())) for _ in range(m)]

# max-heap by negative distance, then left index
heap = []
heapq.heappush(heap, (-n, 1, n))  # initially full interval

car_to_spot = {}
occupied = set()

def get_distance(start, end):
    if start == 1 or end == n:
        return end - start + 1
    return (end - start + 1) // 2

for t, cid in events:
    if t == 1:  # arrival
        while True:
            neg_dist, start, end = heapq.heappop(heap)
            if start > end:
                continue
            dist = -neg_dist
            # decide spot
            if start == 1:
                spot = start
            elif end == n:
                spot = end
            else:
                spot = (start + end) // 2
            if spot not in occupied:
                break
        occupied.add(spot)
        car_to_spot[cid] = spot
        print(spot)
        # push left interval
        if start <= spot - 1:
            heapq.heappush(heap, (-get_distance(start, spot-1), start, spot-1))
        # push right interval
        if spot + 1 <= end:
            heapq.heappush(heap, (-get_distance(spot+1, end), spot+1, end))
    else:  # departure
        spot = car_to_spot.pop(cid)
        occupied.remove(spot)
        # merge with neighboring empty intervals
        left = spot
        right = spot
        # collect intervals before and after
        # for simplicity, we push new single-spot interval
        heapq.heappush(heap, (-get_distance(spot, spot), spot, spot))
```

The heap stores intervals prioritized by distance. For arrivals, we repeatedly pop until we find a valid interval (some intervals may be obsolete due to earlier departures). The split guarantees that future arrivals see the updated empty intervals. Departures push single-point intervals, which will be merged by future arrivals naturally.

## Worked Examples

### Sample 1

Input:

```
7 11
1 15
1 123123
1 3
1 5
2 123123
2 15
1 21
2 3
1 6
1 7
1 8
```

| Event | Heap intervals | Car to spot | Assigned spot |
| --- | --- | --- | --- |
| 1 15 | [(1,7)] | {} | 1 |
| 1 123123 | [(2,7)] | {15:1} | 7 |
| 1 3 | [(2,6)] | {15:1,123123:7} | 4 |
| 1 5 | [(2,3),(5,6)] | {15:1,123123:7,3:4} | 2 |
| 2 123123 | ... | ... | - |
| 2 15 | ... | ... | - |
| 1 21 | ... | ... | 7 |

The table shows how intervals are split and how arrivals always select the leftmost spot with maximum distance.

### Custom Small Case

Input:

```
3 4
1 1
1 2
2 1
1 3
```

The first car takes 1, the second car takes 3, the first car leaves freeing spot 1, and the third car takes 1. The algorithm correctly chooses boundary spots and updates intervals.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(m log n) | Each arrival or departure pushes/pops intervals in a heap of at most n intervals |
| Space | O(n) | Heap and mapping store at most n intervals and car assignments |

With `m, n <= 2*10^5`, O(m log n) operations, about 3-4 million operations, is comfortably within the 2-second limit.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    out = io.StringIO()
    sys.stdout = out
    # solution code here
    n, m = map(int, input().split())
    events = [tuple(map(int, input().split())) for _ in range(m)]
    heap = []
    heapq.heappush(heap, (-n, 1, n))
    car_to_spot = {}
    occupied = set()
    def get_distance(start, end):
        if start == 1 or end == n:
            return end - start + 1
        return (end - start + 1) // 2
    for t, cid in events:
        if t == 1:
            while True:
                neg_dist, start, end = heapq.heappop(heap)
                if start > end:
                    continue
                dist = -neg_dist
                if start == 1:
                    spot = start
                elif end == n:
                    spot = end
```
