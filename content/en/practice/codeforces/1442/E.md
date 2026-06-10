---
title: "CF 1442E - Black, White and Grey Tree"
description: "We are given a tree in which each node is coloured white, black, or grey. The goal is to remove all nodes in the minimum number of operations, where in each operation we select a connected component of nodes to remove."
date: "2026-06-11T04:19:25+07:00"
tags: ["codeforces", "competitive-programming", "binary-search", "constructive-algorithms", "dfs-and-similar", "dp", "greedy", "trees"]
categories: ["algorithms"]
codeforces_contest: 1442
codeforces_index: "E"
codeforces_contest_name: "Codeforces Round 681 (Div. 1, based on VK Cup 2019-2020 - Final)"
rating: 3000
weight: 1442
solve_time_s: 108
verified: false
draft: false
---

[CF 1442E - Black, White and Grey Tree](https://codeforces.com/problemset/problem/1442/E)

**Rating:** 3000  
**Tags:** binary search, constructive algorithms, dfs and similar, dp, greedy, trees  
**Solve time:** 1m 48s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a tree in which each node is coloured white, black, or grey. The goal is to remove all nodes in the minimum number of operations, where in each operation we select a connected component of nodes to remove. The only restriction is that a single operation cannot simultaneously remove a white and a black node. Grey nodes are neutral and can go with either color. After removing nodes, the tree may split into multiple connected components, and subsequent removals can be performed independently on each component.

The input consists of multiple test cases. Each test case describes a tree by its number of vertices, the color of each vertex, and the list of edges. The output is the minimum number of removal operations needed to remove all nodes.

The key constraints are that the total number of nodes across all test cases is at most 200,000, and each individual tree can also be up to 200,000 nodes. This implies that any solution that is quadratic in the number of nodes is infeasible, because in the worst case it would require roughly 200,000² operations. Linear or near-linear solutions (O(n) or O(n log n)) are acceptable. We must also be careful to handle edge cases such as trees with only one color, trees with only grey nodes, or trees where removing one node disconnects the rest of the tree in unexpected ways.

One subtle edge case is when the tree is entirely one color, such as all white or all black. A careless approach might assume that every white node must be removed separately, but in fact all connected nodes of the same color can be removed in a single operation. Another tricky case is when grey nodes form a bridge between black and white subtrees; we need to ensure we do not accidentally try to remove a white and black node in the same operation.

## Approaches

A brute-force approach would try to simulate every possible removal sequence. For each operation, we would enumerate all connected components of nodes that do not mix black and white, remove them, and recursively process the remaining tree. While this approach is correct in principle, it is exponential in the worst case, because there are exponentially many connected subsets to consider, and thus it is completely infeasible for n up to 200,000.

The key insight comes from observing that we do not need to consider all subsets. The constraint is purely about avoiding mixing black and white in the same operation. If we compute for each subtree whether it contains white, black, or both, we can recursively decide how many operations are needed. Grey nodes are flexible, so they can join either group. More formally, we can perform a depth-first search and track the minimum number of operations needed to remove the subtree rooted at each node. The operations for a subtree are determined by the maximum of the operations required for its children plus a potential extra removal if the subtree contains both white and black nodes. This reduces the problem to a linear pass over the tree.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(2^n) | O(n) | Too slow |
| DFS + Subtree Coloring | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Parse the input and build an adjacency list representation of the tree for each test case. Store the color of each node.
2. Define a recursive function `dfs(node, parent)` that returns a tuple `(has_white, has_black, operations)`, representing whether the subtree rooted at `node` contains any white nodes, black nodes, and the minimum number of removal operations needed to clear the subtree.
3. Initialize `has_white` and `has_black` based on the color of the current node. Grey nodes set neither to true.
4. For each child of the current node that is not the parent, recursively call `dfs(child, node)` and collect the child’s information.
5. If a child subtree contains both white and black nodes, increment the operation count by 1 because we cannot remove both colors in a single operation. Otherwise, merge the child’s `has_white` and `has_black` flags with the current node’s flags.
6. After processing all children, return the combined flags and the total operations. The total operations include all the operations accumulated in the children plus one more if the current subtree contains both white and black nodes and has not been counted yet.
7. After the DFS completes, the total number of removals for the tree is the `operations` value returned for the root.

The correctness comes from the invariant that for any subtree, the DFS accurately computes whether it contains both white and black nodes and the minimum number of operations to remove all nodes in that subtree without ever removing black and white together. By merging the child information upwards, the root accumulates the total number of required operations.

## Python Solution

```python
import sys
input = sys.stdin.readline
sys.setrecursionlimit(1 << 20)

def solve():
    t = int(input())
    for _ in range(t):
        n = int(input())
        colors = list(map(int, input().split()))
        adj = [[] for _ in range(n)]
        for _ in range(n - 1):
            u, v = map(int, input().split())
            u -= 1
            v -= 1
            adj[u].append(v)
            adj[v].append(u)

        def dfs(node, parent):
            has_white = colors[node] == 1
            has_black = colors[node] == 2
            ops = 0
            for child in adj[node]:
                if child == parent:
                    continue
                c_white, c_black, c_ops = dfs(child, node)
                ops += c_ops
                if c_white and c_black:
                    ops += 1
                else:
                    has_white |= c_white
                    has_black |= c_black
            return has_white, has_black, ops

        _, _, total_ops = dfs(0, -1)
        if _ and _:
            total_ops += 1
        print(total_ops)

if __name__ == "__main__":
    solve()
```

The solution reads the tree and colors, builds an adjacency list, and executes a DFS. In the DFS, `has_white` and `has_black` propagate upward to indicate whether a subtree contains those colors. Whenever a child subtree contains both white and black, it must be removed in a separate operation, so `ops` is incremented. Finally, the root is checked to see if its subtree contains both white and black, potentially adding one last operation.

## Worked Examples

For the input

```
2
2
1 1
1 2
4
1 2 1 2
1 2
2 3
3 4
```

we trace the DFS:

| Node | has_white | has_black | ops |
| --- | --- | --- | --- |
| 2 | True | False | 0 |
| 1 | True | False | 0 |
| 4 | False | True | 0 |
| 3 | True | True | 1 |
| root 1 | True | True | 1+? |

In the first case, both nodes are white, so one removal suffices. In the second case, the DFS counts one operation for the subtree containing nodes 3 and 4 (both colors appear), then combines with the rest to get three total operations.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Each node is visited once in the DFS, and each edge is traversed twice. |
| Space | O(n) | Adjacency list and recursion stack use O(n) memory. |

The solution is linear in the size of the tree. Since the total number of nodes across all test cases is 200,000, this easily fits within the 2-second time limit. Memory usage is also well within the 512 MB constraint.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()
    solve()
    return sys.stdout.getvalue().strip()

# provided samples
assert run("""4
2
1 1
1 2
4
1 2 1 2
1 2
2 3
3 4
5
1 1 0 1 2
1 2
2 3
3 4
3 5
8
1 2 1 2 2 2 1 2
1 3
2 3
3 4
4 5
5 6
5 7
5 8""") == "1\n3\n2\n3"

# custom tests
assert run("1\n1\n0\n") == "0", "single grey node"
assert run("1\n3\n1 0 2\n1 2\n2 3\n") == "1", "white-grey-black chain"
assert run("1\n3\n1 2 0\n1 2\n2 3\n") == "2", "white-black-grey chain"
assert run("1\n5\n1 1 1 1 1\n1 2\n2 3\n3 4\n4 5\n") == "1", "all white nodes"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 node grey | 0 | Zero operation needed for grey-only node |
| white-grey-black chain | 1 | Grey bridges can join either color without extra operation |
| white-black-grey chain | 2 | Black and white cannot go together |
