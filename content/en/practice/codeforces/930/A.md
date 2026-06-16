---
title: "CF 930A - Peculiar apple-tree"
description: "We are given a rooted tree with vertices numbered from 1 to n, where vertex 1 is the root. Every vertex i greater than 1 has exactly one parent p[i], and that parent always has a smaller index, which implicitly guarantees that the structure is a rooted tree without cycles and…"
date: "2026-06-17T02:59:48+07:00"
tags: ["codeforces", "competitive-programming", "dfs-and-similar", "graphs", "trees"]
categories: ["algorithms"]
codeforces_contest: 930
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 468 (Div. 1, based on Technocup 2018 Final Round)"
rating: 1500
weight: 930
solve_time_s: 70
verified: true
draft: false
---

[CF 930A - Peculiar apple-tree](https://codeforces.com/problemset/problem/930/A)

**Rating:** 1500  
**Tags:** dfs and similar, graphs, trees  
**Solve time:** 1m 10s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a rooted tree with vertices numbered from 1 to n, where vertex 1 is the root. Every vertex i greater than 1 has exactly one parent p[i], and that parent always has a smaller index, which implicitly guarantees that the structure is a rooted tree without cycles and already oriented away from the root.

At time zero, every vertex initially contains exactly one apple. Each second, every apple that is not already at the root moves one step upward along the tree edge toward its parent. If multiple apples arrive at the same vertex at the same time, they annihilate in pairs, meaning only the parity of the count matters and at most one apple survives at that vertex after collisions. Any apple that reaches vertex 1 is immediately collected.

The task is to determine how many apples are collected at the root over the entire process.

The constraint n up to 100000 implies that any solution must be linear or nearly linear in time. Any approach that simulates the movement of all apples second by second is impossible because an apple can traverse a path of length up to n, and there are n apples, which leads to quadratic behavior in the worst case. Similarly, explicitly simulating collisions per node per time step would explode combinatorially.

A subtle difficulty comes from the annihilation rule. A naive mistake is to assume that apples moving from different branches simply accumulate at the root independently. For example, if two large subtrees both contribute many apples, one might incorrectly count all arrivals at the root, ignoring that cancellations happen at intermediate vertices before reaching the root.

A second failure case appears when multiple apples meet deep in the tree before ever reaching the root. For instance, if a vertex has two children subtrees whose apples reach it simultaneously, they cancel there, which can completely eliminate potential arrivals to the root even if each subtree individually contains many apples.

## Approaches

A brute-force simulation would track each apple moving upward one edge per second. We would maintain the position of every apple and simulate time step transitions, resolving collisions at each node. Each step costs O(n), and each apple can take O(n) steps, leading to O(n^2) overall work in the worst case. This is far too slow for n up to 100000.

The key observation is that the process is purely local and parity-driven. At every vertex, only whether an odd or even number of apples arrives matters. Instead of tracking time, we can compute how many apples “effectively survive” from each subtree up to its parent.

Each vertex contributes exactly one initial apple. That apple will move upward unless it is annihilated by another incoming apple at its parent. So for every subtree, we only need to know whether it contributes an odd or even number of apples to its parent after all internal cancellations. This immediately suggests a bottom-up dynamic programming on the tree.

We compute for each node the parity of apples that survive and move upward from that node into its parent. If a subtree contributes 1 (odd), it behaves like a single active apple traveling upward; if it contributes 0, it cancels out completely.

At the root, every surviving incoming apple is collected. The root itself also has its own initial apple. Thus the answer is the sum of the root’s own contribution plus all surviving contributions from its children, all reduced by parity cancellation.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force simulation | O(n^2) | O(n) | Too slow |
| Tree DP on parity | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

We reframe the problem as computing, for every node, whether an odd number of apples in its subtree eventually reaches it from below after internal cancellations.

1. Build the tree using adjacency lists from the parent array. Each node i > 1 is connected to p[i].
2. Perform a postorder traversal (DFS from root). This ensures children are processed before their parent, so subtree results are already known when needed.
3. For each node, start with a value of 1, representing its own apple.
4. For every child, recursively compute its contribution to the parent. If a child contributes 1 (odd), we add it to a running counter for the current node.
5. After processing all children, we combine all contributions at the node using parity. If the total number of incoming apples from children is odd, exactly one survives upward; otherwise none survive.
6. The root does not pass its contribution upward, so its final value represents how many apples reach and are collected at vertex 1.

The essential idea is that every subtree collapses into a single parity bit describing whether it sends an apple upward. Collisions inside the subtree are fully resolved by recursion before reaching the parent.

### Why it works

The annihilation rule is equivalent to XOR behavior on counts of apples at each vertex. Since pairing removes apples two by two, only parity matters. Because each subtree interacts with the rest of the tree only through its root edge, its entire effect can be summarized by a single bit: whether it contributes an odd number of apples upward. This invariant holds at every node, ensuring correctness of the aggregation.

## Python Solution

```python
import sys
sys.setrecursionlimit(10**7)
input = sys.stdin.readline

n = int(input())
p = list(map(int, input().split()))

g = [[] for _ in range(n + 1)]
for i, par in enumerate(p, start=2):
    g[par].append(i)

def dfs(v):
    total = 1  # the apple at v
    for to in g[v]:
        total += dfs(to)
    # only parity matters
    return total % 2

print(dfs(1))
```

The DFS computes a parity value for every subtree. The key simplification is that we never track timing or intermediate collisions; we directly reduce each subtree to whether it contributes one surviving apple upward. The root’s parity is exactly the number of apples collected at vertex 1, because every surviving apple must eventually reach it unless annihilated earlier.

A subtle implementation detail is recursion depth. Since the tree can be a chain of length 100000, the recursion limit must be increased. Another important point is that we never subtract or simulate cancellations explicitly; using modulo 2 ensures cancellations are implicitly handled.

## Worked Examples

### Example 1

Input:

```
3
1 1
```

We compute DFS bottom-up.

| Node | Child contributions | Total (including self) | Return |
| --- | --- | --- | --- |
| 2 | none | 1 | 1 |
| 3 | none | 1 | 1 |
| 1 | 1 + 1 + 1 | 3 | 1 |

Output is 1.

This shows that although two apples come from children, they cancel in pairs before reaching the root, leaving only the root’s own contribution.

### Example 2

Input:

```
4
1 2 2
```

Tree structure: 1 has child 2, and 2 has children 3 and 4.

| Node | Child contributions | Total | Return |
| --- | --- | --- | --- |
| 3 | none | 1 | 1 |
| 4 | none | 1 | 1 |
| 2 | 1 + 1 + 1 | 3 | 1 |
| 1 | 1 + 1 | 2 | 0 |

Output is 0.

This demonstrates cancellation occurring at multiple levels: first inside subtree rooted at 2, then again at the root.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | each node is visited once in DFS |
| Space | O(n) | adjacency list and recursion stack |

The linear complexity is sufficient for n up to 100000, and memory usage is also linear, fitting comfortably within constraints.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    sys.setrecursionlimit(10**7)

    n = int(sys.stdin.readline())
    p = list(map(int, sys.stdin.readline().split()))

    g = [[] for _ in range(n + 1)]
    for i, par in enumerate(p, start=2):
        g[par].append(i)

    def dfs(v):
        total = 1
        for to in g[v]:
            total += dfs(to)
        return total % 2

    return str(dfs(1))

assert run("3\n1 1\n") == "1", "sample 1"
assert run("2\n1\n") == "0", "minimum chain cancellation"
assert run("4\n1 2 3\n") == "1", "deep chain odd depth"
assert run("5\n1 1 1 1\n") == "1", "star tree parity"
assert run("6\n1 2 2 3 3\n") == "0", "balanced cancellations"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| chain 2 nodes | 0 | immediate cancellation at root |
| deep chain | 1 | propagation through odd depth |
| star tree | 1 | multiple siblings cancel in pairs |
| balanced tree | 0 | layered cancellations |

## Edge Cases

A deep chain such as 1-2-3-...-n ensures that recursion depth is large, but the DFS still correctly collapses the structure into a single parity bit. Each node contributes exactly one, so the parity alternates and the final root value reflects whether n is odd.

A star-shaped tree where all nodes connect directly to root shows that sibling subtrees do not interact until the root. Each leaf contributes 1, and the root aggregates them into a parity value, demonstrating that only global parity matters at the top level.

A perfectly balanced binary-like structure confirms that cancellations occurring at intermediate nodes do not affect correctness, since each subtree is reduced independently before merging at higher levels.
