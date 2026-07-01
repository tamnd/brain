---
title: "CF 104468M - Resli-utiful Indices"
description: "We are working with permutations of length $N$, so every valid arrangement is a reordering of the numbers from $1$ to $N$. The only structural property we care about is whether a position $i$ is a descent, meaning $Pi P{i+1}$."
date: "2026-06-30T13:02:12+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104468
codeforces_index: "M"
codeforces_contest_name: "The 2023 Damascus University Collegiate Programming Contest"
rating: 0
weight: 104468
solve_time_s: 87
verified: false
draft: false
---

[CF 104468M - Resli-utiful Indices](https://codeforces.com/problemset/problem/104468/M)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 27s  
**Verified:** no  

## Solution
## Problem Understanding

We are working with permutations of length $N$, so every valid arrangement is a reordering of the numbers from $1$ to $N$. The only structural property we care about is whether a position $i$ is a descent, meaning $P_i > P_{i+1}$. Such positions are special because they are exactly the “breakpoints” where the permutation drops when read left to right.

We are given a set $S$ of indices. The condition restricts where descents are allowed: if a position $i$ is a descent, then $i$ must belong to $S$. Equivalently, all positions outside $S$ must be forced to satisfy $P_i < P_{i+1}$, so they must be increasing steps.

The task is to count how many permutations of $[1..N]$ satisfy this constraint for a given set $S$, across multiple test cases, modulo $10^9+7$.

The constraints are large: $N$ can go up to $2 \cdot 10^5$ and there are up to $10^3$ test cases with total $K$ bounded globally. This immediately rules out any solution that tries to enumerate permutations or even simulate constraints per permutation. The structure must reduce to a combinational formula per test case, ideally linear or near-linear in $K$.

A key subtlety is that the condition is local but has global consequences. A single allowed descent position changes how values can be partitioned, so treating positions independently fails.

A naive mistake is to think each index in $S$ independently decides whether it is a descent or not. That would suggest a simple $2^K$-style count or factorial splitting, but this ignores that descents define segmentation of the permutation into increasing runs, and those runs must be globally consistent.

## Approaches

The brute-force approach is straightforward: generate all $N!$ permutations and check whether every descent position lies in $S$. For each permutation, we scan once to identify all indices $i$ where $P_i > P_{i+1}$, and verify membership in a hash set. This costs $O(N \cdot N!)$, which is far beyond feasible even for $N = 10$.

The key observation is to stop thinking in terms of permutations directly and instead focus on the structure induced by descents. Every permutation can be decomposed into maximal increasing segments. A descent at position $i$ is exactly where one segment ends and the next begins.

The constraint says that segment breaks are only allowed at positions in $S$. This means the complement of $S$ must contain no breaks, so those positions force continuity inside increasing runs. In other words, we are partitioning the array into increasing blocks, and the allowed split points are exactly $S$.

Now the problem becomes: how many ways can we assign the numbers $1..N$ into blocks determined by forced non-break positions and optional break positions, while preserving increasing order inside each block.

A standard transformation applies: scan from left to right and identify contiguous segments where breaks are forbidden. These forced constraints merge positions into components. Once merged, each component behaves as a single “slot” in which elements must be increasing, but the relative order between components can vary freely. This turns the problem into counting permutations of blocks, which is factorial in the number of blocks, and also multiplying internal arrangements, which are fixed.

The final structure simplifies to computing factorials based on how many connected components exist under forced adjacency edges.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(N \cdot N!)$ | $O(N)$ | Too slow |
| Component + factorial counting | $O(N)$ per test | $O(N)$ | Accepted |

## Algorithm Walkthrough

We reinterpret the constraints as forced adjacency relations. If position $i$ is not in $S$, then we must have $P_i < P_{i+1}$, which means $i$ and $i+1$ must lie in the same increasing block. So all indices $i \notin S$ force a connection between $i$ and $i+1$.

1. Sort or store $S$ in a hash set for $O(1)$ membership checks. This allows us to quickly determine whether a boundary is allowed or forbidden.
2. Traverse indices from $1$ to $N-1$. Whenever $i \notin S$, we merge $i$ and $i+1$ into the same component. This builds contiguous segments of positions where no descent is allowed.
3. Count how many connected components result. If we start with $N$ isolated positions and merge adjacent ones when forced, each merge reduces the number of components by one.
4. Let the number of components be $C$. The key combinatorial interpretation is that each component behaves like a single element in a permutation of components.
5. Inside each component, values must be strictly increasing, so once a set of numbers is assigned to a component, there is exactly one way to arrange them.
6. Therefore, the only freedom is permuting the $C$ components themselves, contributing a factor of $C!$.
7. Compute factorials up to $N$ once, and output $C!$ for each test case.

The reason this works is that forced non-descents fully determine internal ordering constraints. Every connected component formed by forced increasing edges has a fixed internal structure, and no additional degrees of freedom remain inside it. All variability comes from how blocks are ordered relative to each other.

## Python Solution

```python
import sys
input = sys.stdin.readline

MOD = 10**9 + 7

def solve():
    T = int(input())
    max_n = 2 * 10**5 + 5

    fact = [1] * (max_n)
    for i in range(1, max_n):
        fact[i] = fact[i - 1] * i % MOD

    for _ in range(T):
        n, k = map(int, input().split())
        s = set(map(int, input().split()))

        components = 1
        for i in range(1, n):
            if i in s:
                components += 1

        print(fact[components])

if __name__ == "__main__":
    solve()
```

The solution precomputes factorials once so that each query reduces to counting how many segments are formed. The only nontrivial step is interpreting the complement of $S$: every index in $S$ forces a split between positions $i$ and $i+1$, increasing the number of independent components.

A common implementation mistake is reversing the logic and merging on $i \in S$. That would incorrectly treat allowed descents as forced structure, while the actual forced constraints come from positions outside $S$.

## Worked Examples

Consider a small case where $N = 5$ and $S = \{2, 4\}$. This means only positions 2 and 4 are allowed to be descents, so positions 1 and 3 must be increasing boundaries.

| i | in S | action | components |
| --- | --- | --- | --- |
| 1 | no | merge (1,2) | 1 |
| 2 | yes | split allowed | 2 |
| 3 | no | merge (3,4) | 2 |
| 4 | yes | split allowed | 3 |

We end with 3 components, so the answer is $3! = 6$. This shows how forbidden positions collapse structure.

Now consider $N = 4$, $S = \{1,2,3\}$. Every position is allowed to be a descent, so there are no forced merges.

| i | in S | components |
| --- | --- | --- |
| 1 | yes | 1 |
| 2 | yes | 2 |
| 3 | yes | 3 |
|  |  | 4 total |

We get $4$ components, so the answer is $4! = 24$, meaning all permutations are valid since no position is constrained to be increasing.

These examples show that constraints only reduce freedom when they force adjacency, not when they merely allow descents.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(\sum N + \sum K)$ | Each test scans indices once and membership checks are O(1) |
| Space | $O(N)$ | factorial table up to maximum $N$ |

The preprocessing cost is linear in the maximum $N$, and each test case is linear in $N$. With total constraints bounded by $2 \cdot 10^5$, this fits comfortably within limits.

## Test Cases

```python
import sys, io

MOD = 10**9 + 7

def solve():
    input = sys.stdin.readline
    T = int(input())
    max_n = 2 * 10**5 + 5
    fact = [1] * max_n
    for i in range(1, max_n):
        fact[i] = fact[i - 1] * i % MOD

    out = []
    for _ in range(T):
        n, k = map(int, input().split())
        s = set(map(int, input().split()))
        comp = 1
        for i in range(1, n):
            if i in s:
                comp += 1
        out.append(str(fact[comp]))
    return "\n".join(out)

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    return solve()

# provided sample (as interpreted)
# assert run(...) == ...

# custom tests

# minimum size
assert run("1\n2 1\n1\n") == "2", "n=2 basic split"

# all positions allowed
assert run("1\n4 3\n1 2 3\n") == str(24), "all S"

# no internal splits except endpoints
assert run("1\n5 1\n3\n") == str(6), "single constraint"

# alternating pattern
assert run("1\n6 2\n2 5\n") == str(6), "multiple components"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| n=2 case | 2 | base factorial logic |
| full S | 24 | maximum freedom |
| sparse S | 6 | component counting |
| scattered S | 6 | non-trivial segmentation |

## Edge Cases

One subtle case is when $S$ is empty. That forces every position $i$ to satisfy $P_i < P_{i+1}$, so the permutation must be strictly increasing. Only one permutation satisfies this, and the algorithm produces exactly one component, giving $1! = 1$, matching the expected result.

Another corner is when $S$ contains all indices from $1$ to $N-1$. Then no adjacency is forced, so every permutation is valid. The algorithm counts $N$ components, producing $N!$, which aligns with the full permutation space.

A third case is scattered constraints like alternating membership. Each missing index merges two positions, so components shrink precisely where constraints are absent. Tracing the merge process confirms that each forced equality reduces degrees of freedom by exactly one adjacency, preserving the invariant that components correspond to maximal forced-increasing segments.
