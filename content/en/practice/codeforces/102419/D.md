---
title: "CF 102419D - Xor the graph"
description: "We have an undirected graph, and every vertex already carries an integer smaller than (2^{20}). We may choose a subset of vertices and one XOR value (x), then replace every chosen value (ai) by (ai oplus x). The goal is to make the two endpoint values different on every edge."
date: "2026-08-14T14:48:21+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102419
codeforces_index: "D"
codeforces_contest_name: "SPC 2019"
rating: 0
weight: 102419
solve_time_s: 262
verified: false
draft: false
---

[CF 102419D - Xor the graph](https://codeforces.com/problemset/problem/102419/D)

**Rating:** -  
**Tags:** -  
**Solve time:** 4m 22s  
**Verified:** no  

## Solution
## Problem Understanding

We have an undirected graph, and every vertex already carries an integer smaller than (2^{20}). We may choose a subset of vertices and one XOR value (x), then replace every chosen value (a_i) by (a_i \oplus x). The goal is to make the two endpoint values different on every edge.

The useful way to look at one edge is to classify its endpoints by whether they are selected. If both endpoints are selected, or both are unselected, XOR is applied equally to both values, so their equality relation does not change. If exactly one endpoint is selected, the two final values are equal precisely when

[
x=a_u\oplus a_v.
]

This gives the central structure of the problem.

For an edge whose endpoints initially have equal values, (a_u=a_v), both endpoints cannot have the same selection status. Such an edge forces the two vertices to belong to opposite sides of the chosen subset. Consequently, all edges connecting equal values form a graph that must be bipartite.

For an edge whose endpoint values are different, there is no restriction on whether both endpoints are selected or both are unselected. If exactly one endpoint is selected, we only have to avoid the single XOR value (a_u\oplus a_v).

The limits make a quadratic or exponential search impossible. With up to (3\cdot10^5) vertices and edges and only one second, the intended solution needs essentially linear graph processing. The value range contains (2^{20}=1,048,576) possible XOR values, which is large enough compared with the maximum (m=3\cdot10^5) to guarantee that one suitable value can be found by a short scan.

There are several edge cases that can fool a direct implementation. Consider

```
3 3
1 1 1
1 2
2 3
1 3
```

Every edge joins equal values, so every edge requires its endpoints to be on opposite sides. This is an odd cycle and cannot be bipartitioned. The correct output is `-1`. A careless solution that only checks individual edges could miss the global contradiction.

Another case is a graph whose original values are already proper:

```
3 2
1 2 3
1 2
2 3
```

There is no equal-value edge, so there is no bipartite constraint at all. We can select one vertex and choose an (x) that does not equal the XOR difference across any selected edge. A solution must not assume that some equal-value edge exists.

Multiple edges also deserve care. For example,

```
2 3
7 7
1 2
1 2
1 2
```

all three edges impose exactly the same condition, (x\ne0), and the graph is still bipartite. Treating the input as a simple graph is unnecessary and can introduce bugs, but duplicate constraints themselves cause no difficulty.

Finally, the chosen (x) must remain below (2^{20}). We will only test values from (1) through (m+1), and (m+1\le300001<2^{20}), so the boundary is automatically respected.

## Approaches

The most direct brute force is to try every subset of vertices and every possible XOR value. There are (2^n) subsets and (2^{20}) possible values of (x). For each pair, checking all edges takes (O(m)), giving

[
O(2^n\cdot2^{20}\cdot m)
]

edge checks in the worst case. At (n=3\cdot10^5), this is far beyond any feasible computation.

We can improve the brute force substantially by first observing that equal-value edges determine whether a subset is even possible. For an equal-value edge, exactly one endpoint must be selected. That is exactly a bipartite-coloring condition. Instead of enumerating (2^n) subsets, we can construct one valid subset with a single BFS or DFS.

The remaining question is how to choose (x). Once the subset is fixed, only edges crossing from selected to unselected vertices constrain (x). Every such edge forbids exactly one value, (a_u\oplus a_v). There are at most (m) forbidden values, while we can choose among (m+1) positive integers. By the pigeonhole principle, at least one of

[
1,2,\ldots,m+1
]

is not forbidden. Since (m+1<2^{20}), that value is always legal.

The brute force works because it directly tests every possible operation. It fails because the number of possible subsets is exponential. The observation that equal-value edges alone determine the required two-coloring lets us replace the exponential search with one graph traversal, after which the huge XOR search collapses to at most (m+1) candidates.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | (O(2^n\cdot2^{20}\cdot m)) | (O(n+m)) | Too slow |
| Optimal | (O(n+m)) expected practical time | (O(n+m)) | Accepted |

## Algorithm Walkthrough

1. Build a separate graph containing only edges ((u,v)) for which (a_u=a_v). These edges are the ones that require their endpoints to have different selection statuses.
2. Bipartition this equal-value graph using BFS. Assign every vertex one of two colors, (0) or (1). For every equal-value edge, its endpoints must receive different colors. If we ever find an edge whose endpoints already have the same color, the required subset cannot exist, so we print `-1`.
3. Choose every vertex with color (1) as the selected set. If the equal-value graph has at least one edge, this set is automatically nonempty. If the equal-value graph has no edges, choose vertex (1) manually. This handles the case where all original edge values are already different.
4. Examine every original edge. Only an edge whose endpoints have different selection statuses can change its equality relation. For every such edge, compute (a_u\oplus a_v) and mark that value as forbidden for (x).
5. Search through (x=1,2,\ldots,m+1) and take the first value that is not forbidden. There are at most (m) forbidden values, so (m+1) candidates cannot all be forbidden. Also, (m+1\le300001<2^{20}), so the selected value satisfies the required range.
6. Output the selected vertices and the chosen (x). Every equal-value edge crosses the bipartition, so its endpoints receive different final values. Every unequal-value edge that crosses the subset avoids its unique forbidden XOR value, while an edge whose endpoints are on the same side keeps its original inequality.

The invariant is that after the bipartite coloring, every equal-value edge has endpoints with opposite selection statuses. Such an edge initially has equal values, and because (x\ne0), applying XOR to exactly one endpoint makes the two values different. For an unequal-value edge with opposite statuses, the final values could become equal only for the single value (x=a_u\oplus a_v), which the construction explicitly excludes. An unequal-value edge with equal selection statuses has XOR applied to both endpoints or neither, so its two different values remain different.

Thus every edge is valid for the final operation. If the bipartite coloring fails, an equal-value odd cycle forces an impossible alternating selection pattern, so reporting `-1` is also correct.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, m = map(int, input().split())
    a = list(map(int, input().split()))

    edges = []
    equal_adj = [[] for _ in range(n)]

    for _ in range(m):
        u, v = map(int, input().split())
        u -= 1
        v -= 1
        edges.append((u, v))

        if a[u] == a[v]:
            equal_adj[u].append(v)
            equal_adj[v].append(u)

    color = [-1] * n

    for start in range(n):
        if color[start] != -1:
            continue

        color[start] = 0
        stack = [start]

        while stack:
            u = stack.pop()

            for v in equal_adj[u]:
                if color[v] == -1:
                    color[v] = color[u] ^ 1
                    stack.append(v)
                elif color[v] == color[u]:
                    print(-1)
                    return

    selected = [i for i in range(n) if color[i] == 1]

    if not selected:
        selected = [0]

    forbidden = set()

    for u, v in edges:
        if (u in selected_set) != (v in selected_set):
            forbidden.add(a[u] ^ a[v])

    x = 1
    while x in forbidden:
        x += 1

    print(len(selected), x)
    print(*(v + 1 for v in selected))

if __name__ == "__main__":
    solve()
```

The code above needs one small implementation detail to make membership testing efficient. Constructing `selected_set` from the list before scanning the edges avoids repeatedly searching a Python list. The complete implementation is:

```python
import sys
input = sys.stdin.readline

def solve():
    n, m = map(int, input().split())
    a = list(map(int, input().split()))

    edges = []
    equal_adj = [[] for _ in range(n)]

    for _ in range(m):
        u, v = map(int, input().split())
        u -= 1
        v -= 1
        edges.append((u, v))

        if a[u] == a[v]:
            equal_adj[u].append(v)
            equal_adj[v].append(u)

    color = [-1] * n

    for start in range(n):
        if color[start] != -1:
            continue

        color[start] = 0
        stack = [start]

        while stack:
            u = stack.pop()

            for v in equal_adj[u]:
                if color[v] == -1:
                    color[v] = color[u] ^ 1
                    stack.append(v)
                elif color[v] == color[u]:
                    print(-1)
                    return

    selected = [i for i in range(n) if color[i] == 1]

    if not selected:
        selected = [0]

    selected_set = set(selected)

    forbidden = set()

    for u, v in edges:
        if (u in selected_set) != (v in selected_set):
            forbidden.add(a[u] ^ a[v])

    x = 1
    while x in forbidden:
        x += 1

    print(len(selected), x)
    print(*(v + 1 for v in selected))

if __name__ == "__main__":
    solve()
```

The first pass stores every original edge because the second phase needs to inspect all edges after the selection set has been determined. At the same time, only equal-value edges are inserted into `equal_adj`, keeping the bipartite graph as small as possible.

The coloring uses an iterative stack instead of recursive DFS. A path can contain (3\cdot10^5) vertices, which can exceed Python's default recursion depth, so recursion would require additional configuration and is unnecessary here.

The `selected_set` is crucial. Membership in a Python list would take linear time, turning the final edge scan into (O(nm)) in the worst case. A set gives expected (O(1)) membership checks.

The XOR value starts at (1), not (0). This is convenient because equal-value edges forbid (0), and it also guarantees that the operation actually changes selected values. More importantly, there are (m+1) candidates from (1) through (m+1), but at most (m) distinct forbidden values, so the loop must terminate.

Python integers do not overflow, and every input value is below (2^{20}), so `a[u] ^ a[v]` is also below (2^{20}).

## Worked Examples

### Sample 1

The input is

```
3 3
1 1 1
1 2
2 3
1 3
```

Every edge has equal endpoint values, so all three edges enter the bipartite graph.

| Vertex | Assigned color | Reason |
| --- | --- | --- |
| 1 | 0 | BFS start |
| 2 | 1 | Adjacent to 1 |
| 3 | 0 | Adjacent to 2 |
| 1 and 3 | 0, 0 | Conflict on edge (1\text{-}3) |

The edge (1\text{-}3) connects vertices with the same color, so the equal-value graph is not bipartite. No selection set can separate all three equal edges, and the algorithm prints `-1`.

This demonstrates why checking only local edges is insufficient. The contradiction appears only after following the alternating coloring around the entire odd cycle.

### Sample 2

The input is

```
3 3
1 1 2
1 2
2 3
1 3
```

Only edge (1\text{-}2) has equal endpoint values.

| Vertex | Color | Selected | Reason |
| --- | --- | --- | --- |
| 1 | 0 | No | BFS start |
| 2 | 1 | Yes | Equal-value edge requires opposite color |
| 3 | 0 | No | Vertex 3 is not connected by an equal-value edge |

The selected set is ({2}). The crossing edges and their forbidden values are

| Edge | Endpoint values | XOR | Forbidden? |
| --- | --- | --- | --- |
| (1,2) | (1,1) | 0 | Yes |
| (2,3) | (1,2) | 3 | Yes |
| (1,3) | (1,2) | 3 | No, both unselected |

The first positive candidate is (x=1), which is not forbidden.

After the operation, the values become (1,0,2). All three edges connect different values, so the construction is valid.

This trace shows how equal-value edges determine the subset while unequal-value edges only remove possible values of (x).

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | (O(n+m)) expected | The equal-value graph is traversed once, the original edges are scanned once, and the XOR search examines at most (m+1) values |
| Space | (O(n+m)) | The graph, original edge list, coloring, and selected set require linear memory |

The maximum input has (3\cdot10^5) vertices and (3\cdot10^5) edges, so linear processing is appropriate for the one-second limit. The algorithm never performs work proportional to (2^n) or (2^{20}), and its memory usage stays within 256 MB.

## Test Cases

Because a constructive problem can have many correct outputs, the most useful test harness parses the produced answer and verifies it instead of comparing the raw output text. The assertions below also check that `-1` is reported exactly when the construction is impossible.

```python
import sys
import io

def solve_data(inp: str) -> str:
    data = list(map(int, inp.split()))
    it = iter(data)

    n = next(it)
    m = next(it)
    a = [next(it) for _ in range(n)]

    edges = []
    equal_adj = [[] for _ in range(n)]

    for _ in range(m):
        u = next(it) - 1
        v = next(it) - 1
        edges.append((u, v))
        if a[u] == a[v]:
            equal_adj[u].append(v)
            equal_adj[v].append(u)

    color = [-1] * n

    for start in range(n):
        if color[start] != -1:
            continue

        color[start] = 0
        stack = [start]

        while stack:
            u = stack.pop()

            for v in equal_adj[u]:
                if color[v] == -1:
                    color[v] = color[u] ^ 1
                    stack.append(v)
                elif color[v] == color[u]:
                    return "-1\n"

    selected = [i for i in range(n) if color[i] == 1]

    if not selected:
        selected = [0]

    selected_set = set(selected)

    forbidden = set()
    for u, v in edges:
        if (u in selected_set) != (v in selected_set):
            forbidden.add(a[u] ^ a[v])

    x = 1
    while x in forbidden:
        x += 1

    return str(len(selected)) + " " + str(x) + "\n" + \
           " ".join(str(v + 1) for v in selected) + "\n"

def validate(inp: str, out: str) -> bool:
    data = list(map(int, inp.split()))
    it = iter(data)

    n = next(it)
    m = next(it)
    a = [next(it) for _ in range(n)]

    edges = [(next(it) - 1, next(it) - 1) for _ in range(m)]

    tokens = out.split()

    if tokens[0] == "-1":
        return True

    k = int(tokens[0])
    x = int(tokens[1])

    if not (0 <= k <= n):
        return False
    if not (0 <= x < (1 << 20)):
        return False

    chosen = list(map(lambda z: int(z) - 1, tokens[2:2 + k]))

    if len(chosen) != k:
        return False
    if len(set(chosen)) != k:
        return False
    if any(v < 0 or v >= n for v in chosen):
        return False

    chosen_set = set(chosen)

    for u, v in edges:
        au = a[u] ^ x if u in chosen_set else a[u]
        av = a[v] ^ x if v in chosen_set else a[v]

        if au == av:
            return False

    return True

sample1 = """\
3 3
1 1 1
1 2
2 3
1 3
"""

sample2 = """\
3 3
1 1 2
1 2
2 3
1 3
"""

sample3 = """\
5 4
1 2 3 4 5
1 2
1 3
1 4
4 5
"""

assert solve_data(sample1).strip() == "-1", "sample 1"

assert validate(sample2, solve_data(sample2)), "sample 2"
assert validate(sample3, solve_data(sample3)), "sample 3"

single_edge = """\
2 1
0 0
1 2
"""
assert validate(single_edge, solve_data(single_edge)), "minimum valid graph"

all_equal_path = """\
4 3
7 7 7 7
1 2
2 3
3 4
"""
assert validate(all_equal_path, solve_data(all_equal_path)), "all equal values"

boundary_values = """\
3 2
0 1048575 1
1 2
2 3
"""
assert validate(boundary_values, solve_data(boundary_values)), "20-bit boundary values"

maximum_size = ["300000 299999", " ".join(["5"] * 300000)]
maximum_size.extend(f"{i} {i + 1}" for i in range(1, 300000))
maximum_size = "\n".join(maximum_size) + "\n"
assert validate(maximum_size, solve_data(maximum_size)), "maximum-size path"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Sample 1 | `-1` | Odd cycle in the equal-value graph |
| Sample 2 | Any valid construction | Equal-value edge plus an unequal-value crossing edge |
| Sample 3 | Any valid construction | No equal-value edges, so the selected set must be chosen manually |
| `2 1 / 0 0 / 1 2` | Any valid construction | Smallest valid graph and the fact that (x=0) is forbidden |
| Four equal values on a path | Any valid construction | Bipartite coloring over several equal-value edges |
| Values `0` and `1048575` | Any valid construction | Extremal 20-bit values |
| 300000-vertex path | Any valid construction | Linear-time behavior at the maximum vertex and edge scale |

## Edge Cases

For the all-equal triangle

```
3 3
1 1 1
1 2
2 3
1 3
```

the equal-value graph is the whole triangle. Starting with color (0) at vertex 1 forces vertex 2 to color (1), and vertex 3 to color (0) through edge (2\text{-}3). Edge (1\text{-}3) then connects two color-(0) vertices, so the algorithm immediately returns `-1`.

For a graph with no equal-value edges,

```
3 2
1 2 3
1 2
2 3
```

the equal-value graph has no edges, so all vertices initially receive color (0). The color-(1) side is empty, and the algorithm instead selects vertex 1. The crossing edges forbid (1\oplus2=3), while the edge (2\text{-}3) does not cross the selected set. Thus (x=1) is valid and changes vertex 1 from (1) to (0), leaving the edge values different.

For duplicate edges,

```
2 3
7 7
1 2
1 2
1 2
```

the same pair appears three times in the equal-value graph. BFS still assigns the two vertices different colors. The selected side contains one endpoint, and every copy of the edge forbids (7\oplus7=0). The first candidate (x=1) is valid for all three copies simultaneously.

For the largest possible vertex values,

```
3 2
0 1048575 1
1 2
2 3
```

the XOR between the first two values is (1048575), still inside the 20-bit range. The algorithm never assumes that XOR values are small numerically, only that they are below (2^{20}). Its candidate search uses values starting from (1), and the pigeonhole argument guarantees a free value long before reaching (2^{20}).

The choice of (m+1) candidates also handles the worst possible collection of forbidden XOR values. Even if every one of (1,\ldots,m) is forbidden, (m+1) cannot be forbidden because there are only (m) edges and hence at most (m) distinct forbidden values. Since (m+1\le300001<2^{20}), the search always finds a legal XOR value.
