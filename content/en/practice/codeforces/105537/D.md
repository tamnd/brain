---
title: "CF 105537D - Defective Script"
description: "We are given a circular network of servers, each holding a non-negative load. The system provides an operation that is supposed to reduce load locally, but it is slightly broken: when applied to a server, it reduces that server by two units and also reduces its previous neighbor…"
date: "2026-06-27T00:58:43+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105537
codeforces_index: "D"
codeforces_contest_name: "2024-2025 ICPC NERC (NEERC), North-Western Russia Regional Contest (Northern Subregionals)"
rating: 0
weight: 105537
solve_time_s: 25
verified: false
draft: false
---

[CF 105537D - Defective Script](https://codeforces.com/problemset/problem/105537/D)

**Rating:** -  
**Tags:** -  
**Solve time:** 25s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a circular network of servers, each holding a non-negative load. The system provides an operation that is supposed to reduce load locally, but it is slightly broken: when applied to a server, it reduces that server by two units and also reduces its previous neighbor in the ring by one unit. We can apply this operation any number of times on any servers, and we are allowed to overuse it even when loads become small, effectively allowing values to drop to zero but not below.

The goal is not to reach an arbitrary configuration, but to make all servers end with the same load, while maximizing that common final value. So we are not minimizing operations, but rather asking for the largest achievable uniform level that can be enforced through these coupled decrements.

The constraints allow up to 2×10^5 total servers across test cases, so any solution must be close to linear per test case. Anything quadratic over n is immediately impossible, and even n log n needs careful design since the total input size is large across tests.

A naive approach would try to simulate all possible sequences of operations, tracking how each operation propagates reductions around the cycle. That fails because each operation affects two positions in a structured way, so the number of states grows exponentially. Even attempting to greedily reduce toward a target value would require repeated global checks of feasibility, which would push complexity toward O(n^2) or worse.

A more subtle issue appears when reasoning locally. For example, suppose we try to decide feasibility of a target value x by independently checking whether each server can be reduced down to x using available operations. This breaks because operations are not local: applying the script at i simultaneously changes i and i−1, so decisions at adjacent positions are coupled. A simple counterexample is a small ring like 3 servers with loads [3, 0, 0], where greedy local reductions on each node independently suggest feasibility of x = 1, but any actual sequence of operations propagates reductions in a way that forces one node to drop too far.

## Approaches

The key to this problem is to stop thinking in terms of individual operations and instead model their cumulative effect.

Each time we apply the script at position i, we reduce a pair of coordinates: a[i] decreases by 2 and a[i−1] decreases by 1. If we let x_i denote how many times we apply the script at i, then the total reduction on position i is determined by x_i and x_{i+1} because i is affected by its own operations and the next node’s operations. Concretely, server i loses 2x_i from its own operations and 1x_{i+1} from the next server in the ring.

This transforms the problem into finding non-negative integers x_i such that after applying these linear constraints, all final values become equal. Instead of simulating operations, we are solving a system of linear equations with inequality constraints.

The critical observation is that once we fix a candidate final value k, the values x_i are not arbitrary. If we re_
