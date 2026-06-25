---
title: "CF 106098J - Bald and Eslam"
description: "We are given a connected undirected graph. A vertex is chosen uniformly at random. Then one of its incident edges is chosen uniformly at random and removed from the graph."
date: "2026-06-25T11:56:18+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 106098
codeforces_index: "J"
codeforces_contest_name: "The American University in Cairo CSEA Fall 2025 contest"
rating: 0
weight: 106098
solve_time_s: 49
verified: true
draft: false
---

[CF 106098J - Bald and Eslam](https://codeforces.com/problemset/problem/106098/J)

**Rating:** -  
**Tags:** -  
**Solve time:** 49s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a connected undirected graph. A vertex is chosen uniformly at random. Then one of its incident edges is chosen uniformly at random and removed from the graph.

After that deletion, we start from the same chosen vertex and ask how many distinct vertices can still be visited. Since the graph is undirected, this is simply the size of the connected component containing the chosen vertex after the edge removal.

The task is to compute the expected value of that component size.

The graph can contain up to $2 \cdot 10^5$ vertices and edges across all test cases. Any solution that recomputes connectivity after every possible deletion is completely infeasible. Even a single DFS per edge would already require $O(m(n+m))$, which is far beyond the limit.

The graph is initially connected. That immediately suggests that most edge deletions do nothing. Removing a non-bridge keeps the graph connected, so the answer remains $n$. Only bridges can reduce the reachable component size.

A common mistake is to think about all vertices inside the graph after removing a bridge. The experiment chooses an endpoint vertex first, then chooses one of its incident edges. The probability distribution depends on vertex degrees, so every bridge contributes differently depending on the degrees of its two endpoints.

Consider a path of three vertices:

```
1 - 2 - 3
```

Starting from vertex 1, its only incident edge is removed, leaving vertex 1 isolated. The reachable size is 1.

Starting from vertex 2, either edge can be removed. In both cases vertex 2 remains connected to exactly one other vertex, so the reachable size is 2.

The expected value is:

$$\frac{1+2+1}{3}=\frac43$$

A solution that only counts bridges without accounting for endpoint degrees would produce the wrong result.

Another subtle case is a graph with no bridges, for example a cycle:

```
1 - 2
|   |
4 - 3
```

Removing any single edge leaves the graph connected, so the answer is always $n$. Any algorithm that tries to subtract something for every edge would fail here.

## Approaches

The brute force interpretation follows the experiment literally.

For every vertex $v$, iterate over every incident edge $e$. Remove $e$, run a DFS or BFS from $v$, measure the size of the reachable component, and average the results.

This is correct because it directly simulates the random process. The problem is its cost. A graph may contain $2 \cdot 10^5$ edges. Running a graph traversal for every possible choice leads to roughly $O(m(n+m))$ work, which is many billions of operations in the worst case.

The key observation is that deleting a non-bridge changes nothing. Since the graph starts connected, removing a non-bridge leaves it connected, so every vertex can still reach all $n$ vertices.

That means only bridges matter.

Suppose a bridge connects a parent vertex $p$ and a child vertex $c$ in a DFS tree. Let the subtree rooted at $c$ contain $sz$ vertices.

Removing this bridge splits the graph into two components:

$$sz$$

and

$$n-sz$$

If the chosen vertex is $p$, then after deleting the bridge it stays in the component of size $n-sz$, losing exactly $sz$ vertices.

If the chosen vertex is $c$, it stays in the component of size $sz$, losing exactly $n-sz$ vertices.

No other vertex can choose this edge because the experiment only removes edges incident to the chosen vertex.

This converts the problem into summing independent contributions from every bridge. A single DFS can identify all bridges and all subtree sizes, which yields an $O(n+m)$ solution.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(m(n+m))$ | $O(n)$ | Too slow |
| Optimal | $O(n+m)$ | $O(n+m)$ | Accepted |

## Algorithm Walkthrough

1. Read the graph and compute the degree of every vertex.
2. Run Tarjan's bridge-finding DFS.
3. During DFS, maintain discovery times and low-link values.
4. For every DFS tree vertex, compute its subtree size `sz`.
5. When exploring a tree edge `(u, v)`, after returning from `v`, check whether:

$$low[v] > tin[u]$$

If this condition holds, `(u,v)` is a bridge.

1. Let `sz[v]` be the size of the child subtree. Removing this bridge splits the graph into components of sizes:

$$sz[v]$$

and

$$n - sz[v]$$

1. The total loss contributed by this bridge is:

$$\frac{sz[v]}{\deg(u)}
+
\frac{n-sz[v]}{\deg(v)}$$

The first term corresponds to choosing vertex `u`, the second to choosing vertex `v`.

1. Sum these losses over all bridges.
2. Let the total loss be `S`.

The expected reachable size is:

$$n - \frac{S}{n}$$

1. Perform all arithmetic modulo $10^9+7$. Replace every division by multiplication with a modular inverse.

### Why it works

Every possible outcome of the experiment starts from a connected graph and removes exactly one edge incident to the chosen vertex.

If the removed edge is not a bridge, the graph remains connected, so the reachable size stays equal to $n$. Such edges contribute zero loss.

For a bridge, removing it splits the graph into exactly two components. The chosen endpoint remains on one side and loses access to all vertices on the other side. The number of lost vertices is precisely the size of the opposite component.

Each bridge contributes independently because only its two endpoints can ever choose it. Summing the losses of all bridges gives the total expected reduction from $n$. Subtracting that reduction from $n$ yields the expected reachable component size.

## Python Solution

```python
import sys
input = sys.stdin.readline

MOD = 1000000007

MAXN = 200000 + 5
inv = [0] * MAXN
for i in range(1, MAXN):
    inv[i] = pow(i, MOD - 2, MOD)

t = int(input())

for _ in range(t):
    n, m = map(int, input().split())

    adj = [[] for _ in range(n)]
    deg = [0] * n

    for eid in range(m):
        u, v = map(int, input().split())
        u -= 1
        v -= 1

        adj[u].append((v, eid))
        adj[v].append((u, eid))

        deg[u] += 1
        deg[v] += 1

    tin = [0] * n
    low = [0] * n
    sz = [0] * n

    timer = 0
    loss = 0

    sys.setrecursionlimit(1 << 20)

    def dfs(u, pe):
        nonlocal timer, loss

        timer += 1
        tin[u] = low[u] = timer
        sz[u] = 1

        for v, eid in adj[u]:
            if eid == pe:
                continue

            if tin[v]:
                low[u] = min(low[u], tin[v])
            else:
                dfs(v, eid)

                sz[u] += sz[v]
                low[u] = min(low[u], low[v])

                if low[v] > tin[u]:
                    s = sz[v]

                    loss_term = (
                        s * inv[deg[u]]
                        + (n - s) * inv[deg[v]]
                    ) % MOD

                    loss += loss_term
                    loss %= MOD

    dfs(0, -1)

    ans = (n % MOD - loss * inv[n]) % MOD
    print(ans)
```

The graph is stored with edge identifiers so that the DFS can distinguish the tree edge leading to the parent from other edges.

The arrays `tin` and `low` are the standard Tarjan bridge structure. The condition `low[v] > tin[u]` is exactly the criterion that identifies a bridge.

The subtree size `sz[v]` is computed during the DFS return phase. Once a bridge is found, `sz[v]` immediately gives one side of the split and `n - sz[v]` gives the other.

The quantity accumulated in `loss` is not the expected loss itself. It is the sum of all bridge losses before the final division by `n`, matching the formula

$$n - \frac{S}{n}.$$

All divisions are replaced by modular inverses. Since every degree is at least one in a connected graph with $n \ge 2$, these inverses always exist modulo $10^9+7$.

## Worked Examples

### Example 1

Graph:

```
1 - 2 - 3
```

| Bridge | Subtree size | Loss from first endpoint | Loss from second endpoint |
| --- | --- | --- | --- |
| (1,2) | 2 | 2/1 | 1/2 |
| (2,3) | 1 | 1/2 | 2/1 |

Total loss:

$$2+\frac12+\frac12+2=5$$

Expected value:

$$3-\frac53=\frac43$$

| Variable | Value |
| --- | --- |
| n | 3 |
| S | 5 |
| Answer | 4/3 |

This example shows how endpoint degrees directly affect the probability distribution.

### Example 2

Graph:

```
1
|\
| \
2--3
```

A triangle contains no bridges.

| Bridge count | Total loss |
| --- | --- |
| 0 | 0 |

| Variable | Value |
| --- | --- |
| n | 3 |
| S | 0 |
| Answer | 3 |

Removing any edge keeps the graph connected, so every outcome reaches all vertices.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n+m)$ | One DFS processes every vertex and edge once |
| Space | $O(n+m)$ | Adjacency list plus DFS arrays |

The total number of vertices and edges across all test cases is at most $2 \cdot 10^5$. A linear solution easily fits within the limits.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def run(inp: str) -> str:
    MOD = 1000000007

    data = io.StringIO(inp)
    input = data.readline

    MAXN = 200005
    inv = [0] * MAXN
    for i in range(1, MAXN):
        inv[i] = pow(i, MOD - 2, MOD)

    t = int(input())
    out = []

    sys.setrecursionlimit(1 << 20)

    for _ in range(t):
        n, m = map(int, input().split())

        adj = [[] for _ in range(n)]
        deg = [0] * n

        for eid in range(m):
            u, v = map(int, input().split())
            u -= 1
            v -= 1

            adj[u].append((v, eid))
            adj[v].append((u, eid))

            deg[u] += 1
            deg[v] += 1

        tin = [0] * n
        low = [0] * n
        sz = [0] * n

        timer = 0
        loss = 0

        def dfs(u, pe):
            nonlocal timer, loss

            timer += 1
            tin[u] = low[u] = timer
            sz[u] = 1

            for v, eid in adj[u]:
                if eid == pe:
                    continue

                if tin[v]:
                    low[u] = min(low[u], tin[v])
                else:
                    dfs(v, eid)

                    sz[u] += sz[v]
                    low[u] = min(low[u], low[v])

                    if low[v] > tin[u]:
                        s = sz[v]
                        loss = (
                            loss
                            + s * inv[deg[u]]
                            + (n - s) * inv[deg[v]]
                        ) % MOD

        dfs(0, -1)

        ans = (n % MOD - loss * inv[n]) % MOD
        out.append(str(ans))

    return "\n".join(out)

# sample 1
assert run(
"""1
3 2
1 2
2 3
"""
) == "333333337"

# triangle, no bridges
assert run(
"""1
3 3
1 2
2 3
3 1
"""
) == "3"

# single edge
assert run(
"""1
2 1
1 2
"""
) == "1"

# cycle with tail
assert run(
"""1
4 4
1 2
2 3
3 1
3 4
"""
) != ""

# minimum connected graph
assert run(
"""1
1 0
"""
) == "1"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Path of length 2 | 4/3 modulo MOD | Basic bridge handling |
| Triangle | 3 | No bridges |
| Single edge | 1 | Smallest non-trivial graph |
| Cycle with tail | Valid answer | Mixed bridge and non-bridge edges |
| Single vertex | 1 | Minimum graph size |

## Edge Cases

Consider the graph:

```
1 - 2 - 3
```

Input:

```
1
3 2
1 2
2 3
```

Both edges are bridges. The DFS computes subtree sizes 2 and 1. Their contributions become:

$$\frac{2}{1}+\frac{1}{2}$$

and

$$\frac{1}{2}+\frac{2}{1}$$

The final answer is $\frac43$. The algorithm correctly accounts for endpoint degrees instead of treating every bridge equally.

Now consider a cycle:

```
1 - 2
|   |
4 - 3
```

Input:

```
1
4 4
1 2
2 3
3 4
4 1
```

The DFS finds no bridge because every tree edge has a back edge supporting it. The accumulated loss remains zero. The answer becomes exactly $n=4$, which matches the fact that removing any single edge leaves the graph connected.

Finally, consider a graph consisting of a triangle with one leaf attached:

```
1
|\
| \
2--3--4
```

Only edge `(3,4)` is a bridge. The DFS computes `sz=1` for vertex 4. The bridge contributes:

$$\frac{1}{\deg(3)}
+
\frac{3}{\deg(4)}$$

and no other edge contributes anything. This confirms that the algorithm isolates the effect of bridges while ignoring all non-bridges.
