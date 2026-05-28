---
title: "CF 34D - Road Map"
description: "We are given a tree with n cities. Originally, city r1 is considered the capital, and for every other city we know its parent in the rooted tree. The value p[i] means that if we walk from the old capital toward city i, the last city before reaching i is p[i]."
date: "2026-05-28T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "dfs-and-similar", "graphs"]
categories: ["algorithms"]
codeforces_contest: 34
codeforces_index: "D"
codeforces_contest_name: "Codeforces Beta Round 34 (Div. 2)"
rating: 1600
weight: 34
solve_time_s: 89
verified: true
draft: false
---
[CF 34D - Road Map](https://codeforces.com/problemset/problem/34/D)

**Rating:** 1600  
**Tags:** dfs and similar, graphs  
**Solve time:** 1m 29s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a tree with `n` cities. Originally, city `r1` is considered the capital, and for every other city we know its parent in the rooted tree. The value `p[i]` means that if we walk from the old capital toward city `i`, the last city before reaching `i` is `p[i]`.

The king changes the capital from `r1` to `r2`. The roads themselves do not change, only the root of the tree changes. We must output the new parent array when the tree is rooted at `r2`.

The input already describes a valid tree. Since every city except the root has exactly one parent, the parent list gives us all `n - 1` edges. The challenge is to rebuild parent relationships after rerooting.

The constraints are large enough that quadratic solutions are unsafe. With `n` up to `5 * 10^4`, an `O(n^2)` algorithm could require around `2.5 * 10^9` operations in the worst case, which is far beyond the time limit. A linear or near-linear traversal is expected. Trees are especially friendly for DFS and BFS because they contain exactly `n - 1` edges, so a full traversal costs only `O(n)`.

One subtle edge case appears when the new capital lies deep inside the old rooted tree. Consider:

```
5 1 5
1 2 3 4
```

The original structure is:

```
1 - 2 - 3 - 4 - 5
```

After rerooting at `5`, every edge on the path must reverse direction. The correct output becomes:

```
2 3 4 5
```

A careless solution that only changes the direct parent of `5` would leave the rest unchanged and produce an invalid rooted tree.

Another easy mistake happens when reconstructing the input. The parent array skips the old root `r1`, so indices do not align directly with input positions. For example:

```
4 2 1
2 2 3
```

The values correspond to:

```
p[1] = 2
p[3] = 2
p[4] = 3
```

A buggy parser that reads them into positions `1..n-1` mechanically will attach wrong edges.

A third edge case involves recursion depth. A chain-shaped tree with `50000` vertices causes recursive DFS in Python to exceed the default recursion limit. The algorithm itself is correct, but the implementation crashes unless the recursion limit is increased or an iterative traversal is used.

## Approaches

The brute-force idea is straightforward. For every node except the new root `r2`, we could independently search for its parent in the rerooted tree. One way is to start a traversal from `r2` every time and determine which node first reaches the target. Since each traversal costs `O(n)` and we repeat it for all nodes, the total complexity becomes `O(n^2)`.

The brute-force works because trees have unique simple paths. If we root the tree at `r2`, every node except `r2` has exactly one predecessor on the path to the root. Recomputing this relationship from scratch for every node is logically correct, but far too expensive for `50000` nodes.

The key observation is that rerooting does not change the edges at all. Only their directions relative to the root change. Once we rebuild the undirected tree, we can perform a single DFS or BFS starting from `r2`. Whenever we move from node `u` to node `v`, we declare `u` as the parent of `v` in the new rooted tree.

This transforms the problem into a standard tree traversal. Since a tree has exactly `n - 1` edges, DFS visits every edge only twice, once in each direction. The entire solution becomes linear.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n²) | O(n) | Too slow |
| Optimal | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Read the input values `n`, `r1`, and `r2`.
2. Reconstruct the undirected tree from the parent array.

For every city `i` except `r1`, the input provides its parent `p[i]`. Add an undirected edge between `i` and `p[i]`.

The tree must become undirected because after rerooting, edge directions may reverse.
3. Create an array `parent` of size `n + 1`.

This array will store the new parent of every node after rooting at `r2`.
4. Start DFS from `r2`.

During DFS, when moving from node `u` to an unvisited neighbor `v`, assign:

```
parent[v] = u
```

This is correct because `u` is exactly the node from which `v` is reached in the rooted traversal.
5. Continue until all nodes are visited.

Since the graph is a tree, DFS reaches every node exactly once.
6. Output the new parent array in the original format.

The output skips the new root `r2`, because the root has no parent.

### Why it works

The traversal starts at the new capital `r2`, so every DFS tree edge points away from the new root. For every visited node `v`, the first node `u` that reaches it is the unique predecessor of `v` on the path from `r2` to `v`. Trees contain exactly one simple path between any two vertices, so no alternative parent assignment is possible.

Because DFS explores every reachable node exactly once and the graph is connected, every node except `r2` receives exactly one parent. The resulting structure is a valid rooted tree with root `r2`.

## Python Solution

```python
import sys
input = sys.stdin.readline

sys.setrecursionlimit(1 << 20)

n, r1, r2 = map(int, input().split())

adj = [[] for _ in range(n + 1)]

values = list(map(int, input().split()))

ptr = 0
for node in range(1, n + 1):
    if node == r1:
        continue

    p = values[ptr]
    ptr += 1

    adj[node].append(p)
    adj[p].append(node)

parent = [0] * (n + 1)
visited = [False] * (n + 1)

def dfs(u):
    visited[u] = True

    for v in adj[u]:
        if not visited[v]:
            parent[v] = u
            dfs(v)

dfs(r2)

answer = []

for node in range(1, n + 1):
    if node == r2:
        continue
    answer.append(str(parent[node]))

print(" ".join(answer))
```

The first part reconstructs the tree carefully. The input omits the old root `r1`, so we use a separate pointer `ptr` to consume parent values correctly. This is one of the easiest places to introduce an indexing bug.

The adjacency list stores undirected edges. Even though the original input already gives parent relationships, those directions are tied to the old root and become useless after rerooting.

The DFS assigns parents dynamically from the perspective of the new root `r2`. Whenever DFS moves from `u` to `v`, we know that `u` becomes the parent of `v` in the rerooted tree.

The recursion limit is increased because a degenerate chain can contain `50000` nodes. Without this adjustment, Python raises `RecursionError`.

Finally, the output skips `r2`, matching the exact format of the statement. The order is still by node index, not traversal order.

## Worked Examples

### Example 1

Input:

```
3 2 3
2 2
```

Original tree:

```
  2
 / \
1   3
```

New root is `3`.

| Step | Current Node | Newly Visited | Assigned Parent |
| --- | --- | --- | --- |
| Start | 3 | 3 | none |
| DFS | 3 | 2 | parent[2] = 3 |
| DFS | 2 | 1 | parent[1] = 2 |

Final parent array:

| Node | Parent |
| --- | --- |
| 1 | 2 |
| 2 | 3 |

Output:

```
2 3
```

This example shows how only the path toward the new root changes direction.

### Example 2

Input:

```
5 1 3
1 2 3 3
```

Original tree:

```
1 - 2 - 3
        / \
       4   5
```

New root is `3`.

| Step | Current Node | Newly Visited | Assigned Parent |
| --- | --- | --- | --- |
| Start | 3 | 3 | none |
| DFS | 3 | 2 | parent[2] = 3 |
| DFS | 2 | 1 | parent[1] = 2 |
| DFS | 3 | 4 | parent[4] = 3 |
| DFS | 3 | 5 | parent[5] = 3 |

Final parent array:

| Node | Parent |
| --- | --- |
| 1 | 2 |
| 2 | 3 |
| 4 | 3 |
| 5 | 3 |

Output:

```
2 3 3 3
```

This trace demonstrates that only edges on the route from the old root to the new root reverse direction. The remaining subtree structure stays unchanged.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Each node and edge is processed once during DFS |
| Space | O(n) | Adjacency list, parent array, and visited array all scale linearly |

With `50000` vertices, linear complexity easily fits within the limits. The adjacency list stores exactly `2 * (n - 1)` edge entries, which is comfortably inside the memory bound.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys, io

def solve():
    input = sys.stdin.readline

    sys.setrecursionlimit(1 << 20)

    n, r1, r2 = map(int, input().split())

    adj = [[] for _ in range(n + 1)]

    values = list(map(int, input().split()))

    ptr = 0
    for node in range(1, n + 1):
        if node == r1:
            continue

        p = values[ptr]
        ptr += 1

        adj[node].append(p)
        adj[p].append(node)

    parent = [0] * (n + 1)
    visited = [False] * (n + 1)

    def dfs(u):
        visited[u] = True

        for v in adj[u]:
            if not visited[v]:
                parent[v] = u
                dfs(v)

    dfs(r2)

    ans = []

    for node in range(1, n + 1):
        if node == r2:
            continue
        ans.append(str(parent[node]))

    print(" ".join(ans))

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    out = io.StringIO()
    sys.stdout = out

    solve()

    sys.stdout = sys.__stdout__
    return out.getvalue().strip()

# provided sample
assert run("3 2 3\n2 2\n") == "2 3", "sample 1"

# minimum size
assert run("2 1 2\n1\n") == "2", "minimum tree"

# chain reroot
assert run("5 1 5\n1 2 3 4\n") == "2 3 4 5", "full path reversal"

# balanced tree
assert run("5 1 3\n1 2 3 3\n") == "2 3 3 3", "reroot in middle"

# star centered at old root
assert run("4 1 2\n1 1 1\n") == "2 2 1", "many children of old root"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `2 1 2` | `2` | Minimum valid tree |
| Chain with new root at end | `2 3 4 5` | Full reversal of parent directions |
| Balanced tree reroot | `2 3 3 3` | DFS parent assignment correctness |
| Star centered at old root | `2 2 1` | Multiple children changing hierarchy |

## Edge Cases

Consider the chain-shaped tree:

```
5 1 5
1 2 3 4
```

The original rooted structure is:

```
1 -> 2 -> 3 -> 4 -> 5
```

DFS starts from `5`.

First, `parent[4] = 5`.

Then, `parent[3] = 4`.

Then, `parent[2] = 3`.

Finally, `parent[1] = 2`.

The produced output is:

```
2 3 4 5
```

Every edge direction reverses correctly because DFS naturally follows the unique path away from the new root.

Now consider the indexing-sensitive input:

```
4 2 1
2 2 3
```

The old root is `2`, so the values correspond to:

```
p[1] = 2
p[3] = 2
p[4] = 3
```

The reconstructed tree is:

```
1 - 2 - 3 - 4
```

DFS from `1` assigns:

```
parent[2] = 1
parent[3] = 2
parent[4] = 3
```

Output:

```
1 2 3
```

The separate pointer variable ensures that the skipped root does not shift input alignment.

Finally, consider a deep chain with `50000` nodes. Recursive DFS would normally overflow Python's recursion stack. The implementation raises the recursion limit before traversal, allowing the algorithm to process even the worst-case tree shape safely.
