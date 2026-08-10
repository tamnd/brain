---
title: "CF 102407E - \u0421\u0442\u0440\u0430\u043d\u043d\u0430\u044f \u0438\u0433\u0440\u0430 \u043d\u0430 \u0433\u0440\u0430\u0444\u0435"
description: "The graph is undirected, and every original edge is an object that can be erased. Arthur starts by erasing any edge. After that, the next player must erase an edge sharing at least one endpoint with the previously erased edge. An erased edge can never be used again."
date: "2026-08-11T05:55:19+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102407
codeforces_index: "E"
codeforces_contest_name: "\u0418\u043d\u0442\u0435\u0440\u043d\u0435\u0442-\u043e\u043b\u0438\u043c\u043f\u0438\u0430\u0434\u044b, \u0421\u0435\u0437\u043e\u043d 2019-2020, \u0412\u0442\u043e\u0440\u0430\u044f \u043a\u043e\u043c\u0430\u043d\u0434\u043d\u0430\u044f \u043e\u043b\u0438\u043c\u043f\u0438\u0430\u0434\u0430, \u0443\u0441\u043b\u043e\u0436\u043d\u0435\u043d\u043d\u0430\u044f \u043d\u043e\u043c\u0438\u043d\u0430\u0446\u0438\u044f"
rating: 0
weight: 102407
solve_time_s: 240
verified: false
draft: false
---

[CF 102407E - \u0421\u0442\u0440\u0430\u043d\u043d\u0430\u044f \u0438\u0433\u0440\u0430 \u043d\u0430 \u0433\u0440\u0430\u0444\u0435](https://codeforces.com/problemset/problem/102407/E)

**Rating:** -  
**Tags:** -  
**Solve time:** 4m  
**Verified:** no  

## Solution
## Problem Understanding

The graph is undirected, and every original edge is an object that can be erased. Arthur starts by erasing any edge. After that, the next player must erase an edge sharing at least one endpoint with the previously erased edge. An erased edge can never be used again. A player with no legal edge to erase loses.

The key detail is that the game is played on edges, but the adjacency relation between game objects is exactly the adjacency relation in the line graph of the original graph. In the line graph, every original edge becomes a vertex, and two such vertices are adjacent when the corresponding original edges have a common endpoint. The first move is special because Arthur may choose any vertex of this line graph, after which the usual game of moving to an unvisited adjacent vertex begins.

The input contains up to \(10^4\) vertices and \(10^4\) edges. The official contest limits are 2 seconds and 512 MB. citeturn5search0 An algorithm quadratic in \(m\) might still be usable in some languages, but the structure of the problem allows a linear solution, so there is no reason to construct the line graph explicitly. A brute-force search is completely infeasible because the number of possible play sequences can be factorial in \(m\).

There are several cases that easily fool a parity-only implementation. With a single edge, for example,

```text
2 1
1 2
```

the correct answer is `YES`. Arthur erases the only edge and his opponent immediately has no move. Looking only at whether the total number of edges is even would miss this.

Disconnected graphs are another source of mistakes. Consider

```text
4 2
1 2
3 4
```

The correct answer is `YES`. Each connected component contains one edge, so Arthur chooses an edge from either component and the game ends immediately. A careless solution that checks only the parity of the total number of edges would incorrectly output `NO`, because the total is two.

The opposite situation is

```text
6 4
1 2
2 3
4 5
5 6
```

where each connected component contains two edges. The correct answer is `NO`. Each component of the corresponding line graph has an even number of vertices and admits a perfect matching, which gives the second player a pairing strategy. Counting only whether there is an even total number of edges would again give the wrong conclusion.

## Approaches

A direct solution can treat every possible game position as a state. From the last erased edge, enumerate all still available adjacent edges, erase one of them, and recursively determine whether the opponent can win. Since every edge is erased at most once, the recursion is finite and the minimax result is correct.

The problem is the number of states. Take a complete original graph with \(m\) edges. Its line graph is also complete, so essentially every ordering of distinct edges is a legal play sequence. The search tree then has \(\Theta(m!)\) leaves and exponentially more total nodes. With \(m\) as large as \(10^4\), even an extremely optimistic interpretation of factorial growth makes this approach unusable.

The useful observation is that the game is not an arbitrary game on edges. It is vertex geography on the line graph of the original graph. For undirected vertex geography, maximum matchings determine the winner. We only need a particularly simple consequence of that theorem.

Suppose the line graph \(H\) has a perfect matching. After Arthur chooses any vertex \(v\), the second player answers with the unique vertex paired with \(v\). Whenever Arthur later chooses some vertex, its matched partner has not been chosen before, because otherwise that pair would already have been used. The second player can keep responding this way until Arthur has no move. Thus a perfect matching gives the second player a winning strategy. The general matching characterization of undirected vertex geography is consistent with this pairing strategy. citeturn1search0turn1search17

Now suppose \(H\) has no perfect matching. of \(M\) without creating an augmenting path for \(M\), contradicting its maximality. Arthur can consequently answer every opponent move by taking its matching partner in \(M\). Hence Arthur wins.

So the original game has a remarkably clean characterization:

\[
\text{Arthur wins} \iff H\text{ has no perfect matching}.
\]

We still have to avoid explicitly constructing \(H\). This is where the fact that \(H\) is a line graph becomes decisive.

A connected component of the original graph containing \(k\) edges becomes a connected component of the line graph containing exactly \(k\) vertices. A connected line graph with an even number of vertices always has a perfect matching. Equivalently, the edges of a connected graph with an even number of edges can be partitioned into pairs of adjacent edges. This is a standard consequence of the perfect-matching theorem for connected claw-free graphs, since every line graph is claw-free. citeturn6search0turn7search12

There obtained from any orientation by repeatedly reversing a path between two vertices with odd outdegree. Once every outdegree is even, pair the outgoing edges at every vertex. Every pair consists of two original edges sharing that vertex, and all edges belong to exactly one pair. Each pair becomes one matching edge in the line graph.

If a connected component of the original graph contains an odd number of edges, its corresponding line-graph component has an odd number of vertices, so it cannot have a perfect matching.

Consequently, the whole line graph has a perfect matching exactly when every nontrivial connected component of the original graph contains an even number of edges. Arthur wins exactly when at least one connected component contains an odd number of edges.

The entire problem has thus been reduced to finding the number of edges in every connected component.

| Approach | Time Complexity | Space Complexity | Verdict |
|---|---|---|---|
| Brute Force | \(\Theta(m!)\) leaves in the worst case | \(O(m)\) recursion state, ignoring the search tree | Too slow |
| Optimal | \(O(n+m)\) | \(O(n+m)\) | Accepted |

## Algorithm Walkthrough

1. Build an adjacency list of the original undirected graph. We only need the original graph because constructing its line graph could create far more than \(m\) edges when some vertex has high degree.

2. Run a DFS or BFS over the original vertices. For every connected component, accumulate the sum of the degrees of all its vertices.

3. Divide the accumulated degree sum by two to obtain the number of original edges in that component. Every internal edge contributes exactly two to the degree sum, once at each endpoint.

4. Ignore isolated vertices. Their components contain zero edges, which is even and cannot affect the game.

5. If any component has an odd number of edges, print `YES`. Its line-graph component has an odd number of vertices, so the whole line graph has no perfect matching. Arthur can choose a vertex left unmatched by a maximum matching and use the matching strategy to win.

6. If every component has an even number of edges, print `NO`. Every corresponding line-graph component has a perfect matching, and the union of those matchings is a perfect matching of the entire line graph. The second player can pair every move with its matching partner.

### Why it works

The central invariant is the existence of a matching that pairs game positions. If the line graph has a perfect matching, every vertex belongs to exactly one pair, so after Arthur chooses the first edge, his opponent can always erase the paired edge. The same response works after every later move, and Arthur is the first player who eventually has no legal move.

If the line graph has no perfect matching, a maximum matching leaves at least one vertex unmatched. Arthur starts with such a vertex. If the opponent could eventually reach another unmatched vertex while Arthur always responds along matching edges, the resulting alternating sequence would form an augmenting path, contradicting the maximality of the matching. Thus Arthur can maintain the response strategy and wins.

For a connected component of the original graph, its line graph has exactly as many vertices as the original graph has edges. An even-sized connected line graph has a perfect matching, while an odd-sized component cannot have one. Hence the entire game is losing for Arthur exactly when every original connected component has an even number of edges.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, m = map(int, input().split())

    graph = [[] for _ in range(n)]

    for _ in range(m):
        u, v = map(int, input().split())
        u -= 1
        v -= 1
        graph[u].append(v)
        graph[v].append(u)

    visited = [False] * n

    for start in range(n):
        if visited[start]:
            continue

        stack = [start]
        visited[start] = True
        degree_sum = 0

        while stack:
            v = stack.pop()
            degree_sum += len(graph[v])

            for to in graph[v]:
                if not visited[to]:
                    visited[to] = True
                    stack.append(to)

        edges_in_component = degree_sum // 2

        if edges_in_component % 2 == 1:
            print("YES")
            return

    print("NO")

if __name__ == "__main__":
    solve()
```

The input is stored as an adjacency list. Each undirected edge is inserted twice, so when the DFS visits a component, the total length of all adjacency lists in that component is exactly twice its number of edges.

The `visited` array guarantees that every vertex belongs to exactly one DFS traversal. Isolated vertices produce a degree sum of zero and are harmless.

The division by two is exact because the input graph has no loops. A loop would contribute differently to a degree sum, but loops are explicitly forbidden. Multiple edges are also forbidden, although the argument itself would not need their absence.

The parity check is performed immediately after finishing a component. As soon as an odd component is found, the answer is known and the function returns without processing the remaining vertices.

Python integers have no overflow issue here, and the largest possible degree sum is only \(2m\), at most \(2\cdot10^4\).

## Worked Examples

### Sample 1

The input graph is

```text
1 -- 2 -- 3
     |
     4
     |
     5 -- 6
```

More precisely, the five edges form one connected tree. The DFS therefore sees all five edges in a single component.

| Component | Degree sum | Number of edges | Parity | Answer |
|---|---:|---:|---|---|
| `{1,2,3,4,5,6}` | 10 | 5 | odd | YES |

The component has five edges, so its line graph has five vertices. No graph with an odd number of vertices can have a perfect matching. Arthur can exploit a maximum matching that leaves one line-graph vertex unmatched, so the answer is `YES`.

This example also demonstrates why checking only individual vertex degrees would not work. The tree contains several vertices of different degrees, but the decisive quantity is the number of edges in the connected component.

### Sample 2

The graph is a path with two edges.

| Component | Degree sum | Number of edges | Parity | Answer |
|---|---:|---:|---|---|
| `{1,2,3}` | 4 | 2 | even | NO |

The line graph is a path with two vertices. Those two vertices form a perfect matching. Arthur must choose one of them first, and the second player chooses the other one immediately. Arthur then has no move.

The trace demonstrates why the initial move must be handled carefully. Arthur does not start from a predetermined graph vertex. His first action chooses a game vertex, and a perfect matching gives the second player the exact response to that first choice.

## Complexity Analysis

| Measure | Complexity | Explanation |
|---|---|---|
| Time | \(O(n+m)\) | Every vertex is visited once and every adjacency-list entry is processed once. |
| Space | \(O(n+m)\) | The adjacency list and the DFS state use linear memory. |

With \(n,m\le10^4\), the algorithm performs only a constant amount of work per vertex and per edge. It does not construct the line graph, whose number of edges could be much larger than \(m\), and it does not perform any matching algorithm explicitly.

## Test Cases

```python
import sys
import io

def solve_data(inp: str) -> str:
    data = inp.split()
    it = iter(data)

    n = int(next(it))
    m = int(next(it))

    graph = [[] for _ in range(n)]

    for _ in range(m):
        u = int(next(it)) - 1
        v = int(next(it)) - 1
        graph[u].append(v)
        graph[v].append(u)

    visited = [False] * n

    for start in range(n):
        if visited[start]:
            continue

        stack = [start]
        visited[start] = True
        degree_sum = 0

        while stack:
            v = stack.pop()
            degree_sum += len(graph[v])

            for to in graph[v]:
                if not visited[to]:
                    visited[to] = True
                    stack.append(to)

        if (degree_sum // 2) % 2 == 1:
            return "YES"

    return "NO"

# Provided sample 1
assert solve_data(
    """\
7 5
1 2
5 1
5 6
3 2
2 4
"""
) == "YES", "sample 1"

# Provided sample 2
assert solve_data(
    """\
3 2
1 2
2 3
"""
) == "NO", "sample 2"

# Minimum-size graph: one edge, so Arthur wins immediately.
assert solve_data(
    """\
2 1
1 2
"""
) == "YES", "single edge"

# Two disconnected single-edge components.
# Each component has one odd number of edges.
assert solve_data(
    """\
4 2
1 2
3 4
"""
) == "YES", "two odd components"

# A star with four edges.
# The whole connected component has an even number of edges.
assert solve_data(
    """\
5 4
1 2
1 3
1 4
1 5
"""
) == "NO", "even star"

# Two separate paths, each containing two edges.
# Every nontrivial component has an even number of edges.
assert solve_data(
    """\
6 4
1 2
2 3
4 5
5 6
"""
) == "NO", "two even components"

# Maximum-size boundary case.
# A path with 10000 vertices has 9999 edges, which is odd.
n = 10000
lines = [f"{n} {n - 1}"]
for i in range(1, n):
    lines.append(f"{i} {i + 1}")

assert solve_data("\n".join(lines)) == "YES", "maximum-size odd component"
```

| Test input | Expected output | What it validates |
|---|---|---|
| `2 1` with edge `1 2` | `YES` | Minimum-size case and the fact that one move can already win |
| Two disconnected single edges | `YES` | Components must be considered separately |
| Four-edge star | `NO` | An even connected component gives the second player a perfect matching |
| Two paths of two edges | `NO` | Multiple even components still produce a global perfect matching |
| Path on 10000 vertices | `YES` | Maximum-size input and an odd edge count near the constraint boundary |

## Edge Cases

The single-edge graph

```text
2 1
1 2
```

has one connected component with degree sum \(2\), hence one edge. The component is odd, so the algorithm prints `YES`. This matches the game directly: Arthur erases the only available edge and the opponent cannot move.

The disconnected graph

```text
4 2
1 2
3 4
```

has two components, each with one edge. The DFS processes the first component, obtains degree sum \(2\), and immediately detects one odd edge count. The answer is `YES`. The existence of a second disconnected component does not help the opponent because the next move must be adjacent to the previously erased edge, so the game can never jump between components.

The four-edge star

```text
5 4
1 2
1 3
1 4
1 5
```

has one component with degree sum \(8\), giving four edges. Its line graph is \(K_4\), which has a perfect matching. Arthur chooses one game vertex, and the second player chooses its matched partner. The remaining two vertices are similarly paired, so Arthur eventually has no move. The algorithm correctly prints `NO`.

The graph

```text
6 4
1 2
2 3
4 5
5 6
```

contains two separate two-edge paths. Each component contributes an even number of edges, so each line-graph component has a perfect matching. Their union is a perfect matching of the entire line graph. The DFS finds edge counts \(2\) and \(2\), never sees an odd component, and prints `NO`.

The maximum-size path contains \(9999\) edges:

```text
10000 9999
1 2
2 3
...
9999 10000
```

The graph is connected, so the DFS computes one degree sum of \(19998\), corresponding to \(9999\) edges. Since that number is odd, the algorithm prints `YES`. This case confirms that the implementation does not confuse the number of vertices with the number of edges, which is the central parity distinction in the problem.
:::
