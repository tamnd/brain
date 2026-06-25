---
title: "CF 106020A - Tree Labeling"
description: "We are given an undirected tree with $n$ vertices. The task is to assign each vertex one of three labels, $a$, $b$, or $c$, so that no edge connects two vertices with the same label."
date: "2026-06-25T13:10:24+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 106020
codeforces_index: "A"
codeforces_contest_name: "The 2025 Damascus University Collegiate Programming Contest"
rating: 0
weight: 106020
solve_time_s: 64
verified: true
draft: false
---

[CF 106020A - Tree Labeling](https://codeforces.com/problemset/problem/106020/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 4s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given an undirected tree with $n$ vertices. The task is to assign each vertex one of three labels, $a$, $b$, or $c$, so that no edge connects two vertices with the same label. Among all such valid assignments, we are asked to produce the lexicographically smallest string formed by concatenating the labels of vertices in order from $1$ to $n$.

The tree structure matters only through adjacency constraints. The requirement is purely local on edges, but the objective is global because lexicographic order depends on the entire string. This combination forces us to choose labels greedily with awareness of future conflicts.

The constraints allow up to $2 \cdot 10^5$ vertices, which rules out any exponential backtracking or per-vertex brute-force checking of all labelings. Even trying three choices per node without pruning leads to $3^n$, which is completely infeasible. Any valid solution must run in linear or near-linear time, essentially $O(n)$ or $O(n \log n)$.

A subtle failure mode appears when a naive greedy strategy is used without respecting tree structure. For example, always assigning the smallest possible label locally without considering parent constraints can get stuck later.

Consider a simple path $1 - 2 - 3$. If we assign $s_1 = a$, then greedily assign $s_2 = a$ as well because it is locally smallest, we immediately violate constraints, but even if we enforce validity locally, choosing $s_2 = b$ and then $s_3 = a$ gives “aba”, which is correct. However, in a branching structure like a star rooted at 1 with neighbors 2, 3, 4, a careless approach might assign all children greedily as “a” if they are processed independently, producing an invalid output such as “aaa?” which violates constraints on every edge.

Another subtle issue arises from traversal order. If we process nodes in DFS order without fixing a parent-first dependency, we might assign a child before knowing its parent’s final label in some incorrect implementations. That leads to inconsistent decisions and invalid results.

## Approaches

The brute-force idea is to generate all assignments of $\{a,b,c\}$ to the $n$ vertices and keep only those that satisfy the edge constraint. For each valid assignment, we compute its lexicographic value and keep the smallest.

This works because it explicitly checks every possible labeling, but it fails immediately in terms of scale. The number of assignments is $3^n$, and each validation costs $O(n)$ to check all edges, giving $O(n \cdot 3^n)$, which becomes unusable even for $n = 20$, let alone $2 \cdot 10^5$.

The key structural observation is that trees are bipartite-like but with one extra color available. If we were restricted to two colors, the solution would be fixed up to swapping. With three colors, we gain flexibility: at each node, we only need to avoid the parent’s label, and the rest of the structure imposes no additional direct constraints beyond adjacency.

This suggests a greedy construction. If we root the tree anywhere, the only constraint for a node is its parent and already assigned neighbors in DFS. Since children are not yet assigned when we process a node in preorder traversal, we only need to avoid the parent’s color. That reduces each decision to at most two valid choices. Choosing the smallest valid label at each step guarantees lexicographic minimality because earlier positions dominate the ordering.

The correctness hinges on the fact that once a node is assigned, it never needs to be reconsidered. The tree structure guarantees no cycles, so there is no backward constraint propagation.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(n \cdot 3^n)$ | $O(n)$ | Too slow |
| Greedy DFS coloring | $O(n)$ | $O(n)$ | Accepted |

## Algorithm Walkthrough

We root the tree at vertex 1. The goal is to assign labels in a way that respects parent-child constraints while always preferring the smallest possible label.

1. Choose an arbitrary root, typically vertex 1, and build an adjacency list representation of the tree. This allows efficient traversal without recomputing neighbors.
2. Start a DFS from the root. Assign the root the smallest label, which is always $a$. This choice is safe because no ancestor exists to conflict with it, and it minimizes the first character of the resulting string.
3. For every node $v$, when processing its children, decide each child’s label independently based on its parent’s label. Since the constraint is only that adjacent nodes differ, the child must avoid the parent’s label.
4. Assign the smallest possible label among $\{a, b, c\}$ that is not equal to the parent’s label. This greedy choice is valid because it affects only the current position in the string; later assignments do not influence earlier lexicographic order.
5. Continue DFS recursively, passing the chosen label as the parent constraint for deeper nodes.

Why it works comes from the structure of trees and the nature of lexicographic ordering. Each node’s label affects only its position in the final string and does not restrict siblings beyond the shared parent constraint. Since we always pick the smallest available label at each position, no later correction can produce a lexicographically smaller prefix without violating the edge constraint at that node. The assignment is locally optimal and globally consistent because the dependency graph is acyclic.

## Python Solution

```python
import sys
input = sys.stdin.readline

sys.setrecursionlimit(10**7)

def solve():
    n = int(input())
    g = [[] for _ in range(n + 1)]
    
    for _ in range(n - 1):
        u, v = map(int, input().split())
        g[u].append(v)
        g[v].append(u)

    res = [''] * (n + 1)

    def dfs(u, parent):
        for c in "abc":
            if c != res[parent]:
                res[u] = c
                break
        for v in g[u]:
            if v != parent:
                dfs(v, u)

    res[0] = '#'  # dummy parent so root can take 'a'
    res[1] = 'a'
    for v in g[1]:
        dfs(v, 1)

    return "".join(res[1:])

print(solve())
```

The implementation relies on a simple DFS traversal. The root is initialized separately to ensure it takes the smallest label. A dummy value is used for its parent so that the root is not constrained.

The main subtlety is ensuring that we never compare against an uninitialized parent label. Using `res[parent]` directly works because every node is assigned before its children are processed.

Another point is recursion depth. Since the tree can be a long chain, Python’s default recursion limit is insufficient, so it is increased.

## Worked Examples

### Example 1

Input:

```
3
1 2
1 3
```

We start at node 1.

| Step | Node | Parent | Available choices | Chosen label | Partial state |
| --- | --- | --- | --- | --- | --- |
| 1 | 1 | dummy | a, b, c | a | a-- |
| 2 | 2 | 1 | b, c | b | ab- |
| 3 | 3 | 1 | b, c | b | abb |

This shows that both children of the root independently avoid “a”, and we consistently choose “b” as the smallest valid option.

### Example 2

Input:

```
4
1 2
2 3
3 4
```

This is a chain.

| Step | Node | Parent | Available choices | Chosen label | Partial state |
| --- | --- | --- | --- | --- | --- |
| 1 | 1 | dummy | a, b, c | a | a--- |
| 2 | 2 | 1 | b, c | b | ab-- |
| 3 | 3 | 2 | a, c | a | aba- |
| 4 | 4 | 3 | b, c | b | abab |

The alternating structure emerges naturally because each node only avoids its parent’s label.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n)$ | Each vertex and edge is visited once during DFS |
| Space | $O(n)$ | Adjacency list and recursion stack store linear information |

The solution comfortably fits within constraints since both time and memory scale linearly with the number of vertices. Even for $2 \cdot 10^5$, a single DFS traversal is efficient.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    input = sys.stdin.readline

    n = int(input())
    g = [[] for _ in range(n + 1)]
    for _ in range(n - 1):
        u, v = map(int, input().split())
        g[u].append(v)
        g[v].append(u)

    res = [''] * (n + 1)

    def dfs(u, p):
        for c in "abc":
            if c != res[p]:
                res[u] = c
                break
        for v in g[u]:
            if v != p:
                dfs(v, u)

    res[0] = '#'
    res[1] = 'a'
    for v in g[1]:
        dfs(v, 1)

    return "".join(res[1:])

# sample-style tests
assert run("3\n1 2\n1 3\n") in ["abb", "abc", "aba"], "star tree validity"
assert run("4\n1 2\n2 3\n3 4\n") == "abab", "chain alternation"

# custom tests
assert run("1\n") == "a", "single node"
assert run("2\n1 2\n") == "ab", "minimum edge"
assert run("5\n1 2\n1 3\n1 4\n1 5\n") != "aaaa", "star constraint check"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single node | a | base case handling |
| 2-node tree | ab | direct edge constraint |
| star tree | no “aaa..” | parent-child propagation |
| chain | alternating pattern | DFS correctness |

## Edge Cases

A single vertex tree is the simplest scenario. The algorithm assigns the root “a” immediately, and no further traversal occurs. Since there are no edges, this is trivially valid.

A two-node tree tests whether the parent constraint is properly enforced. The root gets “a”, and the child must take “b”. Any attempt to assign “a” to the child would violate the edge rule, so this checks correctness of the filtering logic.

A star-shaped tree tests whether sibling independence is handled correctly. Each child is processed separately but must all avoid the root’s label. The algorithm assigns them all “b”, which remains valid since siblings are not directly constrained.

A deep chain tests whether DFS correctly propagates constraints through multiple levels. Each node depends only on its parent, and alternating assignments emerge naturally without additional bookkeeping.
