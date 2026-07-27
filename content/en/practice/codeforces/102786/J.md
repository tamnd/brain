---
title: "CF 102786J - \u041f\u0443\u0442\u0435\u0448\u0435\u0441\u0442\u0432\u0438\u0435 \u041aOR\u043e\u0432\u044c\u0435\u0432\u0430"
description: "I will provide the editorial as a complete document. Edit We have an undirected road network. Each house is a vertex, each road is an edge, and every road has an integer label."
date: "2026-07-27T19:31:21+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102786
codeforces_index: "J"
codeforces_contest_name: "\u041e\u0442\u043a\u0440\u044b\u0442\u044b\u0439 \u0447\u0435\u043c\u043f\u0438\u043e\u043d\u0430\u0442 \u042f\u0440\u0413\u0423 \u0438\u043c. \u041f.\u0413. \u0414\u0435\u043c\u0438\u0434\u043e\u0432\u0430 Demidov Open IT Cup 2019"
rating: 0
weight: 102786
solve_time_s: 57
verified: true
draft: false
---

[CF 102786J - \u041f\u0443\u0442\u0435\u0448\u0435\u0441\u0442\u0432\u0438\u0435 \u041aOR\u043e\u0432\u044c\u0435\u0432\u0430](https://codeforces.com/problemset/problem/102786/J)

**Rating:** -  
**Tags:** -  
**Solve time:** 57s  
**Verified:** yes  

## Solution
I will provide the editorial as a complete document.

Edit

# Problem Understanding

We have an undirected road network. Each house is a vertex, each road is an edge, and every road has an integer label. We need to travel from one specified house to another, but the cost of a route is not the sum of road lengths. The cost is the bitwise OR of all road values used on that route. The task is to find the smallest possible such value among all routes, or report that the two houses are disconnected.

The input describes a graph with up to 100000 vertices and 100000 edges. The weights can be as large as 10^9, so only about 30 binary positions can appear. A graph of this size immediately rules out algorithms that enumerate paths or run a search over all possible route combinations. Even ordinary shortest path algorithms such as Dijkstra do not apply directly because OR does not have the additive property required by them.

The key difficulty is that a route with many edges can be better than a route with fewer edges. For example, a path with weights 8 and 1 has value 9, while a single edge with weight 10 has value 10. The number of edges is irrelevant, only the set of bits appearing in the route matters.

There are several edge cases that break simple implementations. If the graph is disconnected, the answer must be -1 instead of some large initial value. For example:

```
3 1
1 2 7
1 3
```

The correct output is:

```
-1
```

A careless solution that initializes the answer to zero or only checks existing edges could incorrectly return a value even though house 3 cannot be reached.

A second trap is assuming that the path with the smallest number of roads is optimal. Consider:

```
3 3
1 2 6
2 3 1
1 3 7
1 3
```

The correct output is:

```
7
```

The direct road gives 7, and the two-road route gives 6 OR 1, which is also 7. A method based on edge count would not solve the actual optimization problem.

Another common mistake is processing bits in the wrong direction. Since the binary value of a high bit dominates all lower bits, removing a high bit can only be done after checking whether connectivity remains possible without it. For example, if a solution accidentally keeps a bit that could have been removed, no amount of later lower-bit optimization can fix the result.

# Approaches

A direct brute force approach would try to explore all possible paths between the two vertices and compute the OR of every path. This is correct because every possible answer comes from some path, but the number of paths in a dense graph can be exponential. Even a graph with 100000 edges can contain an enormous number of different routes, making enumeration impossible.

A slightly more structured idea is to use a shortest path algorithm and store the best OR value found so far for every vertex. The transition from a vertex to a neighbor would be:

```
new_value = current_value | edge_weight
```

The problem is that the number of different OR values that can reach a vertex is not naturally bounded by one. The usual Dijkstra argument depends on combining path lengths with addition, while OR can make a previously worse-looking state become useful later. A normal shortest path framework does not exploit the special structure of OR values.

The important observation is that an OR result only contains bits that appear on at least one edge in the chosen route. Instead of trying to construct the route directly, we can construct the answer bit by bit.

Suppose we currently have a set of bits that are still allowed to appear in the answer. If we remove one bit and the two target vertices are still connected using only edges that fit inside the remaining mask, then that bit was unnecessary and can be permanently discarded. If removing it disconnects the graph, then every valid route needs that bit, so we must keep it.

This turns the problem into repeated connectivity checks. Since edge weights have only about 30 relevant bits, we only need around 30 checks. Each check can be done with a disjoint set union structure.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | Exponential in the number of paths | O(n + m) | Too slow |
| Optimal | O(B(n + m) α(n)) where B is the number of bits | O(n) | Accepted |

# Algorithm Walkthrough

1. Compute a mask containing the OR of every edge weight in the graph. Any valid route can only contain bits that exist in this mask, so this is the largest possible answer.
2. Process bits from the highest bit down to the lowest bit. For the current bit, temporarily remove it from the mask and test whether the starting vertex can still reach the destination using only edges whose set bits are all contained in this smaller mask.
3. During a connectivity test, build a disjoint set union structure. For every edge, merge its endpoints if its weight satisfies `(weight & mask) == weight`. This condition means that the edge does not introduce any forbidden bit.
4. If the two vertices are in the same component after removing the bit, keep the bit removed. If they are disconnected, restore the bit because every possible route requires it.
5. After all bits have been processed, the remaining mask is the minimum possible OR value. If the original graph never allowed a connection, the final mask is not enough to distinguish that case, so perform a final connectivity check and output -1 when the destination is unreachable.

The reason this greedy process is correct is that binary numbers are ordered lexicographically by their highest differing bit. When considering a bit, removing it is always better than keeping it if a valid route still exists without it. Any later decision only affects lower bits and cannot compensate for unnecessarily keeping a higher bit. The invariant is that after processing a prefix of bits, the current mask is the smallest possible set of already considered high bits that still permits a valid route.

# Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, m = map(int, input().split())
    edges = []
    mask = 0

    for _ in range(m):
        u, v, w = map(int, input().split())
        u -= 1
        v -= 1
        edges.append((u, v, w))
        mask |= w

    a, b = map(int, input().split())
    a -= 1
    b -= 1

    def connected(cur_mask):
        parent = list(range(n))
        size = [1] * n

        def find(x):
            while parent[x] != x:
                parent[x] = parent[parent[x]]
                x = parent[x]
            return x

        def union(x, y):
            x = find(x)
            y = find(y)
            if x == y:
                return
            if size[x] < size[y]:
                x, y = y, x
            parent[y] = x
            size[x] += size[y]

        for u, v, w in edges:
            if (w & cur_mask) == w:
                union(u, v)

        return find(a) == find(b)

    if not connected(mask):
        print(-1)
        return

    for bit in range(30, -1, -1):
        candidate = mask & ~(1 << bit)
        if connected(candidate):
            mask = candidate

    print(mask)

if __name__ == "__main__":
    solve()
```

The variable `mask` represents the best answer still possible after removing unnecessary bits. It starts as the OR of all edges because no route can contain a bit that does not appear anywhere in the graph.

The `connected` function performs the repeated graph test. It does not need to construct a new graph. Instead, it joins exactly those edges whose weights are compatible with the current mask. The expression `(w & cur_mask) == w` checks that every bit used by the edge is allowed.

The disjoint set union implementation uses path compression and union by size, keeping every connectivity check close to linear time. The weights are at most 10^9, so checking bits 30 down to 0 covers every possible set bit.

The initial connectivity check is necessary because the final mask alone cannot represent the difference between an unreachable graph and a reachable graph with answer zero. A path containing only zero-weight edges is valid and must return zero.

# Worked Examples

For the first sample:

```
3 3
1 2 5
1 3 1
2 3 5
1 2
```

The initial mask is `5 | 1 | 5 = 5`. The target vertices are already connected.

| Step | Current mask | Removed bit | Connectivity | Decision |
| --- | --- | --- | --- | --- |
| Start | 5 | none | connected | begin |
| Check bit 2 | 1 | 4 | disconnected | keep bit |
| Check bit 0 | 4 | 1 | disconnected | keep bit |

The final answer is 5. The only possible routes between vertices 1 and 2 use a road with weight 5, so the OR value cannot be smaller.

For the second sample:

```
5 3
3 5 6
1 4 7
2 4 6
1 3
```

The initial mask is `6 | 7 | 6 = 7`. Vertices 1 and 3 are disconnected.

| Step | Current mask | Connectivity | Result |
| --- | --- | --- | --- |
| Initial check | 7 | disconnected | output -1 |

This demonstrates why reachability must be checked separately. Bit minimization cannot create a path where none exists.

# Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(31(n + m) α(n)) | There are at most 31 bit checks, and each check builds a DSU over all edges |
| Space | O(n + m) | The graph and DSU arrays are stored |

The limits allow roughly a few million simple operations. The algorithm performs at most 31 full scans of the edge list, which is around 3.1 million edge checks for the maximum input, and the DSU operations are nearly constant amortized time.

# Test Cases

```python
import sys
import io

def run(inp: str) -> str:
    old_stdin = sys.stdin
    old_stdout = sys.stdout
    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    solve()

    result = sys.stdout.getvalue()
    sys.stdin = old_stdin
    sys.stdout = old_stdout
    return result

assert run("""3 3
1 2 5
1 3 1
2 3 5
1 2
""") == "5\n", "sample 1"

assert run("""5 3
3 5 6
1 4 7
2 4 6
1 3
""") == "-1\n", "sample 2"

assert run("""2 1
1 2 0
1 2
""") == "0\n", "zero edge"

assert run("""3 3
1 2 6
2 3 1
1 3 7
1 3
""") == "7\n", "equal route values"

assert run("""4 4
1 2 8
2 3 4
3 4 2
1 4 15
1 4
""") == "14\n", "higher bit removal"

assert run("""2 1
1 2 1073741823
1 2
""") == "1073741823\n", "large weight"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Two vertices connected by a zero edge | 0 | Confirms that zero is a valid answer |
| Multiple paths with the same OR value | 7 | Confirms that edge count does not matter |
| Large edge weight | 1073741823 | Confirms bit handling near the integer boundary |
| Unreachable vertices | -1 | Confirms disconnected handling |

# Edge Cases

The disconnected graph case is handled before any bit removal begins. For the input:

```
3 1
1 2 7
1 3
```

The initial mask is 7. The first connectivity check finds that vertex 3 is not in the same DSU component as vertex 1, so the algorithm immediately returns -1. It never attempts to minimize a nonexistent route.

The algorithm also correctly handles routes with zero-weight edges. For:

```
2 1
1 2 0
1 2
```

The initial mask is zero. The connectivity check accepts the only edge because `(0 & 0) == 0`. No bits can be removed, and the answer remains zero.

A route with many edges can be better than a direct edge, and the algorithm does not prefer either one. For:

```
4 4
1 2 8
2 3 4
3 4 2
1 4 15
1 4
```

The direct edge gives 15. The longer path gives `8 | 4 | 2 = 14`. The greedy removal checks each high bit and discovers that bit 0 can disappear while the vertices remain connected, leaving 14 as the minimum value.

The final edge cases involve high bits. Because the algorithm processes all possible bits from 30 down to 0, weights such as 1073741823 are handled without overflow or missing significant positions.

This editorial can be adjusted to be shorter, more contest-style, or more proof-focused if needed.
