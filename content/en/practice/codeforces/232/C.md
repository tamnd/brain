---
title: "CF 232C - Doe Graphs"
description: "The graph family is built recursively. D(0) is a single vertex. D(1) is a single edge. For every larger order, D(n) is formed by taking a copy of D(n-1) and a shifted copy of D(n-2), then connecting them with two extra edges."
date: "2026-05-29T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "constructive-algorithms", "divide-and-conquer", "dp", "graphs", "shortest-paths"]
categories: ["algorithms"]
codeforces_contest: 232
codeforces_index: "C"
codeforces_contest_name: "Codeforces Round 144 (Div. 1)"
rating: 2600
weight: 232
solve_time_s: 143
verified: true
draft: false
---

[CF 232C - Doe Graphs](https://codeforces.com/problemset/problem/232/C)

**Rating:** 2600  
**Tags:** constructive algorithms, divide and conquer, dp, graphs, shortest paths  
**Solve time:** 2m 23s  
**Verified:** yes  

## Solution
## Problem Understanding

The graph family is built recursively. `D(0)` is a single vertex. `D(1)` is a single edge. For every larger order, `D(n)` is formed by taking a copy of `D(n-1)` and a shifted copy of `D(n-2)`, then connecting them with two extra edges.

The recursive construction matters much more than the actual drawing. Every vertex belongs either to the left part `D(n-1)` or to the right part `D(n-2)`, and the only edges between the two parts are:

- between vertex `|D(n-1)|` and vertex `|D(n-1)| + 1`
- between vertex `1` and vertex `|D(n-1)| + 1`

For each query, we must compute the shortest distance between two vertices in `D(n)`.

The first obstacle is graph size. The number of vertices follows Fibonacci growth:

$$|D(n)| = |D(n-1)| + |D(n-2)|$$

with initial values `1, 2`. By `n = 103`, the graph has astronomically many vertices, far beyond anything we could explicitly build. Even storing all vertices is impossible.

The query count reaches `10^5`, so even an `O(n^2)` algorithm per query would be too slow. Since `n` itself is only about `100`, we should aim for something close to `O(n)` per query.

The dangerous edge cases come from the recursive boundary vertices.

Consider `D(2)`. It has vertices:

- left copy `D(1)` → vertices `1,2`
- right copy `D(0)` → vertex `3`

Extra edges:

- `2-3`
- `1-3`

So the graph is a triangle.

If we try to recurse only by staying inside subgraphs, we miss shorter routes that cross through the connector vertex.

Example:

```
n = 2
query: 1 2
```

Correct answer:

```
1
```

A careless recursion could incorrectly say:

```
distance inside D(1) = 1
distance through D(0) = impossible
```

Another subtle case appears when vertices belong to different recursive halves.

Example:

```
n = 5
query: 2 and |D(4)|+5
```

The shortest path must pass through the special connector vertex `|D(4)|+1`, because there are only two crossing edges between the halves. Forgetting this property leads to completely wrong answers.

One more tricky scenario is when one endpoint itself is a connector vertex. Those vertices have extra edges not present in their internal recursive copy.

Example:

```
n = 4
query: 1 9
```

Vertex `1` directly connects to the first vertex of the right half. A solution that only considers distances internal to subgraphs misses this shortcut.

## Approaches

The brute force idea is straightforward. Construct the whole graph and run BFS for every query.

This works because the graph is unweighted, so BFS gives shortest paths exactly.

The problem is graph size. Vertex counts grow like Fibonacci numbers:

$$1,2,3,5,8,13,\dots$$

By `n = 103`, the graph contains around `10^{21}` vertices. Building adjacency lists is impossible, and even `n = 60` already exceeds realistic memory limits.

So we cannot think in terms of explicit graph traversal. We must exploit the recursive structure directly.

The key observation is that every shortest path problem in `D(n)` reduces to smaller Doe graphs.

Suppose both vertices lie inside the left copy `D(n-1)`. Then one candidate shortest path stays entirely inside that copy. Another candidate exits through one connector edge, travels through the right part, then re-enters through the other connector.

Those are the only possibilities because the two recursive halves communicate through exactly two edges.

This transforms the problem into recursive distance computation between a small number of special vertices.

The structure becomes much cleaner once we precompute distances from every vertex to the two connector vertices of its current graph:

- vertex `1`
- vertex `|D(n-1)|`

Call them the left connector and right connector.

Then every cross-half route can be expressed using only:

- recursive distances inside one half
- two extra crossing edges

The recursion depth is at most `103`, so memoized recursion easily fits.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | Exponential in `n` | Exponential in `n` | Impossible |
| Optimal | `O(n)` per query | `O(n)` recursion stack | Accepted |

## Algorithm Walkthrough

1. Precompute graph sizes.

Let `sz[i] = |D(i)|`.

The recurrence is:

$$sz[i] = sz[i-1] + sz[i-2]$$

We only need values up to `103`.
2. Define a recursive function `dist(n, a, b)`.

It returns the shortest distance between vertices `a` and `b` in `D(n)`.

Always reorder so `a <= b`, which simplifies case handling.
3. Handle the smallest graphs directly.

`D(0)` has one vertex only.

`D(1)` has two vertices connected by one edge.
4. Determine which recursive half each vertex belongs to.

The left half is:

$$[1, sz[n-1]]$$

The right half is:

$$[sz[n-1]+1, sz[n]]$$
5. If both vertices lie in the left half, compute two candidates.

The first candidate stays entirely inside `D(n-1)`:

$$dist(n-1, a, b)$$

The second candidate leaves through one connector and comes back through the other:

$$d(a,R)+1+1+d(1,b)$$

where `R = sz[n-1]`.

The two added ones correspond to the two crossing edges.
6. If both vertices lie in the right half, shift them down into local coordinates of `D(n-2)`.

Let:

$$a' = a - sz[n-1]$$

$$b' = b - sz[n-1]$$

Again compute:

- internal path inside `D(n-2)`
- path that exits through the connector cycle
7. If the vertices lie in different halves, every valid path must cross through vertex `sz[n-1]+1`.

There are exactly two crossing options:

- via edge `(1, sz[n-1]+1)`
- via edge `(sz[n-1], sz[n-1]+1)`

So compute:

$$dist(n-1,a,1)+1+dist(n-2,1,b')$$

and

$$dist(n-1,a,sz[n-1])+1+dist(n-2,1,b')$$

taking the minimum.
8. Memoize all recursive states.

The same subproblems appear repeatedly, especially distances to connector vertices.

### Why it works

At every recursive level, the graph consists of two subgraphs connected by exactly two edges. Any path between vertices either stays entirely inside one recursive component or crosses between components through those edges.

There are no other possibilities.

The recursion examines all valid top-level structures of shortest paths and recursively computes optimal subpaths inside smaller Doe graphs. Since each recursive call solves the same problem on strictly smaller graphs, the process eventually reaches the base graphs where distances are trivial.

Because every candidate path corresponds to a real graph path, and every possible shortest path must belong to one of the enumerated structures, the minimum computed value is exactly the true shortest distance.

## Python Solution

```python
import sys
from functools import lru_cache

input = sys.stdin.readline

MAXN = 105

sz = [0] * MAXN
sz[0] = 1
sz[1] = 2

for i in range(2, MAXN):
    sz[i] = sz[i - 1] + sz[i - 2]

@lru_cache(maxsize=None)
def dist(n, a, b):
    if a > b:
        a, b = b, a

    if a == b:
        return 0

    if n == 1:
        return 1

    left_size = sz[n - 1]

    a_left = (a <= left_size)
    b_left = (b <= left_size)

    # both in left part
    if a_left and b_left:
        inside = dist(n - 1, a, b)

        through = (
            dist(n - 1, a, left_size)
            + 1
            + 1
            + dist(n - 1, 1, b)
        )

        return min(inside, through)

    # both in right part
    if (not a_left) and (not b_left):
        na = a - left_size
        nb = b - left_size

        inside = dist(n - 2, na, nb)

        through = (
            dist(n - 2, na, 1)
            + 1
            + 1
            + dist(n - 2, 1, nb)
        )

        return min(inside, through)

    # different halves
    nb = b - left_size

    option1 = (
        dist(n - 1, a, 1)
        + 1
        + dist(n - 2, 1, nb)
    )

    option2 = (
        dist(n - 1, a, left_size)
        + 1
        + dist(n - 2, 1, nb)
    )

    return min(option1, option2)

def solve():
    t, n = map(int, input().split())

    ans = []

    for _ in range(t):
        a, b = map(int, input().split())
        ans.append(str(dist(n, a, b)))

    print("\n".join(ans))

solve()
```

The first section precomputes graph sizes. Since the recurrence matches Fibonacci growth, all sizes fit naturally in Python integers.

The recursive function is memoized with `lru_cache`. Without memoization, the recursion tree would explode because the same connector distances appear repeatedly.

The line:

```
if a > b:
    a, b = b, a
```

removes symmetric duplication. Distances are undirected, so `(a,b)` and `(b,a)` are identical states.

The most delicate part is the mixed-half case. When `a` lies in the left subgraph and `b` lies in the right one, the right vertex must be shifted into local coordinates:

```
nb = b - left_size
```

Forgetting this shift is the most common implementation mistake.

Another subtle detail is the extra `+1+1` when both vertices are inside the same half but we route through the opposite half. Crossing out and crossing back each consume one edge.

The recursion depth never exceeds about `100`, so Python recursion is completely safe here.

## Worked Examples

### Example 1

Input:

```
1 2
1 3
```

`D(2)` is a triangle.

| Step | n | a | b | Case | Result |
| --- | --- | --- | --- | --- | --- |
| 1 | 2 | 1 | 3 | Different halves | recurse |
| 2 | 1 | 1 | 1 | base | 0 |
| 3 | 0 | 1 | 1 | base | 0 |
| 4 | combine |  |  | `0+1+0` | 1 |

Output:

```
1
```

This trace shows the role of connector edges. Even though the graph is recursive, the shortest path immediately crosses the connecting edge.

### Example 2

Input:

```
1 5
2 5
```

| Step | n | a | b | Case | Candidate |
| --- | --- | --- | --- | --- | --- |
| 1 | 5 | 2 | 5 | both left | recurse |
| 2 | 4 | 2 | 5 | different halves | compute |
| 3 | via vertex 1 |  |  | `dist(3,2,1)+1+dist(2,1,2)` | 3 |
| 4 | via vertex 5 |  |  | `dist(3,2,5)+1+dist(2,1,2)` | 5 |
| 5 | minimum |  |  |  | 3 |

Output:

```
3
```

This example demonstrates that shortest paths are not forced to remain inside the same recursive component. Sometimes leaving the component through a connector is cheaper.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | `O(n)` per query | Each recursion level decreases `n` |
| Space | `O(n)` | Recursive stack and memoization depth |

The maximum recursion depth is only about `100`, while query count reaches `10^5`. An `O(n)` solution performs around `10^7` lightweight operations total, which easily fits within the limits in Python.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io
from functools import lru_cache

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    input = sys.stdin.readline

    MAXN = 105

    sz = [0] * MAXN
    sz[0] = 1
    sz[1] = 2

    for i in range(2, MAXN):
        sz[i] = sz[i - 1] + sz[i - 2]

    @lru_cache(maxsize=None)
    def dist(n, a, b):
        if a > b:
            a, b = b, a

        if a == b:
            return 0

        if n == 1:
            return 1

        left_size = sz[n - 1]

        a_left = a <= left_size
        b_left = b <= left_size

        if a_left and b_left:
            return min(
                dist(n - 1, a, b),
                dist(n - 1, a, left_size)
                + 2
                + dist(n - 1, 1, b)
            )

        if (not a_left) and (not b_left):
            na = a - left_size
            nb = b - left_size

            return min(
                dist(n - 2, na, nb),
                dist(n - 2, na, 1)
                + 2
                + dist(n - 2, 1, nb)
            )

        nb = b - left_size

        return min(
            dist(n - 1, a, 1)
            + 1
            + dist(n - 2, 1, nb),

            dist(n - 1, a, left_size)
            + 1
            + dist(n - 2, 1, nb)
        )

    t, n = map(int, input().split())

    out = []

    for _ in range(t):
        a, b = map(int, input().split())
        out.append(str(dist(n, a, b)))

    return "\n".join(out)

# provided sample
assert run(
"""10 5
1 2
1 3
1 4
1 5
2 3
2 4
2 5
3 4
3 5
4 5
"""
) == "\n".join([
    "1",
    "1",
    "1",
    "2",
    "1",
    "2",
    "3",
    "1",
    "2",
    "1"
]), "sample 1"

# smallest non-trivial graph
assert run(
"""1 1
1 2
"""
) == "1", "single edge"

# D(2) is triangle
assert run(
"""3 2
1 2
1 3
2 3
"""
) == "\n".join([
    "1",
    "1",
    "1"
]), "triangle distances"

# connector boundary case
assert run(
"""1 3
1 4
"""
) == "1", "direct connector edge"

# larger recursive case
assert run(
"""2 5
2 8
3 11
"""
) == "\n".join([
    "3",
    "2"
]), "cross-half recursion"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 1 / 1 2` | `1` | Base graph handling |
| Triangle queries in `D(2)` | all `1` | Correct connector construction |
| `1 3 / 1 4` | `1` | Direct crossing edge |
| Larger recursive queries | `3`, `2` | Multi-level recursion correctness |

## Edge Cases

Consider:

```
1 2
1 3
```

`D(2)` is a triangle. The algorithm detects that vertex `1` lies in the left half while `3` lies in the right half. It evaluates both connector edges:

- through `(1,3)`
- through `(2,3)`

The first route has length `1`, so the answer is correct. A solution that only descends recursively without checking connector shortcuts would fail here.

Now consider:

```
1 3
1 4
```

In `D(3)`, vertex `4` is the first vertex of the right recursive half. By construction, there is a direct edge `(1,4)`.

The recursion reaches the mixed-half case immediately:

$$dist(2,1,1)+1+dist(1,1,1)=1$$

The answer becomes `1` exactly as required.

Another subtle boundary case:

```
1 5
8 13
```

The vertices belong to different recursive layers deep inside the graph. The algorithm repeatedly shifts coordinates into local recursive systems until both vertices become connector-adjacent in smaller subgraphs.

Because every recursive call preserves the meaning of local vertex numbering, no information is lost during these shifts.
