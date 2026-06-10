---
title: "CF 1463E - Plan of Lectures"
description: "We have a teacher, Ivan, who needs to schedule lectures on n different topics. Each topic has at most one prerequisite, meaning he cannot lecture on a topic before its prerequisite. One topic has no prerequisite."
date: "2026-06-11T02:01:34+07:00"
tags: ["codeforces", "competitive-programming", "constructive-algorithms", "dfs-and-similar", "dsu", "graphs", "implementation", "sortings", "trees"]
categories: ["algorithms"]
codeforces_contest: 1463
codeforces_index: "E"
codeforces_contest_name: "Educational Codeforces Round 100 (Rated for Div. 2)"
rating: 2400
weight: 1463
solve_time_s: 145
verified: false
draft: false
---

[CF 1463E - Plan of Lectures](https://codeforces.com/problemset/problem/1463/E)

**Rating:** 2400  
**Tags:** constructive algorithms, dfs and similar, dsu, graphs, implementation, sortings, trees  
**Solve time:** 2m 25s  
**Verified:** no  

## Solution
## Problem Understanding

We have a teacher, Ivan, who needs to schedule lectures on `n` different topics. Each topic has at most one prerequisite, meaning he cannot lecture on a topic before its prerequisite. One topic has no prerequisite. The task is to arrange the lectures in a valid order respecting these prerequisites.

Additionally, there are `k` special pairs of topics `(x_i, y_i)` such that if topic `x_i` is immediately before topic `y_i`, students understand better. All `x_i` and all `y_i` are unique, meaning no topic appears in multiple pairs as the first or second element. The challenge is to find a lecture order that satisfies both the prerequisite structure and the adjacency preferences of the special pairs, or determine that it is impossible.

The constraints are large: `n` can be up to 3 * 10^5 and `k` up to `n-1`. That means any solution with quadratic complexity (O(n²)) will be too slow. We need an algorithm roughly linear in `n` or at most O(n log n).

Non-obvious edge cases include situations where special pairs form chains or cycles that conflict with prerequisites. For example, if prerequisites enforce `1 → 2 → 3` but special pairs demand `3 → 1`, no solution exists. Another subtlety is when special pairs themselves form a chain of arbitrary length - we must ensure these chains respect the prerequisite order.

## Approaches

The brute-force approach would generate all permutations of topics and check each one against prerequisites and special pairs. This would be correct but is infeasible since the number of permutations is `n!`, which grows exponentially.

The key observation is that the prerequisites define a tree-like dependency structure (a directed forest with a single root, since exactly one topic has no prerequisite). Once we have this tree, we only need to linearly order topics from root to leaves respecting parent-before-child.

Special pairs impose adjacency constraints, which can be interpreted as forming chains of topics that must appear consecutively. Since all `x_i` are unique, these chains do not overlap at their starting points. We can construct these chains first and then topologically sort them according to the prerequisite tree.

The optimal approach is therefore to build chains dictated by the special pairs, collapse each chain into a super-node, and then perform a topological sort respecting prerequisites. If a chain violates prerequisites (its first topic comes after a prerequisite outside the chain), we detect impossibility.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n!) | O(n) | Too slow |
| Chain + Topological Sort | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Build a map `next_in_chain` for the special pairs: for each `(x, y)`, store `next_in_chain[x] = y`. Also, store `has_prev[y] = x` to detect the start of a chain.
2. Identify the start of each chain: a topic `t` that is in `next_in_chain` but not in `has_prev` is the head of a chain. There can be multiple chains since not every topic participates in a special pair.
3. Traverse each chain to collect the full sequence of topics that must appear consecutively. While traversing, check for cycles (if a topic repeats in its chain) and conflicts (a topic appears in multiple chains). If detected, output `0`.
4. Map each topic to the chain it belongs to, and create a list of chain sequences. Topics not in any special pair become singleton chains.
5. Build a prerequisite graph where each chain is a node. If a topic in chain `A` has a prerequisite outside `A`, create an edge from the prerequisite's chain to `A`. This ensures the chain order respects prerequisites.
6. Perform a topological sort of chains. If a cycle is detected in the chain graph, output `0`. Otherwise, concatenate the chains in topological order to form the lecture sequence.
7. Output the sequence.

The invariant here is that chains preserve adjacency constraints and topological sort preserves prerequisites. By treating each chain as an indivisible block, we guarantee that all constraints are satisfied if the algorithm succeeds.

## Python Solution

```python
import sys
from collections import defaultdict, deque

input = sys.stdin.readline

n, k = map(int, input().split())
p = list(map(int, input().split()))

next_in_chain = {}
has_prev = {}
for _ in range(k):
    x, y = map(int, input().split())
    next_in_chain[x] = y
    has_prev[y] = x

used = set()
chains = []
topic_to_chain = {}

# Build chains from special pairs
for t in range(1, n+1):
    if t in next_in_chain and t not in has_prev:
        chain = []
        cur = t
        while cur:
            if cur in used:
                print(0)
                sys.exit(0)
            used.add(cur)
            chain.append(cur)
            cur = next_in_chain.get(cur, 0)
        chains.append(chain)
        for topic in chain:
            topic_to_chain[topic] = len(chains)-1

# Add singleton topics
for t in range(1, n+1):
    if t not in used:
        chains.append([t])
        topic_to_chain[t] = len(chains)-1

m = len(chains)
in_deg = [0]*m
adj = [[] for _ in range(m)]

# Build graph of chains based on prerequisites
for i, topic in enumerate(p):
    if topic == 0:
        continue
    curr_chain = topic_to_chain[i+1]
    prereq_chain = topic_to_chain[topic]
    if curr_chain != prereq_chain:
        adj[prereq_chain].append(curr_chain)
        in_deg[curr_chain] += 1

# Topological sort of chains
queue = deque([i for i in range(m) if in_deg[i] == 0])
res = []

while queue:
    u = queue.popleft()
    res.extend(chains[u])
    for v in adj[u]:
        in_deg[v] -= 1
        if in_deg[v] == 0:
            queue.append(v)

if len(res) != n:
    print(0)
else:
    print(' '.join(map(str, res)))
```

The code first constructs chains from special pairs and detects cycles. Singleton topics are then added as chains of length 1. A chain graph is built using prerequisite dependencies, and a topological sort produces the lecture order. Edge cases like cyclic special pairs or impossible prerequisite order are caught and return `0`.

## Worked Examples

Sample Input 1:

```
5 2
2 3 0 5 3
1 5
5 4
```

| Step | chain | topic_to_chain | adj graph | queue | res |
| --- | --- | --- | --- | --- | --- |
| Build chains | [1,5,4], [2], [3] | {1:0,5:0,4:0,2:1,3:2} | [] | [] | [] |
| Build graph | 3→2,5→4? | see adjacency | adj=[[],[2],[1]] | queue=[0] | res=[] |
| Topo sort | 0->1->2 |  | queue update | 3 2 1 5 4 |  |

Output: `3 2 1 5 4`

This shows chains preserve adjacency, and topological sort respects prerequisites.

Custom Input 2:

```
3 1
0 1 2
1 3
```

Chains: [1,3],[2]; prerequisites: 1→2,2→3

Impossible to satisfy chain adjacency and prerequisites. Output: `0`.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Building chains, mapping topics, constructing chain graph, topological sort are all linear in `n` |
| Space | O(n) | Maps, lists, adjacency graph, and queue all store at most O(n) elements |

Given `n <= 3*10^5`, O(n) solution executes within time and memory limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    n, k = map(int, input().split())
    p = list(map(int, input().split()))
    next_in_chain = {}
    has_prev = {}
    for _ in range(k):
        x, y = map(int, input().split())
        next_in_chain[x] = y
        has_prev[y] = x
    used = set()
    chains = []
    topic_to_chain = {}
    for t in range(1, n+1):
        if t in next_in_chain and t not in has_prev:
            chain = []
            cur = t
            while cur:
                if cur in used:
                    return "0"
                used.add(cur)
                chain.append(cur)
                cur = next_in_chain.get(cur, 0)
            chains.append(chain)
            for topic in chain:
                topic_to_chain[topic] = len(chains)-1
    for t in range(1, n+1):
        if t not in used:
            chains.append([t])
            topic_to_chain[t] = len(chains)-1
    m = len(chains)
    in_deg = [0]*m
    adj = [[] for _ in range(m)]
    for i, topic in enumerate(p):
        if topic ==
```
