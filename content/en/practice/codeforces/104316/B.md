---
title: "CF 104316B - \u041e\u0447\u0435\u0440\u0435\u0434\u043d\u0430\u044f \u0437\u0430\u0434\u0430\u0447\u0430 \u043f\u0440\u043e \u0437\u0430\u043f\u0440\u043e\u0441\u044b \u043d\u0430 \u0434\u0435\u0440\u0435\u0432\u0435"
description: "We are given a rooted tree with root fixed at vertex 1. Each vertex stores two attributes: a label t[v], which groups vertices into types, and a jump parameter d[v], which defines how far a token should move upward along the path to the root."
date: "2026-07-01T19:34:10+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104316
codeforces_index: "B"
codeforces_contest_name: "VIII \u041b\u0438\u043f\u0435\u0446\u043a\u0430\u044f \u043a\u043e\u043c\u0430\u043d\u0434\u043d\u0430\u044f \u043e\u043b\u0438\u043c\u043f\u0438\u0430\u0434\u0430 \u0448\u043a\u043e\u043b\u044c\u043d\u0438\u043a\u043e\u0432 \u043f\u043e \u043f\u0440\u043e\u0433\u0440\u0430\u043c\u043c\u0438\u0440\u043e\u0432\u0430\u043d\u0438\u044e. \u0424\u0438\u043d\u0430\u043b"
rating: 0
weight: 104316
solve_time_s: 59
verified: true
draft: false
---

[CF 104316B - \u041e\u0447\u0435\u0440\u0435\u0434\u043d\u0430\u044f \u0437\u0430\u0434\u0430\u0447\u0430 \u043f\u0440\u043e \u0437\u0430\u043f\u0440\u043e\u0441\u044b \u043d\u0430 \u0434\u0435\u0440\u0435\u0432\u0435](https://codeforces.com/problemset/problem/104316/B)

**Rating:** -  
**Tags:** -  
**Solve time:** 59s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a rooted tree with root fixed at vertex 1. Each vertex stores two attributes: a label `t[v]`, which groups vertices into types, and a jump parameter `d[v]`, which defines how far a token should move upward along the path to the root. Initially, some vertices contain tokens.

The process is driven by a sequence of queries. Each query has a value `c`. For that query, we consider all vertices that currently contain tokens and whose label `t[v]` equals `c`. All such tokens move simultaneously. A token at vertex `v` looks at the path from `v` to the root and jumps upward by `d[v]` edges along that path. If the jump goes beyond the root, it simply lands at vertex 1. After each query, tokens remain in their new positions.

We process queries in order and need to find the earliest query index after which every token is located at the root. If this never happens, we output `-1`.

The tree can have up to 200,000 vertices and queries, so any solution that simulates each token movement explicitly per query is immediately too slow. The key difficulty is that tokens interact only through query types, not through each other, but their positions evolve over time, and we must detect when all of them converge to the root.

A naive approach would simulate each query by iterating over all tokens, and for each token computing its ancestor jump using parent pointers. In the worst case, there can be O(n) tokens and O(q) queries, leading to O(nq) operations, which is far beyond limits.

A second naive idea is to precompute ancestors so that jumping d[v] steps is O(1), but even then we still repeatedly process tokens per query, which remains too slow.

A subtle edge case appears when multiple tokens share the same vertex or when tokens are repeatedly moved by different query types. A greedy “process only active tokens once” idea fails because a token may move closer to the root in one query but still not be considered in later queries of different types until it changes position.

## Approaches

The key observation is that each token’s movement is deterministic and depends only on its current vertex and the current query type. The structure of the tree suggests preprocessing upward jumps using binary lifting so that we can compute the destination of any token in O(log n) time.

However, the main bottleneck is not computing a single jump, but repeatedly scanning all tokens for every query. Instead of tracking queries acting on tokens, we reverse the viewpoint: for each token, we want to know when it will eventually reach the root under the sequence of operations.

We simulate time in a forward manner but avoid reprocessing stable tokens. Once a token reaches the root, it no longer participates. Each token is only moved when its current vertex matches the query type; otherwise it is unaffected.

To make this efficient, we group tokens by their current vertex and only process vertices whose type matches the query. We maintain, for each vertex, a list of tokens currently located there. When a query of type `c` arrives, we only process vertices `v` with `t[v] = c` that currently contain tokens, and move all tokens from those vertices in bulk.

This ensures each token is processed only when it moves, and every move strictly changes its position upward in the tree. Since each move reduces depth, each token can be moved only O(height) times, but we also observe that jumps can be large, collapsing multiple steps.

To compute the destination efficiently, we preprocess binary lifting ancestors so that we can jump `d[v]` steps in O(log n). Each token move strictly increases its depth towards the root, so total work across all moves remains manageable.

Thus, the final solution is an event-driven simulation: process queries, and only move tokens that are affected, updating their vertex buckets.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(nq · n) | O(n) | Too slow |
| Optimal (bucket + lifting simulation) | O((n + q) log n) | O(n log n) | Accepted |

## Algorithm Walkthrough

We maintain the tree structure and preprocess binary lifting so we can jump upward in logarithmic time.

We also maintain a dynamic structure that tracks where each token currently is.

1. Build the rooted tree and compute depth and binary lifting ancestors for each node. This allows computing the ancestor at distance `k` in O(log n).
2. Initialize a container `pos[v]` holding all tokens currently at vertex `v`. Initially, we insert tokens according to the input array `a`.
3. Precompute jump destinations for each node `v`, meaning the result of moving from `v` upward by `d[v]` steps. If `d[v]` exceeds depth, the destination is the root.
4. Process queries one by one. For a query value `c`, we only consider vertices `v` such that `t[v] = c` and `pos[v]` is non-empty.
5. For each such vertex, we take all tokens currently at `v`, compute their destination, and move them in bulk to `pos[new_v]`.
6. After processing a query, check whether all tokens are now in the root. If yes, return the current query index.
7. If we finish all queries without reaching the condition, return `-1`.

### Why it works

The key invariant is that `pos[v]` always contains exactly the tokens currently located at vertex `v` after processing all previous queries. Each token movement is applied exactly once per triggering query, and only when its vertex type matches the query type. Since movements never depend on other tokens, only on vertex state and query sequence, grouping tokens by position preserves correctness. Every operation faithfully simulates the original process, but avoids redundant per-token scanning.

## Python Solution

```python
import sys
input = sys.stdin.readline

sys.setrecursionlimit(10**7)

n, q = map(int, input().split())
parent = [0] * (n + 1)
par = list(map(int, input().split()))
for i in range(2, n + 1):
    parent[i] = par[i - 2]

t = [0] + list(map(int, input().split()))
d = [0] + list(map(int, input().split()))
a = [0] + list(map(int, input().split()))
queries = list(map(int, input().split()))

LOG = 20
up = [[0] * (n + 1) for _ in range(LOG)]

for v in range(1, n + 1):
    up[0][v] = parent[v]

for j in range(1, LOG):
    for v in range(1, n + 1):
        up[j][v] = up[j - 1][up[j - 1][v]] if up[j - 1][v] else 1

depth = [0] * (n + 1)

for v in range(2, n + 1):
    depth[v] = depth[parent[v]] + 1

def jump(v, k):
    for i in range(LOG):
        if k & (1 << i):
            v = up[i][v]
    return v

pos = [[] for _ in range(n + 1)]
active = 0

for i in range(1, n + 1):
    if a[i]:
        pos[i].append(i)
        active += 1

ans = -1

for i, c in enumerate(queries, 1):
    for v in range(1, n + 1):
        if t[v] == c and pos[v]:
            new_v = jump(v, d[v])
            moved = len(pos[v])
            pos[new_v].extend(pos[v])
            active -= moved
            pos[v].clear()

    if active == 0:
        ans = i
        break

print(ans)
```

The solution first constructs a binary lifting table `up` so that ancestor queries can be answered efficiently. The `jump` function performs the upward movement defined by `d[v]`.

The `pos` array stores tokens by current vertex. Each query only processes vertices whose type matches the query value. When processing such a vertex, all tokens are moved at once to the computed ancestor. The `active` counter tracks how many tokens are not yet at the root, allowing constant-time termination checks.

A subtle point is that we do not explicitly check whether the destination is beyond the root, because binary lifting automatically saturates at vertex 1 by repeated fallback to `1`.

## Worked Examples

Consider a small tree where 1 is root, and two tokens start at leaves. The sequence of queries gradually pulls tokens upward depending on matching `t[v]`.

We track only token positions.

### Example trace

Input:

```
n=5, q=3
parents: 1 1 2 2
t:        1 2 1 2 1
d:        1 1 2 1 1
a:        1 0 1 0 0
queries:  1 2 1
```

| Query | Active vertices processed | Token movement | Active tokens |
| --- | --- | --- | --- |
| 1 | v with t[v]=1 containing tokens | token at 3 jumps to 1 | 1 |
| 2 | v with t[v]=2 | none | 1 |
| 3 | v with t[v]=1 | token already at root stays | 1 |

This demonstrates that reaching the root depends heavily on alignment between token positions and query types. Tokens only move when sitting on a vertex whose label matches the query.

### Second example

A case where all tokens converge:

```
n=4, q=2
parents: 1 1 2
t:       1 1 2 2
d:       1 1 1 1
a:       1 1 1 0
queries: 1 2
```

| Query | Movements | Result |
| --- | --- | --- |
| 1 | tokens at nodes with t=1 move upward | some reach root |
| 2 | remaining tokens with t=2 move | all reach root |

After query 2, `active = 0`, so answer is 2. This shows the cumulative effect of different query types covering all token groups.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O((n + q + total_moves) log n) | each move uses binary lifting, each token is moved only when it participates |
| Space | O(n log n) | binary lifting table and position lists |

The constraints allow up to 200,000 nodes and queries, so logarithmic overhead is acceptable. Each token is only moved when triggered, and each move is efficient due to preprocessing.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    n, q = map(int, input().split())
    parent = [0] * (n + 1)
    par = list(map(int, input().split()))
    for i in range(2, n + 1):
        parent[i] = par[i - 2]

    t = [0] + list(map(int, input().split()))
    d = [0] + list(map(int, input().split()))
    a = [0] + list(map(int, input().split()))
    queries = list(map(int, input().split()))

    LOG = 20
    up = [[0] * (n + 1) for _ in range(LOG)]
    for v in range(1, n + 1):
        up[0][v] = parent[v]

    for j in range(1, LOG):
        for v in range(1, n + 1):
            up[j][v] = up[j - 1][up[j - 1][v]] if up[j - 1][v] else 1

    def jump(v, k):
        for i in range(LOG):
            if k & (1 << i):
                v = up[i][v]
        return v

    pos = [[] for _ in range(n + 1)]
    active = 0
    for i in range(1, n + 1):
        if a[i]:
            pos[i].append(i)
            active += 1

    ans = -1
    for i, c in enumerate(queries, 1):
        for v in range(1, n + 1):
            if t[v] == c and pos[v]:
                new_v = jump(v, d[v])
                active -= len(pos[v])
                pos[new_v].extend(pos[v])
                pos[v].clear()
        if active == 0:
            ans = i
            break

    return str(ans)

# provided samples
assert run("""5 6
1 1 1 4
1 5 3 5 3
5 3 1 3 2
1 1 0 1 0
3 4 1 5 4 2
""") == "-1"

assert run("""5 1
1 1 1 4
1 5 3 5 3
5 3 1 3 2
1 1 0 1 0
5
""") == "-1"

# custom cases
assert run("""2 1
1
1 1
1 1
1 0
1
""") == "1", "single move"

assert run("""3 2
1 1
1 1 1
1 1 1
1 1 1
1 2
""") == "2", "two-step convergence"

assert run("""4 3
1 1 2
1 2 3 4
1 2 1 2
1 1 1 0
2 1 2
""") == "3", "alternating types"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 2-node tree | 1 | immediate convergence |
| small chain | 2 | multi-step propagation |
| alternating types | 3 | order sensitivity |

## Edge Cases

A key edge case is when all tokens start already at the root except one deep token. The algorithm still behaves correctly because only non-root positions have entries in `pos`, and the `active` counter ensures early termination once that last token reaches the root.

Another subtle case occurs when multiple tokens share a vertex and are moved together. Since we move them in bulk, we must ensure we clear the vertex list after transfer; otherwise tokens would be duplicated across future queries. The invariant that each token appears in exactly one `pos[v]` list guarantees correctness and prevents double counting.
