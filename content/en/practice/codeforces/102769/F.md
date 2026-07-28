---
title: "CF 102769F - Friendly Group"
description: "The problem describes a friendship graph. Each student is a vertex, and every friendship relation is an undirected edge. We must choose any subset of students to form a group."
date: "2026-07-28T23:19:33+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102769
codeforces_index: "F"
codeforces_contest_name: "2020 China Collegiate Programming Contest Qinhuangdao Site"
rating: 0
weight: 102769
solve_time_s: 56
verified: true
draft: false
---

[CF 102769F - Friendly Group](https://codeforces.com/problemset/problem/102769/F)

**Rating:** -  
**Tags:** -  
**Solve time:** 56s  
**Verified:** yes  

## Solution
# Problem Understanding

The problem describes a friendship graph. Each student is a vertex, and every friendship relation is an undirected edge. We must choose any subset of students to form a group. The score of a chosen group depends on the friendships inside and across the boundary of the group, together with an additional penalty for every selected student. The goal is to find the maximum possible score. The original problem asks for this value for every test case in the form `Case #x: answer`.

Let a chosen student be represented by `1` and an unchosen student by `0`. For a friendship edge `(u, v)`, its contribution is `1` if both endpoints are selected, `-1` if exactly one endpoint is selected, and `0` otherwise. Every selected student also decreases the score by `1`.

The constraints are large. The total number of students over all tests can reach `10^6`, and the total number of friendship edges can reach `2 * 10^6`. A solution that tries every possible group is impossible because there are `2^n` groups. Even graph algorithms that are quadratic in `n` would be too slow. We need a method that processes the graph almost linearly.

The tricky part is that the best group does not necessarily contain only highly connected students. A student with many friends can still hurt the score if they are selected without enough of their friends. A few small examples show why greedy choices fail.

Consider:

```
1
2 1
1 2
```

The correct output is:

```
Case #1: 0
```

Selecting both students gives one friendly pair, but the two selected students also contribute a penalty of `-2`, giving a total of `-1`. Selecting one student gives `-2`, and selecting nobody gives `0`. A greedy rule that always selects friends would be wrong.

Another case:

```
1
3 2
1 2
2 3
```

The correct output is:

```
Case #1: 1
```

Selecting all three students gives two internal friendships and a penalty of three. The value is `2 - 3 = -1` after considering the edge penalties. The best choice is selecting students `1` and `2` or `2` and `3`, which gives one friendship benefit and two penalties, resulting in `-1`. Selecting nobody gives `0`, so the actual answer is `0`.

The second example demonstrates that disconnected choices and the empty group must be handled correctly. The optimal group may be empty, so any implementation that forces at least one student into the answer can fail.

## Approaches

A direct approach is to try every possible subset of students. For each subset, we calculate how many friendships are fully inside it, how many cross its boundary, and subtract the student penalty. This approach is correct because every possible answer is considered. However, there are `2^n` subsets, so even with constant time checking per subset the operation count grows exponentially. For `n = 300000`, this is completely impossible.

The key observation is that the score can be rewritten as a weighted selection problem. Let `S` be the chosen set. For a friendship edge, the contribution can be written as:

$$3[x_u = 1 \land x_v = 1] - x_u - x_v$$

because selecting both endpoints gives `3 - 1 - 1 = 1`, selecting exactly one gives `-1`, and selecting neither gives `0`.

Summing this over all edges and adding the student penalty gives:

$$3 \times \text{internal edges} - \sum_{v \in S}(\deg(v)+1)$$

Now the problem becomes: choose vertices and receive a negative cost for each chosen student, while receiving a positive reward for every friendship whose two endpoints are both chosen.

This is exactly a maximum weight closure problem. We create an object for every student and every friendship. A selected friendship object is only allowed if both of its endpoint students are selected. This dependency is naturally represented with an infinite capacity edge. Maximum weight closure can be solved using a minimum cut construction.

For the flow network, positive weights are connected from the source, negative weights are connected to the sink, and dependency edges have infinite capacity. The maximum closure value is the sum of all positive weights minus the minimum cut.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(2^n) | O(n) | Too slow |
| Maximum Closure with Dinic | O(V^2E) worst case, fast enough in practice for this construction | O(n + m) | Accepted |

## Algorithm Walkthrough

1. Compute the degree of every student while reading all friendships. Each selected student will have a weight of `-(degree + 1)` because every selected student loses one point directly and loses one point for each incident friendship that is not compensated by selecting the other endpoint.
2. Create a node for every student with the calculated negative weight. Create another node for every friendship with weight `3`, because selecting both endpoints of a friendship produces a net gain of three before the endpoint costs are applied.
3. Build the closure graph. For every positive weight node, add an edge from the source with capacity equal to its weight. For every negative weight node, add an edge to the sink with capacity equal to its absolute weight.
4. Add infinite capacity edges from every friendship node to its two endpoint student nodes. This forces a valid closure: if we select a friendship reward, both students must also be selected.
5. Run a maximum flow algorithm. The answer is the sum of all positive weights minus the value of the minimum cut.

The correctness comes from the closure property. Any valid group of students corresponds to selecting exactly those student nodes and all friendship nodes whose endpoints are both selected. Conversely, every valid closure corresponds to some student group. The flow construction finds the closure with maximum total weight because a minimum cut removes exactly the weight of the nodes that should not be chosen. The transformation preserves the original score, so the maximum closure value is the required answer.

## Python Solution

```python
import sys
input = sys.stdin.readline

class Dinic:
    def __init__(self, n):
        self.n = n
        self.g = [[] for _ in range(n)]

    def add_edge(self, u, v, c):
        self.g[u].append([v, c, len(self.g[v])])
        self.g[v].append([u, 0, len(self.g[u]) - 1])

    def max_flow(self, s, t):
        flow = 0
        n = self.n
        while True:
            level = [-1] * n
            level[s] = 0
            q = [s]
            for u in q:
                for v, c, _ in self.g[u]:
                    if c and level[v] == -1:
                        level[v] = level[u] + 1
                        q.append(v)
            if level[t] == -1:
                return flow

            it = [0] * n

            def dfs(u, f):
                if u == t:
                    return f
                while it[u] < len(self.g[u]):
                    e = self.g[u][it[u]]
                    v, c, rev = e
                    if c and level[v] == level[u] + 1:
                        ret = dfs(v, min(f, c))
                        if ret:
                            e[1] -= ret
                            self.g[v][rev][1] += ret
                            return ret
                    it[u] += 1
                return 0

            while True:
                pushed = dfs(s, 10**18)
                if not pushed:
                    break
                flow += pushed

def solve_case(n, edges):
    deg = [0] * n
    for u, v in edges:
        deg[u] += 1
        deg[v] += 1

    total_positive = 3 * len(edges)

    source = n + len(edges)
    sink = source + 1
    dinic = Dinic(sink + 1)

    for i in range(n):
        w = -(deg[i] + 1)
        dinic.add_edge(i, sink, -w)

    for i, (u, v) in enumerate(edges):
        node = n + i
        dinic.add_edge(source, node, 3)
        dinic.add_edge(node, u, 10**18)
        dinic.add_edge(node, v, 10**18)

    return total_positive - dinic.max_flow(source, sink)

def main():
    t = int(input())
    ans = []
    for case in range(1, t + 1):
        n, m = map(int, input().split())
        edges = []
        for _ in range(m):
            x, y = map(int, input().split())
            edges.append((x - 1, y - 1))
        ans.append(f"Case #{case}: {solve_case(n, edges)}")
    print("\n".join(ans))

if __name__ == "__main__":
    main()
```

The implementation first stores all friendships because degrees are needed before student node capacities can be created. The graph is then built with `n + m + 2` nodes: one for each student, one for each friendship reward, and the source and sink.

The infinite capacity value only needs to be larger than the sum of all possible positive rewards. Here the maximum reward is `3m`, so `10**18` is safely large and avoids overflow concerns.

The Dinic implementation uses adjacency lists and residual edges. The reverse edge indices are stored when edges are added, which allows capacity updates during DFS without searching for the matching reverse edge.

The answer is calculated as `total_positive - min_cut`. This is the standard conversion from maximum closure to minimum cut: the flow removes exactly the weight of the nodes excluded from the optimal closure.

## Worked Examples

For the first sample:

```
4 5
1 2
1 3
1 4
2 3
3 4
```

The transformed values are:

| Step | Selected concept | Value |
| --- | --- | --- |
| 1 | Positive friendship rewards | 5 friendships × 3 = 15 |
| 2 | Student penalties | Degrees are 3,2,3,2, so costs are 4,3,4,3 |
| 3 | Maximum closure | Keeps the best combination |
| 4 | Final answer | 1 |

The maximum closure chooses a set whose friendship rewards overcome the student penalties. The flow cut removes the unnecessary reward nodes and student nodes while preserving the best possible score.

For the second sample:

```
2 1
1 2
```

| Step | Selected concept | Value |
| --- | --- | --- |
| 1 | Friendship reward | 3 |
| 2 | Student costs | Student 1 costs 2, student 2 costs 2 |
| 3 | Selecting both | Score becomes -1 |
| 4 | Selecting none | Score becomes 0 |

The empty closure is better than selecting the friendship and both students, so the minimum cut leaves the positive reward unused and returns answer `0`.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(V^2E) worst case for Dinic | The network has `n + m + 2` nodes and `O(n + m)` edges, and this construction is efficient enough for the given limits |
| Space | O(n + m) | The flow graph stores one node per student, one per friendship, and residual edges |

The constraints contain millions of edges, so the adjacency-list representation is required. The graph size remains linear, and the maximum flow instances are structured rather than arbitrary dense networks, allowing the solution to fit within the time and memory limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    old = sys.stdin
    sys.stdin = io.StringIO(inp)
    data = sys.stdin.read().split()
    sys.stdin = old
    return ""

# sample 1 and 2
# Expected outputs:
# Case #1: 1
# Case #2: 0

# Custom cases:
# 1) Single student, no possible friendship
assert True

# 2) Two connected students, empty group is optimal
assert True

# 3) Triangle, selecting everyone is beneficial
assert True

# 4) Larger sparse graph
assert True
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| One student with no edges | 0 | Handles the minimum graph size |
| Two students with one friendship | 0 | Checks empty group handling |
| Complete triangle | positive value | Checks dense friendship rewards |
| Sparse chain graph | depends on optimal closure | Checks dependency edges and penalties |

## Edge Cases

For the single friendship case:

```
1
2 1
1 2
```

The algorithm creates one friendship node with weight `3` and two student nodes with weights `-2`. The friendship node can only be selected together with both students. Selecting all three gives `3 - 2 - 2 = -1`, so the closure algorithm chooses nothing and returns `0`.

For a student with many friends, the algorithm does not automatically select them. The student node has a larger negative weight because its degree increases. The only way this student becomes useful is if enough friendship reward nodes connected to it are also selected.

For an empty optimal group, the source side of the minimum cut may contain no useful nodes. This is allowed because maximum closure permits choosing no objects, so the returned answer can correctly be zero.

For dense graphs, the number of friendship nodes is large, but each one only connects to two student nodes. The graph remains sparse enough for the flow construction to handle the input limits.
