---
title: "CF 105048F - Word Inventing"
description: "We are given a string of length $n$. We are allowed to repeatedly apply a swap operation that exchanges characters at positions $i$ and $i+k$, as long as both indices are valid. These swaps can be performed any number of times in any order."
date: "2026-06-28T05:43:11+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105048
codeforces_index: "F"
codeforces_contest_name: "UTPC Contest 03-22-24 Div. 2 (Beginner)"
rating: 0
weight: 105048
solve_time_s: 91
verified: false
draft: false
---

[CF 105048F - Word Inventing](https://codeforces.com/problemset/problem/105048/F)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 31s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a string of length $n$. We are allowed to repeatedly apply a swap operation that exchanges characters at positions $i$ and $i+k$, as long as both indices are valid. These swaps can be performed any number of times in any order.

The task is to determine how many distinct strings can be produced from the original string by applying any sequence of these swaps. Two strings are considered different if at least one position differs.

The key structure is that swaps do not act globally. Each swap only connects positions whose indices differ by exactly $k$. This immediately suggests that indices are partitioned into independent groups based on their remainder modulo $k$.

The constraint $n \le 10^6$ implies any solution must be essentially linear or $O(n \log n)$. Anything involving enumerating permutations or BFS over states is impossible since the state space is factorial in $n$. We are forced to compress the effect of swaps into a combinatorial counting problem rather than simulate transformations.

A subtle failure case for naive reasoning is assuming that any permutation of the string is possible if enough swaps exist. For example, with $n=4, k=2$, the string “aabb” cannot produce all 4! permutations. Only positions (1,3) and (2,4) are connected, so characters can only be rearranged within those pairs. A naive global permutation model overcounts massively.

Another edge case is when $k=1$. Then every adjacent swap is allowed, which means the entire string can be permuted arbitrarily, so the answer is $n!$ divided by multiplicities of characters.

At the other extreme, when $k=n$, no swaps are possible, so only one configuration exists.

## Approaches

The brute-force approach would model each index as a node and add edges between $i$ and $i+k$. Then we would build connected components and simulate all reachable permutations within each component. Each component of size $m$ would contribute $m!$ rearrangements, but duplicates must be removed due to repeated characters. This leads to multinomial coefficients per component.

However, brute-force fails because explicitly generating all permutations inside components is exponential. Even building a state graph is infeasible since each component alone may have size $O(n)$, giving factorial growth.

The key observation is that swaps only allow arbitrary rearrangements within each connected component formed by stepping in increments of $k$. These components are exactly the residue classes modulo $\gcd(n,k)$ structure induced by the graph $i \leftrightarrow i+k$. In fact, the indices split into $k$ independent chains:

$$i, i+k, i+2k, \dots$$

within bounds. Within each chain, any permutation is achievable because adjacent swaps along the chain generate the full symmetric group on that component.

Thus the problem reduces to: for each chain, count how many distinct permutations of its multiset of characters exist. These are multinomial counts, and since chains are independent, we multiply results across all chains.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Enumeration | exponential | exponential | Too slow |
| Component + Multinomial Counting | $O(n)$ | $O(n)$ | Accepted |

## Algorithm Walkthrough

### Step 1: Partition indices into chains

We group positions by their residue modulo $k$. For each remainder $r$, consider indices $r, r+k, r+2k, \dots$. Each such group is independent because swaps never move characters between different groups. This is the fundamental decoupling of the problem.

### Step 2: Count characters in each chain

For each chain, we collect the multiset of characters appearing at those positions. Since any permutation inside the chain is reachable, the number of distinct arrangements depends only on multiplicities.

### Step 3: Compute multinomial contribution per chain

If a chain has length $m$, and character counts $c_1, c_2, \dots$, then the number of distinct permutations is:

$$\frac{m!}{\prod c_i!}$$

We compute factorials and modular inverses to evaluate this efficiently.

The reason this is valid is that swaps generate all adjacent transpositions along the chain, which generate the full symmetric group on that chain.

### Step 4: Multiply contributions

Since chains are independent, the total number of reachable strings is the product over all chains.

### Why it works

Each swap preserves the partition of indices by residue modulo $k$, so no character ever leaves its chain. Inside a chain, swaps form a connected path graph, and adjacent swaps generate all permutations of that path. Therefore each chain contributes exactly the number of permutations of its multiset, independent of other chains. Independence implies multiplication.

## Python Solution

```python
import sys
input = sys.stdin.readline

MOD = 10**9 + 7

def modinv(x):
    return pow(x, MOD - 2, MOD)

def solve():
    n, k = map(int, input().split())
    s = input().strip()

    fact = [1] * (n + 1)
    invfact = [1] * (n + 1)

    for i in range(1, n + 1):
        fact[i] = fact[i - 1] * i % MOD

    invfact[n] = modinv(fact[n])
    for i in range(n, 0, -1):
        invfact[i - 1] = invfact[i] * i % MOD

    used = [False] * n
    ans = 1

    for r in range(k):
        freq = [0] * 26
        length = 0
        i = r
        while i < n:
            freq[ord(s[i]) - 97] += 1
            length += 1
            i += k

        ways = fact[length]
        for c in freq:
            ways = ways * invfact[c] % MOD

        ans = ans * ways % MOD

    print(ans)

if __name__ == "__main__":
    solve()
```

The solution begins by precomputing factorials and inverse factorials up to $n$, since every chain requires multinomial coefficients. Modular inverses are computed using Fermat’s theorem, which is valid because the modulus is prime.

The main loop iterates over the $k$ residue classes. For each class, we walk through indices spaced by $k$, accumulating character frequencies. The multinomial formula is applied directly using factorial tables.

A common pitfall is forgetting that each chain must be processed independently; m
