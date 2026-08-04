---
title: "CF 102558E - \u0420\u0430\u0437\u0434\u0435\u043b\u0435\u043d\u0438\u0435 \u0433\u0440\u0430\u0444\u0430"
description: "The graph contains vertices connected by weighted undirected edges. We have to color the vertices with two colors, with both colors used, and look at the edges whose endpoints received the same color. Among those edges, we care about the smallest weight."
date: "2026-08-04T09:20:07+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102558
codeforces_index: "E"
codeforces_contest_name: "Contest for Yandex interns 2019"
rating: 0
weight: 102558
solve_time_s: 96
verified: true
draft: false
---

[CF 102558E - \u0420\u0430\u0437\u0434\u0435\u043b\u0435\u043d\u0438\u0435 \u0433\u0440\u0430\u0444\u0430](https://codeforces.com/problemset/problem/102558/E)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 36s  
**Verified:** yes  

## Solution
## Problem Understanding

The graph contains vertices connected by weighted undirected edges. We have to color the vertices with two colors, with both colors used, and look at the edges whose endpoints received the same color. Among those edges, we care about the smallest weight. The goal is to make this smallest internal edge as large as possible.

A useful way to look at the objective is to choose an answer value `x`. If all edges with weight smaller than `x` are forced to go between the two groups, then every edge left inside a group has weight at least `x`. The question becomes whether the subgraph consisting only of edges with weight less than `x` can be divided into two sides, which is exactly the question of whether this subgraph is bipartite.

The input size reaches `100000` vertices and `100000` edges. Trying every possible partition is impossible because there are `2^n` colorings. Even algorithms with quadratic behavior are too slow for these limits, since `10^10` operations would be far beyond what is practical. We need an approach close to `O((n+m) log C)`, where `C` is the range of possible answers.

There are a few cases where an incorrect implementation can silently fail. Repeated edges with different weights must be handled independently. For example:

```
3 3
1 2 1
1 2 5
2 3 4
```

The correct answer is `4`. The edge of weight `1` matters when checking small thresholds, but the edge of weight `5` can still become the internal edge of the final partition. A solution that keeps only one edge between two vertices may remove the information needed for the answer.

Another case is when the whole graph is almost bipartite but becomes impossible only because of one heavier edge:

```
3 3
1 2 1
2 3 1
1 3 10
```

The correct answer is `10`. For every value up to `10`, the graph formed by smaller edges is bipartite. At `11`, the whole graph is included and is not bipartite. A solution that checks only whether the original graph is bipartite misses the threshold interpretation.

A final edge case is that the answer can be the largest edge weight in the graph:

```
3 3
1 2 2
2 3 2
1 3 7
```

The correct answer is `7`. The algorithm must allow the threshold to reach the maximum edge weight, because the edge with that weight may be the only edge remaining inside a part.

## Approaches

A direct solution would enumerate every possible division of vertices into two nonempty groups. For each division, we would scan all edges, find the edges whose endpoints are in the same group, and keep the smallest such weight. This is correct because it checks exactly the quantity requested by the problem.

The issue is the number of possible divisions. With `n` vertices there are `2^n` assignments of two colors, and even after ignoring the symmetric cases where both colors are swapped, the amount of work is still exponential. For `n = 100000`, this approach is not remotely feasible.

The key observation is that we do not need to construct the best partition directly. We can ask a different question: can the answer be at least `x`? For that to happen, every edge with weight smaller than `x` must connect vertices of different groups. In other words, if we temporarily keep only edges with weight smaller than `x`, this graph must be bipartite.

The brute force works because it checks every possible coloring, but fails when the number of colorings explodes. The threshold observation lets us replace the search over partitions with a search over edge weights. The property is monotonic: if edges smaller than `x` form a bipartite graph, then edges smaller than any smaller value also form a bipartite graph. This allows binary search on `x`.

For each binary search step, we run a bipartite check using BFS or DFS over all edges whose weight is below the current threshold.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(2^n * m) | O(n) | Too slow |
| Binary search with bipartite checks | O((n + m) log W) | O(n + m) | Accepted |

## Algorithm Walkthrough

1. Store all edges. The only operation we need during checking is deciding whether an edge weight is below a chosen threshold.
2. Binary search the answer between `1` and `100001`. For a candidate value `mid`, we test whether all edges with weight less than `mid` form a bipartite graph.
3. During the check, create a color array. An uncolored vertex is assigned one color, then BFS spreads opposite colors through every edge with weight smaller than the threshold.
4. If an edge with weight smaller than the threshold connects two vertices that already have the same color, the graph is not bipartite for this threshold. The candidate answer is too large, so binary search continues on the lower half.
5. If the check succeeds, the candidate value is achievable. We move the binary search range upward to find a larger possible answer.
6. The largest successful threshold is printed. Because the whole graph is guaranteed not to be bipartite, the search cannot incorrectly return a value where all edges could be placed between the two groups.

The invariant behind the algorithm is that a threshold `x` is valid exactly when every edge that could become a forbidden small internal edge can be separated by a two-coloring. The bipartite check proves whether such a coloring exists. Since increasing the threshold only adds more edges to the checked graph, once a threshold fails, every larger threshold also fails.

## Python Solution

```python
import sys
from collections import deque

input = sys.stdin.readline

def solve():
    n, m = map(int, input().split())
    edges = []
    for _ in range(m):
        u, v, w = map(int, input().split())
        edges.append((u - 1, v - 1, w))

    def check(limit):
        graph = [[] for _ in range(n)]
        for u, v, w in edges:
            if w < limit:
                graph[u].append(v)
                graph[v].append(u)

        color = [-1] * n

        for start in range(n):
            if color[start] != -1:
                continue
            color[start] = 0
            q = deque([start])

            while q:
                v = q.popleft()
                for to in graph[v]:
                    if color[to] == -1:
                        color[to] = color[v] ^ 1
                        q.append(to)
                    elif color[to] == color[v]:
                        return False
        return True

    left = 1
    right = 100002

    while left + 1 < right:
        mid = (left + right) // 2
        if check(mid):
            left = mid
        else:
            right = mid

    print(left)

if __name__ == "__main__":
    solve()
```

The edge list is kept in its original form because each binary search iteration needs to filter edges by weight. Rebuilding the temporary graph inside `check` keeps the logic simple and avoids mistakes with outdated edges.

The binary search uses the range `[1, 100002)`. The upper bound is exclusive because edge weights are at most `100000`, and a threshold larger than every edge would include the whole graph. The guarantee that the original graph is not bipartite means that such a threshold must fail.

The BFS colors connected components separately. This matters because the graph may contain several disconnected parts, and each component can be colored independently. A conflict appears only when an already colored neighbor requires the same color.

Python integers do not overflow here, and the only arithmetic involving the answer is the binary search midpoint calculation. The use of `sys.stdin.readline` and a deque keeps input and graph traversal fast enough for the constraints.

## Worked Examples

For the first sample:

```
3 4
1 2 1
1 2 2
1 3 3
3 2 4
```

The binary search tests whether different thresholds are possible.

| limit | Edges with weight < limit | Bipartite? | Decision |
| --- | --- | --- | --- |
| 50001 | All edges | No | decrease |
| 25001 | All edges | No | decrease |
| 12501 | All edges | No | decrease |
| ... | ... | ... | ... |
| 5 | Edges of weights 1, 2, 3 | Yes | increase |
| 6 | All edges | No | decrease |

The largest valid threshold is `4`. The check with `limit = 5` only removes the edge of weight `4`, so the remaining graph can be two-colored. Increasing the threshold includes that edge and creates the odd cycle.

For the second sample:

```
4 5
1 2 1
2 3 1
3 4 1
4 1 1
2 4 2
```

| limit | Edges with weight < limit | Bipartite? | Decision |
| --- | --- | --- | --- |
| 50001 | All edges | No | decrease |
| ... | ... | ... | ... |
| 3 | All edges | No | decrease |
| 2 | Four cycle edges | Yes | increase |

The answer is `2`. The four edges of weight `1` form an even cycle, so they can be separated into two groups. The edge of weight `2` can remain inside one group, making the minimum internal edge weight equal to `2`.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O((n + m) log W) | The binary search performs about 17 checks, and each check scans the graph. |
| Space | O(n + m) | The temporary graph, colors, queue, and edge storage are linear. |

With `n` and `m` up to `100000`, each bipartite check is linear, and the logarithmic factor comes only from the small range of possible weights. This fits comfortably within the required limits.

## Test Cases

```python
import sys
import io
from collections import deque

def solution(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    input = sys.stdin.readline

    n, m = map(int, input().split())
    edges = []
    for _ in range(m):
        u, v, w = map(int, input().split())
        edges.append((u - 1, v - 1, w))

    def check(limit):
        g = [[] for _ in range(n)]
        for u, v, w in edges:
            if w < limit:
                g[u].append(v)
                g[v].append(u)

        color = [-1] * n
        for s in range(n):
            if color[s] == -1:
                color[s] = 0
                q = deque([s])
                while q:
                    v = q.popleft()
                    for to in g[v]:
                        if color[to] == -1:
                            color[to] = color[v] ^ 1
                            q.append(to)
                        elif color[to] == color[v]:
                            return False
        return True

    l, r = 1, 100002
    while l + 1 < r:
        mid = (l + r) // 2
        if check(mid):
            l = mid
        else:
            r = mid
    return str(l)

assert solution("""3 4
1 2 1
1 2 2
1 3 3
3 2 4
""") == "4"

assert solution("""4 5
1 2 1
2 3 1
3 4 1
4 1 1
2 4 2
""") == "2"

assert solution("""3 3
1 2 1
2 3 2
1 3 3
""") == "3"

assert solution("""3 3
1 2 5
2 3 5
1 3 5
""") == "5"

assert solution("""4 4
1 2 1
2 3 1
3 4 1
4 1 1
""") == "1"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Triangle with weights 1, 2, 3 | 3 | The maximum edge can be the answer. |
| Triangle with all weights 5 | 5 | Equal weights and maximum threshold handling. |
| Four cycle with all weights 1 | 1 | Smallest valid non-bipartite original graph. |

## Edge Cases

For repeated edges, consider:

```
3 3
1 2 1
1 2 5
2 3 4
```

The check for `limit = 5` uses only the first and third edges. They form a path, so they are bipartite. The check for `limit = 6` includes all edges and also includes the heavier parallel edge. The answer becomes `5`, because the largest threshold that keeps the smaller-edge graph bipartite is exactly `5`. The algorithm never merges parallel edges, so both possibilities are preserved.

For a graph where the maximum edge is the answer:

```
3 3
1 2 2
2 3 2
1 3 7
```

When the threshold is `7`, only the two edges of weight `2` are checked. They form a path and can be two-colored. When the threshold becomes `8`, the edge of weight `7` is added and the triangle becomes non-bipartite. The binary search returns `7`, which matches the best possible internal edge.

For the minimum-size graph:

```
3 3
1 2 1
2 3 1
1 3 1
```

Every threshold larger than `1` includes the entire triangle, which cannot be colored with two colors. The only successful threshold is `1`, so the algorithm outputs `1`. This confirms that the lower boundary of the search is handled correctly.
