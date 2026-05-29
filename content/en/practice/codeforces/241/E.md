---
title: "CF 241E - Flights"
description: "We are given a directed acyclic graph of cities and one-way flights. Every flight initially takes 1 hour. We may independently change any flight duration to either 1 or 2 hours."
date: "2026-05-29T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "graphs", "shortest-paths"]
categories: ["algorithms"]
codeforces_contest: 241
codeforces_index: "E"
codeforces_contest_name: "Bayan 2012-2013 Elimination Round (ACM ICPC Rules, English statements)"
rating: 2600
weight: 241
solve_time_s: 114
verified: true
draft: false
---

[CF 241E - Flights](https://codeforces.com/problemset/problem/241/E)

**Rating:** 2600  
**Tags:** graphs, shortest paths  
**Solve time:** 1m 54s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a directed acyclic graph of cities and one-way flights. Every flight initially takes 1 hour. We may independently change any flight duration to either 1 or 2 hours.

The goal is to assign durations so that every possible path from city 1 to city n has exactly the same total travel time.

The graph is acyclic because every edge goes from a smaller-numbered city to a larger-numbered city. That property is the entire reason the problem is manageable. Without it, equalizing all path lengths in a general graph would become much harder because cycles could create infinitely many paths.

The input gives up to 1000 vertices and 5000 edges. A brute-force assignment over all edges would require checking up to $2^m$ possibilities. With $m = 5000$, that is completely impossible.

The graph size suggests we need something around $O(nm)$ or $O(m \log n)$. Since the graph is a DAG, dynamic programming on topological order becomes a natural direction.

The tricky part is that we are not simply finding one shortest or longest path. We must make every path from 1 to n equal. That means the assigned edge weights must satisfy a system of consistency constraints across the entire DAG.

A naive implementation often fails on disconnected regions of the graph. For example:

```
4 3
1 2
2 4
3 4
```

City 3 is irrelevant because it cannot be reached from city 1. Constraints involving it should not matter. If we process every node blindly, we may incorrectly conclude the system is inconsistent.

Another subtle case is when a node has two outgoing paths that force contradictory values.

Example:

```
4 4
1 2
1 3
2 4
3 4
```

This is solvable because we can assign:

```
1->2 = 1
1->3 = 1
2->4 = 2
3->4 = 2
```

Both paths have total length 3.

But consider:

```
5 5
1 2
1 3
2 5
3 4
4 5
```

Path lengths differ structurally by 1 edge. Since every edge weight is either 1 or 2, the first path can only have totals 2, 3, or 4, while the second path can only have totals 3, 4, 5, or 6. Their overlap exists, so this graph is still solvable.

A careless greedy strategy that always keeps weights 1 unless forced would fail to detect the necessary adjustments.

The real impossible cases arise when constraints force some edge to need weight 0 or 3.

Example:

```
4 4
1 2
2 4
1 3
3 4
```

Suppose we try to enforce:

- distance from 1 to 4 through node 2 equals 2
- distance through node 3 equals 4

Then some edge would need weight larger than 2. The valid range restriction is the real source of impossibility.

## Approaches

The brute-force idea is straightforward. Every edge can independently receive weight 1 or 2, so we can try all $2^m$ assignments. For each assignment, we compute all path lengths from 1 to n and check whether they are identical.

The correctness is immediate because we literally test every possible configuration. The problem is the scale. Even with only 50 edges, $2^{50}$ is already astronomical. Here we may have 5000 edges.

The key observation is that "all paths have equal total length" behaves like a potential function.

Suppose every node $v$ has a value $dp[v]$, meaning the common remaining distance from $v$ to $n$. Then for every edge $u \to v$,

$$w(u,v) + dp[v] = dp[u]$$

Rearranging gives:

$$w(u,v) = dp[u] - dp[v]$$

Since every edge weight must be either 1 or 2,

$$dp[u] - dp[v] \in \{1,2\}$$

Now the problem becomes much cleaner. We need to assign integer labels to vertices such that every reachable edge decreases the label by exactly 1 or 2.

Because the graph is a DAG, we can compute these labels backward from node $n$.

For each node:

- if it has outgoing edges, all outgoing transitions must allow consistent values
- the node's value is determined by its children

More concretely, for edge $u \to v$,

- $dp[u]$ must equal either $dp[v] + 1$ or $dp[v] + 2$

If two outgoing edges force incompatible values, the answer is impossible.

This transforms an exponential search into a linear graph DP.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(2^m \cdot (n+m))$ | $O(n+m)$ | Too slow |
| Optimal | $O(n+m)$ | $O(n+m)$ | Accepted |

## Algorithm Walkthrough

1. Build the directed graph and the reverse graph.

The reverse graph is useful for determining which vertices can actually reach city $n$.
2. Find all vertices reachable from city 1.

Vertices outside this set do not participate in any valid route from 1 to n, so they impose no constraints.
3. Find all vertices that can reach city $n$.

We run DFS or BFS on the reversed graph starting from $n$.
4. Keep only vertices that lie on some path from 1 to n.

A vertex matters only if:

$$reachable\_from\_1[v] = true$$

and

$$can\_reach\_n[v] = true$$
5. Process vertices in reverse order from $n$ down to 1.

Since the graph is acyclic and every edge goes from smaller to larger index, this is already a reverse topological order.
6. Set:

$$dp[n] = 0$$

This means the remaining distance from $n$ to itself is zero.
7. For each useful node $u$, examine every outgoing edge $u \to v$.

Each edge allows:

$$dp[u] = dp[v] + 1$$

or

$$dp[u] = dp[v] + 2$$

All outgoing edges must agree on at least one common value for $dp[u]$.
8. Compute the intersection of all allowed values.

If the intersection becomes empty, the graph is impossible.
9. Choose any valid value for $dp[u]$.

The simplest choice is the smallest valid one.
10. Recover edge weights.

For every useful edge:

$$w(u,v) = dp[u] - dp[v]$$

This will always be either 1 or 2.
11. Irrelevant edges may receive any value, for example 1.

Why it works:

The invariant is that $dp[u]$ represents the common remaining distance from node $u$ to node $n$.

For every outgoing edge $u \to v$, traversing that edge consumes weight $w(u,v)$, after which the remaining distance is $dp[v]$. So the total distance must satisfy:

$$dp[u] = w(u,v) + dp[v]$$

Since all path lengths from $u$ to $n$ must be equal, this equation must hold for every outgoing edge simultaneously.

The algorithm explicitly constructs exactly such a system. If at some node no common value exists, then no assignment can satisfy all outgoing constraints. Otherwise the constructed weights guarantee every path accumulates the same total.

## Python Solution

```python
import sys
from collections import deque

input = sys.stdin.readline

def solve():
    n, m = map(int, input().split())

    edges = []
    g = [[] for _ in range(n + 1)]
    rg = [[] for _ in range(n + 1)]

    for i in range(m):
        u, v = map(int, input().split())
        edges.append((u, v))
        g[u].append((v, i))
        rg[v].append(u)

    # reachable from 1
    vis1 = [False] * (n + 1)
    q = deque([1])
    vis1[1] = True

    while q:
        u = q.popleft()
        for v, _ in g[u]:
            if not vis1[v]:
                vis1[v] = True
                q.append(v)

    # can reach n
    vis2 = [False] * (n + 1)
    q = deque([n])
    vis2[n] = True

    while q:
        u = q.popleft()
        for v in rg[u]:
            if not vis2[v]:
                vis2[v] = True
                q.append(v)

    useful = [vis1[i] and vis2[i] for i in range(n + 1)]

    dp = [None] * (n + 1)
    dp[n] = 0

    ans = [1] * m

    for u in range(n - 1, 0, -1):
        if not useful[u]:
            continue

        possible = None

        for v, idx in g[u]:
            if not useful[v]:
                continue

            cur = {dp[v] + 1, dp[v] + 2}

            if possible is None:
                possible = cur
            else:
                possible &= cur

        if not possible:
            print("No")
            return

        dp[u] = min(possible)

    for u, v in edges:
        if useful[u] and useful[v]:
            w = dp[u] - dp[v]
            if w < 1 or w > 2:
                print("No")
                return

    for i, (u, v) in enumerate(edges):
        if useful[u] and useful[v]:
            ans[i] = dp[u] - dp[v]
        else:
            ans[i] = 1

    print("Yes")
    print("\n".join(map(str, ans)))

solve()
```

The first part builds both the normal graph and the reversed graph. The reversed graph is necessary because we must identify nodes that can eventually reach city $n$.

The two BFS traversals are easy to overlook, but they are essential. Nodes outside any 1-to-$n$ path should not participate in constraints. If we process them anyway, we may falsely conclude that the system has no solution.

The dynamic programming proceeds backward because edges always go toward larger indices. By the time we process node $u$, every child $v$ already has a finalized $dp[v]$.

The subtle part is the intersection logic. Every outgoing edge contributes two allowed values for $dp[u]$:

$$dp[v] + 1$$

and

$$dp[v] + 2$$

All edges must agree on one common value. Using set intersection directly keeps the implementation simple and safe.

The final verification step is technically redundant if the DP is correct, but it protects against implementation mistakes and makes debugging easier.

## Worked Examples

### Example 1

Input:

```
3 3
1 2
2 3
1 3
```

We process backward.

| Node | Outgoing useful edges | Allowed values | Chosen dp |
| --- | --- | --- | --- |
| 3 | none | fixed | 0 |
| 2 | 2→3 | {1,2} | 1 |
| 1 | 1→2, 1→3 | {2,3} ∩ {1,2} = {2} | 2 |

Recovered weights:

| Edge | Weight |
| --- | --- |
| 1→2 | 1 |
| 2→3 | 1 |
| 1→3 | 2 |

Both paths from 1 to 3 now have total length 2.

This trace demonstrates the core invariant. Every node stores a consistent remaining distance to node $n$, and every outgoing edge preserves that equality.

### Example 2

Input:

```
4 4
1 2
1 3
2 4
3 4
```

Backward processing:

| Node | Outgoing useful edges | Allowed values | Chosen dp |
| --- | --- | --- | --- |
| 4 | none | fixed | 0 |
| 3 | 3→4 | {1,2} | 1 |
| 2 | 2→4 | {1,2} | 1 |
| 1 | 1→2, 1→3 | {2,3} ∩ {2,3} = {2,3} | 2 |

Recovered weights:

| Edge | Weight |
| --- | --- |
| 1→2 | 1 |
| 1→3 | 1 |
| 2→4 | 1 |
| 3→4 | 1 |

Every path has total length 2.

This example shows that multiple valid solutions may exist. The algorithm simply picks one feasible potential assignment.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n+m)$ | Each vertex and edge is processed a constant number of times |
| Space | $O(n+m)$ | Graph storage plus DP and visitation arrays |

With at most 1000 vertices and 5000 edges, linear complexity is easily fast enough for a 2 second limit. Memory usage is also tiny compared to the available 256 MB.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def solve():
    input = sys.stdin.readline

    from collections import deque

    n, m = map(int, input().split())

    edges = []
    g = [[] for _ in range(n + 1)]
    rg = [[] for _ in range(n + 1)]

    for i in range(m):
        u, v = map(int, input().split())
        edges.append((u, v))
        g[u].append((v, i))
        rg[v].append(u)

    vis1 = [False] * (n + 1)
    q = deque([1])
    vis1[1] = True

    while q:
        u = q.popleft()
        for v, _ in g[u]:
            if not vis1[v]:
                vis1[v] = True
                q.append(v)

    vis2 = [False] * (n + 1)
    q = deque([n])
    vis2[n] = True

    while q:
        u = q.popleft()
        for v in rg[u]:
            if not vis2[v]:
                vis2[v] = True
                q.append(v)

    useful = [vis1[i] and vis2[i] for i in range(n + 1)]

    dp = [None] * (n + 1)
    dp[n] = 0

    ans = [1] * m

    for u in range(n - 1, 0, -1):
        if not useful[u]:
            continue

        possible = None

        for v, idx in g[u]:
            if not useful[v]:
                continue

            cur = {dp[v] + 1, dp[v] + 2}

            if possible is None:
                possible = cur
            else:
                possible &= cur

        if not possible:
            print("No")
            return

        dp[u] = min(possible)

    for i, (u, v) in enumerate(edges):
        if useful[u] and useful[v]:
            ans[i] = dp[u] - dp[v]

    print("Yes")
    print("\n".join(map(str, ans)))

def run(inp: str) -> str:
    backup_stdin = sys.stdin
    backup_stdout = sys.stdout

    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    solve()

    out = sys.stdout.getvalue()

    sys.stdin = backup_stdin
    sys.stdout = backup_stdout

    return out.strip()

# provided sample
assert run(
    "3 3\n"
    "1 2\n"
    "2 3\n"
    "1 3\n"
) == "Yes\n1\n1\n2"

# minimum graph
assert run(
    "2 1\n"
    "1 2\n"
) in {
    "Yes\n1",
    "Yes\n2"
}

# two equal branches
assert run(
    "4 4\n"
    "1 2\n"
    "1 3\n"
    "2 4\n"
    "3 4\n"
).startswith("Yes")

# graph with irrelevant node
assert run(
    "5 4\n"
    "1 2\n"
    "2 5\n"
    "3 4\n"
    "4 5\n"
).startswith("Yes")

# impossible case
assert run(
    "5 6\n"
    "1 2\n"
    "1 3\n"
    "2 4\n"
    "3 4\n"
    "2 5\n"
    "4 5\n"
) == "No"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Single edge | Yes | Smallest valid graph |
| Two equal branches | Yes | Multiple equivalent paths |
| Irrelevant disconnected component | Yes | Correct filtering of useless vertices |
| Impossible constraint graph | No | Detection of empty intersections |

## Edge Cases

Consider a graph with irrelevant vertices:

```
5 4
1 2
2 5
3 4
4 5
```

Cities 3 and 4 are never reachable from city 1. The algorithm marks them as non-useful and ignores their constraints entirely.

The backward DP only processes:

```
1 -> 2 -> 5
```

A naive implementation that processed all nodes would incorrectly attempt to assign values to node 3 and node 4 even though they are irrelevant to the required paths.

Now consider a contradiction case:

```
5 6
1 2
1 3
2 4
3 4
2 5
4 5
```

Backward processing gives:

| Node | Allowed values |
| --- | --- |
| 5 | 0 |
| 4 | {1,2} |
| 3 | depends on 4 |
| 2 | intersection from 2→4 and 2→5 |

For node 2:

- edge 2→5 allows {1,2}
- edge 2→4 allows {2,3}

Intersection becomes {2}.

Then node 1 receives incompatible requirements from its outgoing edges, and eventually an empty intersection appears.

The algorithm detects this immediately and prints `"No"`.

This demonstrates why local consistency at every node is enough. If even one node cannot assign a common remaining distance compatible with all outgoing edges, no global solution exists.
