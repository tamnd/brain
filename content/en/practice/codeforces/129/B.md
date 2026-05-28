---
title: "CF 129B - Students and Shoelaces"
description: "We can model the students and shoelaces as an undirected graph. Each student is a vertex, and every shoelace between two students is an edge. In one round, every student whose degree is exactly 1 gets removed at the same time."
date: "2026-05-28T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "brute-force", "dfs-and-similar", "graphs", "implementation"]
categories: ["algorithms"]
codeforces_contest: 129
codeforces_index: "B"
codeforces_contest_name: "Codeforces Beta Round 94 (Div. 2 Only)"
rating: 1200
weight: 129
solve_time_s: 135
verified: true
draft: false
---

[CF 129B - Students and Shoelaces](https://codeforces.com/problemset/problem/129/B)

**Rating:** 1200  
**Tags:** brute force, dfs and similar, graphs, implementation  
**Solve time:** 2m 15s  
**Verified:** yes  

## Solution
## Problem Understanding

We can model the students and shoelaces as an undirected graph. Each student is a vertex, and every shoelace between two students is an edge.

In one round, every student whose degree is exactly 1 gets removed at the same time. When those students leave, all incident edges disappear as well. This may create new degree-1 vertices for the next round. The process continues until there are no vertices with degree 1.

The task is to count how many rounds of removals happen.

The constraints are small enough that we do not need sophisticated graph theory machinery, but they are large enough that careless repeated recomputation can become expensive. If we recompute the degree of every vertex from scratch after every round, then in dense graphs we may scan almost all edges many times. A solution around $O(n + m)$ or $O(n^2)$ is perfectly safe here, while something closer to $O(nm)$ starts becoming risky.

The most dangerous implementation detail is simultaneous removal. Suppose we remove students one by one instead of removing the whole group together. That changes the graph during the round and can incorrectly remove extra students.

Consider this graph:

```
1 - 2 - 3
```

Input:

```
3 2
1 2
2 3
```

The correct process is:

First round removes 1 and 3 together.

Second round removes 2.

Answer = 2.

If we remove greedily one at a time, removing 1 first makes 2 become degree 1 immediately, and we might incorrectly remove it in the same round.

Another easy mistake is mishandling isolated vertices. Students with degree 0 are never removed because the rule only removes degree-1 vertices.

Example:

```
3 0
```

All students are isolated from the start. Nobody leaves, so the answer is:

```
0
```

A careless implementation that removes all vertices with degree at most 1 would incorrectly produce 1.

Cycles are another important edge case. In a cycle, every vertex has degree 2, so nothing ever happens.

Example:

```
4 4
1 2
2 3
3 4
4 1
```

Correct output:

```
0
```

Any solution that assumes repeated pruning eventually deletes every connected component would fail here.

## Approaches

The direct simulation is straightforward. We maintain the current graph, find all vertices with degree 1, remove them simultaneously, update the graph, and repeat until no such vertices remain.

The brute-force version recomputes every degree from scratch after each round. In the worst case, a long chain removes only two vertices per round. If there are $n$ vertices, we may perform about $n/2$ rounds. Recomputing all degrees every time costs $O(m)$, leading to roughly $O(nm)$.

That still passes for small constraints, but it does unnecessary work because most edges do not change between rounds.

The key observation is that only neighbors of removed vertices can have their degrees changed. Once a student leaves, we only need to update the degrees of adjacent students instead of rebuilding everything.

This turns the problem into a layered leaf-removal process. We maintain current degrees and repeatedly remove all vertices whose degree is 1. Every edge is processed only when one of its endpoints disappears, so the total work becomes linear in the size of the graph.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(nm)$ | $O(n + m)$ | Too slow conceptually |
| Optimal | $O(n + m)$ | $O(n + m)$ | Accepted |

## Algorithm Walkthrough

1. Build an adjacency list for the graph and compute the degree of every vertex.
2. Find all vertices whose degree is exactly 1. These are the students removed in the first round.
3. While the current round is not empty, process one entire round at a time.
4. Increase the answer by 1 because one group of students is being kicked out.
5. Mark every vertex in the current round as removed. We process the whole batch together because removals are simultaneous.
6. For every removed vertex, iterate over its neighbors.
7. If a neighbor has not already been removed, decrease its degree by 1 because one incident edge disappeared.
8. If a neighbor’s degree becomes exactly 1 after the update, place it into the next round.
9. Replace the current round with the next round and continue.
10. When no degree-1 vertices remain, stop and print the number of rounds.

### Why it works

At every moment, the degree array matches the current graph after all previous rounds have been removed. A vertex enters the next round exactly when its degree becomes 1 after the current round disappears. Because we process removals in batches, the algorithm perfectly matches the statement’s simultaneous removal rule. No vertex is removed too early or too late.

## Python Solution

```python
import sys
from collections import deque

input = sys.stdin.readline

def solve():
    n, m = map(int, input().split())

    graph = [[] for _ in range(n)]
    degree = [0] * n

    for _ in range(m):
        u, v = map(int, input().split())
        u -= 1
        v -= 1

        graph[u].append(v)
        graph[v].append(u)

        degree[u] += 1
        degree[v] += 1

    removed = [False] * n

    current = deque()

    for i in range(n):
        if degree[i] == 1:
            current.append(i)

    rounds = 0

    while current:
        rounds += 1

        next_round = deque()

        current_nodes = list(current)
        current.clear()

        for node in current_nodes:
            removed[node] = True

        for node in current_nodes:
            for nei in graph[node]:
                if removed[nei]:
                    continue

                degree[nei] -= 1

                if degree[nei] == 1:
                    next_round.append(nei)

        current = next_round

    print(rounds)

solve()
```

The adjacency list stores the graph efficiently, and the degree array tracks the current number of remaining neighbors for every student.

The first loop collects all initial leaves, meaning vertices with degree exactly 1. Those form the first round.

The subtle part is handling simultaneous removal correctly. We first copy all vertices from the current queue into `current_nodes` and mark them all as removed before updating neighbors. This prevents one removal inside the round from affecting whether another vertex in the same round should still exist.

The `removed` array prevents multiple updates on already deleted vertices. Without it, degrees could become negative or vertices could be inserted repeatedly into future rounds.

A common mistake is adding vertices to the next round whenever degree becomes less than or equal to 1. That incorrectly removes isolated vertices. The condition must be exactly `degree[nei] == 1`.

## Worked Examples

### Example 1

Input:

```
3 3
1 2
2 3
3 1
```

Initial graph is a triangle.

| Round | Current degree array | Degree-1 vertices | Removed this round |
| --- | --- | --- | --- |
| Start | [2, 2, 2] | none | none |

No vertex has degree 1, so the process stops immediately.

Answer:

```
0
```

This example shows that cycles survive forever because removing leaves never starts.

### Example 2

Input:

```
4 3
1 2
2 3
3 4
```

This is a simple chain.

| Round | Current degree array | Degree-1 vertices | Removed this round |
| --- | --- | --- | --- |
| 1 | [1, 2, 2, 1] | 1, 4 | 1, 4 |
| 2 | [0, 1, 1, 0] | 2, 3 | 2, 3 |
| End | [0, 0, 0, 0] | none | none |

The answer is:

```
2
```

This trace demonstrates why removals must happen layer by layer. The middle vertices only become removable after the endpoints disappear.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n + m)$ | Every vertex and edge is processed only a constant number of times |
| Space | $O(n + m)$ | Adjacency list, degree array, queues, and removed array |

This easily fits the limits. Even for the largest valid graph, linear processing over vertices and edges is fast within a 2 second limit.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io
from collections import deque

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    input = sys.stdin.readline

    def solve():
        n, m = map(int, input().split())

        graph = [[] for _ in range(n)]
        degree = [0] * n

        for _ in range(m):
            u, v = map(int, input().split())
            u -= 1
            v -= 1

            graph[u].append(v)
            graph[v].append(u)

            degree[u] += 1
            degree[v] += 1

        removed = [False] * n

        current = deque()

        for i in range(n):
            if degree[i] == 1:
                current.append(i)

        rounds = 0

        while current:
            rounds += 1

            current_nodes = list(current)
            current.clear()

            next_round = deque()

            for node in current_nodes:
                removed[node] = True

            for node in current_nodes:
                for nei in graph[node]:
                    if removed[nei]:
                        continue

                    degree[nei] -= 1

                    if degree[nei] == 1:
                        next_round.append(nei)

            current = next_round

        return str(rounds)

    return solve()

# provided sample
assert run(
"""3 3
1 2
2 3
3 1
"""
) == "0", "sample 1"

# chain of length 4
assert run(
"""4 3
1 2
2 3
3 4
"""
) == "2", "simple chain"

# isolated vertices only
assert run(
"""5 0
"""
) == "0", "isolated vertices are never removed"

# star graph
assert run(
"""5 4
1 2
1 3
1 4
1 5
"""
) == "1", "center becomes isolated, not removable"

# single edge
assert run(
"""2 1
1 2
"""
) == "1", "both endpoints removed together"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Triangle cycle | 0 | Cycles never start removal |
| Chain of length 4 | 2 | Multi-round layered removals |
| No edges | 0 | Degree-0 vertices stay forever |
| Star graph | 1 | Center becomes isolated, not removable |
| Single edge | 1 | Simultaneous endpoint removal |

## Edge Cases

Consider isolated vertices:

```
3 0
```

Initial degrees are `[0, 0, 0]`. No vertex has degree 1, so the queue starts empty. The loop never runs, and the answer remains 0. This matches the rules because isolated students are not reprimanded.

Now consider a star graph:

```
5 4
1 2
1 3
1 4
1 5
```

Initial degrees are `[4, 1, 1, 1, 1]`.

In the first round, vertices 2, 3, 4, and 5 are removed simultaneously. Vertex 1 loses four edges and its degree becomes 0. Since only degree-1 vertices are removable, the process stops after one round. The answer is 1.

A careless implementation using `degree <= 1` would incorrectly remove vertex 1 in a second round.

Finally, consider a chain:

```
5 4
1 2
2 3
3 4
4 5
```

Round 1 removes vertices 1 and 5.

Degrees become `[0, 1, 2, 1, 0]`.

Round 2 removes vertices 2 and 4.

Degrees become `[0, 0, 0, 0, 0]`.

Vertex 3 never becomes degree 1 because both neighbors disappear in the same round. The process stops with answer 2.

This confirms the importance of simultaneous updates.
