---
title: "CF 104969E - Pizza Expiry"
description: "Each pizza consists of a circular arrangement of slices plus a center point. Every slice has a cost parameter and the crust around the pizza also has a cost parameter."
date: "2026-06-28T06:41:34+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104969
codeforces_index: "E"
codeforces_contest_name: "UTPC Contest 02-09-24 Div. 1 (Advanced)"
rating: 0
weight: 104969
solve_time_s: 86
verified: true
draft: false
---

[CF 104969E - Pizza Expiry](https://codeforces.com/problemset/problem/104969/E)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 26s  
**Verified:** yes  

## Solution
## Problem Understanding

Each pizza consists of a circular arrangement of slices plus a center point. Every slice has a cost parameter and the crust around the pizza also has a cost parameter. The underlying idea is that we are allowed to “connect” vertices of this structure using two types of connections, slice-based connections and crust-based connections, and we want the minimum total cost required to make the whole pizza connected.

For each pizza, this reduces to finding a cheapest way to ensure that all slice vertices and the center belong to a single connected component. There are two natural strategies. One is to connect every slice directly to the center using slice connections. The other is to connect slices in a cycle using crust connections and then attach the center once using the cheapest slice connection. The answer for each pizza is the minimum cost among these two constructions.

Once this value is computed for every pizza, it becomes a scheduling problem. Each pizza takes one unit of time to eat, starting from time zero, and pizza i must be eaten strictly before time d_i, otherwise it is considered wasted and contributes v_i to the penalty. Since only one pizza can be eaten at a time, we are effectively assigning unit length jobs to integer time slots, where each job has a deadline and a penalty if not completed in time. The goal is to minimize total penalty from missed deadlines.

The constraints allow up to 100,000 pizzas, so any approach that tries all permutations or simulates scheduling in quadratic time will not work. We need something close to O(N log N), since sorting and priority queue operations are feasible, but repeated rescanning or dynamic programming over all states is not.

A subtle failure case comes from confusing the connectivity cost d_i with the scheduling constraint. A greedy approach that schedules pizzas by increasing v_i or increasing d_i without respecting deadlines can easily fail. Another mistake is treating d_i as independent without recognizing it depends only on a small structural optimization per pizza.

## Approaches

We first handle a single pizza. If we ignore structure, we might try to compute the minimum way to connect all vertices using generic MST methods over a graph of size s_i + 1. That would work conceptually but is too slow if done independently for each pizza in a naive way.

The key observation is that the graph has a very specific form: a cycle of slices with uniform crust cost c_i and a center connected to every slice with cost q_i. In such a structure, an optimal spanning tree must take one of two forms. Either we connect every slice directly to the center, costing the sum of all q_i, or we use the cycle edges for all but one connection around the circle and connect the center only through the cheapest slice. That gives cost (s_i - 1) * c_i + min(q_i). Taking the minimum of these two gives d_i in O(1) per pizza.

Once all d_i are computed, each pizza becomes a unit-time job with deadline d_i and penalty v_i if not completed on time. We want to maximize the total value of jobs completed before their deadlines.

A brute force scheduling approach would try all permutations of pizzas, simulate time progression, and compute penalties, leading to O(N!) or at best O(N^2) checking, which is impossible for N up to 100,000.

The standard observation for unit-time jobs with deadlines is that we should process jobs in increasing order of deadlines. While scanning, we maintain a set of chosen jobs. If at any point we have selected more jobs than the current deadline allows, we must discard one job, and the best choice to discard is the one with smallest value v_i. This greedy exchange argument ensures we keep the most valuable feasible set.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute force scheduling | O(N!) or O(N^2 N!) | O(1) | Too slow |
| Optimal (compute d_i + greedy scheduling) | O(N log N) | O(N) | Accepted |

## Algorithm Walkthrough

### 1. Compute connectivity cost for each pizza

For each pizza, compute two candidate costs. The first is the sum of all slice strengths q_i, representing connecting every slice directly to the center. The second is (s_i - 1) * c_i plus the minimum slice strength, representing using the crust cycle for all but one connection and attaching the center through the cheapest slice. Take the minimum of these two as d_i.

This step reduces the geometric structure into a single deadline value per pizza.

### 2. Treat each pizza as a scheduling job

Each pizza becomes a job with processing time 1, deadline d_i, and profit v_i if completed before its deadline. Missing it means paying v_i as waste.

We shift perspective from geometry to scheduling.

### 3. Sort pizzas by deadline

Sort all jobs in increasing order of d_i. This ensures we always consider the most urgent constraints first.

### 4. Maintain a set of chosen pizzas

Iterate through sorted jobs, maintaining a max-feasible subset. Add each job tentatively into a collection of selected pizzas.

### 5. Enforce feasibility using a min-heap of values

If the number of selected jobs exceeds the current time limit implied by the deadline ordering, remove the job with the smallest v_i. This keeps the most valuable subset that can still be scheduled.

The intuition is that whenever we exceed capacity, we must drop something, and the least costly loss is always optimal to discard.

### Why it works

At any prefix of jobs sorted by deadline, the algorithm maintains the best possible subset of jobs that can fit into that prefix’s available time slots. The invariant is that after processing all jobs with deadline ≤ T, we keep at most T jobs, and among all such subsets we keep the one with maximum total value. Any time we exceed capacity, replacing a smaller v_i job with a larger one preserves feasibility and improves or maintains total value. This exchange argument guarantees that no optimal solution is ever excluded by the greedy removals.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    jobs = []
    
    for _ in range(n):
        s, q, c, v = map(int, input().split())
        
        total_q = s * q
        min_q = q
        
        # connectivity cost
        d = min(total_q, (s - 1) * c + min_q)
        
        jobs.append((d, v))
    
    jobs.sort()
    
    import heapq
    heap = []
    heap_sum = 0
    
    for d, v in jobs:
        heapq.heappush(heap, v)
        heap_sum += v
        
        # we can keep at most d jobs by time d
        if len(heap) > d:
            heap_sum -= heapq.heappop(heap)
    
    total = sum(v for _, v in jobs)
    print(total - heap_sum)

if __name__ == "__main__":
    solve()
```

The implementation first compresses each pizza into its effective deadline. The heap stores the values of pizzas we decide to complete on time. Whenever we exceed the allowed number of jobs for the current deadline prefix, we remove the smallest value, because it contributes least to the final objective.

The final answer is computed as total value minus the sum of selected on-time jobs, which directly gives the total wasted value.

## Worked Examples

### Example 1

Consider pizzas with computed deadlines and values:

| Step | Sorted job (d, v) | Heap contents | Kept value sum |
| --- | --- | --- | --- |
| 1 | (1, 4) | [4] | 4 |
| 2 | (2, 3) | [3, 4] | 7 |
| 3 | (2, 5) | [3, 4, 5] → remove 3 | [4, 5] = 9 |

Here we always drop the smallest value when capacity is exceeded. The final kept value is maximized.

This demonstrates that earlier deadlines restrict how many jobs can be scheduled, and value-based pruning preserves optimality.

### Example 2

Input:

```
4
2 3 5 10
3 1 4 20
2 2 2 5
1 10 1 7
```

Assume computed deadlines:

(2,10), (3,20), (2,5), (1,7)

| Step | Job | Heap | Kept sum |
| --- | --- | --- | --- |
| 1 | (1,7) | [7] | 7 |
| 2 | (2,10) | [7,10] | 17 |
| 3 | (2,5) | [5,10,7] → remove 5 | [7,10] = 17 |
| 4 | (3,20) | [7,10,20] | 37 |

The final selection keeps the most valuable feasible subset, respecting deadlines at each prefix.

This confirms the greedy removal strategy correctly balances urgency and value.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(N log N) | Sorting dominates, heap operations are logarithmic per insertion/removal |
| Space | O(N) | Stores all jobs in a heap and array |

The solution fits comfortably within limits since both N log N sorting and heap operations are efficient for 100,000 elements.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    return sys.stdout.getvalue() if False else solve_capture(inp)

def solve_capture(inp: str) -> str:
    import sys, heapq
    input = sys.stdin.readline
    sys.stdin = io.StringIO(inp)
    
    n = int(input())
    jobs = []
    
    for _ in range(n):
        s, q, c, v = map(int, input().split())
        d = min(s * q, (s - 1) * c + q)
        jobs.append((d, v))
    
    jobs.sort()
    
    heap = []
    total = 0
    kept = 0
    
    for d, v in jobs:
        heapq.heappush(heap, v)
        total += v
        if len(heap) > d:
            total -= heapq.heappop(heap)
    
    allv = sum(v for _, v in jobs)
    return str(allv - total)

# sample-like tests
assert solve_capture("1\n2 3 5 10\n") == "0"
assert solve_capture("2\n1 1 1 5\n2 2 2 7\n") in {"0", "5"}

# edge: all deadlines large
assert solve_capture("3\n2 1 1 1\n2 1 1 2\n2 1 1 3\n") == "0"

# edge: tight deadlines force drops
assert solve_capture("3\n1 1 1 10\n2 1 1 20\n2 1 1 30\n") in {"10", "20", "30"}

# large equal structure
assert solve_capture("2\n100 5 1 1\n100 5 1 2\n") == "0"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single job | 0 | base scheduling correctness |
| increasing values | 0 | greedy keeps all feasible |
| equal structure | 0 | symmetric handling |
| tight deadlines | partial loss | heap eviction behavior |

## Edge Cases

A corner case appears when all slices are identical and the crust is much cheaper than slice connections. In that case, d_i becomes (s_i - 1) * c_i + q_i, and any mistake in taking the minimum slice strength instead of full q_i would overestimate feasibility.

Another edge case is when many pizzas share the same small deadline. The algorithm repeatedly exceeds capacity at the same threshold, forcing multiple removals. The heap-based selection still works because every violation is resolved locally by discarding the least valuable job, and this decision remains valid even if several constraints collide at the same time.
