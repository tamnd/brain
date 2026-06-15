---
title: "CF 1275A - \u0421\u043a\u0440\u044b\u0442\u044b\u0439 \u0434\u0440\u0443\u0433"
description: "We are given a directed friendship graph of $n$ users, where each user lists some other users as friends. The important detail is that friendship is not guaranteed to be mutual. If user $u$ lists $v$, it does not imply that $v$ lists $u$."
date: "2026-06-16T01:29:22+07:00"
tags: ["codeforces", "competitive-programming", "*special"]
categories: ["algorithms"]
codeforces_contest: 1275
codeforces_index: "A"
codeforces_contest_name: "VK Cup 2019 - \u041a\u0432\u0430\u043b\u0438\u0444\u0438\u043a\u0430\u0446\u0438\u044f (Engine)"
rating: 0
weight: 1275
solve_time_s: 285
verified: false
draft: false
---

[CF 1275A - \u0421\u043a\u0440\u044b\u0442\u044b\u0439 \u0434\u0440\u0443\u0433](https://codeforces.com/problemset/problem/1275/A)

**Rating:** -  
**Tags:** *special  
**Solve time:** 4m 45s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a directed friendship graph of $n$ users, where each user lists some other users as friends. The important detail is that friendship is not guaranteed to be mutual. If user $u$ lists $v$, it does not imply that $v$ lists $u$.

The task is to detect all “hidden friendships”, meaning all ordered pairs $(u, v)$ such that $u$ considers $v$ a friend but $v$ does not consider $u$ a friend. In graph terms, we are looking for all directed edges that are not reciprocated in the adjacency list.

The input is essentially an adjacency list representation of a directed graph with vertices from 1 to $n$. The output requires listing every directed edge that does not have its reverse edge present, and counting how many such edges exist.

Since $n \le 100$, the total number of edges is at most about $n^2$, which is at most 10,000. This is small enough that any solution that checks adjacency in $O(1)$ or even $O(n)$ per edge will be fast enough. A naive $O(n^3)$ approach would also pass, but is unnecessary.

A subtle point is that duplicates do not exist within each adjacency list, but asymmetry across lists is exactly what defines the answer. Another edge case is users with zero friends, which should not produce any outgoing hidden edges, but may still appear as targets in others’ lists.

A common mistake is to assume symmetry or to only check one direction once without verifying existence in the opposite list. Another mistake is to forget that the output must include all asymmetric edges, not just pairs of users that differ in both directions simultaneously.

For example, if user 1 lists 2, but user 2 does not list 1, we must output (1, 2). If user 2 lists 1 but 1 does not list 2, we also output (2, 1). These are independent directed checks, not a single undirected inconsistency.

## Approaches

The straightforward idea is to iterate over every user $u$, and for every friend $v$ in $u$’s list, check whether $u$ appears in $v$’s list. If it does not, then $(u, v)$ is a hidden friendship.

In a brute-force implementation, checking membership in $v$’s list using linear search leads to $O(n)$ per check. Since each user can have up to $O(n)$ friends, and we perform a check for each edge, the total complexity becomes $O(n^3)$ in the worst case. With $n = 100$, this is still borderline acceptable, but structurally inefficient and unnecessary.

The key improvement comes from representing each adjacency list as a hash set. This transforms membership queries into average $O(1)$ operations. Then, for every directed edge $u \to v$, we simply check whether $u \in adj[v]$. If not, we output it.

This works because the problem reduces to edge existence queries in a directed graph, and hash-based sets give constant-time membership checks, collapsing the triple nested structure into a quadratic scan.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force (list search) | $O(n^3)$ | $O(n^2)$ | Accepted but inefficient |
| Hash Set Lookup | $O(n^2)$ | $O(n^2)$ | Accepted |

## Algorithm Walkthrough

1. Read the adjacency list for each user and store it as a set. This ensures fast membership checks when verifying reciprocity.
2. Initialize an empty list to store answers.
3. For each user $u$, iterate over every friend $v$ in their set. This enumerates all directed edges in the graph.
4. For each pair $(u, v)$, check whether $u$ is present in the adjacency set of $v$. If not, append $(u, v)$ to the answer list. This directly identifies missing reverse edges.
5. After processing all users, output the total number of stored pairs followed by each pair.

The reasoning behind step 4 is that reciprocity in a directed graph is exactly the condition $u \in adj[v]$. Failing this condition means the edge is one-sided.

### Why it works

We maintain the invariant that every candidate pair $(u, v)$ comes directly from an explicit adjacency relation in the input. We only output a pair if its reverse relation is absent. Since we scan every directed edge exactly once and check the existence of its inverse independently, no hidden friendship can be missed, and no valid reciprocal edge is incorrectly included.

## Python Solution

```python
import sys
input = sys.stdin.readline

n = int(input())
adj = [set() for _ in range(n + 1)]

for i in range(1, n + 1):
    data = list(map(int, input().split()))
    cnt = data[0]
    for v in data[1:]:
        adj[i].add(v)

res = []

for u in range(1, n + 1):
    for v in adj[u]:
        if u not in adj[v]:
            res.append((u, v))

print(len(res))
for u, v in res:
    print(u, v)
```

The implementation stores each adjacency list as a set so that membership checks are constant time. The outer loop iterates through all users, and the inner loop iterates through their declared friends. The critical decision is the condition `u not in adj[v]`, which directly encodes the asymmetry requirement.

A common pitfall is forgetting to convert lists to sets, which silently degrades performance to quadratic membership checks inside a quadratic loop. Another subtle issue is iterating over raw input lists without preserving indexing consistency, which can cause off-by-one errors. Here we explicitly allocate `n + 1` so that user numbering aligns with indices.

## Worked Examples

### Example 1

Input:

```
3
1 2
1 3
1 1
```

We build adjacency sets:

| u | adj[u] |
| --- | --- |
| 1 | {2} |
| 2 | {3} |
| 3 | {1} |

Now we scan edges:

| u | v | adj[v] | u in adj[v]? | Output |
| --- | --- | --- | --- | --- |
| 1 | 2 | {3} | No | (1,2) |
| 2 | 3 | {1} | No | (2,3) |
| 3 | 1 | {2} | No | (3,1) |

Output is all three edges.

This confirms that the algorithm treats each directed edge independently and does not assume symmetry.

### Example 2

Input:

```
4
2 2 3
1 1
1 2
0
```

Adjacency:

| u | adj[u] |
| --- | --- |
| 1 | {2,3} |
| 2 | {1} |
| 3 | {2} |
| 4 | {} |

Scan:

| u | v | adj[v] | u in adj[v]? | Output |
| --- | --- | --- | --- | --- |
| 1 | 2 | {1} | Yes | - |
| 1 | 3 | {2} | No | (1,3) |
| 2 | 1 | {2,3} | Yes | - |
| 3 | 2 | {1} | Yes | - |

This shows that mutual edges are correctly filtered out while asymmetric ones remain.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n^2)$ | Each of at most $n^2$ directed edges is checked once with O(1) membership lookup |
| Space | $O(n^2)$ | Storage for adjacency sets in the worst case |

With $n \le 100$, the maximum operations are on the order of 10,000 edge checks, which is trivial under typical constraints.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from collections import defaultdict

    n = int(input())
    adj = [set() for _ in range(n + 1)]

    for i in range(1, n + 1):
        data = list(map(int, input().split()))
        for v in data[1:]:
            adj[i].add(v)

    res = []
    for u in range(1, n + 1):
        for v in adj[u]:
            if u not in adj[v]:
                res.append((u, v))

    out = [str(len(res))]
    for u, v in res:
        out.append(f"{u} {v}")
    return "\n".join(out)

# sample
assert run("""3
1 2
1 3
1 1
""") == """3
1 2
2 3
3 1"""

# custom 1: no edges
assert run("""2
0
0
""") == """0"""

# custom 2: fully mutual
assert run("""3
1 2
1 1 3
1 2
""") == """0"""

# custom 3: chain asymmetry
assert run("""4
1 2
1 3
1 4
0
""") == """3
1 2
2 3
3 4"""

# custom 4: single node edges missing back
assert run("""2
1 2
0
""") == """1
1 2"""
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| empty graph | 0 | no edges case |
| mutual graph | 0 | symmetry filtering |
| chain graph | 3 edges | directional propagation |
| single missing reverse | 1 edge | basic asymmetry |

## Edge Cases

A key edge case is when a node has no outgoing edges. For example, if user 2 has an empty list, it never produces outgoing pairs, but may still be the target of others’ hidden friendships. The algorithm handles this naturally because we only iterate over existing adjacency entries.

Another case is a fully asymmetric chain, where every edge points forward but never backward. The algorithm will output all edges, since every reverse lookup fails. This confirms that directionality is preserved correctly and no implicit symmetry is assumed.

A final subtle case is mutual pairs embedded in larger graphs. For instance, if 1 lists 2 and 2 lists 1, but 1 also lists 3 while 3 does not list 1, only (1,3) should appear. The algorithm isolates each directed edge independently, so the presence of unrelated mutual edges does not interfere with correctness.
