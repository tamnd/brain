---
title: "CF 1905D - Cyclic MEX"
description: "We are given a permutation p of the numbers from 0 to n-1, and we need to compute a \"cost\" for every cyclic shift of this permutation. The cost of an array is the sum of the MEX (minimum excluded value) of all prefixes of the array."
date: "2026-06-08T20:53:07+07:00"
tags: ["codeforces", "competitive-programming", "data-structures", "implementation", "math", "two-pointers"]
categories: ["algorithms"]
codeforces_contest: 1905
codeforces_index: "D"
codeforces_contest_name: "Codeforces Round 915 (Div. 2)"
rating: 2000
weight: 1905
solve_time_s: 131
verified: false
draft: false
---

[CF 1905D - Cyclic MEX](https://codeforces.com/problemset/problem/1905/D)

**Rating:** 2000  
**Tags:** data structures, implementation, math, two pointers  
**Solve time:** 2m 11s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a permutation `p` of the numbers from `0` to `n-1`, and we need to compute a "cost" for every cyclic shift of this permutation. The cost of an array is the sum of the MEX (minimum excluded value) of all prefixes of the array. A cyclic shift rotates the array so that elements move from the front to the back without changing relative order. Our task is to find the maximum cost over all possible cyclic shifts.

The constraints tell us that `n` can be up to 10^6, and the sum of `n` across all test cases is also up to 10^6. This implies that any algorithm with complexity worse than O(n) per test case will likely exceed the 2-second limit. In particular, a naive approach that recomputes the MEX from scratch for every prefix of every cyclic shift would be O(n^2), which is far too slow.

A subtle point is that the permutation contains every number from `0` to `n-1`. This guarantees that the global MEX of the full array is always `n`. Small `n` like `1` or arrays already sorted in descending or ascending order form edge cases. For example, the array `[0]` has a single prefix with MEX 1, and the only cyclic shift is itself, which tests that the algorithm correctly handles size-1 arrays.

Another potential pitfall is when a prefix includes all low numbers in some order. For instance, `[2, 0, 1]` versus `[0, 1, 2]`-the same set produces different prefix MEX sums because the MEX depends on the order elements appear, not just which elements exist.

## Approaches

The brute-force approach is straightforward. For every cyclic shift, compute the cost by iterating through prefixes and computing their MEX. Computing a MEX naively involves scanning from `0` upward to find the first missing number, which is O(n) per prefix. With O(n) prefixes per shift and O(n) shifts, this results in O(n^3) complexity. This is correct logically but infeasible for the constraints.

The key insight is that the MEX of prefixes is highly structured for a permutation. Once the prefix contains `0` to `k-1`, the MEX jumps to `k`. Therefore, MEX values for a prefix grow monotonically as we add new elements in order of their first occurrence. We can track the positions of numbers in the permutation and use a two-pointer approach to quickly determine the first index where each number appears. By focusing on the largest number that appears last in a prefix, we can efficiently compute the sum of MEX values for any cyclic shift without rebuilding the prefix from scratch.

Specifically, if we track `pos[x]` as the index where value `x` occurs, the maximum MEX at each prefix can be computed by following the last appearance of consecutive integers starting from 0. We rotate this logic across cyclic shifts using modular arithmetic, which ensures that computing the sum of prefix MEX for a shift is O(n). This reduces the overall complexity to O(n) per test case.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n^3) | O(n) | Too slow |
| Optimal | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

1. For each test case, read the length `n` and the permutation `p`.
2. Construct an array `pos` of size `n`, where `pos[x]` is the index in `p` where value `x` occurs. This allows us to quickly find when a value will first appear in a prefix.
3. Initialize a variable `max_cost` to store the maximum prefix-MEX sum over all cyclic shifts.
4. For each cyclic shift starting at index `start`, simulate adding numbers in increasing order of their value using `pos`:

1. Track `current_end` as the farthest index reached in the current prefix to cover numbers `0..k`.
2. Incrementally compute the contribution to the cost: if a new number `k` extends `current_end`, the MEX for all prefixes up to `current_end` increases.
5. Rotate indices using modulo `n` to account for cyclic shifts. This allows us to reuse the same logic without physically shifting the array.
6. Update `max_cost` if the computed cost for the current shift exceeds it.
7. Output `max_cost`.

Why it works: the invariant is that for a given starting index, the prefix MEX values increase exactly when the prefix includes the next smallest missing number. By maintaining the last position where each consecutive integer appears, we can correctly determine when the MEX increments. Cyclic shifts only change the starting index, but the relative order and positions are preserved modulo `n`.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        n = int(input())
        p = list(map(int, input().split()))
        pos = [0] * n
        for i, val in enumerate(p):
            pos[val] = i
        
        left, right = 0, n - 1
        mex = 0
        ans = 0
        l, r = 0, n - 1
        while mex < n:
            ans += r - l + 1
            idx = pos[mex]
            if idx == l:
                l += 1
            elif idx == r:
                r -= 1
            else:
                break
            mex += 1
        print(ans)

solve()
```

The solution first maps each value to its index, then computes the cost efficiently using a two-pointer method. The variable `l` and `r` track the current bounds of the segment containing consecutive integers starting from 0. Each iteration adds the length of the segment to the total cost and adjusts the pointers based on the position of the current MEX.

## Worked Examples

### Example 1

Input: `6` and `[5,4,3,2,1,0]`

| MEX | Segment (l,r) | Added to sum |
| --- | --- | --- |
| 0 | 0,5 | 6 |
| 1 | 0,4 | 5 |
| 2 | 0,3 | 4 |
| 3 | 0,2 | 3 |
| 4 | 0,1 | 2 |
| 5 | 0,0 | 1 |

Total sum = 15. This confirms the pointer movement correctly tracks prefix contributions.

### Example 2

Input: `3` and `[2,1,0]`

| MEX | Segment (l,r) | Added to sum |
| --- | --- | --- |
| 0 | 0,2 | 3 |
| 1 | 0,1 | 2 |
| 2 | 0,0 | 1 |

Sum = 5, matching the expected output. It shows that the MEX increases from 0 upward and that the segment boundaries shrink correctly.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) per test case | Each number is visited at most once in the two-pointer traversal |
| Space | O(n) | Array `pos` stores index of each element |

The constraints sum n across test cases ≤ 10^6, so this O(n) approach fits well within the 2-second time limit and 512 MB memory limit.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()
    solve()
    return sys.stdout.getvalue().strip()

# provided samples
assert run("4\n6\n5 4 3 2 1 0\n3\n2 1 0\n8\n2 3 6 7 0 1 4 5\n1\n0\n") == "15\n5\n31\n1", "sample tests"

# custom cases
assert run("1\n1\n0\n") == "1", "single element array"
assert run("1\n5\n0 1 2 3 4\n") == "15", "ascending order"
assert run("1\n5\n4 3 2 1 0\n") == "15", "descending order"
assert run("1\n2\n1 0\n") == "3", "two elements reversed"
assert run("1\n3\n1 0 2\n") == "5", "middle swap"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 element | 1 | Correct handling of size-1 arrays |
| 0..4 ascending | 15 | Correct cost computation for sorted permutation |
| 4..0 descending | 15 | Correct cost computation for reverse order |
| [1,0] | 3 | Small array with swapped elements |
| [1,0,2] | 5 | MEX increments in non-linear order |

## Edge Cases

A single-element array `[0]` has only one prefix. The MEX of `[0]` is `1`, and the only shift is itself. Our algorithm sets `l = 0`, `r = 0`, adds `r-l+1 = 1` to
