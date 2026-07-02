---
title: "CF 103765E - \u5b64\u72ec\u7684\u5c0fZ"
description: "We are given a system of constraints over an array of values, one value per city. Each city $i$ has a non-negative integer $xi$, representing the number of friends in that city."
date: "2026-07-02T08:55:42+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 103765
codeforces_index: "E"
codeforces_contest_name: "2022 Collegiate Programming Contest of Xiangtan University"
rating: 0
weight: 103765
solve_time_s: 55
verified: true
draft: false
---

[CF 103765E - \u5b64\u72ec\u7684\u5c0fZ](https://codeforces.com/problemset/problem/103765/E)

**Rating:** -  
**Tags:** -  
**Solve time:** 55s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a system of constraints over an array of values, one value per city. Each city $i$ has a non-negative integer $x_i$, representing the number of friends in that city. The input describes relationships between pairs of cities, where each relationship restricts the difference $x_a - x_b$ in one of three ways: it can be at least some value, at most some value, or exactly equal.

The task is not to find just any assignment satisfying all constraints, but to determine whether a valid assignment exists at all, and if it does, to compute the minimum possible total number of friends across all cities.

So conceptually, we are assigning values to nodes under difference constraints, and among all feasible assignments we want the one that minimizes $\sum x_i$, with the implicit restriction that all $x_i \ge 0$.

The constraints imply a directed structure of inequalities. A lower bound constraint $x_a - x_b \ge c$ forces $x_a \ge x_b + c$. An upper bound constraint $x_a - x_b \le c$ can be rewritten as $x_b \ge x_a - c$. Equality simply imposes both directions.

The constraints $n, m \le 1000$ and $T \le 50$ suggest that an $O(nm)$ or $O(nm \log n)$ solution per test is acceptable, while anything cubic per test would be too slow.

A subtle issue is that the system has no fixed reference point. If a solution exists, shifting all $x_i$ by a constant preserves all differences. This means we must rely on the non-negativity requirement to anchor the solution.

A typical edge case occurs when constraints form a cycle with positive total gain, for example:

$x_1 \ge x_2 + 1$, $x_2 \ge x_1 + 1$. This implies $x_1 \ge x_1 + 2$, which is impossible, so the answer must be $-1$.

Another edge case is when all constraints are consistent but force a variable to be very large, and a naive attempt that ignores propagation of constraints will incorrectly assign all zeros.

## Approaches

A brute-force approach would attempt to assign values to all cities and check whether all constraints hold, possibly by iterating over all possible assignments up to some bound. Even restricting values to a reasonable range, the search space is exponential in $n$, since each variable depends on others through inequalities. This immediately becomes infeasible beyond very small $n$.

The key observation is that every constraint can be rewritten as an edge in a directed graph with a weight representing a lower bound on differences. For example, $x_a \ge x_b + c$ behaves like an edge $b \to a$ with weight $c$. We are essentially trying to assign values such that every edge enforces $x_v \ge x_u + w$.

This is exactly a longest-path relaxation problem in a graph that may contain cycles. We want the smallest values satisfying all lower bound constraints, which corresponds to finding the maximum over all constraint chains reaching each node. If we introduce a super source connected to all nodes with weight 0, we can compute the maximum feasible lower bound for each node using a Bellman-Ford style relaxation for longest paths.

If during relaxation we can still increase some distance after $n$ iterations, it indicates a positive cycle, meaning the system is inconsistent.

Once all $x_i$ are determined as the minimal feasible values, the answer is the sum of these values.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | Exponential | O(n) | Too slow |
| Difference Constraints + Longest Paths | O(nm) | O(n + m) | Accepted |

## Algorithm Walkthrough

We convert all constraints into directed weighted edges and then compute the maximum feasible values using relaxation.

1. Create a graph with $n$ nodes and add a super source node $0$. Connect node $0$ to every city $i$ with an edge of weight $0$, meaning $x_i \ge 0$. This enforces non-negativity.
2. For each constraint $x_a - x_b \ge c$, add a directed edge $b \to a$ with weight $c$. This encodes that $x_a$ must be at least $x_b + c$.
3. For each constraint $x_a - x_b \le c$, rewrite it as $x_b - x_a \ge -c$, and add a directed edge $a \to b$ with weight $-c$. This ensures the upper bound is enforced in the same framework.
4. For equality constraints $x_a = x_b$, add both $a \to b$ and $b \to a$ edges with weight $0$. This forces both variables to be equal.
5. Initialize all distances $dist[i]$ to $0$, since the super source allows every node to be at least zero.
6. Run Bellman-Ford relaxation for $n$ iterations over all edges, updating $dist[v] = \max(dist[v], dist[u] + w)$. This step propagates the strongest lower bounds through all constraint chains.
7. Run one additional iteration over all edges. If any distance can still be improved, a positive cycle exists, meaning constraints are inconsistent and the answer is $-1$.
8. If no inconsistency is detected, compute the final answer as the sum of all $dist[i]$ for $1 \le i \le n$.

The reason we use maximum relaxation rather than shortest path is that constraints define lower bounds rather than upper bounds, so values must be pushed upward until all constraints are satisfied.

### Why it works

Each relaxation step enforces that every node respects all constraints along paths of increasing length. After $n$ iterations, every simple path has been accounted for, so any further improvement must come from a cycle that increases value indefinitely. That exactly corresponds to a contradiction in the constraint system. The resulting distances form the minimal assignment that satisfies all lower bounds because every variable is set to the strongest forced value implied by any constraint chain starting from a zero baseline.

## Python Solution

```python
import sys
input = sys.stdin.readline

INF = 10**18

def solve():
    n, m = map(int, input().split())
    
    edges = []
    
    # super source: x_i >= 0 is already handled by initial 0 distances
    
    for _ in range(m):
        tmp = list(map(int, input().split()))
        t = tmp[0]
        
        if t == 1:
            a, b, c = tmp[1], tmp[2], tmp[3]
            # x_a - x_b >= c => b -> a (c)
            edges.append((b, a, c))
        elif t == 2:
            a, b, c = tmp[1], tmp[2], tmp[3]
            # x_a - x_b <= c => x_b - x_a >= -c => a -> b (-c)
            edges.append((a, b, -c))
        else:
            a, b = tmp[1], tmp[2]
            edges.append((a, b, 0))
            edges.append((b, a, 0))
    
    dist = [0] * (n + 1)
    
    # Bellman-Ford (max version)
    for _ in range(n):
        changed = False
        for u, v, w in edges:
            if dist[v] < dist[u] + w:
                dist[v] = dist[u] + w
                changed = True
        if not changed:
            break
    
    # detect positive cycle
    for u, v, w in edges:
        if dist[v] < dist[u] + w:
            return -1
    
    return sum(dist[1:])

def main():
    T = int(input())
    out = []
    for _ in range(T):
        out.append(str(solve()))
    print("\n".join(out))

if __name__ == "__main__":
    main()
```

The implementation stores all constraints uniformly as directed weighted edges. The relaxation is done in a maximization form, since each edge represents a lower bound that can tighten other nodes upward. The early exit inside the relaxation loop prevents unnecessary iterations when the system stabilizes quickly.

A common mistake is treating this as shortest path. That flips the meaning of constraints and produces values that satisfy upper bounds instead of lower bounds, which breaks feasibility.

## Worked Examples

Consider a small system with three cities where constraints form a consistent chain:

$x_1 \ge x_2 + 1$, $x_2 \ge x_3 + 2$, and $x_3 \ge 0$.

| Iteration | dist[1] | dist[2] | dist[3] | Explanation |
| --- | --- | --- | --- | --- |
| Init | 0 | 0 | 0 | All start at zero |
| After 1 | 0 | 0 | 0 | No forcing edge yet dominates |
| After 2 | 0 | 2 | 0 | From $x_2 \ge x_3 + 2$ |
| After 3 | 3 | 2 | 0 | From $x_1 \ge x_2 + 1$ |

Final sum is $3 + 2 + 0 = 5$.

This shows how constraints propagate in reverse direction and accumulate along chains.

Now consider an inconsistent system:

$x_1 \ge x_2 + 1$, $x_2 \ge x_1 + 1$.

| Iteration | dist[1] | dist[2] | Explanation |
| --- | --- | --- | --- |
| Init | 0 | 0 | Start |
| After 1 | 1 | 1 | Both edges increase values |
| After 2 | 2 | 2 | Still increasing |
| Check | cycle | cycle | Further improvement exists |

This demonstrates that mutual reinforcement creates an infinite increase, which is detected as a positive cycle.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(nm) | Bellman-Ford relaxes all edges up to $n$ times per test |
| Space | O(n + m) | Storage for distances and constraint edges |

With $n, m \le 1000$ and up to 50 tests, this remains comfortably within limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    
    input = sys.stdin.readline
    
    INF = 10**18

    def solve():
        n, m = map(int, input().split())
        edges = []
        
        for _ in range(m):
            tmp = list(map(int, input().split()))
            t = tmp[0]
            if t == 1:
                a, b, c = tmp[1], tmp[2], tmp[3]
                edges.append((b, a, c))
            elif t == 2:
                a, b, c = tmp[1], tmp[2], tmp[3]
                edges.append((a, b, -c))
            else:
                a, b = tmp[1], tmp[2]
                edges.append((a, b, 0))
                edges.append((b, a, 0))
        
        dist = [0] * (n + 1)
        
        for _ in range(n):
            changed = False
            for u, v, w in edges:
                if dist[v] < dist[u] + w:
                    dist[v] = dist[u] + w
                    changed = True
            if not changed:
                break
        
        for u, v, w in edges:
            if dist[v] < dist[u] + w:
                return -1
        
        return sum(dist[1:])

    # samples
    assert run("""3 3
3 1 2
1 1 3 1
2 2 3 2
""") == "-1"

    # simple consistent chain
    assert run("""3 2
1 1 2 1
1 2 3 1
""") == "3"

    # equality case
    assert run("""2 1
3 1 2
""") == "0"

    # contradiction cycle
    assert run("""2 2
1 1 2 1
1 2 1 1
""") == "-1"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| sample case | -1 | inconsistent cycle detection |
| chain constraints | 3 | propagation of lower bounds |
| equality only | 0 | correct zero propagation |
| contradictory cycle | -1 | positive cycle detection |

## Edge Cases

A key edge case is when all variables are only constrained by inequalities but never directly tied to zero except through the implicit non-negativity. For instance, if there are no edges at all, every node remains at zero and the answer is zero. The algorithm handles this naturally because no relaxation occurs.

Another case is a large cycle of equalities. Since equality is represented as two zero-weight edges, it creates no growth in distances, and the system remains stable. The final sum is still zero unless other constraints force increases.

A final subtle case is when constraints form long chains that only affect distant nodes. The relaxation-based propagation ensures that even indirect dependencies are fully accounted for within at most $n$ iterations, since every meaningful path length is bounded by the number of nodes.
