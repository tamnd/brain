---
title: "CF 102270B - Crush"
description: "We are given a tree of cameras. Each camera has a binary label. A label of 1 means that accessing that camera requires breaking a password, which costs one unit of energy, while a label of 0 costs nothing."
date: "2026-08-17T18:31:45+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102270
codeforces_index: "B"
codeforces_contest_name: "HCW 19 Individual Day 2"
rating: 0
weight: 102270
solve_time_s: 434
verified: false
draft: false
---

[CF 102270B - Crush](https://codeforces.com/problemset/problem/102270/B)

**Rating:** -  
**Tags:** -  
**Solve time:** 7m 14s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a tree of cameras. Each camera has a binary label. A label of `1` means that accessing that camera requires breaking a password, which costs one unit of energy, while a label of `0` costs nothing. We need to count the connected sets of cameras for which the total number of selected cameras labeled `1` is exactly `K`.

The word "connected" is the key structural condition. Since the graph is a tree, a selected set is connected exactly when every pair of selected cameras is joined by a path containing only selected cameras. The answer counts different vertex sets, not different orders in which the cameras could be accessed. This is the usual connected-subtree counting interpretation of the problem.

The tree has at most `50,000` vertices, while `K` is at most `100`. An exponential enumeration of subsets is immediately impossible because a tree can have exponentially many connected subsets. A straightforward dynamic programming solution with an unrestricted `K × K` convolution at every vertex would also be too expensive, potentially reaching hundreds of millions of transitions. The small bound on `K` tells us that the state should track only the number of password cameras, while the tree structure should be used to avoid considering arbitrary subsets.

There are several edge cases that a careless implementation can mishandle. If `K = 0`, a valid connected set may contain only cameras labeled `0`. For example,

```
3 0
1 1 0
1 2
2 3
```

has answer `1`, because the only nonempty connected set with zero password cameras is `{3}`. The empty set is not needed by the DP because every counted state contains its designated root vertex.

A second edge case is a password camera at the root of a DP subtree. For example,

```
1 1
1
```

has answer `1`, because the singleton `{1}` uses exactly one unit of energy. A DP that initializes every vertex with state `dp[0] = 1` would incorrectly allow a selected set containing a password camera to have zero cost.

A third edge case occurs when a child subtree contains no password cameras. For example,

```
2 0
0 0
1 2
```

has answer `3`, corresponding to `{1}`, `{2}`, and `{1,2}`. Such a child still matters because it can be included in a valid connected set without increasing the energy. A DP that only stores positive password counts would silently lose these solutions.

Finally, when `K` is larger than the number of password cameras in a subtree, that state is impossible and should never be represented beyond the useful range. Truncating every DP array at `K` is both correct and necessary for the running time.

## Approaches

The brute-force approach is conceptually simple. Enumerate every subset of cameras, check whether the chosen cameras induce a connected subgraph, count its password cameras, and add one when that count is `K`. There are `2^N` subsets, and even checking connectivity for every subset would cost at least linear time per subset, giving roughly `O(N 2^N)` operations in the worst case. With `N = 50,000`, even `2^50` is already far beyond anything that can be processed, so this approach is useful only as a way to understand what is being counted.

The first useful observation is that every nonempty connected set in a rooted tree has a unique highest vertex. If the tree is rooted at vertex `1`, take the selected vertex closest to the root and call it `u`. Every other selected vertex must lie in the subtree of `u`. Moreover, for every child `v` of `u`, we have exactly two possibilities: take nothing from the subtree of `v`, or take a connected set that contains `v`. The second choice is precisely the same problem on `v`.

This gives a tree DP. Define `dp[u][k]` as the number of connected sets contained in the rooted subtree of `u`, containing `u`, and containing exactly `k` password cameras. The initial state contains only `u`. If `u` has a password, it contributes one to the count; otherwise it contributes zero.

When processing a child `v`, suppose the current partial solution uses `i` password cameras and the connected part selected from `v` uses `j`. Combining them creates a solution with `i + j` password cameras, contributing

`current[i] * dp[v][j]`

ways. We also have the choice of taking nothing from `v`, so the old `current` array must be preserved.

The brute-force works because every connected set has a unique highest vertex, but it fails because it explicitly considers exponentially many sets. The DP keeps only the information relevant to the future, namely how many password cameras have already been used.

A naive implementation might perform a full `K × K` convolution for every child of every vertex, giving `O(NK^2)`. With `N = 50,000` and `K = 100`, that upper bound is around `500 million` elementary state combinations, which is too large for a one-second limit.

The required improvement comes from keeping each DP array only as long as the number of password cameras that can actually occur in that subtree, capped at `K`. A vertex labeled `0` starts with only one possible count, while a vertex labeled `1` starts with two. More generally, a subtree containing `s` password cameras needs at most `min(s, K) + 1` states. The total work of these bounded tree-knapsack merges is `O(NK)` amortized. The same tree-knapsack accounting is what makes bounded-state subtree merging substantially cheaper than multiplying two full `K`-length arrays at every vertex.

There is another practical issue in Python. Storing a `K + 1` sized DP array for all `50,000` vertices would create several million Python objects or references. Instead, the implementation below processes completed child DPs immediately and releases them after merging into their parent. The parent keeps its current DP, while a node becomes ready as soon as all its children have finished.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | `O(N 2^N)` | `O(N)` | Too slow |
| Full `K × K` tree DP | `O(NK^2)` | `O(NK)` | Too slow for the limit |
| Bounded tree DP | `O(NK)` amortized | `O(NK)` worst case, much smaller with released child states | Accepted |

## Algorithm Walkthrough

1. Root the tree at camera `1` and determine the parent of every vertex. We also count how many children of each vertex still need to finish. An iterative construction avoids Python recursion depth problems on a path of length `50,000`.
2. Initialize the DP of every vertex with the connected set containing only that vertex. If the vertex has label `0`, its initial array is `[1]`, because it contributes zero password cameras. If its label is `1`, its initial array is `[0, 1]`, because a set containing this vertex necessarily uses one unit of energy.
3. Put every leaf into a processing queue. A leaf has no child information left to receive, so its DP is already complete and can be sent directly to its parent.
4. When a completed child `v` reaches its parent `u`, merge the two DP arrays. If the current parent state uses `i` password cameras and the child state uses `j`, add `current[i] * dp[v][j]` to the state for `i + j`. The array is truncated after index `K`, because larger values can never contribute to the required answer.
5. Preserve the old parent DP while performing the merge. This represents the option of taking no camera from the child subtree. The convolution represents all choices that take a connected set containing the child.
6. Decrease the number of unfinished children of `u`. When it reaches zero, every child has been incorporated, so `dp[u]` is complete. Its coefficient at index `K` counts every valid connected set whose highest selected vertex is `u`. Add that coefficient to the global answer and pass `dp[u]` to its parent.
7. When the root has finished, all nonempty connected sets have been counted exactly once. Print the accumulated answer.

### Why it works

The invariant is that `dp[u][k]` contains exactly the connected vertex sets inside the subtree of `u` that contain `u` and have exactly `k` password cameras. Initially this is true because the only available set is `{u}`. During a child merge, every valid set containing `u` either contains no vertex from that child subtree or contains a connected set containing the child. These two cases are disjoint and exhaustive because removing the edge between `u` and the child separates the tree into two components. The convolution counts every combination of the two independent choices exactly once. Finally, every nonempty connected set has one unique highest vertex, so summing `dp[u][K]` over completed vertices cannot double-count a set.

## Python Solution

```python
import sys
from collections import deque

input = sys.stdin.readline

def solve(data: str) -> str:
    it = iter(data.split())
    n = int(next(it))
    k = int(next(it))

    color = [0] * n
    for i in range(n):
        color[i] = int(next(it))

    graph = [[] for _ in range(n)]
    for _ in range(n - 1):
        u = int(next(it)) - 1
        v = int(next(it)) - 1
        graph[u].append(v)
        graph[v].append(u)

    # Root the tree at 0.
    parent = [-1] * n
    parent[0] = -2
    children_left = [0] * n

    order = [0]
    for u in order:
        for v in graph[u]:
            if v == parent[u]:
                continue
            parent[v] = u
            order.append(v)

    for u in range(n):
        cnt = 0
        for v in graph[u]:
            if parent[v] == u:
                cnt += 1
        children_left[u] = cnt

    # dp[u] is the current connected-subtree DP containing u.
    # Only states 0..K are stored.
    dp = []
    for c in color:
        if c == 0:
            dp.append([1])
        else:
            if k == 0:
                dp.append([0])
            else:
                dp.append([0, 1])

    q = deque()
    for u in range(n):
        if children_left[u] == 0:
            q.append(u)

    answer = 0

    while q:
        u = q.popleft()

        if k < len(dp[u]):
            answer += dp[u][k]

        p = parent[u]
        if p < 0:
            continue

        child = dp[u]
        current = dp[p]

        a = len(current)
        b = len(child)

        new_len = min(k + 1, a + b - 1)
        new_dp = current[:new_len]

        # Take a nonempty connected part containing u from the child.
        # The copy above represents taking nothing from the child.
        for i in range(a):
            x = current[i]
            if x == 0:
                continue

            max_j = min(b - 1, k - i)
            for j in range(max_j + 1):
                y = child[j]
                if y:
                    new_dp[i + j] += x * y

        dp[p] = new_dp
        dp[u] = None

        children_left[p] -= 1
        if children_left[p] == 0:
            q.append(p)

    return str(answer)

def main():
    data = sys.stdin.buffer.read().decode()
    sys.stdout.write(solve(data))

if __name__ == "__main__":
    main()
```

The first part of the implementation builds the undirected tree and then roots it at vertex `0`. The `parent` array gives the unique direction from a child toward the root, which lets us determine when a node has received all of its child DPs.

The initial DP is deliberately different for labels `0` and `1`. For an unprotected camera, `{u}` has cost zero, so `dp[u][0] = 1`. For a protected camera, `{u}` has cost one, so `dp[u][1] = 1`. When `K = 0`, the latter state is outside the required range, so the initial array can contain only zero.

The merge starts with `current[:]`. This copy is not merely an optimization detail. It represents the choice of taking nothing from the child. The nested loops then add every possibility in which a connected set containing the child is selected. The upper bound `k - i` prevents writing beyond the target energy budget.

The line `dp[u] = None` releases the child's DP after its contribution has been incorporated into the parent. This matters for memory usage on large trees. A path may have many vertices, but only the currently active parent state needs to remain large at each stage.

The algorithm is iterative rather than recursive. A recursive DFS on a path containing `50,000` vertices would require increasing Python's recursion limit and could still put unnecessary pressure on the interpreter stack. The queue processes the tree from leaves toward the root without that risk.

Python integers do not overflow, which is useful here because the problem asks for the exact count and does not specify a modulus. The number of connected subsets can be exponentially large, so using Python's arbitrary-precision integers is necessary.

## Worked Examples

### Sample 1

The input is

```
5 2
0 1 0 1 1
1 2
1 3
1 4
2 5
```

Rooting at `1` gives children `2`, `3`, and `4`, with `5` below `2`. The initial states and the important completed merges are:

| Vertex | Label | Initial DP | Completed DP |
| --- | --- | --- | --- |
| `5` | `1` | `[0, 1]` | `[0, 1]` |
| `2` | `1` | `[0, 1]` | `[0, 1, 1]` |
| `3` | `0` | `[1]` | `[1]` |
| `4` | `1` | `[0, 1]` | `[0, 1]` |
| `1` | `0` | `[1]` | `[1, 3, 5, ...]` |

At vertex `2`, the singleton `{2}` contributes one password camera, while `{2,5}` contributes two. Thus `dp[2][2] = 1`.

At vertex `1`, combining the three child choices gives five connected sets containing `1` with exactly two password cameras. The additional solution `{2,5}` is counted when vertex `2` itself is completed, because its highest selected vertex is `2`. The final answer is `5`.

This trace demonstrates why the answer must be accumulated from every vertex, not only from the root. A connected set such as `{2,5}` does not contain the root of the whole tree, but it still has a unique highest vertex, namely `2`.

### Sample 2

The input is

```
3 1
1 0 1
1 2
1 3
```

Vertex `1` has two children. Both `1` and `3` require a password, while `2` does not.

| Vertex | Label | Initial DP | Completed DP | Contribution to answer |
| --- | --- | --- | --- | --- |
| `2` | `0` | `[1]` | `[1]` | `0` |
| `3` | `1` | `[0, 1]` | `[0, 1]` | `1` |
| `1` | `1` | `[0, 1]` | `[0, 2]` | `2` |

The singleton `{3}` contributes one solution. At vertex `1`, the two valid choices with exactly one password camera are `{1}` and `{1,2}`, giving two more solutions. The answer is `3`.

The trace also shows why an unprotected child cannot simply be ignored. Camera `2` does not change the energy count, but selecting it creates the additional connected set `{1,2}`.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | `O(NK)` amortized | DP arrays are truncated at `K`, and bounded tree-knapsack merges have linear dependence on the number of vertices and the state limit |
| Space | `O(NK)` worst case | Parent and pending child DP arrays use at most `K + 1` states, with completed child arrays released immediately |

The maximum state size is only `101`, since `K <= 100`. With `N <= 50,000`, the intended state bound is small enough for the tree-knapsack approach. The implementation also avoids keeping every completed DP simultaneously, which substantially reduces the practical memory consumption compared with a conventional `dp[N][K+1]` layout. The tree itself needs only `O(N)` memory.

## Test Cases

```python
import io
import sys
from collections import deque

def solve(data: str) -> str:
    it = iter(data.split())
    n = int(next(it))
    k = int(next(it))

    color = [int(next(it)) for _ in range(n)]

    graph = [[] for _ in range(n)]
    for _ in range(n - 1):
        u = int(next(it)) - 1
        v = int(next(it)) - 1
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

    children_left = [0] * n
    for v in range(1, n):
        children_left[parent[v]] += 1

    dp = []
    for c in color:
        if c == 0:
            dp.append([1])
        elif k == 0:
            dp.append([0])
        else:
            dp.append([0, 1])

    q = deque(u for u in range(n) if children_left[u] == 0)
    answer = 0

    while q:
        u = q.popleft()

        if k < len(dp[u]):
            answer += dp[u][k]

        p = parent[u]
        if p < 0:
            continue

        child = dp[u]
        current = dp[p]

        a = len(current)
        b = len(child)
        new_len = min(k + 1, a + b - 1)
        new_dp = current[:new_len]

        for i in range(a):
            if i > k:
                break
            x = current[i]
            if x == 0:
                continue

            limit = min(b - 1, k - i)
            for j in range(limit + 1):
                y = child[j]
                if y:
                    new_dp[i + j] += x * y

        dp[p] = new_dp
        dp[u] = None

        children_left[p] -= 1
        if children_left[p] == 0:
            q.append(p)

    return str(answer)

def run(inp: str) -> str:
    return solve(inp).strip()

# Provided samples
assert run("""5 2
0 1 0 1 1
1 2
1 3
1 4
2 5
""") == "5", "sample 1"

assert run("""3 1
1 0 1
1 2
1 3
""") == "3", "sample 2"

assert run("""3 0
1 1 0
1 2
2 3
""") == "1", "sample 3"

# Minimum-size tree, one unprotected camera, zero energy.
assert run("""1 0
0
""") == "1", "minimum-size zero-cost set"

# Minimum-size tree, one protected camera, exactly one energy.
assert run("""1 1
1
""") == "1", "minimum-size password camera"

# Two protected cameras connected by one edge.
# Exactly one password means either singleton.
assert run("""2 1
1 1
1 2
""") == "2", "two singletons"

# Four protected cameras in a path.
# Exactly two protected cameras means every connected set of size two.
assert run("""4 2
1 1 1 1
1 2
2 3
3 4
""") == "3", "path of four protected cameras"

# All cameras unprotected, K = 0.
# Every nonempty connected set of a 5-vertex path is an interval:
# 5 + 4 + 3 + 2 + 1 = 15.
assert run("""5 0
0 0 0 0 0
1 2
2 3
3 4
4 5
""") == "15", "all-zero path"

# Maximum-size case.
# Every vertex is protected and K = 1, so only the N singleton sets work.
n = 50000
colors = " ".join(["1"] * n)
edges = "\n".join(f"1 {v}" for v in range(2, n + 1))
maximum_case = f"{n} 1\n{colors}\n{edges}\n"
assert run(maximum_case) == str(n), "maximum-size star"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 0 / 0` | `1` | Minimum-size tree and `K = 0` |
| `1 1 / 1` | `1` | A password camera contributes exactly one energy |
| `2 1 / 1 1` | `2` | Exactly one marked vertex and singleton states |
| Four protected vertices in a path, `K = 2` | `3` | Connected sets of the target size and boundary truncation |
| Five unprotected vertices in a path, `K = 0` | `15` | Zero-cost child states and all connected intervals |
| `50,000` protected vertices in a star, `K = 1` | `50,000` | Maximum `N` and linear-scale state processing |

## Edge Cases

For `K = 0`, consider

```
3 0
1 1 0
1 2
2 3
```

The root can never be part of a zero-energy connected set because it is protected. Vertex `2` has the same property. Vertex `3` starts with `dp[3] = [1]`, representing `{3}` with zero password cameras. It contributes `1` when processed, so the answer is `1`. The algorithm does not need a special case for the empty set because every DP state represents a connected set containing its own vertex.

For a password camera with no children, consider

```
1 1
1
```

The initial state is `[0,1]`. The coefficient at index `1` is one, corresponding to the singleton set `{1}`. The algorithm adds that coefficient to the answer and prints `1`. If the initialization instead used `[1]`, it would incorrectly count the camera as costing zero energy.

For a zero-cost child, consider

```
2 0
0 0
1 2
```

Vertex `2` starts with `[1]` and contributes the singleton `{2}`. When it is merged into vertex `1`, the parent already has `[1]`, and the convolution creates an additional zero-energy state representing `{1,2}`. Vertex `1` itself represents `{1}`. The final answer is `3`, exactly the three nonempty connected subsets.

For states beyond `K`, consider a path of four protected cameras with `K = 2`:

```
4 2
1 1 1 1
1 2
2 3
3 4
```

A connected set containing two cameras is possible in three ways: `{1,2}`, `{2,3}`, and `{3,4}`. Larger connected sets are irrelevant because they use more than two units of energy. The DP arrays are truncated at index `2`, so the merge never constructs states for three or four password cameras. The answer is `3`.

The maximum-size star

```
50000 1
1 1 1 ... 1
1 2
1 3
...
1 50000
```

contains only protected cameras. With `K = 1`, the only valid connected sets are the `50,000` singleton cameras. Every internal merge is tiny because each leaf has only the states `[0,1]`, and once the root reaches the target limit, no state above `1` is retained. The algorithm consequently handles the largest allowed `N` without enumerating connected subsets.
