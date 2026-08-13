---
title: "CF 102373B - Wooden Castle"
description: "We have a tree whose vertices are colored with two colors, represented by 0 and 1. We may either flip the color of one still-existing vertex, paying one operation, or choose a vertex and destroy the entire connected component of its current color containing that vertex, also…"
date: "2026-08-14T03:03:04+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102373
codeforces_index: "B"
codeforces_contest_name: "\u0426\u0438\u043a\u043b \u0418\u043d\u0442\u0435\u0440\u043d\u0435\u0442-\u043e\u043b\u0438\u043c\u043f\u0438\u0430\u0434 \u0434\u043b\u044f \u0448\u043a\u043e\u043b\u044c\u043d\u0438\u043a\u043e\u0432, \u0421\u0435\u0437\u043e\u043d 2019-2020, \u041f\u0435\u0440\u0432\u0430\u044f \u043a\u043e\u043c\u0430\u043d\u0434\u043d\u0430\u044f \u043e\u043b\u0438\u043c\u043f\u0438\u0430\u0434\u0430"
rating: 0
weight: 102373
solve_time_s: 143
verified: false
draft: false
---

[CF 102373B - Wooden Castle](https://codeforces.com/problemset/problem/102373/B)

**Rating:** -  
**Tags:** -  
**Solve time:** 2m 23s  
**Verified:** no  

## Solution
## Problem Understanding

We have a tree whose vertices are colored with two colors, represented by `0` and `1`. We may either flip the color of one still-existing vertex, paying one operation, or choose a vertex and destroy the entire connected component of its current color containing that vertex, also paying one operation. The goal is to remove every vertex with as few operations as possible.

The answer is not simply the current number of monochromatic components, because recoloring a carefully chosen vertex can merge several components and make one chain reaction remove all of them. The sample illustrates exactly this: in the star with center color `1` and three leaves color `0`, changing the center to `0` creates one monochromatic component, so two operations are enough.

The tree contains up to `200000` vertices. Since a tree has exactly `n - 1` edges, reading and processing the input already requires linear time. An algorithm with quadratic behavior is too slow at this size, and an exponential search over colorings is completely infeasible. The intended solution needs to process every vertex and edge only a constant number of times, giving `O(n)` time.

There are several small cases where a superficial solution can fail. With one vertex, for example,

```
1
0
```

the answer is `1`, because the single vertex can simply be destroyed. A formula that always adds a recoloring operation would incorrectly return `2`.

An all-equal tree such as

```
3
000
1 2
2 3
```

also has answer `1`. Every vertex already belongs to the same monochromatic component, so one chain reaction removes the whole tree.

The opposite extreme is an alternating path:

```
3
010
1 2
2 3
```

Its answer is `2`. Recoloring the middle vertex gives `000`, after which one chain reaction removes everything. A method that only counts the initial monochromatic components would see three components and miss the useful recoloring.

The structure of the tree matters as well. In

```
4
1000
1 2
1 3
1 4
```

the answer is `2`, not `4`: either destroy the black center and then the white leaves as one component, or recolor the center to `0` and destroy the resulting all-white tree.

## Approaches

A direct brute-force approach is to decide the color that every vertex should have immediately before it is destroyed. There are `2^n` possible target colorings. For each target coloring, we can count how many vertices changed color and how many monochromatic connected components it contains, then take the minimum. Evaluating one coloring takes `O(n)` time because we inspect every vertex and edge, so the total complexity is `Theta(n * 2^n)`. This is already hopeless for a few dozen vertices, let alone `200000`.

The useful observation is that we do not actually have to simulate the chain reactions.

Consider any complete sequence of operations. Give every vertex the color it has at the moment it is destroyed. Every vertex whose final destruction color differs from its initial color must have been recolored at least once. Now look at two adjacent vertices that receive the same destruction color. If they were destroyed in different chain reactions, we could conceptually merge those reactions into one monochromatic component, which can only reduce the number of destruction operations. Thus an optimal strategy can be represented by a final binary coloring of the tree.

For a fixed final coloring, the number of recoloring operations needed is exactly its Hamming distance from the original coloring. The number of chain reactions is the number of monochromatic connected components in that final coloring.

Because the graph is a tree, this component count has an especially simple form. Start with one component. Every edge whose endpoints have different final colors separates two components, while an edge whose endpoints have the same color stays inside one component. Consequently,

`number of components = 1 + number of edges whose endpoints have different colors`.

The entire problem therefore becomes minimizing

`1 + sum over vertices [final_color != initial_color] + sum over edges [final_color differs across the edge]`.

This is a standard two-state tree DP. For each vertex, we calculate the minimum cost of its subtree when that vertex receives final color `0` or `1`. The contribution of a child depends only on whether the child's final color equals its parent's final color, so each child can be handled independently.

The brute force works because every possible final coloring describes a valid way to organize the destruction process, but it fails because there are exponentially many colorings. The observation that the objective consists only of independent vertex costs and edge costs lets us optimize those `2^n` choices with a two-state DP on the tree.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | `O(n * 2^n)` | `O(n)` | Too slow |
| Optimal tree DP | `O(n)` | `O(n)` | Accepted |

## Algorithm Walkthrough

1. Root the tree at vertex `0`. The choice of root is arbitrary, because the objective is defined on the undirected tree.
2. For every vertex `v`, maintain two values `dp[v][0]` and `dp[v][1]`. `dp[v][c]` is the minimum cost contributed by the subtree of `v` if `v` receives final color `c`, excluding the global `+1` corresponding to the first connected component.
3. Initialize the state of `v` with its recoloring cost. If the original color of `v` is already `c`, this cost is `0`; otherwise it is `1`.
4. Process every child `u` of `v`. If `u` receives the same color `c` as `v`, the edge `(v,u)` does not create an additional monochromatic component boundary, so the child contributes `dp[u][c]`. If `u` receives the opposite color, the edge is a boundary between two components and contributes `dp[u][1-c] + 1`.

Thus the transition for a fixed parent color `c` is

`dp[v][c] += min(dp[u][c], dp[u][1-c] + 1)`.

The `+1` in the second option represents the edge whose endpoints have different final colors.
5. Process vertices in postorder so that every child's DP values are known before its parent is calculated. An iterative traversal is preferable in Python because a tree can be a path of length `200000`, which would exceed Python's default recursive call depth.
6. At the root, choose whichever final color is cheaper. Finally add `1` for the global component-count term, giving

`answer = 1 + min(dp[root][0], dp[root][1])`.

The extra `1` is always present because every nonempty tree has at least one monochromatic component.

### Why it works

For any chosen final coloring, every vertex with a changed color costs exactly one recoloring operation, and every edge joining different final colors increases the number of monochromatic components by exactly one. Since a tree starts with one component, the total cost for that coloring is precisely the DP objective plus one.

Conversely, any actual sequence of operations can be converted into such a final coloring by assigning each vertex its color when it is destroyed. The number of recolorings in the sequence is at least the number of vertices whose final color differs from their initial color, while the number of destruction operations is at least the number of monochromatic components of the final coloring. Thus the DP objective cannot be larger than the cost of an optimal operation sequence. For every DP coloring, we can first perform its required recolorings and then destroy each monochromatic component, so the DP value is achievable. The two directions establish optimality.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    s = input().strip()

    graph = [[] for _ in range(n)]

    for _ in range(n - 1):
        a, b = map(int, input().split())
        a -= 1
        b -= 1
        graph[a].append(b)
        graph[b].append(a)

    parent = [-1] * n
    order = [0]
    parent[0] = n

    for v in order:
        for u in graph[v]:
            if u == parent[v]:
                continue
            parent[u] = v
            order.append(u)

    dp0 = [0] * n
    dp1 = [0] * n

    for v in reversed(order):
        original = ord(s[v]) - ord('0')

        dp0[v] = 1 if original != 0 else 0
        dp1[v] = 1 if original != 1 else 0

        for u in graph[v]:
            if parent[u] != v:
                continue

            dp0[v] += min(dp0[u], dp1[u] + 1)
            dp1[v] += min(dp1[u], dp0[u] + 1)

    print(1 + min(dp0[0], dp1[0]))

if __name__ == "__main__":
    solve()
```

The adjacency list stores the tree in the usual undirected form. Since there are exactly `n - 1` edges, it uses linear memory.

The first traversal constructs `parent` and `order`. Because `order` is produced by walking away from the root, reversing it gives a valid bottom-up order. This avoids recursion entirely, which is useful for a path-shaped tree with `200000` vertices.

The two DP arrays store the two possible final colors independently. For a vertex whose original color is `0`, `dp0[v]` starts at `0` while `dp1[v]` starts at `1`. The opposite happens for an original `1`.

When child `u` is attached to a parent forced to color `0`, there are only two possibilities. Keeping `u` at `0` costs `dp0[u]`, while giving it color `1` costs `dp1[u] + 1` because the connecting edge becomes a boundary between monochromatic components. The same reasoning gives the transition for parent color `1`.

The test `if parent[u] != v` is necessary because the adjacency list contains both directions of every edge. It prevents the parent from being processed as though it were another child.

All costs are at most a small multiple of `n`, so Python integers have no overflow issue. The use of `sys.stdin.readline` keeps input processing linear and fast enough for `200000` edges.

## Worked Examples

### Sample 1

The input is

```
4
1000
1 2
1 3
1 4
```

Root the tree at vertex `1`. The leaves are vertices `2`, `3`, and `4`, all initially `0`.

| Vertex | Original | `dp0` before children | `dp1` before children | Final `dp0` | Final `dp1` |
| --- | --- | --- | --- | --- | --- |
| 4 | 0 | 0 | 1 | 0 | 1 |
| 3 | 0 | 0 | 1 | 0 | 1 |
| 2 | 0 | 0 | 1 | 0 | 1 |
| 1 | 1 | 1 | 0 | 1 | 3 |

For the root to finish with color `0`, every leaf can also finish with color `0`, giving cost `0` for each child. The root itself needs one recoloring, so the DP cost is `1`.

For the root to finish with color `1`, keeping each leaf at `0` creates three boundary edges, giving cost `3`.

The final answer is

`1 + min(1, 3) = 2`.

The corresponding strategy is exactly the sample's strategy: recolor vertex `1`, then destroy the single all-white component.

### Constructed Sample 2

Consider

```
3
010
1 2
2 3
```

The tree is a path, and its colors alternate.

| Vertex | Original | `dp0` | `dp1` |
| --- | --- | --- | --- |
| 3 | 0 | 0 | 1 |
| 2 | 1 | 1 | 1 |
| 1 | 0 | 1 | 2 |

At vertex `3`, keeping color `0` costs nothing, while changing it to `1` costs one.

At vertex `2`, choosing color `0` costs one for recoloring and then can use vertex `3` at color `0` without an edge boundary, giving `1`. Choosing color `1` costs one for recoloring, while the child can remain `0` at an additional edge cost, also giving `1`.

At vertex `1`, choosing color `0` allows vertex `2` to use color `0` with cost `1`, so the subtree cost is `1`. Choosing color `1` is more expensive.

The answer is

`1 + min(1, 2) = 2`.

This corresponds to changing the middle vertex from `1` to `0`, after which all three vertices form one monochromatic component.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | `O(n)` | Every vertex and every tree edge is processed a constant number of times. |
| Space | `O(n)` | The adjacency list, traversal arrays, parent array, and two DP arrays are all linear in `n`. |

With `n <= 200000`, linear processing is appropriate. The algorithm performs only a few arithmetic operations for each edge and avoids both recursion depth problems and exponential enumeration, so it fits the intended constraints comfortably.

## Test Cases

```python
import sys
import io

def solve():
    input = sys.stdin.readline

    n = int(input())
    s = input().strip()

    graph = [[] for _ in range(n)]

    for _ in range(n - 1):
        a, b = map(int, input().split())
        a -= 1
        b -= 1
        graph[a].append(b)
        graph[b].append(a)

    parent = [-1] * n
    order = [0]
    parent[0] = n

    for v in order:
        for u in graph[v]:
            if u == parent[v]:
                continue
            parent[u] = v
            order.append(u)

    dp0 = [0] * n
    dp1 = [0] * n

    for v in reversed(order):
        original = ord(s[v]) - ord('0')

        dp0[v] = original
        dp1[v] = 1 - original

        for u in graph[v]:
            if parent[u] != v:
                continue

            dp0[v] += min(dp0[u], dp1[u] + 1)
            dp1[v] += min(dp1[u], dp0[u] + 1)

    return str(1 + min(dp0[0], dp1[0]))

def run(inp: str) -> str:
    old_stdin = sys.stdin
    sys.stdin = io.StringIO(inp)
    try:
        return solve().strip()
    finally:
        sys.stdin = old_stdin

assert run("""4
1000
1 2
1 3
1 4
""") == "2", "sample 1"

assert run("""1
0
""") == "1", "single vertex"

assert run("""3
000
1 2
2 3
""") == "1", "all vertices already form one component"

assert run("""3
010
1 2
2 3
""") == "2", "recolor the middle vertex"

assert run("""4
0101
1 2
2 3
3 4
""") == "3", "alternating path"

n = 200000
edges = "\n".join(f"{i} {i + 1}" for i in range(1, n))
large_case = f"{n}\n" + ("0" * n) + "\n" + edges + "\n"
assert run(large_case) == "1", "maximum-size all-equal tree"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 / 0` | `1` | Minimum-size tree and the absence of a nonexistent extra edge. |
| `000` on a path | `1` | All vertices already belong to one monochromatic component. |
| `010` on a path | `2` | A recoloring can merge multiple components. |
| `0101` on a path | `3` | Alternating colors and repeated edge-boundary decisions. |
| `200000` zeros on a path | `1` | Maximum input size, iterative traversal, and linear complexity. |

## Edge Cases

The single-vertex case is handled directly by the DP. For

```
1
0
```

the only state with final color `0` has cost `0`, while the state with final color `1` has cost `1`. The final `+1` gives `1`, which is exactly the one destruction operation needed.

For an already monochromatic tree,

```
3
000
1 2
2 3
```

every vertex can retain color `0`. The two edges both have equal endpoints, so neither contributes a component boundary. The DP value before the global constant is `0`, and the answer is `1`. A method based only on the number of recolorings would miss that one destruction operation is still required.

For the alternating path

```
3
010
1 2
2 3
```

the initial coloring has three components. The DP chooses final coloring `000`, paying one recoloring for vertex `2` and zero edge-boundary costs. Adding the mandatory first component gives `2`. This catches the common mistake of assuming that destroying the original components is always optimal.

For the star

```
4
1000
1 2
1 3
1 4
```

the DP chooses final color `0` for every vertex. Only the center changes color, so the recoloring cost is `1`, and all three edges have equal endpoints, so there are no additional component boundaries. The answer is `1 + 1 = 2`.

Finally, a path of `200000` equal-colored vertices stresses the implementation rather than the mathematics. The iterative parent traversal handles the path without recursion, and every DP transition is processed once. The result remains `1`, while the total work grows linearly with the number of vertices.
