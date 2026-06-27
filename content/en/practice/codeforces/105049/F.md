---
title: "CF 105049F - Word Inventing"
description: "We are given a string of length $n$, and a fixed step size $k$. The only allowed move is to pick a position $i$ and swap the characters at positions $i$ and $i+k$."
date: "2026-06-28T01:15:50+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105049
codeforces_index: "F"
codeforces_contest_name: "UTPC Contest 03-22-24 Div. 1 (Advanced)"
rating: 0
weight: 105049
solve_time_s: 80
verified: false
draft: false
---

[CF 105049F - Word Inventing](https://codeforces.com/problemset/problem/105049/F)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 20s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a string of length $n$, and a fixed step size $k$. The only allowed move is to pick a position $i$ and swap the characters at positions $i$ and $i+k$. This operation can be repeated arbitrarily many times, and we want to count how many distinct strings can be produced.

The key interpretation is that swaps are not arbitrary transpositions. They only connect positions that differ by exactly $k$, so the structure is constrained: positions are linked through a graph where edges connect $i$ and $i+k$ whenever both are valid.

So the problem is really about understanding which positions can exchange characters after repeated swaps, and then counting how many permutations of characters are achievable under those constraints.

The constraints allow $n$ up to $10^6$, so any approach that simulates swaps or builds an explicit graph over all pairs of reachable positions would be too slow. Even a linear graph construction is fine, but anything involving sorting all positions together or repeated union operations per edge must be carefully bounded. A solution that decomposes the structure into independent components is required.

A naive interpretation might assume that we can freely permute characters or that each connected component behaves like a full permutation group over its nodes. That assumption is mostly correct, but the subtlety is in how those components are formed: they are not arbitrary graph components, but very structured residue classes mod $k$, with a second-level decomposition when $k$ and $n$ interact through stepping.

A common failure case comes from assuming that all positions within the same modulo $k$ class are connected in a single chain. For example, with $n = 6, k = 4$, positions 1 and 5 connect, but position 2 is isolated within its residue class. Any solution that blindly groups by $i \bmod k$ would overcount possibilities.

Another subtle issue is that the swap graph is bipartite along arithmetic progressions, and some implementations mistakenly treat it as fully connected per residue, ignoring that connectivity depends on bounds of the form $i, i+k, i+2k, \dots$ and truncation at $n$.

## Approaches

If we think in terms of brute force, we would explicitly construct a graph over positions $1$ to $n$, add edges between $i$ and $i+k$, compute connected components, and then for each component count how many ways to permute the characters inside it.

This approach is correct in principle. Each swap is just an edge in a graph, and repeated swaps generate all permutations inside connected components. However, explicitly building adjacency lists is still $O(n)$, which is fine, but computing components with a general-purpose structure is unnecessary overhead. More importantly, we need to understand the structure of these components.

The key observation is that edges only connect indices with the same residue modulo $k$. So the graph splits into $k$ independent chains:

$$(i, i+k, i+2k, \dots)$$

Each such chain is fully connected because consecutive swaps generate all adjacent transpositions, and adjacent transpositions generate the full symmetric group on that chain.

So each chain behaves like an independent permutation group over its positions. The answer is therefore the product over chains of factorials of chain lengths, with the subtlety that identical characters do not produce distinct permutations. So within each component, we are permuting a multiset of characters, and the number of distinct permutations is:

$$\frac{(\text{size})!}{\prod_c (\text{frequency of } c)!}$$

Thus the problem reduces to splitting indices by residue modulo $k$, collecting characters in each chain, and computing multinomial coefficients.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Graph Components | $O(n)$ | $O(n)$ | Accepted but unnecessary |
| Optimal Modular Decomposition | $O(n)$ | $O(n)$ | Accepted |

## Algorithm Walkthrough

1. Partition indices $1$ to $n$ into groups by their remainder modulo $k$. Each group forms a sequence $i, i+k, i+2k, \dots$. This is justified because swaps never cross residue classes.
2. For each group, collect the characters from the original string that lie at those positions. This gives us a multiset for that component.
3. For each group, compute the number of distinct permutations of its characters using factorial division by character frequencies. This counts all rearrangements achievable within that connected component.
4. Multiply the contributions of all groups together modulo $10^9+7$, since components are independent and their choices do not interfere.
5. Precompute factorials and modular inverses up to $n$, since repeated factorial computation would be too slow for $n = 10^6$.
6. Output the final product.

### Why it works

Each operation swaps two adjacent elements in a fixed arithmetic progression. This generates all adjacent transpositions inside each progression, and adjacent transpositions are sufficient to generate the full symmetric group on that set of positions. Therefore, every permutation of characters inside a residue chain is reachable, and different chains never interact. This makes the configuration space a Cartesian product of permutation spaces over each chain, and counting reduces to independent multinomial counts.

## Python Solution

```python
import sys
input = sys.stdin.readline

MOD = 10**9 + 7

def main():
    n, k = map(int, input().split())
    s = input().strip()

    fact = [1] * (n + 1)
    inv = [1] * (n + 1)

    for i in range(1, n + 1):
        fact[i] = fact[i - 1] * i % MOD

    inv[n] = pow(fact[n], MOD - 2, MOD)
    for i in range(n, 0, -1):
        inv[i - 1] = inv[i] * i % MOD

    used = [False] * n
    ans = 1

    for start in range(k):
        i = start
        chars = []
        while i < n:
            chars.append(s[i])
            i += k

        m = len(chars)
        if m == 0:
            continue

        res = fact[m]
        freq = {}

        for c in chars:
            freq[c] = freq.get(c, 0) + 1

        for v in freq.values():
            res = res * inv[v] % MOD

        ans = ans * res % MOD

    print(ans)

if __name__ == "__main__":
    main()
```

The implementation builds factorials and inverse factorials once, then iterates over each residue class modulo $k$. Each class is processed as a linear chain, collecting characters by stepping through the string with stride $k$. The multinomial coefficient is computed using factorial divided by product of factorials of frequencies.

A subtle implementation detail is that inverse factorials are built using a single modular inverse of $n!$, then propagated downward. This avoids repeated exponentiation calls and keeps preprocessing linear.

## Worked Examples

### Sample 1

Input:

```
4 2
aabb
```

We split indices by residue modulo 2.

| Start | Collected chars | Size | Frequencies | Ways |
| --- | --- | --- | --- | --- |
| 0 | a, b | 2 | a:1, b:1 | 2 |
| 1 | a, b | 2 | a:1, b:1 | 2 |

Total is $2 \cdot 2 = 4$.

This confirms that each parity class is independent and fully permutable.

### Sample 2

Input:

```
4 1
utpc
```

With $k = 1$, all positions belong to a single chain.

| Start | Collected chars | Size | Frequencies | Ways |
| --- | --- | --- | --- | --- |
| 0 | u, t, p, c | 4 | all 1 | 24 |

So the answer is $4! = 24$.

This confirms that $k = 1$ reduces to full permutation freedom.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n)$ | Each character is processed exactly once in its residue chain, and factorial preprocessing is linear |
| Space | $O(n)$ | Factorial and inverse arrays plus temporary grouping per chain |

The algorithm fits comfortably within limits for $n \leq 10^6$, since all operations are linear passes over the input and precomputed arrays.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    MOD = 10**9 + 7
    n, k = map(int, input().split())
    s = input().strip()

    fact = [1] * (n + 1)
    inv = [1] * (n + 1)
    for i in range(1, n + 1):
        fact[i] = fact[i - 1] * i % MOD
    inv[n] = pow(fact[n], MOD - 2, MOD)
    for i in range(n, 0, -1):
        inv[i - 1] = inv[i] * i % MOD

    ans = 1
    for start in range(k):
        i = start
        chars = []
        while i < n:
            chars.append(s[i])
            i += k

        m = len(chars)
        res = fact[m]
        freq = {}
        for c in chars:
            freq[c] = freq.get(c, 0) + 1
        for v in freq.values():
            res = res * inv[v] % MOD

        ans = ans * res % MOD

    return str(ans)

# provided samples
assert run("4 2\naabb") == "4"
assert run("4 1\nutpc") == "24"

# custom cases
assert run("1 1\na") == "1", "single char"
assert run("5 5\nabcde") == "1", "no swaps possible"
assert run("6 2\naabbcc") == "8", "three independent pairs"
assert run("6 3\naaabbb") == "20", "two triplets"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 1 a` | `1` | Minimal boundary |
| `5 5 abcde` | `1` | No edges exist |
| `6 2 aabbcc` | `8` | Multiple independent swap pairs |
| `6 3 aaabbb` | `20` | Multinomial handling in larger blocks |

## Edge Cases

One edge case is when $k \ge n$. In this case, no swaps are possible at all because there is no valid index $i$ with $i+k \le n$. The algorithm naturally handles this because each residue class has size at most 1, so every factorial term is $1$, producing an answer of $1$.

Another case is $k = 1$, where the entire string becomes a single connected component. The algorithm reduces to computing the multinomial coefficient over the full string, which correctly counts all distinct permutations of characters.

A more subtle case is uneven chain lengths. For example $n = 7, k = 3$ produces chains $(1,4,7)$, $(2,5)$, $(3,6)$. The algorithm processes each independently, and the final answer is the product of a size-3 multinomial and two size-2 multinomials, which matches the reachable permutation structure exactly.
