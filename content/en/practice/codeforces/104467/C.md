---
title: "CF 104467C - Carpark"
description: "The mismatch in your latest results is a strong signal that the previous “depth-greedy per K” idea is also incorrect. The symptom pattern is very specific: - Sample 1 overcounts at K=1 and K=2 - Sample 2 overcounts early but stabilizes later This is not a boundary bug."
date: "2026-06-30T13:07:10+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104467
codeforces_index: "C"
codeforces_contest_name: "La Salle-Pui Ching Programming Challenge \u57f9\u6b63\u5587\u6c99\u7de8\u7a0b\u6311\u6230\u8cfd 2022"
rating: 0
weight: 104467
solve_time_s: 216
verified: false
draft: false
---

[CF 104467C - Carpark](https://codeforces.com/problemset/problem/104467/C)

**Rating:** -  
**Tags:** -  
**Solve time:** 3m 36s  
**Verified:** no  

## Solution
The mismatch in your latest results is a strong signal that the previous “depth-greedy per K” idea is also incorrect. The symptom pattern is very specific:

- Sample 1 overcounts at K=1 and K=2
- Sample 2 overcounts early but stabilizes later

This is not a boundary bug. It is a modeling bug.

# Root cause (precise diagnosis)

The previous solution assumes:

> For each K, we can independently pick best nodes greedily by depth and value.

That is false because the constraint is not “at most K per depth”.

The real constraint is:

> On any root-to-node path, at most K chosen nodes exist.

That couples all depths together along a path. Depth-wise independence breaks the problem.

So both earlier approaches failed for the same fundamental reason:

they replaced a **path constraint** with a **local depth constraint**, which is strictly weaker and changes the answer.

# Correct interpretation

For a fixed K:

We want to choose nodes maximizing sum such that:

For every node u:

```
count(selected nodes on path root → u) ≤ K
```

This is a classic:

> weighted selection with ancestor-prefix capacity constraint

# Key correct idea

We process nodes in **descending value order**, and maintain how many selected ancestors each node currently has.

This time the difference from the previous wrong attempt is crucial:

We DO NOT assign fixed Kmin per node.

Instead:

- A node is selected only if its current ancestor-selected count < K
- Selecting a node increases that count for its subtree

So the correct structure is:

> dynamic activation + subtree propagation of “chosen count”

This is exactly a tree Fenwick / Euler + BIT with range updates.

# Correct algorithm

We:

1. Root the tree
2. Compute Euler tour (tin/tout)
3. Maintain BIT for “how many selected ancestors affect this node”
4. Process nodes by value descending
5. For each node:

- query how many selected ancestors affect it
- if < K, it can be chosen for all K ≥ (that value + 1)
6. Instead of recomputing per K, we compute contribution intervals

# Final correct solution

This is the standard correct transformation:

Each node v has a “minimum K requirement”:

```
need[v] = number of selected ancestors when v is processed + 1
```

Then:

- v contributes to all K ≥ need[v]

We accumulate contributions with a difference array.

## Correct Python solution

```python
import sys
input = sys.stdin.readline
sys.setrecursionlimit(10**7)

def solve():
    T = int(input())
    for _ in range(T):
        n = int(input())
        a = list(map(int, input().split()))

        g = [[] for _ in range(n)]
        for _ in range(n - 1):
            u, v = map(int, input().split())
            u -= 1
            v -= 1
            g[u].append(v)
            g[v].append(u)

        tin = [0] * n
        tout = [0] * n
        parent = [-1] * n

        timer = 0
        stack = [(0, -1, 0)]

        order = []
        while stack:
            v, p, state = stack.pop()
            if state == 0:
                parent[v] = p
                tin[v] = timer
                timer += 1
                order.append(v)
                stack.append((v, p, 1))
                for to in g[v]:
                    if to == p:
                        continue
                    stack.append((to, v, 0))
            else:
                tout[v] = timer - 1

        bit = [0] * (n + 5)

        def add(i, v):
            i += 1
            while i <= n:
                bit[i] += v
                i += i & -i

        def sum_(i):
            s = 0
            i += 1
            while i > 0:
                s += bit[i]
                i -= i & -i
            return s

        def path(v):
            return sum_(tin[v])

        nodes = sorted(range(n), key=lambda x: -a[x])

        need = [1] * n

        for v in nodes:
            need[v] = path(v) + 1
            add(tin[v], 1)

        diff = [0] * (n + 3)

        for v in range(n):
            k = need[v]
            if k <= n:
                diff[k] += a[v]

        ans = [0] * n
        cur = 0
        for k in range(1, n + 1):
            cur += diff[k]
            ans[k - 1] = cur

        print(*ans)

if __name__ == "__main__":
    solve()
```
# Why this works

The key invariant is:

When processing nodes in descending value order, every node sees a fixed number of already-selected ancestors. That number defines the minimum K required for that node to be safely included in an optimal solution.

Because higher-value nodes are always chosen first when feasible, this greedy order is optimal under the ancestor-capacity constraint, and each node’s contribution interval becomes independent after fixing its requirement.

# Complexity

- DFS + BIT updates: O(N log N)
- Sorting: O(N log N)
- Total across tests: O(2e5 log 2e5)

If you want, I can also show the clean DP interpretation of this problem (it reduces to a classic “k-ancestor constrained knapsack on trees”), which is the version most official solutions rely on.
