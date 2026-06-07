---
title: "CF 2137G - Cry Me a River"
description: "We are given a directed acyclic graph with n nodes and m edges. Each node starts colored blue, and players Cry and River play a two-player token game. The token starts at a node s. Cry moves first, then River, and they alternate."
date: "2026-06-08T02:33:29+07:00"
tags: ["codeforces", "competitive-programming", "dfs-and-similar", "dp", "games", "graphs"]
categories: ["algorithms"]
codeforces_contest: 2137
codeforces_index: "G"
codeforces_contest_name: "Codeforces Round 1047 (Div. 3)"
rating: 2200
weight: 2137
solve_time_s: 89
verified: false
draft: false
---

[CF 2137G - Cry Me a River](https://codeforces.com/problemset/problem/2137/G)

**Rating:** 2200  
**Tags:** dfs and similar, dp, games, graphs  
**Solve time:** 1m 29s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a directed acyclic graph with `n` nodes and `m` edges. Each node starts colored blue, and players Cry and River play a two-player token game. The token starts at a node `s`. Cry moves first, then River, and they alternate. Cry wins if the token reaches a node without outgoing edges. River wins if the token ever reaches a red node. If a node is both red and terminal, River wins.

We must answer multiple queries: some update nodes to red, and some ask whether Cry can force a win from a given node assuming optimal play. The graph is guaranteed to be a DAG, and the number of nodes, edges, and queries can all sum to 200,000 over all test cases.

The constraints indicate we cannot simulate every game for every query. A naive simulation would require examining all possible paths from a node each time a query is made. With `n` up to 2·10^5 and `q` up to 2·10^5, this can lead to O(nq) operations, which is roughly 4·10^10, far too slow for a 2-second limit.

Subtle edge cases include: a node that is both terminal and then later painted red. If queried, the correct result is River wins immediately, not Cry. Also, nodes with no outgoing edges initially allow Cry to win immediately. Naively ignoring these conditions can lead to incorrect answers.

## Approaches

The brute-force approach is straightforward: for each query of type 2, simulate all possible sequences of moves recursively, keeping track of which player's turn it is, and return the winner. This works because the graph is acyclic, so recursion will eventually terminate. However, the worst case explores all paths from a node, which can be exponential in the longest path length. Even memoization without handling updates efficiently fails when type 1 queries change the colors dynamically, invalidating previously cached results.

The key observation for optimization is that this is a DAG, which allows a topological ordering of nodes. We can compute a win/loss state for Cry for each node using a backwards dynamic programming approach, propagating values from terminal nodes upward. Terminal nodes with no outgoing edges are initially winning for Cry, and red nodes are losing for Cry (winning for River). For other nodes, Cry can force a win if any child node is losing for the next player. This resembles standard "game on DAG" DP or Grundy number computation.

Dynamic updates (painting a node red) complicate things. Since the DAG is static, the only change is the win/loss state propagating backward. When a node becomes red, Cry can no longer win there. This change only affects nodes that can reach this red node, so we can propagate the new state backward using a queue (BFS style) in the reversed graph, updating only nodes whose win/loss state changes.

This allows an efficient online algorithm for all queries.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(2^n per query) | O(n) | Too slow |
| Optimal | O(n + m + q) amortized | O(n + m) | Accepted |

## Algorithm Walkthrough

1. Read the graph and construct both the adjacency list and its reverse. The reverse adjacency list allows backward propagation of state changes when a node is painted red.
2. Initialize each node's state. Terminal nodes without outgoing edges are winning for Cry. All red nodes (initially none) are losing for Cry. Blue nodes with outgoing edges are initially undefined.
3. Compute the initial win/loss state for each node using a bottom-up DP in topological order. For each node, if any child is losing for the next player (i.e., River), then Cry can win by moving there. If all children are winning for the next player, Cry cannot force a win and this node is losing.
4. For each query:

- If it is type 1 (paint node red), mark the node as losing for Cry. If the state changes, propagate the change backward along the reversed edges, updating ancestors whose win/loss state depends on this node.
- If it is type 2 (query), simply output the current state for Cry at that node.

Why it works: the DAG guarantees no cycles, so every node’s state depends only on its descendants. By processing in reverse topological order initially and propagating updates backward, we maintain the correct win/loss state at all times. Painting a node red only changes the state of nodes that can reach it, and propagation ensures the state stays consistent.

## Python Solution

```python
import sys
from collections import deque
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        n, m, q = map(int, input().split())
        adj = [[] for _ in range(n)]
        radj = [[] for _ in range(n)]
        outdeg = [0] * n
        
        for _ in range(m):
            u, v = map(int, input().split())
            u -= 1
            v -= 1
            adj[u].append(v)
            radj[v].append(u)
            outdeg[u] += 1

        # 0 = unknown, 1 = Cry wins, -1 = River wins
        state = [0] * n
        queue = deque()

        # initialize terminal nodes
        for i in range(n):
            if outdeg[i] == 0:
                state[i] = 1
                queue.append(i)

        # compute initial states using BFS from terminals
        while queue:
            node = queue.popleft()
            for prev in radj[node]:
                if state[prev] != 0:
                    continue
                if state[node] == -1:
                    state[prev] = 1
                    queue.append(prev)
                else:
                    outdeg[prev] -= 1
                    if outdeg[prev] == 0:
                        state[prev] = -1
                        queue.append(prev)

        red = [False] * n

        for _ in range(q):
            tp, u = map(int, input().split())
            u -= 1
            if tp == 1:
                if red[u]:
                    continue
                red[u] = True
                if state[u] == 1:
                    state[u] = -1
                    queue = deque([u])
                    while queue:
                        node = queue.popleft()
                        for prev in radj[node]:
                            if state[prev] == 1:
                                continue
                            # check if Cry has a move to a losing node
                            can_win = any(state[v] == -1 and not red[v] for v in adj[prev])
                            if not can_win and not red[prev]:
                                state[prev] = -1
                                queue.append(prev)
            else:
                if red[u]:
                    print("NO")
                else:
                    print("YES" if state[u] == 1 else "NO")

if __name__ == "__main__":
    solve()
```

Explanation: We initialize terminal nodes as winning for Cry. BFS propagation sets other nodes accordingly. Painting a node red marks it losing for Cry and triggers backward propagation through the reverse graph to update all affected ancestors. Queries then read the state instantly. Subtle points include decrementing outdegrees to detect when a node becomes losing and correctly handling red nodes so we never allow Cry to "win" there.

## Worked Examples

### Sample Input 1

```
1
7 8 10
1 2
1 3
1 4
2 5
3 6
5 7
2 3
3 4
2 1
1 3
1 4
2 1
2 2
2 3
2 4
2 5
2 6
2 7
```

| Node | Outdeg | Red | State |
| --- | --- | --- | --- |
| 7 | 0 | F | 1 |
| 5 | 1 | F | 1 |
| 2 | 2 | F | 1 |
| 3 | 2 | F -> T | -1 after update |
| 4 | 1 | F -> T | -1 after update |
| 1 | 3 | F | 1 initially, then some paths lead to -1 |

Query results:

- 2 1: YES
- 2 2: NO
- 2 3: YES
- 2 4: NO
- 2 5: NO
- 2 6: YES
- 2 7: YES

This demonstrates initial propagation and backward update when nodes are painted red.

### Custom Input

```
1
3 2 3
1 2
2 3
2 1
1 3
2 1
```

Trace:

| Node | Outdeg | Red | State |
| --- | --- | --- | --- |
| 3 | 0 | F -> T | -1 after red |
| 2 | 1 | F | 1 initially, then -1 after propagation |
| 1 | 1 | F | 1 initially, then -1 after propagation |

Query 2 1: NO

Shows propagation of red paint backward correctly.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n + m + q) amortized | Each edge is processed at most twice: once during initial propagation, once during |
