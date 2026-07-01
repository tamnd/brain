---
title: "CF 104274A - \u0420\u0443\u0434\u043e\u043b\u044c\u0444 \u0438 \u0430\u0440\u0435\u043d\u0434\u0430"
description: "Rudolf spends up to one million days on a foreign planet, and the entire timeline is treated as a single continuous calendar starting from day one. The key complication is that two independent schedules overlap. The first schedule is monthly rent."
date: "2026-07-01T21:17:15+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104274
codeforces_index: "A"
codeforces_contest_name: "2023 VIII \u0418\u043d\u0442\u0435\u043b\u043b\u0435\u043a\u0442\u0443\u0430\u043b\u044c\u043d\u0430\u044f \u043e\u043b\u0438\u043c\u043f\u0438\u0430\u0434\u0430 \u041f\u0424\u041e"
rating: 0
weight: 104274
solve_time_s: 33
verified: false
draft: false
---

[CF 104274A - \u0420\u0443\u0434\u043e\u043b\u044c\u0444 \u0438 \u0430\u0440\u0435\u043d\u0434\u0430](https://codeforces.com/problemset/problem/104274/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 33s  
**Verified:** no  

## Solution
## Problem Understanding

Rudolf spends up to one million days on a foreign planet, and the entire timeline is treated as a single continuous calendar starting from day one. The key complication is that two independent schedules overlap.

The first schedule is monthly rent. Time is split into repeating blocks of length $M$ days. In each month, payment is only allowed during the last $H$ days of that month. Since months repeat periodically, the set of valid payment days is every day whose position within its month lies in the interval from $M - H + 1$ to $M$. However, payment is only possible if Rudolf is physically present on the planet that day.

The second schedule is Rudolf’s presence. He repeatedly arrives in cycles: he stays for $A$ consecutive days, then is absent for $B-A$ days, and the pattern repeats. The first stay starts on day $C$. Outside these intervals, he cannot perform any actions on the planet.

Finally, there is a set of $N$ forbidden days when Rudolf is busy and cannot pay even if both conditions above allow it. If a month passes and no valid payment day occurred while he was present and available, Rudolf is evicted on the first day of the next month.

The task is to determine the exact day of eviction, or to confirm that he survives all $10^6$ days.

The constraints imply that the timeline is large in absolute value but all structured components are small. The number of busy days is up to $10^5$, which allows linear scanning or binary search-based skipping but makes any per-day simulation potentially borderline if implemented with heavy operations. The periodic structure of both the month system and presence schedule suggests that an efficient solution should avoid iterating day-by-day over the full range without jumps.

A subtle issue appears around boundaries of months. Payment is tied to the last $H$ days, so a naive approach that only checks “month end” without verifying actual overlap with presence intervals can miss valid payment opportunities. Another failure mode comes from assuming that busy days only block a single month decision; in reality they may systematically remove all valid payment days in a month, forcing eviction exactly at the boundary.

Edge cases that frequently break naive implementations include months where Rudolf is present only outside the payment window, months where he is present inside but all valid days are busy, and cases where his presence interval overlaps two months but only partially intersects the payment window.

## Approaches

A brute-force interpretation would simulate every day up to $10^6$, track whether Rudolf is present, whether the day lies in a payment window, and whether it is not blocked by a busy day. We would maintain a pointer over busy days and a pointer over presence intervals, and for each month we would scan all days, checking if at least one valid payment opportunity exists. This is correct because it directly models the rules, but its cost becomes significant: one million iterations, each potentially doing multiple checks and boundary computations, leads to a large constant-factor solution that is acceptable only if carefully optimized.
