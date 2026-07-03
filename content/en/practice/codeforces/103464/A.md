---
title: "CF 103464A - Stegosauruses"
description: "We are given a collection of stegosauruses, each associated with a single integer value representing the number of spikes it has."
date: "2026-07-03T06:52:47+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 103464
codeforces_index: "A"
codeforces_contest_name: "The second stage of the Republican Olympiad in Informatics. Mogilev region, 2021."
rating: 0
weight: 103464
solve_time_s: 45
verified: true
draft: false
---

[CF 103464A - Stegosauruses](https://codeforces.com/problemset/problem/103464/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 45s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a collection of stegosauruses, each associated with a single integer value representing the number of spikes it has. From this collection, we must choose any two distinct stegosauruses and measure how similar they are in appearance, where similarity is defined as the absolute difference between their spike counts.

The task reduces to finding the pair of values whose numerical difference is as small as possible, and outputting that minimum difference.

Rephrased in algorithmic terms, we are given an array and must compute the smallest absolute difference between any two distinct elements.

The key observation from the constraints is that $n \le 10^5$, which immediately rules out any quadratic pairwise comparison approach. A naive double loop would examine roughly $\frac{n(n-1)}{2}$ pairs, which in the worst case is about $5 \times 10^9$ operations. This is far beyond a typical one-second or two-second limit in competitive programming.

A few edge cases matter in practice. If many values are identical, such as input like `1 1 1 1`, the correct answer is zero because selecting any equal pair yields zero difference. A careless approach that only checks adjacent positions in an unsorted array would fail here if it does not ensure equal values become adjacent after preprocessing.

Another subtle case appears when values are widely scattered, for example `0 100 50 49 51`. The correct answer is 1, coming from the pair (50, 49) or (50, 51). Any solution that does not globally reason about closeness after ordering might miss such pairs.

## Approaches

The brute-force idea is straightforward. We try every pair of stegosauruses, compute the absolute difference of their spike counts, and keep the minimum. This works because it directly evaluates the definition of the answer without any transformation. However, it becomes too slow because it requires checking all pairs, leading to $O(n^2)$ comparisons.

The key insight comes from recognizing that absolute difference behaves nicely under sorting. If we sort the array, then the closest pair in terms of value must appear next to each other in sorted order. This is because any non-adjacent pair has at least one element in between, and that intermediate element can only reduce the gap between neighbors, never increase it beyond a better adjacent candidate.

So instead of comparing all pairs, we only need to compare consecutive elements after sorting. This reduces the problem to scanning the sorted array once and tracking the minimum adjacent difference.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(n^2)$ | $O(1)$ | Too slow |
| Sort + Scan | $O(n \log n)$ | $O(1)$ or $O(n)$ | Accepted |

## Algorithm Walkthrough

1. Read the integer $n$ and the array of spike counts. This forms the dataset we must analyze.
2. Sort the array in non-decreasing order. Sorting is crucial because it rearranges values so that nearby numbers in value space become neighbors in the array.
3. Initialize a variable `ans` with a very large number. This variable tracks the smallest difference found so far.
4. Iterate through the array from the first element to the second-to-last element, examining each adjacent pair.
5. For each index $i$, compute the difference between `a[i+1]` and `a[i]`. Since the array is sorted, this difference is guaranteed to be non-negative and represents the closest possible comparison involving `a[i]` on its right side.
6. Update `ans` if this difference is smaller than the current stored value. This ensures we always retain the best candidate seen so far.
7. After processing all adjacent pairs, output `ans`.

### Why it works

The correctness relies on the fact that in a sorted array, any pair $(i, j)$ with $j > i + 1$ cannot produce a smaller difference than some adjacent pair between them. Formally, for any $i < k < j$, we have:

$$a[j] - a[i] = (a[j] - a[k]) + (a[k] - a[i])$$

Both terms are non-negative after sorting, so the total difference is at least as large as one of the adjacent gaps inside the interval. This guarantees that the global minimum must occur between consecutive elements.

## Python Solution

```python
import sys
input = sys.stdin.readline

n = int(input())
a = list(map(int, input().split()))

a.sort()

ans = float('inf')

for i in range(n - 1):
    diff = a[i + 1] - a[i]
    if diff < ans:
        ans = diff

print(ans)
```

The code follows the algorithm directly. The sorting step ensures we only need local comparisons. The loop over adjacent pairs is safe because every relevant candidate pair is represented there. Using `float('inf')` is a convenient way to initialize the minimum tracker without worrying about bounds of input values.

A common implementation mistake is forgetting to sort the array, which leads to missing the optimal pair entirely. Another subtle issue is using absolute differences on unsorted data but only checking neighbors, which is incorrect because closeness is not local in an unsorted arrangement.

## Worked Examples

### Example 1

Input:

```
5
2 6 0 19 10
```

Sorted array becomes `[0, 2, 6, 10, 19]`.

| i | a[i] | a[i+1] | diff | ans |
| --- | --- | --- | --- | --- |
| 0 | 0 | 2 | 2 | 2 |
| 1 | 2 | 6 | 4 | 2 |
| 2 | 6 | 10 | 4 | 2 |
| 3 | 10 | 19 | 9 | 2 |

Final answer is `2`.

This trace shows how the smallest gap emerges immediately after sorting, and no later comparison improves it.

### Example 2

Input:

```
7
1 2 1 2 4 2 3
```

Sorted array becomes `[1, 1, 2, 2, 2, 3, 4]`.

| i | a[i] | a[i+1] | diff | ans |
| --- | --- | --- | --- | --- |
| 0 | 1 | 1 | 0 | 0 |
| 1 | 1 | 2 | 1 | 0 |
| 2 | 2 | 2 | 0 | 0 |
| 3 | 2 | 2 | 0 | 0 |
| 4 | 2 | 3 | 1 | 0 |
| 5 | 3 | 4 | 1 | 0 |

Final answer is `0`.

This confirms that duplicates are naturally handled because sorting groups identical values together, immediately producing zero difference.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n \log n)$ | Sorting dominates, single linear scan after |
| Space | $O(1)$ or $O(n)$ | Depends on sorting implementation |

Given $n \le 10^5$, sorting comfortably fits within time limits, and the linear pass is negligible.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys as _sys
    input = _sys.stdin.readline

    n = int(input())
    a = list(map(int, input().split()))
    a.sort()
    ans = float('inf')
    for i in range(n - 1):
        ans = min(ans, a[i + 1] - a[i])
    return str(ans)

# provided samples
assert run("5\n2 6 0 19 10\n") == "2"
assert run("7\n1 2 1 2 4 2 3\n") == "0"
assert run("2\n10 15\n") == "5"

# custom cases
assert run("2\n0 0\n") == "0", "all equal"
assert run("3\n1000000000 0 500000000\n") == "500000000", "large spread"
assert run("4\n1 100 101 102\n") == "1", "clustered values"
assert run("5\n5 4 3 2 1\n") == "1", "reverse order input"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `0 0` case | 0 | duplicates handling |
| large spread | 500000000 | large values correctness |
| clustered values | 1 | adjacent minimum detection |
| reverse order | 1 | sorting necessity |

## Edge Cases

For duplicate-heavy inputs like `4 4 4 4`, the algorithm sorts into a constant array, and every adjacent difference is zero, so the result is correctly zero without special handling.

For reverse-sorted inputs like `5 4 3 2 1`, sorting transforms it into `1 2 3 4 5`, and the minimum adjacent difference becomes 1. A naive approach that skips sorting and only checks original neighbors would incorrectly conclude larger gaps such as 4 or 3.

For large-value separation cases like `0 1000000000 500`, sorting ensures the closest pair is revealed as `(500, 0)` or `(1000000000, 500)`, with the correct minimum extracted from adjacent comparisons after ordering.
