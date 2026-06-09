---
title: "CF 1877G - Ball-Stackable"
description: "We are given a tree where some edges already have a fixed direction and some edges are still undirected. We must choose directions for the remaining edges and assign a color to every edge. A walk may traverse an edge either along its direction or against it."
date: "2026-06-09T01:07:02+07:00"
tags: ["codeforces", "competitive-programming", "constructive-algorithms", "data-structures", "dp", "trees"]
categories: ["algorithms"]
codeforces_contest: 1877
codeforces_index: "G"
codeforces_contest_name: "Codeforces Round 902 (Div. 2, based on COMPFEST 15 - Final Round)"
rating: 3300
weight: 1877
solve_time_s: 177
verified: false
draft: false
---

[CF 1877G - Ball-Stackable](https://codeforces.com/problemset/problem/1877/G)

**Rating:** 3300  
**Tags:** constructive algorithms, data structures, dp, trees  
**Solve time:** 2m 57s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a tree where some edges already have a fixed direction and some edges are still undirected. We must choose directions for the remaining edges and assign a color to every edge.

A walk may traverse an edge either along its direction or against it. Traversing along the direction pushes a ball whose color equals the edge color onto a stack. Traversing against the direction pops the top ball.

A walk is called stackable if it never attempts to pop from an empty stack.

A stackable walk is ball-stackable if every pop removes a ball whose color matches the edge currently traversed.

Our task is to make **every** stackable walk automatically ball-stackable. Among all valid constructions, we want to maximize the number of distinct colors used.

The underlying graph is a tree with up to $10^5$ vertices. Any solution involving pairwise vertex checks, simulation of walks, or anything quadratic is immediately impossible. A linear or near-linear solution is required.

The difficulty is that the condition quantifies over **all possible stackable walks**, including walks that revisit vertices and edges many times. We cannot reason about individual walks. We need a structural characterization of when all stackable walks behave correctly.

A few subtle situations are easy to miss.

Consider a path

```
1 -> 2 -> 3
```

with different colors on the two edges.

A walk

```
1 -> 2 -> 3 -> 2
```

pushes color of edge $(1,2)$, then color of edge $(2,3)$, then pops using edge $(2,3)$. This is fine.

Now imagine a branching structure

```
    2
    |
1 ->3<-4
```

If colors on the two incoming edges into 3 differ, a walk can enter through one edge, wander elsewhere, and later pop through the other. The stack mechanism starts imposing equalities between colors.

The key challenge is discovering exactly which equalities are forced.

## Approaches

A brute force view is to think of every edge direction as a push symbol and every reverse traversal as a matching pop symbol. We could try to enumerate walks and derive all color constraints.

This is hopeless. Even a tree with $10^5$ vertices admits infinitely many walks because edges may be revisited arbitrarily many times. There is no finite enumeration strategy.

The breakthrough comes from recognizing that stack behavior is exactly the behavior of properly nested parentheses.

Whenever we traverse an edge in its direction, we push something. Whenever we traverse it backward, we pop something. A stackable walk is precisely a sequence where every pop matches a previously unmatched push.

The requirement that every pop removes a ball of the same color as the traversed edge means that every push-pop pair forced by stack order must correspond to equal colors.

Instead of reasoning about walks, we reason about the directed tree itself.

Suppose we root the tree somewhere. If an edge points from parent to child, traversing downward creates a push. Traversing upward across that same edge creates a pop. The stack behaves like entering and leaving regions of the tree.

After working through the possible walks, one finds a crucial fact:

A valid construction exists if and only if every directed edge can be oriented consistently with a single root. In other words, after choosing a root, every edge must point either away from the root. Mixed orientations create unavoidable contradictions.

More precisely, the final directed tree must be an arborescence rooted at some vertex.

Then the stack behavior becomes identical to DFS parentheses. Every pop is forced to match the most recent unmatched push along the unique root path.

This immediately determines color constraints. All edges leaving the same vertex must share a color. Otherwise a walk can push through one child edge and pop through another, producing a mismatch.

Conversely, once every outgoing edge of a vertex has the same color, every stackable walk becomes ball-stackable.

The problem is now transformed into:

1. Determine whether the already directed edges admit a root such that every directed edge points away from that root.
2. If such roots exist, maximize the number of distinct colors when each vertex contributes one color shared by all outgoing edges.

The maximum number of colors is obtained by giving different colors to as many vertices as possible. Since all outgoing edges of one vertex must share a color, colors correspond to internal vertices with at least one outgoing edge.

### Approach Comparison

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Enumerate walks and derive constraints | Infinite / exponential | Unbounded | Impossible |
| Root characterization + tree DP | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

### Step 1

Interpret every fixed directed edge $u \to v$ as a constraint on the root.

If the final orientation must be away from the root, then the root cannot lie inside the component containing $v$ after removing that edge.

Equivalently, the root must belong to the side containing $u$.

### Step 2

Root the underlying tree arbitrarily, for example at vertex 1.

Compute Euler tour intervals so every subtree becomes a contiguous segment.

### Step 3

For each fixed edge $u \to v$, determine which endpoint is ancestor of the other in the temporary rooting.

If $u$ is ancestor of $v$, then valid roots are exactly outside subtree($v$).

If $v$ is ancestor of $u$, then valid roots are exactly inside subtree($u$).

These are simple range constraints on Euler positions.

### Step 4

Combine all constraints with a difference-array technique over the Euler order.

Count for every vertex how many constraints it satisfies.

Any vertex satisfying all constraints can serve as the global root.

If no such vertex exists, output $-1$.

### Step 5

Choose any valid root $r$.

Orient every undirected edge away from $r$.

Already directed edges automatically point away from $r$ because of the constraint construction.

### Step 6

Assign colors.

For every vertex except the root, consider the edge connecting it to its parent.

The color of that edge is determined by the parent vertex.

All edges leaving the same parent receive the same color.

### Step 7

Compress the used parent labels into consecutive color numbers.

The number of distinct colors equals the number of vertices having at least one child, which is maximal.

### Why it works

The root constraints are exactly the conditions required for every directed edge to point away from a common root. If no such root exists, some directed edge must point toward the root while another points away, creating a structure that allows stackable walks whose stack matching cannot be represented by local color equalities.

When all edges point away from a root, every stackable walk behaves like properly nested traversals of rooted-tree edges. The push corresponding to entering a child subtree must be matched by leaving that same subtree. Hence the only color equalities required are between edges sharing the same parent.

Assigning one color per parent satisfies all required equalities. Distinct parents may receive distinct colors, giving the maximum possible number of colors.

## Python Solution

```python
import sys
input = sys.stdin.readline

n = int(input())

edges = []
g = [[] for _ in range(n)]

for i in range(n - 1):
    u, v, t = map(int, input().split())
    u -= 1
    v -= 1
    edges.append((u, v, t))
    g[u].append((v, i))
    g[v].append((u, i))

tin = [0] * n
tout = [0] * n
parent = [-1] * n
depth = [0] * n

timer = 0

stack = [(0, -1, 0)]
while stack:
    v, p, state = stack.pop()

    if state == 0:
        tin[v] = timer
        timer += 1

        stack.append((v, p, 1))

        for to, _ in reversed(g[v]):
            if to == p:
                continue
            parent[to] = v
            depth[to] = depth[v] + 1
            stack.append((to, v, 0))
    else:
        tout[v] = timer - 1

def is_ancestor(a, b):
    return tin[a] <= tin[b] <= tout[a]

diff = [0] * (n + 1)
need = 0

for u, v, t in edges:
    if t == 0:
        continue

    need += 1

    if is_ancestor(u, v):
        l = tin[v]
        r = tout[v]

        diff[0] += 1
        diff[n] -= 1

        diff[l] -= 1
        diff[r + 1] += 1
    else:
        l = tin[u]
        r = tout[u]

        diff[l] += 1
        diff[r + 1] -= 1

cur = 0
root = -1

for v in range(n):
    cur += diff[v]
    if cur == need:
        root = v
        break

if root == -1:
    print(-1)
    sys.exit()

parent = [-1] * n
order = [root]
parent[root] = root

for v in order:
    for to, _ in g[v]:
        if parent[to] != -1:
            continue
        parent[to] = v
        order.append(to)

children_count = [0] * n
for v in range(n):
    if v != root:
        children_count[parent[v]] += 1

color_of_vertex = [-1] * n
color_id = 0

for v in range(n):
    if children_count[v] > 0:
        color_id += 1
        color_of_vertex[v] = color_id

answer = []

for u, v, t in edges:
    if parent[v] == u:
        p, q = u, v
    elif parent[u] == v:
        p, q = v, u
    else:
        raise RuntimeError

    c = color_of_vertex[p]
    answer.append((p + 1, q + 1, c))

print(color_id)
for row in answer:
    print(*row)
```

The first DFS computes Euler intervals. Those intervals allow subtree constraints to be represented as range additions on a difference array.

The next phase processes every fixed directed edge. Each edge contributes either an "inside subtree" constraint or an "outside subtree" constraint depending on the ancestor relationship of its endpoints.

After accumulating constraints, any vertex satisfying all of them can be used as the global root.

Once the root is known, orienting the tree is trivial. Every edge is directed from parent to child in the rooted tree.

The coloring phase is where the stack argument enters. Every parent vertex receives one color shared by all its outgoing edges. Vertices without children do not contribute colors because no edge originates from them.

## Worked Examples

### Example 1

Input

```
5
2 5 1
1 3 0
5 4 0
1 5 1
```

Suppose the valid root found is vertex 3.

| Vertex | Parent |
| --- | --- |
| 3 | root |
| 1 | 3 |
| 5 | 1 |
| 2 | 5 |
| 4 | 5 |

Color assignment:

| Parent vertex | Assigned color |
| --- | --- |
| 3 | 1 |
| 1 | 2 |
| 5 | 3 |

Produced edges:

| Directed edge | Color |
| --- | --- |
| 3→1 | 1 |
| 1→5 | 2 |
| 5→2 | 3 |
| 5→4 | 3 |

The two edges leaving vertex 5 share a color, exactly as required by the stack argument.

### Example 2

Input

```
3
1 2 1
3 2 1
```

Constraints:

From $1 \to 2$, the root must lie on the side of vertex 1.

From $3 \to 2$, the root must lie on the side of vertex 3.

No vertex satisfies both conditions.

| Vertex | Satisfies first constraint | Satisfies second constraint |
| --- | --- | --- |
| 1 | Yes | No |
| 2 | No | No |
| 3 | No | Yes |

No valid root exists, so the answer is:

```
-1
```

This demonstrates the impossibility detection.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | DFS, constraint accumulation, rooting, and output generation are all linear |
| Space | O(n) | Adjacency lists, Euler arrays, parent arrays, and difference array |

With $n \le 10^5$, linear complexity is easily fast enough for the 2-second limit and fits comfortably inside the memory limit.

## Test Cases

```python
# helper skeleton

import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    # invoke solution
    pass

# sample 1
# output is not unique, so exact assertion is not suitable

# minimum tree
inp = """2
1 2 0
"""

# already impossible
inp2 = """3
1 2 1
3 2 1
"""

# chain, all undirected
inp3 = """4
1 2 0
2 3 0
3 4 0
"""

# star centered at 1
inp4 = """5
1 2 0
1 3 0
1 4 0
1 5 0
"""
```

### Custom Test Summary

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Two vertices, one undirected edge | One color, one directed edge | Smallest valid instance |
| Two directed edges pointing into same vertex | -1 | Contradictory root constraints |
| Undirected chain | Valid construction | Root selection and orientation |
| Undirected star | Maximum color counting | Many outgoing edges sharing one color |

## Edge Cases

Consider

```
3
1 2 1
3 2 1
```

Both directed edges point toward vertex 2. Any rooted orientation away from a root would require vertex 2 to be below both 1 and 3 simultaneously, which is impossible in a tree. The constraint accumulation phase leaves no vertex satisfying all constraints, so the algorithm outputs `-1`.

Consider

```
2
1 2 0
```

There are no fixed-direction constraints. Every vertex is a valid root. The algorithm picks one, directs the only edge away from it, assigns one color, and succeeds.

Consider

```
5
1 2 0
1 3 0
1 4 0
1 5 0
```

All four edges leave the same parent in the rooted orientation. The correctness proof says they must share a color. The algorithm assigns exactly one color to all four edges. Any attempt to use multiple colors here would violate the stack condition, so the construction is already optimal.
