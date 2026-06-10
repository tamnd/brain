---
title: "CF 1549A - Gregor and Cryptography"
description: "The problem asks us to find two integers, $a$ and $b$, that serve as “bases” for a given prime number $P$ in the sense that $P$ modulo $a$ equals $P$ modulo $b$, and both numbers lie between $2$ and $P$, with $a$ strictly smaller than $b$."
date: "2026-06-10T13:31:20+07:00"
tags: ["codeforces", "competitive-programming", "math", "number-theory"]
categories: ["algorithms"]
codeforces_contest: 1549
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 736 (Div. 2)"
rating: 800
weight: 1549
solve_time_s: 204
verified: false
draft: false
---

[CF 1549A - Gregor and Cryptography](https://codeforces.com/problemset/problem/1549/A)

**Rating:** 800  
**Tags:** math, number theory  
**Solve time:** 3m 24s  
**Verified:** no  

## Solution
## Problem Understanding

The problem asks us to find two integers, $a$ and $b$, that serve as “bases” for a given prime number $P$ in the sense that $P$ modulo $a$ equals $P$ modulo $b$, and both numbers lie between $2$ and $P$, with $a$ strictly smaller than $b$. We are given multiple test cases, each with a single prime number, and for each case we need to print any valid pair $(a, b)$ satisfying these conditions.

Since $P$ is prime, the smallest nontrivial divisor is $2$, and $P$ itself has no divisors between $2$ and $P-1$. That implies that remainders modulo small integers are easily predictable: for any $k$, $P \bmod k$ is $P - k$ if $k$ is close to $P$, or simply $P \bmod k$ if $k$ is small.

The constraints give $P$ up to $10^9$ and up to $1000$ test cases. This rules out any solution that would iterate through all possible pairs of $(a, b)$, because checking all $O(P^2)$ pairs for the largest $P$ would be computationally infeasible. Edge cases include very small primes like $5$, where the solution set is limited, and larger primes where multiple valid pairs exist.

A naive approach could miss small primes entirely if it assumes a generic formula for $a$ and $b$, so the algorithm must handle the minimum primes carefully.

## Approaches

The brute-force solution would check every pair $(a, b)$ such that $2 \le a < b \le P$ and compute $P \bmod a$ and $P \bmod b$, returning the first pair where the remainders match. This is correct because it directly implements the definition, but for $P$ up to $10^9$, the worst case would require roughly $10^{18}$ operations, which is impossible.

The key insight comes from observing that for a prime $P$, the modulo of $P$ with respect to $k$ is $P \bmod k = P - k$ if $k > P/2$, because $P$ is larger than $k$ but less than $2k$. This suggests a simple and general construction: choose $a = 2$, then set $b = a + (P \bmod a)$. Since $P \bmod a$ i
