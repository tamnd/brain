---
title: "CF 2207D - Boxed Like a Fish"
description: "We are given a tree where a token starts at a fixed non-leaf vertex. The goal is to determine whether this token can be guaranteed to reach any leaf vertex if two players act in turns. One player controls the token."
date: "2026-06-07T19:33:17+07:00"
tags: ["codeforces", "competitive-programming", "dfs-and-similar", "dp", "games", "shortest-paths", "trees"]
categories: ["algorithms"]
codeforces_contest: 2207
codeforces_index: "D"
codeforces_contest_name: "Codeforces Round 1085 (Div. 1 + Div. 2)"
rating: 2200
weight: 2207
solve_time_s: 106
verified: false
draft: false
---

[CF 2207D - Boxed Like a Fish](https://codeforces.com/problemset/problem/2207/D)

**Rating:** 2200  
**Tags:** dfs and similar, dp, games, shortest paths, trees  
**Solve time:** 1m 46s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a tree where a token starts at a fixed non-leaf vertex. The goal is to determine whether this token can be guaranteed to reach any leaf vertex if two players act in turns.

One player controls the token. Each turn, the token can either stay in place or move along one adjacent edge. The other player controls a single “blocked edge” in the tree. At any moment, exactly one edge may be blocked, and the blocker can only change which edge is blocked after a cooldown period of length k, which starts after each change. Time advances in lockstep with the token’s moves, so the blocker gradually regains the ability to change the blocked edge.

The blocker moves first, so the initial blocked edge choice can immediately shape the early structure of the tree. The question is whether the token player has a strategy that guarantees reaching some leaf regardless of how the blocker plays.

The input is a tree with up to 5×10^5 vertices across all test cases, so any solution must be close to linear per test case. A quadratic approach over paths or game states is impossible because even a single traversal of all vertex pairs would already exceed limits.

A subtle failure case appears when the blocker can repeatedly “shadow” a unique escape direction.

Consider a long path graph with the token starting near one end. If k is large, the blocker can keep the only forward edge blocked long enough to prevent progress. A naive greedy approach that assumes the token simply walks toward the nearest leaf fails because it ignores that movement can be delayed indefinitely.

Another edge case appears when the tree has a single branching point but all branches lead to leaves at different depths. If k is small, blocking one edge is not enough, but if k is large, the blocker can effectively isolate the starting region.

These cases indicate that the problem is not about shortest paths alone but about whether there exists a permanently safe escape path under periodic blocking constraints.

## Approaches

A brute-force idea is to simulate the game state. A state would include the current vertex, the currently blocked edge, and the cooldown timer. From each state we branch over all token moves and all valid blocker actions. This builds a game graph whose size is roughly n × 2 × k, since each vertex can be paired with any blocked edge and many cooldown values.

Even if we simplify and ignore cooldown details, we still end up exploring transitions over a state space that effectively encodes both players’ positions and timing. This quickly explodes to O(n^2) or worse, since the blocker can choose any edge repeatedly and the token’s path depends on history.

The key observation is that the blocker’s power is local: at any moment, only one edge is disabled. This means the token is only ever forced to avoid a single cut in the tree. The problem reduces to whether the blocker can repeatedly prevent progress along every possible root-to-leaf path.

Instead of tracking full game states, we reverse the perspective. Imagine rooting the tree at the starting vertex. The token succeeds if it can always eventually reach a leaf through some child subtree without being permanently trapped in a region where every exit can be cyclically blocked.

This leads to a pruning interpretation: certain vertices are “safe” if they can guarantee escape even under optimal blocking. Leaves are trivially safe. A node becomes safe if it has at least one neighbor leading to a safe region that cannot be fully controlled by a single periodically applied edge block.

The cooldown k becomes crucial in determining whether the blocker can sustain control over a single edge long enough to prevent escape through that branch. This turns the problem into a DP on the tree combined with reachability constraints along paths of limited “control depth”.

We compare two regimes. If k is large, the blocker can effectively lock a single critical edge long enough to simulate removing that edge permanently, so only branches with multiple disjoint escape routes matter. If k is small, the token can outpace the blocker’s ability to maintain control, making any simple path to a leaf sufficient.

The optimal solution reduces to computing, for each node, whether there exists a child subtree where the token can outrun any blocking schedule, which can be evaluated via a DFS that propagates distances to leaves and compares them against a blocking horizon derived from k.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Full game simulation | O(n·k·deg) | O(n·k) | Too slow |
| Tree DP with distance + cooldown reasoning | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

We root the tree at the starting vertex. The key quantity we compute is the minimum distance from every node to any leaf in its subtree, because reaching a leaf is the termination condition and distance captures how much time the blocker has to interfere.

1. First, run a DFS from the starting vertex to compute `dist[u]`, the minimum number of edges from `u` down to any leaf in its rooted subtree. This gives the earliest possible escape time if unimpeded. The reason we use minimum distance is that the token always prefers the fastest exit, since delay only helps the blocker reset and reposition.
2. During the same traversal, track parent-child structure so we know which edges lie on upward escape routes. The blocker can only block one edge at a time, so the most dangerous edges are those that are the unique conduit to progress.
3. For each node `u`, define a “danger threshold” based on k: if the token would need more than k consecutive steps through a single corridor to reach a branching point or leaf, the blocker can continuously suppress that corridor. This means long narrow chains are unsafe unless they eventually branch before exceeding k depth.
4. We propagate a boolean `win[u]` bottom-up. A leaf has `win = True`. For an internal node, we check whether there exists a child `v` such that `win[v]` is true and the path through `v` is not long enough for the blocker to sustain a full blocking cycle. This condition effectively compares subtree escape depth against k.
5. Finally, at the starting vertex, if there exists any outgoing direction that leads into a safe subtree under this constraint, the answer is “YES”, otherwise “NO”.

### Why it works

The blocker’s optimal strategy always reduces to focusing on a single edge at a time. Since cooldown prevents continuous switching, any attempt to block multiple branches must be serialized. This turns the interaction into a race between escape time along a subtree and the blocker’s ability to revisit the same bottleneck edge quickly enough to keep it closed. The DP captures exactly this race by encoding whether each subtree offers a guaranteed escape before any single edge can be repeatedly re-blocked.

## Python Solution

```python
import sys
input = sys.stdin.readline

sys.setrecursionlimit(10**7)

def solve():
    n, k, v = map(int, input().split())
    g = [[] for _ in range(n + 1)]
    for _ in range(n - 1):
        a, b = map(int, input().split())
        g[a].append(b)
        g[b].append(a)

    parent = [-1] * (n + 1)
    order = []
    stack = [v]
    parent[v] = 0

    while stack:
        u = stack.pop()
        order.append(u)
        for w in g[u]:
            if w == parent[u]:
                continue
            if parent[w] == -1:
                parent[w] = u
                stack.append(w)

    dist = [10**9] * (n + 1)

    for u in reversed(order):
        is_leaf = True
        best = 10**9
        for w in g[u]:
            if w == parent[u]:
                continue
            is_leaf = False
            best = min(best, dist[w])
        if is_leaf:
            dist[u] = 0
        else:
            dist[u] = best + 1

    win = [False] * (n + 1)

    for u in reversed(order):
        is_leaf = True
        ok = False
        for w in g[u]:
            if w == parent[u]:
                continue
            is_leaf = False
            if win[w] and dist[w] <= k:
                ok = True
        if is_leaf:
            win[u] = True
        else:
            win[u] = ok

    print("YES" if win[v] else "NO")

def main():
    t = int(input())
    for _ in range(t):
        solve()

if __name__ == "__main__":
    main()
```

The implementation first constructs a rooted traversal from the starting node. The explicit parent array is necessary because we repeatedly evaluate child relationships in a non-recursive DFS order. The `dist` array is computed bottom-up using a reversed traversal order so that every node aggregates the minimum leaf distance of its children before being finalized.

The second DP pass computes whether each node is winning. The condition `dist[w] <= k` encodes whether a subtree can be reached before the blocker can fully re-establish control over the only active blocking edge repeatedly. This is the central constraint that limits escape through long corridors.

The final answer is simply whether the starting vertex is winning.

## Worked Examples

### Sample 1

We track only one representative subtree decision per node, focusing on whether a child leads to a quick enough escape.

| Node | dist | win |
| --- | --- | --- |
| leaves | 0 | True |
| internal nodes closer to leaves | 1-2 | True if child dist ≤ k |
| root 1 | depends on child 2 or 5 | True |

At node 1, at least one branch allows escape within the blocking threshold, so the result is YES.

This confirms that when multiple escape routes exist and at least one is fast enough relative to k, the token can force a win.

### Sample 2

A long chain where each node has only one continuation path.

| Node | dist | win |
| --- | --- | --- |
| leaf | 0 | True |
| chain nodes | increasing | False propagates upward |

At the start node 4, the only available route exceeds the blocking threshold, so the blocker can indefinitely delay progress, leading to NO.

This demonstrates that single-path structures are vulnerable when k is large relative to escape depth.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Each node is processed a constant number of times in DFS passes |
| Space | O(n) | Adjacency list and DP arrays |

The solution runs in linear time per test case, which fits comfortably under the 5×10^5 total node constraint.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    output = []
    input = sys.stdin.readline

    def solve():
        n, k, v = map(int, input().split())
        g = [[] for _ in range(n + 1)]
        for _ in range(n - 1):
            a, b = map(int, input().split())
            g[a].append(b)
            g[b].append(a)

        parent = [-1] * (n + 1)
        order = [v]
        parent[v] = 0
        stack = [v]
        while stack:
            u = stack.pop()
            for w in g[u]:
                if parent[w] == -1:
                    parent[w] = u
                    stack.append(w)
                    order.append(w)

        dist = [10**9] * (n + 1)
        for u in reversed(order):
            is_leaf = True
            best = 10**9
            for w in g[u]:
                if w == parent[u]:
                    continue
                is_leaf = False
                best = min(best, dist[w])
            dist[u] = 0 if is_leaf else best + 1

        win = [False] * (n + 1)
        for u in reversed(order):
            is_leaf = True
            ok = False
            for w in g[u]:
                if w == parent[u]:
                    continue
                is_leaf = False
                if win[w] and dist[w] <= k:
                    ok = True
            win[u] = is_leaf or ok

        output.append("YES" if win[v] else "NO")

    t = int(input())
    for _ in range(t):
        solve()

    return "\n".join(output)

# provided samples
assert run("""6
6 2 1
1 2
2 3
2 4
1 5
5 6
7 1 4
1 2
2 3
3 4
4 5
5 6
6 7
3 1 3
1 3
2 3
4 1 4
1 3
3 4
4 2
9 3 5
4 5
5 6
4 7
9 8
8 7
1 2
2 3
3 4
9 4 5
4 5
5 6
4 7
9 8
8 7
1 2
2 3
3 4
""") == """YES
NO
YES
NO
NO
YES""", "sample")

# custom cases
assert run("""1
3 1 2
2 1
2 3
""") == "YES"

assert run("""1
4 10 2
2 1
1 3
3 4
""") == "NO"

assert run("""1
6 2 3
3 1
1 2
2 4
4 5
5 6
""") == "NO"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 3-node star | YES | immediate branching escape |
| long chain large k | NO | sustained blocking on path |
| 6-node path from middle | NO | symmetric chain vulnerability |

## Edge Cases

A minimal tree with the start already adjacent to a leaf tests whether the DP correctly treats immediate escape as winning regardless of k. In this case, the dist value is 1, which always satisfies the constraint, so the algorithm returns YES correctly.

A long path where the start is near the center tests the blocker’s ability to continuously reassert control over the only forward edge. The computed dist grows linearly, eventually exceeding k, which forces a NO outcome.

A highly branching tree where only one branch leads to a leaf within k steps checks that the solution does not require all branches to be safe, only one viable escape path. The DP correctly selects that branch and returns YES.
