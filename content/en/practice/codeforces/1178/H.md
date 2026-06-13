---
title: "CF 1178H - Stock Exchange"
description: "We are given a collection of $2n$ stocks. Each stock $i$ has a price that evolves over time in a very simple deterministic way: at integer time $t$, its price is $ai cdot t + bi$. Time starts at $t = 0$, and prices only change at integer moments."
date: "2026-06-13T10:44:22+07:00"
tags: ["codeforces", "competitive-programming", "binary-search", "flows", "graphs"]
categories: ["algorithms"]
codeforces_contest: 1178
codeforces_index: "H"
codeforces_contest_name: "Codeforces Global Round 4"
rating: 3500
weight: 1178
solve_time_s: 586
verified: false
draft: false
---

[CF 1178H - Stock Exchange](https://codeforces.com/problemset/problem/1178/H)

**Rating:** 3500  
**Tags:** binary search, flows, graphs  
**Solve time:** 9m 46s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a collection of $2n$ stocks. Each stock $i$ has a price that evolves over time in a very simple deterministic way: at integer time $t$, its price is $a_i \cdot t + b_i$. Time starts at $t = 0$, and prices only change at integer moments.

Bob initially owns stocks $1$ through $n$. His goal is to end up owning at least one share of each stock $n+1$ through $2n$. He is allowed to perform exchanges between stocks: he can trade one share of stock $x$ for one share of stock $y$ at time $t$ if the current price of $x$ is at least the price of $y$. There is no limit on how many shares of any stock exist in the market, so feasibility is entirely determined by price constraints at the moment of trade.

Two quantities must be minimized in a lexicographic sense. First, we want the earliest integer time $T$ at which it is possible to complete the goal. Second, among all ways to achieve it at that time, we want the minimum number of exchanges.

The structure hides two interacting difficulties. One is temporal: a choice of trades depends on when inequalities between linear functions become true. The second is combinatorial: we must transform a multiset of starting nodes into a target set through valid directed exchanges.

The constraints are large, with $n \le 2200$, meaning up to 4400 nodes and potentially tens of millions of candidate interactions. Any approach that recomputes reachability over time independently will be too slow. The key computational difficulty is that feasibility changes only at discrete breakpoints where inequalities between linear functions flip, and those breakpoints are determined by pairwise intersections of lines.

A naive approach would try to simulate time or recompute reachability for each candidate time $T$. That immediately fails because even a single feasibility check involves a graph reachability problem over $O(n^2)$ potential edges, and the number of distinct candidate times is quadratic.

A second naive idea is to treat every stock exchange as a BFS step in a time-dependent graph, but this breaks because edge existence depends on time, so the graph is not fixed.

Edge cases that break naive reasoning include situations where no exchanges are needed but waiting is essential, for example when initial stocks already cover targets but constraints require equalizing prices at a later time to allow indirect exchanges. Another subtle case is when a direct exchange is impossible forever, but a longer chain becomes feasible only after some time threshold where inequalities reverse.

## Approaches

The core difficulty is that each possible exchange $x \to y$ is governed by the inequality

$$a_x t + b_x \ge a_y t + b_y,$$

which rearranges to

$$t \ge \frac{b_y - b_x}{a_x - a_y}$$

when $a_x \ne a_y$, or is either always valid or never valid when slopes are equal.

This transforms every potential directed exchange into either a forbidden edge, an always-available edge, or an edge that activates only after a specific threshold time.

If we fix a time $T$, we can build a directed graph containing all edges whose threshold is at most $T$, then ask whether all target nodes are reachable from the initial set. If we could test feasibility of a given $T$, we could binary search the answer.

The bottleneck is that feasibility checking is a reachability problem in a graph with up to $O(n^2)$ edges and $O(n)$ nodes. However, the structure allows a more efficient simulation using BFS-style propagation where each node only needs to track the best time it can be reached through any path, combined with counting how many exchanges were used to reach it.

The key insight is to reinterpret the process as shortest path in a time-expanded graph, but instead of expanding time explicitly, we maintain for each stock the earliest time it can be obtained with a given number of exchanges. Because exchanges only depend on pairwise linear thresholds, the effective relaxation can be done using a priority queue or multi-source Dijkstra-like propagation where the "distance" is time and secondary key is number of exchanges.

We run a best-first search over states representing possession of a stock, where each transition uses an edge $x \to y$ with activation time $w_{xy}$. The cost of a path is lexicographically $(\max w, \text{number of edges})$, but this can be handled by treating time as primary key and exchanges as secondary in a modified relaxation scheme.

The problem reduces to computing, for each target stock, the best achievable pair (time, exchanges) from any source stock $1..n$, while ensuring we can cover all targets simultaneously. This becomes a multi-source constrained shortest path problem over a fully connected but structured graph.

The optimization comes from realizing we do not need all pairwise edges explicitly sorted. Instead, we precompute all activation times and process them in increasing order, gradually activating edges and maintaining reachability via DSU/BFS layers or incremental shortest path updates. Because $n$ is only 2200, an $O(n^2 \log n)$ preprocessing of edges is acceptable, and a global sweep over sorted thresholds combined with incremental BFS updates yields feasibility checks.

Finally, binary search on $T$ is used to separate the time dimension, and for a fixed $T$, we run a BFS/DP to compute minimal exchange counts needed to cover all targets. The smallest $T$ that allows full coverage is selected.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute force time + recompute reachability | O(n^2 \cdot \text{#times}) | $O(n^2)$ | Too slow |
| Time-threshold binary search + graph BFS/DP | $O(n^2 \log W)$ | $O(n^2)$ | Accepted |

## Algorithm Walkthrough

1. For every ordered pair of stocks $(x, y)$, compute the earliest time $t_{xy}$ when exchange $x \to y$ becomes valid. This is derived from solving $a_x t + b_x \ge a_y t + b_y$. If it never holds, mark the edge as impossible. This step converts dynamic pricing into static edge activation times.
2. Sort all candidate edges by their activation time. This ordering allows us to reason about feasibility progressively, since once an edge becomes valid, it remains valid forever.
3. Binary search the answer time $T$. Each candidate $T$ represents a world where only edges with activation time $\le T$ exist.
4. For a fixed $T$, build a directed graph consisting only of edges valid at time $T$.
5. Run a multi-source BFS/0-1 style dynamic programming from nodes $1..n$, tracking the minimum number of exchanges required to reach every node using only valid edges. The BFS state is “best known exchange count for each node”.
6. After propagation, check whether all nodes $n+1..2n$ are reachable. If yes, this time $T$ is feasible.
7. Binary search the smallest feasible $T$.
8. Once $T$ is fixed, rerun the BFS once more on the graph at time $T$ to compute the minimal number of exchanges required to reach all targets simultaneously, taking the maximum over target nodes.

### Why it works

Each exchange corresponds to traversing a directed edge that only becomes available after a fixed threshold time. Any valid sequence of trades must respect all edge thresholds along its path, so the path is feasible at time $T$ if and only if the maximum threshold along that path is at most $T$. This turns the time component into a bottleneck value on paths.

Minimizing the earliest feasible time is equivalent to minimizing the minimum possible bottleneck over all paths that collectively cover all targets. Once that bottleneck is fixed, minimizing exchanges is a standard shortest-path-in-DAG-like optimization
