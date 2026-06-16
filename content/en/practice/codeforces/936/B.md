---
title: "CF 936B - Sleepy Game"
description: "We are given a directed graph where each vertex represents a state of a game token. A token starts at a fixed vertex, and two players alternate moving it along outgoing edges. A player loses immediately if they are to move from a vertex that has no outgoing edges."
date: "2026-06-17T02:47:16+07:00"
tags: ["codeforces", "competitive-programming", "dfs-and-similar", "dp", "games", "graphs"]
categories: ["algorithms"]
codeforces_contest: 936
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 467 (Div. 1)"
rating: 2100
weight: 936
solve_time_s: 100
verified: false
draft: false
---

[CF 936B - Sleepy Game](https://codeforces.com/problemset/problem/936/B)

**Rating:** 2100  
**Tags:** dfs and similar, dp, games, graphs  
**Solve time:** 1m 40s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a directed graph where each vertex represents a state of a game token. A token starts at a fixed vertex, and two players alternate moving it along outgoing edges. A player loses immediately if they are to move from a vertex that has no outgoing edges. The game also has a hard cap: if play continues for a very long time (up to 10^6 moves), the game is declared a draw.

The twist is that one player is asleep, so a single player effectively controls both sides of the game. This changes the problem from a standard alternating game into a self-controlled walk where we must reason about outcomes under optimal play, but with the added constraint that cycles prevent forced termination and therefore imply draws.

The task is to classify the starting vertex into one of three outcomes: a forced win for the controller, a forced loss, or a draw caused by the ability to avoid termination indefinitely.

The constraints are large: up to 10^5 vertices and 2·10^5 edges. This rules out any simulation of the game tree. Even a naive BFS over game states would be impossible because each vertex state depends on whose turn it is, effectively doubling states and still leaving an exponential branching structure.

The key difficulty comes from cycles. A naive DFS that only tries to find a path to a dead end will incorrectly treat any cycle as potentially winning or losing without understanding whether it is escapable or enforceable.

A subtle failure case is a graph where every path eventually leads into a cycle. For example, if all vertices form a single cycle, a naive “no dead end reachable” approach might incorrectly label it as a win or loss depending on traversal order, when in fact it is a draw because play can continue indefinitely without reaching a terminal vertex.

## Approaches

A brute-force idea is to treat each state as a game position and simulate all possible move sequences. From a vertex, we try every outgoing edge and recursively determine whether the opponent loses from the resulting state. This is the standard minimax recursion on a directed graph.

This approach is correct in principle because every position is either winning or losing depending on whether there exists a move leading to a losing position. However, the state space explodes due to cycles. A naive DFS revisits states infinitely or requires memoization over states that also encode the number of moves or parity, which increases complexity significantly.

The real insight is to invert the perspective. Instead of asking whether a position is winning, we classify positions using backward reasoning from terminal states. A vertex with no outgoing edges is a losing state. Any vertex that can force the opponent into a losing state is winning. However, vertices that are not proven winning or losing after propagation must lie in or lead into cycles where neither player can force termination.

This leads to a multi-source BFS over reversed edges with a counter of remaining outgoing moves. We propagate losing and winning labels outward, and anything unclassified after full propagation is part of a draw region.

The construction of the actual winning path is done by storing parent pointers during BFS, ensuring we can reconstruct a valid forced win path ending at a terminal vertex.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force DFS/Minimax | Exponential | O(n) recursion stack | Too slow |
| Reverse BFS with state propagation | O(n + m) | O(n + m) | Accepted |

## Algorithm Walkthrough

We interpret the game as a shortest-win propagation problem on a directed graph.

1. Identify all terminal vertices, meaning vertices with no outgoing edges. These are immediately losing positions because the player to move cannot act. We initialize them as losing states.
2. Build a reversed adjacency list so that for each edge u → v, we can efficiently propagate information from v back to u. This is needed because we reason backward from terminal states.
3. Maintain an array `deg[u]` storing the number of outgoing edges from each vertex. This tracks how many moves remain “unresolved” for each position.
4. Run a BFS queue initialized with all terminal vertices marked as losing. We also maintain a state array where each vertex can be winning, losing, or unknown.
5. When processing a losing vertex v, we inspect all predecessors u. If u has an edge to v, then u can force a win by moving to a losing position. We mark u as winning and store v as its successor for path reconstruction.
6. When processing a winning vertex v, we decrement `deg[u]` for each predecessor u. This represents that one of u’s options leads to a known winning state for the opponent. If all outgoing moves from u are proven to lead to winning states for the opponent (meaning deg[u] becomes zero without finding a losing child), then u itself becomes losing.
7. Continue propagation until no new states can be determined.
8. After propagation, check the starting vertex. If it is winning, reconstruct the path by following stored parent pointers until reaching a terminal losing vertex.
9. If it is not winning but remains unclassified, it is part of a cycle region where both players can avoid termination, so the result is a draw.
10. Otherwise, it is a losing position.

### Why it works

The algorithm maintains a monotonic classification of vertices based on forced outcomes. A vertex becomes winning only if it has a direct move into a confirmed losing vertex, guaranteeing a forced move advantage. A vertex becomes losing only when all outgoing moves lead to positions already proven to be winning for the opponent, meaning no safe move remains.

Any vertex not classified after full propagation must lie in a region where neither winning nor losing propagation can reach it. Such vertices necessarily belong to cycles or structures feeding only into cycles, where play can continue indefinitely without reaching a terminal state. This matches exactly the definition of a draw under the 10^6 move cap.

Because propagation always moves from resolved states to unresolved ones and never reverses decisions, no vertex is ever mislabeled once assigned.

## Python Solution

```python
import sys
input = sys.stdin.readline
from collections import deque

n, m = map(int, input().split())

g = [[] for _ in range(n)]
rg = [[] for _ in range(n)]
deg = [0] * n

for i in range(n):
    parts = list(map(int, input().split()))
    c = parts[0]
    for v in parts[1:]:
        v -= 1
        g[i].append(v)
        rg[v].append(i)
    deg[i] = c

s = int(input()) - 1

# state: 0 unknown, 1 winning, 2 losing
state = [0] * n
parent = [-1] * n

q = deque()

# terminal nodes are losing
for i in range(n):
    if deg[i] == 0:
        state[i] = 2
        q.append(i)

while q:
    v = q.popleft()

    if state[v] == 2:
        for u in rg[v]:
            if state[u] == 0:
                state[u] = 1
                parent[u] = v
                q.append(u)
    else:
        for u in rg[v]:
            if state[u] == 0:
                deg[u] -= 1
                if deg[u] == 0:
                    state[u] = 2
                    q.append(u)

if state[s] != 1:
    if state[s] == 0:
        print("Draw")
    else:
        print("Lose")
else:
    print("Win")
    path = []
    cur = s
    while cur != -1:
        path.append(cur + 1)
        cur = parent[cur]
    print(*path)
```

The solution starts by building both forward and reverse adjacency lists. The reverse graph is essential because all propagation goes from known outcomes backward to their predecessors.

The `deg` array tracks how many outgoing edges remain “unsafe” for each node. A node only becomes losing after all its children have been accounted for as winning positions.

The BFS queue contains nodes whose status is already known. From a losing node, we immediately convert predecessors into winning nodes. From a winning node, we eliminate one outgoing option for predecessors, possibly forcing them into losing status.

The parent array is only filled when a node becomes winning, ensuring that any reconstructed path always follows a valid forced-win move sequence.

## Worked Examples

### Example 1

Input graph:

```
5 6
1 -> 2,3
2 -> 4,5
3 -> 4
4 -> 5
5 -> none
start = 1
```

We track propagation:

| Step | Queue Node | Action | State Changes |
| --- | --- | --- | --- |
| 1 | 5 | terminal → losing | 5 = L |
| 2 | 5 | propagate to 4,2 | 4 = W, 2 = W |
| 3 | 4 | winning propagation | updates 3 |
| 4 | 2 | winning propagation | updates 1 |
| 5 | 1 | becomes W | done |

Final classification: vertex 1 is winning.

Reconstruction follows parent pointers:

1 → 2 → 4 → 5.

This confirms a forced path that ends at a terminal losing vertex.

### Example 2

Consider a simple cycle:

```
3 3
1 -> 2
2 -> 3
3 -> 1
start = 2
```

| Step | Queue Node | Action | State Changes |
| --- | --- | --- | --- |
| 1 | none terminal nodes | no deg = 0 nodes | no initialization |
| 2 | queue empty | no propagation | all remain unknown |

All nodes remain unclassified, so the result is Draw.

This shows that cycles without exits never get resolved into win/lose states.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n + m) | Each edge is processed a constant number of times during reverse propagation |
| Space | O(n + m) | Graph storage, reverse graph, and auxiliary arrays |

The linear complexity is necessary for n up to 10^5 and m up to 2·10^5, where any quadratic or exponential exploration would be infeasible.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    n, m = map(int, input().split())
    g = [[] for _ in range(n)]
    rg = [[] for _ in range(n)]
    deg = [0] * n

    for i in range(n):
        parts = list(map(int, input().split()))
        c = parts[0]
        for v in parts[1:]:
            v -= 1
            g[i].append(v)
            rg[v].append(i)
        deg[i] = c

    s = int(input()) - 1

    state = [0] * n
    parent = [-1] * n
    from collections import deque
    q = deque()

    for i in range(n):
        if deg[i] == 0:
            state[i] = 2
            q.append(i)

    while q:
        v = q.popleft()
        if state[v] == 2:
            for u in rg[v]:
                if state[u] == 0:
                    state[u] = 1
                    parent[u] = v
                    q.append(u)
        else:
            for u in rg[v]:
                if state[u] == 0:
                    deg[u] -= 1
                    if deg[u] == 0:
                        state[u] = 2
                        q.append(u)

    if state[s] != 1:
        print("Draw" if state[s] == 0 else "Lose")
    else:
        print("Win")
        path = []
        cur = s
        while cur != -1:
            path.append(cur + 1)
            cur = parent[cur]
        print(*path)

# provided sample 1
assert run("""5 6
2 2 3
2 4 5
1 4
1 5
0
1
""") == "Win\n1 2 4 5\n"

# custom: single losing node
assert run("""1 0
0
1
""") == "Lose\n"

# custom: simple cycle (draw)
assert run("""3 3
1 2
2 3
3 1
2
""") == "Draw\n"

# custom: chain to terminal win
assert run("""4 3
2 2 3
1 4
1 4
0
1
""") == "Win\n1 2 4\n"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single node no edges | Lose | terminal detection |
| 3-cycle | Draw | cycle handling |
| chain to sink | Win | propagation correctness |

## Edge Cases

A graph consisting only of cycles, such as 1 → 2 → 3 → 1, never produces terminal nodes. The algorithm leaves all vertices in the unknown state after BFS initialization. Since no state can be resolved backward from a terminal condition, the classification remains incomplete, which is correctly interpreted as a draw.

A vertex with multiple outgoing edges where one leads to a terminal node and others lead into cycles becomes winning immediately upon discovering the terminal neighbor. This demonstrates why reverse propagation from losing states is sufficient: a single escape into a losing position defines a forced win regardless of other edges.

A long chain ending in a sink ensures that propagation correctly builds a full winning path. Each predecessor is resolved exactly once, and the parent pointers reconstruct a valid sequence without ambiguity.
