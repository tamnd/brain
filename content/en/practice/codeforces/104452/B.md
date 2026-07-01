---
title: "CF 104452B - Time to reap the harvest"
description: "We are given a list of plant heights along a line, and a set of queries. Each query gives a cutting height $L$, and we must compute how much material remains above that cut. For each bush with height $ai$, only the portion above $L$ contributes, and only if it is positive."
date: "2026-06-30T14:42:24+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104452
codeforces_index: "B"
codeforces_contest_name: "ICPC Central Russia Regional Contest - 2020"
rating: 0
weight: 104452
solve_time_s: 191
verified: true
draft: false
---

[CF 104452B - Time to reap the harvest](https://codeforces.com/problemset/problem/104452/B)

**Rating:** -  
**Tags:** -  
**Solve time:** 3m 11s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a list of plant heights along a line, and a set of queries. Each query gives a cutting height $L$, and we must compute how much material remains above that cut.

For each bush with height $a_i$, only the portion above $L$ contributes, and only if it is positive. So each bush contributes $\max(a_i - L, 0)$. The task is to sum this contribution over all bushes for every query.

So each query is independent: we imagine placing a horizontal cut at height $L$, discarding everything below it, and summing the leftover vertical lengths.

The constraints $N, K \le 10^5$ force us to avoid recomputing the sum from scratch per query. A direct simulation would cost $O(NK)$, which is about $10^{10}$ operations in the worst case, far too slow. This immediately suggests preprocessing the heights so each query can be answered in logarithmic or constant time.

A naive mistake that often appears here is recomputing only over elements $a_i > L$ without preprocessing. For example, if heights are $[10^9, 10^9, \dots]$ and queries are many small values, every query still scans the full array, causing a timeout even though most values behave similarly across queries.

Another subtle pitfall is forgetting that the contribution depends both on how many elements exceed $L$ and by how much they exceed it. Treating it as just a count of elements above $L$ loses magnitude information and produces incorrect answers.

## Approaches

The brute-force approach evaluates each query independently. For a given $L$, it iterates through all $a_i$, accumulates $a_i - L$ when $a_i > L$, and outputs the sum. This is correct because it directly follows the definition, but it repeats the same scan $K$ times, resulting in $O(NK)$ time.

The key observation is that for a fixed $L$, only elements greater than $L$ matter, and their contribution can be rewritten in a way that separates counting from summation. If we sort the array and maintain prefix sums, we can quickly compute both how many elements exceed $L$ and their total sum. This reduces each query to a binary search plus arithmetic, allowing efficient evaluation.

We transform the expression:

$$\sum \max(a_i - L, 0)
= \sum_{a_i > L} a_i - L \cdot (\text{count of } a_i > L)$$

Once the array is sorted, both terms can be obtained with a single binary search and a prefix sum lookup.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(NK)$ | $O(1)$ | Too slow |
| Sorting + Prefix Sum | $O(N \log N + K \log N)$ | $O(N)$ | Accepted |

## Algorithm Walkthrough

1. Sort the array of heights in non-decreasing order. This allows us to isolate all elements greater than a given query value using binary search.
2. Build a prefix sum array where `pref[i]` stores the sum of the first `i` elements in the sorted array. This allows constant-time range sum queries.
3. For each query value $L$, use binary search to find the first index `pos` such that `a[pos] > L`. Everything from `pos` to $N-1$ contributes to the answer.
4. Compute the sum of all elements greater than $L$ as `total = pref[n] - pref[pos]`.
5. Compute how many elements exceed $L$ as `cnt = n - pos`.
6. Subtract the lost base height $L \cdot cnt$ from `total` to obtain the final answer.
7. Output the result for each query independently.

The key idea is that once the threshold splits the array, the contribution becomes a linear function of the number of remaining elements, so both required statistics come directly from preprocessing.

### Why it works

Sorting ensures that all valid contributors form a contiguous suffix of the array. Prefix sums encode cumulative totals, so any suffix sum can be computed in constant time. Since the transformation rewrites the original nonlinear max-expression into a difference of two linear quantities over that suffix, every query reduces to a single interval computation. No information is lost because every term is accounted for exactly once either in the prefix or excluded suffix.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    a = list(map(int, input().split()))
    k = int(input())
    
    a.sort()
    
    pref = [0] * (n + 1)
    for i in range(n):
        pref[i + 1] = pref[i] + a[i]
    
    from bisect import bisect_right
    
    for _ in range(k):
        L = int(input())
        pos = bisect_right(a, L)
        cnt = n - pos
        total = pref[n] - pref[pos]
        ans = total - L * cnt
        print(ans)

if __name__ == "__main__":
    solve()
```

After sorting, we can quickly isolate the suffix of elements that exceed each query threshold. The prefix sum array converts that suffix into a constant-time sum query. The binary search locates the boundary between contributing and non-contributing elements. Each query is then evaluated using a fixed arithmetic expression derived directly from the original definition.

A common implementation mistake is using `bisect_left` instead of `bisect_right`, which incorrectly includes elements equal to $L$. Another subtle issue is forgetting that subtraction must be applied after computing the full suffix sum, not per element, otherwise integer operations degrade into unnecessary loops.

## Worked Examples

### Example 1

Input:

```
a = [0, 0, 0, 0]
queries = [0, 1, 2]
```

Sorted array is unchanged, prefix sums are all zero.

| L | pos (first > L) | cnt | suffix sum | answer |
| --- | --- | --- | --- | --- |
| 0 | 4 | 0 | 0 | 0 |
| 1 | 4 | 0 | 0 | 0 |
| 2 | 4 | 0 | 0 | 0 |

Every value is ≤ L, so no contribution exists. This confirms correctness on fully saturated cuts.

### Example 2

Input:

```
a = [4, 0, 2, 1, 2]
queries = [0, 1, 2, 3, 4]
```

Sorted: `[0, 1, 2, 2, 4]`, prefix sums: `[0,1,3,5,9]`

| L | pos | cnt | suffix sum | answer |
| --- | --- | --- | --- | --- |
| 0 | 1 | 4 | 9 | 9 |
| 1 | 2 | 3 | 8 | 8 - 3 = 5 |
| 2 | 3 | 2 | 6 | 6 - 4 = 2 |
| 3 | 4 | 1 | 4 | 4 - 3 = 1 |
| 4 | 5 | 0 | 0 | 0 |

This trace shows how the answer decreases linearly as the threshold increases, reflecting shrinking suffix size.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(N \log N + K \log N)$ | sorting plus one binary search per query |
| Space | $O(N)$ | prefix sums stored for constant-time range sums |

The constraints allow up to $2 \times 10^5$ operations, so this solution comfortably fits within limits since sorting dominates and each query is logarithmic.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    n = int(input())
    a = list(map(int, input().split()))
    k = int(input())
    a.sort()

    pref = [0]
    for x in a:
        pref.append(pref[-1] + x)

    from bisect import bisect_right

    out = []
    for _ in range(k):
        L = int(input())
        pos = bisect_right(a, L)
        cnt = n - pos
        total = pref[n] - pref[pos]
        out.append(str(total - L * cnt))
    return "\n".join(out)

# provided samples
assert run("4\n0 0 0 0\n3\n0\n1\n2\n") == "0\n0\n0"
assert run("5\n4 0 2 1 2\n5\n0\n1\n2\n3\n4\n") == "9\n5\n2\n1\n0"

# custom cases
assert run("1\n10\n3\n0\n5\n10\n") == "10\n5\n0"
assert run("3\n1 2 3\n2\n2\n1\n") == "1\n3"
assert run("6\n5 5 5 5 5 5\n2\n4\n6\n") == "6\n0"
assert run("4\n0 100 0 100\n3\n50\n100\n0\n") == "100\n0\n200"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single element | decreasing contributions | base case correctness |
| small sorted mix | threshold splitting logic | binary search boundary |
| uniform array | symmetry and linear decay | equal values handling |
| alternating extremes | correctness of suffix aggregation | prefix-suffix correctness |

## Edge Cases

A key edge case is when all elements are less than or equal to $L$. In that situation, the suffix is empty and the answer must be zero. The algorithm handles this because `pos = n`, so both suffix sum and count are zero, and the formula naturally returns zero.

Another case is when $L = 0$. Then every element contributes fully, and the answer becomes the total sum of the array. The binary search returns `pos = 0`, so the suffix is the entire array and subtraction does nothing.

When all elements are equal, each query either keeps everything or removes everything in a single step. The formula correctly captures this abrupt transition because both suffix sum and count scale together, preserving exact cancellation when $L$ exceeds the value.
