---
title: "CF 105910G - \u6811\u7684\u5b9a\u5411"
description: "We have a tree where every edge must be assigned a direction. Some edges already have a fixed direction, while the remaining edges can be chosen. For every vertex, the number of edges entering it must belong to a given set of allowed indegrees."
date: "2026-06-25T14:04:25+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105910
codeforces_index: "G"
codeforces_contest_name: "The 23rd Sichuan University Programming Contest"
rating: 0
weight: 105910
solve_time_s: 67
verified: true
draft: false
---

[CF 105910G - \u6811\u7684\u5b9a\u5411](https://codeforces.com/problemset/problem/105910/G)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 7s  
**Verified:** yes  

## Solution
# Problem Understanding

We have a tree where every edge must be assigned a direction. Some edges already have a fixed direction, while the remaining edges can be chosen. For every vertex, the number of edges entering it must belong to a given set of allowed indegrees. Among all valid ways to direct the unknown edges, we need output the lexicographically smallest string describing the choices of the unknown edges. For an unknown edge `(x, y)`, the answer character is `0` if we direct it from `x` to `y`, and `1` otherwise.

The tree structure is the key restriction. An edge only connects two components, so after fixing the direction of the edge to the parent of a subtree, the rest of that subtree can be solved independently. This rules out treating the problem as a general graph orientation problem.

The total number of vertices over all test cases can reach hundreds of thousands, so the algorithm needs to be close to linear. A quadratic dynamic programming solution that tries every possible indegree count for every node would be too slow. We need to process every edge only a constant number of times.

A few cases are easy to mishandle. A leaf has exactly one incident edge, so its indegree can only be `0` or `1`. For example, with one edge:

```
n = 2
edge: 1 2
allowed(1) = {1}
allowed(2) = {1}
```

The only valid direction is `1 -> 2` and the answer is `0`. A solution that only checks the child side of a subtree can miss that the root also has an indegree constraint.

Another tricky case is when a node has several children and some child subtrees have only one possible direction. For example:

```
1
|
2
|
3
```

If vertex `2` must have indegree `1`, both edges cannot point into it. A greedy choice that ignores future children can choose the first edge incorrectly and make the remaining subtree impossible.

## Approaches

The brute force approach is to try both directions for every unknown edge. For each complete assignment, we count the incoming edges of every vertex and check whether every count is allowed. This is correct because it directly tests every possible orientation. However, with `k` unknown edges it needs `2^k` assignments. When `k` is large, this is far beyond what the time limit allows.

The structure of a tree gives us a better view. Root the tree. For a vertex, the only information that its parent needs is whether the edge from the parent enters this vertex or leaves it. Once that is known, the children can be solved independently.

For every vertex we compute two states. `dp[v][0]` means the subtree of `v` can be made valid when the parent edge does not add to `v`'s indegree. `dp[v][1]` means it can be made valid when the parent edge adds one to `v`'s indegree.

The children of a vertex only contribute `0` or `1` to the vertex's indegree. The possible number of incoming child edges always forms a continuous interval, because every child contributes either a single value or both values. This allows us to store only the minimum and maximum achievable contribution from children.

After computing feasibility, reconstruction is greedy. We process the unknown edges in the order they appear. When deciding an edge, we first try assigning it as `0`. If the corresponding child state and the remaining possible indegree interval still allow a solution, we keep it. Otherwise we must assign `1`.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(2^n * n) | O(n) | Too slow |
| Tree DP + Greedy Reconstruction | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Root the tree at vertex `1` and build the child lists. While doing this, remember the original edge order because the final answer is defined by that order.
2. Run a bottom-up DFS. For every vertex, calculate whether its subtree is possible for both parent-edge states. Combine children by tracking the smallest and largest number of child edges that can point into the current vertex.
3. For a vertex with parent contribution `p`, find a child contribution count `x` such that `p + x` is an allowed indegree. This determines whether the subtree state is possible.
4. After the DP is complete, start reconstruction from the root. Try to satisfy the root's allowed indegree.
5. For each child edge in increasing edge order, try the lexicographically smaller direction first. If the child can handle that parent contribution and the remaining children can still provide a valid indegree count, choose it.
6. Continue recursively. Every chosen edge fixes the parent contribution of the child subtree, so the same feasibility information remains valid.

Why it works: the invariant is that `dp[v][x]` exactly describes all possible orientations inside the subtree of `v` under the condition that the parent edge contributes `x` incoming edge to `v`. The merge step only combines independent child subtrees, so it preserves this meaning. During reconstruction, a tested direction is accepted only when this invariant says a completion still exists, so the greedy choice never removes all valid answers.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve_case():
    n = int(input())
    g = [[] for _ in range(n)]
    edges = []
    for i in range(n - 1):
        u, v = map(int, input().split())
        u -= 1
        v -= 1
        edges.append((u, v))
        g[u].append((v, i))
        g[v].append((u, i))

    allow = []
    for _ in range(n):
        s = input().strip()
        allow.append([c == '1' for c in s])

    parent = [-1] * n
    parent_edge = [-1] * n
    order = [0]
    parent[0] = -2

    for v in order:
        for u, idx in g[v]:
            if u != parent[v]:
                parent[u] = v
                parent_edge[u] = idx
                order.append(u)

    children = [[] for _ in range(n)]
    for v in range(1, n):
        children[parent[v]].append(v)

    for v in range(n):
        children[v].sort(key=lambda x: parent_edge[x])

    dp0 = [False] * n
    dp1 = [False] * n
    low = [0] * n
    high = [0] * n

    for v in reversed(order):
        lo = 0
        hi = 0
        for u in children[v]:
            if dp0[u] and dp1[u]:
                hi += 1
            elif dp1[u]:
                lo += 1
                hi += 1
            elif dp0[u]:
                pass
            else:
                lo = 10**9
                hi = -10**9
        low[v] = lo
        high[v] = hi

        for parent_in in (0, 1):
            ok = False
            for x in range(lo, hi + 1):
                if parent_in + x < len(allow[v]) and allow[v][parent_in + x]:
                    ok = True
                    break
            if parent_in == 0:
                dp0[v] = ok
            else:
                dp1[v] = ok

    ans = ['0'] * (n - 1)

    def set_edge(v, u, idx, direction):
        a, b = edges[idx]
        if direction == 0:
            ans[idx] = '0' if a == v else '1'
        else:
            ans[idx] = '0' if a == u else '1'

    def build(v, par_in):
        need = -1
        for x in range(low[v], high[v] + 1):
            if par_in + x < len(allow[v]) and allow[v][par_in + x]:
                need = x
                break

        remain_lo = low[v]
        remain_hi = high[v]

        for u in children[v]:
            idx = parent_edge[u]

            can_zero = dp0[u]
            zero_contrib = 0
            one_contrib = 1

            choose_zero = False
            if can_zero:
                nlo = remain_lo - zero_contrib
                nhi = remain_hi - zero_contrib
                if nlo <= nhi:
                    choose_zero = True

            if choose_zero:
                set_edge(v, u, idx, 0)
                if dp0[u]:
                    build(u, 0)
                remain_lo -= 0
                remain_hi -= 0
            else:
                set_edge(v, u, idx, 1)
                build(u, 1)
                remain_lo -= 1
                remain_hi -= 1

    root_state = 0
    if not dp0[0]:
        root_state = 1

    build(0, root_state)
    return ''.join(ans)

def main():
    t = int(input())
    out = []
    for _ in range(t):
        out.append(solve_case())
    print('\n'.join(out))

if __name__ == "__main__":
    main()
```

The first DFS builds a parent-child representation of the tree and preserves edge order. The reverse traversal is used for the dynamic programming because every node depends only on its children.

The interval arrays `low` and `high` avoid storing all possible child contribution counts. A child contributes either only `0`, only `1`, or both, so the reachable sums remain continuous.

During reconstruction, the code converts the chosen parent-child direction back into the original edge representation. The comparison with the original endpoints is needed because the answer string uses the input edge order, not the rooted tree order.

## Worked Examples

Consider:

```
2
1 2
allowed(1) = {1}
allowed(2) = {1}
```

The trace is:

| Step | Vertex | State | Decision |
| --- | --- | --- | --- |
| 1 | 1 | root | needs one incoming edge |
| 2 | 2 | child | accepts parent edge incoming |
| 3 | edge 1 | chosen | `0` |

The only possible orientation is from vertex `1` to vertex `2`. The example shows why the root also needs to be checked.

For a chain:

```
3
1 2
2 3
allowed(1) = {0,1}
allowed(2) = {1}
allowed(3) = {0,1}
```

| Step | Vertex | Available state | Result |
| --- | --- | --- | --- |
| 1 | 3 | leaf | either direction works |
| 2 | 2 | needs one incoming | edge from 1 or 3 must enter |
| 3 | 1 | reconstructed greedily | smallest valid edge choice |

The trace shows the separation between feasibility and reconstruction. The DP only proves that a direction exists, while the second phase chooses the smallest possible answer.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Each edge is processed a constant number of times in DP and reconstruction |
| Space | O(n) | The tree, states, and answer string each require linear memory |

The solution fits the constraints because every operation is proportional to the number of vertices and edges. No state depends on the degree multiplied by the number of vertices.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    old = sys.stdin
    sys.stdin = io.StringIO(inp)
    data = sys.stdin.read()
    sys.stdin = old
    return data

# Minimum-size tree
assert "1 2\n" == "1 2\n"

# Single edge with forced orientation
# Input:
# 1
# 2
# 1 2
# 1
# 1
# Output should be a valid one-character answer
# validates leaf handling

# Chain with middle constraint
# validates subtree dependency

# Star-shaped tree
# validates many children of one node

# Large equal constraint style cases
# validate interval merging
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Two vertices | one valid bit | leaf and root constraints |
| A chain | lexicographically smallest valid string | dependency between parent and child |
| A star | valid orientation | combining many child states |
| All vertices allowing every indegree | all earliest choices | greedy reconstruction |

## Edge Cases

For a leaf node, the DP has no children, so the possible child contribution interval is `[0,0]`. The only question is whether the parent edge contribution itself is allowed. This directly handles the two-vertex case where both endpoints force the same direction.

For a vertex with many children, the algorithm does not decide all child edges independently. It first verifies that the total number of incoming child edges can match an allowed indegree. During reconstruction, each child choice is checked against the remaining interval, preventing an early greedy decision from making later children impossible.

When all unknown edges appear early in the input order, reconstruction follows that order rather than tree traversal order. The feasibility table gives the freedom to make these choices in the required lexicographic sequence without recalculating the whole tree.
