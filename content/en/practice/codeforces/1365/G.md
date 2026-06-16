---
title: "CF 1365G - Secure Password"
description: "We are given an unknown array of non-negative integers, each up to 64-bit range. We cannot see the array directly. Instead, we can query any subset of indices, and the judge returns the bitwise OR of the elements at those positions."
date: "2026-06-16T11:50:19+07:00"
tags: ["codeforces", "competitive-programming", "bitmasks", "combinatorics", "constructive-algorithms", "interactive", "math"]
categories: ["algorithms"]
codeforces_contest: 1365
codeforces_index: "G"
codeforces_contest_name: "Codeforces Round 648 (Div. 2)"
rating: 2800
weight: 1365
solve_time_s: 123
verified: false
draft: false
---

[CF 1365G - Secure Password](https://codeforces.com/problemset/problem/1365/G)

**Rating:** 2800  
**Tags:** bitmasks, combinatorics, constructive algorithms, interactive, math  
**Solve time:** 2m 3s  
**Verified:** no  

## Solution
## Problem Understanding

We are given an unknown array of non-negative integers, each up to 64-bit range. We cannot see the array directly. Instead, we can query any subset of indices, and the judge returns the bitwise OR of the elements at those positions.

From this hidden array, a second array is defined. For each position i, the output value is the bitwise OR of all elements except the i-th one. So each output entry is the OR of an almost-complete array, missing exactly one element.

Our task is to reconstruct this entire output array using at most 13 subset OR queries.

The key observation is that we are not trying to recover the original array. We only need, for each index i, the OR of “all except i”. That changes the problem completely, because OR is idempotent and loses information, so reconstructing A is impossible in general, but reconstructing these complements is feasible.

The constraint n ≤ 1000 with only 13 queries immediately rules out any per-index querying strategy. A naive approach would query n times or even n log n times, which is far beyond the budget. This strongly suggests a global bitwise strategy where each query extracts information for many indices simultaneously.

A subtle edge case arises when many elements share bits. If we assume we can isolate elements cleanly, we might try to reconstruct each A[i], but OR does not decompose uniquely. For example, A = [1, 2, 3] and A = [3, 0, 3] can produce identical OR behavior for many subsets. So any approach relying on recovering individual values is fundamentally unsafe. The only stable quantity is the full OR over all elements.

## Approaches

A direct but incorrect idea is to attempt reconstructing each A[i] by comparing the total OR with and without i. If we could compute total OR of all elements, then each answer would simply be that OR, unless removing i removes some unique bit. The difficulty is that we do not know which indices contribute unique bits without isolating them, and isolating requires too many queries.

The key structural insight is to exploit bit independence. Since OR operates per bit, each bit behaves independently across indices. A bit contributes to P[i] if and only if it exists in at least one A[j] for j ≠ i. So for a fixed bit, the only problematic case for position i is when that bit appears exclusively in A[i]. This turns the problem into identifying, for each index, whether it is the unique carrier of a bit.

We can exploit this using a classical technique: partition queries and reconstruction via complementing contributions. The core idea is to compute the OR of all elements, then for each index determine whether removing it changes the global OR. If removing i does not change the total OR, then A[i] contributes no unique bits. If removing i does change it, then A[i] contains at least one bit that is exclusive to it.

To compute all P[i] efficiently, we observe a stronger formulation. Let T be the OR of the entire array. Then:

P[i] = T if A[i] does not contain any bit that is unique in the full array excluding i, otherwise P[i] is still T because removing a non-unique element does not affect OR. The only situation where P[i] differs from T is when A[i] is the only source of some bit; in that case removing it reduces the OR.

So we need to detect, for each bit, how many times it appears. Instead of counting exactly, we only need to know, for each i, whether A[i] is the unique holder of some bit.

We achieve this using a standard bit-splitting construction: represent indices in binary using up to 10 bits (since n ≤ 1000), and perform group OR queries over subsets defined by bit positions. Each query collects OR over a carefully chosen partition so that each index is excluded from exactly a controlled set of queries. By combining results, we can reconstruct, for each index, the OR of all elements except itself.

The construction
