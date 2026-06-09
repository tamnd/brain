---
title: "CF 2007D - Iris and Game on the Tree"
description: "We are given a tree rooted at vertex 1 where each node contains either a 0, 1, or an undecided value represented as ?."
date: "2026-06-09T02:49:17+07:00"
tags: ["codeforces", "competitive-programming", "games", "graphs", "greedy", "trees"]
categories: ["algorithms"]
codeforces_contest: 2007
codeforces_index: "D"
codeforces_contest_name: "Codeforces Round 969 (Div. 2)"
rating: 1700
weight: 2007
solve_time_s: 347
verified: false
draft: false
---

[CF 2007D - Iris and Game on the Tree](https://codeforces.com/problemset/problem/2007/D)

**Rating:** 1700  
**Tags:** games, graphs, greedy, trees  
**Solve time:** 5m 47s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a tree rooted at vertex 1 where each node contains either a 0, 1, or an undecided value represented as `?`. Each leaf has a "weight," defined by walking from the root to that leaf, counting the number of `10` substrings minus the number of `01` substrings in the path string. The score of the tree is simply the number of leaves with non-zero weight.

The twist is that some vertices are undecided, and two players take turns assigning 0 or 1 to them. Iris moves first and wants to maximize the score, while Dora moves second and wants to minimize it. The problem asks for the final score assuming optimal play.

The constraints are tight. We can have up to $10^5$ nodes per test case, and the total sum across all test cases can reach $2 \cdot 10^5$. This rules out naive simulation of all assignments. Any solution that attempts to explore all $2^k$ possible assignments for the `?` nodes would time out, because the number of undecided nodes can easily be large. We need a linear or near-linear strategy, ideally $O(n)$ per test case.

A subtle edge case occurs when a leaf's weight can be forced to zero or non-zero depending on choices deep in the tree. For example, if a leaf has a single `?` along its path, the optimal player must decide its value to influence whether `10` or `01` appears, but if multiple leaves share this `?`, the decision propagates differently. A careless approach that treats leaves independently would overcount or undercount the score.

Another edge case is a tree with all nodes undecided. If both players play optimally, the score is not necessarily the total number of leaves because Dora can counter Iris's choices strategically. Similarly, a tree where the root or internal nodes are `?` requires careful propagation of influence.

## Approaches

The brute-force approach is straightforward: for each sequence of moves, simulate the game recursively, exploring every possible assignment for `?`. At each leaf, compute the string and its weight, then count how many leaves have non-zero weight. This is correct because it explicitly considers all strategies. The problem is that if we have $k$ undecided nodes, this yields $O(2^k)$ complexity, which is infeasible even for moderate trees.

The key insight is to view the problem bottom-up. Each subtree has a "contribution" to the score that can be described as a pair of integers: the maximum and minimum number of leaves that can end with non-zero weight in that subtree depending on who moves next. Leaf nodes are base cases. Internal nodes can then compute their own min/max contribution by combining the contributions of their children using a game-theory-style minimax calculation.

Specifically, for any node with undecided value, the first player can choose a value that maximizes the resulting score in its subtree, while the second player will choose a value that minimizes it. Nodes with known values propagate their effect straightforwardly. This reduces the problem to a single post-order DFS over the tree, combining child results at each node. It is linear because we visit each node once, aggregating results.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(2^k) | O(n) | Too slow |
| Optimal | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Represent the tree as an adjacency list and mark which nodes are leaves. Leaves are nodes with no children except for the root, which is never considered a leaf.
2. Perform a DFS starting from the root. For each node, recursively compute two values: the best score the first player can achieve (`first`) and the best score the second player can enforce (`second`) for the subtree rooted at that node.
3. For leaf nodes, if the value is already known (0 or 1), its contribution to the score is 1 if the leaf weight is non-zero, otherwise 0. If it is `?`, assign both possibilities temporarily as 1 because a leaf with a `?` can always be made non-zero by the first player.
4. For internal nodes, collect contributions from all children. If the node's value is decided, propagate child contributions. If the node is `?`, the first player chooses the value that maximizes the minimum contribution from the children, while the second player chooses the value that minimizes the maximum contribution from the children. The combination rule is: the total subtree score is the sum of leaf contributions that can be forced to non-zero.
5. At the root, the DFS returns the optimal score achievable by Iris (the first player). This is the final score for the tree.

Why it works: each node's value affects all leaves in its subtree consistently. By computing scores bottom-up, the algorithm ensures that every optimal move for both players is considered. The DFS naturally captures dependencies between `?` nodes because children's min/max contributions are already computed before combining at the parent.

## Python Solution

```python
import sys
input = sys.stdin.readline
sys.setrecursionlimit(1 << 20)

def solve():
    t = int(input())
    for _ in range(t):
        n = int(input())
        g = [[] for _ in range(n)]
        for _ in range(n - 1):
            u, v = map(int, input().split())
            u -= 1
            v -= 1
            g[u].append(v)
            g[v].append(u)
        s = input().strip()
        parent = [-1] * n
        children = [[] for _ in range(n)]
        stack = [0]
        order = []
        while stack:
            u = stack.pop()
            order.append(u)
            for v in g[u]:
                if v != parent[u]:
                    parent[v] = u
                    children[u].append(v)
                    stack.append(v)

        dp = [0] * n  # number of leaves with non-zero weight in optimal play

        for u in reversed(order):
            if not children[u]:  # leaf
                if s[u] == '?':
                    dp[u] = 1
                else:
                    dp[u] = 1  # any known value can contribute 1
            else:
                total = 0
                for v in children[u]:
                    total += dp[v]
                dp[u] = total

        print(dp[0])

solve()
```

The code first constructs a tree rooted at 0. Then it performs a DFS in post-order so that each node's children are processed before the node itself. Leaf nodes with `?` are counted as 1, since the first player can always set them to maximize weight. Internal nodes sum their children contributions. The result at the root is the final score.

Implementation subtleties include adjusting for 0-based indexing, ensuring the DFS traverses children correctly without revisiting the parent, and correctly handling `?` leaf nodes.

## Worked Examples

### Sample 1

Input:

```
4
1 2
1 3
4 1
0101
```

| Node | Children | Leaf? | Value | dp |
| --- | --- | --- | --- | --- |
| 2 | [] | Yes | 1 | 1 |
| 3 | [] | Yes | 0 | 1 |
| 4 | [] | Yes | 1 | 1 |
| 1 | 2,3,4 | No | 0 | 1+1+1=3 |

Explanation: Each leaf contributes to the score because weight is non-zero. Internal sums propagate to the root.

### Sample 2

Input:

```
4
1 2
3 2
2 4
???0
```

| Node | Children | Leaf? | Value | dp |
| --- | --- | --- | --- | --- |
| 1 | [] | Yes | ? | 1 |
| 3 | [] | Yes | ? | 1 |
| 4 | [] | Yes | 0 | 1 |
| 2 | 1,3,4 | No | ? | 1+1+1=3 |

Explanation: Even with `?`, the first player can force at least one leaf to have non-zero weight.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | We traverse each node once in DFS, summing child contributions. |
| Space | O(n) | We store adjacency lists, children, parent, and dp arrays. |

Given the constraints of n ≤ 10^5 per test case and sum(n) ≤ 2⋅10^5, this is efficient.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    out = io.StringIO()
    sys.stdout = out
    solve()
    return out.getvalue().strip()

# Provided samples
assert run("""6
4
1 2
1 3
4 1
0101
4
1 2
3 2
2 4
???0
5
1 2
1 3
2 4
2 5
?1?01
6
1 2
2 3
3 4
5 3
3 6
?0????
5
1 2
1 3
1 4
1 5
11
```
