---
title: "CF 105093A - 4 \u2666"
description: "We are given a complete record of a single execution of a classic three-switch, three-bulb deduction puzzle. Three switches A, B, and C each control exactly one of the bulbs 1, 2, and 3, but the mapping is unknown. All switches start in the off state."
date: "2026-06-27T20:48:49+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105093
codeforces_index: "A"
codeforces_contest_name: "2024 UP ACM Algolympics Final Round"
rating: 0
weight: 105093
solve_time_s: 28
verified: false
draft: false
---

[CF 105093A - 4 \u2666](https://codeforces.com/problemset/problem/105093/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 28s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a complete record of a single execution of a classic three-switch, three-bulb deduction puzzle. Three switches A, B, and C each control exactly one of the bulbs 1, 2, and 3, but the mapping is unknown. All switches start in the off state. The transcript describes two switches being turned on, waiting, one of them being turned off, and then the door is opened. After that, we observe which bulb is lit and the temperature state of exactly one other bulb.

The key point is that the physical reasoning in the puzzle fully determines the mapping. The bulb that is currently on must correspond to the switch that remained on. The bulb that is hot but off must correspond to the switch that was turned on and then turned off after some time. The bulb that is cool must correspond to the switch that was never touched.

The output is required to be a permutation of A, B, and C in the order of bulbs 1, 2, and 3, meaning we must output which switch controls bulb 1, which controls bulb 2, and which controls bulb 3.

The input size is constant: exactly seven lines. This removes any algorithmic complexity concerns; correctness depends entirely on correct parsing and deterministic reasoning.

The main non-obvious edge case is that the second observed bulb in the input is not necessarily the hot bulb. Instead, only one bulb is directly identified as ON, and the other given bulb is either HOT or COOL. A naive implementation that assumes fixed ordering of bulbs or assumes which bulb is reported as hot can misassign roles.

For example, if the input reports bulb 2 as ON and bulb 3 as COOL, then bulb 1 must be HOT implicitly, even though it is not explicitly labeled in the input. A careless solution that only uses explicitly mentioned bulbs and ignores inference of the missing state would fail.

## Approaches

A brute-force solution would try all 6 permutations of assignments from switches to bulbs. For each permutation, we would simulate the described actions: two switches turned on, one turned off, and then determine bulb states. We would then compare the resulting states with the observed output lines. Since there are only 6 permutations, this approach is trivially fast and correct. Even if extended to more switches, simulation per permutation would cost linear time in number of actions, here constant.

However, this problem does not require simulation at all. The transcript directly encodes the final classification logic used in the puzzle:

One switch is the “still ON” switch, one is the “HOT but OFF” switch, and one is the “never touched” switch. Each category maps uniquely to a bulb type: ON bulb, HOT bulb, and COOL bulb.

Thus the problem reduces to identifying three categories from the transcript and assigning them to bulbs 1, 2, and 3.

We simply parse:

the switch that is ON at the end,

the switch that was turned OFF after being on,

and the remaining switch.

Then we parse:

the bulb that is ON,

the bulb that is HOT or COOL, and infer the missing third bulb.

This gives a direct bijection between switches and bulbs.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Simulation | O(1) | O(1) | Accepted |
| Direct Deduction | O(1) | O(1) | Accepted |

## Algorithm Walkthrough

1. Parse the two “TURN ON” commands and record the two switches involved. These are the only switches that could be in the ON or recently-ON categories.
2. Parse the “TURN OFF” command. The switch mentioned here is the one that w
