---
title: "CF 102407E - \u0421\u0442\u0440\u0430\u043d\u043d\u0430\u044f \u0438\u0433\u0440\u0430 \u043d\u0430 \u0433\u0440\u0430\u0444\u0435"
description: "The board is an undirected simple graph. A move does not remove a vertex, it removes an edge, and the next move has to use an edge sharing an endpoint with the edge removed immediately before it. An edge can be used only once because it disappears after being selected."
date: "2026-08-11T16:14:44+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102407
codeforces_index: "E"
codeforces_contest_name: "\u0418\u043d\u0442\u0435\u0440\u043d\u0435\u0442-\u043e\u043b\u0438\u043c\u043f\u0438\u0430\u0434\u044b, \u0421\u0435\u0437\u043e\u043d 2019-2020, \u0412\u0442\u043e\u0440\u0430\u044f \u043a\u043e\u043c\u0430\u043d\u0434\u043d\u0430\u044f \u043e\u043b\u0438\u043c\u043f\u0438\u0430\u0434\u0430, \u0443\u0441\u043b\u043e\u0436\u043d\u0435\u043d\u043d\u0430\u044f \u043d\u043e\u043c\u0438\u043d\u0430\u0446\u0438\u044f"
rating: 0
weight: 102407
solve_time_s: 148
verified: true
draft: false
---

[CF 102407E - \u0421\u0442\u0440\u0430\u043d\u043d\u0430\u044f \u0438\u0433\u0440\u0430 \u043d\u0430 \u0433\u0440\u0430\u0444\u0435](https://codeforces.com/problemset/problem/102407/E)

**Rating:** -  
**Tags:** -  
**Solve time:** 2m 28s  
**Verified:** yes  

## Solution
## Problem Understanding

The board is an undirected simple graph. A move does not remove a vertex, it removes an edge, and the next move has to use an edge sharing an endpoint with the edge removed immediately before it. An edge can be used only once because it disappears after being selected.

A useful way to reinterpret the game is to forget the original vertices for a moment. Create a new graph whose vertices are the original edges. Connect two new vertices exactly when the corresponding original edges share an endpoint. This is the **line graph** of the original graph. The game is now the following: the first player chooses any vertex of the line graph, and every subsequent move chooses an unused adjacent vertex. This is the undirected vertex version of Geography. The first player wins if they can choose the initial vertex so that optimal play eventually leaves the second player without a move. The matching characterization of this game says that the second player wins from every possible starting vertex exactly when the line graph has a perfect matching.

The input contains at most (10^4) original vertices and (10^4) original edges. The official limits are 2 seconds and 512 MB. A direct construction of the line graph is already suspicious because a single high-degree vertex in the original graph creates a clique containing all of its incident edges. With (10^4) edges, that clique can contain nearly (10^4) vertices and around (5\cdot10^7) adjacency pairs. More importantly, brute-force game search is exponential or worse, so the intended solution has to exploit the structure of the line graph rather than enumerate game states.

There are several edge cases that expose common incorrect interpretations. First, the parity of the **total** number of edges is not enough. Consider

```
4 2
1 2
3 4
```

The total number of edges is 2, but each connected component contains one edge. The two edges are not adjacent, so after the first player chooses either one, the second player has no move. The answer is `YES`. A solution checking only `m % 2` would incorrectly print `NO`.

Second, isolated vertices have no effect. For

```
4 1
1 2
```

vertices 3 and 4 cannot participate in any move. The only edge forms a one-vertex component in the line graph, so Arthur wins immediately and the answer is `YES`. Counting vertices instead of edges, or requiring every original vertex to belong to a nontrivial component, would give the wrong result.

Third, a connected component with an even number of edges gives the opposite outcome. For

```
4 3
1 2
1 3
1 4
```

the three original edges are all mutually adjacent, so the line graph is (K_3). Arthur chooses one edge, his opponent chooses another, and Arthur chooses the last one, so Arthur wins. The answer is `YES`. A careless argument based only on the fact that every connected component is connected would miss the parity of its edge count.

## Approaches

The brute-force approach is to treat the current erased edge and the set of already erased edges as the complete game state. For every legal next edge, recursively determine whether the opponent can win, and declare the current state winning if at least one move leads to a losing state for the opponent. This is correct because the game is finite and every possible continuation is considered.

The problem is the number of continuations. Take an original star with (m) edges. Every two edges of the star share its center, so its line graph is (K_m). After the first edge is selected, any remaining edge is legal, then any remaining edge after that, and so on. The recursion can consequently examine on the order of (m!) different play sequences. With (m) close to (10^4), this is completely infeasible. Even memoization does not make the general state space practical, because a state is essentially a subset of used edges together with the current edge, giving (O(m2^m)) possible states.

The key observation is that this particular undirected game has a matching characterization. In undirected vertex Geography, a graph with a perfect matching gives the second player a simple response strategy. Whenever the first player enters a vertex, the second player moves to its partner in the fixed perfect matching. Conversely, if a maximum matching leaves some vertex unmatched, the first player can start there and use the matching edges as a response strategy. If the strategy ever failed because an unmatched vertex became reachable at the wrong time, the alternating path would be an augmenting path, contradicting maximality of the matching. This is the standard matching characterization of undirected vertex Geography.

Our first player is allowed to choose the starting vertex freely. Consequently, the line graph is losing for the first player exactly when it has a perfect matching. We therefore only need to decide whether the line graph of the given graph has a perfect matching.

There is another structural simplification. Consider one connected component of the original graph containing (k) edges. Its line graph is connected and has exactly (k) vertices. A connected line graph with an even number of vertices always has a perfect matching. Equivalently, the edges of every connected graph with an even number of edges can be partitioned into pairs such that the two edges in each pair share a vertex. This is a standard property of line graphs.

The converse is immediate because a perfect matching can exist only in a graph with an even number of vertices. Thus a connected component of the original graph produces a perfectly matchable component of the line graph exactly when its number of original edges is even.

So the entire game reduces to a very simple condition: Arthur loses exactly when **every connected component of the original graph contains an even number of edges**. If at least one connected component has an odd number of edges, its line-graph component has odd size and no perfect matching, giving Arthur a winning starting edge.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | (O(m!)) | (O(m)) recursion depth | Too slow |
| Optimal | (O(n+m)) | (O(n)) | Accepted |

The optimal algorithm does not need to construct the line graph and does not need to know the actual winning sequence of erased edges. It only needs the parity of the number of edges in each connected component.

## Algorithm Walkthrough

1. Build the connected components of the original graph with a Disjoint Set Union structure. For every input edge ((u,v)), unite (u) and (v). The only information needed from the component structure is which component contains each edge.
2. After all unions are finished, scan the original edges once more. For an edge ((u,v)), find the representative of (u), which is also the representative of (v), and increment the edge count of that component. Counting edges after all unions avoids any dependence on the order in which the input edges appeared.
3. Check every component that contains at least one edge. If its edge count is odd, print `YES`. Such a component produces a line-graph component with an odd number of vertices, so that component cannot have a perfect matching. Arthur can start with an edge from it and has a winning strategy.
4. If every nonempty component has an even number of edges, print `NO`. Each corresponding line-graph component has an even number of vertices and therefore has a perfect matching. The disjoint union of these perfect matchings is a perfect matching of the entire line graph, so the second player can answer every initial choice using the matching strategy.

### Why it works

The central invariant is the correspondence between the original graph's connected components and the line graph's connected components. Two original edges can be connected through a sequence of adjacent original edges exactly when they belong to the same connected component, so no game move can cross from one original component to another.

Inside one connected component with (k) edges, the line graph has (k) vertices. If (k) is odd, it cannot have a perfect matching, so the free-start undirected Geography game on that component is winning for the first player. If (k) is even, the line graph has a perfect matching, so the second player can always reply along the matching edge. The global line graph has a perfect matching precisely when every nonempty original component has an even edge count. Hence the algorithm prints `YES` exactly when Arthur has a winning component to start in.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, m = map(int, input().split())

    parent = list(range(n))
    size = [1] * n
    edges = []

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    def union(a, b):
        a = find(a)
        b = find(b)
        if a == b:
            return

        if size[a] < size[b]:
            a, b = b, a

        parent[b] = a
        size[a] += size[b]

    for _ in range(m):
        u, v = map(int, input().split())
        u -= 1
        v -= 1
        edges.append((u, v))
        union(u, v)

    edge_count = [0] * n

    for u, _ in edges:
        root = find(u)
        edge_count[root] += 1

    for v in range(n):
        if edge_count[v] % 2 == 1:
            print("YES")
            return

    print("NO")

if __name__ == "__main__":
    solve()
```

The first loop stores every edge and joins its endpoints in the DSU. Path compression in `find` and union by component size make the total DSU work effectively linear for these constraints.

The second loop counts edges by their final component representative. Using the first endpoint is sufficient because every edge was already united, so both endpoints belong to the same DSU component. We deliberately perform this counting after all unions. If it were done while reading the input, an edge could initially be assigned to a representative that later gets merged into another component.

The final loop checks parity only at DSU representatives that have a nonzero count. Non-representatives have count zero because every edge is assigned using its final representative. Isolated vertices also have count zero, which correctly makes them irrelevant to the game.

There is no integer-overflow issue in Python, and the largest possible component count is only (10^4). The indexing is converted from the problem's one-based vertices to zero-based Python arrays immediately, so the DSU has exactly (n) elements.

## Worked Examples

### Sample 1

The graph is

```
7 5
1 2
5 1
5 6
3 2
2 4
```

All five edges belong to the same connected component. The DSU operations merge all vertices that appear in the graph, and the final edge count of that component is 5.

| Component representative | Edge count | Parity | Decision |
| --- | --- | --- | --- |
| component containing 1 | 5 | odd | `YES` |

The corresponding line graph has five vertices. Since its number of vertices is odd, it cannot have a perfect matching. Arthur can choose an edge in this component as his first move and force a win. This matches the sample output `YES`.

### Sample 2

The graph is

```
3 2
1 2
2 3
```

Both edges belong to the same connected component, whose edge count is 2.

| Component representative | Edge count | Parity | Decision |
| --- | --- | --- | --- |
| component containing 1 | 2 | even | continue |
| all components | even | even | `NO` |

The two original edges share vertex 2, so the line graph contains two adjacent vertices. The first player selects one, and the second player selects the other. The first player then has no move. Thus Arthur loses and the answer is `NO`.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | (O(n+m)) | DSU operations and the two linear scans over vertices and edges |
| Space | (O(n+m)) | DSU arrays plus storage for the original edges |

With (n,m\le 10^4), this is comfortably inside the official 2-second and 512 MB limits. More significantly, the algorithm never constructs the potentially dense line graph and never explores game states.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def solve():
    input = sys.stdin.readline

    n, m = map(int, input().split())
    parent = list(range(n))
    size = [1] * n
    edges = []

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    def union(a, b):
        a = find(a)
        b = find(b)

        if a == b:
            return

        if size[a] < size[b]:
            a, b = b, a

        parent[b] = a
        size[a] += size[b]

    for _ in range(m):
        u, v = map(int, input().split())
        u -= 1
        v -= 1
        edges.append((u, v))
        union(u, v)

    edge_count = [0] * n

    for u, _ in edges:
        edge_count[find(u)] += 1

    for count in edge_count:
        if count % 2 == 1:
            return "YES"

    return "NO"

def run(inp: str) -> str:
    old_stdin = sys.stdin
    sys.stdin = io.StringIO(inp)
    try:
        return solve()
    finally:
        sys.stdin = old_stdin

# Provided samples
assert run(
    """7 5
1 2
5 1
5 6
3 2
2 4
"""
) == "YES", "sample 1"

assert run(
    """3 2
1 2
2 3
"""
) == "NO", "sample 2"

# Minimum-size graph: one edge is an odd component.
assert run(
    """2 1
1 2
"""
) == "YES", "minimum-size graph"

# Two separate one-edge components. Total m is even, but
# each component is odd, so checking only m % 2 would fail.
assert run(
    """4 2
1 2
3 4
"""
) == "YES", "disconnected odd components"

# Four edges incident to the same center. The line graph is K4,
# which has a perfect matching.
assert run(
    """5 4
1 2
1 3
1 4
1 5
"""
) == "NO", "even star"

# Three edges incident to the same center. The line graph is K3,
# which has odd size and no perfect matching.
assert run(
    """4 3
1 2
1 3
1 4
"""
) == "YES", "odd star"

# Maximum-size instance: n = m = 10000.
# A path with 9999 edges plus edge (1, 3) has 10000 edges
# and remains connected, so the answer is NO.
n = 10000
edges = [(i, i + 1) for i in range(1, n)]
edges.append((1, 3))

inp = f"{n} {len(edges)}\n"
inp += "\n".join(f"{u} {v}" for u, v in edges) + "\n"

assert run(inp) == "NO", "maximum-size connected even-edge graph"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `2 1 / 1 2` | `YES` | Minimum possible graph and odd component |
| `4 2 / 1 2 / 3 4` | `YES` | Disconnected components and the fact that global edge parity is insufficient |
| `5 4 / 1 2 / 1 3 / 1 4 / 1 5` | `NO` | Four mutually adjacent edges and an even component |
| `4 3 / 1 2 / 1 3 / 1 4` | `YES` | Odd component with many adjacent edges |
| `10000 10000` connected construction | `NO` | Maximum bounds and large connected component |

## Edge Cases

For the disconnected case

```
4 2
1 2
3 4
```

the DSU produces two components. The first contains one edge and the second also contains one edge, so their counts are `1` and `1`. The algorithm encounters an odd count immediately and prints `YES`. This is exactly the situation where checking only the parity of `m` fails, because (1+1=2) is even while neither component has a perfect matching in its line graph.

For isolated vertices, consider

```
4 1
1 2
```

The DSU creates one component containing vertices 1 and 2 with one edge, while vertices 3 and 4 remain isolated with edge count zero. The nonzero component has odd size, so the algorithm prints `YES`. The zero-edge components do not matter because there is no edge to select from them and consequently no game position associated with them.

For the odd star

```
4 3
1 2
1 3
1 4
```

all three edges are in one component, so the edge count is 3. The line graph is (K_3). Arthur can erase any edge first, his opponent can erase one of the two remaining edges, and Arthur erases the last one. The algorithm prints `YES` without ever constructing that triangle.

For the even star

```
5 4
1 2
1 3
1 4
1 5
```

the component contains four edges, and every pair of those edges is adjacent. The line graph is (K_4), whose perfect matching can pair the four vertices into two pairs. The second player can always answer the first player's chosen edge with its matching partner, so Arthur loses and the algorithm prints `NO`.

The most dangerous implementation mistake is to count edges before the DSU has finished merging components. For example,

```
4 2
1 2
2 3
```

first joins 1 with 2, then joins 2 with 3. Both edges ultimately belong to one component, whose count is 2, so the answer is `NO`. Counting against stale representatives during input processing can split those two edges between temporary component IDs and produce the wrong parity. The solution avoids that by storing the edges and counting them only after all unions are complete.

The final boundary case is a graph with (10^4) vertices and (10^4) edges. A connected construction is obtained from the path

```
1-2-3-...-10000
```

with one extra edge `1 3`. It has exactly 10000 edges, all in one connected component, so the component parity is even and the answer is `NO`. The DSU processes the entire instance with the same linear structure as a small graph, which is why the solution remains fast at the upper bound.
