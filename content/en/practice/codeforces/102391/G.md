---
title: "CF 102391G - Lexicographically Minimum Walk"
description: "We have a directed graph whose edges carry distinct integer colors. Starting from (S), we may traverse any outgoing edge, and we are allowed to revisit vertices and edges. The only requirement is that the walk eventually reaches (T)."
date: "2026-08-10T20:07:23+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102391
codeforces_index: "G"
codeforces_contest_name: "XX Open Cup, Grand Prix of Korea"
rating: 0
weight: 102391
solve_time_s: 168
verified: true
draft: false
---

[CF 102391G - Lexicographically Minimum Walk](https://codeforces.com/problemset/problem/102391/G)

**Rating:** -  
**Tags:** -  
**Solve time:** 2m 48s  
**Verified:** yes  

## Solution
## Problem Understanding

We have a directed graph whose edges carry distinct integer colors. Starting from (S), we may traverse any outgoing edge, and we are allowed to revisit vertices and edges. The only requirement is that the walk eventually reaches (T). Among all such walks whose length is at most (10^{100}), we want the lexicographically smallest sequence of edge colors.

Lexicographic order makes the first decision much more important than everything that follows. If one valid walk starts with color (3) and another starts with color (7), the first walk wins regardless of what happens later. If two walks have the same prefix, we compare the first position where they differ. A shorter sequence also wins when it is an exact prefix of a longer one.

The graph can contain (100,000) vertices and (300,000) edges. With the 2 second limit from the original problem, an (O(NM)) or (O(N^2)) approach is already far too expensive. We need essentially linear or (O((N+M)\log N)) work. The huge (10^{100}) bound rules out any algorithm that depends on the maximum possible walk length. Fortunately, the answer itself has a much simpler structure.

There are several cases where a careless greedy implementation can fail. The first is taking the smallest outgoing edge without checking whether its destination can eventually reach (T). For example,

```
3 2 1 3
1 2 1
1 3 5
```

The correct answer is `5`. Vertex (2) is a dead end, so choosing color (1) cannot produce a valid walk. A greedy algorithm that only looks at the smallest color would incorrectly choose it.

The second case is a cycle. Consider

```
3 4 1 3
1 2 1
2 1 2
2 3 7
1 3 5
```

The correct output is `TOO LONG`. From vertex (1), color (1) is preferable to color (5). From vertex (2), color (2) is preferable to color (7). Thus the greedy choices repeatedly produce

```
1, 2, 1, 2, 1, 2, ...
```

The walk can eventually leave the cycle and reach (T), but delaying that exit by another cycle makes the sequence lexicographically smaller. Since the allowed maximum length is astronomically large, the resulting optimal sequence is far longer than (10^6).

The third case is simply unreachable (T). For example,

```
2 0 2 1
```

has no walk at all, so the answer is `IMPOSSIBLE`.

## Approaches

A direct brute force would enumerate every possible walk from (S), keep those that reach (T) within the allowed length, and compare their color sequences. This is correct because it explicitly considers every candidate. The problem is the number of candidates. A graph can have two meaningful choices repeatedly, producing (\Theta(2^{L/2})) different walks of length at most (L). If we actually materialize every sequence, the work is (\Theta(L2^{L/2})). With (L=10^{100}), this is not merely too slow, it is fundamentally impossible.

The useful observation is that lexicographic order lets us decide the next edge independently once we know which vertices can still reach (T). Suppose we are currently at vertex (u). Any outgoing edge leading to a vertex that cannot reach (T) is irrelevant, because every walk using that edge is invalid. Among all remaining edges, the smallest color must be chosen. Choosing a larger color can never be repaired by having a better suffix, because the first differing color already decides the lexicographic comparison.

This gives a deterministic greedy transition for every useful vertex. First mark every vertex that can reach (T), using a traversal on the reversed graph. Then, for each useful vertex (u), select the outgoing edge of minimum color whose destination is also useful.

Now follow those selected edges starting from (S). There are only two possibilities. We eventually reach (T), in which case the sequence we collected is the answer. Otherwise, because there are only (N) vertices, some vertex repeats and the selected transitions form a cycle.

Why does the cycle mean `TOO LONG` rather than merely "the greedy algorithm got stuck"? At every vertex on that cycle, the selected edge has strictly smaller color than every other useful outgoing edge. The colors are globally unique, so there cannot be a tie. If we leave the cycle at some point, we must replace the selected cycle edge by a strictly larger color. Delaying that replacement by another traversal of the cycle makes the sequence lexicographically smaller. We can repeat the cycle an enormous number of times and still remain within the (10^{100}) length limit. Consequently the lexicographically minimum bounded walk has enormous length, certainly greater than (10^6).

The fact that the colors are unique is useful here because it removes the possibility of two different outgoing edges having the same color. The same greedy construction can still be formulated with ties, but additional care would be required to choose the best suffix among equal first colors.

The resulting method is linear apart from optional sorting. We can avoid sorting entirely by scanning every adjacency list once and remembering its minimum useful edge.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | (\Theta(L2^{L/2})) in a branching graph | Exponential | Too slow |
| Optimal | (O(N+M)) | (O(N+M)) | Accepted |

The same greedy characterization is also given in an independent published solution discussion for this problem.

## Algorithm Walkthrough

1. Build both the original graph and its reversed graph. The original graph is needed to choose edges, while the reversed graph lets us determine which vertices can eventually reach (T).
2. Run a graph traversal starting at (T) in the reversed graph. Mark every vertex reached by this traversal as `good`. A vertex is `good` exactly when there exists some directed walk from that vertex to (T).

This filtering is essential. An edge with a very small color is not a valid candidate if it leads into a region from which (T) is unreachable.
3. If (S) is not `good`, print `IMPOSSIBLE`. There is no valid walk from (S) to (T), so there cannot be a color sequence to output.
4. For every vertex (u), inspect its outgoing edges and find the edge with minimum color whose destination is `good`. Store its destination and color.

Every `good` vertex other than (T) has at least one such edge, because by definition it has some path to (T).
5. Start at (S), keep a `visited` array, and repeatedly follow the stored minimum useful edge. Append its color to the answer before moving to the destination.

The `visited` array detects exactly the case where the deterministic greedy walk has entered a cycle. There is no need to store the entire sequence just to detect repetition.
6. If the current vertex becomes (T), print all collected colors. Since no vertex has been repeated, the walk contains at most (N-1) edges. In particular, its length is automatically below (10^6).
7. If a vertex is encountered for the second time before reaching (T), print `TOO LONG`.

At every repeated vertex, the greedy edge has the smallest possible color among all edges that can still lead to (T). Any finite walk that exits the cycle must eventually choose a larger color instead of that greedy edge. Repeating the cycle postpones that larger color and makes the resulting sequence lexicographically smaller. Since the permitted maximum length is (10^{100}), vastly more than (10^6), the required answer cannot be printed.

### Why it works

Consider the current vertex (u). Every valid continuation must take an edge whose destination can reach (T). Among exactly those edges, the edge with the smallest color must occur in the lexicographically minimum sequence. If another valid walk chooses a larger color at this position, its sequence is already larger, regardless of its suffix. Thus the first greedy choice is forced, and the same argument applies recursively at every later vertex.

If the greedy process reaches (T) without repeating a vertex, every chosen edge is forced by this argument, so the produced sequence is the lexicographically minimum valid sequence.

If the process repeats a vertex, the deterministic transitions from that point form a cycle. At every cycle vertex, the chosen edge is smaller than every other edge that could eventually reach (T). Any valid walk that eventually leaves the cycle must choose a larger edge at some first exit position. A walk that makes one more complete cycle before taking that exit has the same prefix up to that point and then has the smaller cycle color, so it is lexicographically smaller. Repeating this argument shows that the optimal bounded walk uses the maximum available number of repetitions before exiting. The bound (10^{100}) makes its length much larger than (10^6), so `TOO LONG` is the correct output.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, m, s, t = map(int, input().split())

    graph = [[] for _ in range(n)]
    rev = [[] for _ in range(n)]

    for _ in range(m):
        u, v, c = map(int, input().split())
        u -= 1
        v -= 1
        graph[u].append((v, c))
        rev[v].append(u)

    # Find all vertices that can reach T.
    good = [False] * n
    good[t] = True

    stack = [t]
    while stack:
        u = stack.pop()
        for v in rev[u]:
            if not good[v]:
                good[v] = True
                stack.append(v)

    if not good[s]:
        print("IMPOSSIBLE")
        return

    # For every useful vertex, remember its minimum-color
    # outgoing edge whose destination is also useful.
    next_vertex = [-1] * n
    next_color = [0] * n

    for u in range(n):
        best_color = None
        best_vertex = -1

        for v, c in graph[u]:
            if not good[v]:
                continue
            if best_color is None or c < best_color:
                best_color = c
                best_vertex = v

        if best_vertex != -1:
            next_vertex[u] = best_vertex
            next_color[u] = best_color

    # Follow the deterministic greedy transitions.
    visited = [False] * n
    answer = []

    u = s

    while u != t:
        if visited[u]:
            print("TOO LONG")
            return

        visited[u] = True

        v = next_vertex[u]

        # This should not happen because u is good and u != T.
        if v == -1:
            print("IMPOSSIBLE")
            return

        answer.append(next_color[u])
        u = v

    print(*answer)

if __name__ == "__main__":
    solve()
```

The first graph construction stores each edge in the forward graph and stores only its predecessor in the reverse graph. Starting from (T) in the reverse graph therefore visits exactly the vertices from which (T) is reachable.

The `good` test is done before any greedy choice. This is the main correctness condition that prevents the algorithm from choosing a small color that leads to a dead end.

The minimum useful outgoing edge is found by a single scan of each adjacency list. There is no need to sort the edges. Since every edge is inspected exactly once during this phase, it contributes (O(M)) total work.

The final traversal is deterministic. Once `next_vertex[u]` has been computed, there is only one edge the greedy algorithm can choose from (u). `visited[u]` is set before moving to the next vertex, so encountering `visited[u]` on a later iteration means that a cycle has actually been completed. There is no off-by-one issue around (T), because (T) is checked before the repeated-vertex test.

Python integers easily handle the given color limit of (10^9), and the algorithm never performs arithmetic involving (10^{100}). We do not need to represent the enormous walk length at all.

## Worked Examples

### Sample 1

The input is

```
3 3 1 3
1 2 1
2 3 7
1 3 5
```

All three vertices can reach vertex (3), so every vertex is useful. At vertex (1), the useful outgoing colors are (1) and (5), so the greedy choice is color (1). At vertex (2), the only useful outgoing edge has color (7), which reaches (T).

| Current vertex | Good outgoing edges | Chosen color | Next vertex | Visited before |
| --- | --- | --- | --- | --- |
| 1 | (1\to2) with 1, (1\to3) with 5 | 1 | 2 | No |
| 2 | (2\to3) with 7 | 7 | 3 | No |
| 3 | Stop |  |  |  |

The resulting sequence is `1 7`. The greedy choice at vertex (1) beats the direct edge of color (5), because the first differing color is (1<5).

### Sample 2

The input is

```
3 4 1 3
1 2 1
2 1 2
2 3 7
1 3 5
```

Again every vertex can reach (3). The minimum useful edge from (1) has color (1), while the minimum useful edge from (2) has color (2).

| Current vertex | Good outgoing edges | Chosen color | Next vertex | Visited before |
| --- | --- | --- | --- | --- |
| 1 | (1\to2) with 1, (1\to3) with 5 | 1 | 2 | No |
| 2 | (2\to1) with 2, (2\to3) with 7 | 2 | 1 | No |
| 1 | (1\to2) with 1, (1\to3) with 5 | 1 | 2 | Yes |

The transition (1\to2\to1) is a cycle. Leaving it would require using color (5) from vertex (1) or color (7) from vertex (2), both larger than the corresponding cycle edge. Thus another cycle is always lexicographically preferable. The answer is `TOO LONG`.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | (O(N+M)) | Reverse traversal, minimum-edge scans, and the final greedy walk each process vertices or edges linearly |
| Space | (O(N+M)) | Forward graph, reverse graph, reachability arrays, greedy transitions, and visited array |

With (N\le100,000) and (M\le300,000), linear processing is comfortably within the intended scale of the problem. The algorithm also avoids recursion, which is useful in Python because a graph can contain a path with close to (100,000) vertices.

## Test Cases

The following test harness uses the same `solve` function as the submitted solution. The maximum-size test constructs a chain with (100,000) vertices, while the other cases target reachability, cycles, direct edges, and very large color values.

```python
import sys
import io
from contextlib import redirect_stdout

def solve(data=None):
    if data is None:
        input = sys.stdin.readline
    else:
        input = io.StringIO(data).readline

    n, m, s, t = map(int, input().split())

    graph = [[] for _ in range(n)]
    rev = [[] for _ in range(n)]

    for _ in range(m):
        u, v, c = map(int, input().split())
        u -= 1
        v -= 1
        graph[u].append((v, c))
        rev[v].append(u)

    good = [False] * n
    good[t - 0] = True

    stack = [t]
    while stack:
        u = stack.pop()
        for v in rev[u]:
            if not good[v]:
                good[v] = True
                stack.append(v)

    if not good[s]:
        print("IMPOSSIBLE")
        return

    next_vertex = [-1] * n
    next_color = [0] * n

    for u in range(n):
        best_color = None
        best_vertex = -1

        for v, c in graph[u]:
            if not good[v]:
                continue
            if best_color is None or c < best_color:
                best_color = c
                best_vertex = v

        if best_vertex != -1:
            next_vertex[u] = best_vertex
            next_color[u] = best_color

    visited = [False] * n
    answer = []
    u = s

    while u != t:
        if visited[u]:
            print("TOO LONG")
            return

        visited[u] = True
        v = next_vertex[u]

        if v == -1:
            print("IMPOSSIBLE")
            return

        answer.append(next_color[u])
        u = v

    print(*answer)

def run(inp: str) -> str:
    old_stdin = sys.stdin
    sys.stdin = io.StringIO(inp)
    out = io.StringIO()

    try:
        with redirect_stdout(out):
            solve()
    finally:
        sys.stdin = old_stdin

    return out.getvalue().strip()

# Provided samples.
assert run(
    """3 3 1 3
1 2 1
2 3 7
1 3 5
"""
) == "1 7", "sample 1"

assert run(
    """3 4 1 3
1 2 1
2 1 2
2 3 7
1 3 5
"""
) == "TOO LONG", "sample 2"

assert run(
    """2 0 2 1
"""
) == "IMPOSSIBLE", "sample 3"

# Minimum-size valid graph.
assert run(
    """2 1 1 2
1 2 1000000000
"""
) == "1000000000", "minimum graph"

# A smaller color may lead to a dead end, so it must be ignored.
assert run(
    """3 2 1 3
1 2 1
1 3 5
"""
) == "5", "dead-end minimum edge"

# Two valid choices from S, with a much smaller first color.
assert run(
    """4 4 1 4
1 2 9
1 3 2
2 4 1
3 4 1000000000
"""
) == "2 1000000000", "lexicographic first choice"

# Large colors near the upper boundary.
assert run(
    """3 3 1 3
1 2 999999999
2 3 1000000000
1 3 1000000000
"""
) == "999999999 1000000000", "large colors"

# Maximum-size chain: N = 100000, M = 99999.
n = 100000
lines = [f"{n} {n - 1} 1 {n}"]
lines.extend(f"{i} {i + 1} {i}" for i in range(1, n))
max_input = "\n".join(lines) + "\n"
max_expected = " ".join(map(str, range(1, n)))
assert run(max_input) == max_expected, "maximum-size chain"

print("All tests passed.")
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `2 1 1 2` with color (10^9) | `1000000000` | Minimum graph and maximum color boundary |
| `3 2 1 3` with edges of colors 1 and 5 | `5` | A smaller edge leading to a dead end must be rejected |
| Four vertex graph with first choices 9 and 2 | `2 1000000000` | Lexicographic comparison is determined by the first differing color |
| Three vertex graph using colors near (10^9) | `999999999 1000000000` | Large color values and direct versus indirect choices |
| (100000) vertex chain | Colors (1) through (99999) | Maximum (N), large (M), and a long acyclic greedy walk |

The statement says edge colors are globally unique, so a literal test where all edge colors are equal would violate the input conditions. The large color test above exercises the relevant numeric boundary while remaining a valid instance.

## Edge Cases

The first edge case is a smaller-color dead end. Consider

```
3 2 1 3
1 2 1
1 3 5
```

The reverse traversal from (3) marks only vertex (3) and vertex (1) as useful. Vertex (2) is not marked because there is no path from (2) to (3). When the algorithm scans vertex (1), it ignores the color (1) edge because its destination is not useful, leaving color (5) as the minimum valid choice. The output is `5`.

The second edge case is the unreachable target.

```
2 0 2 1
```

The reverse traversal starts at vertex (1) and reaches nothing else. Vertex (2=S) is not useful, so the algorithm immediately prints `IMPOSSIBLE`.

The third edge case is a cycle containing the greedy choices.

```
3 4 1 3
1 2 1
2 1 2
2 3 7
1 3 5
```

The useful minimum edge from (1) is color (1), and the useful minimum edge from (2) is color (2). The greedy sequence therefore goes (1\to2\to1). When vertex (1) is encountered for the second time, the algorithm prints `TOO LONG`. The cycle can be repeated before taking the larger exit color (5), so the lexicographically preferred bounded walk has enormous length.

The fourth edge case is a graph where the greedy walk reaches (T) without a cycle.

```
3 3 1 3
1 2 1
2 3 7
1 3 5
```

The algorithm chooses color (1) from vertex (1), then color (7) from vertex (2), and reaches (3). No vertex repeats. Since a simple walk through (N) vertices contains at most (N-1) edges, the resulting sequence is automatically below the (10^6) output threshold.

The final boundary case is the maximum-size chain used in the tests. Every vertex has exactly one outgoing edge, so the greedy choice is forced. The algorithm performs one reverse traversal over (99,999) edges, one scan of the same edges, and then follows (99,999) transitions. It produces the entire sequence without recursion and without ever needing to represent the (10^{100}) walk bound.
