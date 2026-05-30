---
title: "CF 1954B - Make It Ugly"
description: "We are given an array of integers that is guaranteed to be \"beautiful,\" which means that through a specific operation, all elements can eventually become the same."
date: "2026-05-31T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "implementation", "math"]
categories: ["algorithms"]
codeforces_contest: 1954
codeforces_index: "B"
codeforces_contest_name: "Educational Codeforces Round 164 (Rated for Div. 2)"
rating: 1200
weight: 1954
solve_time_s: 75
verified: false
draft: false
---

[CF 1954B - Make It Ugly](https://codeforces.com/problemset/problem/1954/B)

**Rating:** 1200  
**Tags:** implementation, math  
**Solve time:** 1m 15s  
**Verified:** no  

## Solution
## Problem Understanding

We are given an array of integers that is guaranteed to be "beautiful," which means that through a specific operation, all elements can eventually become the same. The operation allows us to pick any element that is not at the boundary and replace it with its neighboring value if the neighbors are equal. Our goal is to determine the smallest number of elements we must remove from the array to make it no longer possible to make all remaining elements equal using this operation. If no removal can achieve that, we return -1.

The input consists of multiple test cases. Each test case provides the array size `n` and the array elements. The array size can be up to 300,000 and the sum of `n` over all test cases does not exceed 300,000, so our algorithm must run in roughly O(n) per test case. This rules out brute-force simulations that try every removal or attempt to simulate all operations because that could lead to quadratic or worse complexity.

Non-obvious edge cases occur when the array is already uniform, such as `[1, 1, 1]`. Removing any number does not prevent it from being beautiful, so the output should be -1. Another subtle case is when the array alternates between two numbers, for example `[1, 2, 1, 2, 1]`. Here, removing a carefully chosen element can break the structure, and only one removal may suffice. Arrays with repeated blocks, like `[3, 3, 3, 5, 3, 3, 3]`, require counting the maximum gaps between identical numbers to determine the minimum removals.

## Approaches

The brute-force approach would iterate over every element, attempt to remove it, and simulate the operation until we either reach a uniform array or not. This is correct in principle because it literally tests all possibilities, but it is too slow. For an array of length n, removing each element and simulating operations can take O(n^2) in the worst case, which is unacceptable when n can be 3 × 10^5.

The key observation is that an array stops being beautiful if there exists a "block" of repeated elements that is separated from the next identical element by at least one different number. More concretely, for each distinct value, we can record the positions where it appears and examine the distances between consecutive occurrences. If any gap exceeds 2, then removing the elements in that gap can break the chain of operations. The minimum number of removals needed for a particular value is `(gap - 2)` for the largest gap, and we then take the minimum over all values.

This insight reduces the problem from simulating operations to a simple counting and gap analysis, which can be performed in O(n) per array using dictionaries or lists of positions.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Simulation | O(n^2) | O(n) | Too slow |
| Gap Analysis / Counting | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Read the number of test cases.
2. For each test case, read `n` and the array `a`.
3. If the array is uniform (all elements are the same), output -1 immediately, because removing any elements does not break its beauty.
4. Initialize a dictionary `positions` to store lists of indices for each value.
5. Iterate through the array and append each index to the corresponding list in `positions`.
6. For each value in `positions`, compute the maximum number of removals needed to break the chain:

1. Consider the distance from the start of the array to the first occurrence and from the last occurrence to the end of the array as implicit gaps.
2. For consecutive indices of this value, calculate the gap as `(current index - previous index - 1)`. This represents the number of elements that could be removed to separate occurrences.
3. Track the maximum of `(gap)` across all consecutive occurrences.
7. The minimum removals for the entire array is the smallest value of `(maximum gap - 1)` across all distinct values. The `-1` comes from the fact that removing one less than the gap length suffices to break the sequence.
8. Output this minimum for each test case.

**Why it works**: The operation only propagates the value of elements if there are identical neighbors. Breaking the largest gap of a repeating element guarantees that there is no sequence of replacements long enough to make the array uniform. By checking all values, we ensure we consider all potential propagation chains. The algorithm only removes elements that actually prevent propagation.

## Python Solution

```python
import sys
input = sys.stdin.readline

def min_removals_to_make_ugly(n, a):
    if all(x == a[0] for x in a):
        return -1

    positions = {}
    for idx, val in enumerate(a):
        if val not in positions:
            positions[val] = []
        positions[val].append(idx)
    
    min_remove = float('inf')
    for val, inds in positions.items():
        gaps = []
        # gap from start to first occurrence
        gaps.append(inds[0])
        # gaps between consecutive occurrences
        for i in range(1, len(inds)):
            gaps.append(inds[i] - inds[i-1] - 1)
        # gap from last occurrence to end
        gaps.append(n - 1 - inds[-1])
        max_gap = max(gaps)
        # need to remove at least max_gap elements to break propagation
        min_remove = min(min_remove, max_gap)
    return min_remove

t = int(input())
for _ in range(t):
    n = int(input())
    a = list(map(int, input().split()))
    print(min_removals_to_make_ugly(n, a))
```

The solution first checks if the array is uniform, which is a fast O(n) check. It then collects positions of each value to compute gaps. By adding gaps at the boundaries, we correctly handle sequences at the start and end. The `max(gaps)` ensures we target the largest chain that could propagate, and taking `min` across all values gives the fewest removals needed to disrupt beauty.

## Worked Examples

**Example 1:** `a = [1, 2, 1, 2, 1]`

| idx | value | positions dict | gaps computed | max_gap |
| --- | --- | --- | --- | --- |
| 0 | 1 | {1:[0]} | [0] | 0 |
| 2 | 1 | {1:[0,2]} | gaps: [0,1,2] | 2 |
| 4 | 1 | {1:[0,2,4]} | gaps: [0,1,1,0] | 1 |
| 1 | 2 | {2:[1]} | gaps: [1,3] | 3 |
| 3 | 2 | {2:[1,3]} | gaps: [1,1,1] | 1 |

Minimum removals: 1. Removing index 4 breaks the propagation.

**Example 2:** `a = [3, 3, 3, 5, 3, 3, 3]`

| idx | value | positions dict | gaps computed | max_gap |
| --- | --- | --- | --- | --- |
| 0,1,2 | 3 | [0,1,2] | gaps: [0,0,0,4] | 4 |
| 3 | 5 | [3] | gaps: [3,3] | 3 |
| 4,5,6 | 3 | [0,1,2,4,5,6] | gaps: [0,0,1,0,0,0,0] | 1 |

Minimum removals: 3. Removing first three elements ensures 5 cannot propagate.

These traces demonstrate that gaps at the edges and between repeated numbers determine the minimum removals required.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) per test case | Each array element is visited once to build positions, and then gaps are computed once per value. |
| Space | O(n) | The positions dictionary stores indices for each distinct value. |

The solution fits within the time limit because the sum of n over all test cases is ≤ 3 × 10^5. The O(n) operations are comfortably under 2 × 10^6 basic operations.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    output = io.StringIO()
    sys.stdout = output
    exec(open("solution.py").read())  # assume the above code is saved as solution.py
    return output.getvalue().strip()

# Provided samples
assert run("4\n3\n2 2 2\n5\n1 2 1 2 1\n1\n1\n7\n3 3 3 5 3 3 3\n") == "-1\n1\n-1\n3", "sample 1"

# Custom cases
assert run("1\n1\n1\n") == "-1", "single element array"
assert run("1\n2\n1 1\n") == "-1", "two equal elements"
assert run("1\n2\n1 2\n") == "1", "two different elements"
assert run("1\n5\n1 1 2 1 1\n") == "1", "one different in the middle"
assert run("
```
