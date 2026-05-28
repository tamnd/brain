---
title: "CF 41E - 3-cycles"
description: "We need to build an undirected graph on n cities such that no triangle exists. A triangle means three distinct cities where every pair is directly connected."
date: "2026-05-28T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "constructive-algorithms", "graphs", "greedy"]
categories: ["algorithms"]
codeforces_contest: 41
codeforces_index: "E"
codeforces_contest_name: "Codeforces Beta Round 40 (Div. 2)"
rating: 1900
weight: 41
solve_time_s: 108
verified: false
draft: false
---
[CF 41E - 3-cycles](https://codeforces.com/problemset/problem/41/E)

**Rating:** 1900  
**Tags:** constructive algorithms, graphs, greedy  
**Solve time:** 1m 48s  
**Verified:** no  

## Solution
## Problem Understanding

We need to build an undirected graph on `n` cities such that no triangle exists. A triangle means three distinct cities where every pair is directly connected. Among all graphs with no 3-cycles, we want the one with the maximum possible number of roads, and we must also print one valid construction.

The input contains only the number of cities. The output must first print the maximum number of roads, then list every road.

The bound `n ≤ 100` is small enough that almost any polynomial-time construction works comfortably. Even an `O(n^3)` verification step would be fine because `100^3 = 1,000,000` operations. The real challenge is not performance, it is discovering the extremal graph structure that maximizes the number of edges while avoiding triangles.

A common mistake is trying to greedily add edges while checking whether a triangle appears. That approach can get stuck in locally optimal configurations that are not globally optimal.

For example, suppose `n = 4`.

A careless greedy construction might build:

```
1-2
2-3
3-4
```

This graph has only 3 edges. But the optimal answer is 4 edges:

```
1-3
1-4
2-3
2-4
```

This is a complete bipartite graph with partitions `{1,2}` and `{3,4}`.

Another subtle case is odd `n`.

For `n = 5`, splitting into equal halves is impossible. If we choose partitions of sizes `2` and `3`, the number of edges becomes `2 × 3 = 6`.

A buggy implementation might incorrectly try partitions `1` and `4`, producing only 4 edges. The optimal partition sizes must be as balanced as possible.

The smallest cases also matter.

For `n = 1`, the graph has no edges.

For `n = 2`, exactly one edge is possible.

A construction that blindly connects all pairs across two partitions must still handle empty partitions correctly.

## Approaches

The brute-force idea is straightforward. Consider every possible subset of edges among the `n(n-1)/2` candidate edges, test whether the graph contains a triangle, and keep the largest valid graph.

This works because the definition is explicit: we only need to reject graphs containing any 3-cycle. Triangle detection itself can be done in `O(n^3)` by checking every triple of vertices.

The problem is the number of graphs. There are `2^(n(n-1)/2)` possible undirected graphs. Even for `n = 20`, this becomes astronomically large. Exhaustive search is completely impossible.

A more reasonable greedy idea is adding edges one by one while avoiding triangles. That still does not guarantee optimality because local decisions can block future edges.

The key observation is a classical extremal graph result: the triangle-free graph with the maximum number of edges is always a complete bipartite graph with the two parts as balanced as possible.

Why does bipartite matter here? Any triangle requires three vertices where every pair is connected. In a bipartite graph, vertices are divided into two groups, and edges only go across groups. A triangle would need two vertices from the same group, but same-group edges do not exist. So bipartite graphs are automatically triangle-free.

Among bipartite graphs, if one partition has size `a` and the other has size `b`, then every cross-pair can be connected, giving `a × b` edges.

Since `a + b = n`, the product `a × b` is maximized when the two values are as close as possible. So the optimal partition sizes are:

```
⌊n/2⌋ and ⌈n/2⌉
```

Then we simply connect every vertex from the first part to every vertex from the second part.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(2^(n²) · n³) | O(n²) | Too slow |
| Optimal | O(n²) | O(1) excluding output | Accepted |

## Algorithm Walkthrough

1. Read the value `n`.
2. Split the vertices into two groups as evenly as possible.

Let:

```
left = n // 2
right = n - left
```

The first group will contain vertices `1...left`, and the second group will contain vertices `left+1...n`.
3. Create an empty list of edges.
4. For every vertex `i` in the first group, connect it to every vertex `j` in the second group.

This creates a complete bipartite graph.
5. Print the number of edges.
6. Print every stored edge.

### Why it works

The graph is bipartite, so no edge exists between vertices inside the same partition. Any triangle would require at least one such edge, which is impossible. So the construction is always triangle-free.

Now consider the edge count. If the partition sizes are `a` and `b`, the graph contains `a × b` edges. Since `a + b = n`, this product is maximized when the two numbers are as balanced as possible. Our construction uses exactly those partition sizes, so no triangle-free graph can contain more edges.

## Python Solution

```python
import sys
input = sys.stdin.readline

n = int(input())

left = n // 2

edges = []

for i in range(1, left + 1):
    for j in range(left + 1, n + 1):
        edges.append((i, j))

print(len(edges))

for u, v in edges:
    print(u, v)
```

The code directly implements the constructive proof.

The variable `left` stores the size of the first partition. The second partition automatically contains the remaining vertices.

The nested loops generate every cross-edge between the two partitions. Since each pair is added exactly once, duplicate edges cannot appear.

The vertex ranges are carefully chosen to avoid off-by-one mistakes. The first partition is:

```
1 ... left
```

The second partition is:

```
left + 1 ... n
```

This works correctly for both even and odd `n`.

For example, when `n = 5`:

```
left = 2
first group  = {1, 2}
second group = {3, 4, 5}
```

All six cross-edges are added.

The memory usage is tiny because at most `2500` edges exist when `n = 100`.

## Worked Examples

### Example 1

Input:

```
3
```

The partitions become:

```
{1}
{2, 3}
```

| Step | Current i | Current j | Added Edge | Total Edges |
| --- | --- | --- | --- | --- |
| Start | - | - | - | 0 |
| 1 | 1 | 2 | (1,2) | 1 |
| 2 | 1 | 3 | (1,3) | 2 |

Final output:

```
2
1 2
1 3
```

This trace shows that every edge goes across the partition boundary. Since vertices `2` and `3` are not connected, no triangle exists.

### Example 2

Input:

```
5
```

The partitions become:

```
{1, 2}
{3, 4, 5}
```

| Step | Current i | Current j | Added Edge | Total Edges |
| --- | --- | --- | --- | --- |
| Start | - | - | - | 0 |
| 1 | 1 | 3 | (1,3) | 1 |
| 2 | 1 | 4 | (1,4) | 2 |
| 3 | 1 | 5 | (1,5) | 3 |
| 4 | 2 | 3 | (2,3) | 4 |
| 5 | 2 | 4 | (2,4) | 5 |
| 6 | 2 | 5 | (2,5) | 6 |

Final output:

```
6
1 3
1 4
1 5
2 3
2 4
2 5
```

This example demonstrates why balanced partitions matter. A `2 × 3` split gives 6 edges, which is larger than any unbalanced alternative.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n²) | Every cross-pair between the two partitions is processed once |
| Space | O(n²) | The edge list may contain up to about n²/4 edges |

With `n ≤ 100`, the maximum number of generated edges is only `2500`. The solution easily fits within both the time and memory limits.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def solve():
    input = sys.stdin.readline

    n = int(input())

    left = n // 2

    edges = []

    for i in range(1, left + 1):
        for j in range(left + 1, n + 1):
            edges.append((i, j))

    print(len(edges))

    for u, v in edges:
        print(u, v)

def run(inp: str) -> str:
    backup_stdin = sys.stdin
    backup_stdout = sys.stdout

    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    solve()

    out = sys.stdout.getvalue()

    sys.stdin = backup_stdin
    sys.stdout = backup_stdout

    return out

# provided sample
assert run("3\n") == (
    "2\n"
    "1 2\n"
    "1 3\n"
), "sample 1"

# minimum size
assert run("1\n") == "0\n", "single vertex"

# two vertices
assert run("2\n") == (
    "1\n"
    "1 2\n"
), "single edge"

# odd n
assert run("5\n") == (
    "6\n"
    "1 3\n"
    "1 4\n"
    "1 5\n"
    "2 3\n"
    "2 4\n"
    "2 5\n"
), "balanced odd partition"

# even n
assert run("4\n") == (
    "4\n"
    "1 3\n"
    "1 4\n"
    "2 3\n"
    "2 4\n"
), "balanced even partition"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1` | `0` edges | Handles empty graph correctly |
| `2` | One edge | Smallest non-trivial graph |
| `4` | 4 edges | Correct balanced bipartite construction for even n |
| `5` | 6 edges | Correct balanced bipartite construction for odd n |

## Edge Cases

Consider the smallest possible input:

```
1
```

The algorithm computes:

```
left = 0
```

So the first partition is empty and the second partition contains vertex `1`. The nested loops never execute, producing zero edges:

```
0
```

This is correct because no roads can exist.

Now consider:

```
2
```

The partitions become:

```
{1}
{2}
```

The algorithm adds exactly one edge:

```
1 2
```

No triangle can exist with only two vertices.

The odd-size case is more subtle:

```
5
```

The partitions become sizes `2` and `3`. The algorithm generates `2 × 3 = 6` edges.

A buggy implementation using partitions `1` and `4` would only produce 4 edges:

```
1-2
1-3
1-4
1-5
```

That graph is triangle-free but not maximal. The balanced split is necessary to maximize the product.

Finally, consider:

```
6
```

The partitions are perfectly balanced:

```
{1,2,3}
{4,5,6}
```

The graph contains `3 × 3 = 9` edges. Any attempt to add an edge inside either partition immediately creates a triangle.

For example, adding edge `(1,2)` creates:

```
1-2-4-1
```

because both `1` and `2` are already connected to `4`. This confirms why the complete bipartite structure is maximal.
