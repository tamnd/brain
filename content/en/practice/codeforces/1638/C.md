---
title: "CF 1638C - Inversion Graph"
description: "We are given a permutation of size $n$, which is an array containing all integers from 1 to $n$ exactly once in some order. From this permutation, we construct an undirected graph on $n$ vertices, where each vertex corresponds to a position in the permutation."
date: "2026-06-10T04:29:53+07:00"
tags: ["codeforces", "competitive-programming", "data-structures", "dsu", "graphs", "math"]
categories: ["algorithms"]
codeforces_contest: 1638
codeforces_index: "C"
codeforces_contest_name: "Codeforces Round 771 (Div. 2)"
rating: 1300
weight: 1638
solve_time_s: 71
verified: true
draft: false
---

[CF 1638C - Inversion Graph](https://codeforces.com/problemset/problem/1638/C)

**Rating:** 1300  
**Tags:** data structures, dsu, graphs, math  
**Solve time:** 1m 11s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a permutation of size $n$, which is an array containing all integers from 1 to $n$ exactly once in some order. From this permutation, we construct an undirected graph on $n$ vertices, where each vertex corresponds to a position in the permutation. An edge exists between two vertices $i < j$ if and only if the value at the earlier position is greater than the value at the later position, $p_i > p_j$. Essentially, each inversion in the permutation defines an edge in the graph.

The task is to determine the number of connected components in this graph for multiple test cases. A connected component is a maximal subset of vertices such that each pair is connected directly or indirectly by edges.

The constraints allow $n$ up to $10^5$ per test case and the sum of $n$ over all test cases up to $2 \cdot 10^5$. This implies that any algorithm with worse than linear or near-linear complexity will be too slow. A naive approach that checks every possible pair of vertices would perform up to $O(n^2)$ operations per test case, which is infeasible.

Subtle edge cases include strictly increasing permutations, where no edges exist, so each vertex forms its own component, and strictly decreasing permutations, where all vertices are connected in a single component. Permutations that alternate between high and low values can create multiple intertwined components, which requires careful handling. For example, for $[2,1,4,3,5]$, the components are not immediately obvious without tracking maximums.

## Approaches

The brute-force approach is to build the full graph explicitly by iterating over every pair $(i,j)$ with $i<j$ and checking if $p_i>p_j$. Then we could run BFS or DFS from each unvisited vertex to count connected components. While correct, this would require $O(n^2)$ operations to build edges plus $O(n + e)$ to traverse the graph, which can be up to $O(n^2)$ as $e$ could also be $O(n^2)$. This fails for $n=10^5$.

The key observation is that connections in the graph are determined solely by inversions, and these have a left-to-right ordering. In other words, any vertex is connected to all vertices to its right that have smaller values, and transitive closure implies that consecutive segments with overlapping maximums form single components. We do not need to store edges explicitly. Instead, we can scan the permutation from left to right while tracking the maximum value seen so far. Whenever the current index equals the maximum value seen so far, we can end a component because all vertices in this segment are interconnected by inversions, directly or indirectly.

This observation reduces the problem to a single linear scan of the permutation, maintaining a running maximum, and counting the points where the maximum equals the current index. This is $O(n)$ per test case, which is efficient enough for the given constraints.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force (build graph + BFS/DFS) | O(n^2) | O(n^2) | Too slow |
| Linear scan with max tracking | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

1. Initialize a counter for components, `components = 0`, and a variable to track the running maximum, `current_max = 0`.
2. Iterate over the permutation using index `i` from 1 to `n` (1-based for clarity, or 0-based in code with adjustments).
3. For each position, update `current_max` to be the maximum of `current_max` and `p[i]`. This keeps track of the largest value seen in the current segment.
4. If the current index `i` equals `current_max`, we have reached the end of a connected component. Increment `components` by 1. The reasoning is that all previous indices in this segment are connected through chains of inversions, so the current vertex closes the segment.
5. After scanning the entire permutation, `components` contains the number of connected components for this test case.
6. Repeat the above steps for each test case and output the results.

Why it works: By definition, edges exist whenever a larger value precedes a smaller value. Any sequence of indices where the maximum value is exactly the rightmost index of the sequence forms a segment where every vertex is connected directly or indirectly. The running maximum ensures that we capture all indirect connections caused by overlapping inversions. Each time the running maximum matches the current index, no subsequent vertex can connect back to this segment, so it forms a distinct component.

## Python Solution

```python
import sys
input = sys.stdin.readline

t = int(input())
for _ in range(t):
    n = int(input())
    p = list(map(int, input().split()))
    components = 0
    current_max = 0
    for i, val in enumerate(p, start=1):
        current_max = max(current_max, val)
        if current_max == i:
            components += 1
    print(components)
```

The code reads the number of test cases and then iterates through each one. For each permutation, it tracks the running maximum. Whenever the current position matches the running maximum, a component ends, and the counter increments. Enumerate is used with `start=1` to align array indices with the problem’s 1-based permutation values. This prevents off-by-one errors when comparing indices with values.

## Worked Examples

**Example 1: [1,2,3]**

| i | val | current_max | current_max == i? | components |
| --- | --- | --- | --- | --- |
| 1 | 1 | 1 | yes | 1 |
| 2 | 2 | 2 | yes | 2 |
| 3 | 3 | 3 | yes | 3 |

Strictly increasing permutation produces 3 components, each vertex alone.

**Example 2: [6,1,4,2,5,3]**

| i | val | current_max | current_max == i? | components |
| --- | --- | --- | --- | --- |
| 1 | 6 | 6 | no | 0 |
| 2 | 1 | 6 | no | 0 |
| 3 | 4 | 6 | no | 0 |
| 4 | 2 | 6 | no | 0 |
| 5 | 5 | 6 | no | 0 |
| 6 | 3 | 6 | yes | 1 |

All vertices are connected, forming a single component. This confirms that the maximum-based segment correctly identifies all indirect connections.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) per test case, O(total n) overall | Each element is visited exactly once, updating max and checking a condition |
| Space | O(1) extra | Only a counter and a max variable are needed; permutation is read in place |

Given the constraint that the total sum of `n` over all test cases is $2 \cdot 10^5$, this solution runs in linear time and fits comfortably within memory limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    out = io.StringIO()
    sys.stdout = out
    t = int(input())
    for _ in range(t):
        n = int(input())
        p = list(map(int, input().split()))
        components = 0
        current_max = 0
        for i, val in enumerate(p, start=1):
            current_max = max(current_max, val)
            if current_max == i:
                components += 1
        print(components)
    return out.getvalue().strip()

# provided samples
assert run("6\n3\n1 2 3\n5\n2 1 4 3 5\n6\n6 1 4 2 5 3\n1\n1\n6\n3 2 1 6 5 4\n5\n3 1 5 2 4") == "3\n3\n1\n1\n2\n1"

# custom cases
assert run("2\n1\n1\n2\n2 1") == "1\n1", "minimum size and two-element reverse"
assert run("1\n5\n5 4 3 2 1") == "1", "strictly decreasing"
assert run("1\n5\n1 3 2 5 4") == "3", "interleaving"
assert run("1\n4\n1 4 2 3") == "2", "mixed order"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 element | 1 | single vertex forms a component |
| 2 elements reversed | 1 | two vertices form one component |
| 5 elements decreasing | 1 | full single component |
| 5 elements interleaving | 3 | multiple intertwined components |
| 4 elements mixed | 2 | partial segments handled |

## Edge Cases

For strictly increasing permutations like `[1,2,3,4]`, the algorithm correctly identifies each vertex as its own component. At each index `i`, `current_max` equals `i`, so `components` increments every step, giving 4 components.

For strictly decreasing permutations like `[5,4,
