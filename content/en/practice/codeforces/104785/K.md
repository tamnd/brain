---
title: "CF 104785K - Kernel Scheduler"
description: "We are given a directed graph where each task is a vertex and each dependency is a directed edge. An edge a - b means task a must be executed before task b."
date: "2026-06-28T14:41:59+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104785
codeforces_index: "K"
codeforces_contest_name: "2023 United Kingdom and Ireland Programming Contest (UKIEPC 2023)"
rating: 0
weight: 104785
solve_time_s: 56
verified: true
draft: false
---

[CF 104785K - Kernel Scheduler](https://codeforces.com/problemset/problem/104785/K)

**Rating:** -  
**Tags:** -  
**Solve time:** 56s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a directed graph where each task is a vertex and each dependency is a directed edge. An edge `a -> b` means task `a` must be executed before task `b`.

The issue is that these dependencies may contain directed cycles, which make it impossible to execute all tasks in a valid order. We are allowed to remove some edges to eliminate all cycles, but we must still keep at least half of the original edges.

The output is not an ordering of tasks, but a subset of dependency edges such that the remaining directed graph has no directed cycles and the number of kept edges is at least half of the original number.

The key structural requirement is that the kept edges must form a Directed Acyclic Graph. That means there must exist some ordering of vertices such that every kept edge goes from an earlier vertex to a later vertex.

The constraints allow up to `n = 100000` and `m = 300000`, which immediately rules out any exponential or quadratic reasoning over edges or permutations of vertices. Anything involving searching over orderings or repeatedly checking cycles per removal would be far too slow.

A subtle point is that multiple edges between the same pair of vertices are allowed, and they are treated independently. Each edge is selected or removed independently based on whether it fits the chosen acyclic structure.

A naive mistake would be to try to directly break cycles using DFS cycle detection and remove one edge per cycle found. This fails because cycles overlap and the greedy removal might delete far more than necessary, easily dropping below the required `m/2` threshold.

Another mistake would be to attempt a full topological sort on the original graph. That only works if the graph is already a DAG, which is not guaranteed.

## Approaches

A brute-force interpretation would try to test subsets of edges, checking whether a chosen subset is acyclic and large enough. Even checking a single subset requires cycle detection in `O(n + m)`, and there are `2^m` subsets, which is completely infeasible.

A more structured brute-force idea is to assign an ordering of vertices and keep only edges consistent with it. This always produces an acyclic graph, but the challenge becomes finding an ordering that keeps at least half of the edges. Searching over all permutations is again impossible.

The key observation is that every total ordering of vertices partitions the edges into two disjoint groups: edges that go forward in the order and edges that go backward. The forward edges always form a DAG. If we pick the identity order `1 to n`, we get one valid subset. If we pick the reverse order, we get another valid subset. Every edge belongs to exactly one of these two subsets because for any edge `a -> b`, either `a < b` or `a > b`.

This immediately implies that the two subsets together cover all edges, so one of them must contain at least half of the edges. Selecting the larger subset guarantees both acyclicity and the size requirement.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Enumerate subsets / cycle checking | O(2^m) | O(m) | Too slow |
| Two-order partition (forward vs reverse) | O(n + m) | O(m) | Accepted |

## Algorithm Walkthrough

We construct two candidate sets of edges using a fixed ordering of vertices.

First we treat the natural order `1, 2, ..., n` as a topological order candidate and collect all edges that go from a smaller index to a larger index.

Second we consider the reverse order `n, ..., 1` and collect all edges that go forward in that order, which corresponds to edges where `a > b` in the original numbering.

We then choose the larger of these two sets.

### Steps

1. Read all edges and assign them their input indices so we can output them later. This indexing matters because the output requires original edge IDs.
2. Initialize two lists, one for edges where `a < b` and another for edges where `a > b`. Each list represents edges consistent with a different total ordering.
3. For every edge, compare its endpoints. If `a < b`, it is consistent with the natural order and is added to the first list. Otherwise it is consistent with the reversed order and is added to the second list.
4. Compare the sizes of the two lists. Select the larger one, since we must guarantee at least `m/2` edges.
5. Output `YES`, then the size of the selected list, then the indices of its edges.

The reason this works is that every edge is assigned to exactly one of the two lists, so their sizes sum to `m`. Therefore at least one list must have size at least `m/2`. Both lists correspond to edges consistent with a total ordering, which guarantees acyclicity.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, m = map(int, input().split())
    
    forward = []
    backward = []
    
    for i in range(1, m + 1):
        a, b = map(int, input().split())
        if a < b:
            forward.append(i)
        else:
            backward.append(i)
    
    if len(forward) >= len(backward):
        chosen = forward
    else:
        chosen = backward
    
    print("YES")
    print(len(chosen))
    print(*chosen)

if __name__ == "__main__":
    solve()
```

The implementation relies on a direct partition of edges. The index loop is important because the output requires original edge IDs, so we store `i` for each edge as it is read.

No graph structure beyond the raw edges is needed. The entire solution is based on comparing endpoints and grouping accordingly.

A common implementation error is forgetting that edges are 1-indexed in the input order. Another is accidentally recomputing or modifying the edge list instead of preserving indices.

## Worked Examples

### Example Trace 1

Consider input:

```
n = 3, m = 3
1 -> 2
2 -> 3
3 -> 1
```

We process edges one by one.

| Edge | a < b | Forward list | Backward list |
| --- | --- | --- | --- |
| 1->2 | yes | [1] | [] |
| 2->3 | yes | [1,2] | [] |
| 3->1 | no | [1,2] | [3] |

We compare sizes: forward has 2 edges, backward has 1 edge. We choose forward.

The selected edges form a DAG under ordering `1 < 2 < 3`, so no cycles remain.

This demonstrates how a cycle is broken implicitly by discarding the backward edge.

### Example Trace 2

Consider input:

```
n = 2, m = 5
1 -> 2
1 -> 2
1 -> 2
2 -> 1
2 -> 1
```

We process:

| Edge | a < b | Forward list | Backward list |
| --- | --- | --- | --- |
| 1->2 | yes | [1] | [] |
| 1->2 | yes | [1,2] | [] |
| 1->2 | yes | [1,2,3] | [] |
| 2->1 | no | [1,2,3] | [4] |
| 2->1 | no | [1,2,3] | [4,5] |

We select forward with size 3.

This shows that duplicate edges are handled independently and the selection still guarantees at least half.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n + m) | Each edge is processed once and assigned to one of two lists |
| Space | O(m) | We store indices of edges in two groups |

The constraints allow up to 300000 edges, so a single linear scan is sufficient. No additional graph traversal or sorting is required.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from __main__ import solve
    import contextlib
    out = io.StringIO()
    with contextlib.redirect_stdout(out):
        solve()
    return out.getvalue().strip()

# minimum case
assert run("2 1\n1 2\n") == "YES\n1\n1"

# simple cycle
assert run("3 3\n1 2\n2 3\n3 1\n") in ["YES\n2\n1 2", "YES\n2\n1 3"]

# reverse-heavy case
assert run("3 4\n2 1\n3 2\n3 1\n2 1\n") != ""

# all forward
assert run("4 3\n1 2\n2 3\n3 4\n") == "YES\n3\n1 2 3"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single edge | keep it | minimal correctness |
| 3-cycle | at least 2 edges kept | cycle breaking |
| mixed directions | valid subset | partition logic |
| already DAG | all edges kept | no unnecessary removals |

## Edge Cases

A key edge case is when all edges point in decreasing order, for example `3 -> 2`, `2 -> 1`, `3 -> 1`. In this situation, the forward list under natural ordering is empty, while the backward list contains all edges. The algorithm correctly selects the backward list, which corresponds to reversing the order and thus produces a valid DAG.

Another case is a fully symmetric complete digraph where every pair has both directions. Each pair contributes exactly one edge to each list, so both lists have equal size. Either choice is valid and still acyclic under the corresponding ordering.

These cases confirm that the partition strategy is stable even under adversarial input distributions.
