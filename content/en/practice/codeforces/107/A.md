---
title: "CF 107A - Dorm Water Supply"
description: "The houses and pipes form a directed graph with a very special structure. Every house can have at most one incoming pipe and at most one outgoing pipe. That restriction changes the graph from a general directed graph into a collection of independent chains."
date: "2026-05-28T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "dfs-and-similar", "graphs"]
categories: ["algorithms"]
codeforces_contest: 107
codeforces_index: "A"
codeforces_contest_name: "Codeforces Beta Round 83 (Div. 1 Only)"
rating: 1400
weight: 107
solve_time_s: 139
verified: true
draft: false
---

[CF 107A - Dorm Water Supply](https://codeforces.com/problemset/problem/107/A)

**Rating:** 1400  
**Tags:** dfs and similar, graphs  
**Solve time:** 2m 19s  
**Verified:** yes  

## Solution
## Problem Understanding

The houses and pipes form a directed graph with a very special structure. Every house can have at most one incoming pipe and at most one outgoing pipe. That restriction changes the graph from a general directed graph into a collection of independent chains.

A house with outgoing flow but no incoming flow is the start of a chain. That house needs a tank. A house with incoming flow but no outgoing flow is the end of a chain. That house needs a tap.

For every such chain, we must report three values:

1. the starting house containing the tank,
2. the ending house containing the tap,
3. the minimum pipe diameter along the path.

The minimum diameter matters because water can only flow as much as the narrowest pipe allows.

For example, if we have:

```
1 -> 2 (10)
2 -> 3 (20)
3 -> 4 (5)
```

then the answer is:

```
1 4 5
```

because the bottleneck pipe has diameter 5.

The constraints are small, only up to 1000 houses and 1000 pipes. Even an $O(n^2)$ solution would pass comfortably. Still, the graph structure allows a clean linear solution.

The most dangerous mistakes come from misunderstanding the chain structure.

One common bug is starting DFS from every node instead of only true sources.

Consider:

```
4 3
1 2 5
2 3 4
3 4 3
```

The correct output is:

```
1
1 4 3
```

A careless implementation might also generate:

```
2 4 3
3 4 3
```

because it starts traversals from internal nodes.

Another subtle case is isolated houses.

```
3 0
```

No house has pipes, so there are no tank-tap pairs at all:

```
0
```

A naive solution may accidentally treat isolated nodes as both tanks and taps.

A third edge case is multiple disconnected chains.

```
6 4
1 2 8
2 3 6
4 5 10
5 6 7
```

The answer must contain both independent systems:

```
2
1 3 6
4 6 7
```

The output order matters. Results must be sorted by tank house index, which naturally happens if we scan houses from 1 to $n$.

## Approaches

The brute-force idea is straightforward. For every house, try following outgoing pipes until the chain ends. While walking, keep track of the minimum diameter seen.

This works because each node has at most one outgoing edge, so traversal is simple and never branches.

The problem appears when we repeat the same work many times. In a chain of length $n$:

```
1 -> 2 -> 3 -> ... -> n
```

starting from every node causes repeated traversals.

From node 1 we walk $n$ steps.

From node 2 we walk $n-1$ steps.

From node 3 we walk $n-2$ steps.

The total becomes:

$$n + (n-1) + (n-2) + \dots + 1 = O(n^2)$$

With the given constraints this still passes, but it ignores the key structure of the graph.

The important observation is that every valid water system starts at a node with:

```
indegree = 0
outdegree = 1
```

Such a node is the unique beginning of a chain. If we start only from these nodes, every pipe is visited exactly once overall.

From each source node, we repeatedly move forward until we reach a node with no outgoing pipe. During traversal we maintain the minimum diameter.

Because every node has at most one outgoing edge, the traversal is deterministic. No branching, no revisits, no ambiguity.

This reduces the complexity to linear time.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n²) | O(1) | Accepted |
| Optimal | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Create arrays to store outgoing connections, incoming connections, and pipe diameters.

Since every node has at most one outgoing pipe, we only need one destination per node instead of an adjacency list.
2. Read every pipe `(a, b, d)`.

Store:

- `to[a] = b`
- `diameter[a] = d`
- `indegree[b] += 1`

This gives direct access to the next node in the chain.
3. Scan all houses from `1` to `n`.

A house is the start of a valid system if:

- it has an outgoing pipe,
- it has no incoming pipe.

These are exactly the tank houses.
4. For each tank house, follow the chain until no outgoing pipe exists.

While traversing:

- update the minimum diameter,
- move to the next node.
5. The last reached node is the tap house.

Store:

- tank,
- tap,
- minimum diameter.
6. Print all stored results.

Since houses were scanned in increasing order, the output order is already correct.

### Why it works

Every connected component in this graph is a simple directed chain because each node has at most one incoming and one outgoing edge.

A valid water system must begin at the unique node with no incoming edge and end at the unique node with no outgoing edge.

Starting traversal only from source nodes guarantees that:

- every chain is processed exactly once,
- no internal node incorrectly becomes a separate tank,
- the minimum diameter collected during traversal is exactly the bottleneck capacity of that chain.

Since traversal follows the only possible path in the component, the algorithm cannot miss or duplicate any valid answer.

## Python Solution

```python
import sys
input = sys.stdin.readline

n, p = map(int, input().split())

to = [0] * (n + 1)
diameter = [0] * (n + 1)
indegree = [0] * (n + 1)

for _ in range(p):
    a, b, d = map(int, input().split())
    to[a] = b
    diameter[a] = d
    indegree[b] += 1

answer = []

for i in range(1, n + 1):
    if indegree[i] == 0 and to[i] != 0:
        current = i
        minimum_diameter = float('inf')

        while to[current] != 0:
            minimum_diameter = min(minimum_diameter, diameter[current])
            current = to[current]

        answer.append((i, current, minimum_diameter))

print(len(answer))

for tank, tap, d in answer:
    print(tank, tap, d)
```

The arrays are the core simplification. Because every node has at most one outgoing edge, `to[u]` uniquely identifies the next house in the chain. We do not need adjacency lists or DFS recursion.

The `indegree` array identifies which nodes are true sources. Only those nodes may contain tanks.

The traversal loop walks through a chain one node at a time. The variable `minimum_diameter` tracks the bottleneck pipe encountered so far. Since the path is linear, this single running minimum is sufficient.

Using `float('inf')` as the initial value avoids special-case handling for the first edge.

One easy mistake is updating the minimum after moving to the next node. The pipe diameter belongs to the current node's outgoing edge, so the minimum must be updated before advancing.

Another subtle point is stopping correctly. The last node in the chain has `to[current] == 0`, meaning it has no outgoing pipe and is the tap house.

## Worked Examples

### Example 1

Input:

```
3 2
1 2 10
2 3 20
```

Traversal state:

| Current Node | Next Node | Current Minimum |
| --- | --- | --- |
| 1 | 2 | 10 |
| 2 | 3 | 10 |

Final result:

```
1 3 10
```

The chain starts at house 1 because it has no incoming pipe. The minimum diameter along the path is `min(10, 20) = 10`.

### Example 2

Input:

```
6 4
1 2 8
2 3 6
4 5 10
5 6 7
```

First chain traversal:

| Current Node | Next Node | Current Minimum |
| --- | --- | --- |
| 1 | 2 | 8 |
| 2 | 3 | 6 |

Second chain traversal:

| Current Node | Next Node | Current Minimum |
| --- | --- | --- |
| 4 | 5 | 10 |
| 5 | 6 | 7 |

Final output:

```
2
1 3 6
4 6 7
```

This example shows that disconnected chains are processed independently. Each chain has its own tank, tap, and bottleneck diameter.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Every node and pipe is processed at most once |
| Space | O(n) | Arrays for outgoing edges, diameters, and indegrees |

With at most 1000 houses and pipes, the solution easily fits within the limits. Even quadratic solutions would pass, but the linear traversal fully exploits the graph structure.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def solve():
    input = sys.stdin.readline

    n, p = map(int, input().split())

    to = [0] * (n + 1)
    diameter = [0] * (n + 1)
    indegree = [0] * (n + 1)

    for _ in range(p):
        a, b, d = map(int, input().split())
        to[a] = b
        diameter[a] = d
        indegree[b] += 1

    answer = []

    for i in range(1, n + 1):
        if indegree[i] == 0 and to[i] != 0:
            current = i
            minimum_diameter = float('inf')

            while to[current] != 0:
                minimum_diameter = min(minimum_diameter, diameter[current])
                current = to[current]

            answer.append((i, current, minimum_diameter))

    output = [str(len(answer))]

    for a, b, d in answer:
        output.append(f"{a} {b} {d}")

    print("\n".join(output))

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    solve()

    return sys.stdout.getvalue()

# provided sample
assert run(
"""3 2
1 2 10
2 3 20
"""
) == """1
1 3 10
"""

# no pipes
assert run(
"""3 0
"""
) == """0
"""

# single pipe
assert run(
"""2 1
1 2 5
"""
) == """1
1 2 5
"""

# multiple disconnected chains
assert run(
"""6 4
1 2 8
2 3 6
4 5 10
5 6 7
"""
) == """2
1 3 6
4 6 7
"""

# equal diameters
assert run(
"""4 3
1 2 5
2 3 5
3 4 5
"""
) == """1
1 4 5
"""

# bottleneck in middle
assert run(
"""5 4
1 2 100
2 3 2
3 4 50
4 5 60
"""
) == """1
1 5 2
"""
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| No pipes | `0` | Isolated nodes are ignored |
| Single pipe | `1 2 5` | Simplest valid chain |
| Multiple disconnected chains | Two outputs | Independent components |
| Equal diameters | Minimum remains unchanged | Stable bottleneck tracking |
| Bottleneck in middle | Minimum becomes internal edge | Correct minimum propagation |

## Edge Cases

### Internal Nodes Incorrectly Treated as Tanks

Input:

```
4 3
1 2 5
2 3 4
3 4 3
```

The algorithm computes indegrees:

| Node | Indegree |
| --- | --- |
| 1 | 0 |
| 2 | 1 |
| 3 | 1 |
| 4 | 1 |

Only node 1 qualifies as a tank because it alone has no incoming edge.

Traversal:

```
1 -> 2 -> 3 -> 4
```

Minimum diameter becomes:

```
min(5, 4, 3) = 3
```

Output:

```
1
1 4 3
```

Internal nodes are skipped automatically because their indegree is not zero.

### Isolated Houses

Input:

```
3 0
```

Every node has:

```
indegree = 0
outdegree = 0
```

The condition for starting traversal is:

```
indegree[i] == 0 and to[i] != 0
```

Since no node has outgoing pipes, no traversal starts.

Output:

```
0
```

This prevents isolated houses from being incorrectly reported as tank-tap pairs.

### Multiple Independent Systems

Input:

```
6 4
1 2 8
2 3 6
4 5 10
5 6 7
```

The algorithm finds two source nodes:

```
1 and 4
```

First traversal:

```
1 -> 2 -> 3
minimum = 6
```

Second traversal:

```
4 -> 5 -> 6
minimum = 7
```

Output:

```
2
1 3 6
4 6 7
```

Each connected component is processed independently, and no edges are revisited.
