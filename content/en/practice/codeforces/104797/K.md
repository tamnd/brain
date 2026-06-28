---
title: "CF 104797K - Single-track railway"
description: "We are given a linear railway consisting of stations connected in a chain. Between each pair of neighboring stations there is a travel time. Two trains depart simultaneously: one starts at station 1 and moves right, the other starts at station n and moves left."
date: "2026-06-28T13:46:14+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104797
codeforces_index: "K"
codeforces_contest_name: "2021-2022 ICPC Central Europe Regional Contest (CERC 21)"
rating: 0
weight: 104797
solve_time_s: 23
verified: false
draft: false
---

[CF 104797K - Single-track railway](https://codeforces.com/problemset/problem/104797/K)

**Rating:** -  
**Tags:** -  
**Solve time:** 23s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a linear railway consisting of stations connected in a chain. Between each pair of neighboring stations there is a travel time. Two trains depart simultaneously: one starts at station 1 and moves right, the other starts at station n and moves left. They can only pass each other at stations, not on the tracks.

If both trains aim to meet at some station i, each train arrives at that station after accumulating the travel times along its path. The waiting time is the absolute difference between their arrival times. The goal is to choose the meeting station that minimizes this waiting time.

After each update, a single edge weight between two consecutive stations changes. For every state of the railway, including the initial one, we must output the minimum possible waiting time.

The structure is a path graph, so every meeting station i corresponds to two prefix sums: one from the left end to i, and one from the right end to i. The waiting time at i is the absolute difference between these two sums.

The constraints allow up to 200,000 stations and 200,000 updates. Any solution that recomputes prefix sums from scratch after each update would cost O(nk), which is far beyond acceptable limits. Even recomputing a single prefix array per query is already too slow.

A key edge case appears when all edge weights are identical. Then the best meeting point is the middle station, and the answer is zero or very small depending on parity. Any solution that incorrectly assumes a fixed meeting point or ignores updates to prefix balance will fail immediately under updates that shift the balance across the midpoint.

Another subtle case is when a single upd
