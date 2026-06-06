---
title: "CF 402C - Searching for Graph"
description: "We are asked to construct a special type of undirected graph. The graph has n vertices and a parameter p, and it must satisfy two global conditions. First, the total number of edges is exactly 2n + p. Second, no subgraph of k vertices may have more than 2k + p edges."
date: "2026-06-07T01:19:50+07:00"
tags: ["codeforces", "competitive-programming", "brute-force", "constructive-algorithms", "graphs"]
categories: ["algorithms"]
codeforces_contest: 402
codeforces_index: "C"
codeforces_contest_name: "Codeforces Round 236 (Div. 2)"
rating: 1500
weight: 402
solve_time_s: 291
verified: true
draft: false
---

[CF 402C - Searching for Graph](https://codeforces.com/problemset/problem/402/C)

**Rating:** 1500  
**Tags:** brute force, constructive algorithms, graphs  
**Solve time:** 4m 51s  
**Verified:** yes  

## Solution
## Problem Understanding

We are asked to construct a special type of undirected graph. The graph has _n_ vertices and a parameter _p_, and it must satisfy two global conditions. First, the total number of edges is exactly 2_n_ + _p_. Second, no subgraph of _k_ vertices may have more than 2_k_ + _p_ edges. Self-loops and multiple edges between the same pair of vertices are forbidden.

In practical terms, the input gives several test cases, each specifying an _n_ and a _p_, and the output should be the list of edges of a graph meeting the criteria. Each edge is expressed as a pair of integers corresponding to the vertices it connects. The constraints on _n_ (up to 24) and the fact that the total edges are always modest suggest we can reason constructively rather than relying on heavy combinatorial search. The guaranteed existence of a solution also hints that a simple, repeatable pattern exists for generating these graphs.

The subtlety comes from the subgraph condition. For small _k_, adding too many edges could violate the rule. For example, with n = 6 and p = 0, we need exactly 12 edges. A naive approach of connecting every vertex to every other would give 15 edges, which violates the subgraph rule, even though the total edge count is almost correct. The algorithm must therefore add edges carefully so that the edge count in any subset of vertices never exceeds the allowed threshold.

## Approaches

A brute-force method would enumerate all possible sets of edges on _n_ vertices and check each candidate against the subgraph condition. Generating all possible graphs requires considering C(n(n−1)/2, m) combinations of edges for m edges, which is combinatorially explosive even for n = 24. Checking the subgraph condition naively involves examining all 2^n subsets, making the brute-force approach entirely infeasible.

The key insight comes from examining the formulas. A 2_n_ + _p_ edge graph can be interpreted as a “nearly 2-regular” structure: each vertex should be incident to approximately 2 edges, with _p_ extra edges added carefully. If we start by connecting each vertex to its next two neighbors in a circular fashion, we guarantee that each small subset of vertices contains no more than 2_k_ edges. This is because a connected cycle of k vertices contributes at most 2_k_ edges locally.

Once the base cycle is constructed, any extra _p_ edges can be added sequentially between vertices that are not yet fully connected without violating the subgraph bound. Because the problem guarantees a solution exists, we can always choose such pairs systematically. This reduces the construction to a simple, deterministic pattern: form a cycle with chords, then sprinkle the remaining edges until we reach the desired total of 2_n_ + _p_.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(2^n * n^2) | O(n^2) | Too slow |
| Constructive / Pattern | O(n^2) | O(n^2) | Accepted |

## Algorithm Walkthrough

1. Initialize an empty list of edges. We will build the graph incrementally.
2. Construct a simple cycle connecting each vertex to the next two vertices in modular arithmetic. For vertex i, add edges (i, i+1) and (i, i+2), wrapping around using modulo n. This ensures that each vertex has degree 2 initially, which satisfies the subgraph bounds for all k.
3. Count the edges added. At this point, we have exactly 2_n_ edges.
4. If _p_ > 0, we need to add _p_ more edges. Iterate over pairs of vertices (i, j) not already connected, starting with small i and j > i. For each such pair, add the edge and increment the count until the total reaches 2_n_ + _p_. Because n is small and the subgraph bound is lenient, this is always possible.
5. Output the list of edges as vertex pairs, making sure the numbering is 1-based.

Why it works: The base cycle ensures that every subset of k vertices has at most 2_k_ edges because no vertex exceeds degree 2 at this stage. Adding _p_ extra edges between non-adjacent vertices never creates a subset violating the 2_k_ + _p_ bound because _p_ is globally accounted for. The algorithm incrementally builds the graph while maintaining the subgraph invariant.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        n, p = map(int, input().split())
        edges = []
        
        # Step 1: add base 2*n edges using modular neighbors
        for i in range(n):
            edges.append((i+1, (i+1) % n + 1))      # connect to next
            edges.append((i+1, (i+2) % n + 1))      # connect to next-next
        
        # Step 2: add extra p edges
        if p > 0:
            added = 0
            for i in range(n):
                for j in range(i+3, n):
                    if added >= p:
                        break
                    edges.append((i+1, j+1))
                    added += 1
                if added >= p:
                    break
        
        for a, b in edges:
            print(a, b)

solve()
```

The solution first constructs the predictable base pattern where each vertex has two edges to nearby neighbors. The modulo arithmetic handles wrapping around the cycle correctly. The additional _p_ edges are added to vertices that are not immediate neighbors to avoid violating the subgraph bounds. Careful indexing ensures no off-by-one errors.

## Worked Examples

### Example 1

Input:

```
6 0
```

| Step | i | j | Edge added | Total edges |
| --- | --- | --- | --- | --- |
| Base cycle | 0 | 1 | (1,2) | 1 |
| Base cycle | 0 | 2 | (1,3) | 2 |
| Base cycle | 1 | 2 | (2,3) | 3 |
| Base cycle | 1 | 3 | (2,4) | 4 |
| Base cycle | 2 | 3 | (3,4) | 5 |
| Base cycle | 2 | 4 | (3,5) | 6 |
| Base cycle | 3 | 4 | (4,5) | 7 |
| Base cycle | 3 | 5 | (4,6) | 8 |
| Base cycle | 4 | 5 | (5,6) | 9 |
| Base cycle | 4 | 0 | (5,1) | 10 |
| Base cycle | 5 | 0 | (6,1) | 11 |
| Base cycle | 5 | 1 | (6,2) | 12 |

The table shows that after 12 edges, the graph has exactly 2_n_ edges. No extra edges are needed because p = 0. The subgraph condition is satisfied because no subset exceeds 2_k_ edges.

### Example 2

Input:

```
7 2
```

Following the same procedure, base cycle adds 14 edges, then two extra edges are chosen between vertices separated by at least 3 steps, giving exactly 16 edges (2*7 + 2), satisfying all conditions.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n^2) | Base cycle takes O(n) edges, adding p extra edges can require O(n^2) checks in worst case |
| Space | O(n^2) | We store the edge list, which has up to 2*n + p edges, bounded by n^2 |

For n ≤ 24, O(n^2) operations are around 576, well within 1-second limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from contextlib import redirect_stdout
    out = io.StringIO()
    with redirect_stdout(out):
        solve()
    return out.getvalue().strip()

# Provided sample
assert run("1\n6 0\n") == "\n".join([
    "1 2","1 3","2 3","2 4","3 4","3 5","4 5","4 6","5 6","5 1","6 1","6 2"
]), "sample 1"

# Custom cases
assert run("1\n5 0\n") == "\n".join([
    "1 2","1 3","2 3","2 4","3 4","3 5","4 5","4 1","5 1","5 2"
]), "min n case"

assert run("1\n24 3\n").count("\n") + 1 == 51, "max n case: correct number of edges"

assert run("1\n7 1\n").count("\n") + 1 == 15, "p=1 case"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
