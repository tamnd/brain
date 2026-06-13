---
title: "CF 1215B - The Number of Products"
description: "We are given a sequence of nonzero integers and asked to count how many subarrays produce a positive product and how many produce a negative product. A subarray is defined by choosing two indices $l le r$ and multiplying everything from $al$ to $ar$."
date: "2026-06-13T17:32:07+07:00"
tags: ["codeforces", "competitive-programming", "combinatorics", "dp", "implementation"]
categories: ["algorithms"]
codeforces_contest: 1215
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 585 (Div. 2)"
rating: 1400
weight: 1215
solve_time_s: 218
verified: true
draft: false
---

[CF 1215B - The Number of Products](https://codeforces.com/problemset/problem/1215/B)

**Rating:** 1400  
**Tags:** combinatorics, dp, implementation  
**Solve time:** 3m 38s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a sequence of nonzero integers and asked to count how many subarrays produce a positive product and how many produce a negative product. A subarray is defined by choosing two indices $l \le r$ and multiplying everything from $a_l$ to $a_r$.

Because every number is nonzero, the sign of any product depends only on how many negative elements are inside the subarray. An even number of negatives makes the product positive, and an odd number makes it negative. The magnitude never matters.

The constraint $n \le 2 \cdot 10^5$ rules out any quadratic enumeration of subarrays. There are roughly $n(n+1)/2$ subarrays, which is about $2 \cdot 10^{10}$ at maximum input size. Any solution that explicitly checks each subarray or multiplies ranges is too slow.

A naive attempt often fails in a subtle way: even if multiplication is avoided and only signs are tracked, iterating over all $l, r$ pairs still exceeds limits. Another common mistake is recomputing sign parity from scratch for each $r$, which leads to $O(n^2)$ behavior.

Edge cases that matter here include all-positive arrays, where every subarray is positive, and alternating signs, where parity flips frequently. For example, in an input like $[-1, -1, -1]$, the subarray $[1,3]$ has product $-1$, but $[1,2]$ is positive. Any solution must consistently track parity rather than recompute it.

## Approaches

A brute-force method considers every pair $(l, r)$, counts the number of negative elements inside, and decides the sign of the product. This is logically correct because the sign depends only on parity. However, counting negatives inside each subarray requires scanning up to $O(n)$ elements, producing an $O(n^3)$ solution if done directly, or $O(n^2)$ with prefix optimization. With $n = 2 \cdot 10^5$, even $10^10$ operations is far beyond feasible runtime.

The key insight is to avoid looking at subarrays explicitly. Instead, we track how many subarrays ending at each position have even or odd parity of negatives. Once we know this for each endpoint $r$, we can accumulate answers.

The transformation comes from reframing the problem as prefix parity counting. If we define a prefix parity value that flips whenever we see a negative number, then a subarray has negative product exactly when its endpoints have different parity, and positive product when they match. This reduces the problem to counting pairs of equal or different prefix states, which can be done in linear time by maintaining counts of how many prefixes have each parity.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(n^2)$ or worse | $O(1)$ | Too slow |
| Optimal | $O(n)$ | $O(1)$ | Accepted |

## Algorithm Walkthrough

We convert the problem into counting prefix parity states.

1. We define a running variable that tracks the parity of the number of negative elements seen so far. This parity is either even or odd and flips whenever we encounter a negative number. This gives us a compact representation of all past subarrays ending at each index.
2. We maintain two counters: how many prefix positions have even parity and how many have odd parity. Initially, before processing the array, the empty prefix has even parity, so even count starts at 1 and odd at 0.
3. We iterate through the array and update the current parity. If the current element is negative, we flip the parity; otherwise, we keep it unchanged.
4. At each position, we decide how many subarrays ending here are positive or negative. If current parity is even, then subarrays ending here with positive product correspond to previous even prefixes, and negative ones correspond to previous odd prefixes. If current parity is odd, the roles swap.
5. We accumulate these counts into global answers.
6. After processing the element, we update the frequency of the current prefix parity so future positions can use it.

The reason this ordering matters is that subarrays ending at index $i$ depend on prefix information strictly before or including $i$, so updates must happen after counting contributions.

### Why it works

Each subarray $(l, r)$ corresponds to a pair of prefix states: the parity at $r$ and the parity just before $l$. The product sign depends only on whether these parities are equal or different. By counting how many prefixes of each type exist at every step, we implicitly count all valid subarrays exactly once. No subarray is missed because every endpoint is processed, and no subarray is double counted because each pair of prefixes defines exactly one segment.

## Python Solution

```
PythonRun
```

The code keeps a running parity of negatives and uses prefix counts to determine how many earlier prefixes combine with the current position to form positive or negative subarrays. The key subtlety is updating the answer before incrementing the prefix counter, ensuring the current position is not incorrectly counted as a prior prefix.

## Worked Examples

Consider the sample input:

```

```

We track prefix parity and counts.

| Index | Value | Parity | Even count | Odd count | Positive added | Negative added |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | 5 | 0 | 1 | 0 | 1 | 0 |
| 2 | -3 | 1 | 1 | 1 | 0 | 1 |
| 3 | 3 | 1 | 1 | 2 | 1 | 1 |
| 4 | -1 | 0 | 2 | 2 | 2 | 2 |
| 5 | 1 | 0 | 3 | 2 | 3 | 2 |

Final result is negative = 8, positive = 7.

This trace shows how each prefix state contributes combinatorially rather than individually enumerating subarrays.

A second example:

```

```

| Index | Value | Parity | Even count | Odd count | Positive added | Negative added |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | -1 | 1 | 1 | 1 | 0 | 1 |
| 2 | -1 | 0 | 2 | 1 | 2 | 1 |
| 3 | -1 | 1 | 2 | 2 | 2 | 2 |

Final answer: negative = 4, positive = 2.

This demonstrates how alternating parity naturally balances the counts.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n)$ | single pass through the array with constant-time updates |
| Space | $O(1)$ | only counters for parity and prefix counts |

The linear scan fits comfortably within constraints for $n \le 2 \cdot 10^5$, and memory usage is constant.

## Test Cases

```
PythonRun
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| all positive array | 0 10 | baseline combinatorics correctness |
| all negative array | 4 2 | parity handling |
| single positive | 0 1 | base case correctness |
| single negative | 1 0 | minimal negative case |

## Edge Cases

An all-positive array keeps parity fixed at zero throughout execution. Every subarray pairs with two even prefixes, so every segment contributes to the positive count. The algorithm correctly accumulates only positive contributions since the odd counter remains zero.

An all-negative array alternates parity at every step. For input `[-1, -1, -1]`, prefix parity flips each index, causing systematic mixing between even and odd prefix counts. The algorithm captures all pairings between differing parity states, producing exactly the expected number of negative subarrays while still counting positive ones formed by even-length segments.
