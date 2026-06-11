---
title: "CF 1195B - Sport Mafia"
description: "We are asked to determine how many candies Alya ate during a sequence of $n$ actions with a candy box. Each action is either putting candies into the box or eating exactly one candy from it. The first action always adds one candy."
date: "2026-06-12T00:14:47+07:00"
tags: ["codeforces", "competitive-programming", "binary-search", "brute-force", "math"]
categories: ["algorithms"]
codeforces_contest: 1195
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 574 (Div. 2)"
rating: 1000
weight: 1195
solve_time_s: 147
verified: false
draft: false
---

[CF 1195B - Sport Mafia](https://codeforces.com/problemset/problem/1195/B)

**Rating:** 1000  
**Tags:** binary search, brute force, math  
**Solve time:** 2m 27s  
**Verified:** no  

## Solution
## Problem Understanding

We are asked to determine how many candies Alya ate during a sequence of $n$ actions with a candy box. Each action is either putting candies into the box or eating exactly one candy from it. The first action always adds one candy. Every subsequent action that adds candies must add one more than the last time candies were added. Eating is only allowed if the box has at least one candy. At the end of all $n$ actions, the box contains $k$ candies. Our task is to compute how many times Alya chose to eat a candy.

The input consists of two integers, $n$ and $k$, where $n$ can go up to $10^9$ and $k$ up to $10^9$. This immediately rules out any solution that tries to simulate each action sequentially, because doing $O(n)$ operations would be far too slow. We need an approach that computes the number of candies eaten directly from $n$ and $k$ using arithmetic reasoning.

A subtle edge case occurs when the box ends up with more candies than the minimum sum from the sequence of "put" actions. For example, if $n=1$ and $k=1$, Alya has done only one move and never ate a candy. A careless approach might try to compute some formula that produces a negative number of eaten candies. Another edge case is when $k$ is very small compared to $n$, which forces many "eat" actions, so any formula needs to handle subtraction carefully to avoid underflow or off-by-one mistakes.

## Approaches

The brute-force approach would be to simulate the sequence of $n$ actions. Start with a counter for candies eaten, track the number of candies in the box, and increase the number of candies to add each time a "put" action occurs. For each action, either eat a candy if possible or add the next increment of candies. This is correct because it mirrors the problem rules directly. However, if $n$ is up to $10^9$, performing $n$ iterations is computationally infeasible. Even with $10^8$ iterations per second, this would take 10 seconds or more, which exceeds the 2-second time limit.

The key observation is that the total number of candies added in a strictly increasing "put" sequence is a triangular number. If we let $m$ be the number of "put" actions, then the sum of candies added is $1 + 2 + 3 + ... + m = m(m+1)/2$. If Alya ate $x$ candies, then the total number of actions $n$ splits into $m$ puts and $x$ eats such that $m + x = n$, and the final candies $k$ satisfy $k = m(m+1)/2 - x$. This gives the quadratic relation $m(m+1)/2 - (n-m) = k$, which can be solved for $m$ and then $x$.

This observation reduces the problem to solving a quadratic equation for $m$, taking care to round down the root since $m$ must be an integer. Once $m$ is known, the number of candies eaten is simply $x = n - m$. This approach is constant time, $O(1)$, and uses no additional memory beyond a few integers.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n) | O(1) | Too slow |
| Optimal | O(1) | O(1) |  |
