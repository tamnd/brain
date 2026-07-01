---
title: "CF 104081K - \u533a\u95f4\u548c"
description: "We are given an array of length $n$, and every element is a non-negative integer. From this array we consider every contiguous subarray, and each subarray has a weight equal to the sum of its elements."
date: "2026-07-02T02:38:47+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104081
codeforces_index: "K"
codeforces_contest_name: "2022\u5e74\u4e2d\u56fd\u5927\u5b66\u751f\u7a0b\u5e8f\u8bbe\u8ba1\u7ade\u8d5b\u5973\u751f\u4e13\u573a"
rating: 0
weight: 104081
solve_time_s: 46
verified: true
draft: false
---

[CF 104081K - \u533a\u95f4\u548c](https://codeforces.com/problemset/problem/104081/K)

**Rating:** -  
**Tags:** -  
**Solve time:** 46s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given an array of length $n$, and every element is a non-negative integer. From this array we consider every contiguous subarray, and each subarray has a weight equal to the sum of its elements.

If we list all subarray sums and sort them in non-decreasing order, we are asked to answer multiple queries. Each query gives an integer $k$, and we must output the value of the $k$-th smallest subarray sum in that sorted list.

The important hidden structure is that although there are $O(n^2)$ subarrays, the array contains only zeros and positive values, so subarray sums behave monotonically as we extend or shrink a window. This monotonicity is what makes the problem solvable in near-linear time per check.

If $n$ is large, say up to $2 \times 10^5$, enumerating all subarrays already produces about $2 \times 10^{10}$ sums, which is impossible to sort explicitly. Even storing them is infeasible. This immediately rules out any approach that explicitly builds or sorts all interval sums.

A naive mistake is to assume prefix sums and sort differences directly. That still requires generating all pairs of prefix indices, which is again quadratic. Another subtle failure case is trying to maintain a heap of subarray sums by expanding intervals, which still degenerates to quadratic behavior.

For example, if the array is $[1, 2, 3]$, the subarray sums are $[1, 2, 3, 3, 5, 6]$. A correct solution must correctly handle duplicates like the two occurrences of 3, which already breaks simplistic “greedy pick next extension” ideas.

## Approaches

The brute-force method is straightforward. Compute every subarray sum by fixing a left endpoint and extending the right endpoint, accumulate all sums into a list, then sort the list and answer queries by indexing. This is correct because it directly constructs the multiset we need. However, it performs $O(n^2)$ subarray constructions and sorting them takes $O(n^2 \log n^2)$, which is far beyond limits even for moderate $n$. With $n = 2 \times 10^5$, the number of subarrays alone makes this approach infeasible.

The key observation is that we do not need to explicitly construct or sort all sums. Instead, we can ask a decision question: given a value $x$, how many subarrays have sum less than or equal to $x$? If we can compute this efficiently, then we can binary search on $x$ to find the smallest value such that at least $k$ subarrays have sum $\le x$. This transforms the problem from sorting a huge implicit array into repeated counting over a monotone predicate.

The counting step becomes efficient because all array values are non-negative. This ensures that if we fix a left boundary, expanding the right boundary only increases the sum, so we can maintain a sliding window with two pointers in linear time.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(n^2 \log n^2)$ | $O(n^2)$ | Too slow |
| Binary Search + Two Pointers | $O(n \log S)$ | $O(1)$ | Accepted |

Here $S$ is the total sum of the array, which bounds all subarray sums.

## Algorithm Walkthrough

We reduce the problem to answering multiple kth-order statistic queries over subarray sums using binary search on the answer space.

1. Compute the maximum possible subarray sum, which is the total sum of the array. This becomes the upper bound for binary search. The lower bound is zero.
2. Define a function `count(x)` that returns how many subarrays have sum less than or equal to $x$. This function is the core of the solution.
3. Compute `count(x)` using two pointers. Maintain a sliding window $[l, r]$ and its sum. For each right endpoint $r$, increase the sum. If the sum exceeds $x$, move $l$ forward until the sum is valid again. At each position $r$, all subarrays ending at $r$ and starting from any index in $[l, r]$ are valid, contributing $r - l + 1$ subarrays. This works because all numbers are non-negative, so shrinking the window never increases the sum.
4. For each query $k$, perform binary search on the value range $[0, S]$. At each midpoint $mid$, compute `count(mid)`. If it is at least $k$, we can move left; otherwise we move right.
5. The final binary search result is the smallest value such that at least $k$ subarrays have sum less than or equal to it, which is exactly the $k$-th smallest subarray sum.

### Why it works

The correctness hinges on the monotonicity of the predicate “number of subarrays with sum ≤ x”. As $x$ increases, this count never decreases because every previously valid subarray remains valid. This makes binary search valid over the answer space.

Inside `count(x)`, correctness comes from the sliding window invariant that at every step, the window $[l, r]$ is the smallest left boundary such that the sum of the window is ≤ $x$. Because all elements are non-negative, extending $r$ can only increase the sum, and moving $l$ can only decrease it. Therefore every valid subarray ending at $r$ is exactly those starting between $l$ and $r$, and no valid subarray is missed or double-counted.

## Python Solution

```python
import sys
input = sys.stdin.readline

def count_subarrays_leq(arr, x):
    n = len(arr)
    l = 0
    s = 0
    res = 0
    for r in range(n):
        s += arr[r]
        while l <= r and s > x:
            s -= arr[l]
            l += 1
        res += (r - l + 1)
    return res

def solve():
    n = int(input().strip())
    arr = list(map(int, input().split()))
    q = int(input().strip())
    queries = [int(input().strip()) for _ in range(q)]

    total = sum(arr)

    def kth(k):
        lo, hi = 0, total
        ans = total
        while lo <= hi:
            mid = (lo + hi) // 2
            if count_subarrays_leq(arr, mid) >= k:
                ans = mid
                hi = mid - 1
            else:
                lo = mid + 1
        return ans

    for k in queries:
        print(kth(k))

if __name__ == "__main__":
    solve()
```

The function `count_subarrays_leq` is the sliding window counter. The key implementation detail is maintaining `l` so that the window sum never exceeds `x`. This guarantees linear complexity per call.

The function `kth` performs binary search over possible subarray sums. The upper bound is safely set to the total sum because no subarray can exceed it.

## Worked Examples

Consider the array $[1, 2, 3]$. The subarray sums are $[1, 3, 6, 2, 5, 3]$, which sorted become $[1, 2, 3, 3, 5, 6]$.

For $k = 4$, we expect the answer to be 3.

### Binary search trace for $k = 4$

| mid | count(mid) | decision |
| --- | --- | --- |
| 3 | 5 | go left |
| 1 | 1 | go right |
| 2 | 3 | go right |
| 3 (final candidate) | 5 | valid |

The smallest value with count ≥ 4 is 3.

This trace shows how duplicate sums are naturally handled, since the counting function includes all occurrences rather than unique values.

Now consider $[0, 0, 1]$. Subarray sums are $[0, 0, 1, 0, 1, 1]$, sorted as $[0, 0, 0, 1, 1, 1]$.

For $k = 2$, answer is 0.

### Binary search trace for $k = 2$

| mid | count(mid) | decision |
| --- | --- | --- |
| 1 | 6 | go left |
| 0 | 3 | go left |
| 0 | 3 | stop |

The algorithm correctly handles many zero-sum subarrays, which are common when the input contains zeros.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n \log S \cdot q)$ | Each query performs a binary search over sum range, and each check uses a linear two-pointer scan |
| Space | $O(1)$ | Only pointers and counters are used |

The total sum $S$ is bounded by the sum of the array elements, so the binary search depth is small. With typical constraints, this comfortably fits within limits when optimized input is used.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from sys import stdout
    import contextlib
    out = io.StringIO()
    with contextlib.redirect_stdout(out):
        solve()
    return out.getvalue().strip()

# sample-like case
assert run("3\n1 2 3\n2\n1\n4\n") == "1\n3"

# all zeros
assert run("4\n0 0 0 0\n3\n1\n5\n10\n") == "0\n0\n0"

# single element
assert run("1\n5\n2\n1\n1\n") == "5\n5"

# mixed case
assert run("3\n0 1 0\n3\n1\n2\n3\n") == "0\n0\n1"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| all zeros | 0s | handling many equal subarray sums |
| single element | 5, 5 | minimal structure correctness |
| mixed zeros | 0, 0, 1 | duplicate sums and ordering |

## Edge Cases

For an all-zero array like $[0, 0, 0]$, every subarray has sum 0. The counting function `count(x)` returns the full number of subarrays for any $x \ge 0$, and binary search correctly converges to 0 for every query, since 0 is the only possible value.

For a strictly increasing array like $[1, 2, 3]$, subarray sums are all distinct or mildly duplicated, but still monotone. The sliding window always shrinks only when necessary, and every subarray is counted exactly once in `count(x)` because each right endpoint contributes a contiguous block of valid starts.

For a case with internal zeros such as $[1, 0, 1]$, sums like 1 appear multiple times from different subarrays. The algorithm does not distinguish structure, only sums, so duplicates are naturally included in the count, preserving correctness of rank-based queries.
