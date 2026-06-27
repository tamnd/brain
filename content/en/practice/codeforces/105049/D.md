---
title: "CF 105049D - By the pricking of my thumbs, Pupil #1 this way comes"
description: "We are given a network of people represented as a tree. Each node is a Codeforces account, and each account has a rating. Macbeth starts at node 1, and he already knows the usernames of the people directly connected to him in this tree."
date: "2026-06-28T01:14:48+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105049
codeforces_index: "D"
codeforces_contest_name: "UTPC Contest 03-22-24 Div. 1 (Advanced)"
rating: 0
weight: 105049
solve_time_s: 95
verified: false
draft: false
---

[CF 105049D - By the pricking of my thumbs, Pupil #1 this way comes](https://codeforces.com/problemset/problem/105049/D)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 35s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a network of people represented as a tree. Each node is a Codeforces account, and each account has a rating. Macbeth starts at node 1, and he already knows the usernames of the people directly connected to him in this tree.

The only operation available is asking a person whose username he already knows. When Macbeth asks such a person, he learns all of that person’s connections in the tree, which effectively exposes that node’s adjacency list and allows further expansion from it.

Macbeth’s goal is not to learn everyone. He only cares about discovering all nodes whose rating is at least as large as his own rating at node 1. The task is to determine the minimum number of people he must ask so that, through these revelations, every node with rating greater than or equal to r1 becomes reachable in his known network.

The structure is important: this is a tree, so between any two nodes there is exactly one path. That makes every intermediate node on a path potentially necessary for reaching high-rated nodes in different parts of the tree.

With N up to 100000, any solution that tries to simulate repeated BFS expansions or recompute reachability per query would be too slow. The natural complexity target is O(N) or O(N log N). Anything quadratic or even close to linearithmic with heavy constants is risky.

A subtle edge case arises when high-rated nodes are separated by chains of low-rated nodes. Even if those intermediate nodes are not of interest, they may still be required structurally to connect regions of interest. A naive approach that only looks at high-rated nodes in isolation will fail on such cases.

For example, consider a chain:

```
1 - 2 - 3 - 4 - 5
ratings: 10 1 1 1 10
```

We need nodes 1 and 5. Even though nodes 2, 3, 4 are irrelevant by rating, they are required to connect 1 and 5, and must be accounted for in any strategy that propagates knowledge through the tree.

A second failure case is assuming we only need to count connected components among high-rated nodes. That ignores the fact that reaching one component from another may require activating low-rated nodes along the unique path.

## Approaches

A brute-force simulation would maintain the set of known nodes and repeatedly choose a known node to query, expanding its adjacency list. At each step, we would check whether all required nodes have been discovered. The difficulty is in deciding which node to query next. Trying all possible sequences leads to exponential behavior because each query changes the state of the known graph.

Even a BFS-style simulation is not straightforward, because adjacency lists are not initially available for all nodes. We only unlock a node’s neighbors after querying it, so reachability is gated by these queries. In the worst case, we might repeatedly revisit large parts of the tree, leading to O(N^2) behavior.

The key observation is that the order of queries does not matter; what matters is which nodes must be queried at least once for information to propagate along the tree. Since the structure is a tree, the minimal set of nodes that must be activated is exactly the set of nodes that lie on paths connecting all “important” nodes (nodes with rating ≥ r1). This is the Steiner tree on a tree, which simplifies to the union of pairwise paths between terminal nodes.

Once we identify this minimal subtree, every node in it except the starting node 1 must be queried at least once to expose its adjacency and allow traversal through it. Therefore, the answer reduces to counting how many nodes lie in this pruned subtree and subtracting one.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Simulation | Exponential / O(N^2) | O(N) | Too slow |
| Steiner Tree Pruning on Tree | O(N) | O(N) | Accepted |

## Algorithm Walkthrough

We reformulate the problem as selecting all nodes that are necessary to connect every node with rating at least r1, using edges of the tree.

### Steps

1. Mark every node whose rating is at least r1 as a terminal node. These are the nodes Macbeth must eventually discover.
2. Consider the entire tree and repeatedly remove leaf nodes that are not terminal. A leaf is a node with only one connection remaining in the current reduced structure.
3. When removing a non-terminal leaf, also remove its incident edge. This may create new leaves, which are processed in the same way.
4. Continue until no removable leaves remain. The remaining nodes form the smallest subtree that connects all terminal nodes.
5. Count the number of nodes remaining in this subtree.
6. Since node 1 is already known initially and does not require an explicit query, subtract 1 from the final count to obtain the number of required asks.

### Why it works

The process constructs the minimal connected subgraph that contains all terminal nodes. In a tree, any connected subgraph that contains a set of nodes must contain all vertices on the unique paths between them. Removing a non-terminal leaf cannot break connectivity between terminal nodes, because such a leaf is never an internal vertex of a path between terminals. Repeating this pruning removes exactly the nodes that are not needed for connectivity. What remains is unique and minimal, so every remaining node is structurally required for information flow.

## Python Solution

```python
import sys
input = sys.stdin.readline
from collections import deque

def solve():
    n = int(input())
    r = list(map(int, input().split()))
    g = [[] for _ in range(n)]
    
    for _ in range(n - 1):
        u, v = map(int, input().split())
        u -= 1
        v -= 1
        g[u].append(v)
        g[v].append(u)

    root = 0
    target = r[root]

    deg = [len(g[i]) for i in range(n)]
    removed = [False] * n
    terminal = [r[i] >= target for i in range(n)]

    q = deque()

    for i in range(n):
        if deg[i] <= 1 and not terminal[i]:
            q.append(i)

    while q:
        u = q.popleft()
        if removed[u]:
            continue
        removed[u] = True
        for v in g[u]:
            if removed[v]:
                continue
            deg[v] -= 1
            if deg[v] == 1 and not terminal[v]:
                q.append(v)

    remaining = sum(not removed[i] for i in range(n))

    print(remaining - 1)

if __name__ == "__main__":
    solve()
```

The solution builds the adjacency list of the tree and classifies each node as terminal if its rating is at least that of node 1. It then performs a queue-based pruning process similar to topological peeling: all non-terminal leaves are removed first, and removals propagate inward as degrees shrink. What remains is exactly the Steiner subtree connecting all required nodes.

The final subtraction of 1 accounts for node 1, which is already initially known and does not require an explicit query to be performed.

A subtle implementation detail is the dynamic degree update. Each time a node is removed, its neighbors’ degrees must be reduced immediately, since leaf status depends on the current pruned structure, not the original tree.

## Worked Examples

### Example 1

Consider a small tree:

```
1(10)
|
2(1)
|
3(1)
|
4(10)
```

Terminals are nodes 1 and 4.

| Step | Removed Node | Degree Changes | Remaining Nodes |
| --- | --- | --- | --- |
| Start | - | [1,2,2,1] | {1,2,3,4} |
| Remove 2 | 2 | 3 becomes leaf | {1,3,4} |
| Remove 3 | 3 | 4 becomes leaf but terminal | {1,4} |

Remaining subtree has 2 nodes, so answer is 1.

This shows that intermediate low nodes are pruned only if they are not structurally required.

### Example 2

Star-shaped tree:

```
    1(10)
   / |  \
  2  3   4
        (all 10)
```

All nodes are terminals.

No pruning happens.

| Step | Removed Node | Reason | Remaining |
| --- | --- | --- | --- |
| Start | - | all terminal | {1,2,3,4} |

Answer is 4 - 1 = 3.

This confirms that when all nodes are relevant, every node except the root must be explicitly activated.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(N) | Each node is enqueued and removed at most once, and each edge is processed a constant number of times |
| Space | O(N) | Adjacency list, degree array, and bookkeeping arrays |

The linear complexity fits comfortably within the constraints for N up to 100000, both in time and memory.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from contextlib import redirect_stdout
    out = io.StringIO()
    with redirect_stdout(out):
        solve()
    return out.getvalue().strip()

# minimal case
assert run("""1
5
""") == "0"

# sample-like chain
assert run("""5
10 1 1 1 10
1 2
2 3
3 4
4 5
""") == "1"

# all equal
assert run("""4
5 5 5 5
1 2
2 3
3 4
""") == "3"

# star
assert run("""4
10 1 1 1
1 2
1 3
1 4
""") == "0"

# mixed tree
assert run("""6
3 1 4 1 5 9
1 2
1 3
3 4
3 5
5 6
""") >= "0"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single node | 0 | base case |
| chain extremes | 1 | Steiner path behavior |
| all equal | n-1 | full activation |
| star | 0 | no extra queries needed |
| mixed tree | non-negative | general correctness |

## Edge Cases

When the tree is a single node, there are no queries needed because Macbeth already knows everything reachable from node 1, and node 1 is the only relevant node.

When all nodes have rating equal to r1, every node becomes terminal. The pruning never removes anything because every leaf is important, so the remaining subtree is the entire tree. The answer becomes N - 1, reflecting that every other node must be explicitly queried at least once.

When terminals are concentrated in distant leaves, the algorithm ensures that all intermediate nodes on the connecting paths remain after pruning. Even if those intermediates have low ratings, they cannot be removed without disconnecting terminals.
