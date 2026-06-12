---
title: "CF 919D - Substring"
description: "We are given a directed graph where each vertex carries a lowercase letter. A valid walk follows directed edges from node to node, and we are allowed to revisit nodes and edges as long as we respect direction."
date: "2026-06-13T02:42:04+07:00"
tags: ["codeforces", "competitive-programming", "dfs-and-similar", "dp", "graphs"]
categories: ["algorithms"]
codeforces_contest: 919
codeforces_index: "D"
codeforces_contest_name: "Codeforces Round 460 (Div. 2)"
rating: 1700
weight: 919
solve_time_s: 767
verified: true
draft: false
---

[CF 919D - Substring](https://codeforces.com/problemset/problem/919/D)

**Rating:** 1700  
**Tags:** dfs and similar, dp, graphs  
**Solve time:** 12m 47s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a directed graph where each vertex carries a lowercase letter. A valid walk follows directed edges from node to node, and we are allowed to revisit nodes and edges as long as we respect direction.

For any such walk, we look at the sequence of letters we encounter along the visited nodes. The value of the walk is defined as the maximum frequency of any single letter along that sequence. For example, if the walk produces the string “abaca”, then the best letter is ‘a’, which appears 3 times, so the value is 3.

The task is to find a walk with the maximum possible value. If there exists a cycle that allows us to keep accumulating occurrences of some letter indefinitely, the answer is unbounded and we must return -1.

The input size reaches up to 300,000 nodes and edges. This immediately rules out any approach that enumerates paths or performs exponential exploration. Even O(n²) is too large in practice, so we are forced toward a linear or near-linear graph traversal strategy.

A subtle edge case appears when the graph contains a directed cycle. If that cycle is reachable and contains at least one node contributing a particular letter, then by looping indefinitely we can increase that letter’s count without bound. For instance, if nodes 1 → 2 → 3 → 1 form a cycle and all have letter 'a', then the answer is -1. A naive DFS that tracks best path sums without detecting revisits will incorrectly treat cycles as finite and produce a bounded answer.

Another issue is that even when cycles exist, not all of them imply infinity. If a cycle exists but we are counting a letter not present in the cycle, the cycle does not help increase that letter’s frequency. The correct reasoning depends on tracking letter-specific accumulation, not just reachability.

## Approaches

A brute-force strategy would attempt to explore all paths in the graph and compute letter frequencies along each path. One could imagine doing DFS from every node, maintaining a 26-length frequency array and updating a global maximum. This is conceptually correct for small graphs but fails because each node may be revisited through many paths, and cycles create infinitely many walks. Even if we restrict ourselves to simple paths, the number of them in a directed graph can grow exponentially.

The key insight is to reverse the perspective. Instead of thinking in terms of paths, we treat this as a longest path problem on a DAG, but with a twist: we need 26 independent dynamic programs, one per letter. For each letter c, we want to compute the maximum number of occurrences of c along any path ending at each node.

If the graph had no cycles, this would be straightforward. We could topologically sort the graph and relax transitions: for each edge u → v, we propagate best values forward. The presence of cycles breaks this, but we can detect cycles using Kahn’s algorithm. If we fail to process all nodes in topological order, a cycle exists, and since any cycle can be traversed repeatedly along a path, it implies the possibility of arbitrarily large accumulation for at least one letter along some reachable cycle. In that case, we return -1.

Thus the solution becomes a combination of cycle detection and multi-source dynamic programming over the DAG structure.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force DFS over paths | Exponential | O(n) | Too slow |
| Toposort + DP per letter | O(26 · (n + m)) | O(26 · n) | Accepted |

## Algorithm Walkthrough

We treat each letter independently and compute best possible counts using a DP over a topological ordering.

1. Build adjacency list and compute indegrees of all nodes. This prepares us for Kahn’s algorithm, which processes nodes in a valid topological order when the graph is acyclic.
2. Initialize a DP table `dp[v][c]` meaning the maximum number of occurrences of letter `c` along any path ending at node `v`. Initially all zeros. If node `v` itself has letter `c`, we set `dp[v][c] = 1`.
3. Push all nodes with indegree 0 into a queue. These are valid starting points for any path.
4. Repeatedly pop a node `u` from the queue and propagate its DP values to its neighbors `v`. For each letter `c`, we attempt to update:

`dp[v][c] = max(dp[v][c], dp[u][c] + (1 if s[v] == c else 0))`.

This step ensures that any best path ending at `u` can be extended to `v`.
5. Whenever we relax an edge, decrement indegree of the destination node. If it becomes zero, push it into the queue. This maintains correct topological processing order.
6. Keep a counter of processed nodes. If after the queue finishes we have not processed all nodes, a cycle exists. In that case, return -1 because some cycle can be used to repeat traversal indefinitely, making the answer unbounded.
7. After processing, the answer is the maximum value over all dp[v][c].

The reasoning behind the DP is that any valid path in a DAG can be decomposed according to a topological order, and optimal substructure holds because extending a best path into a neighbor preserves optimality.

### Why it works

The core invariant is that when a node `u` is popped from the queue, all paths ending at `u` have already been fully considered in terms of DP values. This is guaranteed by topological ordering: every incoming edge to `u` originates from a node that has already been processed.

Therefore, `dp[u][c]` is final when `u` is processed, and all future updates to neighbors correctly build on a complete subproblem solution. Since every acyclic graph admits a topological ordering, this ensures we explore all valid paths exactly once in dependency order.

If a cycle exists, Kahn’s algorithm cannot process all nodes, meaning there is no valid topological ordering. That corresponds exactly to the existence of a cycle, which in this problem implies the possibility of infinite repetition along some path, so returning -1 is correct.

## Python Solution

```python
import sys
input = sys.stdin.readline
from collections import deque

def solve():
    n, m = map(int, input().split())
    s = input().strip()

    g = [[] for _ in range(n)]
    indeg = [0] * n

    for _ in range(m):
        x, y = map(int, input().split())
        x -= 1
        y -= 1
        g[x].append(y)
        indeg[y] += 1

    dp = [[0] * 26 for _ in range(n)]

    for i in range(n):
        dp[i][ord(s[i]) - 97] = 1

    q = deque([i for i in range(n) if indeg[i] == 0])
    visited = 0

    while q:
        u = q.popleft()
        visited += 1

        for v in g[u]:
            for c in range(26):
                val = dp[u][c] + (1 if ord(s[v]) - 97 == c else 0)
                if val > dp[v][c]:
                    dp[v][c] = val

            indeg[v] -= 1
            if indeg[v] == 0:
                q.append(v)

    if visited < n:
        print(-1)
        return

    ans = 0
    for i in range(n):
        ans = max(ans, max(dp[i]))
    print(ans)

if __name__ == "__main__":
    solve()
```

The solution relies on Kahn’s algorithm to enforce acyclic processing order. The DP table is updated in place during edge relaxation, and each state represents the best achievable frequency for each letter up to that node. A common implementation pitfall is forgetting to initialize `dp[i][s[i]] = 1`, which would incorrectly treat starting nodes as contributing zero occurrences of their own letter.

Another subtle point is cycle detection: simply checking whether a node is revisited is not enough. The correct criterion is whether topological processing finishes all nodes.

## Worked Examples

### Example 1

Input:

```
5 4
abaca
1 2
1 3
3 4
4 5
```

We track only key states for letter 'a'.

| Step | Node | dp at node (a) | Action |
| --- | --- | --- | --- |
| init | - | [1,0,1,1,1] per node basis | initialize from labels |
| process 1 | 1 | propagates to 2,3 | dp[2]=1, dp[3]=2 |
| process 3 | 3 | dp[3]=2 | propagate to 4 |
| process 4 | 4 | dp[4]=3 | propagate to 5 |
| process 5 | 5 | dp[5]=3 | final |

The best path accumulates three 'a' characters along 1 → 3 → 4 → 5, confirming output 3.

### Example 2

Input:

```
3 3
aaa
1 2
2 3
3 1
```

| Step | Queue state | processed | cycle detected |
| --- | --- | --- | --- |
| init | [1,2,3] may form cycle | partial processing | indegree never fully clears |

After processing, not all nodes are visited due to the cycle 1 → 2 → 3 → 1. The algorithm returns -1 immediately.

This confirms that any cycle reachable in the graph leads to an unbounded value when letters can be accumulated indefinitely.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(26 · (n + m)) | Each edge relaxes 26 letter states once |
| Space | O(26 · n) | DP table for each node and letter |

With n, m up to 300,000, this runs comfortably within limits since the constant factor 26 is manageable and all operations are linear scans over edges.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from collections import deque

    n, m = map(int, input().split())
    s = input().strip()

    g = [[] for _ in range(n)]
    indeg = [0] * n

    for _ in range(m):
        x, y = map(int, input().split())
        x -= 1
        y -= 1
        g[x].append(y)
        indeg[y] += 1

    dp = [[0] * 26 for _ in range(n)]
    for i in range(n):
        dp[i][ord(s[i]) - 97] = 1

    q = deque([i for i in range(n) if indeg[i] == 0])
    visited = 0

    while q:
        u = q.popleft()
        visited += 1
        for v in g[u]:
            for c in range(26):
                val = dp[u][c] + (1 if ord(s[v]) - 97 == c else 0)
                if val > dp[v][c]:
                    dp[v][c] = val
            indeg[v] -= 1
            if indeg[v] == 0:
                q.append(v)

    if visited < n:
        return "-1"

    return str(max(max(row) for row in dp))

# provided sample
assert run("""5 4
abaca
1 2
1 3
3 4
4 5
""") == "3"

# single node
assert run("""1 0
a
""") == "1"

# simple chain
assert run("""3 2
abc
1 2
2 3
""") == "1"

# all same letters no cycle
assert run("""4 3
aaaa
1 2
2 3
3 4
""") == "4"

# cycle case
assert run("""3 3
abc
1 2
2 3
3 1
""") == "-1"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single node | 1 | base case initialization |
| chain graph | 1 | DP propagation correctness |
| all same letters DAG | 4 | accumulation across path |
| cycle graph | -1 | cycle detection |

## Edge Cases

A minimal node graph tests initialization behavior. With a single node labeled 'a', there are no edges, so the DP should directly return 1. The algorithm initializes dp[0][a] = 1 and processes it immediately, producing the correct result.

A fully cyclic graph tests unbounded growth detection. In a triangle cycle 1 → 2 → 3 → 1, indegrees never drop to zero for all nodes, so Kahn’s algorithm processes fewer than n nodes. The visited counter detects this and returns -1, correctly signaling infinite accumulation potential.
