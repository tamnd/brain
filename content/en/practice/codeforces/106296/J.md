---
title: "CF 106296J - AND Components"
description: "We are given a collection of integers, and we are asked to understand connectivity induced by a bitwise rule. Each number can be thought of as a node in a graph."
date: "2026-06-25T07:44:19+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 106296
codeforces_index: "J"
codeforces_contest_name: "The 4th Universal Cup. Extra Stage 3: Osijek (Farhod Contest)"
rating: 0
weight: 106296
solve_time_s: 41
verified: true
draft: false
---

[CF 106296J - AND Components](https://codeforces.com/problemset/problem/106296/J)

**Rating:** -  
**Tags:** -  
**Solve time:** 41s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a collection of integers, and we are asked to understand connectivity induced by a bitwise rule. Each number can be thought of as a node in a graph. Two nodes are connected if their bitwise AND is non-zero, meaning they share at least one bit position where both have a 1.

Once these connections are considered, the task is to determine how many connected components the resulting graph has.

The key difficulty is that the graph is not explicitly constructed. With up to large inputs, checking every pair would be too slow, so the structure must be inferred from bit patterns.

From a complexity perspective, if there are up to about 2×10^5 numbers, a quadratic solution that checks all pairs would require around 10^10 operations, which is far beyond any practical limit in two seconds. Even building all edges explicitly is impossible. This immediately forces us to avoid pairwise reasoning and instead exploit structure in the bit representation.

A few edge cases are easy to miss.

If all numbers are zero, no two nodes share a set bit, so every node is isolated. For example, input `[0, 0, 0]` must produce 3 components.

If all numbers are identical and non-zero, every node shares at least one bit with every other node, so the answer must be 1.

If there is a mix of zero and non-zero values, zeros never connect to anything, but non-zero values may still form a large connected structure.

A subtle case appears when numbers do not directly overlap pairwise but are connected transitively through intermediate values. For example, `2 (010)`, `4 (100)`, `6 (110)` form a single component even though `2 & 4 = 0`, because both connect through `6`.

## Approaches

A brute-force solution builds the full graph by checking every pair of numbers and adding an edge if their AND is non-zero. Then a DFS or BFS counts connected components. This is correct because it directly simulates the definition of connectivity.

However, the pairwise check is the bottleneck. With `n` elements, there are `n(n-1)/2` comparisons, each requiring a bitwise operation. For `n = 2×10^5`, this is far too large. Even if edge construction were possible, running graph traversal on a dense graph would also be expensive.

The key observation is that the AND condition depends only on shared bits. Instead of comparing numbers against each other, we can group numbers by the bits they contain. Every number belongs to several bit groups, one for each set bit. If we connect all numbers that share a particular bit, then any pair with a non-zero AND will end up in the same connected structure.

This transforms the problem from reasoning over pairs to reasoning over bits. Each bit acts as a hub: all numbers containing that bit belong to the same union. The final connected components are exactly the connected components formed by these unions.

We can implement this efficiently using a disjoint set union structure, merging all indices that share a given bit.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Pair Checking | O(n²) | O(1) extra (or O(n²) graph) | Too slow |
| Bitwise DSU Grouping | O(n · B α(n)) | O(n + B) | Accepted |

Here `B` is the number of bits needed to represent values, typically around 20 to 30.

## Algorithm Walkthrough

1. Initialize a disjoint set union structure where each number starts in its own component. This represents the state where no connections are assumed.
2. For each bit position from 0 up to the maximum relevant bit, maintain a list of indices whose numbers contain that bit. This groups nodes by shared structural features rather than comparing them pairwise.
3. For every bit, if multiple numbers contain it, merge all of them into a single connected group using DSU unions. We can do this by taking the first element in the list as a representative and unioning it with every other element in the same list.
4. After processing all bits, compute how many distinct DSU roots remain. Each root corresponds to one connected component.

The reason merging within each bit is valid is that any two numbers sharing a bit are guaranteed to be connected directly by an edge. Once they are merged, transitivity of union-find ensures that any chain of shared bits also becomes connected.

### Why it works

Each number is connected to all numbers that share at least one common bit with it. If two numbers share a bit, they are forced into the same component through that bit’s grouping. If they do not share a bit directly but can be connected through intermediate numbers, those intermediates must share bits forming a chain. DSU preserves exactly this transitive closure over bit-sharing relationships, which matches the graph connectivity defined by the AND condition.

## Python Solution

```python
import sys
input = sys.stdin.readline

class DSU:
    def __init__(self, n):
        self.parent = list(range(n))
        self.size = [1] * n

    def find(self, x):
        while self.parent[x] != x:
            self.parent[x] = self.parent[self.parent[x]]
            x = self.parent[x]
        return x

    def union(self, a, b):
        a = self.find(a)
        b = self.find(b)
        if a == b:
            return
        if self.size[a] < self.size[b]:
            a, b = b, a
        self.parent[b] = a
        self.size[a] += self.size[b]

def solve():
    n = int(input())
    a = list(map(int, input().split()))

    dsu = DSU(n)

    bit_to_nodes = [[] for _ in range(32)]

    for i, val in enumerate(a):
        for b in range(32):
            if val & (1 << b):
                bit_to_nodes[b].append(i)

    for b in range(32):
        nodes = bit_to_nodes[b]
        for i in range(1, len(nodes)):
            dsu.union(nodes[0], nodes[i])

    roots = set(dsu.find(i) for i in range(n))
    print(len(roots))

if __name__ == "__main__":
    solve()
```

The DSU implementation uses path compression and union by size to keep operations effectively constant. The bit grouping step ensures that we only perform unions where a direct structural reason exists, instead of exploring edges explicitly.

The loop over bits is fixed size, so the main cost is proportional to how many numbers contain each bit, which is efficient under typical constraints.

## Worked Examples

Consider the input:

```
5
2 4 6 1 8
```

We track which indices fall into each bit group.

| Step | Bit processed | Nodes with bit | DSU merges | Components |
| --- | --- | --- | --- | --- |
| 1 | bit 1 (2) | [0, 2] | union(0,2) | {0,2}, {1}, {3}, {4} |
| 2 | bit 2 (4) | [1, 2] | union(1,2) | {0,1,2}, {3}, {4} |
| 3 | bit 3 (8) | [4] | none | unchanged |

After processing, nodes 0,1,2 are connected through shared bit 1 and 2 chains, while others remain separate.

This demonstrates that connectivity emerges from shared-bit transitivity rather than direct pairwise overlap.

Now consider:

```
3
1 2 4
```

| Step | Bit processed | Nodes with bit | DSU merges | Components |
| --- | --- | --- | --- | --- |
| 1 | bit 0 | [0] | none | {0}, {1}, {2} |
| 2 | bit 1 | [1] | none | unchanged |
| 3 | bit 2 | [2] | none | unchanged |

No merges occur because no two numbers share a bit, so each node remains isolated.

This confirms that the algorithm correctly handles the fully disconnected case.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n · B α(n)) | Each number contributes to up to B bit lists, and DSU unions are nearly constant time |
| Space | O(n + B) | DSU arrays plus bit buckets |

The bit width B is constant for typical constraints (around 20-32), so the solution behaves almost linearly in practice and easily fits within limits for n up to 2×10^5.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from collections import deque

    class DSU:
        def __init__(self, n):
            self.p = list(range(n))
        def f(self, x):
            while self.p[x] != x:
                self.p[x] = self.p[self.p[x]]
                x = self.p[x]
            return x
        def u(self, a, b):
            a, b = self.f(a), self.f(b)
            if a != b:
                self.p[b] = a

    n = int(input())
    a = list(map(int, input().split()))
    d = DSU(n)
    bits = [[] for _ in range(32)]
    for i, v in enumerate(a):
        for b in range(32):
            if v & (1 << b):
                bits[b].append(i)
    for b in range(32):
        for i in range(1, len(bits[b])):
            d.u(bits[b][0], bits[b][i])
    return str(len({d.f(i) for i in range(n)}))

# minimal
assert run("1\n5\n") == "1"

# all zero
assert run("3\n0 0 0\n") == "3"

# all same non-zero
assert run("4\n7 7 7 7\n") == "1"

# chain connectivity
assert run("3\n2 4 6\n") == "1"

# disjoint bits
assert run("3\n1 2 4\n") == "3"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single element | 1 | base case |
| all zeros | n | no shared bits |
| identical values | 1 | full connectivity |
| chain (2,4,6) | 1 | transitive merging |
| disjoint bits | 3 | no accidental connections |

## Edge Cases

For inputs consisting entirely of zeros, the bit grouping step never assigns any index to any bucket. As a result, no union operations are performed and each node remains its own parent. The DSU root count equals `n`, matching the fact that no AND between distinct zeros produces a connection condition.

For inputs where all numbers are identical and non-zero, every index is inserted into the same set of bit buckets. Each bit bucket triggers unions that collapse all nodes into a single representative. Even though unions are repeated across multiple bits, DSU ignores redundant merges safely, so the final structure is a single component.

For sparse inputs like `[1, 2, 4]`, each number activates a disjoint bit bucket. Since no bucket contains more than one index, no union occurs at all. The DSU remains in its initial state, correctly producing three components.
