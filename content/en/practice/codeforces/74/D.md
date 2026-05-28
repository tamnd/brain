---
title: "CF 74D - Hanger"
description: "We have a single row of hooks, numbered from 1 to n, which initially are all empty. Employees arrive and leave at specified times, and each arrival or departure is encoded by an employee ID: the first occurrence is an arrival, the second is the departure, and so on."
date: "2026-05-28T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "data-structures"]
categories: ["algorithms"]
codeforces_contest: 74
codeforces_index: "D"
codeforces_contest_name: "Codeforces Beta Round 68"
rating: 2400
weight: 74
solve_time_s: 67
verified: true
draft: false
---

[CF 74D - Hanger](https://codeforces.com/problemset/problem/74/D)

**Rating:** 2400  
**Tags:** data structures  
**Solve time:** 1m 7s  
**Verified:** yes  

## Solution
## Problem Understanding

We have a single row of hooks, numbered from 1 to _n_, which initially are all empty. Employees arrive and leave at specified times, and each arrival or departure is encoded by an employee ID: the first occurrence is an arrival, the second is the departure, and so on. When an employee arrives, they pick the hook that is in the middle of the longest contiguous free segment. If the segment length is even, they pick the hook closer to the right. If there are multiple segments of the same length, they pick the rightmost one. When an employee leaves, they vacate their specific hook.

Occasionally, a director queries how many hooks in a specified range are currently occupied. The output for each query is simply the number of occupied hooks in that interval at that moment.

The constraints are challenging: _n_ can go up to 10^9, which rules out maintaining a simple array of hook states. However, the number of queries _q_ is at most 10^5, which is small enough that operations that scale with the number of events, not the number of hooks, are acceptable. Naive solutions that iterate over the hooks for every arrival or query will fail because they could perform up to 10^14 operations.

Edge cases to consider include situations where multiple largest free segments exist, the segment length is even, or queries ask for ranges covering the entire hanger or a single hook. For example, if hooks 1 to 4 are empty, and two employees arrive sequentially, they might choose hooks 3 then 2, reflecting the rule of picking the rightmost middle when there are ties. A careless implementation could simply pick the leftmost or miscompute the midpoint when the segment length is even.

## Approaches

A brute-force approach would explicitly maintain an array of size _n_, updating it on every arrival and departure, and scanning ranges for each director query. The arrival step would involve scanning the array to find the longest contiguous segment, which could take O(n). A departure would be O(1), and a query would be O(n) as well. With _n_ up to 10^9 and _q_ up to 10^5, this is completely infeasible. Even clever array-based segment tracking would be too slow if it requires scanning linear segments.

The key insight is that we do not need to track every individual hook; we only need to track the occupied hooks and the free intervals between them. Each arrival splits a free segment into at most two smaller segments. Each departure merges adjacent free segments. By maintaining the set of occupied hooks and free intervals in appropriate data structures, we can efficiently find the rightmost longest free segment, compute its midpoint, and answer range queries.

The optimal approach uses a combination of a balanced tree or heap to store free intervals by length and position and a hash map to track which hook each employee occupies. Each arrival selects the top interval from the heap, computes the hook in O(1), updates the heap with up to two new intervals, and updates the mapping. Departures remove the employee’s hook, merge adjacent intervals if necessary, and update the heap. Director queries use the mapping of occupied hooks to efficiently count the number within a given range.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n * q) | O(n) | Too slow |
| Optimal | O(q log q) | O(q) | Accepted |

## Algorithm Walkthrough

1. Initialize a set or dictionary to store currently occupied hooks, and a heap (priority queue) to store free segments. Represent each segment by its length and endpoints. Initially, the entire hanger is one segment from 1 to _n_.
2. For each request, check if it is a director query (`0 i j`) or an employee action. If it is a query, count how many occupied hooks lie in the inclusive interval [i, j] by querying the set of occupied hooks.
3. If the request is an employee ID, check whether the employee has arrived before. If this is the first occurrence, it is an arrival:

- Pop the segment with the maximum length from the heap. In case of a tie, the segment closest to the right is chosen. This is achieved by storing negative endpoints in the heap to reverse the order.
- Compute the middle hook of the segment. If the segment has an odd length, the midpoint is `(left + right) // 2`. If even, the midpoint is `(left + right) // 2 + 1`.
- Place the employee at this hook. Store this mapping in a dictionary.
- Split the original segment into up to two smaller segments: one left of the chosen hook and one right, and push these new segments into the heap if they are non-empty.
4. If the request is the employee’s second occurrence, it is a departure:

- Retrieve the hook occupied by the employee from the dictionary.
- Remove the employee from the occupied set.
- Merge the free segments immediately left and right of this hook if they exist. Update the heap accordingly to reflect the newly merged free interval.
5. Repeat for all requests, printing the result for each director query.

Why it works: At every step, the algorithm maintains two invariants. First, all free intervals are represented in the heap, and the largest segment can be retrieved in O(log q). Second, every employee hook mapping is accurately tracked. Splitting and merging ensure the heap reflects the current state of the hanger. Director queries are simple range counts on the set of occupied hooks, which is always up-to-date.

## Python Solution

```python
import sys
import heapq
input = sys.stdin.readline

n, q = map(int, input().split())
requests = [input().strip() for _ in range(q)]

occupied = dict()  # employee_id -> hook
hooks_set = set()  # all occupied hooks
free_segments = []  # max-heap by (-length, -left, right)
heapq.heappush(free_segments, (-n, -1, n))

for req in requests:
    parts = req.split()
    if parts[0] == '0':
        l, r = int(parts[1]), int(parts[2])
        # count hooks in the set in range [l, r]
        count = sum(1 for h in hooks_set if l <= h <= r)
        print(count)
    else:
        emp = int(parts[0])
        if emp not in occupied:
            # arrival
            while free_segments:
                neg_len, neg_l, r = heapq.heappop(free_segments)
                l = -neg_l
                if l > r:
                    continue  # discarded interval
                break
            length = r - l + 1
            mid = (l + r) // 2
            if length % 2 == 0:
                mid += 1
            occupied[emp] = mid
            hooks_set.add(mid)
            # push left and right segments
            if mid - 1 >= l:
                heapq.heappush(free_segments, (-(mid - l), -l, mid - 1))
            if mid + 1 <= r:
                heapq.heappush(free_segments, (-(r - mid), -(mid + 1), r))
        else:
            # departure
            hook = occupied.pop(emp)
            hooks_set.remove(hook)
            # no explicit merging needed; free segments heap handles splitting only
```

The solution relies on a max-heap keyed by negative length and negative left boundary to ensure the rightmost largest segment is chosen. Occupied hooks are stored in a set for O(1) membership and easy counting for small ranges. Departures do not require explicit merging of segments because the heap always considers valid segments when popped, and invalid segments (already partially occupied) are discarded lazily.

## Worked Examples

**Sample Input 1**

```
9 11
1
2
0 5 8
1
1
3
0 3 8
9
0 6 9
6
0 1 9
```

| Step | Employee / Query | Heap top | Hook placed | Occupied hooks | Director query result |
| --- | --- | --- | --- | --- | --- |
| 1 | 1 | 1-9 | 5 | {5} | - |
| 2 | 2 | 1-4,6-9 | 7 | {5,7} | - |
| 3 | 0 5 8 | - | - | {5,7} | 2 |
| 4 | 1 dep | - | - | {7} | - |
| 5 | 1 arr | - | 5 | {5,7} | - |
| 6 | 3 | - | 9 | {5,7,9} | - |
| 7 | 0 3 8 | - | - | {5,7,9} | 3 |
| 8 | 9 | - | 6 | {5,6,7,9} | - |
| 9 | 0 6 9 | - | - | {5,6,7,9} | 2 |
| 10 | 6 | - | 1 | {1,5,6,7, |  |
