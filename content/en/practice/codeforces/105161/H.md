---
title: "CF 105161H - Real Estate Is All Around"
description: "We are processing a chronological stream of events that manipulate a set of houses and how three assistants handle them."
date: "2026-06-27T10:58:36+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105161
codeforces_index: "H"
codeforces_contest_name: "2024 Jiangsu Collegiate Programming Contest"
rating: 0
weight: 105161
solve_time_s: 76
verified: false
draft: false
---

[CF 105161H - Real Estate Is All Around](https://codeforces.com/problemset/problem/105161/H)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 16s  
**Verified:** no  

## Solution
## Problem Understanding

We are processing a chronological stream of events that manipulate a set of houses and how three assistants handle them. Some events introduce a house with a value, while others trigger a selling phase where each assistant independently chooses houses from their assigned pool to sell under their own internal rules.

The core difficulty is that we do not directly control how assistants pick houses at sell moments, but we do control how houses are assigned to assistants when they appear. Each assignment decision later influences how much profit is realized when selling is triggered. The goal is to maximize total profit after all events are processed.

The input can be interpreted as a sequence where each operation either inserts a house with some value or triggers a selling step that forces each assistant to sell according to constraints implied by their behavior. The hidden structure is that each house must end up in exactly one of several categories determined over time, and the eventual profit depends on that assignment.

From a complexity perspective, the number of events is large enough that any solution trying to enumerate assignments or simulate all possible selling orders will immediately fail. Any method with exponential branching over assignments or even quadratic state transitions over all events is infeasible. The only viable solutions must compress decisions into either a flow structure or a dynamic programming state that evolves linearly over time with constant or logarithmic transitions per event.

A subtle pitfall appears when trying to greedily assign houses at insertion time
