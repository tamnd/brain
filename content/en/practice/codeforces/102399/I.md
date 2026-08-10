---
title: "CF 102399I - \u0416\u0443\u043b\u0438\u043a, \u043d\u0435 \u0432\u043e\u0440\u0443\u0439"
description: "We have a connected simple undirected graph. Swiper chooses a nonempty proper set of vertices and removes those vertices together with all incident edges. The remaining vertices must keep the same degree modulo (3) that they had before the removal."
date: "2026-08-10T17:23:57+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102399
codeforces_index: "I"
codeforces_contest_name: "2019 \u041c\u043e\u0441\u043a\u043e\u0432\u0441\u043a\u0430\u044f \u043a\u043e\u043c\u0430\u043d\u0434\u043d\u0430\u044f \u043e\u043b\u0438\u043c\u043f\u0438\u0430\u0434\u0430 \u0448\u043a\u043e\u043b\u044c\u043d\u0438\u043a\u043e\u0432, \u043b\u0438\u0433\u0430 A"
rating: 0
weight: 102399
solve_time_s: 671
verified: true
draft: false
---

[CF 102399I - \u0416\u0443\u043b\u0438\u043a, \u043d\u0435 \u0432\u043e\u0440\u0443\u0439](https://codeforces.com/problemset/problem/102399/I)

**Rating:** -  
**Tags:** -  
**Solve time:** 11m 11s  
**Verified:** yes  

## Solution
## Problem Understanding

We have a connected simple undirected graph. Swiper chooses a nonempty proper set of vertices and removes those vertices together with all incident edges. The remaining vertices must keep the same degree modulo (3) that they had before the removal.

Let (S) be the stolen vertices and let (R=V\setminus S) be the vertices that remain. For every (v\in R), exactly the edges from (v) to (S) disappear. Hence the condition is

[
\deg_S(v)\equiv 0\pmod 3.
]

Since (\deg_G(v)=\deg_R(v)+\deg_S(v)), the same condition can be written as

[
\deg_R(v)\equiv\deg_G(v)\pmod 3.
]

This second form is much easier to construct with. We will build a suitable set (R) of vertices that remain, and then steal every vertex outside (R).

The original Codeforces version has (n,m\le 500000), with the sums of (n) and (m) over all test cases also bounded by (500000). The original contest limits are 2 seconds and 512 MB. This immediately rules out anything quadratic in the graph size, and even a traversal repeated a linear number of times would be too expensive. The target is (O(n+m)) per graph, up to a constant number of graph traversals.

There are several small cases where an implementation can silently produce an invalid answer. With one vertex,

```
1
1 0
```

the graph has no proper nonempty subset to steal, so the answer is `No`. A program that blindly sees a degree divisible by (3) and keeps that vertex would accidentally try to steal zero vertices.

For two connected vertices,

```
1
2 1
1 2
```

both degrees are (1). The only nonempty proper stolen set has one vertex, but the output requires at least two stolen vertices. The correct answer is `No`.

A cycle also needs special treatment. For

```
1
4 4
1 2
2 3
3 4
4 1
```

every vertex has degree (2). The entire graph is a valid retained cycle, but retaining the entire graph means stealing nothing. Any proper subset of a cycle contains a path whose endpoints have internal degree (1), which does not match the original residue (2). Thus the answer is `No`.

A fourth subtle case is a graph with a vertex of degree divisible by (3). For example,

```
1
4 3
1 2
1 3
1 4
```

vertex (1) has degree (3). Keeping only vertex (1) is valid because all three incident edges disappear, and (3\equiv0\pmod3). Consequently the three leaves can be stolen.

## Approaches

The direct brute force is conceptually simple. Enumerate every nonempty proper subset (S) of vertices, count for every vertex outside (S) how many of its neighbors belong to (S), and check that every such count is divisible by (3). This is correct because it tests exactly the definition of a legal theft. There are (2^n-2) possible subsets, and checking one subset takes (O(n+m)) time if the graph is represented by adjacency lists. The worst-case complexity is therefore

[
O(2^n(n+m)).
]

For (n=500000), this is not merely too slow, it is completely infeasible.

The useful observation is to stop thinking about arbitrary subsets. For every remaining vertex (v), its internal degree must have the same residue modulo (3) as its original degree. That means vertices with original degree residue (0), (1), and (2) naturally suggest different small structures that can be kept.

Call these three types (Z,A,B), according to degree modulo (3).

A (Z)-vertex can be kept alone. Its internal degree is (0), exactly the required residue.

Two (A)-vertices connected by a suitable path can be kept. The two endpoints have one internal edge, and every internal (B)-vertex has two internal edges. A shortest path between two (A)-vertices gives exactly this structure.

A cycle consisting of (B)-vertices can be kept. Every cycle vertex has two internal edges, matching residue (2). Choosing a shortest cycle makes it chordless, so every cycle vertex really has exactly two neighbors inside the chosen set.

If none of those structures exists, there is exactly one (A)-vertex and the (B)-vertices form a forest. Each tree component must touch the unique (A)-vertex at least twice. Two such components give two paths from the (A)-vertex back to itself, forming two cycles that share only the (A)-vertex. Keeping those two paths and the (A)-vertex gives internal degree (4) at the (A)-vertex, which is again (1\bmod3), while every (B)-vertex on the paths has internal degree (2).

These cases are exhaustive. The official problem is the Codeforces 1239F problem, and this classification is the central constructive idea behind accepted solutions.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | (O(2^n(n+m))) | (O(n+m)) | Too slow |
| Optimal | (O(n+m)) | (O(n+m)) | Accepted |

## Algorithm Walkthrough

1. Compute the degree of every vertex and classify it by `degree % 3`. The three classes are (Z), (A), and (B). The classification tells us what internal degree a retained vertex must have modulo (3).
2. If there is a (Z)-vertex (v), keep only (v). Its internal degree is zero, matching its original degree modulo (3). If (n>2), stealing every other vertex gives a valid answer. For (n=1) there is nothing to steal, and (n=2) cannot contain a (Z)-vertex in a connected graph.
3. Look for a cycle entirely inside the (B)-vertices. A cycle gives every selected vertex exactly two selected neighbors, which is the required residue for a (B)-vertex. We need the cycle to be chordless, so we find a shortest cycle in the DFS-tree sense. A non-tree edge between an ancestor and a descendant creates a fundamental cycle, and choosing the one with minimum tree-distance gives a cycle with no chord.
4. If such a cycle exists and does not use every vertex, steal its complement. If the cycle is the entire graph, the graph is exactly a cycle and no proper solution exists through this construction. We continue to the next cases only if the complement would not satisfy the required output size.
5. If there are at least two (A)-vertices, run BFS from one (A)-vertex through the graph and stop when another (A)-vertex is reached. The resulting path is shortest, so it cannot contain another (A)-vertex internally. Its two endpoints have one internal neighbor, while its internal (B)-vertices have two internal neighbors. Keep this path and steal everything else.
6. If the previous constructions failed, there is no (Z)-vertex, there is no (B)-cycle, and there is at most one (A)-vertex. Because the graph is connected and has more than one vertex, there must actually be exactly one (A)-vertex. Every other vertex is (B), and the subgraph induced by (B)-vertices is a forest.
7. Consider one connected component (T) of this (B)-forest. Suppose it has (r) edges going from its vertices to the unique (A)-vertex. Since every (B)-vertex has degree (2\bmod3),

[
2|V(T)|\equiv 2|E(T)|+r\pmod3.
]

Because (T) is a tree, (|E(T)|=|V(T)|-1). Substituting gives

[
r\equiv2\pmod3.
]

Thus every (B)-tree has at least two edges to the (A)-vertex. There must also be at least two such components, because the degree of the unique (A)-vertex is (1\bmod3), whereas one component would contribute (2\bmod3).

1. In two different (B)-components, choose two vertices adjacent to the (A)-vertex. In each component, start from one such vertex and find the nearest other vertex adjacent to (A). The path between them contains no other (A)-neighbor internally, so adding the (A)-vertex turns that path into a clean cycle. Keep both paths and the (A)-vertex.
2. If the resulting retained set is proper and leaves at least two stolen vertices, output its complement. If it is the entire graph, the graph consists of exactly two (A)-to-(A) paths joined at (A), and no legal proper retained set exists in this final case. The earlier constructions would already have handled every other possibility.

Why it works: for every construction, the degree inside the retained set has exactly the same residue as the original degree. A (Z)-vertex has internal degree (0). A retained (A)-to-(A) path gives internal degree (1) at its endpoints and (2) at its (B)-internal vertices. A chordless (B)-cycle gives internal degree (2) everywhere. In the final construction, each selected (B)-path has internal degree (2) at its (B)-vertices, while the unique (A)-vertex has four selected neighbors. Since (4\equiv1\pmod3), its residue is also preserved.

The exhaustion argument follows the same structure. If a (Z)-vertex exists, the first construction works. Otherwise, a (B)-cycle gives the second construction. Otherwise, two (A)-vertices give the third construction. If none of these happens, there is exactly one (A)-vertex and the (B)-subgraph is a forest, which forces the final structure. If that final structure occupies the whole graph, any valid retained set would have to contain the unique (A)-vertex and at least two (B)-components, forcing both complete paths to remain, so no proper solution exists.

## Python Solution

```python
import sys
from collections import deque

input = sys.stdin.readline

def make_answer(n, keep):
    mark = bytearray(n)
    for v in keep:
        mark[v] = 1

    stolen = [v + 1 for v in range(n) if not mark[v]]

    if 1 < len(stolen) < n:
        return stolen
    return None

def find_b_cycle(g, typ):
    n = len(g)

    color = bytearray(n)
    parent = [-1] * n
    depth = [0] * n
    tin = [-1] * n
    tout = [-1] * n

    timer = 0

    for s in range(n):
        if typ[s] != 2 or color[s]:
            continue

        color[s] = 1
        tin[s] = timer
        timer += 1

        stack = [(s, 0)]

        while stack:
            u, idx = stack[-1]

            if idx == len(g[u]):
                color[u] = 2
                tout[u] = timer
                stack.pop()
                continue

            v = g[u][idx]
            stack[-1] = (u, idx + 1)

            if typ[v] != 2:
                continue

            if color[v] == 0:
                parent[v] = u
                depth[v] = depth[u] + 1
                color[v] = 1
                tin[v] = timer
                timer += 1
                stack.append((v, 0))

    best_anc = -1
    best_desc = -1
    best_diff = 10**18

    for u in range(n):
        if typ[u] != 2:
            continue

        for v in g[u]:
            if v <= u or typ[v] != 2:
                continue

            if parent[v] == u or parent[u] == v:
                continue

            if tin[u] <= tin[v] < tout[u]:
                anc, desc = u, v
            elif tin[v] <= tin[u] < tout[v]:
                anc, desc = v, u
            else:
                continue

            diff = depth[desc] - depth[anc]

            if diff < best_diff:
                best_diff = diff
                best_anc = anc
                best_desc = desc

    if best_anc == -1:
        return None

    cycle = []
    x = best_desc

    while x != best_anc:
        cycle.append(x)
        x = parent[x]

    cycle.append(best_anc)
    return cycle

def find_a_path(g, typ):
    n = len(g)
    start = -1

    for v in range(n):
        if typ[v] == 1:
            start = v
            break

    if start == -1:
        return None

    parent = [-2] * n
    parent[start] = -1
    q = deque([start])

    target = -1

    while q:
        u = q.popleft()

        for v in g[u]:
            if typ[v] == 0 or parent[v] != -2:
                continue

            parent[v] = u

            if typ[v] == 1:
                target = v
                q.clear()
                break

            q.append(v)

        if target != -1:
            break

    if target == -1:
        return None

    path = []
    x = target

    while x != -1:
        path.append(x)
        x = parent[x]

    path.reverse()
    return path

def find_tree_path_to_attachment(g, start, attach):
    n = len(g)

    parent = [-2] * n
    parent[start] = -1
    q = deque([start])
    target = -1

    while q:
        u = q.popleft()

        for v in g[u]:
            if parent[v] != -2:
                continue

            if attach[v] == 0:
                parent[v] = u
                q.append(v)
            elif v != start:
                parent[v] = u
                target = v
                q.clear()
                break

        if target != -1:
            break

    if target == -1:
        return None

    path = []
    x = target

    while x != -1:
        path.append(x)
        x = parent[x]

    path.reverse()
    return path

def solve_case(n, m):
    g = [[] for _ in range(n)]
    deg = [0] * n

    for _ in range(m):
        u, v = map(int, input().split())
        u -= 1
        v -= 1
        g[u].append(v)
        g[v].append(u)
        deg[u] += 1
        deg[v] += 1

    typ = [d % 3 for d in deg]

    # Case 1: a degree-0-mod-3 vertex.
    for v in range(n):
        if typ[v] == 0:
            keep = [v]
            ans = make_answer(n, keep)
            if ans is not None:
                return ans

    # Case 2: a cycle consisting only of degree-2-mod-3 vertices.
    cycle = find_b_cycle(g, typ)

    if cycle is not None:
        ans = make_answer(n, cycle)
        if ans is not None:
            return ans

    # Case 3: a path between two degree-1-mod-3 vertices.
    a_count = sum(1 for x in typ if x == 1)

    if a_count >= 2:
        path = find_a_path(g, typ)

        if path is not None:
            ans = make_answer(n, path)
            if ans is not None:
                return ans

    # Case 4: exactly one A vertex and the B-subgraph is a forest.
    if a_count != 1:
        return None

    a = typ.index(1)

    attach = bytearray(n)
    for v in g[a]:
        if typ[v] == 2:
            attach[v] = 1

    visited = bytearray(n)
    chosen_components = []

    for s in range(n):
        if typ[s] != 2 or visited[s]:
            continue

        stack = [s]
        visited[s] = 1
        attachments = []

        while stack:
            u = stack.pop()

            if attach[u]:
                attachments.append(u)

            for v in g[u]:
                if typ[v] == 2 and not visited[v]:
                    visited[v] = 1
                    stack.append(v)

        if len(attachments) >= 2:
            chosen_components.append(attachments)

            if len(chosen_components) == 2:
                break

    if len(chosen_components) < 2:
        return None

    keep = {a}

    for attachments in chosen_components:
        start = attachments[0]
        path = find_tree_path_to_attachment(g, start, attach)

        if path is None:
            return None

        keep.update(path)

    ans = make_answer(n, keep)
    return ans

def main():
    t = int(input())
    out = []

    for _ in range(t):
        line = input()

        while line and not line.strip():
            line = input()

        n, m = map(int, line.split())

        ans = solve_case(n, m)

        if ans is None:
            out.append("No")
        else:
            out.append("Yes")
            out.append(str(len(ans)))
            out.append(" ".join(map(str, ans)))

    sys.stdout.write("\n".join(out))

if __name__ == "__main__":
    main()
```

The degree array is computed while the edges are read, so there is no separate traversal just to classify vertices. The value `typ[v]` is exactly the residue of the original degree and is used throughout the construction.

The cycle routine performs an iterative DFS because Python recursion is not safe for a graph with (500000) vertices. `tin` and `tout` describe the DFS intervals, allowing every non-tree edge to be recognized as an ancestor-descendant edge. Among those edges we choose the smallest depth difference. Any chord inside its corresponding tree path would itself be a non-tree edge with a strictly smaller depth difference, so the selected cycle has no chord.

The (A)-path is found with BFS. Since BFS stops at the first other (A)-vertex, the path cannot contain another (A)-vertex internally. This is exactly what we need for the residue (1) endpoints.

The final case uses the unique (A)-vertex to mark every (B)-vertex adjacent to it. In each (B)-tree, starting from one marked vertex and stopping at the first other marked vertex gives a path with no marked internal vertex. That prevents the unique (A)-vertex from having an unwanted chord into the middle of the path.

The implementation uses `bytearray` for DFS colors, visited flags, and attachment markers. This saves substantial memory compared with storing Python booleans or integers for several arrays of length (500000). There is no integer-overflow issue in Python, and all vertex indices are converted to zero-based form immediately after reading them. The final answer is converted back to one-based indices only when printed.

## Worked Examples

For the first graph in the sample, the graph is a triangle. Every vertex has degree (2), so all three vertices are (B)-vertices. The (B)-subgraph contains a cycle, but that cycle contains every vertex. Stealing its complement would steal nothing, so the construction is rejected.

| Stage | State |
| --- | --- |
| Degrees | (2,2,2) |
| Types | (B,B,B) |
| (Z)-vertex found | No |
| (B)-cycle | (1-2-3-1) |
| Cycle uses all vertices | Yes |
| (A)-vertices | None |
| Final forest case | Not applicable |
| Answer | `No` |

This demonstrates why detecting a cycle is not by itself enough. The selected retained structure must be proper. A whole graph that is already a cycle cannot be used because there would be no stolen vertices.

For the second graph, the degrees are (2,5,2,1,1,1). There is no (Z)-vertex and the (B)-vertices are (1) and (3), connected by one edge, so there is no (B)-cycle. Vertices (4,5,6) are (A)-vertices. BFS from vertex (4) reaches vertex (5) through vertex (2).

| Stage | State |
| --- | --- |
| Degrees | (2,5,2,1,1,1) |
| Types | (B,B,B,A,A,A) |
| (Z)-vertex found | No |
| (B)-cycle | No |
| BFS start | (4) |
| First other (A)-vertex | (5) |
| Retained path | (4-2-5) |
| Stolen vertices | (1,3,6) |
| Degree of retained (2) after theft | (2) |
| Original degree of (2) modulo (3) | (5\bmod3=2) |
| Answer | `Yes` |

The retained vertex (2) has three stolen neighbors, namely (1,3,6), so its degree decreases from (5) to (2). The other retained vertices (4) and (5) lose no incident edges. Thus every remaining degree keeps its residue modulo (3).

The third sample graph illustrates the final case. Vertex (1) has degree (7), so it is the unique (A)-vertex. The (B)-subgraph consists of several trees. One tree contains vertices (2,3,6,7,8), with (6,7,8) adjacent to vertex (1). Another contains (4,5), with both (4) and (5) adjacent to (1). Starting from (6), the nearest other attachment is (3), while the second tree gives the path (4-5). Keeping (1,6,3,4,5) and stealing (2,7,8) is one valid solution.

| Component | Attachment start | First other attachment | Retained path |
| --- | --- | --- | --- |
| ({2,3,6,7,8}) | 6 | 3 | (6-3) |
| ({4,5}) | 4 | 5 | (4-5) |
| Central vertex | 1 | Both paths | 1 |

The selected (B)-vertices have internal degree (2). Vertex (1) has four selected neighbors, so its degree changes from (7) to (4), and both values are (1\bmod3). The stolen vertices are (2,7,8).

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | (O(n+m)) | A constant number of DFS, BFS, and adjacency scans are performed |
| Space | (O(n+m)) | The adjacency lists and linear-size auxiliary arrays dominate memory |

The total (n) and total (m) over all test cases are at most (500000), so the aggregate running time is (O(\sum n+\sum m)). The algorithm never constructs an (n\times n) structure and never enumerates subsets, which keeps both memory and running time within the original contest limits.

## Test Cases

The output of this problem is non-unique, so the tests should validate the structural requirements rather than compare the exact list of stolen vertices. The following harness checks the status, the size of the stolen set, distinctness, and the degree-modulo-(3) condition for every remaining vertex.

```python
# Run this after the solution above has been defined.
import sys
import io

def run(inp: str) -> str:
    global input

    old_stdin = sys.stdin
    old_stdout = sys.stdout
    old_input = input

    sys.stdin = io.StringIO(inp)
    input = sys.stdin.readline
    sys.stdout = io.StringIO()

    try:
        main()
        return sys.stdout.getvalue()
    finally:
        sys.stdin = old_stdin
        sys.stdout = old_stdout
        input = old_input

def validate(inp: str, out: str, expected):
    data = list(map(int, inp.split()))
    pos = 0
    t = data[pos]
    pos += 1

    tokens = out.split()
    out_pos = 0

    for case_id in range(t):
        n = data[pos]
        m = data[pos + 1]
        pos += 2

        edges = []
        deg = [0] * n

        for _ in range(m):
            u = data[pos] - 1
            v = data[pos + 1] - 1
            pos += 2
            edges.append((u, v))
            deg[u] += 1
            deg[v] += 1

        assert out_pos < len(tokens)
        status = tokens[out_pos]
        out_pos += 1

        assert status == expected[case_id], (
            f"case {case_id}: expected {expected[case_id]}, got {status}"
        )

        if status == "No":
            continue

        c = int(tokens[out_pos])
        out_pos += 1

        stolen = list(map(int, tokens[out_pos:out_pos + c]))
        out_pos += c

        assert 1 < c < n
        assert len(stolen) == c
        assert len(set(stolen)) == c

        stolen_zero = {x - 1 for x in stolen}

        assert all(0 <= x < n for x in stolen_zero)

        for v in range(n):
            if v in stolen_zero:
                continue

            lost = 0
            for u, w in edges:
                if u == v and w in stolen_zero:
                    lost += 1
                elif w == v and u in stolen_zero:
                    lost += 1

            assert lost % 3 == 0, (
                f"case {case_id}: vertex {v + 1} loses {lost} edges"
            )

    assert out_pos == len(tokens)

sample = """\
3
3 3
1 2
2 3
3 1

6 6
1 2
1 3
2 3
2 5
2 6
2 4

8 12
1 2
1 3
2 3
1 4
4 5
5 1
3 6
3 7
3 8
6 1
7 1
8 1
"""

sample_out = run(sample)
validate(sample, sample_out, ["No", "Yes", "Yes"])

minimum = """\
1
1 0
"""
assert run(minimum).strip() == "No"

two_vertices = """\
1
2 1
1 2
"""
assert run(two_vertices).strip() == "No"

star = """\
1
4 3
1 2
1 3
1 4
"""
star_out = run(star)
validate(star, star_out, ["Yes"])

cycle = """\
1
4 4
1 2
2 3
3 4
4 1
"""
assert run(cycle).strip() == "No"

two_triangles = """\
1
5 6
1 2
2 3
3 1
1 4
4 5
5 1
"""
assert run(two_triangles).strip() == "No"

five_triangles = """\
1
11 15
1 2
2 3
3 1
1 4
4 5
5 1
1 6
6 7
7 1
1 8
8 9
9 1
1 10
10 11
11 1
"""
five_triangles_out = run(five_triangles)
validate(five_triangles, five_triangles_out, ["Yes"])

# Maximum-size connected graph, a star with 500000 vertices.
# The center has degree 499999, which is 1 modulo 3.
max_n = 500000
max_edges = "\n".join(f"1 {v}" for v in range(2, max_n + 1))
max_case = f"1\n{max_n} {max_n - 1}\n{max_edges}\n"

max_out = run(max_case)
validate(max_case, max_out, ["Yes"])

print("All tests passed.")
```

The minimum-size test checks the (n=1) boundary where there is no legal theft. The two-vertex test checks the strict requirement (1<c<n). The star checks the (0\bmod3) construction. The four-cycle checks the case where the entire graph is a (B)-cycle. Two triangles sharing one vertex are the smallest example of the final impossible structure. Five triangles sharing one (A)-vertex create five (B)-components and exercise the final constructive case. The maximum-size star checks both the large input boundary and the linear-time behavior.

| Test input | Expected output | What it validates |
| --- | --- | --- |
| (n=1,m=0) | `No` | Minimum-size graph |
| (n=2,m=1) | `No` | Strict (1<c<n) boundary |
| Four-vertex star | `Yes` | Degree (0\bmod3) construction |
| Four-cycle | `No` | Whole graph is a (B)-cycle |
| Two triangles sharing one vertex | `No` | Final impossible structure |
| Five triangles sharing one vertex | `Yes` | Multiple (B)-tree components |
| (500000)-vertex star | `Yes` | Maximum-size input and linear complexity |

## Edge Cases

For the one-vertex graph

```
1
1 0
```

the only vertex has degree (0), so it belongs to class (Z). The first construction would keep it, but that would leave no stolen vertex. `make_answer` rejects the construction because the number of stolen vertices is not greater than (1), and there are no other cases to use. The output is `No`.

For the two-vertex graph

```
1
2 1
1 2
```

both vertices have degree (1), so they are both class (A). BFS immediately finds the path (1-2), but this path contains every vertex. Its complement is empty, so the construction is rejected. There is no other proper subset containing at least two stolen vertices, and the output is `No`.

For the four-cycle

```
1
4 4
1 2
2 3
3 4
4 1
```

all four vertices are class (B). The DFS finds a non-tree edge and reconstructs a cycle containing all four vertices. The complement has size zero, so it cannot be stolen. A proper retained subset of a cycle is a collection of paths, and a path endpoint has internal degree (1), which does not match residue (2). The algorithm consequently returns `No`.

For the four-vertex star

```
1
4 3
1 2
1 3
1 4
```

the center has degree (3), hence is class (Z). Keeping only the center gives internal degree (0), while its original degree is (3), so the residue is preserved. The three leaves are stolen, giving a valid answer with (c=3).

For the final impossible structure,

```
1
5 6
1 2
2 3
3 1
1 4
4 5
5 1
```

vertex (1) has degree (4), hence is the unique (A)-vertex. The (B)-vertices form two tree components, each a single edge, and each component has exactly two edges to vertex (1). The only way to give the (A)-vertex the required internal degree residue is to use both components. Since each component is already exactly the path between its two attachments, retaining both paths means retaining all five vertices. There is no proper valid retained set, so the answer is `No`.

For a graph containing several such components, the situation changes. With five triangles sharing vertex (1), vertex (1) has degree (10), which is (1\bmod3). The five (B)-components are separate edges, each attached to (1) at both endpoints. Keeping the paths in any two components gives vertex (1) internal degree (4), while all selected (B)-vertices have internal degree (2). The other three components can be stolen, so the answer becomes `Yes`.
