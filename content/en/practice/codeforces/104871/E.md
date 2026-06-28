---
title: "CF 104871E - Equal Schedules"
description: "We are given two complete schedules that describe continuous on-call coverage over a timeline that starts at time 0. Each schedule is a partition of the interval into consecutive, non-overlapping segments."
date: "2026-06-28T10:37:24+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104871
codeforces_index: "E"
codeforces_contest_name: "2023-2024 ICPC Central Europe Regional Contest (CERC 23)"
rating: 0
weight: 104871
solve_time_s: 34
verified: false
draft: false
---

[CF 104871E - Equal Schedules](https://codeforces.com/problemset/problem/104871/E)

**Rating:** -  
**Tags:** -  
**Solve time:** 34s  
**Verified:** no  

## Solution
## Problem Understanding

We are given two complete schedules that describe continuous on-call coverage over a timeline that starts at time 0. Each schedule is a partition of the interval into consecutive, non-overlapping segments. Every segment assigns a single person to be responsible for that entire interval.

The task is to compare the total amount of time each person is on-call in the first schedule versus the second schedule. For every person who appears in at least one schedule, we compute the difference: time in the second schedule minus time in the first schedule. Only non-zero differences are reported, sorted by name.

The structure of each schedule is particularly important. Because segments are contiguous and non-overlapping, each schedule can be interpreted as a full coverage of the interval from 0 up to the final endpoint, with no gaps or overlaps. This removes any ambiguity about partial coverage or double counting.

The constraint that each schedule ends at at most 1000 means the total number of unit time changes is small. Even if we discretize time at unit resolution, a direct array-based solution is feasible because the timeline is short.

A subtle edge case occurs when a name appears only in one schedule. For example, if someone is on-call in schedule one but absent in schedule two, their difference should be negative of their full duration. Another edge case is when schedules permute assignments but keep durations identical, which should yield no output.

A naive mistake would be to treat segments independently and forget to accumulate durations per person. Another common issue is failing to reset or separate accumulation between the two schedules, which leads to mixing contributions.

## Approaches

The brute-force idea is to expand each schedule into individual time units. For every interval si to ei, we assign the person ti to all integer times in that range. We maintain two arrays, one for each schedule, mapping each time unit to a name. After expansion, we count how many times each name appears in each array.

This is correct because the schedules form a disjoint partition of time, so each unit time belongs to exactly one person. However, expanding intervals into unit time becomes inefficient if the timeline were large, since it would cost proportional to the total length of all intervals.

In this problem, the maximum endpoint is only 1000, so the brute-force expansion is already fast enough. But we can still present a cleaner optimal solution that avoids explicit expansion and directly aggregates interval lengths per person.

The key observation is that each segment already encodes a duration ei − si. We can simply add this value to the corresponding person's total. Doing this separately for the first and second schedule gives us the exact totals we need in linear time in the number of segments.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force (unit expansion) | O(T) where T ≤ 1000 | O(T + names) | Accepted |
| Interval aggregation | O(N) | O(names) | Accepted |

## Algorithm Walkthrough

1. Read the first schedule line by line and maintain a dictionary that maps each name to accumulated time. For every segment si ei ti, add ei − si to the corresponding entry.
2. Repeat the same process for the second schedule using a separate dictionary. Keeping them separate ensures we never mix contributions between schedules.
3. Build the set of all names that appear in either dictionary. This ensures we account for people who appear only in one schedule.
4. For each name, compute diff[name] = second[name] − first[name]. This directly encodes whether
