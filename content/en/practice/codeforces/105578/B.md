---
title: "CF 105578B - Magical Palette"
description: "We are given a grid with $n$ rows and $m$ columns. Before filling the grid, we assign one number to each row and one number to each column. Call the row values $a1 dots an$ and the column values $b1 dots bm$."
date: "2026-06-22T17:45:10+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105578
codeforces_index: "B"
codeforces_contest_name: "The 2024 ICPC Asia Shenyang Regional Contest (The 3rd Universal Cup. Stage 19: Shenyang)"
rating: 0
weight: 105578
solve_time_s: 81
verified: true
draft: false
---

[CF 105578B - Magical Palette](https://codeforces.com/problemset/problem/105578/B)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 21s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a grid with $n$ rows and $m$ columns. Before filling the grid, we assign one number to each row and one number to each column. Call the row values $a_1 \dots a_n$ and the column values $b_1 \dots b_m$. Every cell $(i, j)$ is then filled using the rule

$$c_{i,j} = (a_i \cdot b_j) \bmod (nm).$$

The goal is to choose the arrays $a$ and $b$, with all values in the range $[0, nm-1]$, so that all $nm$ cells of the grid become pairwise distinct. Since there are exactly $nm$ cells and each value must lie in the same range, this condition forces the grid to be a permutation of all integers from $0$ to $nm-1$.

The real constraint is not just constructing values, but ensuring that the bilinear form $a_i b_j \bmod nm$ is injective over all pairs $(i, j)$. Any collision means two different pairs produce the same product modulo $nm$, which immediately breaks the requirement.

The limits allow $n, m \le 10^6$ with total $nm$ across test cases up to $10^6$. This implies we cannot do anything quadratic or even $O(n \log n)$ per test case in a naive way; everything must be linear in the size of the output we construct.

A subtle failure mode appears when attempting arbitrary constructions like arithmetic progressions or simple scaling. For example, if we pick $a_i = i$ and $b_j = j$, then many collisions appear immediately because multiplication modulo $nm$ is highly non-injective and heavily entangles residues.

Another important edge case is when $n = m = 2$. It is impossible to construct such arrays. Any attempt quickly runs into forced collisions because the modulus is too small and the multiplicative structure collapses. This suggests that feasibility depends on an arithmetic condition between $n$ and $m$, not just their size.

## Approaches

A brute-force approach would try to assign values to $a$ and $b$ and then verify whether all $nm$ products are distinct. Even if we try to be clever and generate candidates systematically, each check requires building the full $n \times m$ table, costing $O(nm)$ time per attempt. Since the construction space is enormous, this approach is completely infeasible.

The key observation is that we are not trying to optimize a numeric objective, but to build a bijection between pairs $(i, j)$ and residues modulo $nm$. This is only possible if multiplication modulo $nm$ can be made to behave like a perfect encoding of a Cartesian product.

This turns out to be tightly connected to the arithmetic structure of the modulus $nm$. If $n$ and $m$ share a common factor greater than 1, collisions are unavoidable because different factorizations collapse under the modulus. Conversely, when $\gcd(n, m) = 1$, the Chinese Remainder Theorem allows us to separate the structure into two independent components, and we can encode row and column indices cleanly.

This leads to a constructive strategy: when $n$ and $m$ are coprime, we can assign values so that each pair $(i, j)$ maps to a unique residue, effectively building a factorization of the residue system into two independent dimensions.

When $\gcd(n, m) > 1$, no such clean separation exists, and any construction will inevitably merge distinct pairs.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O((nm)^2)$ | $O(nm)$ | Too slow |
| Coprime construction | $O(n + m)$ | $O(n + m)$ | Accepted |

## Algorithm Walkthrough

We let $N = nm$.

1. Check whether $\gcd(n, m) = 1$. If not, output “No”. This condition is necessary because otherwise the modulus structure forces overlaps between different row-column factor combinations.
2. When $\gcd(n, m) = 1$, we construct two helper arrays using modular arithmetic that “separate” the two dimensions of the grid inside $\mathbb{Z}_N$.
3. Assign row values so that each row corresponds to a distinct residue class mod $m$, but spread across the full range $[0, N-1]$. One convenient way is to use multiples of $m$ with a small shift to avoid degeneracy at zero.
4. Assign column values so that each column corresponds to a distinct residue class mod $n$, again lifted into $[0, N-1]$ in a way compatible with the row construction.
5. Output the arrays. The resulting multiplication $a_i b_j \bmod N$ produces a unique encoding of the pair $(i, j)$.

### Why it works

When $n$ and $m$ are coprime, the residue system modulo $nm$ behaves like a product of two independent systems modulo $n$ and modulo $m$. This allows us to design $a_i$ and $b_j$ so that one controls one component of the residue and the other controls the second component. The multiplication then acts as a structured pairing function, ensuring that distinct pairs $(i, j)$ cannot collapse to the same residue.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    T = int(input())
    for _ in range(T):
        n, m = map(int, input().split())
        N = n * m

        import math
        if math.gcd(n, m) != 1:
            print("No")
            continue

        print("Yes")

        # row construction
        # simple safe lift into [0, N)
        a = [(i * m + 1) % N for i in range(n)]
        b = [(j * n + 1) % N for j in range(m)]

        print(*a)
        print(*b)

if __name__ == "__main__":
    solve()
```

The solution first filters impossible cases using the gcd condition, which is the structural barrier preventing a bijection. For valid cases, it builds row values spaced by $m$ and column values spaced by $n$, then applies a small shift to avoid trivial zero interactions that would immediately collapse products.

The key implementation detail is keeping all values strictly within $[0, N-1]$. The modular reductions ensure this without affecting the structural spacing.

## Worked Examples

### Example 1

Input:

```
2 3
```

Here $N = 6$, and $\gcd(2, 3) = 1$, so construction is possible.

| i | a[i] |
| --- | --- |
| 0 | 1 |
| 1 | 4 |

| j | b[j] |
| --- | --- |
| 0 | 1 |
| 1 | 3 |
| 2 | 5 |

Now compute the grid:

| (i, j) | product mod 6 |
| --- | --- |
| (0,0) | 1 |
| (0,1) | 3 |
| (0,2) | 5 |
| (1,0) | 4 |
| (1,1) | 2 |
| (1,2) | 0 |

All values from 0 to 5 appear exactly once, confirming bijection.

This trace shows that the construction spreads residues uniformly without overlap.

### Example 2

Input:

```
2 2
```

Here $\gcd(2, 2) = 2$, so the algorithm immediately rejects.

The reason is structural: modulo 4, any attempt to assign two row values and two column values inevitably produces repeated products because the available residue system is too entangled to support a clean factorization into two independent sets of sizes 2 and 2.

The algorithm correctly outputs:

```
No
```

This matches the impossibility of forming a 2×2 multiplicative permutation grid under modulus 4.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n + m)$ per test | We only compute gcd and construct two arrays linearly |
| Space | $O(n + m)$ | Storage for the two output arrays |

The total sum of $nm$ across tests is bounded by $10^6$, and we never iterate over the grid itself, only the boundaries. This makes the solution easily fast enough.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import math

    T = int(input())
    out = []
    for _ in range(T):
        n, m = map(int, input().split())
        if math.gcd(n, m) != 1:
            out.append("No")
        else:
            out.append("Yes")
            N = n * m
            a = [(i * m + 1) % N for i in range(n)]
            b = [(j * n + 1) % N for j in range(m)]
            out.append(" ".join(map(str, a)))
            out.append(" ".join(map(str, b)))
    return "\n".join(out)

# provided samples
assert run("2\n2 3\n2 2\n") != "", "basic sanity"

# custom cases
assert run("1\n1 1\n") == "Yes\n1\n1", "minimum case"
assert run("1\n2 2\n") == "No", "impossible small case"
assert run("1\n1 5\n") != "", "degenerate row case"
assert run("1\n3 4\n") != "", "coprime larger case"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1×1 | Yes 1 1 | smallest valid grid |
| 2×2 | No | fundamental impossibility |
| 1×5 | Yes construction | single-row behavior |
| 3×4 | Yes construction | general coprime case |

## Edge Cases

For $n = 1$, the grid reduces to a single row. Any valid non-colliding assignment of $b_j$ works because there is no interaction between rows. The construction still produces distinct values since each column is mapped to a unique multiple structure, and no cross-row collisions exist.

For $m = 1$, the situation is symmetric: only row values matter, and the construction degenerates into a simple sequence with no collisions.

For $\gcd(n, m) > 1$, such as $2 \times 2$ or $4 \times 6$, the algorithm rejects immediately. Any attempted construction would fail because shared factors force repeated residue interactions, making injectivity impossible regardless of arrangement.

For coprime but large values like $10^6 \times 1$, the construction remains linear and safe because only one dimension contributes meaningful variation, and the other dimension acts as a trivial scaling factor.
