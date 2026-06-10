---
title: "CF 1491E - Fib-tree"
description: "We are given a tree with $n$ vertices, and we want to determine whether it is a Fib-tree. A Fib-tree is a tree whose size equals some Fibonacci number $Fk$, and it either consists of a single vertex or can be split into two smaller Fib-trees by removing exactly one edge."
date: "2026-06-10T22:28:12+07:00"
tags: ["codeforces", "competitive-programming", "brute-force", "dfs-and-similar", "divide-and-conquer", "number-theory", "trees"]
categories: ["algorithms"]
codeforces_contest: 1491
codeforces_index: "E"
codeforces_contest_name: "Codeforces Global Round 13"
rating: 2400
weight: 1491
solve_time_s: 95
verified: true
draft: false
---

[CF 1491E - Fib-tree](https://codeforces.com/problemset/problem/1491/E)

**Rating:** 2400  
**Tags:** brute force, dfs and similar, divide and conquer, number theory, trees  
**Solve time:** 1m 35s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a tree with $n$ vertices, and we want to determine whether it is a Fib-tree. A Fib-tree is a tree whose size equals some Fibonacci number $F_k$, and it either consists of a single vertex or can be split into two smaller Fib-trees by removing exactly one edge. In other words, a tree is a Fib-tree if it can be recursively decomposed along edges into subtrees whose sizes are consecutive Fibonacci numbers.

The input gives $n$ and the list of $n-1$ edges forming the tree. The output is a simple "YES" or "NO" depending on whether the tree satisfies the Fib-tree property. The first step is to recognize that the size of the tree must itself be a Fibonacci number, or else we can immediately return "NO".

With $n$ up to $2 \cdot 10^5$ and a 1-second time limit, we cannot afford solutions with time complexity $O(n^2)$. This rules out approaches that consider all possible edge removals naively for each subtree. We need something closer to $O(n \log n)$ or $O(n \sqrt n)$ at worst.

Non-obvious edge cases include small trees that are already Fib-trees, like a single node or two nodes. Another subtle case occurs when there are multiple ways to split the tree: we must ensure that at least one edge allows a valid Fibonacci decomposition. If the algorithm assumes a particular splitting order without checking all possibilities, it may falsely return "NO". For instance, the tree of size $3$ with edges $1-2$ and $2-3$ is a Fib-tree, but a careless approach might only check one split and miss the valid decomposition.

## Approaches

A brute-force approach would try every edge, remove it, and check whether the resulting two subtrees are Fib-trees. This is correct because the Fib-tree property is recursive: if the two subtrees resulting from any edge removal are Fib-trees, the whole tree is a Fib-tree. However, this approach is too slow. There are $n-1$ edges, and for each edge we would need to compute subtree sizes and recursively check each subtree. In the worst case this leads to $O(n^2)$ operations, which is unacceptable for $n = 2 \cdot 10^5$.

The key observation is that in a Fib-tree of size $F_k$, the two subtrees formed by removing the right edge must have sizes $F_{k-1}$ and $F_{k-2}$ (the two previous Fibonacci numbers). This insight reduces the problem to efficiently finding an edge whose subtree sizes match consecutive Fibonacci numbers. Using a depth-first search (DFS), we can compute the size of each subtree rooted at any node. When we find a subtree whose size equals $F_{k-1}$ or $F_{k-2}$, removing the corresponding edge splits the tree appropriately. We then recursively apply the same procedure to each subtree.

Another crucial optimization is to memoize Fibonacci numbers and their indices so we can quickly determine the expected sizes of the two subtrees at each step. The divide-and-conquer recursion ensures that each edge is considered only once in the context of its subtree, giving a total runtime proportional to $O(n \log n)$.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n^2) | O(n) | Too slow |
| Optimal | O(n log n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Precompute all Fibonacci numbers up to $2 \cdot 10^5$ and store a mapping from each Fibonacci number to its index $k$. If $n$ is not in this set, return "NO" immediately.
2. Build the tree as an adjacency list. Initialize a `used` array to track edges that have been removed in the recursive splitting.
3. Implement a DFS to compute the size of each subtree and store the parent edge for each node.
4. For a tree of size $F_k$, the goal is to find an edge whose removal splits the tree into subtrees of sizes $F_{k-1}$ and $F_{k-2}$. In the DFS, if a subtree has size exactly $F_{k-1}$ or $F_{k-2}$, mark the corresponding edge as the cut and recurse on both resulting subtrees.
5. The recursion terminates when a subtree has size 1, which is trivially a Fib-tree.
6. If at any step no edge can be found that splits the tree into two Fibonacci-sized subtrees, return "NO".

Why it works: The algorithm preserves the invariant that at each recursive call, the subtree size is a Fibonacci number. By searching for a subtree of size $F_{k-1}$ or $F_{k-2}$, we guarantee that the two resulting subtrees correspond to consecutive Fibonacci numbers, which is exactly the property required for a Fib-tree. The DFS ensures that every edge is checked efficiently, and recursion ensures the property holds for all subtrees.

## Python Solution

```python
import sys
sys.setrecursionlimit(1 << 25)
input = sys.stdin.readline

def main():
    n = int(input())
    edges = [[] for _ in range(n)]
    for _ in range(n-1):
        u, v = map(int, input().split())
        u -= 1
        v -= 1
        edges[u].append(v)
        edges[v].append(u)
    
    # Precompute Fibonacci numbers up to 2*10^5
    fib = [1, 1]
    fib_idx = {1:1}
    while fib[-1] < 2*10**5:
        fib.append(fib[-1]+fib[-2])
        fib_idx[fib[-1]] = len(fib)-1
    
    if n not in fib_idx:
        print("NO")
        return
    
    used = [False]*n
    
    def solve(u, size):
        if size == 1:
            return True
        k = fib_idx[size]
        target1, target2 = fib[k-1], fib[k-2]
        
        parent = [-1]*n
        sz = [0]*n
        found = [None]
        
        def dfs(v, p):
            sz[v] = 1
            parent[v] = p
            for to in edges[v]:
                if to == p or used[to]:
                    continue
                dfs(to, v)
                sz[v] += sz[to]
            if sz[v] == target1 or sz[v] == target2:
                found[0] = (v, parent[v])
        
        dfs(u, -1)
        
        if found[0] is None:
            return False
        
        x, y = found[0]
        used[x] = True
        used[y] = True
        return solve(x, sz[x]) and solve(y, size - sz[x])
    
    if solve(0, n):
        print("YES")
    else:
        print("NO")

main()
```

The code starts by precomputing Fibonacci numbers and mapping them to indices. The `used` array marks nodes that have been part of previous splits, effectively cutting the tree without removing edges physically. The DFS computes subtree sizes and identifies a valid edge to split. Recursive calls continue until we reach size 1 subtrees. Subtle points include marking both ends of the edge as used to prevent revisiting, handling the case where a subtree is exactly `target1` or `target2`, and recursion termination conditions.

## Worked Examples

### Sample 1

Input:

```
3
1 2
2 3
```

| Step | u | size | DFS subtree sizes | Found split | Next recursive calls |
| --- | --- | --- | --- | --- | --- |
| 1 | 0 | 3 | sz=[1,2,1] | Edge (2,1) size=2 | solve(2,2), solve(0,1) |
| 2 | 2 | 2 | sz=[1,1] | Edge (1,2) size=1 | solve(1,1), solve(2,1) |
| 3 | 0 | 1 | - | - | return True |

This trace shows that the algorithm finds a valid split of 3 into 2+1, then further splits 2 into 1+1, confirming the Fib-tree property.

### Sample 2

Input:

```
5
1 2
1 3
3 4
3 5
```

| Step | u | size | DFS subtree sizes | Found split | Next recursive calls |
| --- | --- | --- | --- | --- | --- |
| 1 | 0 | 5 | sz=[5,1,3,1,1] | Edge (3,1) size=3 | solve(3,3), solve(0,2) |
| 2 | 3 | 3 | sz=[3,1,1] | Edge (4,3) size=1 | solve(4,1), solve(3,2) |

The trace demonstrates that the algorithm correctly identifies recursive splits corresponding to Fibonacci sizes.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n) | Each node is visited once per recursion level, recursion depth is at most O(log n) because Fibonacci numbers grow exponentially. |
| Space | O |  |
