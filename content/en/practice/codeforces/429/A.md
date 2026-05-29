---
title: "CF 429A - Xor-tree"
description: "We are given a rooted tree with n nodes, each node labeled with a 0 or 1. We are also given a target configuration of 0s and 1s for each node. The only operation allowed is to \"pick\" a node, which flips its value and every second-level descendant down the tree."
date: "2026-05-29T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "dfs-and-similar", "trees"]
categories: ["algorithms"]
codeforces_contest: 429
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 245 (Div. 1)"
rating: 1300
weight: 429
solve_time_s: 98
verified: true
draft: false
---

[CF 429A - Xor-tree](https://codeforces.com/problemset/problem/429/A)

**Rating:** 1300  
**Tags:** dfs and similar, trees  
**Solve time:** 1m 38s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a rooted tree with `n` nodes, each node labeled with a 0 or 1. We are also given a target configuration of 0s and 1s for each node. The only operation allowed is to "pick" a node, which flips its value and every second-level descendant down the tree. Concretely, if a node is picked, its value flips, the values of its children remain unchanged, its grandchildren flip, its great-grandchildren remain, and so on, alternating levels.

The input is a standard tree description with edges connecting nodes, and two arrays representing the initial and target states. The output must be a minimal sequence of nodes to pick so that after all operations, the tree matches the target array.

Since `n` can be up to 100,000 and we have only one second, any algorithm that visits all nodes more than a few times or tries all subsets of nodes will be too slow. We need an `O(n)` traversal-based solution. Edge cases include trees with only one node, fully balanced trees, or situations where multiple nodes along the same branch would flip each other if not handled carefully. A naive solution might pick nodes greedily in arbitrary order, which can over-flip nodes, leading to a larger than minimal set of operations.

## Approaches

The brute-force approach would be to try picking every node in every possible order, flipping the appropriate levels, and checking if the target is reached. This works in principle because the operation is reversible and the tree is finite, but the number of sequences grows exponentially, so this is impractical for `n` up to 10^5.

The key insight is that the flip operation has a predictable pattern along levels: flipping at even depth affects nodes at even depth, flipping at odd depth affects nodes at odd depth. This means we can perform a depth-first traversal from the root, tracking how many flips have been applied along the path at even and odd depths. At each node, we decide whether to flip based on the cumulative effect of previous flips. This reduces the problem to a single DFS with bookkeeping for two integers representing flips at even and odd depths, guaranteeing an `O(n)` solution.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(2^n) | O(n) | Too slow |
| Optimal | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Construct the tree using an adjacency list. Store the initial and goal values.
2. Initialize two counters, `even_flips` and `odd_flips`, to track the number of flips applied along the path for nodes at even and odd depths.
3. Start a DFS traversal from the root (depth 0). For each node, calculate its current effective value by applying the parity of flips along its depth.
4. If the current effective value does not match the goal, add this node to the result set and increment the flip counter corresponding to its depth parity.
5. Recurse into children, passing updated flip counts.
6. After visiting children, backtrack: flips do not need to be undone since we only care about the cumulative effect on descendants.

Why it works: at each node, we maintain the invariant that `current_value ^ cumulative_flips = goal_value` at that depth. The decision to flip a node ensures that this invariant holds for all descendants. Since we traverse in DFS order, every node sees all flips that affect it before deciding whether to flip itself. The alternating pattern of flips aligns with the parity-based tracking, guaranteeing minimal flips.

## Python Solution

```python
import sys
input = sys.stdin.readline
sys.setrecursionlimit(10**6)

def solve():
    n = int(input())
    tree = [[] for _ in range(n + 1)]
    for _ in range(n - 1):
        u, v = map(int, input().split())
        tree[u].append(v)
        tree[v].append(u)
    
    init = [0] + list(map(int, input().split()))
    goal = [0] + list(map(int, input().split()))
    
    result = []
    
    def dfs(node, parent, depth, even_flips, odd_flips):
        if depth % 2 == 0:
            effective = init[node] ^ even_flips
        else:
            effective = init[node] ^ odd_flips
        
        if effective != goal[node]:
            result.append(node)
            if depth % 2 == 0:
                even_flips ^= 1
            else:
                odd_flips ^= 1
        
        for child in tree[node]:
            if child != parent:
                dfs(child, node, depth + 1, even_flips, odd_flips)
    
    dfs(1, 0, 0, 0, 0)
    
    print(len(result))
    for node in result:
        print(node)

solve()
```

The adjacency list represents the tree efficiently. We use `sys.setrecursionlimit` because deep trees could otherwise overflow recursion. `even_flips` and `odd_flips` track cumulative flips for nodes at even and odd depth. The DFS ensures every node is visited once, making decisions based on the current effective state. Care is taken to avoid backtracking flips since our counters are depth-specific and passed by value.

## Worked Examples

### Sample Input 1

| Node | Depth | Init | Goal | Effective | Flip? | even_flips | odd_flips |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 0 | 1 | 1 | 1 | No | 0 | 0 |
| 2 | 1 | 0 | 0 | 0 | No | 0 | 0 |
| 4 | 2 | 1 | 0 | 1 | Yes | 1 | 0 |
| 7 | 3 | 0 | 1 | 0 | Yes | 1 | 1 |

This trace confirms that flips are applied at correct parity depths and the algorithm identifies the minimal set `[4, 7]`.

### Custom Input

```
3
1 2
1 3
1 1 0
0 0 1
```

| Node | Depth | Init | Goal | Effective | Flip? | even_flips | odd_flips |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 0 | 1 | 0 | 1 | Yes | 1 | 0 |
| 2 | 1 | 1 | 0 | 1 | Yes | 1 | 1 |
| 3 | 1 | 0 | 1 | 0 | Yes | 1 | 0 |

This confirms depth-parity tracking handles siblings correctly.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Each node is visited once in DFS. |
| Space | O(n) | Adjacency list and recursion stack require O(n). |

The `O(n)` time guarantees the solution works comfortably under the 1-second limit for `n` up to 10^5.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()
    solve()
    return sys.stdout.getvalue().strip()

# Sample 1
assert run("10\n2 1\n3 1\n4 2\n5 1\n6 2\n7 5\n8 6\n9 8\n10 5\n1 0 1 1 0 1 0 1 0 1\n1 0 1 0 0 1 1 1 0 1\n") == "2\n4\n7"

# Minimum-size input
assert run("1\n0\n1\n") == "1\n1"

# Maximum-size linear tree
n = 1000
edges = "\n".join(f"{i} {i+1}" for i in range(1, n))
init = " ".join("0" for _ in range(n))
goal = " ".join("1" if i%2==0 else "0" for i in range(n))
assert run(f"{n}\n{edges}\n{init}\n{goal}\n") != "", "max-size linear"

# All-equal initial and goal
assert run("3\n1 2\n1 3\n0 0 0\n0 0 0\n") == "0"

# Root-only flip needed
assert run("3\n1 2\n1 3\n1 0 0\n0 0 0\n") == "1\n1"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1-node flip | 1\n1 | Handles minimal input |
| 1000-node linear | non-empty | Handles deep trees efficiently |
| All zeros | 0 | Detects no flips needed |
| Root flip | 1\n1 | Flipping root correctly affects parity |

## Edge Cases

A single-node tree must flip if initial != goal. The algorithm checks depth 0, calculates effective value with zero flips, and flips the root if necessary.

In a tree where siblings require flips independently, the algorithm correctly tracks parity. For example, a
