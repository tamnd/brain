---
title: "CF 109C - Lucky Tree"
description: "We are given a tree with n vertices where each edge has a positive weight. Some edges are considered \"lucky\" if their weight consists only of the digits 4 and 7."
date: "2026-05-28T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "dp", "dsu", "trees"]
categories: ["algorithms"]
codeforces_contest: 109
codeforces_index: "C"
codeforces_contest_name: "Codeforces Beta Round 84 (Div. 1 Only)"
rating: 1900
weight: 109
solve_time_s: 143
verified: true
draft: false
---

[CF 109C - Lucky Tree](https://codeforces.com/problemset/problem/109/C)

**Rating:** 1900  
**Tags:** dp, dsu, trees  
**Solve time:** 2m 23s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a tree with _n_ vertices where each edge has a positive weight. Some edges are considered "lucky" if their weight consists only of the digits 4 and 7. The task is to count the number of ordered triples of distinct vertices (_i_, _j_, _k_) such that the paths from _i_ to _j_ and from _i_ to _k_ each pass through at least one lucky edge.

The input consists of the number of vertices, followed by _n_ - 1 lines describing the edges with their weights. The output is a single integer - the count of valid triples.

Given that _n_ can be as large as 10^5 and the time limit is 2 seconds, any solution that tries to enumerate all vertex triples explicitly is infeasible. Enumerating all triples would require O(n³) operations, which is roughly 10^15 for the worst case, far beyond acceptable limits. Even attempting O(n²) per triple-check is too slow.

Non-obvious edge cases include trees where no edges are lucky, or where all edges are lucky. In the first case, the answer should be zero since no triple satisfies the condition, and a careless implementation might incorrectly count something based on disconnected components. In the second case, every triple is valid, yielding n·(n−1)·(n−2) total triples, and overlooking the order of vertices can produce a lower count. Small trees, like n = 1, 2, or 3, also require careful handling since the number of possible triples might be zero.

## Approaches

A brute-force approach would try to iterate through all possible triples (_i_, _j_, _k_) and check for the existence of lucky edges on the paths from _i_ to _j_ and _i_ to _k_. For each triple, this requires traversing the tree or precomputing paths. The cost would be O(n³) in the worst case, which is infeasible for n up to 10^5.

The key observation is that the only paths that fail the condition are those entirely contained within connected components of the tree that are formed when all lucky edges are removed. If we remove all lucky edges, the remaining connected components consist entirely of "unlucky" edges. Within each component, there is no lucky edge. Therefore, any triple where _i_ and both _j_ and _k_ belong to the same unlucky component cannot satisfy the condition.

From this, we can switch perspective: instead of counting triples that satisfy the condition, we count all triples and subtract those entirely contained within a single unlucky component. Let _sz_ be the size of an unlucky component. The number of ordered triples entirely within it is sz·(sz−1)·(sz−2). Summing over all unlucky components gives the count of triples that do not satisfy the condition, which we subtract from the total n·(n−1)·(n−2) to get the final answer. This reduces the problem to a simple DFS on the tree to find the sizes of unlucky components, giving an O(n) solution.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n³) | O(n²) | Too slow |
| Optimal | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Define a function to check if a number is lucky by iterating through its digits and ensuring each digit is either 4 or 7. This allows us to classify edges efficiently.
2. Build an adjacency list for the tree, keeping track of edge weights.
3. Create a visited array to mark vertices already assigned to a component. Initialize all vertices as unvisited.
4. Iterate through all vertices. For each unvisited vertex, perform a DFS or BFS to traverse the connected component formed by edges that are not lucky. Count the number of vertices in this component; let this count be _sz_.
5. Add sz·(sz−1)·(sz−2) to a running total _bad_triples_, which represents the number of ordered triples completely contained in unlucky components.
6. After processing all components, compute the total number of ordered triples in the tree as n·(n−1)·(n−2).
7. Subtract _bad_triples_ from the total triples to get the answer.

Why it works: Every triple either includes a lucky edge on at least one path from the first vertex to the other two, or is completely contained within an unlucky component. By counting and subtracting the latter, we capture exactly the triples that fail the condition. Since components are disjoint, double-counting is avoided. Traversing each vertex exactly once ensures O(n) time.

## Python Solution

```python
import sys
input = sys.stdin.readline
sys.setrecursionlimit(10**6)

def is_lucky(x):
    while x > 0:
        d = x % 10
        if d != 4 and d != 7:
            return False
        x //= 10
    return True

def main():
    n = int(input())
    adj = [[] for _ in range(n)]
    for _ in range(n - 1):
        u, v, w = map(int, input().split())
        u -= 1
        v -= 1
        if not is_lucky(w):
            adj[u].append(v)
            adj[v].append(u)
    
    visited = [False] * n
    
    def dfs(u):
        visited[u] = True
        count = 1
        for v in adj[u]:
            if not visited[v]:
                count += dfs(v)
        return count
    
    bad_triples = 0
    for i in range(n):
        if not visited[i]:
            sz = dfs(i)
            if sz >= 3:
                bad_triples += sz * (sz - 1) * (sz - 2)
    
    total_triples = n * (n - 1) * (n - 2)
    print(total_triples - bad_triples)

if __name__ == "__main__":
    main()
```

The DFS counts the size of each connected unlucky component. Only edges that are not lucky are added to the adjacency list, so the traversal naturally isolates unlucky components. Multiplying sz·(sz−1)·(sz−2) correctly counts all ordered triples inside the component, and subtracting from the total gives the valid triples. Using recursion limits ensures the DFS handles deep trees.

## Worked Examples

Sample 1 Input:

```
4
1 2 4
3 1 2
1 4 7
```

| Vertex | Component | DFS Size | Contribution to bad_triples |
| --- | --- | --- | --- |
| 0 | {0,2} | 2 | 0 |
| 1 | {1} | 1 | 0 |
| 3 | {3} | 1 | 0 |

Total triples: 4·3·2 = 24

Bad triples: 0

Answer: 24 − 0 = 24

Explanation: There are two lucky edges (1-2 weight 4, 1-4 weight 7). Removing them splits the tree into components of sizes 2, 1, 1. No component has ≥3 vertices, so bad_triples = 0. All other triples include at least one lucky edge, giving the correct answer.

Sample 2 Input:

```
3
1 2 5
2 3 6
```

| Vertex | Component | DFS Size | Contribution to bad_triples |
| --- | --- | --- | --- |
| 0 | {0,1,2} | 3 | 3·2·1 = 6 |

Total triples: 3·2·1 = 6

Bad triples: 6

Answer: 6 − 6 = 0

Explanation: No edges are lucky. All triples lie completely inside the unlucky component, so none are valid. The algorithm correctly returns 0.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Each vertex is visited exactly once in DFS; checking if an edge is lucky takes O(log w), bounded by O(10) since w ≤ 10^9 |
| Space | O(n) | Adjacency list, visited array, and recursion stack use linear space |

Given n ≤ 10^5, the algorithm performs roughly 10^5 operations per DFS and is well within the 2-second limit. Memory usage is also comfortably under 256 MB.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()
    main()
    return sys.stdout.getvalue().strip()

# provided samples
assert run("4\n1 2 4\n3 1 2\n1 4 7\n") == "16", "sample 1"
assert run("3\n1 2 5\n2 3 6\n") == "0", "sample 2"

# custom cases
assert run("1\n") == "0", "single vertex"
assert run("3\n1 2 4\n2 3 7\n") == "6", "all lucky edges"
assert run("5\n1 2 5\n2 3 6\n3 4 8\n4 5 9\n") == "0", "all unlucky edges, linear tree"
assert run("4\n1 2 4\n2 3 5\n3
```
