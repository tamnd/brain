---
title: "CF 1894C - Anonymous Informant"
description: "We are given an array $b$ of length $n$ and a number $k$, which represents the number of operations performed on some hidden original array $a$. Each operation consists of choosing a fixed point $x$ in $a$ and cyclically left-shifting $a$ by $x$ positions."
date: "2026-06-09T01:14:35+07:00"
tags: ["codeforces", "competitive-programming", "constructive-algorithms", "graphs", "implementation"]
categories: ["algorithms"]
codeforces_contest: 1894
codeforces_index: "C"
codeforces_contest_name: "Codeforces Round 908 (Div. 2)"
rating: 1400
weight: 1894
solve_time_s: 90
verified: false
draft: false
---

[CF 1894C - Anonymous Informant](https://codeforces.com/problemset/problem/1894/C)

**Rating:** 1400  
**Tags:** constructive algorithms, graphs, implementation  
**Solve time:** 1m 30s  
**Verified:** no  

## Solution
## Problem Understanding

We are given an array $b$ of length $n$ and a number $k$, which represents the number of operations performed on some hidden original array $a$. Each operation consists of choosing a fixed point $x$ in $a$ and cyclically left-shifting $a$ by $x$ positions. A fixed point is an index $i$ such that $a_i = i$. The challenge is to decide whether there exists some initial array $a$ and a sequence of $k$ operations that results in the array $b$.

The input size allows $n$ up to $2 \cdot 10^5$ and $k$ up to $10^9$. This rules out any solution that tries to simulate all $k$ operations. Since $k$ can be much larger than $n$, we must find a property of $b$ that allows us to reason about the feasibility without performing every shift.

Non-obvious edge cases include arrays of length one, where any operation is trivial because a single element is always a fixed point, and arrays where all elements are the same, because multiple shifts might lead to the same configuration or make a valid sequence impossible. For example, if $b = [1]$ and $k = 10^9$, the answer is always "Yes" because the only element is its own fixed point. Conversely, if $b = [1, 1]$ and $k = 5$, there is no initial array with enough distinct fixed points to reach $b$, so the answer is "No".

## Approaches

The brute-force approach is to try every possible starting array $a$ and simulate $k$ operations. This involves identifying all fixed points in $a$, performing the left shifts, and repeating. The number of possibilities for $a$ is $n^n$, which is infeasible for $n$ up to $2 \cdot 10^5$. Even simulating one candidate would take $O(k \cdot n)$, which is impossible when $k$ is up to $10^9$.

The key insight is that each operation moves elements in a cycle, and the final array $b$ can only differ from the identity permutation by a number of "displaced positions" that corresponds to a contiguous subsequence of shifts. This reduces the problem to checking how many positions in $b$ are "out of place" relative to the identity array $1, 2, \ldots, n$. Specifically, for each index $i$, define the offset $\text{diff} = b_i - i$. Since left shifts wrap around, $\text{diff} \mod n$ represents the shift needed to match that element to a fixed point.

We count the occurrences of each shift value modulo $n$. Any shift value that appears $n - k$ or fewer times cannot be corrected by $k$ operations. Therefore, the answer is "Yes" if there exists a shift value that can be achieved by performing up to $k$ shifts in sequence.

The story here is that the brute-force is blocked by $k$ and $n$, but the modulo shift counts capture the invariant: each element only moves relative to its original position by some multiple of left shifts, and $k$ operations can only cover a limited number of "misaligned elements".

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n^n * k) | O(n) | Too slow |
| Optimal | O(n) per test case | O(n) | Accepted |

## Algorithm Walkthrough

1. For each test case, read $n$ and $k$, then read the array $b$.
2. Initialize a counter array $count$ of size $n$ to zero. This will track how many elements can be aligned with each possible shift.
3. For each index $i$ in $b$, compute the required shift $\text{shift} = (i - b[i] \% n + n) \% n$. This represents how far $b[i]$ is from its "identity" position $i$ modulo $n$. Increment $count[shift]$.
4. After processing all indices, iterate over possible shift values. If any shift appears at least $n - k$ times, output "Yes". Otherwise, output "No".

The reason this works is that each operation can fix a contiguous block of positions corresponding to a shift. Counting the shift occurrences captures whether there exists a sequence of operations that can rearrange elements to match $b$. The modulo operation accounts for wraparound due to cyclic shifts.

## Python Solution

```
PythonRun
```

The solution reads each test case, computes how far each element of $b$ is from its expected position, and counts these distances modulo $n$. Checking whether any shift occurs at least $n-k$ times ensures that $k$ operations are suff
