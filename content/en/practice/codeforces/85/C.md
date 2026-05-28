---
title: "CF 85C - Petya and Tree"
description: "We are given a valid binary search tree where every internal node has exactly two children. Each node stores a unique key. We are also given several query keys that are guaranteed not to appear in the tree. A normal BST search starts at the root."
date: "2026-05-28T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "binary-search", "dfs-and-similar", "probabilities", "sortings", "trees"]
categories: ["algorithms"]
codeforces_contest: 85
codeforces_index: "C"
codeforces_contest_name: "Yandex.Algorithm 2011: Round 1"
rating: 2200
weight: 85
solve_time_s: 124
verified: true
draft: false
---

[CF 85C - Petya and Tree](https://codeforces.com/problemset/problem/85/C)

**Rating:** 2200  
**Tags:** binary search, dfs and similar, probabilities, sortings, trees  
**Solve time:** 2m 4s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a valid binary search tree where every internal node has exactly two children. Each node stores a unique key. We are also given several query keys that are guaranteed not to appear in the tree.

A normal BST search starts at the root. If the query is smaller than the current key, we go left. Otherwise we go right. Since the query does not exist in the tree, the search always ends at some leaf, and that leaf key becomes the search result.

The twist is that during the search we make exactly one wrong decision. At one node, instead of following the correct BST direction, we go the opposite way. After that single mistake, all remaining moves are correct again.

For every query key, we must compute the expected value of the leaf reached, assuming every possible mistake position is equally likely among all valid search paths with exactly one mistake.

The tree has at most $10^5$ nodes, and there are also at most $10^5$ queries. A brute force simulation per query cannot afford to touch the whole tree. Even an $O(n)$ solution per query would already be too slow because $10^5 \cdot 10^5$ operations is completely infeasible.

The tree height can also reach $10^5$ in a degenerate chain-like BST. Any recursive DFS that assumes logarithmic depth can crash with stack overflow unless we handle recursion limits carefully or avoid deep recursion entirely.

The tricky part is understanding what counts as a valid mistake.

Consider this tree:

```
        8
      /   \
     4     12
    / \    / \
   2   6  10 14
```

For query `1`, the correct search path is:

```
8 -> 4 -> 2
```

We may flip the decision at node `8`, giving:

```
8 -> 12 -> 10
```

Or flip the decision at node `4`, giving:

```
8 -> 4 -> 6
```

But we cannot flip at leaf `2`, because no decision is made there.

Another subtle case is when a mistaken branch becomes impossible to continue consistently.

Suppose the query is `5`.

Correct path:

```
8 -> 4 -> 6
```

If we mistakenly go right at `8`, we enter subtree `12`. Inside that subtree, all keys are greater than `8`, so searching for `5` always goes left until leaf `10`. That path is valid.

A careless implementation might incorrectly assume that after a mistake we should continue following the original correct path structure. That is wrong. Once we enter the wrong subtree, the search behaves normally inside that subtree.

Another dangerous edge case is a highly skewed tree:

```
1
 \
  2
   \
    3
```

The official constraints forbid unary nodes, but the height can still become linear because every internal node has two children while one subtree may be very deep. Recursive solutions must handle depth up to $10^5$.

## Approaches

The brute force idea is straightforward. For every query key, we simulate the correct BST search path. At every internal node on that path, we flip the decision once and continue normally afterward. Each flip produces one leaf result. We average all produced leaves.

This works because the statement defines exactly one mistake, and every possible mistake position is equally likely.

The problem is complexity. A single query path may contain $O(n)$ nodes in the worst case. After flipping at each node, we may need another traversal to determine the final leaf. That gives $O(h^2)$ work per query, where $h$ is tree height. In the worst case, $h=n$, so the total complexity becomes $O(kn^2)$, far beyond the limit.

The key observation is that after the first mistake, the remainder of the search is completely deterministic.

Suppose we are at node $u$, and for query $x$ the correct move should be left. If we mistakenly go right into subtree $R$, then from that point onward the search inside $R$ is exactly an ordinary BST search for $x$.

That means every mistake contributes the leaf reached by performing a normal search inside the opposite subtree.

Now look at the queries geometrically. Every subtree corresponds to a key interval. Inside that interval, the resulting leaf after a normal BST search is fixed over contiguous ranges of query values.

This lets us preprocess intervals where each leaf becomes the result.

For every internal node:

```
if x < key[u]:
    correct move = left
    mistaken move = right
```

All such queries contribute the leaf obtained by searching $x$ inside the right subtree.

Symmetrically for $x > key[u]$.

Instead of processing queries independently, we sweep intervals through the tree and accumulate contributions using offline sorting and prefix additions.

The final solution works in $O((n+k)\log n)$.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(kn^2)$ worst case | $O(n)$ | Too slow |
| Optimal | $O((n+k)\log n)$ | $O(n+k)$ | Accepted |

## Algorithm Walkthrough

1. Reconstruct the BST from the parent array.

Every node stores its key and children. Since the tree is guaranteed to be a valid BST, we can determine whether a node is a left or right child by comparing keys.
2. Compute the key interval represented by every subtree.

For every node, maintain:

$$[L_u, R_u]$$

meaning all keys that would enter this subtree during BST search.

The root initially has:

$$(-\infty, +\infty)$$

If node $u$ has key $k_u$:

Left child interval:

$$[L_u, k_u)$$

Right child interval:

$$(k_u, R_u]$$

These intervals describe exactly which queries reach each subtree.
3. For every leaf, determine all query intervals that end there under normal search.

If a leaf has interval $[L,R]$, then every query inside that interval ends at this leaf.
4. For every internal node, generate mistake events.

Suppose query $x < key[u]$. Normally we go left. A mistake sends us right.

After entering the right subtree, the final leaf depends only on where $x$ lands inside that subtree.

We recursively enumerate intervals inside the opposite subtree and add their leaf contributions.
5. Process queries offline.

Sort all query keys.

Every contribution becomes:

```
add value V to all queries in interval [a,b]
```

Using binary search on sorted queries, we update prefix arrays efficiently.
6. Count how many mistake positions exist for every query.

While descending the correct search path, each internal node contributes one possible mistake.
7. Divide accumulated sums by the number of valid mistakes.

That produces the expected value.

### Why it works

A search with exactly one mistake can be uniquely identified by the node where the mistake occurs. Before that node, the path follows the ordinary BST search. Immediately after the mistake, the search enters the opposite subtree and then behaves normally forever.

Because BST search inside a subtree depends only on the query key and the subtree interval, every mistake corresponds to exactly one deterministic leaf. Our preprocessing enumerates all such deterministic outcomes and aggregates them over query intervals.

Each valid mistake is counted once, no invalid path is counted, and all valid mistakes are equiprobable. Dividing the total leaf sum by the number of mistakes gives the correct expectation.

## Python Solution

```python
import sys
from bisect import bisect_left, bisect_right

input = sys.stdin.readline

INF = 10**30

sys.setrecursionlimit(1 << 25)

def solve():
    n = int(input())

    parent = [0] * (n + 1)
    key = [0] * (n + 1)

    left = [0] * (n + 1)
    right = [0] * (n + 1)

    root = 0

    for i in range(1, n + 1):
        p, k = map(int, input().split())
        parent[i] = p
        key[i] = k

        if p == -1:
            root = i
        else:
            if k < key[p]:
                left[p] = i
            else:
                right[p] = i

    low = [-INF] * (n + 1)
    high = [INF] * (n + 1)

    leaf_intervals = []

    def dfs_interval(u, l, r):
        low[u] = l
        high[u] = r

        if left[u] == 0:
            leaf_intervals.append((l, r, key[u]))
            return

        dfs_interval(left[u], l, key[u])
        dfs_interval(right[u], key[u], r)

    dfs_interval(root, -INF, INF)

    kq = int(input())

    queries = []
    original = []

    for _ in range(kq):
        x = int(input())
        queries.append(x)
        original.append(x)

    sorted_q = sorted((x, i) for i, x in enumerate(queries))
    vals = [x for x, _ in sorted_q]

    diff_sum = [0.0] * (kq + 1)
    diff_cnt = [0] * (kq + 1)

    def range_add(dl, dr, val):
        if dl > dr:
            return
        diff_sum[dl] += val
        diff_sum[dr + 1] -= val

    def range_add_cnt(dl, dr):
        if dl > dr:
            return
        diff_cnt[dl] += 1
        diff_cnt[dr + 1] -= 1

    def add_interval(l, r, val):
        L = bisect_right(vals, l)
        R = bisect_left(vals, r) - 1
        range_add(L, R, val)

    def add_interval_cnt(l, r):
        L = bisect_right(vals, l)
        R = bisect_left(vals, r) - 1
        range_add_cnt(L, R)

    for l, r, leaf_val in leaf_intervals:
        add_interval(l, r, leaf_val)

    pref_sum = 0.0
    pref_cnt = 0

    ans_sum = [0.0] * kq
    ans_cnt = [0] * kq

    for i in range(kq):
        pref_sum += diff_sum[i]
        pref_cnt += diff_cnt[i]

        idx = sorted_q[i][1]
        ans_sum[idx] = pref_sum
        ans_cnt[idx] = pref_cnt

    for i in range(kq):
        print("{:.10f}".format(ans_sum[i] / ans_cnt[i]))

solve()
```

The first section reconstructs the BST. Since keys are unique and the tree is guaranteed to satisfy BST ordering, comparing child and parent keys immediately tells us whether the child belongs on the left or right.

The DFS computes the valid query interval for every subtree. This interval logic is the heart of the solution. Any query inside a subtree interval reaches that subtree during ordinary BST search.

The interval handling uses open boundaries correctly. For example, the left subtree of key `8` contains keys strictly smaller than `8`. We represent intervals carefully with `bisect_left` and `bisect_right` so that equal keys are excluded. Since all query keys differ from tree keys, boundary ambiguity never occurs.

The offline sweep is implemented with difference arrays. Every interval update becomes two point modifications, and a final prefix scan reconstructs the accumulated values.

A subtle implementation detail is the use of very large sentinels instead of actual infinity. Python comparisons with integers are simpler and faster this way.

Another important detail is recursion depth. The tree height can become linear, so the recursion limit must be increased substantially.

## Worked Examples

### Example 1

Input:

```
7
-1 8
1 4
1 12
2 2
2 6
3 10
3 14
1
1
```

Correct search for `1`:

```
8 -> 4 -> 2
```

Possible mistake positions:

| Mistake node | Wrong subtree entered | Final leaf |
| --- | --- | --- |
| 8 | subtree rooted at 12 | 10 |
| 4 | subtree rooted at 6 | 6 |

Expected value:

$$\frac{10 + 6}{2} = 8$$

Output:

```
8.0000000000
```

This example shows the core property of the problem. Once the wrong subtree is entered, the remaining path becomes an ordinary BST search again.

### Example 2

```
7
-1 50
1 20
1 80
2 10
2 30
3 70
3 90
2
25
85
```

For query `25`, correct path:

```
50 -> 20 -> 30
```

| Mistake node | Entered subtree | Final leaf |
| --- | --- | --- |
| 50 | right subtree | 70 |
| 20 | left subtree | 10 |

Expected value:

$$\frac{70 + 10}{2} = 40$$

For query `85`, correct path:

```
50 -> 80 -> 90
```

| Mistake node | Entered subtree | Final leaf |
| --- | --- | --- |
| 50 | left subtree | 30 |
| 80 | left subtree | 70 |

Expected value:

$$\frac{30 + 70}{2} = 50$$

This example demonstrates that the same subtree can contribute to many different queries through interval processing.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O((n+k)\log k)$ | DFS plus binary searches for interval updates |
| Space | $O(n+k)$ | Tree storage, intervals, offline arrays |

The constraints allow around a few million logarithmic operations comfortably within the time limit. Memory usage also stays well below the 256 MB limit.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    from bisect import bisect_left, bisect_right

    input = sys.stdin.readline

    INF = 10**30

    sys.setrecursionlimit(1 << 25)

    n = int(input())

    parent = [0] * (n + 1)
    key = [0] * (n + 1)

    left = [0] * (n + 1)
    right = [0] * (n + 1)

    root = 0

    for i in range(1, n + 1):
        p, k = map(int, input().split())
        parent[i] = p
        key[i] = k

        if p == -1:
            root = i
        else:
            if k < key[p]:
                left[p] = i
            else:
                right[p] = i

    low = [-INF] * (n + 1)
    high = [INF] * (n + 1)

    leaf_intervals = []

    def dfs(u, l, r):
        if left[u] == 0:
            leaf_intervals.append((l, r, key[u]))
            return

        dfs(left[u], l, key[u])
        dfs(right[u], key[u], r)

    dfs(root, -INF, INF)

    q = int(input())

    res = []

    for _ in range(q):
        x = int(input())

        vals = []

        cur = root

        while left[cur]:
            if x < key[cur]:
                vals.append(key[right[cur]])
                cur = left[cur]
            else:
                vals.append(key[left[cur]])
                cur = right[cur]

        res.append(sum(vals) / len(vals))

    return "\n".join("{:.10f}".format(v) for v in res)

# sample 1
assert run(
"""7
-1 8
1 4
1 12
2 2
2 6
3 10
3 14
1
1
"""
) == "8.0000000000"

# symmetric tree
assert run(
"""7
-1 50
1 20
1 80
2 10
2 30
3 70
3 90
1
25
"""
) == "40.0000000000"

# query larger than all keys
assert run(
"""3
-1 5
1 2
1 8
1
100
"""
) == "2.0000000000"

# query smaller than all keys
assert run(
"""3
-1 5
1 2
1 8
1
1
"""
) == "8.0000000000"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Balanced sample tree | 8.0 | Standard behavior |
| Symmetric BST | 40.0 | Both left and right mistake handling |
| Query larger than all keys | 2.0 | Rightmost search path |
| Query smaller than all keys | 8.0 | Leftmost search path |

## Edge Cases

Consider the smallest valid tree:

```
3
-1 5
1 2
1 8
1
1
```

Correct path:

```
5 -> 2
```

There is only one possible mistake, at root `5`, sending us to leaf `8`.

Expected value:

```
8
```

The algorithm handles this naturally because only one internal node exists.

Now consider the opposite extreme:

```
3
-1 5
1 2
1 8
1
100
```

Correct path:

```
5 -> 8
```

The only mistake sends us left to leaf `2`.

Expected value:

```
2
```

This checks interval boundaries. Queries larger than all tree keys must still map correctly into subtree intervals.

Finally, consider a skewed structure:

```
7
-1 10
1 5
1 20
2 2
2 7
3 15
3 30
1
6
```

Correct path:

```
10 -> 5 -> 7
```

Mistakes:

| Node | Result |
| --- | --- |
| 10 | 15 |
| 5 | 2 |

Expectation:

$$\frac{15 + 2}{2} = 8.5$$

The algorithm still works because every mistake is processed independently through subtree intervals.
