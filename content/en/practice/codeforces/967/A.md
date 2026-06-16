---
title: "CF 967A - Mind the Gap"
description: "We are given a timeline of scheduled landings, each occupying exactly one minute, already sorted in increasing order. We must insert one additional event, a takeoff that also lasts one minute, into this timeline. The key restriction is safety spacing."
date: "2026-06-17T01:36:09+07:00"
tags: ["codeforces", "competitive-programming", "implementation"]
categories: ["algorithms"]
codeforces_contest: 967
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 477 (rated, Div. 2, based on VK Cup 2018 Round 3)"
rating: 1100
weight: 967
solve_time_s: 27
verified: false
draft: false
---

[CF 967A - Mind the Gap](https://codeforces.com/problemset/problem/967/A)

**Rating:** 1100  
**Tags:** implementation  
**Solve time:** 27s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a timeline of scheduled landings, each occupying exactly one minute, already sorted in increasing order. We must insert one additional event, a takeoff that also lasts one minute, into this timeline.

The key restriction is safety spacing. If a landing occurs at time t, then the takeoff must not occur in any minute from t − s through t + s inclusive. Since both events last one minute, this creates a blocked interval around every landing where no takeoff can start.

The task is to find the earliest possible starting time for the takeoff that does not violate these forbidden zones. Time is measured from 00:00 at day zero, and we may need to go beyond 24 hours if necessary.

The constraints are small: at most 100 landings and a safety margin up to 60 minutes. This immediately rules out any need for advanced data structures or optimization beyond a single linear scan or simulation. Even a direct check of candidate times would be feasible because time only advances through a small number of relevant intervals.

A few edge cases matter.

One is when there is a large gap early, for example a first landing at 00:00 and s = 60. A naive idea that only checks between landings might miss the fact that time before the first landing is also constrained by its safety window.

Another is when landings are so close that their forbidden zones overlap. For example, if one landing is at 1:00 and another at 1:30 with s = 60, their forbidden intervals merge into a continuous blocked region, and a correct solution must treat this as a single constraint rather than two independent gaps.

Finally, the answer might be after the last landing, possibly far beyond the original day boundary, so restricting the search to 24 hours would be incorrect.

## Approaches

A brute-force approach would simulate every possible minute starting from time zero onward. For each candidate time t, we check whether placing a one-minute interval starting at t conflicts with any landing. A conflict occurs if |t − li| ≤ s for any landing time li.

This is correct because it directly enforces the safety condition. However, in the worst case, we may need to scan far into the future until we find a valid slot. If landings span up to 24 hours and the gap is large, we could end up checking on the order of tens of thousands of minutes, and each check scans up to n landings, giving roughly O(T·n), which is unnecessary.

The key observation is that we do not need to consider every minute individually. The only times that matter are those near landings. Between two consecutive landings, the only relevant question is whether the gap between their forbidden intervals is large enough to fit the takeoff. Instead of testing every minute, we can “jump” from one forbidden region to the next by tracking the earliest time we are allowed to start.

We process landings in order, maintaining the earliest valid time we can place the takeoff so far. For each landing, we ensure that our candidate time is not inside its forbidden interval; if it is, we push it forward to the end of that interval. This turns the problem into a single linear sweep.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(T · n) | O(1) | Too slow |
| Optimal | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

We convert all times into minutes from the start. This simplifies comparisons and avoids dealing with hour-minute boundary cases repeatedly.

1. Convert each landing time into total minutes from time zero. This allows direct arithmetic comparisons with the safety margin.
2. Initialize a variable current_time = 0. This represents the earliest ti_
