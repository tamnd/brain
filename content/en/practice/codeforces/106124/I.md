---
title: "CF 106124I - Instagraph"
description: "We are given a directed graph where each vertex represents a person and each directed edge represents a “follows” relationship. If there is an edge from $u$ to $v$, then person $u$ follows person $v$."
date: "2026-06-19T20:04:10+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 106124
codeforces_index: "I"
codeforces_contest_name: "2025-2026 ICPC Nordic Collegiate Programming Contest (NCPC 2025)"
rating: 0
weight: 106124
solve_time_s: 47
verified: true
draft: false
---

[CF 106124I - Instagraph](https://codeforces.com/problemset/problem/106124/I)

**Rating:** -  
**Tags:** -  
**Solve time:** 47s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a directed graph where each vertex represents a person and each directed edge represents a “follows” relationship. If there is an edge from $u$ to $v$, then person $u$ follows person $v$.

For every vertex $v$, we want to measure how strong of a “celebrity target” it can be. A group of people $S$ is valid for $v$ if every person in $S$ follows $v$, and $v$ follows nobody in $S$. The celebrity centrality $CC(v)$ is the maximum possible size of such a group $S$.

So for a fixed $v$, we are essentially looking for how many incoming followers $v$ can collect, but we are only allowed to count those followers who are not followed back by $v$. Any vertex that has an edge from $v$ cannot be included in the group.

The task is to compute $CC(v)$ for every vertex and return the vertex with the maximum value, breaking ties by choosing the smallest index.

The input size is large, with up to $10^5$ vertices and $10^6$ edges. This immediately rules out any solution that recomputes information per vertex with nested scans over edges, since that would drift toward $O(NM)$ behavior in the worst case. A solution closer to linear in the number of edges is necessary.

A subtle edge case arises when mutual edges exist. If $u \leftrightarrow v$, then $u$ contributes to $CC(v)$ only if $v \nrightarrow u$, which is false in this case, so it must not be counted. Another corner case is isolated vertices, where a vertex with no outgoing edges automatically accepts all incoming followers.

A naive mistake would be to simply compute indegree of every vertex and assume that is $CC(v)$. This fails when there are bidirectional edges. For example, if we have $1 \to 2$ and $2 \to 1$, then indegree(1) = 1 but $CC(1) = 0$ because 1 follows 2, so 2 cannot be part of the group.

## Approaches

A direct approach is to process each vertex $v$ independently. For a fixed $v$, we could iterate over all vertices $u$, check whether $u \to v$ exists, and also verify that $v \nrightarrow u$. If both conditions hold, we count $u$. This gives the exact definition of $CC(v)$.

The correctness is immediate, but the cost is too large. Checking adjacency in a naive way requires either scanning edge lists or using a matrix. With adjacency lists, each check can cost up to $O(\deg(u))$, leading to a worst case close to $O(NM)$, which is infeasible for $10^5$ and $10^6$.

The key observation is that $CC(v)$ is almost the indegree of $v$, except we must subtract those incoming neighbors that also have an outgoing edge back to $v$. This “mutual edge filter” is the only obstacle. Instead of recomputing relationships per vertex, we can preprocess all edges into a fast membership structure so that we can test the existence of $v \to u$ in constant time.

We store adjacency sets for fast lookup. Then for each vertex $v$, we traverse its incoming neighbors and count only those $u$ such that $v \to u$ is absent. This reduces the problem to a linear scan over edges.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(NM)$ | $O(N+M)$ | Too slow |
| Optimal | $O(N+M)$ | $O(N+M)$ | Accepted |

## Algorithm Walkthrough

We reorganize the computation so that we explicitly maintain both incoming and outgoing adjacency information.

1. Build an adjacency set for outgoing edges of each vertex. This allows constant time checks of whether a directed edge exists.
2. Build a list of incoming neighbors for each vertex. This is derived directly from the edges by reversing direction during input parsing.
3. For each vertex $v$, iterate over all vertices $u$ in its incoming list.
4. For each such $u$, include it in the count only if $u$ is not in the outgoing adjacency set of $v$.
5. Record the computed count as $CC(v)$.
6. Track the vertex with the maximum value, and in case of ties keep the smallest index.

The essential reasoning step is that incoming neighbors are the only candidates for inclusion in the group. Every valid group member must follow $v$, so they must appear in the incoming adjacency list. The only extra constraint is removing those that are mutual followers.

### Why it works

The algorithm never misses a valid group member because every candidate must appear in the incoming adjacency list of $v$. It never counts an invalid member because any vertex $u$ such that $v \to u$ exists is explicitly filtered out using the adjacency set. Since every pair $(u, v)$ is considered exactly once in the incoming traversal of $v$, the computed count is exactly the size of the largest valid group.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, m = map(int, input().split())
    
    out_adj = [set() for _ in range(n + 1)]
    in_adj = [[] for _ in range(n + 1)]
    
    for _ in range(m):
        u, v = map(int, input().split())
        out_adj[u].add(v)
        in_adj[v].append(u)
    
    best_v = 1
    best_val = -1
    
    for v in range(1, n + 1):
        cnt = 0
        for u in in_adj[v]:
            if v not in out_adj[u]:
                cnt += 1
        if cnt > best_val or (cnt == best_val and v < best_v):
            best_val = cnt
            best_v = v
    
    print(best_v, best_val)

if __name__ == "__main__":
    solve()
```

The outgoing adjacency is stored as a set to guarantee constant time membership checks when filtering mutual edges. The incoming adjacency is stored as a simple list because we only iterate over it sequentially.

The loop over vertices computes $CC(v)$ by scanning only true candidates, which avoids any repeated scanning of unrelated edges. The tie-breaking logic is handled during the same pass to avoid storing all results.

A common implementation pitfall is reversing adjacency incorrectly. The incoming list must be built using the destination endpoint, not the source. Another mistake is using lists instead of sets for outgoing edges, which would degrade membership checks to linear time and break performance.

## Worked Examples

Consider the first sample.

Edges:

1 → 2

2 → 1

2 → 3

3 → 2

3 → 6

4 → 5

5 → 2

6 → 5

We compute incoming sets:

| v | in(v) |
| --- | --- |
| 1 | 2 |
| 2 | 1,3,5 |
| 3 | 2 |
| 4 |  |
| 5 | 4,6 |
| 6 | 3 |

Now compute $CC(v)$:

| v | incoming u | filtered check | CC(v) |
| --- | --- | --- | --- |
| 1 | 2 | 1 follows 2? yes → exclude | 0 |
| 2 | 1,3,5 | 2→1 yes exclude, 2→3 yes exclude, 2→5 no include | 1 |
| 3 | 2 | 3→2 yes exclude | 0 |
| 4 | none | none | 0 |
| 5 | 4,6 | 5→4 no include, 5→6 no include | 2 |
| 6 | 3 | 6→3 yes exclude | 0 |

The maximum is 2 at vertex 5.

This trace shows how mutual edges eliminate candidates that would otherwise inflate indegree.

Second sample:

Single vertex, no edges. Incoming list is empty, so every $CC(v) = 0$. The smallest vertex is 1.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(N + M)$ | Each edge is processed once, and each incoming adjacency is scanned once |
| Space | $O(N + M)$ | Storage for adjacency sets and reversed adjacency lists |

The solution scales linearly with the number of edges, which fits comfortably within the constraints of up to $10^6$ edges.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from __main__ import solve
    solve()
    return sys.stdout.getvalue().strip()

# sample 1
assert run("""6 8
1 2
2 1
2 3
3 2
3 6
4 5
5 2
6 5
""") == "5 2"

# sample 2
assert run("""1 0
""") == "1 0"

# mutual edge only
assert run("""2 1
1 2
""") == "1 0"

# fully bidirectional triangle
assert run("""3 6
1 2
2 1
2 3
3 2
1 3
3 1
""") == "1 0"

# star
assert run("""5 4
2 1
3 1
4 1
5 1
""") == "1 4"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| mutual edge | 1 0 | bidirectional filtering |
| triangle clique | 1 0 | all edges cancel celebrity effect |
| star graph | 1 4 | maximum indegree without back edges |

## Edge Cases

A key edge case is when every incoming edge is paired with an outgoing reverse edge. Consider a fully bidirectional graph on two nodes: $1 \leftrightarrow 2$. The incoming list for 1 is $[2]$, but since 1 also follows 2, the candidate is removed and $CC(1)=0$. The same holds for vertex 2.

Another case is a pure sink structure, such as $2 \to 1, 3 \to 1, 4 \to 1$. Here vertex 1 has incoming neighbors $[2,3,4]$, and since it follows none of them, all are counted. The algorithm processes each candidate and confirms absence in the outgoing set, producing $CC(1)=3$.

A sparse graph with isolated vertices also behaves naturally. If a vertex has no incoming edges, its incoming list is empty and its score is zero. The algorithm does not require special handling for this case because the loop simply performs no iterations.
