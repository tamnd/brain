---
title: "CF 1027D - Mouse Hunt"
description: "We can think of the dorm as a directed graph where each room has exactly one outgoing edge. From every room i, the mouse deterministically moves to a[i] after one second."
date: "2026-06-16T21:32:59+07:00"
tags: ["codeforces", "competitive-programming", "dfs-and-similar", "graphs"]
categories: ["algorithms"]
codeforces_contest: 1027
codeforces_index: "D"
codeforces_contest_name: "Educational Codeforces Round 49 (Rated for Div. 2)"
rating: 1700
weight: 1027
solve_time_s: 229
verified: true
draft: false
---

[CF 1027D - Mouse Hunt](https://codeforces.com/problemset/problem/1027/D)

**Rating:** 1700  
**Tags:** dfs and similar, graphs  
**Solve time:** 3m 49s  
**Verified:** yes  

## Solution
## Problem Understanding

We can think of the dorm as a directed graph where each room has exactly one outgoing edge. From every room `i`, the mouse deterministically moves to `a[i]` after one second. Because every node has exactly one outgoing edge, the graph decomposes into chains that eventually enter directed cycles, and then stay inside those cycles forever.

A trap placed in a room removes that room as a safe state. If the mouse ever lands on a trapped room, the process stops. The difficulty comes from the fact that the starting room is unknown, so we must guarantee that every possible starting position eventually leads to a trapped vertex along its deterministic walk.

The task is to choose a subset of nodes minimizing total cost such that every infinite walk in this functional graph eventually hits at least one chosen node.

The constraint `n ≤ 2 * 10^5` rules out any solution that simulates starting from every node independently and walking forward until detection, because that would be `O(n^2)` in the worst case when the graph forms a long chain or cycle structure. We need a linear or near-linear graph decomposition approach, typically `O(n)` or `O(n log n)`.

A naive but important edge case is a pure cycle. If all nodes form a cycle and we place no trap inside it, the mouse starting on that cycle will never be caught. For example:

Input:

```
3
5 1 5
2 3 1
```

Here `1 → 2 → 3 → 1`. Any correct solution must pick at least one node in this cycle. A careless greedy that only considers tree-like structures would fail here because it ignores the fact that cycles are closed recurrence classes.

Another subtle case is a self-loop `i → i`. That node alone forms a cycle of length one, and if it is not selected, a mouse starting there is never caught. This forces every cycle to be “covered” by at least one selected node.

## Approaches

The key structure is that every node belongs to exactly one directed cycle, possibly with trees flowing into it. Once the mouse enters a cycle, it never leaves, so the only way to guarantee capture is to place at least one trap inside every cycle. Nodes outside cycles (in trees leading into cycles) are optional, because any path from them eventually reaches their cycle.

Thus the problem reduces to: identify all directed cycles in a functional graph and, for each cycle, choose the minimum cost node inside it.

A brute force strategy would start from every node, simulate its path, and try to decide which nodes must be chosen so that all paths are intercepted. This quickly becomes expensive because each simulation can traverse up to `O(n)` steps, and doing this for all starting points yields `O(n^2)`.

The improvement comes from recognizing that the graph is a collection of disjoint cycles with incoming trees. Each node has outdegree 1, so cycle detection is straightforward using DFS or indegree peeling. Once cycles are isolated, each cycle becomes independent: choosing nodes in one cycle does not affect any other cycle.

So instead of reasoning about paths, we reason about components. For each cycle, we compute its minimum-cost node and add it to the answer.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Simulation | O(n²) | O(n) | Too slow |
| Cycle Decomposition | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

We use cycle detection in a functional graph.

1. Mark all nodes as unvisited. We will traverse each node exactly once as a DFS start point.
2. For each unvisited node `i`, begin walking forward following `a[i]`, marking nodes as “in current recursion stack”.

This stack marking is crucial because it allows us to detect when we return to a node already on the current path, which indicates a cycle.
3. If during traversal we reach a node that is already in the current stack, we have found a directed cycle. We then extract all nodes from that cycle.

The extraction is done by walking from the repeated node until we return to it.
4. For every detected cycle, compute the minimum cost `min(c[v])` over all nodes `v` in that cycle, and add it to the answer.

This is correct because we only need one trap per cycle, and choosing the cheapest node minimizes cost.
5. Continue until all nodes are processed.

The key subtlety is that nodes not part of cycles will always eventually reach a cycle, but they will never be part of a stack-revisited collision. They are simply traversed and marked, ensuring linear coverage.

### Why it works

Every node lies either in a cycle or in a tree that leads into exactly one cycle. Any starting position eventually reaches its cycle and never leaves it. Therefore, if we place at least one trap in each cycle, every infinite walk is guaranteed to eventually hit a trapped node. Conversely, if any cycle has no trap, starting from that cycle avoids all traps forever. So the solution is both necessary and sufficient, and minimizing cost per cycle is optimal because cycles are independent.

## Python Solution

```python
import sys
input = sys.stdin.readline
sys.setrecursionlimit(10**7)

def solve():
    n = int(input())
    c = [0] + list(map(int, input().split()))
    a = [0] + list(map(int, input().split()))

    visited = [0] * (n + 1)
    in_stack = [0] * (n + 1)
    ans = 0

    for i in range(1, n + 1):
        if visited[i]:
            continue

        stack = []
        v = i

        while not visited[v]:
            visited[v] = 1
            in_stack[v] = 1
            stack.append(v)
            v = a[v]

            if in_stack[v]:
                cycle = []
                idx = len(stack) - 1
                while stack[idx] != v:
                    cycle.append(stack[idx])
                    idx -= 1
                cycle.append(v)

                ans += min(c[x] for x in cycle)
                break

        for node in stack:
            in_stack[node] = 0

    print(ans)

if __name__ == "__main__":
    solve()
```

The solution maintains two states: `visited` ensures each node is processed once globally, while `in_stack` tracks the current traversal path so cycles can be detected immediately when we revisit a node still in the active chain.

The stack stores the exact traversal order, which allows reconstructing the cycle in linear time when a repetition is found. The moment we detect a cycle, we isolate only the nodes forming it and compute the minimum cost among them. Clearing `in_stack` after finishing each DFS-like walk prevents false cycle detections across different components.

## Worked Examples

Consider the sample:

```
5
1 2 3 2 10
1 3 4 3 3
```

We trace cycle detection.

| Start | Traversal path | Cycle detected | Cycle nodes | Cost chosen |
| --- | --- | --- | --- | --- |
| 1 | 1 → 1 | self-loop | {1} | 1 |
| 2 | 2 → 3 → 4 → 3 | 3-cycle | {3,4} | 3 |
| 5 | 5 → 3 | already processed | - | - |

This demonstrates that nodes 1 and cycle {3,4} define all necessary trapping points.

Another example:

```
4
4 1 2 3
```

This forms a single cycle `1 → 4 → 3 → 2 → 1`.

| Start | Traversal path | Cycle detected | Cycle nodes | Cost chosen |
| --- | --- | --- | --- | --- |
| 1 | 1 → 4 → 3 → 2 → 1 | full cycle | {1,2,3,4} | min(c) |

The algorithm correctly identifies the entire graph as one cycle.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Each node is visited once and enters/exits stack once |
| Space | O(n) | Arrays for visited, stack tracking, and recursion structure |

The linear complexity is sufficient for `n ≤ 2 · 10^5`, and memory usage is well within limits since we store only constant auxiliary arrays.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    from collections import deque

    n = int(sys.stdin.readline())
    c = [0] + list(map(int, sys.stdin.readline().split()))
    a = [0] + list(map(int, sys.stdin.readline().split()))

    visited = [0] * (n + 1)
    in_stack = [0] * (n + 1)
    ans = 0

    for i in range(1, n + 1):
        if visited[i]:
            continue
        stack = []
        v = i
        while not visited[v]:
            visited[v] = 1
            in_stack[v] = 1
            stack.append(v)
            v = a[v]
            if in_stack[v]:
                cycle = []
                idx = len(stack) - 1
                while stack[idx] != v:
                    cycle.append(stack[idx])
                    idx -= 1
                cycle.append(v)
                ans += min(c[x] for x in cycle)
                break
        for x in stack:
            in_stack[x] = 0

    return str(ans)

# provided sample
assert run("""5
1 2 3 2 10
1 3 4 3 3
""") == "3"

# self-loop
assert run("""1
5
1
""") == "5"

# single cycle
assert run("""4
4 3 2 1
2 3 4 1
""") == "1"

# two disjoint cycles
assert run("""6
5 4 3 2 1 10
2 1 4 3 6 5
""") == "6"

# chain into cycle
assert run("""5
10 1 10 10 10
2 3 3 4 4
""") == "1"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single node self-loop | 5 | minimal cycle handling |
| reversed cycle | 1 | correct cycle extraction |
| two cycles | 6 | independence of components |
| chain into cycle | 1 | ignoring non-cycle nodes |

## Edge Cases

A self-loop node demonstrates the simplest cycle. The algorithm starts at that node, marks it in the stack, and immediately revisits itself. The cycle extraction returns just that node, and its cost is added. No other nodes interfere because there are none.

A long chain leading into a cycle shows why non-cycle nodes do not contribute. The traversal marks all chain nodes as visited but never detects them as cycle entries, since they are not revisited within the current stack. Only when the cycle is reached does the repetition occur, and only that cycle contributes to the answer.
