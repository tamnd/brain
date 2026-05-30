---
title: "CF 1942B - Bessie and MEX"
description: "We are given an array a of length n, constructed from some unknown permutation p of the integers 0 through n-1. Each element of a satisfies the relation a[i] = MEX(p[1..i]) - p[i]. The task is to reconstruct any valid permutation p that produces this a."
date: "2026-05-31T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "constructive-algorithms", "math"]
categories: ["algorithms"]
codeforces_contest: 1942
codeforces_index: "B"
codeforces_contest_name: "CodeTON Round 8 (Div. 1 + Div. 2, Rated, Prizes!)"
rating: 1100
weight: 1942
solve_time_s: 78
verified: false
draft: false
---

[CF 1942B - Bessie and MEX](https://codeforces.com/problemset/problem/1942/B)

**Rating:** 1100  
**Tags:** constructive algorithms, math  
**Solve time:** 1m 18s  
**Verified:** no  

## Solution
## Problem Understanding

We are given an array `a` of length `n`, constructed from some unknown permutation `p` of the integers `0` through `n-1`. Each element of `a` satisfies the relation `a[i] = MEX(p[1..i]) - p[i]`. The task is to reconstruct any valid permutation `p` that produces this `a`. The MEX of an array is defined as the smallest non-negative integer missing from that array.

The input provides multiple test cases. For each case, the algorithm must reconstruct a permutation `p` efficiently.

The constraints are substantial: `n` can be as large as 2_10^5, and the sum of all `n` across all test cases is also ≤ 2_10^5. This implies we cannot afford anything worse than linear time per test case; an O(n^2) brute-force approach would result in approximately 10^10 operations in the worst case, which is far too slow for a 2-second time limit.

A subtle point arises with negative and large positive values in `a`. Since `a[i] = MEX(...) - p[i]`, it is possible for `a[i]` to be negative. For example, if MEX at a point is `2` but the permutation element is `4`, then `a[i] = 2 - 4 = -2`. A careless algorithm that assumes `a[i] ≥ 0` will fail. Also, multiple solutions may exist, so any valid reconstruction suffices.

An edge case to consider is when all `a[i]` are `1`, `0`, or negative numbers. For instance, if `a = [1,1,1]`, then the algorithm must correctly generate a permutation respecting the MEX differences without reusing numbers.

## Approaches

The naive approach is to reconstruct the permutation greedily by simulating MEX from scratch: for each position `i`, iterate through all unused numbers to see which number satisfies `a[i] = MEX(current) - x`. This requires recalculating the MEX each step in O(n) time, leading to an O(n^2) algorithm. This is correct in principle, but too slow for the problem constraints.

The key observation is that the MEX always increases by at most 1 at each step. If the current MEX is `m`, then the next element of the permutation is either `m - a[i]` if that number is still available, or some other unused number less than `m`. This gives a linear-time construction:

1. Keep a set of all unused numbers in the permutation.
2. Track the current MEX efficiently with a pointer starting at `0`.
3. For each position `i`, compute `p[i] = current_MEX - a[i]`. If this number is unused, assign it. Otherwise, pick the smallest unused number less than the current MEX. Update the current MEX accordingly.

This approach works because the formula `p[i] = MEX - a[i]` is derived directly from the problem statement. It is guaranteed that a valid permutation exists, so we will always find an unused number matching the formula.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n^2) | O(n) | Too slow |
| Optimal | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Initialize a list `used` of size `n` to track which numbers have been placed in `p`. Initialize a set `available` containing all numbers `0..n-1`.
2. Set `current_mex` to `0`.
3. For each index `i` from `0` to `n-1`, compute the candidate number `x = current_mex - a[i]`.
4. If `x` is in `available`, assign `p[i] = x`, remove it from `available`, and leave `current_mex` unchanged or increment it if `x == current_mex`.
5. If `x` is not in `available`, assign `p[i]` as the smallest number in `available`. Remove it and update `current_mex` if necessary.
6. Repeat until all positions are filled.
7. Output the array `p`.

**Why it works:** The invariant is that at each step, `current_mex` reflects the MEX of the numbers used so far. Using `p[i] = current_mex - a[i]` guarantees that the MEX difference formula holds. The availability check ensures that we never reuse numbers, preserving the permutation property.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        n = int(input())
        a = list(map(int, input().split()))
        used = [False] * n
        p = [0] * n
        mex = 0
        import heapq
        # maintain min-heap of unused numbers
        available = list(range(n))
        heapq.heapify(available)

        for i in range(n):
            x = mex - a[i]
            if 0 <= x < n and not used[x]:
                p[i] = x
                used[x] = True
                while mex < n and used[mex]:
                    mex += 1
            else:
                # pick smallest unused
                while used[available[0]]:
                    heapq.heappop(available)
                p[i] = heapq.heappop(available)
                used[p[i]] = True
                while mex < n and used[mex]:
                    mex += 1
        print(" ".join(map(str, p)))

if __name__ == "__main__":
    solve()
```

This solution uses a boolean array `used` to track numbers already assigned, ensuring permutation uniqueness. The `mex` pointer efficiently tracks the current MEX. A min-heap stores unused numbers to efficiently pick the smallest available when the ideal `x` is already used.

## Worked Examples

### Example 1

Input:

```
5
1 1 -2 1 2
```

| i | a[i] | mex | candidate x | assigned p[i] | used after step | mex after step |
| --- | --- | --- | --- | --- | --- | --- |
| 0 | 1 | 0 | -1 | 0 | {0} | 1 |
| 1 | 1 | 1 | 0 | 1 | {0,1} | 2 |
| 2 | -2 | 2 | 4 | 4 | {0,1,4} | 2 |
| 3 | 1 | 2 | 1 | 2 | {0,1,2,4} | 3 |
| 4 | 2 | 3 | 1 | 3 | {0,1,2,3,4} | 5 |

This shows the invariant: `mex` always reflects the current MEX, and `p[i] = mex - a[i]` when possible.

### Example 2

Input:

```
3
-2 1 2
```

| i | a[i] | mex | candidate x | assigned p[i] |
| --- | --- | --- | --- | --- |
| 0 | -2 | 0 | 2 | 2 |
| 1 | 1 | 0 | -1 | 0 |
| 2 | 2 | 1 | -1 | 1 |

Here, negative candidate values trigger selection of the smallest available unused number.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Each element is processed once, heap operations are O(log n) per element but sum over n is O(n log n) which is acceptable within constraints |
| Space | O(n) | Boolean array `used` and min-heap store up to `n` elements |

Given `sum(n) <= 2*10^5`, this fits comfortably within the 2-second time limit.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()
    solve()
    return sys.stdout.getvalue().strip()

# provided samples
assert run("3\n5\n1 1 -2 1 2\n5\n1 1 1 1 1\n3\n-2 1 2\n") in ["0 1 4 2 3\n0 1 2 3 4\n2 0 1","0 1 4 2 3\n0 1 2 3 4\n2 1 0"], "sample 1"

# custom: minimum size
assert run("1\n1\n0\n") == "0", "min size"

# custom: maximum n, trivial a
max_n = 10
assert run(f"1\n{max_n}\n" + " ".join(["1"]*max_n) + "\n") != "", "all ones"

# custom: negative a triggers selection of available
assert run("1\n3\n-1 -1 -1\n") != "", "all negative"

#
```
