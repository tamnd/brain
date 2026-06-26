---
title: "CF 105728H - The Revolving Death Clock"
description: "The task can be understood as simulating a process on a circular arrangement of positions, where a pointer moves around like the hand of a clock and repeatedly removes elements according to a fixed rule until only one position remains."
date: "2026-06-26T07:50:12+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105728
codeforces_index: "H"
codeforces_contest_name: "EPT Solving Cup 5.0 \uacf5\uc2dd \uacbd\uc5f0\ub300\ud68c"
rating: 0
weight: 105728
solve_time_s: 48
verified: true
draft: false
---

[CF 105728H - The Revolving Death Clock](https://codeforces.com/problemset/problem/105728/H)

**Rating:** -  
**Tags:** -  
**Solve time:** 48s  
**Verified:** yes  

## Solution
## Problem Understanding

The task can be understood as simulating a process on a circular arrangement of positions, where a pointer moves around like the hand of a clock and repeatedly removes elements according to a fixed rule until only one position remains. Each position represents a participant arranged in a circle, and the process advances in a fixed step size that wraps around the circle repeatedly. Whenever the pointer lands on a position that has not been removed yet, that position is eliminated, and the process continues from the next available position.

The input describes the size of the circle and the step size that determines how far the pointer moves between eliminations. The output is the label of the final surviving position after all eliminations are performed.

From a complexity perspective, a direct simulation would require maintaining a dynamically shrinking circular structure and advancing a pointer repeatedly over it. With up to large values of n, potentially on the order of 10^5 or more, any approach that repeatedly scans or shifts elements inside a list would degrade to quadratic behavior. This immediately rules out naive array deletion or repeated traversal over the full structure.

A subtle edge case appears when the step size is 1. In that situation, every element is removed in order, and the last element in the initial arrangement is always the answer. Another edge case arises when the step size is larger than the current number of remaining elements, where naive modulo handling can easily go wrong if indexing is not carefully normalized to the reduced circle size. For example, with n = 5 and k = 7, the elimination should still behave as if k = 7 mod 5 in the current state, but careless implementations often mis-handle the wrap-around and skip incorrect positions.

## Approaches

A brute-force simulation keeps all positions in a list or deque and repeatedly advances a pointer k steps forward, removes the current element, and continues. Each removal requires either shifting elements or iterating through already removed positions. Even with a linked list or deque, the repeated traversal of k steps for each of n removals leads to O(nk) behavior. In the worst case where k is comparable to n, this degenerates into O(n^2), which is too slow for large inputs.

The key observation is that after each elimination, the problem reduces to the same structure but with one fewer element, and the relative indexing of survivors shifts in a predictable way. Instead of explicitly simulating the circle, we can track the position of the survivor in a shrinking array using a recurrence relation. If we define f(i) as the winning position in a circle of size i, then moving from size i - 1 to i shifts indices forward by the step size and wraps around modulo i. This eliminates the need for any explicit data structure and reduces the process to a simple linear recurrence.

The brute-force works because it directly mimics the process, but fails when the number of operations grows large due to repeated traversal and deletion. The observation that only the relative position of the survivor matters allows us to compress the entire process into a single pass over n states.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Simulation | O(n^2) | O(n) | Too slow |
| Recurrence (Josephus DP) | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

We define a function that tracks the survivor index as the circle grows from size 1 to size n.

1. Start with a single element circle. The survivor is trivially position 0 in 0-indexed form. This acts as the base state because no eliminations are possible.
2. Increase the circle size from 2 up to n, and for each size i, update the survivor position using the recurrence relation. At each step, we simulate how the previous solution shifts when a new element is added.
3. The update rule is: the new survivor position becomes `(previous_position + k) % i`. This reflects the fact that the elimination pointer advances k steps and wraps around the current circle size i.
4. After iterating through all sizes up to n, convert the final 0-indexed position to 1-indexed form for output.

The reason this works is that each expansion step preserves the structure of the elimination process, and the recurrence correctly models how the indexing shifts when the circle size increases. The elimination order is invariant under this transformation because every configuration of size i builds consistently on the solution for size i - 1.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, k = map(int, input().split())
    
    # josephus recurrence
    res = 0
    for i in range(1, n + 1):
        res = (res + k) % i
    
    print(res + 1)

if __name__ == "__main__":
    solve()
```

The implementation keeps only a single integer state, `res`, which represents the survivor index in a 0-indexed system. Each iteration expands the circle size and applies the modular shift that corresponds to one elimination round. The final conversion to 1-indexed output is necessary because the problem labels positions starting from 1 rather than 0.

A common implementation pitfall is forgetting that the modulo must be taken with respect to the current size `i`, not the final size `n`. Another subtle issue is mixing 0-indexed and 1-indexed reasoning inside the loop, which leads to off-by-one errors that only show up for small inputs.

## Worked Examples

Consider an input where n = 5 and k = 2. We track the survivor index as the circle grows.

| i | previous res | computation | new res |
| --- | --- | --- | --- |
| 1 | 0 | (0 + 2) % 1 = 0 | 0 |
| 2 | 0 | (0 + 2) % 2 = 0 | 0 |
| 3 | 0 | (0 + 2) % 3 = 2 | 2 |
| 4 | 2 | (2 + 2) % 4 = 0 | 0 |
| 5 | 0 | (0 + 2) % 5 = 2 | 2 |

The final answer is 3 in 1-indexed form. This trace shows how the recurrence naturally shifts the survivor as the circle expands.

Now consider n = 6, k = 3.

| i | previous res | computation | new res |
| --- | --- | --- | --- |
| 1 | 0 | (0 + 3) % 1 = 0 | 0 |
| 2 | 0 | (0 + 3) % 2 = 1 | 1 |
| 3 | 1 | (1 + 3) % 3 = 1 | 1 |
| 4 | 1 | (1 + 3) % 4 = 0 | 0 |
| 5 | 0 | (0 + 3) % 5 = 3 | 3 |
| 6 | 3 | (3 + 3) % 6 = 0 | 0 |

The final answer is 1. This demonstrates how periodic resets occur when the step size aligns with intermediate circle sizes.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | We iterate once from 1 to n, performing constant work per iteration |
| Space | O(1) | Only a single integer state is maintained |

This is efficient for large n because it avoids any explicit simulation of the circular structure and replaces it with a direct mathematical recurrence.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline
    
    n, k = map(int, input().split())
    res = 0
    for i in range(1, n
```
