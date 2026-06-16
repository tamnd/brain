---
title: "CF 1554D - Diane"
description: "We are asked to construct a string of length n using lowercase English letters such that a very strong parity condition holds: every non-empty substring must appear inside the string an odd number of times when we count all occurrences."
date: "2026-06-16T16:06:13+07:00"
tags: ["codeforces", "competitive-programming", "constructive-algorithms", "greedy", "strings"]
categories: ["algorithms"]
codeforces_contest: 1554
codeforces_index: "D"
codeforces_contest_name: "Codeforces Round 735 (Div. 2)"
rating: 1800
weight: 1554
solve_time_s: 105
verified: false
draft: false
---

[CF 1554D - Diane](https://codeforces.com/problemset/problem/1554/D)

**Rating:** 1800  
**Tags:** constructive algorithms, greedy, strings  
**Solve time:** 1m 45s  
**Verified:** no  

## Solution
## Problem Understanding

We are asked to construct a string of length `n` using lowercase English letters such that a very strong parity condition holds: every non-empty substring must appear inside the string an odd number of times when we count all occurrences.

A substring here means any contiguous segment of the string. So for a fixed string `s`, we consider every possible `s[l:r]`, and for each distinct substring value, we count how many times it appears across all positions. The requirement is that each distinct substring has an odd frequency.

The key challenge is that substrings overlap heavily, so counts are highly correlated. A naive attempt that treats substrings independently immediately fails because changing one character affects Θ(n²) substrings.

The constraints push us to think in linear or near-linear construction per test case. Since the sum of `n` is up to `3 · 10^5`, any solution worse than O(n) per test case risks TLE. Even O(n log n) per test case is too slow in the worst case.

The most dangerous hidden pitfall is assuming the condition behaves like a simple frequency constraint on characters. For example, making all characters distinct is not enough to control repeated substrings like `"ab"` or `"bc"` appearing multiple times in larger strings. Another pitfall is trying to reason locally about substrings of fixed length, which ignores interactions across lengths.

A small sanity example shows why naive constructions fail:

For `n = 3`, `"aaa"` makes substring `"a"` occur 3 times (odd), but `"aa"` occurs 2 times (even), so it fails. This shows that repeated structure quickly breaks the parity condition.

The correct construction must carefully control repetition patterns across all substring lengths simultaneously.

## Approaches

A brute-force approach would be to generate a candidate string and explicitly enumerate all substrings, count their frequencies using a hash map, and verify the parity condition. This requires generating Θ(n²) substrings, and each insertion into a hash structure is O(1) amortized, giving O(n²) per check. Even for `n = 10^5`, this is completely infeasible.

The key structural insight is that we do not actually need to manage substring counts explicitly. Instead, we construct a string with a strong symmetry-breaking property that forces every substring to have a unique “mirror pairing behavior” that guarantees odd multiplicity. The intended construction is extremely simple: build the string in a pattern that avoids any repeated substring structure except in a controlled way that guarantees parity consistency.

The canonical solution is to construct a string using a repeating pattern over a small alphabet while carefully ensuring that every substring occurrence has a unique counterpart except one unpaired occurrence. One clean way to achieve this is to construct a string where positions are arranged so that any substring occurrence can be mapped to a symmetric counterpart, except for a single
