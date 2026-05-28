---
title: "CF 29C - Mail Stamps"
description: "Each stamp describes a direct transfer between two cities. If the envelope contains n stamps, then the letter passed thr"
date: "2026-05-28T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "data-structures", "dfs-and-similar", "graphs", "implementation"]
categories: ["algorithms"]
codeforces_contest: 29
codeforces_index: "C"
codeforces_contest_name: "Codeforces Beta Round 29 (Div. 2, Codeforces format)"
rating: 1700
weight: 29
solve_time_s: 97
verified: false
draft: false
---

[CF 29C - Mail Stamps](https://codeforces.com/problemset/problem/29/C)

**Rating:** 1700  
**Tags:** data structures, dfs and similar, graphs, implementation  
**Solve time:** 1m 37s  
**Verified:** no  

## Solution
## Problem Understanding

Each stamp describes a direct transfer between two cities. If the envelope contains `n` stamps, then the letter passed through exactly `n + 1` cities in sequence. The route never revisits a city, so the entire journey forms a simple path.

The stamps are unordered. We only know which pairs of cities were consecutive during delivery. Our task is to reconstruct one valid ordering of all cities in the route.

This is naturally a graph problem. Every city is a vertex, every stamp is an undirected edge, and the final graph is guaranteed to be a simple path. A path with `n` edges always has exactly two vertices of degree `1`, the endpoints, while every internal vertex has degree `2`.

The constraints are large enough that brute-force permutation checking is impossible. With `n` up to `10^5`, the solution must stay close to linear time. Any approach that repeatedly scans the graph or tries multiple candidate routes would quickly become too slow. An `O(n)` or `O(n log n)` solution is completely safe.

There are a few easy mistakes that silently break the reconstruction.

One common bug is starting traversal from an arbitrary node instead of an endpoint. Consider:

```
3
1 2
2 3
3 4
```

If we start from `2`, we can move to `1` and get stuck, missing half the route. The correct traversal must start from a degree `1` node, either `1` or `4`.

Another subtle issue is assuming city labels are small integers. The problem allows values up to `10^9`.

```
2
1000000000 7
7 42
```

Using an array indexed by city number would waste huge amounts of memory or crash entirely. A hash map is required.

A third mistake is forgetting that the graph is undirected. For example:

```
2
1 100
100 2
```

The valid routes are:

```
1 100 2
2 100 1
```

Treating stamps as directed edges would incorrectly reject one of these answers.

## Approaches

The brute-force idea is straightforward. We could try every possible ordering of the cities and check whether consecutive pairs correspond to stamps. Since there are `n + 1` cities, this requires checking `(n + 1)!` permutations.

Even for `n = 15`, this becomes enormous. For `n = 10^5`, it is completely impossible.

A slightly better brute-force would build the route incrementally. Pick a starting city, repeatedly choose an unused adjacent edge, and backtrack whenever the path becomes invalid. This works because the graph is guaranteed to be a path, but without exploiting that structure directly, the algorithm still wastes time exploring unnecessary states.

The key observation is that the input graph is already a simple path. Every internal city connects to exactly two neighbors, and only the two endpoints connect to one neighbor each.

Once we identify one endpoint, the reconstruction becomes trivial. From the current city, there is at most one unvisited neighbor we can move to next. The route is forced.

This turns the problem into a simple graph traversal on a path graph.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O((n+1)!) | O(n) | Too slow |
| Optimal | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Build an adjacency list for the graph.

For every stamp `(u, v)`, add `v` to the neighbor list of `u`, and add `u` to the neighbor list of `v`.
2. Find one endpoint of the path.

In a simple path, endpoints are exactly the vertices with degree `1`. We scan all cities and choose any city whose adjacency list has size `1`.
3. Start traversing from that endpoint.

Add the starting city to the answer.
4. Repeatedly move to the next unvisited neighbor.

Since the graph is a path, every internal node has exactly two neighbors. One is the previous city we came from, and the other is the next city in the route.
5. Keep track of the previous city.

At each step, inspect the neighbors of the current city. Move to the neighbor that is different from the previous city.
6. Stop when no further move exists.

This happens at the other endpoint, where the only neighbor is the previous city.

### Why it works

The graph formed by the stamps is guaranteed to be a simple path. A simple path has exactly two endpoints and no cycles.

Starting from an endpoint guarantees that every step forward is uniquely determined. At any internal vertex, one adjacent city is the city we came from, while the other is the next city in the route. Since no city repeats, choosing the unused neighbor always follows the original path.

The traversal visits every edge exactly once and every vertex exactly once, so the produced sequence is a valid route containing all stamps.

## Python Solution

```python
import sys
input = sys.stdin.readline

from collections import defaultdict

def solve():
    n = int(input())

    graph = defaultdict(list)

    for _ in range(n):
        u, v = map(int, input().split())
        graph[u].append(v)
        graph[v].append(u)

    start = -1

    for node in graph:
        if len(graph[node]) == 1:
            start = node
            break

    ans = []

    prev = None
    curr = start

    while True:
        ans.append(curr)

        next_node = None

        for nei in graph[curr]:
            if nei != prev:
                next_node = nei
                break

        if next_node is None:
            break

        prev, curr = curr, next_node

    print(*ans)

solve()
```

The adjacency list stores all neighboring cities for each city. A `defaultdict(list)` is ideal because city labels can be as large as `10^9`, so we cannot index arrays directly by city number.

The scan for the starting node relies on the defining property of a path graph: endpoints have degree `1`. Either endpoint is acceptable because the reverse route is also valid.

The traversal uses two variables, `prev` and `curr`. This avoids needing a visited set. Since every node has degree at most `2`, excluding the previous city immediately identifies the correct next city.

The stopping condition is subtle. At the final endpoint, every neighbor equals `prev`, so no valid `next_node` exists. At that moment the route is complete.

A common implementation bug is updating `prev` and `curr` in the wrong order. The simultaneous assignment:

```
prev, curr = curr, next_node
```

keeps both values correct.

## Worked Examples

### Example 1

Input:

```
2
1 100
100 2
```

Adjacency lists:

```
1 -> [100]
100 -> [1, 2]
2 -> [100]
```

The endpoints are `1` and `2`. Suppose we start from `1`.

| Step | prev | curr | next_node | ans |
| --- | --- | --- | --- | --- |
| 1 | None | 1 | 100 | [1] |
| 2 | 1 | 100 | 2 | [1, 100] |
| 3 | 100 | 2 | None | [1, 100, 2] |

Output:

```
1 100 2
```

This trace shows why the traversal becomes deterministic after choosing an endpoint.

### Example 2

Input:

```
4
10 20
30 40
20 30
40 50
```

Adjacency lists:

```
10 -> [20]
20 -> [10, 30]
30 -> [40, 20]
40 -> [30, 50]
50 -> [40]
```

Endpoints are `10` and `50`.

| Step | prev | curr | next_node | ans |
| --- | --- | --- | --- | --- |
| 1 | None | 10 | 20 | [10] |
| 2 | 10 | 20 | 30 | [10, 20] |
| 3 | 20 | 30 | 40 | [10, 20, 30] |
| 4 | 30 | 40 | 50 | [10, 20, 30, 40] |
| 5 | 40 | 50 | None | [10, 20, 30, 40, 50] |

Output:

```
10 20 30 40 50
```

This example demonstrates that the stamps may arrive in arbitrary order, but the graph structure still uniquely determines the path.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Each edge and vertex is processed a constant number of times |
| Space | O(n) | The adjacency list stores all edges |

The graph contains exactly `n` edges and `n + 1` vertices. Every operation in the algorithm is linear in the graph size, which easily fits within the limits for `n = 10^5`.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys, io
from collections import defaultdict

def solve():
    input = sys.stdin.readline

    n = int(input())

    graph = defaultdict(list)

    for _ in range(n):
        u, v = map(int, input().split())
        graph[u].append(v)
        graph[v].append(u)

    start = -1

    for node in graph:
        if len(graph[node]) == 1:
            start = node
            break

    ans = []

    prev = None
    curr = start

    while True:
        ans.append(curr)

        nxt = None

        for nei in graph[curr]:
            if nei != prev:
                nxt = nei
                break

        if nxt is None:
            break

        prev, curr = curr, nxt

    print(*ans)

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    solve()

    return sys.stdout.getvalue().strip()

# provided sample
out = run("2\n1 100\n100 2\n")
assert out in ["1 100 2", "2 100 1"], "sample 1"

# minimum size
out = run("1\n5 9\n")
assert out in ["5 9", "9 5"], "minimum case"

# long chain
out = run("4\n10 20\n30 40\n20 30\n40 50\n")
assert out in ["10 20 30 40 50", "50 40 30 20 10"], "unordered edges"

# large labels
out = run("2\n1000000000 7\n7 42\n")
assert out in [
    "1000000000 7 42",
    "42 7 1000000000"
], "large city ids"

# negative traversal direction
out = run("3\n1 2\n2 3\n3 4\n")
assert out in [
    "1 2 3 4",
    "4 3 2 1"
], "path traversal"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 / 5 9` | `5 9` or `9 5` | Smallest valid graph |
| Unordered chain | Full ordered route | Reconstruction independent of input order |
| Large city labels | Correct path | Hash map handling for sparse values |
| Straight 4-node path | Either direction | Endpoint-based traversal |

## Edge Cases

Consider the case where the traversal starts in the middle instead of at an endpoint.

Input:

```
3
1 2
2 3
3 4
```

The graph is:

```
1 - 2 - 3 - 4
```

Our algorithm first scans degrees and finds either `1` or `4`. Suppose it picks `1`.

Traversal:

```
1 -> 2 -> 3 -> 4
```

At each internal node, the previous city is excluded, leaving exactly one valid next city. The algorithm never gets stuck early.

Now consider very large city identifiers.

Input:

```
2
1000000000 7
7 42
```

The adjacency structure becomes:

```
1000000000 -> [7]
7 -> [1000000000, 42]
42 -> [7]
```

Because the implementation uses dictionaries instead of indexed arrays, the city values themselves do not affect memory usage.

Finally, consider the smallest possible valid path.

Input:

```
1
8 9
```

Both cities have degree `1`. Starting from either endpoint immediately produces:

```
8 9
```

or

```
9 8
```

The traversal stops correctly after one edge because the second city has no unused neighbor left.
