---
title: "CF 104925H - Minimum Cost Flow\u00b2"
description: "We are given a directed graph with a designated source node and sink node. Instead of choosing a discrete set of paths or integer flows, we assign a real-valued flow to every edge, possibly negative, as long as flow conservation holds at every vertex and the net flow from source…"
date: "2026-06-28T07:54:03+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104925
codeforces_index: "H"
codeforces_contest_name: "Osijek Competitive Programming Camp, Fall 2023. Day 6: Estonian Contest (The 2nd Universal Cup. Stage 19: Estonia)"
rating: 0
weight: 104925
solve_time_s: 35
verified: true
draft: false
---

[CF 104925H - Minimum Cost Flow\u00b2](https://codeforces.com/problemset/problem/104925/H)

**Rating:** -  
**Tags:** -  
**Solve time:** 35s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a directed graph with a designated source node and sink node. Instead of choosing a discrete set of paths or integer flows, we assign a real-valued flow to every edge, possibly negative, as long as flow conservation holds at every vertex and the net flow from source to sink equals one unit.

The cost model is the key departure from classical minimum cost flow. Each edge contributes a cost equal to the square of the flow on that edge multiplied by a positive coefficient. So if an edge carries flow $f_e$, it contributes $c_e f_e^2$ to the total cost. The goal is to route exactly one unit of flow from node 1 to node n while minimizing the sum of these quadratic edge costs.

The graph has at most 100 vertices and 300 edges per test, and multiple test cases with a small combined size. The crucial implication is that anything cubic in the number of vertices is potentially acceptable, but anything involving combinatorial enumeration of flows or paths is immediately infeasible. The presence of real-valued flow and a strictly convex objective signals that the solution will come from continuous optimization, not combinatorics.

A subtle aspect is that flows are allowed to be negative, which means we are not restricted to a directed acyclic notion of routing. This turns the problem into a symmetric quadratic optimization over a linear subspace defined by flow conservation.

A naive mistake would be to think in terms of splitting the unit flow into paths and minimizing a sum over paths. That fails because splitting interacts nonlinearly with squared edge costs.

As a concrete failure case, consider a graph with two parallel edges from 1 to 2, both with cost 1. Sending all flow through one edge gives cost $1$. Splitting equally gives each edge flow $1/2$, so cost becomes $2 \cdot (1/4) = 1/2$, strictly better. Any path-based or unsplittable reasoning would incorrectly suggest cost 1 as optimal.

Another common pitfall is assuming linearity of optimal flows. If costs were linear, the solution would be a shortest path. Here, convexity pushes flow to spread across multiple routes, fundamentally changing structure.

## Approaches

The brute-force viewpoint is to treat each edge flow $f_e$ as a variable and solve a constrained quadratic program with $m$ variables and $n-1$ linear constraints. Writing it directly gives a convex quadratic minimization:

$$\min \sum c_e f_e^2 \quad \text{subject to } Af = b$$

where $A$ encodes flow conservation.

A direct numerical solution would attempt to eliminate constraints or apply generic convex solvers. However, generic Gaussian elimination on the full KKT system has size roughly $m + n$, leading to $O((n+m)^3)$ time per test. With 400 total vertices and edges across tests, this is still borderline but acceptable only if implemented carefully and reused structure is exploited.

The key observation is that the objective is diagonal in edge space, meaning there are no cross terms between edges. This makes the KKT system sparse and structured: it corresponds exactly to a weighted Laplacian system on the graph. This transforms the problem into solving a single linear system derived from Kirchhoff-type laws, where edge weights behave like resistances $1/c_e$.

Once reinterpreted physically, each edge acts like a resistor with conductance proportional to $c_e$, and we inject one unit of current from source to sink. The optimal flow is exactly the electrical current, and the minimum energy equals the effective resistance between nodes 1 and n, expressed in a dual weighted form.

Thus the problem reduces to solving a Laplacian linear system and extracting the potential difference induced by unit injection.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Direct quadratic programming | $O((n+m)^3)$ | $O(n^2)$ | Too slow |
| Laplacian / linear system reduction | $O(n^3)$ per test | $O(n^2)$ | Accepted |

## Algorithm Walkthrough

We reinterpret the flow variables using node potentials. The convex quadratic objective implies that optimality satisfies first-order conditions: each edge flow is proportional to the potential difference between its endpoints.

### 1. Introduce node potentials

Assign a potential $x_u$ to each vertex. For an edge $u \to v$, optimality forces the flow to satisfy

$$f_{uv} = \frac{x_u - x_v}{2c_{uv}}.$$

This comes from minimizing $c_e f_e^2$ with respect to $f_e$ under Lagrange multipliers associated with conservation constraints.

The factor $2$ is irrelevant modulo normalization and will be absorbed later.

### 2. Substitute into conservation laws

At every vertex except source and sink, flow conservation becomes:

$$\sum_{(u,v)} \frac{x_u - x_v}{c_{uv}} = 0.$$

This is exactly a weighted Laplacian equation.

### 3. Build Laplacian system

Construct matrix $L$ where for each edge $u-v$ we add weight $w = 1/c$. Then:

- $L[u][u] += w$
- $L[v][v] += w$
- $L[u][v] -= w$
- $L[v][u] -= w$

We then fix:

$$x_n = 0$$

and enforce a unit flow injection at node 1, which becomes a right-hand side vector with $b_1 = 1$, $b_n = -1$.

### 4. Solve linear system

Solve $L' x = b$ after removing one row and column (sink is grounded). Gaussian elimination over modular arithmetic gives potentials.

### 5. Compute answer

Once potentials are known, energy equals:

$$\sum c_e f_e^2 = \sum \frac{(x_u - x_v)^2}{4c_e}.$$

Compute this directly over all edges.

### Why it works

The objective is strictly convex and constraints are linear, so KKT conditions are both necessary and sufficient. The stationarity conditions convert edge-wise quadratic penalties into linear relations between flows and node potentials. This collapses the system into a Laplacian structure, which uniquely characterizes the optimal flow. Since the Laplacian system has a unique solution once a reference node is fixed, the computed potentials correspond exactly to the global minimizer, and the resulting flow satisfies all constraints while minimizing energy.

## Python Solution

```python
import sys
input = sys.stdin.readline

MOD = 998244353

def modinv(x):
    return pow(x, MOD - 2, MOD)

def solve_case(n, edges):
    # Build Laplacian
    # We solve Lx = b with x[n-1] = 0
    size = n - 1
    L = [[0] * size for _ in range(size)]
    b = [0] * size

    def add_edge(u, v, c):
        w = 1 * modinv(c) % MOD
        if u != n:
            L[u-1][u-1] = (L[u-1][u-1] + w) % MOD
        if v != n:
            L[v-1][v-1] = (L[v-1][v-1] + w) % MOD
        if u != n and v != n:
            L[u-1][v-1] = (L[u-1][v-1] - w) % MOD
            L[v-1][u-1] = (L[v-1][u-1] - w) % MOD

    for u, v, c in edges:
        add_edge(u, v, c)

    # inject 1 unit flow at source
    b[0] = 1

    # Gaussian elimination
    for i in range(size):
        pivot = i
        for j in range(i, size):
            if L[j][i]:
                pivot = j
                break
        L[i], L[pivot] = L[pivot], L[i]
        b[i], b[pivot] = b[pivot], b[i]

        inv = modinv(L[i][i])
        for j in range(i, size):
            L[i][j] = L[i][j] * inv % MOD
        b[i] = b[i] * inv % MOD

        for j in range(size):
            if j != i and L[j][i]:
                factor = L[j][i]
                for k in range(i, size):
                    L[j][k] = (L[j][k] - factor * L[i][k]) % MOD
                b[j] = (b[j] - factor * b[i]) %*
```
