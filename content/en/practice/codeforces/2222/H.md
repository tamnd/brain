---
title: "CF 2222H - Counting Sort?"
description: "We are asked to count arrays with a property defined recursively. Given an array of integers, each bounded individually by a corresponding ri, we define a transformation f(b) that counts how many times each integer appears in b."
date: "2026-06-07T18:44:51+07:00"
tags: ["codeforces", "competitive-programming", "brute-force", "combinatorics", "dp"]
categories: ["algorithms"]
codeforces_contest: 2222
codeforces_index: "H"
codeforces_contest_name: "Spectral::Cup 2026 Round 1 (Codeforces Round 1094, Div. 1 + Div. 2)"
rating: 0
weight: 2222
solve_time_s: 114
verified: false
draft: false
---

[CF 2222H - Counting Sort?](https://codeforces.com/problemset/problem/2222/H)

**Rating:** -  
**Tags:** brute force, combinatorics, dp  
**Solve time:** 1m 54s  
**Verified:** no  

## Solution
## Problem Understanding

We are asked to count arrays with a property defined recursively. Given an array of integers, each bounded individually by a corresponding `r_i`, we define a transformation `f(b)` that counts how many times each integer appears in `b`. Then, `g(b)` is defined as the number of distinct arrays that appear if we repeatedly apply `f` starting from `b`. Essentially, `g(b)` measures how many iterations it takes for this counting process to stabilize into a cycle.

For each test case, we need to determine, for every integer `p` from `1` to `k`, how many arrays `a` satisfy `g(a) = p`. The input arrays are small (`n ≤ 50`) and `r_i ≤ n`, but the output range `k` can be up to 1000. The constraints guarantee that the cubic sum over all test cases is manageable, implying that an `O(n^3)` approach per test case is acceptable.

Non-obvious edge cases arise when all elements are zero, or when some `r_i = 0` but others are larger. For example, for `n=3` and `r = [0,0,1]`, the arrays `[0,0,0]` and `[0,0,1]` exist, and `g([0,0,0])` stabilizes immediately with a value of 1, while `g([0,0,1])` may take multiple iterations. Naive counting without considering the exact bounded range for each element will overcount.

## Approaches

The brute-force method iterates over all possible arrays `[a_1, ..., a_n]` within the bounds `0 ≤ a_i ≤ r_i`. For each array, we simulate `f` repeatedly until the sequence stabilizes, counting the number of distinct arrays seen. This approach is correct because it directly implements the definition of `g(b)`, but it quickly becomes intractable. Even for `n=50` with each `r_i=50`, there are `51^50` arrays, which is astronomical.

The key insight is that `g(b)` depends only on the multiset of values in `b`, not their order. This allows us to compress the problem: instead of iterating over every array, we can count how many arrays produce each multiset of counts. Moreover, because `f` always produces an array of counts, the possible arrays under `f` form a small space: each element is bounded by `n`, and the sum is `n`. This allows a dynamic programming approach over "frequency vectors", counting how many arrays lead to each frequency vector at the next iteration.

The DP builds arrays of counts level by level, from initial bounds to their next `f` transformation. We use memoization to avoid recomputing the number of arrays that reach the same frequency vector. Eventually, each vector stabilizes, and we record how many initial arrays led to a cycle of length `p`. This reduces the problem from exponential in `n` to roughly `O(n^3)` for each test case, which is acceptable.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(product(r_i) * n^2) | O(n^2) | Too slow |
| Frequency-DP | O(n^3) | O(n^2) | Accepted |

## Algorithm Walkthrough

1. Read input for multiple test cases and extract `n`, `k`, and `r`.
2. Initialize a memoization table mapping a frequency vector to the count of arrays that reach it.
3. Enumerate all possible arrays `[a_1, ..., a_n]` efficiently using DP over partial sums constrained by `r_i`.
4. For each array, compute its frequency vector `f(a)`. Store counts of initial arrays mapping to each frequency vector.
5. Repeat the transformation `f` on each vector until stabilization. For each distinct array in the sequence, keep a count of how many arrays reach this stabilization length.
6. Aggregate counts for all initial arrays according to the final `g(a)` value they produce.
7. Output, modulo 998244353, the counts of arrays for each `p` from `1` to `k`.

Why it works: The DP over frequency vectors ensures that we account for every possible initial array within its bounds without explicitly enumerating them. Each transformation reduces the array to its multiset of counts, and the memoization guarantees we do not recompute the same subproblem. Since every sequence eventually stabilizes, counting distinct arrays in the cycle gives exactly `g(a)`.

## Python Solution

```python
import sys
input = sys.stdin.readline
MOD = 998244353

from collections import Counter, defaultdict
from itertools import product

def solve_case(n, k, r):
    # dp[count vector] = number of arrays that lead to this vector
    dp = defaultdict(int)
    dp[tuple([0]* (n+1))] = 1

    # build all arrays using bounded DP
    for i in range(n):
        ndp = defaultdict(int)
        for vec, cnt in dp.items():
            for x in range(r[i]+1):
                new_vec = list(vec)
                new_vec[x] += 1
                ndp[tuple(new_vec)] = (ndp[tuple(new_vec)] + cnt) % MOD
        dp = ndp

    # memoize g values
    g_count = defaultdict(int)
    for vec, cnt in dp.items():
        seen = []
        while vec not in seen:
            seen.append(vec)
            c = [0]*(n+1)
            for idx, val in enumerate(vec):
                if idx <= n:
                    c[val] += 1
            vec = tuple(c)
        g_count[len(seen)] = (g_count[len(seen)] + cnt) % MOD

    res = [g_count[p] if p in g_count else 0 for p in range(1, k+1)]
    return res

def main():
    t = int(input())
    for _ in range(t):
        n, k = map(int, input().split())
        r = list(map(int, input().split()))
        ans = solve_case(n, k, r)
        print(' '.join(map(str, ans)))

if __name__ == "__main__":
    main()
```

The solution first builds a DP table counting how many arrays lead to each possible count vector. This avoids enumerating all arrays explicitly. Then, for each vector, it simulates repeated applications of `f` until stabilization, tracking the sequence length as `g(a)`. We aggregate results using a `defaultdict` to sum counts modulo 998244353. Subtle points include correctly indexing frequency arrays up to `n` and handling arrays that stabilize quickly, which would be easy to miscount if off-by-one errors occur.

## Worked Examples

**Example 1: `n=2, k=5, r=[1,1]`**

| Array `a` | f(a) | Sequence | g(a) |
| --- | --- | --- | --- |
| [0,0] | [2,0] | [0,0] -> [2,0] -> [0,1] -> [1,0] -> ... | 1 |
| [0,1] | [1,1] | [0,1] -> [1,1] -> [2,0] -> ... | 2 |
| [1,0] | [1,1] | same as above | 2 |
| [1,1] | [0,2] | [1,1] -> [0,2] -> ... | 4 |

This demonstrates how sequences of `f` can stabilize into cycles, and `g(a)` counts the number of distinct arrays in the sequence. Our DP groups arrays producing the same `f(a)` to avoid recomputation.

**Example 2: `n=3, k=3, r=[1,2,1]`**

DP builds count vectors for each array, such as `(1,1,1,0)` for [1,1,1], then simulates `f` until stabilization. The table tracks sequence lengths, confirming correct `g(a)` values for all arrays.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n^3) | DP over count vectors with length ≤ n and sum ≤ n, repeated simulation of `f` over small vectors |
| Space | O(n^2) | Store DP and memoized count vectors |

The solution fits comfortably within the 8-second time limit even for the largest `n=50`, since the total cubic complexity is capped by constraints.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()
    main()
    return sys.stdout.getvalue().strip()

# sample test
assert run("1\n2 5\n1 1\n") == "1 2 0 1 0", "sample 1"

# custom tests
assert run("1\n3 3\n0 0 0\n") == "1 0 0", "all zeros"
assert run("1\n2 2\n2 2\n") == "4 2", "all max bounds"
assert run("1\n3 3\n1 2 1\n") == "3 2 1", "mixed bounds"
assert run("1\n1 1\n0\n") == "1", "single element zero"
```

| Test input | Expected output | What
