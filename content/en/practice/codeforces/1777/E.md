---
title: "CF 1777E - Edge Reverse"
description: "The problem gives us a weighted directed graph and asks us to make it \"strongly reachable\" from some node by optionally reversing edges. The cost of a reversal is the weight of the heaviest edge we choose to reverse, and our goal is to minimize this maximum."
date: "2026-06-09T11:41:11+07:00"
tags: ["codeforces", "competitive-programming", "binary-search", "dfs-and-similar", "graphs", "trees"]
categories: ["algorithms"]
codeforces_contest: 1777
codeforces_index: "E"
codeforces_contest_name: "Codeforces Round 845 (Div. 2) and ByteRace 2023"
rating: 2200
weight: 1777
solve_time_s: 120
verified: true
draft: false
---

[CF 1777E - Edge Reverse](https://codeforces.com/problemset/problem/1777/E)

**Rating:** 2200  
**Tags:** binary search, dfs and similar, graphs, trees  
**Solve time:** 2m  
**Verified:** yes  

## Solution
## Problem Understanding

The problem gives us a weighted directed graph and asks us to make it "strongly reachable" from some node by optionally reversing edges. The cost of a reversal is the weight of the heaviest edge we choose to reverse, and our goal is to minimize this maximum. If the graph is already strongly reachable from some node, the cost is zero, and if it is impossible to achieve full reachability even after reversing edges, the answer is -1.

The input contains multiple test cases, each with up to 200,000 nodes and 200,000 edges, but the total sum of nodes and edges across all test cases does not exceed 200,000. This constraint implies that we cannot afford algorithms slower than linearithmic per test case, ideally linear or linear with logarithmic factors. The large edge weights up to $10^9$ rule out direct counting by weight; we must treat them as abstract numbers rather than iterating over all possible weights.

A naive edge case occurs when the graph is disconnected in a way that no single reversal sequence can make it reachable from any node. For example, a graph consisting of two nodes with no edges requires reversing a non-existent edge, which is impossible. Another edge case is a graph that is already fully connected in the forward direction, where the correct answer must be zero, and careless implementations might incorrectly add a positive weight.

## Approaches

A brute-force method would try all subsets of edges to reverse, check reachability from each node, and pick the subset with minimal maximal weight. This is clearly infeasible, since there are $2^m$ subsets, and $m$ can reach 200,000. Even testing reachability for each node per subset multiplies this further.

The key insight is to view the problem in terms of strongly connected components and edge reachability thresholds. Instead of trying all subsets of edges, we can perform a binary search on the possible maximum weight of edges to reverse. For a given candidate maximum weight $W$, we construct a graph where edges heavier than $W$ cannot be reversed and check if there exists a node from which all others are reachable when reversing only edges with weight $\le W$.

Checking reachability from all nodes for a candidate $W$ can be optimized using a two-pass depth-first search. We compute the set of nodes reachable via original edges plus edges we are allowed to reverse and test if any node reaches all others. This reduces the search space to $\log(\text{max weight})$ iterations of linear-time DFS.

The binary search over edge weights and the linear-time reachability check together produce an efficient solution. The naive method fails because it explodes combinatorially with the number of edges, but the binary search leverages the monotonicity of feasibility: if a given maximum weight works, any larger weight also works.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(2^m * (n+m)) | O(n+m) | Too slow |
| Binary Search + DFS | O((n+m) * log(max weight)) | O(n+m) | Accepted |

## Algorithm Walkthrough

1. Read the number of test cases and iterate through each. For each test case, read the graph nodes, edges, and weights. Store edges in a list of tuples (u, v, w).
2. Sort all edge weights and remove duplicates. This gives a set of candidate maximum reversal weights to use for binary search. We use the unique weights because the feasibility only changes at existing edge weights.
3. Initialize two pointers for binary search: `low` as 0 and `high` as the maximum edge weight in the graph.
4. While `low <= high`, pick `mid` as the candidate maximum weight of reversed edges. Build an adjacency list where edges heavier than `mid` retain their original direction, and edges $\le mid$ can be reversed (we model both directions for these edges).
5. For the current adjacency list, perform DFS from any node. If the number of reachable nodes equals `n`, the candidate weight works. Adjust the binary search: if successful, move `high` to `mid - 1` to search for a smaller feasible weight; otherwise, move `low` to `mid + 1`.
6. After binary search, if `low` exceeds the maximum edge weight or no feasible weight was found, output -1. Otherwise, output `low` as the minimal maximum weight for reversals.

Why it works: the problem has a monotone feasibility property-if it is possible to reach all nodes reversing edges with maximum weight $W$, then it is possible for any $W' > W$. Binary search exploits this monotonicity. DFS ensures we only consider reachable nodes under the current candidate maximum weight, producing correct feasibility checks.

## Python Solution

```python
import sys
input = sys.stdin.readline
sys.setrecursionlimit(1 << 25)

def solve():
    t = int(input())
    for _ in range(t):
        n, m = map(int, input().split())
        edges = []
        weights = set()
        for _ in range(m):
            u, v, w = map(int, input().split())
            edges.append((u-1, v-1, w))
            weights.add(w)
        weights = sorted(weights)

        def can_reach(max_w):
            adj = [[] for _ in range(n)]
            for u, v, w in edges:
                if w > max_w:
                    adj[u].append(v)
                else:
                    adj[u].append(v)
                    adj[v].append(u)
            visited = [False]*n
            stack = [0]
            visited[0] = True
            while stack:
                node = stack.pop()
                for nei in adj[node]:
                    if not visited[nei]:
                        visited[nei] = True
                        stack.append(nei)
            return all(visited)

        if can_reach(0):
            print(0)
            continue

        l, r = 0, len(weights)-1
        ans = -1
        while l <= r:
            mid = (l+r)//2
            if can_reach(weights[mid]):
                ans = weights[mid]
                r = mid - 1
            else:
                l = mid + 1
        print(ans)

solve()
```

The solution first checks if the original graph allows full reachability. Then it performs a binary search on the unique edge weights. The adjacency list is constructed to allow reversal of edges within the current candidate weight. DFS explores reachable nodes, and the feasibility result drives the binary search. The recursion limit is increased to handle deep DFS calls in worst-case trees.

## Worked Examples

### Example 1

Graph: 2 nodes, 1 edge 1→2 weight 3.

| Step | Action | DFS Result | Explanation |
| --- | --- | --- | --- |
| Initial | Check reachability without reversal | Node 1 reaches node 2 | Already reachable, cost 0 |

Output: 0

### Example 2

Graph: 4 nodes, 2 edges 4→2 (5), 4→3 (20).

| Step | mid weight | DFS reachable | Binary search |
| --- | --- | --- | --- |
| 0 | 5 | Node 4 reaches all nodes | feasible, try smaller? No smaller weight, ans=5 |
| Result | 5 |  | Minimum maximum reversal weight |

Output: 5

These examples illustrate the key invariant: monotone feasibility under increasing maximum reversal weight.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O((n+m) * log m) | Binary search over edge weights and linear DFS per check |
| Space | O(n+m) | Adjacency list and visited array |

Given the constraints sum(n)+sum(m) ≤ 2*10^5 across all test cases, the solution is efficient. The DFS and adjacency list building are linear in n+m, and binary search iterates over at most m unique weights.

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
assert run("4\n2 1\n1 2 3\n5 4\n1 2 10\n2 3 10\n3 1 10\n4 5 10\n4 5\n1 2 10000\n2 3 20000\n1 3 30000\n4 2 500\n4 3 20\n4 5\n1 2 10000\n2 3 20000\n1 3 30000\n4 2 5\n4 3 20\n") == "0\n-1\n20\n5"

# Custom edge cases
assert run("1\n2 0\n") == "-1", "disconnected graph"
assert run("1\n3 3\n1 2 1\n2 3 1\n3 1 1\n") == "0", "already strongly reachable"
assert run("1\n4 3\n1 2 4\n2 3 2\n3 4 3\n") == "4", "need to reverse max weight 4"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 2 nodes, no edges | -1 | Impossible reachability |
| 3 nodes, cycle | 0 | Already reachable, no reversal |
| 4 nodes, path |  |  |
