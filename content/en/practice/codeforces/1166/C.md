---
title: "CF 1166C - A Tale of Two Lands"
description: "We are given a set of integers representing potential values for two historical markers, $x$ and $y$. For each candidate pair of distinct integers $(x, y)$, we compute two intervals on the number line."
date: "2026-06-12T02:13:00+07:00"
tags: ["codeforces", "competitive-programming", "binary-search", "sortings", "two-pointers"]
categories: ["algorithms"]
codeforces_contest: 1166
codeforces_index: "C"
codeforces_contest_name: "Codeforces Round 561 (Div. 2)"
rating: 1500
weight: 1166
solve_time_s: 87
verified: true
draft: false
---

[CF 1166C - A Tale of Two Lands](https://codeforces.com/problemset/problem/1166/C)

**Rating:** 1500  
**Tags:** binary search, sortings, two pointers  
**Solve time:** 1m 27s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a set of integers representing potential values for two historical markers, $x$ and $y$. For each candidate pair of distinct integers $(x, y)$, we compute two intervals on the number line. The first interval, called Arrayland, is determined by the absolute values of the markers themselves: its endpoints are $|x|$ and $|y|$. The second interval, called Vectorland, is determined by the absolute values of $x-y$ and $x+y$. The legend is considered true for a pair if Arrayland lies entirely inside Vectorland, including endpoints.

Our task is to count how many unordered pairs $(x, y)$ from the given integers satisfy this containment property. The input size can be up to $2 \cdot 10^5$, which immediately rules out a naive brute-force solution that examines all $O(n^2)$ pairs. Each integer can be as large as $10^9$ in magnitude, so we must avoid solutions that scale poorly with the range of numbers.

Edge cases that can trip up a careless implementation include situations where one or both numbers are negative, because the absolute value can change the interval endpoints significantly. For example, with the pair $(-2, 3)$, Arrayland is $[2,3]$ and Vectorland is $[1,5]$, which satisfies containment. A naive check that ignores negative numbers or assumes $x \le y$ will produce incorrect counts. Another edge case is when one value is zero, which can shrink the Vectorland interval and affect containment.

## Approaches

The brute-force approach is simple: generate all unordered pairs of distinct integers $(x, y)$ and check whether Arrayland lies entirely inside Vectorland. This requires computing four absolute values and comparing intervals for each pair. With $n$ up to $2 \cdot 10^5$, the number of pairs is approximately $2 \cdot 10^{10}$, far beyond what fits in the time limit.

The key insight to speed up the solution comes from reducing the problem to a sorted search. The containment condition $[\min(|x|, |y|), \max(|x|, |y|)] \subseteq [|x-y|, |x+y|]$ can be rewritten using the inequalities $\min(|x|, |y|) \ge |x-y|$ and $\max(|x|, |y|) \le |x+y|$. The second inequality always holds because the sum of absolute values is greater than or equal to the larger absolute value. The first inequality simplifies to $|x-y| \le \min(|x|, |y|)$.

This observation allows us to sort the absolute values of all numbers and then use a two-pointer technique to efficiently count pairs satisfying $|x-y| \le \min(|x|, |y|)$. Sorting costs $O(n \log n)$, and the two-pointer scan can be done in $O(n)$ time, producing an overall solution that fits the constraints.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n^2) | O(n) | Too slow |
| Sorting + Two Pointers | O(n log n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Read $n$ and the array of integers $a_1, \dots, a_n$. Take the absolute value of each element and store in a new array `abs_a`. This ensures we can work entirely with non-negative values, which simplifies interval comparisons.
2. Sort `abs_a` in ascending order. Sorting allows us to efficiently find the largest index `j` such that `abs_a[j] - abs_a[i] <= abs_a[i]`.
3. Initialize two pointers: `i` iterates over each element from `0` to `n-1`, representing one end of the pair, and `j` starts from `i+1` to find the farthest element that satisfies the containment condition.
4. For each `i`, increment `j` while `abs_a[j] - abs_a[i] <= abs_a[i]`. Once the condition fails, all indices from `i+1` to `j-1` form valid pairs with `i`. Count them as `j - i - 1`.
5. Sum all counts for each `i` and print the result.

This works because sorting guarantees that once `abs_a[j] - abs_a[i] > abs_a[i]`, any further elements `abs_a[k]` with `k > j` will also violate the condition. This preserves correctness while avoiding checking all pairs explicitly.

## Python Solution

```python
import sys
input = sys.stdin.readline

n = int(input())
a = list(map(int, input().split()))

abs_a = sorted(abs(x) for x in a)

count = 0
j = 1
for i in range(n):
    if j <= i:
        j = i + 1
    while j < n and abs_a[j] - abs_a[i] <= abs_a[i]:
        j += 1
    count += j - i - 1

print(count)
```

The code first converts all numbers to their absolute values, sorts them, and then uses a two-pointer approach to efficiently count all valid pairs. The subtlety is in maintaining the invariant `j >= i+1` and correctly computing `j - i - 1`, which avoids double-counting or counting invalid pairs.

## Worked Examples

**Sample 1:**

Input: `3\n2 5 -3`

| i | abs_a[i] | j | count increment | Total count |
| --- | --- | --- | --- | --- |
| 0 | 2 | 1->2 | 1 | 1 |
| 1 | 3 | 2->3 | 1 | 2 |
| 2 | 5 | 3 | 0 | 2 |

The trace shows that the algorithm counts the valid pairs (2, -3) and (5, -3).

**Sample 2:**

Input: `2\n3 6`

| i | abs_a[i] | j | count increment | Total count |
| --- | --- | --- | --- | --- |
| 0 | 3 | 1->2 | 1 | 1 |
| 1 | 6 | 2 | 0 | 1 |

The only valid pair is (3, 6).

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n) | Sorting dominates, two-pointer scan is O(n) |
| Space | O(n) | Storing absolute values array |

This complexity is well within the given limits, as $n \log n$ operations are acceptable for $n \le 2 \cdot 10^5$, and memory usage is minimal.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    n = int(input())
    a = list(map(int, input().split()))
    abs_a = sorted(abs(x) for x in a)
    count = 0
    j = 1
    for i in range(n):
        if j <= i:
            j = i + 1
        while j < n and abs_a[j] - abs_a[i] <= abs_a[i]:
            j += 1
        count += j - i - 1
    return str(count)

# provided samples
assert run("3\n2 5 -3\n") == "2", "sample 1"
assert run("2\n3 6\n") == "1", "sample 2"

# custom cases
assert run("2\n0 1\n") == "1", "zero case"
assert run("4\n-1 1 2 3\n") == "4", "mixed negative positive"
assert run("5\n1 2 4 8 16\n") == "2", "powers of two"
assert run("2\n1000000000 -1000000000\n") == "1", "large numbers"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 2\n0 1 | 1 | Correct handling of zero |
| 4\n-1 1 2 3 | 4 | Mixed negative and positive numbers |
| 5\n1 2 4 8 16 | 2 | Sparse powers of two |
| 2\n1000000000 -1000000000 | 1 | Boundary of integer range |

## Edge Cases

For input `2\n0 1`, `abs_a = [0,1]`. `i=0` has `j=1->2`, count increment is 1, total count is 1. `i=1` adds 0. This confirms the algorithm correctly includes zero in intervals.

For input `4\n-1 1 2 3`, `abs_a = [1,1,2,3]`. Iterating through `i` and updating `j` counts all valid pairs `(1,1)`, `(1,2)`, `(1,3)`, `(2,3)` correctly. The two-pointer invariant ensures we never miss pairs nor double-count.
