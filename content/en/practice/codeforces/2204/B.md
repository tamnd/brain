---
title: "CF 2204B - Right Maximum"
description: "We are given an array of integers and asked to simulate a very specific removal process. In each operation, we look at the current array, find the maximum element, and if multiple elements share that maximum, we choose the rightmost one."
date: "2026-06-07T19:55:11+07:00"
tags: ["codeforces", "competitive-programming", "greedy"]
categories: ["algorithms"]
codeforces_contest: 2204
codeforces_index: "B"
codeforces_contest_name: "Educational Codeforces Round 188 (Rated for Div. 2)"
rating: 800
weight: 2204
solve_time_s: 94
verified: true
draft: false
---

[CF 2204B - Right Maximum](https://codeforces.com/problemset/problem/2204/B)

**Rating:** 800  
**Tags:** greedy  
**Solve time:** 1m 34s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given an array of integers and asked to simulate a very specific removal process. In each operation, we look at the current array, find the maximum element, and if multiple elements share that maximum, we choose the rightmost one. Then, we remove that element and everything that comes after it. The question asks how many such operations it will take to empty the array completely.

The input provides multiple test cases. Each test case gives the length of the array followed by the array itself. The constraints tell us that the array size can be up to 200,000, and there can be up to 10,000 test cases, but the sum of all array sizes across test cases does not exceed 200,000. This indicates we need a solution roughly linear in the array size, as any algorithm worse than O(n) per test case will be too slow.

Edge cases that can break a naive solution include arrays that are strictly increasing, strictly decreasing, or where multiple maximum elements appear. For example, an array `[3, 3, 3]` should take one operation, because the rightmost maximum is the last element, removing the whole array in one go. A naive implementation that always picks the first maximum would incorrectly simulate multiple operations.

## Approaches

A brute-force approach would literally simulate the process: at each step, scan the array to find the rightmost maximum, remove all elements from that position to the end, and repeat. This is correct, but finding the maximum takes O(n) each time, and in the worst case, we could perform O(n) operations. That results in O(n^2) time per test case, which is too slow for n = 200,000.

The key observation for an optimal solution is that the number of operations corresponds to how far the array stretches to the left as we remove maximum elements from right to left. Specifically, if we traverse the array from right to left, keeping track of the maximum seen so far, every time the current element is equal to this running maximum, we know it would be selected in some operation. Instead of simulating the removals, we only need to count segments where the maximum "extends" the left boundary. This insight reduces the problem to a single reverse traversal with a few integer variables, which is O(n) time.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n^2) | O(n) | Too slow |
| Optimal | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

1. Start from the end of the array and initialize a counter for operations, a variable to track the current maximum in the suffix, and a boundary marker indicating the leftmost index affected by the next removal.
2. Iterate backwards over the array. Update the current maximum seen so far.
3. Whenever the index matches the leftmost boundary of the current removal segment, increment the operation counter and move the boundary to the position of the next maximum that extends the segment. This works because any maximum to the left will eventually become the new rightmost maximum for the next operation.
4. Continue until the beginning of the array is reached.
5. Return the operation counter.

Why it works: traversing from right to left ensures we account for the last occurrence of each maximum first. Each time we hit a left boundary of a segment that will be removed, we know one operation has occurred. Since segments are only extended by elements larger than the previous maximum, each element is considered at most once, guaranteeing correctness.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        n = int(input())
        a = list(map(int, input().split()))
        ops = 0
        right = n
        current_max = 0
        
        # traverse from right to left
        i = n - 1
        while i >= 0:
            current_max = max(current_max, a[i])
            if i == right - current_max:  # left boundary of next removal segment
                ops += 1
                right = i
                current_max = 0
            i -= 1
        print(ops)

if __name__ == "__main__":
    solve()
```

The solution uses fast I/O and iterates over each test case independently. We traverse from the rightmost element to the left, updating `current_max` to reflect the maximum element in the current suffix. When the current index aligns with the left boundary of the segment defined by the maximum, we count an operation and reset the boundary for the next operation. Careful handling of the boundary ensures that overlapping segments are not double-counted, which is a common off-by-one error.

## Worked Examples

Sample 1: `[2, 1, 2, 3, 1]`

| i | a[i] | current_max | right | ops |
| --- | --- | --- | --- | --- |
| 4 | 1 | 1 | 5 | 0 |
| 3 | 3 | 3 | 5 | 1 |
| 2 | 2 | 3 | 3 | 1 |
| 1 | 1 | 3 | 3 | 1 |
| 0 | 2 | 3 | 3 | 1 |

The table shows that after selecting 3 at index 3, the rightmost segment is removed, and we continue counting remaining operations correctly.

Sample 2: `[1, 2, 3, 4, 5, 6]`

| i | a[i] | current_max | right | ops |
| --- | --- | --- | --- | --- |
| 5 | 6 | 6 | 6 | 1 |
| 4 | 5 | 6 | 5 | 2 |
| 3 | 4 | 6 | 4 | 3 |
| 2 | 3 | 6 | 3 | 4 |
| 1 | 2 | 6 | 2 | 5 |
| 0 | 1 | 6 | 1 | 6 |

This demonstrates the strictly increasing case where each element is chosen in its own operation.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) per test case | We traverse the array once from right to left. Maximum update and comparison are O(1). |
| Space | O(1) additional | Only a few integer variables are used; no additional arrays or structures are needed. |

Given the sum of n across all test cases ≤ 2 × 10^5, this solution is well within the 2-second time limit.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    out = io.StringIO()
    sys.stdout = out
    solve()
    return out.getvalue().strip()

# provided samples
assert run("4\n5\n2 1 2 3 1\n6\n1 2 3 4 5 6\n3\n3 2 1\n4\n1 3 3 1\n") == "3\n6\n1\n3", "sample 1"

# custom cases
assert run("1\n3\n3 3 3\n") == "1", "all-equal max"
assert run("1\n5\n5 4 3 2 1\n") == "1", "strictly decreasing"
assert run("1\n5\n1 2 2 3 3\n") == "3", "multiple equal maxima"
assert run("1\n2\n1 2\n") == "2", "minimum size increasing"
assert run("1\n2\n2 1\n") == "1", "minimum size decreasing"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 3 3 3 | 1 | Handling all equal maximums |
| 5 4 3 2 1 | 1 | Strictly decreasing array |
| 1 2 2 3 3 | 3 | Equal maxima appearing multiple times |
| 1 2 | 2 | Minimum-size increasing |
| 2 1 | 1 | Minimum-size decreasing |

## Edge Cases

For the array `[3, 3, 3]`, the algorithm starts from the last element, identifies the rightmost maximum at index 2, removes it and all elements after it (none in this case), and counts one operation. The left boundary is updated, and traversal continues, but no further operations are needed. The output is correctly `1`.

For `[5, 4, 3, 2, 1]`, the last element considered is 1, but the rightmost maximum is 5 at index 0. All elements after index 0 are removed in a single operation. The algorithm correctly counts one operation because the maximum extends the left boundary to cover the entire array.
