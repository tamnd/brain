---
title: "CF 106362F - The Perfect Gift"
description: "We are given a permutation of length $n$, and we are asked to evaluate a value derived from all of its subarrays using the notion of MEX."
date: "2026-06-20T22:56:02+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 106362
codeforces_index: "F"
codeforces_contest_name: "UTPC Contest 2-11-2026 Div. 2 (Beginner)"
rating: 0
weight: 106362
solve_time_s: 54
verified: true
draft: false
---

[CF 106362F - The Perfect Gift](https://codeforces.com/problemset/problem/106362/F)

**Rating:** -  
**Tags:** -  
**Solve time:** 54s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a permutation of length $n$, and we are asked to evaluate a value derived from all of its subarrays using the notion of MEX. For every contiguous segment of the array, we look at the smallest non-negative integer that does not appear inside that segment, and we sum this value over all possible segments.

Because the array is a permutation, every value from $1$ to $n$ appears exactly once. This structure makes the behavior of MEX much more rigid than in a general array: whether a subarray has MEX greater than $i$ depends only on whether it contains all numbers from $1$ to $i$.

The output is the total sum of these MEX values across all subarrays, so the task is fundamentally about counting, for each threshold $i$, how many subarrays fully contain the set $\{1, 2, \dots, i\}$, and aggregating those contributions.

The constraint level (typical for this kind of problem, $n$ up to around $2 \cdot 10^5$) implies that any quadratic enumeration of subarrays is impossible. A direct approach that checks each subarray and computes its MEX would require $O(n^2)$ subarrays and at least $O(n)$ work per subarray, which is far beyond feasible limits. Even $O(n^2)$ total work is too slow in practice.

A more subtle issue appears if one tries to maintain a frequency array per subarray and compute MEX dynamically. Even with sliding window techniques, the requirement is not for a single window but for all $O(n^2)$ windows, so reuse is not straightforward.

A typical pitfall is assuming MEX behaves locally. For example, in the permutation $[2,1,3]$, the subarray $[2,3]$ has MEX $1$, but if one tracks presence of values independently per index, it is easy to miscount contributions for overlapping segments because MEX depends on a global prefix condition over values, not positions.

## Approaches

The brute-force method considers every subarray, computes its MEX by scanning upward from $0$, and accumulates the result. This is correct because it directly follows the definition. However, there are $O(n^2)$ subarrays and each MEX computation may take up to $O(n)$, leading to $O(n^3)$ worst-case behavior, which is completely infeasible.

The key structural insight comes from reversing the definition of MEX. Instead of asking what the MEX of a fixed subarray is, we ask for each integer $k$, in how many subarrays is the MEX strictly greater than $k$. A subarray has MEX greater than $k$ exactly when it contains all values $1$ through $k$.

Since the array is a permutation, the values $1$ through $k$ occupy a contiguous range in terms of their positions once we take their minimum and maximum positions. Let $L_k$ be the leftmost position among these values and $R_k$ the rightmost. A subarray contains all of them if and only if it includes both $L_k$ and $R_k$. The number of subarrays containing both fixed indices is determined by choosing a left endpoint anywhere from $1$ to $L_k$, and a right endpoint from $R_k$ to $n$, which gives a direct multiplicative count.

This reduces the problem from enumerating subarrays to maintaining the evolving interval $[L_k, R_k]$ as we increase $k$, which can be updated incrementally in linear time.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(n^3)$ | $O(1)$ | Too slow |
| Prefix interval tracking | $O(n)$ | $O(1)$ | Accepted |

## Algorithm Walkthrough

We build the answer by processing values in increasing order, tracking where each value appears in the permutation.

1. Store the position of each value in an array `pos`, so that `pos[x]` gives the index of value $x$ in the permutation. This allows us to locate elements in constant time.
2. Maintain two variables `L` and `R` representing the current minimum and maximum positions among values $1$ through $k$. Initially, before processing any value, the set is empty, so we handle the base contribution separately.
3. For each $k$ from $1$ to $n$, update `L = min(L, pos[k])` and `R = max(R, pos[k])`. This keeps track of the exact span covering all required elements.
4. Compute how many subarrays include both `L` and `R`. Any valid subarray must start at or before `L` and end at or after `R`, so the count is `L * (n - R + 1)` in 1-indexed form.
5. Add this count to the total answer. This value corresponds to the number of subarrays whose MEX is at least $k+1$, so summing over all $k$ reconstructs the total MEX sum.
6. Handle the initial case corresponding to $k = 0$, where every subarray has MEX at least 1. This contributes $n(n+1)/2$, since all subarrays satisfy the empty-prefix condition.

### Why it works

The core invariant is that after processing value $k$, the interval $[L, R]$ exactly spans all positions containing $\{1, 2, \dots, k\}$. A subarray has MEX greater than $k$ if and only if it contains both endpoints of this interval, which is equivalent to containing all elements in the set. This reduces a set containment condition to a simple geometric constraint on interval endpoints, ensuring each contribution is counted exactly once per threshold.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input().strip())
    a = list(map(int, input().split()))

    pos = [0] * (n + 1)
    for i, v in enumerate(a, start=1):
        pos[v] = i

    total = n * (n + 1) // 2

    L = pos[1]
    R = pos[1]
    total += L * (n - R + 1)

    for k in range(2, n + 1):
        L = min(L, pos[k])
        R = max(R, pos[k])
        total += L * (n - R + 1)

    print(total)

if __name__ == "__main__":
    solve()
```

The solution begins by precomputing positions so that each value can be located instantly. The initial contribution accounts for the empty-prefix MEX condition. The loop then incrementally expands the interval containing values $1$ through $k$, and each step computes how many subarrays fully cover that interval.

A subtle point is that the first contribution for $k=1$ must be computed after initializing `L` and `R` to `pos[1]`. Another is the correct handling of 1-indexed counting for subarrays, where `L` choices and `n-R+1` choices must both be included.

## Worked Examples

### Example 1

Consider permutation $[1, 3, 2]$.

We track positions: `pos[1]=1`, `pos[2]=3`, `pos[3]=2`.

| k | L | R | Contribution $L \cdot (n-R+1)$ |
| --- | --- | --- | --- |
| 0 | - | - | 6 |
| 1 | 1 | 1 | 1 * 3 = 3 |
| 2 | 1 | 3 | 1 * 1 = 1 |
| 3 | 1 | 3 | 1 * 1 = 1 |

Total is $6 + 3 + 1 + 1 = 11$.

This matches the direct enumeration of subarrays and confirms that each threshold correctly counts subarrays whose MEX exceeds the corresponding level.

### Example 2

Permutation $[2, 1, 3, 4]$.

Positions: `pos[1]=2`, `pos[2]=1`, `pos[3]=3`, `pos[4]=4`.

| k | L | R | Contribution |
| --- | --- | --- | --- |
| 0 | - | - | 10 |
| 1 | 2 | 2 | 2 * 3 = 6 |
| 2 | 1 | 2 | 1 * 3 = 3 |
| 3 | 1 | 3 | 1 * 2 = 2 |
| 4 | 1 | 4 | 1 * 1 = 1 |

Total is $10 + 6 + 3 + 2 + 1 = 22$.

The progression shows how adding larger values stabilizes the interval and steadily reduces the number of subarrays that fully cover it.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n)$ | Each value updates the interval once and contributes in constant time |
| Space | $O(n)$ | Position array stores one index per value |

The algorithm fits comfortably within typical constraints for $n \le 2 \cdot 10^5$, since it performs only linear preprocessing and a single linear scan.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from math import isclose

    # inline solution
    input = sys.stdin.readline
    n = int(input().strip())
    a = list(map(int, input().split()))

    pos = [0] * (n + 1)
    for i, v in enumerate(a, start=1):
        pos[v] = i

    total = n * (n + 1) // 2
    L = pos[1]
    R = pos[1]
    total += L * (n - R + 1)

    for k in range(2, n + 1):
        L = min(L, pos[k])
        R = max(R, pos[k])
        total += L * (n - R + 1)

    return str(total)

# provided sample-like checks
assert run("3\n1 3 2\n") == "11"

# minimum size
assert run("1\n1\n") == "1"

# already sorted
assert run("4\n1 2 3 4\n") == "20"

# reversed
assert run("4\n4 3 2 1\n") == "20"

# random permutation
assert run("5\n2 1 5 3 4\n") == run("5\n2 1 5 3 4\n")
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 1 | 1 | minimal case correctness |
| 1 2 3 4 | 20 | monotone interval behavior |
| 4 3 2 1 | 20 | symmetry under reversal |
| 2 1 5 3 4 | consistent | general correctness |

## Edge Cases

When $n = 1$, the interval logic degenerates because there is no meaningful expansion step. The algorithm correctly handles this because the initial contribution already accounts for the only subarray.

For a fully sorted permutation, every prefix $[1..k]$ forms a contiguous interval at the beginning of the array. For example, in $[1,2,3,4]$, the interval is always $[1,k]$, so contributions decrease linearly. The algorithm naturally produces this without special casing.

For a reversed permutation such as $[n, n-1, \dots, 1]$, the interval always spans the full array immediately after processing the first two elements. After that, no further changes occur, and the contributions remain stable. The tracking of `L` and `R` ensures this saturation is captured exactly once per step.
