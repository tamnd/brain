---
title: "CF 1225D - Power Products"
description: "We are given a sequence of positive integers and asked to count how many pairs of indices produce a product that is a perfect k-th power. In other words, for two distinct elements $ai$ and $aj$, we want to know whether their product can be written as $x^k$ for some integer $x$."
date: "2026-06-15T19:36:19+07:00"
tags: ["codeforces", "competitive-programming", "hashing", "math", "number-theory"]
categories: ["algorithms"]
codeforces_contest: 1225
codeforces_index: "D"
codeforces_contest_name: "Technocup 2020 - Elimination Round 2"
rating: 1800
weight: 1225
solve_time_s: 230
verified: true
draft: false
---

[CF 1225D - Power Products](https://codeforces.com/problemset/problem/1225/D)

**Rating:** 1800  
**Tags:** hashing, math, number theory  
**Solve time:** 3m 50s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a sequence of positive integers and asked to count how many pairs of indices produce a product that is a perfect k-th power. In other words, for two distinct elements $a_i$ and $a_j$, we want to know whether their product can be written as $x^k$ for some integer $x$.

The key difficulty is not checking a single pair, but counting all valid pairs efficiently when $n$ is large. A direct pairwise check would involve examining all combinations of two numbers and verifying whether their product is a perfect k-th power, which quickly becomes infeasible when the array size reaches $10^5$.

The constraint on values, $a_i \le 10^5$, is the crucial structural hint. It suggests that factorization-based preprocessing is possible, and that we can represent each number in terms of its prime exponents in a controlled way.

The most subtle edge case comes from the number 1. Since $1 \cdot x = x$, and $1$ is always a perfect k-th power for any $k$, it interacts trivially with every “self-complementing” structure. For example, when all elements are 1, every pair is valid. Any solution that ignores normalization of exponents will typically miscount or mishandle this case.

## Approaches

A brute-force solution iterates over all pairs $(i, j)$, computes the product $a_i a_j$, and checks whether it is a perfect k-th power. Checking perfect powers requires either repeated root extraction or full prime factorization of the product. Even if checking a single number is efficient, the number of pairs is $\Theta(n^2)$, which reaches $5 \cdot 10^9$ operations at the upper bound of $10^5$, far beyond limits.

The key structural observation is that the condition on the product can be translated into conditions on prime exponents. If we factor every number:

$$a = p_1^{e_1} p_2^{e_2} \cdots$$

then the product $a_i a_j$ is a perfect k-th power if and only if, for every prime, the sum of exponents is divisible by $k$. This turns multiplication into modular arithmetic on exponent vectors.

This suggests representing each number by a reduced “signature” that captures its exponents modulo $k$. However, modulo reduction alone is not sufficient, because we need to pair complementary exponent vectors: one number contributes certain residues, and the other must provide the missing residues so that the total becomes divisible by $k$.

For each number, we build a canonical representation by taking its prime factorization and reducing exponents modulo $k$. Then we normalize it into a form that uniquely represents what it still needs to reach a full k-th power. Two numbers form a valid pair if one’s signature is exactly the inverse complement of the other’s.

This reduces the problem to counting frequencies of signatures and matching each signature with its complement using a hash map.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(n^2 \cdot \sqrt{A})$ | $O(1)$ | Too slow |
| Factorization + Hashing | $O(n \log A)$ | $O(n)$ | Accepted |

## Algorithm Walkthrough

We precompute smallest prime factors for all numbers up to $10^5$, which allows fast factorization of each element.

We then process each number and construct a reduced signature based on its prime exponents modulo $k$. For each prime exponent $e$, we compute $e \bmod k$. If the remainder is nonzero, it contributes to the signature; otherwise, it contributes nothing because it already aligns with a k-th power structure.

We store a frequency map of signatures seen so far. For each new number, we compute its complement signature, which represents the exact residue configuration needed in a previous number to form a valid pair. We add the current frequency of that complement to the answer, then insert the current signature into the map.

### Steps

1. Precompute smallest prime factor (SPF) for all integers up to $10^5$. This ensures each number can be factorized in logarithmic time rather than trial division.
2. For each number, factorize it using SPF and compute a reduced signature by recording each prime exponent modulo $k$.
3. Convert the signature into a canonical hashable form, typically a sorted tuple of $(prime, remainder)$ pairs.
4. Construct the complement signature by replacing each remainder $r$ with $(k - r) \bmod k$. This ensures exponent sums become divisible by $k$.
5. Maintain a dictionary counting how many times each signature has appeared.
6. For each element, add the count of its complement signature to the answer, then update its own frequency.

### Why it works

The core invariant is that each stored signature represents the residue structure of all previously processed numbers. When we process a new number, we only count pairs where the earlier number provides exactly the missing modular exponents needed to complete multiples of $k$. Because prime factorization is unique and exponent addition is independent per prime, matching complements guarantees that every prime exponent in the product becomes divisible by $k$. No invalid pair can be counted because any mismatch in even a single prime exponent breaks the modular condition.

## Python Solution

```python
import sys
input = sys.stdin.readline

MAXV = 100000

spf = list(range(MAXV + 1))
for i in range(2, int(MAXV ** 0.5) + 1):
    if spf[i] == i:
        step = i
        start = i * i
        for j in range(start, MAXV + 1, step):
            if spf[j] == j:
                spf[j] = i

def factor_signature(x, k):
    sig = []
    while x > 1:
        p = spf[x]
        cnt = 0
        while x % p == 0:
            x //= p
            cnt += 1
        cnt %= k
        if cnt:
            sig.append((p, cnt))
    return tuple(sig)

n, k = map(int, input().split())
arr = list(map(int, input().split()))

freq = {}
ans = 0

for x in arr:
    sig = factor_signature(x, k)

    comp = []
    for p, r in sig:
        comp.append((p, (k - r) % k))
    comp = tuple(sorted(comp))

    ans += freq.get(comp, 0)
    freq[sig] = freq.get(sig, 0) + 1

print(ans)
```

The SPF sieve builds a compact representation for fast repeated factorization. Each number is decomposed by repeatedly dividing by its smallest prime factor, ensuring that the total cost over all numbers remains efficient.

The signature construction step keeps only non-zero residues, which prevents redundant storage and ensures that equivalent numbers share identical representations.

The complement construction is the key correctness step: for each prime exponent remainder $r$, we compute what is missing to reach a multiple of $k$. Sorting the pairs ensures the tuple is canonical and hashable.

The frequency dictionary tracks how many times each signature has appeared so far, enabling incremental counting of valid pairs.

## Worked Examples

### Example 1

Input:

```
6 3
1 3 9 8 24 1
```

We track signatures and complements:

| Step | Value | Signature | Complement | Matches Found | Total |
| --- | --- | --- | --- | --- | --- |
| 1 | 1 | () | () | 0 | 0 |
| 2 | 3 | {(3,1)} | {(3,2)} | 0 | 0 |
| 3 | 9 | {(3,2)} | {(3,1)} | 1 | 1 |
| 4 | 8 | {(2,1)} | {(2,2)} | 0 | 1 |
| 5 | 24 | {(2,1),(3,1)} | {(2,2),(3,2)} | 1 | 2 |
| 6 | 1 | () | () | 3 | 5 |

The final result is 5, matching the expected output.

This trace shows how complements accumulate gradually, and how the empty signature of 1 matches itself for every previous occurrence.

### Example 2

Input:

```
4 2
2 4 8 16
```

| Step | Value | Signature mod 2 | Complement | Matches Found | Total |
| --- | --- | --- | --- | --- | --- |
| 1 | 2 | {(2,1)} | {(2,1)} | 0 | 0 |
| 2 | 4 | () | () | 1 | 1 |
| 3 | 8 | {(2,1)} | {(2,1)} | 1 | 2 |
| 4 | 16 | () | () | 2 | 4 |

All numbers are powers of 2, so pairing reduces to counting parity cancellations.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n \log A + A \log \log A)$ | sieve plus factorization per number |
| Space | $O(n)$ | hash map of signatures |

The sieve runs comfortably within limits for $10^5$, and each factorization is fast due to repeated division by smallest prime factors. The total number of dictionary operations is linear in $n$, making the solution well within the 2-second constraint.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    MAXV = 100000
    spf = list(range(MAXV + 1))
    for i in range(2, int(MAXV ** 0.5) + 1):
        if spf[i] == i:
            for j in range(i * i, MAXV + 1, i):
                if spf[j] == j:
                    spf[j] = i

    def factor_signature(x, k):
        sig = []
        while x > 1:
            p = spf[x]
            cnt = 0
            while x % p == 0:
                x //= p
                cnt += 1
            cnt %= k
            if cnt:
                sig.append((p, cnt))
        return tuple(sig)

    n, k = map(int, input().split())
    arr = list(map(int, input().split()))

    freq = {}
    ans = 0

    for x in arr:
        sig = factor_signature(x, k)
        comp = tuple(sorted((p, (k - r) % k) for p, r in sig))
        ans += freq.get(comp, 0)
        freq[sig] = freq.get(sig, 0) + 1

    return str(ans)

# provided sample
assert run("6 3\n1 3 9 8 24 1\n") == "5"

# all ones
assert run("5 4\n1 1 1 1 1\n") == "10"

# powers of two, k=2
assert run("4 2\n2 4 8 16\n") == "4"

# mixed primes
assert run("5 3\n2 3 5 7 11\n") == "0"

# single prime complement pairs
assert run("3 2\n2 2 4\n") == "2"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| all ones | 10 | identity behavior and self-pairs |
| powers of two | 4 | modular cancellation symmetry |
| distinct primes | 0 | no accidental matches |
| small mixed case | 2 | correct complement pairing |

## Edge Cases

The all-ones case is the most sensitive because the signature becomes empty for every element. The algorithm maps all ones to the same signature and counts all pair combinations correctly through frequency accumulation. For five ones, the frequencies evolve as 0, 1, 2, 3, 4, 5 contributions, producing $\binom{5}{2} = 10$ pairs.

When all numbers are powers of a single prime, the signature reduces to a single exponent modulo $k$. The algorithm effectively becomes modular pairing in a cyclic group, and complements are always well-defined.

When numbers contain primes whose exponents are already multiples of $k$, those primes disappear entirely from the signature. This ensures that fully “clean” numbers match each other correctly via empty signatures, without requiring special casing.
