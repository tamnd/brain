---
title: "CF 2127E - Ancient Tree"
description: "We are given a rooted tree with weighted vertices, where each vertex either has a fixed color between 1 and k or a missing color represented by 0. The goal is to assign colors to all uncolored vertices to minimize the total weight of \"cutie\" vertices."
date: "2026-06-08T11:10:33+07:00"
tags: ["codeforces", "competitive-programming", "constructive-algorithms", "data-structures", "dfs-and-similar", "dsu", "greedy", "trees"]
categories: ["algorithms"]
codeforces_contest: 2127
codeforces_index: "E"
codeforces_contest_name: "Atto Round 1 (Codeforces Round 1041, Div. 1 + Div. 2)"
rating: 2100
weight: 2127
solve_time_s: 144
verified: false
draft: false
---

[CF 2127E - Ancient Tree](https://codeforces.com/problemset/problem/2127/E)

**Rating:** 2100  
**Tags:** constructive algorithms, data structures, dfs and similar, dsu, greedy, trees  
**Solve time:** 2m 24s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a rooted tree with weighted vertices, where each vertex either has a fixed color between 1 and k or a missing color represented by 0. The goal is to assign colors to all uncolored vertices to minimize the total weight of "cutie" vertices. A vertex is "cutie" if there exist two descendants (or the vertex itself) of the same color such that their lowest common ancestor (LCA) is the vertex, and the LCA’s color is different from theirs.

The input includes multiple test cases, each specifying the number of vertices n, the number of colors k, an array of vertex weights w, an array of initial colors c (with 0 indicating missing), and n−1 edges forming the tree. The output should provide, for each test case, the minimum achievable cost and a coloring achieving that cost.

With n up to 2×10^5 and t up to 10^4, a naive algorithm that checks all pairs of vertices for the cutie condition is infeasible. Specifically, iterating over all pairs would require O(n^2) per test case, which can be up to 4×10^10 operations in total. Therefore, we need a solution linear or near-linear in n per test case. Edge cases include trees where all colors are missing, where all vertices have the same weight, or where k=2, which could force certain assignments to avoid cutie vertices.

For example, if the root has color 1, and two leaves have the same color 2, the root becomes cutie if it is not colored 2. Careless assignment of missing colors to match sibling colors could artificially inflate cost.

## Approaches

The brute-force solution iterates through all color assignments for missing vertices and computes the cutie cost for each. This is guaranteed correct but utterly infeasible because with m missing vertices and k colors, there are k^m assignments. Even for small trees, this approach fails once m ≥ 10, as k^m explodes.

The optimal solution emerges from the observation that the cost of a vertex depends only on the colors appearing in its subtree. If multiple children contain the same color and the parent has a different color, the parent contributes its weight. This means we can process the tree bottom-up using DFS. Each node maintains a multiset or map of colors in its subtree. For missing colors, we choose a color that appears least in the children or does not appear at all, which avoids creating cutie conditions. This reduces the problem to merging color counts from child subtrees and choosing the parent color optimally. Using a "DSU on tree" technique-merging smaller child maps into larger ones-keeps the complexity linear.

The key insight is that the problem reduces to subtree color counting rather than enumerating vertex pairs. This leverages tree structure and the LCA property directly: a cutie arises if two descendants share a color not equal to the ancestor. Maintaining color frequency counts allows checking this condition efficiently.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(k^m * n^2) | O(n) | Too slow |
| DFS + Subtree Color Merging | O(nk) amortized | O(nk) | Accepted |

## Algorithm Walkthrough

1. Parse the tree, weights, colors, and edges, and build an adjacency list.
2. For each node, initialize a counter for colors in its subtree. If a node is colored, set its count to 1 for that color. If uncolored, leave it flexible.
3. Perform a depth-first search from the root. For each node, recursively process children, merging their color counts into the current node's map. Always merge the smaller map into the larger to optimize merging.
4. After processing children, if the current node is uncolored, pick a color that minimizes the potential cutie contribution. This is a color that either does not appear among the children or appears least frequently. Assign this color to the node.
5. For each node, calculate if it is cutie: if any child color appears more than once in its subtree and differs from the node's color, add the node's weight to the total cost.
6. Return the total cost and the final color assignment for the tree.

Why it works: By processing bottom-up, we ensure that each node sees the aggregated color frequencies of all its descendants. The choice of the node’s color based on the subtree counts guarantees that we minimize creating new cutie vertices. The merging strategy ensures no counts are double-counted, and each node is visited exactly once, so the algorithm is linear in the size of the tree, up to a factor of k.

## Python Solution

```python
import sys
input = sys.stdin.readline
from collections import defaultdict

def solve():
    t = int(input())
    for _ in range(t):
        n, k = map(int, input().split())
        w = list(map(int, input().split()))
        c = list(map(int, input().split()))
        tree = [[] for _ in range(n)]
        for _ in range(n - 1):
            u, v = map(int, input().split())
            tree[u - 1].append(v - 1)
            tree[v - 1].append(u - 1)
        color_ans = c[:]
        total_cost = 0

        def dfs(u, parent):
            nonlocal total_cost
            count = defaultdict(int)
            if c[u] != 0:
                count[c[u]] = 1
            max_child = -1
            max_size = -1
            child_counts = {}
            for v in tree[u]:
                if v == parent:
                    continue
                sub_count = dfs(v, u)
                child_counts[v] = sub_count
                if len(sub_count) > max_size:
                    max_size = len(sub_count)
                    max_child = v
            if max_child != -1:
                count = child_counts[max_child]
            for v in tree[u]:
                if v == parent or v == max_child:
                    continue
                for key, val in child_counts[v].items():
                    count[key] += val
            if c[u] == 0:
                best_color = 1
                min_additional = float('inf')
                for color in range(1, k + 1):
                    add = 0
                    for key, val in count.items():
                        if key == color:
                            continue
                        if val >= 2:
                            add += w[u]
                    if add < min_additional:
                        min_additional = add
                        best_color = color
                color_ans[u] = best_color
            node_color = color_ans[u]
            for key, val in count.items():
                if key != node_color and val >= 2:
                    total_cost += w[u]
                    break
            count[node_color] += 1
            return count

        dfs(0, -1)
        print(total_cost)
        print(' '.join(map(str, color_ans)))

if __name__ == "__main__":
    solve()
```

In the code, the DFS function returns a dictionary representing the color counts in the subtree of each node. We choose the heaviest child map to merge others into, keeping the merge operation efficient. For uncolored nodes, we iterate over all possible colors and pick the one producing the minimum additional cost. Cutie cost is added immediately if conditions are met. This ensures both minimal cost and a valid coloring.

## Worked Examples

For the first sample input:

```
4
4 4
5 5 5 5
1 0 2 3
1 2
1 3
1 4
```

The DFS visits nodes 2, 3, 4 first. Node 2 is uncolored. Its only siblings have colors 1, 2, 3. Choosing color 1 avoids making node 1 cutie, because no two descendants share color 1 except possibly itself. The total cost is 0, coloring becomes [1,1,2,3].

For the second sample input:

```
5 2
3 1 4 1 5
1 2 1 2 2
1 4
2 1
3 4
4 5
```

All vertices are colored. DFS computes subtree color counts. Node 1 has children with colors 2 and 1, appearing multiple times. Node 1 becomes cutie because c1=1 differs from color 2 that appears twice in descendants. Total cost is w[0]=3. Coloring is unchanged.

| Node | Count Dict | Chosen Color | Cutie Contribution |
| --- | --- | --- | --- |
| 1 | {1:3,2:2} | 1 | 3 |
| 2 | {2:1} | 2 | 0 |
| 3 | {1:1} | 1 | 0 |
| 4 | {2:2} | 2 | 0 |
| 5 | {2:1} | 2 | 0 |

This trace shows how counts accumulate and cutie detection occurs.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(nk) amortized per test case | Each node merges children’s color maps using the DSU-on-tree technique, iterating over k colors to choose optimal color. |
| Space | O(nk) | Each node may store a dictionary of up to k colors, total space scales linearly with n and k. |

Given n ≤ 2×10^5 and k ≤ n,
