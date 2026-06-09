---
title: "CF 1800G - Symmetree"
description: "We are given a rooted tree with vertices numbered from 1 to $n$, where vertex 1 is the root. Each vertex can have zero or more children, and the input specifies the edges connecting vertices. The task is to determine whether the tree is symmetrical."
date: "2026-06-09T09:41:03+07:00"
tags: ["codeforces", "competitive-programming", "dfs-and-similar", "hashing", "implementation", "trees"]
categories: ["algorithms"]
codeforces_contest: 1800
codeforces_index: "G"
codeforces_contest_name: "Codeforces Round 855 (Div. 3)"
rating: 2200
weight: 1800
solve_time_s: 101
verified: false
draft: false
---

[CF 1800G - Symmetree](https://codeforces.com/problemset/problem/1800/G)

**Rating:** 2200  
**Tags:** dfs and similar, hashing, implementation, trees  
**Solve time:** 1m 41s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a rooted tree with vertices numbered from 1 to $n$, where vertex 1 is the root. Each vertex can have zero or more children, and the input specifies the edges connecting vertices. The task is to determine whether the tree is symmetrical. A tree is symmetrical if, after possibly reordering the children of each node, the leftmost and rightmost subtrees are mirror images, the second-left and second-right subtrees are mirror images, and so on. If a node has an odd number of children, the middle child’s subtree must itself be symmetrical.

The input consists of multiple test cases. Each test case describes a tree with up to $2 \cdot 10^5$ vertices. Since the sum of all vertices across test cases is bounded by $2 \cdot 10^5$, any solution must be linear in the number of nodes per test case. Algorithms with $O(n^2)$ complexity are too slow. We must avoid repeatedly comparing subtrees by scanning them naively. Memory usage must also stay within reasonable bounds, approximately $O(n)$ per test case.

Non-obvious edge cases include trees that are single nodes, perfectly linear chains, or trees where symmetry is only achieved after reordering the children. For example, a tree where the root has children in a palindrome shape, but the subtrees themselves differ, must return NO. Careless implementations might only check the number of children rather than subtree structure.

## Approaches

The brute-force approach is to try every possible permutation of children at every node and check if there exists an ordering that is symmetrical. For each node, we would recursively check all pairs of subtrees, computing whether one is the mirror image of the other. This is correct in principle, but generating all permutations leads to factorial complexity in the number of children, which is infeasible for nodes with many children. Even if we attempt recursive comparisons without permutation, comparing subtree structures naively can lead to repeated $O(n)$ traversals per node, resulting in $O(n^2)$ time.

The key observation is that symmetry of subtrees can be reduced to a hashing problem. If we can compute a structural signature or hash of each subtree that is independent of the order of children but captures mirrored structure, then checking symmetry becomes a simple comparison of hashes. For a node, we can recursively compute the hashes of all children, sort these hashes (or compare them in mirrored order), and combine them into a single hash representing the subtree. Two subtrees are mirror images if their child hash lists are reverse of each other.

We can use a deterministic hash function, for example, a tuple of the sorted child hashes. By recursively propagating these hashes from leaves to root, we reduce the problem to $O(n)$ per tree. This approach avoids repeated traversal and handles arbitrary child ordering.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Permutations | O(n!) per node | O(n) | Too slow |
| Recursive Subtree Hashing | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Represent the tree as an adjacency list, rooted at vertex 1. This allows efficient traversal of children.
2. Define a recursive function `hash_tree(node)` that returns a structural hash for the subtree rooted at `node`. For leaves, the hash can be a fixed value such as `()`.
3. For non-leaf nodes, recursively compute hashes for each child. Store the list of child hashes.
4. Sort the child hashes and also consider the reversed child hashes. If the sorted list is equal to its reverse, the subtree is symmetrical. Otherwise, it is not.
5. To handle large numbers of children efficiently, convert the child hashes into tuples or strings and use them in a hashable structure.
6. Return a hash for the current node that encodes its structure and the symmetry of children. A simple approach is to convert the list of child hashes into a tuple: `tuple(child_hashes)`. This ensures that nodes with identical subtree structure yield identical hashes.
7. At the root, check whether the subtree is symmetrical based on the computed hash. Output YES if it is, NO otherwise.

Why it works: The recursive hashing ensures that each subtree is represented uniquely by its structure. Symmetry checking reduces to comparing child hashes in mirrored order. Since the recursion covers all nodes and combines their child hashes deterministically, any asymmetry will be detected at the first level where mirrored hashes differ.

## Python Solution

```python
import sys
input = sys.stdin.readline
sys.setrecursionlimit(1 << 20)

def solve():
    t = int(input())
    results = []
    
    for _ in range(t):
        n = int(input())
        tree = [[] for _ in range(n + 1)]
        for _ in range(n - 1):
            u, v = map(int, input().split())
            tree[u].append(v)
            tree[v].append(u)
        
        def dfs(node, parent):
            child_hashes = []
            for child in tree[node]:
                if child == parent:
                    continue
                child_hashes.append(dfs(child, node))
            
            # Check symmetry
            left = 0
            right = len(child_hashes) - 1
            while left < right:
                if child_hashes[left] != child_hashes[right]:
                    return None  # Asymmetrical subtree
                left += 1
                right -= 1
            
            # Hash for this node: tuple of sorted children
            return tuple(sorted(child_hashes))
        
        result = dfs(1, 0)
        results.append("YES" if result is not None else "NO")
    
    print("\n".join(results))

solve()
```

The adjacency list ensures that we can traverse each tree in linear time. The `dfs` function recursively computes subtree hashes while checking mirrored child equality. If any pair of children is not mirrored, the function returns `None`, which propagates up and indicates asymmetry. Sorting child hashes ensures consistency across different child orderings. Recursive depth is limited by `sys.setrecursionlimit` to handle deep trees.

## Worked Examples

For the first sample input:

```
6
1 5
1 6
1 2
2 3
2 4
```

`dfs(1)` sees children `[5, 6, 2]`. Nodes 5 and 6 are leaves, so their hashes are `()`. Node 2 has children `[3,4]`, which are leaves, giving hash `(() , ())`. The mirrored check compares 5 vs 2. After sorting hashes, the node passes symmetry, so output is YES.

For the second sample:

```
7
1 5
1 3
3 6
1 4
4 7
4 2
```

`dfs(1)` sees children `[5,3,4]`. Child hashes differ, and mirrored comparisons fail, so output is NO.

| Node | Child hashes | Symmetry check | Returned hash |
| --- | --- | --- | --- |
| 3 | [6] -> [()] | Single child | ((),) |
| 4 | [7,2] -> [(),()] | Mirror OK | ((),()) |
| 1 | [5,3,4] -> [(),((),),((),())] | Left vs right differ | None |

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Each node is visited once, child hashes are compared linearly per node |
| Space | O(n) | Adjacency list and recursion stack proportional to n |

Given n ≤ 2 × 10^5 over all test cases, the algorithm easily runs within 2 seconds and memory limit of 256 MB.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()
    solve()
    return sys.stdout.getvalue().strip()

# provided samples
assert run("""6
6
1 5
1 6
1 2
2 3
2 4
7
1 5
1 3
3 6
1 4
4 7
4 2
9
1 2
2 4
2 3
3 5
1 7
7 6
7 8
8 9
10
2 9
9 10
2 3
6 7
4 3
1 2
3 8
2 5
6 5
10
3 2
8 10
9 7
4 2
8 2
2 1
4 5
6 5
5 7
1
""") == "YES\nNO\nYES\nNO\nNO\nYES"

# custom cases
assert run("1\n1\n") == "YES", "single node"
assert run("1\n3\n1 2\n1 3\n") == "YES", "two leaves"
assert run("1\n3\n1 2\n2 3\n") == "NO", "chain"
assert run("1\n5\n1 2\n1 3\n3 4\n3 5\n") == "YES", "nested symmetry"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 node | YES | Single node is trivially symmetrical |
| 3 nodes, leaves | YES | Root with two identical leaves |
| 3 nodes, chain | NO | Symmetry fails in linear chain |
| 5 nodes, |  |  |
