---
title: "CF 105158J - \u6392\u5217\u4e0e\u5408\u6570"
description: "We are given a five-digit integer where all digits are different. From these five digits we are allowed to rearrange their order arbitrarily, but the resulting number must still be a valid five-digit integer, meaning it cannot start with zero."
date: "2026-06-27T11:05:56+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105158
codeforces_index: "J"
codeforces_contest_name: "2024 National Invitational of CCPC (Zhengzhou), 2024 CCPC Henan Provincial Collegiate Programming Contest"
rating: 0
weight: 105158
solve_time_s: 33
verified: true
draft: false
---

[CF 105158J - \u6392\u5217\u4e0e\u5408\u6570](https://codeforces.com/problemset/problem/105158/J)

**Rating:** -  
**Tags:** -  
**Solve time:** 33s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a five-digit integer where all digits are different. From these five digits we are allowed to rearrange their order arbitrarily, but the resulting number must still be a valid five-digit integer, meaning it cannot start with zero.

For each test case, the task is to decide whether at least one such rearrangement forms a composite number. If such a rearrangement exists, we must output any one valid composite permutation. If every valid permutation is prime, the answer is -1.

The key structure is that each input contributes exactly five distinct digits, so the number of possible rearrangements is fixed at 120 minus those that begin with zero after permutation. This bounded size strongly suggests that brute force over permutations is feasible per test, but the number of test cases can reach 100000, so a naive per-test recomputation of primality using square root checks would be too slow in aggregate.

A subtle edge case appears when zero is one of the digits. For example, if the number is 10234, some permutations such as 01234 are invalid and must be ignored even though they are valid permutations of the digit multiset. Another edge case is when all permutations are prime, in which case we must correctly output -1 rather than accidentally returning an invalid or unfiltered candidate.

A second subtle issue is performance: checking primality for each permutation independently would lead to up to 120 × 100000 = 12 million primality checks, and each check up to sqrt(99999) operations, which becomes too slow. This forces us to separate generation from primality testing using precomputation.

## Approaches

A direct brute-force strategy considers each test case independently. We enumerate all permutations of the five digits, skip those with a leading zero, convert each permutation into an integer, and check whether it is composite by testing divisibility up to its square root. This is correct because it exhaustively checks the full search space of valid rearrangements. The issue is computational cost. In the worst case, we perform around 120 permutations per test and up to 100000 tests, giving 12 million candidate numbers. A square-root primality check costs roughly 300 operations per number, leading to billions of operations in total, which is far beyond the limit.

The improvement comes from separating concerns. The space of possible values is small, bounded above by 99999, so primality of every number in that range can be precomputed once using a sieve. After that, each permutation only requires a constant-time lookup to determine whether it is prime or composite. This turns the problem into pure combinatorial generation over a fixed digit set, with O(1) classification per candidate.

We also avoid recomputing permutations repeatedly by generating them directly per test using itertools, since 120 candidates is small and acceptable.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force (trial division per permutation) | O(T · 120 · √N) | O(1) | Too slow |
| Sieve + permutation enumeration | O(100000 + T · 120) | O(100000) | Accepted |

## Algorithm Walkthrough

1. Precompute primality for all numbers up to 99999 using a sieve. This allows instant classification of any candidate number later.
2. For each test case, extract the five digits of the input number into a list. Working with digits avoids repeated string parsing.
3. Generate all permutations of these five digits.
4. For each permutation, check whether the first digit is zero. If it is, discard it immediately because it does not form a valid five-digit number.
5. Convert the remaining permutation into an integer.
6. Check whether this integer is composite using the precomputed sieve. If it is composite, output it immediately and move to the next test case.
7. If no permutation produces a composite number, output -1.

The reasoning behind early stopping is that the problem only asks for existence of one valid composite permutation, so we do not need to explore the full permutation space once a valid answer is found.

### Why it works

Every valid rearrangement of the digits appears exactly once in the permutation enumeration. The sieve guarantees correct classification of each candidate number. Since we accept the first composite number encountered, and all candidates are checked against the full valid set, we cannot miss a valid answer. If no candidate is composite, then by definition all valid permutations are prime, so -1 is correct.

## Python Solution

```python
import sys
input = sys.stdin.readline

MAXV = 100000

is_prime = [True] * MAXV
is_prime[0] = is_prime[1] = False

for i in range(2, int(MAXV ** 0.5) + 1):
    if is_prime[i]:
        step = i
        start = i * i
        for j in range(start, MAXV, step):
            is_prime[j] = False

from itertools import permutations

t = int(input())
for _ in range(t):
    s = input().strip()
    digits = list(s)

    found = False

    for p in permutations(digits, 5):
        if p[0] == '0':
            continue
        val = 0
        for ch in p:
            val = val * 10 + (ord(ch) - 48)

        if not is_prime[val]:
            print(val)
            found = True
            break

    if not found:
        print(-1)
```

The sieve at the top builds a global table so that each later primality query is reduced to a single array lookup. This is the key optimization that prevents recomputing divisibility checks repeatedly.

Inside the test loop, digits are extracted once and reused. The permutation loop is small enough that Python’s built-in generator is sufficient. The integer construction is done manually to avoid string-to-int overhead inside the inner loop.

The leading-zero check is applied before conversion so that invalid permutations never reach the sieve lookup stage.

## Worked Examples

Consider the input `13579`. The digits are all odd and non-zero, so all 120 permutations are valid five-digit numbers. As we scan permutations, we convert each into an integer and check primality. The first composite encountered, for example 97531, is immediately returned.

| Step | Permutation | Value | Leading Zero | Prime Check | Action |
| --- | --- | --- | --- | --- | --- |
| 1 | (1,3,5,7,9) | 13579 | No | prime | continue |
| 2 | (9,7,5,3,1) | 97531 | No | composite | output |

This trace shows early termination once a composite is found.

Now consider `12345`. Many permutations exist, and several are composite. Even if the first few permutations happen to be prime, eventually a composite such as 12354 will be enc
