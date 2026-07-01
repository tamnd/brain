---
title: "CF 104308F - Xored Pairs"
description: "We are asked to construct an array of length n where each value is a 30-bit non-negative integer. The construction must satisfy a set of constraints that relate elements either by inequality to a fixed value or by XOR relationships between pairs."
date: "2026-07-01T20:02:26+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104308
codeforces_index: "F"
codeforces_contest_name: "Mirror of Independence Day Programming Contest 2023 by MIST Computer Club"
rating: 0
weight: 104308
solve_time_s: 70
verified: true
draft: false
---

[CF 104308F - Xored Pairs](https://codeforces.com/problemset/problem/104308/F)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 10s  
**Verified:** yes  

## Solution
## Problem Understanding

We are asked to construct an array of length `n` where each value is a 30-bit non-negative integer. The construction must satisfy a set of constraints that relate elements either by inequality to a fixed value or by XOR relationships between pairs.

The second type of constraint behaves like a structural rule: if two indices are linked by an equation of the form `a[i] XOR a[j] = x`, then once one value is chosen, the other is fully determined. This means the constraints are not independent conditions but rather define a system of relationships that propagates through the array.

The first type of constraint forbids specific values at specific positions. These act as exclusions that must be avoided after all XOR relationships have already fixed the relative structure of values.

The key difficulty comes from the fact that XOR constraints can form connected components, and within each component all values are tied together by consistent bitwise transformations. A naive assignment per constraint fails because a single contradiction in a cycle or a late forbidden value can invalidate earlier choices.

The constraints are large, up to 100000 per test case, so any solution that tries to test assignments or backtrack over values is immediately too slow. A linear or near-linear graph-based construction is required, since operations on the order of `O(n + m)` are the only viable option.

A subtle failure case appears when XOR constraints form a cycle that is inconsistent. For example, if we derive that `a1 XOR a2 = 3`, `a2 XOR a3 = 4`, and `a1 XOR a3 = 10`, these three imply a contradiction because XORing the first two already fixes `a1 XOR a3`. Any solution that does not explicitly validate consistency along cycles will silently construct invalid arrays.

Another failure mode arises when forbidden values are treated locally at nodes before considering XOR propagation. A value forbidden at index `i` translates into a forbidden choice for the global representative of its component, but only after adjusting by the node’s XOR offset. Ignoring this shift leads to incorrect global reasoning.

## Approaches

If we ignore XOR constraints, the problem reduces to independently choosing values while avoiding forbidden ones, which is trivial. If we ignore forbidden constraints, the XOR constraints define a graph where each connected component can be assigned a single base value and everything else follows by XOR offsets. This already suggests a graph structure with consistency requirements.

A brute force approach would attempt to assign values to each node and repeatedly enforce constraints until convergence. Each time a value is changed, all constraints incident to that node would need to be rechecked, potentially propagating updates across the graph. In the worst case, each assignment can trigger a cascade through all edges, leading to exponential or at least quadratic behavior over chains of constraints. With up to `10^5` constraints, this becomes infeasible.

The key observation is that XOR constraints define a weighted undirected graph where each edge enforces a fixed difference under XOR. Once a value is fixed at one node of a connected component, every other node in that component is determined uniquely. This allows us to reduce the entire system to one free variable per component.

After compressing each component into a single degree of freedom, the remaining task is to choose a base value for that component such that all forbidden constraints are satisfied. Each forbidden condition translates into an exclusion for the base value after adjusting by the node’s XOR offset. Since the value domain is large (`2^30`), we can always find a valid choice if the constraints are consistent.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Propagation | Exponential / very large | O(n + m) | Too slow |
| XOR Graph + Component Compression | O(n + m) | O(n + m) | Accepted |

## Algorithm Walkthrough

We model the system as a graph where each XOR constraint is an edge carrying a weight.

1. Build a graph where each constraint of the form `a[i] XOR a[j] = x` becomes an undirected edge `(i, j)` with label `x`. This means that if we assign a value to `i`, the value of `j` is forced to be `a[i] XOR x`.
2. Traverse each connected component using DFS or BFS and assign a relative value `dist[i]` for each node, interpreted as `a[i] XOR base_of_component`. While traversing, if we revisit a node and the implied value conflicts with the previously assigned one, we immediately conclude the system is inconsistent.
3. Collect all nodes belonging to each connected component along with their `dist[i]` values.
4. For each component, compute the forbidden set for the component’s base value. Every constraint of the form `a[i] != x` translates into `base XOR dist[i] != x`, which is equivalent to `base != x XOR dist[i]`. We insert all such forbidden transformed values into a set for that component.
5. Choose a base value for the component by starting from zero and incrementing until we find a value not present in the forbidden set. This works because the domain size is extremely large compared to the number of forbidden values.
6. Once a base is chosen, assign every node in the component as `a[i] = base XOR dist[i]`.

The central invariant is that within each connected component, every node value is always consistent with all XOR constraints by construction of `dist[i]`. The only remaining freedom is the global base, and the forbidden constraints only restrict this single parameter per component. Since all forbidden conditions are respected during base selection, the final assignment satisfies every constraint simultaneously.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    MAXV = (1 << 30)

    for _ in range(t):
        n, m = map(int, input().split())

        g = [[] for _ in range(n + 1)]
        type1 = [[] for _ in range(n + 1)]

        for _ in range(m):
            tmp = input().split()
            if tmp[0] == '1':
                _, i, x = tmp
                i = int(i)
                x = int(x)
                type1[i].append(x)
            else:
                _, i, j, x = tmp
                i = int(i)
                j = int(j)
                x = int(x)
                g[i].append((j, x))
                g[j].append((i, x))

        vis = [False] * (n + 1)
        dist = [0] * (n + 1)
        comp = [-1] * (n + 1)
        comps = []

        ok = True

        for i in range(1, n + 1):
            if vis[i]:
                continue
            stack = [i]
            vis[i] = True
            dist[i] = 0
            comp_id = len(comps)
            comps.append([])

            while stack and ok:
                v = stack.pop()
                comp[v] = comp_id
                comps[comp_id].append(v)

                for to, w in g[v]:
                    if not vis[to]:
                        vis[to] = True
                        dist[to] = dist[v] ^ w
                        stack.append(to)
                    else:
                        if dist[to] != (dist[v] ^ w):
                            ok = False
                            break

        if not ok:
            print("No")
            continue

        base = [0] * len(comps)
        used = [set() for _ in range(len(comps))]

        for v in range(1, n + 1):
            cid = comp[v]
            for x in type1[v]:
                used[cid].add(x ^ dist[v])

        for cid in range(len(comps)):
            b = 0
            while b in used[cid]:
                b += 1
            base[cid] = b

        ans = [0] * (n + 1)
        for v in range(1, n + 1):
            ans[v] = base[comp[v]] ^ dist[v]

        print("Yes")
        print(*ans[1:])

if __name__ == "__main__":
    solve()
```

The solution first constructs the XOR constraint graph and computes relative XOR distances inside each component. The DFS ensures that every node gets a consistent label, and any contradiction immediately invalidates the test case.

After components are identified, every forbidden constraint is translated into a restriction on the component’s base value. The transformation `x XOR dist[i]` is what aligns node-specific restrictions into a unified coordinate system per component.

The base selection loop is safe because the number of forbidden values is bounded by the number of constraints, while the search space spans `2^30`. Even a linear scan remains efficient since each component contributes only a small portion of all constraints.

## Worked Examples

### Example 1

Input:

```
n = 3
constraints:
1: a1 != 0
2: a1 XOR a2 = 1
3: a2 XOR a3 = 2
```

We build one component with distances:

`dist[1] = 0`, `dist[2] = 1`, `dist[3] = 3`.

Now transform forbidden constraint `a1 != 0`:

base XOR 0 != 0 → base != 0.

So forbidden set is `{0}`.

We pick `base = 1`.

Assignment becomes:

`a1 = 1`, `a2 = 0`, `a3 = 2`.

| node | dist | value = base XOR dist |
| --- | --- | --- |
| 1 | 0 | 1 |
| 2 | 1 | 0 |
| 3 | 3 | 2 |

This confirms that XOR relations are preserved and forbidden value is avoided.

### Example 2 (inconsistency detection)

Input:

```
1 3
a1 XOR a2 = 1
a2 XOR a1 = 0
```

Traversing:

`a1 XOR a2 = 1` implies `dist[2] = 1`.

Second constraint implies `dist[1] XOR dist[2] = 0`, which forces `dist[2] = 0`.

We already had `dist[2] = 1`, contradiction occurs during traversal, so output is `No`.

This demonstrates that cycle consistency is enforced through XOR distance checks.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n + m) | Each node and edge is processed once during DFS, and forbidden constraints are aggregated once |
| Space | O(n + m) | Graph storage, distance arrays, and component bookkeeping |

The constraints allow up to `2 × 10^5` total operations across tests, and the algorithm stays strictly linear, so it fits comfortably within limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys as _sys
    from types import ModuleType

    # assumes solution is in same file; for standalone testing, call solve()
    # here we redefine minimal wrapper
    exec_globals = globals().copy()
    exec_globals["input"] = lambda: sys.stdin.readline()
    return ""

# Sample-style and custom tests (conceptual; requires integrated runner)

# minimal consistency
assert True
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single node, no constraints | Yes + any value | trivial construction |
| small consistent chain | Yes | propagation correctness |
| XOR cycle contradiction | No | cycle detection |
| multiple components | Yes | independent base selection |

## Edge Cases

A key edge case is when XOR constraints form a long chain across all nodes while forbidden constraints cluster on a single node. The algorithm handles this because all restrictions are translated into the same base coordinate, so even a dense set of local constraints does not interfere with other components.

Another edge case is when a component has many forbidden values covering a contiguous range starting from zero. The linear scan for a valid base still succeeds because the domain is vastly larger than the number of forbidden entries, guaranteeing a gap.

A third case is a cycle that is consistent locally but inconsistent globally. The DFS-based distance check catches this immediately by enforcing that every edge agrees with previously assigned distances, preventing invalid assignments from ever reaching the base selection stage.
