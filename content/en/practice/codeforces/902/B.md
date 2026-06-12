---
title: "CF 902B - Coloring a Tree"
description: "We are given a rooted tree with n vertices, where vertex 1 is the root. Each vertex must be colored with a target color specified in the input. Initially, all vertices are color 0."
date: "2026-06-12T22:46:58+07:00"
tags: ["codeforces", "competitive-programming", "dfs-and-similar", "dsu", "greedy"]
categories: ["algorithms"]
codeforces_contest: 902
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 453 (Div. 2)"
rating: 1200
weight: 902
solve_time_s: 277
verified: true
draft: false
---

[CF 902B - Coloring a Tree](https://codeforces.com/problemset/problem/902/B)

**Rating:** 1200  
**Tags:** dfs and similar, dsu, greedy  
**Solve time:** 4m 37s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a rooted tree with _n_ vertices, where vertex 1 is the root. Each vertex must be colored with a target color specified in the input. Initially, all vertices are color 0. A coloring operation consists of picking any vertex _v_ and a color _x_, and coloring all vertices in the subtree rooted at _v_ with _x_. The task is to find the minimum number of operations needed to achieve the target coloring for every vertex.

The input specifies the tree as a parent array, where each entry _p_i_ indicates the parent of vertex _i_. The colors are given as an array of size _n_. The output is a single integer: the minimum number of coloring operations.

The constraints tell us _n_ can be up to 10⁴. A brute-force simulation that explores all subsets of vertices or all possible sequences of operations would be far too slow, as the number of operations grows exponentially. We need a linear-time approach, ideally O(n), because we can afford roughly 10⁵ operations per second.

A subtle edge case arises when a child has the same target color as its parent. A naive approach might count coloring the child as a separate operation, but since a parent coloring would already set its subtree, no additional step is needed. Another case is when the root itself has a non-zero color: that must always be counted as the first operation, because initially all colors are zero. For instance, if the root is color 2 and all children are color 2, the answer is still 1, not n.

## Approaches

The brute-force approach would attempt to color each vertex individually or recursively simulate every possible subtree coloring. One could imagine starting from leaves and checking if coloring the parent helps, but keeping track of the exact state of the entire tree after each operation is cumbersome and slow. In the worst case, this leads to O(n²) operations, because each operation might require traversing an entire subtree.

The key insight is that we do not need to explicitly simulate subtree coloring. Observe that a coloring operation only matters when the color of a vertex differs from the color it would inherit from its parent. If a vertex has the same color as its parent, it is already correctly colored once the parent’s subtree is colored. Conversely, if a vertex differs from its parent, we must perform a coloring operation at this vertex or one of its ancestors that includes it. Therefore, the optimal strategy is to traverse the tree and count each vertex whose color differs from its parent. The root is treated specially: since it has no parent, any non-zero color at the root always counts as one operation.

This observation reduces the problem to a single DFS over the tree. For each vertex, we compare its target color to its parent’s target color and increment the operation count if they differ.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n²) | O(n) | Too slow |
| Optimal | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Parse the input to build the tree as an adjacency list. Each vertex keeps a list of its children for easy traversal.
2. Initialize a counter for operations. If the root’s color is non-zero, increment the counter by one. This represents the first coloring operation at the root.
3. Perform a DFS starting from the root. For each vertex visited, compare its target color with the color of its parent. If the colors differ, increment the operation counter. The reasoning is that any vertex with a color different from its parent cannot inherit the parent’s coloring and thus requires an explicit operation.
4. Recursively continue the DFS for all children. Since the tree is connected and acyclic, this traversal visits each vertex exactly once.
5. After the DFS finishes, the counter contains the minimum number of operations needed.

Why it works: Every vertex whose color matches its parent is automatically handled by the coloring operation of the parent. Only vertices with differing colors require explicit operations. By traversing the tree once and counting these vertices, we account for all necessary operations without redundancy. The DFS guarantees that we do not miss any vertex, and the subtree property of coloring ensures that counting only parent-child color differences suffices.

## Python Solution

```python
import sys
input = sys.stdin.readline
sys.setrecursionlimit(100000)

def main():
    n = int(input())
    parents = list(map(int, input().split()))
    colors = list(map(int, input().split()))
    
    tree = [[] for _ in range(n)]
    for i, p in enumerate(parents, start=1):
        tree[p-1].append(i)
    
    operations = 0
    
    def dfs(v, parent_color):
        nonlocal operations
        if colors[v] != parent_color:
            operations += 1
        for child in tree[v]:
            dfs(child, colors[v])
    
    dfs(0, 0)
    print(operations)

if __name__ == "__main__":
    main()
```

The solution begins by constructing the tree from the parent array. The DFS function takes the current vertex and the color of its parent. For each vertex, we increment the operations counter if its color differs from the parent. We pass the current vertex’s color down to its children so they can make the same comparison. Using `sys.setrecursionlimit` ensures that the DFS does not hit recursion limits for large trees.

## Worked Examples

**Sample 1**

Input:

```
6
1 2 2 1 5
2 1 1 1 1 1
```

| Vertex | Parent | Color | Parent Color | Counted? |
| --- | --- | --- | --- | --- |
| 1 | - | 2 | 0 | Yes |
| 2 | 1 | 1 | 2 | Yes |
| 3 | 2 | 1 | 1 | No |
| 4 | 2 | 1 | 1 | No |
| 5 | 1 | 1 | 2 | Yes |
| 6 | 5 | 1 | 1 | No |

Total operations: 3

**Sample 2**

Input:

```
7
1 1 2 2 3 3
3 1 1 2 1 3 3
```

| Vertex | Parent | Color | Parent Color | Counted? |
| --- | --- | --- | --- | --- |
| 1 | - | 3 | 0 | Yes |
| 2 | 1 | 1 | 3 | Yes |
| 3 | 1 | 1 | 3 | Yes |
| 4 | 2 | 2 | 1 | Yes |
| 5 | 2 | 1 | 1 | No |
| 6 | 3 | 3 | 1 | Yes |
| 7 | 3 | 3 | 1 | Yes |

Total operations: 6

These traces show that each vertex is counted exactly once if and only if its color differs from its parent, which matches the logic of the DFS.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | We traverse each vertex once in the DFS, and building the adjacency list takes O(n). |
| Space | O(n) | The adjacency list and recursion stack use O(n) memory. |

Since n ≤ 10⁴, the algorithm fits comfortably within the 1-second time limit and 256 MB memory limit.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()
    exec(open(__file__).read())
    return sys.stdout.getvalue().strip()

# Provided samples
assert run("6\n1 2 2 1 5\n2 1 1 1 1 1\n") == "3", "sample 1"
assert run("7\n1 1 2 2 3 3\n3 1 1 2 1 3 3\n") == "6", "sample 2"

# Minimum input
assert run("2\n1\n1 2\n") == "2", "minimum input"

# All equal colors
assert run("5\n1 1 2 2\n1 1 1 1 1\n") == "1", "all equal"

# Maximum size linear tree
inp = "10000\n" + " ".join(str(i) for i in range(1,10000)) + "\n" + " ".join(["1"]*10000) + "\n"
assert run(inp) == "1", "linear tree all same"

# Alternating colors
inp = "4\n1 2 3\n1 2 1 2\n"
assert run(inp) == "4", "alternating colors"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 2 vertices, different colors | 2 | Minimum-size input and parent-child difference |
| 5 vertices, all same color | 1 | Single operation suffices for uniform color |
| Linear tree 10⁴ vertices, all same | 1 | Maximum size, confirms O(n) efficiency |
| Alternating colors | 4 | Each vertex differs from parent, counting correctness |

## Edge Cases

For the root having a non-zero color with all children sharing the same color, the DFS correctly counts the root as one operation, and no additional operations are counted for children. Input:

```
3
1 1
2 2 2
```

DFS starts at root 1 with parent color
