---
title: "CF 102392F - Game on a Tree"
description: "Root the given tree at vertex 1. The game can be viewed more naturally as a game on another graph. Create a graph whose vertices are the tree vertices, and connect two vertices whenever one is an ancestor of the other in the rooted tree."
date: "2026-08-10T19:33:44+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102392
codeforces_index: "F"
codeforces_contest_name: "2019-2020 ICPC Southeastern European Regional Programming Contest (SEERC 2019)"
rating: 0
weight: 102392
solve_time_s: 85
verified: true
draft: false
---

[CF 102392F - Game on a Tree](https://codeforces.com/problemset/problem/102392/F)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 25s  
**Verified:** yes  

## Solution
## Problem Understanding

Root the given tree at vertex `1`. The game can be viewed more naturally as a game on another graph. Create a graph whose vertices are the tree vertices, and connect two vertices whenever one is an ancestor of the other in the rooted tree. A move in the original game is exactly a move along one of these edges to a vertex that has not been visited before. The original tree edges are only a way to describe this ancestor relation, and a move may jump over several levels.

Alice first chooses any vertex, which is equivalent to choosing the starting vertex of a vertex-geography game on this ancestor graph. Every subsequent move marks a previously unused vertex, and the player who has no legal unused neighbor loses. The required output is `Alice` if the first player has a winning strategy and `Bob` otherwise.

There are up to `100000` vertices and `99999` edges. With a one-second time limit, an algorithm whose work grows quadratically is already too expensive in Python, and anything exponential is completely out of reach. The tree itself can be processed in linear time, so the target is `O(n)` time and `O(n)` memory. The key challenge is that the implicit ancestor graph can have `Theta(n^2)` edges, so explicitly constructing it is not an option.

The first edge case is a single vertex.

```
1
```

The correct answer is `Alice`. Alice makes the only possible initial move, after which Bob has no move. An implementation that starts only from tree edges or assumes every game contains at least one move after the initial placement can mishandle this case.

A second edge case is a path with an even number of vertices.

```
4
1 2
2 3
3 4
```

The answer is `Bob`. Every pair of vertices is comparable on a rooted path, so after Alice's first choice the remaining three vertices are all reachable. The players consequently visit all four vertices, with Bob making the last move. A solution based only on parity is tempting, but it fails on branching trees, because incomparable vertices cannot be used as consecutive moves.

A third edge case is branching with an even number of vertices.

```
4
1 2
1 3
1 4
```

The answer is `Alice`. Alice can start at a leaf. Bob can move to the root, after which Alice moves to another leaf, and Bob has no legal move. Treating every pair of tree vertices as adjacent would incorrectly turn this into a complete graph and give the wrong winner.

Finally, ancestor does not mean immediate parent or child. For example,

```
4
1 2
2 3
3 4
```

allows vertex `1` to move directly to vertex `4`, because they are ancestor and descendant. An algorithm that constructs only the original tree edges solves a different game and can fail on hidden tests.

## Approaches

A direct brute-force solution can represent the set of black vertices and recursively try every legal next vertex. It is correct because the game is finite, so minimax can examine every possible continuation and determine whether the current position is winning. On a path, however, every vertex is comparable with every other vertex. Once the first vertex is selected, any remaining vertex can be chosen next, so the game contains all `n!` possible complete visitation orders. A straightforward recursive search consequently has `Theta(n!)` terminal branches, and scanning possible moves at each state can push the work to `O(n * n!)`. Even with memoization, there can be `Theta(n * 2^n)` states, which is still hopeless for `n = 100000`.

The useful observation is that this game has a standard matching characterization. For any undirected graph, if there is a perfect matching, the second player can answer every move by moving to the vertex matched with the vertex just chosen. The matched vertex is guaranteed to be unused, because its partner was the only vertex that could have consumed it earlier.

The reverse direction is just as useful. Suppose a maximum matching is not perfect, and let Alice start at an unmatched vertex. Bob cannot move from Alice's starting vertex to another unmatched vertex, because such a move would create an augmenting path for the maximum matching. Thus every vertex Bob can reach is matched. Alice can answer using its matching partner, exactly as the second-player strategy works in the perfect-matching case. This gives Alice the winning strategy. This matching characterization is the central game-theoretic reduction.

So the game is reduced to one question: does the ancestor graph have a perfect matching?

We still cannot build the ancestor graph, because it may contain quadraticly many edges. The special structure of a rooted tree saves us. Inside a subtree of `u`, vertices belonging to two different child subtrees are incomparable, so they can never be paired with each other. The only vertex in `u`'s subtree that can connect different child subtrees is `u` itself. This makes a very small tree DP possible.

Let `dp[u]` be the minimum number of vertices left unmatched after taking a maximum matching entirely inside the subtree of `u`. If the children collectively leave `s` unmatched vertices, then when `s = 0`, `u` itself has nobody below it to pair with, so one unmatched vertex remains. When `s > 0`, `u` can be paired with one of those unmatched descendants, leaving `s - 1`. Thus

dp[u]={ 1, s−1, ​ s=0, s>0, ​

where

s= v child of u ∑ ​ dp[v].

This is exactly the tree DP used for the problem's ancestor-descendant matching formulation.

The root has a perfect matching precisely when `dp[1] = 0`. If it is zero, Bob wins. Otherwise, Alice wins.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | `O(n · n!)` without memoization | `O(n)` recursion/state | Too slow |
| Optimal | `O(n)` | `O(n)` | Accepted |

## Algorithm Walkthrough

1. Build the original tree as an adjacency list. We never explicitly construct ancestor-descendant edges, because there can be `Theta(n^2)` of them.
2. Root the tree at vertex `1` and compute a parent array together with a traversal order. Processing the vertices in reverse traversal order gives a bottom-up tree DP without relying on Python's recursion depth.
3. For every vertex `u`, compute

s=∑dp[v]

over its children `v`. Each child contributes the minimum number of unmatched vertices that its subtree must expose.
4. If `s = 0`, set `dp[u] = 1`. Every child subtree can already be perfectly matched internally, so there is no available descendant for `u` to pair with. Vertex `u` itself must remain unmatched.
5. If `s > 0`, set `dp[u] = s - 1`. At least one unmatched vertex exists somewhere below `u`, and every such vertex is a descendant of `u`, so `u` can be matched with one of them. This consumes exactly one previously unmatched vertex.
6. After processing the root, check `dp[1]`. A value of zero means the entire tree can be partitioned into ancestor-descendant pairs, which is a perfect matching of the game graph. Bob wins in that case. Any positive value means the maximum matching leaves at least one vertex unmatched, so Alice starts at such an unmatched vertex and wins.

Why it works: the DP maintains the invariant that `dp[u]` is the minimum number of unmatched vertices among all matchings contained completely in the subtree of `u`. Child subtrees cannot interact with each other because vertices from different child subtrees are incomparable. Consequently, the only possible improvement after combining the children is to use `u` to match one exposed descendant. The recurrence considers exactly those two possibilities and therefore computes the true minimum. At the root, zero unmatched vertices is equivalent to a perfect matching. The matching game argument then determines the winner.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())

    graph = [[] for _ in range(n)]

    for _ in range(n - 1):
        u, v = map(int, input().split())
        u -= 1
        v -= 1
        graph[u].append(v)
        graph[v].append(u)

    # Root the tree at 0.
    parent = [-1] * n
    order = [0]
    parent[0] = -2

    for u in order:
        for v in graph[u]:
            if v == parent[u]:
                continue
            parent[v] = u
            order.append(v)

    # Process children before parents.
    dp = [0] * n

    for u in reversed(order):
        total = 0

        for v in graph[u]:
            if parent[v] == u:
                total += dp[v]

        if total == 0:
            dp[u] = 1
        else:
            dp[u] = total - 1

    print("Bob" if dp[0] == 0 else "Alice")

if __name__ == "__main__":
    solve()
```

The adjacency list stores only the `n - 1` original tree edges. The `parent` array roots the tree at vertex `1`, represented by index `0` in Python. The `order` array is a traversal from the root, so reversing it guarantees that every child has already received its `dp` value when its parent is processed.

The DP itself is deliberately small. For every vertex, `total` is the sum of the values of its children. The expression `total == 0` is the only boundary case in the recurrence. When it is zero, the current vertex contributes one unmatched vertex. Otherwise, it consumes one unmatched descendant.

The implementation is iterative rather than recursive. A path with `100000` vertices would create recursion depth around `100000`, which is unsafe in Python even if the recursion limit is manually increased. No integer overflow is possible because Python integers are arbitrary precision, and in fact every `dp[u]` is at most the size of its subtree.

The order of operations matters. Computing a parent before pushing a neighbor prevents the undirected edge back to the parent from being treated as a child edge. The condition `parent[v] == u` in the DP phase then identifies exactly the children of `u`.

## Worked Examples

### Sample 1

The tree is a path:

```
1 - 2 - 3 - 4
```

Every vertex has at most one child after rooting at `1`.

| Vertex | Children | Child sum | `dp` |
| --- | --- | --- | --- |
| 4 | none | 0 | 1 |
| 3 | 4 | 1 | 0 |
| 2 | 3 | 0 | 1 |
| 1 | 2 | 1 | 0 |

The root has `dp[1] = 0`, so the ancestor graph has a perfect matching. One such matching is `(1,2), (3,4)`. Bob can always respond using the matching partner of Alice's latest move, so the output is `Bob`.

### Sample 2

After rooting at `1`, vertex `1` has children `2` and `3`. Vertex `2` has children `4`, `5`, `6`, and `7`, while `3` is a leaf.

| Vertex | Children | Child sum | `dp` |
| --- | --- | --- | --- |
| 4 | none | 0 | 1 |
| 5 | none | 0 | 1 |
| 6 | none | 0 | 1 |
| 7 | none | 0 | 1 |
| 2 | 4, 5, 6, 7 | 4 | 3 |
| 3 | none | 0 | 1 |
| 1 | 2, 3 | 4 | 3 |

The root has `dp[1] = 3`, so three vertices remain unmatched after the best possible matching. There is no perfect matching, and Alice wins. This agrees with the sample strategy, where Alice starts at vertex `3` and uses the branching structure to prevent Bob from maintaining a matching response.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | `O(n)` | Each tree edge is examined a constant number of times. |
| Space | `O(n)` | The adjacency list, parent array, traversal order, and DP array each use linear space. |

The input contains at most `100000` vertices, so linear processing is comfortably within the intended limits. The algorithm never constructs the quadratic-size ancestor graph and avoids recursive DFS depth problems on a degenerate path.

## Test Cases

```python
import sys
import io

def solve():
    input = sys.stdin.readline

    n = int(input())
    graph = [[] for _ in range(n)]

    for _ in range(n - 1):
        u, v = map(int, input().split())
        u -= 1
        v -= 1
        graph[u].append(v)
        graph[v].append(u)

    parent = [-1] * n
    parent[0] = -2
    order = [0]

    for u in order:
        for v in graph[u]:
            if v == parent[u]:
                continue
            parent[v] = u
            order.append(v)

    dp = [0] * n

    for u in reversed(order):
        total = 0
        for v in graph[u]:
            if parent[v] == u:
                total += dp[v]

        dp[u] = 1 if total == 0 else total - 1

    print("Bob" if dp[0] == 0 else "Alice")

def run(inp: str) -> str:
    old_stdin = sys.stdin
    old_input = globals()["input"]

    sys.stdin = io.StringIO(inp)
    globals()["input"] = sys.stdin.readline

    try:
        from io import StringIO
        old_stdout = sys.stdout
        sys.stdout = StringIO()

        solve()
        result = sys.stdout.getvalue().strip()

        sys.stdout = old_stdout
        return result
    finally:
        sys.stdin = old_stdin
        globals()["input"] = old_input

# Provided samples
assert run(
    """4
1 2
2 3
3 4
"""
) == "Bob", "sample 1"

assert run(
    """7
2 1
2 6
1 3
2 5
7 2
2 4
"""
) == "Alice", "sample 2"

# Minimum-size tree
assert run(
    """1
"""
) == "Alice", "single vertex"

# Small branching tree
assert run(
    """4
1 2
1 3
1 4
"""
) == "Alice", "star with three leaves"

# Perfect matching in the ancestor graph
assert run(
    """6
1 2
1 3
2 4
3 5
4 6
"""
) == "Bob", "perfect ancestor matching"

# Maximum-size path, n is even
n = 100000
edges = "\n".join(f"{i} {i + 1}" for i in range(1, n))
assert run(f"{n}\n{edges}\n") == "Bob", "maximum-size path"

# Maximum-size star, repeated identical leaf structure
n = 100000
edges = "\n".join(f"1 {i}" for i in range(2, n + 1))
assert run(f"{n}\n{edges}\n") == "Alice", "maximum-size star"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1` | `Alice` | Minimum-size boundary case and leaf recurrence |
| `1-2, 1-3, 1-4` | `Alice` | Branching where parity alone is insufficient |
| `1-2, 1-3, 2-4, 3-5, 4-6` | `Bob` | A nontrivial perfect matching |
| Path with `100000` vertices | `Bob` | Maximum depth and iterative traversal |
| Star with `100000` vertices | `Alice` | Maximum degree and repeated identical child states |

The phrase "all-equal values" does not correspond to an input feature here because the problem has no vertex values. The maximum-size star serves the same testing purpose structurally: every leaf has exactly the same local state, so it checks whether repeated identical DP contributions are accumulated correctly.

## Edge Cases

For the single-vertex case,

```
1
```

the traversal contains only the root. Its child sum is zero, so `dp[1] = 1`. The root cannot be perfectly matched, meaning the ancestor graph has no perfect matching. Alice wins immediately, and the algorithm prints `Alice`.

For the four-vertex path,

```
4
1 2
2 3
3 4
```

the bottom-up values are `dp[4] = 1`, `dp[3] = 0`, `dp[2] = 1`, and `dp[1] = 0`. The zero at the root represents the matching `(1,2), (3,4)`. Bob can use these pairs as responses, giving `Bob`. This case also confirms that the DP is not simply counting vertices modulo two.

For the branching tree,

```
4
1 2
1 3
1 4
```

each leaf contributes `1`, so the root receives a child sum of `3` and obtains `dp[1] = 2`. There is no perfect matching. Alice can start at a leaf, after which Bob is forced to the root, and Alice takes another leaf. Bob then has no legal move. The algorithm correctly prints `Alice`.

For the nontrivial perfect-matching case,

```
6
1 2
1 3
2 4
3 5
4 6
```

the values are `dp[6] = 1`, `dp[4] = 0`, `dp[2] = 1`, `dp[5] = 1`, `dp[3] = 0`, and finally `dp[1] = 0`. A perfect matching is `(4,6), (2,1), (3,5)`. The pairs need not all be original tree edges in general, only ancestor-descendant pairs. Since the matching covers every vertex, Bob has a response to every Alice move.

For the maximum-size path, the implementation never recursively descends through `100000` stack frames. It constructs the parent order iteratively, processes that order backwards, and obtains `dp[1] = 0` because an even-length path has a perfect matching. The result is `Bob`.

For the maximum-size star, every leaf contributes `1`. The root sees `99999` unmatched descendants and consumes one of them, leaving `99998`, so `dp[1] > 0`. The result is `Alice`. This also exercises the largest possible degree and confirms that the child contributions must be summed rather than reduced to a Boolean state.
