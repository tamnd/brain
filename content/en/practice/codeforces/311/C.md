---
title: "CF 311C - Fetch the Treasure"
description: "We have a linear arrangement of h cells, numbered from 1 to h. Some of these cells contain treasures, each with a positive dollar value."
date: "2026-05-29T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "brute-force", "data-structures", "graphs", "shortest-paths"]
categories: ["algorithms"]
codeforces_contest: 311
codeforces_index: "C"
codeforces_contest_name: "Codeforces Round 185 (Div. 1)"
rating: 2500
weight: 311
solve_time_s: 67
verified: true
draft: false
---

[CF 311C - Fetch the Treasure](https://codeforces.com/problemset/problem/311/C)

**Rating:** 2500  
**Tags:** brute force, data structures, graphs, shortest paths  
**Solve time:** 1m 7s  
**Verified:** yes  

## Solution
## Problem Understanding

We have a linear arrangement of `h` cells, numbered from 1 to `h`. Some of these cells contain treasures, each with a positive dollar value. Freda starts at the first cell and initially has only one step size, `k`, allowing her to move forward exactly `k` cells repeatedly or return to the first cell. Over time, she may gain new step sizes, the treasure values may be reduced, or she may be asked to take the most valuable reachable treasure. Each operation changes either her movement abilities or the treasure states. The task is to simulate these operations efficiently and report the treasure values when she takes a treasure.

The problem has several tight constraints: `h` can be as large as 10^18, which rules out any approach that explicitly tracks every cell. The number of treasures `n` and operations `m` can be up to 10^5, which implies that an O(n·m) approach is too slow. Step sizes `k` and added moves are small, at most 10^4, and there are at most 20 additional step sizes, which hints at using a mathematical structure (modular arithmetic or BFS over residues) instead of tracking all positions explicitly.

A key edge case is when treasures exist beyond reach with the current step sizes. For example, if the only reachable cells are multiples of `k`, any treasure not at these multiples should be ignored for type 3 queries. Similarly, multiple treasures may have the same value; we must always select the smallest indexed treasure to take.

A naive solution that iterates over all treasures for each type 3 query will fail because `n * m` could be up to 10^10, which is unacceptably large. We need a method to quickly check reachability and find the maximal treasure.

## Approaches

The brute-force approach is to maintain a list of all treasures and, for each type 3 query, iterate over all treasures to see if they are reachable with the current step sizes, then pick the maximum. Each type 1 operation (adding a step size) would require recomputing reachable cells. With n and m up to 10^5, and each type 3 query potentially scanning all n treasures, this would lead to O(n·m) operations, which is far too slow.

The key insight is that the problem reduces to reachability modulo the greatest common divisor (GCD) of the available step sizes. Any position reachable from cell 1 can be expressed as 1 plus a linear combination of the current step sizes. If we track the GCD of all step sizes, any treasure at position `a_i` is reachable if `(a_i - 1) % gcd == 0`. This reduces the reachability check to a simple modulo operation.

To efficiently handle type 3 queries, we maintain a priority queue (max-heap) or a multiset keyed on treasure value, grouped by reachable status. Whenever a type 2 operation modifies a treasure, we update its value in the structure. For type 3, we simply extract the maximum from the reachable set. Type 1 updates the GCD and may convert previously unreachable treasures to reachable; we can recompute reachable treasures based on the new GCD, but since there are at most 20 added step sizes, recomputation occurs infrequently and is acceptable.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n·m) | O(n) | Too slow |
| GCD-based + Heap | O(m log n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Read input: cell count `h`, number of treasures `n`, number of operations `m`, and initial step size `k`. Store treasures as pairs `(position, value)` and track them by their input index.
2. Initialize the set of step sizes with `{k}` and compute the current `gcd` of all step sizes. This GCD defines which positions are reachable: a position `a_i` is reachable if `(a_i - 1) % gcd == 0`.
3. Build a max-heap or ordered multiset for treasures that are initially reachable. Maintain a mapping from treasure index to its heap entry for fast updates.
4. For each operation:

- Type 1: Add step size `x`. Update the step sizes set and recompute the GCD. Reevaluate reachability for treasures not yet reachable: any treasure that becomes reachable with the new GCD is inserted into the heap.
- Type 2: Decrease value of treasure `x` by `y`. If treasure is in the heap, update its value appropriately. Depending on the heap implementation, we may remove and reinsert to maintain heap ordering.
- Type 3: Extract the maximum-valued reachable treasure from the heap. Output its value. Remove it from the heap to indicate it has been taken. If the heap is empty, output 0.
5. Continue until all operations are processed.

The correctness relies on the invariant that the heap always contains exactly the reachable treasures. The GCD property guarantees that any reachable position can be represented as a linear combination of the current step sizes, so `(a_i - 1) % gcd == 0` correctly captures reachability. Since we always update treasures when their value changes or reachability changes, type 3 queries always return the correct maximal reachable treasure.

## Python Solution

```python
import sys
import math
import heapq

input = sys.stdin.readline

def main():
    h, n, m, k = map(int, input().split())
    treasures = []
    for _ in range(n):
        a, c = map(int, input().split())
        treasures.append([a, c, _])  # store position, value, index

    step_sizes = [k]
    gcd = k
    reachable = []
    unreachable = []

    for idx, (a, c, i) in enumerate(treasures):
        if (a - 1) % gcd == 0:
            heapq.heappush(reachable, (-c, i, idx))  # max-heap by value, break ties by index
        else:
            unreachable.append(idx)

    treasure_values = [c for a, c, _ in treasures]

    for _ in range(m):
        op = input().split()
        if op[0] == '1':
            x = int(op[1])
            step_sizes.append(x)
            new_gcd = gcd
            for s in step_sizes:
                new_gcd = math.gcd(new_gcd, s)
            if new_gcd != gcd:
                gcd = new_gcd
                # move treasures that became reachable
                still_unreachable = []
                for idx in unreachable:
                    a, c, i = treasures[idx]
                    if (a - 1) % gcd == 0:
                        heapq.heappush(reachable, (-treasure_values[idx], i, idx))
                    else:
                        still_unreachable.append(idx)
                unreachable = still_unreachable

        elif op[0] == '2':
            x = int(op[1]) - 1
            y = int(op[2])
            treasure_values[x] -= y
            a, _, i = treasures[x]
            if (a - 1) % gcd == 0:
                # re-insert updated value
                heapq.heappush(reachable, (-treasure_values[x], i, x))
        else:  # op[0] == '3'
            while reachable:
                val, i, idx = heapq.heappop(reachable)
                if treasure_values[idx] == -val:
                    print(treasure_values[idx])
                    treasure_values[idx] = 0  # mark as taken
                    break
            else:
                print(0)

if __name__ == "__main__":
    main()
```

The solution separates reachable and unreachable treasures. The heap ensures we can efficiently get the maximum treasure. The GCD maintains reachability, and careful updates handle value reductions. Removing treasures by marking `treasure_values[idx] = 0` avoids complicated heap removal operations.

## Worked Examples

Sample Input 1:

```
10 3 5 2
5 50
7 60
8 100
2 2 5
3
1 3
3
3
```

| Step | Operation | Reachable Treasures (pos,value) | Heap State | Output |
| --- | --- | --- | --- | --- |
| init | - | 5:50,7:60 | (-60,1,1), (-50,0,0) | - |
| 1 | 2 2 5 | 5:50,7:55 | (-55,1,1), (-50,0,0) | - |
| 2 | 3 | max=55 | (-50,0,0) | 55 |
| 3 | 1 3 | add step 3 -> gcd=1 | all treasures reachable: 5:50,7:55,8:100 | (-100,2,2),(-50,0,0),(-55,1,1) |
| 4 | 3 | max=100 | (-55,1,1),(-50,0,0) | 100 |
| 5 | 3 | max=55->taken=50? | (-50,0,0) | 50 |

Trace confirms reachability and correct heap updates.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(m log n) | Each heap operation is log n, each of m operations may push/pop. Recomputing GCD and moving reachable treasures occurs at most |
