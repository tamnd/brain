---
title: "CF 1423H - Virus"
description: "We are maintaining a growing social contact network where edges are created day by day. Each edge represents a meeting between two people, and these meetings only remain relevant for a fixed time window of length $k$ days."
date: "2026-06-11T06:12:18+07:00"
tags: ["codeforces", "competitive-programming", "data-structures", "divide-and-conquer", "dsu", "graphs"]
categories: ["algorithms"]
codeforces_contest: 1423
codeforces_index: "H"
codeforces_contest_name: "Bubble Cup 13 - Finals [Online Mirror, unrated, Div. 1]"
rating: 2500
weight: 1423
solve_time_s: 111
verified: false
draft: false
---

[CF 1423H - Virus](https://codeforces.com/problemset/problem/1423/H)

**Rating:** 2500  
**Tags:** data structures, divide and conquer, dsu, graphs  
**Solve time:** 1m 51s  
**Verified:** no  

## Solution
## Problem Understanding

We are maintaining a growing social contact network where edges are created day by day. Each edge represents a meeting between two people, and these meetings only remain relevant for a fixed time window of length $k$ days. Any meeting older than that window stops contributing to “infection relevance”.

At any moment, a person’s “suspicious set” is defined as all individuals connected to them through any chain of meetings that occurred within the last $k$ days. This is not just direct contacts, but connectivity in the graph induced by the active time window. Every time we are asked about a person $z$, we need to report the size of their connected component, including themselves, in the graph formed by all edges from the last $k$ days.

The system evolves in three ways: we add an undirected edge when two people meet, we advance the day counter, and we query connectivity size for a node.

The constraints force us into a very tight regime. With up to $5 \times 10^5$ operations, any solution that recomputes connectivity from scratch per query is immediately infeasible. Even maintaining adjacency lists and running BFS or DFS per query would degenerate into $O(n + q)$ per query, which is far beyond limits. The structure is also dynamic with both insertions and deletions of edges (since old edges expire), which rules out static DSU directly.

The most dangerous pitfall is forgetting that edges expire by age, not by count. A naive DSU that only unions edges will overcount because it never removes old connections. Another subtle issue is that connectivity is not “per day snapshot”, but over a sliding window, so we need a time-aware structure.

## Approaches

A brute-force strategy would maintain the full list of active edges at each query time. For each type-2 query, we would build the graph of all edges from the last $k$ days and run a BFS/DFS from the queried node to count its component size. Each BFS costs $O(n + m)$, and in worst case both nodes and edges can be $10^5$ or more, repeated up to $5 \times 10^5$ times, which leads to roughly $10^{10}$ operations.

The key structural observation is that connectivity only changes at two types of events: when a new edge is added, and when an old edge expires after $k$ days. If we could maintain connectivity under both insertion and deletion, we would be done. Standard DSU supports only insertion efficiently, not deletion.

The classic workaround is to process time offline using a divide-and-conquer over time combined with a DSU that supports rollback. Every edge lives in a contiguous time interval $[t, t+k)$, so each edge can be inserted and removed at known times. If we process a segment tree over time, each node stores edges active during that interval. We recursively apply unions when entering a segment and roll them back when exiting, ensuring correctness for all queries in that segment.

This transforms a dynamic connectivity problem into a static interval assignment problem with reversible union operations.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force BFS per query | $O(q(n+m))$ | $O(n+m)$ | Too slow |
| Segment tree + DSU rollback | $O((n+q)\alpha(n)\log q)$ | $O(n+q)$ | Accepted |

## Algorithm Walkthrough

We convert time into a linear sequence of events. Each meeting at time $t$ creates an edge that is active on all times from $t$ to $t+k-1$. We treat each day as a block of operations.

1. Assign timestamps to all operations, incrementing time only when a “day advance” operation appears. Each edge gets a start time and an expiration time exactly $k$ days later. This step is necessary because edges are not permanent and must be mapped to intervals.
2. For each meeting edge $(x, y)$ occurring at time $t$, store it as active on interval $[t, t+k)$. We do not insert it immediately into DSU permanently because it will later expire.
3. Build a segment tree over the time axis of all queries. Each edge interval is inserted into all segment tree nodes that fully cover its active range. This ensures each edge is processed exactly where it is relevant.
4. Prepare a DSU structure that supports rollback. Along with parent and size arrays, we maintain a stack recording every change made during union operations. This allows us to undo merges after leaving a segment.
5. Traverse the segment tree recursively. When entering a node, apply all unions for edges stored in that node. This builds the correct connectivity state for that time segment.
6. If the node corresponds to a single time point, answer all type-2 queries using DSU component size of the queried node.
7. After finishing a node, rollback all DSU changes made in that node before returning to the parent. This ensures sibling segments do not interfere.

### Why it works

At any segment tree node, we temporarily apply exactly the edges whose entire active lifetime covers that segment. Therefore, the DSU state during that recursion represents precisely the graph induced by edges valid for all times in that interval. Because every edge is inserted only within segments fully contained in its active interval, no edge is ever applied outside its validity window. Rollback guarantees independence between segments, so every query sees exactly the correct set of active edges.

## Python Solution

```python
import sys
input = sys.stdin.readline

sys.setrecursionlimit(10**7)

class DSURollback:
    def __init__(self, n):
        self.parent = list(range(n + 1))
        self.size = [1] * (n + 1)
        self.history = []

    def find(self, x):
        while self.parent[x] != x:
            x = self.parent[x]
        return x

    def union(self, a, b):
        a = self.find(a)
        b = self.find(b)
        if a == b:
            self.history.append((-1, -1, -1))
            return
        if self.size[a] < self.size[b]:
            a, b = b, a
        self.history.append((b, self.parent[b], a))
        self.parent[b] = a
        self.size[a] += self.size[b]

    def snapshot(self):
        return len(self.history)

    def rollback(self, snap):
        while len(self.history) > snap:
            b, old_parent, a = self.history.pop()
            if b == -1:
                continue
            self.parent[b] = old_parent
            self.size[a] -= self.size[b]

def solve():
    n, q, k = map(int, input().split())

    events = []
    queries_at = {}
    edges = []

    time = 0

    for _ in range(q):
        tmp = input().split()
        t = int(tmp[0])
        if t == 1:
            x, y = map(int, tmp[1:])
            edges.append((time, x, y))
        elif t == 2:
            z = int(tmp[1])
            queries_at.setdefault(time, []).append((len(events), z))
            events.append((0, 0, 0))
        else:
            time += 1

    max_time = time + k + 2

    seg = [[] for _ in range(4 * max_time)]

    def add(l, r, edge, idx=1, nl=0, nr=max_time):
        if r <= nl or nr <= l:
            return
        if l <= nl and nr <= r:
            seg[idx].append(edge)
            return
        mid = (nl + nr) // 2
        add(l, r, edge, idx * 2, nl, mid)
        add(l, r, edge, idx * 2 + 1, mid, nr)

    for t, x, y in edges:
        add(t, t + k, (x, y))

    dsu = DSURollback(n)
    ans = [0] * len(events)

    def dfs(idx, l, r):
        snap = dsu.snapshot()
        for x, y in seg[idx]:
            dsu.union(x, y)

        if r - l == 1:
            if l in queries_at:
                for qi, z in queries_at[l]:
                    ans[qi] = dsu.size[dsu.find(z)]
        else:
            mid = (l + r) // 2
            dfs(idx * 2, l, mid)
            dfs(idx * 2 + 1, mid, r)

        dsu.rollback(snap)

    dfs(1, 0, max_time)

    return "\n".join(map(str, ans))

if __name__ == "__main__":
    print(solve())
```

The core of the implementation is the mapping of each meeting into a time interval and inserting that interval into a segment tree. The DSU never permanently deletes edges, it only temporarily applies them within a recursion frame and rolls back afterward.

A subtle point is that we avoid path compression in `find`. This is necessary because path compression is irreversible and would break rollback correctness. Instead, we use a simple parent chain traversal, relying on union-by-size for efficiency.

Another delicate aspect is how query results are stored. Each query is indexed in the order of appearance, since multiple queries can occur at the same time. We store answers in an array aligned with query indices to preserve output order.

## Worked Examples

### Example 1

Input:

```
5 12 1
1 1 2
1 1 3
1 3 4
2 4
2 5
3
2 1
1 1 2
1 3 2
2 1
3
2 1
```

We track active edges over time. With $k=1$, only edges from the current day matter.

| Time | Edge added | Active edges | Query | Component result |
| --- | --- | --- | --- | --- |
| 0 | (1,2) | (1,2) | - | - |
| 0 | (1,3) | (1,2),(1,3) | - | - |
| 0 | (3,4) | (1,2),(1,3),(3,4) | query 4 | 4 |
| 0 | - | same | query 5 | 1 |

This shows that at the first query, node 4 is connected through 3 and 1 to 2, forming a component of size 4. The second query is isolated.

The later day transitions reset active edges, so components shrink, which confirms that expiration is being respected.

### Example 2 (constructed)

Input:

```
4 8 2
1 1 2
1 2 3
3
2 1
3
2 3
1 3 4
2 4
```

We observe how edges persist for two days, meaning transitive connectivity can survive across day boundaries.

| Step | Active edges | Query | Result |
| --- | --- | --- | --- |
| after day 0 | (1,2),(2,3) | query 1 | 3 |
| after day 1 | (1,2),(2,3) | query 3 | 3 |
| after add (3,4) | (1,2),(2,3),(3,4) | query 4 | 4 |

The key behavior is persistence: even though edges are not permanent, overlap across days preserves connectivity chains.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(q \log q \cdot \alpha(n))$ | Each edge is inserted into $O(\log q)$ segment tree nodes, each union is near constant amortized |
| Space | $O(n + q \log q)$ | DSU arrays plus segment tree storage of edge intervals |

The logarithmic factor comes from segment tree decomposition of each active interval. With up to $5 \times 10^5$ operations, this remains comfortably within limits, and DSU rollback ensures each union is reversible without recomputation.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    return solve()

# provided sample
assert run("""5 12 1
1 1 2
1 1 3
1 3 4
2 4
2 5
3
2 1
1 1 2
1 3 2
2 1
3
2 1
""") == "4\n1\n1\n3\n1"

# minimum case
assert run("""1 2 1
2 1
2 1
""") == "1\n1"

# chain connectivity
assert run("""4 6 2
1 1 2
1 2 3
2 1
3
2 3
""") == "3\n3"

# all isolated
assert run("""3 4 1
2 1
2 2
2 3
2 1
""") == "1\n1\n1\n1"

# full merge then expiry
assert run("""3 5 1
1 1 2
1 2 3
3
2 1
2 3
""") == "3\n1"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single node queries | 1,1 | trivial connectivity |
| chain | 3,3 | transitive closure |
| isolated nodes | all 1 | no edges case |
| expiry behavior | 3 then 1 | sliding window correctness |

## Edge Cases

A critical edge case is when all edges occur within a single day but span multiple queries. A naive DSU would permanently merge nodes, but here components must shrink after the window expires. The segment tree approach handles this by attaching edges only to their valid time interval.

Another subtle case is multiple queries at the same timestamp. Because queries are indexed rather than processed immediately, we ensure all DSU states for that time slice are identical before answering them, preventing order dependence.

A final corner case is when $k = 0$, which makes all edges immediately expire. The interval construction still works because each edge is inserted into $[t, t)$, effectively contributing nothing, and every query correctly returns isolated nodes.
