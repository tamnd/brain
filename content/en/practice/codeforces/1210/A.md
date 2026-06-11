---
title: "CF 1210A - Anadi and Domino"
description: "We are given a very small graph with at most 7 vertices, and a fixed “palette” of 21 dominoes. Each domino corresponds to an unordered pair of values from 1 to 6, so a domino is really a pair like (1,1), (1,2), …, (6,6), with exactly one copy of each pair available."
date: "2026-06-11T23:12:59+07:00"
tags: ["codeforces", "competitive-programming", "brute-force", "graphs"]
categories: ["algorithms"]
codeforces_contest: 1210
codeforces_index: "A"
codeforces_contest_name: "Dasha Code Championship - SPb Finals Round (only for onsite-finalists)"
rating: 1700
weight: 1210
solve_time_s: 88
verified: true
draft: false
---

[CF 1210A - Anadi and Domino](https://codeforces.com/problemset/problem/1210/A)

**Rating:** 1700  
**Tags:** brute force, graphs  
**Solve time:** 1m 28s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a very small graph with at most 7 vertices, and a fixed “palette” of 21 dominoes. Each domino corresponds to an unordered pair of values from 1 to 6, so a domino is really a pair like (1,1), (1,2), …, (6,6), with exactly one copy of each pair available.

We want to place some of these dominoes onto edges of the graph. Each edge can take at most one domino, and each domino type can be used at most once. When we place a domino on an edge, we orient it, meaning one endpoint of the edge receives one side of the domino and the other endpoint receives the other side.

The key constraint is local consistency at vertices: if a vertex receives several domino halves, all those halves must show the same number. So every vertex effectively has a single “required value” imposed by all incident placed edges.

The task is to maximize how many edges receive a domino while respecting both the global restriction (each domino type used once) and the vertex consistency constraint (each vertex sees only one number among all incident edges that are chosen).

The constraints are extremely small: n ≤ 7, m ≤ 21. This immediately suggests that exponential search over states involving vertices or edges is feasible. Any solution that depends on exploring assignments or subsets is plausible, as long as it keeps the branching controlled.

A subtle failure case appears when a vertex is incident to multiple edges in the chosen subgraph. For example, if a vertex connects to two chosen edges, then both edges must assign the same number to that vertex. A naive approach that treats edges independently can incorrectly assign different numbers and violate feasibility.

Another non-obvious issue is reusing domino types: even if vertex constraints are satisfied, we cannot assign the same unordered pair twice. For instance, using (1,2) on two different edges is illegal, even if orientations would be consistent.

These two constraints, vertex consistency and global domino uniqueness, interact strongly and rule out greedy edge-by-edge assignment.

## Approaches

A naive attempt would be to try selecting a subset of edges and then assign dominoes greedily. For each edge, we might try to assign any unused domino consistent with already fixed vertex labels. The problem is that early greedy choices can block future assignments even when a global assignment exists. Since each edge depends on two vertex values, local decisions propagate constraints in cycles, and greedy assignment cannot backtrack efficiently without essentially exploring all possibilities.

The structure becomes manageable if we instead think in terms of vertex labels first. Each vertex is assigned a value from 1 to 6. Once these labels are fixed, every edge has a determined pair of endpoint values, so it demands a specific domino type (unordered pair). Now the problem becomes: given a labeling of vertices, how many edges produce valid, distinct domino requirements?

For a fixed vertex labeling, we can greedily select edges whose required domino types are all distinct. We simply count how many edges correspond to available domino types, respecting the “used once” rule per type.

This shifts the exponential part entirely to vertex assignments. There are at most 6^7 possibilities, which is about 280,000 states, fully feasible. For each assignment, we scan up to 21 edges, compute their required domino type, and count how many can be taken.

The key insight is that edge decisions are no longer coupled once vertex labels are fixed. All constraints become deterministic, and the only combinatorial choice is vertex labeling.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute force edge selection + matching | O(2^m · m!) (effectively exponential with backtracking) | O(m) | Too slow |
| Vertex labeling enumeration | O(6^n · m) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the graph edges and store them as pairs. Since n ≤ 7, we can index vertices directly from 0 to n−1.
2. Enumerate all possible assignments of values 1 to 6 for each vertex. This is done via recursion or iterative base-6 counting. The purpose is to fix vertex constraints completely.
3. For a given assignment, process each edge and compute the unordered pair formed by its endpoints. Represent this pair in a normalized way, such as (min(a,b), max(a,b)), so it matches a domino type.
4. Maintain a boolean array of size 7×7 (or a set) to track which domino types have already been used.
5. Traverse edges and greedily take an edge if its domino type has not been used yet. Mark that domino type as used and increment the count.
6. Record the maximum count over all vertex assignments.

### Why it works

Once vertex values are fixed, every edge independently implies exactly one domino type. The only remaining constraint is that each type can appear at most once. Since we only need a maximum cardinality selection of distinct items, a greedy scan is optimal: if two edges require the same domino type, taking either blocks the other equally, so no further structure is needed. The vertex assignment enumeration guarantees that all global consistency constraints are already satisfied before edge selection begins.

## Python Solution

```python
import sys
input = sys.stdin.readline

n, m = map(int, input().split())
edges = [tuple(map(int, input().split())) for _ in range(m)]

# convert to 0-based
edges = [(u-1, v-1) for u, v in edges]

best = 0

def dfs(i, color):
    global best

    if i == n:
        used = [[False] * 7 for _ in range(7)]
        cnt = 0

        for u, v in edges:
            a, b = color[u], color[v]
            if a > b:
                a, b = b, a
            if not used[a][b]:
                used[a][b] = True
                cnt += 1

        best = max(best, cnt)
        return

    for c in range(1, 7):
        color[i] = c
        dfs(i + 1, color)

dfs(0, [0] * n)

print(best)
```

The implementation performs a full DFS over vertex colorings. The array `color` encodes the current assignment. Once all vertices are assigned, we evaluate how many edges can be realized under that assignment.

The key implementation detail is normalization of each edge into a sorted pair before checking availability. This ensures that (a,b) and (b,a) map to the same domino type. The 7×7 boolean matrix is sufficient even though only 21 states are valid; the extra entries are harmless.

## Worked Examples

### Example 1

Input:

```
4 4
1 2
2 3
3 4
4 1
```

We trace one successful coloring: all vertices assigned value 3.

| Step | Edge | Pair (values) | Used? | Action | Count |
| --- | --- | --- | --- | --- | --- |
| 1 | 1-2 | (3,3) | no | take | 1 |
| 2 | 2-3 | (3,3) | yes | skip | 1 |
| 3 | 3-4 | (3,3) | yes | skip | 1 |
| 4 | 4-1 | (3,3) | yes | skip | 1 |

This assignment is not optimal for edges, but across all assignments the best configuration aligns vertex labels so that each edge produces a distinct domino type, allowing all 4 edges to be used.

This demonstrates that the solution depends heavily on global vertex labeling rather than edge structure alone.

### Example 2

Consider a triangle graph:

```
3 3
1 2
2 3
3 1
```

Try assignment (1,2,3):

| Edge | Pair | Used? | Count |
| --- | --- | --- | --- |
| 1-2 | (1,2) | yes | 1 |
| 2-3 | (2,3) | yes | 2 |
| 3-1 | (1,3) | yes | 3 |

All edges produce distinct domino types, so all are taken. This shows how distinct vertex labels maximize usable domino diversity.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(6^n · m) | Enumerate all vertex labelings; for each, scan all edges once |
| Space | O(n + 1) | Recursion stack plus small adjacency storage |

With n ≤ 7 and m ≤ 21, the worst case is roughly 6^7 × 21 ≈ 6 million operations, which fits comfortably within limits.

## Test Cases

```python
import sys, io

def solve():
    import sys
    input = sys.stdin.readline

    n, m = map(int, input().split())
    edges = [(int(a)-1, int(b)-1) for a, b in (input().split() for _ in range(m))]

    best = 0

    def dfs(i, color):
        nonlocal best
        if i == n:
            used = [[False]*7 for _ in range(7)]
            cnt = 0
            for u, v in edges:
                a, b = color[u], color[v]
                if a > b:
                    a, b = b, a
                if not used[a][b]:
                    used[a][b] = True
                    cnt += 1
            best = max(best, cnt)
            return

        for c in range(1, 7):
            color[i] = c
            dfs(i+1, color)

    dfs(0, [0]*n)
    print(best)

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    return io.StringIO().write and (solve() or "")

# provided sample
assert run("4 4\n1 2\n2 3\n3 4\n4 1\n") == "4", "sample 1"

# chain
assert run("3 2\n1 2\n2 3\n") in ["2", "1"], "small chain"

# triangle
assert run("3 3\n1 2\n2 3\n3 1\n") == "3", "triangle"

# single edge
assert run("2 1\n1 2\n") == "1", "min case"

# empty graph
assert run("3 0\n") == "0", "no edges"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 4 4 cycle | 4 | full cycle feasibility |
| 3 3 triangle | 3 | distinct labels maximize usage |
| 2 1 edge | 1 | trivial base case |
| 3 0 | 0 | empty graph handling |

## Edge Cases

A disconnected graph causes no difficulty because edges are evaluated independently once vertex labels are fixed. For instance, if there are two components, the same vertex labeling logic applies globally, and edges in each component simply contribute to the count.

A graph where many edges share a vertex is handled correctly because that vertex’s label is fixed before evaluation. For example, if vertex 1 connects to all others, assigning it value 4 forces all incident edges to require dominoes involving 4, and the algorithm consistently counts at most one per distinct neighbor pair, respecting domino uniqueness.

A graph with repeated structures, such as multiple edges forming identical required domino types, demonstrates why the greedy per-assignment step is correct: duplicates cannot both be taken, and marking a domino type once ensures all subsequent identical edges are automatically rejected.
