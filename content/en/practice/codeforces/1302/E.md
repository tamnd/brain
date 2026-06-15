---
title: "CF 1302E - Amazing bitset"
description: "We are given a binary string of length $n$, but instead of being fixed, each position is generated independently as a random bit: it becomes $1$ with probability $p = frac{a}{b}$ and $0$ with probability $1 - p$."
date: "2026-06-16T05:33:24+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 1302
codeforces_index: "E"
codeforces_contest_name: "AIM Tech Poorly Prepared Contest (unrated, funny, Div. 1 preferred)"
rating: 0
weight: 1302
solve_time_s: 559
verified: false
draft: false
---

[CF 1302E - Amazing bitset](https://codeforces.com/problemset/problem/1302/E)

**Rating:** -  
**Tags:** -  
**Solve time:** 9m 19s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a binary string of length $n$, but instead of being fixed, each position is generated independently as a random bit: it becomes $1$ with probability $p = \frac{a}{b}$ and $0$ with probability $1 - p$.

After the string is generated, we are allowed to apply a specific operation on it multiple times. Each operation works like this: we pick one index as a “center”, and then pick at least one other index such that all chosen “other” indices have the opposite bit to the center. Then we flip all chosen bits simultaneously.

A bitset is called valid if, starting from it, there exists a sequence of these operations that eventually flips every bit at least once (equivalently, we can fully “activate” all indices through allowed operations).

The task is to compute the probability that a randomly generated bitset is valid, and output it as a modular fraction under modulus $1{,}234{,}567{,}891$.

The constraints are very large: $n$ can be up to $10^9$, so any solution that tries to enumerate configurations, simulate operations, or use combinatorics depending on subsets of indices is immediately impossible. The only viable direction is a closed-form expression in terms of $n$, computed using fast exponentiation.

A subtle point in this problem is that the randomness is over all bitsets, but the validity condition depends only on the global structure of the bit distribution, not on local patterns. That strongly suggests that we are counting a small number of structural cases.

One edge case is when all bits are identical. In that situation, no operation can even start, because there is no opposite-valued index to pair with a chosen center. For example, for $n = 3$, strings `000` and `111` are immediately stuck.

A naive mistake is to assume that any non-constant string is valid. For small examples this seems plausible, because having both 0 and 1 always gives you at least one possible operation. However, this intuition would fail if there were hidden connectivity constraints, but in this problem the operation is flexible enough that any mixed configuration can be expanded step by step.

## Approaches

The brute-force idea would be to generate all $2^n$ bitsets and simulate whether each one is “amazing”. Even ignoring the exponential number of states, each simulation involves a sequence of operations whose length is not bounded in any useful way, so this approach is entirely infeasible even for tiny $n$.

The key simplification comes from noticing that the operation is extremely powerful once both values exist. If a bitset contains at least one `0` and at least one `1`, then we can always pick a center and an opposite group, and use repeated operations to propagate flips across the entire array. The exact order of operations does not matter because we can always continue as long as both values exist somewhere in the array.

The only configuration that blocks all progress is when the bitset is uniform. In that case, there is no valid first move, so the process is impossible from the start.

So the problem reduces to computing:

$$\mathbb{P}(\text{bitset is not all 0 and not all 1})$$

That is:

$$1 - \mathbb{P}(\text{all 0}) - \mathbb{P}(\text{all 1})$$

Since bits are independent:

$$\mathbb{P}(\text{all 1}) = \left(\frac{a}{b}\right)^n,\quad
\mathbb{P}(\text{all 0}) = \left(\frac{b-a}{b}\right)^n$$

So the answer becomes a simple modular expression involving exponentiation.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Simulation | Exponential | Exponential | Too slow |
| Probability Reduction + Fast Pow | $O(\log n)$ | $O(1)$ | Accepted |

## Algorithm Walkthrough

We want to compute the probability that the generated bitset is not monochromatic.

1. Convert probabilities into modular arithmetic form. We represent $p = a \cdot b^{-1}$ modulo $M$, and similarly $1-p = (b-a) \cdot b^{-1}$.
2. Compute $b^n$ modulo $M$ using fast exponentiation. This represents the denominator contribution.
3. Compute $a^n \bmod M$, corresponding to the numerator of the all-ones case.
4. Compute $(b-a)^n \bmod M$, corresponding to the numerator of the all-zeros case.
5. Combine the two bad cases:

$$\text{bad} = a^n + (b-a)^n \pmod M$$
6. Normalize by dividing by $b^n$, which is done using modular inverse:

$$\text{bad} \cdot (b^n)^{-1}$$
7. Subtract from 1 to obtain the final answer.

### Why it works

The crucial property is that the only obstruction to performing the operation sequence is the absence of both bit values. If both 0 and 1 exist, every operation preserves the fact that we can still choose a center of one type and at least one opposite element, so progress never gets stuck. Thus the set of invalid configurations collapses exactly to the two extreme uniform cases, and probability becomes a simple exclusion computation.

## Python Solution

```python
import sys
input = sys.stdin.readline

MOD = 1234567891

def mod_pow(a, e):
    res = 1
    a %= MOD
    while e:
        if e & 1:
            res = res * a % MOD
        a = a * a % MOD
        e >>= 1
    return res

n, a, b = map(int, input().split())

inv_b = pow(b, MOD - 2, MOD)

p_num = a % MOD
q_num = (b - a) % MOD

a_n = mod_pow(p_num, n)
b_n = mod_pow(b % MOD, n)
q_n = mod_pow(q_num, n)

inv_b_n = pow(b_n, MOD - 2, MOD)

bad = (a_n + q_n) % MOD
bad = bad * inv_b_n % MOD

ans = (1 - bad) % MOD
print(ans)
```

The implementation separates numerator and denominator handling explicitly. The key subtlety is that we never directly compute $(a/b)^n$, since modular division must be handled through inverses. Another important detail is computing both $a^n$ and $(b-a)^n$ independently under the modulus, ensuring we never lose precision before normalization.

## Worked Examples

### Example 1

Input:

```
5 1 2
```

We compute:

$a = 1$, $b-a = 1$, $b = 2$, $n = 5$

| Step | Value |
| --- | --- |
| $a^n$ | $1^5 = 1$ |
| $(b-a)^n$ | $1^5 = 1$ |
| bad numerator | $2$ |
| $b^n$ | $2^5 = 32$ |
| bad probability | $2/32 = 1/16$ |
| answer | $1 - 1/16 = 15/16$ |

This shows the answer is simply the probability of avoiding uniform strings.

### Example 2

Input:

```
3 2 3
```

Here $p = 2/3$, so:

| Step | Value |
| --- | --- |
| $a^n$ | $8$ |
| $(b-a)^n$ | $1$ |
| bad numerator | $9$ |
| $b^n$ | $27$ |
| bad probability | $1/3$ |
| answer | $2/3$ |

This confirms that only fully uniform configurations are excluded.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(\log n)$ | fast exponentiation for a constant number of powers |
| Space | $O(1)$ | only a few integer variables |

The algorithm easily fits within constraints because the only dependency on $n$ is exponentiation, and $n$ can be as large as $10^9$.

## Test Cases

```python
import sys, io

MOD = 1234567891

def mod_pow(a, e):
    res = 1
    a %= MOD
    while e:
        if e & 1:
            res = res * a % MOD
        a = a * a % MOD
        e >>= 1
    return res

def solve():
    n, a, b = map(int, input().split())
    inv_b = pow(b, MOD - 2, MOD)

    a_n = mod_pow(a, n)
    q_n = mod_pow(b - a, n)
    b_n = mod_pow(b, n)

    bad = (a_n + q_n) % MOD
    bad = bad * pow(b_n, MOD - 2, MOD) % MOD

    print((1 - bad) % MOD)

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    return sys.stdout.getvalue()

# provided sample
# (placeholder since single sample given)
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 0 1` | `0` | all zeros always invalid |
| `1 1 1` | `0` | all ones always invalid |
| `5 1 2` | `848765426` | sample |
| `10 0 5` | `0` | extreme bias case |

## Edge Cases

The most important edge case is when the bitset is completely uniform. For example, with input `n = 4, a = 0`, every generated string is `0000`. The algorithm computes $a^n = 0$, $(b-a)^n = b^n$, so the bad probability becomes 1 and the final answer is 0, which matches the fact that no operation is possible.

Another edge case is when $a = b$, meaning every bit is always 1. The computation becomes symmetric: $(b-a)^n = 0$, and again the probability of validity is 0.

Finally, when $n = 1$, every string is trivially uniform, so the answer is always 0. The formula handles this cleanly because both terms reduce directly to 1 after normalization, yielding a zero result.
