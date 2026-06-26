---
title: "CF 105705A - Max Xor Pair"
description: "The task is about finding how different two chosen numbers from a collection can be when we compare them using bitwise XOR. You are given a list of integers, and you must pick two distinct elements whose XOR value is as large as possible."
date: "2026-06-26T08:04:44+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105705
codeforces_index: "A"
codeforces_contest_name: "AlgoChief Sprint Round 3"
rating: 0
weight: 105705
solve_time_s: 32
verified: false
draft: false
---

[CF 105705A - Max Xor Pair](https://codeforces.com/problemset/problem/105705/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 32s  
**Verified:** no  

## Solution
## Problem Understanding

The task is about finding how different two chosen numbers from a collection can be when we compare them using bitwise XOR. You are given a list of integers, and you must pick two distinct elements whose XOR value is as large as possible. The output is that maximum possible XOR value.

The input represents a sequence of integers, each of which can be thought of as a binary number. The operation of XOR compares these binary representations bit by bit and produces a new number where each bit is set if the corresponding bits of the two inputs differ. The goal is to find a pair whose differences are concentrated in the most significant bits, since those contribute more to the numeric value.

If the array size is up to around 100,000 and each number can be as large as typical 32-bit or 60-bit integers, a quadratic solution that checks every pair would require on the order of 10^10 operations in the worst case, which is far beyond what can run in a time limit of a few seconds. This immediately suggests that we need a structure that allows us to reason about many pairs at once instead of enumerating them.

A common edge case is when all numbers are identical. For example, if the input is `[7, 7, 7]`, every XOR is zero, so the correct answer is `0`. A naive approach that does not carefully initialize the maximum or that assumes at least one positive XOR might behave incorrectly if it is not written carefully. Another edge case is when numbers differ only in low bits, such as `[8, 9, 10]`, where the maximum XOR is small but comes from subtle bit differences. Any solution must correctly consider all bit positions, not just magnitude of numbers.

## Approaches

The most direct strategy is to try every pair of numbers and compute their XOR. This is correct because it explicitly evaluates all possibilities, and XOR is deterministic for any pair. The problem is that this approach performs a nested loop over all elements, leading to about n²/2 XOR operations. When n reaches 100,000, this becomes roughly five billion comparisons, which is too slow for practical execution.

The key observation is that XOR is determined bit by bit from the most significant side downward. If we want to maximize the result, we want to make the highest possible bit equal to 1 in the answer. That means we want two numbers that differ as early as possible in binary representation. Instead of checking all pairs, we can organize numbers so that we can quickly find, for any number, another number that has opposite bits in high positions.

This structure is naturally captured by a binary trie. Each number is inserted bit by bit, forming a tree where each edge represents a binary digit. When trying to maximize XOR for a given number, we walk the trie preferring the opposite bit at each step, because choosing a different bit increases the XOR at that position. This greedy choice works because higher bits dominate the final value, so maximizing them first guarantees global optimality.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n²) | O(1) | Too slow |
| Binary Trie | O(n · B) | O(n · B) | Accepted |

Here B is the number of bits needed to represent the largest number, typically around 31 or 60.

## Algorithm Walkthrough

We build a binary trie where each node has up to two children, corresponding to bit 0 and bit 1.

1. Determine the maximum bit length needed by inspecting the largest number in the array. This ensures we process all relevant bit positions consistently.
2. Initialize an empty trie with a single root node. This node represents no bits chosen yet.
3. Insert each number into the trie by iterating from t
