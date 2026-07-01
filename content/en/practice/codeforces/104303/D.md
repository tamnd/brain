---
title: "CF 104303D - \"\u9006\"\u5929\u6c42\u548c"
description: "For each query, we are given a prime number $p$. We look at all integers from $1$ to $p-1$, and for each such integer $a$, we compute its multiplicative inverse modulo $p$. That means we find a number $b$ in the range $[1, p-1]$ such that $a cdot b equiv 1 pmod p$."
date: "2026-07-01T20:09:46+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104303
codeforces_index: "D"
codeforces_contest_name: "2023 Xiangtan Unversity Freshman Conteset"
rating: 0
weight: 104303
solve_time_s: 48
verified: true
draft: false
---

[CF 104303D - \"\u9006\"\u5929\u6c42\u548c](https://codeforces.com/problemset/problem/104303/D)

**Rating:** -  
**Tags:** -  
**Solve time:** 48s  
**Verified:** yes  

## Solution
## Problem Understanding

For each query, we are given a prime number $p$. We look at all integers from $1$ to $p-1$, and for each such integer $a$, we compute its multiplicative inverse modulo $p$. That means we find a number $b$ in the range $[1, p-1]$ such that $a \cdot b \equiv 1 \pmod p$. Because $p$ is prime, every nonzero residue has exactly one such inverse.

The task is to compute the sum of all these inverses:

$$\sum_{i=1}^{p-1} i^{-1} \bmod p$$

for each query.

The input consists of multiple independent primes, and for each one we output this sum.

The constraint $T \le 9592$ means we cannot afford any per-query loop up to $p$, since $p$ can be large. A direct computation of modular inverses for every query would require $O(p)$ per test case, which would be far too slow in aggregate.

A subtle point that can trap naive reasoning is thinking inverses behave independently. For example, computing a few inverses and trying to infer a pattern quickly leads to incorrect conclusions unless the group structure is used.

Another edge case is $p = 2$. In that case the range $1$ to $p-1$ contains only $1$, and its inverse is itself, so the sum is $1$. Many general modular arguments implicitly assume $p > 2$, so this needs separate attention.

## Approaches

A brute-force method would compute each modular inverse using fast exponentiation via Fermat’s theorem $a^{-1} \equiv a^{p-2} \pmod p$, then sum them. This works correctly because every term is computed independently and correctly modulo $p$. However, it performs $p-1$ exponentiations per test case, and each exponentiation costs $O(\log p)$, leading to $O(p \log p)$ per query. With up to nearly ten thousand queries, this becomes infeasible as soon as primes are moderately large.

The key structural observation is that the mapping $a \mapsto a^{-1} \bmod p$ is a permutation of the set $\{1, 2, \dots, p-1\}$. This is a direct consequence of the fact that every nonzero element in a finite field has a unique inverse, and applying inversion twice returns the original element.

Because inversion is a bijection on the same set, summing all inverses is equivalent to summing all original numbers in a different order. That means the multiset of inverses is exactly the same as the multiset $\{1, 2, \dots, p-1\}$. Therefore the sum of inverses is identical to:

$$1 + 2 + \dots + (p-1) = \frac{(p-1)p}{2}$$

Since we output this value modulo $p$, the expression simplifies immediately because it contains a factor of $p$, making it divisible by $p$. Hence the result is $0$ modulo $p$ for all odd primes. The only exception is $p = 2$, where the formula degenerates.

So the entire computation reduces to a constant-time check per query.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force (compute inverses) | $O(p \log p)$ | $O(1)$ | Too slow |
| Optimal (group permutation insight) | $O(1)$ per query | $O(1)$ | Accepted |

## Algorithm Walkthrough

We rely entirely on the fact that inversion permutes the nonzero residue system modulo a prime.

1. Read each prime $p$ from input. Each query is independent, so no preprocessing is needed.
2. If $p = 2$, directly output $1$. This comes from the fact that the only element is $1$, and $1^{-1} = 1$.
3. If $p > 2$, output $0$. This follows because the set of inverses is just a rearrangement of $1$ to $p-1$, and the sum of a full residue system modulo $p$ excluding zero always collapses to $0 \bmod p$.

### Why it works

The function $f(a) = a^{-1} \bmod p$ is a bijection over $\{1, \dots, p-1\}$. A bijection preserves multisets, so it preserves sums modulo $p$. Therefore:

$$\sum_{a=1}^{p-1} a^{-1} \equiv \sum_{a=1}^{p-1} a \pmod p$$

The right-hand side equals $\frac{p(p-1)}{2}$, which is divisible by $p$, hence congruent to $0$ modulo $p$. This invariant holds for every prime $p > 2$, ensuring correctness of the constant-time solution.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    out = []
    for _ in range(t):
        p = int(input())
        if p == 2:
            out.append("1")
        else:
            out.append("0")
    print("\n".join(out))

if __name__ == "__main__":
    solve()
```

The implementation follows the derived characterization directly. Each query is handled in constant time. The only branching condition is the special case $p = 2$, which must be separated to avoid incorrectly applying the modular cancellation argument when the set contains only one element.

## Worked Examples

### Example 1

Input:

$$p = 5$$

We consider inverses modulo 5:

| a | a^{-1} mod 5 |
| --- | --- |
| 1 | 1 |
| 2 | 3 |
| 3 | 2 |
| 4 | 4 |

Sum of inverses is $1 + 3 + 2 + 4 = 10$, which is $0 \bmod 5$.

This confirms that the inverse mapping only permutes elements, producing the same multiset.

### Example 2

Input:

$$p = 2$$

| a | a^{-1} mod 2 |
| --- | --- |
| 1 | 1 |

Sum is $1$, which is the correct special case output.

This demonstrates why the general cancellation argument does not apply when the set size is 1.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(T)$ | Each query is answered by a constant-time check |
| Space | $O(1)$ | Only simple variables and output storage |

The solution easily fits within the limits since even $T \approx 10^4$ operations is trivial.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    t = int(input())
    out = []
    for _ in range(t):
        p = int(input())
        out.append("1" if p == 2 else "0")
    return "\n".join(out)

# provided-like samples
assert run("1\n2\n") == "1", "p=2 case"
assert run("1\n5\n") == "0", "odd prime case"

# custom cases
assert run("3\n3\n5\n7\n") == "0\n0\n0", "all odd primes"
assert run("2\n2\n2\n") == "1\n1", "repeated minimal prime"
assert run("1\n11\n") == "0", "larger prime"
assert run("4\n2\n3\n2\n5\n") == "1\n0\n1\n0", "mixed cases"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| repeated 2 | all 1 | handles smallest prime repeatedly |
| several odd primes | all 0 | general correctness |
| mixed 2 and odd primes | 1 or 0 correctly | branching logic |

## Edge Cases

For $p = 2$, the inversion set collapses to a single element. The algorithm explicitly checks this case before applying the general rule.

For $p > 2$, every element has a distinct inverse within the same range, so the sum is just a permutation sum. For example with $p = 3$, we have inverses $1 \leftrightarrow 1$ and $2 \leftrightarrow 2$, giving sum $3 \equiv 0 \pmod 3$. The algorithm correctly outputs $0$.

For larger primes like $p = 11$, even though individual inverses look irregular, the permutation property guarantees the sum remains fixed, and the algorithm avoids computing any of them directly while still returning the correct result.
