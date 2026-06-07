---
title: "CF 2126E - G-C-D, Unlucky!"
description: "We are given two arrays of integers, p and s, each of length n. Array p represents the prefix GCDs of some unknown array a, and array s represents the suffix GCDs of the same array. The task is to decide whether such an array a exists."
date: "2026-06-08T03:23:06+07:00"
tags: ["codeforces", "competitive-programming", "math", "number-theory"]
categories: ["algorithms"]
codeforces_contest: 2126
codeforces_index: "E"
codeforces_contest_name: "Codeforces Round 1037 (Div. 3)"
rating: 1400
weight: 2126
solve_time_s: 78
verified: true
draft: false
---

[CF 2126E - G-C-D, Unlucky!](https://codeforces.com/problemset/problem/2126/E)

**Rating:** 1400  
**Tags:** math, number theory  
**Solve time:** 1m 18s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given two arrays of integers, `p` and `s`, each of length `n`. Array `p` represents the prefix GCDs of some unknown array `a`, and array `s` represents the suffix GCDs of the same array. The task is to decide whether such an array `a` exists. Formally, if `a` exists, then for every index `i`:

```
p[i] = gcd(a[1], a[2], ..., a[i])
s[i] = gcd(a[i], a[i+1], ..., a[n])
```

The input consists of up to 10^4 test cases, and the sum of all `n` values across test cases is at most 10^5. This means we must process each test case efficiently in roughly O(n) time, because anything O(n^2) would be too slow.

The non-obvious part of the problem comes from the constraints on GCD propagation. For example, the prefix GCD array `p` must be non-increasing up to the first element that is 1. Similarly, `s` must be non-increasing from the last element backward. A naive approach might attempt to reconstruct all candidate arrays `a` and check if they generate the given `p` and `s`, but this is infeasible for large `n`. Small edge cases include arrays where all `p` values are equal or all `s` values are equal, and arrays with `1` in them which affects GCD propagation. For instance, if `p = [2, 2, 2]` and `s = [2, 2, 1]`, the answer is "No" because there is no single array that satisfies both the prefix and suffix GCDs at all positions.

## Approaches

The brute-force approach would attempt to try every possible array `a` consistent with `p` and `s`. At each position `i`, we could try any integer divisible by `p[i]` and `s[i]` while satisfying the running prefix and suffix GCDs. This would be correct in principle but extremely slow, because the number of possible arrays grows combinatorially with `n`. With `n` up to 10^5, this approach is not practical.

The key insight is that the value at position `i` in array `a` must be a multiple of both the previous prefix GCD (or `p[i]` itself) and the subsequent suffix GCD (or `s[i]`). Concretely, we can define `a[i]` as the least common multiple (LCM) of `p[i]` and `s[i]`. Since `p[i]` divides the prefix GCD and `s[i]` divides the suffix GCD, choosing `a[i] = lcm(p[i], s[i])` ensures that both GCDs are preserved at that position. After constructing this candidate array, we can recompute prefix and suffix GCDs and verify that they match `p` and `s`. This reduces the problem to a linear scan with simple arithmetic at each step.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(2^n) | O(n) | Too slow |
| Optimal | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Initialize a candidate array `a` of length `n`. For each index `i`, set `a[i] = lcm(p[i], s[i])`. The reasoning is that this is the minimal number divisible by both `p[i]` and `s[i]`, which preserves the necessary divisibility for prefix and suffix GCDs.
2. Compute the prefix GCD array `p_check` from `a`. Start with `p_check[0] = a[0]`, then for each `i` from 1 to `n-1`, set `p_check[i] = gcd(p_check[i-1], a[i])`.
3. Compute the suffix GCD array `s_check` from `a`. Start with `s_check[n-1] = a[n-1]`, then for each `i` from `n-2` down to 0, set `s_check[i] = gcd(s_check[i+1], a[i])`.
4. Compare `p_check` with `p` and `s_check` with `s`. If both arrays match exactly, print "YES"; otherwise, print "NO".

Why it works: The invariant is that `lcm(p[i], s[i])` is divisible by both the prefix and suffix GCDs at index `i`. Because GCD is associative and commutative, if the candidate array preserves divisibility at each position, the recomputed prefix and suffix GCDs will match the original arrays only if a valid array exists. Any discrepancy indicates that no such array can satisfy both `p` and `s` simultaneously.

## Python Solution

```python
import sys
import math
input = sys.stdin.readline

def main():
    t = int(input())
    for _ in range(t):
        n = int(input())
        p = list(map(int, input().split()))
        s = list(map(int, input().split()))
        a = [0] * n
        for i in range(n):
            a[i] = (p[i] * s[i]) // math.gcd(p[i], s[i])
        p_check = [0] * n
        s_check = [0] * n
        p_check[0] = a[0]
        for i in range(1, n):
            p_check[i] = math.gcd(p_check[i-1], a[i])
        s_check[-1] = a[-1]
        for i in range(n-2, -1, -1):
            s_check[i] = math.gcd(s_check[i+1], a[i])
        if p_check == p and s_check == s:
            print("YES")
        else:
            print("NO")

if __name__ == "__main__":
    main()
```

The solution constructs the candidate array using LCM, then verifies prefix and suffix GCDs. We use integer division to compute the LCM efficiently and avoid floating-point errors. Boundary conditions such as arrays of length 1 or values equal to 1 are naturally handled because `lcm(x, x) = x` and `gcd(x, x) = x`.

## Worked Examples

**Sample 1**

Input:

```
6
72 24 3 3 3 3
3 3 3 6 12 144
```

| i | p[i] | s[i] | a[i] = lcm(p[i], s[i]) | prefix GCD | suffix GCD |
| --- | --- | --- | --- | --- | --- |
| 0 | 72 | 3 | 72 | 72 | 3 |
| 1 | 24 | 3 | 24 | 24 | 3 |
| 2 | 3 | 3 | 3 | 3 | 3 |
| 3 | 3 | 6 | 6 | 3 | 6 |
| 4 | 3 | 12 | 12 | 3 | 12 |
| 5 | 3 | 144 | 144 | 3 | 144 |

After computing prefix and suffix GCDs, both match the input arrays. Output: YES.

**Sample 2**

Input:

```
1 2 3
4 5 6
```

Calculating `a[i] = lcm(p[i], s[i])` gives `[4, 10, 6]`. Prefix GCDs: `[4, 2, 2]` do not match `[1, 2, 3]`. Output: NO. This demonstrates that the LCM-based candidate preserves divisibility constraints, and mismatch detects impossibility.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) per test case | Constructing candidate array and computing prefix/suffix GCDs are linear in `n`. |
| Space | O(n) per test case | We store arrays `a`, `p_check`, and `s_check`. |

Given the sum of all `n` ≤ 10^5, the total operations are roughly 3 × 10^5 per test run, comfortably under the 2-second limit.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from contextlib import redirect_stdout
    f = io.StringIO()
    with redirect_stdout(f):
        main()
    return f.getvalue().strip()

# provided samples
assert run("""5
6
72 24 3 3 3 3
3 3 3 6 12 144
3
1 2 3
4 5 6
5
125 125 125 25 25
25 25 25 25 75
4
123 421 282 251
125 1981 239 223
3
124 521 125
125 121 121
""") == "YES\nNO\nYES\nNO\nNO", "provided samples"

# custom cases
assert run("""1
1
10
10
""") == "YES", "single element, equal"

assert run("""1
3
5 5
```
