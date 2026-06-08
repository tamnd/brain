---
title: "CF 1920C - Partitioning the Array"
description: "This is a Type B problem, a proof of existence. The requirement is to show that for any placement of 650 points in a disk of radius 16, there exists at least one annulus of inner radius 2 and outer radius 3 containing at least 10 points."
date: "2026-06-08T19:27:16+07:00"
tags: ["codeforces", "competitive-programming", "brute-force", "math", "number-theory"]
categories: ["algorithms"]
codeforces_contest: 1920
codeforces_index: "C"
codeforces_contest_name: "Codeforces Round 919 (Div. 2)"
rating: 1600
weight: 1920
solve_time_s: 48
verified: false
draft: false
---

[CF 1920C - Partitioning the Array](https://codeforces.com/problemset/problem/1920/C)

**Rating:** 1600  
**Tags:** brute force, math, number theory  
**Solve time:** 48s  
**Verified:** no  

## Solution
## Problem-Type Check

This is a **Type B problem**, a proof of existence. The requirement is to show that for **any placement** of 650 points in a disk of radius 16, there exists **at least one annulus** of inner radius 2 and outer radius 3 containing at least 10 points. The proposed solution attempts to establish this using a universal lower bound on the area of admissible centers, summed over all points, and an averaging argument. The approach is consistent with the requirements of a Type B problem.

## Step-by-Step Verification

**Step 1: Define admissible-center regions - VALID**

The claim that for a fixed point $P$, the set $S(P)$ of centers $O$ with $2\le |OP|\le 3$ is a circular annulus of area $5\pi$ is correct. The computation $\pi(3^2-2^2)=5\pi$ is exact. This step is fully justified.

**Step 2: Restrict centers to a smaller disk - UNJUSTIFIED (Justification gap)**

The solution defines $D_{13}$ and claims that at least half of each annulus $S(P_i)$ lies inside $D_{13}$ because the annulus has width $1$ and the distance from $P_i$ to the boundary of $D_{13}$ is at most $3$. This is a heuristic geometric argument; it **does not rigorously guarantee** that $\operatorname{area}(S_{13}(P_i))\ge 5\pi/2$ for all positions of $P_i$. For example, if $P_i$ lies near the edge of $D_{16}$ opposite the origin, a substantial portion of the annulus could lie outside $D_{13}$ and the fraction of area inside $D_{13}$ could be less than $1/2$. This is a **justification gap**, not a critical error: the conclusion is likely correct, but the argument is insufficiently rigorous. A precise lower bound would require computing the minimal intersection of a circle of radius 3 with a disk of radius 13, which is omitted.

**Step 3: Double-count incidences - VALID**

The integral identity

$\int_{D_{13}} N(O)\, dO = \sum_{i=1}^{650} \operatorname{area}(S_{13}(P_i))$

correctly counts the measure of incidences $(O,P_i)$. This step is standard and fully justified once Step 2 is assumed.

**Step 4: Apply the lower bound - UNJUSTIFIED (Justification gap)**

The argument relies on the claimed bound $\operatorname{area}(S_{13}(P_i)) \ge 5\pi/2$. Since Step 2 does not rigorously justify this bound, the averaging argument that $\int N(O),dO \ge 650 \cdot 5\pi/2$ is unproven. This is a **justification gap**, not a critical error: the averaging argument would work if the bound were valid.

## Completeness Check

The proposed solution correctly sets up the framework for a universal existence argument using double-counting and averaging. All points are considered, and the final conclusion follows if the area lower bound holds. The **only unhandled or unjustified part** is the precise geometric estimate that guarantees at least half the area of each annulus lies inside $D_{13}$. There are no other missing cases.

## Summary

The solution correctly identifies the structure of the argument and applies double-counting and averaging properly. The **primary flaw** is the lack of a fully rigorous justification for the lower bound on the area of $S_{13}(P_i)$. The claim that at least half the annulus lies inside the smaller disk is presented as a heuristic geometric estimate rather than a precise computation. This gap leaves the argument logically incomplete, even though the conclusion is almost certainly correct.

VERDICT: FAIL - the solution lacks a rigorous proof that at least half of each point's admissible annulus lies inside the radius-13 disk.
