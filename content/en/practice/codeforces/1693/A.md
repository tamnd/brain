---
title: "CF 1693A - Directional Increase"
description: "The proposed solution answers the exercise that was actually asked. Exercise 3.4.2.10 asks for a modification of Algorithm R that eliminates the reservoir when the current sample of size $n$ can be stored directly in memory."
date: "2026-06-09T22:51:01+07:00"
tags: ["codeforces", "competitive-programming", "greedy"]
categories: ["algorithms"]
codeforces_contest: 1693
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 800 (Div. 1)"
rating: 1300
weight: 1693
solve_time_s: 150
verified: false
draft: false
---

[CF 1693A - Directional Increase](https://codeforces.com/problemset/problem/1693/A)

**Rating:** 1300  
**Tags:** greedy  
**Solve time:** 2m 30s  
**Verified:** no  

## Solution
## Correctness

The proposed solution answers the exercise that was actually asked. Exercise 3.4.2.10 asks for a modification of Algorithm R that eliminates the reservoir when the current sample of size $n$ can be stored directly in memory. The solution presents such a modification and describes the new state representation $S[1],\ldots,S[n]$.

The modified algorithm is operationally equivalent to Algorithm R. In Algorithm R, the reservoir exists only to retain the records currently represented by the sample indices. If the sample records themselves fit in memory, the index table and reservoir become unnecessary. Replacing the selected sample entry directly by the new record is exactly the same update that Algorithm R performs indirectly through $I[M]$ and the reservoir.

The correctness argument is essentially the standard proof of reservoir sampling. The solution shows that the new record enters the sample with probability $n/(t+1)$, that any existing sampled record is removed with probability $1/(t+1)$, and that a previously processed record remains in the sample with probability

$$\frac{n}{t}\cdot\frac{t}{t+1} = \frac{n}{t+1}.$$

Thus all $t+1$ records have equal probability $n/(t+1)$ of belonging to the sample after processing the next input record. Since the update rule is identical to Algorithm R except for storage representation, the sampling distribution is unchanged.

The algorithm therefore produces the same random sample as Algorithm R while eliminating both the reservoir and the index table.

## Gaps and Errors

There is one minor justification gap.

The solution states the stronger invariant that every one of the $\binom{t}{n}$ samples occurs with probability $1/\binom{t}{n}$, but the proof that follows establishes only the weaker statement that each individual record is present with probability $n/t$. Equal marginal probabilities do not by themselves imply uniformity over all $n$-subsets.

This is a **Justification gap**, not a critical error. The exercise asks for a modification of Algorithm R, not for a complete reproof of its uniformity. Since the modified algorithm performs exactly the same random replacement decisions as Algorithm R, the uniform distribution over samples is inherited directly from the correctness of Algorithm R. The solution explicitly appeals to this fact when it says that the correctness is identical to that of Algorithm R.

No step in the algorithm itself is wrong. No claim essential to the modification is false.

## Summary

The proposed solution gives the standard reservoir-sampling variant that stores only the current sample in memory. The algorithm is correct, the reservoir is genuinely eliminated, and the correctness argument is sufficient for the purpose of this exercise. The only weakness is that the stated stronger invariant is not fully reproved, although it follows immediately from the equivalence with Algorithm R.

VERDICT: PASS - the solution is correct and complete.
