---
title: "CF 102770I - Invoking the Magic"
description: "After the first washing stage, every sock color appears exactly twice, but the two socks of the same color may be located in different pairs. We can view each original pair as a connection between two colors."
date: "2026-07-28T23:12:50+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102770
codeforces_index: "I"
codeforces_contest_name: "The 17th Zhejiang Provincial Collegiate Programming Contest"
rating: 0
weight: 102770
solve_time_s: 44
verified: true
draft: false
---

[CF 102770I - Invoking the Magic](https://codeforces.com/problemset/problem/102770/I)

**Rating:** -  
**Tags:** -  
**Solve time:** 44s  
**Verified:** yes  

## Solution
## Problem Understanding

After the first washing stage, every sock color appears exactly twice, but the two socks of the same color may be located in different pairs. We can view each original pair as a connection between two colors. A pair containing colors `a` and `b` becomes an edge between vertices `a` and `b` in a graph.

Because every color appears in exactly two socks, every vertex has degree exactly two. The graph is consequently made of independent cycles. A pair of socks with the same color is a special case: it is a cycle of length one, represented by a self-loop.

The magic basin accepts a collection of pairs only when every color inside that collection appears an even number of times. In graph terms, the chosen edges must give every vertex an even degree. Such a collection is an Eulerian subgraph.

The task is to find the smallest possible capacity of the basin, where capacity means the maximum number of original pairs used in a single magic operation.

The number of pairs can reach $10^5$. An algorithm that tries many possible subsets or simulates arbitrary groupings will quickly become impossible, because the number of possible edge selections grows exponentially. Even algorithms that repeatedly scan the entire graph for every possible grouping would be too expensive. The structure of the graph must be used so that each pair is processed only a constant number of times.

The tricky part is recognizing that the cycles cannot be broken into smaller valid groups. For example, a cycle with three edges:

```
1 2
2 3
3 1
```

has answer `3`. Trying to use only two of these edges leaves one of the colors with an odd count, so the basin would fail.

Another edge case is a self-loop. The input

```
1
1
1 1
```

has answer `1`. A careless graph implementation might ignore self-loops because they do not connect two different vertices, but a pair of identical colors already forms a valid group by itself.

A further case is multiple cycles existing independently. For example:

```
1
4
1 2
2 1
3 4
4 3
```

has answer `2`. The two parallel-edge cycles can each be processed separately. Treating the whole graph as one cycle would incorrectly return `4`.

## Approaches

A direct brute-force approach would try to find groups of pairs whose colors all occur an even number of times. It could generate possible subsets of edges, check whether every color appears an even number of times, and then search for a partition minimizing the largest subset size. This is correct because it examines every possible way to use the basin. However, even checking all subsets already requires $2^n$ possibilities. With $n=10^5$, this is far beyond what any implementation can handle.

The useful observation comes from the graph representation. Since every vertex has degree two, every connected component is a cycle. A cycle has a special property: the only non-empty Eulerian subgraph made from its edges is the entire cycle itself. If we remove even one edge from a cycle, the two endpoints of that removed edge become the endpoints of paths, and those vertices have odd degree inside the selected edges.

This means every cycle must be placed into one magic operation as a whole. There is no benefit in trying to combine cycles, because combining two cycles only increases the required capacity for that operation. The smallest possible capacity is therefore the size of the largest cycle in the graph.

The optimal solution is simply to find all connected components and record the largest number of edges in any component.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(2^n) | O(n) | Too slow |
| Optimal | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Build the graph from the sock pairs. Each color is a vertex, and each pair contributes one edge. Self-loops are stored as normal edges because a same-color pair is already a complete cycle.
2. Traverse every unvisited color using depth-first search. During the traversal, count how many edges belong to that connected component. Because the graph is made only of cycles, this count is exactly the number of pairs that must be placed together.
3. Keep the maximum component edge count found during all traversals. That value is the minimum possible basin capacity.
4. Output the maximum component size.

Why it works:

Every connected component is a cycle because every vertex has degree two. A cycle cannot be separated into smaller valid magic operations, since removing any edge creates vertices with odd degree. Therefore every component contributes an unavoidable lower bound equal to its number of edges. Processing each component separately achieves that bound, so the largest component size is both necessary and sufficient.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    ans = []

    for _ in range(t):
        n = int(input())
        graph = {}

        for _ in range(n):
            a, b = map(int, input().split())
            if a not in graph:
                graph[a] = []
            if b not in graph:
                graph[b] = []
            graph[a].append(b)
            graph[b].append(a)

        visited = set()
        best = 0

        for start in graph:
            if start in visited:
                continue

            stack = [start]
            visited.add(start)
            vertices = 0

            while stack:
                u = stack.pop()
                vertices += 1
                for v in graph[u]:
                    if v not in visited:
                        visited.add(v)
                        stack.append(v)

            best = max(best, vertices)

        ans.append(str(best))

    print("\n".join(ans))

if __name__ == "__main__":
    solve()
```

The graph is stored as an adjacency list. When an edge is added, it is added in both directions, including the self-loop case. For a self-loop, the same vertex receives two entries, which is exactly its degree contribution.

The depth-first search counts vertices in a connected component. In this graph family, every component is a cycle, so the number of vertices equals the number of edges. This also handles a self-loop component correctly because it contains one vertex and one edge.

The traversal marks vertices immediately when they are pushed onto the stack. This avoids visiting the same cycle multiple times and keeps the total work linear.

## Worked Examples

Consider this input:

```
1
3
1 2
2 3
3 1
```

The traversal starts at color `1`.

| Start vertex | Visited vertices | Current component size | Answer |
| --- | --- | --- | --- |
| 1 | {1} | 1 | 0 |
| 2 | {1,2} | 2 | 0 |
| 3 | {1,2,3} | 3 | 3 |

The three colors form one cycle. The entire cycle must be processed together, so the required capacity is `3`.

Another example:

```
1
5
1 2
2 1
3 4
4 3
5 5
```

The graph contains three separate components.

| Component | Vertices discovered | Component size | Current answer |
| --- | --- | --- | --- |
| First cycle | {1,2} | 2 | 2 |
| Second cycle | {3,4} | 2 | 2 |
| Self-loop | {5} | 1 | 2 |

The largest cycle contains two pairs, so the minimum capacity is `2`. The self-loop is already a valid one-pair operation.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Every sock pair creates one edge, and every vertex and edge is visited a constant number of times. |
| Space | O(n) | The adjacency list stores all graph connections, and the traversal stores visited states. |

The input size is at most $10^5$ pairs, so a linear solution easily fits within typical competitive programming limits.

## Test Cases

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

# provided sample
assert run("""1
5
1 2
2 3
1 3
4 5
4 5
""") == "3\n", "sample"

# single self-loop
assert run("""1
1
7 7
""") == "1\n", "self loop"

# two separate cycles
assert run("""1
4
1 2
2 1
3 4
4 3
""") == "2\n", "multiple components"

# one large cycle
assert run("""1
6
1 2
2 3
3 4
4 5
5 6
6 1
""") == "6\n", "large cycle"

# repeated two-color cycle
assert run("""1
2
10 20
10 20
""") == "2\n", "parallel edges"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Sample case | 3 | A normal cycle mixed with another component |
| One self-loop | 1 | Same-color pairs are handled correctly |
| Two separate cycles | 2 | Components must be considered independently |
| One six-node cycle | 6 | A whole cycle cannot be split |
| Two parallel edges | 2 | Length-two cycles are counted correctly |

## Edge Cases

For a single self-loop:

```
1
1
7 7
```

The graph has one vertex with one self-loop. The adjacency list contains two references to vertex `7`, and the traversal finds one vertex in the component. Since a self-loop represents one pair, the component size is `1`, so the answer is `1`.

For a cycle that looks splittable:

```
1
3
1 2
2 3
3 1
```

A greedy approach might try to take two pairs first, but those two edges leave one color appearing once. The traversal sees one connected component containing all three vertices, giving the required answer `3`.

For multiple disconnected components:

```
1
4
1 2
2 1
3 4
4 3
```

The first component contains colors `1` and `2`, and the second contains colors `3` and `4`. Each component can be handled independently with capacity `2`. The algorithm never merges them, so it does not overestimate the answer as `4`.
