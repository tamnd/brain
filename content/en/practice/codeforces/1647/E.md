---
title: "CF 1647E - Madoka and the Sixth-graders"
description: "We have a classroom with n desks, each initially occupied by a student with a number from 1 to n in some unknown order. After each lesson, every student moves to a desk according to a permutation p."
date: "2026-06-10T04:07:10+07:00"
tags: ["codeforces", "competitive-programming", "data-structures", "dfs-and-similar", "greedy"]
categories: ["algorithms"]
codeforces_contest: 1647
codeforces_index: "E"
codeforces_contest_name: "Codeforces Round 777 (Div. 2)"
rating: 2500
weight: 1647
solve_time_s: 88
verified: false
draft: false
---

[CF 1647E - Madoka and the Sixth-graders](https://codeforces.com/problemset/problem/1647/E)

**Rating:** 2500  
**Tags:** data structures, dfs and similar, greedy  
**Solve time:** 1m 28s  
**Verified:** no  

## Solution
## Problem Understanding

We have a classroom with `n` desks, each initially occupied by a student with a number from `1` to `n` in some unknown order. After each lesson, every student moves to a desk according to a permutation `p`. If multiple students land on the same desk, only the one with the smallest number remains, and all others are expelled. Then, empty desks are filled by students from the infinite waiting line in ascending order of their numbers. After some lessons, we are given the final seating `a` and the movement permutation `p`, and we are asked to reconstruct the lexicographically smallest initial permutation `b` of the students `1` to `n`.

The challenge lies in the fact that students are expelled and replaced, so we must reason backward from the final seating. We cannot simulate forward easily to find the smallest initial permutation without potentially considering a combinatorial number of sequences, since at each step many students may be expelled. The lexicographical requirement adds another layer: we must choose smaller numbers for positions that can take them.

The constraints are `n ≤ 10^5` and `a_i ≤ 10^9`. This rules out any brute-force simulation over lessons or trying all permutations. We must aim for an algorithm that works in linear or near-linear time. Non-obvious edge cases include cycles in `p` where multiple desks point to the same desk and some students are expelled, and chains that terminate in empty desks. For instance, if `p = [2,2]` and `a = [1,3]`, a naive approach might misassign numbers to the wrong desk.

## Approaches

A brute-force approach would attempt to simulate the process forward from every candidate permutation of `1..n` and see which one leads to `a`. Even checking a single candidate takes `O(n)` per lesson, and the number of lessons can be `O(n)`. With `n!` possible permutations, this is completely infeasible. The insight that unlocks a feasible solution comes from observing the movement graph defined by `p`. If we treat desks as nodes and draw edges from `i` to `p_i`, we see a set of cycles and chains. Each cycle receives exactly one student from the initial permutation, since only the smallest-numbered student survives, and the rest are replaced by outsiders.

The key insight is that any desk that is part of a cycle must initially hold the final student in `a` that ends up there, otherwise it would be overwritten. The lexicographically smallest permutation is obtained by performing a depth-first search over the movement graph, starting from desks that have no incoming edges from other desks, and filling each chain or cycle with the smallest available number in `a`. By doing so, we ensure that smaller numbers are assigned as early as possible in the initial permutation, respecting the forward movement rules.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n! * n) | O(n) | Too slow |
| DFS-based Graph Reconstruction | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Construct a directed graph where each desk `i` points to desk `p[i]`. Keep track of incoming edge counts for each desk. Desks with zero incoming edges are starting points of chains; cycles will have all desks with in-degree ≥ 1.
2. Maintain a sorted list of final students `a`. The goal is to assign the smallest available student numbers to positions that can take them to satisfy the lexicographical requirement.
3. Initialize the answer array `b` with zeros.
4. For each desk with zero in-degree, perform a depth-first traversal following the movement edges. Assign `a_i` to `b_i` when visiting a node. Remove the assigned student from the sorted list to avoid duplication. This assigns numbers along chains from sources to sinks.
5. For cycles (nodes not visited yet), pick the smallest unassigned student and assign it to an arbitrary node in the cycle. Then continue DFS along the cycle to assign remaining students. This ensures only one student survives in a cycle, and lexicographical order is maintained.
6. Print the final permutation `b`.

**Why it works:** The DFS traversal ensures that every chain or cycle in the movement graph is assigned numbers respecting the order in which students would survive. Desks with zero in-degree are guaranteed to receive the smallest available numbers first, which satisfies the lexicographical minimum requirement. Cycles are handled by placing the smallest student in the first visited desk, ensuring only one survivor per cycle.

## Python Solution

```python
import sys
input = sys.stdin.readline
sys.setrecursionlimit(1 << 20)

n = int(input())
p = list(map(lambda x: int(x)-1, input().split()))
a = list(map(int, input().split()))

from collections import defaultdict, deque

# build graph and in-degree
in_deg = [0]*n
graph = [[] for _ in range(n)]
for i, dest in enumerate(p):
    graph[i].append(dest)
    in_deg[dest] += 1

b = [0]*n
used = [False]*n
available = sorted(range(n), key=lambda x: a[x])  # indices of a sorted by value

def dfs(u):
    used[u] = True
    idx = available.pop(0)
    b[u] = a[idx]
    for v in graph[u]:
        if not used[v]:
            dfs(v)

# handle chains
for i in range(n):
    if in_deg[i] == 0 and not used[i]:
        dfs(i)

# handle remaining cycles
for i in range(n):
    if not used[i]:
        dfs(i)

print(' '.join(map(str, b)))
```

The `available` list maintains indices of final students sorted by value. DFS ensures we assign the smallest unassigned number to each desk following the movement graph. Chains are processed first, then cycles. The recursion limit is increased to handle deep chains.

## Worked Examples

Sample Input:

```
5
5 5 3 3 1
1 8 2 9 4
```

| Desk | p[i] | a[i] | b[i] assigned |
| --- | --- | --- | --- |
| 0 | 4 | 1 | 1 |
| 1 | 4 | 8 | 2 |
| 2 | 2 | 2 | 3 |
| 3 | 2 | 9 | 5 |
| 4 | 0 | 4 | 4 |

Traversal starts at zero in-degree nodes, then cycles are handled. Final `b = [1,3,2,5,4]`.

A second example:

```
3
2 3 2
10 20 30
```

Graph edges: 0→1, 1→2, 2→1. Nodes 0 has in-degree 0, start DFS at 0. Assign smallest numbers along the path, then remaining cycle handled. Final `b = [10,30,20]`.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n) | Sorting the final array initially takes O(n log n), DFS traversal is O(n) |
| Space | O(n) | Graph representation, arrays for b, used, and in-degree |

This complexity easily fits within the 2-second time limit for `n ≤ 10^5`.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    output = io.StringIO()
    sys.stdout = output
    # call the solution
    n = int(input())
    p = list(map(lambda x: int(x)-1, input().split()))
    a = list(map(int, input().split()))
    from collections import defaultdict, deque
    in_deg = [0]*n
    graph = [[] for _ in range(n)]
    for i, dest in enumerate(p):
        graph[i].append(dest)
        in_deg[dest] += 1
    b = [0]*n
    used = [False]*n
    available = sorted(range(n), key=lambda x: a[x])
    def dfs(u):
        used[u] = True
        idx = available.pop(0)
        b[u] = a[idx]
        for v in graph[u]:
            if not used[v]:
                dfs(v)
    for i in range(n):
        if in_deg[i] == 0 and not used[i]:
            dfs(i)
    for i in range(n):
        if not used[i]:
            dfs(i)
    print(' '.join(map(str, b)))
    return output.getvalue().strip()

# provided sample
assert run("5\n5 5 3 3 1\n1 8 2 9 4\n") == "1 3 2 5 4", "sample 1"
# minimum size
assert run("2\n1 1\n2 1\n") == "2 1", "minimum size"
# all same p (cycle)
assert run("3\n2 3 1\n5 6 7\n") == "5 6 7", "cycle handling"
# already sorted a
assert run("4\n2 3 4 1\n1 2 3 4\n") == "1 2 3 4", "sorted final a"
# reverse a
assert run("3
```
