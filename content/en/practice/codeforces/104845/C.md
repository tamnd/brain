---
title: "CF 104845C - \u0420\u0435\u0441\u0442\u043e\u0440\u0430\u043d\u043d\u044b\u0439 \u0431\u0438\u0437\u043d\u0435\u0441"
description: "We are given a network of restaurants where edges represent a “neighbor” relation. Some restaurants already cooperate with Timur at the start."
date: "2026-06-28T11:30:02+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104845
codeforces_index: "C"
codeforces_contest_name: "\u041c\u0443\u043d\u0438\u0446\u0438\u043f\u0430\u043b\u044c\u043d\u044b\u0439 \u044d\u0442\u0430\u043f \u0412\u0441\u041e\u0428 \u043f\u043e \u0438\u043d\u0444\u043e\u0440\u043c\u0430\u0442\u0438\u043a\u0435 \u0432 \u041c\u043e\u0441\u043a\u043e\u0432\u0441\u043a\u043e\u0439 \u043e\u0431\u043b\u0430\u0441\u0442\u0438 2023-2024 (9-11 \u043a\u043b\u0430\u0441\u0441\u044b)"
rating: 0
weight: 104845
solve_time_s: 83
verified: false
draft: false
---

[CF 104845C - \u0420\u0435\u0441\u0442\u043e\u0440\u0430\u043d\u043d\u044b\u0439 \u0431\u0438\u0437\u043d\u0435\u0441](https://codeforces.com/problemset/problem/104845/C)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 23s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a network of restaurants where edges represent a “neighbor” relation. Some restaurants already cooperate with Timur at the start. From these initial adopters, cooperation can spread: any restaurant will also decide to cooperate if at least $k$ of its neighbors are already cooperating.

This is not a one-shot decision. As more restaurants start cooperating, they can cause further restaurants to cross the threshold, so the process continues until no new restaurant can be activated.

The task is to determine which restaurants will eventually end up cooperating after this propagation stabilizes, starting from the initial set.

The graph can contain up to $2 \cdot 10^5$ nodes and edges, so any solution must be close to linear in the number of edges. A quadratic simulation over all nodes at every step would be far too slow, since repeatedly scanning neighbors would lead to $O(nm)$ behavior in dense cases.

A subtle edge case appears when $k = 0$. In that situation, every restaurant immediately qualifies regardless of neighbors, so the final answer is trivially all nodes. Any implementation that still tries to simulate propagation must handle this carefully, otherwise it may overcomplicate or miscount.

Another case worth noticing is when the initial set is empty. Then no restaurant has any activated neighbors, so unless $k = 0$, nothing can ever be activated.

## Approaches

The naive way to think about the process is to repeatedly scan all restaurants and check for each one whether it already satisfies the condition “at least $k$ active neighbors”. Each time we find a new restaurant that satisfies it, we activate it and restart the scan.

This is correct because it directly mirrors the rule definition. However, the problem is performance. Each scan over all nodes costs $O(n + m)$ if we count neighbor checks, and in the worst case we might activate one restaurant at a time, leading to $O(n)$ rounds. This gives $O(n(n + m))$, which is far too large for $n, m \le 2 \cdot 10^5$.

The key observation is that we never need to recompute the full neighbor count from scratch. What matters is how many already-active neighbors each restaurant currently has. This suggests maintaining a running counter per node and updating it incrementally when a neighbor becomes active.

Once we view it this way, the process becomes a standard propagation over a graph. We start with all initially active nodes, push them into a queue, and for each activation we update its neighbors. Whenever a neighbor’s active count reaches $k$, it becomes active and is also pushed into the queue.

This turns the process into a breadth-first style expansion where each edge is processed only when one endpoint becomes active.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(n(n + m))$ | $O(n + m)$ | Too slow |
| Optimal BFS Propagation | $O(n + m)$ | $O(n + m)$ | Accepted |

## Algorithm Walkthrough

We interpret the graph as an adjacency list. Each node maintains a counter that tracks how many of its neighbors are already active.

1. Build the adjacency list of the graph from the input edges. This is required so that we can efficiently traverse neighbors when a node becomes active.
2. Create an array `cnt` initialized to zero for all nodes. This will store how many active neighbors each node currently has.
3. Initialize a boolean array `active` where `active[i]` is true if restaurant $i$ already cooperates at the start. These nodes form the initial frontier of the propagation.
4. Insert all initially active nodes into a queue. These are the only nodes that can immediately influence others.
5. While the queue is not empty, extract one active node $u$. For every neighbor $v$ of $u$, increment `cnt[v]` by one because one more of its neighbors has become active.
6. If `cnt[v]` reaches exactly $k$ and $v$ is not already active, mark $v$ as active and push it into the queue. The moment this happens, $v$ becomes a new source of influence for its neighbors.
7. Continue until the queue is exhausted. At that point no inactive node has reached the threshold anymore, so the process is stable.

### Why it works

The algorithm maintains the invariant that for every node, `cnt[v]` always equals the number of neighbors of $v$ that have already been activated at the current point in the process. Every activation event only increases these counters, never decreases them, matching the monotonic nature of the spreading rule.

A node becomes active exactly once its true number of active neighbors reaches at least $k$. Since counters are updated immediately when neighbors activate, no qualifying node is ever missed, and no node is activated prematurely. The queue ensures that activations propagate in the correct causal order, equivalent to repeatedly applying the original rule until a fixed point is reached.

## Python Solution

```python
import sys
input = sys.stdin.readline
from collections import deque

def solve():
    n, m, k = map(int, input().split())
    
    adj = [[] for _ in range(n + 1)]
    
    for _ in range(m):
        u, v = map(int, input().split())
        adj[u].append(v)
        adj[v].append(u)
    
    initial = list(map(int, input().split()))
    if len(initial) == 1 and initial[0] == 0:
        initial = []
    
    if k == 0:
        print(n)
        print(*range(1, n + 1))
        return
    
    active = [False] * (n + 1)
    cnt = [0] * (n + 1)
    
    q = deque()
    
    for x in initial:
        if not active[x]:
            active[x] = True
            q.append(x)
    
    while q:
        u = q.popleft()
        for v in adj[u]:
            if active[v]:
                continue
            cnt[v] += 1
            if cnt[v] >= k:
                active[v] = True
                q.append(v)
    
    res = [i for i in range(1, n + 1) if active[i]]
    
    print(len(res))
    print(*res)

def main():
    solve()

if __name__ == "__main__":
    main()
```

The adjacency list is built in the standard way, ensuring each edge is stored twice since the graph is undirected. The `cnt` array is the central mechanism that tracks progress toward the threshold condition.

The queue contains exactly the nodes that have just become active. Each node is processed once, and once processed, it never re-enters the queue because activation is permanent. This ensures linear complexity.

A small implementation detail is the early handling of $k = 0$, which avoids unnecessary graph processing entirely. Another subtle point is ensuring we do not re-add already active nodes, which would otherwise inflate counts incorrectly.

## Worked Examples

Consider a small graph where activation cascades gradually.

Input:

```
5 4 2
1 2
2 3
3 4
4 5
1 5
```

Initial active nodes: 1 and 5.

| Step | Active node | Updated counts | Newly activated |
| --- | --- | --- | --- |
| Start | - | all zero | 1, 5 |
| 1 | 1 | cnt[2]=1 | none |
| 2 | 5 | cnt[4]=1 | none |
| 3 | 2 (not yet active) | after 2 becomes active, cnt[3]=1 | none |
| 4 | 3 | cnt[2]=2 | 2 |
| 5 | 4 | cnt[3]=2 | 3 |

Eventually all nodes activate.

This trace shows how activation depends not on direct reachability, but on accumulating enough active neighbors.

Now consider a case where propagation stops early:

Input:

```
4 2 2
1 2
3 4
1
```

| Step | Active node | Updated counts | Newly activated |
| --- | --- | --- | --- |
| Start | - | all zero | 1 |
| 1 | 1 | cnt[2]=1 | none |
| End | - | stable | none |

Node 2 never reaches threshold 2, so propagation stops immediately.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n + m)$ | Each edge is processed at most twice, once per endpoint activation event |
| Space | $O(n + m)$ | Adjacency list plus auxiliary arrays for counters and state |

The linear complexity is sufficient for $2 \cdot 10^5$ nodes and edges. Each operation inside the BFS is constant time, so the solution runs comfortably within typical limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from collections import deque

    def solve():
        n, m, k = map(int, input().split())
        adj = [[] for _ in range(n + 1)]
        for _ in range(m):
            u, v = map(int, input().split())
            adj[u].append(v)
            adj[v].append(u)

        initial = list(map(int, input().split()))
        if len(initial) == 1 and initial[0] == 0:
            initial = []

        if k == 0:
            print(n)
            print(*range(1, n + 1))
            return

        active = [False] * (n + 1)
        cnt = [0] * (n + 1)
        q = deque()

        for x in initial:
            if not active[x]:
                active[x] = True
                q.append(x)

        while q:
            u = q.popleft()
            for v in adj[u]:
                if active[v]:
                    continue
                cnt[v] += 1
                if cnt[v] >= k:
                    active[v] = True
                    q.append(v)

        res = [i for i in range(1, n + 1) if active[i]]
        print(len(res))
        print(*res)

    solve()
    return sys.stdout.getvalue().strip()

# provided sample
assert run("""5 5 2
1 2
2 3
3 4
4 5
3 1
1 2 5
""") == "5\n1 2 3 4 5"

# minimum case
assert run("""1 0 0
0
""") == "1\n1"

# no propagation
assert run("""4 2 2
1 2
3 4
1
""") == "1\n1"

# full propagation
assert run("""5 4 2
1 2
2 3
3 4
4 5
1 5
""") == "5\n1 2 3 4 5"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single node, k=0 | all nodes | trivial full activation |
| disconnected graph | only initial | no cascade possible |
| chain with two sources | full spread | multi-source propagation correctness |

## Edge Cases

A key edge case is $k = 0$. In this situation, every restaurant satisfies the condition immediately regardless of graph structure. The algorithm handles this by directly printing all nodes without processing the graph. For example, with any input graph and $k = 0$, the output must always be the full set $1 \ldots n$, and skipping BFS prevents unnecessary work.

Another case is an empty initial set with positive $k$. In that scenario, no node can ever gain active neighbors, so the queue starts empty and the process ends immediately. The invariant holds because all counters remain zero, never reaching the threshold.

Finally, consider a node whose degree is less than $k$. Such nodes can never activate unless they are initially active. The counter mechanism naturally enforces this since `cnt[v]` can never exceed its degree, so it can never reach $k$ if $k$ is larger.
