---
title: "CF 1557B - Moamen and k-subarrays"
description: "We are given an array of distinct integers, and we are allowed to perform a very specific sequence of operations to sort it. First, we must split the array into exactly $k$ non-empty subarrays."
date: "2026-06-10T12:34:25+07:00"
tags: ["codeforces", "competitive-programming", "greedy", "sortings"]
categories: ["algorithms"]
codeforces_contest: 1557
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 737 (Div. 2)"
rating: 1100
weight: 1557
solve_time_s: 253
verified: false
draft: false
---

[CF 1557B - Moamen and k-subarrays](https://codeforces.com/problemset/problem/1557/B)

**Rating:** 1100  
**Tags:** greedy, sortings  
**Solve time:** 4m 13s  
**Verified:** no  

## Solution
## Problem Understanding

We are given an array of distinct integers, and we are allowed to perform a very specific sequence of operations to sort it. First, we must split the array into exactly $k$ non-empty subarrays. Then, we can reorder these subarrays in any order, and finally, we concatenate them back together. The goal is to determine whether it is possible to make the entire array sorted in non-decreasing order after these operations.

Each test case provides the array length $n$, the number $k$ of subarrays we must create, and the array itself. Our output is a simple "YES" if sorting is possible or "NO" if it is not.

The constraints indicate that $n$ can reach $10^5$ and the sum over all test cases does not exceed $3 \cdot 10^5$. This means we need a linear or linearithmic solution per test case, as an $O(n^2)$ approach would be far too slow.

A subtle edge case arises when $k = 1$ or $k = n$. If $k = 1$, we cannot reorder anything, so the array must already be sorted. If $k = n$, each element forms its own subarray, and any permutation is possible, so the answer is always "YES". Another tricky scenario is when elements are almost sorted but require exactly the right number of splits to become sortable; a naive approach that tries random splits will fail.

## Approaches

A brute-force approach would try every possible way of splitting the array into $k$ subarrays and check if any ordering produces a sorted array. The number of ways to split an array into $k$ subarrays grows combinatorially, roughly as $\binom{n-1}{k-1}$, making this completely impractical for $n$ up to $10^5$.

The key insight is to consider the sorted array as a reference and track contiguous blocks that already appear in the same relative order. Any contiguous segment of the sorted array that appears consecutively in the original array can be kept as one subarray. The minimal number of such blocks determines the minimum $k$ needed to rearrange the array into sorted order. If this number of blocks is less than or equal to $k$, sorting is possible; otherwise, it is impossible. This observation reduces the problem to a single pass over the array while comparing it to its sorted version, resulting in an $O(n \log n)$ solution due to the sort, and $O(n)$ for the block counting.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n choose k) | O(n) | Too slow |
| Optimal | O(n log n) | O(n) | Accepted |

## Algorithm Walkthrough

1. For each test case, read $n$ and $k$ and the array $a$.
2. Create a sorted copy of the array, $b$. This represents the desired order of elements.
3. Build a mapping from element values to their positions in $b$ for quick look-up. This lets us track where each element belongs in the sorted array.
4. Initialize a counter `blocks = 1`. This counts the number of contiguous sequences in $a$ that correspond to consecutive positions in $b$.
5. Iterate through the array $a$ from left to right. For each element $a[i]$, check its position in the sorted array using the mapping. If the current element's position is not consecutive with the previous element's position, increment `blocks` because we have started a new subarray.
6. After processing the entire array, compare `blocks` with $k$. If `blocks <= k`, print "YES"; otherwise, print "NO".

Why it works: Each "block" corresponds to a segment of the original array that can remain intact and be moved as a single subarray. Since reordering the subarrays allows us to place blocks in sorted order, the minimum number of blocks determines the minimal number of subarrays required. If $k$ is at least this number, sorting is achievable.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        n, k = map(int, input().split())
        a = list(map(int, input().split()))
        b = sorted(a)
        pos = {val: i for i, val in enumerate(b)}
        
        blocks = 1
        for i in range(1, n):
            if pos[a[i]] != pos[a[i-1]] + 1:
                blocks += 1
        
        print("YES" if blocks <= k else "NO")

solve()
```

The solution reads multiple test cases efficiently and builds a position map for constant-time lookups. Counting blocks relies on comparing consecutive elements’ positions in the sorted array. This avoids any complicated subarray generation or reordering logic. Edge conditions such as $k = 1$ or $k = n$ are handled naturally because they correspond to the number of blocks being exactly 1 or any number less than or equal to $n$.

## Worked Examples

### Example 1

Input:

```
5 4
6 3 4 2 1
```

| i | a[i] | pos[a[i]] | pos[a[i-1]] +1 | new block? | blocks |
| --- | --- | --- | --- | --- | --- |
| 0 | 6 | 4 | - | - | 1 |
| 1 | 3 | 2 | 5 | yes | 2 |
| 2 | 4 | 3 | 3 | no | 2 |
| 3 | 2 | 1 | 4 | yes | 3 |
| 4 | 1 | 0 | 2 | yes | 4 |

Blocks = 4, k = 4, output = YES. This matches the correct split and reorder described in the problem statement.

### Example 2

Input:

```
4 2
1 -4 0 -2
```

| i | a[i] | pos[a[i]] | pos[a[i-1]] +1 | new block? | blocks |
| --- | --- | --- | --- | --- | --- |
| 0 | 1 | 3 | - | - | 1 |
| 1 | -4 | 0 | 4 | yes | 2 |
| 2 | 0 | 2 | 1 | yes | 3 |
| 3 | -2 | 1 | 3 | yes | 4 |

Blocks = 4, k = 2, output = NO. The algorithm correctly identifies that 2 subarrays are insufficient.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n) | Sorting the array dominates; building the mapping and counting blocks are O(n) |
| Space | O(n) | Storing the sorted array and position map |

Given the sum of $n$ over all test cases is ≤ 3·10^5, the solution will comfortably run within the 2-second limit and stay within 256 MB memory.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()
    solve()
    return sys.stdout.getvalue().strip()

# Provided samples
assert run("3\n5 4\n6 3 4 2 1\n4 2\n1 -4 0 -2\n5 1\n1 2 3 4 5\n") == "YES\nNO\nYES", "samples"

# Custom tests
assert run("1\n3 1\n3 2 1\n") == "NO", "k=1, unsorted"
assert run("1\n3 3\n3 2 1\n") == "YES", "k=n, any order allowed"
assert run("1\n1 1\n42\n") == "YES", "single element"
assert run("1\n5 2\n5 1 4 2 3\n") == "NO", "not enough subarrays"
assert run("1\n5 5\n5 4 3 2 1\n") == "YES", "each element own subarray"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 3 1\n3 2 1 | NO | k=1, unsorted array |
| 3 3\n3 2 1 | YES | k=n, permutation always possible |
| 1 1\n42 | YES | single element |
| 5 2\n5 1 4 2 3 | NO | insufficient k for required blocks |
| 5 5\n5 4 3 2 1 | YES | maximal k allows any arrangement |

## Edge Cases

When $k = 1$, the array must already be sorted. For example, input `[3 2 1]` with `k=1` produces blocks = 3, which is greater than 1, so the algorithm outputs NO.

When $k = n$, each element forms its own block
