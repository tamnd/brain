---
title: "CF 106420B - Beta Tester"
description: "The problem can be understood as exploring connectivity in a directed system of rooms. Each room represents a node in a graph, and each one-way vent represents a directed edge from one node to another."
date: "2026-06-20T03:46:27+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 106420
codeforces_index: "B"
codeforces_contest_name: "UTPC Contest 3-11-26 (Beginner)"
rating: 0
weight: 106420
solve_time_s: 61
verified: true
draft: false
---

[CF 106420B - Beta Tester](https://codeforces.com/problemset/problem/106420/B)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 1s  
**Verified:** yes  

## Solution
## Problem Understanding

The problem can be understood as exploring connectivity in a directed system of rooms. Each room represents a node in a graph, and each one-way vent represents a directed edge from one node to another. Starting from room 1, we are asked to determine how many distinct rooms can eventually be visited by repeatedly following these directed connections.

The input therefore describes a directed graph: rooms are vertices and vents are edges. The output is a single number, the size of the reachable set of vertices starting from vertex 1.

From a constraints perspective, this is a classic linear or near-linear graph traversal setting. Even without explicit bounds, Codeforces graph problems of this form typically allow up to 10^5 or 2 × 10^5 vertices and edges. That immediately rules out anything quadratic such as checking reachability between all pairs of nodes. A solution that tries to recompute reachability from scratch for every node would explode to O(n(n + m)), which is not feasible under typical limits.

A subtle edge case comes from cycles and disconnected components. A naive recursive traversal without tracking visited nodes can loop forever. For example, if room 1 leads to room 2 and room 2 leads back to room 1, the traversal would alternate indefinitely unless we explicitly mark visited nodes.

Another corner case is when room 1 has no outgoing edges. In that case the correct answer is 1, because we can only stay in the starting room.

## Approaches

A brute-force idea is to repeatedly expand from the current set of reachable rooms. We could start from room 1, then add all directly reachable rooms, then from those add their neighbors, and so on, recomputing the frontier until no new room appears. If implemented poorly, this becomes repeatedly scanning all edges to check whether their start node is already in the reachable set. In the worst case, each expansion pass processes O(m) edges, and there can be O(n) such passes, leading to O(nm) behavior.

The structure of the problem suggests a cleaner view: once a room is reachable, it should only be processed once, and once we explore its outgoing vents, we never need to revisit them. This is exactly the setting for a graph traversal that marks nodes as visited when first discovered. Depth-first search or breadth-first search both naturally enforce this “visit once” property and ensure each edge is traversed at most once.

This reduces the repeated scanning of edges into a single pass over adjacency lists, yielding linear complexity in the size of the graph.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Expansion | O(nm) | O(n) | Too slow |
| DFS/BFS Traversal | O(n + m) | O(n + m) | Accepted |

## Algorithm Walkthrough

We model the rooms as adjacency lists, where each room stores all rooms directly reachable from it.

1. Build an adjacency list from the input. Each directed vent from u to v is stored in u’s list. This allows efficient enumeration of outgoing connections without scanning unrelated edges.
2. Create a visited array of size n + 1 initialized to false. This prevents revisiting rooms and is essential to avoid infinite loops in cyclic graphs.
3. Start a traversal from room 1. Mark room 1 as visited immediately before exploring neighbors. This ensures we never enqueue or recurse into it again.
4. Use a stack or queue to manage exploration. Pop one room, and iterate over all its outgoing neighbors. Any neighbor not yet visited is marked visited and added to the structure for later processing.
5. Continue until there are no more rooms to process. At this point, all reachable nodes have been discovered exactly once.
6. Count how many entries in the visited array are true. This count is the number of distinct reachable rooms.

The choice between stack and queue does not affect correctness. DFS explores deeper paths first, while BFS explores level by level, but both guarantee complete reachability coverage because they systematically expand along all outgoing edges of every discovered node.

### Why it works

The key invariant is that every room marked as visited is reachable from room 1, and every reachable room will eventually be marked visited. We maintain this by only marking a node visited when we first discover it through a valid directed edge from an already reachable node. Since we never revisit nodes, each node is processed at most once, and all outgoing edges from reachable nodes are eventually explored. This guarantees that no reachable node is missed and no unreachable node is incorrectly included.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, m = map(int, input().split())
    adj = [[] for _ in range(n + 1)]
    
    for _ in range(m):
        u, v = map(int, input().split())
        adj[u].append(v)
    
    visited = [False] * (n + 1)
    stack = [1]
    visited[1] = True
    count = 0
    
    while stack:
        u = stack.pop()
        count += 1
        
        for v in adj[u]:
            if not visited[v]:
                visited[v] = True
                stack.append(v)
    
    print(count)

if __name__ == "__main__":
    solve()
```

The adjacency list construction is direct translation of the input into a graph representation. The visited array is critical to prevent revisiting nodes, and it is updated at the moment a node is discovered rather than when it is popped, which avoids duplicate entries in the stack.

The stack-based DFS ensures we traverse each connected reachable region completely. The counter increments exactly once per node when it is processed, matching the invariant that each node is popped once.

## Worked Examples

### Example 1

Consider a small graph where 1 leads to 2 and 3, and 2 leads to 4.

Initial state:

| Step | Stack | Visited | Count | Action |
| --- | --- | --- | --- | --- |
| 1 | [1] | {1} | 0 | Start from node 1 |
| 2 | [] | {1} | 1 | Pop 1 |
| 3 | [2, 3] | {1,2,3} | 1 | Expand neighbors of 1 |
| 4 | [2] | {1,2,3} | 2 | Pop 3 |
| 5 | [] | {1,2,3} | 3 | Pop 2 |
| 6 | [4] | {1,2,3,4} | 3 | Expand neighbors of 2 |
| 7 | [] | {1,2,3,4} | 4 | Pop 4 |

Final answer is 4, meaning all nodes are reachable from 1.

This trace shows how the stack explores all branches without duplication, and how visited prevents reprocessing nodes.

### Example 2

A disconnected graph where 1 only connects to 2, and 3 is isolated.

| Step | Stack | Visited | Count | Action |
| --- | --- | --- | --- | --- |
| 1 | [1] | {1} | 0 | Start |
| 2 | [] | {1} | 1 | Pop 1 |
| 3 | [2] | {1,2} | 1 | Visit neighbor 2 |
| 4 | [] | {1,2} | 2 | Pop 2 |

Node 3 never appears in traversal, so it is not counted.

This demonstrates that the algorithm correctly restricts itself to the reachable component only.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n + m) | Each node is visited once and each edge is scanned once during adjacency traversal |
| Space | O(n + m) | Adjacency list stores all edges and visited array stores node states |

The linear complexity matches typical constraints for graph reachability problems on Codeforces, where n and m can be large but still require efficient traversal.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from __main__ import solve
    return sys.stdout.getvalue() if False else capture(inp)

def capture(inp: str) -> str:
    import sys, io
    backup_in = sys.stdin
    backup_out = sys.stdout
    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()
    solve()
    out = sys.stdout.getvalue()
    sys.stdin = backup_in
    sys.stdout = backup_out
    return out.strip()

# sample-like tests
assert capture("4 3\n1 2\n2 3\n1 4\n") == "4"
assert capture("3 1\n1 2\n") == "2"

# minimum case
assert capture("1 0\n") == "1"

# cycle case
assert capture("3 3\n1 2\n2 3\n3 1\n") == "3"

# disconnected graph
assert capture("5 2\n1 2\n2 3\n") == "3"

# star graph
assert capture("6 5\n1 2\n1 3\n1 4\n1 5\n1 6\n") == "6"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 node, no edges | 1 | minimal graph handling |
| cycle | full count | cycle safety with visited |
| disconnected | partial reachability | correctness of restriction to component |
| star | n | high-degree node traversal |

## Edge Cases

A self-loop case like `1 -> 1` is handled cleanly because node 1 is marked visited before exploration begins. When processing its adjacency list, the neighbor is already visited, so it is ignored and the traversal terminates after counting only node 1.

A pure cycle such as `1 -> 2 -> 3 -> 1` demonstrates why the visited array is essential. Without it, the DFS would keep revisiting nodes indefinitely. With it, each node is inserted into the stack once, popped once, and skipped thereafter if encountered again.

A graph where node 1 has no outgoing edges is handled immediately: the stack starts with `[1]`, we pop it, increment the count once, and find no neighbors, resulting in an output of 1.
