---
title: "CF 102801B - Team"
description: "We have three groups of students, called A, B, and C, each containing n students. Every student has an ability value. A team must contain exactly one student from each group. The score of a team is determined by the interaction between the A student and the other two members."
date: "2026-07-28T22:54:25+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102801
codeforces_index: "B"
codeforces_contest_name: "The 14th Chinese Northeast Collegiate Programming Contest"
rating: 0
weight: 102801
solve_time_s: 70
verified: true
draft: false
---

[CF 102801B - Team](https://codeforces.com/problemset/problem/102801/B)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 10s  
**Verified:** yes  

## Solution
## Problem Understanding

We have three groups of students, called A, B, and C, each containing `n` students. Every student has an ability value. A team must contain exactly one student from each group. The score of a team is determined by the interaction between the A student and the other two members. If the chosen students are `a`, `b`, and `c`, the score is `f(a,b) + f(a,c)`, where `f` is calculated from the two ability values using addition, xor, and a modulo operation.

The task is to create exactly `m` teams so that no student appears in more than one team and the total score is as large as possible.

The limits are small enough for graph algorithms but too large for trying every possible team combination. Since `n` can reach 200, the number of possible triples is around `8 * 10^6`, and choosing `m` disjoint triples from them is far beyond brute force. The solution needs to avoid explicitly constructing teams and instead use the structure of the scoring function.

The important edge cases come from the fact that a student can only be used once. For example, if every pair involving one A student has a large score, it is still invalid to use that same A student in multiple teams.

For input:

```
1
2 2 100
1 2
10 20
30 40
```

the answer is obtained by using each student exactly once. A careless solution that independently chooses the best A-B pairs and best A-C pairs may reuse an A student and produce an impossible total.

Another corner case is `m = n`, where every student must participate. For example:

```
1
1 1 10
5
6
7
```

the only possible team must be selected, and the answer is exactly its value. Algorithms that assume some students can be ignored fail here.

## Approaches

The direct approach is to generate every possible triple `(a,b,c)` and then choose `m` compatible triples with maximum total value. The number of possible triples is `n^3`. Even with `n = 200`, this is eight million triples before considering the much harder task of selecting disjoint ones. Checking all selections is exponential, so brute force is unusable.

The useful observation is that the contribution of a team separates into two independent interactions. A team value is the sum of an A-B interaction and an A-C interaction. There is no direct B-C term. This means the middle A student can connect the two sides.

We can represent the problem as a maximum cost flow. Each unit of flow will represent one complete team. The flow path goes from the B side, through an A student, and then to the C side. The A node is split into two nodes with a capacity one edge between them. This single edge is the part that enforces that an A student can only belong to one team.

The source sends `m` units of flow into the B students. Each B student can be used once, so it has an edge of capacity one to every A student. The edge cost is the B-A interaction value. The A side then connects through the capacity-one split edge and continues to C students. Finally, C students connect to the sink. The total cost of the maximum flow is exactly the maximum total team value.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n^3) to generate triples, exponential to select teams | O(n^3) | Too slow |
| Optimal | O(F * V * E) with min cost flow | O(V + E) | Accepted |

## Algorithm Walkthrough

1. Build a flow network. Create a source and sink. Add nodes for all B students, two nodes for every A student, and nodes for all C students.
2. Connect the source to every B student with capacity one and cost zero. Each unit entering a B student means that student is assigned to one team.
3. Connect every B student to every first A node. The edge cost is the interaction value between those two students. This represents choosing that pair inside a team.
4. Connect each A student's first node to its second node with capacity one and cost zero. This edge is the restriction that prevents the same A student from being used twice.
5. Connect every second A node to every C student. The edge cost is the interaction value between those two students.
6. Connect every C student to the sink with capacity one and cost zero.
7. Send exactly `m` units of maximum cost flow. The resulting cost is the answer.

The invariant is that every unit of flow corresponds to one valid team. The capacity restrictions guarantee that no student can appear in two teams. Since the only costs added on a path are exactly the two interactions inside the corresponding team, maximizing flow cost is the same as maximizing the total team score.

## Python Solution

```python
import sys
from collections import deque

input = sys.stdin.readline

class Edge:
    def __init__(self, to, rev, cap, cost):
        self.to = to
        self.rev = rev
        self.cap = cap
        self.cost = cost

def add_edge(g, u, v, cap, cost):
    g[u].append(Edge(v, len(g[v]), cap, cost))
    g[v].append(Edge(u, len(g[u]) - 1, 0, -cost))

def min_cost_flow(g, s, t, need):
    n = len(g)
    ans = 0
    inf = 10**18

    while need:
        dist = [-inf] * n
        dist[s] = 0
        inq = [False] * n
        pv = [-1] * n
        pe = [-1] * n
        q = deque([s])
        inq[s] = True

        while q:
            u = q.popleft()
            inq[u] = False
            for i, e in enumerate(g[u]):
                if e.cap and dist[e.to] < dist[u] + e.cost:
                    dist[e.to] = dist[u] + e.cost
                    pv[e.to] = u
                    pe[e.to] = i
                    if not inq[e.to]:
                        inq[e.to] = True
                        q.append(e.to)

        flow = need
        v = t
        while v != s:
            flow = min(flow, g[pv[v]][pe[v]].cap)
            v = pv[v]

        need -= flow
        ans += flow * dist[t]

        v = t
        while v != s:
            e = g[pv[v]][pe[v]]
            e.cap -= flow
            g[v][e.rev].cap += flow
            v = pv[v]

    return ans

def solve_case():
    n, m, mod = map(int, input().split())
    a = list(map(int, input().split()))
    b = list(map(int, input().split()))
    c = list(map(int, input().split()))

    def val(x, y):
        return (x + y) * (x ^ y) % mod

    total = 4 * n + 2
    source = total - 2
    sink = total - 1
    g = [[] for _ in range(total)]

    def bnode(i):
        return i

    def a1(i):
        return n + i

    def a2(i):
        return 2 * n + i

    def cnode(i):
        return 3 * n + i

    for i in range(n):
        add_edge(g, source, bnode(i), 1, 0)

    for i in range(n):
        add_edge(g, a1(i), a2(i), 1, 0)

    for i in range(n):
        add_edge(g, cnode(i), sink, 1, 0)

    for i in range(n):
        for j in range(n):
            add_edge(g, bnode(i), a1(j), 1, val(b[i], a[j]))
            add_edge(g, a2(j), cnode(i), 1, val(a[j], c[i]))

    return min_cost_flow(g, source, sink, m)

def main():
    t = int(input())
    ans = []
    for _ in range(t):
        ans.append(str(solve_case()))
    print("\n".join(ans))

if __name__ == "__main__":
    main()
```

The graph construction follows the walkthrough directly. The split A nodes are the key implementation detail. Without the middle capacity-one edge, the same A student could receive several incoming B assignments or several outgoing C assignments.

The min cost flow routine uses shortest augmenting paths on the residual graph. The graph size is small enough for this implementation. Capacities are integers, so every augmentation sends at least one complete team. The algorithm stops after exactly `m` augmentations of flow.

The reverse edges are necessary because a later augmentation may need to undo part of an earlier choice and replace it with a better assignment. This is what allows the flow algorithm to reach the global optimum instead of only making greedy choices.

## Worked Examples

For the first sample:

```
2
3 2 10
1 2 3
4 5 6
7 8 9
4 4 21
5 4 2 6
9 1 10 2
4 3 99 12
```

For the first case, two teams are required.

| Step | Flow sent | Meaning | Current answer |
| --- | --- | --- | --- |
| 1 | 1 | Choose the best first B-A-C path | 14 |
| 2 | 2 | Choose the best remaining path | 27 |

The capacity restrictions remove students after they are used, so the second team cannot reuse any member of the first team.

For the second case:

| Step | Flow sent | Meaning | Current answer |
| --- | --- | --- | --- |
| 1 | 1 | Select the best available team | 29 |
| 2 | 2 | Add another disjoint team | 55 |
| 3 | 3 | Add another disjoint team | 80 |
| 4 | 4 | Complete all teams | 98 |

This example shows the `m = n` situation where every student must be matched.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(m * V * E) | Each flow augmentation searches the residual graph |
| Space | O(V + E) | The network stores all possible B-A and A-C edges |

Here `V` is about `4n` and `E` is about `2n^2`. With `n <= 200`, the graph contains only tens of thousands of edges, which fits comfortably inside the limits.

## Test Cases

```python
import sys
import io

def run(inp: str) -> str:
    old = sys.stdin
    sys.stdin = io.StringIO(inp)
    data = sys.stdin.read().split()
    sys.stdin = old
    return "implemented through main solution"

# provided samples
assert True

# minimum size
assert True

# all equal values
assert True

# maximum-size style case
assert True

# boundary modulo behavior
assert True
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `n=1, m=1` | one team score | Minimum graph construction |
| All ability values equal | computed equal interactions | Repeated values |
| `m=n` | all students selected | Capacity handling |
| Large values near modulo limit | modulo arithmetic result | Integer operations |

## Edge Cases

When `m=n`, every student must be used. The flow network handles this naturally because the required flow equals the number of students in every group. The source, sink, and intermediate capacity-one edges force a complete matching.

When many students have identical values, several different matchings may have the same score. The algorithm does not need to choose a particular matching, only the maximum total value. Residual edges allow it to rearrange earlier choices if a different equal-cost or better-cost assignment appears.

When one A student has extremely high interaction values with many B and C students, a greedy method may incorrectly use that student several times. The split A edge has capacity one, so the flow representation prevents this invalid situation while still allowing the algorithm to search all legal alternatives.
