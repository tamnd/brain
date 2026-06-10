---
title: "CF 1490D - Permutation Transformation"
description: "We are given a permutation of length $n$, which is an array containing every integer from 1 to $n$ exactly once. The task is to view this permutation as a way to construct a binary tree: the root is the largest element, the elements to the left of it form the left subtree…"
date: "2026-06-10T22:39:20+07:00"
tags: ["codeforces", "competitive-programming", "dfs-and-similar", "divide-and-conquer", "implementation"]
categories: ["algorithms"]
codeforces_contest: 1490
codeforces_index: "D"
codeforces_contest_name: "Codeforces Round 702 (Div. 3)"
rating: 1200
weight: 1490
solve_time_s: 152
verified: false
draft: false
---

[CF 1490D - Permutation Transformation](https://codeforces.com/problemset/problem/1490/D)

**Rating:** 1200  
**Tags:** dfs and similar, divide and conquer, implementation  
**Solve time:** 2m 32s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a permutation of length $n$, which is an array containing every integer from 1 to $n$ exactly once. The task is to view this permutation as a way to construct a binary tree: the root is the largest element, the elements to the left of it form the left subtree recursively, and the elements to the right form the right subtree recursively. For each element in the permutation, we want to compute its depth in this tree, where the root has depth 0, its children depth 1, and so on.

The input consists of multiple test cases. For each test case, the first line is the permutation length $n$ and the second line contains the permutation itself. The output is a list of depths corresponding to each element in the permutation.

Given that $n \le 100$ and there can be up to 100 test cases, the algorithm must handle about 10,000 total elements efficiently. Any approach with complexity worse than $O(n^2)$ per test case might start to feel slow, but for this problem, even a simple recursive approach is acceptable because $n$ is small. Key edge cases include permutations of length 1, where the only element is the root and has depth 0, and permutations that are already sorted ascending or descending, which create skewed trees.

A naive implementation might fail if it does not correctly split the array around the maximum element or forgets to track depth during recursion. For example, for a permutation `[1,2,3,4]`, the maximum is 4, so its depth is 0, 1, 2, 3 for elements `[1,2,3,4]` respectively if we recurse incorrectly.

## Approaches

The brute-force approach is to simulate the tree construction literally. For each subarray, we find the maximum, assign its depth, and recursively call on the left and right subarrays. This works because the tree definition is recursive and the maximum element always defines the root. The main cost is repeatedly scanning subarrays to find the maximum. For $n=100$, the worst-case scenario is scanning subarrays of length $n, n-1, n-2, \dots, 1$, giving a total of roughly $n^2/2$ operations per test case. This is acceptable given the problem limits.

The optimal approach is essentially the same because the input size is small. No advanced data structures are needed. We can implement it cleanly as a recursive function that takes a subarray and a depth, finds the maximum element, assigns its depth, and recurses on the left and right subarrays.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n^2) | O(n) | Accepted |
| Recursive DFS | O(n^2) | O(n) | Accepted |

## Algorithm Walkthrough

1. For each test case, read the permutation of length $n$.
2. Initialize an array `depths` of length $n$ to store the result.
3. Define a recursive function `assign_depth(l, r, d)` where `l` and `r` are the current subarray indices (inclusive), and `d` is the current depth.
4. In `assign_depth`, if `l > r`, return immediately because the subarray is empty.
5. Find the index of the maximum element in the subarray `a[l:r+1]`. Assign `depths[max_index] = d`.
6. Recursively call `assign_depth(l, max_index - 1, d + 1)` to assign depths to the left subtree.
7. Recursively call `assign_depth(max_index + 1, r, d + 1)` to assign depths to the right subtree.
8. After the recursion completes, print the `depths` array for the test case.

Why it works: Each recursive call ensures that the maximum element of the current subarray becomes the root of that subtree. By passing the current depth `d` into the recursion, we correctly assign the depth for each element. The recursion naturally splits the array into left and right children, preserving the tree structure defined in the problem.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        n = int(input())
        a = list(map(int, input().split()))
        depths = [0] * n

        def assign_depth(l, r, d):
            if l > r:
                return
            # find max element in current subarray
            max_index = l
            for i in range(l, r + 1):
                if a[i] > a[max_index]:
                    max_index = i
            depths[max_index] = d
            # recurse on left and right subarrays
            assign_depth(l, max_index - 1, d + 1)
            assign_depth(max_index + 1, r, d + 1)

        assign_depth(0, n - 1, 0)
        print(' '.join(map(str, depths)))

if __name__ == "__main__":
    solve()
```

The code first reads the number of test cases. For each test case, it reads the permutation and initializes a `depths` array. The `assign_depth` function handles the recursive assignment of depths. It searches for the maximum element in the current subarray, assigns the depth, and recursively processes the left and right partitions. Using indices instead of slicing the array avoids creating new lists at each recursion step, saving memory and simplifying depth tracking.

## Worked Examples

### Example 1

Input: `[3, 5, 2, 1, 4]`

Permutation length: 5

| Subarray | Max element | Depth assigned | Left recursion | Right recursion |
| --- | --- | --- | --- | --- |
| `[3,5,2,1,4]` | 5 at index 1 | 0 | `[3]` | `[2,1,4]` |
| `[3]` | 3 at index 0 | 1 | `[]` | `[]` |
| `[2,1,4]` | 4 at index 4 | 1 | `[2,1]` | `[]` |
| `[2,1]` | 2 at index 2 | 2 | `[]` | `[1]` |
| `[1]` | 1 at index 3 | 3 | `[]` | `[]` |

Output depths: `[1,0,2,3,1]`

### Example 2

Input: `[4,3,1,2]`

| Subarray | Max element | Depth assigned | Left recursion | Right recursion |
| --- | --- | --- | --- | --- |
| `[4,3,1,2]` | 4 at index 0 | 0 | `[]` | `[3,1,2]` |
| `[3,1,2]` | 3 at index 1 | 1 | `[]` | `[1,2]` |
| `[1,2]` | 2 at index 3 | 2 | `[1]` | `[]` |
| `[1]` | 1 at index 2 | 3 | `[]` | `[]` |

Output depths: `[0,1,3,2]`

These tables show how the recursion correctly assigns depths, confirming the algorithm handles both left-skewed and right-skewed partitions.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n^2) | Each recursion finds the maximum element by scanning the subarray. Worst-case is n + (n-1) + ... + 1 = O(n^2) |
| Space | O(n) | The recursion depth is at most n, plus the `depths` array of size n |

Given the constraints $n \le 100$ and $t \le 100$, this complexity is comfortably within the limits. Memory usage is minimal, and the recursion depth will not exceed Python's default recursion limit.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    out = io.StringIO()
    sys.stdout = out
    solve()
    sys.stdout = sys.__stdout__
    return out.getvalue().strip()

# Provided samples
assert run("3\n5\n3 5 2 1 4\n1\n1\n4\n4 3 1 2\n") == "1 0 2 3 1\n0\n0 1 3 2"

# Minimum size
assert run("1\n1\n1\n") == "0"

# Increasing sequence
assert run("1\n5\n1 2 3 4 5\n") == "4 3 2 1 0"

# Decreasing sequence
assert run("1\n5\n5 4 3 2 1\n") == "0 1 2 3 4"

# Random permutation
assert run("1\n6\n2 6 1 4 5 3\n") == "1 0 3 2 1 2"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1\n1\n1` | `0` | Single element tree, depth 0 |
| `1\n5\n1 2 3 4 5` | `4 3 2 1 |  |
