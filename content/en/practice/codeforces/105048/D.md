---
title: "CF 105048D - By the pricking of my thumbs, Pupil #1 this way comes"
description: "We are given a tree of people, where each node represents a UT competitive programmer and edges represent mutual knowledge of Codeforces usernames."
date: "2026-06-28T01:22:54+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105048
codeforces_index: "D"
codeforces_contest_name: "UTPC Contest 03-22-24 Div. 2 (Beginner)"
rating: 0
weight: 105048
solve_time_s: 90
verified: false
draft: false
---

[CF 105048D - By the pricking of my thumbs, Pupil #1 this way comes](https://codeforces.com/problemset/problem/105048/D)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 30s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a tree of people, where each node represents a UT competitive programmer and edges represent mutual knowledge of Codeforces usernames. Macbeth starts at node 1, and initially only knows the usernames of node 1 and anyone directly reachable through people whose usernames he has already learned, but only after he explicitly asks someone.

The key mechanic is that when Macbeth asks a person, that person reveals all usernames they know, effectively revealing the entire connected knowledge region reachable through that person in one operation. The goal is to choose a minimum number of such people to ask so that Macbeth eventually learns the usernames of all nodes whose rating is at least his own rating.

The graph structure is a tree, so there is exactly one simple path between any two nodes. This makes propagation patterns deterministic and prevents cycles in knowledge spread.

The constraint of up to 100,000 nodes immediately rules out any solution that recomputes reachability or simulates propagation separately for each node or query. Any solution that is quadratic in the number of nodes would fail. We should expect something around linear or near-linear time, possibly with a greedy or tree dynamic programming structure.

A naive approach would be to consider every high-rated node and simulate whether it is already reachable from previously chosen asks. In a tree, this would still require repeated traversals or union operations, and in worst case could degrade to O(N^2).

A subtle edge case appears when high-rated nodes form a connected subtree that is almost the entire tree. For example, if all nodes except leaves have high rating, a naive approach might redundantly "ask" inside already-covered regions and overcount.

Another edge case is when node 1 is low-rated. Then Macbeth cannot rely on free propagation starting from node 1, so the solution must explicitly ensure all high-rated regions are covered via chosen queries.

## Approaches

A brute-force strategy would be to repeatedly pick an unvisited node whose rating is at least Macbeth’s rating and perform a DFS/BFS from that node, marking all reachable nodes as discovered. Each such choice represents an “ask”, and we continue until all required nodes are covered. This is correct because every ask reveals an entire connected component of known nodes, but it is not efficient because each traversal can cost O(N), and in the worst case we might perform O(N) such operations, leading to O(N^2).

The key observation is that we are not trying to traverse arbitrary reachability, but instead to cover all nodes in a tree that satisfy a condition (rating ≥ threshold). On a tree, any connected set of “bad” nodes (nodes we do not need) acts like a separator. If we conceptually remove all nodes with rating below Macbeth’s, the remaining graph becomes a forest. Each connected component of this forest can be solved with a single ask at any node inside it, because asking any node reveals its entire connected knowledge component, which spans the whole component of valid nodes.

So the problem reduces to counting connected components in the induced subgraph of nodes with rating ≥ r_1.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(N^2) | O(N) | Too slow |
| Optimal (DFS/BFS on filtered tree) | O(N) | O(N) | Accepted |

## Algorithm Walkthrough

We treat nodes with rating at least r_1 as “active”. All other nodes are “blocked”.

1. Mark every node as active if its rating is ≥ r_1, otherwise mark it inactive. This defines the only nodes Macbeth actually cares about.
2. Build adjacency lists for the tree. We will traverse only through active nodes, effectively considering the induced subgraph.
3. Maintain a visited array initialized to false for all nodes.
4. Iterate through all nodes from 1 to N. Whenever we find a node that is active and not yet visited, we start a DFS or BFS from it, but we only move through active nodes.
5. Each time we start such a traversal, we increment our answer by 1. This corresponds to selecting one person to ask, which reveals the entire connected component of active nodes.
6. During DFS/BFS, mark every reachable active node as visited. This ensures we do not recount nodes in the same component.
7. After processing all nodes, output the number of times we started a traversal.

The reason this works is that each DFS run exactly covers one connected component in the subgraph induced by active nodes. Since asking one person reveals everything in their connected knowledge region, one ask per component is both necessary and sufficient.

### Why it works

The algorithm relies on the invariant that at any point, every visited node belongs to exactly one explored connected component of active nodes, and no traversal ever crosses an inactive node. In a tree, removing inactive nodes splits the structure into disconnected components. Each such component is internally reachable, but there is no path between components without passing through an inactive node. Since inactive nodes cannot be used as starting points or bridges for the target set, each component must be discovered independently. Therefore, each DFS initiation corresponds to exactly one required ask, and no two components can be merged by any valid operation.

## Python Solution

```python
import sys
input = sys.stdin.readline
sys.setrecursionlimit(10**7)

def solve():
    n = int(input())
    ratings = list(map(int, input().split()))
    adj = [[] for _ in range(n)]
    
    for _ in range(n - 1):
        p, q = map(int, input().split())
        p -= 1
        q -= 1
        adj[p].append(q)
        adj[q].append(p)

    threshold = ratings[0]
    active = [r >= threshold for r in ratings]
    visited = [False] * n

    def dfs(u):
        stack = [u]
        visited[u] = True
        while stack:
            v = stack.pop()
            for nxt in adj[v]:
                if not visited[nxt] and active[nxt]:
                    visited[nxt] = True
                    stack.append(nxt)

    ans = 0
    for i in range(n):
        if active[i] and not visited[i]:
            ans += 1
            dfs(i)

    print(ans)

if __name__ == "__main__":
    solve()
```

The implementation builds the adjacency list for the tree and then filters nodes using a boolean array `active`. The DFS is iterative to avoid recursion depth issues on long chains. Each time we encounter an unvisited active node, we launch a traversal that marks its entire connected component, and we increment the answer.

A common mistake here is using recursion without increasing recursion depth, which can fail on a skewed tree of size 100,000. Another is forgetting to skip inactive nodes during traversal, which would incorrectly merge components through forbidden nodes.

## Worked Examples

### Example 1

Consider a small tree where nodes 1, 3, and 5 are active, and edges connect them in a chain: 1-2-3-4-5, with nodes 2 and 4 inactive.

| Step | Node | Active | Visited | Action | Components Found |
| --- | --- | --- | --- | --- | --- |
| 1 | 1 | Yes | {1} | Start DFS | 1 |
| 2 | 3 | Yes | {1,3} | Start DFS (new component) | 2 |
| 3 | 5 | Yes | {1,3,5} | Start DFS (new component) | 3 |

This shows that inactive nodes split the chain into separate components, forcing multiple asks.

### Example 2

Now consider a fully active tree of 4 nodes in a star centered at 1.

| Step | Node | Active | Visited | Action | Components Found |
| --- | --- | --- | --- | --- | --- |
| 1 | 1 | Yes | {1,2,3,4} | DFS covers all | 1 |
| 2 | 2 | Yes | already visited | skip | 1 |
| 3 | 3 | Yes | already visited | skip | 1 |
| 4 | 4 | Yes | already visited | skip | 1 |

Only one ask is needed because the entire active graph is connected.

## Complexity Analysis

| Measure | Complexity | Explanation |

|---|---|---|---|

| Time | O(N) | Each node and edge is processed at most once during DFS over the tree |

| Space | O(N) | Adjacency list and visited array store linear information |

The solution fits easily within the constraints because both memory and time grow linearly with the number of nodes, and N is up to 100,000.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from __main__ import solve
    return run_capture(inp)

def run_capture(inp: str) -> str:
    import sys, io
    backup = sys.stdout
    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()
    solve()
    out = sys.stdout.getvalue()
    sys.stdout = backup
    return out.strip()

# minimum case
assert run_capture("1\n5\n") == "1"

# two nodes, different ratings
assert run_capture("2\n5 1\n1 2\n") == "1"

# chain alternating active/inactive
assert run_capture("5\n5 1 5 1 5\n1 2\n2 3\n3 4\n4 5\n") == "3"

# fully active star
assert run_capture("4\n10 10 10 10\n1 2\n1 3\n1 4\n") == "1"

# all inactive except root
assert run_capture("4\n10 1 1 1\n1 2\n1 3\n1 4\n") == "1"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 node | 1 | minimal graph |
| 2-node pair | 1 | direct connectivity |
| alternating chain | 3 | split components |
| full star active | 1 | single component |
| root-only active | 1 | isolated single node component |

## Edge Cases

One edge case is when only node 1 is active. The input

```
4
10 1 1 1
1 2
1 3
1 4
```

produces a single active component consisting only of node 1. The DFS starts at node 1, marks only itself, and no other traversal is initiated. The answer is 1, matching the expectation that Macbeth needs only one ask.

Another edge case is a long alternating path such as

```
5
5 1 5 1 5
1 2
2 3
3 4
4 5
```

Here, inactive nodes act as separators, producing three isolated active nodes. Each DFS call triggers exactly one component traversal, giving an output of 3. The algorithm correctly avoids crossing inactive nodes, so no component is merged incorrectly.
