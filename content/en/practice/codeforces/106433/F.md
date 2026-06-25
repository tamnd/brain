---
title: "CF 106433F - Broken Line Operation"
description: "The network is a tree of agents. Exactly k agents must be marked as active. Every communication channel whose two endpoints receive different statuses, one active and one inactive, contributes one point."
date: "2026-06-25T09:38:13+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 106433
codeforces_index: "F"
codeforces_contest_name: "XXX Spain Olympiad in Informatics, online qualifier"
rating: 0
weight: 106433
solve_time_s: 39
verified: true
draft: false
---

[CF 106433F - Broken Line Operation](https://codeforces.com/problemset/problem/106433/F)

**Rating:** -  
**Tags:** -  
**Solve time:** 39s  
**Verified:** yes  

## Solution
## Problem Understanding

The network is a tree of agents. Exactly `k` agents must be marked as active. Every communication channel whose two endpoints receive different statuses, one active and one inactive, contributes one point. The goal is to choose the active agents so that the number of such crossing channels is as large as possible.

Because the network is a tree, every pair of agents has a unique path between them. This property removes cycles and makes a subtree dynamic programming approach natural.

The constraint `n <= 2000` is the main clue. A quadratic solution is realistic because the total number of vertices across all test cases is also only 2000. A solution around `O(n^2)` per test case is safe, while solutions that enumerate subsets or try all choices of `k` vertices are impossible because the number of possible selections grows exponentially.

The important edge cases come from the exact value of `k` and from the structure of the tree.

For `k = 0`, no agent is active, so no edge can connect different groups. For example:

```
Input
1
2 0
1 2
```

The answer is:

```
0
```

A careless solution that assumes at least one active vertex might access invalid states or count the edge incorrectly.

For `k = n`, every agent is active, so again there are no crossing edges. For example:

```
Input
1
3 3
1 2
2 3
```

The answer is:

```
0
```

A greedy method that tries to maximize the degree of selected vertices may fail because selecting all vertices removes every possible boundary.

A chain also behaves differently from a star. Consider:

```
Input
1
5 2
1 2
1 3
1 4
1 5
```

The answer is:

```
3
```

Selecting the center and one leaf gives only three crossing edges. Selecting two leaves gives only two crossing edges. A strategy based only on selecting high degree vertices can miss the need to consider how selected vertices interact with their children.

## Approaches

A direct brute force solution would try every possible group of `k` active agents, count the edges crossing between active and inactive groups, and keep the maximum. This is correct because every valid choice is checked. However, the number of choices is `C(n, k)`, which becomes enormous even for moderate `n`. With `n = 2000`, enumerating subsets is completely impossible.

The tree structure gives us a way to build the answer instead of guessing it. When we root the tree, every edge connects a vertex with one of its children. Whether that edge contributes depends only on the status of the two endpoints. This means each subtree can summarize all possible choices inside it.

The missing information in a one dimensional subtree DP is whether the root of that subtree is active. A child subtree containing active vertices does not necessarily make the edge to its parent a crossing edge, because the child itself might still be inactive. We solve this by keeping two states: one where the current vertex is active and one where it is inactive.

The brute force works because it checks all possible active sets, but fails because there are too many. The observation that every edge contribution only depends on the two endpoints lets us combine optimal answers from smaller subtrees with knapsack style merging.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(C(n,k) * n) | O(n) | Too slow |
| Tree DP | O(n^2) | O(n^2) | Accepted |

## Algorithm Walkthrough

1. Root the tree at an arbitrary vertex, such as vertex `1`, and run a depth first search. The DFS order lets us process children before their parent.
2. For every vertex `v`, maintain two arrays. `active[v][i]` is the maximum number of crossing edges inside the subtree of `v` when exactly `i` vertices are active and `v` itself is active. `inactive[v][i]` has the same meaning when `v` itself is inactive.
3. Initialize every vertex with two possibilities. If `v` is active, the subtree currently contains one active vertex and contributes zero crossing edges. If `v` is inactive, it contains zero active vertices and also contributes zero crossing edges.
4. Merge every child subtree into the current vertex using knapsack transitions. Suppose a child subtree contributes `j` active vertices. If `v` is active, choosing an active child root uses `active[child][j]`, while choosing an inactive child root uses `inactive[child][j] + 1` because the edge between `v` and the child crosses the partition.
5. Perform the symmetric transition when `v` is inactive. Choosing an active child root adds one crossing edge, while choosing an inactive child root does not.
6. After all children are merged, the answer is the better of making the root active with `k` active vertices or making it inactive with `k` active vertices.

Why it works:

The invariant is that after processing a vertex, each DP state stores the best possible number of crossing edges inside that subtree for every possible number of active vertices while respecting the state of the subtree root. Every edge is considered exactly once, when its parent and child are merged. At that moment the DP states know the statuses of both endpoints, so the edge is either counted exactly when it crosses or ignored when it does not. Since every subtree combination is explored through the knapsack merges, the final root state represents the best possible selection of exactly `k` active vertices.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve_case(n, k, edges):
    graph = [[] for _ in range(n)]
    for u, v in edges:
        u -= 1
        v -= 1
        graph[u].append(v)
        graph[v].append(u)

    active = [None] * n
    inactive = [None] * n
    size = [0] * n

    def dfs(v, p):
        size[v] = 1
        active[v] = [-10**9] * 2
        inactive[v] = [-10**9] * 2

        active[v][1] = 0
        inactive[v][0] = 0

        for u in graph[v]:
            if u == p:
                continue
            dfs(u, v)

            new_active = [-10**9] * (size[v] + size[u] + 1)
            new_inactive = [-10**9] * (size[v] + size[u] + 1)

            for i in range(size[v] + 1):
                if active[v][i] > -10**9:
                    for j in range(size[u] + 1):
                        if active[u][j] > -10**9:
                            new_active[i + j] = max(
                                new_active[i + j],
                                active[v][i] + active[u][j]
                            )
                        if inactive[u][j] > -10**9:
                            new_active[i + j] = max(
                                new_active[i + j],
                                active[v][i] + inactive[u][j] + 1
                            )

                if inactive[v][i] > -10**9:
                    for j in range(size[u] + 1):
                        if active[u][j] > -10**9:
                            new_inactive[i + j] = max(
                                new_inactive[i + j],
                                inactive[v][i] + active[u][j] + 1
                            )
                        if inactive[u][j] > -10**9:
                            new_inactive[i + j] = max(
                                new_inactive[i + j],
                                inactive[v][i] + inactive[u][j]
                            )

            size[v] += size[u]
            active[v] = new_active[:size[v] + 1]
            inactive[v] = new_inactive[:size[v] + 1]

    dfs(0, -1)
    return max(active[0][k], inactive[0][k])

def main():
    t = int(input())
    ans = []
    for _ in range(t):
        n, k = map(int, input().split())
        edges = [tuple(map(int, input().split())) for _ in range(n - 1)]
        ans.append(str(solve_case(n, k, edges)))
    print("\n".join(ans))

if __name__ == "__main__":
    main()
```

The adjacency list stores the tree because every vertex can have many neighbors and the input only gives edges. The DFS converts the undirected tree into rooted subtrees.

The two DP arrays are the central implementation detail. `active[v][i]` and `inactive[v][i]` have different meanings, which avoids the common mistake of counting an edge when the child subtree contains active vertices but the child itself is inactive.

During merging, the loops try every possible split of active vertices between the already processed part of `v` and the new child subtree. The transition adds one only when the endpoint statuses differ. The initial states handle the boundary cases `0` and `1` active vertex inside a subtree.

Python integers do not overflow, but the negative sentinel value is still needed to represent impossible states. The answer is always found at index `k`, because the problem requires exactly that many active vertices.

## Worked Examples

### Sample 1

Input:

```
3
3 2
1 2
2 3
5 2
1 2
1 3
1 4
1 5
2 0
1 2
```

For the first tree:

| Vertex | State | Active count | Best crossing edges |
| --- | --- | --- | --- |
| 1 | inactive | 2 | 2 |
| 1 | active | 2 | 1 |
| Answer |  |  | 2 |

The optimal choice activates the two endpoints of the chain. Both edges cross the partition.

For the second tree:

| Vertex | State | Active count | Best crossing edges |
| --- | --- | --- | --- |
| 1 | active | 2 | 3 |
| 1 | inactive | 2 | 2 |
| Answer |  |  | 3 |

Activating the center and one leaf creates three crossing edges from the remaining leaves.

### Sample 2

Input:

```
1
4 1
1 2
2 3
3 4
```

| Vertex | State | Active count | Best crossing edges |
| --- | --- | --- | --- |
| 1 | active | 1 | 1 |
| 2 | active | 1 | 2 |
| 3 | active | 1 | 2 |
| 4 | active | 1 | 1 |
| Answer |  |  | 2 |

The best single active vertex is one of the middle vertices because it has two incident edges that can cross.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n^2) | Each tree edge performs a knapsack merge over possible active counts. |
| Space | O(n^2) | The stored DP arrays across all vertices contain quadratic total information in the worst case. |

The maximum total `n` across all cases is 2000, so a quadratic algorithm fits comfortably within the limits. The implementation only stores arrays for the current tree, keeping memory usage practical.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    old = sys.stdin
    sys.stdin = io.StringIO(inp)
    data = sys.stdin.read().split()
    sys.stdin = old

    if not data:
        return ""

    it = iter(data)
    t = int(next(it))
    out = []

    def solve_case(n, k, edges):
        graph = [[] for _ in range(n)]
        for u, v in edges:
            u -= 1
            v -= 1
            graph[u].append(v)
            graph[v].append(u)

        A = [None] * n
        B = [None] * n
        sz = [0] * n

        def dfs(v, p):
            sz[v] = 1
            A[v] = [-10**9, 0]
            B[v] = [0, -10**9]

            for u in graph[v]:
                if u == p:
                    continue
                dfs(u, v)
                na = [-10**9] * (sz[v] + sz[u] + 1)
                nb = [-10**9] * (sz[v] + sz[u] + 1)
                for i in range(sz[v] + 1):
                    for j in range(sz[u] + 1):
                        if i < len(A[v]) and j < len(A[u]):
                            na[i+j] = max(na[i+j], A[v][i] + A[u][j])
                        if i < len(A[v]) and j < len(B[u]):
                            na[i+j] = max(na[i+j], A[v][i] + B[u][j] + 1)
                        if i < len(B[v]) and j < len(A[u]):
                            nb[i+j] = max(nb[i+j], B[v][i] + A[u][j] + 1)
                        if i < len(B[v]) and j < len(B[u]):
                            nb[i+j] = max(nb[i+j], B[v][i] + B[u][j])
                sz[v] += sz[u]
                A[v] = na[:sz[v]+1]
                B[v] = nb[:sz[v]+1]

        dfs(0, -1)
        return max(A[0][k], B[0][k])

    for _ in range(t):
        n = int(next(it))
        k = int(next(it))
        edges = []
        for _ in range(n - 1):
            edges.append((int(next(it)), int(next(it))))
        out.append(str(solve_case(n, k, edges)))

    return "\n".join(out)

assert run("""3
3 2
1 2
2 3
5 2
1 2
1 3
1 4
1 5
2 0
1 2
""") == "2\n3\n0", "samples"

assert run("""1
2 1
1 2
""") == "1", "minimum tree"

assert run("""1
5 5
1 2
2 3
3 4
4 5
""") == "0", "all active"

assert run("""1
5 0
1 2
1 3
1 4
1 5
""") == "0", "none active"

assert run("""1
4 1
1 2
2 3
3 4
""") == "2", "middle vertex choice"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Three sample cases | `2, 3, 0` | Basic correctness and boundary `k` values |
| Two vertices with one active | `1` | Smallest possible tree |
| Entire tree active | `0` | No crossing edges when all vertices share a state |
| No active vertices | `0` | Empty selected set handling |
| Chain with one active vertex | `2` | Choosing an internal vertex instead of a leaf |

## Edge Cases

When `k = 0`, every DP state except the fully inactive state is impossible at the root. For:

```
1
2 0
1 2
```

the DFS starts with each leaf allowing zero active vertices only through its inactive state. The merge never creates a crossing edge because both endpoints remain inactive, giving answer `0`.

When `k = n`, every vertex must be active. The DP can only use active states all the way through the tree. Since every edge has two active endpoints, no transition adds a crossing contribution. For:

```
1
3 3
1 2
2 3
```

the answer remains `0`.

For a star-shaped tree:

```
1
5 2
1 2
1 3
1 4
1 5
```

the root has four children. The DP compares selecting the center with one leaf against selecting two leaves. The center selection creates three child edges with different endpoint states, so it reaches the optimal answer `3`.

For a chain:

```
1
4 1
1 2
2 3
3 4
```

the DP keeps both root-status possibilities for every subtree. It discovers that selecting vertex `2` or `3` gives two crossing edges, while selecting an endpoint gives only one. This is exactly the kind of case where a local degree based greedy choice is insufficient.
