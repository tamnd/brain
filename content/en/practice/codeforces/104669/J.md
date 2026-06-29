---
title: "CF 104669J - Keys and the Subtree Permutation (Easy Version)"
description: "A tree is given with nodes numbered from 1 to N, rooted at node 1. Each node carries a distinct label, and these labels form a permutation of the numbers from 1 to N. For every node, we look at the nodes inside its rooted subtree and collect their labels."
date: "2026-06-29T09:43:48+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104669
codeforces_index: "J"
codeforces_contest_name: "Turtle Codes"
rating: 0
weight: 104669
solve_time_s: 70
verified: true
draft: false
---

[CF 104669J - Keys and the Subtree Permutation (Easy Version)](https://codeforces.com/problemset/problem/104669/J)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 10s  
**Verified:** yes  

## Solution
## Problem Understanding

A tree is given with nodes numbered from 1 to N, rooted at node 1. Each node carries a distinct label, and these labels form a permutation of the numbers from 1 to N.

For every node, we look at the nodes inside its rooted subtree and collect their labels. The task is to determine whether this collected set of labels forms a perfect permutation of length equal to the size of the subtree. In other words, if a subtree has k nodes, we check whether its labels are exactly the numbers from 1 to k in some order.

The output is a sequence of answers, one per node, indicating whether that node’s subtree satisfies this property.

The constraint N up to 200,000 forces a linear or near linear solution. Any approach that repeatedly inspects entire subtrees independently will recompute the same structure many times and drift toward quadratic behavior, which is far beyond acceptable limits. Even operations like sorting each subtree would imply a total cost of roughly O(N log N) per node in the worst case, which degenerates to O(N^2 log N) on a chain shaped tree.

A subtle edge case comes from the fact that labels are globally unique. This removes any ambiguity about duplicates inside a subtree, but it also hides the key difficulty: even though there are no repeats, a subtree can still fail the condition if its values are not exactly the range 1 through k.

For example, consider a subtree of size 3 containing values {2, 3, 4}. It is not valid, even though it is perfectly sized and has no duplicates, because it does not match the required canonical numbering.

Another case is a subtree of size 3 containing {1, 2, 4}. This also fails, and a naive "check min and max only" approach might incorrectly pass it if not carefully reasoned.

## Approaches

A direct approach is to compute, for each node, the full list of values in its subtree, sort it, and then verify whether it matches the sequence 1 to k. This is correct because it explicitly reconstructs the condition being tested. The issue is cost. Each subtree extraction is linear in its size, and sorting adds a logarithmic factor, so over all nodes this becomes prohibitively expensive in large trees where many subtrees overlap.

The key observation is that we do not actually need the full ordering of values. Since every label is unique globally, each subtree already contains k distinct integers. The only thing that matters is whether those k integers exactly fill the interval from 1 to k without gaps. That condition can be verified using only two aggregates: the minimum value and the maximum value inside the subtree.

If a subtree of size k has minimum value 1 and maximum value k, then all values must lie inside [1, k], and since there are exactly k distinct values, they must occupy every integer in that range. This reduces the problem from maintaining sets to maintaining simple subtree statistics.

We therefore switch from recomputing explicit sets to a single DFS that computes subtree size, minimum, and maximum for every node.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force (subtree extraction + sorting) | O(N² log N) | O(N) | Too slow |
| DFS with subtree min, max, size | O(N) | O(N) | Accepted |

## Algorithm Walkthrough

We root the tree at node 1 and perform a postorder traversal so that children are processed before their parent.

1. Start a DFS from node 1, treating the tree as directed away from the root. This ensures each subtree is processed exactly once in a bottom-up manner.
2. For each node u, initialize its subtree size as 1, and set both its minimum and maximum value to P[u]. This represents the trivial subtree containing only u.
3. Traverse each child v of u, skipping the parent to avoid cycling back in the undirected tree.
4. After returning from DFS(v), merge the information from v into u by adding sizes, taking the minimum of subtree minima, and the maximum of subtree maxima. This step combines disjoint child subtrees into the full subtree of u.
5. Once all children are processed, the subtree of u is fully represented by three values: sz[u], mn[u], mx[u].
6. Check whether mn[u] equals 1 and mx[u] equals sz[u]. If both hold, mark u as valid, otherwise mark it invalid.

The correctness of the merge step relies on the fact that subtree decomposition in a tree is disjoint: each node belongs to exactly one child subtree, so aggregation over children preserves exact counts and value ranges without overlap.

### Why it works

Each subtree maintains a complete summary of its values through three invariants: its size, its smallest label, and its largest label. Because all labels are distinct globally, these summaries are lossless for the specific condition being checked. A subtree of size k whose values lie entirely within [1, k] must contain every integer in that interval, since skipping even one number would force either a smaller size or a gap that contradicts the max bound.

## Python Solution

```python
import sys
sys.setrecursionlimit(10**7)
input = sys.stdin.readline

def solve():
    n = int(input())
    p = [0] + list(map(int, input().split()))
    
    g = [[] for _ in range(n + 1)]
    for _ in range(n - 1):
        u, v = map(int, input().split())
        g[u].append(v)
        g[v].append(u)
    
    sz = [0] * (n + 1)
    mn = [10**18] * (n + 1)
    mx = [0] * (n + 1)
    ans = [False] * (n + 1)
    
    def dfs(u, parent):
        sz[u] = 1
        mn[u] = p[u]
        mx[u] = p[u]
        
        for v in g[u]:
            if v == parent:
                continue
            dfs(v, u)
            sz[u] += sz[v]
            mn[u] = min(mn[u], mn[v])
            mx[u] = max(mx[u], mx[v])
        
        if mn[u] == 1 and mx[u] == sz[u]:
            ans[u] = True
    
    dfs(1, -1)
    
    out = []
    for i in range(1, n + 1):
        out.append("YES" if ans[i] else "NO")
    print("\n".join(out))

if __name__ == "__main__":
    solve()
```

The DFS computes subtree statistics in a single traversal. Each node initializes its own contribution and then absorbs results from its children. The parent parameter prevents revisiting the previous node in the undirected adjacency list.

A common implementation pitfall is forgetting to initialize mn[u] and mx[u] for every node before merging children, which would cause values from previous test cases or recursive calls to leak into unrelated computations. Another subtle point is recursion depth, since a chain-shaped tree at N = 200,000 would overflow default Python limits without an explicit increase.

## Worked Examples

### Example 1

Input:

```
4
4 2 1 3
2 1
3 2
4 1
```

We track subtree summaries.

| Node | sz | mn | mx | Valid check |
| --- | --- | --- | --- | --- |
| 1 | 4 | 1 | 4 | YES |
| 2 | 2 | 1 | 2 | YES |
| 3 | 1 | 1 | 1 | YES |
| 4 | 1 | 3 | 3 | NO |

This shows how the condition depends only on whether the subtree values cover exactly the range from 1 to its size. Node 4 fails because its single value is not 1, even though it forms a valid single-element subtree structurally.

### Example 2

Input:

```
5
1 3 2 5 4
1 2
1 3
3 4
3 5
```

| Node | sz | mn | mx | Valid check |
| --- | --- | --- | --- | --- |
| 1 | 5 | 1 | 5 | YES |
| 3 | 3 | 2 | 5 | NO |
| 4 | 1 | 5 | 5 | NO |
| 5 | 1 | 4 | 4 | NO |

Only the full tree rooted at 1 satisfies the condition because only it contains values 1 through 5. Subtree 3 fails because its values are not normalized to 1..3.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(N) | Each node and edge is visited once during DFS, and all operations inside are constant time |
| Space | O(N) | Adjacency list plus recursion stack and per-node arrays |

The linear traversal fits comfortably within the constraints of up to 200,000 nodes, and memory usage remains proportional to the input size.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from contextlib import redirect_stdout
    out = io.StringIO()
    with redirect_stdout(out):
        solve()
    return out.getvalue().strip()

# sample 1
assert run("""4
4 2 1 3
2 1
3 2
4 1
""") == """YES
YES
YES
NO"""

# single node
assert run("""1
1
""") == "YES"

# chain
assert run("""3
1 2 3
1 2
2 3
""") == """YES
YES
YES"""

# invalid subtree
assert run("""3
2 1 3
1 2
1 3
""") == """YES
YES
NO"""

# reversed order
assert run("""4
2 1 4 3
1 2
1 3
3 4
""") == """YES
YES
NO
NO"""
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single node | YES | smallest subtree correctness |
| chain | all YES | linear structure propagation |
| invalid subtree | mixed | non-consecutive values |
| reversed order | partial NO | subtree gap detection |

## Edge Cases

A single node tree is the simplest scenario. The DFS initializes sz to 1, mn and mx to the node value. Since the condition checks mn equals 1 and mx equals sz, only node labeled 1 passes. The provided implementation correctly handles this because both initialization and check occur within the same recursion frame.

A chain-shaped tree stresses recursion depth. Each node becomes a deep recursive call, but since the parent pointer prevents revisiting, each node is still processed exactly once. The algorithm remains linear, and correctness is preserved because subtree aggregation does not depend on traversal order beyond postorder structure.

Cases where values are not aligned with subtree sizes demonstrate the core logic. For instance, a subtree of size 3 containing values {2, 3, 4} produces mn = 2 and mx = 4. Even though mx - mn + 1 equals 3, mn is not 1, so the condition correctly rejects it, preventing false positives from interval-based reasoning alone.
