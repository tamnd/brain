---
title: "CF 102215D - Country Division"
description: "We have a tree of cities. For each prediction, some vertices are red, some are blue, and all remaining vertices are neutral. We may remove any roads we like."
date: "2026-08-18T11:50:13+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102215
codeforces_index: "D"
codeforces_contest_name: "2019, XII Samara Regional Intercollegiate Programming Contest"
rating: 0
weight: 102215
solve_time_s: 328
verified: true
draft: false
---

[CF 102215D - Country Division](https://codeforces.com/problemset/problem/102215/D)

**Rating:** -  
**Tags:** -  
**Solve time:** 5m 28s  
**Verified:** yes  

## Solution
## Problem Understanding

We have a tree of cities. For each prediction, some vertices are red, some are blue, and all remaining vertices are neutral. We may remove any roads we like. After removing them, every red city must still belong to one connected component, every blue city must belong to another connected component, and no red city may be connected to any blue city.

The key difficulty is that the roads we remove are shared by many possible paths. Connecting two red cities may force us to keep roads through neutral cities, and those neutral cities can become part of the red region. The same happens for blue cities. The question is really whether the minimal connected subtree containing all red vertices can be made disjoint from the minimal connected subtree containing all blue vertices. The official input has up to (200000) cities and the total number of colored vertices over all predictions is also at most (200000).

For (n=200000), an (O(n^2)) algorithm is far beyond the two second limit. The useful target is roughly (O(n\log n)) preprocessing followed by (O((r+b)\log n)) work per prediction, because the total (r+b) over every prediction is only (200000). We can afford logarithmic work for each colored city, but we cannot afford to scan all (n) cities for every prediction.

There are several edge cases that defeat simpler interpretations of the problem. First, a red and a blue Steiner subtree can meet at a neutral city even though no city has both colors. For example:

```
5
1 2
1 3
2 4
3 5
1
2 2 4 5 3
```

Here the red cities are (2,4), and the blue cities are (5,3). The red connection uses (2-1), while the blue connection uses (3-1), so both connected regions contain city (1). The correct answer is `NO`. A careless solution that only checks whether the explicitly colored vertices overlap would incorrectly return `YES`.

The same phenomenon appears in the first sample. For the second prediction, the red cities are (4,6) and the blue cities are (5,7). Their colored vertices are completely separate, but both required connections pass through city (1), so the answer is `NO`.

A second edge case occurs when one color's required subtree contains the other color's LCA. Consider the chain

```
4
1 2
2 3
3 4
1
2 1 1 3 4
```

The red cities are (1,3), so their required subtree contains (1,2,3). The blue city is (4). These can be separated by cutting edge (3-4), so the answer is `YES`. The fact that the red LCA is an ancestor of the blue vertex does not by itself make the answer negative.

The opposite case is

```
4
1 2
2 3
3 4
1
2 1 1 4 3
```

The red cities are (1,4), while blue is (3). The red path is the entire chain and necessarily contains the blue city, so the answer is `NO`. A test that only compares the two LCA vertices would miss this.

## Approaches

A direct brute-force approach is possible conceptually. For every road, remove that road and inspect the two resulting components. We could check whether all red cities are on one side and all blue cities are on the other side, and whether the red and blue groups are each connected. Since there are (n-1) candidate roads and a full verification can inspect (O(n)) cities, one prediction can take (O(n^2)) time. The number of predictions can be as large as (100000), because every prediction contains at least one red and one blue city while the total number of colored cities is bounded by (200000). A worst-case construction can consequently reach about (10^5\cdot 2\cdot 10^5=2\cdot10^{10}) vertex checks, which is nowhere close to feasible.

The brute force works because a valid division of a tree is always represented by cutting edges between connected components. The problem is finding those components without explicitly considering every edge.

The useful observation is that, inside a tree, there is only one path between any two cities. Consequently, if several red cities have to remain connected, every path between them is forced. Their union is a unique minimal connected subtree. The same is true for the blue cities. This is exactly the tree version of a Steiner subtree, the minimal connected subgraph containing a specified set of terminals.

If the two required subtrees are vertex-disjoint, we can keep every edge inside each subtree and cut the edges separating them from the rest of the tree. The red cities remain connected, the blue cities remain connected, and the two groups cannot reach each other. If the two subtrees intersect, no choice of road removals can help, because every connected component containing all red cities must contain the red subtree, and every connected component containing all blue cities must contain the blue subtree.

Now root the tree at city (1). For any set of vertices, let its LCA be the lowest common ancestor of all vertices in that set. If (A) is the LCA of all red cities, every red vertex lies in the subtree of (A). Similarly, if (B) is the LCA of all blue cities, every blue vertex lies in the subtree of (B).

There are then only two structural possibilities. If neither (A) nor (B) is an ancestor of the other, their rooted subtrees are disjoint, so the two required subtrees are disjoint and the answer is `YES`. If (A) is an ancestor of (B), the blue required subtree lies inside the subtree of (B). The only way the red required subtree can intersect it is for some red city itself to lie inside the subtree of (B). The symmetric argument applies when (B) is an ancestor of (A).

This gives the same LCA-based characterization used by known solutions for this problem.

We can find the LCA of two vertices in (O(\log n)) using binary lifting. The LCA of an entire color class is then obtained incrementally: start with the first red city and repeatedly replace the current LCA with the LCA of it and the next red city. The same process gives the blue LCA. Because the total number of colored cities across all predictions is at most (200000), this is fast enough.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | (O(qn^2)) in the direct form | (O(n)) | Too slow |
| Optimal | (O(n\log n + S\log n)), where (S\le 200000) is the total number of colored cities | (O(n\log n)) | Accepted |

## Algorithm Walkthrough

1. Root the tree at city (1), and compute the depth and immediate parent of every city. The parent relation gives us the structure needed for LCA queries.
2. Build a binary lifting table. `up[k][v]` stores the ancestor of (v) that is (2^k) edges above it. This lets us move upward by large distances in logarithmically many operations.
3. For each prediction, read all red cities and compute their common LCA incrementally. Start with the first red city as `red_lca`. For every following red city (x), set `red_lca = LCA(red_lca, x)`. The resulting vertex is the lowest vertex that is an ancestor of every red city.
4. Do the same for all blue cities and obtain `blue_lca`.
5. Compute `common = LCA(red_lca, blue_lca)`. If `common` is different from both LCAs, then neither color LCA is an ancestor of the other. The two required regions lie in different child subtrees of `common`, so output `YES`.
6. If `red_lca == common`, then the red LCA is an ancestor of the blue LCA. The blue required subtree is contained in the subtree rooted at `blue_lca`. Check every red city (x). If `LCA(x, blue_lca) == blue_lca`, then (x) lies inside the blue-LCA subtree. Since the red subtree must connect (x) to the other red cities, it reaches `blue_lca`, which belongs to the blue required subtree. The regions intersect, so output `NO`. If no red city lies there, output `YES`.
7. The remaining case is `blue_lca == common`, so the blue LCA is an ancestor of the red LCA. Perform the symmetric test on every blue city, checking whether `LCA(x, red_lca) == red_lca`. An intersection gives `NO`; otherwise the two required regions are disjoint and the answer is `YES`.

The invariant behind the algorithm is that `red_lca` and `blue_lca` always describe the forced root of their respective required connected subtrees. When the two LCAs are in separate rooted subtrees, the required regions cannot meet. When one LCA contains the other, intersection can happen only inside the descendant LCA's subtree, and that intersection exists exactly when the opposite color has a terminal there. This characterizes every possible arrangement, so every `YES` corresponds to a realizable set of road cuts and every `NO` corresponds to an unavoidable intersection.

## Python Solution

```python
import sys
from array import array

input = sys.stdin.readline

def solve(reader=None):
    input = reader if reader is not None else sys.stdin.readline

    n = int(input())

    graph = [[] for _ in range(n + 1)]
    for _ in range(n - 1):
        u, v = map(int, input().split())
        graph[u].append(v)
        graph[v].append(u)

    # Root the tree at 1.
    parent = array('i', [0]) * (n + 1)
    depth = array('i', [0]) * (n + 1)

    parent[1] = 1
    stack = [1]

    while stack:
        u = stack.pop()
        pu = parent[u]
        du = depth[u] + 1

        for v in graph[u]:
            if v == pu:
                continue
            parent[v] = u
            depth[v] = du
            stack.append(v)

    # Binary lifting table.
    log = n.bit_length()
    up = [parent]

    for _ in range(1, log):
        prev = up[-1]
        cur = array('i', (prev[prev[v]] for v in range(n + 1)))
        up.append(cur)

    def lca(a, b):
        if depth[a] < depth[b]:
            a, b = b, a

        diff = depth[a] - depth[b]
        bit = 0

        while diff:
            if diff & 1:
                a = up[bit][a]
            diff >>= 1
            bit += 1

        if a == b:
            return a

        for k in range(log - 1, -1, -1):
            ua = up[k][a]
            ub = up[k][b]
            if ua != ub:
                a = ua
                b = ub

        return up[0][a]

    q = int(input())
    answers = []

    for _ in range(q):
        parts = list(map(int, input().split()))
        r, b = parts[0], parts[1]

        red = parts[2:2 + r]
        blue = parts[2 + r:2 + r + b]

        red_lca = red[0]
        for x in red[1:]:
            red_lca = lca(red_lca, x)

        blue_lca = blue[0]
        for x in blue[1:]:
            blue_lca = lca(blue_lca, x)

        common = lca(red_lca, blue_lca)

        if red_lca != common and blue_lca != common:
            answers.append("YES")
            continue

        if red_lca == common:
            possible = True

            for x in red:
                if lca(x, blue_lca) == blue_lca:
                    possible = False
                    break

            answers.append("YES" if possible else "NO")
        else:
            possible = True

            for x in blue:
                if lca(x, red_lca) == red_lca:
                    possible = False
                    break

            answers.append("YES" if possible else "NO")

    return "\n".join(answers)

if __name__ == "__main__":
    sys.stdout.write(solve())
```

The adjacency list stores the original tree. The DFS is iterative rather than recursive because a tree can be a chain of length (200000), which would exceed Python's normal recursion depth.

The `parent` array is a compact integer array instead of a Python list. The same representation is used for every binary lifting level. This matters under the (256) MB memory limit because a Python list of (200000) integers carries substantially more overhead than a packed integer array. Python's `array` type stores fixed-size numeric elements compactly.

The root has itself as its parent. Thus repeated jumps above the root remain at vertex (1), which makes the LCA implementation simple and avoids special handling for zero ancestors.

The LCA function first equalizes depths using the binary representation of their difference. After that, it considers jumps from the largest power of two downward. If the two corresponding ancestors differ, both vertices can safely jump upward because their LCA is strictly above those ancestors. When no larger jump is possible, their immediate parent is the LCA.

For each query, the red and blue lists are sliced directly from the input line. The constraints guarantee that a complete query fits on one input line. The lists are retained because, in the ancestor case, we must inspect every terminal of the opposite color.

There is no integer overflow issue in Python. The largest values used as vertex identifiers, depths, and table entries are at most (200000).

The use of `array('i')` also keeps the (O(n\log n)) binary lifting table compact. The table has roughly (200000\cdot18) integer entries, and each packed integer occupies four bytes on the usual implementation, so the table itself is only around fifteen megabytes rather than hundreds of megabytes of Python integer objects.

## Worked Examples

The first trace uses the first prediction of Sample 1.

The tree is rooted at (1). The red vertices are (2,4), so their common LCA is (2). The blue vertices are (6,7), so their common LCA is (3).

| Stage | Red LCA | Blue LCA | Common LCA | Decision |
| --- | --- | --- | --- | --- |
| Start with red (2) | 2 |  |  |  |
| Add red (4) | 2 |  |  |  |
| Start with blue (6) | 2 | 6 |  |  |
| Add blue (7) | 2 | 3 |  |  |
| Compute `LCA(2,3)` | 2 | 3 | 1 | `YES` |

Since (1) is different from both (2) and (3), the two color LCAs are in different child subtrees of the root. The red required subtree is (2-4), while the blue required subtree is (3-6) and (3-7). They are disjoint, so roads can be cut between those regions and the answer is `YES`.

The second trace uses Sample 1's second prediction. Its red vertices are (4,6), while its blue vertices are (5,7).

| Stage | Red LCA | Blue LCA | Common LCA | Decision |
| --- | --- | --- | --- | --- |
| Start with red (4) | 4 |  |  |  |
| Add red (6) | 1 |  |  |  |
| Start with blue (5) | 1 | 5 |  |  |
| Add blue (7) | 1 | 1 |  |  |
| Compute `LCA(1,1)` | 1 | 1 | 1 | Ancestor case |
| Check red (4) | 1 | 1 | `LCA(4,1)=1` | `NO` |

Here both color LCAs are (1). The red required subtree contains the path between (4) and (6), which passes through (1). The blue required subtree contains the path between (5) and (7), which also passes through (1). The common vertex is unavoidable, so no road blocking can separate the two groups.

As a second independent example, consider this chain:

```
5
1 2
2 3
3 4
4 5
2
2 1 1 3 5
2 1 1 5 3
```

The first query has red (1,3) and blue (5). The red LCA is (1), the blue LCA is (5), and `LCA(1,5)=1`. The red LCA is the ancestor case, but neither red city is inside the subtree of (5), so the result is `YES`.

The second query has red (1,5) and blue (3). The red LCA is (1), the blue LCA is (3), and again the red LCA is the ancestor. This time red city (5) satisfies `LCA(5,3)=3`, meaning it lies inside the subtree rooted at (3). The red path is forced through city (3), so the result is `NO`.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | (O(n\log n + S\log n)) | Building binary lifting takes (O(n\log n)); every colored city participates in only a constant number of LCA operations, and (S\le200000) |
| Space | (O(n\log n)) | The lifting table contains (O(n\log n)) packed integers, while the tree and query storage use (O(n)) additional space |

With (n\le200000), the preprocessing has about eighteen binary lifting levels. The total number of colored cities is also at most (200000), so the query work remains bounded by a few million logarithmic ancestor operations. The iterative traversal avoids recursion depth problems, and the packed lifting table keeps memory comfortably within the (256) MB limit.

## Test Cases

The following test harness assumes the solution above is saved as `solution.py`. It calls the same `solve` function with a `StringIO` reader, so the assertions exercise the actual implementation rather than a separate reference algorithm.

```
# solution.py must contain the solve(reader=None) function from above.

import io
from solution import solve

def run(inp: str) -> str:
    return solve(io.StringIO(inp).readline)

# Provided sample
sample1 = """\
7
1 2
1 3
2 4
2 5
3 6
3 7
6
2 2 4 5 6 7
2 2 4 6 5 7
2 1 4 5 2
2 1 4 5 1
1 1 1 2
6 1 1 2 3 4 5 6 7
"""

assert run(sample1) == """\
YES
NO
NO
YES
YES
YES
""".strip(), "sample 1"

# Minimum-size tree. With two cities, one red and one blue,
# cutting the only road always separates them.
assert run("""\
2
1 2
1
1 1 1 2
""") == "YES", "minimum-size tree"

# A chain where the red path contains the blue city.
assert run("""\
5
1 2
2 3
3 4
4 5
1
2 1 1 5 3
""") == "NO", "intersection on a required path"

# A chain where the groups can be separated at one edge.
assert run("""\
5
1 2
2 3
3 4
4 5
1
2 1 1 3 5
""") == "YES", "ancestor case with valid separation"

# Every city is colored. Red leaves must connect through the blue center,
# so the answer is NO.
assert run("""\
5
1 2
1 3
1 4
1 5
1
4 1 2 3 4 5
""") == "NO", "all cities colored"

# Maximum-size test. The tree is a star with 199999 red leaves and
# the center blue. Connecting all red leaves forces the blue center
# into the red component.
n = 200000
edges = "\n".join(f"1 {v}" for v in range(2, n + 1))
red = " ".join(map(str, range(2, n + 1)))

max_case = (
    f"{n}\n"
    f"{edges}\n"
    "1\n"
    f"{n - 1} 1 {red} 1\n"
)

assert run(max_case) == "NO", "maximum-size star"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| (n=2), one red and one blue | `YES` | Minimum tree and the fact that a single separating edge is sufficient |
| Chain with red (1,5) and blue (3) | `NO` | A neutral or opposite-colored city lying on a forced red path |
| Chain with red (1,3) and blue (5) | `YES` | The ancestor case where the two required subtrees still separate |
| Star with every city colored | `NO` | All cities colored and a forced intersection at the center |
| Star with (200000) cities | `NO` | Maximum (n), maximum query size, and memory/time behavior |

The statement requires all city identifiers inside a prediction to be distinct, so a literal test where all input city values are equal is invalid. The all-colored star is the relevant boundary case: every city belongs to one of the two color classes, leaving no neutral city that can absorb an intersection.

## Edge Cases

For a single red city and a single blue city, each required subtree consists only of its colored vertex. Since the two city identifiers are distinct, the two subtrees cannot intersect. The algorithm gets `red_lca = red`, `blue_lca = blue`, and their LCA is one of them, so it reaches the ancestor case. The containment check fails because the opposite colored city cannot be inside its own distinct vertex's subtree. The answer is `YES`.

For an intersection at a neutral vertex, consider

```
5
1 2
1 3
2 4
3 5
1
2 2 4 5 3
```

The red LCA is (2), because red cities are (2,4). The blue LCA is (3), because blue cities are (5,3). Their common LCA is (1), different from both. At first glance this looks like the separated case, but the red required subtree is (2-4), while the blue required subtree is just (3-5). They do not actually intersect, so the correct answer is `YES` for this particular input.

To exercise the genuine neutral intersection, use

```
5
1 2
1 3
2 4
3 5
1
2 2 5 4 3
```

The red cities are (5,4), so their LCA is (1). The blue cities are (3,4) would violate distinct colors, so instead the clean example is the sample structure with red (4,6) and blue (5,7):

```
7
1 2
1 3
2 4
2 5
3 6
3 7
1
2 2 4 6 5 7
```

The red LCA is (1), the blue LCA is (1), and the algorithm enters the ancestor case immediately. Checking red city (4) against blue LCA (1) gives `LCA(4,1)=1`, so the intersection is detected and the output is `NO`.

For an ancestor relationship that is still separable, consider

```
5
1 2
2 3
3 4
4 5
1
2 1 1 3 5
```

The red LCA is (1), the blue LCA is (5), and the common LCA is (1). The algorithm checks whether either red city lies in the subtree of (5). Neither does, so it returns `YES`. Cutting edge (4-5) separates the blue city while leaving the red cities connected.

For the opposite case,

```
5
1 2
2 3
3 4
4 5
1
2 1 1 5 3
```

the red LCA is (1), the blue LCA is (3), and the common LCA is (1). Red city (5) lies in the subtree rooted at (3), which is detected by `LCA(5,3) == 3`. The red connection must pass through the blue city (3), so the algorithm returns `NO`.

Finally, the maximum-size star

```
200000
1 2
1 3
...
1 200000
1
199999 1 2 3 ... 200000 1
```

has every leaf red and the center blue. The LCA of all red cities is (1), which is also the blue LCA. The first red leaf already satisfies `LCA(2,1) == 1`, so the query terminates with `NO`. This demonstrates that the algorithm can reject a large query immediately once it finds the forced intersection, while still handling the full (200000)-vertex input within the intended asymptotic bounds.
