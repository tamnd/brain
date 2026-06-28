---
title: "CF 104842H - Hungry Cannibals"
description: "We are given a group of people trying to cross a river using a very small boat. There are two types of people: cannibals and missionaries."
date: "2026-06-28T11:32:47+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104842
codeforces_index: "H"
codeforces_contest_name: "2020-2021 ICPC, Moscow Subregional"
rating: 0
weight: 104842
solve_time_s: 21
verified: false
draft: false
---

[CF 104842H - Hungry Cannibals](https://codeforces.com/problemset/problem/104842/H)

**Rating:** -  
**Tags:** -  
**Solve time:** 21s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a group of people trying to cross a river using a very small boat. There are two types of people: cannibals and missionaries. The boat can carry at most two passengers per trip, but it cannot move unless at least one of the passengers is capable of operating the paddle. Only a subset of cannibals and a subset of missionaries have this ability.

The safety constraint is the classical predator-prey rule applied on each river bank independently. At any moment, if a bank contains at least one missionary, then the number of cannibals on that same bank must not exceed the number of missionaries. If there are no missionaries on a bank, cannibals can be present freely without causing danger.

The task is to determine whether it is possible to move everyone from the starting bank to the opposite bank using a sequence of valid boat trips, while never violating the safety constraint on either bank.

Each test case gives the number of cannibals and missionaries, along with how many in each group can operate the boat.

The constraints allow up to 1000 test cases, with each group size up to 1000. This immediately suggests that any simulation of states must be extremely compact. A naive state graph over all distributions of people between banks would already be large, but more importantly, the boat constraint adds directionality and skill constraints, making full BFS over configurations too expensive if done carelessly per state without structure.

The key edge cases come from situations where movement is impossible due to lack of paddlers or forced unsafe intermediate configurations. For example, if no one can operate the boat, even a single person cannot be moved, so any non-empty initial configuration with both banks involved becomes impossible unless everyone is already on one side. Another subtle case is when missionaries are present but always outnumbered on some side after a transfer, which can happen even if total counts seem balanced.

A concrete failing scenario is:

Inp
