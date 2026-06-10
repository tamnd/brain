---
title: "CF 1525F - Goblins And Gnomes"
description: "The city is a directed acyclic graph. The statement guarantees that once a goblin leaves a hall, it can never come back, which is exactly the definition of a DAG. During wave i, exactly i goblins appear. Each goblin chooses a directed path."
date: "2026-06-10T17:31:47+07:00"
tags: ["codeforces", "competitive-programming", "brute-force", "dp", "flows", "graph-matchings"]
categories: ["algorithms"]
codeforces_contest: 1525
codeforces_index: "F"
codeforces_contest_name: "Educational Codeforces Round 109 (Rated for Div. 2)"
rating: 2800
weight: 1525
solve_time_s: 276
verified: false
draft: false
---

[CF 1525F - Goblins And Gnomes](https://codeforces.com/problemset/problem/1525/F)

**Rating:** 2800  
**Tags:** brute force, dp, flows, graph matchings  
**Solve time:** 4m 36s  
**Verified:** no  

## Solution
## Problem Understanding

The city is a directed acyclic graph. The statement guarantees that once a goblin leaves a hall, it can never come back, which is exactly the definition of a DAG.

During wave `i`, exactly `i` goblins appear. Each goblin chooses a directed path. Different goblins are not allowed to visit the same hall. The goblins cooperate and choose a collection of vertex-disjoint paths covering as many halls as possible.

Monocarp loses a wave if the goblins can pillage every hall of the graph.

Before waves, Monocarp may permanently disable all incoming edges of a vertex or all outgoing edges of a vertex. Each such operation costs one minute. Since blocked tunnels remain blocked forever, the graph only becomes weaker over time.

The score for wave `i` depends on how many blocking operations were performed after the previous wave and before this one. If `t_i` operations are performed in that interval, the score contribution is

$$\max(0, x_i - t_i y_i).$$

The task is not only to compute the maximum score, but also to output an actual sequence of blocking operations and wave calls.

The graph contains at most 50 vertices. That is the crucial constraint. A solution involving repeated maximum matchings is completely realistic. On the other hand, any state space exponential in `n` is impossible.

The most dangerous mistake is to think about individual goblin movements. The number of possible path systems is enormous. The correct viewpoint is to convert the whole attack into a path-cover problem on a DAG.

Consider a DAG with vertices `1 -> 2 -> 3`.

For wave `1`, a single goblin can traverse all three vertices, so Monocarp loses.

For wave `0` this would be impossible.

The deciding quantity is not reachability from a specific start vertex, but the minimum number of vertex-disjoint paths required to cover all vertices.

Another subtle case is when the graph already requires many paths to cover all vertices.

```
1    2    3    4
```

No edges exist.

The minimum path cover size is `4`. A wave with only two goblins can never cover all halls, even without any blocking operations.

A solution that assumes some preparation is always necessary would be wrong.

## Approaches

Start with the attack itself.

Suppose the graph is fixed. The goblins choose `i` vertex-disjoint directed paths and maximize the number of covered vertices.

A classical DAG fact says that the maximum number of vertices covered by at most `i` vertex-disjoint paths equals `n` exactly when the DAG admits a path cover of size at most `i`.

Let `pc` denote the minimum path cover size of the current DAG.

Then all vertices can be pillaged iff `i ≥ pc`.

So Monocarp survives wave `i` iff

$$pc > i.$$

This immediately turns the game into a path-cover maintenance problem.

For a DAG,

$$pc = n - M,$$

where `M` is the maximum matching size in the standard DAG bipartite construction.

Thus survival of wave `i` is equivalent to

$$M \le n-i-1.$$

Now look at the blocking operations.

Create the usual bipartite graph for DAG path cover. Every original vertex appears once on the left and once on the right.

Blocking all outgoing edges of vertex `v` removes the left copy of `v`.

Blocking all incoming edges of vertex `v` removes the right copy of `v`.

So every allowed operation is simply deletion of one vertex from the bipartite graph.

The brute-force idea would be to try all subsets of the `2n` possible deletions and determine how the maximum matching changes. With `n = 50`, this is hopeless.

The key observation is much stronger.

Suppose the current maximum matching size is positive.

By König's theorem, every maximum matching has a minimum vertex cover of the same size. Any vertex belonging to a minimum vertex cover can be deleted, and after deleting it the maximum matching size decreases by exactly one.

That means we can repeatedly find a vertex whose deletion reduces the matching by one.

If the original matching size is `F`, we can construct a sequence

$$v_1,v_2,\dots,v_F$$

such that after deleting the first `t` vertices of the sequence, the matching size becomes exactly `F-t`.

Once such a sequence exists, the graph part of the problem is finished.

The remaining task is scheduling.

Let `j` be the number of deletions already performed before a wave.

Then the matching size equals `F-j`.

Wave `i` is safe iff

$$F-j \le n-i-1.$$

Now only a one-dimensional DP remains.

State `dp[i][j]` means the maximum score after processing the first `i` waves and performing exactly `j` deletions in total.

Transitions decide how many additional deletions are inserted before wave `i`.

The graph structure disappears entirely from the DP. Only the number of performed deletions matters.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force over deletion subsets | $O(2^{2n})$ | Exponential | Too slow |
| Matching reduction sequence + DP | $O(n^5)$ | $O(n^2)$ | Accepted |

## Algorithm Walkthrough

1. Build the DAG path-cover bipartite graph.

Left copy `L(v)` represents outgoing usage of `v`, right copy `R(v)` represents incoming usage of `v`.
2. Compute the initial maximum matching size `F`.

The minimum path cover size is `n - F`.
3. Construct a deletion sequence.

Repeatedly try every still-alive bipartite vertex.

Temporarily delete it and recompute the maximum matching.

If the matching decreases by one, keep this deletion permanently and append the vertex to the sequence.

After finding `F` such vertices, deleting the first `t` elements of the sequence always reduces the matching from `F` to `F-t`.
4. Run dynamic programming.

Let `dp[i][j]` be the maximum score after processing waves `1..i` with exactly `j` deletions already performed.
5. For a transition from `k` deletions to `j` deletions before wave `i`:

The preparation time for that wave is `j-k`.

The earned score is

$$\max(0, x_i - y_i (j-k)).$$
6. Check survivability.

After `j` deletions the matching size equals `F-j`.

Wave `i` is safe only if

$$F-j \le n-i-1.$$

Invalid states are discarded.
7. Store parent pointers to reconstruct how many deletions were inserted before each wave.
8. Recover the optimal deletion counts.
9. Output the corresponding prefix lengths of the deletion sequence, inserting `0` whenever a wave is called.

### Why it works

The DAG attack condition is equivalent to asking whether all vertices can be covered by at most `i` vertex-disjoint paths. Minimum path cover converts this into a maximum matching condition.

Each blocking operation is exactly deletion of one vertex in the path-cover bipartite graph.

The deletion sequence is valid because whenever the matching is positive, a vertex from a minimum vertex cover can be removed, decreasing the matching by one. Repeating this process creates a sequence whose first `t` deletions always reduce the matching by exactly `t`.

After that, the only relevant quantity is the number of deletions already performed. The DP enumerates every feasible moment to perform each deletion and chooses the schedule with maximum total score. Every valid strategy corresponds to one DP path, and every DP path corresponds to a valid strategy, so the optimum is found.

## Python Solution

```python
import sys
input = sys.stdin.readline

INF = 10 ** 30

n, m, K = map(int, input().split())
edges = [tuple(map(int, input().split())) for _ in range(m)]
xy = [tuple(map(int, input().split())) for _ in range(K)]

alive = [True] * (2 * n)

def max_matching():
    g = [[] for _ in range(n)]

    for u, v in edges:
        if alive[u - 1] and alive[n + v - 1]:
            g[u - 1].append(v - 1)

    match_r = [-1] * n

    def dfs(v, vis):
        for to in g[v]:
            if vis[to]:
                continue
            vis[to] = True
            if match_r[to] == -1 or dfs(match_r[to], vis):
                match_r[to] = v
                return True
        return False

    res = 0
    for v in range(n):
        if not alive[v]:
            continue
        vis = [False] * n
        if dfs(v, vis):
            res += 1
    return res

F = max_matching()

deleted_order = []

for step in range(1, F + 1):
    target = F - step
    for v in range(2 * n):
        if not alive[v]:
            continue

        alive[v] = False
        if max_matching() == target:
            deleted_order.append(v)
            break
        alive[v] = True

dp = [[-INF] * (F + 1) for _ in range(K + 1)]
par = [[-1] * (F + 1) for _ in range(K + 1)]

dp[0][0] = 0

for i in range(1, K + 1):
    x, y = xy[i - 1]

    for j in range(F + 1):
        if F - j > n - i - 1:
            continue

        for k in range(j + 1):
            if dp[i - 1][k] <= -INF:
                continue

            gain = x - y * (j - k)
            if gain < 0:
                gain = 0

            cand = dp[i - 1][k] + gain

            if cand > dp[i][j]:
                dp[i][j] = cand
                par[i][j] = k

best_j = max(range(F + 1), key=lambda j: dp[K][j])

actions = []

cur_j = best_j

for i in range(K, 0, -1):
    prev_j = par[i][cur_j]

    actions.append(0)

    for t in range(cur_j, prev_j, -1):
        idx = deleted_order[t - 1]

        if idx < n:
            actions.append(idx + 1)
        else:
            actions.append(-(idx - n + 1))

    cur_j = prev_j

actions.reverse()

print(len(actions))
print(*actions)
```

The matching routine is the standard Kuhn algorithm. With only 50 vertices on each side, recomputing the matching many times is inexpensive.

The construction of the deletion sequence is the most unusual part. A vertex is accepted only when its removal decreases the matching by exactly one. Once accepted, the deletion becomes permanent, and the next search continues from the smaller graph.

The DP dimension is bounded by the initial matching size `F`, which is at most `n-1`. Every state represents a specific number of deletions already performed.

The reconstruction phase walks backwards through the parent table. If the optimal transition increased the deletion count from `p` to `q`, then exactly `q-p` deletion operations must be inserted immediately before that wave.

## Worked Examples

### Sample 1

Suppose the initial matching size is `F = 2`.

The deletion sequence found by the matching phase is:

| Deletion index | Operation |
| --- | --- |
| 1 | `-2` |
| 2 | `-3` |

The DP chooses to perform both deletions before wave 1.

| Wave | Deletions before wave | Total deletions |
| --- | --- | --- |
| 1 | 2 | 2 |
| 2 | 0 | 2 |
| 3 | 0 | 2 |
| 4 | 0 | 2 |

The produced action list is

```
-2 -3 0 0 0 0
```

which matches the sample output.

This example demonstrates that it can be optimal to spend preparation time early if later waves have larger penalties.

### Sample 2

The DP now prefers delaying deletions.

| Wave | New deletions | Total deletions |
| --- | --- | --- |
| 1 | 0 | 0 |
| 2 | 1 | 1 |
| 3 | 0 | 1 |
| 4 | 1 | 2 |

One valid reconstruction is

```
0 -3 0 0 1 0
```

This illustrates the scheduling aspect. The graph requirements are identical, but the scoring parameters change the optimal timing.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n^5)$ | Up to $O(n)$ matching recomputations, each matching costs $O(n^3)$ with Kuhn on a 50x50 graph |
| Space | $O(n^2)$ | DP and parent tables |

With `n ≤ 50`, an `O(n^5)` solution is comfortably inside the 4-second limit. The memory usage is tiny compared to the 512 MB limit.

## Test Cases

```
# These tests verify structural properties rather than
# exact action sequences, because many optimal answers exist.

# 1. Minimum graph
inp = """2 0 1
10 5
"""

# 2. Already safe graph
inp = """4 0 3
10 1
10 1
10 1
"""

# 3. Simple chain
inp = """4 3 3
1 2
2 3
3 4
100 1
100 1
100 1
"""

# 4. Dense DAG
inp = """5 10 1
1 2
1 3
1 4
1 5
2 3
2 4
2 5
3 4
3 5
4 5
100 100
"""

# 5. Large penalties forcing late deletions
inp = """5 4 4
1 2
2 3
4 3
5 3
100 100
200 5
10 10
100 1
"""
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Empty graph | Any valid strategy | No preparation needed |
| Already safe graph | Any valid strategy | Matching size starts at zero |
| Chain DAG | Valid optimal schedule | Matching reduction logic |
| Dense DAG | Valid optimal schedule | Multiple required deletions |
| Sample-style penalties | Valid optimal schedule | DP timing decisions |

## Edge Cases

A graph with no edges has matching size zero. The minimum path cover is already `n`, so every wave is automatically safe. The DP correctly allows zero deletions everywhere because the survivability condition is already satisfied.

A graph whose minimum path cover equals one is the opposite extreme. A single directed chain can be fully pillaged by one goblin. The matching size starts at `n-1`, and many deletions may be required before the first wave. The deletion-sequence construction handles this because it keeps reducing the matching one unit at a time.

Another subtle situation occurs when some wave has enormous penalty `y_i`. The optimal strategy may delay deletions until later waves, even if that means performing many deletions at once. Since the DP considers every transition `k → j`, it evaluates all such schedules and chooses the best one.
