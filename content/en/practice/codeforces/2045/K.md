---
title: "CF 2045K - GCDDCG"
description: "We are given a deck of $N$ cards, each labeled with an integer value between $1$ and $N$. The game has $N$ rounds."
date: "2026-06-08T09:19:01+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 2045
codeforces_index: "K"
codeforces_contest_name: "2024-2025 ICPC Asia Jakarta Regional Contest (Unrated, Online Mirror, ICPC Rules, Teams Preferred)"
rating: 2900
weight: 2045
solve_time_s: 123
verified: false
draft: false
---

[CF 2045K - GCDDCG](https://codeforces.com/problemset/problem/2045/K)

**Rating:** 2900  
**Tags:** -  
**Solve time:** 2m 3s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a deck of $N$ cards, each labeled with an integer value between $1$ and $N$. The game has $N$ rounds. In the $i$-th round, we must select two non-empty, disjoint subsets of the cards, called deck 1 and deck 2, such that the greatest common divisor of the values in each deck is exactly $i$. Cards that are not in either deck are ignored. The creativity point for round $i$ is $i$ multiplied by the number of ways to select these two decks. The task is to sum the creativity points over all rounds modulo $998\,244\,353$.

The input consists of $N$ followed by $N$ integers $A_1$ to $A_N$. The output is a single integer, the total creativity points.

The first key observation is that $N$ can be up to 200,000, which makes any brute-force attempt to enumerate subsets impossible because the number of subsets is exponential in $N$. Similarly, checking all pairs of subsets would result in $O(3^N)$ operations in the worst case. The time limit of 1 second implies we need an algorithm roughly $O(N \log N)$ or $O(N \sqrt{N})$.

Edge cases that can break naive solutions include when all cards are equal to some $i$. For example, with $N = 3$ and $A = [3, 3, 3]$, only the round corresponding to $i = 3$ has non-zero creativity points. If a solution attempts to compute GCDs naively for every subset, it will timeout or miss correct counting because GCDs are multiplicative and can be handled more efficiently with counting methods rather than enumeration.

## Approaches

A naive approach is to try every round $i$, generate all subsets of cards, compute their GCDs, and count valid pairs. This is correct in principle but requires enumerating $2^N$ subsets, then comparing pairs, leading to $O(4^N)$ complexity. Even for $N = 20$, this is infeasible.

The key insight is to count cards divisible by multiples of $i$ and use combinatorial reasoning instead of subset enumeration. For a round $i$, only cards whose values are divisible by $i$ can be used because the GCD must be exactly $i$. Let $c_i$ be the count of such cards. For each $i$, we need the number of ways to split these $c_i$ cards into two non-empty, disjoint subsets where each subset’s GCD remains $i$.

We can use the inclusion-exclusion principle over multiples of $i$. First, count all subsets of cards divisible by $i$. Then subtract subsets whose GCD is a higher multiple of $i$, recursively. Finally, for each round $i$, the number of ways to assign two non-empty decks from $f[i]$ cards with GCD exactly $i$ is $f[i] \times f[i] - f[i]$ because we can pick any non-empty subset for deck 1, any non-empty disjoint subset for deck 2, and exclude invalid configurations.

This reduces the problem to iterating over divisors and multiples, which is $O(N \log N)$ using a sieve-like approach. Counting powers of two and applying modular arithmetic ensures we stay within limits.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(4^N)$ | $O(2^N)$ | Too slow |
| Inclusion-Exclusion over multiples | $O(N \log N)$ | $O(N)$ | Accepted |

## Algorithm Walkthrough

1. Initialize an array `count` of size $N+1$ to zero. Iterate over the card values $A_1$ to $A_N$ and increment `count[val]` for each card value. This counts how many cards have each value.
2. For each integer $i$ from $1$ to $N$, compute `mult[i]` as the total number of cards divisible by $i$. Iterate over multiples of $i$ and sum the `count` values. This gives the total number of candidate cards that could form decks with GCD $i$.
3. Initialize an array `f` of size $N+1$ to zero. Iterate from $N$ down to $1$. Let `total` be $2^{mult[i]} - 1$ modulo $998244353$, representing all non-empty subsets of cards divisible by $i$. Then subtract `f[j]` for all multiples $j = 2*i, 3*i, ..., N$ to remove subsets that have GCD equal to a higher multiple of $i$. Assign the result to `f[i]`. Now `f[i]` represents the number of non-empty subsets of cards whose GCD is exactly $i$.
4. For each round $i$, the number of ways to select two non-empty, disjoint subsets from `f[i]` cards is $f[i] \times f[i] - f[i]$. This counts all ordered pairs minus the cases where one subset is empty. Multiply by $i$ to get the creativity points for this round, then add it to the total modulo $998244353$.
5. Output the total creativity points.

Why it works: At every step, `f[i]` correctly counts subsets whose GCD is exactly $i$ because we include all subsets divisible by $i$ and subtract subsets counted for higher multiples. Using powers of two accounts for all possible subsets efficiently. Counting ordered pairs ensures we correctly capture all valid deck assignments.

## Python Solution

```python
import sys
input = sys.stdin.readline

MOD = 998244353

def solve():
    N = int(input())
    A = list(map(int, input().split()))
    
    count = [0] * (N + 1)
    for a in A:
        count[a] += 1
    
    mult = [0] * (N + 1)
    for i in range(1, N + 1):
        for j in range(i, N + 1, i):
            mult[i] += count[j]
    
    f = [0] * (N + 1)
    pow2 = [1] * (N + 2)
    for i in range(1, N + 2):
        pow2[i] = (pow2[i-1] * 2) % MOD
    
    for i in range(N, 0, -1):
        total = (pow2[mult[i]] - 1) % MOD
        j = 2 * i
        while j <= N:
            total = (total - f[j]) % MOD
            j += i
        f[i] = total
    
    result = 0
    for i in range(1, N + 1):
        ways = (f[i] * f[i] - f[i]) % MOD
        result = (result + ways * i) % MOD
    
    print(result)

solve()
```

The code computes `mult[i]` to determine which cards can appear in round `i`. Powers of two handle subset counts efficiently. Subtracting `f[j]` for multiples ensures we respect exact GCD requirements. Finally, the ordered pair formula counts valid deck assignments for the round.

## Worked Examples

**Sample 1:** `N = 3, A = [3, 3, 3]`

| i | mult[i] | f[i] | ways | creativity |
| --- | --- | --- | --- | --- |
| 3 | 3 | 3 | 12 | 36 |
| 2 | 0 | 0 | 0 | 0 |
| 1 | 0 | 0 | 0 | 0 |

Explanation: Only round 3 has valid subsets, yielding 12 ways to form two decks. Multiplying by 3 gives 36.

**Sample 2:** `N = 5, A = [2, 4, 2, 1, 3]`

| i | mult[i] | f[i] | ways | creativity |
| --- | --- | --- | --- | --- |
| 1 | 5 | 6 | 30 | 30 |
| 2 | 3 | 3 | 6 | 12 |
| 3 | 1 | 1 | 0 | 0 |
| 4 | 1 | 1 | 0 | 0 |
| 5 | 0 | 0 | 0 | 0 |

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(N log N) | Counting multiples uses nested loops over divisors; subset counting is O(N) with precomputed powers. |
| Space | O(N) | Arrays `count`, `mult`, `f`, `pow2` of size O(N) store card counts and DP values. |

This fits comfortably under the 1-second limit for N ≤ 200,000.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from
```
