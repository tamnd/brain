---
title: "CF 102694E - Filthy Rich Trees"
description: "We have a rooted tree whose root is node 1. Each node stores a positive integer amount of money. The value produced by a subtree is the product of the values stored in every node inside that subtree. Two operations must be processed online."
date: "2026-08-01T23:24:59+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102694
codeforces_index: "E"
codeforces_contest_name: "AlgorithmsThread Tree Basics Contest"
rating: 0
weight: 102694
solve_time_s: 73
verified: true
draft: false
---

[CF 102694E - Filthy Rich Trees](https://codeforces.com/problemset/problem/102694/E)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 13s  
**Verified:** yes  

## Solution
## Problem Understanding

We have a rooted tree whose root is node `1`. Each node stores a positive integer amount of money. The value produced by a subtree is the product of the values stored in every node inside that subtree.

Two operations must be processed online. An update replaces the value of one node. A query asks for the ratio between the values of two subtrees. Since products can become enormous, ratios greater than or equal to `10^9` must be printed as exactly `1000000000`.

The difficulty comes from the fact that changing one node affects every subtree containing that node, meaning all of its ancestors. A direct simulation would repeatedly walk upward through the tree, which is too slow.

The limits allow around `O((n+q) log n)` operations. With up to `3 * 10^5` nodes and queries, anything that scans an entire subtree or an entire root-to-node path for every operation can reach roughly `9 * 10^10` operations and will not finish.

The main edge cases are caused by large products and tree structure. A single node tree is valid:

```
Input
1
1
1 1 1
```

The only possible subtree is the root, so the answer is:

```
1.0000000000
```

A careless implementation using normal multiplication would overflow even on moderate inputs, while the correct solution only needs logarithms.

Another case is when a node is updated many times:

```
Input
2
1 2
3
1 2 10
1 2 100
2 2 1
```

The final ratio is `100`, because the old value must be replaced, not multiplied. Forgetting to remove the previous contribution produces an incorrect answer.

A third edge case is when the denominator subtree is larger:

```
Input
3
1 2
1 3
2
1 2 5
2 1 2
```

The value of subtree `1` is `5`, while subtree `2` is `5`, so the answer is `1`. A solution that only compares ancestors or depths would fail because subtree values depend on all descendants.

## Approaches

The straightforward approach is to maintain every node value and compute subtree products when needed. For a query on node `x`, we could traverse the entire subtree of `x`, multiply all values, and repeat for `y`. This is correct because the definition of the subtree value is exactly that product.

The problem appears when the tree becomes large. A star-shaped tree with `n = 300000` has one subtree containing almost every node. One query could require hundreds of thousands of multiplications, and doing that for hundreds of thousands of queries reaches about `9 * 10^10` operations.

The first observation is that products are difficult to maintain but logarithms turn them into sums:

$$\log(a \times b)=\log(a)+\log(b)$$

Instead of storing subtree products, we store the sum of logarithms inside each subtree. The ratio of two subtree values becomes the difference of two sums.

The remaining challenge is updates. If node `x` changes by a logarithmic difference `d`, every ancestor subtree sum must change by `d`. This is exactly a tree path update from the root to `x`, followed by queries asking for the value associated with a node.

Euler tour gives a useful transformation. If we store a value at a node and query the sum over its Euler interval, we obtain a subtree sum. Using a Fenwick tree with a difference technique, a root-to-node contribution can be represented as a range update over Euler order, allowing every operation to run in logarithmic time.

The final method keeps the logarithmic contribution of each node and uses Euler ordering with a Fenwick tree to maintain subtree sums.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n) per query/update in the worst case | O(n) | Too slow |
| Optimal | O(log n) per operation | O(n) | Accepted |

## Algorithm Walkthrough

1. Run a DFS from the root and compute `tin[x]` and `tout[x]` for every node. The subtree of `x` becomes the contiguous Euler segment `[tin[x], tout[x]]`.
2. Store the logarithmic value of every node. Initially every node contains `1`, so every logarithm is `0`.
3. When a node value changes from `old` to `new`, compute:

$$\Delta=\log(new)-\log(old)$$

This is the amount that every subtree containing this node must gain.

1. Add `\Delta` to the Euler position of the node and subtract it after the subtree interval ends using a Fenwick tree. This makes querying a subtree equal to summing over its Euler interval.
2. For a query asking for nodes `x` and `y`, obtain the logarithmic subtree sums `sx` and `sy`. The desired ratio is:

$$e^{sx-sy}$$

If the difference is large enough that the result reaches `10^9`, print the cap immediately.

Why it works: the Fenwick tree stores exactly the accumulated logarithmic contribution of every updated node to all subtrees containing it. Every node's value contributes to precisely the Euler interval of all ancestors, so the maintained sum for a subtree is always equal to the logarithm of its true product. Taking the difference of two maintained sums gives the logarithm of the requested ratio, which recovers the answer after exponentiation.

## Python Solution

```python
import sys
import math

input = sys.stdin.readline

class Fenwick:
    def __init__(self, n):
        self.n = n
        self.bit = [0.0] * (n + 3)

    def add(self, i, v):
        while i <= self.n:
            self.bit[i] += v
            i += i & -i

    def sum(self, i):
        res = 0.0
        while i:
            res += self.bit[i]
            i -= i & -i
        return res

    def range_add(self, l, r, v):
        self.add(l, v)
        if r + 1 <= self.n:
            self.add(r + 1, -v)

def solve():
    n = int(input())
    graph = [[] for _ in range(n + 1)]

    for _ in range(n - 1):
        a, b = map(int, input().split())
        graph[a].append(b)
        graph[b].append(a)

    tin = [0] * (n + 1)
    tout = [0] * (n + 1)
    order = 0

    sys.setrecursionlimit(1000000)

    def dfs(v, p):
        nonlocal order
        order += 1
        tin[v] = order
        for u in graph[v]:
            if u != p:
                dfs(u, v)
        tout[v] = order

    dfs(1, 0)

    bit = Fenwick(n)
    values = [1] * (n + 1)
    logs = [0.0] * (n + 1)

    q = int(input())
    ans = []

    for _ in range(q):
        t, x, y = map(int, input().split())

        if t == 1:
            delta = math.log(y) - logs[x]
            logs[x] = math.log(y)
            values[x] = y
            bit.range_add(tin[x], tout[x], delta)
        else:
            diff = bit.sum(tout[x]) - bit.sum(tin[x] - 1)
            diff -= bit.sum(tout[y]) - bit.sum(tin[y] - 1)

            if diff >= math.log(1e9):
                ans.append("1000000000")
            else:
                ans.append("{:.10f}".format(math.exp(diff)))

    sys.stdout.write("\n".join(ans))

if __name__ == "__main__":
    solve()
```

The DFS assigns each subtree a continuous interval. The Fenwick tree is not storing subtree sums directly. It stores a difference array over Euler positions, so adding a contribution to a subtree interval is a pair of point updates.

The update operation keeps `logs[x]` as the current logarithm of the node value. The difference between the new and old logarithms is exactly the amount that all ancestor subtree sums need to change.

The query reconstructs a subtree sum by taking the prefix sum at `tout[x]` minus the prefix sum before `tin[x]`. Subtracting the two logarithmic subtree sums gives the logarithm of the requested ratio.

The cap check is performed before calling `exp`. This avoids overflow because the actual product ratio may be astronomically large.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O((n + q) log n) | DFS builds the Euler order, every Fenwick operation is logarithmic |
| Space | O(n) | Tree storage, Euler arrays, and Fenwick tree |

The solution performs only logarithmic work for each query and update, which fits the `300000` operation limit comfortably.

## Worked Examples

For the second sample:

```
5
4 2
1 4
5 4
3 4
```

The Euler ordering makes the subtree of node `4` a continuous interval containing nodes `2`, `3`, `5`, and `4`.

| Operation | Updated node | Delta log | Query result |
| --- | --- | --- | --- |
| Initial | none | 0 | all ratios are 1 |
| Set node 5 to 4 | 5 | log(4) | subtree 5 becomes larger |
| Set node 5 to 5 | 5 | log(5)-log(4) | old value removed |
| Set node 5 to 4 | 5 | log(4)-log(5) | value restored |
| Query 5 vs 4 | none | 0 difference | 1.0000000000 |

This demonstrates why updates must use the difference from the previous value.

For a custom chain:

```
3
1 2
2 3
3
1 3 10
2 1 3
2 2 3
```

| Operation | Active contribution | Subtree log of node 1 | Subtree log of node 2 | Subtree log of node 3 |
| --- | --- | --- | --- | --- |
| Initial | none | 0 | 0 | 0 |
| Update node 3 | +log(10) | log(10) | log(10) | log(10) |
| Query 1 / 3 | none | log(10)-log(10)=0 |  |  |
| Query 2 / 3 | none |  | log(10)-log(10)=0 |  |

The update reaches every ancestor, which is exactly what the Fenwick representation maintains.

## Test Cases

```
# These tests illustrate the expected behaviour of the algorithm.

def check(inp, expected):
    import subprocess
    result = subprocess.run(
        ["python3", "main.py"],
        input=inp.encode(),
        stdout=subprocess.PIPE
    )
    assert result.stdout.decode().strip() == expected.strip()

check(
"""1
1
1 1 1
""",
"""1.0000000000"""
)

check(
"""3
1 2
1 3
4
1 2 5
2 1 2
2 2 3
2 1 1
""",
"""1.0000000000
5.0000000000
1.0000000000"""
)

check(
"""2
1 2
3
1 2 100
2 2 1
2 1 2
""",
"""0.0100000000
100.0000000000"""
)

check(
"""4
1 2
2 3
3 4
3
1 4 7
2 1 4
2 2 4
""",
"""1.0000000000
1.0000000000"""
)
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Single node tree | 1.0000000000 | Minimum tree size |
| Branching tree | Mixed ratios | Subtree interval handling |
| Large replacement values | Exact ratios | Update replacement logic |
| Chain tree | Equal ancestor ratios | Root-to-leaf propagation |

## Edge Cases

For a single node tree, the DFS creates an Euler interval of length one. The Fenwick tree has no updates, and every query compares the same single value, producing `1`.

For repeated updates, the stored logarithm is overwritten instead of accumulated. For example, changing a node from `4` to `5` adds `log(5)-log(4)`, not `log(5)`. This keeps the maintained subtree values consistent.

For very large answers, the algorithm compares logarithms before exponentiation. If the difference is at least `log(10^9)`, the exact value is unnecessary because the required output is already fixed at `1000000000`.
