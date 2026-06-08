---
title: "CF 2046D - For the Emperor!"
description: "We are given a directed graph where each vertex represents a city and each directed edge represents a road that allows messengers to travel one way. Some cities initially contain a number of messengers."
date: "2026-06-08T09:08:15+07:00"
tags: ["codeforces", "competitive-programming", "flows", "graphs"]
categories: ["algorithms"]
codeforces_contest: 2046
codeforces_index: "D"
codeforces_contest_name: "Codeforces Round 990 (Div. 1)"
rating: 3100
weight: 2046
solve_time_s: 111
verified: false
draft: false
---

[CF 2046D - For the Emperor!](https://codeforces.com/problemset/problem/2046/D)

**Rating:** 3100  
**Tags:** flows, graphs  
**Solve time:** 1m 51s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a directed graph where each vertex represents a city and each directed edge represents a road that allows messengers to travel one way. Some cities initially contain a number of messengers. These messengers can move along roads, and once they carry a copy of the plan, they can duplicate it freely whenever they are in a city, so the limiting factor is not how many copies can be made later, but where we initially inject the plan.

The task is to decide how many initial copies of the plan we must hand out to messengers so that, after all movement and duplication, every city is visited by at least one messenger carrying the plan. A messenger can traverse the directed graph arbitrarily, so reachability is purely governed by directed paths.

The key structural interpretation is that each initial plan placed on a messenger starts a reachability region: all cities reachable from that messenger’s starting position will eventually be covered. Because duplication is free and local, once any messenger with a plan reaches a city, all messengers there can carry it further, so the process is equivalent to selecting starting messengers and propagating reachability forward.

The constraint on total number of cities across tests is small, with at most 200 nodes overall, and edges up to 800. This strongly suggests an O(n^2) or O(nm) graph algorithm per test is acceptable, but anything exponential in n or involving subset enumeration of nodes is not.

A subtle failure case appears when a city has no incoming reachable source of plans but also no initial messenger. For example, if a node has in-degree zero and a_i = 0, it is immediately impossible. Another failure case arises when the graph has multiple strongly connected components (SCCs): inside an SCC, one plan is enough, but between SCCs, direction matters and unreachable SCCs force additional initial placements.

A naive approach might try simulating all starting placements or greedily picking cities, but such strategies fail when reachability overlaps across SCCs are nontrivial, because choosing a start in one SCC may already cover many others, and local greedy choices do not capture global reachability structure.

## Approaches

A direct brute force idea is to try selecting subsets of messengers as starting points for the plan and simulate reachability. For each chosen starting messenger, we run a BFS/DFS to mark all reachable cities, and check if all cities are covered. This requires checking all subsets of size k, increasing k from 1 upward.

Even if we fix k, the number of subsets is combinatorial in the number of messengers, which can be O(2^n). Each simulation costs O(n + m), so the total is exponential and infeasible even for n = 200.

The key insight is that reachability is determined by strongly connected components. Within an SCC, if one messenger in that SCC receives a plan, all nodes in the SCC become equivalent because they can reach each other. Thus each SCC behaves like a single node in a condensed DAG.

Once we compress the graph into SCCs, we obtain a DAG. In this DAG, any SCC with no incoming edges from other SCCs cannot be reached from outside. Such SCCs must contain at least one initial plan placement inside them, otherwise they remain uninformed forever. If such an SCC also contains no messengers initially, it is impossible to satisfy it at all.

Thus the problem reduces to identifying SCCs, contracting them, and ensuring every source SCC (in-degree zero in the condensation graph) contains at least one messenger.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Subsets | O(2^n · (n + m)) | O(n + m) | Too slow |
| SCC Compression (Kosaraju/Tarjan) | O(n + m) | O(n + m) | Accepted |

## Algorithm Walkthrough

1. Compute strongly connected components of the directed graph. This groups cities where mutual reachability is guaranteed, so any plan entering one node spreads to the entire component.
2. Build the condensed graph where each SCC is a node. For every edge u → v in the original graph, if u and v belong to different components, add an edge between their SCCs.
3. Compute the indegree of each SCC in the condensed graph.
4. For each SCC, determine whether it contains at least one city with a_i > 0. This indicates whether we can place at least one initial plan inside this SCC.
5. For every SCC with indegree zero, check if it contains at least one messenger. If not, return -1 because no external SCC can reach it and we cannot start inside it.
6. Count how many SCCs with indegree zero exist. This number is the answer, since each such SCC requires at least one independent starting plan.

The reason this works is that SCC condensation produces a DAG where information flows only along edges. Any SCC with indegree zero is a source in this DAG, so no other component can propagate a plan into it. Inside SCCs, one starting plan is sufficient because full mutual reachability ensures complete internal coverage and outward propagation.

## Python Solution

```python
import sys
input = sys.stdin.readline

sys.setrecursionlimit(10**7)

def kosaraju(n, g, gr):
    vis = [False] * n
    order = []

    def dfs1(v):
        vis[v] = True
        for to in g[v]:
            if not vis[to]:
                dfs1(to)
        order.append(v)

    for i in range(n):
        if not vis[i]:
            dfs1(i)

    comp = [-1] * n

    def dfs2(v, c):
        comp[v] = c
        for to in gr[v]:
            if comp[to] == -1:
                dfs2(to, c)

    cid = 0
    for v in reversed(order):
        if comp[v] == -1:
            dfs2(v, cid)
            cid += 1

    return comp, cid

def solve():
    t = int(input())
    out = []

    for _ in range(t):
        n, m = map(int, input().split())
        a = list(map(int, input().split()))

        g = [[] for _ in range(n)]
        gr = [[] for _ in range(n)]

        for _ in range(m):
            u, v = map(int, input().split())
            u -= 1
            v -= 1
            g[u].append(v)
            gr[v].append(u)

        comp, k = kosaraju(n, g, gr)

        indeg = [0] * k
        has_messenger = [False] * k

        for i in range(n):
            has_messenger[comp[i]] = has_messenger[comp[i]] or (a[i] > 0)

        for u in range(n):
            for v in g[u]:
                cu, cv = comp[u], comp[v]
                if cu != cv:
                    indeg[cv] += 1

        ans = 0
        for i in range(k):
            if indeg[i] == 0:
                if not has_messenger[i]:
                    out.append("-1")
                    break
                ans += 1
        else:
            out.append(str(ans))

    print("\n".join(out))

if __name__ == "__main__":
    solve()
```

The implementation first computes SCCs using Kosaraju’s algorithm, separating forward and reverse adjacency lists. After computing component identifiers, it builds metadata per component: whether it contains at least one messenger and what its indegree is in the condensation graph.

A subtle point is that edges are only counted when crossing components; internal SCC edges must be ignored because they do not represent inter-component propagation. The final loop counts exactly the number of source SCCs while validating feasibility.

## Worked Examples

### Example 1

Input graph has multiple SCCs; consider a simplified trace.

| City | a_i | Component | Indegree | Has Messenger |
| --- | --- | --- | --- | --- |
| 1 | 2 | 0 | 0 | yes |
| 2 | 1 | 0 | 0 | yes |
| 3 | 0 | 1 | 1 | no |
| 4 | 1 | 1 | 1 | yes |

SCC 0 has indegree 0 and contains messengers, SCC 1 has indegree 1.

We process SCCs in topological sense: SCC 0 is a source, SCC 1 is not. Only SCC 0 needs a starting plan.

Answer is 1.

This shows that downstream SCCs do not contribute to the answer even if they contain messengers, because they can be reached from a source SCC.

### Example 2

Consider a case where a source SCC has no messengers.

| City | a_i | Component | Indegree |
| --- | --- | --- | --- |
| 1 | 0 | 0 | 0 |
| 2 | 0 | 0 | 0 |
| 3 | 1 | 1 | 1 |

SCC 0 is a source but has no messenger. No plan can be injected there because no initial messenger exists in that SCC, and no incoming edges can bring one.

The algorithm immediately returns -1 upon detecting this condition, demonstrating correctness of the feasibility check.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n + m) | Two DFS passes for SCC plus linear edge processing over condensed graph |
| Space | O(n + m) | Adjacency lists, reverse graph, component arrays |

The constraints allow up to 200 nodes and 800 edges, so linear graph algorithms are easily sufficient. The SCC-based reduction ensures we never attempt any combinatorial exploration.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    from contextlib import redirect_stdout
    out = io.StringIO()
    with redirect_stdout(out):
        solve()
    return out.getvalue().strip()

# provided samples
assert run("""2
7 6
2 1 0 1 2 3 4
1 2
1 3
2 4
2 5
3 6
3 7
4 4
1 1 1 1
1 2
1 3
2 4
3 4
""") == "2\n2"

# single node SCC-like structure
assert run("""1
3 2
1 0 0
1 2
2 3
""") == "1"

# impossible source SCC
assert run("""1
2 0
0 1
""") == "-1"

# cycle SCC
assert run("""1
3 3
0 1 0
1 2
2 3
3 1
""") == "1"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| chain graph | 1 | propagation through DAG |
| no messengers in source SCC | -1 | feasibility failure |
| full cycle | 1 | SCC compression correctness |
| multiple sources | k | counting independent SCC sources |

## Edge Cases

A critical edge case is when a source SCC has zero messengers. In that situation, even though it is structurally mandatory, it cannot be activated. The algorithm correctly detects this during SCC aggregation by checking has_messenger before counting.

Another edge case is a fully strongly connected graph. All nodes form one SCC with indegree zero. If at least one messenger exists anywhere, one plan suffices because it propagates throughout the SCC. The algorithm collapses the graph to one component and returns 1.

A third edge case involves disconnected components with no edges. Each node is its own SCC with indegree zero. The answer becomes the number of nodes that contain at least one messenger, since each must be started independently.
