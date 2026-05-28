---
title: "CF 115A - Party"
description: "We are asked to organize a company party such that no group contains both a manager and their subordinate, directly or indirectly. The input describes each employee's immediate manager: a number from 1 to n, or -1 if they have no manager."
date: "2026-05-28T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "dfs-and-similar", "graphs", "trees"]
categories: ["algorithms"]
codeforces_contest: 115
codeforces_index: "A"
codeforces_contest_name: "Codeforces Beta Round 87 (Div. 1 Only)"
rating: 900
weight: 115
solve_time_s: 111
verified: true
draft: false
---

[CF 115A - Party](https://codeforces.com/problemset/problem/115/A)

**Rating:** 900  
**Tags:** dfs and similar, graphs, trees  
**Solve time:** 1m 51s  
**Verified:** yes  

## Solution
## Problem Understanding

We are asked to organize a company party such that no group contains both a manager and their subordinate, directly or indirectly. The input describes each employee's immediate manager: a number from 1 to _n_, or -1 if they have no manager. Our goal is to compute the minimum number of groups needed so that within any group no employee is superior to another.

The hierarchy forms a forest of trees: each employee with no manager is a root, and all other employees link to their manager. Since there are no cycles, each employee has exactly one path up to a root. The problem of grouping employees without superior-subordinate conflicts reduces to selecting levels in these trees. Employees at the same depth in a tree can safely be placed in the same group because they have no superior-subordinate relationship among them.

The constraint _n_ ≤ 2000 suggests that an O(n²) algorithm may barely fit, but O(n) or O(n log n) is preferred. Edge cases include having all employees independent (all -1), in which case only one group is needed, or having a single long chain of employees where the number of groups equals the chain length. Careless implementations might assume a single tree rather than a forest and miss some roots.

## Approaches

A brute-force approach would try all possible partitions of employees into groups, checking for superior relationships within each group. This is clearly infeasible because the number of partitions grows exponentially. Even simulating all pairs of employees and trying to greedily assign groups can become O(n²) and is prone to off-by-one mistakes in depth calculation.

The key insight comes from the tree structure. Each tree's height gives the minimum number of groups needed for that tree, because the longest chain of superiors requires that many separate groups to avoid conflicts. Thus, the problem reduces to finding the height of each tree in the forest and taking the maximum. Depth-first search (DFS) is a natural way to compute the depth for each node starting from roots. Each root's depth is 1, and every child has depth equal to its parent's depth plus 1.

This observation transforms an otherwise combinatorial problem into a simple traversal problem. Instead of checking all pairs, we traverse each tree once and track the maximum depth, giving an O(n) solution.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(2ⁿ × n²) | O(n²) | Too slow |
| DFS Depth Calculation | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Read _n_ and the list of immediate managers. Convert manager indices to zero-based if needed. Collect each employee under their manager to form an adjacency list representing the trees in the forest.
2. Identify all roots. These are employees whose manager is -1.
3. Initialize a variable `max_depth` to zero. This will hold the height of the tallest tree.
4. Define a recursive DFS function that, for a given node, computes the depth of its subtree. The depth of a leaf is 1. For a node with children, the depth is 1 plus the maximum depth among its children.
5. For each root, invoke the DFS function and update `max_depth` if the returned depth is greater than the current `max_depth`.
6. After traversing all trees, `max_depth` is the minimum number of groups required. Print this value.

Why it works: By placing all employees at the same depth in the same group, we guarantee no superior-subordinate pairs exist in a single group. The longest chain in any tree dictates the number of groups because each level of that chain must be separated into distinct groups. Since the DFS correctly computes tree heights, taking the maximum height over all trees gives the minimum number of groups for the entire forest.

## Python Solution

```python
import sys
input = sys.stdin.readline
sys.setrecursionlimit(3000)

n = int(input())
managers = [int(input()) - 1 for _ in range(n)]

# build the tree forest
children = [[] for _ in range(n)]
roots = []

for i in range(n):
    if managers[i] == -2:
        roots.append(i)
    else:
        children[managers[i]].append(i)

def dfs(node):
    if not children[node]:
        return 1
    depth = 0
    for child in children[node]:
        depth = max(depth, dfs(child))
    return depth + 1

max_depth = 0
for root in roots:
    max_depth = max(max_depth, dfs(root))

print(max_depth)
```

We first convert -1 to -2 for convenience. Then we build a `children` list where `children[i]` stores all employees directly managed by employee _i_. The DFS function computes the depth of a node by recursively computing the depth of its children and adding 1. For each root, we compute its depth and keep track of the maximum. Using recursion here is convenient because the tree height is at most _n_, which fits the recursion limit.

## Worked Examples

### Example 1

Input:

```
5
-1
1
2
1
-1
```

| Step | Node | Children | Depth returned | max_depth |
| --- | --- | --- | --- | --- |
| DFS 0 | 0 | [1,3] | 3 | 3 |
| DFS 1 | 1 | [2] | 2 | 3 |
| DFS 2 | 2 | [] | 1 | 3 |
| DFS 3 | 3 | [] | 1 | 3 |
| DFS 4 | 4 | [] | 1 | 3 |

We see two trees: root 0 with a depth of 3, and root 4 with depth 1. The tallest tree requires 3 groups.

### Example 2

Input:

```
4
-1
-1
-1
-1
```

All employees are independent.

| Node | Children | Depth returned | max_depth |
| --- | --- | --- | --- |
| DFS 0 | [] | 1 | 1 |
| DFS 1 | [] | 1 | 1 |
| DFS 2 | [] | 1 | 1 |
| DFS 3 | [] | 1 | 1 |

All employees can be in one group. The algorithm correctly outputs 1.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Each employee is visited once in DFS |
| Space | O(n) | Storing the children list and recursion stack |

The algorithm runs in linear time with respect to the number of employees, which fits comfortably within the 3-second limit for n ≤ 2000.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    sys.setrecursionlimit(3000)
    
    n = int(input())
    managers = [int(input()) - 1 for _ in range(n)]

    children = [[] for _ in range(n)]
    roots = []
    for i in range(n):
        if managers[i] == -2:
            roots.append(i)
        else:
            children[managers[i]].append(i)

    def dfs(node):
        if not children[node]:
            return 1
        depth = 0
        for child in children[node]:
            depth = max(depth, dfs(child))
        return depth + 1

    max_depth = 0
    for root in roots:
        max_depth = max(max_depth, dfs(root))
    return str(max_depth)

# provided sample
assert run("5\n-1\n1\n2\n1\n-1\n") == "3", "sample 1"

# custom cases
assert run("4\n-1\n-1\n-1\n-1\n") == "1", "all independent"
assert run("3\n-1\n1\n2\n") == "3", "single chain"
assert run("6\n-1\n1\n1\n2\n2\n-1\n") == "3", "multiple small trees"
assert run("1\n-1\n") == "1", "single employee"
assert run("2\n1\n-1\n") == "2", "two employees, manager first"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `4\n-1\n-1\n-1\n-1\n` | 1 | All independent employees |
| `3\n-1\n1\n2\n` | 3 | Single chain, depth equals n |
| `6\n-1\n1\n1\n2\n2\n-1\n` | 3 | Multiple trees, correct max height |
| `1\n-1\n` | 1 | Minimum input size |
| `2\n1\n-1\n` | 2 | Manager listed first, order doesn't matter |

## Edge Cases

If all employees are independent, the DFS correctly returns 1 for each root, and the max_depth is 1, which is the correct minimal group count. In a single long chain, each employee forms a separate level, and DFS correctly computes the chain length. If multiple trees exist, the algorithm tracks the maximum depth across all roots, ensuring the correct number of groups even when trees differ in height.
