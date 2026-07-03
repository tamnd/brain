---
title: "CF 103427B - Bitwise Exclusive-OR Sequence"
description: "We are given a sequence of unknown nonnegative integers $a1, a2, dots, an$. Instead of the values themselves, we receive a set of constraints of the form that the XOR of two positions is fixed: $au oplus av = w$."
date: "2026-07-03T11:56:02+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 103427
codeforces_index: "B"
codeforces_contest_name: "The 2021 ICPC Asia Shenyang Regional Contest"
rating: 0
weight: 103427
solve_time_s: 49
verified: true
draft: false
---

[CF 103427B - Bitwise Exclusive-OR Sequence](https://codeforces.com/problemset/problem/103427/B)

**Rating:** -  
**Tags:** -  
**Solve time:** 49s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a sequence of unknown nonnegative integers $a_1, a_2, \dots, a_n$. Instead of the values themselves, we receive a set of constraints of the form that the XOR of two positions is fixed: $a_u \oplus a_v = w$.

The task is not only to decide whether such a sequence exists, but if it does, to construct one that satisfies all constraints and minimizes the total sum of all elements. The answer is this minimum possible sum, or $-1$ if the constraints contradict each other.

Each constraint behaves like a relationship between two nodes in a graph: it does not fix absolute values, but fixes the XOR difference between them. This immediately suggests that values inside a connected component are tightly coupled, while different components can be shifted independently by choosing a base value.

The constraints are large in number, up to $2 \times 10^5$, over up to $10^5$ nodes, which rules out anything quadratic or even cubic in $n$. Any solution must essentially be near-linear or near-log-linear, meaning graph traversal with some union structure or DFS is the only realistic direction.

A subtle issue arises from consistency. Consider a cycle of constraints. It is possible that the XOR equations imply contradictory values. For example, if we have:

$a_1 \oplus a_2 = 1$, $a_2 \oplus a_3 = 1$, and $a_1 \oplus a_3 = 0$, then combining the first two implies $a_1 \oplus a_3 = 0$, so this is consistent. But if the third constraint were $1$, it would immediately contradict.

Another subtle edge case is multiple constraints between the same pair of nodes. If two different XOR values are given for the same pair, the answer is immediately impossible. A naive implementation that overwrites edges without checking consistency may miss this conflict.

Finally, the objective is not just feasibility but minimization of sum. That changes the problem from a pure constraint satisfaction task into an optimization problem over each connected component.

## Approaches

A brute-force interpretation would be to assign values to all nodes and try to satisfy constraints one by one, backtracking when contradictions appear. This quickly becomes exponential because each component can propagate constraints across cycles, and every guess branches.

A more structured brute-force would try fixing $a_1 = x$ for each component and propagate constraints using BFS or DFS. This ensures consistency checking in $O(n + m)$, but still leaves the optimization problem: trying all possible base values is impossible because values are unbounded integers.

The key observation is that XOR constraints define relative differences. If we pick a root in each connected component and define $a_v$ relative to it, then every node has a fixed expression:

$$a_v = a_{root} \oplus dist[v]$$

where $dist[v]$ is the XOR accumulated along a path from the root. This reduces all constraints inside a component to a single free variable: the root value.

Now the problem becomes: for each component, choose a root value $x$ minimizing

$$\sum_v (x \oplus dist[v])$$

This is a classical bitwise optimization problem. Since XOR operates independently per bit, we can minimize each bit of $x$ separately. For each bit, we count how many nodes in the component have that bit set in $dist[v]$. If more nodes would benefit from having a 0 or a 1 at the root bit, we choose the cheaper option.

Thus each component contributes independently to the answer, and the global answer is the sum of optimal costs over components.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force (assign + backtrack / try roots) | exponential | O(n) | Too slow |
| Optimal (graph + XOR propagation + bit counting) | $O((n+m)\cdot 30)$ | O(n + m) | Accepted |

## Algorithm Walkthrough

We process each connected component separately while maintaining XOR distances from an arbitrary root.

1. Build a graph where each constraint $u \oplus v = w$ becomes an undirected edge with label $w$. This encodes that knowing one endpoint determines the other.
2. For each unvisited node, start a BFS or DFS treating it as a root and assign its XOR distance as 0. This root represents the free variable for its component.
3. During traversal, if we go from node $u$ to $v$ with constraint $w$, we set:

$$dist[v] = dist[u] \oplus w$$

If $v$ is already visited, we verify consistency by checking whether the computed value matches the existing one. If not, the system of equations contradicts itself and the answer is $-1$.
4. After finishing a component, we have fixed $dist[v]$ for all nodes in it. Now we compute the best possible choice of root value $x$ bit by bit. For each bit position $b$, we count how many nodes in the component have bit $b$ set in $dist[v]$. If we set bit $b$ of $x$ to 0, the contribution is the number of ones in that bit. If we set it to 1, the contribution is the number of zeros. We choose the smaller.
5. Sum contributions of all bits to get the optimal cost for the component, then add it to the global answer.

### Why it works

The BFS ensures that every node in a component is assigned a value consistent with all constraints along the traversal tree. Any remaining edge is checked against this assignment, so cycles cannot silently violate constraints.

Once distances are fixed relative to a root, every valid solution differs only by XORing all nodes in the component by the same constant $x$. This is because XOR constraints preserve relative differences. Therefore every feasible assignment is captured by choosing a single root value.

The cost function splits by bits because XOR does not mix bits. Each bit behaves like an independent binary decision over all nodes in the component, and minimizing total sum reduces to minimizing each bit contribution independently.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, m = map(int, input().split())
    g = [[] for _ in range(n)]
    
    for _ in range(m):
        u, v, w = map(int, input().split())
        u -= 1
        v -= 1
        g[u].append((v, w))
        g[v].append((u, w))
    
    vis = [False] * n
    dist = [0] * n
    sys.setrecursionlimit(10**7)
    
    ans = 0
    MAXB = 30
    
    for i in range(n):
        if vis[i]:
            continue
        
        stack = [i]
        vis[i] = True
        dist[i] = 0
        comp = []
        
        ok = True
        
        while stack:
            u = stack.pop()
            comp.append(u)
            for v, w in g[u]:
                if not vis[v]:
                    vis[v] = True
                    dist[v] = dist[u] ^ w
                    stack.append(v)
                else:
                    if dist[v] != (dist[u] ^ w):
                        ok = False
        
        if not ok:
            print(-1)
            return
        
        for b in range(MAXB):
            ones = 0
            for u in comp:
                if (dist[u] >> b) & 1:
                    ones += 1
            zeros = len(comp) - ones
            ans += min(ones, zeros) * (1 << b)
    
    print(ans)

if __name__ == "__main__":
    solve()
```

The graph construction encodes each XOR constraint symmetrically, ensuring traversal can propagate values in both directions. The `dist` array stores XOR distance from the chosen root in each component, and consistency checking happens immediately when a previously visited node is encountered.

The key implementation detail is that we do not try to assign actual values, only relative XOR distances. The final optimization is done after the component is fully resolved, which avoids any interaction between propagation and minimization.

The bit loop up to 30 is sufficient because constraints are bounded by $2^{30}$, so all values remain within that range.

## Worked Examples

### Example 1

Input:

```
3 2
1 2 1
2 3 1
```

We build a single component. Starting from node 1, we get:

$dist[1]=0$, $dist[2]=1$, $dist[3]=0$.

| Step | Node | dist assignment | Component |
| --- | --- | --- | --- |
| 1 | 1 | 0 | [1] |
| 2 | 2 | 1 | [1,2] |
| 3 | 3 | 0 | [1,2,3] |

For each bit, we minimize contribution. The best root choice leads to values [0,1,0] and sum is 1.

This shows how relative XOR structure fully determines all nodes once a root is fixed.

### Example 2

Input:

```
3 3
1 2 1
2 3 1
1 3 1
```

Traversal gives:

$dist[1]=0$, $dist[2]=1$, $dist[3]=0$, but the last constraint demands $dist[1] \oplus dist[3] = 1$, which evaluates to 0, so contradiction occurs.

| Edge processed | Check |
| --- | --- |
| 1-2=1 | OK |
| 2-3=1 | OK |
| 1-3=1 | mismatch |

The algorithm detects inconsistency immediately and returns -1.

This confirms cycle consistency checking prevents invalid XOR systems.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O((n+m)\cdot 30)$ | Each node and edge is processed once, and each bit is evaluated per component |
| Space | $O(n+m)$ | adjacency list plus arrays for visited state and distances |

The constraints allow up to $3 \times 10^5$ operations per bit layer, which fits comfortably within limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from __main__ import solve
    try:
        solve()
    except SystemExit:
        pass
    return ""

# provided sample 1 (feasible)
assert run("""3 2
1 2 1
2 3 1
""").strip() == "1"

# provided sample 2 (inconsistent)
assert run("""3 3
1 2 1
2 3 1
1 3 1
""").strip() == "-1"

# single node
assert run("""1 0
""").strip() == "0"

# disconnected components
assert run("""4 2
1 2 2
3 4 3
""").strip() == "5"

# immediate contradiction
assert run("""2 2
1 2 1
1 2 2
""").strip() == "-1"

# all zeros constraints
assert run("""5 4
1 2 0
2 3 0
3 4 0
4 5 0
""").strip() == "0"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single node | 0 | base case |
| disconnected components | 5 | independent component handling |
| duplicate conflicting edge | -1 | constraint consistency detection |
| all-zero constraints | 0 | trivial propagation correctness |

## Edge Cases

One edge case is when multiple edges impose conflicting constraints between the same pair of nodes. For example, if we have $1 \leftrightarrow 2$ with values 1 and 2, the BFS will reach node 2 from node 1 using the first edge and assign $dist[2]=1$. When encountering the second edge, it checks $dist[1] \oplus 2 = 2$, which does not match $dist[2]=1$, triggering immediate failure and returning -1.

Another case is a disconnected graph. Each component is processed independently, and since XOR constraints never connect components, each component contributes its own optimal root choice. The algorithm naturally resets traversal state per component, so no interference occurs.

A final subtle case is a tree-like component with no cycles. Here there is never a consistency check triggered, and all nodes receive unique XOR distances. The optimization step alone determines the minimal sum, confirming that cycle handling is not required for correctness in acyclic structures.
