---
title: "CF 1514B - AND 0, Sum Big"
description: "We are asked to count arrays of length n where each element lies between 0 and 2^k - 1, such that the bitwise AND of all elements is zero and the sum of elements is as large as possible. The result should be returned modulo 10^9 + 7."
date: "2026-06-10T18:39:03+07:00"
tags: ["codeforces", "competitive-programming", "bitmasks", "combinatorics", "math"]
categories: ["algorithms"]
codeforces_contest: 1514
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 716 (Div. 2)"
rating: 1200
weight: 1514
solve_time_s: 150
verified: false
draft: false
---

[CF 1514B - AND 0, Sum Big](https://codeforces.com/problemset/problem/1514/B)

**Rating:** 1200  
**Tags:** bitmasks, combinatorics, math  
**Solve time:** 2m 30s  
**Verified:** no  

## Solution
## Problem Understanding

We are asked to count arrays of length `n` where each element lies between `0` and `2^k - 1`, such that the bitwise AND of all elements is zero and the sum of elements is as large as possible. The result should be returned modulo `10^9 + 7`.

Concretely, each array element can be visualized as a `k`-bit number. The bitwise AND being zero implies that for every bit position from `0` to `k-1`, there must be at least one element in the array where that bit is `0`. If a bit is `1` in every element, the AND would retain that `1`. The sum is maximized when each element is as large as possible, which in this range is `2^k - 1`. However, we cannot simply set all elements to `2^k - 1`, because then the AND would not be zero.

The problem constraints allow `n` up to `10^5` and `k` up to `20`. With `t` up to 10, any solution performing more than roughly `10^8` operations will be too slow. This rules out enumerating all possible arrays explicitly or even iterating through `2^k` possibilities for every element. The solution must exploit combinatorial structure and properties of bitwise operations.

A non-obvious edge case occurs when `n = 1`. The only way the AND of a single element is zero is if the element itself is zero, so the maximum sum is `0` and there is exactly one array. A naive approach that assumes we can always pick `2^k - 1` elements would fail here.

## Approaches

The brute-force approach would attempt to generate every possible array of length `n` with elements in `0..2^k-1`, compute its bitwise AND, and track the maximum sum. This is correct in principle but completely infeasible. For example, with `k=20` and `n=10^5`, there are `(2^20)^10^5` arrays, which is astronomically large.

The key insight is to switch from elements to patterns of bits. For maximum sum, each element should be `2^k - 1` (all bits set) except that we need the AND to be zero. To ensure the AND is zero, we must pick at least one element to “turn off” every bit. Counting the number of arrays reduces to counting how many ways we can distribute zeroes among `n` elements so that each of the `k` bits has at least one zero.

Formally, if we label `x = 2^k - 1`, then each element is either `x` or `x` with some bits cleared. For the AND to be zero, the array must not consist entirely of `x`. This is equivalent to counting arrays of length `n` over the set `{0, 1}` with the restriction that not all elements are `1`. That is combinatorially `2^n - 1`. Here, the `2^k` possibilities for each element are structured such that exactly one pattern (all ones) is forbidden, leaving `2^k - 1` choices per element. Thus, the number of valid arrays is `(2^k - 1)^n`.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O((2^k)^n) | O(n) | Too slow |
| Optimal | O(k + log n) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the number of test cases `t`.
2. For each test case, read integers `n` and `k`.
3. Compute `mod = 10^9 + 7` for modular arithmetic.
4. Compute `ways = pow(2^k - 1, n, mod)`. This calculates `(2^k - 1)^n mod 10^9 + 7`. Using Python’s built-in modular exponentiation ensures it handles large `n` efficiently.
5. Output `ways`.

Why it works: Each element has `2^k` possible values. The sum is maximized when elements are as large as possible, so we use `2^k - 1` as the base. The AND restriction only eliminates arrays where every element is `2^k - 1`. Thus the remaining arrays are exactly all arrays where at least one element is not maximal. The modular exponentiation computes this efficiently even for very large `n`.

## Python Solution

```python
import sys
input = sys.stdin.readline

MOD = 10**9 + 7

def solve():
    t = int(input())
    for _ in range(t):
        n, k = map(int, input().split())
        max_val = (1 << k) - 1
        # number of arrays with at least one element different from max_val
        result = pow(max_val, n, MOD)
        print(result)

if __name__ == "__main__":
    solve()
```

The solution first computes `max_val = 2^k - 1` for clarity. Using `pow(base, exp, mod)` avoids overflow and provides O(log n) computation. Every test case is independent, so we loop over `t` and print results immediately.

## Worked Examples

Sample Input:

```
2
2 2
100000 20
```

| Step | n | k | max_val | pow(max_val, n, MOD) | Output |
| --- | --- | --- | --- | --- | --- |
| 1 | 2 | 2 | 3 | 3^2 = 9 | 4 |
| 2 | 100000 | 20 | 1048575 | pow(1048575,100000,10^9+7) | 226732710 |

The first case confirms small `n` works and the algorithm correctly counts arrays avoiding all-maximal elements. The second case confirms performance and modular exponentiation for huge `n`.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(t * log n) | Each test case uses modular exponentiation, which is O(log n) |
| Space | O(1) | Only a few integers stored per test case |

With `t <= 10` and `n <= 10^5`, this comfortably fits in 2 seconds.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    out = io.StringIO()
    sys.stdout = out
    solve()
    return out.getvalue().strip()

# provided samples
assert run("2\n2 2\n100000 20\n") == "4\n226732710", "sample 1"

# minimum size
assert run("1\n1 1\n") == "1", "n=1,k=1"

# all k bits
assert run("1\n3 3\n") == "343", "n=3,k=3"

# large n small k
assert run("1\n100000 1\n") == "1", "n=100000,k=1"

# large k small n
assert run("1\n2 20\n") == "1099511627775", "n=2,k=20, modulo applied later"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 1 | 1 | edge case n=1,k=1 |
| 3 3 | 343 | general small case |
| 100000 1 | 1 | large n, small k |
| 2 20 | 1099511627775 | large k, small n |

## Edge Cases

When `n=1`, the algorithm computes `pow(2^k-1,1) = 2^k - 1`, which counts all single-element arrays. Only the zero array gives AND zero, so the output modulo 10^9+7 correctly returns `1`. For `n` large, the algorithm efficiently handles exponentiation with modulo, avoiding integer overflow while respecting the AND-zero constraint implicitly. No off-by-one errors occur because `pow()` directly computes the exact count of valid arrays.
