---
title: "CF 445B - DZY Loves Chemistry"
description: "The chemicals and reactions form an undirected graph. Each vertex represents a chemical, and an edge between two vertices means those two chemicals react. We start with danger equal to 1. Chemicals are poured one at a time in any order."
date: "2026-06-07T16:02:53+07:00"
tags: ["codeforces", "competitive-programming", "dfs-and-similar", "dsu", "greedy"]
categories: ["algorithms"]
codeforces_contest: 445
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 254 (Div. 2)"
rating: 1400
weight: 445
solve_time_s: 109
verified: true
draft: false
---

[CF 445B - DZY Loves Chemistry](https://codeforces.com/problemset/problem/445/B)

**Rating:** 1400  
**Tags:** dfs and similar, dsu, greedy  
**Solve time:** 1m 49s  
**Verified:** yes  

## Solution
## Problem Understanding

The chemicals and reactions form an undirected graph. Each vertex represents a chemical, and an edge between two vertices means those two chemicals react.

We start with danger equal to 1. Chemicals are poured one at a time in any order. Whenever the newly added chemical has at least one reaction edge to a chemical that is already inside the tube, the current danger is multiplied by 2. Otherwise the danger stays unchanged.

The task is to choose the pouring order that maximizes the final danger.

A direct reading suggests that the answer depends on the ordering, but the graph structure hides a much simpler pattern. The key question is how many times we can force a multiplication by 2.

The constraints are small enough that any linear or near linear graph algorithm is easily acceptable. Even if $n$ and $m$ are only around a few dozen in the original problem, the intended solution is based on connected components and runs in $O(n+m)$. Brute forcing permutations would require $n!$ possibilities, which becomes impossible almost immediately.

Several edge cases are easy to misinterpret.

Consider a graph with no edges:

```
3 0
```

No chemical ever reacts with a previously inserted one. The danger never changes, so the answer is:

```
1
```

A careless approach that counts vertices instead of reactions might incorrectly produce a larger value.

Consider a connected chain:

```
3 2
1 2
2 3
```

One optimal order is 1, 2, 3. The first chemical gives no multiplication. The second and third both react with something already present, so danger is multiplied twice. The answer is:

```
4
```

A common mistake is to think every edge contributes a multiplication. There are two edges here, but only two successful insertions after the first vertex.

Consider two disconnected components:

```
4 2
1 2
3 4
```

Each component contributes one multiplication. The answer is:

```
4
```

Treating the whole graph as a single structure would incorrectly give $2^3=8$.

## Approaches

The brute-force idea is to try every possible pouring order. For each permutation, we simulate the process and count how many insertions cause a reaction with an already inserted chemical.

This is correct because it explicitly evaluates every valid ordering. Unfortunately, there are $n!$ permutations. Even for $n=15$, this is already over a trillion possibilities, making it completely infeasible.

To find a better approach, we need to understand what happens inside one connected component.

Take any connected component containing $k$ vertices. The first chemical poured from that component cannot react with anything from the same component because none of its component mates are present yet. Every other vertex can be arranged to react.

Why? Start from any vertex of the component. Since the component is connected, we can reveal the remaining vertices in a DFS or BFS order. Every newly revealed vertex has an edge to some previously revealed vertex, so each of those insertions multiplies the danger by 2.

That means a connected component of size $k$ contributes exactly $k-1$ multiplications.

Different connected components are independent. Each component contributes its own $k-1$ multiplications, and summing over all components gives

$$\sum (k_i - 1)$$

where $k_i$ is the size of the $i$-th connected component.

Since the component sizes add up to $n$,

$$\sum (k_i - 1) = n - c$$

where $c$ is the number of connected components.

The final danger is therefore

$$2^{\,n-c}.$$

All that remains is to count connected components with DFS, BFS, or DSU.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(n! \cdot (n+m))$ | $O(n)$ | Too slow |
| Optimal | $O(n+m)$ | $O(n)$ | Accepted |

## Algorithm Walkthrough

1. Build the undirected graph from the reaction pairs.
2. Find all connected components using DFS.
3. For each unvisited vertex, start a DFS and count how many vertices belong to its component.
4. If a component contains $k$ vertices, add $k-1$ to the total number of danger multiplications.

The first vertex of the component cannot create a reaction. Every remaining vertex can be inserted after a neighbor that is already present.
5. After processing all components, let the total number of multiplications be $cnt$.
6. The answer is $2^{cnt}$.
7. Print the answer.

### Why it works

Inside a connected component of size $k$, at least one vertex must be inserted first. That insertion cannot multiply the danger because no other vertex of the component is present.

Every other vertex can be inserted after reaching it through a DFS or BFS traversal. At that moment, one of its neighbors is already present, so the insertion multiplies the danger by 2.

Thus a component contributes exactly $k-1$ multiplications, no more and no less. Summing over all components gives the total number of multiplications. Since each multiplication doubles the danger and the initial danger is 1, the final answer is $2^{\sum(k-1)}$.

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
    multiplications = 0

    for start in range(n):
        if visited[start]:
            continue

        stack = [start]
        visited[start] = True
        size = 0

        while stack:
            v = stack.pop()
            size += 1

            for to in graph[v]:
                if not visited[to]:
                    visited[to] = True
                    stack.append(to)

        multiplications += size - 1

    print(1 << multiplications)

if __name__ == "__main__":
    solve()
```

The graph is stored as an adjacency list because the input naturally describes edges between chemicals.

The DFS counts the size of each connected component. Once a component size is known, we add `size - 1` to the number of successful danger doublings.

The final answer is a power of two. Python integers have arbitrary precision, so even the largest valid answer fits comfortably. Using `1 << multiplications` computes $2^{\text{multiplications}}$ directly and efficiently.

The vertices in the input are numbered from 1, while Python lists use 0-based indexing, so each endpoint is decremented exactly once when reading the edges.

## Worked Examples

### Example 1

Input:

```
1 0
```

| Step | Component Size | Multiplications Added | Total Multiplications |
| --- | --- | --- | --- |
| DFS from 1 | 1 | 0 | 0 |

Final answer:

$$2^0 = 1$$

Output:

```
1
```

This demonstrates the smallest possible graph. A single isolated chemical never creates a reaction.

### Example 2

Input:

```
4 2
1 2
3 4
```

| Step | Component Size | Multiplications Added | Total Multiplications |
| --- | --- | --- | --- |
| DFS from 1 | 2 | 1 | 1 |
| DFS from 3 | 2 | 1 | 2 |

Final answer:

$$2^2 = 4$$

Output:

```
4
```

This example shows that disconnected components contribute independently. Each component of size two contributes one doubling.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n+m)$ | Each vertex and edge is visited at most once during DFS |
| Space | $O(n+m)$ | Adjacency list plus visited array |

The algorithm performs a single graph traversal. Every edge is examined a constant number of times, making it easily fast enough for the problem limits.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    input = sys.stdin.readline

    n, m = map(int, input().split())

    graph = [[] for _ in range(n)]

    for _ in range(m):
        u, v = map(int, input().split())
        u -= 1
        v -= 1
        graph[u].append(v)
        graph[v].append(u)

    visited = [False] * n
    mult = 0

    for i in range(n):
        if visited[i]:
            continue

        stack = [i]
        visited[i] = True
        size = 0

        while stack:
            v = stack.pop()
            size += 1

            for to in graph[v]:
                if not visited[to]:
                    visited[to] = True
                    stack.append(to)

        mult += size - 1

    return str(1 << mult)

# provided sample
assert run("1 0\n") == "1", "sample 1"

# single edge
assert run("2 1\n1 2\n") == "2", "one reaction"

# chain of three vertices
assert run("3 2\n1 2\n2 3\n") == "4", "connected component size 3"

# two disconnected pairs
assert run("4 2\n1 2\n3 4\n") == "4", "two components"

# complete graph on four vertices
assert run(
    "4 6\n"
    "1 2\n"
    "1 3\n"
    "1 4\n"
    "2 3\n"
    "2 4\n"
    "3 4\n"
) == "8", "single component size 4"

# all isolated vertices
assert run("5 0\n") == "1", "no reactions"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 0` | `1` | Minimum input |
| `2 1` | `2` | Single connected component of size 2 |
| Chain of length 3 | `4` | Connected traversal logic |
| Two disconnected pairs | `4` | Multiple components |
| Complete graph with 4 vertices | `8` | Dense graph, answer depends only on component size |
| `5 0` | `1` | All vertices isolated |

## Edge Cases

### All chemicals are isolated

Input:

```
4 0
```

The graph contains four connected components, each of size 1.

| Component Size | Contribution |
| --- | --- |
| 1 | 0 |
| 1 | 0 |
| 1 | 0 |
| 1 | 0 |

Total multiplications equal 0, so the answer is:

$$2^0 = 1.$$

The algorithm correctly computes `size - 1 = 0` for every component.

### One large connected component

Input:

```
4 3
1 2
2 3
3 4
```

The graph is connected.

| Component Size | Contribution |
| --- | --- |
| 4 | 3 |

The answer is:

$$2^3 = 8.$$

The DFS finds a single component of size 4 and adds exactly 3 multiplications.

### Multiple disconnected components of different sizes

Input:

```
6 3
1 2
2 3
5 6
```

Component sizes are 3, 1, and 2.

| Component Size | Contribution |
| --- | --- |
| 3 | 2 |
| 1 | 0 |
| 2 | 1 |

Total multiplications:

$$2 + 0 + 1 = 3.$$

Final answer:

$$2^3 = 8.$$

This confirms that the algorithm handles isolated vertices and nontrivial components together without any special cases.
