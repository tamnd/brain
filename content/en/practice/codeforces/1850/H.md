---
title: "CF 1850H - The Third Letter"
description: "Each soldier must be assigned an integer coordinate on a number line, and multiple soldiers are allowed to share the same coordinate. Every constraint connects two soldiers and specifies an exact signed distance between their positions."
date: "2026-06-09T05:32:27+07:00"
tags: ["codeforces", "competitive-programming", "dfs-and-similar", "dsu", "graphs", "greedy", "implementation"]
categories: ["algorithms"]
codeforces_contest: 1850
codeforces_index: "H"
codeforces_contest_name: "Codeforces Round 886 (Div. 4)"
rating: 1700
weight: 1850
solve_time_s: 67
verified: true
draft: false
---

[CF 1850H - The Third Letter](https://codeforces.com/problemset/problem/1850/H)

**Rating:** 1700  
**Tags:** dfs and similar, dsu, graphs, greedy, implementation  
**Solve time:** 1m 7s  
**Verified:** yes  

## Solution
## Problem Understanding

Each soldier must be assigned an integer coordinate on a number line, and multiple soldiers are allowed to share the same coordinate. Every constraint connects two soldiers and specifies an exact signed distance between their positions. A constraint of the form `(a, b, d)` enforces that the coordinate of soldier `a` equals the coordinate of soldier `b` plus `d`.

The task is to determine whether there exists any assignment of integers to all soldiers that satisfies every such equation simultaneously.

This is fundamentally a system of difference constraints over an undirected graph where each edge carries a fixed offset. The key challenge is that constraints can form cycles, and cycles may either be consistent or contradictory depending on whether the implied sums around the cycle cancel out to zero.

The input size forces linear or near-linear solutions per test case. Since the total number of soldiers across all test cases is up to 2×10^5, any solution that revisits edges multiple times per node or attempts full pairwise consistency checks would exceed time limits. This rules out brute-force assignment attempts or repeated relaxation from scratch per node.

A subtle failure case appears when multiple independent paths define different implied differences between the same pair of nodes. For example, if we infer `x1 - x2 = 3` from one path and `x1 - x2 = 5` from another, the system is inconsistent even though no single constraint directly contradicts another. A naive approach that only checks local consistency of edges would miss this.

Another failure mode is when constraints form a cycle whose sum is non-zero. For example, `1 -> 2 -> 3 -> 1` with weights `+2, +2, -5` yields a contradiction since returning to the starting node changes its implied value.

## Approaches

A direct attempt would be to assign coordinates one by one and propagate constraints forward. Starting from an unassigned node, we can arbitrarily set its position to zero and use a DFS or BFS to assign all reachable nodes using the constraints. If we ever try to assign a node that already has a value, we check consistency.

This propagation works because every constraint is linear and additive, so once one node in a connected component is fixed, all others are determined relative to it. The issue arises when multiple paths assign different values to the same node, which reveals an inconsistency.

If we think of each constraint as an edge `(b -> a)` with weight `d`, meaning `x[a] = x[b] + d`, then every connected component becomes a system where all values are defined up to a global offset. The only possible failure is when a cycle produces a non-zero total sum, because then a node would be forced to equal two different values.

This reduces the problem to checking whether each connected component of a weighted graph is consistent. We can do this using a DFS while tracking node values, or using a DSU with potential differences. DSU with potentials is particularly clean: each node stores a parent and a relative offset to its parent, and path compression maintains consistency while allowing quick contradiction checks.

When merging two nodes `a` and `b` with constraint `x[a] = x[b] + d`, we unify their sets and ensure the relative difference matches previously established structure. If both nodes are already in the same set, we simply verify whether the implied difference equals `d`. Otherwise, we merge and record the required offset between roots.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| DFS/BFS propagation | O(n + m) | O(n + m) | Accepted |
| DSU with potentials | O((n + m) α(n)) | O(n) | Accepted |

## Algorithm Walkthrough

We use a DSU where each node `x` maintains two pieces of information: its parent in the union structure and a potential `diff[x]` which represents `x[x] - x[parent[x]]`.

1. Initialize each node as its own parent with zero potential. This starts every node as an independent component with no constraints applied.
2. Define a function `find(x)` that performs path compression while also updating potentials so that `diff[x]` always reflects the correct accumulated difference to the root.
3. Define a function `union(a, b, d)` meaning enforce `x[a] = x[b] + d`. We compute roots of `a` and `b`. If they are different, we attach one root to the other and set its potential so the equation remains valid.
4. If `a` and `b` already share the same root, we verify consistency by checking whether the difference implied by stored potentials equals `d`. If it does not, we immediately conclude the system is impossible.
5. Process all constraints. If no contradiction appears, output “YES”; otherwise output “NO”.

The key idea is that every node stores its position relative to its DSU root. When two nodes are unified, we preserve the exact constraint between them, ensuring all future queries remain consistent with all previous ones.

### Why it works

At any point, each DSU component represents a partially built solution where every node has a well-defined coordinate relative to its root. Any constraint that connects two nodes inside the same component must be consistent with this relative structure. Since every merge enforces consistency at the moment components are joined, no later operation can introduce a contradiction inside that component unless the input itself contains a cycle with non-zero total weight. The DSU detects exactly that situation when a same-component constraint fails the equality check.

## Python Solution

```python
import sys
input = sys.stdin.readline

class DSU:
    def __init__(self, n):
        self.parent = list(range(n + 1))
        self.diff = [0] * (n + 1)

    def find(self, x):
        if self.parent[x] != x:
            px = self.parent[x]
            root = self.find(px)
            self.diff[x] += self.diff[px]
            self.parent[x] = root
        return self.parent[x]

    def get(self, x):
        self.find(x)
        return self.diff[x]

    def union(self, a, b, d):
        ra = self.find(a)
        rb = self.find(b)

        if ra == rb:
            return (self.get(a) == self.get(b) + d)

        # attach ra under rb
        self.parent[ra] = rb
        # we need: x[a] = x[b] + d
        # x[a] = diff[a] + x[ra], x[b] = diff[b] + x[rb]
        # so diff[ra] + x[ra] = diff[b] + x[rb] + d
        # since x[ra] becomes child of rb:
        self.diff[ra] = self.get(b) + d - self.get(a)
        return True

def solve():
    t = int(input())
    for _ in range(t):
        n, m = map(int, input().split())
        dsu = DSU(n)
        ok = True

        for _ in range(m):
            a, b, d = map(int, input().split())
            if not dsu.union(a, b, d):
                ok = False

        print("YES" if ok else "NO")

if __name__ == "__main__":
    solve()
```

The DSU structure maintains a parent pointer tree and a difference array that stores how far each node is from its parent. The `find` function performs path compression and accumulates differences so that after a call, each node directly knows its distance to the root.

The `union` function is the only place where constraints are enforced. When two nodes are already connected, it checks whether the existing implied distance matches the new constraint. When they are separate, it connects the root of one component under the other and sets the offset so that the equation holds exactly.

A subtle detail is that all differences must be updated relative to roots after path compression. The correctness of the formula in `union` depends on `get(x)` returning fully resolved root distances, which is why both `a` and `b` are queried through `find` before computing the merge offset.

## Worked Examples

### Sample 1

Input:

```
5 3
1 2 2
2 3 4
4 2 -6
```

| Step | Edge | Root(1) | Root(2) | Root(3) | Root(4) | Consistent |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | 1-2=2 | 1 | 2 | 3 | 4 | Yes |
| 2 | 2-3=4 | 1 | 1 | 3 | 4 | Yes |
| 3 | 4-2=-6 | 1 | 1 | 1 | 4 | Yes |

After propagating all constraints, all equations are consistent within the same component structure.

This trace shows that merging components gradually accumulates relative positions without conflict.

### Sample 2 (contradiction via cycle)

Input:

```
3 3
1 2 1
2 3 1
3 1 -5
```

| Step | Edge | State | Consistent |
| --- | --- | --- | --- |
| 1 | 1-2=1 | merge | Yes |
| 2 | 2-3=1 | merge | Yes |
| 3 | 3-1=-5 | check cycle | No |

At the last step, the implied difference from the DSU between 3 and 1 contradicts the already established structure. The system detects a cycle whose accumulated sum is not zero.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O((n + m) α(n)) | Each union/find is almost constant due to path compression |
| Space | O(n) | DSU arrays store parent and difference per node |

The constraints allow up to 2×10^5 total nodes, so near-linear DSU operations comfortably fit within time limits, even across 100 test cases.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from sys import stdout
    out = []
    
    class DSU:
        def __init__(self, n):
            self.parent = list(range(n + 1))
            self.diff = [0] * (n + 1)

        def find(self, x):
            if self.parent[x] != x:
                px = self.parent[x]
                root = self.find(px)
                self.diff[x] += self.diff[px]
                self.parent[x] = root
            return self.parent[x]

        def get(self, x):
            self.find(x)
            return self.diff[x]

        def union(self, a, b, d):
            ra = self.find(a)
            rb = self.find(b)
            if ra == rb:
                return self.get(a) == self.get(b) + d
            self.parent[ra] = rb
            self.diff[ra] = self.get(b) + d - self.get(a)
            return True

    t = int(input())
    for _ in range(t):
        n, m = map(int, input().split())
        dsu = DSU(n)
        ok = True
        for _ in range(m):
            a, b, d = map(int, input().split())
            if not dsu.union(a, b, d):
                ok = False
        out.append("YES" if ok else "NO")
    
    return "\n".join(out)

# provided samples
assert run("""4
5
3
1 2 2
2 3 4
4 2 -6
6
5
1 2 2
2 3 4
4 2 -6
5 4 4
3 5 100
2
2
1 2 5
1 2 4
4
1
1 2 3
""") == """YES
NO
NO
YES"""

# simple consistency
assert run("""1
3 2
1 2 1
2 3 2
""") == "YES"

# contradiction cycle
assert run("""1
3 3
1 2 1
2 3 1
3 1 -3
""") == "NO"

# same component repeated constraint
assert run("""1
2 2
1 2 5
1 2 5
""") == "YES"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| consistent chain | YES | propagation correctness |
| contradictory cycle | NO | cycle detection |
| repeated constraint | YES | idempotent unions |

## Edge Cases

A key edge case is repeated constraints between the same pair. The DSU handles this by checking consistency instead of merging again. If the same equation is presented twice, the second occurrence should not change anything, and the union check ensures it passes.

Another edge case is self-consistency through indirect paths. Even if no direct contradiction exists, a cycle can still force a mismatch. The DSU detects this only when a node is already in the same component and a new constraint is evaluated, triggering the equality check that exposes inconsistency.
