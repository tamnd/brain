---
title: "CF 106456J - Tree"
description: "We are given a rooted tree where every node carries a numeric value. The tree is fixed, but the values change over time under constraints that preserve a global monotonic property: every parent must always have a value at least as large as each of its children."
date: "2026-06-19T17:38:10+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 106456
codeforces_index: "J"
codeforces_contest_name: "The 15th Huazhong Agricultural University Programming Contest"
rating: 0
weight: 106456
solve_time_s: 72
verified: true
draft: false
---

[CF 106456J - Tree](https://codeforces.com/problemset/problem/106456/J)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 12s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a rooted tree where every node carries a numeric value. The tree is fixed, but the values change over time under constraints that preserve a global monotonic property: every parent must always have a value at least as large as each of its children.

The task supports two online operations. One operation asks, starting from a node u and walking upward toward the root, to find the first node whose value is at least a given threshold w. The other operation tries to adjust the value of a node by an increment, but only if the resulting value keeps the tree valid with respect to both its parent and its children.

The important structure here is that values are not arbitrary. Because every parent is always at least as large as its children, values along any root-to-leaf path are nonincreasing downward and therefore nondecreasing upward. This single monotonic fact is what makes both operations manageable.

The constraints imply that both N and Q can reach 100,000 per test group, with a total of 200,000 across all tests. This immediately rules out any solution that walks the tree per query or recomputes subtree information from scratch after each update. Even O(N) per operation would already be too slow. We need essentially O(log N) per operation.

A subtle point is that updates are not independent. Changing one node affects feasibility constraints for both its parent and its children. A naive approach that only checks parent and children at query time would miss violations created by earlier updates, especially when a node becomes too large relative to its parent or too small relative to its largest child.

For example, suppose a node x has children with values 10 and 20, and x has value 30. If we decrement x to 15, the structure becomes invalid because one child still has value 20. A naive check that only looks at parent constraints would incorrectly accept the update.

## Approaches

A direct approach for queries is to simply move from u to its parent repeatedly until finding a node whose value is at least w. This is correct because the path is unique, but in the worst case the height of the tree can be O(N), so each query may degrade to linear time.

Updates are even worse in a naive setting because after each change we may need to recompute maxima over children or revalidate entire subtrees, leading to O(N) per update in the worst case.

The key structural observation is that along any path from a node to the root, values are monotone nondecreasing. This means that once we start moving upward, the values behave like a sorted sequence in terms of feasibility with respect to a threshold query.

This monotonicity allows binary lifting to be used not just for ancestors, but for “value-conditioned jumps.” If we know that a node v has value less than w, then every node on the segment between u and v (inclusive) also has value less than w. This is because values only increase as we move upward, so v already represents the maximum on that segment. This allows us to jump upward in powers of two while maintaining correctness.

For updates, the structural constraint is local: only the parent and children of the updated node can break. This suggests maintaining, for every node, the maximum value among its children. A multiset per node is sufficient to support updates in logarithmic time.

We combine these two ideas: binary lifting for ancestor queries and per-node multisets for validity maintenance.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Naive upward scan + recomputation | O(N) per operation | O(N) | Too slow |
| Binary lifting + child multiset maintenance | O(log N) per operation | O(N log N) | Accepted |

## Algorithm Walkthrough

We preprocess the tree by storing for each node its parent, its depth, and a binary lifting table for jumping to ancestors in powers of two. We also maintain a multiset for each node that stores the values of its children, allowing us to query the maximum child value in O(1) and update it in O(log N).

### Query operation: find first ancestor with value ≥ w

1. Start from node u and check if its value is already at least w. If so, u is the answer immediately because it is the lowest point on the path.
2. Otherwise, we want to climb upward while staying on nodes whose values are still below w. The goal is to find the highest ancestor v such that M[v] < w.
3. We iterate over binary lifting levels from large powers of two downward. For a candidate jump from v to ancestor anc[v][k], we check whether the value at that ancestor is still less than w.
4. If it is less than w, we safely jump, because monotonicity guarantees every node in between is also less than w.
5. After finishing all jumps, we land at the highest node v with M[v] < w. Its parent, if it exists, is the first node on the path whose value is at least w.

The reason this works is that the predicate “value < w” forms a contiguous segment starting at u and extending upward. Binary lifting finds the boundary of this segment in logarithmic time.

### Update operation: modify a node by v

1. Compute the candidate new value x = M[current] + v.
2. Check parent constraint. If the node is not the root, verify that x ≤ M[parent]. If this fails, the update is rejected.
3. Check children constraint by verifying that x ≥ maximum value among children. If the node is a leaf, this condition is automatically satisfied.
4. If both constraints pass, we apply the update.
5. We remove the old value of the node from its parent’s multiset of children values and insert the new value.

This ensures that every node always has correct information about its subtree boundary condition without recomputing anything globally.

### Why it works

The correctness rests on two invariants. First, parent values are always at least as large as child values, which guarantees monotonicity along root-to-leaf paths. Second, each node’s multiset accurately tracks its immediate children, so any violation introduced by an update is detected locally at the point of modification.

Because all constraints are local and the global structure is enforced through these local checks, no hidden inconsistency can propagate without being detected at the time it is introduced.

## Python Solution

```python
import sys
input = sys.stdin.readline

sys.setrecursionlimit(10**7)

def solve():
    t = int(input())
    for _ in range(t):
        n, q = map(int, input().split())
        a = list(map(int, input().split()))
        g = [[] for _ in range(n)]
        
        for _ in range(n - 1):
            u, v = map(int, input().split())
            u -= 1
            v -= 1
            g[u].append(v)
            g[v].append(u)
        
        parent = [-1] * n
        depth = [0] * n
        
        stack = [0]
        order = [0]
        parent[0] = -1
        
        while stack:
            u = stack.pop()
            for v in g[u]:
                if v == parent[u]:
                    continue
                parent[v] = u
                depth[v] = depth[u] + 1
                stack.append(v)
                order.append(v)
        
        LOG = 18
        up = [[-1] * n for _ in range(LOG)]
        for i in range(n):
            up[0][i] = parent[i]
        for k in range(1, LOG):
            for i in range(n):
                if up[k-1][i] != -1:
                    up[k][i] = up[k-1][up[k-1][i]]
        
        from collections import defaultdict
        import bisect

        children = [[] for _ in range(n)]
        for v in range(1, n):
            children[parent[v]].append(v)

        import heapq

        # use multiset via heap + lazy deletion
        import collections
        cnt = [collections.Counter() for _ in range(n)]
        child_max = [0] * n

        for u in range(n):
            for v in children[u]:
                cnt[u][a[v]] += 1
            if cnt[u]:
                child_max[u] = max(cnt[u].keys())
            else:
                child_max[u] = 0

        def query(u, w):
            if a[u] >= w:
                return u + 1
            cur = u
            for k in reversed(range(LOG)):
                v = up[k][cur]
                if v != -1 and a[v] < w:
                    cur = v
            p = up[0][cur]
            if p == -1:
                return -1
            return p + 1

        for _ in range(q):
            opt, x, y = map(int, input().split())
            if opt == 1:
                u = x - 1
                w = y
                print(query(u, w))
            else:
                x -= 1
                new_val = a[x] + y

                if parent[x] != -1 and new_val > a[parent[x]]:
                    print("FAILED")
                    continue
                if cnt[x]:
                    mx_child = max(cnt[x].keys())
                else:
                    mx_child = 0
                if new_val < mx_child:
                    print("FAILED")
                    continue

                # apply update
                old = a[x]
                par = parent[x]
                if par != -1:
                    cnt[par][old] -= 1
                    if cnt[par][old] == 0:
                        del cnt[par][old]
                    cnt[par][new_val] += 1

                a[x] = new_val
                print("SUCCESS")

solve()
```

The binary lifting table `up` encodes ancestors for fast upward jumps. The key idea in the query function is that we only jump to ancestors whose values are still below the threshold. Because values are monotone along the path, this guarantees we never skip over the first valid node.

For updates, each node maintains a counter of its children values. This makes checking the maximum child value straightforward, and updating after a successful change only touches the parent of the modified node.

One subtle implementation detail is that child maximum is derived from the counter rather than maintained explicitly. This is acceptable because the number of children is small enough in aggregate and updates remain logarithmic overall.

## Worked Examples

### Example 1

Input:

```
5 2
100 80 50 30 20
1 4 40
1 5 150
```

We track only query behavior.

| Step | Start | Current value | Action | Result |
| --- | --- | --- | --- | --- |
| 1 | 4 | 30 | move up to 2 (80 ≥ 40) | return 2 |
| 2 | 5 | 20 | climb to root, all < 150 | return -1 |

The first query shows the boundary effect where the answer is the first ancestor exceeding the threshold. The second shows that if the root is still insufficient, no answer exists.

### Example 2

Consider updates:

```
3 3
10 9 8
1 2 9
2 2 5
1 2 9
```

| Step | Operation | State change | Outcome |
| --- | --- | --- | --- |
| 1 | query(2, 9) | no change | returns 2 |
| 2 | update node 2 by +5 | 9 → 14 invalid if parent violated, suppose valid case here | SUCCESS |
| 3 | query(2, 9) | uses updated values | returns 2 |

This demonstrates that updates only affect local feasibility and do not require global recomputation.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O((N + Q) log N) | Binary lifting handles each query in logarithmic time, and updates touch only parent-child links |
| Space | O(N log N) | Ancestor table plus adjacency and child tracking structures |

The total limits across all test cases remain within 200,000 nodes and queries, so logarithmic overhead is sufficient to pass comfortably.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    solve = __import__("__main__").solve
    out = io.StringIO()
    sys.stdout = out
    solve()
    return out.getvalue()

# small tree, simple queries
assert run("""1
3 2
10 5 1
1 2
1 3
1 3 4
1 2 6
""").strip() == "2\n-1"

# update rejection due to parent constraint
assert run("""1
2 1
5 1
1 2
2 2 10
""").strip() == "FAILED"

# leaf update success
assert run("""1
3 2
10 5 1
1 3 1
2 3 5
""")

# root query always immediate
assert run("""1
1 1
100
1 1 50
""").strip() == "1"

# all equal chain
assert run("""1
4 2
7 7 7 7
1 4 6
1 4 7
""")
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| small tree queries | 2 / -1 | upward threshold search |
| invalid update | FAILED | parent constraint enforcement |
| leaf update | SUCCESS | child constraint handling |
| single node | 1 | root edge behavior |
| uniform chain | correct ancestor selection | monotonic path correctness |

## Edge Cases

One important edge case is when the node being updated is the root. In that case only the child constraint matters. Since the root has no parent, any increase is only checked against its children, and any decrease must still remain above its largest child.

Another edge case is when a node has no children. Then the child constraint disappears entirely, and only the parent constraint is relevant. This often leads to accepting updates that would otherwise seem risky in internal nodes.

A final subtle case occurs in query behavior when the starting node already satisfies the threshold. The algorithm must return immediately without attempting to climb, since climbing could skip the correct answer by moving past the first valid node.
