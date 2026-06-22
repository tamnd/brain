---
title: "CF 105394A - Alien Attack 2"
description: "We are given a social network of people where friendships form an undirected graph. The aliens cannot abduct individuals independently."
date: "2026-06-23T04:57:20+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105394
codeforces_index: "A"
codeforces_contest_name: "2024-2025 ICPC German Collegiate Programming Contest (GCPC 2024)"
rating: 0
weight: 105394
solve_time_s: 44
verified: true
draft: false
---

[CF 105394A - Alien Attack 2](https://codeforces.com/problemset/problem/105394/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 44s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a social network of people where friendships form an undirected graph. The aliens cannot abduct individuals independently. If they choose any person from a connected group of friends, they must take the entire connected group at the same time so that no missing person is noticed.

The task is to determine the minimum capacity required on a spaceship so that all required abductions can be completed. Since each connected component must be taken as a whole, a single trip can carry one entire component, and the ship must be able to fit the largest such component.

The input describes a graph with up to 200,000 people and 200,000 friendships. This scale rules out any quadratic approach such as repeatedly checking reachability from every node using fresh traversals. Any correct solution must process the graph in linear time, typically O(n + m), since even O(n log n) is acceptable but unnecessary.

A subtle failure case appears when friendships are sparse or completely absent. If there are no edges, every node is isolated and each forms a component of size 1, so the answer is 1. A naive mistake is to assume at least one edge exists and start component tracking only from adjacency lists, which would miss isolated nodes entirely.

Another edge case is when the graph is fully connected. In that case, the answer is n, since a single component contains everyone. Any solution that incorrectly counts edges or assumes multiple components exist would underestimate the required capacity.

## Approaches

A direct way to solve the problem is to treat each person as a starting point and run a graph traversal, such as depth-first search or breadth-first search, whenever we encounter an unvisited node. Each traversal discovers one connected component, and we count how many nodes are in that component. We track the maximum size over all components.

This brute-force idea is correct because it explicitly simulates the rule: friendships force grouping, and connectivity defines group membership. The cost comes from repeated traversals over a large graph. In the worst case, if we are careless and do not mark visited nodes properly, we may re-explore large portions of the graph multiple times, leading to O(nm) behavior. Even with correct visited tracking, we still need to traverse every node and edge once, which becomes O(n + m), which is fine.

The key insight is that the problem does not require us to simulate multiple trips or any dynamic process. It only asks for the size of the largest connected component in an undirected graph. Once we recognize that each abduction corresponds exactly to one connected component, the entire problem reduces to computing component sizes and taking a maximum.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Repeated naive exploration | O(nm) | O(n + m) | Too slow |
| DFS/BFS connected components | O(n + m) | O(n + m) | Accepted |

## Algorithm Walkthrough

1. Build an adjacency list representation of the graph from the friendship pairs. This allows efficient traversal of neighbors of any person without scanning all edges repeatedly.
2. Maintain a visited array initialized to false for all people. This ensures each node is processed exactly once across all traversals.
3. Iterate over all people from 1 to n. For each person, if they have not been visited, start a traversal from that node.
4. During traversal, use a stack or queue to explore all reachable nodes in the same connected component. Mark each visited node immediately when it is discovered to avoid revisiting.
5. Count how many nodes are visited during this traversal. This count represents the size of the current connected component.
6. Update the answer with the maximum component size encountered so far.
7. After processing all nodes, output the maximum value.

The reason this procedure works is that each traversal exactly matches the definition of a connected component in an undirected graph. Once a node is marked visited, it cannot belong to another component, so every node contributes to exactly one component size. The maximum over these sizes is therefore the smallest ship capacity that can handle any required abduction group.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, m = map(int, input().split())
    adj = [[] for _ in range(n + 1)]

    for _ in range(m):
        a, b = map(int, input().split())
        adj[a].append(b)
        adj[b].append(a)

    visited = [False] * (n + 1)
    best = 1

    for i in range(1, n + 1):
        if visited[i]:
            continue

        stack = [i]
        visited[i] = True
        size = 0

        while stack:
            v = stack.pop()
            size += 1

            for to in adj[v]:
                if not visited[to]:
                    visited[to] = True
                    stack.append(to)

        if size > best:
            best = size

    print(best)

if __name__ == "__main__":
    solve()
```

The adjacency list construction ensures we can traverse friendships efficiently. The visited array guarantees each node is processed once, preventing repeated counting. The DFS stack avoids recursion depth issues in Python for large graphs. The variable `best` stores the largest connected component encountered.

A subtle implementation detail is marking nodes as visited at push time rather than pop time. This prevents multiple insertions of the same node into the stack, which would inflate runtime in dense graphs.

## Worked Examples

### Sample 1

Input graph has five nodes with edges forming components {1,2,3} and {4,5}.

| Start node | Stack | Visited set | Component size |
| --- | --- | --- | --- |
| 1 | [1] → [] | {1,2,3} | 3 |
| 2 | skipped | already visited | - |
| 3 | skipped | already visited | - |
| 4 | [4] → [] | {4,5} | 2 |
| 5 | skipped | already visited | - |

The largest component size is 3, which becomes the required capacity.

### Sample 2

With no friendships, every node is isolated.

| Node | Action | Component size |
| --- | --- | --- |
| 1 | new DFS | 1 |
| 2 | new DFS | 1 |
| 3 | new DFS | 1 |

The maximum is 1, meaning the ship only needs space for a single person per trip.

This confirms that isolated nodes are handled correctly and that the algorithm does not assume the presence of edges.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n + m) | Each node is visited once and each edge is traversed at most twice in an undirected graph |
| Space | O(n + m) | Adjacency list plus visited array and traversal stack |

The constraints allow up to 200,000 nodes and edges, and linear processing comfortably fits within time limits in Python when implemented iteratively.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from contextlib import redirect_stdout
    import io as sysio

    out = sysio.StringIO()
    with redirect_stdout(out):
        solve()
    return out.getvalue().strip()

# provided samples
assert run("5 3\n1 2\n2 3\n4 5\n") == "3", "sample 1"
assert run("3 0\n") == "1", "sample 2"

# custom cases
assert run("1 0\n") == "1", "single node"
assert run("4 3\n1 2\n2 3\n3 4\n") == "4", "fully connected chain"
assert run("6 3\n1 2\n3 4\n5 6\n") == "2", "multiple equal components"
assert run("5 4\n1 2\n2 3\n3 1\n4 5\n") == "3", "cycle plus pair"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 node, no edges | 1 | minimal graph handling |
| chain 1-2-3-4 | 4 | single large component |
| disjoint pairs | 2 | multiple components |
| cycle + pair | 3 | cycle correctness |

## Edge Cases

A graph with no edges is the most fragile case for incorrect implementations. For input `3 0`, the adjacency list is empty for all nodes. The algorithm still iterates over every node, starting a DFS of size 1 for each. The maximum remains 1, which is correct.

A fully connected graph exposes errors where traversal is incorrectly limited to immediate neighbors or where visited marking is delayed. For input `4 6` with all possible edges, starting at node 1 leads to a traversal that eventually reaches all nodes, producing size 4. Any premature marking or incorrect neighbor iteration would underestimate this size.

A chain graph tests propagation of reachability. In `1-2-3-4`, starting from 1 must eventually reach 4 through intermediate nodes. The stack-based DFS ensures transitive closure is fully explored, so the component size becomes 4 rather than 1 or 2, which would happen if only direct neighbors were counted.
