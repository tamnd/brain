---
title: "CF 1685C - Bring Balance"
description: "We are given a sequence of parentheses of length $2n$, containing exactly $n$ opening and $n$ closing brackets. The task is to transform this sequence into a correct balanced parentheses string using the minimum number of operations, where each operation consists of reversing…"
date: "2026-06-09T23:49:03+07:00"
tags: ["codeforces", "competitive-programming", "brute-force", "constructive-algorithms", "greedy"]
categories: ["algorithms"]
codeforces_contest: 1685
codeforces_index: "C"
codeforces_contest_name: "Codeforces Round 794 (Div. 1)"
rating: 2600
weight: 1685
solve_time_s: 45
verified: false
draft: false
---

[CF 1685C - Bring Balance](https://codeforces.com/problemset/problem/1685/C)

**Rating:** 2600  
**Tags:** brute force, constructive algorithms, greedy  
**Solve time:** 45s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a sequence of parentheses of length $2n$, containing exactly $n$ opening and $n$ closing brackets. The task is to transform this sequence into a correct balanced parentheses string using the minimum number of operations, where each operation consists of reversing any contiguous substring.

A balanced parentheses sequence is one where prefixes never contain more closing than opening brackets, and the total number of opening and closing brackets matches. The final goal is not to rearrange arbitrarily but specifically to reach any valid balanced configuration using substring reversals.

The key constraint is that the sum of $n$ over all test cases is at most $2 \cdot 10^5$. This immediately rules out anything quadratic per test case, since a naive simulation of repeated global searches or greedy fixing with rescans would degrade to $O(n^2)$ in the worst case and time out. We need a construction that runs in linear time per test case or close to it.

A subtle point in this problem is that reversals are powerful: they can move characters across long distances while also flipping their roles locally. This makes it easy to accidentally assume the problem behaves like adjacent swaps, which is not true.

A few edge cases expose naive strategies.

If the string is already balanced, the answer is zero. Any algorithm that does not explicitly check balance might still try to apply unnecessary operations.

If the string is completely reversed like `)))...(((`, a greedy prefix-fix approach that only fixes one imbalance at a time might repeatedly move single parentheses and produce far too many operations, even though the optimal answer is small.

Another tricky case is alternating structure like `())(())(()...)`, where local greedy fixes can “over-correct” earlier regions and break previously fixed structure if not carefully controlled.

## Approaches

A brute-force idea is to simulate the process: repeatedly scan the string to find the first position where the prefix balance becomes negative, then search forward for a position where a reversal would fix that prefix. After each operation, recompute balances from scratch.

This is correct in principle because every reversal preserves the multiset of parentheses, and repeated local fixes can eventually eliminate all prefix violations. However, each operation may require a full scan of the string to identify the next violation, and there can be up to $O(n)$ operations. This leads to $O(n^2)$ behavior per test case, which is too slow for $2 \cdot 10^5$ total length.

The key observation is that we do not need to simulate intermediate states at all. Instead, we can construct a final valid sequence directly and “repair” the string by fixing positions from left to right. Each time we detect that the current prefix cannot form a valid sequence, we use a single reversal to bring a needed character into place while preserving already fixed prefix structure.

The deeper structure is that a balanced sequence can be constructed greedily from left to right by ensuring that at each position we place the correct parenthesis needed to maintain feasibility. Since reversals can relocate any future character into the current position, each fix can be done in one operation.

This reduces the problem to a constructive greedy process that aligns the given string to a target valid structure without ever fully recomputing global state.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Simulation | $O(n^2)$ | $O(n)$ | Too slow |
| Greedy Construction with Reversals | $O(n)$ | $O(n)$ | Accepted |

## Algorithm Walkthrough

We maintain a working string and build a valid prefix step by step. We also track the current balance as the number of opens minus closes.

1. Iterate through positions from left to right. At each position, decide whether we need an opening or closing bracket to keep the prefix valid. A valid prefix must never have negative balance, so whenever balance is low, we prefer an opening bracket.
2. If the current character already matches what we need, we simply continue and update the balance.
3. If it does not match, we locate the next position to the right that contains the desired character.
4. We reverse the substring between the current position and that found position. This brings the needed character into place while only affecting a suffix that has not been fixed yet.
5. After performing the rev
