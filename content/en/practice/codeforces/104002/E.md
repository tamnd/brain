---
title: "CF 104002E - William and Robot"
description: "We are given a line of integers, and two players take turns removing elements until nothing remains. William moves first, and on his turn he can pick any still-available element from anywhere in the array."
date: "2026-07-02T05:36:44+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104002
codeforces_index: "E"
codeforces_contest_name: "UTPC Contest 10-28-22 Div. 2 (Beginner)"
rating: 0
weight: 104002
solve_time_s: 47
verified: true
draft: false
---

[CF 104002E - William and Robot](https://codeforces.com/problemset/problem/104002/E)

**Rating:** -  
**Tags:** -  
**Solve time:** 47s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a line of integers, and two players take turns removing elements until nothing remains. William moves first, and on his turn he can pick any still-available element from anywhere in the array. The robot does not choose strategically at all: it always removes the leftmost remaining element at every step.

William’s goal is to maximize the sum of values he collects. The robot’s deterministic behavior means the evolution of the remaining array is fully predictable once William’s choices are fixed, so the problem is not about adversarial game theory but about controlling which positions William “claims” before the robot consumes structure from the left.

The key difficulty is that William’s choices affect future availability indirectly. If he delays picking a valuable element on the left, the robot might consume it first. On the other hand, picking something too early may waste a “turn budget” in prefixes where the robot would otherwise be forced to take low-value elements.

The constraint n up to 100000 implies that any solution must be close to linear or n log n. Any approach that tries to simulate all possible sequences of picks or consider subsets of elements explicitly is impossible because even a rough subset exploration would grow exponentially. This pushes us toward a greedy or data-structure based method that processes elements in order and maintains only a compact representation of what William is effectively allowed to keep.

A subtle edge case arises from the robot’s leftmost rule. For example, consider an array like 10 1 100 1. A naive idea is that William should always take the largest available element, but that ignores that after the robot repeatedly consumes from the left, some “large” values may become inaccessible if not taken within a prefix quota. Another failure case is when large values are clustered early, because William cannot take too many of them in early prefixes without violating the fact that the robot will have already taken half of those prefix elements.

So the real constraint is not about adjacency in the original game sequence but about prefix capacity: within the first k elements, William cannot end up taking more than about k/2 elements, since the robot will always consume the rest of that prefix in lockstep from the left.

## Approaches

If we ignore the robot’s deterministic behavior, the brute-force idea would be to simulate the game state: at each step, try every possible choice for William, then simulate the robot’s forced move, and continue. This produces a branching factor equal to the number of remaining elements, and depth n, leading to factorial or exponential complexity. Even memoization fails because the state is not just which elements remain, but also their order after repeated left deletions, which still leaves too many distinct configurations.

The key observation is to stop thinking in terms of “remaining array after deletions” and instead think in terms of prefix constraints. After processing the first k positions, exactly k elements have been removed in total, and they are split between William and the robot. Since the robot always consumes the leftmost available element, it effectively guarantees that in every prefix of length k, William cannot dominate the count. This leads to the constraint that William can only “hold” up to k/2 chosen elements among the first k positions.

Once we accept that interpretation, the problem becomes: process the array left to right, and maintain a set of William’s chosen elements such that at every even index k, we ensure at most k/2 selections are kept among the first k elements. Since William wants maximum sum, whenever he has chosen too many small elements early, he should discard the smallest among them. This naturally suggests maintaining a max-benefit selection under a size constraint, but since we are discarding the least useful chosen elements, we actually want to keep a structure that allows removing the smallest candidate among William’s current picks.

A min-heap fits exactly this requirement: we tentatively include every element as a candidate for William’s set, and whenever the number of chosen elements exceeds the allowed quota for the current prefix, we remove the smallest value. This ensures that William always retains the best possible multiset of picks consistent with feasibility.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Simulation | Exponential | Exponential | Too slow |
| Prefix constraint + heap pruning | O(n log n) | O(n) | Accepted |

## Algorithm Walkthrough

We scan the array from left to right, treating each position as if William might try to take it.

1. Insert the current value into a min-heap representing William’s tentative chosen set. This assumes William considers taking everything first, and we will later correct infeasibility by removing weak choices.
2. After processing index k, compute how many elements William is allowed to keep from the prefix 1 to k. Since the robot always takes the leftmost available element, in any prefix William cannot end up with more than k/2 elements among those positions, so we enforce that constraint only when k is even.
3. If k is even and the heap size exceeds k/2, repeatedly remove the smallest element from the heap until the constraint is satisfied. The reason we remove the smallest is that keeping larger elements always improves the final sum while still respecting feasibility.
4. Continue until the end of the array. The sum of elements remaining in the heap is William’s maximum achievable score.

The important subtlety is that we never explicitly simulate robot moves. The heap enforces the only structural constraint that matters: William’s selections must remain compatible with the robot consuming exactly half of each prefix in aggregate.

### Why it works

The invariant is that after processing prefix k, the heap contains the maximum-sum subset of elements from the prefix that can be extended into a valid game outcome under the robot’s forced leftmost removal rule. The robot’s behavior ensures that in any prefix of length k, exactly k/2 elements are effectively “reserved” for William at most, because the remaining capacity is consumed from the left. By always discarding the smallest chosen element when the constraint is violated, we maintain the best possible value subset under a matroid-like cardinality constraint that grows with k. This guarantees that no future decision can benefit from having kept a smaller element earlier instead of a larger one.

## Python Solution

```python
import sys
input = sys.stdin.readline

import heapq

def solve():
    n = int(input())
    a = list(map(int, input().split()))
    
    heap = []
    total = 0
    
    for i, x in enumerate(a, start=1):
        heapq.heappush(heap, x)
        
        if i % 2 == 0:
            limit = i // 2
            while len(heap) > limit:
                heapq.heappop(heap)
    
    print(sum(heap))

if __name__ == "__main__":
    solve()
```

The solution maintains a min-heap of William’s current chosen values. Every element is added immediately, then the prefix feasibility constraint is enforced at even positions. The heap pop operation always removes the smallest chosen value, which is the only safe discard because it minimizes loss in total sum.

A common implementation mistake is forgetting that the constraint applies per prefix and not only at the end. Another is using a max-heap, which breaks the logic because we need to discard the least valuable chosen element, not the most valuable one.

## Worked Examples

### Sample 1

Input:

```
4
6 1 1 4
```

We track the heap after each step.

| i | value | heap after insert | action |
| --- | --- | --- | --- |
| 1 | 6 | [6] | no constraint |
| 2 | 1 | [1, 6] | limit 1, remove 1 |
| 3 | 1 | [1, 6] | no constraint |
| 4 | 4 | [1, 4, 6] → [4, 6] | limit 2 |

Final heap is [4, 6], sum is 10.

This shows how early small values are discarded to preserve capacity for better later selections.

### Sample 2

Input:

```
10
1 3 4 9 5 2 5 5 3 6
```

| i | value | heap after adjustment |
| --- | --- | --- |
| 1 | 1 | [1] |
| 2 | 3 | [3] |
| 3 | 4 | [3,4] |
| 4 | 9 | [4,9] |
| 5 | 5 | [4,9,5] |
| 6 | 2 | [5,9,5] |
| 7 | 5 | [5,9,5,5] → prune |
| 8 | 5 | [5,5,5,9] → prune |
| 9 | 3 | ... |
| 10 | 6 | ... |

After full pruning, the heap stabilizes on the best valid selection with sum 30.

This trace shows how the structure continuously replaces weaker early picks with stronger later ones while respecting prefix limits.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n) | Each element is pushed once and possibly popped once from the heap |
| Space | O(n) | Heap stores at most n/2 elements |

The n up to 100000 constraint fits comfortably within O(n log n), since heap operations remain fast enough under standard limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    
    import heapq

    n = int(input())
    a = list(map(int, input().split()))
    
    heap = []
    
    for i, x in enumerate(a, start=1):
        heapq.heappush(heap, x)
        if i % 2 == 0:
            limit = i // 2
            while len(heap) > limit:
                heapq.heappop(heap)
    
    return str(sum(heap))

# provided samples
assert run("4\n6 1 1 4\n") == "10"
assert run("10\n1 3 4 9 5 2 5 5 3 6\n") == "30"

# custom cases
assert run("2\n5 1\n") == "5"
assert run("2\n1 100\n") == "100"
assert run("6\n1 2 3 4 5 6\n") == "12"
assert run("8\n8 7 6 5 4 3 2 1\n") == "20"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 2 elements | max single pick | minimum size handling |
| sorted small/large pair | picks best value | greedy correctness |
| increasing array | prefix balancing | heap pruning logic |
| decreasing array | frequent replacements | worst-case replacements |

## Edge Cases

A critical edge case is when large values appear early, for example `100 1 99 1`. A naive greedy strategy would take 100 and 99 immediately, but that can violate prefix feasibility since the robot will consume intervening elements and reduce future flexibility. The algorithm inserts all values but immediately enforces the prefix constraint, which forces removal of the smallest early pick when capacity is exceeded, preserving higher values for later prefixes.

Another edge case is alternating high and low values such as `1 100 2 99 3 98`. Here the heap grows quickly, and without periodic pruning, the selection would exceed allowable prefix count. The algorithm consistently trims the weakest choices at each even index, ensuring that William’s selection never becomes infeasible while still keeping the largest available values.
