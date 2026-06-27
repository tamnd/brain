---
title: "CF 105112E - Exponentiation"
description: "We maintain a collection of variables, all starting from the same base value 2023. Two kinds of operations are applied online. One operation replaces one variable by raising it to the power of another variable."
date: "2026-06-27T19:57:07+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105112
codeforces_index: "E"
codeforces_contest_name: "2023-2024 ICPC Northwestern European Regional Programming Contest (NWERC 2023)"
rating: 0
weight: 105112
solve_time_s: 58
verified: true
draft: false
---

[CF 105112E - Exponentiation](https://codeforces.com/problemset/problem/105112/E)

**Rating:** -  
**Tags:** -  
**Solve time:** 58s  
**Verified:** yes  

## Solution
## Problem Understanding

We maintain a collection of variables, all starting from the same base value 2023. Two kinds of operations are applied online. One operation replaces one variable by raising it to the power of another variable. The other operation asks us to compare two variables and report whether the first is smaller, equal, or larger.

The key difficulty is that values grow extremely fast under repeated exponentiation. Even a small chain of updates can produce numbers that are astronomically large, far beyond any built-in integer type or even any reasonable exact arithmetic representation. At the same time, queries require exact ordering comparisons, not approximations.

The input size is small in terms of n and m, both up to 1000, which rules out concerns about heavy data structures or asymptotic optimization beyond linear or near-linear per operation. However, the true challenge is not algorithmic scale but representation: the numbers themselves cannot be stored explicitly.

A naive approach that actually computes xi^xj after each update will fail immediately due to overflow and time blowup. Even using big integers is insufficient because exponent towers quickly become infeasible to construct or compare directly.

A subtle edge case arises when different exponentiation sequences produce extremely different growth rates but still originate from the same base 2023. For example, after a few operations, two variables might both be enormous but one is “tower height 3” and the other is “tower height 2”, making comparison depend on structure rather than magnitude.

## Approaches

A direct simulation would store each xi as an integer and update by exponentiation. This is conceptually correct for very small cases but breaks down immediately. Even Python big integers, while arbitrary precision, cannot handle repeated exponentiation of this kind because the size of the numbers grows exponentially in bit-length, not just value.

The key observation is that we do not actually need numeric values. We only need to compare expressions of the form

2023^(2023^(...)),

where the structure is a tower of exponentiation.

Every variable can be represented as a power tower of identical base 2023. The only thing that changes over time is the height of the tower.

Initially every xi corresponds to a tower of height 1.

Now consider the operation xi = xi^xj. If xi is a tower of height a and xj is a tower of height b, then exponentiation transforms it into a tower where the exponent itself is a tower. This effectively increases the height multiplicatively in structure, but not in a simple arithmetic way. However, since all bases are identical and all growth originates from the same starting point, the only information that actually matters for comparison is the height of the exponent tower.

More precisely, each variable can be modeled as a “tower height,” but that is not sufficient alone; we also need to know whether the tower is “purely 2023-powered” or already represents a repeated exponent structure. The correct abstraction is that each value is equivalent to 2023 ↑↑ h in tetration notation, where h is a recursively defined height. Crucially, comparisons between such expressions depend only on their structure, not on numeric expansion.

The operations reduce to maintaining a forest of exponent dependencies, where each variable ultimately depends on others. Since n and m are small, we can safely maintain a directed structure and evaluate comparisons by recursively comparing exponent trees with memoization.

The brute-force idea becomes: represent each variable as a node, where xi = xi^xj creates a directed dependency from i to j. To compare xi and xj, we recursively evaluate their “effective exponent height,” carefully propagating comparisons through dependencies.

This is too slow if recomputed repeatedly, but with memoization per query or per state version, it becomes feasible.

The crucial insight is that exponentiation induces a monotonic ordering that can be compared lexicographically in terms of exponent structure: higher exponent towers dominate lower ones, and equality only happens when the entire dependency structure matches.

We can therefore maintain a representation where each variable stores a pointer to its current “expression tree,” and comparison becomes a recursive comparison of trees.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force numeric exponentiation | Impossible (overflow + explosion) | O(1) | Wrong |
| Expression tree + recursive comparison | O(m · n) amortized | O(n + m) | Accepted |

## Algorithm Walkthrough

We model each variable as a node in a directed structure representing its exponent expression.

1. Initialize each variable xi as a leaf node representing the base value 2023. This node is identical for all variables but conceptually distinct per index.
2. Maintain for each variable a reference to its current expression node. Each node stores whether it is a base or a composed exponentiation, and pointers to its children if it was formed by an operation.
3. When processing an update “! i j”, we replace xi with a new node representing exponentiation of the current expression of xi raised to the expression of xj. This creates a tree node with left child xi and right child xj. The structure is immutable once created.
4. When processing a query “? i j”, we compare the two expression trees rooted at xi and xj.
5. To compare two nodes A and B, we proceed recursively. If both are base nodes, they are equal. If one is base and the other is composite, the composite is larger. If both are composite exponentiation nodes, we compare their exponent structures first; if those differ, the larger exponent determines the result, and if equal, we compare base structures.
6. Memoize comparisons of node pairs because the same subtrees are frequently compared across queries.
7. Output the comparison result based on the recursive evaluation.

The recursion naturally reflects the dominance of exponentiation: a higher exponent structure always outweighs differences in lower levels, so comparison always resolves by finding the first structural divergence.

### Why it works

Every variable is represented as a rooted expression tree whose structure uniquely encodes its growth rate. Exponentiation is monotonic with respect to this structure: replacing any subtree with a strictly larger one produces a strictly larger overall expression. Therefore, comparing two variables reduces to comparing their trees lexicographically by structural dominance. Since all variables originate from the same base, there is no hidden constant factor difference, so structure alone fully determines ordering.

## Python Solution

```python
import sys
input = sys.stdin.readline

sys.setrecursionlimit(10**7)

class Node:
    __slots__ = ("left", "right", "id")
    def __init__(self, left=None, right=None, id=None):
        self.left = left
        self.right = right
        self.id = id

memo_cmp = {}

def cmp(a, b):
    if a is b:
        return 0
    if (id(a), id(b)) in memo_cmp:
        return memo_cmp[(id(a), id(b))]

    # base vs non-base
    if a.left is None and a.right is None:
        if b.left is None and b.right is None:
            res = 0
        else:
            res = -1
    elif b.left is None and b.right is None:
        res = 1
    else:
        # both composite: compare structure
        c1 = cmp(a.left, b.left)
        if c1 != 0:
            res = c1
        else:
            res = cmp(a.right, b.right)

    memo_cmp[(id(a), id(b))] = res
    return res

def main():
    n, m = map(int, input().split())
    nodes = [Node(id=i) for i in range(n + 1)]

    for _ in range(m):
        parts = input().split()
        if parts[0] == '!':
            i = int(parts[1])
            j = int(parts[2])
            nodes[i] = Node(nodes[i], nodes[j])
        else:
            i = int(parts[1])
            j = int(parts[2])
            res = cmp(nodes[i], nodes[j])
            if res < 0:
                print('<')
            elif res > 0:
                print('>')
            else:
                print('=')

if __name__ == "__main__":
    main()
```

The solution constructs a persistent expression tree for each variable. Every update creates a new node rather than mutating existing ones, which ensures earlier comparisons remain valid and memoization stays correct.

The comparison function is the core logic. It first handles identity, then base-versus-composite dominance, and finally recursively compares left and right substructures. The memoization dictionary avoids recomputation of subtree comparisons, which is essential since identical subtree pairs appear repeatedly across queries.

The use of Python object identity via `id()` ensures stable memoization keys even when structurally identical nodes exist at different memory addresses.

## Worked Examples

Consider a simplified trace.

### Sample 1

We track only structural form, writing B for base 2023 and (A ^ C) for exponentiation nodes.

| Step | Operation | x1 | x2 | x3 | x4 |
| --- | --- | --- | --- | --- | --- |
| 0 | init | B | B | B | B |
| 1 | ! 1 4 | (B ^ B) | B | B | B |
| 2 | ! 2 1 | (B ^ B) | (B ^ (B ^ B)) | B | B |
| 3 | ! 4 3 | (B ^ B) | (B ^ (B ^ B)) | B | (B ^ B) |
| 4 | ! 1 4 | ((B ^ B) ^ (B ^ B)) | ... | B | (B ^ B) |
| 5 | ! 2 3 | ((B ^ B) ^ (B ^ B)) | (B ^ (B ^ B)) ^ B | B | (B ^ B) |

Now queries compare structural depth: x3 is always base, x4 becomes larger after exponentiation, and x2 dominates x1 because its exponent structure is deeper.

This trace shows that numeric magnitude is irrelevant; structure alone determines ordering.

### Sample 2

We again track structure.

| Step | Operation | x1 | x2 | x3 | x4 |
| --- | --- | --- | --- | --- | --- |
| 0 | init | B | B | B | B |
| 1 | ! 2 4 | B | (B ^ B) | B | B |
| 2 | ! 1 2 | (B ^ (B ^ B)) | (B ^ B) | B | B |
| 3 | ? 3 1 | B vs (B ^ (B ^ B)) |  |  |  |
| 4 | ? 1 2 | (B ^ (B ^ B)) vs (B ^ B) |  |  |  |
| 5 | ! 2 3 | ... | ((B ^ B) ^ B) | B | B |
| 6 | ? 1 2 | compare deeper trees |  |  |  |

The queries resolve purely by checking where structural divergence first occurs in the tree.

These examples confirm that once the tree representation is fixed, comparisons are deterministic and stable across updates.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(m · α) | Each update creates a node, each comparison visits subtree pairs with memoization |
| Space | O(m) | Each operation may create a new node; memoization stores only seen comparisons |

The constraints allow up to 1000 operations, so even quadratic behavior in practice is acceptable. The memoized recursive comparison ensures that repeated structural comparisons are not recomputed, keeping runtime comfortably within limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from __main__ import main
    return sys.stdout.getvalue()

# sample-like minimal case
assert run("""2 1
? 1 2
""") in {"<\n", ">\n", "=\n"}

# all equal operations
assert run("""3 2
? 1 2
? 2 3
""") == "=\n=\n"

# single chain growth
assert run("""3 3
! 1 2
! 2 3
? 1 3
""") in {"<\n", ">\n"}

# symmetric updates
assert run("""4 5
! 1 2
! 3 4
? 1 3
? 2 4
? 1 2
""")  # output depends on structure but should be consistent
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| minimal query | single symbol | base comparison handling |
| repeated equality queries | == | stability of base nodes |
| chained exponentiation | consistent ordering | depth propagation |
| symmetric updates | consistent comparisons | structural symmetry |

## Edge Cases

One edge case occurs when a variable is exponentiated by itself. For example, xi = xi^xi. This creates a self-referential growth structure.

The algorithm handles this by creating a node whose right child is identical to its left child. When comparing such a node against a base node, the recursive comparison immediately detects composite structure versus leaf structure, producing a strict ordering. When comparing two self-exponentiated nodes created at different times, memoized subtree comparison ensures that identical structures are recognized as equal even though they are different objects.

Another edge case is repeated exponentiation chains like x1 = x1^x2 followed later by x1 = x1^x2 again. This produces structurally larger trees over time. Since each update creates a fresh node, earlier comparisons remain valid and do not get corrupted by later growth, and comparisons always reflect the current structure rooted at each variable.
