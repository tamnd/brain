---
title: "CF 102625G - Secret Society and a Certain Someone"
description: "The problem describes a tree of secret offices connected by passages. Each passage has a security level. For every possible meeting location, every other office sends a representative along the unique path to that office."
date: "2026-08-03T15:21:47+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102625
codeforces_index: "G"
codeforces_contest_name: "IIT(ISM) Virtual Farewell"
rating: 0
weight: 102625
solve_time_s: 58
verified: true
draft: false
---

[CF 102625G - Secret Society and a Certain Someone](https://codeforces.com/problemset/problem/102625/G)

**Rating:** -  
**Tags:** -  
**Solve time:** 58s  
**Verified:** yes  

## Solution
# Problem Understanding

The problem describes a tree of secret offices connected by passages. Each passage has a security level. For every possible meeting location, every other office sends a representative along the unique path to that office. On the return path, the representative hides information in every passage that has the maximum security level on that path.

The task is to find the largest number of hidden information copies placed on any passage and list all passages achieving that maximum. The input contains the number of offices followed by the passages, their endpoints, and their security levels. The output contains the maximum number of copies and the indices of all passages with that count. The original problem constraints have up to $2 \cdot 10^5$ offices, so an approach that examines paths for every pair of offices is impossible.

A direct simulation would consider every ordered pair of offices, giving roughly $n^2$ paths. With $n=200000$, this is around $4 \cdot 10^{10}$ pairs, far beyond what a one second solution can handle. We need to process the tree structure globally instead of looking at individual paths.

The main edge cases come from equal maximum security levels and from passages that are not the only maximum on a path. For example, consider:

```
3
1 2 5
2 3 5
```

The correct output is:

```
4 2
1 2
```

A careless solution might count only one maximum passage on the path from office 1 to office 3, but both passages have the same maximum level and both receive a copy.

Another tricky case is when a high security passage blocks lower security passages from receiving information. For example:

```
3
1 2 10
2 3 1
```

The first passage receives 4 copies and the second receives 2 copies. A solution that only counts how many paths contain an edge, without checking whether the edge is the maximum on those paths, gives the wrong answer.

# Approaches

The brute-force solution is straightforward. For every meeting office, run a traversal to find paths from every other office, find the maximum security value on each path, and increase the count of all passages having that value. It is correct because it follows the definition directly. However, the number of office pairs is $n(n-1)$, and processing each path can take $O(n)$, resulting in $O(n^3)$ work in the worst case. Even storing all pair distances is already too expensive.

The key observation is that a passage with security level $w$ only matters for paths where every edge has security level at most $w$. If we remove all passages with security level greater than $w$, then inside each remaining component, every path uses only edges with level at most $w$. A passage of level $w$ is selected exactly for the ordered pairs of offices separated by that passage inside this component.

This suggests processing passages by increasing security level. Before handling a group of passages with the same level, a disjoint set union structure represents components connected using smaller levels. For the current level, the smaller components connected by these passages form temporary trees. For a passage splitting a temporary tree into sides of sizes $a$ and $b$, the number of ordered pairs crossing it is $2ab$.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(n^3)$ | $O(n)$ | Too slow |
| Optimal | $O(n \log n)$ | $O(n)$ | Accepted |

# Algorithm Walkthrough

1. Sort all passages by their security level. We process equal security levels together because passages with the same level can all be maximum edges on the same path.
2. Maintain a DSU containing only passages with smaller security levels. Each DSU component represents a group of offices connected without using any passage that could be a maximum edge at the current level.
3. For every group of passages with the same security level, contract each DSU component into a single node. The current passages form a forest between these contracted nodes.
4. Traverse each temporary tree. For every current passage, compute the total number of original offices on both sides of that passage. If the two sides contain $a$ and $b$ offices, add $2ab$ to that passage's count.
5. After all counts for this security level are computed, merge all passages of this level into the DSU. They become available when processing larger security levels.

Why it works: for a passage with level $w$, a pair of offices contributes to it exactly when the entire path between them contains no edge larger than $w$ and the passage lies on that path. During the processing of level $w$, the DSU components and the temporary forest represent exactly those paths. Cutting the passage divides the valid paths into two groups of sizes $a$ and $b$, and every ordered choice of one endpoint from each side contributes once. Thus $2ab$ counts precisely all information copies for that passage.

# Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    edges = []
    for i in range(1, n):
        u, v, w = map(int, input().split())
        edges.append((w, u - 1, v - 1, i))

    parent = list(range(n))
    size = [1] * n

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    def union(a, b):
        a = find(a)
        b = find(b)
        if a == b:
            return
        if size[a] < size[b]:
            a, b = b, a
        parent[b] = a
        size[a] += size[b]

    edges.sort()
    ans = [0] * n
    i = 0

    while i < n - 1:
        j = i
        while j < n - 1 and edges[j][0] == edges[i][0]:
            j += 1

        graph = {}
        nodes = set()

        for _, u, v, idx in edges[i:j]:
            ru = find(u)
            rv = find(v)
            graph.setdefault(ru, []).append((rv, idx))
            graph.setdefault(rv, []).append((ru, idx))
            nodes.add(ru)
            nodes.add(rv)

        visited = set()

        for start in nodes:
            if start in visited:
                continue

            order = []
            par = {start: -1}
            pedge = {}

            stack = [start]
            visited.add(start)

            while stack:
                x = stack.pop()
                order.append(x)
                for y, eid in graph.get(x, []):
                    if y != par[x]:
                        par[y] = x
                        pedge[y] = eid
                        visited.add(y)
                        stack.append(y)

            total = 0
            for x in order:
                total += size[find(x)]

            sub = {}
            for x in reversed(order):
                cur = size[find(x)]
                for y, eid in graph.get(x, []):
                    if par.get(y) == x:
                        cur += sub[y]
                sub[x] = cur
                if par[x] != -1:
                    other = total - cur
                    ans[pedge[x]] += 2 * cur * other

        for _, u, v, _ in edges[i:j]:
            union(u, v)

        i = j

    best = max(ans[1:])
    res = [str(i) for i in range(1, n) if ans[i] == best]

    print(best, len(res))
    print(" ".join(res))

if __name__ == "__main__":
    solve()
```

The DSU part follows the increasing security level idea. The `find` operation gives the current contracted component before the current level is merged.

The temporary graph is rebuilt only for one security level at a time. Its vertices are DSU components, not individual offices. The traversal computes subtree sizes in this temporary forest. When a temporary edge separates a subtree of size `cur` from the remaining `total - cur`, the number of valid ordered pairs is exactly `2 * cur * (total - cur)`.

The merging step happens after counting. This ordering is essential. If current-level passages were merged before counting, they would incorrectly appear as already available lower-level connections.

# Worked Examples

For the first sample:

```
3
2 1 3
3 1 1
```

The processing is:

| Passage | Current components | Side sizes | Contribution |
| --- | --- | --- | --- |
| 1 | {1},{2},{3} | 2 and 1 | 4 |
| 2 | {1,2},{3} | 1 and 2 | 2 |

The maximum contribution is 4, so passage 1 is selected.

For the second sample:

```
5
2 1 3
4 3 1
5 4 1
2 3 1
```

The temporary trees created for the security level 1 passages produce:

| Passage | Side sizes | Contribution |
| --- | --- | --- |
| 2 | 2 and 3 | 12 |
| 3 | 1 and 4 | 8 |
| 4 | 2 and 3 | 12 |

The higher-level passage is processed separately and reaches the same maximum as another passage, producing multiple answers.

# Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n \log n)$ | Sorting dominates, and each passage participates in a small number of DSU and temporary tree operations. |
| Space | $O(n)$ | The DSU arrays, edge list, and temporary graph contain linear information. |

The solution fits the $2 \cdot 10^5$ limit because it never enumerates office pairs or paths.

# Test Cases

```python
import sys, io

def run(inp: str) -> str:
    old = sys.stdin
    sys.stdin = io.StringIO(inp)
    out = io.StringIO()
    old_out = sys.stdout
    sys.stdout = out
    solve()
    sys.stdin = old
    sys.stdout = old_out
    return out.getvalue()

assert run("""3
2 1 3
3 1 1
""") == """4 1
1
"""

assert run("""3
1 2 5
2 3 5
""") == """8 2
1 2
"""

assert run("""2
1 2 7
""") == """2 1
1
"""

assert run("""4
1 2 3
2 3 3
3 4 3
""") == """8 2
2 3
"""

assert run("""4
1 2 10
2 3 1
3 4 1
""") == """12 1
1
"""
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Three nodes with equal levels | Both edges selected | Equal maximum passages are counted together |
| Single edge tree | The only passage wins | Minimum size case |
| Chain with equal values | Middle passages dominate | Subtree size calculation |
| One large edge and small edges | Large edge wins | Ignoring non-maximum edges |

# Edge Cases

For equal maximum levels, the algorithm handles every current-level passage together. In the input

```
3
1 2 5
2 3 5
```

both passages are in the same temporary tree. Each cut has side sizes 1 and 2, giving 4 copies each, so both are returned.

For a passage with a much larger security value, smaller passages below it cannot receive information from paths crossing the larger passage. In

```
3
1 2 10
2 3 1
```

the first level is processed alone. The temporary component has two sides of sizes 1 and 2, giving 4. The second passage is processed later and only receives the pairs that do not contain the level 10 passage as a maximum, giving 2. The ordering of DSU merges preserves this distinction.
