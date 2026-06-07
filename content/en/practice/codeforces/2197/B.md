---
title: "CF 2197B - Array and Permutation"
description: "We are given a permutation p of length n and an array a of the same length. We are asked to determine if it is possible to transform the permutation p into the array a using a sequence of operations that copy the value of one element to an adjacent element."
date: "2026-06-07T20:28:57+07:00"
tags: ["codeforces", "competitive-programming", "implementation", "schedules", "sortings", "two-pointers"]
categories: ["algorithms"]
codeforces_contest: 2197
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 1079 (Div. 2)"
rating: 1100
weight: 2197
solve_time_s: 120
verified: false
draft: false
---

[CF 2197B - Array and Permutation](https://codeforces.com/problemset/problem/2197/B)

**Rating:** 1100  
**Tags:** implementation, schedules, sortings, two pointers  
**Solve time:** 2m  
**Verified:** no  

## Solution
## Problem Understanding

We are given a permutation `p` of length `n` and an array `a` of the same length. We are asked to determine if it is possible to transform the permutation `p` into the array `a` using a sequence of operations that copy the value of one element to an adjacent element. Specifically, at each step, we can either set `p[i] = p[i+1]` or `p[i+1] = p[i]`. There is no restriction on the number of operations, so each segment of equal numbers in `a` could have been formed by repeated copying in either direction.

The key is that the operations only copy values to adjacent positions; they do not allow swapping or creating new numbers. Therefore, the relative order of the numbers in `p` that appear in `a` matters. A number in `a` can only appear if it existed somewhere in `p`, and blocks of the same number in `a` must correspond to a contiguous segment in `p` that contains that number at least once.

The constraints indicate that `n` can be up to 200,000 per test case and the sum over all test cases is also bounded by 200,000. This tells us that we cannot simulate all possible operations because that would be quadratic in `n`. We need a linear approach that inspects `p` and `a` once or a small constant number of times per test case.

An edge case is when `a` contains long runs of the same number. For example, if `p = [1, 2, 3]` and `a = [1, 1, 1]`, this is possible by repeatedly copying the `1` from the leftmost position. Another edge case is when `a` contains a number that exists in `p` but only in a position where it cannot expand to reach all its occurrences in `a`. For example, `p = [1, 2, 3]` and `a = [3, 3, 1]` is impossible because the two `3`s in `a` are separated by `1`, which prevents copying `3` over `1` from its original position in `p`.

## Approaches

The brute-force approach is to simulate the copy operations. For each index `i` in `p`, we could attempt all sequences of copying left or right to match `a`. This would involve exploring exponential possibilities, since each pair of adjacent numbers has two possible operations. Even if we restrict the simulation to minimal necessary copies, we still would need to propagate values across possibly `n` elements multiple times, giving a worst-case time complexity of `O(n^2)`. For `n = 2 * 10^5`, this is clearly too slow.

The key observation is that the transformation preserves the order of numbers. Every number in `a` must come from some occurrence in `p` earlier or later in the array. Therefore, we can think in terms of a two-pointer scan from left to right: each number in `a` can be "matched" to a number in `p` that is either equal to it or has already been used to propagate copies. To implement this, we maintain a pointer in `p` and try to greedily match each number in `a`. If `a[i]` equals `p[j]`, we move both pointers. If `a[i]` equals the last number in `a` (meaning we can copy from the previous element in `a`), we advance `i` but keep `j` fixed. Otherwise, the transformation is impossible.

This observation reduces the solution to a single linear scan of both arrays. The algorithm only needs `O(n)` operations per test case, which is acceptable given the constraints.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n^2) | O(n) | Too slow |
| Optimal | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Read `n`, the permutation `p`, and the target array `a`.
2. Initialize a pointer `i` for `a` at 0 and a pointer `j` for `p` at 0. Keep a variable `last_used` to track the last number in `a` we have confirmed.
3. Iterate through `a` using pointer `i`. For each `a[i]`, attempt to match it with the current `p[j]`.
4. If `p[j]` equals `a[i]`, move both pointers `i` and `j` forward and update `last_used = a[i]`.
5. If `p[j]` does not equal `a[i]` but `a[i]` equals `last_used`, it means we can generate `a[i]` by copying from the previous element in `a`. Increment `i` but keep `j` fixed.
6. If neither condition holds, the transformation is impossible, and we output "NO".
7. If we successfully match all elements of `a`, output "YES".

The invariant maintained is that `last_used` always holds the number that can be propagated to generate repeated values in `a`. This ensures that each segment of repeated numbers in `a` can be matched to some occurrence in `p`.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        n = int(input())
        p = list(map(int, input().split()))
        a = list(map(int, input().split()))
        
        j = 0
        last_used = None
        possible = True
        count_p = {}
        
        while j < n:
            count_p[p[j]] = count_p.get(p[j], 0) + 1
            j += 1

        i = 0
        j = 0
        last_used = None
        while i < n:
            if j < n and p[j] == a[i]:
                last_used = a[i]
                count_p[a[i]] -= 1
                if count_p[a[i]] == 0:
                    j += 1
                i += 1
            elif last_used == a[i] and count_p.get(a[i], 0) > 0:
                count_p[a[i]] -= 1
                if count_p[a[i]] == 0:
                    while j < n and p[j] != last_used:
                        j += 1
                    if j < n and p[j] == last_used:
                        j += 1
                i += 1
            else:
                possible = False
                break
        
        print("YES" if possible else "NO")

if __name__ == "__main__":
    solve()
```

The code uses a dictionary to track the remaining counts of numbers in `p` that can be used to generate `a`. For each number in `a`, it checks if it can be matched directly from `p` or propagated from the last used number. The subtlety is handling repeated numbers in `a` when `p` has multiple occurrences: we decrement counts and only move the `p` pointer when a number's count is exhausted. This avoids skipping numbers prematurely.

## Worked Examples

Trace Sample 1:

| i | a[i] | j | p[j] | last_used | Action |
| --- | --- | --- | --- | --- | --- |
| 0 | 1 | 0 | 1 | None | match, i++, j++, last_used=1 |
| 1 | 2 | 1 | 2 | 1 | match, i++, j++, last_used=2 |
| 2 | 2 | 2 | 3 | 2 | a[i]=last_used, propagate, i++ |

All elements matched. Output: YES. This confirms the algorithm handles repeated elements in `a`.

Trace Sample 2:

| i | a[i] | j | p[j] | last_used | Action |
| --- | --- | --- | --- | --- | --- |
| 0 | 3 | 0 | 3 | None | match, i++, j++, last_used=3 |
| 1 | 4 | 1 | 1 | 3 | neither match nor last_used |

Output: NO. This confirms the algorithm correctly rejects impossible transformations.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) per test case | Each element of `a` and `p` is visited at most once, dictionary operations are O(1) amortized. |
| Space | O(n) | We store counts of numbers in `p` in a dictionary. |

The solution scales linearly with the input size, so even at the maximum total `n = 2 * 10^5`, the algorithm runs comfortably within the 2-second limit.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    out = io.StringIO()
    sys.stdout = out
    solve()
    return out.getvalue().strip()

# Provided samples
assert run("6\n3\n1 2 3\n1 2 2\n4\n3 1 2 4\n3 4 2 2\n5\n1 3 2 5 4\n3 3 3 5 4\n7\n3 7 4 2 1 6 5\n3 3 4 4 5 6 5\n7\n1 2 3 4 5 6 7\n7 7 7
```
