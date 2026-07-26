---
title: "CF 102835G - Graph Cards"
description: "The input describes a deck of graph cards. Each card contains an undirected simple graph. A card is valid because the graph has the same number of vertices and edges and is connected, which means every card represents a connected unicyclic graph: a tree with exactly one…"
date: "2026-07-26T14:59:26+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102835
codeforces_index: "G"
codeforces_contest_name: "The 2020 ICPC Asia Taipei-Hsinchu Site Programming Contest"
rating: 0
weight: 102835
solve_time_s: 41
verified: true
draft: false
---

[CF 102835G - Graph Cards](https://codeforces.com/problemset/problem/102835/G)

**Rating:** -  
**Tags:** -  
**Solve time:** 41s  
**Verified:** yes  

## Solution
## Problem Understanding

The input describes a deck of graph cards. Each card contains an undirected simple graph. A card is valid because the graph has the same number of vertices and edges and is connected, which means every card represents a connected unicyclic graph: a tree with exactly one additional edge. Two cards are considered the same when their graphs can be relabeled to become identical. The task is to count how many different graph shapes appear in the whole deck.

The graph labels on the input are irrelevant. A graph with vertices numbered `1,2,3` and the same graph with vertices numbered `10,20,30` should contribute only once. The challenge is to build a representation of the structure that ignores vertex names.

The number of vertices in a card can be large, so checking every pair of graphs with a general graph isomorphism algorithm is not practical. A general isomorphism comparison can be very expensive, while this problem has extra structure. A connected graph with equal numbers of vertices and edges has exactly one cycle, and everything outside that cycle is a collection of rooted trees. That structure lets us create a canonical representation in linear time per card.

The edge cases come from the symmetry of the cycle and from trees attached to the cycle. A naive traversal from an arbitrary vertex fails because the chosen starting point may be different for two identical graphs.

For example, the following two cards describe the same cycle with differently numbered vertices:

```
1
3 1 2 2 3 3 1
3 2 3 3 1 1 2
```

The correct output is:

```
1
```

A traversal that records the order in which vertices are visited can produce different strings because it starts from different places on the cycle.

Another common mistake is ignoring that a cycle can be traversed in either direction. For example:

```
1
4 1 2 2 3 3 4 4 1
4 1 4 4 3 3 2 2 1
```

The correct output is:

```
1
```

The second graph is just the first graph viewed backwards. A representation that only checks rotations but not reversed rotations treats them as different.

A third edge case is a cycle vertex having several attached branches. Consider a cycle where one vertex has two identical leaf children. The children have no order, so sorting the child descriptions is required. Without sorting, two equivalent trees can receive different encodings.

## Approaches

The brute-force idea is to compare every pair of cards and run a graph isomorphism check. This works because two cards are identical exactly when an isomorphism exists between their graphs. The problem is that if there are many cards, the number of comparisons becomes quadratic. With `n` cards, this already requires `O(n^2)` comparisons, and each comparison may need to inspect every edge and vertex, making the total work far too large.

The useful observation is that every graph in this problem has exactly one cycle. We do not need a general graph isomorphism algorithm. We can first identify the unique cycle, remove it conceptually, and look at the rooted trees hanging from each cycle vertex.

A rooted tree has a simple canonical form. A leaf is represented by an empty pair of parentheses. A vertex is represented by the sorted list of its children's canonical forms surrounded by parentheses. Sorting removes the dependency on child ordering.

The only remaining difficulty is the cycle itself. The cycle is a circular sequence of rooted-tree descriptions. Two circular sequences are equal if one can be rotated or reversed to obtain the other. We generate the smallest representation among all rotations of the sequence and all rotations of the reversed sequence.

The brute-force method fails because it repeatedly solves the same structural problem. The canonical representation solves it once per card and turns equality checking into string or tuple comparison.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(C² · V) | O(V) | Too slow |
| Optimal | O(C · V log V) | O(V) | Accepted |

Here `C` is the number of cards and `V` is the total number of vertices in one card. The logarithmic factor comes from sorting children of tree nodes.

## Algorithm Walkthrough

1. Read one graph card and build its adjacency list. The vertex numbers are only temporary identifiers, because the final representation must not depend on them.
2. Find the unique cycle using leaf pruning. Every vertex whose degree is one cannot be part of the cycle, so repeatedly removing leaves leaves exactly the cycle vertices. This works because a unicyclic graph has only one closed component.
3. For every cycle vertex, compute the canonical form of the tree attached to it while ignoring the two cycle neighbors. The tree encoding recursively combines all child encodings in sorted order.
4. Put the obtained tree encodings into the order around the cycle. The starting cycle vertex is arbitrary, so generate every rotation. Also generate every rotation of the reversed order because the same cycle can be walked in the opposite direction.
5. Choose the lexicographically smallest cycle representation. This value is the canonical identifier of the entire graph.
6. Insert the identifier into a set. After all cards are processed, the size of the set is the number of different graph cards.

Why it works:

The tree encoding is unique because every node is represented by the multiset of its child subtrees, and sorting converts that multiset into a deterministic order. The cycle encoding is unique because every possible choice of starting point and direction is considered. Any two isomorphic unicyclic graphs must have the same cycle length and the same sequence of attached rooted trees up to rotation and reversal, so their canonical identifiers match. Non-isomorphic graphs cannot produce the same identifier because the identifier reconstructs the complete cycle and every attached tree.

## Python Solution

```python
import sys
input = sys.stdin.readline

def rooted_tree_code(v, parent, adj, on_cycle):
    children = []
    for u in adj[v]:
        if u != parent and not on_cycle[u]:
            children.append(rooted_tree_code(u, v, adj, on_cycle))
    children.sort()
    return "(" + "".join(children) + ")"

def canonical_graph(edges, n):
    adj = [[] for _ in range(n)]
    for u, v in edges:
        adj[u].append(v)
        adj[v].append(u)

    degree = [len(x) for x in adj]
    alive = [True] * n
    stack = [i for i in range(n) if degree[i] == 1]

    while stack:
        v = stack.pop()
        alive[v] = False
        for u in adj[v]:
            if alive[u]:
                degree[u] -= 1
                if degree[u] == 1:
                    stack.append(u)

    cycle = [i for i in range(n) if alive[i]]
    on_cycle = alive[:]

    cycle_adj = [[] for _ in range(n)]
    for v in cycle:
        for u in adj[v]:
            if on_cycle[u]:
                cycle_adj[v].append(u)

    start = cycle[0]
    order = []
    prev = -1
    cur = start

    while True:
        order.append(cur)
        nxt = cycle_adj[cur][0]
        if nxt == prev:
            nxt = cycle_adj[cur][1]
        prev, cur = cur, nxt
        if cur == start:
            break

    parts = [rooted_tree_code(v, -1, adj, on_cycle) for v in order]

    m = len(parts)
    best = None

    for arr in (parts, list(reversed(parts))):
        for i in range(m):
            cand = tuple(arr[i:] + arr[:i])
            if best is None or cand < best:
                best = cand

    return best

def solve():
    t = int(input())
    ans = []
    for _ in range(t):
        cards = int(input())
        seen = set()

        for _ in range(cards):
            data = list(map(int, input().split()))
            k = data[0]
            vals = data[1:]

            edges = []
            mx = 0
            for i in range(k):
                u = vals[2 * i] - 1
                v = vals[2 * i + 1] - 1
                edges.append((u, v))
                mx = max(mx, u, v)

            seen.add(canonical_graph(edges, mx + 1))

        ans.append(str(len(seen)))

    print("\n".join(ans))

if __name__ == "__main__":
    solve()
```

The adjacency list stores the temporary graph representation. The leaf-pruning loop removes every tree vertex and leaves only the unique cycle. The boolean `on_cycle` array separates the cycle from the attached trees.

`rooted_tree_code` never enters another cycle vertex, so every recursive call stays inside one rooted tree. The children are sorted before building the result, which is the detail that removes dependence on input ordering.

The cycle traversal creates one direction of the cycle. The final loop handles all possible starting positions and both directions. A tuple is used for the final identifier because it compares naturally and avoids ambiguity between concatenated strings.

The implementation does not use recursion on the cycle itself. The recursion depth is only the depth of attached trees, which is the part that needs to be represented structurally.

## Worked Examples

Consider a single triangle card:

```
1
3 1 2 2 3 3 1
```

The trace is:

| Step | Remaining cycle | Attached tree codes | Current best |
| --- | --- | --- | --- |
| After pruning | 1,2,3 | `()`, `()`, `()` | unset |
| First direction | `(),(),()` | all rotations equal | `(),(),()` |
| Reverse direction | `(),(),()` | all rotations equal | `(),(),()` |

The graph receives one canonical identifier, so identical triangles are merged.

Consider a cycle with one extra leaf:

```
1
4 1 2 2 3 3 1 1 4
```

The trace is:

| Step | Remaining cycle | Attached tree codes | Current best |
| --- | --- | --- | --- |
| After pruning | 1,2,3 | `(()),(),()` | unset |
| Rotation 1 | `(()),(),()` | chosen | `(()),(),()` |
| Other rotations | `(),(()),()` and `(),(),(())` | larger | unchanged |
| Reverse rotations | checked | unchanged | `(()),(),()` |

The leaf is attached to a specific cycle vertex, and the canonical cycle order preserves that relationship.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(V log V) per card | Each vertex is processed once, and child lists are sorted during tree encoding |
| Space | O(V) | The adjacency list, pruning arrays, and recursion state store information for one card |

The algorithm avoids pairwise graph comparisons, so the total work grows linearly with the number of cards. The structure of unicyclic graphs is what makes canonicalization possible within the limits.

## Test Cases

```python
import sys
import io

def run(inp: str) -> str:
    old = sys.stdin
    sys.stdin = io.StringIO(inp)
    data = sys.stdin.read().split()
    sys.stdin = old

    it = iter(data)
    t = int(next(it))
    out = []

    for _ in range(t):
        c = int(next(it))
        seen = set()
        for _ in range(c):
            k = int(next(it))
            edges = []
            mx = 0
            for _ in range(k):
                u = int(next(it)) - 1
                v = int(next(it)) - 1
                edges.append((u, v))
                mx = max(mx, u, v)
            seen.add(canonical_graph(edges, mx + 1))
        out.append(str(len(seen)))

    return "\n".join(out)

assert run("""1
2
4 1 2 2 3 3 1 1 4
4 1 2 2 3 3 1 2 4
""") == "1"

assert run("""1
3
3 1 2 2 3 3 1
4 1 2 2 3 3 4 4 1
4 1 4 4 3 3 2 2 1
""") == "2"

assert run("""1
1
3 1 2 2 3 3 1
""") == "1"

assert run("""1
2
4 1 2 2 3 3 1 1 4
5 1 2 2 3 3 1 1 4 4 5
""") == "2"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Two differently labeled triangles | 1 | Ignores vertex numbering |
| Cycles with reversed traversal | 2 | Handles reflection symmetry |
| Single triangle | 1 | Minimum cycle-only graph |
| Same cycle with an added branch | 2 | Distinguishes attached trees |

## Edge Cases

A cycle with no attached trees is handled because every cycle vertex receives the same empty tree code. The cycle normalization still checks rotations and reversals, so a triangle or larger ring is identified correctly regardless of input numbering.

A graph where the only difference is the direction used to walk the cycle is handled by comparing both the original sequence and its reverse. For example, the input

```
1
4 1 2 2 3 3 4 4 1
```

and the same cycle listed backwards both generate the same minimal cyclic representation.

A vertex with many identical children is handled by sorting child encodings. For a cycle vertex connected to two leaves, the attached tree code becomes a sorted combination of two identical leaf codes. The algorithm never depends on the order in which edges appeared in the input, so the same branching structure always receives the same representation.
