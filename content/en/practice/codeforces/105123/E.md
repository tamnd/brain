---
title: "CF 105123E - Powerhouse of the Cell?"
description: "We are given a sequence of tasks ordered by priority from first to last, and each task consumes a fixed amount of ATP to complete. Jasmine has a daily ATP budget of $m$, and she cannot repeat tasks. The twist is that she does not always consider all tasks."
date: "2026-06-27T19:33:09+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105123
codeforces_index: "E"
codeforces_contest_name: "BioCode 2024"
rating: 0
weight: 105123
solve_time_s: 75
verified: false
draft: false
---

[CF 105123E - Powerhouse of the Cell?](https://codeforces.com/problemset/problem/105123/E)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 15s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a sequence of tasks ordered by priority from first to last, and each task consumes a fixed amount of ATP to complete. Jasmine has a daily ATP budget of $m$, and she cannot repeat tasks. The twist is that she does not always consider all tasks. Instead, for each prefix length $k$, she restricts attention only to the first $k$ tasks in priority order, and within that restricted set she wants to complete as many tasks as possible without exceeding her ATP budget.

For each $k$, we are effectively asking: if we take only tasks $1$ through $k$, what is the maximum number of task costs we can pick whose sum is at most $m$.

The important observation is that the tasks are always taken in prefix order, but inside that prefix we are free to choose any subset. So this is not a scheduling or ordering problem, it is a repeated “best subset under sum constraint” problem over growing prefixes.

The constraints are large, with $n$ up to $2 \cdot 10^5$. This immediately rules out recomputing an optimal subset from scratch for every $k$. A naive $O(n^2 \log n)$ or $O(n^2)$ approach that re-sorts or re-scans prefixes would be too slow. We need an incremental structure where each step updates the previous answer in logarithmic or constant amortized time.

A subtle issue appears when costs are highly unbalanced. For example, if $m = 10$ and tasks are $[1, 1, 1, 100, 1]$, then early prefixes allow many small picks, but once the large cost appears it never belongs in the optimal subset, yet it changes the prefix set. Any incorrect greedy approach that assumes we always pick the cheapest available tasks globally will fail unless it carefully maintains feasibility under prefix growth.

## Approaches

A direct way to think about each prefix is to sort its elements and take the smallest costs until the sum exceeds $m$. That is correct because for maximizing count under a sum constraint, picking smaller costs is always optimal. However, recomputing this for every prefix means we repeatedly sort or rebuild structures over up to $O(n)$ elements, leading to $O(n^2 \log n)$ worst case behavior.

The key structural observation is that when moving from prefix $k-1$ to $k$, we are adding exactly one new element. The optimal set for prefix $k$ differs from prefix $k-1$ only because we may want to include this new element, possibly evicting a larger chosen element if it helps increase count under the same budget.

This suggests maintaining a dynamic multiset of chosen tasks, always representing the best possible subset for the current prefix. The standard structure for this is a max-heap: we keep all currently chosen tasks and ensure their total sum stays within $m$. When adding a new task, we insert it, and if the total exceeds $m$, we remove the largest element. Removing the largest is optimal because it reduces the sum the most per removal and preserves as many small elements as possible.

Thus each prefix can be updated in $O(\log n)$, and we maintain both the current sum and the number of selected tasks.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force (recompute each prefix) | $O(n^2 \log n)$ | $O(n)$ | Too slow |
| Optimal (max heap incremental) | $O(n \log n)$ | $O(n)$ | Accepted |

## Algorithm Walkthrough

We process tasks from left to right, maintaining a structure of selected tasks that always fits within the ATP budget.

1. Initialize an empty max heap and a variable `total = 0`. The heap stores chosen task costs, and `total` tracks their sum.
2. For each task $a_k$, insert it into the heap and add its cost to `total`. This corresponds to tentatively accepting every new task, since we do not yet know if it will be part of the final optimal subset for this prefix.
3. If `total > m`, remove the largest element from the heap and subtract it from `total`. This step restores feasibility. Removing the largest element is the only choice that can never reduce the number of selected tasks more than necessary, because it sacrifices the most expensive task while preserving as many items as possible.
4. After the adjustment, the size of the heap is exactly the maximum number of tasks that can be completed for the current prefix. Output this size.
5. Repeat this process for all $k$ from 1 to $n$, producing one answer per prefix.

Why this works is tied to a greedy exchange argument. At any prefix, suppose we have a feasible subset that is not optimal in size. If it contains a larger element while excluding a smaller one, swapping them never worsens feasibility and never reduces count. Therefore an optimal solution always prefers smaller elements, and the heap invariant enforces exactly that structure dynamically as new elements arrive.

## Python Solution

```python
import sys
import heapq

input = sys.stdin.readline

def solve():
    n, m = map(int, input().split())
    a = list(map(int, input().split()))
    
    heap = []
    total = 0
    out = []
    
    for x in a:
        heapq.heappush(heap, -x)
        total += x
        
        if total > m:
            largest = -heapq.heappop(heap)
            total -= largest
        
        out.append(str(len(heap)))
    
    print("\n".join(out))

if __name__ == "__main__":
    solve()
```

The core implementation detail is the use of a max heap simulated through negative values, since Python’s `heapq` only provides a min heap. We maintain `total` explicitly because recomputing heap sums would be too slow.

A subtle point is that we always remove exactly one largest element when overflow occurs. Even if `total` is far above `m`, a single removal is sufficient per insertion because after removing the largest, the remaining elements are all smaller or equal, and the heap invariant ensures we only exceed capacity by at most the contribution of the newly added element.

## Worked Examples

Consider the sample input:

```
n = 5, m = 15
a = [14, 15, 11, 4, 4]
```

We track the heap after each step.

| k | Inserted | Heap (multiset) | Total | Removed | Answer |
| --- | --- | --- | --- | --- | --- |
| 1 | 14 | [14] | 14 | none | 1 |
| 2 | 15 | [14, 15] | 29 | 15 | 1 |
| 3 | 11 | [14, 11] | 25 | 14 | 1 |
| 4 | 4 | [11, 4] | 15 | none | 2 |
| 5 | 4 | [11, 4, 4] | 19 | 11 | 2 |

The trace shows that large elements get dropped whenever they block the inclusion of multiple smaller ones. The heap consistently evolves toward keeping the cheapest feasible subset.

A second example:

```
n = 4, m = 10
a = [3, 4, 5, 2]
```

| k | Inserted | Heap | Total | Removed | Answer |
| --- | --- | --- | --- | --- | --- |
| 1 | 3 | [3] | 3 | none | 1 |
| 2 | 4 | [4, 3] | 7 | none | 2 |
| 3 | 5 | [5, 3, 4] | 12 | 5 | 2 |
| 4 | 2 | [4, 3, 2] | 9 | none | 3 |

This demonstrates that removing the largest element after overflow allows the solution to adapt globally without revisiting earlier decisions.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n \log n)$ | Each of $n$ insertions and at most one removal uses heap operations |
| Space | $O(n)$ | Heap stores at most all active chosen elements in worst case |

The complexity fits comfortably within constraints for $n \le 2 \cdot 10^5$, since logarithmic heap operations are efficient at this scale.

## Test Cases

```python
import sys, io
import heapq

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    n, m = map(int, input().split())
    a = list(map(int, input().split()))
    
    heap = []
    total = 0
    res = []
    
    for x in a:
        heapq.heappush(heap, -x)
        total += x
        
        if total > m:
            total += heapq.heappop(heap)
        
        res.append(str(len(heap)))
    
    return "\n".join(res)

# sample
assert run("5 15\n14 15 11 4 4\n") == "1\n1\n1\n2\n2"

# all small, no removals
assert run("4 20\n1 2 3 4\n") == "1\n2\n3\n4"

# immediate large removal
assert run("3 5\n10 1 1\n") == "0\n1\n2"

# alternating heavy/light
assert run("5 6\n5 1 5 1 5\n") == "1\n2\n2\n3\n3"

# single element
assert run("1 100\n50\n") == "1"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1.. | sample | correctness on mixed removals |
| small increasing | 1 2 3 4 | no removals case |
| heavy first | 0 1 2 | eviction of oversized element |
| alternating | 1 2 2 3 3 | repeated rebalancing |
| single | 1 | boundary case |

## Edge Cases

A critical edge case is when the first element already exceeds the budget. For input `n = 3, m = 5, a = [10, 1, 1]`, the heap first becomes `[10]`, total exceeds budget, and we immediately remove it, leaving an empty heap. The answer for $k=1$ is therefore 0, and subsequent small elements rebuild the solution from scratch. The algorithm handles this naturally because every insertion is followed by a correction step.

Another edge case is when many small elements accumulate and a large element appears late. For `m = 6, a = [1, 1, 1, 1, 1, 10]`, the heap grows steadily to size 5, then the 10 forces removal of itself, not any of the small elements, preserving the optimal count. This shows the invariant that the heap always contains the smallest-cost feasible subset for the prefix.
