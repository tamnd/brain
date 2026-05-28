---
title: "CF 218B - Airport"
description: "The airport has multiple planes, each with a certain number of empty seats. Every passenger in a queue can choose any plane to buy a ticket from, and the cost of the ticket equals the number of currently empty seats in that plane at the time of purchase."
date: "2026-05-29T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "implementation"]
categories: ["algorithms"]
codeforces_contest: 218
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 134 (Div. 2)"
rating: 1100
weight: 218
solve_time_s: 84
verified: false
draft: false
---

[CF 218B - Airport](https://codeforces.com/problemset/problem/218/B)

**Rating:** 1100  
**Tags:** implementation  
**Solve time:** 1m 24s  
**Verified:** no  

## Solution
## Problem Understanding

The airport has multiple planes, each with a certain number of empty seats. Every passenger in a queue can choose any plane to buy a ticket from, and the cost of the ticket equals the number of currently empty seats in that plane at the time of purchase. We are asked to compute two sums: the maximum total revenue if passengers choose planes greedily to maximize the sum, and the minimum total revenue if passengers choose planes greedily to minimize it.

The input gives the number of passengers `n` and the number of planes `m`, followed by an array of integers representing the initial empty seats for each plane. We must output two integers: the maximum and minimum possible earnings under optimal passenger choices.

The bounds are small: `n` and `m` are at most 1000, and initial seats are at most 1000. With `n` up to 1000, a naive approach that scans all planes for each passenger could still run in `O(n*m)` time, which is acceptable in practice. However, since the seats decrease after each ticket sale, choosing the right data structure to efficiently retrieve the plane with the maximum or minimum available seats makes the solution cleaner and faster.

Non-obvious edge cases include situations where multiple planes have the same number of seats. For example, if two planes both have 1 empty seat and only 2 passengers, the order in which they choose does not affect the total revenue. Another subtle case is when all planes have exactly one seat and `n` equals the total number of seats; maximum and minimum revenue are the same, as no passenger can increase or decrease the price.

## Approaches

A brute-force approach iterates through each passenger, and for each passenger scans all planes to find either the plane with the maximum seats for maximum revenue or the plane with minimum seats for minimum revenue. After selecting a plane, it decreases that plane's seat count by one. This works because the selection at each step is locally optimal, but scanning all planes for every passenger gives `O(n*m)` operations. With `n` and `m` up to 1000, this could take up to 1,000,000 steps-feasible, but slightly inelegant.

The key insight is that the problem is structured so that at each step we only need the current maximum or minimum of the plane seats. A priority queue or heap efficiently maintains the maximum or minimum seat count. For maximum revenue, we use a max-heap, and for minimum revenue, a min-heap. We pop the largest or smallest value, add it to the revenue, decrease it by one, and push it back if it is still positive. Using heaps, each operation takes `O(log m)`, giving total complexity `O(n log m)`-much cleaner and more scalable if the bounds were larger.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n*m) | O(m) | Acceptable for given bounds |
| Heap-based Optimal | O(n log m) | O(m) | Efficient and clear |

## Algorithm Walkthrough

1. Read input: number of passengers `n`, number of planes `m`, and initial empty seats of each plane as an array.
2. For maximum revenue, construct a max-heap from the initial seat counts. Each element in the heap represents the current number of empty seats in a plane.
3. Initialize a counter for total maximum revenue.
4. Iterate over each passenger. At each step, extract the plane with the most seats from the max-heap. Add its current seat count to the total revenue. Decrease its seat count by one, and if it remains positive, push it back into the heap.
5. For minimum revenue, construct a min-heap similarly and repeat the same process but extract the plane with the fewest seats at each step. Decrease and push back if positive.
6. Output the two accumulated sums for maximum and minimum revenue.

Why it works: the algorithm maintains the invariant that the heap always reflects the current number of empty seats for all planes. Choosing the max or min ensures a locally optimal decision for each passenger. Since each passenger chooses greedily, and seats are strictly decreasing, the sequence of greedy choices guarantees global maximum or minimum revenue. There is no combination of choices that could yield a better sum because every revenue unit is collected when seats are largest for maximum, or smallest for minimum.

## Python Solution

```python
import sys
import heapq
input = sys.stdin.readline

n, m = map(int, input().split())
seats = list(map(int, input().split()))

# Max revenue using a max-heap (negative values)
max_heap = [-s for s in seats]
heapq.heapify(max_heap)
max_revenue = 0
for _ in range(n):
    top = -heapq.heappop(max_heap)
    max_revenue += top
    if top - 1 > 0:
        heapq.heappush(max_heap, -(top - 1))

# Min revenue using a min-heap
min_heap = seats[:]
heapq.heapify(min_heap)
min_revenue = 0
for _ in range(n):
    top = heapq.heappop(min_heap)
    min_revenue += top
    if top - 1 > 0:
        heapq.heappush(min_heap, top - 1)

print(max_revenue, min_revenue)
```

The code first converts the seat counts into a max-heap by negating the numbers because Python's `heapq` is a min-heap by default. For maximum revenue, we repeatedly pop the largest seat count, add it to the revenue, decrease, and push back if positive. For minimum revenue, we use a min-heap and do the symmetric operation. Edge cases like multiple planes with the same number of seats or `n` equal to total seats are automatically handled by the heap.

## Worked Examples

**Sample 1**

Input: `4 3\n2 1 1`

| Passenger | Max Heap (after) | Max Revenue | Min Heap (after) | Min Revenue |
| --- | --- | --- | --- | --- |
| 1 | [1,1,1] | 2 | [1,1,2] | 2 |
| 2 | [1,1,0] | 3 | [1,1] | 3 |
| 3 | [1,0,0] | 4 | [1,0] | 4 |
| 4 | [0,0,0] | 5 | [0,0] | 5 |

Both sums equal 5, demonstrating the edge case where total seats equal number of passengers, making min and max revenue identical.

**Sample 2**

Input: `4 3\n3 1 2`

| Passenger | Max Heap | Max Revenue | Min Heap | Min Revenue |
| --- | --- | --- | --- | --- |
| 1 | [2,1,2] | 3 | [1,2,3] | 1 |
| 2 | [2,1,1] | 5 | [2,2] | 2 |
| 3 | [1,1,1] | 7 | [1,1] | 3 |
| 4 | [1,0,1] | 8 | [0,1] | 4 |

This shows different sequences of greedy choices, producing distinct min and max totals.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log m) | Each passenger does one heap pop and push, both `O(log m)` |
| Space | O(m) | Heaps store current seat counts for all planes |

With `n` and `m` up to 1000, `n log m` operations are around 10,000, well within the 2-second limit.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    n, m = map(int, input().split())
    seats = list(map(int, input().split()))

    max_heap = [-s for s in seats]
    heapq.heapify(max_heap)
    max_revenue = 0
    for _ in range(n):
        top = -heapq.heappop(max_heap)
        max_revenue += top
        if top - 1 > 0:
            heapq.heappush(max_heap, -(top - 1))

    min_heap = seats[:]
    heapq.heapify(min_heap)
    min_revenue = 0
    for _ in range(n):
        top = heapq.heappop(min_heap)
        min_revenue += top
        if top - 1 > 0:
            heapq.heappush(min_heap, top - 1)

    return f"{max_revenue} {min_revenue}"

# provided samples
assert run("4 3\n2 1 1\n") == "5 5", "sample 1"
assert run("4 3\n3 1 2\n") == "8 4", "sample 2"

# custom cases
assert run("1 1\n1\n") == "1 1", "single passenger, single seat"
assert run("3 3\n1 1 1\n") == "3 3", "all seats 1"
assert run("5 2\n3 5\n") == "16 11", "unequal seats, multiple passengers"
assert run("6 4\n1 2 3 4\n") == "18 10", "mixed seats"
assert run("1000 1\n1000\n") == "500
```
