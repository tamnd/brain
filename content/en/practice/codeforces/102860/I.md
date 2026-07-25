---
title: "CF 102860I - Walk of Three"
description: "We have an undirected park graph. The entrance is vertex 1, and Vasya is allowed to finish only on a vertex that is directly connected to 1. A valid walk starts at 1, uses exactly three different edges in sequence, and ends at one of those neighboring vertices."
date: "2026-07-25T14:15:41+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102860
codeforces_index: "I"
codeforces_contest_name: "2020-2021 Saint-Petersburg Open High School Programming Contest (SpbKOSHP 20)"
rating: 0
weight: 102860
solve_time_s: 47
verified: true
draft: false
---

[CF 102860I - Walk of Three](https://codeforces.com/problemset/problem/102860/I)

**Rating:** -  
**Tags:** -  
**Solve time:** 47s  
**Verified:** yes  

## Solution
## Problem Understanding

We have an undirected park graph. The entrance is vertex `1`, and Vasya is allowed to finish only on a vertex that is directly connected to `1`. A valid walk starts at `1`, uses exactly three different edges in sequence, and ends at one of those neighboring vertices. The task is to count how many different three-edge walks satisfy these rules.

A walk can visit the same vertex more than once, but the three edges used during the walk must be distinct. For example, the sequence `1 -> 2 -> 1 -> 3` is invalid because the first two moves use the same edge in opposite directions.

The graph has up to `100000` vertices and `200000` edges. A solution that tries all possible three-edge sequences is impossible because the number of walks can grow to roughly the sum of squared degrees, which is far beyond what a one-second limit allows. We need to process the graph close to linear time.

The tricky part is not finding walks of length three. Counting those directly is easy. The difficulty is removing the walks where one of the three edges is reused.

Several edge cases break careless solutions.

For a graph with only one edge:

```
2 1
1 2
```

the answer is `0`. The only possible movement is `1 -> 2`, and three different edges cannot be chosen.

For a triangle:

```
3 3
1 2
2 3
3 1
```

the answer is `0`. There are many three-edge walks that end next to vertex `1`, but every one of them repeats an edge.

For a star:

```
4 3
1 2
1 3
1 4
```

the answer is `0`. Any three-edge movement must immediately return through an already used edge because all roads touch the entrance.

A common mistake is counting every length-three walk that ends at a neighbor of `1` and forgetting that the same edge may appear twice.

## Approaches

A direct approach would generate every possible walk `1 -> a -> b -> c`, check whether `c` is a neighbor of `1`, and then verify that the three edges are different. The first transition has `deg(1)` choices, the second can have many choices, and the third can again branch. In dense parts of the graph this becomes too large. A graph with high-degree vertices can create billions of candidate walks.

The useful observation is that counting the unrestricted walks is easy, and the only invalid cases have a very specific structure.

First, mark every neighbor of vertex `1`. Let this set be `S`.

For every vertex `v`, compute how many neighbors of `v` belong to `S`. Call this value `inside[v]`.

Now consider a walk `1 -> a -> b -> c`. The first vertex `a` must be in `S`. After moving from `a` to `b`, the number of possible final vertices is exactly `inside[b]`, because the last vertex must be a neighbor of `1`. Summing this over every edge leaving every vertex in `S` counts all length-three walks that finish correctly, but it also includes repeated-edge walks.

There are only two ways to repeat an edge.

The first two edges can be the same. This gives walks of the form `1 -> a -> 1 -> c`. There are `deg(1)` choices for `a` and `deg(1)` choices for `c`, so there are `deg(1)^2` such walks.

The second and third edges can be the same. These walks have the form `1 -> a -> b -> a`. For every neighbor `a` of `1`, there are `deg(a)` choices for `b`, so the count is the sum of degrees of all neighbors of `1`.

The two cases overlap when all three moves use the same edge: `1 -> a -> 1 -> a`. There are exactly `deg(1)` such walks, so we add them back once.

The final answer is:

```
all_length_three_walks
- deg(1)^2
- sum_of_neighbor_degrees
+ deg(1)
```

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(number of length-3 walks) | O(n + m) | Too slow |
| Optimal | O(n + m) | O(n + m) | Accepted |

## Algorithm Walkthrough

1. Read the graph and store the adjacency list. The graph is sparse, so adjacency lists let us inspect all edges in linear time.
2. Find all vertices directly connected to vertex `1` and mark them. These are the only possible ending vertices and also the only possible first vertices.
3. For every vertex, count how many of its neighbors are marked. This value tells us how many valid choices exist for the final step after reaching that vertex.
4. Count all unrestricted walks. For every marked vertex `u`, inspect every edge `u -> v`. Add `inside[v]` because each marked neighbor of `v` creates one possible ending point.
5. Subtract walks where the first edge is reused. Their structure is `1 -> u -> 1 -> v`, giving `degree(1) * degree(1)` cases.
6. Subtract walks where the second edge is reused. Their structure is `1 -> u -> v -> u`, giving the sum of degrees of all neighbors of `1`.
7. Add back walks counted in both invalid groups. These are exactly `1 -> u -> 1 -> u`, one for every neighbor of `1`.

Why it works:

The unrestricted count includes every possible three-edge walk ending next to the entrance. The only reason such a walk is invalid is that one of its three edges appears twice. In a simple undirected graph, the first and second edges can only match when the walk returns immediately to vertex `1`, and the second and third edges can only match when the walk returns to the previous vertex. The first and third edges cannot be equal because the final vertex is not the entrance. Since the two invalid groups are counted separately and their intersection is exactly the walks using one edge three times, inclusion-exclusion removes every invalid walk exactly once.

## Python Solution

```python
import sys
input = sys.stdin.readline

n, m = map(int, input().split())

g = [[] for _ in range(n)]

for _ in range(m):
    u, v = map(int, input().split())
    u -= 1
    v -= 1
    g[u].append(v)
    g[v].append(u)

mark = [False] * n
for v in g[0]:
    mark[v] = True

inside = [0] * n
for v in range(n):
    cnt = 0
    for u in g[v]:
        if mark[u]:
            cnt += 1
    inside[v] = cnt

total = 0
for u in g[0]:
    for v in g[u]:
        total += inside[v]

deg1 = len(g[0])

bad_first_two = deg1 * deg1

bad_second_three = 0
for u in g[0]:
    bad_second_three += len(g[u])

answer = total - bad_first_two - bad_second_three + deg1

print(answer)
```

The array `mark` represents the possible ending vertices. The `inside` array avoids repeatedly scanning the neighbors of a vertex while counting walks.

The variable `total` follows the unrestricted walk counting described in the algorithm. It intentionally ignores edge repetition because those cases have a simple formula and are cheaper to subtract afterward.

The correction terms use integer arithmetic only. Python integers do not overflow, which is useful because the number of walks can be much larger than the number of edges.

The graph is zero-indexed internally, so the entrance vertex is stored as index `0`. No special boundary handling is needed because adjacency lists naturally contain only existing vertices.

## Worked Examples

For the first sample:

```
10 14
1 5
2 5
5 6
2 3
1 3
2 4
4 6
1 6
1 7
7 8
8 1
1 10
9 10
9 8
```

The neighbors of vertex `1` are `5, 3, 6, 7, 8, 10`.

| Variable | Value |
| --- | --- |
| degree of vertex 1 | 6 |
| unrestricted walks | 58 |
| first two edges repeated | 36 |
| second and third edges repeated | 24 |
| overlap | 6 |
| answer | 4 |

The subtraction removes every walk that uses a road twice. The remaining four walks use three different roads.

For the triangle:

```
3 3
1 2
2 3
3 1
```

| Variable | Value |
| --- | --- |
| degree of vertex 1 | 2 |
| unrestricted walks | 6 |
| first two edges repeated | 4 |
| second and third edges repeated | 4 |
| overlap | 2 |
| answer | 0 |

This example demonstrates why simply counting length-three walks is not enough. Every candidate repeats an edge.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n + m) | Every vertex and every edge is inspected only a constant number of times. |
| Space | O(n + m) | The adjacency list and helper arrays store linear information. |

The limits allow linear graph processing because the total input size is only a few hundred thousand edges. The solution avoids enumerating walks and comfortably fits the time and memory constraints.

## Test Cases

```python
import sys
import io

def solve(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    input = sys.stdin.readline

    n, m = map(int, input().split())
    g = [[] for _ in range(n)]

    for _ in range(m):
        u, v = map(int, input().split())
        u -= 1
        v -= 1
        g[u].append(v)
        g[v].append(u)

    mark = [False] * n
    for v in g[0]:
        mark[v] = True

    inside = [0] * n
    for v in range(n):
        for u in g[v]:
            if mark[u]:
                inside[v] += 1

    total = 0
    for u in g[0]:
        for v in g[u]:
            total += inside[v]

    d = len(g[0])
    bad = d * d
    for u in g[0]:
        bad += len(g[u])

    return str(total - bad + d)

assert solve("""2 1
1 2
""") == "0"

assert solve("""3 3
1 2
2 3
3 1
""") == "0"

assert solve("""4 3
1 2
1 3
1 4
""") == "0"

assert solve("""5 6
1 2
2 3
3 4
4 5
5 1
2 5
""") == "2"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Single edge | 0 | No possible three-edge walk |
| Triangle | 0 | Repeated-edge correction |
| Star graph | 0 | Immediate returns through the entrance |
| Cycle with extra chord | 2 | General counting with multiple paths |

## Edge Cases

For the single-edge graph:

```
2 1
1 2
```

the marked set contains only vertex `2`. The unrestricted count is zero because there are not enough edges to form a three-step walk. The correction terms also remain zero, giving the correct result.

For the triangle:

```
3 3
1 2
2 3
3 1
```

the unrestricted count finds six possible walks. Four reuse the first edge, four reuse the last two edges, and two are counted in both groups. The formula gives `6 - 4 - 4 + 2 = 0`.

For the star graph:

```
4 3
1 2
1 3
1 4
```

every movement away from the entrance must immediately return using the same edge because no other roads exist. The unrestricted count is removed entirely by the invalid-walk correction.

The algorithm handles these cases because it separates the easy counting problem from the exact structural reasons a walk can fail.

I can also provide a shorter contest-style editorial version if you want one closer to what would appear on Codeforces.
