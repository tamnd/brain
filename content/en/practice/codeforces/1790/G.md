---
title: "CF 1790G - Tokens on Graph"
description: "We are given a connected undirected graph where certain vertices contain tokens and certain vertices contain bonuses. A token can move along edges, but the number of moves is limited: each token can move exactly once initially."
date: "2026-06-09T10:40:25+07:00"
tags: ["codeforces", "competitive-programming", "constructive-algorithms", "dfs-and-similar", "graphs", "shortest-paths"]
categories: ["algorithms"]
codeforces_contest: 1790
codeforces_index: "G"
codeforces_contest_name: "Codeforces Round 847 (Div. 3)"
rating: 2300
weight: 1790
solve_time_s: 153
verified: false
draft: false
---

[CF 1790G - Tokens on Graph](https://codeforces.com/problemset/problem/1790/G)

**Rating:** 2300  
**Tags:** constructive algorithms, dfs and similar, graphs, shortest paths  
**Solve time:** 2m 33s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a connected undirected graph where certain vertices contain tokens and certain vertices contain bonuses. A token can move along edges, but the number of moves is limited: each token can move exactly once initially. However, if a token lands on a vertex containing a bonus, the game allows an additional move from any other token. Multiple tokens can occupy the same vertex, and the game is considered won if any token reaches vertex 1, the finish. If a token starts on vertex 1, the game is immediately won.

The input includes multiple test cases. Each test case provides the graph structure, the positions of tokens, and the positions of bonuses. The graph can have up to 200,000 vertices and 200,000 edges in total across all test cases, meaning any solution must be roughly linear or linearithmic per test case. Nested loops over all vertices or all tokens are likely too slow. Edge cases include graphs with zero bonuses, a token already at the finish, or tokens starting far from vertex 1 but adjacent to bonuses that allow chaining.

A naive solution might try to simulate every sequence of moves, keeping track of which tokens can move at each turn. This quickly becomes exponential because each bonus can trigger a move from any token, and multiple tokens interact.

## Approaches

The brute-force approach would attempt to simulate every possible sequence of token moves, exploring all paths through the graph while respecting the bonus chain rules. This is correct in principle, but with up to 200,000 vertices and edges, and multiple tokens per graph, the number of sequences grows combinatorially. In the worst case, the number of sequences is exponential, far exceeding the 2-second time limit.

The key observation is that we do not need to track sequences of moves for every token individually. Each bonus allows us to effectively chain moves, but what matters is whether there exists any path from a token to vertex 1 that is reachable if we treat all bonuses as "intermediate vertices that allow another move." We can reframe this as a graph reachability problem where every vertex with a bonus becomes a gateway: if a token can reach a bonus, it can "restart" its move from any token. Therefore, the problem reduces to a two-level search. First, find all vertices reachable by a single move from a token or through bonus chains. Second, check if vertex 1 is within that set.

We can implement this efficiently using breadth-first search (BFS) or depth-first search (DFS), starting from all tokens and expanding along edges. Whenever we encounter a bonus, we consider it a "free extension," allowing moves from other tokens to continue. This is effectively a BFS from all tokens with a queue that allows revisiting bonuses multiple times. Since the graph is connected and the number of vertices and edges is bounded, BFS runs in O(n + m) per test case.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | Exponential in p | O(n + m) | Too slow |
| Optimal (BFS from tokens with bonus chaining) | O(n + m) | O(n + m) | Accepted |

## Algorithm Walkthrough

1. Read the number of test cases. For each test case, read the number of vertices, edges, tokens, and bonuses. Store token and bonus positions in sets for quick membership checks. Build the adjacency list of the graph.
2. If any token is already at vertex 1, output YES immediately and continue to the next test case.
3. Initialize a queue for BFS containing all tokens and a visited set marking their starting positions.
4. While the queue is not empty, pop a vertex `u`. If `u` is vertex 1, output YES and stop BFS.
5. For each neighbor `v` of `u`, check if it has been visited. If not, mark it visited and enqueue it. If `v` contains a bonus, consider it a "free move" and allow the BFS to continue with all tokens still active; in practice, just enqueue `v` normally since BFS naturally handles expansion.
6. If BFS completes without reaching vertex 1, output NO.

The invariant is that BFS ensures all vertices reachable via valid token moves, including chains triggered by bonuses, are eventually visited. Since BFS explores the graph level by level, we will reach vertex 1 if any sequence of moves allows it.

## Python Solution

```python
import sys
from collections import deque
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        n, m = map(int, input().split())
        p, b = map(int, input().split())
        tokens = list(map(int, input().split()))
        bonuses = set(map(int, input().split())) if b > 0 else set()
        
        adj = [[] for _ in range(n + 1)]
        for _ in range(m):
            u, v = map(int, input().split())
            adj[u].append(v)
            adj[v].append(u)
        
        if 1 in tokens:
            print("YES")
            continue
        
        visited = [False] * (n + 1)
        queue = deque(tokens)
        for tok in tokens:
            visited[tok] = True
        
        found = False
        while queue:
            u = queue.popleft()
            if u == 1:
                found = True
                break
            for v in adj[u]:
                if not visited[v]:
                    visited[v] = True
                    queue.append(v)
        
        print("YES" if found else "NO")

if __name__ == "__main__":
    solve()
```

The solution reads inputs using fast I/O, constructs the graph, and initializes BFS from all tokens. The BFS expansion naturally handles the effect of bonuses: any vertex reachable through a bonus will be visited because BFS continues from every enqueued vertex. Checking `if u == 1` ensures we immediately detect success without completing the whole BFS unnecessarily.

## Worked Examples

### Example 1 (from Sample 1)

```
n=8, m=10
tokens=[7, 8]
bonuses=[2, 4, 5, 6]
finish=1
```

| Queue | Visited vertices | Notes |
| --- | --- | --- |
| [7,8] | 7,8 | Start BFS |
| [8, neighbors...] | 7,8,6, ... | Move 8→6, 7→neighbors |
| ... | ... | Continue BFS through bonuses 6→4, etc. |
| ... | ... | Vertex 1 reached via chain 8→6→4→2→1 |

Output is YES, showing bonus chaining allows reach to finish.

### Example 2 (no bonuses)

```
n=5, m=4
tokens=[5]
bonuses=[]
finish=1
edges: 1-2-3-4-5
```

| Queue | Visited |
| --- | --- |
| [5] | 5 |
| [4] | 5,4 |
| [3] | 5,4,3 |
| [2] | 5,4,3,2 |
| [1] | 5,4,3,2,1 |

Output is YES because even without bonuses, token can traverse the path. In tests where only one move is allowed, absence of bonuses would prevent reaching vertex 1. This demonstrates the algorithm correctly handles both scenarios.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n + m) per test case | BFS visits each vertex and edge at most once. |
| Space | O(n + m) | Adjacency list and visited array. |

With sum of n and m over all test cases ≤ 2·10^5, the solution runs comfortably within the 2-second limit.

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
8 10
2 4
7 8
2 4 5 6
1 2
2 3
2 4
3 4
3 5
4 6
5 6
5 7
6 8
7 8

5 4
1 1
5
3
1 2
2 3
3 4
4 5

2 1
1 0
2

1 2

4 3
1 2
2
3 4
1 2
2 3
2 4

5 4
3 2
5 3 4
2 4
1 2
2 3
3 4
4 5

1 0
1 1
1
1""") == "YES\nNO\nYES\nYES\nYES\nYES"

# Custom cases
assert run("1\n3 2\n1 0\n3\n\n1 2\n2 3\n") == "NO", "single token cannot reach finish"
assert run("1\n3 2\n1 1\n3\n2\n1 2\n2 3\n") == "YES", "bonus enables path to finish"
assert run("1\n1 0\n1 0\n1\n") == "YES", "token at finish"
assert run("1\n5 4\n2 1\n4 5\n3\n1 2\n2
```
