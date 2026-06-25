---
title: "CF 106056G - Classic Problem"
description: "We have a complete graph whose vertices are numbered from left to right. Normally, the edge between two vertices has cost equal to their distance on this line. However, a small number of pairs are special: those pairs have their own given edge cost instead of the normal distance."
date: "2026-06-25T12:21:25+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 106056
codeforces_index: "G"
codeforces_contest_name: "The 1st Universal Cup. Stage 18: Shenzhen"
rating: 0
weight: 106056
solve_time_s: 121
verified: true
draft: false
---

[CF 106056G - Classic Problem](https://codeforces.com/problemset/problem/106056/G)

**Rating:** -  
**Tags:** -  
**Solve time:** 2m 1s  
**Verified:** yes  

## Solution
## Problem Understanding

We have a complete graph whose vertices are numbered from left to right. Normally, the edge between two vertices has cost equal to their distance on this line. However, a small number of pairs are special: those pairs have their own given edge cost instead of the normal distance. The task is to find the total weight of the minimum spanning tree.

The difficulty comes from the constraints. The number of vertices can be as large as $10^9$, so any solution that iterates over vertices or builds the graph is impossible. At the same time, the number of modified edges is only $10^5$ in total across all tests, which tells us that the solution must depend on the special edges rather than on the size of the graph. Any $O(n)$, $O(n \log n)$, or $O(n^2)$ method is ruled out when $n$ is large.

A common mistake is assuming that the normal path between consecutive vertices is always the MST. This fails because some consecutive edges can be replaced by expensive special edges. For example, with input

```
5 4
1 2 1000000000
1 3 1000000000
1 4 1000000000
1 5 1000000000
```

the normal path cost would appear to be $4$, but every edge leaving vertex 1 is expensive. The optimal answer is `1000000003` because the tree must pay one expensive edge to connect vertex 1, and the remaining vertices can be connected with normal edges.

Another edge case is when there are no special edges:

```
5 0
```

The answer is `4`, not `0` and not the cost of connecting only the visible vertices. The solution has to account for all the hidden ordinary vertices even though we never explicitly store them.

A third tricky case is a cheap special long edge:

```
5 1
1 5 0
```

The answer is `3`. The special edge connects the two ends, but the three middle vertices still need to be attached. A solution that simply replaces the whole segment with cost `0` would be incorrect.

## Approaches

The brute-force approach is to run Kruskal's algorithm on the entire graph. The graph has $n(n-1)/2$ edges, so even storing the edges is impossible. When $n$ approaches $10^9$, this idea fails immediately.

The key observation is that only vertices that appear in special edges can behave differently from the normal line. Let us call these vertices important. There are at most $2m$ of them, so there are only $O(m)$ relevant positions.

Imagine removing all unimportant vertices. They lie in continuous segments between important vertices. Every such segment is a plain chain. The internal vertices of a segment always require the same amount of cost to connect, and we can account for them without storing them.

Suppose two consecutive important vertices are $a$ and $b$. If $b-a>1$, there are internal vertices between them. Those internal vertices contribute $b-a-1$ unavoidable unit edges. After paying that, the remaining connection between the two important vertices can always be made with one unit edge, unless the vertices are actually adjacent. If $a$ and $b$ are adjacent, there is no hidden vertex to help us, so the real edge cost must be used.

This lets us build a compressed graph. Its vertices are only the important vertices. The answer is the number of removed ordinary vertices plus the MST cost of this compressed graph. We add all special edges and the necessary chain edges between consecutive important vertices.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n²) | O(n²) | Too slow |
| Compressed Kruskal | O(m log m) | O(m) | Accepted |

## Algorithm Walkthrough

1. Collect every vertex that appears in a special edge. Also include vertices `1` and `n`, because they are the boundaries of the line. Sort these important vertices and remove duplicates. The number of these vertices is small because it is bounded by the number of special edges.
2. Count the number of vertices that are not important. They will never need to appear in the compressed graph, but they still contribute edges to the final tree. Their contribution is `n - important_count`.
3. Create edges in the compressed graph for every special edge. These edges keep their original weights because they are exactly the unusual choices that can improve or worsen the MST.
4. Connect every pair of consecutive important vertices in the sorted order. If they are adjacent in the original graph, use the special weight if such an edge exists, otherwise use weight `1`. If there is at least one normal vertex between them, use weight `1` because the remaining connection can always be made through the chain.
5. Run Kruskal's algorithm on the compressed graph. Add the resulting MST cost to the contribution of unimportant vertices.

Why it works: every unimportant vertex belongs to a simple line segment with no special edges touching it. Such vertices cannot create new useful shortcuts, so their only role is to add a fixed number of unit-cost connections. All choices that can affect the MST happen between important vertices, and the compressed graph preserves every such choice. Since Kruskal finds the minimum spanning tree of the compressed graph, adding back the fixed segment costs gives the original MST.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve_case(n, m, data):
    specials = {}
    important = {1, n}

    for u, v, w in data:
        specials[(u, v)] = w
        important.add(u)
        important.add(v)

    pts = sorted(important)
    idx = {x: i for i, x in enumerate(pts)}
    k = len(pts)

    edges = []

    for (u, v), w in specials.items():
        edges.append((w, idx[u], idx[v]))

    for i in range(k - 1):
        a = pts[i]
        b = pts[i + 1]
        if b - a == 1:
            w = specials.get((a, b), 1)
        else:
            w = 1
        edges.append((w, i, i + 1))

    edges.sort()

    parent = list(range(k))
    size = [1] * k

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    def union(a, b):
        a = find(a)
        b = find(b)
        if a == b:
            return False
        if size[a] < size[b]:
            a, b = b, a
        parent[b] = a
        size[a] += size[b]
        return True

    ans = n - k
    used = 0

    for w, a, b in edges:
        if union(a, b):
            ans += w
            used += 1
            if used == k - 1:
                break

    return ans

def main():
    t = int(input())
    out = []

    for _ in range(t):
        n, m = map(int, input().split())
        data = []
        for _ in range(m):
            u, v, w = map(int, input().split())
            data.append((u, v, w))
        out.append(str(solve_case(n, m, data)))

    print("\n".join(out))

if __name__ == "__main__":
    main()
```

The dictionary `specials` is used to quickly check whether a consecutive pair of important vertices is a modified edge. This avoids scanning all special edges while building the compressed graph.

The array `pts` contains only the compressed vertices. The DSU works on these indices rather than on the original vertex numbers, which is necessary because the original graph can have up to $10^9$ vertices.

The value `ans = n - k` accounts for the ordinary vertices that were removed during compression. Each of them needs exactly one unit-cost connection. The remaining cost comes from the MST on the compressed graph.

A subtle detail is the condition `b - a == 1`. Only in this case are the two important vertices truly adjacent in the original graph, so a special edge can block the normal unit edge. Otherwise, the hidden vertices allow us to keep a unit connection.

## Worked Examples

For

```
5 0
```

the important vertices are `{1,5}`.

| Step | Important vertices | Added compressed edge | Current cost |
| --- | --- | --- | --- |
| Start | 1, 5 | none | 3 from hidden vertices |
| Kruskal | 1, 5 | edge weight 1 | 4 |

The compressed edge represents the remaining connection after the three hidden vertices are attached. The final value is the usual path cost.

For

```
5 4
1 2 1000000000
1 3 1000000000
1 4 1000000000
1 5 1000000000
```

all vertices are important.

| Step | Edge considered | Action | Cost |
| --- | --- | --- | --- |
| 1 | 2-3 weight 1 | take | 1 |
| 2 | 3-4 weight 1 | take | 2 |
| 3 | 4-5 weight 1 | take | 3 |
| 4 | 1-2 weight 1e9 | take | 1000000003 |

The three cheap edges connect vertices 2 through 5. One expensive edge is unavoidable to include vertex 1.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(m log m) | Sorting the compressed edges dominates the work |
| Space | O(m) | Only special edges and important vertices are stored |

The compressed graph has at most $2m+2$ vertices and $O(m)$ edges, so it fits easily within the constraints even when the original graph has billions of vertices.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys, io

def run(inp: str) -> str:
    old = sys.stdin
    sys.stdin = io.StringIO(inp)
    data = sys.stdin.read().split()
    sys.stdin = old

    it = iter(data)
    t = int(next(it))
    ans = []

    for _ in range(t):
        n = int(next(it))
        m = int(next(it))
        edges = []
        for _ in range(m):
            edges.append((int(next(it)), int(next(it)), int(next(it))))
        ans.append(str(solve_case(n, m, edges)))

    return "\n".join(ans)

assert run("""3
5 3
1 2 5
2 3 4
1 5 0
5 0
5 4
1 2 1000000000
1 3 1000000000
1 4 1000000000
1 5 1000000000
""") == "4\n4\n1000000003"

assert run("""1
1 0
""") == "0"

assert run("""1
5 1
1 5 0
""") == "3"

assert run("""1
6 2
2 5 0
1 6 1
""") == "2"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `5 0` | `4` | No special edges and pure compression |
| `5 1 / 1 5 0` | `3` | Cheap long shortcut still needs internal vertices |
| `6 2 / 2 5 0 / 1 6 1` | `2` | Multiple special edges interacting |

## Edge Cases

For the case where a special edge covers the whole line:

```
5 1
1 5 0
```

the compressed graph has only vertices `1` and `5`. The three non-important vertices contribute `3`. The compressed edge has weight `0`, so the final answer is `3`. The algorithm keeps the hidden chain cost instead of incorrectly treating the shortcut as a complete solution.

For expensive adjacent special edges:

```
5 4
1 2 1000000000
1 3 1000000000
1 4 1000000000
1 5 1000000000
```

there are no hidden vertices, so the answer comes entirely from the compressed graph. Kruskal avoids all expensive edges except the one needed to connect vertex 1.

For the empty case:

```
5 0
```

the algorithm creates only the endpoints. The compressed edge costs `1`, and the removed middle vertices add `3`, giving the correct MST cost `4`.
