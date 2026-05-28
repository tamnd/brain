---
title: "CF 164A - Variable, or There and Back Again"
description: "We are given a directed graph where every node represents a program state. Each state does one of three things to a variable: 0 means the variable is ignored. 1 means the variable is assigned a new value. 2 means the variable is used."
date: "2026-05-29T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "dfs-and-similar", "graphs"]
categories: ["algorithms"]
codeforces_contest: 164
codeforces_index: "A"
codeforces_contest_name: "VK Cup 2012 Round 3"
rating: 1700
weight: 164
solve_time_s: 111
verified: true
draft: false
---

[CF 164A - Variable, or There and Back Again](https://codeforces.com/problemset/problem/164/A)

**Rating:** 1700  
**Tags:** dfs and similar, graphs  
**Solve time:** 1m 51s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a directed graph where every node represents a program state. Each state does one of three things to a variable:

`0` means the variable is ignored.

`1` means the variable is assigned a new value.

`2` means the variable is used.

A state is called interesting if it belongs to at least one directed path with this structure:

The path starts at an assignment state, ends at a usage state, and after the starting assignment there are no other assignments on the path.

That last condition is the entire difficulty of the problem. Once a second assignment appears, the old value is overwritten and stops being relevant.

We must output, for every vertex, whether it can lie on some valid path of this type.

The graph can contain up to $10^5$ vertices and $10^5$ edges. This immediately rules out any algorithm that tries to explore all paths explicitly. Even running a DFS from every assignment node independently would become too expensive in dense cases. We need something close to linear time, roughly $O(n + m)$.

The graph is also not guaranteed to be acyclic. Cycles matter because once we enter a region reachable from an assignment without touching another assignment, every node in that region may stay valid indefinitely.

Several edge cases are easy to mishandle.

Consider this graph:

```
1(assign) -> 2(assign) -> 3(use)
```

Input:

```
3 2
1 1 2
1 2
2 3
```

The correct answer is:

```
0 1 1
```

State 1 is not interesting. Any path from 1 to a use node passes through state 2, which overwrites the value first. A careless reachability solution that only checks "can reach a use node" would incorrectly mark state 1.

Another subtle case is when the assignment node itself is also the only interesting node.

```
1(assign) -> 2(ignore)
```

Input:

```
2 1
1 0
1 2
```

Correct output:

```
0 0
```

No usage state is ever reached, so the assigned value never matters.

Cycles also require care:

```
1(assign) -> 2(ignore) -> 3(ignore)
                  ^         |
                  |---------|
3 -> 4(use)
```

All four nodes are interesting because after the assignment at 1 we can loop arbitrarily many times before eventually reaching 4. Algorithms that assume DAG structure fail here.

## Approaches

The brute-force idea is straightforward. For every assignment node, perform a graph traversal that stops whenever another assignment node is encountered. Every visited node that can eventually lead to a use node belongs to a valid path.

This is correct because the traversal exactly simulates all paths where the original value survives. The problem is the cost. In the worst case there may be $10^5$ assignment nodes, and each traversal may scan the whole graph. The complexity becomes $O(n(n+m))$, which is far too large.

The key observation is that we do not actually care which assignment node started the value. We only care whether a node is reachable from some assignment without crossing another assignment, and whether from that node we can still reach a usage state before another assignment overwrites the value.

That suggests propagating information globally instead of restarting searches repeatedly.

We define a state as "alive" if the current value of the variable is still valid there. From an assignment node, the value becomes alive. Traversing through ignore or use nodes preserves it. Traversing into another assignment destroys the old value and starts a new one.

This transforms the problem into a graph reachability problem with barriers.

We can solve it in two phases.

First, we propagate forward from all assignment nodes, but we never continue past another assignment node. Every visited node is reachable while preserving the current value.

Second, among those reachable nodes, we determine which can reach a usage node without crossing another assignment. This can be done by reversing the graph and propagating backward from all usage nodes, again stopping at assignment boundaries.

A node is interesting if both conditions hold simultaneously.

The whole process visits every edge only a constant number of times, giving linear complexity.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(n(n+m))$ | $O(n+m)$ | Too slow |
| Optimal | $O(n+m)$ | $O(n+m)$ | Accepted |

## Algorithm Walkthrough

1. Build the directed graph and its reverse graph.

The reverse graph is needed for backward propagation from usage nodes.
2. Start a multi-source BFS or DFS from every assignment node.

These nodes represent places where a value becomes alive.
3. During this traversal, move through outgoing edges normally, but do not continue from a different assignment node.

If we started from assignment node `s`, then reaching another assignment node means the original value is overwritten there.
4. Mark every visited node as `from_assign`.

This means the node can be reached while carrying some valid variable value.
5. Start another multi-source traversal, this time from every usage node, but on the reversed graph.

Traversing backward answers the question: "can this node eventually lead to a use state?"
6. Again, stop propagation when crossing assignment nodes.

Once we pass through another assignment, the current value changes, so earlier states no longer contribute to the final usage.
7. Mark every visited node as `to_use`.

This means there exists a path from the node to a usage state without overwriting the value first.
8. For every node, output `1` if both `from_assign[node]` and `to_use[node]` are true. Otherwise output `0`.

### Why it works

A node is interesting exactly when it lies on a path that starts with an assignment and ends with a usage without intermediate assignments.

The forward traversal identifies all nodes reachable from some assignment before the value is overwritten.

The backward traversal identifies all nodes that can still reach a usage before another assignment appears.

If both conditions hold for a node, then we can concatenate the two corresponding path segments into one valid complete path. Conversely, if a node belongs to a valid path, then it must satisfy both properties by definition.

## Python Solution

```python
import sys
from collections import deque

input = sys.stdin.readline

def solve():
    n, m = map(int, input().split())
    f = list(map(int, input().split()))

    g = [[] for _ in range(n)]
    rg = [[] for _ in range(n)]

    for _ in range(m):
        a, b = map(int, input().split())
        a -= 1
        b -= 1
        g[a].append(b)
        rg[b].append(a)

    from_assign = [False] * n
    q = deque()

    for i in range(n):
        if f[i] == 1:
            from_assign[i] = True
            q.append(i)

    while q:
        u = q.popleft()

        for v in g[u]:
            if from_assign[v]:
                continue

            from_assign[v] = True

            if f[v] != 1:
                q.append(v)

    to_use = [False] * n
    q = deque()

    for i in range(n):
        if f[i] == 2:
            to_use[i] = True
            q.append(i)

    while q:
        u = q.popleft()

        for v in rg[u]:
            if to_use[v]:
                continue

            to_use[v] = True

            if f[v] != 1:
                q.append(v)

    ans = []

    for i in range(n):
        ans.append('1' if from_assign[i] and to_use[i] else '0')

    print('\n'.join(ans))

solve()
```

The graph and reverse graph are both necessary because the two traversals answer opposite reachability questions.

The first BFS begins from all assignment nodes simultaneously. The subtle detail is that assignment nodes are still marked reachable, but propagation stops there unless the node is itself an initial source. This models overwriting correctly.

The second BFS mirrors the same logic on the reversed graph. Starting from usage nodes and walking backward determines which states can eventually contribute to a usage.

The condition:

```
if f[v] != 1:
    q.append(v)
```

is the critical line in both traversals. We still mark assignment nodes as reachable, because the assignment state itself may be interesting, but we never continue beyond them using the old value.

The final answer is the intersection of the two reachability sets.

## Worked Examples

### Sample 1

Input:

```
4 3
1 0 0 2
1 2
2 3
3 4
```

Forward traversal:

| Step | Queue | Visited after step |
| --- | --- | --- |
| Start | [1] | {1} |
| Visit 1 | [2] | {1,2} |
| Visit 2 | [3] | {1,2,3} |
| Visit 3 | [4] | {1,2,3,4} |
| Visit 4 | [] | {1,2,3,4} |

Backward traversal:

| Step | Queue | Visited after step |
| --- | --- | --- |
| Start | [4] | {4} |
| Visit 4 | [3] | {3,4} |
| Visit 3 | [2] | {2,3,4} |
| Visit 2 | [1] | {1,2,3,4} |
| Visit 1 | [] | {1,2,3,4} |

Every node belongs to both sets, so all outputs are `1`.

This example shows the simplest valid chain. No overwriting occurs, so the value survives through the entire path.

### Sample 2

Input:

```
3 2
1 0 2
1 3
2 3
```

Forward traversal:

| Step | Queue | Visited after step |
| --- | --- | --- |
| Start | [1] | {1} |
| Visit 1 | [3] | {1,3} |
| Visit 3 | [] | {1,3} |

Backward traversal:

| Step | Queue | Visited after step |
| --- | --- | --- |
| Start | [3] | {3} |
| Visit 3 | [1,2] | {1,2,3} |
| Visit 1 | [2] | {1,2,3} |
| Visit 2 | [] | {1,2,3} |

Intersection:

| Node | from_assign | to_use | Answer |
| --- | --- | --- | --- |
| 1 | Yes | Yes | 1 |
| 2 | No | Yes | 0 |
| 3 | Yes | Yes | 1 |

State 2 can reach a usage node, but no assignment can reach it first. That is why it is excluded.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n+m)$ | Each traversal visits every node and edge at most once |
| Space | $O(n+m)$ | Graph storage plus visitation arrays |

With $10^5$ vertices and edges, linear complexity easily fits inside the limits. The memory usage is also safe because adjacency lists store each edge only once per direction.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io
from collections import deque

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    input = sys.stdin.readline

    out = io.StringIO()
    sys.stdout = out

    n, m = map(int, input().split())
    f = list(map(int, input().split()))

    g = [[] for _ in range(n)]
    rg = [[] for _ in range(n)]

    for _ in range(m):
        a, b = map(int, input().split())
        a -= 1
        b -= 1
        g[a].append(b)
        rg[b].append(a)

    from_assign = [False] * n
    q = deque()

    for i in range(n):
        if f[i] == 1:
            from_assign[i] = True
            q.append(i)

    while q:
        u = q.popleft()

        for v in g[u]:
            if from_assign[v]:
                continue

            from_assign[v] = True

            if f[v] != 1:
                q.append(v)

    to_use = [False] * n
    q = deque()

    for i in range(n):
        if f[i] == 2:
            to_use[i] = True
            q.append(i)

    while q:
        u = q.popleft()

        for v in rg[u]:
            if to_use[v]:
                continue

            to_use[v] = True

            if f[v] != 1:
                q.append(v)

    ans = []

    for i in range(n):
        ans.append('1' if from_assign[i] and to_use[i] else '0')

    print('\n'.join(ans))

    sys.stdout = sys.__stdout__
    return out.getvalue()

# provided sample
assert run(
"""4 3
1 0 0 2
1 2
2 3
3 4
"""
) == "1\n1\n1\n1\n", "sample 1"

# overwrite blocks old value
assert run(
"""3 2
1 1 2
1 2
2 3
"""
) == "0\n1\n1\n", "overwrite case"

# no usage reachable
assert run(
"""2 1
1 0
1 2
"""
) == "0\n0\n", "no use state"

# cycle without overwrite
assert run(
"""4 4
1 0 0 2
1 2
2 3
3 2
3 4
"""
) == "1\n1\n1\n1\n", "cycle case"

# minimum size graph
assert run(
"""1 0
0
"""
) == "0\n", "minimum case"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Assignment followed by another assignment | `0 1 1` | Old value must stop at overwrite |
| Assignment with no use reachable | `0 0` | Reachability alone is insufficient |
| Cycle before usage | `1 1 1 1` | Algorithm handles cycles correctly |
| Single isolated node | `0` | Minimum boundary case |

## Edge Cases

Consider again the overwrite scenario:

```
3 2
1 1 2
1 2
2 3
```

The forward traversal starts from both assignment nodes.

From node 1, traversal reaches node 2 but stops there because node 2 is another assignment. The old value cannot continue further.

From node 2, traversal reaches node 3.

The backward traversal from node 3 reaches node 2, but cannot continue past node 2 to node 1 because node 2 overwrites the value.

The intersection becomes `{2,3}` only, producing:

```
0
1
1
```

Now consider the cycle example:

```
4 4
1 0 0 2
1 2
2 3
3 2
3 4
```

The forward traversal from node 1 enters the cycle between 2 and 3 and marks both nodes reachable. Since neither node is an assignment, propagation continues normally.

The backward traversal from node 4 reaches node 3 and then node 2 through the reversed cycle edges.

All nodes satisfy both conditions, so every node is marked interesting.

Finally, consider a graph with assignments but no use:

```
3 2
1 0 0
1 2
2 3
```

The forward traversal marks all nodes reachable from an assignment. The backward traversal starts from no nodes because there are no usage states.

The `to_use` array remains entirely false, so every answer becomes `0`.

This correctly captures the fact that a value only matters if it is eventually used.
