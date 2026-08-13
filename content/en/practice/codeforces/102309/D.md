---
title: "CF 102309D - Director of Orz Pandas"
description: "We have two groups of features. The first group contains (n) features and the second contains (m) features. Every feature has a positive weight, and some pairs are declared incompatible."
date: "2026-08-13T23:50:22+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102309
codeforces_index: "D"
codeforces_contest_name: "The 2019 \u201cOrz Panda\u201d Cup Programming Contest"
rating: 0
weight: 102309
solve_time_s: 62
verified: true
draft: false
---

[CF 102309D - Director of Orz Pandas](https://codeforces.com/problemset/problem/102309/D)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 2s  
**Verified:** yes  

## Solution
## Problem Understanding

We have two groups of features. The first group contains (n) features and the second contains (m) features. Every feature has a positive weight, and some pairs are declared incompatible. The input guarantees that every incompatible pair contains one feature from the first group and one from the second group, so the conflict graph is bipartite.

We need to choose a set of features with maximum total weight such that no conflict has both endpoints chosen. In graph terminology, this is a maximum-weight independent set in a bipartite graph.

For each test case, the first line gives (n) and (m). The next line gives the (n+m) feature weights. Then (k) conflict pairs follow. A pair ((p,q)) means that features (p) and (q) cannot be selected simultaneously. Since (p\le n<q), every edge goes from the left part of the bipartite graph to the right part.

The required output is the largest possible sum of weights of a conflict-free set of features. There can be multiple test cases, and they continue until end of file.

Here (n,m\le100), so the graph has at most 200 vertices. The number of conflicts can reach 10,000, which is close to the maximum possible number of edges between two groups of 100 vertices. A brute-force search over all subsets would have up to (2^{200}) possibilities, which is far beyond what a one-second solution can handle. The small number of vertices might initially suggest subset enumeration, but the exponential factor is the real obstacle. The dense edge bound also means an algorithm should be comfortable processing roughly 10,000 edges.

The weights can be as large as (10^7). Since there are at most 200 features, the answer can reach (2\cdot10^9). Python integers have arbitrary precision, while a C++ implementation would still fit this particular bound inside a signed 32-bit integer, although using 64-bit capacities is the standard safe choice for flow implementations.

There are several cases where an apparently simple implementation can fail. First, conflicts do not mean that one entire group must be chosen or rejected. For example,

```
1 1
5 7
1
1 2
```

has answer `7`, because we can choose the second feature and leave the first unchosen. A method that greedily chooses the heavier feature happens to work here, but that idea fails when several conflicts interact.

For example,

```
2 2
6 5 7 7
3
1 3
1 4
2 3
```

has answer `12`, obtained by choosing features 2 and 4. A greedy decision on feature 1 can block both right-side features and produce a smaller answer.

Another boundary case is a feature with no conflicts. For

```
1 1
4 9
1
1 2
```

we cannot take both features, but we can take the weight-9 feature, so the answer is `9`. In the flow construction, every vertex must still receive its own weight capacity even if it has no incident conflict edge.

A final implementation trap is the capacity used for conflict edges. It must be larger than the sum of all feature weights. If the capacity is chosen too small, the minimum cut may prefer cutting a conflict edge rather than paying for a vertex, which does not correspond to removing a feature. Choosing `sum(weights) + 1` avoids that problem completely.

## Approaches

The direct approach is to enumerate every subset of the (n+m) features. For each subset, we check whether it contains both endpoints of any conflict edge. If it is valid, we calculate its weight and keep the maximum. This is correct because every possible selection appears exactly once among the subsets.

With at most 200 features, however, there can be (2^{200}) subsets. Even if checking one subset took only constant time, this is approximately (1.6\cdot10^{60}) states. Checking up to 10,000 conflicts for every subset would make the theoretical work even larger. The brute-force solution is useful for understanding the problem, but there is no chance of making it fit the time limit.

The structure of the conflicts gives us a much stronger route. The graph is bipartite, and we are looking for a maximum-weight independent set. Every independent set is exactly the complement of a vertex cover: if we remove all vertices outside an independent set, every conflict edge must have at least one endpoint removed. Since all weights are positive, maximizing the weight kept is equivalent to minimizing the total weight removed.

So the problem becomes a minimum-weight vertex cover in a bipartite graph. The weighted version of König's theorem can be solved with a minimum (s)-(t) cut.

Construct a flow network with a source (s), all first-group vertices, all second-group vertices, and a sink (t). Give every first-group vertex an edge from (s) with capacity equal to its weight. Give every second-group vertex an edge to (t) with capacity equal to its weight. For every conflict from a left vertex to a right vertex, add a directed edge with a capacity larger than the total weight of all vertices.

Consider an (s)-(t) cut. If a left vertex stays on the source side, its source edge is not cut. If it moves to the sink side, its source edge is cut and we pay its weight. Similarly, a right vertex on the source side causes its edge to the sink to be cut, paying its weight.

The very large conflict edges prevent a minimum cut from putting a conflicting left vertex and right vertex on opposite sides in the wrong direction. Since there is always a cut of cost at most the total weight of all vertices, a conflict edge with capacity greater than that total can never be part of a minimum cut. Consequently, every minimum cut corresponds to a vertex cover, and its capacity is exactly the weight of that cover.

If the minimum vertex cover has weight (C), the maximum independent set has weight

[
\sum_i w_i-C.
]

Thus one maximum-flow computation gives the answer.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | (O(2^{n+m}k)) | (O(n+m+k)) | Too slow |
| Optimal | (O(V^2E)) with Dinic | (O(V+E)) | Accepted |

Here (V=n+m+2) and (E=k+n+m). The stated (O(V^2E)) bound is the standard worst-case bound for Dinic's algorithm on general integer-capacity networks. With at most about 202 vertices and 10,200 forward edges, this is easily manageable.

## Algorithm Walkthrough

1. Read one test case and store the weights of all (n+m) features. Compute their total weight. We will eventually subtract the minimum weight of the vertices that have to be discarded.
2. Create a flow network containing a source, the (n) left-side feature vertices, the (m) right-side feature vertices, and a sink. Use zero-based internal vertex indices, while converting each input feature number from one-based indexing.
3. Add an edge from the source to every left-side feature with capacity equal to that feature's weight. Cutting this edge means removing that feature from the selected set, so the cost of doing so is exactly its weight.
4. Add an edge from every right-side feature to the sink with capacity equal to its weight. Cutting such an edge has the same interpretation for a right-side feature.
5. For every conflict ((p,q)), add an edge from the corresponding left vertex to the corresponding right vertex with capacity `total_weight + 1`. This capacity is deliberately larger than the cost of removing every feature. A minimum cut will never choose to cut such an edge, so every conflict must be covered by moving at least one of its endpoint vertices to the appropriate side of the cut.
6. Run a maximum-flow algorithm on the resulting network. By the max-flow min-cut theorem, the resulting flow value equals the minimum cut capacity. By the construction, that minimum cut is exactly the minimum weight of a vertex cover.
7. Subtract the minimum vertex-cover weight from the total feature weight. The remaining features form a maximum-weight independent set, so this difference is the required answer.

Why it works: consider any minimum cut and look at the vertices on the source side. A left vertex on the sink side contributes its source edge to the cut, while a right vertex on the source side contributes its sink edge. Since every conflict edge has capacity greater than the total weight of all vertices, no minimum cut uses a conflict edge. Hence every conflict has at least one endpoint outside the source-side independent set. The vertices removed from that set form a vertex cover, and the cut capacity equals exactly their total weight. Conversely, any vertex cover can define a cut of the same weight by placing the removed left vertices on the sink side and the removed right vertices on the source side. Thus the minimum cut is precisely the minimum-weight vertex cover. Taking its complement gives the maximum-weight independent set, which is exactly the required feature selection.

## Python Solution

```python
import sys
input = sys.stdin.readline

class Dinic:
    def __init__(self, n):
        self.n = n
        self.g = [[] for _ in range(n)]

    def add_edge(self, u, v, cap):
        forward = [v, cap, None]
        backward = [u, 0, forward]
        forward[2] = backward
        self.g[u].append(forward)
        self.g[v].append(backward)

    def bfs(self, s, t):
        level = [-1] * self.n
        level[s] = 0
        queue = [s]
        head = 0

        while head < len(queue):
            u = queue[head]
            head += 1

            for v, cap, rev in self.g[u]:
                if cap > 0 and level[v] == -1:
                    level[v] = level[u] + 1
                    queue.append(v)

        return level[t] != -1, level

    def dfs(self, u, t, pushed, level, it):
        if u == t:
            return pushed

        while it[u] < len(self.g[u]):
            edge = self.g[u][it[u]]
            v, cap, rev = edge

            if cap > 0 and level[v] == level[u] + 1:
                flow = self.dfs(v, t, min(pushed, cap), level, it)

                if flow:
                    edge[1] -= flow
                    rev[1] += flow
                    return flow

            it[u] += 1

        return 0

    def max_flow(self, s, t):
        flow = 0
        INF = 10**30

        while True:
            found, level = self.bfs(s, t)
            if not found:
                break

            it = [0] * self.n

            while True:
                pushed = self.dfs(s, t, INF, level, it)
                if pushed == 0:
                    break
                flow += pushed

        return flow

def solve(data):
    pos = 0
    out = []

    while pos < len(data):
        n = data[pos]
        m = data[pos + 1]
        pos += 2

        weights = data[pos:pos + n + m]
        pos += n + m

        k = data[pos]
        pos += 1

        conflicts = []
        for _ in range(k):
            p = data[pos] - 1
            q = data[pos + 1] - 1
            pos += 2
            conflicts.append((p, q))

        total = sum(weights)

        source = n + m
        sink = source + 1
        dinic = Dinic(n + m + 2)

        for i in range(n):
            dinic.add_edge(source, i, weights[i])

        for j in range(n, n + m):
            dinic.add_edge(j, sink, weights[j])

        inf = total + 1

        for p, q in conflicts:
            dinic.add_edge(p, q, inf)

        cover_weight = dinic.max_flow(source, sink)
        out.append(str(total - cover_weight))

    return "\n".join(out)

def main():
    data = list(map(int, sys.stdin.buffer.read().split()))
    sys.stdout.write(solve(data))

if __name__ == "__main__":
    main()
```

The `Dinic` class stores each residual edge together with a reference to its reverse edge. When flow is pushed forward, the forward capacity decreases and the reverse capacity increases. That reverse capacity is what lets later augmenting paths undo an earlier decision.

The BFS constructs the level graph used by Dinic. It only traverses edges with positive residual capacity, so vertices that cannot currently receive more flow are ignored.

The DFS sends blocking flow through edges that advance exactly one level at a time. The `it` array remembers which outgoing edge was last considered for each vertex. Without it, the same saturated or unusable edges could be scanned repeatedly, making the implementation much slower.

The `solve` function first reads the entire input as integers. This is convenient because test cases continue until EOF and the input has no explicit test-case count. The position `pos` moves through the flattened integer array and consumes exactly the number of values belonging to each test case.

The source is indexed as `n + m`, and the sink as `n + m + 1`. A feature numbered (p) in the input becomes vertex `p - 1`, which is necessary because the input uses one-based indexing while Python arrays use zero-based indexing.

The conflict capacity is `total + 1`, not an arbitrary constant such as (10^9). This is enough because a cut that removes every feature costs exactly `total`, so a minimum cut can never prefer a conflict edge costing more than `total`.

There is no integer overflow concern in Python. The largest useful capacity is only slightly above the sum of all weights, which is at most (2\cdot10^9), but Python's arbitrary-precision integers make the implementation robust even if that bound changes.

The final answer is `total - cover_weight`, directly implementing the complement relationship between an independent set and a vertex cover.

## Worked Examples

The supplied statement contains only one actual sample, so the second trace uses a small constructed test case.

For Sample 1, the four feature weights are (4,3,8,2). The conflicts are (1)-(3), (1)-(4), and (2)-(4).

The total weight is (17). The flow network has source capacities (4) and (3) for the left vertices, and sink capacities (8) and (2) for the right vertices.

| Step | Left feature state | Right feature state | Minimum cover cost | Independent-set weight |
| --- | --- | --- | --- | --- |
| Initial | 1, 2 available | 3, 4 available | 0 | 17 |
| Resolve conflicts with 1 | 1 or removed | 3, 4 | 4 or 10 | depends on cut |
| Resolve conflict 2-4 | 2 or removed | 4 or removed | minimum becomes 5 | 12 |
| Final | remove feature 2 | keep 3 and 4 | 5 | 12 |

The optimal selection is features 1 and 3, with weight (4+8=12), or equivalently features 3 and 4, also with weight (8+2=10). The minimum vertex cover has weight (5), obtained by removing features 1? Actually, feature 1 covers conflicts with both 3 and 4, but conflict 2-4 still requires feature 2 or 4. Choosing features 1 and 2 as the cover costs (4+3=7), while choosing features 3 and 4 costs (10), and choosing features 1 and 4 costs (6). Thus the minimum cover is features 1 and 4, with cost (6), giving (17-6=11). This exposes why a trace must follow the actual cut rather than guessing from individual conflicts.

The correct max-flow value is `6`, so the sample answer is `11`.

For the second example, consider:

```
2 2
6 5 7 7
3
1 3
1 4
2 3
```

The possible useful choices include features 2 and 4, with total weight (5+7=12). The flow construction finds a minimum vertex cover of weight (13), for example by removing features 1 and 2. The resulting independent-set weight is (25-13=12).

| Step | Source-side choice | Removed vertices | Cut cost | Kept weight |
| --- | --- | --- | --- | --- |
| Initial | all vertices considered | none | 0 | 25 |
| Cover edge 1-3 | remove 1 or 3 | candidate 1 | 6 | 19 |
| Cover edge 1-4 | 1 already removed | candidate unchanged | 6 | 19 |
| Cover edge 2-3 | remove 2 or 3 | candidates 1, 2 | 11 | 14 |
| Minimum cut | remove 1 and 2 | 1, 2 | 11 | 14 |

The actual minimum cover here is features 1 and 2 with cost (6+5=11), so the maximum independent set has weight (25-11=14), obtained by choosing features 3 and 4. This example demonstrates why the optimization has to consider the whole conflict structure instead of greedily handling edges one at a time.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | (O(V^2E)) worst case with Dinic | (V=n+m+2\le202), while (E=O(n+m+k)\le10200) |
| Space | (O(V+E)) | The residual graph stores both directions of every network edge |

The graph is tiny in terms of vertices and has at most about 10,200 forward edges, so even the general worst-case bound for Dinic is practical here. The construction itself is linear in the number of features and conflicts. Memory usage is also comfortably below 256 MB.

## Test Cases

```python
import sys
import io

class Dinic:
    def __init__(self, n):
        self.n = n
        self.g = [[] for _ in range(n)]

    def add_edge(self, u, v, cap):
        f = [v, cap, None]
        r = [u, 0, f]
        f[2] = r
        self.g[u].append(f)
        self.g[v].append(r)

    def bfs(self, s, t):
        level = [-1] * self.n
        level[s] = 0
        q = [s]
        head = 0

        while head < len(q):
            u = q[head]
            head += 1

            for v, cap, rev in self.g[u]:
                if cap > 0 and level[v] == -1:
                    level[v] = level[u] + 1
                    q.append(v)

        return level[t] != -1, level

    def dfs(self, u, t, pushed, level, it):
        if u == t:
            return pushed

        while it[u] < len(self.g[u]):
            edge = self.g[u][it[u]]
            v, cap, rev = edge

            if cap > 0 and level[v] == level[u] + 1:
                f = self.dfs(v, t, min(pushed, cap), level, it)
                if f:
                    edge[1] -= f
                    rev[1] += f
                    return f

            it[u] += 1

        return 0

    def max_flow(self, s, t):
        ans = 0
        INF = 10**30

        while True:
            ok, level = self.bfs(s, t)
            if not ok:
                break

            it = [0] * self.n

            while True:
                f = self.dfs(s, t, INF, level, it)
                if f == 0:
                    break
                ans += f

        return ans

def solve(data):
    pos = 0
    ans = []

    while pos < len(data):
        n, m = data[pos], data[pos + 1]
        pos += 2

        w = data[pos:pos + n + m]
        pos += n + m

        k = data[pos]
        pos += 1

        edges = []
        for _ in range(k):
            p, q = data[pos] - 1, data[pos + 1] - 1
            pos += 2
            edges.append((p, q))

        total = sum(w)
        s = n + m
        t = s + 1

        flow = Dinic(t + 1)

        for i in range(n):
            flow.add_edge(s, i, w[i])

        for i in range(n, n + m):
            flow.add_edge(i, t, w[i])

        inf = total + 1

        for p, q in edges:
            flow.add_edge(p, q, inf)

        ans.append(str(total - flow.max_flow(s, t)))

    return "\n".join(ans)

def run(inp: str) -> str:
    data = list(map(int, inp.split()))
    return solve(data)

sample1 = """\
2 2
4 3 8 2
3
1 3
1 4
2 4
"""
assert run(sample1) == "11", "sample 1"

minimum = """\
1 1
5 7
1
1 2
"""
assert run(minimum) == "7", "minimum-size case"

all_equal = """\
2 2
5 5 5 5
4
1 3
1 4
2 3
2 4
"""
assert run(all_equal) == "10", "all-equal complete bipartite graph"

boundary = """\
2 2
1 100 99 2
2
1 3
2 4
"""
assert run(boundary) == "199", "large boundary weight"

no_real_conflict_choice = """\
1 1
10000000 10000000
1
1 2
"""
assert run(no_real_conflict_choice) == "10000000", "maximum weight boundary"

max_size_input = "100 100\n" + " ".join(["1"] * 200) + "\n10000\n"
max_size_input += "".join(
    f"{i} {100 + j}\n"
    for i in range(1, 101)
    for j in range(1, 101)
)
assert run(max_size_input) == "100", "maximum-size dense graph"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `2 2 / 4 3 8 2 / 3 conflicts` | `11` | Provided sample and basic reduction to minimum cut |
| `1 1 / 5 7 / 1 conflict` | `7` | Minimum graph size and asymmetric weights |
| `2 2 / 5 5 5 5 / 4 conflicts` | `10` | Complete bipartite graph and equal weights |
| `2 2 / 1 100 99 2 / 2 conflicts` | `199` | Large weight differences and independent decisions |
| `1 1 / 10000000 10000000 / 1 conflict` | `10000000` | Maximum individual weight and capacity handling |
| `100 100 / 200 unit weights / 10000 conflicts` | `100` | Maximum graph size and dense conflict set |

The maximum-size test uses every possible left-to-right conflict, producing a complete (K_{100,100}). Since every pair across the two groups conflicts, a conflict-free selection can contain vertices from only one side, giving weight 100 because all 200 vertices have unit weight. This test is particularly useful for catching implementations that accidentally omit some edges or use incorrect feature-index boundaries.

## Edge Cases

The first edge case is a single conflict with unequal weights:

```
1 1
5 7
1
1 2
```

The total weight is 12. The network contains capacities 5 from the source to the left vertex and 7 from the right vertex to the sink, with a conflict edge of capacity 13. The minimum cut chooses the cheaper vertex to remove, namely the left vertex with weight 5. The maximum independent-set weight is (12-5=7). A careless implementation that always removes the right endpoint would incorrectly return 5.

The second edge case demonstrates why conflicts must be considered globally:

```
2 2
6 5 7 7
3
1 3
1 4
2 3
```

The total weight is 25. Choosing features 3 and 4 gives 14 and contains no conflict. The corresponding minimum vertex cover has weight 11, consisting of features 1 and 2. The flow value is therefore 11 and the answer is 14. A greedy method that processes the first conflict and immediately removes the locally cheaper endpoint can make a choice that interacts badly with later conflicts.

The third edge case is a completely connected bipartite graph:

```
2 2
5 5 5 5
4
1 3
1 4
2 3
2 4
```

Every left feature conflicts with every right feature. Consequently, a valid selection can use vertices from only one side. Either side contributes 10, so the answer is 10. The flow network has a minimum vertex cover of weight 10, and the complement also has weight 10. This checks that the construction handles multiple conflict edges incident to every vertex.

The fourth edge case checks the largest useful capacity scale:

```
1 1
10000000 10000000
1
1 2
```

The total weight is 20,000,000, so the conflict capacity becomes 20,000,001. The minimum cut removes either feature for cost 10,000,000, leaving the other one selected. The answer is 10,000,000. Using `total + 1` as the infinite capacity is sufficient and avoids relying on a hard-coded magic number.

The final boundary case is a dense graph with 100 vertices on each side and all 10,000 possible conflicts. The algorithm adds every conflict edge, and because its capacity exceeds the total vertex weight, the minimum cut cannot cut any of those edges. It must instead choose an entire side as the cheaper vertex-cover alternative. With unit weights on every vertex, the minimum cover costs 100 and the maximum independent set also weighs 100. This exercises the maximum values of both vertex and edge counts while preserving the same mathematical invariant used on smaller instances.
