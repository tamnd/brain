---
title: "CF 1148B - Born This Way"
description: "We are given two sorted timelines of flights forming a mandatory two-leg journey. A passenger first chooses a flight from A to B, spending a fixed travel time, and then immediately connects to a flight from B to C, again with a fixed travel time."
date: "2026-06-12T03:08:59+07:00"
tags: ["codeforces", "competitive-programming", "binary-search", "brute-force", "two-pointers"]
categories: ["algorithms"]
codeforces_contest: 1148
codeforces_index: "B"
codeforces_contest_name: "Codeforces Global Round 3"
rating: 1600
weight: 1148
solve_time_s: 32
verified: false
draft: false
---

[CF 1148B - Born This Way](https://codeforces.com/problemset/problem/1148/B)

**Rating:** 1600  
**Tags:** binary search, brute force, two pointers  
**Solve time:** 32s  
**Verified:** no  

## Solution
## Problem Understanding

We are given two sorted timelines of flights forming a mandatory two-leg journey. A passenger first chooses a flight from A to B, spending a fixed travel time, and then immediately connects to a flight from B to C, again with a fixed travel time. A connection is valid only if the second flight departs no earlier than the arrival time of the first leg.

We are allowed to remove up to k flights total from either segment. After removing flights, we want to make the passenger’s best possible itinerary as bad as possible, meaning we want to maximize the earliest possible arrival time at city C among all remaining valid routes. If we can destroy all valid routes using at most k removals, the answer is -1.

The key object is not just pairs of flights, but how deletions shift the best available pairing. Removing early A-to-B flights forces the passenger to take later departures. Removing early B-to-C flights forces later connections or potentially breaks feasibility entirely.

The constraints n, m up to 200000 immediately rule out any quadratic pairing strategy. Any approach that tries to test all (i, j) pairs or simulate deletions explicitly will not survive. Even O(nm) reasoning about compatibility is too large. We are forced toward an O((n + m) log (n + m)) or O(n + m) solution, typically involving binary search or two-pointer prefix reasoning.

A few failure cases arise in naive thinking.

One subtle case is assuming we always cancel the earliest flights in either list. That is wrong because sometimes removing a slightly later B flight is more valuable than removing an earlier A flight, since it blocks many possible connections.

Another case is assuming independence between the two segments. For example, picking the latest possible A-to-B flight and latest possible B-to-C flight independently fails because validity depends on the connection constraint.

A final pitfall is forgetting that after cancellations, the optimal pairing is still greedy: once A is fixed, the best B is the earliest one that is valid, not necessarily the latest remaining one.

## Approaches

The brute-force viewpoint is to try all ways of removing up to k flights, then recompute the best possible itinerary. Even if we fix a set of deletions, computing the best arrival time is linear by scanning A flights and, for each, finding the earliest valid B flight via binary search. But the number of deletion subsets is exponential in k, and k itself can be as large as 400000 in the worst case. This immediately explodes beyond feasibility.

The key observation is that we do not actually
