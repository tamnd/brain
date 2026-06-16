---
title: "CF 1030G - Linear Congruential Generator"
description: "We are given a system that evolves an $n$-dimensional vector over discrete steps. Each coordinate evolves independently using the same type of rule: a linear transformation modulo a prime."
date: "2026-06-16T21:04:51+07:00"
tags: ["codeforces", "competitive-programming", "number-theory"]
categories: ["algorithms"]
codeforces_contest: 1030
codeforces_index: "G"
codeforces_contest_name: "Technocup 2019 - Elimination Round 1"
rating: 2900
weight: 1030
solve_time_s: 151
verified: true
draft: false
---

[CF 1030G - Linear Congruential Generator](https://codeforces.com/problemset/problem/1030/G)

**Rating:** 2900  
**Tags:** number theory  
**Solve time:** 2m 31s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a system that evolves an $n$-dimensional vector over discrete steps. Each coordinate evolves independently using the same type of rule: a linear transformation modulo a prime.

For each index $i$, the value $f_i^{(k)}$ depends only on its previous value $f_i^{(k-1)}$ through an affine function modulo $p_i$. We are allowed to choose the initial vector and all coefficients of these affine functions freely, with the goal of making the sequence of whole tuples $(f_1^{(k)}, \dots, f_n^{(k)})$ produce as many distinct states as possible before it eventually repeats.

The task is to determine the maximum possible number of distinct tuples that can appear in such a sequence.

The key constraint is that $n$ can be up to $2 \cdot 10^5$, so any solution must be essentially linear in $n$. Each $p_i$ is a prime up to $2 \cdot 10^6$, which strongly suggests we will never iterate over values modulo $p_i$, but instead rely on algebraic structure of the update rule.

A naive simulation would try to reason about cycles of each coordinate for chosen parameters. That immediately fails because each coordinate has up to $p_i$ states, and the product of all $p_i$ is astronomically large.

A more subtle failure case appears if one assumes arbitrary linear recurrences produce complicated cycle structures that must be analyzed individually. For example, one might try to compute cycle lengths for each affine function and then combine them, but incorrectly assume the maximum cycle length depends on both $a_i$ and $b_i$ in a complicated way. In reality, the structure over a prime field is rigid enough that we can force a maximal cycle.

The core difficulty is recognizing that we are not analyzing a fixed generator. We are choosing the generator to maximize the orbit size.

## Approaches

Each coordinate evolves independently under the map

$$x \mapsto a_i x + b_i \pmod{p_i}$$

over a finite field of prime size. So each coordinate is a function on a set of size $p_i$, and the full system is a product of independent dynamical systems.

The brute-force mental model is to pick parameters and simulate the induced cycle lengths. For each coordinate, we could enumerate all choices of $a_i, b_i, x_i$, simulate until repetition, and compute orbit sizes, then try to combine them. This is completely infeasible because even one coordinate already has $O(p_i)$ states, and the number of parameter choices is $O(p_i^2)$, so total work explodes immediately.

The key observation is that the maximum possible orbit size of an affine transformation over a prime field is not complicated. The map is either a permutation or not, and when it is a permutation, its cycle decomposition can be made a single cycle of size $p_i$.

Over a prime field, any function of the form $x \mapsto x + c$ with $c \neq 0$ is a cyclic shift of all elements. Iterating it walks through all $p_i$ values before repeating. This already gives the maximum possible period for a single coordinate, since no system on a set of size $p_i$ can have a cycle longer than $p_i$.

Since coordinates evolve independently, the total number of distinct tuples equals the product of the individual cycle lengths. Maximizing each coordinate independently maximizes the product.

So the optimal strategy is to force every coordinate to have period exactly $p_i$, and the answer becomes the product of all primes.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute force cycle reasoning per parameter | exponential | O(1) | Too slow |
| Optimal product of primes observation | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

1. Observe that each coordinate evolves independently under a function modulo a prime $p_i$. This means the full tuple evolution is the Cartesian product of independent one-dimensional dynamical systems.
2. For a fixed coordinate $i$, recognize that the state space has exactly $p_i$ elements. Any sequence produced by repeated application of a deterministic function must eventually repeat, so the orbit length is at most $p_i$. This gives an absolute upper bound per coordinate.
3. Show that this upper bound is achievable. Choosing $a_i = 1$ and $b_i = 1$ makes the transformation $x \mapsto x + 1 \pmod{p_i}$. Each application moves to a new value until all residues are visited before returning to the start. This produces a cycle of length $p_i$.
4. Conclude that the maximum possible orbit length for coordinate $i$ is exactly $p_i$, since it cannot exceed the number of states and this construction attains it.
5. Since coordinates are independent, the tuple repeats only when every coordinate repeats simultaneously. Therefore the full period is the least common synchronization of independent cycles, which here is exactly the product of their lengths.
6. Multiply all $p_i$ together under modulo $10^9+7$.

### Why it works

The evolution of the full state space is a product of independent finite cycles, one per coordinate. Each coordinate cycle can be maximized independently to length $p_i$, and no coordinate can exceed its state space size. Independence ensures that tuple repetition occurs exactly when all coordinates return to their starting positions simultaneously, so the total number of distinct tuples equals the product of cycle lengths. This establishes both the upper bound and its attainability.

## Python Solution

```python
import sys
input = sys.stdin.readline

MOD = 10**9 + 7

def main():
    n = int(input())
    p = list(map(int, input().split()))
    
    ans = 1
    for x in p:
        ans = (ans * x) % MOD
    
    print(ans)

if __name__ == "__main__":
    main()
```

The implementation directly applies the derived result. The only state maintained is the running product of all primes modulo $10^9+7$. There are no hidden dependencies between coordinates, so no further processing is needed.

A common pitfall here is overcomplicating the recurrence and trying to analyze $a_i, b_i$ combinations. The optimal construction avoids all of that by selecting parameters that guarantee a full cycle.

## Worked Examples

### Sample 1

Input:

```
4
2 3 5 7
```

We compute the product step by step.

| Step | Prime | Running Product |
| --- | --- | --- |
| 1 | 2 | 2 |
| 2 | 3 | 6 |
| 3 | 5 | 30 |
| 4 | 7 | 210 |

The result is 210, which corresponds to achieving full cycles of lengths 2, 3, 5, and 7 independently.

### Sample 2

Consider:

```
3
3 3 5
```

| Step | Prime | Running Product |
| --- | --- | --- |
| 1 | 3 | 3 |
| 2 | 3 | 9 |
| 3 | 5 | 45 |

The answer is 45. Each coordinate independently cycles through all residues modulo its prime modulus, and the tuple cycles through the full Cartesian product.

This confirms that multiplicative independence across coordinates correctly models the global cycle.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n)$ | One multiplication per prime |
| Space | $O(1)$ | Only a running product is stored |

The constraints allow up to $2 \cdot 10^5$ primes, so a single linear pass is sufficient. The values of $p_i$ are small enough to multiply safely under modulo arithmetic without overflow concerns in Python.

## Test Cases

```python
import sys, io

MOD = 10**9 + 7

def solve():
    input = sys.stdin.readline
    n = int(input())
    p = list(map(int, input().split()))
    ans = 1
    for x in p:
        ans = (ans * x) % MOD
    print(ans)

def run(inp: str) -> str:
    old_stdin = sys.stdin
    sys.stdin = io.StringIO(inp)
    old_stdout = sys.stdout
    sys.stdout = io.StringIO()
    solve()
    out = sys.stdout.getvalue()
    sys.stdin = old_stdin
    sys.stdout = old_stdout
    return out.strip()

# provided sample
assert run("4\n2 3 5 7\n") == "210"

# minimum size
assert run("1\n2\n") == "2"

# repeated primes
assert run("3\n3 3 3\n") == str((3*3*3) % MOD)

# mixed primes
assert run("2\n2 7\n") == str((2*7) % MOD)

# larger case
assert run("5\n2 3 5 7 11\n") == str((2*3*5*7*11) % MOD)
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single prime | 2 | minimum boundary |
| repeated primes | 27 | independence across identical moduli |
| mixed primes | 14 | basic multiplication correctness |
| five primes | 2310 | larger product behavior |

## Edge Cases

A subtle edge case is when all $p_i$ are equal to 2. In that case each coordinate has only two states, and it might seem that interactions between affine choices could reduce the cycle. However, using $x \mapsto x + 1 \bmod 2$ ensures a 2-cycle per coordinate, so the full tuple space still has size $2^n$, and the algorithm correctly returns the product $2^n \bmod (10^9+7)$.

Another case is when $n = 1$. The system degenerates to a single affine map over a prime field. The maximum orbit is exactly $p_1$, and the algorithm correctly returns $p_1$, matching the fact that a full cyclic shift exists on any finite field of prime size.
