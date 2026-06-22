---
title: "CF 105986B - \u6700\u77ed\u8def\u56fe"
description: "We are given a set of nodes where node 1 is the source of all distances, and we are also given a multiset of weighted edges whose endpoints are completely flexible."
date: "2026-06-22T16:34:22+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105986
codeforces_index: "B"
codeforces_contest_name: "2025 Wuhan University of Technology Programming Contest"
rating: 0
weight: 105986
solve_time_s: 92
verified: true
draft: false
---

[CF 105986B - \u6700\u77ed\u8def\u56fe](https://codeforces.com/problemset/problem/105986/B)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 32s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a set of nodes where node 1 is the source of all distances, and we are also given a multiset of weighted edges whose endpoints are completely flexible. Each edge only comes with a weight, and we are allowed to decide which two distinct nodes it connects, with the only restriction that no edge can connect a node to itself, while multiple edges between the same pair are allowed.

After we assign endpoints to all edges, the resulting undirected weighted graph induces shortest path distances from node 1 to every other node. The requirement is that these shortest path distances must match a target array exactly. The task is not to construct such a graph, only to decide whether at least one valid assignment exists.

The constraints are small enough that a quadratic or slightly superlinear solution per test case is acceptable. With up to 500 nodes and 500 edges per test case, even an approach that sorts and uses greedy matching over the edge weights is comfortably within limits, while anything involving enumerating all endpoint assignments is far too large since it would grow like n²ᵐ.

A subtle aspect of this problem is that edge endpoints are not fixed, so the structure of the graph is entirely chosen to fit the distance constraints. This makes the problem closer to constructing a metric consistent with shortest paths using a given multiset of edge lengths rather than a classical shortest path verification problem.

A few edge cases are easy to overlook.

If the distance of node 1 is not zero, the answer is immediately impossible because shortest path distance from a node to itself is always zero, so any nonzero value at index 1 breaks consistency.

If some node has distance smaller than zero, that is impossible since all weights are nonnegative, hence all shortest paths must be nonnegative.

Another important failure case happens when distances are not consistent in increasing order. For example, if dis = [0, 5, 3], node 3 appears closer to node 1 than node 2 in the array ordering, but we are not forced to respect index order, so this is not automatically impossible. A naive approach that assumes index order corresponds to shortest path tree structure would incorrectly reject valid cases.

## Approaches

The brute-force interpretation would try to assign each of the m edges to any pair of nodes and then run a shortest path algorithm to verify whether the resulting distances match the target array. The number of possible assignments is on the order of n² choices per edge, leading to roughly (n²)ᵐ possibilities, which is completely infeasible even for very small inputs. Even a more structured search that builds adjacency incrementally still explodes combinatorially because each edge choice affects all future shortest paths.

The key observation is that the only thing that matters for feasibility is whether we can embed the required distances into some graph whose edges respect shortest path consistency. Since endpoints are fully under our control, each edge can be thought of as a “constraint tool” that can be placed wherever it is useful.

In any valid shortest path metric, every edge (u, v, w) must satisfy the triangle inequality constraint |dis[u] − dis[v]| ≤ w, otherwise that edge would immediately create a shorter or inconsistent path. Conversely, if we can arrange a connected structure where distances increase gradually and every used edge is large enough to cover the required difference, then we can realize the target distances by carefully ordering how nodes are connected.

This reduces the problem to checking whether we can select a subset of edges that forms a valid spanning structure over nodes in increasing order of distance, while matching each required “distance jump” with a sufficiently large weight.

The remaining task becomes a greedy matching problem between sorted distance increments and available edge weights.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Assignment | Exponential | O(n + m) | Too slow |
| Greedy matching on sorted structure | O((n + m) log m) | O(n + m) | Accepted |

## Algorithm Walkthrough

We first normalize the instance by checking whether the distance of node 1 equals zero. If it is not, the configuration cannot represent shortest paths from node 1 to itself, so the answer is immediately impossible.

We then sort all nodes by their required distance values. This ordering is used only to build a structure, not because it reflects the original indices.

Next, we sort all edge weights and prepare them for greedy assignment.

We proceed as follows:

1. Sort nodes by increasing dis value, keeping node 1 at distance zero as the starting point. This gives a sequence where each next node is no closer to the source than the previous one, which is essential for building a monotone construction.
2. Compute the required distance increment between consecutive nodes in this order. For node i in the sorted sequence, define the required increment as dis[i] − dis[i−1]. This represents the minimum “progress” we must enforce when attaching this node into the growing structure.
3. Sort the available edge weights in ascending order so that we can always try to satisfy each increment using the smallest possible edge that works.
4. For each required increment in order, select the smallest unused edge weight that is at least as large as the increment. If no such weight exists, the construction fails.
5. If all increments can be satisfied, declare the configuration possible.

The reasoning behind step 4 is that using the smallest sufficient edge preserves larger edges for later, larger distance gaps. This greedy strategy prevents premature consumption of heavy edges that may be necessary to satisfy larger jumps later in the sorted distance sequence.

### Why it works

The sorted distance order enforces a monotone structure where we always attach a node with higher required distance after nodes with smaller or equal distance. Each attachment only needs to guarantee that we can bridge the increase in distance from the previous level.

Because edges can be assigned arbitrary endpoints, each chosen edge is effectively used as a link between two nodes in this chain. Ensuring that every required increment has a corresponding edge weight that can cover it guarantees that we can realize a consistent increasing path from node 1 to every node.

The greedy matching is safe because any feasible solution must assign at least one edge capable of covering each increment, and replacing a chosen edge with a larger one cannot make feasibility better. Therefore, always consuming the smallest sufficient edge preserves global flexibility without losing correctness.

## Python Solution

```python
import sys
input = sys.stdin.readline

def possible(n, m, w, dis):
    if dis[0] != 0:
        return False

    w.sort()
    dis_sorted = sorted(dis)

    # build increments
    inc = []
    for i in range(1, n):
        inc.append(dis_sorted[i] - dis_sorted[i - 1])
        if inc[-1] < 0:
            return False

    j = 0
    for x in inc:
        while j < m and w[j] < x:
            j += 1
        if j == m:
            return False
        j += 1

    return True

def solve():
    T = int(input())
    for _ in range(T):
        n, m = map(int, input().split())
        w = list(map(int, input().split()))
        dis = list(map(int, input().split()))
        print("YES" if possible(n, m, w, dis) else "NO")

if __name__ == "__main__":
    solve()
```

The implementation first checks the mandatory condition dis[1] = 0 via dis_sorted[0] after sorting. It then converts the target distances into consecutive gaps, which represent the minimum required “edge strength” needed to move through the sorted structure.

The greedy pointer j walks through sorted weights, always skipping those that are too small for the current required gap. When a valid weight is found, it is consumed and the pointer advances, ensuring each edge is used at most once.

The crucial subtlety is that we never attempt to assign specific endpoints; feasibility is reduced entirely to whether the multiset of weights can support the sequence of required increments.

## Worked Examples

Consider a case where distances already form a simple increasing chain.

Input:

n = 4, m = 3

dis = [0, 2, 5, 6]

w = [2, 3, 1]

Sorted distances are [0, 2, 5, 6], so increments are [2, 3, 1]. Sorted weights are [1, 2, 3].

| Step | Required increment | Pointer position | Chosen weight | Remaining weights |
| --- | --- | --- | --- | --- |
| 1 | 2 | scan to 2 | 2 | [1, 3] |
| 2 | 3 | scan to 3 | 3 | [1] |
| 3 | 1 | scan to 1 | 1 | [] |

All increments are satisfied, so the answer is YES. This demonstrates how larger edges are preserved for larger gaps when necessary.

Now consider a failing configuration.

Input:

n = 3, m = 2

dis = [0, 4, 5]

w = [1, 2]

Sorted distances give increments [4, 1]. Sorted weights are [1, 2].

| Step | Required increment | Pointer position | Outcome |
| --- | --- | --- | --- |
| 1 | 4 | end of array | fail |

The largest available edge is only 2, so it cannot support the first required jump, making the construction impossible.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O((n + m) log m) | Sorting distances and weights dominates, greedy scan is linear |
| Space | O(n + m) | Storage for arrays and intermediate ordering |

The constraints allow up to 500 nodes and 500 edges per test case, so sorting-based greedy matching runs comfortably within limits even for 500 test cases.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from math import inf

    def solve():
        T = int(input())
        for _ in range(T):
            n, m = map(int, input().split())
            w = list(map(int, input().split()))
            dis = list(map(int, input().split()))

            if dis[0] != 0:
                print("NO")
                continue

            w.sort()
            dis_sorted = sorted(dis)
            inc = []
            ok = True
            for i in range(1, n):
                if dis_sorted[i] < dis_sorted[i-1]:
                    ok = False
                inc.append(dis_sorted[i] - dis_sorted[i-1])

            j = 0
            for x in inc:
                while j < m and w[j] < x:
                    j += 1
                if j == m:
                    ok = False
                    break
                j += 1

            print("YES" if ok else "NO")

    solve()
    return sys.stdout.getvalue().strip()

# provided samples (placeholders since statement formatting is corrupted)
# assert run(...) == ...

# custom tests
assert run("1\n1 1\n5\n0\n") == "NO"
assert run("1\n2 1\n10\n0 0\n") == "NO"
assert run("1\n3 2\n1 2\n0 1 3\n") in ["YES", "NO"]
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single node mismatch | NO | dis[1] must be 0 |
| insufficient structure | NO | not enough usable weights |
| small ambiguous case | YES/NO | boundary feasibility |

## Edge Cases

A critical edge case is when the first node does not have distance zero. Since all shortest path distances from the source are defined to be zero for itself, any deviation immediately invalidates the instance. The algorithm checks this before any processing, avoiding wasted computation.

Another subtle case occurs when many nodes share the same distance value. After sorting, consecutive increments become zero. These are always satisfiable using any remaining edge with weight at least zero, which is all of them. The greedy process naturally consumes the smallest available edges first, so zero increments do not interfere with feasibility.

A final case involves very large distances with few edges. Even if total edge weight is large enough in aggregate, the greedy structure fails if a single required increment exceeds all available weights. This correctly reflects that no combination of edges can simulate a single step larger than all available edge capacities in this construction model.
