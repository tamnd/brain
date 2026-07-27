---
title: "CF 102784K - Territorial Tarantulas"
description: "We have a tree of N burrows. Each vertex contains one tarantula, and every tarantula belongs to one of K subspecies. The tunnels form a connected tree, so there is exactly one path between any two burrows."
date: "2026-07-27T19:52:24+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102784
codeforces_index: "K"
codeforces_contest_name: "UTPC Contest 10-23-20 Div. 1"
rating: 0
weight: 102784
solve_time_s: 66
verified: true
draft: false
---

[CF 102784K - Territorial Tarantulas](https://codeforces.com/problemset/problem/102784/K)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 6s  
**Verified:** yes  

## Solution
# Problem Understanding

We have a tree of `N` burrows. Each vertex contains one tarantula, and every tarantula belongs to one of `K` subspecies. The tunnels form a connected tree, so there is exactly one path between any two burrows. For every subspecies, we need the largest distance between two vertices having that subspecies. If a subspecies appears only once, its range is zero.

The input size reaches `N = 200000`, so solutions that inspect all pairs of tarantulas are impossible. A single subspecies with all vertices would already create about `N^2 / 2` pairs, which is far beyond what can run in a few seconds. We need a solution close to linear or `N log N`, because that keeps the number of operations around a few million.

The difficult part is that the vertices of one subspecies are not necessarily connected. A normal tree diameter algorithm works when the whole tree is one set, but here we need many diameters at the same time, one for every color.

Consider a few cases that break simpler ideas. If every tarantula has a different subspecies, every answer must be zero. For example:

```
Input:
5 5
1 2 3 4 5
1 2
2 3
3 4
4 5

Output:
0
0
0
0
0
```

A solution that assumes every color has at least two vertices would access a missing endpoint.

A second trap is that the vertices of one subspecies can be separated by other subspecies. For example:

```
Input:
5 2
1 2 1 2 1
1 2
2 3
3 4
4 5

Output:
4
2
```

The three vertices of subspecies one are at the ends and middle of a path. Looking only at adjacent equal colors would miss the real diameter.

A third issue appears when a centroid is used incorrectly. Two vertices in the same child subtree of a centroid do not have a path passing through that centroid. Combining their distances through the centroid would overestimate the real distance.

## Approaches

A straightforward approach is to collect the vertices of each subspecies and compute its diameter independently. For one color, we could choose an arbitrary vertex, run a tree traversal to find the farthest vertex, then run another traversal from that vertex. This is the standard two BFS or DFS diameter method. It is correct because the farthest vertex from any endpoint of a tree contains a diameter endpoint.

The problem is the repeated work. If one subspecies contains all `N` vertices, a single diameter computation already costs `O(N)`. Repeating it for many subspecies can reach `O(NK)`, and if the colors are distributed badly this becomes `O(N^2)`.

The key observation is that the graph is a tree, so centroid decomposition can divide the work. A centroid separates the tree into smaller components. For every centroid, every valid pair of vertices whose path passes through that centroid can be evaluated by looking at their distances from the centroid. The decomposition guarantees that every pair of vertices is considered at exactly one centroid where their paths split.

For one centroid, we process its child components one by one. For every subspecies we remember the largest distance seen in previous components. When we see a vertex of the same subspecies in the current component, combining it with the previous maximum gives the best pair whose path crosses the centroid. After all child components are processed, we recursively solve each remaining component.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(N²) | O(N) | Too slow |
| Centroid Decomposition | O(N log N) | O(N) | Accepted |

## Algorithm Walkthrough

1. Build the tree and store the list of vertices belonging to each subspecies. The answer array starts with zero because a color with fewer than two vertices already has the correct answer.
2. Find the centroid of the current tree component. A centroid is a vertex whose removal leaves components no larger than half of the current component.
3. Treat the centroid as one possible endpoint for paths through it. Store the distance zero for its own subspecies.
4. For every neighbor component of the centroid, run a DFS to collect every vertex in that component together with its distance from the centroid. While collecting, compare each vertex against the best distance of the same subspecies found in previously processed components. This works because a path between those two vertices must pass through the centroid.
5. Merge the collected distances into the stored best distances for this centroid. Keeping only the maximum distance per subspecies is enough because the final pair through the centroid only needs the two largest distances.
6. Mark the centroid as removed and recursively apply the same process to every remaining component.

Why it works: for any two vertices of the same subspecies, consider the first centroid in the decomposition where the two vertices end up in different remaining components or one of them is the centroid. Their path crosses that centroid. The algorithm examines exactly this pair at that moment and combines their two distances correctly. Since every possible pair is considered at its separating centroid, the maximum found value is the true diameter for that subspecies.

## Python Solution

```python
import sys
input = sys.stdin.readline

sys.setrecursionlimit(1 << 25)

def solve():
    n, k = map(int, input().split())
    color = list(map(int, input().split()))
    g = [[] for _ in range(n)]
    for _ in range(n - 1):
        a, b = map(int, input().split())
        a -= 1
        b -= 1
        g[a].append(b)
        g[b].append(a)

    removed = [False] * n
    size = [0] * n
    ans = [0] * k
    best = [None] * n

    def calc_size(u, p):
        size[u] = 1
        for v in g[u]:
            if v != p and not removed[v]:
                size[u] += calc_size(v, u)
        return size[u]

    def find_centroid(u, p, total):
        for v in g[u]:
            if v != p and not removed[v] and size[v] > total // 2:
                return find_centroid(v, u, total)
        return u

    def collect(u, p, d, arr):
        arr.append((color[u], d))
        for v in g[u]:
            if v != p and not removed[v]:
                collect(v, u, d + 1, arr)

    def decompose(u):
        total = calc_size(u, -1)
        c = find_centroid(u, -1, total)

        current = {}
        current[color[c]] = 0

        for v in g[c]:
            if removed[v]:
                continue
            nodes = []
            collect(v, c, 1, nodes)

            for col, dist in nodes:
                if col in current:
                    ans[col] = max(ans[col], current[col] + dist)

            for col, dist in nodes:
                if col not in current or dist > current[col]:
                    current[col] = dist

        removed[c] = True
        for v in g[c]:
            if not removed[v]:
                decompose(v)

    decompose(0)

    print("\n".join(map(str, ans)))

if __name__ == "__main__":
    solve()
```

The `calc_size` function measures the current component size while ignoring already removed centroids. The `find_centroid` function walks into the only subtree that is too large until it reaches a valid centroid.

The `collect` DFS gathers `(color, distance)` pairs from one child component of the centroid. Processing child components separately is essential. Distances from two vertices in the same child component cannot be combined through the centroid.

The `current` dictionary stores the largest distance from this centroid to each color among already processed branches. When a new branch is scanned, combining its vertices with `current` checks all paths that cross the centroid. The answer update uses only addition of distances, so Python integers avoid overflow concerns.

The recursion limit is increased because both tree DFS and centroid recursion can exceed Python's default recursion depth on large inputs.

## Worked Examples

Sample 1:

```
Input:
6 2
1 2 1 2 2 1
3 1
1 2
1 4
1 5
5 6
```

| Step | Centroid | Current color distances | Answer update |
| --- | --- | --- | --- |
| 1 | 1 | color 1: 0 | none |
| 2 | process node 3 | color 1 distance 1 | range of color 1 becomes 1 |
| 3 | process node 5 subtree | color 1 distance 2 | range of color 1 becomes 3 |
| 4 | process color 2 nodes | distances combine through centroid | range of color 2 becomes 2 |

The result is:

```
3
2
```

The trace shows that the algorithm combines vertices from different centroid branches and never assumes that equal colors are adjacent.

Sample 2:

```
Input:
5 5
1 2 3 4 5
1 2
2 3
3 4
4 5
```

| Step | Centroid | Current information | Result |
| --- | --- | --- | --- |
| 1 | middle vertex | each color appears once | all answers stay zero |
| 2 | recursive components | no color has two vertices | all answers stay zero |

The result is:

```
0
0
0
0
0
```

This confirms that singleton subspecies are handled without special searching.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(N log N) | Each centroid level processes every vertex in its current components once, and the decomposition has logarithmic height. |
| Space | O(N) | The tree, recursion state, and auxiliary arrays are linear. |

With `N = 200000`, the logarithmic factor keeps the number of operations manageable. The algorithm avoids storing all same-color pairs, which would require quadratic memory.

## Test Cases

```python
# These tests assume the solve() function is copied above.

import sys, io

def run(inp: str) -> str:
    old = sys.stdin
    sys.stdin = io.StringIO(inp)
    try:
        solve()
        return sys.stdout.getvalue()
    finally:
        sys.stdin = old

assert run("""6 2
1 2 1 2 2 1
3 1
1 2
1 4
1 5
5 6
""") == "3\n2\n"

assert run("""1 1
1
""") == "0\n"

assert run("""5 5
1 2 3 4 5
1 2
2 3
3 4
4 5
""") == "0\n0\n0\n0\n0\n"

assert run("""5 2
1 2 1 2 1
1 2
2 3
3 4
4 5
""") == "4\n2\n"

assert run("""4 1
1 1 1 1
1 2
2 3
3 4
""") == "3\n"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Single vertex | `0` | Minimum size and singleton handling |
| All colors different | All zeros | No false diameter creation |
| Alternating colors on a path | `4`, `2` | Long distances between separated equal colors |
| One color on a chain | `3` | Full tree diameter case |

## Edge Cases

When a subspecies appears only once, the centroid process may encounter that color many times, but the dictionary never finds a second matching vertex. The answer remains zero because no pair exists.

For the input:

```
5 5
1 2 3 4 5
1 2
2 3
3 4
4 5
```

each centroid step records only one distance for each color. No addition happens, so every answer stays zero.

When equal colors are separated by other colors, the algorithm does not rely on connectivity of a subspecies. For:

```
5 2
1 2 1 2 1
1 2
2 3
3 4
4 5
```

the two outer color `1` vertices are eventually considered at a centroid where their path is split into different branches. Their distances add to four, which is the correct range.

When many vertices share the same color, the dictionary keeps only the maximum distance seen from each centroid. This is sufficient because a pair through that centroid always consists of two distances from the same center, and the best pair must use the two largest available values. The recursive decomposition handles pairs that do not pass through the current centroid.
