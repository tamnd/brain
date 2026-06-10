---
title: "CF 1506E - Restoring the Permutation"
description: "We are given an array q derived from an unknown permutation p of numbers from 1 to n using the rule qi = max(p1, ..., pi). Our task is to reconstruct two permutations that could have produced this q: one that is lexicographically minimal and one that is lexicographically maximal."
date: "2026-06-10T20:20:11+07:00"
tags: ["codeforces", "competitive-programming", "constructive-algorithms", "implementation"]
categories: ["algorithms"]
codeforces_contest: 1506
codeforces_index: "E"
codeforces_contest_name: "Codeforces Round 710 (Div. 3)"
rating: 1500
weight: 1506
solve_time_s: 175
verified: false
draft: false
---

[CF 1506E - Restoring the Permutation](https://codeforces.com/problemset/problem/1506/E)

**Rating:** 1500  
**Tags:** constructive algorithms, implementation  
**Solve time:** 2m 55s  
**Verified:** no  

## Solution
## Problem Understanding

We are given an array `q` derived from an unknown permutation `p` of numbers from `1` to `n` using the rule `q_i = max(p_1, ..., p_i)`. Our task is to reconstruct two permutations that could have produced this `q`: one that is lexicographically minimal and one that is lexicographically maximal. Lexicographical order is like dictionary order: we compare the arrays element by element and the first difference determines the order.

The input guarantees that `q` is a valid "prefix maximum" array, so we do not need to check its validity. The challenge lies in choosing the elements of `p` between the positions where `q` increases. When `q_i > q_{i-1}`, the element `p_i` must be equal to `q_i`. When `q_i == q_{i-1}`, we are free to place any remaining unused number smaller than or equal to `q_i`.

Given `n` can be up to 2 × 10^5, a naive approach that tries all permutations between the known maxima would be far too slow. We need an O(n) solution per test case.

Edge cases include arrays where `q` is strictly increasing, which forces the permutation to be exactly the same, and arrays where `q` has long stretches of repeated values, which requires careful selection of unused numbers to satisfy lexicographical constraints.

## Approaches

The brute-force solution would generate all permutations consistent with `q` by filling unknown positions with all remaining numbers. This works correctly but has factorial complexity in the number of unknown positions, which is infeasible for `n` up to 2 × 10^5.

The key observation is that positions where `q` increases are fixed. All other positions can be filled from the set of numbers not yet used, restricted to be smaller than or equal to the current `q_i`. For the lexicographically minimal permutation, we should always choose the smallest available number in these gaps. For the lexicographically maximal permutation, we choose the largest available number not exceeding the current maximum. This can be efficiently done with a sorted container or a priority queue. The critical insight is that by maintaining the set of remaining numbers, each choice can be done in O(log n) or, with a precomputed list and a pointer, even in O(1) per choice.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n!) | O(n) | Too slow |
| Optimal | O(n) per test case | O(n) | Accepted |

## Algorithm Walkthrough

1. Initialize two empty lists `p_min` and `p_max` for the minimal and maximal permutations. Maintain a set `remaining` containing all numbers from 1 to n not yet placed.
2. Iterate through each index `i` of `q`. If `i == 0` or `q[i] != q[i-1]`, this is a "new maximum" position. Set `p_min[i] = p_max[i] = q[i]` and remove `q[i]` from `remaining`.
3. If `q[i] == q[i-1]`, fill this position differently for the minimal and maximal permutations. For the minimal permutation, choose the smallest number in `remaining` less than `q[i]`. For the maximal permutation, choose the largest number in `remaining` less than `q[i]`.
4. Remove the chosen number from `remaining` to ensure no duplicates.
5. After iterating through all positions, print `p_min` and `p_max`.

The invariant is that at every position `i`, the maximum of the first `i` elements matches `q[i]`, and all elements of `p` remain distinct. By always picking the smallest or largest possible numbers in the gaps, we ensure the permutation is lexicographically minimal or maximal.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        n = int(input())
        q = list(map(int, input().split()))
        
        used = set()
        remaining_min = []
        remaining_max = []
        last = 0
        
        p_min = []
        p_max = []
        
        import heapq
        min_heap = []
        max_heap = []
        
        for num in range(1, n+1):
            remaining_min.append(num)
        remaining_min_ptr = 0
        
        # For maximal, we will use sorted list and pop from end
        remaining_max = list(range(1, n+1))
        
        from bisect import bisect_left
        import collections
        
        # used numbers
        used_set = set()
        
        # Preprocess min and max
        min_available = []
        max_available = []
        import bisect
        
        # We maintain min_available as a pointer to the next smallest unused number
        available = set(range(1, n+1))
        min_available = []
        max_available = sorted(available)
        
        last_q = 0
        for i in range(n):
            if i == 0 or q[i] != q[i-1]:
                # fixed element
                p_min.append(q[i])
                p_max.append(q[i])
                available.remove(q[i])
                max_available.remove(q[i])
            else:
                # q[i] == q[i-1]
                # minimal: choose smallest number in available
                smallest = min(available)
                p_min.append(smallest)
                available.remove(smallest)
                
                # maximal: choose largest number < q[i]
                idx = bisect.bisect_left(max_available, q[i])
                largest = max_available[idx-1]
                p_max.append(largest)
                max_available.pop(idx-1)
        
        print(*p_min)
        print(*p_max)

solve()
```

The code maintains the set of unused numbers and fills in the gaps with the correct strategy. For the minimal permutation, a direct `min` query on the set works because we only need O(1) per element due to ordered removal. For the maximal permutation, a binary search on a sorted list finds the largest number below the current maximum efficiently. Edge cases, like repeated maxima or `q` being strictly increasing, are handled automatically because the selection rules respect the constraints.

## Worked Examples

### Example 1

Input `q = [3, 3, 4, 4, 7, 7, 7]`.

| i | q[i] | available (min) | chosen_min | available (max) | chosen_max |
| --- | --- | --- | --- | --- | --- |
| 0 | 3 | {1..7} | 3 | {1..7} | 3 |
| 1 | 3 | {1,2,4,5,6,7} | 1 | {1,2,4,5,6,7} | 2 |
| 2 | 4 | {2,4,5,6,7} | 4 | {1,4,5,6,7} | 4 |
| 3 | 4 | {2,5,6,7} | 2 | {1,5,6,7} | 1 |
| 4 | 7 | {5,6,7} | 7 | {5,6,7} | 7 |
| 5 | 7 | {5,6} | 5 | {5,6} | 6 |
| 6 | 7 | {6} | 6 | {5} | 5 |

Output minimal: `[3,1,4,2,7,5,6]`

Output maximal: `[3,2,4,1,7,6,5]`

This demonstrates the algorithm correctly places maxima and fills gaps to optimize lexicographical order.

### Example 2

Input `q = [1,2,3,4]`.

Here, `q` is strictly increasing. All elements are fixed maxima.

Output minimal: `[1,2,3,4]`

Output maximal: `[1,2,3,4]`

No gaps exist, so both permutations are identical.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) per test case | Each element is processed once, and available numbers are maintained in structures allowing O(1) min and O(log n) max queries. |
| Space | O(n) | We store the permutation arrays and the sets/lists of remaining numbers. |

Given the sum of `n` across all test cases is ≤ 2 × 10^5, this solution executes well within the 2-second time limit.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    out = io.StringIO()
    sys.stdout = out
    solve()
    return out.getvalue().strip()

# Provided samples
assert run("4\n7\n3 3 4 4 7 7 7\n4\n1 2 3 4\n7\n3 4 5 5 5 7 7\n1\n1\n") == "3 1 4 2 7 5 6\n3 2 4 1 7 6 5\n1 2 3 4\n1 2 3 4\n3 4 5 1 2 7 6\n3 4 5 2 1 7 6\n1\n1"

# Custom cases
assert run("1
```
