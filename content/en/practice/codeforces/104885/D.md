---
title: "CF 104885D - \u0412\u0440\u0435\u043c\u044f \u043d\u0430 \u043c\u0430\u0440\u0441\u0435"
description: "We are given a time interval on a clock, written in hours and minutes, from a starting moment H1:M1 to an ending moment H2:M2."
date: "2026-06-28T09:08:19+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104885
codeforces_index: "D"
codeforces_contest_name: "Municipal stage of ROI in Nizhny Novgorod 2023"
rating: 0
weight: 104885
solve_time_s: 23
verified: false
draft: false
---

[CF 104885D - \u0412\u0440\u0435\u043c\u044f \u043d\u0430 \u043c\u0430\u0440\u0441\u0435](https://codeforces.com/problemset/problem/104885/D)

**Rating:** -  
**Tags:** -  
**Solve time:** 23s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a time interval on a clock, written in hours and minutes, from a starting moment `H1:M1` to an ending moment `H2:M2`. We move forward in time minute by minute, and for every intermediate time `h:m` we build a string by concatenating the decimal representation of `h` and `m` without separators. For example, `7:05` becomes the string `"705"`, while `12:30` becomes `"1230"`.

For each such string, a fixed rule from the statement assigns a “display cost”, which corresponds to how many display elements (think segments on a digital display) are needed to show all digits of that string. The task is to compute the maximum display cost over all minutes in the given interval.

The key input is therefore not a graph or array, but a continuous sequence of times. The output is a single integer: the worst-case display requirement during the interval.

Even without heavy constraints
