---
title: "CF 1493E - Enormous XOR"
description: "We are given two non-negative integers, l and r, represented as binary strings of equal length. The task is to consider all contiguous ranges [x, y] where l ≤ x ≤ y ≤ r and compute the bitwise XOR of all integers in that range. Let g(x, y) denote this XOR."
date: "2026-06-10T22:15:58+07:00"
tags: ["codeforces", "competitive-programming", "bitmasks", "constructive-algorithms", "greedy", "math", "strings", "two-pointers"]
categories: ["algorithms"]
codeforces_contest: 1493
codeforces_index: "E"
codeforces_contest_name: "Codeforces Round 705 (Div. 2)"
rating: 2600
weight: 1493
solve_time_s: 51
verified: false
draft: false
---

[CF 1493E - Enormous XOR](https://codeforces.com/problemset/problem/1493/E)

**Rating:** 2600  
**Tags:** bitmasks, constructive algorithms, greedy, math, strings, two pointers  
**Solve time:** 51s  
**Verified:** no  

## Solution
## Problem Understanding

We are given two non-negative integers, `l` and `r`, represented as binary strings of equal length. The task is to consider all contiguous ranges `[x, y]` where `l ≤ x ≤ y ≤ r` and compute the bitwise XOR of all integers in that range. Let `g(x, y)` denote this XOR. We are asked to find the maximum possible value of `g(x, y)` over all valid ranges.

In other words, we are looking for a subrange of numbers inside `[l, r]` whose XOR, treated as an integer, is as large as possible. The output must be in binary without leading zeros.

The constraints allow `n` to be up to 10^6, meaning `l` and `r` can be up to one million bits long. This rules out any naive approach that enumerates numbers between `l` and `r` or checks every possible subrange: the number of such ranges grows quadratically in the worst case, and even storing numbers of length 10^6 in a naive array is impractical.

The subtleties lie in the binary representation. Small differences in the most significant bits between `l` and `r` can allow the XOR of some range to reach a number with all ones in high bits. Edge cases include when `l` equals `r`, or when `l` is zero and `r` is a large power-of-two minus one. A careless approach that XORs bits independently or assumes simple numeric properties would fail on these inputs. For example, if `l = 0011` and `r = 0110`, the maximal XOR is `0111`, not `0110`, since XORing a carefully chosen subrange can flip the highest bit where `l` and `r` differ.

## Approaches

The brute-force approach is straightforward: iterate through all possible `x` and `y` in `[l, r]`, compute the XOR `g(x, y)`, and track the maximum. Computing the XOR of a subrange `[x, y]` can be optimized using a prefix XOR array `px[i] = 0 ⊕ 1 ⊕ ... ⊕ i`, with `g(x, y) = px[y] ⊕ px[x-1]`. However, `x` and `y` can each be up to 2^n, and n can be 10^6. Even with prefix XOR, we would need to iterate over an astronomically large number of ranges. Therefore, brute force is infeasible.

The key insight comes from analyzing the binary structure. Consider the binary representations of `l` and `r`. Let `k` be the position of the most significant bit where `l` and `r` differ. To maximize XOR, we want to choose `x` and `y` such that the resulting XOR has this `k`-th bit set. Once we set this bit, we can freely set all lower bits to one to maximize the value. Essentially, the optimal XOR is a number where all bits from the most significant differing bit down to the least significant bit are ones.

This observation reduces the problem to a single calculation: find the most significant bit where `l` and `r` differ, and set all bits from that position downward. This can be done in linear time relative to the bit length of the numbers, O(n). There is no need to enumerate ranges, since the XOR value depends only on the highest differing bit.

| Approach | Time Co
