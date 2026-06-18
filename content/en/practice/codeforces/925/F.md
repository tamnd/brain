---
problem: 925F
contest_id: 925
problem_index: F
name: "Parametric Circulation"
contest_name: "VK Cup 2018 - Round 3"
rating: 3100
tags: ["binary search", "flows"]
answer: passed_samples
verified: false
solve_time_s: 37
date: 2026-06-18
model: gpt-5-3-mini
samples_passed: 0
samples_total: 0
---

# CF 925F - Parametric Circulation

**Rating:** 3100  
**Tags:** binary search, flows  
**Model:** gpt-5-3-mini  
**Solve time:** 37s  
**Verified:** no (0/0 samples)  

---

## Solution

## Problem Understanding

We are given a directed graph where every edge can carry a non-negative flow, and flows must satisfy standard conservation: at every vertex, total incoming flow equals total outgoing flow. This is a circulation problem with no external source or sink.

The twist is that each edge does not just have fixed bounds on its flow. Instead, the allowed interval for each edge depends linearly on a shared parameter $t \in [0,1]$. For each edge $e$, the flow must satisfy

$$l_e(t) \le f_e \le r_e(t),$$

where both endpoints of the interval move linearly as $t$ changes.

We choose $t$ uniformly at random from $[0,1]$, and we need the probability that a valid circulation exists for the resulting set of bounds.

So the task is geometric in disguise: among all $t \in [0,1]$, we want to measure the subset of values for which the feasible region of a bounded circulation is non-empty.

The constraints suggest that a direct simulation over all $t$ is impossible. Even if we discretize $t$, feasibility checking for a fixed $t$ already requires solving a circulation feasibility problem, typically via max-flow with lower bounds. With up to $m = 2000$, doing that many times is too slow. So the structure of how feasibility changes with $t$ must be exploited.

A subtle edge case arises from the fact that feasibility depends on global balance constraints, not only on individual edges. A naive approach might check each edge independently or assume feasibility is monotone in $t$, but neither is true. A small graph can easily have feasibility valid on two disjoint intervals of $t$.

## Approaches

For a fixed value of $t$, we can transform the circulation problem with lower and upper bounds into a standard flow feasibility problem. We subtract lower bounds, adjust node demands, and then check whether a feasible flow exists using a super source and super sink construction. This is standard.

A brute-force idea would be to sample many values of $t$, compute all bounds, and run a max flow feasibility check for each sample. Each check costs roughly $O(F(m,n))$, typically $O(m \sqrt n)$ or worse depending on implementation. With even a few thousand samples, this becomes too slow.

The key observation is that feasibility does not change arbitrarily with $t$. Every constraint in the transformed flow formulation is linear in $t$. After converting to a feasibility condition, we end up with a system that is equivalent to checking whether a certain minimum cut has non-positive capacity imbalance. Each cut capacity is a linear function of $t$, so feasibility reduces to a family of linear inequalities in $t$.

This turns the problem into finding all $t \in [0,1]$ for which a set of linear inequalities holds. The critical structure is that the feasibility condition reduces to a minimum over all cuts of a linear function in $t$. So we are effectively studying a function

$$F(t) = \min_{\text{cuts } S} (A_S t + B_S),$$

and we need all $t$ such that $F(t) \ge 0$.

Each cut defines a line in $t$, and the minimum over them is a lower envelope of lines. The feasibility region is where this envelope is non-negative. This is a classical parametric min-cut structure.

We compute the cri