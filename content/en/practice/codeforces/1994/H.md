---
title: "CF 1994H - Fortnite"
description: "The first problem asks whether an infinite sequence of perfect squares $(an^2)$ can exist such that each term starting from the third satisfies the Fibonacci-type recurrence $an^2 = a{n-1}^2 + a{n-2}^2."
date: "2026-06-09T02:24:27+07:00"
tags: ["codeforces", "competitive-programming", "combinatorics", "constructive-algorithms", "games", "greedy", "hashing", "interactive", "math", "number-theory", "strings"]
categories: ["algorithms"]
codeforces_contest: 1994
codeforces_index: "H"
codeforces_contest_name: "Codeforces Round 959 sponsored by NEAR (Div. 1 + Div. 2)"
rating: 3500
weight: 1994
solve_time_s: 124
verified: false
draft: false
---

[CF 1994H - Fortnite](https://codeforces.com/problemset/problem/1994/H)

**Rating:** 3500  
**Tags:** combinatorics, constructive algorithms, games, greedy, hashing, interactive, math, number theory, strings  
**Solve time:** 2m 4s  
**Verified:** no  

## Solution
## Exploration

The first problem asks whether an infinite sequence of perfect squares $(a_n^2)$ can exist such that each term starting from the third satisfies the Fibonacci-type recurrence

$a_n^2 = a_{n-1}^2 + a_{n-2}^2.$

Since squares grow faster than linearly and the recurrence is additive, the existence of such a sequence is highly restrictive. Any proposed approach must rigorously exclude all possibilities or provide a valid construction.

The second problem asks for an infinite increasing sequence of squares $(a_n^2)$ such that each sum of consecutive terms is itself a perfect square,

$a_n^2 + a_{n+1}^2 = b_n^2$

for some integer $b_n$. This condition is equivalent to requiring that each consecutive triple $(a_n, a_{n+1}, b_n)$ forms a Pythagorean triple. A valid solution must provide an explicit construction and prove the property for all terms.

## Problem Understanding

Problem one is a nonexistence problem. A rigorous solution must examine all integer sequences satisfying $a_n^2 = a_{n-1}^2 + a_{n-2}^2$ and show that no infinite sequence of natural numbers is possible. Testing small integers reveals that the sequence can only start with trivial values, since any nontrivial sequence quickly violates integer constraints.

Problem two is a constructive existence problem. One must define an explicit increasing sequence $(a_n)$ and verify that $a_n^2 + a_{n+1}^2$ is always a perfect square. Any recurrence or formula must produce integers from the first step, as the first pair must satisfy the condition exactly.

## Proof Architecture

For the first problem, one can examine the sequence $(a_n)$ modulo small integers to show constraints, or argue using minimality. Starting with integers $a_1, a_2$, the next term $a_3$ is determined as $a_3 = \sqrt{a_1^2 + a_2^2}$. Since $a_1^2 + a_2^2$ must be a perfect square, the pair $(a_1, a_2)$ must itself form a Pythagorean pair. The sequence then reduces to generating Pythagorean triples in a Fibonacci-style sequence. Known classifications of integer solutions of $x^2 + y^2 = z^2$ show that no infinite strictly increasing sequence of integers can satisfy $a_n^2 = a_{n-1}^2 + a_{n-2}^2$, because eventually the recursion forces noninteger or decreasing terms.

For the second problem, one can exploit the parametrization of primitive Pythagorean triples: for coprime integers $u>v>0$ of opposite parity, the triple $(u^2 - v^2, 2uv, u^2 + v^2)$
