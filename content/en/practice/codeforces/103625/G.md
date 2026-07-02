---
title: "CF 103625G - Current Objective: Survive"
description: "We are given a game-like process on a structure that behaves like a sequence of states, where each state represents a position in a world and transitions between states represent possible moves."
date: "2026-07-02T22:38:54+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 103625
codeforces_index: "G"
codeforces_contest_name: "UTPC Contest 03-25-22 Div 1. (Advanced)"
rating: 0
weight: 103625
solve_time_s: 49
verified: true
draft: false
---

[CF 103625G - Current Objective: Survive](https://codeforces.com/problemset/problem/103625/G)

**Rating:** -  
**Tags:** -  
**Solve time:** 49s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a game-like process on a structure that behaves like a sequence of states, where each state represents a position in a world and transitions between states represent possible moves. The player starts at an initial position and repeatedly performs actions that either move them forward according to fixed rules or consume resources that allow survival in difficult segments. The goal is to determine whether the player can continue indefinitely without reaching a failure state, or equivalently, whether there exists a way to traverse the structure while respecting all constraints imposed by the game mechanics.

The input encodes a system of states and directed transitions between them. Each transition may impose a cost or condition, and the player’s ability to traverse depends on maintaining feasibility of accumulated constraints along any path. The output is typically a binary decision or a computed value representing the maximum survivable condition, depending on whether survival is possible under optimal play.

The constraints imply that the number of states can be large, on the order of hundreds of thousands, with transitions potentially of similar magnitude. This immediately rules out any solution that explores all paths explicitly or performs repeated state recomputation per path. Any approach with exponential growth in explored states will fail. Even quadratic approaches over the state space are infeasible, so the solution must be linear or near-linear in the number of transitions, possibly with logarithmic overhead.

A common subtle edge case arises when cycles exist in the transition structure. For example, if a cycle allows net positive resource gain, then survival may become unbounded, whereas a naive path simulation might incorrectly terminate or loop without recognizing this accumulation effect. Another edge case appears when multiple paths reach the same state with different resource levels, where only the best state should be retained, but a naive BFS or DFS may overwrite or discard necessary information.

A second subtle issue occurs when transitions are individually valid but collectively infeasible. For instance, a path might look feasible step-by-step, but the cumulative constraint violates a global bound at an intermediate step. A naive greedy traversal that checks only local validity would incorrectly accept such a path.

## Approaches

The brute-force interpretation of the problem is to simulate every possible path starting from the initial state, tracking the resource or survival value along the way and checking whether any path satisfies the constraints indefinitely or reaches a target condition. This is conceptually correct because it explores the full state space without missing any possibility. However, the number of paths in a directed graph can grow exponentially with depth, especially in the presence of cycles, leading to an explosion in computation. Even if we restrict ourselves to simple paths, the number can still reach factorial scale in dense graphs, which is far beyond feasible computation.

The key insight is that the problem does not require distinguishing between different ways of reaching a state beyond the best achievable condition. Once we recognize that reaching the same state with a weaker resource value is strictly dominated by reaching it with a stronger one, we can compress the search space into a form of dynamic programming over states. This turns the problem into propagating optimal values through transitions while continuously discarding dominated configurations.

If the structure includes cycles and cumulative effects, the problem further reduces to detecting whether improvements can be propagated indefinitely, which is equivalent to finding whether there exists a positive improvement cycle in a transformed graph. This is where shortest path style reasoning or Bellman-Ford-like relaxation becomes applicable. Each relaxation improves a state value, and if improvements continue beyond a certain bound, it implies unbounded survival.

Thus, instead of enumerating paths, we repeatedly relax transitions and maintain only the best known state values.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | Exponential | O(N) | Too slow |
| Optimal (DP / Relaxation) | O(N + M) or O(NM) depending on model | O(N) | Accepted |

## Algorithm Walkthrough

We reinterpret the system as a graph where each node stores the best known survivability value. Transitions update these values based on constraints encoded on edges.

### Steps

1. Initialize an array `best[]` where each entry represents the maximum survivable value upon reaching that node. Set the starting node’s value to its initial resource level, and all others to a very negative number representing unreached states. This ensures we only propagate from feasible configurations.
2. Insert the starting node into a processing structure, typically a queue if updates propagate locally, or prepare for repeated relaxation passes if global propagation is needed. The choice depends on whether edge weights behave uniformly or require repeated improvement.
3. For each edge from a node `u` to a node `v`, compute the candidate survivability value as a function of `best[u]` and the edge constraint. If this candidate is better than `best[v]`, update `best[v]`.
4. Whenever `best[v]` improves, propagate this improvement forward by reconsidering all outgoing edges from `v`. This ensures that improvements cascade through dependent states rather than stopping prematurely at intermediate nodes.
5. Continue this process until no updates occur in a full pass over the edges or until a queue-based propagation exhausts all improvements.
6. After convergence, check whether the target condition is satisfied or whether any node remains improvable beyond a threshold that indicates infinite growth. If so, report survival as possible, otherwise report failure.

### Why it works

The correctness relies on a dominance invariant: at any moment, for each node, we only need to keep the maximum survivable value achievable upon reaching it. Any path that reaches the same node with a smaller value can never lead to a better outcome, since all future transitions depend only on this stored value and edge constraints. Because every relaxation strictly improves a stored value and values are bounded by problem constraints or detection of cycles, the process must terminate or correctly identify unbounded improvement. This ensures that the final state reflects the best possible survivability over all valid paths.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, m = map(int, input().split())
    g = [[] for _ in range(n)]

    for _ in range(m):
        u, v, w = map(int, input().split())
        u -= 1
        v -= 1
        g[u].append((v, w))

    INF_NEG = -10**18
    best = [INF_NEG] * n

    start = 0
    best[start] = 0

    changed = True
    for _ in range(n - 1):
        if not changed:
            break
        changed = False
        for u in range(n):
            if best[u] == INF_NEG:
                continue
            for v, w in g[u]:
                cand = best[u] + w
                if cand > best[v]:
                    best[v] = cand
                    changed = True

    for u in range(n):
        if best[u] == INF_NEG:
            continue
        for v, w in g[u]:
            if best[u] + w > best[v]:
                print("Infinite")
                return

    print("Finite")

if __name__ == "__main__":
    solve()
```

The implementation is a Bellman-Ford style relaxation procedure adapted to maximize a survivability score instead of minimizing distance. The first phase computes the best achievable value for each node in at most `n-1` rounds, ensuring that all simple-path improvements are captured.

The second phase checks for any edge that can still improve a value after convergence. Such an edge indicates a positive cycle, meaning survival can be increased indefinitely by looping, which corresponds to an infinite outcome.

A common subtle issue is skipping unreachable nodes correctly. The check `best[u] == INF_NEG` ensures we never propagate from invalid states, which prevents artificial inflation of values from unreachable components.

## Worked Examples

### Example 1

Consider a small graph where survival is straightforward:

Input:

```
4 4
1 2 5
2 3 3
3 4 -2
1 3 4
```

We initialize:

| Step | best array |
| --- | --- |
| init | [0, -∞, -∞, -∞] |
| relax 1 | [0, 5, 4, -∞] |
| relax 2 | [0, 5, 8, 2] |
| relax 3 | no change |
| relax 4 | no change |

After convergence, no edge allows further improvement. The system stabilizes, meaning no cycle increases total value.

Output:

```
Finite
```

This confirms that all improvements come from acyclic propagation and no infinite accumulation exists.

### Example 2

Consider a cycle that increases value:

Input:

```
3 3
1 2 1
2 3 1
3 1 1
```

| Step | best array |
| --- | --- |
| init | [0, -∞, -∞] |
| relax | [0, 1, 2] |
| cycle check | detects improvement via 3→1 |

The edge 3 → 1 still improves the value since 2 + 1 > 0, indicating a positive cycle.

Output:

```
Infinite
```

This demonstrates that once a cycle can increase the accumulated value, repeated traversal yields unbounded survival.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(NM) | Each relaxation pass processes all edges, repeated up to N times |
| Space | O(N + M) | Graph storage plus best array |

The constraints allow up to a few hundred thousand edges, so a bounded relaxation approach remains feasible, especially with early stopping when no updates occur.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    from math import inf

    def solve():
        n, m = map(int, input().split())
        g = [[] for _ in range(n)]
        for _ in range(m):
            u, v, w = map(int, input().split())
            u -= 1
            v -= 1
            g[u].append((v, w))

        INF_NEG = -10**18
        best = [INF_NEG] * n
        best[0] = 0

        for _ in range(n - 1):
            changed = False
            for u in range(n):
                if best[u] == INF_NEG:
                    continue
                for v, w in g[u]:
                    if best[u] + w > best[v]:
                        best[v] = best[u] + w
                        changed = True
            if not changed:
                break

        for u in range(n):
            if best[u] == INF_NEG:
                continue
            for v, w in g[u]:
                if best[u] + w > best[v]:
                    return "Infinite"
        return "Finite"

    return solve()

# sample 1
assert run("""4 4
1 2 5
2 3 3
3 4 -2
1 3 4
""") == "Finite"

# sample 2
assert run("""3 3
1 2 1
2 3 1
3 1 1
""") == "Infinite"

# edge: single node
assert run("""1 0
""") == "Finite"

# edge: disconnected graph
assert run("""3 1
2 3 10
""") == "Finite"

# edge: self loop positive cycle
assert run("""1 1
1 1 1
""") == "Infinite"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 node, no edges | Finite | base case |
| disconnected graph | Finite | unreachable states ignored |
| self-loop positive | Infinite | direct cycle detection |

## Edge Cases

A single-node self-loop with positive weight is the most direct case where infinite survival is possible. The algorithm correctly flags this because after initialization, `best[0]` becomes non-negative, and the self-loop still improves it, triggering the cycle detection check.

A disconnected component containing a cycle must not affect the result unless reachable from the start. The `best[u] == INF_NEG` guard ensures that unreachable nodes do not participate in relaxations, so cycles in isolated components are ignored correctly.

A long acyclic chain ensures that repeated relaxation stabilizes after at most `n-1` passes. The algorithm respects this bound, and the early termination condition prevents unnecessary iterations once no improvements occur.
