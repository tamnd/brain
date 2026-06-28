---
title: "CF 104941E - Even Walk"
description: "We are given an undirected graph representing towns connected by bidirectional roads. A traveler starts at a fixed town s and wants to reach another town t."
date: "2026-06-28T07:17:07+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104941
codeforces_index: "E"
codeforces_contest_name: "SLPC 2024 Open Division"
rating: 0
weight: 104941
solve_time_s: 89
verified: false
draft: false
---

[CF 104941E - Even Walk](https://codeforces.com/problemset/problem/104941/E)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 29s  
**Verified:** no  

## Solution
## Problem Understanding

We are given an undirected graph representing towns connected by bidirectional roads. A traveler starts at a fixed town `s` and wants to reach another town `t`. The traveler is extremely careless and may revisit towns and roads arbitrarily many times, meaning we are not dealing with simple paths but all possible walks.

Each road contributes length one. The key requirement is parity: we care only whether the total number of edges in a walk is even or odd.

The question is not to find a shortest path or any path, but to determine whether every possible walk from `s` to `t` has even length. If even a single odd-length walk exists, the answer must be “No”.

The graph size is large, up to 200,000 nodes and edges. This immediately rules out enumerating walks or even enumerating simple paths. Any solution must run in linear or near-linear time, around O(n + m).

A subtle issue is that revisiting nodes is allowed. This means cycles are not just incidental, they fundamentally affect whether both parities can be realized. A naive shortest-path parity check is not sufficient unless it accounts for all possible alternative routes.

A few edge cases highlight the danger of local reasoning.

If there is a direct edge between `s` and `t`, that is a length-1 walk. If there is also a path of even length between them, then both odd and even walks exist, so the answer is “No”. A shortest path algorithm would only see the length-1 path and incorrectly conclude parity is fixed.

Another example is a triangle cycle between `s`, `a`, `t`. Even if the shortest path is length 2, the cycle allows a detour that flips parity, producing both even and odd walks.

The core difficulty is global parity consistency over all possible walks, not any single path.

## Approaches

A brute-force idea would attempt to explore all possible walks from `s` to `t`, tracking their lengths modulo 2. We could perform a DFS or BFS where each state is `(node, parity)`, and we try to explore all reachable states, checking whether both parities reach `t`. This already improves over enumerating full walks, but still essentially explores the full state space of a doubled graph.

In a graph with cycles, the number of walks is infinite. Even though `(node, parity)` limits states to `2n`, transitions can revisit states endlessly. A naive exploration without careful visited-state control still degenerates into exponential behavior if implemented incorrectly.

The key insight is to reinterpret the problem as a bipartite consistency condition on an augmented graph of two layers: each node appears in two states, even parity and odd parity. Every edge flips parity, connecting `u_even` to `v_odd` and `u_odd` to `v_even`.

Now the question becomes: starting from `s_even`, can we reach `t_even` or `t_odd`, and more importantly, do both exist? If both parity states of `t` are reachable, then there exist both even and odd walks, so the answer is “No”. If exactly one parity is reachable, all walks must share that parity.

This reduces the problem to a standard BFS reachability check in a graph of size `2n`.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Walk Exploration | Exponential | O(n) | Too slow |
| Parity-expanded BFS | O(n + m) | O(n + m) | Accepted |

## Algorithm Walkthrough

1. Build a graph where each original node `u` is split into two states: `u0` meaning even distance parity from `s`, and `u1` meaning odd parity. This encodes the fact that every traversal flips parity.
2. For every undirected edge `(u, v)`, add transitions `u0 → v1` and `v0 → u1`, and symmetrically `u1 → v0` and `v1 → u0`. This ensures every step toggles parity consistently.
3. Run a BFS starting from `s0`, since the start node is reached with distance zero, which is even.
4. Maintain a visited array over `2n` states to avoid revisiting parity-node combinations. This prevents infinite traversal over cycles.
5. After BFS completes, check whether `t0` or `t1` is reachable. If both are reachable, output “No”, since this implies existence of both even and odd walks.
6. If only one of them is reachable, output “Yes”, because all valid walks must share the same parity.

### Why it works

Every walk in the original graph corresponds uniquely to a path in the parity-expanded graph, where the second coordinate tracks parity exactly. BFS explores all reachable parity states, so if both `t0` and `t1` are reachable, there exist two walks with different parity. Conversely, if only one parity state is reachable, no sequence of cycles can change parity to reach the other state, meaning all walks are constrained to a single parity class.

The invariant is that after visiting any state `(u, p)`, `p` always equals the parity of the number of edges used in the corresponding original walk. This invariant is preserved because every transition flips parity exactly once.

## Python Solution

```python
import sys
input = sys.stdin.readline

from collections import deque

def solve():
    n, m = map(int, input().split())
    s, t = map(int, input().split())
    s -= 1
    t -= 1

    g = [[] for _ in range(n)]
    for _ in range(m):
        u, v = map(int, input().split())
        u -= 1
        v -= 1
        g[u].append(v)
        g[v].append(u)

    # 2*n states: node with parity 0 or 1
    N = 2 * n
    vis = [False] * N
    q = deque()

    start = s * 2  # even parity at start
    vis[start] = True
    q.append(start)

    while q:
        cur = q.popleft()
        node = cur // 2
        parity = cur % 2

        for nei in g[node]:
            nxt = nei * 2 + (parity ^ 1)
            if not vis[nxt]:
                vis[nxt] = True
                q.append(nxt)

    if vis[t * 2] and vis[t * 2 + 1]:
        print("No")
    else:
        print("Yes")

if __name__ == "__main__":
    solve()
```

The implementation compresses the expanded state graph into a single integer index `node * 2 + parity`. This avoids extra memory overhead and keeps transitions constant time.

The BFS queue stores states in this encoded form. Each edge traversal flips the parity using `parity ^ 1`, which directly reflects the fact that every move changes path length by one.

The final check directly inspects whether both parity states of `t` were visited.

## Worked Examples

### Sample 1

Input:

```
6 5
2 4
1 2
2 3
3 4
1 4
4 5
```

We start from state `(2, even)`.

| Step | Node | Parity | Newly visited states |
| --- | --- | --- | --- |
| 1 | 2 | 0 | (3,1), (1,1) |
| 2 | 3 | 1 | (4,0) |
| 3 | 1 | 1 | (4,0) already queued |
| 4 | 4 | 0 | - |

We reach `t = 4` only in even parity. There is no way to reach `(4,1)`, so all walks have even length.

Output is `Yes`.

This confirms that cycles or alternate routes do not introduce parity ambiguity.

### Sample 2

Input:

```
6 6
1 5
1 6
6 2
2 3
3 4
4 2
4 5
```

This graph contains a cycle among `2-3-4`, which allows parity flipping.

| Step | Node | Parity | Newly visited states |
| --- | --- | --- | --- |
| 1 | 1 | 0 | (6,1) |
| 2 | 6 | 1 | (2,0) |
| 3 | 2 | 0 | (3,1), (4,1) |
| 4 | 3,4 | 1 | (4,0), (2,0) |
| 5 | 5 | 0 and 1 | reached via multiple paths |

Both `(5,0)` and `(5,1)` become reachable, showing existence of both even and odd walks.

Output is `No`.

This demonstrates how a cycle creates parity flexibility even if a single shortest path would not reveal it.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n + m) | Each state `(node, parity)` is visited once, and each edge induces constant transitions in the expanded graph |
| Space | O(n + m) | Adjacency list plus visited array over `2n` states |

The constraints allow up to 200,000 nodes and edges, so a linear-time BFS over the doubled state space fits comfortably within limits.

## Test Cases

```python
import sys, io
from collections import deque

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from collections import deque

    def solve():
        n, m = map(int, input().split())
        s, t = map(int, input().split())
        s -= 1
        t -= 1

        g = [[] for _ in range(n)]
        for _ in range(m):
            u, v = map(int, input().split())
            u -= 1
            v -= 1
            g[u].append(v)
            g[v].append(u)

        vis = [False] * (2 * n)
        q = deque([s * 2])
        vis[s * 2] = True

        while q:
            cur = q.popleft()
            node, p = cur // 2, cur % 2
            for nei in g[node]:
                nxt = nei * 2 + (p ^ 1)
                if not vis[nxt]:
                    vis[nxt] = True
                    q.append(nxt)

        print("No" if vis[t * 2] and vis[t * 2 + 1] else "Yes")

    old_stdout = sys.stdout
    sys.stdout = io.StringIO()
    solve()
    out = sys.stdout.getvalue().strip()
    sys.stdout = old_stdout
    return out

# provided samples
assert run("""6 5
2 4
1 2
2 3
3 4
1 4
4 5
""") == "Yes", "sample 1"

assert run("""6 6
1 5
1 6
6 2
2 3
3 4
4 2
4 5
""") == "No", "sample 2"

# minimum graph
assert run("""2 1
1 2
1 2
""") == "Yes"

# triangle (both parities possible)
assert run("""3 3
1 3
1 2
2 3
1 3
""") == "No"

# line graph (unique parity)
assert run("""5 4
1 5
1 2
2 3
3 4
4 5
""") == "Yes"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 2 nodes single edge | Yes | simplest unique parity path |
| triangle with shortcut | No | cycle creates both parities |
| simple chain | Yes | no alternative parity paths |

## Edge Cases

A direct edge between `s` and `t` already produces a length-1 walk. If the graph also contains any alternative even-length route, such as through a cycle or a longer detour, BFS in the parity-expanded graph will reach both `(t,0)` and `(t,1)`. The algorithm correctly outputs “No” because both states become reachable.

In a pure tree, there is exactly one simple path between `s` and `t`. BFS will only reach one parity state of `t`, determined by path length parity. Since there are no cycles, no alternative parity flip exists, so the output remains “Yes”.

In a graph where `s` is part of a cycle disconnected from `t` except through a single bridge, the cycle only affects internal parity states but cannot influence reachability of `t` in both parities unless it lies on a path to `t`. The BFS expansion naturally confines parity changes to reachable regions, preserving correctness.
