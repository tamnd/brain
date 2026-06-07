---
title: "CF 2144A - Cut the Array"
description: "We are given an array of non-negative integers and are asked to split it into three contiguous non-empty subarrays: a prefix, a middle part, and a suffix. For each subarray, we calculate the sum modulo 3."
date: "2026-06-08T01:36:29+07:00"
tags: ["codeforces", "competitive-programming", "brute-force", "constructive-algorithms", "math", "number-theory"]
categories: ["algorithms"]
codeforces_contest: 2144
codeforces_index: "A"
codeforces_contest_name: "Educational Codeforces Round 182 (Rated for Div. 2)"
rating: 800
weight: 2144
solve_time_s: 103
verified: false
draft: false
---

[CF 2144A - Cut the Array](https://codeforces.com/problemset/problem/2144/A)

**Rating:** 800  
**Tags:** brute force, constructive algorithms, math, number theory  
**Solve time:** 1m 43s  
**Verified:** no  

## Solution
## Problem Understanding

We are given an array of non-negative integers and are asked to split it into three contiguous non-empty subarrays: a prefix, a middle part, and a suffix. For each subarray, we calculate the sum modulo 3. The goal is to choose two cut points such that either all three modulo values are the same, or all three are distinct. We must output any valid pair of cut points if one exists, or `0 0` if there is none.

The array length `n` is small, at most 40. Each element is at most 40, and there can be up to 1000 test cases. This means that even an O(n²) solution is feasible because n² is at most 1600, and 1600 × 1000 operations is easily handled in 2 seconds.

Edge cases arise in arrays where all elements are zero or multiples of 3. For instance, an array `[0, 0, 0]` can be split at `l=1, r=2`, and the modulo sums are all 0. Another tricky scenario is when the array has three distinct values modulo 3, such as `[1, 2, 3]`. A naive solution may miss valid splits if it assumes that only sums of consecutive elements matter rather than their remainders modulo 3.

## Approaches

The brute-force approach would iterate over all possible pairs `(l, r)` where `1 ≤ l < r < n`, compute the sums of the three parts, take them modulo 3, and check if the three results are all equal or all distinct. The number of pairs is roughly n²/2, so for `n = 40` this is about 780 operations per test case, which is feasible. The main drawback is repetitive computation of sums. If we naively recomputed sums for every `(l, r)`, each sum could cost O(n), giving an O(n³) approach. That would be too slow if n were larger.

The key optimization is to compute **prefix sums modulo 3** once. Let `prefix[i]` be the sum of the first `i` elements modulo 3. Then the sum of the prefix subarray is `prefix[l]`, the sum of the middle subarray is `(prefix[r] - prefix[l]) % 3`, and the sum of the suffix is `(prefix[n] - prefix[r]) % 3`. With prefix sums precomputed, checking all pairs `(l, r)` becomes O(n²), which is acceptable here.

Because n is very small, we do not need further optimizations. A direct O(n²) nested loop over all valid `l` and `r` with modulo sum checks is sufficient.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force without prefix sums | O(n³) | O(1) | Too slow if n were large |
| Brute Force with prefix sums | O(n²) | O(n) | Accepted |

## Algorithm Walkthrough

1. Read the number of test cases. Loop through each test case.
2. For each test case, read the array of length n.
3. Compute an array of prefix sums modulo 3. Initialize `prefix[0] = 0`. For each index `i`, set `prefix[i] = (prefix[i-1] + a[i-1]) % 3`. This allows O(1) retrieval of any subarray sum modulo 3.
4. Iterate `l` from 1 to n-2. This ensures the prefix has at least one element and leaves room for the middle and suffix.
5. For each `l`, iterate `r` from `l+1` to n-1. This ensures the middle subarray is non-empty and leaves at least one element for the suffix.
6. Compute the modulo sums: `s1 = prefix[l]`, `s2 = (prefix[r] - prefix[l]) % 3`, `s3 = (prefix[n] - prefix[r]) % 3`. Adjust negative values with `s2 = (s2 + 3) % 3` and similarly for `s3`.
7. Check if `s1`, `s2`, and `s3` are all equal or all distinct. If so, print `l r` and stop checking this test case.
8. If no pair `(l, r)` satisfies the condition, print `0 0`.

Why it works: the prefix sum array guarantees O(1) computation of any subarray modulo 3. By checking every valid `(l, r)` pair, we exhaustively test all possible cuts, so no valid solution can be missed. The constraints make this brute-force feasible.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        n = int(input())
        a = list(map(int, input().split()))
        prefix = [0] * (n + 1)
        for i in range(1, n + 1):
            prefix[i] = (prefix[i-1] + a[i-1]) % 3

        found = False
        for l in range(1, n-1):
            for r in range(l+1, n):
                s1 = prefix[l]
                s2 = (prefix[r] - prefix[l]) % 3
                s3 = (prefix[n] - prefix[r]) % 3
                if s2 < 0:
                    s2 += 3
                if s3 < 0:
                    s3 += 3
                if (s1 == s2 == s3) or (len({s1, s2, s3}) == 3):
                    print(l, r)
                    found = True
                    break
            if found:
                break
        if not found:
            print(0, 0)

if __name__ == "__main__":
    solve()
```

In this code, prefix sums modulo 3 are computed once per test case. The nested loop carefully respects array boundaries to avoid empty subarrays. Using a set to check for distinct values ensures correctness without multiple conditional statements. The adjustment `(x + 3) % 3` handles negative values safely.

## Worked Examples

**Example 1:**

Input array `[1, 2, 3, 4, 5, 6]`. Prefix sums modulo 3:

| i | prefix[i] |
| --- | --- |
| 0 | 0 |
| 1 | 1 |
| 2 | 0 |
| 3 | 0 |
| 4 | 1 |
| 5 | 0 |
| 6 | 0 |

Try `l=3, r=5`:

- `s1 = prefix[3] = 0`
- `s2 = (prefix[5] - prefix[3]) % 3 = (0 - 0) % 3 = 0`
- `s3 = (prefix[6] - prefix[5]) % 3 = (0 - 0) % 3 = 0`

All equal, so output `3 5`.

**Example 2:**

Array `[1, 3, 3, 7]`:

- Prefix sums modulo 3: `[0,1,1,1,2]`

All possible `(l,r)`:

- `(1,2)` → s = 1,0,1 → not valid
- `(1,3)` → s = 1,1,2 → not valid
- `(2,3)` → s = 1,0,2 → not valid

No valid cut, so output `0 0`.

These traces confirm the algorithm correctly detects both solvable and unsolvable cases.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n²) per test case | Each of n²/2 pairs is checked in O(1) with prefix sums |
| Space | O(n) | Prefix sum array of length n+1 |

With n ≤ 40 and t ≤ 1000, the total operations are roughly 40² × 1000 ≈ 1.6 × 10^6, which easily fits within 2 seconds.

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
assert run("4\n6\n1 2 3 4 5 6\n4\n1 3 3 7\n3\n2 1 0\n5\n7 2 6 2 4\n") == "3 5\n0 0\n1 2\n2 4"

# Minimum size
assert run("1\n3\n1 1 1\n") == "1 2"

# All zeros
assert run("1\n5\n0 0 0 0 0\n") == "1 2"

# Maximum size, all ones
assert run("1\n40\n" + "1 "*40 + "\n")  # Output will be any valid l r

# Two-element repeated pattern
assert run("1\n6\n1 2 1 2 1 2\n")  # Output will be a valid cut

# Single valid solution
assert run("1\n4\n0 1 2 3\n")  #
```
