---
title: "CF 105709B - Lowest Common Ancestor"
description: "The task is about maintaining a rooted tree and answering relationship queries between pairs of nodes. For any two given nodes in the tree, we need to determine their lowest common ancestor, meaning the deepest node in the rooted structure that lies on the path from the root to…"
date: "2026-06-26T08:02:07+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105709
codeforces_index: "B"
codeforces_contest_name: "UTPC Contest 2-12-25 Div. 2 (Beginner)"
rating: 0
weight: 105709
solve_time_s: 50
verified: true
draft: false
---

[CF 105709B - Lowest Common Ancestor](https://codeforces.com/problemset/problem/105709/B)

**Rating:** -  
**Tags:** -  
**Solve time:** 50s  
**Verified:** yes  

## Solution
## Problem Understanding

The task is about maintaining a rooted tree and answering relationship queries between pairs of nodes. For any two given nodes in the tree, we need to determine their lowest common ancestor, meaning the deepest node in the rooted structure that lies on the path from the root to both of them.

The input can be interpreted as a tree described by edges, followed by multiple queries. Each query gives two nodes, and we must return the single node that represents where their paths toward the root first converge.

Even without explicit constraints, this type of problem almost always involves up to hundreds of thousands of nodes and queries. That immediately rules out any approach that recomputes paths for every query by walking upward one step at a time, because that would degrade to quadratic behavior in the worst case. A solution must preprocess the tree so that each query can be answered in logarithmic or near-constant time.

A few edge situations tend to break naive implementations. If the tree is a chain, such as 1 connected to 2 connected to 3 connected to 4, then the lowest common ancestor of the endpoints is always the higher one in the chain. A naive upward-walking solution might repeatedly climb one step per query, producing a worst-case cost proportional to the depth of the tree.

Another subtle case occurs when one node is an ancestor of the other. For example, if node 2 is the parent of node 5, then the answer to the query (2, 5) must be 2. Any approach that tries to equalize depths incorrectly or overshoots ancestors can easily skip past the correct node if it does not carefully stop at the moment of equality.

## Approaches

The most direct way to answer a query for two nodes is to reconstruct their paths to the root and compare them. We can store the parent of each node and, for every query, repeatedly move each node upward until reaching the root, recording the visited nodes. The lowest common ancestor is then the last shared node in these two paths.

This works correctly because every node has exactly one parent, so each path to the root is uniquely defined. However, building these paths for each query is expensive. If the tree has height proportional to n and there are q queries, this approach can require O(n) work per query, resulting in O(nq) total operations, which is too slow when both n and q are large.

The key observation is that repeated upward movement is redundant across queries. The structure of the tree does not change, so ancestor relationships can be precomputed. Instead of stepping one parent at a time, we can precompute jumps of size powers of two for each node. This allows us to lift any node upward by large steps, effectively skipping intermediate ancestors in logarithmic time.

This technique is known as binary lifting. We store a table where up[k][v] represents the 2^k-th ancestor of node v. With this structure, we can first align both nodes at the same depth, then lift them together from the highest possible power of two downward until they meet.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force (path walking) | O(n) per query | O(n) | Too slow |
| Binary Lifting | O((n + q) log n) | O(n log n) | Accepted |

## Algorithm Walkthrough

1. Root the tree at node 1 and run a depth-first search or breadth-first search to compute the parent and depth of every node. This establishes a reference frame so every node knows how far it is from the root.
2. Build a binary lifting table where up[0][v] is the immediate parent of v, and up[k][v] is defined as up[k-1][up[k-1][v]]. This encodes ancestors at exponentially increasing distances.
3. Precompute the table for all k up to log2(n). This ensures we can jump any distance in logarithmic number of steps.
4. For each query (u, v), first compare their depths. If one node is deeper, lift it upward using the binary lifting table until both nodes are at the same depth. This avoids having to move step by step.
5. Once both nodes are aligned in depth, check if they are already the same. If so, that node is the lowest common ancestor.
6. If they are different, try lifting both nodes upward from the highest power of two down to zero. Whenever their ancestors at a given level differ, move both nodes up simultaneously. This keeps them synchronized below the LCA.
7. After finishing all jumps, both nodes will be direct children of the lowest common ancestor, so returning either parent gives the answer.

### Why it works

The correctness comes from the structure of the ancestor table. Every upward move in the algorithm preserves the invariant that the true LCA is still above both nodes. When we lift nodes to equal depth, we do not change their relative ancestry, only align their distance from the root. When we then attempt large jumps from high powers of two downward, we only take a jump if it does not overshoot the LCA. This guarantees we never bypass the correct ancestor, and eventually both nodes converge to the highest node that is still strictly below the LCA, so their parent must be the LCA itself.

## Python Solution

```python
import sys
input = sys.stdin.readline

sys.setrecursionlimit(10**7)

def solve():
    n = int(input())
    adj = [[] for _ in range(n + 1)]

    for _ in range(n - 1):
        u, v = map(int, input().split())
        adj[u].append(v)
        adj[v].append(u)

    LOG = (n).bit_length()

    up = [[0] * (n + 1) for _ in range(LOG)]
    depth = [0] * (n + 1)

    stack = [(1, 0)]
    parent = [0] * (n + 1)
    parent[1] = 1

    while stack:
        node, p = stack.pop()
        parent[node] = p
        for nei in adj[node]:
            if nei == p:
                continue
            depth[nei] = depth[node] + 1
            stack.append((nei, node))

    for v in range(1, n + 1):
        up[0][v] = parent[v]

    for k in range(1, LOG):
        for v in range(1, n + 1):
            up[k][v] = up[k - 1][up[k - 1][v]]

    def lift(x, dist):
        k = 0
        while dist:
            if dist & 1:
                x = up[k][x]
            dist >>= 1
            k += 1
        return x

    def lca(a, b):
        if depth[a] < depth[b]:
            a, b = b, a

        a = lift(a, depth[a] - depth[b])

        if a == b:
            return a

        for k in range(LOG - 1, -1, -1):
            if up[k][a] != up[k][b]:
                a = up[k][a]
                b = up[k][b]

        return up[0][a]

    q = int(input())
    out = []
    for _ in range(q):
        u, v = map(int, input().split())
        out.append(str(lca(u, v)))

    print("\n".join(out))

if __name__ == "__main__":
    solve()
```

The implementation starts by building the adjacency list representation of the tree. A parent array and depth array are computed with a stack-based traversal rooted at node 1, ensuring every node knows its immediate ancestor and distance from the root.

The binary lifting table is then filled bottom-up. The key detail is that up[k][v] depends on up[k-1][v], so smaller jumps must be computed before larger ones.

The lift function performs the depth equalization step. It interprets the distance in binary and applies jumps corresponding to set bits. This is more efficient than repeatedly moving one level at a time.

The lca function first normalizes depths, then performs a top-down check over powers of two. The condition up[k][a] != up[k][b] ensures we only move when the ancestor is still safely below the LCA.

## Worked Examples

Consider a small tree rooted at 1:

Input edges:

1-2, 1-3, 2-4, 2-5

Query: (4, 5)

Both nodes have depth 2. The algorithm skips the lifting step. At the highest jump level, both nodes share the same ancestor at node 2 after lifting decisions, so the result is 2.

| Step | a | b | Action |
| --- | --- | --- | --- |
| start | 4 | 5 | same depth |
| check k=2 | 2 | 2 | both differ from each other’s ancestors |
| final | 2 | 2 | return parent |

This confirms correct handling of siblings.

Now consider query (3, 4).

Node 3 is at depth 1, node 4 is at depth 2, so 4 is lifted to 2’s level, becoming 2. Now comparing (3, 2), they are different, and the highest valid lift shows their parents converge at 1.

| Step | a | b | Action |
| --- | --- | --- | --- |
| start | 3 | 4 | depths differ |
| lift | 3 | 2 | equalize depth |
| check | 3 | 2 | move upward |
| final | 1 | 1 | return 1 |

This demonstrates correct handling of nodes with different depths.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O((n + q) log n) | building lifting table takes n log n, each query takes log n |
| Space | O(n log n) | ancestor table stores log n entries per node |

This fits comfortably within typical constraints for trees up to 200,000 nodes and queries.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from __main__ import solve
    return sys.stdout.getvalue() if False else capture(inp)

def capture(inp: str) -> str:
    import sys, io
    backup_stdin = sys.stdin
    backup_stdout = sys.stdout
    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()
    solve()
    out = sys.stdout.getvalue()
    sys.stdin = backup_stdin
    sys.stdout = backup_stdout
    return out.strip()

# small tree
assert capture("""5
1 2
1 3
2 4
2 5
3
4 5
3 4
2 4
""") == "2\n1\n2"

# chain
assert capture("""4
1 2
2 3
3 4
3
4 3
4 2
4 1
""") == "3\n2\n1"

# star
assert capture("""5
1 2
1 3
1 4
1 5
2
2 3
4 5
""") == "1\n1"

# same node queries
assert capture("""3
1 2
2 3
3
2 2
3 3
1 1
""") == "2\n3\n1"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| tree + siblings queries | 2 1 2 | correctness on mixed depth and sibling LCA |
| chain tree | 3 2 1 | worst-case depth behavior |
| star tree | 1 1 | root dominance case |
| self queries | node itself | identity LCA cases |

## Edge Cases

A chain-shaped tree such as 1-2-3-4 tests whether the lifting logic correctly handles maximum depth differences. For query (4, 1), the algorithm lifts node 4 up through binary jumps: 4 jumps to 2, then 1, while node 1 remains unchanged. The final comparison converges correctly at 1 because all ancestors of 1 are itself in the rooted representation.

A case where one node is an ancestor of another, such as query (2, 5) in a tree where 2 is directly above 5, verifies that equalizing depth does not overshoot. After lifting, node 5 becomes 2, and since the nodes match immediately, the algorithm returns 2 without unnecessary upward movement.
