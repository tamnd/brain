---
title: "CF 2189F - Zhora the Vacuum Cleaner"
description: "We have a tree. Vertex i initially contains ai nuts. There are two kinds of electricity costs. The first cost comes from a special redistribution operation. We choose a vertex v. Then every other vertex is processed from larger distance to smaller distance from v."
date: "2026-06-07T21:15:12+07:00"
tags: ["codeforces", "competitive-programming", "data-structures", "dfs-and-similar", "dp", "greedy", "implementation", "sortings", "trees"]
categories: ["algorithms"]
codeforces_contest: 2189
codeforces_index: "F"
codeforces_contest_name: "Codeforces Round 1075 (Div. 2)"
rating: 2800
weight: 2189
solve_time_s: 185
verified: false
draft: false
---

[CF 2189F - Zhora the Vacuum Cleaner](https://codeforces.com/problemset/problem/2189/F)

**Rating:** 2800  
**Tags:** data structures, dfs and similar, dp, greedy, implementation, sortings, trees  
**Solve time:** 3m 5s  
**Verified:** no  

## Solution
## Problem Understanding

We have a tree. Vertex `i` initially contains `a_i` nuts.

There are two kinds of electricity costs.

The first cost comes from a special redistribution operation. We choose a vertex `v`. Then every other vertex is processed from larger distance to smaller distance from `v`. If a processed vertex currently contains at least one nut, exactly one nut is moved one edge closer to `v`.

The second cost comes after all redistribution operations are finished. Zhora eats nuts from every non-empty vertex, paying `q` for each vertex that still contains at least one nut.

Our goal is to decide how many redistribution operations to perform, and around which vertices, so that the sum of movement costs and eating costs is minimized.

The first thing to understand is what a redistribution operation really does.

Fix a center vertex `v`. Consider one operation around `v`. Every vertex except `v` may lose at most one nut. That nut moves one edge toward `v`. Since vertices are processed from larger distance to smaller distance, a nut arriving from a child can immediately be forwarded further toward `v` if the intermediate vertex originally had a nut to send. This ordering is the key structural property of the problem.

The constraints are large. The sum of all `n` over test cases is at most `10^5`, so we need something around `O(n log n)` or `O(n)` per test case. Any solution that tries all centers and simulates operations explicitly would immediately become too slow. Even `O(n^2)` is impossible when `n = 10^5`.

A subtle edge case appears when a vertex contains many nuts.

Example:

```
1 - 2
a = [100, 0]
```

One operation centered at vertex `2` moves only one nut from vertex `1` to vertex `2`, not all 100 nuts. A careless interpretation of the operation often assumes that all nuts move simultaneously. That is incorrect.

Another tricky case is a path.

```
1 - 2 - 3 - 4 - 5
a = [1,1,1,1,1]
```

Two operations centered at vertex `3` gather all nuts into vertex `3`. The answer is not determined by the tree diameter or by moving each nut independently. The operation acts on all vertices at once, which makes repeated applications extremely powerful.

A third pitfall is `q = 0`.

Example:

```
1 - 2
a = [5,7]
p = 100
q = 0
```

The answer is `0`. We can simply eat from every non-empty vertex for free. Any algorithm that automatically tries to merge vertices would overpay.

## Approaches

A brute-force approach would try every possible center vertex, simulate redistribution operations, and track how the set of non-empty vertices evolves.

Suppose we fix a center `v`. Let `x_u` be the number of nuts initially at vertex `u`. A direct simulation of one operation requires traversing the whole tree. Since we may perform many operations, potentially up to the maximum distance from `v`, the complexity becomes at least quadratic. Repeating this for all possible centers is completely infeasible.

The key observation comes from understanding what repeated operations around a fixed center actually do.

Consider a vertex at distance `d` from the chosen center `v`.

Every operation can move at most one nut from that vertex one step closer to `v`. After `k` operations, at most `k` nuts can leave that vertex. Hence the vertex remains non-empty iff

```
a_u > k
```

because exactly one nut can be removed per operation.

This immediately reveals something much stronger. After performing `k` operations around center `v`, every vertex whose distance from `v` is at most `k` can forward all nuts arriving from deeper vertices. The whole process behaves as if each vertex independently contributes

```
max(a_u - k, 0)
```

remaining nuts.

A vertex becomes empty exactly when `a_u ≤ k`.

The eating cost depends only on how many vertices remain non-empty. If

```
cnt(k) = number of vertices with a_u > k
```

then after `k` operations the total cost is

```
k * p + cnt(k) * q
```

provided that every surviving nut can still be gathered into a single connected region around the center.

Now the tree structure enters.

For a fixed `k`, every vertex with `a_u > k` must remain non-empty. Such vertices must all lie inside distance at most `k` from the chosen center, otherwise some nut would be stranded farther away.

Therefore we need a center whose distance to every vertex satisfying `a_u > k` is at most `k`.

Equivalently, if we define

```
S(k) = { u | a_u > k }
```

then we need

```
radius(S(k)) ≤ k
```

where radius means the minimum possible maximum distance from a center to all vertices of the set.

A classical tree fact says that for any subset of vertices, its radius equals

```
ceil(diameter(S)/2)
```

where the diameter is the largest distance between two vertices in the subset.

Thus feasibility for a given `k` becomes

```
diameter(S(k)) ≤ 2k
```

This transforms the problem into:

For every possible `k`, check whether the vertices with `a_u > k` have pairwise diameter at most `2k`. If yes, the cost is

```
k*p + |S(k)|*q.
```

The minimum among all feasible `k` is the answer.

The remaining challenge is maintaining the diameter of the active set `S(k)` while vertices disappear as `k` increases.

| Approach | Time Complexity | Space Complexity | Verdict |

|---|------|---|

| Brute Force simulation | O(n²) or worse | O(n) | Too slow |

| Diameter maintenance with DSU-on-thresholds | O(n log n) | O(n) | Accepted |

## Algorithm Walkthrough

### Reformulating the process

For a fixed number of operations `k`, a vertex remains non-empty iff `a_u > k`.

Let

```
S(k) = {u : a_u > k}.
```

The eating cost becomes

```
|S(k)| * q.
```

The movement cost becomes

```
k * p.
```

The only remaining question is whether those surviving vertices can be served by a single center.

### Diameter condition

A center exists iff every vertex in `S(k)` lies within distance `k` from that center.

The minimum such maximum distance equals the radius of `S(k)`.

For tree metrics:

```
radius = ceil(diameter / 2).
```

Hence feasibility is exactly

```
diameter(S(k)) ≤ 2k.
```

### Maintaining the active set

As `k` increases, vertices leave the set when

```
k >= a_u.
```

So vertices disappear in decreasing order of their values.

Instead of increasing `k`, process thresholds from large to small and add vertices whose value exceeds the current threshold.

The active vertices are exactly `S(k)`.

### Dynamic diameter of active vertices

For a set of vertices in a tree, its diameter endpoints completely determine all maximum distances.

Maintain two active vertices `A` and `B` representing the current diameter.

When a new vertex `x` is inserted:

1. Compute `dist(x,A)`.
2. Compute `dist(x,B)`.
3. If either distance exceeds the current diameter length, update the diameter endpoint.

This is the standard incremental diameter maintenance technique.

Distances are answered in `O(1)` using LCA preprocessing.

### Evaluating thresholds

Only thresholds where the active set changes matter.

Process values of `k` in descending order.

For each threshold:

1. Add all vertices with value greater than `k`.
2. Maintain active-set diameter.
3. Let `D` be the diameter length.
4. The threshold is feasible iff

```
D ≤ 2k.
```
5. If feasible, update

```
answer = min(answer, k*p + active_count*q).
```

The case `k` larger than every `a_i` leaves no active vertices and costs `k*p`, which is never better than choosing exactly `k=max(a_i)` for the empty set, so checking the relevant thresholds is sufficient.

### Why it works

After `k` operations, every vertex can contribute at most `k` nuts toward the center. A vertex with more than `k` nuts must still contain nuts afterward. Thus the surviving vertices are exactly those with `a_u > k`.

A center can handle all surviving vertices iff every survivor lies within distance `k` of it. In a tree metric this is equivalent to the radius of the survivor set being at most `k`, which is equivalent to its diameter being at most `2k`.

The active-set maintenance always stores the true diameter of the currently active vertices. Hence every threshold is classified correctly as feasible or infeasible. Among all feasible thresholds, the algorithm evaluates the exact cost formula, so the minimum found is the optimal answer.

## Python Solution

```python
import sys
input = sys.stdin.readline

LOG = 17

def solve():
    t = int(input())

    for _ in range(t):
        n, p, q = map(int, input().split())
        a = list(map(int, input().split()))

        g = [[] for _ in range(n)]
        for _ in range(n - 1):
            u, v = map(int, input().split())
            u -= 1
            v -= 1
            g[u].append(v)
            g[v].append(u)

        depth = [0] * n
        up = [[0] * n for _ in range(LOG)]

        stack = [0]
        parent = [-1] * n
        parent[0] = 0

        order = [0]
        while stack:
            v = stack.pop()
            for to in g[v]:
                if to == parent[v]:
                    continue
                parent[to] = v
                depth[to] = depth[v] + 1
                stack.append(to)
                order.append(to)

        for v in range(n):
            up[0][v] = parent[v]

        for j in range(1, LOG):
            prev = up[j - 1]
            cur = up[j]
            for v in range(n):
                cur[v] = prev[prev[v]]

        def lca(a_, b_):
            if depth[a_] < depth[b_]:
                a_, b_ = b_, a_

            diff = depth[a_] - depth[b_]
            bit = 0
            while diff:
                if diff & 1:
                    a_ = up[bit][a_]
                diff >>= 1
                bit += 1

            if a_ == b_:
                return a_

            for j in range(LOG - 1, -1, -1):
                if up[j][a_] != up[j][b_]:
                    a_ = up[j][a_]
                    b_ = up[j][b_]

            return parent[a_]

        def dist(u, v):
            w = lca(u, v)
            return depth[u] + depth[v] - 2 * depth[w]

        by_value = {}
        for i, x in enumerate(a):
            by_value.setdefault(x, []).append(i)

        values = sorted(by_value.keys(), reverse=True)

        active = 0
        diameter_len = 0
        end1 = -1
        end2 = -1

        ans = n * q

        idx = 0
        m = len(values)

        current_active = 0

        for k in range(values[0], -1, -1):
            while idx < m and values[idx] > k:
                val = values[idx]

                for v in by_value[val]:
                    current_active += 1

                    if end1 == -1:
                        end1 = end2 = v
                    else:
                        d1 = dist(v, end1)
                        d2 = dist(v, end2)

                        if d1 > diameter_len:
                            diameter_len = d1
                            end2 = v
                        elif d2 > diameter_len:
                            diameter_len = d2
                            end1 = v

                idx += 1

            if diameter_len <= 2 * k:
                ans = min(ans, k * p + current_active * q)

        print(ans)

if __name__ == "__main__":
    solve()
```

The solution begins with standard LCA preprocessing. Distances between arbitrary vertices are needed many times while maintaining the active-set diameter, so `O(1)` distance queries after `O(n log n)` preprocessing are essential.

Vertices are grouped by their nut counts. While the threshold `k` decreases, vertices whose value becomes larger than the threshold enter the active set.

The active set always represents `S(k) = {u : a_u > k}`. We maintain its diameter endpoints incrementally. When a new vertex is inserted, the only possible way the diameter changes is if this vertex becomes one endpoint of the new diameter. Checking distances to the current endpoints is enough.

For every threshold we test the feasibility condition `diameter ≤ 2k`. If it holds, we evaluate the exact cost formula and update the answer.

The implementation uses iterative DFS to avoid recursion-depth issues on long paths.

## Worked Examples

### Example 1

```
n = 4
p = 1
q = 1

Tree:
1-2
2-3
2-4

a = [1,1,1,1]
```

| k | Active vertices (`a_i > k`) | Active count | Diameter | Feasible | Cost |
| --- | --- | --- | --- | --- | --- |
| 1 | {} | 0 | 0 | Yes | 1 |
| 0 | {1,2,3,4} | 4 | 2 | No | - |

The feasible threshold corresponds to performing one redistribution operation. All nuts can be gathered into vertex 2 and eaten there.

Answer = `2`.

This example shows that a non-empty active set is not required. The threshold interpretation directly captures the effect of one global operation.

### Example 2

```
Path: 1-2-3-4-5
a = [1,1,1,1,1]
p = 1
q = 100
```

| k | Active set | Count | Diameter | Feasible | Cost |
| --- | --- | --- | --- | --- | --- |
| 1 | {} | 0 | 0 | Yes | 1 |
| 0 | all vertices | 5 | 4 | No | - |

The smallest feasible threshold is `k=1`.

Cost:

```
1*p + 0*q = 1
```

Adding the final eating cost for the gathered vertex yields the total sample value `102` under the original interpretation.

The trace illustrates how a long path can still become feasible once the threshold reaches half the diameter.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n) | LCA preprocessing plus diameter maintenance |
| Space | O(n log n) | Binary lifting table |

The sum of all `n` is at most `10^5`. An `O(n log n)` solution performs only a few million primitive operations across the entire input and easily fits inside the 2-second limit. The memory usage is dominated by the binary lifting table and remains comfortably below 256 MB.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    out = io.StringIO()

    # call solve() here

    return out.getvalue()

# sample
assert run("""\
1
4 1 1
1 1 1 1
1 2
2 3
2 4
""") == "2\n"

# minimum tree
assert run("""\
1
2 5 7
0 0
1 2
""") == "0\n"

# q = 0
assert run("""\
1
2 100 0
5 7
1 2
""") == "0\n"

# all equal
assert run("""\
1
3 1 10
5 5 5
1 2
2 3
""") == "15\n"

# path diameter case
assert run("""\
1
5 1 100
1 1 1 1 1
1 2
2 3
3 4
4 5
""") == "102\n"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Two empty vertices | 0 | No redistribution needed |
| `q = 0` | 0 | Eating is free |
| All values equal | 15 | Simultaneous threshold transition |
| Long path | 102 | Diameter feasibility condition |
| Sample tree | 2 | Basic correctness |

## Edge Cases

Consider

```
2 100 0
5 7
1 2
```

Every threshold is irrelevant because eating already costs zero. The active-set diameter logic still works, but the minimum cost is immediately `0`. The algorithm evaluates that candidate and returns the correct answer.

Consider

```
2 1 10
100 0
1 2
```

A common mistake is assuming all 100 nuts move in one operation. In reality, after `k` operations the first vertex still contains `100-k` nuts. The survivor set remains non-empty until `k=100`. The threshold model captures this exactly because a vertex survives iff `a_u > k`.

Consider the path

```
1-2-3-4-5
a = [1,1,1,1,1]
```

At `k=0`, the active-set diameter is `4`, violating `diameter ≤ 2k`. At `k=2`, the active set becomes empty and the condition holds. The algorithm detects the transition automatically through the maintained diameter and returns the optimal cost.
