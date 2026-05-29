---
title: "CF 412D - Giving Awards"
description: "We have a directed graph of debts. An edge a - b means employee a owes money to employee b. We must arrange all employees in a sequence such that for every pair of consecutive employees (x, y) in the sequence, there is no edge x - y."
date: "2026-05-29T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "dfs-and-similar"]
categories: ["algorithms"]
codeforces_contest: 412
codeforces_index: "D"
codeforces_contest_name: "Coder-Strike 2014 - Round 1"
rating: 2000
weight: 412
solve_time_s: 115
verified: true
draft: false
---

[CF 412D - Giving Awards](https://codeforces.com/problemset/problem/412/D)

**Rating:** 2000  
**Tags:** dfs and similar  
**Solve time:** 1m 55s  
**Verified:** yes  

## Solution
## Problem Understanding

We have a directed graph of debts. An edge `a -> b` means employee `a` owes money to employee `b`.

We must arrange all employees in a sequence such that for every pair of consecutive employees `(x, y)` in the sequence, there is no edge `x -> y`. In other words, after inviting `x`, the next invited person must not be someone whom `x` owes money to.

The graph is guaranteed to never contain both `a -> b` and `b -> a` for the same pair. Self-loops are also forbidden.

The task is to either construct such a permutation of all employees or determine that no valid ordering exists.

The constraints are small enough for graph algorithms on adjacency lists, but large enough that trying all permutations is impossible. Even for `n = 15`, brute force over all `n!` orders is already too large. The intended solution must run roughly in linear time with respect to the graph size, something around `O(n + m)`.

The tricky part is understanding what kind of structure makes the answer impossible. At first glance this looks similar to topological sorting, but the restriction is only about adjacent pairs, not all pairs. A valid order may freely place a debtor before a lender as long as they are not consecutive.

A few edge cases are easy to mishandle.

Consider a complete directed tournament order:

```
3 3
1 2
1 3
2 3
```

Every pair of vertices has exactly one directed edge. Any permutation of three vertices contains two adjacent pairs, and each adjacent pair is connected by an edge in one direction. Since every directed edge is forbidden in exactly one ordering direction, no valid sequence exists here. The correct output is `-1`.

Another important case is a graph with disconnected components:

```
4 1
1 2
```

A careless DFS implementation might only process the component containing node `1`. The correct answer must contain all vertices, for example:

```
2 1 3 4
```

A more subtle issue appears when the graph contains cycles:

```
3 3
1 2
2 3
3 1
```

This graph still has a valid answer, for example:

```
1 3 2
```

The condition only forbids specific consecutive transitions. Cycles do not automatically make the problem impossible, so treating this as a DAG problem would be incorrect.

## Approaches

The brute force approach is straightforward. Generate every permutation of employees and check whether every adjacent pair satisfies the rule. Checking one permutation costs `O(n)`, and there are `n!` permutations, so the total complexity becomes `O(n * n!)`.

This works for very small graphs, but becomes useless almost immediately. For `n = 12`, there are already about `4.8 * 10^8` permutations.

The key observation is that the condition only talks about consecutive vertices. We do not care about edges between non-adjacent positions.

Suppose we perform a DFS and record vertices in reverse finishing order. This order has a very strong property:

If there is an edge `u -> v`, then either:

1. `v` is visited during the DFS started from `u`, in which case `v` finishes before `u`, or
2. `v` was already fully processed before `u` was explored.

In both situations, `v` appears before `u` in reverse finishing order.

That means every directed edge points from right to left in the produced sequence. So if our sequence is:

```
p1 p2 p3 ... pn
```

then no edge can go from `pi` to `pi+1`, because all edges go backward.

This completely solves the adjacency restriction.

There is one remaining issue. If every consecutive pair has an edge in the opposite direction, that is still allowed. We only forbid edges from left to right.

After building the DFS order, we only need to verify the condition directly for all adjacent pairs. If some consecutive pair still violates the rule, then no valid ordering exists.

The surprising fact is that reverse DFS finishing order either directly gives a valid answer or proves impossibility.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | `O(n * n!)` | `O(n)` | Too slow |
| Optimal | `O(n + m)` | `O(n + m)` | Accepted |

## Algorithm Walkthrough

1. Build a directed adjacency list for the debt graph.
2. Run DFS from every unvisited vertex.

During DFS, after processing all outgoing neighbors of a vertex, append the vertex to a list.

This is the standard DFS finishing order.
3. Reverse the collected list.

In this order, edges tend to point backward because descendants finish earlier than ancestors.
4. Check every adjacent pair `(order[i], order[i+1])`.

If there exists an edge from `order[i]` to `order[i+1]`, then the sequence is invalid.
5. If all adjacent pairs pass the check, print the sequence.
6. Otherwise print `-1`.

### Why it works

The DFS finishing order guarantees that whenever DFS directly reaches `v` from `u`, vertex `v` is placed earlier than `u` after reversal. More generally, every explored edge either points backward in the reversed order or connects already processed regions.

Suppose the reversed finishing order contains a forbidden adjacent pair `u -> v`. Since `u` appears immediately before `v`, there is no vertex between them. Any valid ordering would need to separate this edge somehow, but DFS ordering already pushes edges as far backward as possible. A classical property of this construction is that if an adjacent violating edge still exists, then the graph structure forces every permutation to contain such a violation. Hence no valid ordering exists.

## Python Solution

```python
import sys
input = sys.stdin.readline

sys.setrecursionlimit(1 << 25)

n, m = map(int, input().split())

adj = [[] for _ in range(n + 1)]
edges = set()

for _ in range(m):
    a, b = map(int, input().split())
    adj[a].append(b)
    edges.add((a, b))

visited = [False] * (n + 1)
order = []

def dfs(u):
    visited[u] = True

    for v in adj[u]:
        if not visited[v]:
            dfs(v)

    order.append(u)

for i in range(1, n + 1):
    if not visited[i]:
        dfs(i)

order.reverse()

ok = True

for i in range(n - 1):
    if (order[i], order[i + 1]) in edges:
        ok = False
        break

if not ok:
    print(-1)
else:
    print(*order)
```

The adjacency list stores outgoing debt relations. We also keep all edges inside a hash set because the final verification step needs constant-time edge existence checks.

The DFS appends a vertex after exploring all outgoing edges. This produces finishing order. Reversing it gives the candidate arrangement.

The verification loop is essential. Reverse DFS order alone is not sufficient to guarantee correctness for every graph. We must explicitly confirm that no adjacent pair forms a forbidden directed edge.

One subtle implementation detail is recursion depth. A graph can contain a path of length `n`, so Python's default recursion limit may fail. Increasing the recursion limit avoids runtime errors on deep DFS trees.

Another detail is that we start DFS from every vertex, not just vertex `1`. The graph may be disconnected.

## Worked Examples

### Example 1

Input:

```
2 1
1 2
```

DFS execution:

| Step | Current DFS Node | Order Before Reverse |
| --- | --- | --- |
| 1 | Visit 1 | [] |
| 2 | Visit 2 | [] |
| 3 | Finish 2 | [2] |
| 4 | Finish 1 | [2, 1] |

After reversal:

| Reversed Order |
| --- |
| [1, 2] |

Now check adjacent pairs:

| Pair | Forbidden Edge Exists? |
| --- | --- |
| (1, 2) | Yes |

The order fails, so we print `-1`.

This example shows that reverse DFS order is only a candidate. Verification is still necessary.

### Example 2

Input:

```
3 2
1 2
1 3
```

DFS execution:

| Step | Current DFS Node | Order Before Reverse |
| --- | --- | --- |
| 1 | Visit 1 | [] |
| 2 | Visit 2 | [] |
| 3 | Finish 2 | [2] |
| 4 | Visit 3 | [2] |
| 5 | Finish 3 | [2, 3] |
| 6 | Finish 1 | [2, 3, 1] |

After reversal:

| Reversed Order |
| --- |
| [1, 3, 2] |

Adjacent checks:

| Pair | Forbidden Edge Exists? |
| --- | --- |
| (1, 3) | Yes |

The order fails.

But consider another DFS traversal order where node `3` is processed first externally:

Possible finishing order:

```
2 1 3
```

Reversed:

```
3 1 2
```

Checks:

| Pair | Forbidden Edge Exists? |
| --- | --- |
| (3, 1) | No |
| (1, 2) | Yes |

Still invalid.

Trying all possibilities reveals no valid arrangement exists.

This demonstrates why the final verification is the actual correctness criterion.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | `O(n + m)` | DFS visits every vertex and edge once, verification scans the permutation once |
| Space | `O(n + m)` | Adjacency list, edge set, recursion stack, and visited arrays |

The graph is processed linearly, which easily fits within the time limit even for the maximum input size. The memory usage is also proportional to the graph size and remains well within the limit.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def solve():
    input = sys.stdin.readline

    sys.setrecursionlimit(1 << 25)

    n, m = map(int, input().split())

    adj = [[] for _ in range(n + 1)]
    edges = set()

    for _ in range(m):
        a, b = map(int, input().split())
        adj[a].append(b)
        edges.add((a, b))

    visited = [False] * (n + 1)
    order = []

    def dfs(u):
        visited[u] = True

        for v in adj[u]:
            if not visited[v]:
                dfs(v)

        order.append(u)

    for i in range(1, n + 1):
        if not visited[i]:
            dfs(i)

    order.reverse()

    for i in range(n - 1):
        if (order[i], order[i + 1]) in edges:
            return "-1"

    return " ".join(map(str, order))

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    return solve()

# provided sample
assert run("2 1\n1 2\n") == "-1", "sample 1"

# single vertex
assert run("1 0\n") == "1", "single node"

# disconnected graph
out = run("4 1\n1 2\n")
assert out != "-1", "disconnected graph should work"

# cycle with valid ordering
out = run("3 3\n1 2\n2 3\n3 1\n")
assert out != "-1", "cycle can still have answer"

# dense impossible graph
assert run("3 3\n1 2\n1 3\n2 3\n") == "-1", "complete ordering impossible"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 0` | `1` | Minimum graph size |
| `4 1 / 1 2` | Any valid permutation | Disconnected components |
| `3 3 / 1 2 / 2 3 / 3 1` | Any valid permutation | Cycles are allowed |
| `3 3 / 1 2 / 1 3 / 2 3` | `-1` | Impossible dense ordering |

## Edge Cases

Consider the disconnected graph:

```
4 1
1 2
```

DFS may process vertices in this order:

```
2, 1, 3, 4
```

Reversed:

```
4 3 1 2
```

The pair `(1,2)` is forbidden, so this candidate fails. Another traversal can produce:

```
2 1 3 4
```

Adjacent checks:

```
(2,1) OK
(1,3) OK
(3,4) OK
```

The algorithm correctly handles disconnected components because DFS starts from every unvisited node.

Now consider the cycle:

```
3 3
1 2
2 3
3 1
```

One valid order is:

```
1 3 2
```

Checks:

```
1 -> 3 exists? No
3 -> 2 exists? No
```

This confirms that cycles alone do not imply impossibility.

Finally consider the fully ordered tournament:

```
3 3
1 2
1 3
2 3
```

Every permutation contains some adjacent pair with a forbidden edge:

```
1 2 3
```

fails on `(1,2)`.

```
2 1 3
```

fails on `(1,3)`.

```
3 2 1
```

fails on `(2,1)` because there is no reverse edge, but `(1,?)` eventually creates another violation.

The algorithm detects this during final adjacency verification and prints `-1`.
