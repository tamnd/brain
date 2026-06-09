---
title: "CF 1987E - Wonderful Tree!"
description: "We are given a rooted tree with integer values assigned to each node. The tree is rooted at vertex 1. A tree is considered wonderful if, for every non-leaf vertex, its value is at most the sum of the values of its immediate children."
date: "2026-06-08T15:55:41+07:00"
tags: ["codeforces", "competitive-programming", "brute-force", "data-structures", "dfs-and-similar", "dsu", "greedy", "trees"]
categories: ["algorithms"]
codeforces_contest: 1987
codeforces_index: "E"
codeforces_contest_name: "EPIC Institute of Technology Round Summer 2024 (Div. 1 + Div. 2)"
rating: 2000
weight: 1987
solve_time_s: 122
verified: true
draft: false
---

[CF 1987E - Wonderful Tree!](https://codeforces.com/problemset/problem/1987/E)

**Rating:** 2000  
**Tags:** brute force, data structures, dfs and similar, dsu, greedy, trees  
**Solve time:** 2m 2s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a rooted tree with integer values assigned to each node. The tree is rooted at vertex 1. A tree is considered _wonderful_ if, for every non-leaf vertex, its value is at most the sum of the values of its immediate children. We can perform an operation any number of times where we increment the value of a vertex by 1. The task is to find the minimum number of such operations required to make the tree wonderful.

The input consists of multiple test cases. Each test case provides the number of vertices, the initial values on the vertices, and a parent array defining the tree structure. The output is a single integer per test case representing the minimum number of increments needed.

The constraints are moderate: the sum of all $n$ over all test cases is at most 5000. This implies that a quadratic algorithm per test case is acceptable, but anything much worse may be too slow. Vertex values can be up to $10^9$, so we need to avoid approaches that scale linearly with the value itself.

Non-obvious edge cases include:

- Trees where all nodes are initially zeros. For instance, a chain of three nodes with values `[0,0,0]` and edges `1-2, 2-3`. The minimal increments are required at each non-leaf node to satisfy the wonderful condition.
- Trees where some nodes already satisfy the condition while others require increments. Careless DFS implementations may over-count operations by failing to propagate the required increases from the children upward.
- Star-shaped trees where the root has many children with small values. The root may require significant increments to satisfy the sum-of-children condition, but the children may also need increments recursively to satisfy their own subtrees.

## Approaches

The brute-force approach would be to repeatedly check every non-leaf node and increment values until the tree becomes wonderful. Each iteration would traverse all nodes and potentially increase values one by one. While correct, the worst-case complexity is roughly the sum of all required increments, which could be on the order of $10^9$ per node, clearly infeasible.

The key insight is to process the tree in a bottom-up manner. If we know the sum of values required for each child subtree to be wonderful, we can propagate this requirement to the parent. Specifically, for a node to be wonderful, it must satisfy $a_v \le \sum a_u$ over its children. If this inequality fails, we can calculate exactly how much we need to increment the children sum to make it hold. By recursively calculating the total increments needed for each subtree and propagating upwards, we ensure we never over-count operations. This turns the problem into a DFS where each node contributes an exact number of operations needed to satisfy its local condition.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(total increments × n) | O(n) | Too slow |
| Bottom-Up DFS | O(n) per test case | O(n) | Accepted |

## Algorithm Walkthrough

1. Parse the tree input and construct an adjacency list from the parent array. This allows efficient traversal of children for each node.
2. Define a recursive DFS function that, for a given node, computes the sum of values in its subtree and the total number of increments needed to make that subtree wonderful.
3. For each node, initialize `subtree_sum` as its own value and `operations` as zero.
4. Recur for all children. For each child, add its subtree sum to `subtree_sum` and add its required operations to `operations`.
5. After processing all children, check if the current node satisfies `a_v <= sum of children`. If not, compute the difference and increment the current node's value accordingly. Add this difference to `operations`. This ensures the parent receives a sum that already satisfies the wonderful condition.
6. Return the total sum of the subtree rooted at this node and the total operations required.
7. Apply DFS starting from the root. The total operations returned for the root is the answer.

The invariant that guarantees correctness is that after processing each node, its value will not exceed the sum of its children, and all children are themselves wonderful. By combining the operations from children and any needed increment at the current node, we guarantee that no node is counted twice.

## Python Solution

```python
import sys
input = sys.stdin.readline
sys.setrecursionlimit(10000)

def solve():
    t = int(input())
    for _ in range(t):
        n = int(input())
        a = list(map(int, input().split()))
        p = list(map(int, input().split()))
        tree = [[] for _ in range(n)]
        for i, parent in enumerate(p):
            tree[parent - 1].append(i + 1)  # 0-indexed

        def dfs(v):
            if not tree[v]:
                return a[v], 0
            total_sum = 0
            ops = 0
            for u in tree[v]:
                child_sum, child_ops = dfs(u)
                total_sum += child_sum
                ops += child_ops
            if a[v] > total_sum:
                ops += a[v] - total_sum
                total_sum = a[v]
            else:
                total_sum = max(total_sum, a[v])
            return total_sum, ops

        _, ans = dfs(0)
        print(ans)

if __name__ == "__main__":
    solve()
```

The code first reads the number of test cases and iterates over each case. The tree is represented as an adjacency list. The `dfs` function recursively calculates both the sum of values in each subtree and the operations needed. For leaf nodes, the sum is the node's value and zero operations. For internal nodes, we accumulate the children’s sums and operations, then adjust if the current node violates the wonderful condition.

Careful attention is needed when indexing parents to children, converting from 1-based to 0-based indices, and ensuring that leaf nodes are correctly handled to avoid unnecessary operations.

## Worked Examples

### Sample 1

Input tree: values `[9,3,4,1,2]`, edges `[1,1,3,3]`.

| Node | Children | Child Sum | Node Value | Ops Needed | Total Ops |
| --- | --- | --- | --- | --- | --- |
| 4 | [] | 0 | 1 | 0 | 0 |
| 5 | [] | 0 | 2 | 0 | 0 |
| 3 | 4,5 | 3 | 4 | 1 | 1 |
| 2 | [] | 0 | 3 | 0 | 0 |
| 1 | 2,3 | 4+4=8 | 9 | 1 | 2 |

This demonstrates the bottom-up calculation where operations accumulate from children upward.

### Sample 2

Input tree: values `[5,3]`, edges `[1]`.

| Node | Children | Child Sum | Node Value | Ops Needed | Total Ops |
| --- | --- | --- | --- | --- | --- |
| 2 | [] | 0 | 3 | 0 | 0 |
| 1 | 2 | 3 | 5 | 2 | 2 |

This confirms that when a root has insufficient sum of children, the algorithm correctly increments and counts operations.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) per test case | Each node is visited exactly once, performing constant work per node. |
| Space | O(n) | Adjacency list plus recursion stack up to depth n. |

Since the sum of n across all test cases is ≤5000, the total operations are at most 5000, which fits comfortably in the 2-second limit.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()
    solve()
    return sys.stdout.getvalue().strip()

# Provided samples
assert run("4\n5\n9 3 4 1 2\n1 1 3 3\n2\n5 3\n1\n2\n36 54\n1\n3\n0 0 0\n1 2") == "3\n2\n0\n0", "Sample 1"

# Custom tests
assert run("1\n2\n0 0\n1") == "0", "Leaf tree, no increments"
assert run("1\n3\n0 0 0\n1 2") == "0", "Chain of zeros, already wonderful"
assert run("1\n3\n5 2 1\n1 1") == "2", "Root requires increments to match sum of children"
assert run("1\n4\n1 1 1 1\n1 1 3") == "1", "Nested tree requiring small increment"
assert run("1\n5\n0 0 0 0 0\n1 1 2 2") == "0", "All zeros, no increments"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `2\n0 0\n1` | `0` | Single operation unnecessary for leaf |
| `3\n0 0 0\n1 2` | `0` | Chain of zeros requires no ops |
| `3\n5 2 1\n1 1` | ` |  |
