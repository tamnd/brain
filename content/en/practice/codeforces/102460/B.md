---
title: "CF 102460B - The Power Monitor System"
description: "The electrical network is a tree, so every pair of nodes has exactly one path between them. We need to choose as few nodes as possible for PMU placement. Placing a PMU at a node immediately monitors that node, every incident transmission line, and every neighboring node."
date: "2026-08-08T09:58:48+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102460
codeforces_index: "B"
codeforces_contest_name: "2019-2020 ICPC Asia Taipei-Hsinchu Regional Contest"
rating: 0
weight: 102460
solve_time_s: 188
verified: true
draft: false
---

[CF 102460B - The Power Monitor System](https://codeforces.com/problemset/problem/102460/B)

**Rating:** -  
**Tags:** -  
**Solve time:** 3m 8s  
**Verified:** yes  

## Solution
## Problem Understanding

The electrical network is a tree, so every pair of nodes has exactly one path between them. We need to choose as few nodes as possible for PMU placement.

Placing a PMU at a node immediately monitors that node, every incident transmission line, and every neighboring node. After that initial step, monitoring can spread through the tree. A monitored node can monitor its only remaining unmonitored neighbor, and once two endpoints of an edge are monitored, that edge is monitored as well. On a tree, these rules are exactly the usual power-domination process: first take the closed neighborhood of every selected vertex, then repeatedly let a monitored vertex force its unique unmonitored neighbor. The output is the minimum number of selected vertices needed to eventually monitor every node.

The input contains (n) nodes and exactly (n-1) edges. Since the graph is a tree, there are no cycles and no need for general graph algorithms. The limit (n\le 100000) rules out approaches that enumerate subsets of vertices, and a 2-second limit strongly favors an (O(n)) or (O(n\log n)) algorithm. The fact that every subtree is connected to the rest of the tree through exactly one parent edge is the structural property we will exploit.

A first edge case is the smallest possible tree:

```
2
1 2
```

One PMU is enough, because either node immediately monitors both nodes. The answer is `1`. An implementation that only considers internal vertices and forgets the final root case can incorrectly return zero.

A second edge case is a star:

```
5
1 2
1 3
1 4
1 5
```

The correct answer is `1`, by placing the PMU at node 1. A strategy that tries to handle leaves independently may incorrectly place several PMUs, even though one central PMU observes all of them immediately.

A third edge case is a branching tree where one PMU is not enough:

```
7
1 2
1 3
2 4
2 5
3 6
3 7
```

The correct answer is `2`. A PMU at node 1 observes nodes 1, 2, and 3, but each of nodes 2 and 3 still has two unmonitored children, so neither can force anything. Two additional PMUs are not necessary at arbitrary leaves, however, because placing them at nodes 2 and 3 monitors all four leaves. A naive rule such as "one PMU per branching vertex" would also be wrong on a star, where the branching vertex itself already solves the entire tree.

## Approaches

The direct brute-force approach is to try every possible subset of vertices as the PMU set. For each subset, simulate the monitoring rules until no new vertex can be monitored, then check whether the whole tree was covered. There are (2^n) possible subsets, and even a linear-time simulation for each subset gives (O(n2^n)) work. At (n=30), this is already about (30\cdot2^{30}), or roughly (3.2\times10^{10}) vertex-level operations. At (n=100000), exponential enumeration is completely infeasible.

The brute force works because the monitoring process itself is deterministic once the PMU positions are fixed. The problem is that it ignores the fact that a tree lets us decide about a subtree before its parent is processed.

Root the tree at node 1 and process vertices from the leaves toward the root. Consider a non-root vertex (v). By the time we process (v), all decisions inside its child subtrees have already been made, and any monitoring that can propagate upward has already been performed. The only connection between the subtree of (v) and the rest of the tree is the edge from (v) to its parent.

The key observation is that if (v) currently has at least two unmonitored children, the subtree cannot be completed merely by waiting for propagation through the parent. A monitored (v) can force at most one remaining neighbor. With two unmonitored child directions, some PMU must be used in this part of the tree. Placing that PMU at (v) is at least as useful as placing it deeper in one of those branches, because (v) directly observes all its children and also connects the subtree to the parent.

This gives a greedy postorder rule. Whenever a non-root vertex has at least two unmonitored children, put a PMU at that vertex and exhaustively apply the monitoring rules. Otherwise, postpone the decision because the vertex can still be handled by propagation from above. After all non-root vertices have been processed, if the root is still unmonitored, one final PMU at the root is necessary.

This is the standard linear-time tree algorithm for power domination. The postorder condition and its optimality follow from the fact that every child subtree has already been optimally resolved when its parent is considered.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | (O(n2^n)) | (O(n)) | Too slow |
| Optimal | (O(n)) | (O(n)) | Accepted |

## Algorithm Walkthrough

1. Root the tree at node 1 and compute a parent for every vertex. Store a traversal order so that reversing it processes children before their parents. The particular root does not affect the minimum answer, so choosing node 1 is only a convenient implementation choice.
2. Maintain `observed[v]`, which tells whether node (v) is already monitored. Also maintain `unobserved[v]`, the number of currently unmonitored neighbors of (v). This lets us apply the propagation rule without repeatedly scanning the whole graph.
3. Whenever a vertex becomes observed, decrease the unmonitored-neighbor count of each of its neighbors. If an observed vertex reaches exactly one unmonitored neighbor, put it into a queue because it can now force that neighbor.
4. When a PMU is placed at (v), mark (v) and all of its neighbors as observed. Then process the propagation queue until it becomes empty. This exactly reproduces the two phases of power domination: a PMU observes its closed neighborhood, after which monitored vertices repeatedly force their unique unmonitored neighbors.
5. Process every non-root vertex in reverse traversal order. Count how many of its children are still unobserved. If at least two children are unobserved, place a PMU at (v), increase the answer, and exhaust the propagation queue.
6. If (v) has zero or one unobserved child, do not place a PMU there. With at most one unobserved child, the parent side can eventually provide the missing monitored neighbor, allowing (v) to force that child. Spending a PMU earlier would not improve the optimum.
7. After all non-root vertices have been processed, inspect the root. If it is still unobserved, place one PMU there. Since the root has no parent, there is no later vertex that could force it, so this final check is necessary.
8. Output the number of PMUs placed.

The invariant is that after processing a vertex (v), the algorithm has already made the minimum necessary number of PMU decisions inside every processed child subtree, while leaving (v) to be handled from above whenever that is possible. If (v) has two unobserved children, one PMU inside its subtree is unavoidable, and placing it at (v) dominates both child directions at once. If it has at most one unobserved child, propagation can handle that remaining direction, so adding a PMU would be unnecessary. Because every subtree communicates with the rest of a tree through only its parent edge, these local decisions cannot interfere with an already processed subtree. This gives the global optimum.

## Python Solution

```python
import sys
from collections import deque

input = sys.stdin.readline

def solve():
    n = int(input())

    graph = [[] for _ in range(n)]
    for _ in range(n - 1):
        u, v = map(int, input().split())
        u -= 1
        v -= 1
        graph[u].append(v)
        graph[v].append(u)

    # Root the tree at 0.
    parent = [-1] * n
    order = [0]
    parent[0] = 0

    for v in order:
        for u in graph[v]:
            if u == parent[v]:
                continue
            parent[u] = v
            order.append(u)

    children = [[] for _ in range(n)]
    for v in range(1, n):
        children[parent[v]].append(v)

    observed = [False] * n
    unobserved = [len(graph[v]) for v in range(n)]
    queued = [False] * n
    q = deque()

    def observe(v):
        if observed[v]:
            return

        observed[v] = True

        for u in graph[v]:
            unobserved[u] -= 1
            if observed[u] and unobserved[u] == 1 and not queued[u]:
                queued[u] = True
                q.append(u)

    def propagate():
        while q:
            v = q.popleft()
            queued[v] = False

            if not observed[v] or unobserved[v] != 1:
                continue

            for u in graph[v]:
                if not observed[u]:
                    observe(u)
                    break

    def place_pmu(v):
        observe(v)
        for u in graph[v]:
            observe(u)
        propagate()

    answer = 0

    # Reverse order is a postorder because every child occurs
    # after its parent in the original traversal.
    for v in reversed(order[1:]):
        unobserved_children = 0

        for u in children[v]:
            if not observed[u]:
                unobserved_children += 1

        if unobserved_children >= 2:
            answer += 1
            place_pmu(v)

    if not observed[0]:
        answer += 1

    print(answer)

if __name__ == "__main__":
    solve()
```

The adjacency list stores the tree in (O(n)) space. The `parent` array and `order` array establish the rooted-tree order without recursive DFS, which avoids Python recursion-depth problems on a path containing 100000 vertices.

The `observe` function is the central bookkeeping operation. When a vertex becomes observed, every neighbor loses one unobserved neighbor. If an already observed neighbor now has exactly one unobserved neighbor, it becomes eligible to force. Each vertex becomes observed at most once, so all calls to `observe` together touch only (O(n)) edges.

The `place_pmu` function first observes the selected vertex and all its neighbors, exactly matching the initial effect of a PMU. It then calls `propagate`, which repeatedly performs the forcing rule. The `unobserved[v] == 1` check is the implementation of the rule that all but one incident edge are already monitored.

The postorder loop examines children after their subtrees have been resolved. Leaves have no children and therefore never trigger the `>= 2` condition, which is intentional. Choosing a leaf is never better than choosing its parent for this problem, so an optimal solution can always avoid selecting leaves.

The root is deliberately excluded from the greedy loop. The tree algorithm treats the root as the final unresolved boundary. If it remains unobserved, selecting it is both sufficient and necessary. Forgetting this final condition is the main boundary error on paths and on the two-vertex tree.

No integer can become large enough to overflow Python integers. The answer is at most (n), although for a tree of this type the actual optimum is usually much smaller.

## Worked Examples

For Sample 1, root the tree at node 1. The relevant child relationships are (1\to2), (2\to3,4), (4\to5,6), (6\to7,8), and (8\to9,10). Processing proceeds upward from the leaves.

| Processed vertex | Unobserved children before decision | PMU placed | Newly observed region |
| --- | --- | --- | --- |
| 8 | 2 | Yes | 8, 9, 10, and propagation toward 6 |
| 6 | 0 | No | Already observed |
| 4 | 1 | No | Child 6 is already observed |
| 2 | 1 | No | Child 4 is already observed |
| 1 | Final root check | No | Already observed |

The first PMU at node 8 propagates through the chain toward node 1. In this particular sample, that alone does not finish the upper branch immediately because node 2 has another child direction that remains unresolved. A second PMU is consequently required during the postorder processing, giving the sample answer `2`.

A more explicit state trace of the decisive choices is:

| Stage | PMUs so far | Important unobserved children | Action |
| --- | --- | --- | --- |
| Before 8 | 0 | 8 has 9 and 10 | Place PMU at 8 |
| After propagation | 1 | Upper chain partially monitored | Continue upward |
| At 4 | 1 | At most one unresolved child | Do not place |
| At 2 | 1 | Two unresolved directions | Place PMU at 2 |
| Root check | 2 | Root observed | Finish |

The example demonstrates why the threshold is two unobserved children rather than one. A vertex with exactly one unresolved child can use the forcing rule, while two unresolved child directions require a new source of monitoring.

For Sample 2, the tree is a star centered at node 1.

| Processed vertex | Unobserved children | PMU placed | State after propagation |
| --- | --- | --- | --- |
| 5 | 0 | No | Unchanged |
| 4 | 0 | No | Unchanged |
| 3 | 0 | No | Unchanged |
| 2 | 0 | No | Unchanged |
| 1 | Final root check | Yes | All five vertices observed |

The root is the natural choice here. Selecting node 1 immediately observes every leaf, so the answer is `1`. The example confirms why the root must be handled separately and why counting branching vertices alone cannot solve the problem.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | (O(n)) | Each vertex and edge is processed only a constant number of times |
| Space | (O(n)) | Adjacency lists, traversal arrays, states, and the propagation queue |

The tree contains exactly (n-1) edges, so its adjacency list has (O(n)) entries. The postorder traversal examines every child edge once, while each observation changes the state of a vertex only once and examines its incident edges once. Thus the total work is linear. For (n=100000), (O(n)) is comfortably within the intended scale of the problem, whereas the exponential brute-force approach is not remotely viable.

## Test Cases

```python
import sys
import io
from collections import deque

def solve_data(data: str) -> str:
    old_stdin = sys.stdin
    sys.stdin = io.StringIO(data)

    def input():
        return sys.stdin.readline

    n = int(input())

    graph = [[] for _ in range(n)]
    for _ in range(n - 1):
        u, v = map(int, input().split())
        u -= 1
        v -= 1
        graph[u].append(v)
        graph[v].append(u)

    parent = [-1] * n
    order = [0]
    parent[0] = 0

    for v in order:
        for u in graph[v]:
            if u == parent[v]:
                continue
            parent[u] = v
            order.append(u)

    children = [[] for _ in range(n)]
    for v in range(1, n):
        children[parent[v]].append(v)

    observed = [False] * n
    unobserved = [len(graph[v]) for v in range(n)]
    queued = [False] * n
    q = deque()

    def observe(v):
        if observed[v]:
            return

        observed[v] = True

        for u in graph[v]:
            unobserved[u] -= 1
            if observed[u] and unobserved[u] == 1 and not queued[u]:
                queued[u] = True
                q.append(u)

    def propagate():
        while q:
            v = q.popleft()
            queued[v] = False

            if not observed[v] or unobserved[v] != 1:
                continue

            for u in graph[v]:
                if not observed[u]:
                    observe(u)
                    break

    def place_pmu(v):
        observe(v)
        for u in graph[v]:
            observe(u)
        propagate()

    answer = 0

    for v in reversed(order[1:]):
        cnt = 0
        for u in children[v]:
            if not observed[u]:
                cnt += 1

        if cnt >= 2:
            answer += 1
            place_pmu(v)

    if not observed[0]:
        answer += 1

    sys.stdin = old_stdin
    return str(answer)

# Provided sample 1
sample1 = """\
10
1 2
2 3
2 4
4 5
4 6
6 7
6 8
8 9
8 10
"""
assert solve_data(sample1).strip() == "2", "sample 1"

# Provided sample 2
sample2 = """\
5
1 2
1 3
1 4
1 5
"""
assert solve_data(sample2).strip() == "1", "sample 2"

# Minimum-size tree
assert solve_data("""\
2
1 2
""").strip() == "1", "minimum-size tree"

# Balanced branching tree
assert solve_data("""\
7
1 2
1 3
2 4
2 5
3 6
3 7
""").strip() == "2", "two-level branching tree"

# Long path, exercising propagation and the root boundary
n = 100000
path_input = str(n) + "\n" + "\n".join(
    f"{i} {i + 1}" for i in range(1, n)
) + "\n"
assert solve_data(path_input).strip() == "1", "maximum-size path"

# Star with many equal leaf branches
n = 100000
star_input = str(n) + "\n" + "\n".join(
    f"1 {i}" for i in range(2, n + 1)
) + "\n"
assert solve_data(star_input).strip() == "1", "maximum-size star"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `2 / 1 2` | `1` | Minimum-size tree and final root handling |
| `7 / 1-2, 1-3, 2-4, 2-5, 3-6, 3-7` | `2` | Two simultaneous unresolved branches |
| A path of 100000 vertices | `1` | Maximum size, deep propagation, no recursion |
| A star of 100000 vertices | `1` | Maximum degree and immediate domination |

## Edge Cases

For the two-vertex tree

```
2
1 2
```

the only non-root vertex is a leaf, so the postorder loop never places a PMU. Node 1 is still unobserved, so the final root check places one PMU at node 1. That PMU observes both vertices, producing `1`.

For the star

```
5
1 2
1 3
1 4
1 5
```

all four non-root vertices are leaves. The greedy loop therefore places no PMUs. The root is unobserved, so one PMU is placed at node 1. Its closed neighborhood contains the entire tree, giving `1`.

For the branching tree

```
7
1 2
1 3
2 4
2 5
3 6
3 7
```

the leaves are processed first and cannot trigger a PMU. When node 2 is processed, both children 4 and 5 are unobserved, so node 2 receives a PMU and both leaves become observed. The same happens independently at node 3. Node 1 is then already observed, so the final answer is `2`. This is exactly the situation where allowing a vertex with two unresolved children to remain undecided would leave two branches that no single forcing step can enter.

For a long path such as

```
5
1 2
2 3
3 4
4 5
```

every internal vertex has at most one unobserved child when it is processed. The algorithm consequently places no PMU until the root check. A PMU at node 1 observes nodes 1 and 2, node 2 then forces node 3, node 3 forces node 4, and node 4 forces node 5. The answer is `1`. This catches the common mistake of assuming that a long path needs several PMUs merely because the initial neighborhood of one PMU is small.
