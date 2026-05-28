---
title: "CF 48E - Ivan the Fool VS Gorynych the Dragon"
description: "The game state is completely described by two numbers: how many heads and how many tails the dragon currently has. From a state (h, t) Ivan may choose one of two move types."
date: "2026-05-28T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "dp", "games", "graphs"]
categories: ["algorithms"]
codeforces_contest: 48
codeforces_index: "E"
codeforces_contest_name: "School Personal Contest #3 (Winter Computer School 2010/11) - Codeforces Beta Round 45 (ACM-ICPC Rules)"
rating: 2100
weight: 48
solve_time_s: 141
verified: true
draft: false
---

[CF 48E - Ivan the Fool VS Gorynych the Dragon](https://codeforces.com/problemset/problem/48/E)

**Rating:** 2100  
**Tags:** dp, games, graphs  
**Solve time:** 2m 21s  
**Verified:** yes  

## Solution
## Problem Understanding

The game state is completely described by two numbers: how many heads and how many tails the dragon currently has. From a state `(h, t)` Ivan may choose one of two move types.

If he cuts `i` heads, where `1 ≤ i ≤ n` and `i ≤ h`, then the dragon grows back `headGrow[i]` heads and `tailGrow[i]` tails. The new state becomes:

`(h - i + headGrow[i], t + tailGrow[i])`

If he cuts `i` tails, where `1 ≤ i ≤ m` and `i ≤ t`, then the new state becomes:

`(h + headGrowTail[i], t - i + tailGrowTail[i])`

The fight immediately ends in one of three ways.

Ivan wins if the state becomes `(0, 0)` after regeneration.

The dragon wins if after a move the total number of parts exceeds `R`.

The game is a draw if Ivan can avoid losing forever but can never force a win.

The tricky part is that Ivan always plays optimally under a three-level objective. First he prefers winning in the minimum number of moves. If winning is impossible, he prefers surviving forever. If even that is impossible, he wants to delay defeat as long as possible.

The bounds are small enough to treat every valid `(h, t)` pair as a graph node. Since `h + t ≤ R ≤ 200`, the total number of reachable legal states is at most about `201 × 201`, but only states with `h + t ≤ R` matter. That gives roughly `O(R²)` states, around forty thousand in the worst case. Each state has at most `n + m ≤ 400` outgoing transitions. A graph algorithm over all states is completely feasible.

A naive recursive simulation without memoization fails because the game graph contains cycles. For example, suppose cutting one head regenerates exactly one head. Then the state never changes and recursion loops forever.

A subtle edge case appears when Ivan can survive forever but cannot reach `(0,0)`.

Example:

```
1 0 5
1
1 0
1
0 0
```

From `(1,0)`, cutting one head leads back to `(1,0)`. Ivan never loses because the total never exceeds `R`, but he also never wins. The correct output is:

```
Draw
```

A shortest-path search that only looks for `(0,0)` would incorrectly conclude that Ivan loses.

Another important edge case is when every possible move immediately exceeds `R`.

Example:

```
1 0 1
1
2 0
1
0 0
```

Cutting one head produces `(2,0)`, whose total exceeds `R`. Ivan loses instantly:

```
Zmey
1
```

Careless implementations sometimes forget that exceeding `R` is an immediate terminal loss and accidentally insert those states into the graph.

One more subtle case is when Ivan cannot avoid eventual defeat, but different choices delay it by different amounts.

Example:

```
1 0 3
1
2 0
1
0 0
```

The only move is:

`(1,0) → (2,0) → (3,0) → lose`

The answer is:

```
Zmey
3
```

The number printed is the maximum number of moves Ivan can survive before the unavoidable loss.

## Approaches

The most direct idea is to view each state `(h,t)` as a node and recursively explore all possible moves. If a move reaches `(0,0)`, Ivan wins. If every move eventually exceeds `R`, the dragon wins. If some cycle exists, the game may continue forever.

This recursive approach is logically correct because the game is finite inside the legal region `h + t ≤ R`. The problem is that recursion alone cannot distinguish between useful revisits and infinite loops. A DFS that revisits the same state repeatedly may never terminate. Even with memoization, handling cycles correctly becomes complicated because the game is not a simple win-loss game, it has three outcomes with optimization criteria.

The key observation is that legal states form a directed graph with at most about forty thousand nodes. Once we think in graph terms, the problem splits naturally into three separate graph problems.

First, determine whether Ivan can reach `(0,0)` before leaving the legal region. Since every move costs one step, this is just shortest path in an unweighted graph.

If winning is impossible, determine whether Ivan can survive forever. That happens exactly when some cycle is reachable from the starting state while staying entirely inside the legal region.

If neither winning nor infinite survival is possible, the graph reachable from the start is a DAG ending at losing exits. In that situation Ivan wants the longest possible survival time, which becomes longest path in a DAG.

The structure of the state graph is what makes this decomposition work. Every legal move stays inside a bounded state space unless the dragon wins immediately. That boundedness allows standard graph algorithms to completely characterize the game.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force DFS | Exponential | Exponential recursion tree | Too slow |
| Optimal Graph + BFS + Cycle Detection + DP | O(R²(n+m)) | O(R²) | Accepted |

## Algorithm Walkthrough

1. Generate every legal state `(h,t)` such that `h + t ≤ R`.

These are the only states where the fight can continue. Any move producing a larger total means immediate defeat.
2. Build directed transitions between legal states.

For every state, try all possible head cuts and tail cuts. If the resulting state still satisfies `h + t ≤ R`, add an edge to it. Otherwise, the move is treated as an immediate losing exit.
3. Run BFS from the initial state to compute shortest distances.

Since every move costs exactly one blow, BFS gives the minimum number of moves to every reachable state.
4. If `(0,0)` is reachable, print `"Ivan"` and the BFS distance.

BFS guarantees this is the smallest possible number of blows.
5. Otherwise, check whether the reachable subgraph contains a cycle.

Run DFS with three colors:

`0 = unvisited`

`1 = currently in recursion stack`

`2 = fully processed`

Encountering an edge to a node with color `1` means a reachable cycle exists.
6. If a reachable cycle exists, print `"Draw"`.

Ivan can stay inside that cycle forever and avoid defeat indefinitely.
7. Otherwise, the reachable graph is acyclic.

Every path must eventually terminate at a move that exceeds `R`.
8. Compute the longest survival time with DP on the DAG.

Define `dp[state]` as the maximum number of moves before defeat starting from that state.

For a state with no outgoing legal moves, `dp = 1` because the next move immediately loses.

Otherwise:

`dp[state] = 1 + max(dp[next_state])`
9. Print `"Zmey"` and `dp[start]`.

This is the largest number of moves Ivan can survive when defeat is unavoidable.

### Why it works

The algorithm partitions all possible games into exactly three categories.

If `(0,0)` is reachable, BFS finds the shortest winning sequence because every edge has equal cost.

If `(0,0)` is unreachable but a reachable cycle exists, Ivan can remain inside legal states forever by looping through that cycle. Since defeat only happens by exceeding `R`, such a cycle guarantees infinite survival.

If neither condition holds, the reachable graph is a finite DAG. Every play eventually reaches a dead end where all moves lose immediately. Dynamic programming over the DAG computes the maximum possible survival length because each state chooses the best continuation among all legal moves.

These three cases are mutually exclusive and cover every possible game evolution.

## Python Solution

```python
import sys
from collections import deque

input = sys.stdin.readline

INF = 10**18

def solve():
    H, T, R = map(int, input().split())

    n = int(input())
    head = [(0, 0)] * (n + 1)
    for i in range(1, n + 1):
        head[i] = tuple(map(int, input().split()))

    m = int(input())
    tail = [(0, 0)] * (m + 1)
    for i in range(1, m + 1):
        tail[i] = tuple(map(int, input().split()))

    states = []
    for h in range(R + 1):
        for t in range(R + 1 - h):
            states.append((h, t))

    graph = {}
    for h, t in states:
        nxt = []

        for i in range(1, min(n, h) + 1):
            nh = h - i + head[i][0]
            nt = t + head[i][1]

            if nh + nt <= R:
                nxt.append((nh, nt))

        for i in range(1, min(m, t) + 1):
            nh = h + tail[i][0]
            nt = t - i + tail[i][1]

            if nh + nt <= R:
                nxt.append((nh, nt))

        graph[(h, t)] = nxt

    start = (H, T)
    target = (0, 0)

    dist = {start: 0}
    q = deque([start])

    while q:
        v = q.popleft()

        for to in graph[v]:
            if to not in dist:
                dist[to] = dist[v] + 1
                q.append(to)

    if target in dist:
        print("Ivan")
        print(dist[target])
        return

    color = {}
    has_cycle = False

    def dfs(v):
        nonlocal has_cycle

        color[v] = 1

        for to in graph[v]:
            if to not in dist:
                continue

            if color.get(to, 0) == 0:
                dfs(to)
            elif color[to] == 1:
                has_cycle = True

        color[v] = 2

    dfs(start)

    if has_cycle:
        print("Draw")
        return

    dp = {}

    def longest(v):
        if v in dp:
            return dp[v]

        if not graph[v]:
            dp[v] = 1
            return 1

        best = 0
        for to in graph[v]:
            best = max(best, longest(to))

        dp[v] = best + 1
        return dp[v]

    print("Zmey")
    print(longest(start))

solve()
```

The graph construction follows the exact game rules. Every legal state stores only transitions that remain within the allowed total `R`. Moves exceeding `R` are deliberately excluded because they represent immediate defeat, not another playable state.

The BFS section solves the winning case first because Ivan always prefers winning over drawing or delaying defeat. Using BFS instead of DFS matters because the answer requires the minimum number of blows.

The cycle detection DFS only traverses states reachable from the start. A cycle elsewhere in the graph is irrelevant if Ivan cannot enter it. The three-color DFS is the standard way to detect directed cycles. Seeing a node already in the recursion stack means we found a back edge and thus an infinite loop.

The longest-path DP works only because the graph is guaranteed acyclic after the draw case has been ruled out. Without that property, recursion would loop forever. States with no outgoing legal edges return `1` because Ivan still gets one final move before losing immediately.

One subtle detail is the order of checks. We must test reachability of `(0,0)` before checking cycles. A reachable cycle does not matter if Ivan already has a winning strategy, because he always prefers winning.

## Worked Examples

### Sample 1

Input:

```
2 2 4
2
1 0
0 1
3
0 1
0 1
0 0
```

State transitions:

| Current State | Move | Next State |
| --- | --- | --- |
| (2,2) | cut 2 tails | (2,1) |
| (2,1) | cut 1 head | (2,1) |
| (2,1) | cut 1 tail | (2,1) |
| (2,1) | cut 3 tails impossible | - |
| (2,1) | cut 2 heads | (0,2) |
| (0,2) | cut 2 tails | (0,1) |
| (0,1) | cut 1 tail | (0,0) |

Shortest winning sequence:

| Step | State |
| --- | --- |
| 0 | (2,2) |
| 1 | (0,2) |
| 2 | (0,0) |

Output:

```
Ivan
2
```

This trace shows why BFS is necessary. Multiple loops exist, but BFS still finds the shortest path to victory.

### Example 2

Input:

```
1 0 5
1
1 0
1
0 0
```

Reachable states:

| Step | State |
| --- | --- |
| 0 | (1,0) |
| 1 | (1,0) |
| 2 | (1,0) |
| ... | ... |

The only move returns to the same state forever.

Output:

```
Draw
```

This demonstrates the cycle condition. Ivan cannot win, but he can avoid defeat indefinitely.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(R²(n+m)) | Every legal state tries all head and tail operations |
| Space | O(R²) | Graph, BFS, DFS, and DP store information for each state |

With `R ≤ 200`, the number of states is at most around forty thousand. Each state processes at most four hundred transitions. The total work comfortably fits inside the limits in Python.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io
from collections import deque

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    input = sys.stdin.readline

    H, T, R = map(int, input().split())

    n = int(input())
    head = [(0, 0)] * (n + 1)
    for i in range(1, n + 1):
        head[i] = tuple(map(int, input().split()))

    m = int(input())
    tail = [(0, 0)] * (m + 1)
    for i in range(1, m + 1):
        tail[i] = tuple(map(int, input().split()))

    states = []
    for h in range(R + 1):
        for t in range(R + 1 - h):
            states.append((h, t))

    graph = {}
    for h, t in states:
        nxt = []

        for i in range(1, min(n, h) + 1):
            nh = h - i + head[i][0]
            nt = t + head[i][1]

            if nh + nt <= R:
                nxt.append((nh, nt))

        for i in range(1, min(m, t) + 1):
            nh = h + tail[i][0]
            nt = t - i + tail[i][1]

            if nh + nt <= R:
                nxt.append((nh, nt))

        graph[(h, t)] = nxt

    start = (H, T)
    target = (0, 0)

    dist = {start: 0}
    q = deque([start])

    while q:
        v = q.popleft()

        for to in graph[v]:
            if to not in dist:
                dist[to] = dist[v] + 1
                q.append(to)

    out = []

    if target in dist:
        out.append("Ivan")
        out.append(str(dist[target]))
        return "\n".join(out)

    color = {}
    has_cycle = False

    def dfs(v):
        nonlocal has_cycle

        color[v] = 1

        for to in graph[v]:
            if to not in dist:
                continue

            if color.get(to, 0) == 0:
                dfs(to)
            elif color[to] == 1:
                has_cycle = True

        color[v] = 2

    dfs(start)

    if has_cycle:
        return "Draw"

    dp = {}

    def longest(v):
        if v in dp:
            return dp[v]

        if not graph[v]:
            dp[v] = 1
            return 1

        best = 0
        for to in graph[v]:
            best = max(best, longest(to))

        dp[v] = best + 1
        return dp[v]

    out.append("Zmey")
    out.append(str(longest(start)))

    return "\n".join(out)

# provided sample
assert run(
"""2 2 4
2
1 0
0 1
3
0 1
0 1
0 0
"""
) == "Ivan\n2", "sample 1"

# draw loop
assert run(
"""1 0 5
1
1 0
1
0 0
"""
) == "Draw", "infinite cycle"

# immediate loss
assert run(
"""1 0 1
1
2 0
1
0 0
"""
) == "Zmey\n1", "forced immediate defeat"

# shortest win
assert run(
"""1 1 3
1
0 0
1
0 0
"""
) == "Ivan\n2", "minimal winning path"

# longer forced survival
assert run(
"""1 0 3
1
2 0
1
0 0
"""
) == "Zmey\n3", "maximize survival time"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Infinite self-loop | Draw | Reachable cycle detection |
| Immediate overflow | Zmey 1 | Losing moves are not added as states |
| Small direct win | Ivan 2 | BFS shortest-path correctness |
| Growing chain | Zmey 3 | Longest survival DP |
| Official sample | Ivan 2 | Full integration |

## Edge Cases

Consider the self-loop case:

```
1 0 5
1
1 0
1
0 0
```

From `(1,0)`, cutting one head regenerates one head. BFS never reaches `(0,0)`. DFS then visits `(1,0)` and immediately finds an edge back to a node already in the recursion stack. The algorithm prints:

```
Draw
```

This correctly captures infinite survival.

Now consider immediate defeat:

```
1 0 1
1
2 0
1
0 0
```

The only transition is:

`(1,0) → (2,0)`

Since `2 > R`, this edge is excluded from the graph. The start state has no legal outgoing edges. BFS cannot reach `(0,0)`, DFS finds no cycle, and the DP returns `1`. The algorithm prints:

```
Zmey
1
```

The answer counts the final losing move correctly.

Finally, consider unavoidable but delayed defeat:

```
1 0 3
1
2 0
1
0 0
```

The reachable states are:

`(1,0) → (2,0) → (3,0)`

From `(3,0)`, every move exceeds `R`. The graph is acyclic, so DP computes:

| State | dp |
| --- | --- |
| (3,0) | 1 |
| (2,0) | 2 |
| (1,0) | 3 |

The output becomes:

```
Zmey
3
```

This confirms that the algorithm maximizes survival length when defeat cannot be avoided.
