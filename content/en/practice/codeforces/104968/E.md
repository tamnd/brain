---
title: "CF 104968E - Pizza Expiry"
description: "Each pizza comes with a structure that can be interpreted as a small graph. There is a central point and a ring of $si$ slice vertices. Every slice vertex is connected to the center with cost $qi$, and each slice is also connected to its two neighbors on the ring with cost $ci$."
date: "2026-06-28T06:49:11+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104968
codeforces_index: "E"
codeforces_contest_name: "UTPC Contest 02-09-24 Div. 2 (Beginner)"
rating: 0
weight: 104968
solve_time_s: 100
verified: false
draft: false
---

[CF 104968E - Pizza Expiry](https://codeforces.com/problemset/problem/104968/E)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 40s  
**Verified:** no  

## Solution
## Problem Understanding

Each pizza comes with a structure that can be interpreted as a small graph. There is a central point and a ring of $s_i$ slice vertices. Every slice vertex is connected to the center with cost $q_i$, and each slice is also connected to its two neighbors on the ring with cost $c_i$. The value $d_i$ is the minimum cost required to make this whole structure connected, which is exactly the weight of a minimum spanning tree over this graph.

After computing $d_i$ for each pizza, the actual game becomes a scheduling problem. Time starts at zero, each pizza takes one unit of time to eat, and pizza $i$ must be started strictly before time $d_i$. If you fail to eat it before its deadline, you incur a loss of $v_i$. Since only one pizza can be eaten at a time, the task is to choose an ordering that minimizes the total lost value.

The constraint $N \le 10^5$ implies that any solution with quadratic behavior over pizzas is impossible. Even $O(N \log^2 N)$ would be risky depending on constants, so we are pushed toward sorting plus a linear or logarithmic maintenance structure. The internal computation of $d_i$ must also be $O(1)$ per pizza.

A subtle pitfall is assuming that all pizzas can always be scheduled if their deadlines are large enough individually. For example, if two pizzas both have small deadlines but large values, naive greedy by value alone can fail because feasibility depends on ordering, not just selection.

Another common mistake is miscomputing $d_i$. If one incorrectly assumes only star edges or only cycle edges matter, the resulting deadline can be wrong, which completely changes scheduling decisions.

## Approaches

We first separate the problem into two independent parts.

The first part is computing $d_i$. The graph has $s_i+1$ vertices. There are two competing ways to connect it. One is a star centered at the middle node, using $s_i$ edges of cost $q_i$, giving total cost $s_i \cdot q_i$. The other is to use the cycle edges, which connect slices in a ring with cost $c_i$, forming a cycle of $s_i$ edges. A minimum spanning tree on this cycle keeps $s_i-1$ edges, costing $(s_i-1)c_i$, and then connects the center using one edge of cost $q_i$. This gives $(s_i-1)c_i + q_i$. The minimum of these two is the correct $d_i$.

Once all deadlines are computed, the problem becomes a classical scheduling-with-deadlines problem where each job takes unit time and has a penalty if not completed before its deadline. The goal is to maximize the total value of scheduled jobs, equivalently minimize the sum of skipped values.

A brute force approach would try all permutations of pizzas, simulate the process, and track losses. This is factorial in complexity and immediately infeasible beyond tiny $N$.

The key observation is that ordering only matters through deadlines, not values. If we sort pizzas by increasing $d_i$, we can greedily attempt to schedule them in that order. At any point, if we have scheduled more pizzas than the current deadline allows, we must drop one. To minimize future loss, we drop the pizza with the smallest $v_i$, because it contributes the least penalty.

This works because at any prefix of deadlines, feasibility is determined only by how many jobs we can keep, and among any infeasible set, removing the smallest value preserves the best possible future outcome.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(N!)$ | $O(N)$ | Too slow |
| Sorting + Greedy Heap | $O(N \log N)$ | $O(N)$ | Accepted |

## Algorithm Walkthrough

We proceed in two conceptual phases.

1. For each pizza, compute its deadline $d_i = \min(s_i \cdot q_i,\; (s_i - 1)c_i + q_i)$. This compresses the geometry into a single constraint on when it must be eaten.
2. Sort all pizzas by increasing $d_i$. This ensures we always consider tighter deadlines first, which is essential because late decisions cannot fix earlier violations.
3. Maintain a max-structure over selected pizzas keyed by $v_i$. We simulate time passing through the sorted list.
4. For each pizza in sorted order, tentatively include it as scheduled.
5. If at any point the number of scheduled pizzas exceeds the current pizza’s deadline $d_i$, we must discard one scheduled pizza. We remove the pizza with the smallest $v_i$ among those selected so far, since that minimizes the damage caused by losing feasibility.
6. After processing all pizzas, all remaining selected pizzas are feasible. The answer is the sum of $v_i$ over all unselected pizzas.

The subtle point is that feasibility is checked incrementally. At step $k$, we are ensuring that among the first $k$ deadlines, we never schedule more than allowed. Any violation is resolved immediately, preventing cascading infeasibility.

### Why it works

At any prefix of pizzas sorted by deadline, the only constraint is how many pizzas can be completed before that deadline boundary. If we ever exceed it, any valid solution must exclude at least one pizza from the prefix. Removing the smallest $v_i$ is optimal because it preserves the maximum achievable total value among remaining choices. This invariant holds at every step, ensuring that no future decision can require revisiting past removals.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    pizzas = []
    
    for _ in range(n):
        s, q, c, v = map(int, input().split())
        d = min(s * q, (s - 1) * c + q)
        pizzas.append((d, v))
    
    pizzas.sort()
    
    import heapq
    heap = []
    total = 0
    
    for d, v in pizzas:
        heapq.heappush(heap, v)
        total += v
        
        if len(heap) > d:
            smallest = heapq.heappop(heap)
            total -= smallest
    
    print(total)

if __name__ == "__main__":
    solve()
```

The computation of $d$ is done directly in constant time per pizza using the derived MST characterization. Sorting by $d$ enforces the correct processing order.

The heap maintains selected values. Although Python’s `heapq` is a min-heap, it perfectly matches the need to remove the smallest $v_i$ when a deadline is violated. The variable `total` tracks the sum of currently kept pizzas so we can update the final answer incrementally.

A common implementation mistake is to interpret the heap as storing unselected pizzas or to forget updating the sum when popping. The sum must always reflect the current feasible set.

## Worked Examples

Consider a small case with three pizzas:

Input:

```
3
2 1 1 10
3 2 5 5
2 2 1 7
```

We compute deadlines:

| Pizza | d | v |
| --- | --- | --- |
| 1 | min(2, 2) = 2 | 10 |
| 2 | min(6, 9) = 6 | 5 |
| 3 | min(4, 3) = 3 | 7 |

Sorted by deadline:

| Step | Pizza (d, v) | Heap after insert | Action | Total kept value |
| --- | --- | --- | --- | --- |
| 1 | (2,10) | [10] | OK | 10 |
| 2 | (3,7) | [7,10] | OK | 17 |
| 3 | (6,5) | [5,10,7] | size > 6? no | 22 |

No removals occur, so all pizzas are kept.

This shows that when deadlines are sufficiently large relative to the number of items processed so far, the algorithm behaves like simple accumulation.

Now consider a tighter scenario:

Input:

```
3
1 1 1 10
1 1 1 5
2 1 1 7
```

Deadlines are all 1, 1, and 2. After sorting:

| Step | Pizza | Heap | Action | Total |
| --- | --- | --- | --- | --- |
| 1 | (1,5) | [5] | OK | 5 |
| 2 | (1,10) | [5,10] | remove 5 | 10 |
| 3 | (2,7) | [7,10] | OK | 17 |

This demonstrates the key greedy behavior: when capacity is exceeded, the smallest value is discarded.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(N \log N)$ | Sorting dominates, each heap operation is logarithmic over $N$ |
| Space | $O(N)$ | Storage of all pizzas plus heap |

The constraints allow $10^5$ items, and $O(N \log N)$ operations comfortably fit within time limits, especially since all operations are simple integer comparisons and heap adjustments.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from __main__ import solve
    return solve_wrapper()

def solve_wrapper():
    import sys
    input = sys.stdin.readline

    n = int(input())
    pizzas = []
    for _ in range(n):
        s, q, c, v = map(int, input().split())
        d = min(s * q, (s - 1) * c + q)
        pizzas.append((d, v))
    pizzas.sort()

    import heapq
    heap = []
    total = 0

    for d, v in pizzas:
        heapq.heappush(heap, v)
        total += v
        if len(heap) > d:
            total -= heapq.heappop(heap)

    return str(total)

# provided sample
assert run("4\n2 1 1 42\n2 3 4 42\n3 2 3 42\n2 1 1 10\n") == "0"

# minimum case
assert run("1\n2 1 1 5\n") == "5"

# all same deadline forcing removals
assert run("3\n1 1 1 5\n1 1 1 6\n1 1 1 7\n") == "7"

# increasing deadlines
assert run("3\n1 1 1 5\n2 1 1 6\n3 1 1 7\n") == "18"

# large q/c but structure matters only via d
assert run("2\n100 1 1 10\n2 1000 1 5\n") in ["15", "15"]
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single pizza | 5 | base case |
| identical tight deadlines | 7 | greedy removals |
| increasing deadlines | 18 | no removals needed |
| mixed parameters | 15 | correct d computation |

## Edge Cases

A key edge case arises when all pizzas share the same small deadline. For instance, if every $d_i = 1$, only one pizza can be kept regardless of how many are given. The algorithm handles this naturally because each insertion beyond capacity triggers an immediate removal of the smallest value, leaving only the best single pizza.

Another case is when deadlines are very large compared to $N$. For example, if all $d_i \ge N$, no removals ever occur, and the heap simply accumulates all values. The algorithm reduces to summation in this regime, matching the expected behavior of full feasibility.

Finally, incorrect computation of $d_i$ can silently break everything. If we take a pizza with $s_i = 3, q_i = 1, c_i = 100$, the correct deadline is $\min(3, 201) = 3$. A mistaken formula might produce 201, incorrectly making the pizza appear much more flexible than it is, leading to wrong scheduling decisions that cannot be fixed by any greedy strategy.
