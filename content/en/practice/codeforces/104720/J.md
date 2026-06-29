---
title: "CF 104720J - Smoky Salmon"
description: "We are given a grid that represents a kitchen floor. Some cells are blocked, some are open, and one cell contains the chef’s starting position while another contains a refrigerator."
date: "2026-06-29T07:12:21+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104720
codeforces_index: "J"
codeforces_contest_name: "UTPC x WiCS Contest 10-06-23"
rating: 0
weight: 104720
solve_time_s: 27
verified: false
draft: false
---

[CF 104720J - Smoky Salmon](https://codeforces.com/problemset/problem/104720/J)

**Rating:** -  
**Tags:** -  
**Solve time:** 27s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a grid that represents a kitchen floor. Some cells are blocked, some are open, and one cell contains the chef’s starting position while another contains a refrigerator. The chef moves one step at a time in the four cardinal directions and must always move, never staying in place.

Every move has a base exhaustion cost of 1. However, the grid is affected by smoke that is not static. Instead, there is a second grid that repeats horizontally and shifts left by one column every time step. At each time step, every cell of the kitchen is either covered by smoke or not, depending on this shifting alignment. If the chef leaves a cell at a moment when that cell is covered by smoke, the cost of that move becomes 3 instead of 1.

The task is to compute the minimum possible total exhaustion required to travel from the starting cell to the refrigerator, taking into account that the smoke pattern evolves over time and affects the cost of leaving each cell.

The grid dimensions are at most 100 by 100, and the smoke period is at most 100 columns. This immediately suggests that any solution depending only on grid cells is insufficient, because the cost depends on time as well. A valid state must encode not only position but also time modulo the smoke period. This pushes us toward a state-space shortest path problem with at most about 100 × 100 × 100 states, which is about one million states, comfortably within limits for a Dijkstra-based solution.

A naive attempt that ignores time or assumes a fixed cost per cell would fail because the same cell can have different costs depending on when it is left.

A subtle failure case appears when the optimal route depends on waiting indirectly by taking detours. For example, consider a path where going through a shorter route forces you to leave a cell during a smoke-heavy moment, while a slightly longer detour aligns the same cell with a non-smoke moment, reducing cost. Any solution that reduces this to a static weighted grid cannot capture this interaction.

Another failure case arises if one assumes that the smoke pattern is fixed per cell. Since the pattern shifts every step, a correct solution must treat time as part of the state, otherwise identical spatial paths taken at different times would be incorrectly merged.

## Approaches

A straightforward brute-force approach is to simulate all possible paths through the grid while tracking time explicitly. At each step, we try moving in four directions and keep the current time step. The cost of each move depends on whether the current cell is under smoke at that time. This can be done with a full search over all possible paths.

However, the number of possible paths grows exponentially with path length. Even in a 100 by 100 grid, there can be an enormous number of simple paths, and the time dimension multiplies this further by up to 100 phases. This approach quickly becomes infeasible.

The key observation is that although time progresses, it only matters modulo K, since the smoke pattern repeats every K steps. This turns the problem into a shortest path problem on an expanded graph where each state is defined by a tuple (row, column, time mod K). From each state, there are at most four transitions to adjacent cells, and each transition increments time modulo K.

This structure allows us to apply Dijkstra’s algorithm because all edge weights are non-negative (either 1 or 3). The state space is at most 10^6 nodes, and edges are about four times that, which is efficient enough with a priority queue.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | Exponential in path length | O(1) extra | Too slow |
| Time-expanded Dijkstra | O(N M K log(N M K)) | O(N M K) | Accepted |

## Algorithm Walkthrough

### 1. Precompute smo
