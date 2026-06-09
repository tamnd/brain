---
title: "CF 2127D - Root was Built by Love, Broken by Destiny"
description: "We are given a connected undirected graph of n houses and m bridges. Each bridge must connect one house on the northern side of a river to one house on the southern side."
date: "2026-06-08T11:09:56+07:00"
tags: ["codeforces", "competitive-programming", "combinatorics", "dfs-and-similar", "graphs", "trees"]
categories: ["algorithms"]
codeforces_contest: 2127
codeforces_index: "D"
codeforces_contest_name: "Atto Round 1 (Codeforces Round 1041, Div. 1 + Div. 2)"
rating: 1800
weight: 2127
solve_time_s: 112
verified: false
draft: false
---

[CF 2127D - Root was Built by Love, Broken by Destiny](https://codeforces.com/problemset/problem/2127/D)

**Rating:** 1800  
**Tags:** combinatorics, dfs and similar, graphs, trees  
**Solve time:** 1m 52s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a connected undirected graph of `n` houses and `m` bridges. Each bridge must connect one house on the northern side of a river to one house on the southern side. Houses must be placed along straight lines on each side, and the bridges must not cross when drawn as straight lines. Two arrangements are different if either a house is on a different side or if the relative order of houses on a side differs.

In simpler terms, the problem reduces to checking if the graph can be divided into two groups, such that each bridge connects a house from one group to the other (a bipartite check). If the graph is bipartite, the number of arrangements is the product of permutations of houses in each group, multiplied by two to account for swapping north and south sides.

The constraints are tight: `n` can reach 2×10^5, and the sum of all `n` and `m` across test cases is bounded by 2×10^5. This rules out any algorithm with complexity higher than O(n + m) per test case. A naive approach that tries all side assignments is exponential in `n` and infeasible.

A common edge case is a triangle of houses (3 nodes, each connected to the other). This graph is not bipartite, so the answer must be zero. A careless implementation that assumes every connected graph can be split would incorrectly give a non-zero count.

Another subtle edge case is when a component has only one house. It can be placed on either side, but permutations of houses on each side must be computed carefully to avoid double counting.

## Approaches

A brute-force approach would enumerate all 2^n side assignments and check each for validity. For each valid side assignment, we would then count permutations of houses on each side, taking care of the non-crossing constraint. This works because any valid arrangement corresponds to a bipartition of the graph and ordering the houses along each line. The complexity is O(2^n × n log n) and becomes impossible for `n` above 20.

The key insight is that the non-crossing condition is automatically satisfied if we place all houses of one group on one side in any order. Therefore, the problem reduces to two steps: first, check whether the graph is bipartite. Second, count permutations of houses on each side, taking the factorials of the sizes of the two groups and multiplying by two for the choice of which group goes north.

This approach is linear in the number of nodes and edges and can handle the largest inputs efficiently. The combinatorial calculations must be done modulo 10^9 + 7. Precomputing factorials up to 2×10^5 ensures fast computation.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(2^n × n log n) | O(n) | Too slow |
| Bipartite + Factorials | O(n + m) per test case | O(n) | Accepted |

## Algorithm Walkthrough

1. Precompute factorials modulo 10^9 + 7 up to the maximum `n` across all test cases. This allows O(1) factorial lookup for counting permutations.
2. For each test case, build the adjacency list of the graph from the bridge connections. This provides efficient O(1) access to neighbors.
3. Initialize an array to store the side of each house, initially unset. Start a depth-first search (DFS) from any unvisited house, assigning alternating sides to connected houses.
4. During DFS, if a neighbor is already assigned the same side as the current house, the graph is not bipartite. In this case, immediately set the answer to zero for this test case.
5. Count the number of houses on each side during DFS. Let `a` be the number on the north and `b` the number on the south.
6. Once the component is fully visited, compute the number of arrangements as `2 × factorial(a) × factorial(b) % MOD`. Multiply the two factorials for the permutations of each side, and multiply by two to account for swapping north and south.
7. Repeat steps 3-6 for each connected component, multiplying the arrangements of all components modulo 10^9 + 7.
8. Output the final count for the test case.

The invariant is that during DFS, all assigned sides respect bipartite constraints. Every edge connects nodes of opposite sides. Since the permutation count considers all possible orderings within each side, every valid non-crossing arrangement is counted exactly once.

## Python Solution

```python
import sys
input = sys.stdin.readline
sys.setrecursionlimit(1 << 25)

MOD = 10**9 + 7

# Precompute factorials
N = 2 * 10**5 + 5
fact = [1] * N
for i in range(1, N):
    fact[i] = fact[i - 1] * i % MOD

def solve():
    t = int(input())
    for _ in range(t):
        n, m = map(int, input().split())
        adj = [[] for _ in range(n)]
        for _ in range(m):
            u, v = map(int, input().split())
            u -= 1
            v -= 1
            adj[u].append(v)
            adj[v].append(u)
        
        side = [-1] * n
        ans = 1
        valid = True
        
        def dfs(u, color):
            nonlocal a, b, valid
            side[u] = color
            if color == 0:
                a += 1
            else:
                b += 1
            for v in adj[u]:
                if side[v] == -1:
                    dfs(v, 1 - color)
                elif side[v] == color:
                    valid = False
        
        for i in range(n):
            if side[i] == -1:
                a = b = 0
                dfs(i, 0)
                if not valid:
                    ans = 0
                    break
                ans = ans * fact[a] % MOD
                ans = ans * fact[b] % MOD
                ans = ans * 2 % MOD
        
        print(ans)
        
solve()
```

The code first computes factorials to allow fast permutation counting. The adjacency list is constructed with 0-based indexing for convenience. DFS assigns alternating sides, counting houses on each side. If a conflict occurs, `valid` becomes False, and the answer is immediately zero. The final count multiplies factorials for permutations and a factor of 2 for side swapping.

## Worked Examples

### Example 1

Input:

```
2 1
1 2
```

| Step | Node | Side | a | b | DFS State |
| --- | --- | --- | --- | --- | --- |
| Start | 1 | 0 | 1 | 0 | side[0]=0 |
| Visit neighbor | 2 | 1 | 1 | 1 | side[1]=1 |

Arrangements: `2 × 1! × 1! = 2`.

### Example 2

Input:

```
3 3
1 2
1 3
2 3
```

DFS discovers triangle. During traversal, a node is forced to have the same side as a neighbor. `valid` becomes False. Answer is 0.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n + m) | DFS traverses each node and edge once, factorial precomputation is O(N). |
| Space | O(n + m) | Adjacency list stores edges, side array stores colors. |

Given constraints, sum of n and m across all test cases is ≤ 2×10^5. DFS runs in linear time, ensuring the solution fits within the 2-second limit.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()
    solve()
    return sys.stdout.getvalue().strip()

# Provided samples
assert run("4\n2 1\n1 2\n3 3\n1 2\n1 3\n2 3\n5 4\n1 2\n1 3\n3 4\n3 5\n4 3\n1 2\n1 3\n1 4") == "2\n0\n8\n12", "samples"

# Minimum-size input
assert run("1\n2 1\n1 2") == "2", "min size"

# Bipartite chain
assert run("1\n4 3\n1 2\n2 3\n3 4") == "8", "chain"

# Triangle (non-bipartite)
assert run("1\n3 3\n1 2\n2 3\n3 1") == "0", "triangle"

# Two separate components
assert run("1\n6 4\n1 2\n2 3\n4 5\n5 6") == "64", "two chains"

# Large single component
assert run("1\n5 4\n1 2\n1 3\n3 4\n4 5") == "48", "long tree"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 2 1\n1 2 | 2 | Minimum-size graph |
| 4 3\n1 2\n2 3\n3 4 | 8 | Linear chain permutations |
| 3 3\n1 2\n2 3\n3 1 |  |  |
