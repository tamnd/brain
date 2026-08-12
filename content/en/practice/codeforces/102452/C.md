---
title: "CF 102452C - Constructing Ranches"
description: "Each shop is a vertex of a tree, and shop (i) sells exactly one fence segment of length (ai). Choosing two shops (x) and (y) means taking every segment on the unique tree path between them."
date: "2026-08-12T08:37:23+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102452
codeforces_index: "C"
codeforces_contest_name: "2019-2020 ICPC Asia Hong Kong Regional Contest"
rating: 0
weight: 102452
solve_time_s: 220
verified: true
draft: false
---

[CF 102452C - Constructing Ranches](https://codeforces.com/problemset/problem/102452/C)

**Rating:** -  
**Tags:** -  
**Solve time:** 3m 40s  
**Verified:** yes  

## Solution
## Problem Understanding

Each shop is a vertex of a tree, and shop (i) sells exactly one fence segment of length (a_i). Choosing two shops (x) and (y) means taking every segment on the unique tree path between them. The question is how many pairs (x<y) produce a collection of segment lengths that can be arranged into a non-degenerate simple polygon.

For any fixed path, only the lengths of its segments matter. Suppose their total length is (S), and the longest segment has length (M). A collection of positive lengths can form a simple polygon exactly when

[
S > 2M.
]

The reason is that the longest side must be shorter than the sum of all other sides. If that inequality holds, the segments can be arranged into a polygon; if equality holds, they only form a degenerate straight configuration.

So the graph problem becomes a path-query problem. For every pair of vertices, we need to know the sum of values on their path and the maximum value on that path, then test whether the sum is more than twice the maximum.

The tree contains up to (2\cdot10^5) vertices in one test case, and the total over all test cases is at most (4\cdot10^5). An (O(n^2)) algorithm would inspect roughly (2\cdot10^{10}) pairs at (n=2\cdot10^5), which is far beyond the 5.5 second limit. We need something close to (O(n\log^2 n)), which is the complexity of the intended solution.

There are several boundary cases that are easy to mishandle. With only one vertex there is no pair at all. For example,

```
1
1
5
```

has answer `0`. A path containing two vertices also cannot form a polygon, regardless of the lengths, because one segment cannot be strictly shorter than the sum of the other segment.

Equality must also be rejected. Consider

```
1
3
1 1 2
1 2
2 3
```

The only path containing all three vertices has total length (4) and maximum length (2). Since (4=2\cdot2), it is degenerate, so the answer is `0`. A non-strict comparison such as (S\ge2M) would incorrectly count it.

The maximum segment does not have to be the centroid when we use centroid decomposition. For example,

```
1
3
2 1 2
1 2
2 3
```

gives the path (1\to2\to3) with lengths (2,1,2). Its sum is (5), while twice its maximum is (4), so the answer is `1`. Any solution that only counts paths whose largest segment is at the centroid would fail on this kind of case.

Finally, equal lengths provide a useful sanity check. For

```
1
5
1 1 1 1 1
1 2
1 3
1 4
1 5
```

every path between two leaves contains three unit segments and is valid, while every path involving the center contains only two segments and is invalid. There are (\binom42=6) valid pairs.

## Approaches

The brute-force solution follows directly from the definition. For every pair of vertices (x<y), walk along their unique tree path, accumulating its sum and maximum. Then check whether the sum is greater than twice the maximum. This is correct because the polygon condition depends only on exactly those two quantities.

The problem is the number of paths. There are (\binom n2) endpoint pairs, which is already (O(n^2)), and walking along a path can itself take (O(n)). On a chain, this produces

[
\sum_{k=1}^{n-1} k(n-k)=\Theta(n^3)
]

operations. Even if we preprocess path information enough to make each pair (O(1)), we would still have roughly (2\cdot10^{10}) pairs for (n=2\cdot10^5).

The useful structure is that the graph is a tree. Centroid decomposition lets us split every path according to the first centroid it passes through. At one centroid (c), every path that passes through (c) can be described using information from its two endpoints relative to (c).

For a vertex (u) in the current component, define (s_u) as the sum of values on the path from (c) to (u), including (a_c), and define (m_u) as the maximum value on that same path. If (u) and (v) lie in different components after removing (c), their complete path goes from (u) to (c) and then from (c) to (v). Consequently its sum and maximum are

[
S=s_u+s_v-a_c
]

and

[
M=\max(m_u,m_v).
]

The validity condition becomes

[
s_u+s_v-a_c>2\max(m_u,m_v).
]

This is the central reduction. The tree has disappeared from the inequality. At a fixed centroid, each endpoint is represented by only two numbers, (s_u) and (m_u).

We still need to avoid counting pairs from the same child component of the centroid, because their actual path does not pass through the centroid. A convenient way to do this is to count all pairs among the collected vertices using the formula above, then separately count the pairs entirely inside every child component and subtract them. The centroid itself is kept as a separate group, so pairs involving the centroid remain counted.

To count pairs satisfying the inequality efficiently, sort vertices by decreasing (m). When processing (u), every previously processed vertex (v) satisfies (m_v\ge m_u), so the maximum is (m_v). The inequality becomes

[
s_u+s_v-a_c>2m_v,
]

which can be rearranged as

[
2m_v-s_v+a_c<s_u.
]

For every processed vertex, insert the key

[
k_v=2m_v-s_v+a_c
]

into a Fenwick tree. For the current (u), we only need to count inserted keys strictly smaller than (s_u). Coordinate compression lets the Fenwick tree handle these arbitrary integer keys.

The same counting routine can be applied to the whole centroid component and to each child component separately. Centroid decomposition then recursively processes every child component, so every unordered pair is counted exactly once.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | (O(n^3)) | (O(n)) | Too slow |
| Brute Force with (O(1)) path queries | (O(n^2)) | (O(n^2)) or more | Too slow |
| Centroid decomposition + Fenwick tree | (O(n\log^2 n)) | (O(n)) | Accepted |

## Algorithm Walkthrough

1. First use the polygon lemma. A path is valid exactly when the sum of its segment lengths is strictly greater than twice the maximum segment length on that path.
2. Build a centroid decomposition of the tree. For the current component, find its centroid (c). Every path in this component either passes through (c), or is completely contained in one of the components obtained after removing (c).
3. For every vertex (u) reachable from (c) without crossing another blocked centroid, compute two values. Let (s_u) be the sum from (c) to (u), including (a_c), and let (m_u) be the maximum value on that same path. Record which child component of (c) contains (u).
4. Add the centroid itself as a special record with (s_c=a_c) and (m_c=a_c). This allows paths from (c) to another vertex to be treated by exactly the same formula as paths between two different child components.
5. Count every pair among all collected records using the condition

[
s_u+s_v-a_c>2\max(m_u,m_v).
]

To do this efficiently, sort the records by decreasing (m). For the current record (u), all earlier records (v) have (m_v\ge m_u). The condition is then

[
2m_v-s_v+a_c<s_u.
]

Store (2m_v-s_v+a_c) for earlier records in a Fenwick tree and query how many are strictly smaller than (s_u).

1. The count from the previous step also includes pairs whose two vertices belong to the same child component of (c). Such a pair does not actually pass through (c), so its calculation through (c) is irrelevant. For every child component, run the same pair-counting routine on only its records and subtract that result.
2. Mark (c) as removed from the current component. Recursively solve every remaining child component. Every path that was not counted at (c) is entirely contained in exactly one of these smaller components, so it will be handled there.
3. Sum the contribution from the current centroid and all recursive components. The resulting number is the answer for the test case.

### Why it works

At every centroid (c), the algorithm counts exactly the valid paths whose endpoints are either (c) itself or lie in two different components after removing (c). For such a path, (s_u+s_v-a_c) is exactly its total length and (\max(m_u,m_v)) is exactly its largest segment, so the Fenwick condition is equivalent to the polygon condition.

Pairs lying inside one child component are removed from the current contribution and are passed to the recursive call for that component. Thus every path is handled at the highest centroid where its endpoints become separated, or where one endpoint is the centroid itself. No path can be counted at two different decomposition levels, and no path can be skipped.

The sorting argument is also exact. Once vertices are processed in decreasing (m), an earlier vertex always has the larger or equal path maximum. This lets us replace the maximum of two values by the already processed (m_v), converting the two-variable maximum inequality into a single threshold comparison suitable for a Fenwick tree.

## Python Solution

```python
import sys
from bisect import bisect_left

input = sys.stdin.readline

class Fenwick:
    __slots__ = ("n", "bit")

    def __init__(self, n):
        self.n = n
        self.bit = [0] * (n + 1)

    def add(self, i, value=1):
        n = self.n
        bit = self.bit
        while i <= n:
            bit[i] += value
            i += i & -i

    def sum(self, i):
        bit = self.bit
        res = 0
        while i:
            res += bit[i]
            i -= i & -i
        return res

def count_pairs(items, ac):
    """
    Count unordered pairs (u, v) inside items satisfying

        s_u + s_v - ac > 2 * max(m_u, m_v)

    where each item is (s, m).
    """
    k = len(items)
    if k < 2:
        return 0

    items.sort(key=lambda x: x[1], reverse=True)

    keys = [2 * m - s + ac for s, m in items]
    coords = sorted(set(keys))

    fw = Fenwick(len(coords))
    ans = 0

    for s, m in items:
        # Need key < s, hence bisect_left rather than bisect_right.
        pos = bisect_left(coords, s)
        ans += fw.sum(pos)

        key = 2 * m - s + ac
        idx = bisect_left(coords, key) + 1
        fw.add(idx)

    return ans

def solve(data):
    it = iter(map(int, data.split()))
    t = next(it)
    outputs = []

    for _ in range(t):
        n = next(it)
        a = [next(it) for _ in range(n)]

        graph = [[] for _ in range(n)]
        for _ in range(n - 1):
            u = next(it) - 1
            v = next(it) - 1
            graph[u].append(v)
            graph[v].append(u)

        blocked = [False] * n
        parent = [-1] * n
        size = [0] * n

        def find_centroid(start):
            order = [start]
            parent[start] = -1

            for u in order:
                pu = parent[u]
                for v in graph[u]:
                    if blocked[v] or v == pu:
                        continue
                    parent[v] = u
                    order.append(v)

            for u in reversed(order):
                size[u] = 1
                for v in graph[u]:
                    if blocked[v] or parent[v] != u:
                        continue
                    size[u] += size[v]

            total = len(order)
            centroid = start
            best = total + 1

            for u in order:
                largest = total - size[u]
                for v in graph[u]:
                    if blocked[v] or parent[v] != u:
                        continue
                    if size[v] > largest:
                        largest = size[v]

                if largest < best:
                    best = largest
                    centroid = u

            return centroid

        answer = 0

        def decompose(start):
            nonlocal answer

            c = find_centroid(start)
            ac = a[c]

            all_items = [(ac, ac)]

            branch_items = []

            for first in graph[c]:
                if blocked[first]:
                    continue

                current = []
                stack = [(first, c, ac + a[first], max(ac, a[first]))]

                while stack:
                    u, p, s, m = stack.pop()
                    current.append((s, m))
                    all_items.append((s, m))

                    for v in graph[u]:
                        if blocked[v] or v == p or v == c:
                            continue
                        stack.append(
                            (v, u, s + a[v], max(m, a[v]))
                        )

                branch_items.append(current)

            # Count all pairs whose path is considered through c.
            answer += count_pairs(all_items, ac)

            # Remove pairs whose endpoints are in the same branch.
            for items in branch_items:
                answer -= count_pairs(items, ac)

            blocked[c] = True

            for v in graph[c]:
                if not blocked[v]:
                    decompose(v)

        if n > 0:
            decompose(0)

        outputs.append(str(answer))

    return "\n".join(outputs)

def main():
    data = sys.stdin.buffer.read().decode()
    sys.stdout.write(solve(data))

if __name__ == "__main__":
    main()
```

The Fenwick tree is a standard prefix-count structure. After coordinate compression, `add` inserts one key and `sum(pos)` counts all inserted keys whose compressed position is at most `pos`.

The expression `bisect_left(coords, s)` is deliberately strict. The desired inequality is (2m_v-s_v+a_c<s_u), not less than or equal to (s_u). If the two sides are equal, the polygon is degenerate and must not be counted.

The centroid itself is represented by `(ac, ac)`. If (u) is another vertex, the pair `(c,u)` has total (a_c+s_u-a_c=s_u), and its maximum is (m_u), so the generic formula handles it without special cases.

The subtraction over each branch is what prevents paths that stay entirely inside one branch from being counted at the current centroid. Those paths are still present in the recursive decomposition, where their actual geometry is represented correctly.

Python integers have arbitrary precision, so sums can safely reach (2\cdot10^{14}) without overflow. The implementation also uses iterative traversals for component exploration, avoiding Python recursion depth problems on a chain. The recursion of `decompose` itself has logarithmic depth because each recursive component has at most half the vertices of its parent.

## Worked Examples

### Sample 1

The first sample is

```
3
1 10 100
1 2
3 2
```

The tree is a chain. There are only three possible endpoint pairs, and each path contains at most two segments.

| Pair | Path lengths | Sum | Maximum | Condition | Valid |
| --- | --- | --- | --- | --- | --- |
| (1, 2) | 1, 10 | 11 | 10 | (11>20) | No |
| (1, 3) | 1, 10, 100 | 111 | 100 | (111>200) | No |
| (2, 3) | 10, 100 | 110 | 100 | (110>200) | No |

The answer is `0`. The example also demonstrates why two segments can never form a valid polygon and why a very large segment immediately makes a path invalid.

### Sample 2

The second sample is

```
5
1 1 1 1 1
1 2
1 3
1 4
1 5
```

Vertex 1 is the center and the other four vertices are leaves. Every leaf-to-leaf path has three unit segments.

At the first centroid, (a_c=1). The centroid record is `(1,1)`, and every leaf has `(2,1)` because its path from the center contains two unit values.

| Endpoint type | (s) | (m) | Number |
| --- | --- | --- | --- |
| Centroid | 1 | 1 | 1 |
| Leaf | 2 | 1 | 4 |

For two leaves,

[
s_u+s_v-a_c=2+2-1=3,
]

while

[
2\max(m_u,m_v)=2.
]

So every pair of leaves is valid.

| Pair type | Number of pairs | Valid |
| --- | --- | --- |
| Center and leaf | 4 | No |
| Two different leaves | (\binom42=6) | Yes |

The current centroid contribution is `6`. Every branch contains only one vertex, so there are no same-branch pairs to subtract. All recursive components are single vertices and contribute zero.

The final answer is `6`, matching the sample.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | (O(n\log^2 n)) | Each centroid level processes (O(n)) vertices, sorting and Fenwick operations cost (O(n\log n)), and there are (O(\log n)) levels |
| Space | (O(n)) | The tree, centroid-decomposition state, traversal buffers, and temporary counting arrays are all linear |

The centroid decomposition reduces every component by roughly half, so a vertex participates in (O(\log n)) levels. At each level, sorting and Fenwick operations require (O(n\log n)) total work over that level. With (n\le2\cdot10^5) per case and (4\cdot10^5) vertices in total, this fits the intended (O(n\log^2 n)) solution. The official editorial gives the same complexity.

## Test Cases

The following tests assume the submitted solution is saved as `solution.py` and exposes the `solve(data)` function shown above.

```
from solution import solve

def run(inp: str) -> str:
    return solve(inp).strip()

# Provided sample
sample = """\
2
3
1 10 100
1 2
3 2
5
1 1 1 1 1
1 2
1 3
1 4
1 5
"""
assert run(sample) == "0\n6", "provided samples"

# Minimum-size input
assert run("""\
1
1
7
""") == "0", "one vertex has no pair"

# Two vertices can never form a polygon
assert run("""\
1
2
1 100
1 2
""") == "0", "two segments are impossible"

# Equality case: 1 + 1 = 2, so the polygon is degenerate
assert run("""\
1
3
1 1 2
1 2
2 3
""") == "0", "strict polygon inequality"

# A maximum is away from the centroid.
# Path 1-2-3 has lengths 2, 1, 2 and is valid.
assert run("""\
1
3
2 1 2
1 2
2 3
""") == "1", "maximum need not be the centroid"

# All equal values on a chain.
# Every path with at least 3 vertices is valid.
n = 200000
values = " ".join(["1"] * n)
edges = "\n".join(f"{i} {i + 1}" for i in range(1, n))
expected = (n - 1) * (n - 2) // 2

large_input = f"""\
1
{n}
{values}
{edges}
"""
assert run(large_input) == str(expected), "large all-equal chain"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 / 1 / 7` | `0` | Minimum-size boundary |
| `1 / 2 / 1 100 / 1 2` | `0` | Two segments cannot form a polygon |
| `1 / 3 / 1 1 2 / 1-2-3` | `0` | Strict inequality and equality boundary |
| `1 / 3 / 2 1 2 / 1-2-3` | `1` | Maximum may be away from the centroid |
| Chain of 200000 unit vertices | `19999700001` | Maximum-size input, equal values, performance, large answer |

## Edge Cases

The one-vertex case is handled before any meaningful pair counting can occur. For the input

```
1
1
7
```

the only centroid is vertex 1, and `all_items` contains just `(7,7)`. The Fenwick routine immediately returns zero because there are fewer than two records. The recursive decomposition has no remaining component, so the final answer is `0`.

For two vertices, the algorithm also returns zero. Consider

```
1
2
1 100
1 2
```

The centroid decomposition may choose either vertex as the centroid. The only path contains lengths (1) and (100), giving sum (101) and maximum (100). The required inequality is (101>200), which is false. The Fenwick comparison also rejects it because the corresponding threshold is not strictly below the current sum.

The equality boundary is handled by the use of `bisect_left`. For

```
1
3
1 1 2
1 2
2 3
```

the whole path has (s=4) and (m=2), so (s=2m). In the transformed inequality, the relevant key is exactly equal to the current (s). `bisect_left` places the query before equal keys, so that pair is not counted. This is precisely the required strict inequality.

A maximum outside the centroid is handled because the algorithm does not assume the centroid is the largest value. For

```
1
3
2 1 2
1 2
2 3
```

take vertex 2 as centroid. Each leaf has (s=3) and (m=2), while the centroid has (s=m=1). For the two leaves,

[
3+3-1=5>2\cdot2=4.
]

The pair is counted even though the centroid's value is smaller than both endpoint maxima. This is exactly why the algorithm stores both (s_u) and (m_u), rather than only the sum from the centroid.

For the all-equal maximum-size chain, every path containing at least three vertices is valid. A path of two vertices has sum (2) and maximum (1), so it is already valid under the numerical inequality, but such a path still cannot form a polygon. This apparent issue is resolved by the polygon lemma because for two segments the longest segment is always at least the other segment, making (S>2M) impossible. For unit values, a two-vertex path has (S=2) and (2M=2), so it fails strictly. Every path with three or more vertices succeeds.

Thus on a chain of (n=200000) unit vertices, the valid paths are exactly those with at least three vertices. There are

[
\binom n2-(n-1)
=\frac{(n-1)(n-2)}2
=19999700001
]

of them, which is the value checked by the large test.

The same reasoning explains why the star sample has answer six. A center-to-leaf path contains two unit segments and fails at equality, while every leaf-to-leaf path contains three unit segments and succeeds. The centroid-level subtraction removes no valid leaf pair because every leaf is in a different branch.
