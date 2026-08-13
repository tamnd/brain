---
title: "CF 102331F - Fast Spanning Tree"
description: "We have a weighted set of vertices and a list of indexed edges. Initially there are no graph edges, so every vertex is its own connected component."
date: "2026-08-14T05:00:53+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102331
codeforces_index: "F"
codeforces_contest_name: "2019 Summer Petrozavodsk Camp, Day 2: 300iq Contest 2 (XX Open Cup, Grand Prix of Kazan)"
rating: 0
weight: 102331
solve_time_s: 276
verified: true
draft: false
---

[CF 102331F - Fast Spanning Tree](https://codeforces.com/problemset/problem/102331/F)

**Rating:** -  
**Tags:** -  
**Solve time:** 4m 36s  
**Verified:** yes  

## Solution
## Problem Understanding

We have a weighted set of vertices and a list of indexed edges. Initially there are no graph edges, so every vertex is its own connected component. For an edge (i=(a_i,b_i,s_i)), the edge can be used when its endpoints are currently in different components and the sum of the total vertex weights of those two components is at least (s_i). Among all usable edges, the process always chooses the smallest index, joins the two components, and repeats.

The output is exactly the sequence of edge indices selected by this process. Because every successful operation joins two different components, at most (n-1) edges can be selected. The original problem has (n,m\le 300000), vertex weights and thresholds at most (10^6), a 5 second time limit, and 256 MiB of memory.

A direct simulation cannot repeatedly inspect all (m) edges after every union. In the worst case there can be (n-1) successful unions, so scanning every edge after every union performs roughly

[
(n-1)m < 9\cdot 10^{10}
]

edge checks. That is far beyond what a 5 second implementation can afford.

There are several edge cases that easily break a careless implementation. First, an edge with threshold zero is immediately usable, but only once if later copies connect vertices that have already become connected. For example,

```
2 2
0 0
1 2 0
1 2 0
```

has output

```
1
1
```

The second edge satisfies the weight condition too, but its endpoints are already connected.

Exact equality also matters because the condition is greater than or equal to the threshold. For

```
2 1
2 3
1 2 5
```

the output is

```
1
1
```

A strict comparison would incorrectly reject the only edge.

An edge that is initially unusable can become usable after a completely different, smaller-index edge is selected. For example,

```
3 2
1 1 1
1 2 3
2 3 2
```

initially only edge 2 is usable. After edge 2 joins vertices 2 and 3, that component has weight 2, so edge 1 becomes usable because (1+2=3). The correct output is

```
2
2 1
```

A one-pass scan through the edge array would incorrectly stop after selecting edge 2.

Finally, the nominal lower bound (n\ge1) does not give a valid instance with (n=1,m\ge1), because every tuple requires two distinct endpoints. The smallest valid instance has two vertices.

## Approaches

The brute-force simulation is conceptually simple. Maintain a DSU, repeatedly scan edges from index 1 through (m), and select the first edge whose endpoints have different representatives and whose two component sums reach its threshold. After a successful union, start another scan from index 1. This exactly follows the definition, so its correctness is immediate. Its problem is the repeated scan: there may be (n-1) unions and each scan costs (O(m)), giving (O(nm)), or almost (9\cdot10^{10}) checks at the maximum constraints.

The useful observation is that component weights only increase. Consider an edge whose two current component weights are (x) and (y), with threshold (s). If it is not yet usable, define the remaining amount as

[
r=s-x-y>0.
]

For the edge to become usable, the two component weights together must increase by at least (r). At least one of the two components must contribute at least

[
\left\lceil\frac r2\right\rceil.
]

So instead of checking this edge whenever either endpoint component changes, we put an alarm on both components. The alarm on the component of weight (x) fires at

[
x+\left\lceil\frac r2\right\rceil,
]

and the other fires at

[
y+\left\lceil\frac r2\right\rceil.
]

If neither alarm has fired, the edge definitely cannot have become usable. When one alarm fires, we inspect the edge once. If (x+y\ge s), the edge becomes globally eligible. Otherwise we recompute the remaining amount and split that remaining amount in half again.

Suppose the alarm on the first side fires. That side has increased by at least (\lceil r/2\rceil), so the new remaining amount satisfies

[
r' \le r-\left\lceil\frac r2\right\rceil
= \left\lfloor\frac r2\right\rfloor.
]

Thus every time the same edge is reconsidered without becoming usable, its remaining threshold is at least halved. Since (s\le10^6), an edge needs only (O(\log s)) alarm recalculations.

We still need to avoid having an alarm for every edge attached separately to every vertex. All vertices in the same connected component have exactly the same component weight, so their alarms can be stored together. Each DSU component owns a min-heap of alarms. When two components merge, we merge the smaller alarm heap into the larger one. This is the small-to-large technique, so an alarm entry is moved only (O(\log n)) times.

Finally, every edge that has actually become usable is placed into a global min-heap keyed by its original index. The smallest index is always processed first. An entry can become stale because another selected edge may have already joined its endpoints, so before using a global candidate we check its DSU representatives again.

This is the central connection between the brute force and the optimal solution. The brute force works because every edge is checked exactly when its condition might have changed, but it checks far too many edges. The halving observation lets us schedule only the moments when an edge can possibly become relevant, while DSU and small-to-large make the component changes efficient. The same alarm idea is the standard technique used for this problem in the contest editorial.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | (O(nm)) | (O(n+m)) | Too slow |
| Optimal | (O(m\log C\log n\log m)) for the direct binary-heap implementation | (O(n+m\log C)) | Accepted approach |

Here (C) is the maximum threshold, at most (10^6). With a meldable heap, the heap-merging factor can be reduced, which is the form usually quoted for the intended solution. The direct `heapq` implementation below keeps the data structure simple and follows the same small-to-large strategy.

## Algorithm Walkthrough

1. Build a DSU containing one vertex per component. Store the current total weight of each component at its representative. Since all thresholds are at most (10^6), component weights can safely be capped at (10^6): once a component reaches that value, it alone is already enough to satisfy every possible threshold.
2. For every edge (i=(u,v,s)), find the current components of (u) and (v). Initially they are just the individual vertices. If their weights already sum to at least (s), put (i) into the global candidate min-heap. Otherwise let

[
d=s-w_u-w_v
]

and put an alarm on each endpoint component at

[
w_u+\left\lceil\frac d2\right\rceil
\quad\text{and}\quad
w_v+\left\lceil\frac d2\right\rceil.
]

The two alarms guarantee that the edge will be reconsidered before it could possibly become valid.

1. Repeatedly remove the smallest edge index from the global candidate heap. Find the current DSU representatives of its endpoints. If they are equal, the candidate is stale because some earlier edge already connected those components, so discard it. Otherwise the edge is exactly the smallest currently eligible edge, so append its index to the answer.
2. Merge the two endpoint components. Use small-to-large on their alarm heaps, keeping the larger heap as the destination and moving every alarm from the smaller heap into it. Add the component weights together and cap the result at (10^6).
3. After the merge, inspect the smallest alarm in the new component heap. If its threshold is greater than the new component weight, no alarm below it can fire either, so stop. If its threshold is reached, remove it and reconsider that edge.
4. When reconsidering an alarm, find the current components of the edge's endpoints. If they have already become equal, the alarm is stale and can simply be discarded. Otherwise calculate their current total weight. If it reaches the edge threshold, put the edge into the global candidate heap. If it does not, calculate the new remaining amount and create two new half-threshold alarms.
5. Continue processing the global candidate heap until it becomes empty. At that point there is no edge with different endpoint components that satisfies its threshold, so the original process must also stop.

### Why it works

For every edge whose endpoints are still in different components, maintain the invariant that its alarm threshold on each endpoint is the current component weight plus half of the current remaining deficit, rounded upward. If neither alarm has fired, both components have increased by less than half of that deficit, so their combined increase is less than the whole deficit and the edge cannot yet satisfy its condition. If an alarm fires, checking the real condition determines whether the edge is now eligible. If it is not, the remaining deficit is at most half of what it was before, so replacing the alarms preserves the invariant and guarantees only logarithmically many recalculations.

The global candidate heap contains every edge that has become eligible, possibly together with stale edges whose endpoints were subsequently joined. Because component weights never decrease, an eligible edge remains eligible until its endpoints become equal. Consequently, after discarding stale candidates, the smallest element of the global heap is exactly the smallest valid edge required by the original process. Every union is performed on two different components, so the produced sequence is precisely the sequence from the statement.

## Python Solution

```python
import sys
import heapq

input = sys.stdin.readline

MAX_S = 1_000_000

def solve():
    n, m = map(int, input().split())
    weight = list(map(int, input().split()))

    parent = list(range(n))
    size = [1] * n

    # Component weights. They are capped at MAX_S because
    # every threshold is at most MAX_S.
    comp = weight[:]

    U = [0] * m
    V = [0] * m
    S = [0] * m

    # alarms[root] contains (absolute_threshold, edge_id)
    alarms = [[] for _ in range(n)]

    # Edges that are currently eligible, ordered by original index.
    ready = []

    answer = []

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    def schedule(e):
        u = find(U[e])
        v = find(V[e])

        if u == v:
            return

        remaining = S[e] - comp[u] - comp[v]

        if remaining <= 0:
            heapq.heappush(ready, e)
            return

        half = (remaining + 1) // 2
        heapq.heappush(alarms[u], (comp[u] + half, e))
        heapq.heappush(alarms[v], (comp[v] + half, e))

    def merge_components(a, b):
        a = find(a)
        b = find(b)

        if a == b:
            return a

        # Keep the larger alarm heap.
        if len(alarms[a]) > len(alarms[b]):
            a, b = b, a

        parent[a] = b
        size[b] += size[a]
        comp[b] = min(MAX_S, comp[a] + comp[b])

        small = alarms[a]
        large = alarms[b]

        # Move the smaller heap into the larger heap.
        while small:
            threshold, e = heapq.heappop(small)

            # The old alarm may already be obsolete because its endpoints
            # became connected.
            x = find(U[e])
            y = find(V[e])

            if x == y:
                continue

            if threshold <= comp[b]:
                schedule(e)
            else:
                heapq.heappush(large, (threshold, e))

        # Process every alarm that has become active because the component
        # weight increased.
        while large and large[0][0] <= comp[b]:
            threshold, e = heapq.heappop(large)

            x = find(U[e])
            y = find(V[e])

            if x == y:
                continue

            schedule(e)

        return b

    # Build the initial alarm structure.
    for e in range(m):
        u, v, s = map(int, input().split())
        u -= 1
        v -= 1

        U[e] = u
        V[e] = v
        S[e] = s

        schedule(e)

    while ready:
        e = heapq.heappop(ready)

        u = find(U[e])
        v = find(V[e])

        if u == v:
            continue

        # The edge is eligible and has the smallest index among all
        # candidates currently known to be eligible.
        answer.append(e + 1)

        merge_components(u, v)

    print(len(answer))
    print(*answer)

if __name__ == "__main__":
    solve()
```

The DSU arrays have their usual meaning. `parent` identifies components, `size` supports the union heuristic, and `comp` stores the current total weight for each representative. Path compression makes repeated representative lookups effectively constant amortized time.

`alarms[root]` is the local priority queue for a component. An entry `(threshold, e)` says that edge `e` should be reconsidered as soon as this component reaches `threshold`. The threshold is absolute rather than a relative increment, which makes merging two heaps straightforward.

The `schedule` function is the heart of the halving trick. It first checks whether the edge is already valid. If it is, the edge goes into `ready`. Otherwise the remaining deficit is split evenly between the two endpoint components. The expression `(remaining + 1) // 2` is the integer implementation of the required ceiling.

The merge operation deliberately chooses the smaller alarm heap as the source. Every moved entry doubles the size of the data structure that contains it, so an alarm can move only logarithmically many times. After the component weight changes, the smallest alarms are repeatedly examined until the first one whose threshold is still too large.

The order of operations in `merge_components` matters. The DSU parent is changed and the new component weight is calculated before alarms are reconsidered, because every alarm must be evaluated against the new component state. When `schedule` is called afterward, it uses `find` again, so an edge whose endpoints were accidentally merged during this operation is safely discarded.

All arithmetic is done with Python integers, so there is no overflow issue. In C++, 64-bit integers are a safe choice as well, although the threshold cap makes 32-bit values sufficient for the component sums used by the algorithm.

The original contest constraints are designed around this small-to-large heap technique. The published solution uses the same half-deficit alarms and global candidate priority queue.

## Worked Examples

### Sample 1

The initial component weights are (1,4,3,4,0). Edges 2, 3, 4, and 5 are immediately eligible, while edge 1 has total weight (4+0=4<5).

| Operation | Global candidates | Selected edge | Component change | Result |
| --- | --- | --- | --- | --- |
| Initial | 2, 3, 4, 5 | 2 | (1) and (3) merge, weight (4) | answer = 2 |
| After merge | 3, 4, 5 | 3 | (4) and (0) merge, weight (4) | answer = 2, 3 |
| After merge | 4, 5 | 4 | component weight (4) merges with vertex 4 of weight (4) | answer = 2, 3, 4 |
| After merge | 1, 5 | 1 | edge 1 now joins the weight-8 component to vertex 5, so it is eligible | answer = 2, 3, 1, 4 |

The interesting part is the last transition. Edge 1 was initially below its threshold, but its endpoint component grew from weight 4 to weight 8. The alarm mechanism detects that change without rescanning all edges. The global queue still decides which eligible edge has the smallest index, producing the required order (2,3,1,4). The official sample has exactly this output.

### Sample 2

The initial weights are (3,2,2). Edges 1, 2, and 4 require total weight 6 between vertices 1 and 2, so none is initially valid. Edge 3 has threshold 3 and is immediately valid. Edge 5 requires 6 between vertices 2 and 3 and is initially short as well.

| Operation | Global candidates | Selected edge | Relevant component weights | Result |
| --- | --- | --- | --- | --- |
| Initial | 3 | 3 | (3+2=5) | merge 1 and 2 |
| After edge 3 | 5 | 5 | (5+2=7) | merge 1,2 with 3 |
| Final | empty | none | all vertices connected | stop |

When edge 3 joins vertices 1 and 2, their component weight becomes 5. This crosses the alarm threshold for edge 5, and its actual condition is now (5+2\ge6). Edge 5 is consequently inserted into the global candidate heap and selected next. The output is (3,5), matching the sample.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | (O(m\log C\log n\log m)) | Each edge is reconsidered (O(\log C)) times, alarm entries move (O(\log n)) times under small-to-large merging, and binary heap operations cost (O(\log m)). |
| Space | (O(n+m\log C)) | DSU and edge arrays use (O(n+m)), while the total number of generated alarm entries is (O(m\log C)). |

The threshold bound (C\le10^6) makes the halving factor small, with at most about 20 meaningful reductions per edge. The crucial improvement over brute force is that an edge is no longer inspected after every component merge. The intended solution is commonly summarized as a small-to-large merge combined with (O(\log C)) alarm updates per edge.

For the original 256 MiB limit, a C++ implementation is the safer contest choice because Python heap entries have substantial object overhead. The Python implementation above is a faithful implementation of the algorithm, but the asymptotic method, rather than Python object representation, is what the original contest constraints were designed around.

## Test Cases

```python
# The test harness assumes the solve() function from the solution above
# is already defined.

import sys
import io

def run(inp: str) -> str:
    global input

    old_stdin = sys.stdin
    old_stdout = sys.stdout

    sys.stdin = io.StringIO(inp)
    input = sys.stdin.readline
    output = io.StringIO()
    sys.stdout = output

    try:
        solve()
    finally:
        sys.stdin = old_stdin
        sys.stdout = old_stdout

    return output.getvalue()

# Provided sample 1
assert run("""\
5 5
1 4 3 4 0
4 5 5
3 1 1
2 5 2
4 3 1
4 1 4
""") == """\
4
2 3 1 4
""", "sample 1"

# Provided sample 2
assert run("""\
3 5
3 2 2
1 2 6
1 2 6
1 2 3
1 2 6
2 3 6
""") == """\
2
3 5
""", "sample 2"

# Minimum valid instance, threshold zero.
assert run("""\
2 1
0 0
1 2 0
""") == """\
1
1
""", "minimum valid instance"

# Exact equality at the threshold.
assert run("""\
2 1
2 3
1 2 5
""") == """\
1
1
""", "equality boundary"

# An initially impossible edge becomes valid after another edge is chosen.
assert run("""\
3 2
1 1 1
1 2 3
2 3 2
""") == """\
2
2 1
""", "dynamic eligibility and index ordering"

# Zero weights with a positive threshold: no edge can ever become valid.
assert run("""\
2 1
0 0
1 2 1
""") == """\
0

""", "never eligible"

# Maximum-size structural stress test.
# The first 299999 edges form a chain and are all immediately valid.
n = 300000
edges = [f"{i} {i + 1} 0" for i in range(1, n)]
edges.append(f"1 {n} 0")

large_input = (
    f"{n} {n}\n"
    + " ".join(["0"] * n)
    + "\n"
    + "\n".join(edges)
    + "\n"
)

expected_large = (
    f"{n - 1}\n"
    + " ".join(map(str, range(1, n)))
    + "\n"
)

assert run(large_input) == expected_large, "maximum-size chain"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `2 1`, weights `0 0`, threshold `0` | `1 / 1` | Minimum valid graph and zero threshold |
| `2 1`, weights `2 3`, threshold `5` | `1 / 1` | Exact equality with the threshold |
| `3 2`, weights `1 1 1`, edges `(1,2,3)` and `(2,3,2)` | `2 / 2 1` | An edge becoming eligible after a different edge is selected |
| `2 1`, weights `0 0`, threshold `1` | `0 / blank` | Permanently impossible positive threshold |
| `300000` vertices and `300000` zero-threshold chain edges | `299999 / 1..299999` | Maximum input size, DSU merging, and stale final edge |

## Edge Cases

The zero-threshold case is handled during `schedule`. For

```
2 2
0 0
1 2 0
1 2 0
```

edge 1 is immediately inserted into the global candidate heap. It is selected and joins the two vertices. When edge 2 is eventually removed from the global heap, `find(1)` and `find(2)` are equal, so it is discarded as stale. The output is `1` followed by edge index `1`.

Exact equality is handled by the `remaining <= 0` test. With

```
2 1
2 3
1 2 5
```

the initial component weights sum to exactly 5. The edge is inserted into `ready` immediately and selected, giving output `1` and then `1`.

The dynamic-order case

```
3 2
1 1 1
1 2 3
2 3 2
```

starts with only edge 2 eligible. After selecting it, vertices 2 and 3 form a component of weight 2. Edge 1 now has endpoint component weights 1 and 2, so its threshold 3 is reached. It is inserted into the global candidate heap and selected next. The output is `2 1`. This demonstrates why the algorithm must maintain future alarms rather than scanning edges only once.

For an impossible positive threshold,

```
2 1
0 0
1 2 1
```

the remaining deficit is 1, so both alarms are placed one unit above their current component weights. No component ever grows, so neither alarm fires and the global candidate heap remains empty. The process stops immediately, producing zero selected edges and a blank second line.

The maximum-size chain test uses zero thresholds, so every edge is initially eligible. The global heap repeatedly chooses the smallest remaining index. The first (299999) edges connect the chain, while the final edge joins vertices already in the same component and is discarded. The algorithm therefore produces exactly (299999) selected edges without ever needing to inspect all (300000) edges after every union.
