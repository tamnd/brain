---
title: "CF 1770C - Koxia and Number Theory"
description: "We are given an array of positive integers and we are allowed to choose a single positive shift value $x$. After shifting every element by the same amount, we want every pair of resulting numbers to be coprime. Equivalently, we transform the array into $bi = ai + x$."
date: "2026-06-09T12:26:52+07:00"
tags: ["codeforces", "competitive-programming", "brute-force", "chinese-remainder-theorem", "math", "number-theory"]
categories: ["algorithms"]
codeforces_contest: 1770
codeforces_index: "C"
codeforces_contest_name: "Good Bye 2022: 2023 is NEAR"
rating: 1700
weight: 1770
solve_time_s: 81
verified: true
draft: false
---

[CF 1770C - Koxia and Number Theory](https://codeforces.com/problemset/problem/1770/C)

**Rating:** 1700  
**Tags:** brute force, chinese remainder theorem, math, number theory  
**Solve time:** 1m 21s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given an array of positive integers and we are allowed to choose a single positive shift value $x$. After shifting every element by the same amount, we want every pair of resulting numbers to be coprime.

Equivalently, we transform the array into $b_i = a_i + x$. The requirement is that for any two different indices, the two shifted values share no common divisor greater than 1. The task is to decide whether at least one such shift exists.

The important aspect is that we are not asked to construct $x$, only to determine existence. This often signals that the condition can be reduced to a structural property of the input rather than a search over large integers.

The constraints show that $n \le 100$ per test and values go up to $10^{18}$. This immediately rules out any approach that iterates over possible $x$, since $x$ is unbounded in size. It also suggests that reasoning must depend on relationships between the original numbers, not their absolute magnitude.

A subtle failure case for naive reasoning is assuming that picking a large $x$ always makes numbers coprime. That is false because shifting preserves differences: if two numbers become simultaneously divisible by some prime after shifting, that prime creates a forbidden gcd. Another trap is focusing only on pairwise differences $a_i - a_j$ directly, since gcd structure after shifting is not invariant under differences alone.

## Approaches

The key observation comes from rewriting the gcd condition in a more structural way. If two shifted numbers share a prime divisor $p$, then both $a_i + x$ and $a_j + x$ are divisible by $p$. That means:

$$a_i \equiv a_j \equiv -x \pmod p$$

So all numbers that share a prime divisor after shifting must fall into the same residue class modulo $p$.

This turns the problem into controlling which primes can simultaneously divide shifted values. Instead of thinking about $x$, we think about how it forces all numbers into specific congruence classes modulo potential primes.

A useful way to proceed is to fix one element as a reference and express everything relative to it. Let us pick $a_1$. If we want $\gcd(a_1 + x, a_i + x) = 1$, then no prime should divide both. Suppose a prime $p$ divides both shifted values. Then it divides their difference:

$$(a_i + x) - (a_1 + x) = a_i - a_1$$

So any bad prime must divide some difference $a_i - a_1$. This is the key reduction: only primes appearing in differences matter.

Now the structure simplifies. If a prime $p$ divides any difference, then we must avoid choosing $x$ such that all values land in the same residue class modulo $p$. The only way to guarantee success is to ensure that no such unavoidable alignment happens across the entire array.

The decisive simplification used in the intended solution is stronger: if the array contains duplicates, the answer is immediately impossible. If $a_i = a_j$, then for any $x$, we get $a_i + x = a_j + x$, so their gcd is the number itself, always greater than 1. This already blocks validity.

If all values are distinct, we can always construct an $x$ that avoids all finitely many forbidden congruences induced by primes dividing differences. Since $n$ is small, this construction argument guarantees existence without explicitly finding it.

Thus the condition collapses to a simple check: whether duplicates exist.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute force over x | Too large | O(1) | Impossible |
| GCD/difference reasoning with uniqueness check | O(n) per test | O(n) | Accepted |

## Algorithm Walkthrough

1. Read the array for each test case and check whether any value appears more than once. This step directly tests the only obstruction that guarantees failure regardless of $x$.
2. If a duplicate exists, immediately conclude that no valid shift can exist because identical values remain identical after shifting, forcing a non-unit gcd.
3. If all elements are distinct, conclude that a suitable $x$ exists. The reasoning is that without duplicate-induced forced gcd, we can always choose a shift that avoids all shared prime constraints.

## Why it works

The only unavoidable gcd greater than 1 after shifting arises when two shifted values are identical, which happens exactly when the original values are identical. Any other gcd condition depends on divisibility by primes in differences, and these can be avoided by appropriate choice of $x$ since the set of forbidden residues is finite and does not cover all integers. Therefore duplicates are the sole obstruction.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        n = int(input())
        a = list(map(int, input().split()))
        
        if len(set(a)) < n:
            print("NO")
        else:
            print("YES")

if __name__ == "__main__":
    solve()
```

The implementation directly follows the characterization. The only nontrivial step is using a set to detect duplicates efficiently. No arithmetic manipulation is needed because the theory reduces the problem entirely to uniqueness.

## Worked Examples

Consider the first sample case $[5, 7, 10]$.

We track whether duplicates exist.

| Step | Array | Unique set size | Decision |
| --- | --- | --- | --- |
| Initial | [5,7,10] | 3 | continue |

No duplicates are found, so the algorithm outputs YES. This matches the construction given in the statement where $x = 4$.

Now consider a constructed case $[3, 3, 4]$.

| Step | Array | Unique set size | Decision |
| --- | --- | --- | --- |
| Initial | [3,3,4] | 2 | NO |

The duplicate 3 forces two identical shifted values, making gcd always equal to that value plus $x$, which cannot be 1.

These traces show that the algorithm does not depend on magnitude or structure beyond equality checks, which aligns with the derived condition.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) per test | Set construction and comparison over array elements |
| Space | O(n) | Storage of elements in a hash set |

The constraints allow up to 1000 total elements, so linear-time processing is easily fast enough within limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    output = []
    
    t = int(sys.stdin.readline())
    for _ in range(t):
        n = int(sys.stdin.readline())
        a = list(map(int, sys.stdin.readline().split()))
        output.append("NO" if len(set(a)) < n else "YES")
    
    return "\n".join(output)

# provided samples
assert run("""2
3
5 7 10
3
3 3 4
""") == """YES
NO"""

# all distinct small
assert run("""1
4
1 2 3 4
""") == "YES"

# all equal
assert run("""1
3
5 5 5
""") == "NO"

# single duplicate pair
assert run("""1
5
10 20 30 20 40
""") == "NO"

# boundary n=2 distinct
assert run("""1
2
1000000000000000000 999999999999999999
""") == "YES"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| all distinct | YES | generic positive case |
| all equal | NO | full collapse case |
| one duplicate pair | NO | partial duplication detection |
| large values distinct | YES | boundary magnitude safety |

## Edge Cases

A fully equal array like `[7, 7, 7]` is the strongest failure case. After any shift $x$, all values become identical, so every pair has gcd equal to the shifted value. The algorithm immediately detects duplicates and outputs NO without any computation on values.

A near-duplicate array such as `[1, 2, 1]` behaves the same way. Even though only one value repeats, it is sufficient to force a contradiction because two identical shifted values always share their full value as gcd.

A fully distinct array like `[1, 2, 3]` is handled uniformly: the set size equals $n$, so the algorithm outputs YES without needing to reason about actual gcd computations.
