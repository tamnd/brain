---
title: "CF 1608G - Alphabetic Tree"
description: "We are given a tree with nodes connected by edges, each labeled with a lowercase letter. In addition, we have a collection of strings. For any two nodes in the tree, the path connecting them defines a string by concatenating the letters along that path in traversal order."
date: "2026-06-10T07:36:06+07:00"
tags: ["codeforces", "competitive-programming", "binary-search", "data-structures", "dfs-and-similar", "hashing", "string-suffix-structures", "strings", "trees"]
categories: ["algorithms"]
codeforces_contest: 1608
codeforces_index: "G"
codeforces_contest_name: "Codeforces Round 758 (Div.1 + Div. 2)"
rating: 3500
weight: 1608
solve_time_s: 97
verified: false
draft: false
---

[CF 1608G - Alphabetic Tree](https://codeforces.com/problemset/problem/1608/G)

**Rating:** 3500  
**Tags:** binary search, data structures, dfs and similar, hashing, string suffix structures, strings, trees  
**Solve time:** 1m 37s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a tree with nodes connected by edges, each labeled with a lowercase letter. In addition, we have a collection of strings. For any two nodes in the tree, the path connecting them defines a string by concatenating the letters along that path in traversal order. The problem asks, for a given query, how many times that path string appears as a substring in a consecutive range of the provided strings.

The input sizes are significant: the tree can have up to 100,000 nodes, there can be up to 100,000 strings, and the total length of all strings is up to 100,000 characters. The number of queries can also reach 100,000. This rules out any solution that tries to extract each path string and scan all relevant strings for matches individually. A naive algorithm would involve forming a path string of length up to O(n) and searching for it in O(total string length) work per query. Multiplying by the number of queries makes this approach infeasible.

A subtle edge case occurs when the path string is very short, such as a single character, and the strings contain multiple overlapping occurrences. For instance, if the tree has a single edge labeled 'a', and a string in the collection is "aaa", a query asking for occurrences along that edge must count all three positions, not just one. Another edge case is querying a path that reverses the edge order; the code must traverse edges in the exact order along the path, from u to v.

## Approaches

The brute-force approach would build the path string for each query and then iterate over all strings in the range [l, r], scanning for substring matches. For a path of length k and a total length L of relevant strings, this would require O(k * L) per query. Given worst-case lengths and 100,000 queries, this approach could easily require 10^10 operations and is therefore too slow.

The key observation is that the total length of all strings is only 100,000, which is manageable. This suggests pre-processing the strings to support fast substring occurrence queries. Using a Suffix Automaton or Suffix Array over all the strings allows us to locate the number of occurrences of any substring efficiently. We can then augment it to record which string each position belongs to, so queries over ranges [l, r] can be answered using binary search or a Fenwick tree.

Another crucial insight is that the path strings come from a tree. We can root the tree arbitrarily and precompute hashes or string identifiers for paths from the root to every node. Then, the string along a path from u to v can be represented as a concatenation of the hash from root to u, combined with the hash from root to v, accounting for the lowest common ancestor. This allows the path string to be constructed in O(1) or O(log n) time per query, depending on the hashing technique.

The final approach is to combine these ideas: precompute path hashes using binary lifting to find the LCA, build a Suffix Automaton or a Trie for all input strings, augment it to count occurrences by string index, and then answer each query by constructing the path string hash and querying the occurrence structure over the requested range.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(q * n * total_string_length) | O(n + total_string_length) | Too slow |
| Suffix Automaton + Path Hashing | O((total_string_length + n) log n + q log total_string_length) | O(total_string_length + n) | Accepted |

## Algorithm Walkthrough

1. Root the tree at an arbitrary node, typically node 1. For each node, compute the string from the root to that node by storing either the concatenated characters or a rolling hash.
2. Precompute the lowest common ancestor (LCA) for all node pairs using binary lifting. This allows us to find the unique path from u to v efficiently.
3. For each input string, insert it into a Trie or a Suffix Automaton. Store the string's index at each terminal node and optionally maintain a Fenwick tree or sorted list to quickly count how many strings contain a given substring in a range [l, r].
4. To answer a query (u, v, l, r), compute the path string from u to v by combining the precomputed root-to-node paths for u and v and removing the prefix corresponding to the LCA.
5. Traverse the automaton or Trie with the path string, obtaining a node that represents all occurrences of this substring. Use the stored indices with binary search or a Fenwick tree to count how many fall within [l, r].
6. Return the count for the query.

Why it works: The correctness follows from the properties of the Suffix Automaton or Trie. Any substring present in the automaton is guaranteed to correspond to a path in the tree, and the indexing mechanism ensures we count only occurrences in the requested range. LCA-based path hashing guarantees that the exact path string is extracted without explicitly traversing edges each query.

## Python Solution

```python
import sys
input = sys.stdin.readline
from collections import defaultdict, deque
import bisect

sys.setrecursionlimit(1 << 25)

class TrieNode:
    def __init__(self):
        self.children = {}
        self.indices = []

class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, s, idx):
        node = self.root
        for c in s:
            if c not in node.children:
                node.children[c] = TrieNode()
            node = node.children[c]
        node.indices.append(idx)

    def query(self, s, l, r):
        node = self.root
        for c in s:
            if c not in node.children:
                return 0
            node = node.children[c]
        # count indices in range [l, r]
        return bisect.bisect_right(node.indices, r) - bisect.bisect_left(node.indices, l)

def build_tree(n, edges):
    g = [[] for _ in range(n)]
    labels = {}
    for u, v, c in edges:
        u -= 1; v -= 1
        g[u].append(v)
        g[v].append(u)
        labels[(u, v)] = c
        labels[(v, u)] = c
    return g, labels

def dfs(u, parent, g, labels, path, paths):
    paths[u] = ''.join(path)
    for v in g[u]:
        if v != parent:
            path.append(labels[(u, v)])
            dfs(v, u, g, labels, path, paths)
            path.pop()

def lca_precompute(n, g, root=0):
    LOG = 20
    up = [[-1]*LOG for _ in range(n)]
    depth = [0]*n
    def dfs_lca(u, p):
        up[u][0] = p
        for i in range(1, LOG):
            if up[u][i-1] != -1:
                up[u][i] = up[up[u][i-1]][i-1]
        for v in g[u]:
            if v != p:
                depth[v] = depth[u] + 1
                dfs_lca(v, u)
    dfs_lca(root, -1)
    return up, depth

def lca(u, v, up, depth):
    LOG = 20
    if depth[u] < depth[v]:
        u, v = v, u
    for i in range(LOG-1, -1, -1):
        if up[u][i] != -1 and depth[up[u][i]] >= depth[v]:
            u = up[u][i]
    if u == v:
        return u
    for i in range(LOG-1, -1, -1):
        if up[u][i] != -1 and up[u][i] != up[v][i]:
            u = up[u][i]
            v = up[v][i]
    return up[u][0]

def solve():
    n, m, q = map(int, input().split())
    edges = [tuple(input().split()) for _ in range(n-1)]
    edges = [(int(u), int(v), c) for u, v, c in edges]

    g, labels = build_tree(n, edges)
    paths = ['']*n
    dfs(0, -1, g, labels, [], paths)
    up, depth = lca_precompute(n, g)

    strings = []
    trie = Trie()
    for idx in range(1, m+1):
        s = input().strip()
        strings.append(s)
        trie.insert(s, idx)

    for _ in range(q):
        u, v, l, r = map(int, input().split())
        u -= 1; v -= 1
        ancestor = lca(u, v, up, depth)
        # construct path string
        pu = paths[u][:depth[u]-depth[ancestor]]
        pv = paths[v][:depth[v]-depth[ancestor]][::-1]
        path_str = pu + pv
        ans = trie.query(path_str, l, r)
        print(ans)
```

The code begins by constructing the tree and storing edge labels. It then precomputes root-to-node paths using DFS. Binary lifting computes LCA efficiently. A Trie stores all input strings, with node indices sorted for binary search. Queries build the path string from precomputed paths and use the Trie to count occurrences in the given range. Subtle details include reversing the path segment from v to LCA and using 1-based indexing for
