---
title: "CF 103328C - Perfect Cactus"
description: "We are given a simple undirected graph that is guaranteed to be a cactus, meaning every edge belongs to at most one simple cycle. The task is to decide whether this graph is a perfect graph."
date: "2026-07-03T14:06:33+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 103328
codeforces_index: "C"
codeforces_contest_name: "National Taiwan University NCPC Preliminary 2021"
rating: 0
weight: 103328
solve_time_s: 51
verified: true
draft: false
---

[CF 103328C - Perfect Cactus](https://codeforces.com/problemset/problem/103328/C)

**Rating:** -  
**Tags:** -  
**Solve time:** 51s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a simple undirected graph that is guaranteed to be a cactus, meaning every edge belongs to at most one simple cycle. The task is to decide whether this graph is a perfect graph.

Perfection here is not something we can directly compute from the definition, since checking all induced subgraphs and comparing clique number with chromatic number is infeasible. Instead, we rely on the Strong Perfect Graph Theorem, which characterizes perfect graphs as exactly those without induced odd cycles of length at least 5 and without their complements.

So the problem reduces to a structural question on the cactus: does it contain any induced odd cycle of length at least 5, or any induced odd antihole.

The cactus constraint is the key simplification. Since edges belong to at most one cycle, cycles are cleanly separated and do not overlap in complex ways. This means any non-tree behavior is localized to simple cycles, and we can reason about each cycle independently with only mild interaction through tree attachments.

The input size goes up to 100000 vertices and edges, so any solution must be close to linear. Anything quadratic or even n log n with heavy constants is fine, but anything that attempts to enumerate subgraphs, cycles naively, or simulate coloring is too slow.

A subtle point is that not every cycle in the cactus is automatically an induced cycle in the graph. If a cycle has a chord, it is not a simple cycle in a cactus, so we are safe there. However, the main pitfall is that attachments to a cycle via tree edges do not affect induced subgraph structure on the cycle itself, so each cycle can be treated as induced.

Edge cases arise when the graph is a tree, when there is exactly one cycle, or when multiple cycles share articulation points. For example, a tree is always perfect because it is bipartite. A single 5-cycle is not perfect, but a 4-cycle is perfect. The complement condition is more subtle, but for cacti it turns out that any violation comes directly from the presence of an odd cycle of length at least 5.

A naive approach that tries to run a general perfect graph recognition algorithm would fail because those algorithms are far more complex and unnecessary under the cactus constraint.

## Approaches

The brute-force perspective starts from the definition: for every induced subgraph, we would need to compare clique number and chromatic number. Even if we restrict ourselves using the Strong Perfect Graph Theorem, we would still need to detect induced odd cycles and induced odd antiholes.

For a general graph, detecting induced cycles of all lengths and their complements is expensive. Enumerating all simple cycles already takes exponential time in worst cases. Even in a cactus, listing cycles is manageable, but checking antiholes directly is not.

The key observation is that cactus structure collapses the problem. Every cycle is isolated except at articulation points, so any induced cycle present in the graph is exactly one of the simple cycles in the cactus. Moreover, induced odd antiholes cannot appear in a cactus unless they correspond to very small structured cases, and these reduce to the same cycle condition after simplification.

This means the problem reduces to scanning all simple cycles in the cactus and checking whether any cycle of length at least 5 is odd.

Once we accept this reduction, the task becomes straightforward: find all cycle lengths in the cactus using DFS, compute their parity, and check if any forbidden cycle exists.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute force induced subgraph checking | Exponential | O(n) | Too slow |
| Cycle extraction in cactus + parity check | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

We root the cactus anywhere and perform a DFS to detect back edges that form cycles. Since the graph is a cactus, each edge belongs to at most one cycle, so each back edge uniquely determines a cycle.

1. Run a DFS while maintaining parent pointers and depth for each vertex. This allows us to reconstruct any cycle encountered via a back edge.
2. When we encounter a back edge from a node u to an ancestor v, we reconstruct the cycle by walking from u back through parent pointers until v. The cycle length is the number of vertices visited in this backtracking plus one for the closing edge. This works cleanly because the graph has no overlapping cycles.
3. For each detected cycle, compute its length. If the length is at least 5 and odd, we immediately conclude the graph is not perfect.
4. If no such cycle exists after exploring all edges, we conclude the graph is perfect.

The reconstruction step is safe because in a cactus, the DFS tree ensures that any non-tree edge corresponds to exactly one simple cycle, and there is no ambiguity in cycle structure.

### Why it works

In a cactus, every cycle is isolated in the sense that it shares edges with no other cycle. Therefore, any cycle detected through DFS back edges corresponds exactly to a unique simple cycle in the graph. Since induced subgraphs on cycles are preserved (no extra chords exist), the only way to violate perfectness is to contain an odd cycle of length at least 5, which is directly detected by scanning cycle lengths.

## Python Solution

```python
import sys
input = sys.stdin.readline
sys.setrecursionlimit(10**7)

n, m = map(int, input().split())
g = [[] for _ in range(n)]
for _ in range(m):
    u, v = map(int, input().split())
    u -= 1
    v -= 1
    g[u].append(v)
    g[v].append(u)

parent = [-1] * n
depth = [0] * n
vis = [0] * n

bad = False

def dfs(u, p):
    global bad
    vis[u] = 1
    for v in g[u]:
        if v == p:
            continue
        if not vis[v]:
            parent[v] = u
            depth[v] = depth[u] + 1
            dfs(v, u)
        else:
            if depth[v] < depth[u]:
                length = 1
                cur = u
                while cur != v:
                    length += 1
                    cur = parent[cur]
                if length >= 5 and length % 2 == 1:
                    bad = True

for i in range(n):
    if not vis[i]:
        dfs(i, -1)

print("No" if bad else "Yes")
```

The DFS maintains a parent pointer tree so that when we encounter a back edge, we can reconstruct the cycle by walking upward. The depth check ensures we only count back edges toward ancestors and avoid double counting cross edges in the undirected traversal.

The cycle reconstruction is linear in the cycle length, and since each edge in a cactus belongs to at most one cycle, total reconstruction work across all cycles is linear overall.

A subtle implementation detail is skipping the direct parent edge, otherwise every undirected edge would be misclassified as a back edge.

## Worked Examples

### Example 1

Input:

```
5 5
1 2
2 3
3 4
4 5
5 1
```

This forms a single 5-cycle.

| Step | Event | Cycle Found | Length | Bad Flag |
| --- | --- | --- | --- | --- |
| DFS traversal | Explore cycle | Yes | 5 | True |

When the back edge closes the cycle, we reconstruct all 5 vertices. The length is 5, which is odd and at least 5, so the graph is immediately classified as not perfect.

Output is:

```
No
```

This demonstrates that odd cycles of length 5 are forbidden and are directly detected.

### Example 2

Input:

```
5 4
1 2
2 3
3 4
4 5
```

This is a tree.

| Step | Event | Cycle Found | Length | Bad Flag |
| --- | --- | --- | --- | --- |
| DFS traversal | No back edges | No | - | False |

No cycle is ever detected, so no violation occurs.

Output is:

```
Yes
```

This confirms that trees are perfect in this setting.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n + m) | Each edge is processed once in DFS, and cycle reconstruction over all cycles is linear in total due to cactus structure |
| Space | O(n + m) | Adjacency list plus DFS bookkeeping arrays |

The linear complexity fits comfortably within the constraints of 100000 vertices and edges.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    n, m = map(int, input().split())
    g = [[] for _ in range(n)]
    for _ in range(m):
        u, v = map(int, input().split())
        u -= 1
        v -= 1
        g[u].append(v)
        g[v].append(u)

    parent = [-1] * n
    depth = [0] * n
    vis = [0] * n
    bad = False

    sys.setrecursionlimit(10**7)

    def dfs(u, p):
        nonlocal bad
        vis[u] = 1
        for v in g[u]:
            if v == p:
                continue
            if not vis[v]:
                parent[v] = u
                depth[v] = depth[u] + 1
                dfs(v, u)
            else:
                if depth[v] < depth[u]:
                    length = 1
                    cur = u
                    while cur != v:
                        length += 1
                        cur = parent[cur]
                    if length >= 5 and length % 2 == 1:
                        bad = True

    for i in range(n):
        if not vis[i]:
            dfs(i, -1)

    return "No" if bad else "Yes"

# sample 1
assert run("""5 5
1 2
2 3
3 4
4 5
5 1
""") == "No"

# sample 2
assert run("""5 4
1 2
2 3
3 4
4 5
""") == "Yes"

# triangle (should be perfect)
assert run("""3 3
1 2
2 3
3 1
""") == "Yes"

# square (perfect)
assert run("""4 4
1 2
2 3
3 4
4 1
""") == "Yes"

# single edge
assert run("""2 1
1 2
""") == "Yes"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 5-cycle | No | detects forbidden odd cycle |
| path | Yes | tree case |
| triangle | Yes | small odd cycle is allowed |
| 4-cycle | Yes | even cycle is fine |
| single edge | Yes | minimal graph |

## Edge Cases

A tree input contains no cycles, so the DFS never triggers back-edge reconstruction. The algorithm leaves `bad` as false and correctly outputs Yes.

A pure 4-cycle triggers exactly one cycle reconstruction of length 4. Since the condition requires length at least 5, it does not set the bad flag, matching the fact that 4-cycles are bipartite and therefore perfect.

A 5-cycle is the only minimal forbidden structure in this setting. The moment the back edge closes the cycle, reconstruction walks exactly five nodes and immediately marks the graph as not perfect.
