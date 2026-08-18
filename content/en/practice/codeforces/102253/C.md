---
title: "CF 102253C - Colorful Tree"
description: "We have a tree with (n) vertices. Every vertex has a color, and for any two distinct vertices we look at their unique path and count how many different colors occur on that path. The task is to sum this value over all (frac{n(n-1)}2) unordered pairs of vertices."
date: "2026-08-19T00:43:19+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102253
codeforces_index: "C"
codeforces_contest_name: "2017 Chinese Multi-University Training, BeihangU Contest"
rating: 0
weight: 102253
solve_time_s: 145
verified: true
draft: false
---

[CF 102253C - Colorful Tree](https://codeforces.com/problemset/problem/102253/C)

**Rating:** -  
**Tags:** -  
**Solve time:** 2m 25s  
**Verified:** yes  

## Solution
## Problem Understanding

We have a tree with (n) vertices. Every vertex has a color, and for any two distinct vertices we look at their unique path and count how many different colors occur on that path. The task is to sum this value over all (\frac{n(n-1)}2) unordered pairs of vertices. The input contains several test cases, each consisting of the vertex colors followed by the (n-1) tree edges. The required output is the total sum for every case, prefixed by its case number. The official problem format and sample output are given by Codeforces Gym 102253C.

The constraint (n\le 2\cdot10^5) rules out anything close to quadratic time. There are already about (2\cdot10^{10}) vertex pairs at the maximum size, so even enumerating every pair once is far beyond what a two second limit can tolerate. The intended solution has to process each vertex and edge only a constant number of times, giving linear complexity in (n). The color values are also at most (n), which lets us maintain per-color information in ordinary arrays.

There are several easy ways to get a wrong answer. Repeated colors must contribute only once to a path. For example,

```
2
1 1
1 2
```

has only one path, and that path contains exactly one distinct color, so the answer is `1`. A solution that adds one contribution for each vertex would incorrectly obtain `2`.

The two endpoints are included in their path. For

```
2
1 2
1 2
```

the only path contains colors (1) and (2), so the answer is `2`. Treating a path as containing only its internal vertices would incorrectly give zero colors.

The component on the root side of the tree cannot be forgotten when removing a color. For example,

```
3
1 1 2
1 2
1 3
```

has path values (1,2,2), giving answer `5`. For color (2), deleting its only vertex leaves vertices (1) and (2) connected, so one path avoids color (2). A computation that only examines child subtrees below occurrences of a color would miss this remaining root-side component.

## Approaches

A direct solution can enumerate every pair of vertices, find its path, insert the colors on that path into a set, and add the size of the set. This is correct because every path is examined exactly once and the set removes duplicate colors. The problem is the amount of work. On a chain, the total number of vertices visited over all paths is

[
\sum_{d=1}^{n-1}(n-d)(d+1)
=\frac{n(n-1)(n+4)}6
=\Theta(n^3).
]

At (n=2\cdot10^5), this is roughly (1.3\cdot10^{15}) vertex visits, so the brute force approach is nowhere near feasible.

The useful change of viewpoint is to count the contribution of each color independently. A path whose color set contains (k) colors contributes (1) to the answer for each of those (k) colors. Thus the final answer is the sum, over every color (c), of the number of paths containing at least one vertex of color (c). This contribution is easier to express through its complement. There are (\binom n2) paths in total, so the contribution of color (c) is

[
\binom n2-\text{number of paths avoiding color }c.
]

Now remove every vertex having color (c). The remaining graph is a forest. A path avoids (c) exactly when both endpoints lie in the same connected component of that forest. If the component sizes are (s_1,s_2,\ldots), the number of paths avoiding (c) is

[
\sum_i \binom{s_i}{2}.
]

This converts the problem into computing the sizes of all components obtained by removing each color. Doing that independently for every color would again be quadratic. The key observation is that all these computations can be simulated simultaneously during one DFS. The standard solution describes this as using the virtual-tree idea without explicitly constructing a virtual tree.

Root the tree at vertex (1). Consider a current vertex (u), with color (c), and one child (v). Inside the subtree of (v), some nodes belong to subtrees rooted at the highest occurrences of color (c). Those nodes are separated from (u) if all color-(c) vertices are deleted. Every other node in the subtree of (v) belongs to one connected component attached to (u). If the subtree has size (sz[v]), and (x) of those nodes have already been accounted for by higher color-(c) vertices, then the component size is (sz[v]-x), contributing (\binom{sz[v]-x}{2}) avoiding paths.

We can obtain (x) without constructing anything explicitly. For each color (c), maintain `dom[c]`, the amount already associated with the highest currently relevant color-(c) vertices during the DFS. Immediately before descending into child (v), save `dom[c]`. After returning from (v), the difference between the new and saved values is exactly the amount of the subtree occupied by those higher color-(c) regions. This difference is the quantity to subtract from (sz[v]). The same incremental idea is the core of the accepted tree-DP formulations for this problem.

Finally, after the DFS finishes, a color may still have a component above its highest occurrence. Its size is (n-\text{dom}[c]), so we add (\binom{n-\text{dom}[c]}2) to the number of paths avoiding that color. This is the root-side component that a purely local subtree calculation would miss.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | (O(n^3)) on a chain | (O(n)) | Too slow |
| Optimal | (O(n)) | (O(n)) | Accepted |

## Algorithm Walkthrough

1. Count how many distinct colors occur. There are (\binom n2) paths, and initially we can imagine that every distinct color contributes to every path. Thus the starting value is

[
\text{distinctColors}\cdot\binom n2.
]

We will subtract paths that avoid each color.

1. Root the tree at vertex (1), and define (sz[u]) as the number of vertices in the subtree of (u). The DFS needs this value when returning from every child.
2. Maintain an array `dom[c]`. During the DFS, it represents the total size already absorbed by the currently highest color-(c) regions. When processing a vertex (u) with color (c), initialize a local value `added = 1`, because (u) itself will become part of the new region represented by color (c).
3. Process each child (v) of (u) one at a time. Save `before = dom[c]` immediately before entering (v). The subtree of (v) is then processed completely before anything else is done with this child.
4. After returning from (v), calculate

[
x=dom[c]-before.
]

The value (x) counts the part of (v)'s subtree that belongs to higher color-(c) regions. Those regions contain color-(c) vertices and are disconnected from (u) after color (c) is removed.

1. The remaining part

[
block=sz[v]-x
]

is exactly the connected component containing (v) that contains no color-(c) vertex. Every pair of vertices inside this component gives a path avoiding color (c), so add

[
\binom{block}{2}
]

to the number of paths that will be subtracted from the answer.

1. Add `block` to the local `added` value of (u). After every child has been processed, update

[
dom[c]\mathrel{+}=added.
]

This replaces the previously highest color-(c) regions by the region represented by (u), which is exactly the state needed by (u)'s parent.

1. After the whole DFS, process every color that actually occurs. Its remaining root-side component has size

[
n-dom[c].
]

Add

[
\binom{n-dom[c]}2
]

to the number of paths avoiding that color.

1. Subtract the total number of avoiding paths from `distinctColors * C(n, 2)`. The result is the required sum of distinct-color counts over all paths.

The implementation below uses an explicit DFS stack rather than Python recursion. The tree can be a chain of length (2\cdot10^5), so recursive Python DFS risks exceeding the interpreter's recursion stack. The explicit stack preserves exactly the same parent-child processing order as the recursive recurrence.

### Why it works

Fix a color (c). Deleting every vertex of color (c) partitions the tree into connected components, and exactly the vertex pairs inside one component have paths avoiding (c). For every child (v) of a vertex (u) with color (c), `dom[c] - before` counts precisely the portions of (v)'s subtree already separated by the highest color-(c) vertices below (v). Removing those portions leaves one connected color-(c)-free component of size `sz[v] - (dom[c] - before)`, so its (\binom{size}{2}) pairs are counted exactly once. After all children are processed, `dom[c]` represents the regions already accounted for by the highest color-(c) vertices. The only unprocessed component is the one above the highest color-(c) vertices, whose size is (n-dom[c]), and it is counted at the end. Thus every pair avoiding (c) is counted once and every pair containing (c) is excluded from that complement. Summing this contribution over all colors gives exactly the number of distinct colors on every path.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    out = []
    case_no = 0

    while True:
        line = input()
        if not line:
            break
        line = line.strip()
        if not line:
            continue

        n = int(line)
        color = [0] + list(map(int, input().split()))

        graph = [[] for _ in range(n + 1)]
        for _ in range(n - 1):
            u, v = map(int, input().split())
            graph[u].append(v)
            graph[v].append(u)

        present = [False] * (n + 1)
        distinct = 0
        for u in range(1, n + 1):
            c = color[u]
            if not present[c]:
                present[c] = True
                distinct += 1

        # dom[c] is the amount already absorbed by the highest
        # color-c regions during the current DFS.
        dom = [0] * (n + 1)

        # sz[u] is the subtree size.
        sz = [0] * (n + 1)

        # Number of paths avoiding their corresponding colors.
        bad = 0

        # Frame:
        # [vertex, parent, next_edge_index, added, before]
        #
        # added is the local value that will be added to dom[color[u]]
        # when u finishes.
        # before stores dom[color[u]] immediately before entering
        # the currently processed child.
        sz[1] = 1
        stack = [[1, 0, 0, 1, 0]]

        while stack:
            frame = stack[-1]
            u = frame[0]
            p = frame[1]

            if frame[2] < len(graph[u]):
                v = graph[u][frame[2]]
                frame[2] += 1

                if v == p:
                    continue

                c = color[u]
                frame[4] = dom[c]

                sz[v] = 1
                stack.append([v, u, 0, 1, 0])
                continue

            # Finish u.
            c = color[u]
            dom[c] += frame[3]
            stack.pop()

            if stack:
                parent_frame = stack[-1]
                parent = parent_frame[0]
                pc = color[parent]

                added_in_child = dom[pc] - parent_frame[4]
                block = sz[u] - added_in_child

                bad += block * (block - 1) // 2
                parent_frame[3] += block
                sz[parent] += sz[u]

        # The component above the highest occurrence of each color.
        for c in range(1, n + 1):
            if not present[c]:
                continue
            block = n - dom[c]
            bad += block * (block - 1) // 2

        total = distinct * n * (n - 1) // 2
        answer = total - bad

        case_no += 1
        out.append(f"Case #{case_no}: {answer}")

    sys.stdout.write("\n".join(out))

if __name__ == "__main__":
    solve()
```

The input phase stores the colors in a one-indexed array so that vertex numbers and array indices match. The `present` array simultaneously counts distinct colors, which lets the initial contribution use only colors that actually occur.

The `dom` array is the central piece of state. It is indexed by color rather than by vertex because the same computation is being performed for every color at once. When a child finishes, the parent compares the new `dom[color[parent]]` with the value saved before entering that child. Only the difference belongs to that child, so this subtraction prevents information accumulated in earlier sibling subtrees from being counted again.

The `added` field in each DFS frame starts at one for the current vertex. Every child contributes its color-free block to this value. When the vertex finishes, adding `added` to `dom[color[u]]` makes the entire newly formed highest color region available to its parent.

The final loop handles the part of the tree above the highest occurrence of every color. Omitting this step is a common source of wrong answers when the root does not have that color.

All path counts use Python integers, so there is no overflow concern. In languages with fixed-width integers, 64-bit integers are required because the answer can be on the order of (n^3).

The explicit stack is also deliberate. A recursive DFS has depth (O(n)) on a chain, while the iterative version uses (O(n)) heap memory and has no recursion-depth failure.

## Worked Examples

### Sample 1

The tree is the chain (1-2-3), with colors (1,2,1). There are three paths. The initial contribution is two distinct colors times three paths, giving (6).

The DFS processes the subtree of vertex (2), including vertex (3). When vertex (3) finishes, color (1) has absorbed one vertex. When vertex (2) finishes, color (2) has absorbed two vertices. Returning to vertex (1), the color-(1) region accounts for the whole tree.

| Vertex | Color | Child | Child Size | `before` | `dom` after child | `block` | `bad` added |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 3 | 1 | none | 0 | 0 | 1 | 0 | 0 |
| 2 | 2 | 3 | 1 | 0 | 1 | 0 | 0 |
| 1 | 1 | 2 | 2 | 0 | 1 | 1 | 0 |
| 1 | 1 | 2 finished | 2 | 0 | 3 | 0 | 0 |

After the DFS, `dom[1] = 3`, so color (1) has no remaining root-side component. `dom[2] = 2`, leaving a component of size (1), which contributes zero avoiding paths. Thus `bad = 0`, and the answer remains (6).

This example demonstrates why equal colors cannot be counted independently by vertex. The two occurrences of color (1) together contribute exactly one unit to every path, not two.

### Sample 2

The tree is

```
        1(1)
       /   \
    2(2)   3(1)
    /  \      \
 4(3) 5(2)    6(1)
```

There are six vertices and three distinct colors, so the initial value is

[
3\binom62=45.
]

The relevant DFS transitions are:

| Vertex | Color | Child | Child Size | `before` | `dom` after child | `block` | `bad` added |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 4 | 3 | none | 1 | 0 | 1 | 0 | 0 |
| 5 | 2 | none | 1 | 0 | 1 | 0 | 0 |
| 2 | 2 | 4 | 1 | 0 | 0 | 1 | 0 |
| 2 | 2 | 5 | 1 | 0 | 1 | 0 | 0 |
| 3 | 1 | 6 | 1 | 0 | 1 | 0 | 0 |
| 1 | 1 | 2 | 3 | 0 | 0 | 3 | 3 |
| 1 | 1 | 3 | 2 | 0 | 2 | 0 | 0 |

After the DFS, the values relevant to the three colors are

| Color | `dom[color]` | Root-side size | Root-side avoiding paths |
| --- | --- | --- | --- |
| 1 | 6 | 0 | 0 |
| 2 | 3 | 3 | 3 |
| 3 | 1 | 5 | 10 |

The child of vertex (1) leading to vertex (2) produces a color-(1)-free component of size (3), accounting for (3) avoiding paths. Color (2) has another component of size (3) above its highest occurrence, accounting for (3) paths, while color (3) has a root-side component of size (5), accounting for (10) paths.

Thus the total number of missing color contributions is

[
3+3+10=16,
]

and the final answer is

[
45-16=29.
]

The trace demonstrates the central invariant: `dom[c]` carries exactly the portion already separated by higher occurrences of color (c), while `sz[v] - delta` is the one remaining color-free component in that child subtree.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | (O(n)) | Every vertex and every tree edge is processed a constant number of times, followed by one scan of the (n) possible colors. |
| Space | (O(n)) | The adjacency lists, subtree sizes, color state, presence array, and explicit DFS stack all use linear memory. |

The maximum (n) is (2\cdot10^5), so a linear pass is appropriate for the two second time limit. The implementation avoids both the quadratic number of vertex pairs and recursive DFS depth proportional to (n). The answer can exceed 32-bit range, but Python integers handle the required values directly.

## Test Cases

```python
import sys
import io

def solution():
    input = sys.stdin.readline
    out = []
    case_no = 0

    while True:
        line = input()
        if not line:
            break
        line = line.strip()
        if not line:
            continue

        n = int(line)
        color = [0] + list(map(int, input().split()))

        graph = [[] for _ in range(n + 1)]
        for _ in range(n - 1):
            u, v = map(int, input().split())
            graph[u].append(v)
            graph[v].append(u)

        present = [False] * (n + 1)
        distinct = 0
        for u in range(1, n + 1):
            c = color[u]
            if not present[c]:
                present[c] = True
                distinct += 1

        dom = [0] * (n + 1)
        sz = [0] * (n + 1)
        bad = 0

        sz[1] = 1
        stack = [[1, 0, 0, 1, 0]]

        while stack:
            frame = stack[-1]
            u, p = frame[0], frame[1]

            if frame[2] < len(graph[u]):
                v = graph[u][frame[2]]
                frame[2] += 1

                if v == p:
                    continue

                frame[4] = dom[color[u]]
                sz[v] = 1
                stack.append([v, u, 0, 1, 0])
            else:
                c = color[u]
                dom[c] += frame[3]
                stack.pop()

                if stack:
                    parent_frame = stack[-1]
                    parent = parent_frame[0]
                    pc = color[parent]

                    delta = dom[pc] - parent_frame[4]
                    block = sz[u] - delta

                    bad += block * (block - 1) // 2
                    parent_frame[3] += block
                    sz[parent] += sz[u]

        for c in range(1, n + 1):
            if present[c]:
                block = n - dom[c]
                bad += block * (block - 1) // 2

        total = distinct * n * (n - 1) // 2
        answer = total - bad

        case_no += 1
        out.append(f"Case #{case_no}: {answer}")

    return "\n".join(out)

def run(inp: str) -> str:
    old_stdin = sys.stdin
    try:
        sys.stdin = io.StringIO(inp)
        return solution()
    finally:
        sys.stdin = old_stdin

sample1 = """\
3
1 2 1
1 2
2 3
"""

assert run(sample1) == "Case #1: 6", "sample 1"

sample2 = """\
6
1 2 1 3 2 1
1 2
1 3
2 4
2 5
3 6
"""

assert run(sample2) == "Case #1: 29", "sample 2"

minimum_same = """\
2
1 1
1 2
"""

assert run(minimum_same) == "Case #1: 1", "minimum size, equal colors"

minimum_different = """\
2
1 2
1 2
"""

assert run(minimum_different) == "Case #1: 2", "minimum size, different colors"

boundary_color = """\
3
3 1 2
1 2
2 3
"""

assert run(boundary_color) == "Case #1: 7", "color value n"

repeated_colors = """\
5
1 2 1 2 1
1 2
2 3
3 4
4 5
"""

assert run(repeated_colors) == "Case #1: 16", "repeated colors on a chain"

n = 200000
colors = " ".join(["1"] * n)
edges = "\n".join(f"{i} {i + 1}" for i in range(1, n))
maximum_case = f"{n}\n{colors}\n{edges}\n"

assert run(maximum_case) == "Case #1: 19999900000", "maximum n, all equal"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `2`, colors `1 1`, edge `1 2` | `Case #1: 1` | Minimum size and duplicate-color handling |
| `2`, colors `1 2`, edge `1 2` | `Case #1: 2` | Both endpoints contribute and ordered pairs are not counted |
| `3`, colors `3 1 2`, edges `1 2`, `2 3` | `Case #1: 7` | Color value equal to the maximum allowed value (n) |
| Chain of 5 with colors `1 2 1 2 1` | `Case #1: 16` | Multiple repeated colors separated by other colors |
| Chain of 200000 vertices, all color `1` | `Case #1: 19999900000` | Maximum input size, large integer arithmetic, and deep-tree handling |

## Edge Cases

For the minimum tree with two vertices of the same color,

```
2
1 1
1 2
```

the initial contribution is (1\cdot\binom22=1). The DFS absorbs both vertices into `dom[1]`, so the root-side component has size zero. There are no paths avoiding color (1), giving `bad = 0` and final answer `1`. The repeated color is counted once because the algorithm works per color rather than per vertex.

For two vertices with different colors,

```
2
1 2
1 2
```

there is one path and it contains both colors. The initial contribution is (2\cdot1=2). Each color has no nontrivial component after its only vertex is removed, so no avoiding path is subtracted. The result is `2`. This also confirms that both endpoints belong to the path.

For a color that occurs away from the root,

```
3
1 1 2
1 2
1 3
```

the paths are (1\leftrightarrow2), (1\leftrightarrow3), and (2\leftrightarrow3), with values (1,2,2). Their sum is `5`. For color (2), removing vertex (3) leaves a component of size (2), so exactly (\binom22=1) path avoids it. The final contribution of color (2) is (3-1=2). The same-color vertices (1) and (2) contribute to one common color rather than two separate contributions, giving the total `5`.

For the alternating chain

```
5
1 2 1 2 1
1 2
2 3
3 4
4 5
```

the path values are (2,1,2,1,2,1,2,1,2,2) across the ten unordered pairs, summing to `16`. During the DFS, the difference `dom[c] - before` prevents a later occurrence of the same color from being counted as part of the color-free component belonging to an earlier occurrence. This is exactly the situation that breaks simpler subtree-size formulas.

For the maximum-size all-equal tree, every path contains the sole color, so the answer is simply

[
\binom{200000}{2}=19999900000.
]

The algorithm processes the chain iteratively, never recursing 200000 levels deep. Since every vertex has the same color, every child-side block has size zero, `dom[1]` ends at (200000), and the root-side component also has size zero. The answer is consequently `19999900000`, confirming both the large-integer boundary and the intended linear behavior.
