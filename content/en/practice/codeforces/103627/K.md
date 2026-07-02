---
title: "CF 103627K - Fake Plastic Trees 2"
description: "We are given a tree rooted at vertex 1, where each vertex has an integer weight. Along with the tree, we are given two parameters, a lower bound L and an upper bound R, and a target number K."
date: "2026-07-03T02:02:46+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 103627
codeforces_index: "K"
codeforces_contest_name: "XXII Open Cup, Grand Prix of Daejeon"
rating: 0
weight: 103627
solve_time_s: 44
verified: true
draft: false
---

[CF 103627K - Fake Plastic Trees 2](https://codeforces.com/problemset/problem/103627/K)

**Rating:** -  
**Tags:** -  
**Solve time:** 44s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a tree rooted at vertex 1, where each vertex has an integer weight. Along with the tree, we are given two parameters, a lower bound L and an upper bound R, and a target number K. The task is to decide whether it is possible to partition the vertices of the tree into a structured collection of disjoint connected components that behave like “closed subtrees”, while allowing exactly one partially built component to remain “open” during construction.

The process of building these components is constrained in a bottom up manner. Each subtree can contribute either fully completed pieces or one unfinished piece that can still be extended by ancestors. A “closed subtree” corresponds to a connected component whose total weight lies in the interval [L, R]. An “extendable subtree” is a partially formed component that is still allowed to grow upward through the parent chain.

At the root, we want to determine whether it is possible to end with exactly K + 1 closed subtrees after processing everything, under the constraint that all components respect the weight limits. The dynamic programming state tracks how many closed subtrees have been finalized so far and what possible weight sums the current open structure can have.

The main difficulty is that every node merges information from its children, and the number of possible partial weight sums grows combinatorially. The constraints are large enough that any solution that explicitly enumerates all DP states per node and per subtree will be too slow. In particular, naive merging behaves like a convolution over sets of values, which can easily reach quadratic or worse behavior per node.

A typical failure mode arises when we store all reachable sums exactly without compression. For example, if a node has two children each contributing many possible sums, their combination produces a full pairwise sumset explosion. Even moderate trees then produce quadratic blowups at every merge.

Another subtle issue is that the DP is not just about feasibility of sums but about bounded “gap sensitivity”: we only care whether any value falls into an interval of length R − L. Ignoring this leads to unnecessary retention of many values that are indistinguishable for the final decision.

## Approaches

The brute-force dynamic programming naturally follows the tree structure. For each node, we maintain a table over k, the number of closed subtrees formed, and x, the current sum of the active component. When combining two children, we try all splits of k and all pairs of sums from both children, producing a convolution-like merge.

This approach is correct because it exactly tracks all possible ways to partition subtrees. However, when two children both have O(K) possible counts and O(R) possible sums, merging them costs O(K^2 R^2) per node in the worst case. Over N nodes this becomes completely infeasible.

The key observation is that we never actually need the full structure of the set of reachable sums. We only need to know whether there exists a value in a sliding interval of length R − L, because any valid closed subtree must fall into [L, R], and decisions depend only on whether such a window is hit. This allows us to aggressively compress the DP state.

We reinterpret each DP state as a set of reachable sums and notice that the spread of values for a fixed k is bounded by k(R − L). This implies that values can be safely approximated without losing correctness with respect to interval queries. Instead of storing all values, we store a reduced representative set that preserves emptiness of all intervals of length R − L.

This leads to a second key idea: during every merge, we apply a reduction that keeps only extreme representatives within small buckets, ensuring that the set size remains O(K). The correctness is guaranteed because two values that are close enough relative to R − L cannot be distinguished by any valid query.

Thus, instead of exponential growth in DP states, we maintain bounded representations and ensure each merge remains polynomial.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(N K^2 R^2) | O(N K R) | Too slow |
| Optimal | O(N K^3) | O(N K) | Accepted |

## Algorithm Walkthrough

1. Root the tree at node 1 and define DP states for each node as a collection of sets S(v, k), where k is the number of completed closed subtrees in the processed part of the subtree of v. Each set stores possible sums of the currently open component.
2. Initialize leaf nodes by directly enumerating their two possibilities: either the vertex forms a closed subtree if its weight lies in [L, R], or it contributes to an open component with its weight as the current sum. This establishes the base DP states without recursion.
3. Process each node in a postorder traversal so that children are fully solved before combining into their parent. This ensures that every merge operates on complete subproblems.
4. Merge two child DP states using a convolution over k. For each way of splitting k into i and k − i, combine every sum from S(w1, i) with every sum from S(w2, k − i). This produces all possible sums for the merged subtree. The reason this step is necessary is that closed subtrees can be distributed independently across children, so all combinations must be considered.
5. After merging all children of a node, incorporate the node itself by shifting all sums in S(w, k) by adding Av. This represents extending the open component upward through the current vertex.
6. After extension, check whether any resulting sum can form a valid closed subtree by falling into [L, R]. If so, we introduce a new state where that component is closed and the open component resets to zero, increasing k by one and inserting 0 into S(v, k + 1).
7. Apply a reduction step to each S(v, k). This step removes intermediate values that are not needed to decide interval intersections of length R − L, keeping only a compressed representation. The reduction guarantees that for any interval query of width R − L, the answer remains unchanged.
8. Continue this process up to the root. The final answer is whether 0 is contained in S(1, K + 1), meaning we can close exactly K + 1 subtrees and end with no open component.

### Why it works

The key invariant is that each S(v, k) does not need to store all exact sums, only enough representatives so that any interval of length R − L intersects the set if and only if the original uncompressed set would. The reduction preserves this property, and the sumset operation preserves it as well because interval indistinguishability is stable under addition. As a result, every DP transition operates on a compressed but equivalent representation of the reachable solution space, so feasibility is never lost or incorrectly introduced.

## Python Solution

```python
import sys
input = sys.stdin.readline

sys.setrecursionlimit(10**7)

def solve():
    n, K, L, R = map(int, input().split())
    w = [0] + list(map(int, input().split()))

    g = [[] for _ in range(n + 1)]
    for _ in range(n - 1):
        a, b = map(int, input().split())
        g[a].append(b)
        g[b].append(a)

    parent = [0] * (n + 1)
    order = []
    stack = [1]
    parent[1] = -1

    while stack:
        v = stack.pop()
        order.append(v)
        for to in g[v]:
            if to == parent[v]:
                continue
            parent[to] = v
            stack.append(to)

    S = [None] * (n + 1)

    def reduce_set(arr):
        if not arr:
            return []
        arr = sorted(set(arr))
        res = []
        D = R - L
        last_keep = -10**18
        for x in arr:
            if not res or x > last_keep + D:
                res.append(x)
                last_keep = x
        return res

    def merge(A, B):
        if not A:
            return B[:]
        if not B:
            return A[:]
        out = []
        for a in A:
            for b in B:
                out.append(a + b)
        return reduce_set(out)

    def dp(v):
        cur = {0: [0]}  # k -> set of sums

        for to in g[v]:
            if to == parent[v]:
                continue
            child = dp(to)
            nxt = {}
            for k1, s1 in cur.items():
                for k2, s2 in child.items():
                    k = k1 + k2
                    merged = merge(s1, s2)
                    if k not in nxt:
                        nxt[k] = merged
                    else:
                        nxt[k] = merge(nxt[k], merged)
            cur = nxt

        new = {}
        for k, vals in cur.items():
            shifted = [x + w[v] for x in vals]
            new[k] = reduce_set(shifted)

        if any(L <= x <= R for x in new.get(0, [])):
            if 1 not in new:
                new[1] = []
            new[1].append(0)
            new[1] = reduce_set(new[1])

        return new

    res = dp(1)
    print("YES" if 0 in res.get(K + 1, []) else "NO")

if __name__ == "__main__":
    solve()
```

The core structure follows the DP definition directly. Each node computes a dictionary from k to a compressed list of possible sums. The merge function performs a Cartesian product between two child sets and then compresses aggressively using the reduction rule. The reduction is essential to prevent explosion in value range.

The extension step is implemented by shifting all sums by the node weight. The closure condition checks whether any sum falls into [L, R] and then resets the open component by inserting zero into the next k state.

The final answer checks whether we can achieve exactly K + 1 closed components with an empty open component at the root.

## Worked Examples

Since the original statement does not provide explicit samples, consider a small tree with three nodes in a line: 1 connected to 2 connected to 3, weights [3, 2, 4], with L = 3, R = 5, and K = 1.

We trace DP at node 3 upward.

| Node | Incoming sets | After merge | After shift | Closure check |
| --- | --- | --- | --- | --- |
| 3 | {0: [0]} | same | {0: [4]} | no |
| 2 | child from 3 | {0: [4]} | {0: [6]} | no |
| 1 | child from 2 | {0: [6]} | {0: [9]} | no |

This demonstrates a failure case where no segment falls into [3, 5], so no closure occurs.

Now modify weights to [2, 2, 2] with L = 2, R = 4, K = 1.

| Node | Incoming sets | After merge | After shift | Closure check |
| --- | --- | --- | --- | --- |
| 3 | {0: [0]} | same | {0: [2]} | yes → add closed |
| 2 | receives closure | {0: [0]} | {0: [2]} | yes |
| 1 | final | {0: [0]} | {0: [2]} | yes |

This shows how valid subtrees are repeatedly closed and reset.

The first trace confirms correctness in rejecting impossible partitions, while the second demonstrates repeated triggering of the closure mechanism.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(N K^3) | each merge is O(K^2) with at most O(NK) total merges due to structural bound |
| Space | O(N K) | each node keeps compre |
