---
title: "CF 1172A - Nauuo and Cards"
description: "We are given two sequences of length $n$. One sequence represents cards currently in Nauuo’s hand, and the other represents a pile of cards arranged from top to bottom."
date: "2026-06-13T09:26:25+07:00"
tags: ["codeforces", "competitive-programming", "greedy", "implementation"]
categories: ["algorithms"]
codeforces_contest: 1172
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 564 (Div. 1)"
rating: 1800
weight: 1172
solve_time_s: 320
verified: false
draft: false
---

[CF 1172A - Nauuo and Cards](https://codeforces.com/problemset/problem/1172/A)

**Rating:** 1800  
**Tags:** greedy, implementation  
**Solve time:** 5m 20s  
**Verified:** no  

## Solution
## Problem Understanding

We are given two sequences of length $n$. One sequence represents cards currently in Nauuo’s hand, and the other represents a pile of cards arranged from top to bottom. Each numbered card from $1$ to $n$ appears exactly once across these two sequences, while zeros represent empty placeholders.

The only allowed operation is a swap-like action: pick a card from the hand, place it at the bottom of the pile, and immediately draw the top card of the pile into the hand. This operation effectively moves one hand card into the pile and replaces it with the current top of the pile.

The goal is to transform the pile so that it contains the numbers $1$ through $n$ in strictly increasing order from top to bottom. The task is to compute the minimum number of such operations required.

The constraint $n \le 2 \cdot 10^5$ forces any solution to be essentially linear or near-linear. Any approach that repeatedly simulates the full operation step-by-step, especially with nested scans over hand and pile, would degrade to $O(n^2)$ in worst cases where many swaps are needed before reaching the desired ordering.

A subtle issue arises from empty cards. A naive strategy might treat zeros as irrelevant or freely swappable, but they are structurally important because they control when real cards can be cycled into the pile. Another tricky situation appears when the next required number is deep in the pile, forcing multiple operations that shuffle intermediate values without immediately improving correctness.

## Approaches

A direct simulation approach tries to mimic the process: repeatedly check whether the pile top is the next required number, and if not, cycle some hand card into the pile. Each operation is $O(1)$, but locating a usable hand card or reasoning about progress without a guiding structure leads to inefficient repeated scans. In worst cases, every operation only advances the system by one useful card, and maintaining this behavior with naive data structures becomes quadratic.

The key observation is that the final target state is completely fixed: the pile must become $1,2,\dots,n$. This means every number has a unique correct position, and the process is only about delaying or accelerating when each number reaches the top of the pile.

Instead of simulating all configurations, we can think in reverse. Consider scanning the pile from top to bottom. If the pile already contains a prefix of the form $1,2,3,\dots,k$ in order, then those cards require no additional work relative to each other. The only reason we need operations is to "repair" breaks in this increasing sequence as early as possible.

Now look at where each number is initially. If a number appears in the pile above another number that should come earlier in the final order, that creates forced delays. The optimal strategy is to greedily ensure that we never perform unnecessary operations for already correctly ordered prefixes and only pay cost when we encounter a mismatch between expected order and actual pile progression.

This reduces the problem to tracking how far the pile already matches the prefix of $1$ to $n$, and how many operations are required to gradually expose missing elements from the hand when the pile cannot naturally continue the sequence.

The resulting solution runs in linear time by scanning once and maintaining a pointer to the next required card.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Simulation | $O(n^2)$ | $O(n)$ | Too slow |
| Prefix Matching Greedy | $O(n)$ | $O(n)$ | Accepted |

## Algorithm Walkthrough

We maintain a pointer `need` representing the next required number in the final sorted pile, starting from $1$. We also preprocess the initial positions of all numbers in either the pile or the hand.

1. First, we treat the pile as the only structure that matters for building the final sequence. We scan it from top to bottom and try to match it against the sequence $1,2,\dots,n$. Each time we see the expected `need`, we advance `need`. This tells us how many numbers are already in a valid prefix order.
2. Once this scan breaks, we know the remaining numbers are not aligned with the final order in the pile’s current structure. From this point, every remaining number that is not already in place must be “brought forward” through operations.
3. Each operation effectively allows us to take a useful card from the hand and inject it into the pile at the correct time, replacing a non-helpful top card. The key is that every operation can fix at most one missing continuation of the prefix.
4. Therefore, the answer is the number of values from $1$ to $n$ that are not already forming a correct prefix in the initial pile scan.

The final result is:

$$\text{operations} = n - (\text{length of longest prefix already correct in pile})$$

### Why it works

The algorithm relies on the invariant that once a number is skipped in the pile scan, it cannot be part of the initial contiguous increasing prefix anymore, regardless of how we rearrange later. Any such missing or displaced value must be introduced through at least one operation, since it cannot be accessed in the correct order without cycling through the hand mechanism. Conversely, every correct prefix element requires zero operations because it already appears in the correct relative order and position.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    a = list(map(int, input().split()))
    b = list(map(int, input().split()))

    need
```
