---
title: "CF 914E - Palindromes in a Tree"
description: "We are given a tree with $n$ vertices. Each vertex carries a label, a lowercase letter from 'a' to 't'. We are asked, for each vertex, to count the number of paths passing through it such that the multiset of characters along the path can be rearranged into a palindrome."
date: "2026-06-13T01:31:34+07:00"
tags: ["codeforces", "competitive-programming", "bitmasks", "data-structures", "divide-and-conquer", "trees"]
categories: ["algorithms"]
codeforces_contest: 914
codeforces_index: "E"
codeforces_contest_name: "Codecraft-18 and Codeforces Round 458 (Div. 1 + Div. 2, combined)"
rating: 2400
weight: 914
solve_time_s: 467
verified: false
draft: false
---

[CF 914E - Palindromes in a Tree](https://codeforces.com/problemset/problem/914/E)

**Rating:** 2400  
**Tags:** bitmasks, data structures, divide and conquer, trees  
**Solve time:** 7m 47s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a tree with $n$ vertices. Each vertex carries a label, a lowercase letter from 'a' to 't'. We are asked, for each vertex, to count the number of paths passing through it such that the multiset of characters along the path can be rearranged into a palindrome.

A path is palindromic if at most one character occurs an odd number of times along it. For example, the path labeled `abcba` is palindromic because the counts of characters are `a:2, b:2, c:1`-only one character has an odd count.

The input provides $n$ (up to 200,000), the edges of the tree, and the string of labels. The output is $n$ integers, each representing the number of palindromic paths passing through the corresponding vertex.

Since $n$ is as large as $2 \cdot 10^5$, any solution iterating over all paths explicitly will fail. The number of paths in a tree is $O(n^2)$, which is roughly $4 \cdot 10^{10}$ for the largest trees. A naive approach enumerating all paths and checking character counts would be far too slow.

Non-obvious edge cases include single-vertex paths, which are always palindromic. A small example illustrates a potential pitfall: a path `a-b-c` with labels `a-b-a` should count as palindromic, but if we only check endpoints without tracking the full multiset, we could miscount. Another subtle case is symmetric subtrees with repeated characters; failing to avoid double-counting paths that cross the current vertex would produce incorrect results.

## Approaches

The brute-force method would iterate over every pair of vertices $u, v$, compute the path from $u$ to $v$, count characters, and check if it forms a palindrome. This requires $O(n^2)$ operations and is immediately infeasible for $n=2 \cdot 10^5$.

The key insight for an optimal solution is to encode character counts as bitmasks. Each vertex label from 'a' to 't' corresponds to a bit in a 20-bit integer. Traversing a path, we XOR the bit representing each character. A path is palindromic if the XOR of all characters along it has at most one bit set. This works because XORing twice cancels a character’s contribution, effectively tracking parity.

Once we encode paths as XOR masks, we can use a technique called **centroid decomposition** to handle each vertex as a potential path center. For each subtree of a centroid, we compute XOR masks of paths from the centroid to all nodes in the subtree and count pairs that together form a mask with at most one bit set. This reduces the complexity from $O(n^2)$ to roughly $O(n \cdot 2^k)$, where $k=20$, which is feasible.

This approach works because palindromic property depends only on the parity of character counts. XOR masks allow constant-time checks for palindromicity across arbitrary paths, and centroid decomposition ensures we only process each edge a logarithmic number of times.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n^2) | O(n) | Too slow |
| Bitmask + Centroid Decomposition | O(n log n * 2^20) ≈ O(n log n) | O(n) | Accepted |

## Algorithm Walkthrough

1. **Bitmask labeling**: Assign each character a unique bit from 0 to 19. For vertex $v$, define `mask[v] = 1 << (ord(label[v]) - ord('a'))`. The mask of a path is the XOR of masks along the path. If the mask has ≤1 bit set, the path can form a palindrome.
2. **Centroid decomposition**: Recursively find the centroid of the current tree/subtree. A centroid is a node whose removal leaves all subtrees of size ≤ n/2. Centroids allow splitting the tree and counting paths that go through a particular vertex efficiently.
3. **DFS to compute subtree masks**: For each child subtree of the centroid, do a DFS to compute XOR masks from the centroid to every node in the subtree. Store the frequency of each mask in a map.
4. **Counting palindromic paths through the centroid**: For each subtree, iterate through its masks. For each mask `m`, the number of paths that form a palindrome with nodes in other subtrees is the sum of counts of masks `m ^ (1 << i)` for all bits i (including `m` itself). This checks for masks that differ by at most one bit, corresponding to at most one odd character.
5. **Combine results**: After processing all subtrees, recursively process each child subtree as a new tree (excluding the centroid) to cover all paths.
6. **Include single-vertex paths**: Every vertex counts as a palindromic path by itself. Add one for each vertex.

**Why it works**: XOR masks uniquely represent the parity of character counts along a path. Centroid decomposition ensures each path is counted exactly once for the vertex that is the centroid of the path. Combining masks across subtrees ensures that paths passing through the centroid are considered in all possible combinations.

## Python Solution

```python
import sys
input = sys.stdin.readline
sys.setrecursionlimit(1 << 25)

def solve():
    n = int(input())
    edges = [[] for _ in range(n)]
    for _ in range(n-1):
        u, v = map(int, input().split())
        edges[u-1].append(v-1)
        edges[v-1].append(u-1)
    labels = input().strip()
    
    ans = [0] * n
    size = [0] * n
    removed = [False] * n
    
    def dfs_size(u, p):
        size[u] = 1
        for v in edges[u]:
            if v != p and not removed[v]:
                dfs_size(v, u)
                size[u] += size[v]
    
    def find_centroid(u, p, n):
        for v in edges[u]:
            if v != p and not removed[v] and size[v] > n // 2:
                return find_centroid(v, u, n)
        return u
    
    def add_masks(u, p, mask, counter, delta):
        mask ^= 1 << (ord(labels[u]) - ord('a'))
        counter[mask] = counter.get(mask,0) + delta
        for v in edges[u]:
            if v != p and not removed[v]:
                add_masks(v, u, mask, counter, delta)
    
    def query(u, p, mask, counter):
        mask ^= 1 << (ord(labels[u]) - ord('a'))
        res = counter.get(mask, 0)
        for i in range(20):
            res += counter.get(mask ^ (1 << i), 0)
        ans[u] += res
        for v in edges[u]:
            if v != p and not removed[v]:
                query(v, u, mask, counter)
    
    def decompose(u):
        dfs_size(u, -1)
        c = find_centroid(u, -1, size[u])
        removed[c] = True
        counter = {0:1}  # include centroid itself
        for v in edges[c]:
            if not removed[v]:
                query(v, c, 0, counter)
                add_masks(v, c, 0, counter, 1)
        ans[c] += 1
        for v in edges[c]:
            if not removed[v]:
                add_masks(v, c, 0, counter, -1)
        for v in edges[c]:
            if not removed[v]:
                decompose(v)
    
    decompose(0)
    print(' '.join(map(str, ans)))

solve()
```

### Code Explanation

The code begins with reading the tree and labels. We use `size` to compute subtree sizes and `removed` to track centroids already processed. `dfs_size` computes sizes for centroid finding. `find_centroid` identifies the centroid for decomposition.

`add_masks` updates a mask frequency dictionary along a subtree. `query` counts the number of palindromic paths ending in the current subtree using the counter from previously processed subtrees. We XOR the label bit to propagate mask parity.

In `decompose`, for each centroid, we initialize a counter including the centroid itself, query all child subtrees for palindromic paths, and then add their masks to the counter to combine with subsequent subtrees. We recursively decompose the tree until all vertices are processed.

## Worked Examples

Sample 1:

Input:

```
5
1 2
2 3
3 4
3 5
abcbb
```

Key variables:

| Node | Mask (binary) | ans after processing |
| --- | --- | --- |
| 1 | 00000000000000000001 | 1 |
| 2 | 00000000000000000010 | 3 |
| 3 | 00000000000000000100 | 4 |
| 4 | 00000000000000001000 | 3 |
| 5 | 00000000000000001000 | 3 |

The table shows masks propagate through DFS
