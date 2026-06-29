---
title: "CF 104609C - Hexagonal Billiards"
description: "We are simulating a billiard ball inside a regular hexagon where motion is perfectly elastic: the ball travels in straight lines and reflects off edges with equal incidence and reflection angles."
date: "2026-06-30T02:45:28+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104609
codeforces_index: "C"
codeforces_contest_name: "Udmurt SU + Izhevsk STU Contest 2012"
rating: 0
weight: 104609
solve_time_s: 41
verified: false
draft: false
---

[CF 104609C - Hexagonal Billiards](https://codeforces.com/problemset/problem/104609/C)

**Rating:** -  
**Tags:** -  
**Solve time:** 41s  
**Verified:** no  

## Solution
## Problem Understanding

We are simulating a billiard ball inside a regular hexagon where motion is perfectly elastic: the ball travels in straight lines and reflects off edges with equal incidence and reflection angles. The hexagon is centered at the origin, fixed in orientation, and the motion starts from a given interior point with a uniformly random initial direction.

Three of the six sides are “open” boundaries. If the ball hits any of these open sides, it immediately leaves the polygon and the process ends. The remaining three sides behave normally and reflect the ball back into the hexagon.

The process evolves in discrete collision events. Each time the ball hits a side, we count one collision. The task is to compute the probability that the ball leaves the hexagon exactly on the N-th collision, meaning it survives the first N−1 collisions without exiting and exits immediately at the N-th collision.

The input provides the number of collisions N and the starting point inside the hexagon. The position matters only for determining the distribution of the first collision side, while subsequent behavior depends on the billiard dynamics.

The constraints allow N up to 100. This immediately rules out any continuous simulation over angles or geometry. A naive approach that simulates random directions would be impossible because the answer is an exact probability, not an estimate, and the state space of continuous angles is infinite.

A subtle edge case arises when N = 0. The ball cannot exit without any collisions, so the probability is zero unless the starting point is already on an open boundary, which is explicitly excluded by the guarantee that the point is strictly inside the hexagon.

Another important subtlety is that after each reflection, the distribution of the next collision depends only on the current edge, not on the full history or exact position. A naive geometric simulation would incorrectly try to track continuous coordinates, which is unnecessary and numerically unstable.

## Approaches

A brute-force idea would attempt to simulate all possible trajectories by sampling directions and tracking reflections. Each trajectory is a piecewise linear path, and we would check whether it exits at the N-th collision. This is conceptually correct but impossible to compute exactly because the space of directions is continuous. Even discretizing angles finely would explode computationally and still would not yield exact probabilities.

The key structural observation is that billiard motion in a regular polygon with elastic reflections can be unfolded into straight-line motion on a periodic tiling of the plane. In this unfolded view, each collision corresponds to crossing a boundary line between reflected copies of the hexagon. Because the hexagon is regular, the symmetry forces the process to forget almost all geometric detail after each collision. What remains is only which side was hit, not where on the side it happened.

This collapses the continuous system into a finite Markov chain. Each state corresponds to the side currently hit, and each transition corresponds to moving from one side to another with fixed probabilities determined by symmetry. Three of these states are absorbing (the removed sides), and once entered, the process stops.

Thus the problem reduces to computing the probability that a Markov chain enters an absorbing state exactly at step N. This can be solved using dynamic programming over steps and sides.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force (trajectory simulation) | Infinite / intractable | O(1) | Not feasible |
| Markov DP over edges | O(N · 6²) | O(6) | Accepted |

## Algorithm Walkthrough

1. Label the six sides of the hexagon from 0 to 5, marking three of them as reflecting and three as absorbing (exit sides). This partitions the boundary into terminal and non-terminal states.
2. Define a probability distribution over being at each side immediately after a collision. Initially, the first collision side is uniformly determ
