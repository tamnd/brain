---
title: "CF 103797A - Advisor Enemies"
description: "We are given a collection of precedence rules between named people, where each rule says that one person must appear before another in a valid ordering. Each name is just a string, and every rule is directed from a prerequisite to a dependent."
date: "2026-07-02T08:47:04+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 103797
codeforces_index: "A"
codeforces_contest_name: "IME++ Starters Try-outs 2022"
rating: 0
weight: 103797
solve_time_s: 50
verified: true
draft: false
---

[CF 103797A - Advisor Enemies](https://codeforces.com/problemset/problem/103797/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 50s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a collection of precedence rules between named people, where each rule says that one person must appear before another in a valid ordering. Each name is just a string, and every rule is directed from a prerequisite to a dependent.

The task is to determine whether it is possible to arrange all involved names in some order such that every rule is respected simultaneously. If such an ordering exists, we output a positive verdict, otherwise we report that it is impossible.

Conceptually, each name is a node in a directed graph and each rule is a directed edge. The question becomes whether this directed graph admits a linear ordering consistent with all edges.

The constraints allow up to 100,000 relations, and each name can be up to 30 characters. This size immediately suggests that any quadratic reasoning over all pairs of nodes is impossible. Even constructing an explicit dense adjacency matrix would be infeasible in both memory and time. A linear or near linear graph traversal is required, which points strongly toward graph cycle detection or topological ordering.

A key subtle issue is that nodes are not given as integers. We must map arbitrary strings to compact integer IDs efficiently. Another edge case is duplicate or redundant constraints, which should not affect correctness. Finally, self-loops are impossible by statement, but cycles of length greater than one must be detected.

A naive approach that tries to permute nodes or check all possible orderings would explode combinatorially even for a small number of unique names, since the number of permutations grows factorially.

## Approaches

A direct brute-force strategy would attempt to generate an ordering of all distinct names and verify whether all precedence rules are satisfied. Even if we fix the set of nodes and check all permutations, the complexity becomes factorial in the number of unique names. With up to 100,000 constraints, the number of distinct names can still be large enough that this approach becomes entirely infeasible.

Another naive idea is to repeatedly remove nodes that have no incoming edges, but without careful graph handling this degenerates into repeated scanning of all edges to recompute indegrees, leading to quadratic behavior in the worst case.

The structure of the problem is a directed graph consistency check. The correct insight is that a valid ordering exists if and only if the directed graph is acyclic. Detecting whether a directed graph has a cycle can be done efficiently using either depth-first search with recursion state tracking or Kahn’s algorithm for topological sorting.

Kahn’s algorithm is particularly natural here because it directly simulates repeatedly removing nodes that have no remaining prerequisites. If at some point no such node exists but unprocessed nodes remain, a cycle must exist.

We reduce the problem to building the graph, computing indegrees, and performing a BFS-like elimination process.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute force permutations | O(n!) | O(n) | Too slow |
| Topological sort (Kahn) | O(M + N) | O(M + N) | Accepted |

## Algorithm Walkthrough

We first transform all string names into integer identifiers so that graph operations are efficient. Each unique name is assigned an index when first encountered.

Then we build a directed adjacency list representing all precedence constraints, and compute indegrees for each node.

We then repeatedly select nodes whose indegree is zero, meaning they currently have no unmet prerequisites. These nodes are appended to a processing queue.

We process nodes in this queue one by one, and for each outgoing edge we decrement the indegree of the destination node. If that indegree becomes zero, we add the destination node to the queue.

Finally, we check whether we were able to process all nodes. If yes, the graph is acyclic and a valid ordering exists. If not, there must be a cycle preventing further progress.

Why it works is based on the invariant that any node with indegree zero is safe to place next in a valid ordering, since nothing depends on it being delayed. If a cycle exists, every node in the cycle always has at least one incoming edge from within the cycle, so no node in that cycle can ever reach indegree zero. This prevents the algorithm from consuming all nodes.

## Python Solution

```python
import sys
input = sys.stdin.readline
from collections import defaultdict, deque

def solve():
    m = int(input())
    
    adj = defaultdict(list)
    indeg = defaultdict(int)
    id_map = {}
    idx = 0

    def get_id(x):
        nonlocal idx
        if x not in id_map:
            id_map[x] = idx
            idx += 1
        return id_map[x]

    for _ in range(m):
        a, b = input().split()
        u = get_id(a)
        v = get_id(b)
        adj[u].append(v)
        indeg[v] += 1
        if u not in indeg:
            indeg[u] = indeg[u]

    n = idx
    q = deque()

    for i in range(n):
        if indeg[i] == 0:
            q.append(i)

    processed = 0

    while q:
        u = q.popleft()
        processed += 1
        for v in adj[u]:
            indeg[v] -= 1
            if indeg[v] == 0:
                q.append(v)

    if processed == n:
        print("I disagree with the advisor")
    else:
        print("No more comedians++")

if __name__ == "__main__":
    solve()
```

The code first builds a mapping from strings to integers so that graph storage becomes array-based instead of string-based. This is essential because direct string operations inside graph traversal would introduce unnecessary overhead.

The adjacency list stores all directed constraints, while the indegree dictionary tracks how many prerequisites each node still has. Nodes not appearing as destinations are implicitly initialized with zero indegree.

The queue is initialized with all nodes that have no incoming edges. The BFS loop then simulates repeatedly taking a valid next step in a topological ordering. Each time we remove a node, we reduce the indegree of its neighbors, potentially unlocking new nodes.

The final comparison between processed nodes and total nodes is the cycle detection step. If any node is never processed, it must be part of or blocked by a cycle.

## Worked Examples

### Example 1

Input:

```
JEFF POTATO
JEFF MARK
```

We map JEFF, POTATO, MARK to ids 0, 1, 2. Indegrees start as POTATO:1, MARK:1, JEFF:0.

| Step | Queue | Processed | Indegree changes |
| --- | --- | --- | --- |
| init | [JEFF] | 0 | POTATO=1, MARK=1 |
| take JEFF | [] | 1 | POTATO=0, MARK=0 |
| push newly zero | [POTATO, MARK] | 1 | both unlocked |
| take POTATO | [MARK] | 2 | no outgoing effect |
| take MARK | [] | 3 | done |

All nodes are processed, so the graph is acyclic.

Output:

```
I disagree with the advisor
```

This trace shows how removing prerequisites gradually unlocks dependent nodes until all are reachable.

### Example 2

Input:

```
PETER PARKER
PARKER WAYNE
WAYNE PETER
```

This forms a cycle among three nodes.

| Step | Queue | Processed | Indegree changes |
| --- | --- | --- | --- |
| init | [] | 0 | all have indegree 1 |
| stop | [] | 0 | no zero indegree nodes |

No node can start the process because every node depends on another in the cycle.

Output:

```
No more comedians++
```

This demonstrates the key failure mode: cycles prevent any entry point with zero indegree.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(M + N) | Each edge is processed once, each node is enqueued once |
| Space | O(M + N) | adjacency list and indegree storage plus mapping |

The solution scales linearly with the number of relations, which fits comfortably within the constraints of up to 100,000 edges.

## Test Cases

```python
import sys, io
from collections import defaultdict, deque

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    
    def solve():
        m = int(input())
        adj = defaultdict(list)
        indeg = defaultdict(int)
        id_map = {}
        idx = 0

        def get_id(x):
            nonlocal idx
            if x not in id_map:
                id_map[x] = idx
                idx += 1
            return id_map[x]

        for _ in range(m):
            a, b = input().split()
            u = get_id(a)
            v = get_id(b)
            adj[u].append(v)
            indeg[v] += 1
            if u not in indeg:
                indeg[u] = indeg[u]

        n = idx
        q = deque()
        for i in range(n):
            if indeg[i] == 0:
                q.append(i)

        processed = 0
        while q:
            u = q.popleft()
            processed += 1
            for v in adj[u]:
                indeg[v] -= 1
                if indeg[v] == 0:
                    q.append(v)

        return "I disagree with the advisor" if processed == n else "No more comedians++"

    return solve()

# provided samples
assert run("2\nJEFF POTATO\nJEFF MARK\n") == "I disagree with the advisor"
assert run("3\nPETER PARKER\nPARKER WAYNE\nWAYNE PETER\n") == "No more comedians++"

# custom cases
assert run("1\nA B\n") == "I disagree with the advisor", "single edge"
assert run("2\nA B\nB C\n") == "I disagree with the advisor", "chain"
assert run("3\nA B\nB A\nC D\n") == "No more comedians++", "cycle + separate component"
assert run("0\n") == "I disagree with the advisor", "empty graph"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single edge | valid | minimal DAG |
| chain | valid | multi-step ordering |
| cycle + component | invalid | cycle detection correctness |
| empty graph | valid | boundary condition |

## Edge Cases

One edge case is when constraints form multiple disconnected components. The algorithm handles this naturally because all nodes with zero indegree across all components are enqueued initially. Each component is processed independently without interference.

Another case is a pure cycle with no incoming edges from outside. For input:

```
A B
B C
C A
```

all nodes start with indegree 1, so the queue remains empty. The algorithm immediately returns failure since no progress is possible, correctly identifying the cycle.

A final case is when the graph is large but sparse, such as a long chain of 100,000 nodes. Each node is processed exactly once, and each edge is relaxed exactly once, so the queue never grows beyond a small constant size relative to the structure, ensuring linear performance.
