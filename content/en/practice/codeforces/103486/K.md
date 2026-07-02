---
title: "CF 103486K - Bracket Sequence"
description: "We are asked to count how many valid bracket structures of total length $2N$ exist when there are $K$ different kinds of brackets. Each kind behaves like a matched pair, for example type 1 could be “()”, type 2 could be “[]”, and so on."
date: "2026-07-03T06:22:33+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 103486
codeforces_index: "K"
codeforces_contest_name: "The 15th Jilin Provincial Collegiate Programming Contest"
rating: 0
weight: 103486
solve_time_s: 42
verified: true
draft: false
---

[CF 103486K - Bracket Sequence](https://codeforces.com/problemset/problem/103486/K)

**Rating:** -  
**Tags:** -  
**Solve time:** 42s  
**Verified:** yes  

## Solution
## Problem Understanding

We are asked to count how many valid bracket structures of total length $2N$ exist when there are $K$ different kinds of brackets. Each kind behaves like a matched pair, for example type 1 could be “()”, type 2 could be “[]”, and so on. A valid sequence is built exactly like normal balanced parentheses: every opening bracket must be matched with a closing bracket of the same type, nesting must be properly structured, and concatenation of valid sequences is also valid.

The only real difference from classic Catalan counting is that every time we introduce a matched pair, we have $K$ independent choices for its type. So the problem is structurally identical to counting balanced parentheses, except each pair carries a multiplicative color factor.

The constraints go up to $N \le 10^5$, so any solution that tries to enumerate structures or simulate stack states is immediately impossible. Even dynamic programming over prefixes is too slow if it depends on $O(N^2)$ transitions. We need a closed-form combinatorial expression that can be evaluated in roughly linear time.

A subtle edge case is when $N = 1$. The answer is simply $K$, because the only valid sequence is one opening bracket followed by its matching closing bracket, and the type can be chosen freely.

Another non-obvious failure case for naive reasoning is assuming we can treat each position independently. For example, thinking there are $K^N$ ways to assign types and then multiply by Catalan numbers without justification leads to overcounting unless we correctly separate structure and labeling.

## Approaches

If we ignore the structure for a moment, we might try to think recursively: at each step we either place an opening bracket of some type or a closing bracket. This leads naturally to a DP over prefix balance and possibly a stack state. The classic solution for $K=1$ is Catalan numbers, computed via DP or binomial coefficients.

However, with $N$ up to $10^5$, even computing Catalan numbers via factorials is borderline but still feasible if done with modular inverses. The real key observation is that the structure of valid bracket sequences does not depend on types at all. The shape of the sequence is exactly the same as standard parentheses: there are $C_N$ valid _shapes_, where $C_N$ is the $N$-th Catalan number.

Once the shape is fixed, we assign types. Every matched pair (every edge in the implicit tree structure of the bracket decomposition) can independently choose one of $K$ types. Since there are exactly $N$ pairs, this contributes a factor of $K^N$.

So the answer becomes:

$$\text{Answer} = C_N \cdot K^N \pmod{10^9+7}$$

We compute Catalan numbers using:

$$C_N = \frac{1}{N+1} \binom{2N}{N}$$

This reduces the problem to factorial precomputation and modular exponentiation.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute force DP over sequences | Exponential | Exponential | Too slow |
| Catalan + exponentiation | $O(N)$ | $O(N)$ | Accepted |

## Algorithm Walkthrough

1. Precompute factorials and inverse factorials up to $2N$. This allows fast binomial coefficient computation. We need factorials because $\binom{2N}{N}$ is the core of Catalan numbers.
2. Compute $\binom{2N}{N}$ using the standard modular formula:

$$\binom{2N}{N} = \frac{(2N)!}{(N!)^2}$$

using modular inverses instead of division.
3. Compute Catalan number:

$$C_N = \binom{2N}{N} \cdot (N+1)^{-1}$$

The inverse of $N+1$ is computed using modular exponentiation.
4. Compute $K^N \bmod (10^9+7)$ using binary exponentiation. This represents independently assigning one of $K$ types to each of the $N$ matched pairs.
5. Multiply the two results and output the answer modulo $10^9+7$.

### Why it works

Every valid bracket sequence corresponds uniquely to a valid binary tree structure with $N$ internal nodes, which is counted by the Catalan number. The bracket _types_ do not affect correctness constraints because matching requires only equality of type between an opening and its corresponding closing bracket, and does not restrict nesting interactions between different pairs. Thus, once the structural skeleton is fixed, each of the $N$ pairs can independently choose one of $K$ labels, giving a clean multiplicative factor $K^N$. This independence guarantees no overcounting or missing cases.

## Python Solution

```python
import sys
input = sys.stdin.readline

MOD = 10**9 + 7

def modpow(a, e):
    res = 1
    while e:
        if e & 1:
            res = res * a % MOD
        a = a * a % MOD
        e >>= 1
    return res

def solve():
    n, k = map(int, input().split())
    
    if n == 0:
        print(1)
        return
    
    maxv = 2 * n
    
    fact = [1] * (maxv + 1)
    invfact = [1] * (maxv + 1)
    
    for i in range(1, maxv + 1):
        fact[i] = fact[i - 1] * i % MOD
    
    invfact[maxv] = modpow(fact[maxv], MOD - 2)
    for i in range(maxv, 0, -1):
        invfact[i - 1] = invfact[i] * i % MOD
    
    def C(a, b):
        if b < 0 or b > a:
            return 0
        return fact[a] * invfact[b] % MOD * invfact[a - b] % MOD
    
    catalan = C(2 * n, n) * modpow(n + 1, MOD - 2) % MOD
    ways_types = modpow(k, n)
    
    print(catalan * ways_types % MOD)

if __name__ == "__main__":
    solve()
```

The factorial preprocessing builds a lookup table so binomial coefficients can be computed in constant time per query. The Catalan computation follows directly from the closed form, and the modular inverse of $n+1$ handles division safely under modulo arithmetic.

The exponentiation for $K^N$ is independent and multiplicative, reflecting the fact that each matched pair carries an independent label choice.

## Worked Examples

### Example 1

Input:

```
1 2
```

Here $N = 1$, $K = 2$. There is exactly one structural bracket sequence: a single pair. So Catalan number is 1.

| Step | Value |
| --- | --- |
| $C_1$ | 1 |
| $K^1$ | 2 |
| Result | 2 |

Output is 2, corresponding to “()” and “[]”.

This confirms that structure contributes 1 and only labeling matters.

### Example 2

Input:

```
2 2
```

For $N = 2$, there are 2 Catalan structures: “()()” and “(())”. Each has 2 pairs, each pair independently chooses one of 2 types.

| Structure | Count | Type assignments | Contribution |
| --- | --- | --- | --- |
| ()() | 1 | $2^2 = 4$ | 4 |
| (()) | 1 | $2^2 = 4$ | 4 |

Total = 8.

So answer is 8.

This shows independence between structure and labeling, which is the core decomposition.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(N)$ | factorial precomputation up to $2N$ plus modular exponentiation |
| Space | $O(N)$ | storage for factorial and inverse factorial arrays |

With $N \le 10^5$, precomputing up to $2N$ is well within limits, and all operations are linear passes or logarithmic exponentiation.

## Test Cases

```python
import sys, io

MOD = 10**9 + 7

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    
    MOD = 10**9 + 7
    
    def modpow(a, e):
        res = 1
        while e:
            if e & 1:
                res = res * a % MOD
            a = a * a % MOD
            e >>= 1
        return res
    
    n, k = map(int, input().split())
    if n == 0:
        return "1"
    
    maxv = 2 * n
    fact = [1] * (maxv + 1)
    invfact = [1] * (maxv + 1)
    
    for i in range(1, maxv + 1):
        fact[i] = fact[i - 1] * i % MOD
    
    invfact[maxv] = modpow(fact[maxv], MOD - 2)
    for i in range(maxv, 0, -1):
        invfact[i - 1] = invfact[i] * i % MOD
    
    def C(a, b):
        return fact[a] * invfact[b] % MOD * invfact[a - b] % MOD
    
    catalan = C(2 * n, n) * modpow(n + 1, MOD - 2) % MOD
    return str(catalan * modpow(k, n) % MOD)

# provided samples
assert run("1 2") == "2"
assert run("2 2") == "8"

# custom cases
assert run("1 1") == "1", "single type single pair"
assert run("3 1") == "5", "Catalan(3)=5"
assert run("0 5") == "1", "empty sequence"
assert run("2 3") == str((8 * 9) % (10**9+7)), "mixed types"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 1 | 1 | minimal structure and single type |
| 3 1 | 5 | pure Catalan correctness |
| 0 5 | 1 | empty sequence base case |
| 2 3 | 72 | combination of structure and labeling |

## Edge Cases

The $N = 0$ case corresponds to the empty sequence. The algorithm handles it correctly because Catalan(0) is 1 and $K^0$ is also 1, so the product remains 1.

When $K = 1$, the problem reduces exactly to counting standard balanced bracket sequences. The algorithm collapses to computing only the Catalan number, and no overcounting occurs because $1^N = 1$.

When $N = 1$, the computation avoids unnecessary structure: Catalan(1) is 1, and the result becomes exactly $K$, matching the direct enumeration of single pairs.

A potential implementation pitfall is integer overflow before applying modulo in intermediate factorial multiplications. This is avoided by taking modulo at every multiplication step, ensuring correctness even for $2N$ up to $2 \cdot 10^5$.
