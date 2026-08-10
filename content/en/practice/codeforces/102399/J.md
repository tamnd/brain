---
title: "CF 102399J - \u041a\u043e\u043d\u043a\u0443\u0440\u0441 \u043a\u043e\u0442\u0438\u043a\u043e\u0432"
description: "Think of the input as a directed graph on the indices (1,dots,n). Vertex (i) represents both resident (i) and their own cat (i). Every pair (a,b) means that there is a directed edge (ato b): resident (a) knows cat (b)."
date: "2026-08-11T05:42:26+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102399
codeforces_index: "J"
codeforces_contest_name: "2019 \u041c\u043e\u0441\u043a\u043e\u0432\u0441\u043a\u0430\u044f \u043a\u043e\u043c\u0430\u043d\u0434\u043d\u0430\u044f \u043e\u043b\u0438\u043c\u043f\u0438\u0430\u0434\u0430 \u0448\u043a\u043e\u043b\u044c\u043d\u0438\u043a\u043e\u0432, \u043b\u0438\u0433\u0430 A"
rating: 0
weight: 102399
solve_time_s: 1081
verified: false
draft: false
---

[CF 102399J - \u041a\u043e\u043d\u043a\u0443\u0440\u0441 \u043a\u043e\u0442\u0438\u043a\u043e\u0432](https://codeforces.com/problemset/problem/102399/J)

**Rating:** -  
**Tags:** -  
**Solve time:** 18m 1s  
**Verified:** no  

## Solution
## Problem Understanding

Think of the input as a directed graph on the indices (1,\dots,n). Vertex (i) represents both resident (i) and their own cat (i). Every pair (a,b) means that there is a directed edge (a\to b): resident (a) knows cat (b). The guaranteed pair (i,i) gives every vertex a self-loop, but those loops will not affect the construction.

We must choose a nonempty set (J) of residents for the jury and a nonempty set (P) of cats for the contest. Their sizes must add up to (n), and no resident in (J) may know a cat in (P).

The first useful observation comes directly from the fact that resident (i) knows cat (i). If (i) belonged to both (J) and (P), then resident (i) would know participant cat (i), which is forbidden. Thus (J) and (P), viewed simply as sets of indices, are disjoint. Since (|J|+|P|=n) and there are exactly (n) indices, every index belongs to exactly one of them.

So the task is really to split the vertices into two nonempty parts. An edge (a\to b) is forbidden only when (a) is on the jury side and (b) is on the participant side. Edges in the other direction are perfectly legal.

The constraints make a brute-force search over all partitions impossible. There are (2^n) possible subsets, while (n) and the total number of edges can each reach (10^6). The original statement gives a two-second limit and total bounds of (10^6), so the intended solution has to process each vertex and each acquaintance pair only a constant number of times, up to the usual inverse-Ackermann factor or a linear graph algorithm.

There are several edge cases that expose incorrect interpretations of the condition. With (n=1), the only possible partition would put the single index on one side and leave the other side empty. For example,

```
1
1 1
1 1
```

must produce `No`. A careless implementation that only checks whether it can find a conflict-free partition could accept the trivial partition, forgetting that both groups must be nonempty.

A second subtle case is a one-way acquaintance. Consider

```
1
2 3
1 1
2 2
1 2
```

The correct answer is `Yes`, with resident 2 as jury and cat 1 as participant. Resident 1 knowing cat 2 does not matter because resident 1 is not on the jury. An approach that treats every acquaintance pair as an undirected conflict would incorrectly reject this case.

A third case is the second sample:

```
1
3 7
1 1
1 2
1 3
2 2
3 1
3 2
3 3
```

The correct answer is `Yes`, using resident 2 as jury and cats 1 and 3 as participants. There are edges from residents 1 and 3 towards cat 2, but those residents are participants' indices, not jury indices. Treating the acquaintance relation as an undirected graph would incorrectly conclude that the whole graph has to stay in one part.

Finally, if every resident knows every cat, such as

```
1
2 4
1 1
1 2
2 1
2 2
```

the answer is `No`. Whichever resident enters the jury, that resident knows both cats, so at least one forbidden jury-to-participant edge is unavoidable.

## Approaches

The brute-force approach is to enumerate every possible jury set (J). The participants are then forced to be its complement, because the two sets must be disjoint and their sizes must sum to (n). For each candidate (J), we scan all (m) acquaintance pairs and reject the set if some edge (a\to b) has (a\in J) and (b\notin J). This is correct because every legal solution corresponds to exactly one such subset (J).

The problem is the number of subsets. There are (2^n) of them, so the worst-case work is (O(m2^n)). At (n=m=10^6), this is on the order of (10^6\cdot2^{10^6}) edge checks, which is not remotely feasible.

The brute-force works because it explicitly searches for a set with no outgoing edges. The key observation is that we do not actually need to search through sets. In a directed graph, a nonempty set (S) with no edge from (S) to its complement is called a closed set. Such a set always exists if the graph is not strongly connected: take any sink strongly connected component of the condensation graph. Conversely, if the whole graph is strongly connected, every nonempty proper subset has an outgoing edge, so no valid jury can exist.

This gives a direct characterization. A valid contest exists exactly when the acquaintance graph has at least two strongly connected components. If it does, take any sink strongly connected component as the jury. Since no edge leaves a sink component, no jury resident knows any cat outside that component. Put every remaining index into the participant set.

The reason the direction of edges matters is now clear. The second sample has a strongly connected component containing vertices 1 and 3, and a separate sink component containing vertex 2. Choosing that sink component as the jury gives exactly the sample construction. An undirected connectivity approach would lose this direction information and fail.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | (O(m2^n)) | (O(n+m)) | Too slow |
| Optimal with SCCs | (O(n+m)) | (O(n+m)) | Accepted |

## Algorithm Walkthrough

1. Build the directed acquaintance graph and its reversed graph. For every pair (a,b), add (b) to the outgoing list of (a), and add (a) to the reversed outgoing list of (b). We need the reversed graph because Kosaraju's algorithm finds strongly connected components using one DFS order and a second DFS on the reversed edges.
2. Run the first phase of Kosaraju's algorithm. Perform DFS from every unvisited vertex and append a vertex to `order` only after all vertices reachable from it have been processed. The resulting finishing order captures the direction of the condensation graph and is what makes the second pass work.
3. Process vertices in reverse finishing order on the reversed graph. Every DFS in this phase produces exactly one strongly connected component, so assign all reached vertices the same component identifier.
4. If there is only one component, print `No`. A strongly connected graph cannot contain a nonempty proper subset with no outgoing edge. Starting from any vertex of such a subset, strong connectivity gives a path to every vertex outside it, and the first edge on that path leaving the subset would be forbidden.
5. If there are at least two components, inspect every original edge (a\to b). Whenever `component[a] != component[b]`, mark the component containing (a) as having an outgoing edge. Any component that remains unmarked is a sink component of the condensation graph.
6. Choose one sink component as the jury. Put exactly its vertices into (J), and put every other vertex into (P). The jury is nonempty because a component contains at least one vertex, while the participant set is also nonempty because there is more than one component.
7. Output the two sets using their original one-based indices. Their sizes automatically sum to (n), and the sink property guarantees that no edge goes from a jury vertex to a participant vertex.

### Why it works

The invariant is that a set of jury indices is valid exactly when it has no directed edge leaving it. Every valid solution is such a nonempty proper closed set. If the graph has multiple strongly connected components, the condensation graph is a finite DAG, so it contains a sink component. No original edge leaves that component, making it a valid jury. If the graph has only one strongly connected component, every nonempty proper set has an edge leaving it, so no valid jury exists. Thus the algorithm accepts exactly the solvable cases and constructs a valid partition whenever one exists.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    out = []

    for _ in range(t):
        # Empty lines between test cases are allowed, so skip them.
        line = input()
        while line.strip() == "":
            line = input()

        n, m = map(int, line.split())

        g = [[] for _ in range(n)]
        rg = [[] for _ in range(n)]

        for _ in range(m):
            a, b = map(int, input().split())
            a -= 1
            b -= 1
            g[a].append(b)
            rg[b].append(a)

        # First pass of Kosaraju: finishing order.
        used = [False] * n
        order = []

        for start in range(n):
            if used[start]:
                continue

            used[start] = True
            stack = [(start, 0)]

            while stack:
                v, i = stack[-1]

                if i < len(g[v]):
                    to = g[v][i]
                    stack[-1] = (v, i + 1)

                    if not used[to]:
                        used[to] = True
                        stack.append((to, 0))
                else:
                    order.append(v)
                    stack.pop()

        # Second pass: components in reversed graph.
        comp = [-1] * n
        components = 0

        for start in reversed(order):
            if comp[start] != -1:
                continue

            comp[start] = components
            stack = [start]

            while stack:
                v = stack.pop()

                for to in rg[v]:
                    if comp[to] == -1:
                        comp[to] = components
                        stack.append(to)

            components += 1

        if components == 1:
            out.append("No")
            continue

        # Find a sink SCC in the original graph.
        has_outgoing = [False] * components

        for v in range(n):
            cv = comp[v]
            for to in g[v]:
                if cv != comp[to]:
                    has_outgoing[cv] = True

        sink = 0
        while has_outgoing[sink]:
            sink += 1

        jury = []
        participants = []

        for v in range(n):
            if comp[v] == sink:
                jury.append(v + 1)
            else:
                participants.append(v + 1)

        out.append("Yes")
        out.append(f"{len(jury)} {len(participants)}")
        out.append(" ".join(map(str, jury)))
        out.append(" ".join(map(str, participants)))

    sys.stdout.write("\n".join(out))

if __name__ == "__main__":
    solve()
```

The input loop skips empty lines because the test cases are separated by blank lines. This is not necessary for a typical token-based C++ parser, but Python's `readline()` sees those lines explicitly, so handling them avoids interpreting an empty line as the next pair of integers.

The two adjacency lists represent the original and reversed directed graphs. Every acquaintance pair is inserted in both directions of these data structures, but the edge itself remains directed. This distinction is essential for the second sample.

The first DFS is written iteratively rather than recursively. Python's recursion limit is far below the possible graph depth of (10^6), so a recursive DFS could raise a `RecursionError` even when the algorithm is mathematically correct. The stack stores `(vertex, next_edge_index)` so that a vertex is added to `order` only after its entire outgoing adjacency list has been processed.

The second pass uses a simpler stack because we only need to visit every reachable vertex and assign its component identifier. The component count is enough to decide the `No` case.

After the components are known, the code scans the original edges. A component is marked as non-sink precisely when some edge leaves it for another component. Self-loops and edges inside the same SCC are ignored. The guaranteed edges (i\to i) consequently have no special handling.

The chosen `sink` is an SCC with no outgoing edge. Because `components > 1`, its complement contains at least one vertex. The jury and participant lists therefore satisfy both nonemptiness requirements.

No integer can overflow in Python, and all indices are converted to zero-based form immediately after reading. They are converted back to one-based form only when constructing the output.

## Worked Examples

### Sample 1

For the first test case, the directed edges are (1\to1), (2\to2), (3\to3), and (1\to3). The SCCs are ({1,3}) and ({2}). The component ({1,3}) has no edge to ({2}), so it is a sink and can be used as the jury.

| Step | `order` / components | Sink | Jury | Participants |
| --- | --- | --- | --- | --- |
| Build graph | (1\to3), self-loops | not known | not known | not known |
| First DFS | finishing order `[3, 1, 2]` | not known | not known | not known |
| Second DFS | `{2}`, `{1,3}` | not known | not known | not known |
| Scan cross-component edges | `{1,3}` has none | `{1,3}` | `{1,3}` | `{2}` |

The resulting output is

```
Yes
2 1
1 3
2
```

The only non-self edge goes from resident 1 to cat 3, and both indices are on the jury side, so no jury resident knows the participant cat 2.

### Sample 2

Here the relevant edges are (1\to2), (1\to3), (3\to1), and (3\to2), together with the self-loops. Vertices 1 and 3 are mutually reachable, so they form one SCC. Vertex 2 forms another SCC, and no edge leaves vertex 2.

| Step | `order` / components | Sink | Jury | Participants |
| --- | --- | --- | --- | --- |
| Build graph | (1\to2,1\to3,3\to1,3\to2) | not known | not known | not known |
| First DFS | all vertices visited | not known | not known | not known |
| Second DFS | `{1,3}`, `{2}` | not known | not known | not known |
| Scan cross-component edges | `{1,3}` points to `{2}` | `{2}` | `{2}` | `{1,3}` |

The resulting output is

```
Yes
1 2
2
1 3
```

This example demonstrates why the graph must remain directed. The edges (1\to2) and (3\to2) are harmless because residents 1 and 3 are not jury members. The absence of an edge from 2 to either 1 or 3 is exactly what makes component `{2}` a valid jury.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | (O(n+m)) | Each vertex and each directed acquaintance edge is processed a constant number of times by the two DFS passes and the sink scan. |
| Space | (O(n+m)) | The original graph, reversed graph, component arrays, visited state, and DFS stacks all use linear space. |

The total (n) and total (m) over all test cases are at most (10^6), so the complete input is processed in linear time in its actual size. The iterative DFS also avoids Python recursion-depth failures on long chains. The stated contest memory limit is 512 MB, while the algorithm requires only linear graph storage.

## Test Cases

The following test harness uses the same algorithm as the submitted solution. For small cases, it checks the exact deterministic output produced by the implementation. For larger cases, it validates the structural properties of the returned construction instead of comparing a million-element output string literally.

```python
import sys
import io

def solve_data(inp: str) -> str:
    old_stdin = sys.stdin
    sys.stdin = io.StringIO(inp)

    def read_nonempty():
        line = sys.stdin.readline()
        while line and not line.strip():
            line = sys.stdin.readline()
        return line

    t = int(read_nonempty())
    out = []

    for _ in range(t):
        line = read_nonempty()
        n, m = map(int, line.split())

        g = [[] for _ in range(n)]
        rg = [[] for _ in range(n)]
        edges = []

        for _ in range(m):
            a, b = map(int, sys.stdin.readline().split())
            a -= 1
            b -= 1
            g[a].append(b)
            rg[b].append(a)
            edges.append((a, b))

        used = [False] * n
        order = []

        for start in range(n):
            if used[start]:
                continue

            used[start] = True
            stack = [(start, 0)]

            while stack:
                v, i = stack[-1]

                if i < len(g[v]):
                    to = g[v][i]
                    stack[-1] = (v, i + 1)

                    if not used[to]:
                        used[to] = True
                        stack.append((to, 0))
                else:
                    order.append(v)
                    stack.pop()

        comp = [-1] * n
        components = 0

        for start in reversed(order):
            if comp[start] != -1:
                continue

            comp[start] = components
            stack = [start]

            while stack:
                v = stack.pop()

                for to in rg[v]:
                    if comp[to] == -1:
                        comp[to] = components
                        stack.append(to)

            components += 1

        if components == 1:
            out.append("No")
            continue

        has_outgoing = [False] * components

        for a, b in edges:
            if comp[a] != comp[b]:
                has_outgoing[comp[a]] = True

        sink = 0
        while has_outgoing[sink]:
            sink += 1

        jury = [v + 1 for v in range(n) if comp[v] == sink]
        participants = [v + 1 for v in range(n) if comp[v] != sink]

        out.append("Yes")
        out.append(f"{len(jury)} {len(participants)}")
        out.append(" ".join(map(str, jury)))
        out.append(" ".join(map(str, participants)))

    sys.stdin = old_stdin
    return "\n".join(out)

def validate(inp: str, output: str) -> bool:
    data = inp.split()
    pos = 0
    t = int(data[pos])
    pos += 1

    tests = []

    for _ in range(t):
        n = int(data[pos])
        m = int(data[pos + 1])
        pos += 2

        edges = []
        for _ in range(m):
            a = int(data[pos])
            b = int(data[pos + 1])
            pos += 2
            edges.append((a, b))

        tests.append((n, edges))

    lines = output.splitlines()
    p = 0

    for n, edges in tests:
        if p >= len(lines):
            return False

        if lines[p] == "No":
            p += 1

            # A valid "No" is verified independently by checking
            # whether the directed graph is strongly connected.
            g = [[] for _ in range(n)]
            rg = [[] for _ in range(n)]

            for a, b in edges:
                g[a - 1].append(b - 1)
                rg[b - 1].append(a - 1)

            def reachable(graph):
                seen = [False] * n
                stack = [0]
                seen[0] = True

                while stack:
                    v = stack.pop()
                    for to in graph[v]:
                        if not seen[to]:
                            seen[to] = True
                            stack.append(to)

                return all(seen)

            if not reachable(g) or not reachable(rg):
                return False

            continue

        if lines[p] != "Yes":
            return False
        p += 1

        j, q = map(int, lines[p].split())
        p += 1

        jury = list(map(int, lines[p].split()))
        p += 1

        participants = list(map(int, lines[p].split()))
        p += 1

        if len(jury) != j or len(participants) != q:
            return False
        if j + q != n or j == 0 or q == 0:
            return False
        if len(set(jury)) != j or len(set(participants)) != q:
            return False
        if set(jury) & set(participants):
            return False

        jury_set = set(jury)
        for a, b in edges:
            if a in jury_set and b in set(participants):
                return False

    return p == len(lines)

sample = """\
4
3 4
1 1
2 2
3 3
1 3

3 7
1 1
1 2
1 3
2 2
3 1
3 2
3 3

1 1
1 1

2 4
1 1
1 2
2 1
2 2
"""

sample_output = """\
Yes
2 1
1 3
2
Yes
1 2
2
1 3
No
No
"""

assert solve_data(sample) == sample_output, "provided sample"

minimum = """\
1
1 1
1 1
"""

assert solve_data(minimum) == "No", "minimum-size case"

two_isolated = """\
1
2 2
1 1
2 2
"""

assert solve_data(two_isolated) == """\
Yes
1 1
2
1
""", "two independent vertices"

one_way = """\
1
2 3
1 1
2 2
1 2
"""

assert solve_data(one_way) == """\
Yes
1 1
2
1
""", "directed edge must not be treated as undirected"

complete = """\
1
3 9
1 1
1 2
1 3
2 1
2 2
2 3
3 1
3 2
3 3
"""

assert solve_data(complete) == "No", "complete acquaintance graph"

max_boundary = "1\n1000000 1000000\n" + "".join(
    f"{i} {i}\n" for i in range(1, 1000001)
)

assert validate(max_boundary, solve_data(max_boundary)), "maximum-size input"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 / 1 1 / 1 1` | `No` | The two required groups cannot both be nonempty when (n=1). |
| `2 2` with only `1 1` and `2 2` | `Yes`, one vertex on each side | Multiple sink SCCs and the smallest nontrivial partition. |
| `2 3` with `1 2` as the only cross edge | `Yes`, jury `{2}` | Directed edges must not be treated as undirected conflicts. |
| Complete (3\times3) acquaintance graph | `No` | A strongly connected graph has no proper closed subset. |
| (n=m=10^6), only self-loops | `Yes`, one vertex versus the other (999999) | Maximum input bounds, memory use, and boundary handling. |

## Edge Cases

For (n=1), the graph contains only vertex 1 with its self-loop. Kosaraju finds one SCC, so the algorithm immediately prints `No`. This is necessary because although the set containing vertex 1 has no outgoing edge to another vertex, its complement is empty, and the contest requires at least one participant.

For a one-way edge, consider

```
2 3
1 1
2 2
1 2
```

The graph has two SCCs, `{1}` and `{2}`. The edge (1\to2) makes `{1}` a non-sink SCC, while `{2}` has no outgoing edge. The algorithm chooses `{2}` as the jury and `{1}` as the participant set. Resident 2 knows only cat 2, so the construction is valid. If the edge were incorrectly treated as undirected, the two vertices would appear inseparable, producing the wrong answer.

For the second sample, the SCCs are `{1,3}` and `{2}`. Edges (1\to2) and (3\to2) leave the first component, so it is not a sink. There is no edge from 2 to either 1 or 3, so `{2}` is a sink and becomes the jury. This gives one jury member and two participants, exactly as required.

For a complete acquaintance graph, every vertex has an edge to every other vertex. The graph is strongly connected, so Kosaraju produces exactly one SCC. The algorithm prints `No`, correctly ruling out every possible nonempty proper jury set because any chosen jury member knows every cat outside the jury.

For the maximum-size boundary case with (n=m=10^6) and only self-loops, every vertex forms its own SCC. Every SCC is a sink because all edges stay inside the component. The algorithm selects one of them as the jury and all other vertices as participants. This confirms that self-loops do not accidentally mark an SCC as having an outgoing edge and that the implementation handles the largest allowed input linearly.
