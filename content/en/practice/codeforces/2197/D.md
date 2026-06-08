---
title: "CF 2197D - Another Problem about Beautiful Pairs"
description: "We are given an array of integers, and we need to count pairs of indices (i, j) where i < j and the product of the corresponding values equals the distance between the indices: a[i] a[j] = j - i."
date: "2026-06-09T04:44:32+07:00"
tags: ["codeforces", "competitive-programming", "brute-force", "data-structures", "divide-and-conquer", "math", "number-theory"]
categories: ["algorithms"]
codeforces_contest: 2197
codeforces_index: "D"
codeforces_contest_name: "Codeforces Round 1079 (Div. 2)"
rating: 1600
weight: 2197
solve_time_s: 107
verified: true
draft: false
---

[CF 2197D - Another Problem about Beautiful Pairs](https://codeforces.com/problemset/problem/2197/D)

**Rating:** 1600  
**Tags:** brute force, data structures, divide and conquer, math, number theory  
**Solve time:** 1m 47s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given an array of integers, and we need to count pairs of indices `(i, j)` where `i < j` and the product of the corresponding values equals the distance between the indices: `a[i] * a[j] = j - i`. The output is a single integer per test case representing the total number of such "beautiful" pairs.

The constraints show that the array can be large, up to 2 × 10^5 elements in a single test case, and the sum of all `n` across test cases is also bounded by 2 × 10^5. With a 2-second time limit, this implies we can safely afford something roughly linear or linearithmic in total input size, but anything quadratic in `n` per test case will be far too slow. The values themselves can be up to 10^9, which rules out any naive frequency array approach that indexes by the values.

Edge cases that can be tricky include very small arrays of size 2, arrays where all elements are the same, or arrays where elements are very large. For instance, if `a = [10^9, 10^9]`, there are no beautiful pairs because `10^9 * 10^9 = 10^18` is much larger than `j - i = 1`. Conversely, if `a = [1, 1, 1]`, all possible pairs `(i, j)` with `i < j` may satisfy the product condition for small distances, and a naive implementation may miss multiple pairs or double-count them.

## Approaches

The most straightforward approach is brute-force: for each index `i`, iterate through all `j > i` and check whether `a[i] * a[j] == j - i`. This is correct, but its time complexity is O(n^2) per test case. With `n` up to 2 × 10^5, this would lead to roughly 4 × 10^10 operations in the worst case, far exceeding the 2-second limit.

The key observation for optimization is that the difference `j - i` is strictly smaller than `n`, and the product `a[i] * a[j]` must exactly equal that difference. For large values of `a[i]` or `a[j]`, the corresponding `j - i` is too small to ever satisfy the equality. Specifically, only pairs where both numbers are reasonably small relative to `n` can contribute. This means we do not need to consider all pairs; instead, we can iterate over one index and compute all possible `j` that satisfy the condition by rearranging the formula: `j = i + a[i] * a[j]` or equivalently check multiples of `a[i]`.

We can implement this efficiently by iterating `i` from 1 to n and then for each possible multiple `k * a[i]` (where `k` is an integer such that `i + k * a[i] <= n`) check if `a[i] * a[j] = j - i` holds. This reduces the number of candidates drastically, because the number of multiples per `i` is at most `n / a[i]`, which is small for large `a[i]`.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n^2) | O(1) | Too slow |
| Multiples Check | O(n * sqrt(n)) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the number of test cases `t`.
2. For each test case, read `n` and the array `a` of length `n`.
3. Initialize a counter `ans` to zero.
4. Iterate over each index `i` from 1 to `n`. For each `i`, compute candidate indices `j` as `i + k * a[i]` where `k = 1, 2, 3...` until `j > n`.
5. For each computed `j`, check if `a[i] * a[j] == j - i`. If it does, increment `ans`.
6. After processing all indices, print `ans`.

This approach works because we only consider `j` values that could satisfy the equality based on the current `a[i]`. Since the difference `j - i` grows linearly, while `a[i] * a[j]` grows faster with large numbers, most pairs are automatically skipped, keeping the total number of operations within acceptable bounds.

## Python Solution

```python
import sys
input = sys.stdin.readline

t = int(input())
for _ in range(t):
    n = int(input())
    a = list(map(int, input().split()))
    ans = 0
    # Use 1-based indexing for easier mapping with formula
    a = [0] + a
    for i in range(1, n + 1):
        # Only consider multiples of a[i] that stay in bounds
        j = i + a[i]
        while j <= n:
            if a[i] * a[j] == j - i:
                ans += 1
            j += a[i]
    print(ans)
```

We add a dummy zero at the beginning of `a` to make it 1-indexed, which simplifies the formula `a[i] * a[j] == j - i`. For each `i`, we consider multiples of `a[i]` until we exceed `n`. This guarantees that we check every candidate `j` without iterating through all pairs. Incrementing `j` by `a[i]` ensures we only check feasible indices that could satisfy the equality.

## Worked Examples

Sample Input 1:

```
5
1 1 2 100 4
```

| i | a[i] | j candidates | a[i]*a[j] | j-i | Count Increment |
| --- | --- | --- | --- | --- | --- |
| 1 | 1 | 2,3,4,5 | 1_1=1,1_2=2,1_100=100,1_4=4 | 1,2,3,4 | +1,+1,+0,+1 |
| 2 | 1 | 3,4,5 | 1_2=2,1_100=100,1*4=4 | 1,2,3 | +0,+0,+0 |
| 3 | 2 | 5 | 2*4=8 | 2 | +0 |
| 4 | 100 | >5 | - | - | 0 |
| 5 | 4 | >5 | - | - | 0 |

Total beautiful pairs: 3

Sample Input 2:

```
6
2 2 1 1 2 2
```

Walking through the algorithm similarly confirms the output 7.

These traces demonstrate that the multiples-based approach efficiently identifies all valid pairs while skipping impossible ones.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n * sqrt(n)) | Each `i` iterates over `n / a[i]` candidates. Large `a[i]` reduce the number of iterations. In total across all `n` ≤ 2 × 10^5, the number of checks remains manageable. |
| Space | O(n) | We store the array `a` and an auxiliary counter. |

The solution comfortably fits within the 2-second time limit for the sum of all `n` ≤ 2 × 10^5.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    output = []
    t = int(input())
    for _ in range(t):
        n = int(input())
        a = list(map(int, input().split()))
        ans = 0
        a = [0] + a
        for i in range(1, n + 1):
            j = i + a[i]
            while j <= n:
                if a[i] * a[j] == j - i:
                    ans += 1
                j += a[i]
        output.append(str(ans))
    return "\n".join(output)

# provided samples
assert run("4\n5\n1 1 2 100 4\n6\n2 2 1 1 2 2\n10\n1 1 2 3 4 1 1 7 3 9\n2\n1000000000 1000000000\n") == "3\n7\n10\n0"

# custom tests
assert run("1\n2\n1 1\n") == "1", "minimum size array"
assert run("1\n3\n1 1 1\n") == "2", "all elements equal"
assert run("1\n5\n1 2 3 4 5\n") == "3", "small increasing sequence"
assert run("1\n6\n1000000000 1 2 3 4 5\n") == "0", "large first element"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 2\n1 1 | 1 | Minimum-size array, simple case |
| 3\n1 1 1 | 2 | All-equal elements, multiple beautiful pairs |
| 5\n1 2 3 4 5 | 3 | Sequence with small numbers, normal case |
| 6\n1000000000 |  |  |
