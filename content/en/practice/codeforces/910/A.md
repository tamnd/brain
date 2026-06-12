---
title: "CF 910A - The Way to Home"
description: "We are given a one-dimensional line of positions from 1 to n. Some positions contain a lily, represented by a 1, while others are empty, represented by a 0. A frog starts at position 1 and wants to reach position n."
date: "2026-06-13T00:24:42+07:00"
tags: ["codeforces", "competitive-programming", "dfs-and-similar", "dp", "greedy", "implementation"]
categories: ["algorithms"]
codeforces_contest: 910
codeforces_index: "A"
codeforces_contest_name: "Testing Round 14 (Unrated)"
rating: 800
weight: 910
solve_time_s: 750
verified: true
draft: false
---

[CF 910A - The Way to Home](https://codeforces.com/problemset/problem/910/A)

**Rating:** 800  
**Tags:** dfs and similar, dp, greedy, implementation  
**Solve time:** 12m 30s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a one-dimensional line of positions from 1 to n. Some positions contain a lily, represented by a `1`, while others are empty, represented by a `0`. A frog starts at position 1 and wants to reach position n.

From any position x where a lily exists, the frog may jump forward to any position y such that 1 ≤ y − x ≤ d, but only if position y also contains a lily. Each jump costs exactly one move, and we want the minimum number of jumps needed to reach position n. If reaching n is impossible, the answer is -1.

The structure is essentially a graph where nodes are lily positions and directed edges exist from i to j if j is reachable from i within distance d. The task reduces to finding the shortest path from node 1 to node n in this implicit graph.

The constraint n ≤ 100 immediately suggests that even quadratic or cubic solutions are acceptable. A full BFS over all transitions would be trivial in this range, but even a greedy scan works because of the small size.

A few edge cases are easy to miss. If all positions except endpoints are zero, for example `10000001`, and d is small, the frog is forced to skip over gaps larger than d, making the destination unreachable. Another subtle case is when multiple short hops exist but a greedy jump of maximum length fails to land on a reachable chain, such as:

```
n = 7, d = 3
1000101
```

Even though a far jump might seem tempting, only intermediate lily positions matter, and skipping them breaks connectivity.

## Approaches

The brute-force idea is to treat each lily position as a node and try every possible sequence of jumps. From position i, we can try all reachable j in [i+1, i+d] that contain a lily, recursively exploring all paths until we reach n. This is correct because it enumerates all valid routes, but it is exponential in nature. In the worst case, where every position has a lily and d is large, the number of paths grows like branching factor d over depth n, which quickly becomes infeasible even for n = 100.

The key observation is that all edges have equal weight, each jump costs exactly 1. This transforms the problem into an unweighted shortest path problem. Instead of exploring all paths, we only need the minimum number of steps to reach each reachable position. This naturally suggests dynamic programming or BFS.

A direct DP interpretation is to maintain `dp[i]` as the minimum jumps needed to reach position i. We initialize dp[1] = 0 and relax transitions forward: from i, we try all j in (i+1 to i+d). If j has a lily, we update dp[j] = min(dp[j], dp[i] + 1). Because n is small, a simple O(n·d) relaxation is sufficient.

An equivalent BFS formulation views each position as a node in a graph with edges to the next d positions that contain lilies. BFS guarantees shortest paths in an unweighted graph.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force (all paths) | Exponential | O(n) recursion stack | Too slow |
| DP / BFS over positions | O(n·d) | O(n) | Accepted |

## Algorithm Walkthrough

1. Convert the string into a boolean array where we can quickly check if a position contains a lily. This allows constant-time validity checks during transitions.
2. Create a distance array `dist` of size n+1 and initialize all values to a large number except `dist[1] = 0`, since we start at position 1 with zero jumps.
3. Iterate through positions from 1 to n. For each position i that is reachable (meaning `dist[i]` is not infinity), we attempt to jump forward.
4. From position i, try all next positions j from i+1 to min(n, i+d). If position j has a lily, we can reach it in one additional jump, so we update `dist[j] = min(dist[j], dist[i] + 1)`.
5. Continue this relaxation process for all positions. Because we always propagate shortest known distances forward, later improvements still refine earlier approximations.
6. After processing, check `dist[n]`. If it is still infinity, output -1. Otherwise output `dist[n]`.

The key idea is that every position is processed in increasing order, and all transitions only move forward, so once we finish processing i, we will never find a better path to i later.

### Why it works

The algorithm maintains the invariant that `dist[i]` always stores the minimum number of jumps required to reach i using only valid lily positions. When we process i, all optimal ways to reach i have already been considered because any path to i must come from a smaller index due to strictly forward movement. Every possible last step into a reachable position is examined exactly once, ensuring no shorter path is missed.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, d = map(int, input().split())
    s = input().strip()
    
    INF = 10**9
    dist = [INF] * n
    dist[0] = 0  # position 1
    
    for i in range(n):
        if dist[i] == INF:
            continue
        if s[i] == '0':
            continue
        for j in range(i + 1, min(n, i + d + 1)):
            if s[j] == '1':
                if dist[j] > dist[i] + 1:
                    dist[j] = dist[i] + 1
    
    print(dist[n - 1] if dist[n - 1] != INF else -1)

if __name__ == "__main__":
    solve()
```

The implementation uses a 0-indexed array to represent positions 1 through n. The `dist` array tracks the minimum number of jumps needed to reach each index. The nested loop enumerates all possible forward jumps of length at most d.

A subtle detail is the condition `if s[i] == '0'`. Even if a position has a computed distance, it is irrelevant unless it actually contains a lily, since the frog cannot stand there. This prevents propagating transitions from invalid states.

The inner loop carefully uses `min(n, i + d + 1)` to avoid out-of-bounds access while preserving all valid jump lengths.

## Worked Examples

### Example 1

Input:

```
8 4
10010101
```

We track `dist` as we process.

| i | dist[i] | s[i] | reachable jumps | updates |
| --- | --- | --- | --- | --- |
| 0 | 0 | 1 | 1-4 | dist[3]=1 |
| 3 | 1 | 1 | 4-7 | dist[4]=2, dist[6]=2 |
| 4 | 2 | 0 | none | none |
| 6 | 2 | 1 | 7-7 | dist[7]=3 |

Final answer is 2 because the best path is 1 → 4 → 8.

This trace confirms that skipping invalid positions (like index 4) does not block progress as long as reachable chains exist.

### Example 2

Input:

```
5 2
10101
```

| i | dist[i] | s[i] | reachable jumps | updates |
| --- | --- | --- | --- | --- |
| 0 | 0 | 1 | 1-2 | dist[2]=1 |
| 2 | 1 | 1 | 3-4 | dist[4]=2 |
| 4 | 2 | 1 | none | none |

Answer is 2.

This shows that even though positions are sparse, the DP correctly chains only valid lily positions.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n·d) | For each reachable position, we scan up to d forward positions |
| Space | O(n) | Distance array stores one value per position |

With n ≤ 100, the maximum number of operations is at most 10,000, which is trivial under the time limit.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    return __import__("builtins").input.__globals__['solve']()

# provided sample
assert run("8 4\n10010101\n") == "2"

# minimal case
assert run("2 1\n11\n") == "1"

# unreachable case
assert run("5 2\n10000\n") == "-1"

# all lilies, large jumps
assert run("6 5\n111111\n") == "1"

# forced multi-step
assert run("7 2\n1010101\n") == "3"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 2 1 / 11 |  |  |
