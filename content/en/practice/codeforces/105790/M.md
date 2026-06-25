---
title: "CF 105790M - Giant Worms"
description: "The multiverse forms a rooted directed tree with root universe 1. Every edge points from a universe with more stars to a universe with fewer stars."
date: "2026-06-26T03:51:30+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105790
codeforces_index: "M"
codeforces_contest_name: "UDESC Selection Contest 2024-1"
rating: 0
weight: 105790
solve_time_s: 51
verified: true
draft: false
---

[CF 105790M - Giant Worms](https://codeforces.com/problemset/problem/105790/M)

**Rating:** -  
**Tags:** -  
**Solve time:** 51s  
**Verified:** yes  

## Solution
## Problem Understanding

The multiverse forms a rooted directed tree with root universe `1`. Every edge points from a universe with more stars to a universe with fewer stars. Because star counts strictly decrease along every root-to-leaf path, among all universes that can reach a given set of nodes, the one with the smallest number of stars is simply the deepest common ancestor of those nodes. In tree terminology, that is their Lowest Common Ancestor (LCA).

For each query we are given an ordered list of distinct universes

$$a_1,a_2,\dots,a_K$$

and we must compute

$$\sum_{1 \le i \le j \le K} f(i,j)$$

where $f(i,j)$ is the universe identifier of the deepest node that can reach every universe in the contiguous segment $a_i,\dots,a_j$. Since that node is exactly the LCA of all nodes in the segment, the task becomes:

$$\sum_{1 \le i \le j \le K}
\text{LCA}(a_i,a_{i+1},\dots,a_j)$$

using the universe number itself as the value being added.

The tree contains up to $10^5$ nodes, there are up to $10^5$ queries, and the sum of all query lengths is at most $3 \cdot 10^5$. A solution that examines every subarray independently would require $O(K^2)$ work per query, which is far beyond what fits inside the limits.

A subtle observation is that the node labels are not depths or star counts. The answer adds the universe identifiers returned by the LCA operation.

Consider the query:

```
2 4 5
```

in the sample tree where both 4 and 5 are children of 3.

The intervals are:

```
[4] -> 4
[5] -> 5
[4,5] -> 3
```

The answer is:

```
4 + 5 + 3 = 12
```

A careless implementation that counts LCAs instead of summing their identifiers would produce the wrong result.

Another edge case is a query of length one:

```
1 7
```

The only interval is `[7]`, and the LCA of a single node is the node itself. The answer must be `7`, not its parent or the root.

## Approaches

The brute-force idea is straightforward. For every interval $[i,j]$, compute the LCA of all nodes inside it and add the result to the answer.

One way to do this is to extend intervals from each starting position. If we keep the current LCA while moving the right endpoint, then every interval can be processed in $O(\log N)$ using binary lifting. The total complexity becomes $O(K^2 \log N)$. With $K$ as large as $10^5$, this is completely infeasible.

The key observation is that LCAs collapse very quickly.

Fix a position $r$. Look at all subarrays ending at $r$:

```
[a_r]
[a_{r-1}, a_r]
[a_{r-2}, a_r]
...
```

As we extend the interval to the left, the LCA can only move upward in the tree. Once an LCA changes, it becomes a strict ancestor of the previous one.

Along any root-to-leaf path there are only $O(\log N)$ distinct ancestors that can appear after repeated LCA merges. This is the same property used in classic "distinct gcds of subarrays" problems. The set of distinct LCAs for subarrays ending at a fixed position remains small.

Suppose we already know all distinct LCAs of subarrays ending at position $r-1$. For a new node $a_r$, every old LCA value $v$ becomes:

$$\text{LCA}(v,a_r)$$

for the extended subarray. We also add the new one-element subarray whose LCA is $a_r$.

Many resulting values are equal, so we merge equal LCAs and keep only their counts. The number of distinct LCAs remains small, giving an efficient solution.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(K^2 \log N)$ | $O(1)$ | Too slow |
| Optimal | $O(K \log^2 N)$ per query | $O(\log N)$ per query | Accepted |

The total complexity over all queries is $O((\sum K)\log^2 N)$, which easily fits because $\sum K \le 3 \cdot 10^5$.

## Algorithm Walkthrough

### Preprocessing

1. Root the tree at node `1`.
2. Run a DFS to compute depths and the binary lifting table `up[v][j]`, where `up[v][j]` is the $2^j$-th ancestor of `v`.
3. Implement an `lca(u,v)` function using binary lifting.

### Processing one query

1. Maintain a list `cur` containing pairs `(lca_value, count)`.

The meaning is: among all subarrays ending at the previous position, exactly `count` of them have LCA equal to `lca_value`.
2. For the next node `x`, start a new list `nxt`.
3. Insert `(x,1)` into `nxt`.

This represents the one-element subarray `[x]`.
4. For every pair `(v,c)` in `cur`, compute `w = lca(v,x)`.

Every subarray represented by `(v,c)` becomes a longer subarray ending at `x`, and its new LCA is `w`.
5. If the last pair already stored in `nxt` has LCA `w`, add `c` to its count. Otherwise append `(w,c)`.

Consecutive equal LCAs are merged so that only distinct values remain.
6. Replace `cur` with `nxt`.
7. Add

$$\sum (\text{lca\_value} \times \text{count})$$

over all pairs in `cur` to the query answer.
8. Repeat for every node of the query sequence.

### Why it works

After processing position `r`, the list `cur` represents all subarrays ending at `r`, grouped by their LCA. Every subarray ending at `r` is either the one-element interval `[a_r]` or an extension of a subarray ending at `r-1`.

For an extended interval, the new LCA is exactly

$$\text{LCA}(\text{old LCA}, a_r)$$

because the LCA of a set of nodes can be accumulated incrementally through repeated pairwise LCA operations.

Thus every subarray ending at `r` contributes to exactly one group in `cur`, and every group corresponds to actual subarrays. Summing `lca_value × count` gives the total contribution of all intervals ending at `r`. Summing over all positions counts every interval exactly once.

## Python Solution

```python
import sys
input = sys.stdin.readline

def main():
    n, q = map(int, input().split())

    g = [[] for _ in range(n + 1)]
    for _ in range(n - 1):
        u, v = map(int, input().split())
        g[u].append(v)
        g[v].append(u)

    LOG = (n + 1).bit_length()

    depth = [0] * (n + 1)
    up = [[0] * (n + 1) for _ in range(LOG)]

    stack = [1]
    parent = [0] * (n + 1)
    parent[1] = 1

    order = [1]
    while stack:
        v = stack.pop()
        for to in g[v]:
            if to == parent[v]:
                continue
            parent[to] = v
            depth[to] = depth[v] + 1
            stack.append(to)
            order.append(to)

    for v in range(1, n + 1):
        up[0][v] = parent[v]

    for j in range(1, LOG):
        prev = up[j - 1]
        cur = up[j]
        for v in range(1, n + 1):
            cur[v] = prev[prev[v]]

    def lca(a, b):
        if depth[a] < depth[b]:
            a, b = b, a

        diff = depth[a] - depth[b]
        bit = 0
        while diff:
            if diff & 1:
                a = up[bit][a]
            diff >>= 1
            bit += 1

        if a == b:
            return a

        for j in range(LOG - 1, -1, -1):
            if up[j][a] != up[j][b]:
                a = up[j][a]
                b = up[j][b]

        return up[0][a]

    answers = []

    for _ in range(q):
        arr = list(map(int, input().split()))
        k = arr[0]
        nodes = arr[1:]

        cur = []
        ans = 0

        for x in nodes:
            nxt = [(x, 1)]

            for v, cnt in cur:
                w = lca(v, x)

                if nxt[-1][0] == w:
                    nxt[-1] = (w, nxt[-1][1] + cnt)
                else:
                    nxt.append((w, cnt))

            cur = nxt

            for v, cnt in cur:
                ans += v * cnt

        answers.append(str(ans))

    sys.stdout.write("\n".join(answers))

if __name__ == "__main__":
    main()
```

The preprocessing builds the binary lifting table once for the entire tree. Every LCA query then runs in $O(\log N)$.

The query processing keeps only distinct LCAs for subarrays ending at the current position. When extending all previous subarrays by a new node, several LCAs often collapse into the same ancestor. Merging adjacent equal results is crucial, otherwise the list could grow to linear size.

The answer uses the universe identifier returned by the LCA operation. Since there can be $O(K^2)$ intervals, the final sum should be stored in a 64-bit integer. Python integers handle this automatically.

## Worked Examples

### Example 1

Tree:

```
1
├─2
└─3
  ├─4
  └─5
```

Query:

```
2 4 5
```

| Position | Node | cur after processing | Contribution |
| --- | --- | --- | --- |
| 1 | 4 | (4,1) | 4 |
| 2 | 5 | (5,1), (3,1) | 8 |

Total:

```
4 + 8 = 12
```

The two groups at position 2 correspond to intervals `[5]` and `[4,5]`.

### Example 2

Star-shaped tree:

```
1
├─2
├─3
└─4
```

Query:

```
3 2 3 4
```

| Position | Node | cur after processing | Contribution |
| --- | --- | --- | --- |
| 1 | 2 | (2,1) | 2 |
| 2 | 3 | (3,1), (1,1) | 4 |
| 3 | 4 | (4,1), (1,2) | 6 |

Answer:

```
2 + 4 + 6 = 12
```

This example shows how several intervals can share the same LCA and be represented by a single `(value,count)` pair.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(N \log N + (\sum K)\log^2 N)$ | Preprocessing plus query processing |
| Space | $O(N \log N)$ | Binary lifting table |

The preprocessing cost is paid once. Since the total query length is at most $3 \cdot 10^5$, the overall running time comfortably fits the limits.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    out = io.StringIO()

    import sys as _sys
    old_stdout = _sys.stdout
    _sys.stdout = out

    try:
        main()
    finally:
        _sys.stdout = old_stdout

    return out.getvalue().strip()

# sample 1
assert run(
"""5 2
1 2
1 3
3 4
3 5
1 2
2 4 5
"""
) == "2\n12"

# sample 2
assert run(
"""4 1
1 2
1 3
1 4
3 2 3 4
"""
) == "12"

# sample 3
assert run(
"""1 1
1 1
"""
) == "1"

# single node query
assert run(
"""2 1
1 2
1 2
"""
) == "2"

# chain
assert run(
"""4 1
1 2
2 3
3 4
3 2 3 4
"""
) == "16"

# all LCAs become root
assert run(
"""5 1
1 2
1 3
1 4
1 5
4 2 3 4 5
"""
) == "20"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Single-node tree | 1 | Minimum size |
| Query of length 1 | Node id | LCA of one node equals itself |
| Chain tree | 16 | Ancestor-descendant LCAs |
| Star tree | 20 | Many intervals sharing the root |
| Sample 1 | 2, 12 | General correctness |

## Edge Cases

A query containing only one universe:

```
2 1
1 2
1 2
```

The only interval is `[2]`. The algorithm creates `cur = [(2,1)]`, adds `2 * 1`, and returns `2`. No LCA computation with another node is needed.

A chain:

```
1 - 2 - 3 - 4
query: 2 3 4
```

The interval LCAs are:

```
[2] = 2
[3] = 3
[4] = 4
[2,3] = 2
[3,4] = 3
[2,3,4] = 2
```

The answer is:

```
2 + 3 + 4 + 2 + 3 + 2 = 16
```

The grouped-LCA representation handles this naturally because LCAs move upward only when necessary.

A star rooted at `1`:

```
1 connected to 2,3,4,5
query: 2 3 4 5
```

Every interval of length at least two has LCA `1`. During processing, many extensions collapse into the same value, and the merge step combines them into a single `(1,count)` pair. This is exactly the situation that keeps the number of stored states small.
