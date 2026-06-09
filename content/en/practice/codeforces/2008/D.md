---
title: "CF 2008D - Sakurako's Hobby"
description: "We are given a permutation of integers from 1 to n, and each number is colored black or white. From any starting integer i, we can repeatedly apply the permutation to jump from i to pi, then to p{pi}, and so on."
date: "2026-06-08T13:24:56+07:00"
tags: ["codeforces", "competitive-programming", "dp", "dsu", "graphs", "math"]
categories: ["algorithms"]
codeforces_contest: 2008
codeforces_index: "D"
codeforces_contest_name: "Codeforces Round 970 (Div. 3)"
rating: 1100
weight: 2008
solve_time_s: 124
verified: false
draft: false
---

[CF 2008D - Sakurako's Hobby](https://codeforces.com/problemset/problem/2008/D)

**Rating:** 1100  
**Tags:** dp, dsu, graphs, math  
**Solve time:** 2m 4s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a permutation of integers from 1 to n, and each number is colored black or white. From any starting integer i, we can repeatedly apply the permutation to jump from i to p_i, then to p_{p_i}, and so on. A number j is considered reachable from i if we can reach j after some finite number of these jumps. For each i, we need to compute F(i), the total number of black integers reachable from i.

The input size can be large: n can go up to 200,000, and the sum of n over all test cases does not exceed 200,000. This rules out any solution that explicitly follows the jumps for each starting number in O(n) time per number, because that could result in O(n^2) operations in the worst case, which is roughly 4 * 10^10 operations and far too slow for a 2-second time limit.

Edge cases arise when a cycle is very short or consists of a single element. For instance, if the permutation is [1] and the only element is black, the correct output is 1. A careless solution that tries to precompute reachable nodes without considering cycles may overcount or undercount black nodes. Another edge case occurs when a cycle has all white elements except the starting node; the algorithm must correctly identify which black nodes are included in the reachable set.

## Approaches

The brute-force approach is straightforward: for each index i, follow the permutation until we reach a previously visited number, marking each visited number and counting how many black nodes we encounter. This is correct because we exhaustively explore all reachable numbers. However, in the worst case, each i can traverse up to n steps if the permutation forms a single large cycle. For n=2*10^5, this results in O(n^2) operations and is too slow.

The key insight comes from recognizing that a permutation is composed entirely of disjoint cycles. Once a cycle is detected, every element in that cycle can reach exactly the same set of numbers: all nodes in the cycle and any nodes that lead into it. The black count for a node inside a cycle is the total number of black nodes in that cycle. Nodes leading into the cycle also eventually reach the same black count as the cycle itself. This means we can decompose the permutation into cycles, compute the black count for each cycle, and then assign the count to all nodes in that cycle. For chains leading into a cycle, we propagate the cycle's black count along the chain. This reduces the complexity to O(n) per test case because every node is processed exactly once.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n^2) | O(n) | Too slow |
| Cycle Decomposition | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Initialize an array `visited` of size n to track whether a node has been processed. Also initialize an array `F` to store the black counts for each node.
2. Iterate through each index i from 1 to n. If `visited[i]` is true, skip it. Otherwise, start following the permutation from i and store all visited nodes in a temporary list `path`.
3. As we traverse, keep adding nodes to `path` until we reach a node that has already been visited. If this node is part of the current path, we have detected a cycle. Identify the cycle as the segment of `path` from the first occurrence of this node to the end.
4. Count the number of black nodes in the cycle by checking the color string. For each node in the cycle, set F[node] to the cycle black count.
5. For nodes in `path` that are outside the cycle (nodes leading into the cycle), assign the same F value as the cycle, because they eventually reach the cycle and all nodes in the cycle are reachable.
6. Mark all nodes in `path` as visited.
7. After processing all nodes, output the array F.

Why it works: Each node belongs to exactly one cycle or leads into a unique cycle. By counting black nodes per cycle and propagating that count to nodes leading into the cycle, every node is correctly assigned the number of black nodes reachable from it. The invariant is that when processing a path or cycle, all nodes in it are marked visited exactly once and receive the correct F value.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        n = int(input())
        p = list(map(lambda x: int(x)-1, input().split()))
        s = input().strip()
        F = [0]*n
        visited = [False]*n
        
        for i in range(n):
            if visited[i]:
                continue
            path = []
            current = i
            while not visited[current]:
                path.append(current)
                visited[current] = True
                current = p[current]
            
            # Detect cycle
            if current in path:
                idx = path.index(current)
                cycle = path[idx:]
                cycle_black = sum(1 for x in cycle if s[x]=='0')
                for x in cycle:
                    F[x] = cycle_black
                for x in path[:idx]:
                    F[x] = cycle_black
            else:
                # Entire path leads to an already processed cycle
                cycle_black = F[current]
                for x in path:
                    F[x] = cycle_black
        print(*F)

if __name__ == "__main__":
    solve()
```

The solution handles multiple test cases using a loop. The permutation is converted to zero-based indices for easier array access. The path is traced until a visited node is found; if the visited node is in the current path, we identify a new cycle. Black node counts are calculated and assigned to both the cycle and preceding nodes. The careful distinction between nodes in the cycle and nodes leading into it avoids double-counting or missing nodes.

## Worked Examples

**Sample 1**

Input:

```
5
1
1
0
```

| i | path | cycle | cycle_black | F |
| --- | --- | --- | --- | --- |
| 0 | [0] | [0] | 1 | 1 |

All nodes are cycles of length 1, black count 1. F=[1].

**Sample 2**

Input:

```
6
3 5 6 1 2 4
010000
```

| i | path | cycle | cycle_black | F |
| --- | --- | --- | --- | --- |
| 0 | [0,2,5,3] | [0,2,5,3] | 4 | [4,?,4,4,?,4] |
| 1 | [1,4] | [1,4] | 1 | [4,1,4,4,1,4] |

This confirms that the algorithm correctly separates multiple cycles and assigns black counts.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Each node is visited exactly once, and cycle detection via path.index runs in O(path length), which is at most n per test case. |
| Space | O(n) | Arrays F, visited, and path store at most n elements. |

Given the sum of n across all test cases ≤ 2*10^5, the algorithm runs comfortably within the 2-second limit.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    out = io.StringIO()
    sys.stdout = out
    solve()
    sys.stdout = sys.__stdout__
    return out.getvalue().strip()

# Provided samples
assert run("1\n1\n1\n0\n") == "1", "single element black"
assert run("1\n5\n1 2 4 5 3\n10101\n") == "0 1 1 1 1", "mixed small permutation"
assert run("1\n6\n3 5 6 1 2 4\n010000\n") == "4 1 4 4 1 4", "complex cycles"

# Custom cases
assert run("1\n3\n1 2 3\n000\n") == "1 1 1", "all black, self cycles"
assert run("1\n4\n2 3 4 1\n0110\n") == "2 2 2 2", "single cycle length 4 with mixed colors"
assert run("1\n2\n2 1\n10\n") == "1 1", "two-element cycle with one black"
assert run("1\n5\n5 4 3 2 1\n11111\n") == "0 0 0 0 0", "all white, no black"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 element black | 1 | Base case with a single black node |
| 5-element mixed | 0 1 1 1 1 | Correct propagation of black counts |
| 6-element complex | 4 1 4 4 1 4 | Multiple cycles with leading paths |
| All black, self cycles | 1 1 1 | Black nodes correctly counted in cycles |
| Single 4-cycle mixed | 2 2 2 2 | Black counts in a longer cycle |
| 2-element cycle | 1 1 | Small even-length cycle |
| All white |  |  |
