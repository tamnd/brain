---
title: "CF 1436C - Binary Search"
description: "We are asked to count permutations of size n where a particular number x is placed at a fixed index pos, and the standard binary search procedure, as described in the problem, successfully finds x at that position. A permutation here is any ordering of the numbers 1 through n."
date: "2026-06-11T04:50:17+07:00"
tags: ["codeforces", "competitive-programming", "binary-search", "combinatorics"]
categories: ["algorithms"]
codeforces_contest: 1436
codeforces_index: "C"
codeforces_contest_name: "Codeforces Round 678 (Div. 2)"
rating: 1500
weight: 1436
solve_time_s: 95
verified: true
draft: false
---

[CF 1436C - Binary Search](https://codeforces.com/problemset/problem/1436/C)

**Rating:** 1500  
**Tags:** binary search, combinatorics  
**Solve time:** 1m 35s  
**Verified:** yes  

## Solution
## Problem Understanding

We are asked to count permutations of size `n` where a particular number `x` is placed at a fixed index `pos`, and the standard binary search procedure, as described in the problem, successfully finds `x` at that position. A permutation here is any ordering of the numbers `1` through `n`. The input specifies three integers: `n` for the size of the permutation, `x` for the number we are searching, and `pos` for the index where `x` must end up. The output is the number of valid permutations modulo `10^9+7`.

The non-obvious aspect is that the binary search simulates a series of comparisons. When searching for `x`, the search maintains a left and right bound and repeatedly checks the middle element. Each comparison effectively divides the remaining array into numbers that must be smaller or larger than `x` based on the search path. So for a permutation to succeed, elements to the left of `pos` that were visited as `mid` and compared to `x` must all be smaller than `x`, and elements to the right must be larger.

Constraints are moderate: `n` can go up to 1000, which makes a brute-force approach over all `n!` permutations infeasible, but allows algorithms with cubic or even quadratic complexity.

A key edge case occurs when `x` is at an extreme index (0 or n-1). The binary search will only visit certain positions and may skip others. A naive approach that counts all permutations where `x` is at `pos` without simulating the binary search path would give incorrect results. For example, with `n=3`, `x=2`, and `pos=0`, only certain placements of the other numbers will allow binary search to succeed.

## Approaches

The brute-force approach is simple conceptually. We generate all permutations of size `n`, place `x` at `pos`, simulate the binary search on each permutation, and count successes. This approach is correct but computationally infeasible because `n!` grows rapidly, reaching 10^256 for `n=1000`.

The optimal approach comes from analyzing the binary search behavior. Every iteration of binary search at index `mid` determines whether `mid` is less than, greater than, or equal to `pos`. If `mid < pos`, the element at `mid` must be smaller than `x`. If `mid > pos`, the element must be larger than `x`. Therefore, we can count the number of elements smaller than `x` that must go into positions visited to the left of `pos` and similarly for larger elements. The remaining positions can be filled freely. This turns the problem into a combinatorial counting problem with factorials and combinations.

The insight reduces the problem from generating all permutations to counting ways to distribute smaller and larger numbers while respecting the binary search path.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n!) | O(n) | Too slow |
| Combinatorial Counting | O(n^2) | O(n) | Accepted |

## Algorithm Walkthrough

1. Precompute factorials and inverse factorials modulo 10^9+7 to allow efficient computation of permutations and combinations.
2. Initialize `left = 0` and `right = n`. This represents the binary search bounds. Track two counters: `less_needed` for numbers smaller than `x` that must appear, and `greater_needed` for numbers larger than `x` that must appear.
3. Simulate the binary search: while `left < right`, compute `mid = (left + right) // 2`. If `mid <= pos`, move `left = mid + 1` and increment `less_needed` if `mid != pos` because that index must contain a number smaller than `x`. If `mid > pos`, move `right = mid` and increment `greater_needed` because that index must contain a number larger than `x`.
4. After the loop, we know exactly how many numbers smaller than `x` need to occupy certain positions, and how many numbers larger than `x` need to occupy other positions.
5. Compute the number of ways to assign these numbers using factorials. Choose `less_needed` numbers from `x-1` smaller numbers and arrange them. Choose `greater_needed` numbers from `n-x` larger numbers and arrange them. The remaining numbers can fill the remaining positions freely.
6. Multiply these counts together and take the modulo 10^9+7 to get the final answer.

Why it works: the binary search path imposes a strict order constraint on the elements smaller and larger than `x`. By counting exactly how many smaller and larger elements must occupy positions to the left and right of `pos`, and arranging the remaining elements arbitrarily, we enumerate all valid permutations without duplicates or omissions.

## Python Solution

```python
import sys
input = sys.stdin.readline

MOD = 10**9 + 7

def modinv(a, m):
    return pow(a, m-2, m)

def precompute_factorials(n):
    fact = [1]*(n+1)
    inv_fact = [1]*(n+1)
    for i in range(1, n+1):
        fact[i] = fact[i-1]*i % MOD
    inv_fact[n] = modinv(fact[n], MOD)
    for i in range(n-1, 0, -1):
        inv_fact[i] = inv_fact[i+1]*(i+1) % MOD
    return fact, inv_fact

def solve():
    n, x, pos = map(int, input().split())
    fact, inv_fact = precompute_factorials(n)
    
    left = 0
    right = n
    less_needed = 0
    greater_needed = 0

    while left < right:
        mid = (left + right) // 2
        if mid <= pos:
            if mid != pos:
                less_needed += 1
            left = mid + 1
        else:
            greater_needed += 1
            right = mid

    if less_needed > x - 1 or greater_needed > n - x:
        print(0)
        return

    remaining = n - 1 - less_needed - greater_needed

    def comb(a, b):
        return fact[a]*inv_fact[b]%MOD*inv_fact[a-b]%MOD

    ans = comb(x-1, less_needed) * fact[less_needed] % MOD
    ans = ans * comb(n-x, greater_needed) % MOD
    ans = ans * fact[greater_needed] % MOD
    ans = ans * fact[remaining] % MOD
    print(ans % MOD)

solve()
```

The code starts by precomputing factorials and modular inverses. It then simulates binary search to count how many numbers smaller or larger than `x` must occupy specific positions. Combinatorial formulas compute the number of ways to assign these numbers, and the remaining positions are filled with the leftover numbers. Modulo arithmetic ensures values stay within bounds.

## Worked Examples

**Sample 1:** `n=4, x=1, pos=2`

| Step | left | right | mid | less_needed | greater_needed |
| --- | --- | --- | --- | --- | --- |
| 1 | 0 | 4 | 2 | 0 | 0 |
| 2 | 3 | 4 | 3 | 0 | 1 |
| 3 | 3 | 3 | - | 0 | 1 |

Remaining = 2 (positions 0 and 1). `x-1=0` smaller numbers, `n-x=3` larger numbers. We choose 1 larger number to fill greater_needed, remaining 2 numbers fill remaining. Total ways = 3_1_2 = 6.

**Sample 2:** `n=3, x=2, pos=0`

| Step | left | right | mid | less_needed | greater_needed |
| --- | --- | --- | --- | --- | --- |
| 1 | 0 | 3 | 1 | 0 | 1 |
| 2 | 0 | 1 | 0 | 0 | 1 |

Remaining = 1. Smaller numbers = 1, larger numbers = 1. Ways = 1_1_1*1=1.

These traces show the binary search simulation correctly identifies how many smaller and larger numbers must occupy forced positions.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n^2) | Precomputing factorials and inverses takes O(n), each binary search simulation is O(log n), combinatorial multiplications are O(n) each, so overall O(n^2) |
| Space | O(n) | Arrays for factorials and inverses require O(n) |

The solution fits comfortably in the constraints n ≤ 1000. Factorial calculations modulo 10^9+7 avoid integer overflow.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()
    solve()
    return sys.stdout.getvalue().strip()

# Provided samples
assert run("4 1 2\n") == "6", "sample 1"
assert run("3 2 0\n") == "1", "custom small case"

# Minimum-size input
assert run("1 1 0\n") == "1", "
```
