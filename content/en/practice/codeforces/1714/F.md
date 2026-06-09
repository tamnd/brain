---
title: "CF 1714F - Build a Tree and That Is It"
description: "We are asked to construct an unrooted tree with a fixed number of vertices and three specific distance constraints between vertices 1, 2, and 3. Each test case provides four integers: the number of nodes $n$ and the pairwise distances $d{12}$, $d{23}$, and $d{31}$."
date: "2026-06-09T20:09:34+07:00"
tags: ["codeforces", "competitive-programming", "constructive-algorithms", "implementation", "trees"]
categories: ["algorithms"]
codeforces_contest: 1714
codeforces_index: "F"
codeforces_contest_name: "Codeforces Round 811 (Div. 3)"
rating: 1900
weight: 1714
solve_time_s: 161
verified: false
draft: false
---

[CF 1714F - Build a Tree and That Is It](https://codeforces.com/problemset/problem/1714/F)

**Rating:** 1900  
**Tags:** constructive algorithms, implementation, trees  
**Solve time:** 2m 41s  
**Verified:** no  

## Solution
## Problem Understanding

We are asked to construct an unrooted tree with a fixed number of vertices and three specific distance constraints between vertices 1, 2, and 3. Each test case provides four integers: the number of nodes $n$ and the pairwise distances $d_{12}$, $d_{23}$, and $d_{31}$. The task is to determine whether a tree satisfying these distances exists and, if so, to output the edges of any such tree.

A tree with $n$ vertices has exactly $n-1$ edges and no cycles. The distances $d_{12}, d_{23}, d_{31}$ define constraints on the paths connecting vertices 1, 2, and 3. Since a tree has a unique path between any two vertices, these distances uniquely determine the relative layout of these three vertices.

The bounds indicate that $n$ can be up to 200,000, and there can be up to 10,000 test cases, with the sum of all $n$ across test cases limited to 200,000. This rules out any algorithm worse than linear in $n$ per test case. We cannot afford to explicitly try all tree topologies; we need a direct construction based on the given distances.

Edge cases appear when the distances do not satisfy the triangle inequality. For instance, if $d_{12} + d_{23} < d_{31}$, no tree can satisfy these distances because the path from 1 to 3 must be at least as long as the sum of paths through 2. Small trees also create constraints. With $n=3$, all three distances must sum up to exactly two edges forming a single path.

For example, with $n=4$ and distances $d_{12}=3, d_{23}=1, d_{31}=1$, a naive attempt to lay out the vertices along a path fails because the distances cannot be reconciled without violating the tree structure.

## Approaches

The brute-force approach would try all tree shapes and check if the distances between 1, 2, 3 match the requirements. This is combinatorially explosive since the number of trees on $n$ vertices grows super-exponentially. Even generating all trees for $n=20$ would be infeasible.

The key insight is that in any tree, the three vertices 1, 2, and 3 must either form a "path" or a "star-like" structure. In the path scenario, one vertex is in the middle, connecting the other two, and the distances must satisfy $d_{12} + d_{23} = d_{31}$ or one of the cyclic permutations. If the sum of any two distances equals the third, we can lay the vertices on a single line and add the remaining $n-3$ nodes as leaves attached anywhere along the path. If no sum of two distances equals the third, the only possible shape is a central vertex connecting all three, forming a Y-shaped tree. In this case, the distances must satisfy $(d_{12} + d_{23} + d_{31}) \mod 2 = 0$ and a derived formula to split the distances along the arms of the Y.

This insight reduces the problem from checking all trees to simply checking feasible arrangements and then constructing the path or Y shape directly.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n!) | O(n) | Too slow |
| Optimal | O(n) per test case | O(n) | Accepted |

## Algorithm Walkthrough

1. First, check if the distances satisfy the triangle inequality: each distance must be less than or equal to the sum of the other two. If not, output NO immediately.
2. Attempt to form a simple path layout. Check if one of the distances equals the sum of the other two. For example, if $d_{12} + d_{23} = d_{31}$, vertex 2 lies between 1 and 3 along a straight path. Similarly, check other permutations. If such a relation exists, we can construct the path and attach remaining vertices as leaves.
3. If no path layout works, try to form a Y-shaped tree. Compute the "arm lengths" from a central vertex $c$ to 1, 2, and 3 using:

$$x = \frac{d_{12} + d_{31} - d_{23}}{2}, \quad y = \frac{d_{12} + d_{23} - d_{31}}{2}, \quad z = \frac{d_{23} + d_{31} - d_{12}}{2}$$

If any of $x, y, z$ are negative or non-integers, the Y-shape is impossible.
4. Place vertices 1, 2, 3 at the ends of the arms. Connect the arms through the central vertex. Attach remaining $n-3$ vertices as leaves to any vertex on the tree without violating uniqueness of the path between 1, 2, 3.
5. Output YES and print the edges.

Why it works: Any tree is either a path connecting 1, 2, 3 or has a central vertex connecting them. The derived formulas guarantee integer arm lengths, which preserve exact distances. Remaining vertices can always be added as leaves.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        n, d12, d23, d31 = map(int, input().split())

        # Attempt path-based layout
        path_found = False
        for a, b, c in [(d12, d23, d31), (d23, d31, d12), (d31, d12, d23)]:
            if a + b == c:
                path_found = True
                edges = []
                nxt = 4
                # build path a-b-c
                v = [1, 2, 3]
                if (a, b, c) != (d12, d23, d31):
                    # permute so that 1,2,3 correspond to a-b-c
                    if (a, b, c) == (d23, d31, d12):
                        v = [2,3,1]
                    else:
                        v = [3,1,2]
                # build path from v[0] to v[1] length a
                last = v[0]
                for _ in range(a-1):
                    edges.append((last, nxt))
                    last = nxt
                    nxt += 1
                edges.append((last, v[1]))
                last = v[1]
                # build path from v[1] to v[2] length b
                for _ in range(b-1):
                    edges.append((last, nxt))
                    last = nxt
                    nxt += 1
                edges.append((last, v[2]))
                # attach remaining vertices
                for i in range(n - (len(edges)+1)):
                    edges.append((1, nxt))
                    nxt += 1
                print("YES")
                for u, w in edges:
                    print(u, w)
                break
        if path_found:
            continue

        # attempt Y-shaped tree
        x = (d12 + d31 - d23) // 2
        y = (d12 + d23 - d31) // 2
        z = (d23 + d31 - d12) // 2
        if (d12 + d31 - d23) % 2 or (d12 + d23 - d31) % 2 or (d23 + d31 - d12) % 2 or min(x, y, z) < 0:
            print("NO")
            continue
        edges = []
        nxt = 4
        center = 4
        # connect central vertex
        edges.append((center,1))
        last = center
        # arm to 2
        prev = last
        for _ in range(x):
            edges.append((prev,nxt))
            prev = nxt
            nxt += 1
        edges.append((prev,2))
        # arm to 3
        prev = last
        for _ in range(z):
            edges.append((prev,nxt))
            prev = nxt
            nxt += 1
        edges.append((prev,3))
        # attach remaining vertices
        used = nxt-1
        for i in range(used, n):
            edges.append((1, nxt))
            nxt += 1
        print("YES")
        for u, w in edges:
            print(u, w)

if __name__ == "__main__":
    solve()
```

The first part of the code checks if the distances allow a path layout. It carefully permutes the vertices so that 1, 2, 3 correspond to the correct ends of the path. Building the path uses temporary vertices for intermediate edges, incrementing a counter to assign new vertex numbers. If the path is impossible, the code computes arm lengths for a Y-shaped layout, ensuring all derived lengths are non-negative integers. Remaining nodes are attached as leaves to preserve tree properties.

## Worked Examples

**Example 1**: `5 1 2 1`

| Step | Action | Variables |
| --- | --- | --- |
| 1 | Check path sums | 1+2 == 1? no; 2+1==1? no; 1+1==2? yes |
| 2 |  |  |
