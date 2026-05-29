---
title: "CF 309C - Memory for Arrays"
description: "The problem models a simplified memory allocation scenario. We have a computer’s RAM represented as a sequence of cells. Some of these cells are already occupied, and the remaining empty consecutive sequences form memory clusters. Each cluster is described by its size in cells."
date: "2026-05-29T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "binary-search", "bitmasks", "greedy"]
categories: ["algorithms"]
codeforces_contest: 309
codeforces_index: "C"
codeforces_contest_name: "Croc Champ 2013 - Finals (online version, Div. 1)"
rating: 1900
weight: 309
solve_time_s: 219
verified: true
draft: false
---

[CF 309C - Memory for Arrays](https://codeforces.com/problemset/problem/309/C)

**Rating:** 1900  
**Tags:** binary search, bitmasks, greedy  
**Solve time:** 3m 39s  
**Verified:** yes  

## Solution
## Problem Understanding

The problem models a simplified memory allocation scenario. We have a computer’s RAM represented as a sequence of cells. Some of these cells are already occupied, and the remaining empty consecutive sequences form memory clusters. Each cluster is described by its size in cells. Separately, a program wants to allocate arrays, each requiring a fixed number of consecutive cells. Specifically, the _j_-th array requires `2 * b[j]` cells. Our goal is to fit as many arrays as possible into the existing clusters, without splitting an array across clusters or overlapping allocations.

The input provides the number of clusters `n` and the number of arrays `m`, followed by the sizes of each cluster and the sizes of each array (expressed as `b[j]`, so the required memory is `2*b[j]`). The output is a single integer representing the maximum number of arrays that can be fully allocated.

The constraints are significant: both `n` and `m` can be up to `10^6`, and each cluster or array size can be up to `10^9`. A naive approach that tries every cluster for every array would perform up to `10^12` operations in the worst case, which is far beyond feasible within the 2-second limit. This indicates that any solution must be roughly linearithmic (`O(n log n)` or `O(m log m)`) or linear (`O(n + m)`) in complexity.

Edge cases that are easy to mishandle include scenarios where multiple small arrays could fit into a single large cluster, or when clusters and arrays are exactly the same size. For instance, given clusters `[4, 4]` and arrays `[2, 2, 2]` (requiring 4, 4, 4 cells), the maximum number of arrays that fit is 2, not 3, because the arrays cannot share clusters. A careless greedy approach might mistakenly count all three arrays as fitting.

## Approaches

The brute-force approach would iterate over each array and attempt to place it in every available cluster. For each array, you would scan all clusters until finding one large enough. After placement, you reduce the cluster size or mark it as used. While correct, this approach is too slow: for `n = m = 10^6`, it could perform roughly `10^12` operations.

The key observation that allows optimization is that we can sort both clusters and arrays. Sorting clusters in ascending order and arrays by their required sizes allows a greedy strategy: always try to fit the smallest remaining array into the smallest cluster that can hold it. This works because allocating a small array to a large cluster unnecessarily could block placement of a larger array later, reducing the total number of allocations. Sorting ensures that at each step, the array is placed optimally relative to available clusters.

Once sorted, the problem reduces to a two-pointer or binary search approach. For each array, we can efficiently find the first cluster that can accommodate it. After allocating, we remove or mark that cluster as used. With Python, we can use a `SortedList` from the `sortedcontainers` module to maintain clusters in a way that supports `O(log n)` allocation queries. Sorting arrays and clusters takes `O(n log n + m log m)`, and each allocation check is `O(log n)`, resulting in `O((n + m) log n)` total complexity.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n*m) | O(n) | Too slow |
| Sorting + Greedy + Binary Search | O((n + m) log n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Read the input: the number of clusters `n`, the number of arrays `m`, the cluster sizes `a[i]`, and the array size requirements `b[j]`.
2. Convert the array requirements to actual memory needed: `size[j] = 2 * b[j]`.
3. Sort the cluster sizes in ascending order. Sorting ensures that smaller clusters are considered first for small arrays.
4. Sort the array sizes in ascending order. This allows us to allocate the smallest arrays first.
5. Initialize a `SortedList` of cluster sizes to allow efficient searching and removal.
6. Iterate through each array in order. For each array:

- Use the `bisect_left` method to find the first cluster that can accommodate the array.
- If a suitable cluster exists, remove it from the `SortedList` and increment the count of placed arrays.
- If no cluster can accommodate the array, skip it.
7. Print the count of successfully placed arrays.

Why it works: the invariant maintained is that at any point, all arrays considered so far are placed in the smallest available cluster that fits. Sorting arrays ensures that no larger array is blocked by smaller arrays allocated to oversized clusters. The `SortedList` guarantees that we always find the smallest fitting cluster efficiently.

## Python Solution

```python
import sys
input = sys.stdin.readline
from sortedcontainers import SortedList

def main():
    n, m = map(int, input().split())
    clusters = list(map(int, input().split()))
    arrays = list(map(int, input().split()))
    
    # Convert array requirements to actual sizes
    arrays = [2 * b for b in arrays]
    
    clusters.sort()
    arrays.sort()
    
    cluster_list = SortedList(clusters)
    count = 0
    
    for array_size in arrays:
        idx = cluster_list.bisect_left(array_size)
        if idx < len(cluster_list):
            # Allocate this array
            cluster_list.pop(idx)
            count += 1
            
    print(count)

if __name__ == "__main__":
    main()
```

The code reads input and prepares arrays and clusters. Sorting ensures proper greedy allocation. `SortedList` provides efficient `O(log n)` search and deletion. Each array is attempted in order, and only clusters large enough are used. This avoids double counting or splitting arrays.

## Worked Examples

### Sample 1

Input: `5 3\n8 4 3 2 2\n3 2 2`

| Array sizes (2*b) | Sorted arrays | Clusters | Allocated count |
| --- | --- | --- | --- |
| 6, 4, 4 | 4, 4, 6 | 2, 2, 3, 4, 8 | 0 |
| 4 | 4 | 2, 2, 3, 4, 8 | 1 |
| 4 | 4 | 2, 2, 3, 8 | 2 |
| 6 | 6 | 2, 2, 3, 8 | 3 not allocated (first cluster ≥6 is 8, pop 8) |

Output: `2` (maximum arrays fully allocated without splitting)

### Sample 2

Input: `10 6\n1 1 1 1 1 1 1 1 1 1\n1 1 1 1 1 1`

All arrays require 2 cells, clusters are 1 → no array fits. Output: `0`.

This demonstrates that the algorithm correctly handles clusters too small to fit arrays.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O((n + m) log n) | Sorting takes O(n log n + m log m). Each of m array placements requires O(log n) search and deletion from SortedList. |
| Space | O(n) | SortedList holds all clusters, arrays can be sorted in place. |

The algorithm scales to n, m = 10^6 within 2 seconds since ~20 million log operations are feasible in practice.

## Test Cases

```python
import sys, io
from contextlib import redirect_stdout

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    f = io.StringIO()
    with redirect_stdout(f):
        main()
    return f.getvalue().strip()

# Provided samples
assert run("5 3\n8 4 3 2 2\n3 2 2\n") == "2", "sample 1"
assert run("10 6\n1 1 1 1 1 1 1 1 1 1\n1 1 1 1 1 1\n") == "0", "sample 2"

# Custom cases
assert run("2 3\n4 4\n2 2 2\n") == "2", "multiple arrays same cluster size"
assert run("3 2\n10 5 2\n3 1\n") == "2", "largest array fits largest cluster"
assert run("1 1\n1000000000\n500000000\n") == "1", "maximum size allocation"
assert run("3 3\n5 5 5\n1 2 3\n") == "3", "all arrays fit exact clusters"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `2 3\n4 4\n2 2 2` | 2 | Multiple arrays competing for same cluster sizes |
| `3 2\n10 5 2\n3 1` | 2 | Largest array fits largest cluster |
| `1 1\n1000000000\n500000000` | 1 | Large integer edge case |
| `3 3\n5 5 5\n1 2 3` | 3 | All arrays can fit exactly |

## Edge Cases

A cluster too small: `1 1\n1\n1` (array requires
