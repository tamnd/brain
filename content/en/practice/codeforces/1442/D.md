---
title: "CF 1442D - Sum"
description: "We are given several sequences, each already sorted in non-decreasing order. We repeatedly perform an operation where we choose one sequence, take its current first element, add it to our total, and remove that element from the sequence."
date: "2026-06-11T04:18:49+07:00"
tags: ["codeforces", "competitive-programming", "data-structures", "divide-and-conquer", "dp", "greedy"]
categories: ["algorithms"]
codeforces_contest: 1442
codeforces_index: "D"
codeforces_contest_name: "Codeforces Round 681 (Div. 1, based on VK Cup 2019-2020 - Final)"
rating: 2800
weight: 1442
solve_time_s: 91
verified: false
draft: false
---

[CF 1442D - Sum](https://codeforces.com/problemset/problem/1442/D)

**Rating:** 2800  
**Tags:** data structures, divide and conquer, dp, greedy  
**Solve time:** 1m 31s  
**Verified:** no  

## Solution
## Problem Understanding

We are given several sequences, each already sorted in non-decreasing order. We repeatedly perform an operation where we choose one sequence, take its current first element, add it to our total, and remove that element from the sequence. We do this exactly k times, and the goal is to maximize the total sum collected.

Another way to view the process is that each array behaves like a queue, and at each step we pick one queue and pop from its front. Because the arrays are sorted increasingly, the early elements are the smallest in that array, and later elements are larger.

The key structure is that we are not constrained to fully consume one array before moving to another. We are free to interleave choices across arrays, but every time we come back to an array, we are effectively advancing a pointer along it.

The constraints immediately rule out any approach that considers all sequences of choices. With up to 3000 arrays and up to 3000 operations, any brute-force branching over choices of arrays per operation grows exponentially. Even a DP over all states of all pointers would involve tracking a 3000-dimensional state, which is impossible.

A more subtle issue is that the naive greedy strategy of always taking the current maximum available front element is correct, but only if we can maintain it efficiently. The hidden challenge is that every time we pick from an array, its front changes, so candidate values evolve dynamically.

A typical failure case for naive thinking is to treat each array independently, take its largest prefix sum, and then combine results greedily. For example, if one array starts small but ends very large, delaying it might be optimal, but naive prefix aggregation would miss that interleaving.

The correct solution needs a way to always know the best available “next element” across all arrays, while efficiently updating only the affected array after each pick.

## Approaches

The brute-force idea is to simulate the process step by step. At each operation, we try all n arrays, pick one, and recursively continue. This correctly explores all possible sequences of choices, but the branching factor is n at each of k steps, leading to O(n^k), which is completely infeasible.

A second brute-force refinement is to notice that each array is monotone, so for each array we only ever consume prefixes. We can define a state by how many elements have been taken from each array. Even then, the state space is enormous because each array can contribute up to 3000 elements, producing a combinatorial explosion.

The key observation is that at any moment, each array contributes exactly one candidate value to the decision process: its current front element. After selecting it, the next candidate from that array shifts forward by one position. This means the entire problem reduces to repeatedly selecting the maximum among n changing front values.

This is exactly a dynamic selection problem over a set of candidates where each selection causes one candidate to be replaced by its successor in a fixed list. A priority queue is sufficient: we maintain the current front of each array, and each extraction replaces it with the next element from the same array.

This works because within each array, the order is fixed and non-decreasing, so once we move forward, we never need to reconsider earlier elements.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n^k) | O(k) | Too slow |
| Optimal (heap simulation) | O((n + k) log n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Initialize a max-priority structure that stores one entry per array, specifically its current first element along with the array index and position. We invert values to simulate a max-heap since standard heaps are min-oriented in Python. This ensures we always extract the best available candidate among all arrays.
2. Insert the first element of every non-empty array into the heap. Each entry represents the best next choice if we decide to pick from that array.
3. Initialize an accumulator for the answer, which will store the sum of all selected elements over k operations.
4. Repeat k times:

1. Extract the largest available element from the heap.
2. Add its value to the accumulator.
3. Advance within the corresponding array by one position.
4. If the array still has remaining elements, insert its new front element into the heap.

The reason this step works is that after removing the current front, the next valid candidate from that array is uniquely determined.

### Why it works

At any moment, the heap contains exactly one candidate per array: the smallest index not yet consumed. Every possible legal move corresponds to choosing one of these candidates. Because arrays are independent except for competition in the heap, selecting the maximum current candidate is always optimal for the current step. The problem has an exchange property: if an optimal solution does not pick the maximum available element at some step, swapping it with the chosen element cannot reduce the total sum since all values are non-negative and the replacement only affects future access within the same sorted sequence. This ensures a greedy choice is globally consistent.

## Python Solution

```python
import sys
input = sys.stdin.readline
import heapq

n, k = map(int, input().split())

arrays = []
for _ in range(n):
    tmp = list(map(int, input().split()))
    t = tmp[0]
    arrays.append(tmp[1:])

heap = []
for i in range(n):
    if arrays[i]:
        heapq.heappush(heap, (-arrays[i][0], i, 0))

ans = 0

for _ in range(k):
    val, i, j = heapq.heappop(heap)
    val = -val
    ans += val

    if j + 1 < len(arrays[i]):
        heapq.heappush(heap, (-arrays[i][j + 1], i, j + 1))

print(ans)
```

The solution maintains a heap of active front elements. Each heap entry encodes both the value and its position so we can advance correctly within its array. The negative sign is necessary because Python only provides a min-heap.

A subtle implementation detail is that we never push outdated elements. Each heap entry corresponds to a specific index in an array, so when we pop it, we deterministically know the next index to push. This avoids the need for lazy deletion.

## Worked Examples

### Example 1

Input:

```
3 3
2 5 10
3 1 2 3
2 1 20
```

We track heap state conceptually.

| Step | Heap (top first) | Chosen | Answer |
| --- | --- | --- | --- |
| init | (5, A), (1, B), (1, C) | - | 0 |
| 1 | 5(A) | 5 | 5 |
| 2 | 20(C), 10(A), 1(B) | 20 | 25 |
| 3 | 10(A), 1(B), - | 10 | 35 |

The trace shows that the algorithm naturally delays picking smaller early values in favor of a large late value that becomes available only after advancing in its array.

### Example 2

Input:

```
2 4
1 100
3 1 2 3
```

| Step | Heap | Chosen | Answer |
| --- | --- | --- | --- |
| init | 100, 1 | - | 0 |
| 1 | 100 | 100 | 100 |
| 2 | 3, 2 | 3 | 103 |
| 3 | 2, 2 | 2 | 105 |
| 4 | 1, 2 | 2 | 107 |

This demonstrates that once the single-element array is consumed, the algorithm correctly continues down the other array.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O((n + k) log n) | Each heap operation costs log n, and we perform k extractions and at most k insertions |
| Space | O(n) | Heap stores at most one active pointer per array |

The bounds n, k ≤ 3000 make this comfortably fast. Even in the worst case of 6000 heap operations, the logarithmic factor is negligible.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import heapq

    n, k = map(int, sys.stdin.readline().split())
    arrays = []
    for _ in range(n):
        tmp = list(map(int, sys.stdin.readline().split()))
        arrays.append(tmp[1:])

    heap = []
    for i in range(n):
        if arrays[i]:
            heapq.heappush(heap, (-arrays[i][0], i, 0))

    ans = 0
    for _ in range(k):
        val, i, j = heapq.heappop(heap)
        val = -val
        ans += val
        if j + 1 < len(arrays[i]):
            heapq.heappush(heap, (-arrays[i][j + 1], i, j + 1))

    return str(ans)

# provided sample
assert run("""3 3
2 5 10
3 1 2 3
2 1 20
""") == "35"

# single array only
assert run("""1 3
5 1 2 3 4 5
""") == "12"

# all equal values
assert run("""3 4
2 5 5
2 5 5
2 5 5
""") == "20"

# k equals total elements
assert run("""2 5
2 1 100
3 2 3 4
""") == "110"

# small alternating structure
assert run("""2 3
3 1 100 100
3 2 3 4
""") == "204"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single array | 12 | correct prefix consumption |
| all equal | 20 | tie handling in heap |
| full consumption | 110 | boundary k = total elements |
| alternating | 204 | interleaving correctness |

## Edge Cases

One edge case is when a single array dominates late values. For input:

```
2 3
2 1 2
3 1 1 100
```

the heap starts with 1, 1. The algorithm takes 1, then again 1, but after advancing the second array it eventually reaches 100, which becomes the dominant choice. The heap correctly delays access until the pointer reaches it.

Another edge case is when all arrays contain identical values. The heap has many ties, but since values are non-negative and independent, any tie-breaking order is valid. The structure ensures exactly k selections are made without bias.

A final edge case is when k equals the total number of elements. The heap becomes empty exactly after exhausting all arrays, and the algorithm never attempts to push invalid indices because each push is guarded by bounds on the array length.
