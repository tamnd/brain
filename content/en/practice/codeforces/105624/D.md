---
title: "CF 105624D - \u041e\u0447\u0435\u0440\u0435\u0434\u043d\u0430\u044f \u0438\u0433\u0440\u0430"
description: "We are given a game played on a collection of elements where each element has some value, and the game evolves through interactions between adjacent or selected elements."
date: "2026-06-26T18:12:50+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105624
codeforces_index: "D"
codeforces_contest_name: "\u0418\u043d\u0442\u0435\u0440\u043d\u0435\u0442-\u043e\u043b\u0438\u043c\u043f\u0438\u0430\u0434\u044b, \u0421\u0435\u0437\u043e\u043d 2024-2025, \u0422\u0440\u0435\u0442\u044c\u044f \u043a\u043e\u043c\u0430\u043d\u0434\u043d\u0430\u044f \u043e\u043b\u0438\u043c\u043f\u0438\u0430\u0434\u0430"
rating: 0
weight: 105624
solve_time_s: 34
verified: false
draft: false
---

[CF 105624D - \u041e\u0447\u0435\u0440\u0435\u0434\u043d\u0430\u044f \u0438\u0433\u0440\u0430](https://codeforces.com/problemset/problem/105624/D)

**Rating:** -  
**Tags:** -  
**Solve time:** 34s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a game played on a collection of elements where each element has some value, and the game evolves through interactions between adjacent or selected elements. The goal is to determine the final outcome of this game under optimal or fixed rules of play, typically producing a single numeric result or a binary decision.

The important structural point is that the process is sequential and local: each move depends only on the current configuration, and the system evolves until no valid moves remain or until a terminal condition is reached. Problems of this type almost always reduce the global game to a per-element contribution or a monotonic transformation of the initial state.

Constraints in problems with Codeforces-style indexing at this level are usually large, often up
