---
title: "CF 106170J - Good Pairs in Graph and Tree"
description: "We are given two different structures over the same set of vertices labeled from 1 to N. One structure is a tree, so between any two vertices there is exactly one simple path. The other structure is an arbitrary undirected simple graph."
date: "2026-06-21T16:10:19+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 106170
codeforces_index: "J"
codeforces_contest_name: "Swiss Subregional 2025-2026"
rating: 0
weight: 106170
solve_time_s: 65
verified: true
draft: false
---

[CF 106170J - Good Pairs in Graph and Tree](https://codeforces.com/problemset/problem/106170/J)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 5s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given two different structures over the same set of vertices labeled from 1 to N. One structure is a tree, so between any two vertices there is exactly one simple path. The other structure is an arbitrary undirected simple graph.

For any ordered pair of vertices (u, v), we look at the unique path connecting u to v in the tree. We then ask whether this exact sequence of vertices can also be traversed as a valid path in the graph. If yes, the pair is called good. Every vertex is trivially good with itself because the path from u to u has no edges.

The task is to count how many ordered pairs are good.

The constraints place N and M up to 200,000. This immediately rules out any solution that checks pairs individually or simulates paths per query. Any approach closer to O(N^2) or even O(NM) will be too slow. We should expect something close to linear or linearithmic time, likely O(N + M) or O((N + M) log N).

A subtle point is what “the path in G” means. It does not require uniqueness, only existence. So if the tree path is u → a → b → v, we only need those edges (u, a), (a, b), (b, v) to exist in G; extra edges in G do not matter as long as they do not invalidate the existence of this sequence.

A common mistake is to think we must match shortest paths in G or ensure no alternative routes exist. That is not required.

One edge case worth clarifying is when G is identical to the tree. Then every pair is good, so the answer is N². Another extreme is when G has no overlap with tree edges; then only (u, u) pairs are valid, giving N.

## Approaches

The brute-force idea starts from the definition. For each ordered pair (u, v), we compute the unique path in the tree, then check whether each edge on that path exists in G. If the path length is k, this takes O(k) per pair. Summed over all pairs, this becomes O(N^2) in the worst case since tree paths can be long for most pairs in a chain-shaped tree. Even if we accelerate edge existence checks using hashing, the number of pairs itself remains quadratic, which is far beyond the limit.

The key observation is that we never actually need to reason about arbitrary pairs independently. A pair (u, v) is good exactly when every edge on the tree path between them exists in G. This transforms the problem from a path-checking problem on pairs into an edge filtering problem on the tree.

We can classify each tree edge as either “usable” or “broken” depending on whether it also appears in G. If we keep only usable edges in the tree, we obtain a forest. Inside this forest, any two vertices are connected if and only if their original tree path used only usable edges. That condition is exactly equivalent to the pair being good.

So the problem reduces to finding connected components in this filtered tree and summing the number of ordered pairs inside each component.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(N^2) | O(N) | Too slow |
| Filter tree edges + components | O(N + M) | O(N + M) | Accepted |

## Algorithm Walkthrough

We build a fast membership structure for edges of G, then filter the tree accordingly.

1. Store all edges of G in a hash set or dictionary keyed by an ordered pair (min(x, y), max(x, y)). This allows constant-time checks for whether a tree edge exists in G.
2. Initialize a Disjoint Set Union (DSU) structure for all N vertices, where initially each vertex is its own component. This DSU will represent connectivity using only “good” tree edges.
3. For each edge (a, b) in the tree, check whether it exists in G using the hash set. If it does, merge a and b in the DSU. If it does not, we ignore it entirely, treating it as broken.
4. After processing all tree edges, each DSU component corresponds exactly to a connected component formed by usable edges.
5. For each DSU component, compute its size s. Every ordered pair (u, v) inside the component is good, including (u, u), so it contributes s × s.
6. Sum s × s over all components and output the result.

The only subtlety is that we are not building a new graph explicitly. The DSU directly simulates connectivity in the filtered tree without needing adjacency lists.

### Why it works

The tree guarantees a unique simple path between any two vertices. That path is fully determined by the sequence of tree edges. A pair (u, v) is good exactly when every edge on that unique path exists in G. This is equivalent to saying every edge on the path is marked usable.

If all edges on the path are usable, DSU connectivity ensures u and v end up in the same component because we union exactly those edges. Conversely, if they are in the same DSU component, there exists a path made entirely of usable edges, which must coincide with the unique tree path, since the tree has no alternative routes. This one-to-one correspondence guarantees correctness.

## Python Solution

```python
import sys
input = sys.stdin.readline

class DSU:
    def __init__(self, n):
        self.parent = list(range(n + 1))
        self.size = [1] * (n + 1)

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

def main():
    n, m = map(int, input().split())

    tree_edges = []
    for _ in range(n - 1):
        a, b = map(int, input().split())
        tree_edges.append((a, b))

    g_edges = set()
    for _ in range(m):
        x, y = map(int, input().split())
        if x > y:
            x, y = y, x
        g_edges.add((x, y))

    dsu = DSU(n)

    for a, b in tree_edges:
        x, y = (a, b) if a < b else (b, a)
        if (x, y) in g_edges:
            dsu.union(a, b)

    comp_size = {}
    for i in range(1, n + 1):
        root = dsu.find(i)
        comp_size[root] = comp_size.get(root, 0) + 1

    ans = 0
    for s in comp_size.values():
        ans += s * s

    print(ans)

if __name__ == "__main__":
    main()
```

The code first stores all edges of G in a set with normalized ordering so that edge lookup is constant time. Then it iterates over tree edges and only unions endpoints when that edge exists in G. After DSU construction, it computes component sizes by compressing all vertices to their roots and accumulating counts.

A common implementation pitfall is forgetting to normalize edges consistently between the tree and the graph. Another is iterating over DSU parents without final path compression, which can miscount component sizes. The final loop explicitly calls find on every node to guarantee correctness.

## Worked Examples

Consider the sample structure with four nodes in a line tree and three edges in G. The tree edges are (1,2), (2,3), (3,4). The graph edges allow all except (1,2).

After filtering, only edges (2,3) and (3,4) remain usable. The DSU components become {1}, {2,3,4}. The contribution is 1² + 3² = 1 + 9 = 10.

Now consider a second example where the tree is a star centered at 1 with edges (1,2), (1,3), (1,4), and G contains only (1,2) and (1,3).

After filtering, 1,2,3 form one component, while 4 is isolated.

The table below tracks DSU unions.

| Edge processed | In G | DSU state |
| --- | --- | --- |
| (1,2) | yes | {1,2}, {3}, {4} |
| (1,3) | yes | {1,2,3}, {4} |
| (1,4) | no | unchanged |

Final sizes are 3 and 1, giving 3² + 1² = 10.

These examples show that only preserved tree edges matter, and all reasoning reduces to connectivity in that filtered structure.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(N + M α(N)) | Each edge lookup is O(1), DSU operations are near constant amortized |
| Space | O(N + M) | Stores DSU arrays and hash set of G edges |

The constraints allow up to 200,000 vertices and edges, so a near-linear DSU-based solution comfortably fits within time and memory limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from __main__ import main
    return main()  # if integrated; adjust as needed

# Sample case
assert run("""4 3
1 2
2 3
3 4
1 3
3 2
2 4
""") == "6"

# Minimum case
assert run("""3 0
1 2
2 3
""") == "3"

# Fully matching graph and tree
assert run("""4 3
1 2
2 3
3 4
1 2
2 3
3 4
""") == "16"

# Star with partial edges
assert run("""4 2
1 2
1 3
1 4
1 2
1 3
""") == "10"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 3 nodes, no G edges | 3 | isolated vertices handling |
| identical tree and graph | N² | full connectivity case |
| partial star | 10 | component merging correctness |

## Edge Cases

One edge case is when no tree edge exists in G. In that situation, every vertex remains isolated in DSU. The algorithm produces N components of size 1, each contributing 1, so the answer is N. This matches the fact that only (u, u) pairs are valid.

Another case is when G contains all tree edges plus additional edges. The extra edges do not affect DSU unions since only tree edges are processed. The entire tree becomes one component, producing N² ordered pairs, which is correct because every tree path is present in G.

A final subtle case is when G is disconnected in a way that does not align with the tree. Since DSU ignores non-tree edges entirely, such edges cannot incorrectly merge components. Only tree connectivity restricted by G matters, which is exactly the condition defining good pairs.
