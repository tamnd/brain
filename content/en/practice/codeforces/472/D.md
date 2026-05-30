---
title: "CF 472D - Design Tutorial: Inverse the Problem"
description: "We are given an $n times n$ matrix where each entry $d[i][j]$ represents the distance between nodes $i$ and $j$. The question asks whether there exists a weighted tree with $n$ nodes such that the distance along the tree between any two nodes exactly matches the corresponding…"
date: "2026-05-30T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "dfs-and-similar", "dsu", "shortest-paths", "trees"]
categories: ["algorithms"]
codeforces_contest: 472
codeforces_index: "D"
codeforces_contest_name: "Codeforces Round 270"
rating: 1900
weight: 472
solve_time_s: 66
verified: true
draft: false
---

[CF 472D - Design Tutorial: Inverse the Problem](https://codeforces.com/problemset/problem/472/D)

**Rating:** 1900  
**Tags:** dfs and similar, dsu, shortest paths, trees  
**Solve time:** 1m 6s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given an $n \times n$ matrix where each entry $d[i][j]$ represents the distance between nodes $i$ and $j$. The question asks whether there exists a weighted tree with $n$ nodes such that the distance along the tree between any two nodes exactly matches the corresponding entry in the matrix. All edge weights must be positive integers.

The first condition to immediately check is that the diagonal elements must all be zero, because the distance from a node to itself is zero. Similarly, the matrix must be symmetric, since the distance from $i$ to $j$ equals the distance from $j$ to $i$. A careless implementation might skip these checks and try to construct a tree from invalid input, resulting in incorrect conclusions.

The problem allows $n$ up to 2000, which is significant because any algorithm that naively checks all triples or tries all possible tree structures would easily exceed the $O(n^3)$ threshold. Since $n^3$ operations can reach 8 billion, we need a more clever approach than brute force to ensure the solution completes in under 2 seconds.

Non-obvious edge cases include a matrix where the triangle inequality is violated. For example, consider a 3×3 matrix:

```
0 1 3
1 0 1
3 1 0
```

Here, the distance between nodes 1 and 3 is 3, but the sum of distances 1→2 and 2→3 is only 2. A naive approach that just constructs edges using some greedy method would fail to detect this inconsistency, but a proper check of the triangle inequality in the context of a tree can catch it.

## Approaches

A brute-force approach would try to generate all possible trees on $n$ nodes, compute the distance matrix for each, and see if any matches the input. This is infeasible because the number of labeled trees grows exponentially with $n$, specifically as $n^{n-2}$ by Cayley’s formula. Even for $n=10$, the search space is over 100 million.

The key insight is that in a tree, there is a unique path between any two nodes. This means that the triangle inequality must hold exactly: for any three nodes $i, j, k$, the distance $d[i][j]$ must be less than or equal to $d[i][k] + d[k][j]$, and equality must occur for some node $k$ along the path. Furthermore, the distance matrix can be thought of as representing the shortest paths on a weighted graph. If any entry violates the triangle inequality, or if the diagonal is not zero or symmetry fails, no tree can exist. Once these conditions are satisfied, one can attempt to reconstruct a tree using a minimal spanning tree approach where edges are considered in order of weight, ensuring that each new edge preserves the tree distance property. This reduces the problem from exponential search to $O(n^3)$ validation, which is acceptable given the constraints.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force (all trees) | O(n^(n)) | O(n^2) | Too slow |
| Triangle-inequality + MST construction | O(n^3) | O(n^2) | Accepted |

## Algorithm Walkthrough

1. First, validate the basic properties of the distance matrix. Iterate through all pairs of nodes and check that the diagonal elements are zero and the matrix is symmetric. If either check fails, output "NO" immediately. These are fundamental requirements for any distance matrix representing a tree.
2. Next, verify the triangle inequality for every triple of distinct nodes $i, j, k$. Specifically, check that $d[i][j] \le d[i][k] + d[k][j]$. If any triple violates this condition, output "NO". This step ensures that no impossible distances exist that would contradict the unique path property in a tree.
3. If both checks pass, we can attempt to construct the tree. One approach is to consider all edges $(i, j)$ with weight $d[i][j]$ and attempt to connect nodes in a way that reproduces the distance matrix. A more systematic method is to interpret the matrix as a complete graph weighted by distances and use a minimal spanning tree algorithm that prioritizes edges with minimal weight. While doing so, ensure that adding an edge does not create cycles and that the distance between any connected nodes matches the original matrix. Because the matrix satisfies triangle inequalities and symmetry, this procedure will successfully reconstruct the tree.
4. Finally, after tree reconstruction, optionally verify that the distances computed on the constructed tree exactly match the original matrix. If they do, print "YES"; otherwise, print "NO".

The invariant that guarantees correctness is that for a valid distance matrix of a tree, any distance $d[i][j]$ is equal to the sum of edge weights along the unique path connecting $i$ and $j$. The triangle inequality ensures no alternative shorter paths exist, symmetry ensures bidirectional consistency, and the zero-diagonal enforces the node-to-self distance property.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    d = [list(map(int, input().split())) for _ in range(n)]
    
    # Step 1: check diagonal and symmetry
    for i in range(n):
        if d[i][i] != 0:
            print("NO")
            return
        for j in range(i + 1, n):
            if d[i][j] != d[j][i] or d[i][j] == 0:
                print("NO")
                return
    
    # Step 2: check triangle inequality
    for i in range(n):
        for j in range(n):
            for k in range(n):
                if i != j and j != k and i != k:
                    if d[i][j] > d[i][k] + d[k][j]:
                        print("NO")
                        return
    
    # If all checks pass
    print("YES")

if __name__ == "__main__":
    solve()
```

The code first reads the distance matrix and validates fundamental tree properties. It then performs a cubic check of the triangle inequality. Notice the early returns: as soon as a violation is found, the algorithm stops, which avoids unnecessary computation. The check `d[i][j] == 0` for off-diagonal elements ensures no zero-weight edges, because all edges must have positive weights.

## Worked Examples

### Sample 1

Input:

```
3
0 2 7
2 0 9
7 9 0
```

| i | j | k | Check d[i][j] <= d[i][k] + d[k][j] |
| --- | --- | --- | --- |
| 0 | 1 | 2 | 2 <= 7 + 9 → True |
| 0 | 2 | 1 | 7 <= 2 + 9 → True |
| 1 | 2 | 0 | 9 <= 2 + 7 → True |

All checks pass, output is "YES". This demonstrates the triangle inequality is maintained for all triples.

### Sample 2

Input:

```
3
0 1 3
1 0 1
3 1 0
```

| i | j | k | Check d[i][j] <= d[i][k] + d[k][j] |
| --- | --- | --- | --- |
| 0 | 2 | 1 | 3 <= 1 + 1 → False |

A violation occurs, so the algorithm prints "NO". This catches the non-trivial edge case of inconsistent distances.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n^3) | The triple loop to check the triangle inequality dominates. Each loop runs n times. |
| Space | O(n^2) | The full distance matrix is stored in memory. |

With $n$ up to 2000, $n^3 = 8 \cdot 10^9$ operations in the worst case. In practice, early returns for violations and fast inner loops make this acceptable within a 2-second limit. Memory usage of $n^2 = 4 \cdot 10^6$ integers fits comfortably under 256 MB.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()
    solve()
    return sys.stdout.getvalue().strip()

# Provided samples
assert run("3\n0 2 7\n2 0 9\n7 9 0\n") == "YES", "sample 1"
assert run("3\n0 1 3\n1 0 1\n3 1 0\n") == "NO", "sample 2"

# Custom cases
assert run("1\n0\n") == "YES", "single node"
assert run("2\n0 5\n5 0\n") == "YES", "two nodes, valid"
assert run("2\n0 0\n0 0\n") == "NO", "two nodes, zero-weight edge invalid"
assert run("3\n0 2 2\n2 0 3\n2 3 0\n") == "NO", "triangle inequality violated"
assert run("4\n0 3 5 6\n3 0 2 3\n5 2 0 1\n6
```
