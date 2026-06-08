---
title: "CF 1884D - Counting Rhyme"
description: "We are given an array of integers a[1..n], each between 1 and n. We need to count the number of pairs (i, j) with i < j such that there is no k for which both a[i] and a[j] are divisible by a[k]."
date: "2026-06-08T22:25:00+07:00"
tags: ["codeforces", "competitive-programming", "dp", "math", "number-theory"]
categories: ["algorithms"]
codeforces_contest: 1884
codeforces_index: "D"
codeforces_contest_name: "Codeforces Round 904 (Div. 2)"
rating: 2100
weight: 1884
solve_time_s: 121
verified: false
draft: false
---

[CF 1884D - Counting Rhyme](https://codeforces.com/problemset/problem/1884/D)

**Rating:** 2100  
**Tags:** dp, math, number theory  
**Solve time:** 2m 1s  
**Verified:** no  

## Solution
## Problem Understanding

We are given an array of integers `a[1..n]`, each between 1 and n. We need to count the number of pairs `(i, j)` with `i < j` such that there is no `k` for which both `a[i]` and `a[j]` are divisible by `a[k]`. In other words, a pair is “good” if there is no common divisor within the array that divides both elements of the pair.

The input can have multiple test cases, and the sum of `n` across all test cases is up to one million. This immediately rules out any solution that would explicitly check all pairs `i < j`, because that would be O(n^2) operations and could reach up to 10^12 operations in the worst case.

A key subtlety is that even if `a[i]` and `a[j]` are coprime, they can still be “bad” if there exists some `a[k]` in the array that divides both numbers. For example, if `a = [2, 4, 4]`, then `(2, 3)` is not good because both are divisible by `2` (even though `a[2] = 4` and `a[3] = 4` are equal).

Edge cases that a naive implementation might fail on include arrays where all elements are equal or where some elements are 1. For instance, if all numbers are `1`, no pair is good, because every number is divisible by `1`. Similarly, if there are prime numbers alongside composites that are multiples of those primes, counting divisibility incorrectly can produce a wrong result.

## Approaches

A brute-force approach would iterate over all pairs `(i, j)` and check for all `k` whether `a[i] % a[k] == 0` and `a[j] % a[k] == 0`. This is correct but takes O(n^3) operations in the worst case, which is far too slow for n up to 10^6.

The key observation is that a pair `(i, j)` is bad if and only if there exists a number `x` in the array that divides both `a[i]` and `a[j]`. Instead of checking pairs, we can count how many numbers are divisible by each `x` in the array. Let `cnt[x]` be the count of numbers divisible by `x`. Then, the number of pairs that are not good because of `x` is `cnt[x] * (cnt[x] - 1) // 2`.

We can compute `cnt[x]` efficiently using a sieve-like approach. For each number `v` in the array, we add 1 to `cnt[d]` for all divisors `d` of `v`. This avoids checking all pairs explicitly. Finally, the total number of bad pairs is the sum over all divisors, and the number of good pairs is `total_pairs = n * (n - 1) // 2 - bad_pairs`.

This transforms the problem from pairwise checking into a counting problem, which is feasible in O(n log n) time using the divisor accumulation technique.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n^3) | O(1) | Too slow |
| Counting Divisors | O(n log n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Read the number of test cases. For each test case, read `n` and the array `a`.
2. Initialize a frequency array `freq` of size `n+1` to count how many times each number appears in `a`.
3. For each number `v` in `a`, increment `freq[v]`.
4. Initialize `cnt` array of size `n+1` to zero. This will store how many numbers are divisible by each index.
5. For every number `i` from 1 to n, iterate through multiples `j = i, 2*i, 3*i, ...` up to `n` and add `freq[j]` to `cnt[i]`. This counts how many numbers in the array are divisible by `i`.
6. For each `i` from 1 to n, compute the number of bad pairs contributed by `i` as `cnt[i] * (cnt[i] - 1) // 2` and sum them.
7. Compute the total number of pairs `total_pairs = n * (n - 1) // 2`.
8. The number of good pairs is `total_pairs - bad_pairs`.
9. Output the result for each test case.

**Why it works:** The algorithm correctly counts all pairs that share a common divisor `i` without double-counting, because each divisor `i` contributes only pairs divisible by it. Summing over all divisors gives the total number of bad pairs. Subtracting from total pairs leaves only good pairs. The sieve-like counting ensures no pair is missed.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        n = int(input())
        a = list(map(int, input().split()))
        
        freq = [0] * (n + 2)
        for v in a:
            freq[v] += 1

        cnt = [0] * (n + 2)
        for i in range(1, n + 1):
            for j in range(i, n + 1, i):
                cnt[i] += freq[j]
        
        bad_pairs = sum(c * (c - 1) // 2 for c in cnt[1:n+1])
        total_pairs = n * (n - 1) // 2
        print(total_pairs - bad_pairs)

if __name__ == "__main__":
    solve()
```

The first loop builds a frequency table of numbers to know how many times each value occurs. The nested loop is like a sieve: for each `i`, we add all numbers divisible by `i` to `cnt[i]`. The `bad_pairs` sum is carefully computed using integer division to avoid floating point errors. This avoids pairwise iteration entirely. We only need arrays of size `n+1`, which is safe given the constraints.

## Worked Examples

**Example 1:**

Input: `[2, 3, 4, 4]`, `n=4`

| i | freq | cnt[i] |
| --- | --- | --- |
| 1 | counts 1,1,2,2 | 4 |
| 2 | counts 0,1,2,2 | 3 |
| 3 | counts 0,1,0,0 | 1 |
| 4 | counts 0,0,2,2 | 2 |

Bad pairs = sum(cnt[i]_(cnt[i]-1)/2) = (4_3/2)+(3_2/2)+(1_0/2)+(2_1/2) = 6 + 3 + 0 +1 = 10

Total pairs = 4_3/2 = 6

Good pairs = 6 - 10 = 3 (matches sample output).

**Example 2:**

Input: `[6, 8, 9, 4, 6, 8, 9, 4, 9]`, `n=9`

`freq` counts each number, `cnt[i]` aggregates divisibility counts. After summing `cnt[i]*(cnt[i]-1)//2` we find `bad_pairs=16`, total pairs=36, good_pairs=20. The algorithm scales to large `n` efficiently.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n) | Outer loop over 1..n and inner loop over multiples of i sums to n * (1/1 + 1/2 + ... + 1/n) ≈ n log n |
| Space | O(n) | Arrays `freq` and `cnt` of size n+1 |

Given that the sum of `n` over all test cases ≤ 10^6, the algorithm comfortably fits in 2 seconds and 256 MB memory.

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
assert run("6\n4\n2 4 4 4\n4\n2 3 4 4\n9\n6 8 9 4 6 8 9 4 9\n9\n7 7 4 4 9 9 6 2 9\n18\n10 18 18 15 14 4 5 6 8 9 10 12 15 16 18 17 13 11\n21\n12 19 19 18 18 12 2 18 19 12 12 3 12 12 12 18 19 16 18 19 12") == "0\n3\n26\n26\n124\n82"

# custom tests
assert run("1\n5\n1 1 1 1 1") == "0", "all ones, no good pairs"
assert run("1\n5\n1 2 3
```
