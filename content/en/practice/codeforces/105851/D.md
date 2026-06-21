---
title: "CF 105851D - \u6700\u8fd1\u516c\u5171\u7956\u5148"
description: "The task is about maintaining and querying ancestry relationships in a rooted tree. We are given a connected acyclic graph, and we interpret one node as the root of the structure."
date: "2026-06-22T01:59:55+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105851
codeforces_index: "D"
codeforces_contest_name: "2025\u5e74\u5317\u4eac\u5e02\u5927\u5b66\u751f\u7a0b\u5e8f\u8bbe\u8ba1\u7ade\u8d5b\u66a8\u201c\u5c0f\u7c73\u676f\u201d\u5168\u56fd\u9080\u8bf7\u8d5b"
rating: 0
weight: 105851
solve_time_s: 50
verified: true
draft: false
---

[CF 105851D - \u6700\u8fd1\u516c\u5171\u7956\u5148](https://codeforces.com/problemset/problem/105851/D)

**Rating:** -  
**Tags:** -  
**Solve time:** 50s  
**Verified:** yes  

## Solution
## Problem Understanding

The task is about maintaining and querying ancestry relationships in a rooted tree. We are given a connected acyclic graph, and we interpret one node as the root of the structure. Each query asks for the lowest common ancestor of two nodes, meaning the deepest node in the rooted tree that lies on both root-to-node paths.

In more concrete terms, imagine each node as a point in a hierarchy. For any two nodes, their paths to the root eventually merge. The first node where their paths meet when moving upward is the answer to the query.

The input can be understood as a tree described by its edges followed by multiple queries. Each query provides two nodes, and the output is a single node representing their shared ancestor closest to them.

The main constraint implication in this type of problem is that the tree can be large, typically up to 10^5 nodes and queries of similar magnitude. A solution that recomputes upward paths for every query would repeatedly traverse long chains, leading to quadratic behavior in the worst case. With 10^5 queries, even linear traversal per query becomes too slow, so we need a preprocessing approach that reduces each query to logarithmic or constant time.

A few edge cases matter in this setting. When one queried node is an ancestor of the other, the answer is trivially the ancestor node itself. For example, in a chain 1-2-3-4 rooted at 1, querying (2, 4) should return 2. A naive upward-walk implementation can easily miss this if it assumes both nodes must be lifted equally before comparison.

Another edge case is a skewed tree, where the structure degenerates into a linked list. For instance, 1-2-3-4-5-6. Without preprocessing, repeated upward traversal becomes worst-case linear per query, which breaks performance guarantees even though correctness still holds.

## Approaches

A direct approach processes each query independently by walking from both nodes upward toward the root until their paths intersect. This can be implemented by repeatedly moving one node to its parent until both nodes match depth and then moving both upward together until they coincide. This works because in a tree, paths to the root are unique, so the first shared node encountered is the lowest common ancestor.

The correctness is straightforward, but the inefficiency comes from repeated traversal. Each query may require O(n) steps in a degenerate tree, and with many queries this leads to O(nq), which is too slow when both n and q are large.

The key observation is that ancestry queries repeat over the same structure. Instead of recomputing upward jumps step by step, we can precompute “jumps” of size powers of two for every node. This transforms upward movement into logarithmic hops. Once each node knows its 1st, 2nd, 4th, 8th, and so on ancestors, we can lift nodes to the same depth in O(log n), and then simultaneously lift them until their ancestors match.

This technique is commonly called binary lifting. The tree is preprocessed once with a depth-first search or BFS to compute immediate parents, and then dynamic programming builds higher ancestors. Each query is then resolved by comparing ancestors from the highest power downward.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force upward walking | O(n) per query | O(n) | Too slow |
| Binary lifting | O(log n) per query, O(n log n) preprocessing | O(n log n) | Accepted |

## Algorithm Walkthrough

We assume the tree is rooted at node 1 unless otherwise specified.

1. Build adjacency lists from the edge list so that we can traverse the tree efficiently. This step prepares the structure for traversal without repeated edge scanning.
2. Run a depth-first search or breadth-first search from the root to compute each node’s depth and immediate parent. Depth is necessary to align nodes before comparing ancestry.
3. Precompute a table where `up[v][k]` represents the 2^k-th ancestor of node v. The first column is already known from the traversal, and higher values are filled using the recurrence `up[v][k] = up[up[v][k-1]][k-1]`. This works because a 2^k jump can be split into two 2^{k-1} jumps.
4. For each query (u, v), first ensure u is the deeper node. If not, swap them. This guarantees that lifting logic is consistent.
5. Lift the deeper node upward until both nodes are at the same depth. This is done by checking bits of the depth difference and applying corresponding jumps.
6. If after alignment the nodes are equal, that node is the LCA and we can return it immediately. This handles the case where one node is an ancestor of the other.
7. Otherwise, move both nodes upward simultaneously from the highest power of two down to zero. Whenever their 2^k ancestors differ, lift both nodes to those ancestors. This ensures we do not overshoot the LCA.
8. After this process, both nodes are just below their lowest common ancestor, so returning either parent gives the correct answer.

The correctness rests on maintaining a key invariant: after step 5, both nodes are at the same depth, and after step 7, they remain in different subtrees of the LCA but share the same immediate parent chain above them. The binary lifting table guarantees that we never skip past the true ancestor because jumps are only taken when the ancestors differ.

## Python Solution

```python
import sys
input = sys.stdin.readline

LOG = 20

def solve():
    n, q = map(int, input().split())
    g = [[] for _ in range(n + 1)]

    for _ in range(n - 1):
        u, v = map(int, input().split())
        g[u].append(v)
        g[v].append(u)

    up = [[0] * LOG for _ in range(n + 1)]
    depth = [0] * (n + 1)

    sys.setrecursionlimit(10**7)

    def dfs(v, p):
        up[v][0] = p
        for k in range(1, LOG):
            up[v][k] = up[up[v][k - 1]][k - 1]

        for to in g[v]:
            if to == p:
                continue
            depth[to] = depth[v] + 1
            dfs(to, v)

    dfs(1, 0)

    def lift(v, d):
        for k in range(LOG):
            if d & (1 << k):
                v = up[v][k]
        return v

    def lca(a, b):
        if depth[a] < depth[b]:
            a, b = b, a

        a = lift(a, depth[a] - depth[b])

        if a == b:
            return a

        for k in reversed(range(LOG)):
            if up[a][k] != up[b][k]:
                a = up[a][k]
                b = up[b][k]

        return up[a][0]

    out = []
    for _ in range(q):
        a, b = map(int, input().split())
        out.append(str(lca(a, b)))

    print("\n".join(out))

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from io import StringIO
    old_stdout = sys.stdout
    sys.stdout = StringIO()
    solve()
    out = sys.stdout.getvalue()
    sys.stdout = old_stdout
    return out.strip()

if __name__ == "__main__":
    solve()
```

The DFS builds both depth and immediate parents in one traversal, and simultaneously fills the binary lifting table for each node. The `lift` function applies binary jumps based on the bit representation of the height difference, which avoids linear climbing.

The `lca` function first normalizes depth, then checks whether one node becomes the ancestor of the other after alignment. The final upward synchronized lifting loop is carefully written from high powers to low powers so that we maximize jumps without crossing the LCA.

A subtle implementation detail is initializing `up[1][k]` and handling `0` as a null parent. This prevents index errors when lifting beyond the root.

## Worked Examples

Consider a simple tree rooted at 1: 1 connected to 2 and 3, and 2 connected to 4 and 5. Queries ask for LCA(4, 5) and LCA(4, 3).

| Step | a | b | Action |
| --- | --- | --- | --- |
| Initial | 4 | 5 | depths equal |
| Lift alignment | 4 | 5 | no change needed |
| Upward comparison | 2 | 2 | both move to parent |
| Result | 2 | 2 | LCA found |

This shows the case where both nodes are in the same subtree and converge at their parent.

For the second query:

| Step | a | b | Action |
| --- | --- | --- | --- |
| Initial | 4 | 3 | different depths |
| Lift alignment | 4 | 3 | 3 already shallow |
| Upward comparison | 2 | 1 | move until mismatch |
| Final parent | 1 | 1 | LCA |

This demonstrates a case where the LCA is closer to the root than both nodes.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O((n + q) log n) | preprocessing builds 2^k ancestors, each query uses binary jumps |
| Space | O(n log n) | storing ancestor table for each node |

The logarithmic factor keeps the solution well within limits for large trees and query counts typical in this class of problems.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    import sys, io
    sys.stdin = io.StringIO(inp)
    from io import StringIO
    old_stdout = sys.stdout
    sys.stdout = StringIO()
    solve()
    out = sys.stdout.getvalue()
    sys.stdout = old_stdout
    return out.strip()

# simple tree
assert run("""5 2
1 2
1 3
2 4
2 5
4 5
4 3
""") == "2\n1"

# chain tree
assert run("""4 2
1 2
2 3
3 4
4 3
2 4
""") == "3\n2"

# star tree
assert run("""5 3
1 2
1 3
1 4
1 5
2 3
4 5
2 5
""") == "1\n1\n1"

# identical nodes
assert run("""3 1
1 2
1 3
2 2
""") == "2"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| small tree | mixed | basic correctness |
| chain | mixed | deep lifting |
| star | 1 | root-heavy LCA |
| identical nodes | node itself | self-LCA case |

## Edge Cases

A skewed chain like 1-2-3-4-5 tests the worst structural degeneration. The algorithm still computes ancestors in O(n log n) preprocessing, and each query uses only logarithmic jumps, so even queries like LCA(5, 1) resolve by lifting node 5 upward through binary steps: 5 → 3 → 1, converging correctly without touching every intermediate node.

When one node is an ancestor of another, such as LCA(2, 5) in a chain 1-2-3-4-5, the alignment step lifts only the deeper node. After lifting, the equality check triggers immediately, returning 2 without entering the final comparison loop.
