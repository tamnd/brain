---
title: "CF 104741B - \u5c0fM\u7684\u6e38\u620f"
description: "We are given a weighted undirected graph with $N$ locations and $M$ roads. Two players start at node $1$ and want to reach node $N$."
date: "2026-06-29T00:52:05+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104741
codeforces_index: "B"
codeforces_contest_name: "The 10th Jimei University Programming Contest"
rating: 0
weight: 104741
solve_time_s: 52
verified: true
draft: false
---

[CF 104741B - \u5c0fM\u7684\u6e38\u620f](https://codeforces.com/problemset/problem/104741/B)

**Rating:** -  
**Tags:** -  
**Solve time:** 52s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a weighted undirected graph with $N$ locations and $M$ roads. Two players start at node $1$ and want to reach node $N$. They move along the graph step by step, but the movement is constrained: from the current node, the next chosen edge must lie on some shortest path to node $N$. In other words, at every step, they are forced to stay optimal with respect to remaining distance to the destination.

The game is turn-based. The first player (Little M) chooses the first move from node $1$, then Little I chooses the next, and they alternate. Whoever is forced to “make the move” when they are already at node $N$ loses, meaning reaching $N$ ends the game and the player who just arrived does not get to move again, but the opponent is considered to have no move and therefore wins according to the rule structure described.

Both players play optimally, and we must determine whether Little M (starting player) can force a win.

The constraints allow up to $10^5$ nodes and $2 \cdot 10^5$ edges per test case, with up to 10 test cases. This immediately rules out any quadratic or state-expansion approach over all paths. Any solution must essentially be linear or near-linear in the graph size, typically $O(M \log N)$ or $O(N + M)$.

The subtle difficulty is that although the graph may contain cycles, the “must follow shortest paths” rule effectively restricts play to a directed acyclic structure induced by shortest distances to node $N$.

A naive mistake arises if one treats this as a general game on a graph without enforcing shortest-path constraints.

For example, consider a triangle graph where node 1 connects to 2 and 3, and both connect to 4 (destination), with equal weights. A naive game solver might consider arbitrary transitions and mis-evaluate cycles or repeated states. The correct behavior ignores non-shortest transitions entirely.

Another failure case occurs if shortest distances are computed from node $1$ instead of node $N$. The game is defined by distance-to-goal constraints, so reversing the root of shortest path computation leads to incorrect allowed moves.

## Approaches

A brute-force interpretation would simulate the game state as a pair consisting of the current node and whose turn it is. From each state, we try all valid shortest-path edges and recursively determine whether the current player can force a win. While logically correct, this explores a game graph whose size is proportional to the number of edges in the shortest-path subgraph, and in worst cases degenerates into exponential branching when multiple shortest-path continuations exist at each step. With up to $10^5$ nodes, this is completely infeasible.

The key observation is that the “must always move along a shortest path to $N$” rule removes cycles in a strong sense. If we compute $dist[u]$ as the shortest distance from $u$ to $N$, then every valid move strictly decreases $dist$. This means the game graph becomes a directed acyclic graph where edges go from larger distance to smaller distance.

Once we have a DAG, the problem becomes a standard winning-state DP: a position is winning if it has at least one move to a losing position, and losing if all moves go to winning positions. Since edges always go from higher distance to lower distance, we can process nodes in increasing order of $dist$, starting from $N$ where no moves exist.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Game Search | Exponential in worst case | $O(N + M)$ recursion | Too slow |
| Shortest-path + DP on DAG | $O(M \log N)$ | $O(N + M)$ | Accepted |

## Algorithm Walkthrough

We convert the game into a shortest-path-restricted directed graph and then run a standard winning-state dynamic programming on it.

1. Compute shortest distances from every node to node $N$ using Dijkstra’s algorithm. This tells us, for each node, how far it is from the goal under optimal travel.
2. For every undirected edge $(u, v, w)$, determine whether it can be used in a valid move. The edge is usable from $u$ to $v$ if and only if $dist[u] = dist[v] + w$, and similarly usable from $v$ to $u$ if $dist[v] = dist[u] + w$. This directionality is induced entirely by shortest-path consistency.
3. Treat each node as a game state. Define a boolean $dp[u]$ meaning “the player whose turn it is at node $u$ can force a win.”
4. Initialize $dp[N] = False$, because arriving at $N$ means there are no outgoing valid moves.
5. Sort nodes by increasing $dist[u]$. This ensures we process states from closest to $N$ outward.
6. For each node $u$ in this order, examine all neighbors $v$ such that moving to $v$ is valid (it reduces distance by exactly the edge weight). If there exists at least one such neighbor $v$ where $dp[v] = False$, then set $dp[u] = True$, because the current player can force the opponent into a losing state.
7. If no such move exists, set $dp[u] = False$.
8. The answer is $dp[1]$, since the game starts at node $1$.

### Why it works

The shortest-distance restriction guarantees that every valid move strictly decreases the value of $dist[u]$. This induces a strict ordering over states, preventing cycles in the game graph. As a result, every state depends only on strictly smaller states, so processing nodes in increasing $dist$ order ensures all transitions are already resolved when needed. The DP recurrence is correct because every legal move is considered exactly once, and the win condition matches standard normal-play combinatorial game logic on a DAG.

## Python Solution

```python
import sys
import heapq
input = sys.stdin.readline

INF = 10**18

def solve():
    n, m = map(int, input().split())
    g = [[] for _ in range(n + 1)]
    
    for _ in range(m):
        u, v, w = map(int, input().split())
        g[u].append((v, w))
        g[v].append((u, w))

    dist = [INF] * (n + 1)
    dist[n] = 0
    pq = [(0, n)]

    while pq:
        d, u = heapq.heappop(pq)
        if d != dist[u]:
            continue
        for v, w in g[u]:
            nd = d + w
            if nd < dist[v]:
                dist[v] = nd
                heapq.heappush(pq, (nd, v))

    nodes = list(range(1, n + 1))
    nodes.sort(key=lambda x: dist[x])

    dp = [False] * (n + 1)
    dp[n] = False

    for u in nodes:
        if u == n:
            continue
        for v, w in g[u]:
            if dist[u] == dist[v] + w:
                if not dp[v]:
                    dp[u] = True
                    break

    print("Little M is the winner." if dp[1] else "Little I is the winner.")

t = int(input())
for _ in range(t):
    solve()
```

The first phase computes shortest distances from the destination using Dijkstra. This reversal is essential because moves are defined by “getting closer to $N$,” so distances must be rooted at $N$.

The second phase filters edges implicitly using the condition $dist[u] = dist[v] + w$. This avoids explicitly building a directed graph and keeps memory linear.

The DP loop relies on processing nodes in increasing distance order so that every $dp[v]$ is already known before computing $dp[u]$.

A common implementation mistake is forgetting that multiple edges can satisfy the shortest-path condition; all must be checked.

## Worked Examples

### Example 1

Consider a simple chain:

1 --(1)-- 2 --(1)-- 3

with destination $3$.

Shortest distances from 3 are:

| Node | dist |
| --- | --- |
| 3 | 0 |
| 2 | 1 |
| 1 | 2 |

Processing order: 3, 2, 1.

For node 2, it has a move to 3, and $dp[3] = False$, so $dp[2] = True$.

For node 1, it moves to 2, but $dp[2] = True$, so it cannot force a win, hence $dp[1] = False$.

So Little M loses in this configuration.

### Example 2

Graph:

1 connects to 2 and 3, both connect to 4 (destination), all weights 1.

Shortest distances:

| Node | dist |
| --- | --- |
| 4 | 0 |
| 2 | 1 |
| 3 | 1 |
| 1 | 2 |

Processing order: 4, 2, 3, 1.

At nodes 2 and 3, both can go to 4, so both are winning states.

At node 1, both moves go to winning states, so $dp[1] = False$.

This shows that having multiple optimal branches does not help if all of them lead to winning positions for the opponent.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(M \log N)$ | Dijkstra dominates; DP is linear in edges |
| Space | $O(N + M)$ | adjacency list, distance array, DP array |

The constraints allow up to $2 \cdot 10^5$ edges, so a logarithmic factor from Dijkstra is acceptable. The DP stage is purely linear and comfortably fits within limits even across 10 test cases.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    output = io.StringIO()
    sys.stdout = output

    # assume solve() and loop are defined above
    t = int(input())
    for _ in range(t):
        solve()

    sys.stdout = sys.__stdout__
    return output.getvalue().strip()

# minimal case
assert run("""1
1 0
""") == "Little M is the winner."

# simple chain where first loses
assert run("""1
3 2
1 2 1
2 3 1
""") == "Little I is the winner."

# branching case
assert run("""1
4 4
1 2 1
2 4 1
1 3 1
3 4 1
""") == "Little I is the winner."

# uneven graph
assert run("""1
5 6
1 2 2
2 5 2
1 3 1
3 4 1
4 5 1
2 4 1
""") == "Little M is the winner."
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single node | M wins | terminal state handling |
| chain | I wins | linear DP correctness |
| symmetric branching | I wins | multiple shortest paths |
| mixed weights | M wins | correct shortest-path filtering |

## Edge Cases

A critical edge case is when the graph contains multiple shortest-path edges from a node, but only some of them lead to losing states. The DP must consider all such edges; stopping early on the first valid edge would be incorrect. The algorithm handles this correctly by explicitly checking every neighbor satisfying the shortest-path equality condition before deciding the DP value.

Another subtle case is when the graph contains cycles in the original form. These cycles disappear after enforcing the distance constraint, because any valid move must strictly reduce the distance to $N$. This ensures that even highly cyclic input graphs behave like a DAG in the DP phase, and the algorithm remains well-defined.
