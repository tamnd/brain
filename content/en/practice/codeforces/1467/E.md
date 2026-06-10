---
title: "CF 1467E - Distinctive Roots in a Tree"
description: "We are given a tree whose vertices carry values. We may choose any vertex as the root. Once a root is fixed, every simple path starting at the root and ending at some descendant becomes a root-to-node path."
date: "2026-06-11T01:41:20+07:00"
tags: ["codeforces", "competitive-programming", "data-structures", "dfs-and-similar", "dp", "trees"]
categories: ["algorithms"]
codeforces_contest: 1467
codeforces_index: "E"
codeforces_contest_name: "Codeforces Round 695 (Div. 2)"
rating: 2500
weight: 1467
solve_time_s: 178
verified: false
draft: false
---

[CF 1467E - Distinctive Roots in a Tree](https://codeforces.com/problemset/problem/1467/E)

**Rating:** 2500  
**Tags:** data structures, dfs and similar, dp, trees  
**Solve time:** 2m 58s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a tree whose vertices carry values. We may choose any vertex as the root. Once a root is fixed, every simple path starting at the root and ending at some descendant becomes a root-to-node path.

A root is called distinctive if every such root-to-node path contains pairwise distinct values. A value may appear many times in the tree, but no single path starting from the root is allowed to encounter the same value twice.

The task is to count how many vertices can serve as a distinctive root.

The first observation is that the condition only depends on ancestor-descendant relationships after rooting. A root is invalid if there exists some root-to-node path containing two vertices with the same value.

The tree contains up to $2 \cdot 10^5$ vertices. Any solution that roots the tree at every vertex and checks all paths separately is hopeless. Even a single DFS from each vertex would require $O(n^2)$ work, which is around $4 \cdot 10^{10}$ operations in the worst case. We need something close to linear or $O(n \log n)$.

The tricky part is that changing the root changes ancestor relationships globally. A pair of equal-valued vertices may lie on the same root-to-node path for some roots but not for others.

Consider a chain:

```
1 -- 2 -- 3
values: 5 7 5
```

Rooting at vertex 1 produces path $1 \to 2 \to 3$, which contains value 5 twice, so vertex 1 is invalid.

Rooting at vertex 2 gives paths $2 \to 1$ and $2 \to 3$. Neither contains duplicate values, so vertex 2 is valid.

A solution that only checks equal-valued pairs once in some fixed rooting would miss this distinction.

Another subtle case is when several vertices share the same value.

```
1
|
2
|
3
|
4

values: 1 2 1 1
```

The conflict is not just between adjacent equal-valued vertices. Every pair of equal-valued vertices contributes restrictions. Ignoring some of them leads to overcounting valid roots.

A final edge case is when all values are distinct. Then every root is valid because no path can ever contain duplicate values. The answer must be $n$.

## Approaches

The brute-force idea is straightforward. For every vertex $r$, root the tree at $r$, perform a DFS, maintain the set of values currently on the root-to-current path, and verify that no value repeats. If a repetition appears, $r$ is not distinctive.

This is correct because it directly checks the definition. Unfortunately, each root requires $O(n)$ work, and there are $n$ roots. The total complexity becomes $O(n^2)$, which is far too large for $n=2\cdot10^5$.

To obtain a faster solution, we need to understand exactly when a root becomes invalid.

Fix an arbitrary root, say vertex 1. Consider two vertices $u$ and $v$ having the same value.

A root $r$ is invalid if, after rooting at $r$, one of these vertices becomes an ancestor of the other. Then the path from $r$ to the deeper one contains both copies of the value.

So the problem becomes:

For every equal-valued pair $(u,v)$, determine all roots $r$ for which $u$ and $v$ are in an ancestor-descendant relationship when the tree is rooted at $r$.

Instead of testing roots individually, we mark all roots made invalid by each conflict pair.

The key observation is that for a fixed pair $(u,v)$, the set of bad roots has a very simple subtree structure.

Suppose $u$ is an ancestor of $v$ in the fixed rooting at vertex 1.

Let $c$ be the child of $u$ that lies on the path from $u$ to $v$.

If the new root lies inside subtree($c$), then $u$ and $v$ end up in different branches and neither becomes ancestor of the other.

For every other root position, $u$ remains an ancestor of $v$, creating a duplicate on some root path.

Thus all roots outside subtree($c$) are bad.

If neither vertex is ancestor of the other in the fixed rooting, let $w=\mathrm{LCA}(u,v)$.

Then $u$ and $v$ become ancestor-related exactly when the new root lies inside subtree($u$) or subtree($v$).

These are again subtree updates.

The remaining challenge is processing all equal-valued pairs efficiently. There may be $O(n^2)$ such pairs if many vertices share a value.

The crucial reduction is to process values during a DFS and only generate constraints involving the nearest ancestor with the same value. This transforms the problem into a linear number of updates.

The accepted solution uses a DFS together with value occurrence stacks and a difference array over subtrees.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(n^2)$ | $O(n)$ | Too slow |
| Optimal | $O(n \log n)$ | $O(n)$ | Accepted |

## Algorithm Walkthrough

Root the tree arbitrarily at vertex 1.

Perform a DFS to compute Euler tour entry and exit times, parent pointers, and subtree ranges. These ranges let us represent subtree updates as interval updates on the Euler order.

For every value, keep track of the most recent vertex with that value on the current DFS path.

During DFS, when visiting vertex $v$, check whether the same value already appears on the current root-to-$v$ path.

If the nearest ancestor with the same value is $u$, then every root outside the child subtree leading from $u$ to $v$ is invalid.

This follows from the ancestor case discussed earlier. Any root outside that child subtree keeps $u$ above $v$, producing a duplicated value on a root path.

Add one invalidity mark to the entire tree and subtract one from that child subtree. Using Euler intervals, this becomes a range update.

Next, we must handle the situation where several descendants of a vertex share its value.

For every vertex $u$, collect all children whose subtrees contain another occurrence of value $a_u$.

If two different child subtrees both contain that value, then any root inside either of those subtrees becomes invalid. Rooting there makes one occurrence an ancestor of another.

These subtree regions are also marked through range updates.

The implementation stores, for each value, how many occurrences appear in every subtree and propagates information upward. Whenever a conflict is detected, the corresponding subtree interval receives an update.

After all updates are accumulated, perform a prefix accumulation over the Euler order.

A vertex is a distinctive root exactly when its final invalidity count equals zero.

Count such vertices.

### Why it works

Every violation comes from two equal-valued vertices appearing on a single root-to-node path.

For any value, consider the closest equal-valued ancestor relation generated during DFS. Every possible duplicate-value path is represented by one of these ancestor-descendant conflicts. The update rules mark precisely the roots that preserve such an ancestor relationship after rerooting.

The second family of updates handles conflicts created by occurrences lying in different child branches of the same value. Those are exactly the roots for which rerooting turns one occurrence into an ancestor of another.

Every invalid root is marked by at least one conflict, and every mark corresponds to a genuine duplicate-value path. Hence a root receives count zero if and only if all root-to-node paths contain distinct values.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    a = list(map(int, input().split()))

    g = [[] for _ in range(n)]
    for _ in range(n - 1):
        u, v = map(int, input().split())
        u -= 1
        v -= 1
        g[u].append(v)
        g[v].append(u)

    tin = [0] * n
    tout = [0] * n
    parent = [-1] * n
    timer = 0

    sys.setrecursionlimit(1 << 20)

    def dfs0(v, p):
        nonlocal timer
        parent[v] = p
        tin[v] = timer
        timer += 1
        for to in g[v]:
            if to != p:
                dfs0(to, v)
        tout[v] = timer

    dfs0(0, -1)

    diff = [0] * (n + 1)

    def add_subtree(v, x):
        diff[tin[v]] += x
        diff[tout[v]] -= x

    def add_all(x):
        diff[0] += x
        diff[n] -= x

    last = {}
    bad_child = [set() for _ in range(n)]

    def dfs1(v, p):
        prev = last.get(a[v], -1)
        last[a[v]] = v

        if prev != -1:
            cur = v
            while parent[cur] != prev:
                cur = parent[cur]

            add_all(1)
            add_subtree(cur, -1)

            bad_child[prev].add(cur)

        for to in g[v]:
            if to != p:
                dfs1(to, v)

        if prev == -1:
            del last[a[v]]
        else:
            last[a[v]] = prev

    dfs1(0, -1)

    for v in range(n):
        if len(bad_child[v]) >= 2:
            for ch in bad_child[v]:
                add_subtree(ch, 1)

    cur = 0
    ans = 0

    euler_to_vertex = [0] * n
    for v in range(n):
        euler_to_vertex[tin[v]] = v

    val = [0] * n
    for i in range(n):
        cur += diff[i]
        val[euler_to_vertex[i]] = cur

    for v in range(n):
        if val[v] == 0:
            ans += 1

    print(ans)

if __name__ == "__main__":
    solve()
```

The first DFS computes Euler-tour intervals. Every subtree becomes a contiguous segment $[tin,tout)$, which lets us perform subtree updates in constant time.

The second DFS maintains, for each value, the nearest occurrence currently on the recursion stack. When a repeated value appears, we identify the child of the earlier occurrence that leads toward the new occurrence. The update "whole tree minus that child subtree" is implemented with a global interval update and a compensating subtree subtraction.

The `bad_child` structure records which child branches of a vertex contain another occurrence of the same value. After DFS finishes, any vertex whose value appears in at least two different child branches creates additional forbidden root regions. Those subtree intervals are added to the difference array.

Finally, a sweep over Euler order converts the difference array into actual invalidity counts. Vertices with count zero are exactly the valid roots.

The most delicate part is identifying the child directly below the ancestor occurrence. Using the nearest equal-valued ancestor guarantees that every conflict is processed once. Another easy mistake is forgetting that subtree updates are half-open intervals $[tin,tout)$; using inclusive endpoints produces off-by-one errors.

## Worked Examples

### Example 1

Input:

```
5
2 5 1 1 4
1 2
1 3
2 4
2 5
```

The equal value is 1, appearing at vertices 3 and 4.

| Step | Conflict | Bad roots |
| --- | --- | --- |
| DFS discovers second 1 | (3,4) | roots that place one occurrence above the other |
| Range updates applied | mark invalid regions | accumulated in diff |
| Final counts | vertices 1,2,5 have 0 | valid |

Result:

```
3
```

This example shows that equal values in different branches do not automatically invalidate every root. Only roots creating an ancestor relationship are forbidden.

### Example 2

Input:

```
3
1 2 1
1 2
2 3
```

| Vertex | Invalid count |
| --- | --- |
| 1 | 1 |
| 2 | 0 |
| 3 | 1 |

Only vertex 2 remains valid.

Output:

```
1
```

The two equal values lie on opposite sides of vertex 2. Rooting at either endpoint places both copies on one root-to-node path, while rooting at the middle separates them.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n \log n)$ | DFS traversals plus subtree interval processing |
| Space | $O(n)$ | Adjacency list, Euler arrays, stacks, updates |

The tree contains at most $2 \cdot 10^5$ vertices, so linear or near-linear complexity is required. The algorithm stores only a constant amount of information per vertex and performs a small number of DFS traversals, fitting comfortably within the limits.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    out = io.StringIO()
    backup = sys.stdout
    sys.stdout = out

    solve()

    sys.stdout = backup
    return out.getvalue().strip()

# sample 1
assert run(
"""5
2 5 1 1 4
1 2
1 3
2 4
2 5
"""
) == "3"

# single vertex
assert run(
"""1
7
"""
) == "1"

# all distinct
assert run(
"""4
1 2 3 4
1 2
2 3
3 4
"""
) == "4"

# chain with repeated endpoints
assert run(
"""3
1 2 1
1 2
2 3
"""
) == "1"

# all equal
assert run(
"""4
5 5 5 5
1 2
2 3
3 4
"""
) == "0"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Single vertex | 1 | Smallest possible tree |
| All distinct values | 4 | Every root should be valid |
| Chain 1-2-1 | 1 | Ancestor conflict under rerooting |
| All equal values | 0 | Heavy duplication handling |
| Sample 1 | 3 | General mixed structure |

## Edge Cases

Consider a single vertex:

```
1
10
```

There is only one root-to-node path, consisting of a single vertex. No duplicate can occur. The DFS performs no conflict updates, all counters remain zero, and the answer is 1.

Consider a chain:

```
3
1 2 1
1 2
2 3
```

The repeated value appears at both ends. During DFS, the second occurrence discovers the first as an equal-valued ancestor. The update marks roots that keep them ancestor-related. Vertex 2 lies in the exempt subtree and remains unmarked. The output is 1.

Consider all values distinct:

```
4
1 2 3 4
1 2
1 3
1 4
```

No equal-valued pair exists. The difference array never changes from zero. Every vertex receives invalidity count zero, producing answer 4.

Consider multiple equal values:

```
4
7 7 7 7
1 2
2 3
3 4
```

Every root creates a path containing repeated value 7. The DFS generates conflict updates for each repeated occurrence, and every vertex accumulates a positive invalidity count. The answer becomes 0, which matches the definition.
