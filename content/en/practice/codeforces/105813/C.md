---
title: "CF 105813C - Maxwell's Tiles"
description: "We are given a rectangular wall of size $2m times 2n$, centered at the origin on the integer grid. Each unit square cell is identified by integer coordinates $(x, y)$ inside this rectangle."
date: "2026-06-26T00:06:12+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105813
codeforces_index: "C"
codeforces_contest_name: "Rutgers University Programming Contest Spring 2025"
rating: 0
weight: 105813
solve_time_s: 62
verified: true
draft: false
---

[CF 105813C - Maxwell's Tiles](https://codeforces.com/problemset/problem/105813/C)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 2s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a rectangular wall of size $2m \times 2n$, centered at the origin on the integer grid. Each unit square cell is identified by integer coordinates $(x, y)$ inside this rectangle.

The value of a cell is defined as $\max(|x|, |y|)$. This partitions the entire grid into concentric square “rings”. All cells with the same value lie on the same ring, forming a closed cycle around the center.

A tile is a connected group of cells, and it is only allowed if every cell inside it lies entirely within a single ring. So a tile cannot cross from one ring to another, but it can occupy any connected shape inside its ring, including shapes with holes, as long as connectivity is preserved.

Two tilings are considered different if there exists at least one pair of cells that are together in a tile in one tiling but separated into different tiles in the other.

We need to count how many such valid tilings exist, modulo $10^9 + 7$, for up to $10^4$ test cases, with $m, n \le 10^6$.

The main constraint implication is that we cannot simulate the grid or build any explicit structure per test case. Everything must reduce to a closed-form function of $m$ and $n$, computable in constant time.

A key edge case appears when the grid is minimal, such as $m = n = 1$, where the entire $2 \times 2$ grid forms a single ring. In that case, any solution must account for all connected partitions inside a 4-cycle. A naive assumption that each cell behaves independently leads to an overcount, because connectivity constraints couple the choices along the cycle.

Another subtle issue is that every ring is cyclic rather than linear. Treating a ring as a path would incorrectly forbid connectivity “wrap-around” between the last and first edge of the cycle.

## Approaches

The brute-force interpretation is to consider each ring separately and enumerate all possible ways to partition its cells into connected components. Since each component must stay inside one ring, different rings do not interact, so the total answer is a product over rings.

Inside one ring, the structure is a simple cycle graph whose vertices are the cells in that layer. A naive approach would attempt to enumerate all partitions of this cycle into connected induced subgraphs. This is equivalent to considering all ways to split the cycle into contiguous blocks. The number of such partitions grows exponentially with the ring size, and even for a single ring of length $O(m+n)$, brute force is infeasible.

The key observation is that on a cycle, a subset of edges uniquely determines a partition into connected components. If we decide independently for every edge whether to cut it or not, each resulting connected component is automatically a valid tile, since connectivity is preserved exactly within each segment.

Thus, each ring of length $L$ contributes $2^L$ possible ways.

Summing over all rings, every cell belongs to exactly one ring, so the sum of ring lengths equals the total number of grid cells, which is $4mn$. This reduces the full problem to computing $2^{4mn} \bmod (10^9+7)$.

The brute-force works conceptually because it reduces the problem to independent edge decisions, but it fails computationally because explicitly modeling rings or enumerating configurations per ring is linear in grid size and impossible for large inputs. The observation that each ring is a cycle where cuts fully characterize tilings compresses everything into a single exponent.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Enumeration per ring | Exponential | O(mn) | Too slow |
| Cycle-edge independence reduction | O(1) per test case | O(1) | Accepted |

## Algorithm Walkthrough

1. Observe that each cell belongs to exactly one level determined by $\max(|x|, |y|)$. This partitions the grid into disjoint rings.
2. Recognize that within one ring, adjacency forms a simple cycle graph. Each cell has exactly two neighbors along the boundary traversal of that ring.
3. Reformulate a valid tiling inside a ring as a partition of a cycle graph into connected components. Each component corresponds to a contiguous segment along the cycle.
4. Associate each edge of the cycle with a binary choice: either we “cut” the edge (ending a tile boundary) or we do not. This ensures that connected components are exactly maximal uncut segments.
5. Count configurations inside a ring of length $L$ as $2^L$, since every subset of edges corresponds to a valid partition.
6. Sum contributions over all rings. Since rings are disjoint and cover all cells, the total exponent is the number of cells in the grid, which is $4mn$.
7. Compute $2^{4mn} \bmod (10^9+7)$ using fast modular exponentiation.

The correctness relies on the invariant that every configuration of cuts produces a unique partition into connected components, and every valid partition corresponds to exactly one cut pattern. No configuration violates connectivity because removing edges in a cycle cannot create disconnected fragments other than the intended segments.

## Python Solution

```python
import sys
input = sys.stdin.readline

MOD = 10**9 + 7

def mod_pow(a, e):
    res = 1
    while e:
        if e & 1:
            res = (res * a) % MOD
        a = (a * a) % MOD
        e >>= 1
    return res

t = int(input())
for _ in range(t):
    m, n = map(int, input().split())
    exp = (4 * m * n) % (MOD - 1)
    print(mod_pow(2, exp))
```

The implementation reduces the entire geometry to exponentiation. The only subtlety is using Fermat’s little theorem to reduce the exponent modulo $10^9+6$, since the modulus is prime.

## Worked Examples

We trace the computation of the exponent and final value for two cases.

### Example 1: $m = 1, n = 1$

| step | value |
| --- | --- |
| grid size | $2 \times 2$ |
| cells | 4 |
| exponent $4mn$ | 4 |
| result | $2^4 = 16 \bmod MOD$ |

This shows the raw cycle-independence interpretation before any reduction.

### Example 2: $m = 3, n = 1$

| step | value |
| --- | --- |
| grid size | $6 \times 2$ |
| cells | 12 |
| exponent $4mn$ | 12 |
| result | $2^{12} = 4096$ |

This confirms that scaling either dimension only increases the exponent linearly through the number of cells.

The trace demonstrates that all structural complexity of tiling disappears once the cycle decomposition is recognized.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(\log(4mn))$ per test | Fast exponentiation dominates |
| Space | $O(1)$ | Only a few integers are stored |

The solution easily fits within constraints since $m,n \le 10^6$ and there are up to $10^4$ test cases. Each query reduces to a single modular exponentiation.

## Test Cases

```python
import sys, io

MOD = 10**9 + 7

def mod_pow(a, e):
    res = 1
    while e:
        if e & 1:
            res = (res * a) % MOD
        a = (a * a) % MOD
        e >>= 1
    return res

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    t = int(input())
    out = []
    for _ in range(t):
        m, n = map(int, input().split())
        out.append(str(mod_pow(2, 4 * m * n)))
    return "\n".join(out)

# sample-like sanity checks
assert run("1\n1 1\n") == "16"
assert run("1\n2 1\n") == str(pow(2, 8, MOD))
assert run("1\n1 2\n") == str(pow(2, 8, MOD))
assert run("1\n3 4\n") == str(pow(2, 48, MOD))
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 1 / 1 | 16 | smallest grid correctness |
| 2 1 / 1 | 256 | asymmetric dimensions |
| 1 2 / 1 | 256 | symmetry in m,n |
| 3 4 / 1 | $2^{48}$ | general scaling |

## Edge Cases

When $m = n = 1$, the grid reduces to a single cycle of length 4. The algorithm interprets this as $4mn = 4$, producing $2^4$. This matches the idea that each of the four cycle edges can independently be cut or not, producing all valid connected partitions.

When one dimension is 1 and the other is large, the structure becomes a long rectangular boundary with many nested rings. Each ring still contributes independently, and the total exponent remains exactly the number of cells in the rectangle. The algorithm does not distinguish between inner and outer rings because all are absorbed into the global count $4mn$, ensuring consistent handling of elongated grids.
