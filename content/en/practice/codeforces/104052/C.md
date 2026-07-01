---
title: "CF 104052C - Sliding Dominoes"
description: "The solution answers all parts, but part (b) is incorrect and breaks subsequent reasoning. The error comes from an incorrect application of the quotient definition: it wrongly assumes that $alpha in f/e2$ must itself belong to $f$, which is not required."
date: "2026-07-02T03:40:21+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104052
codeforces_index: "C"
codeforces_contest_name: "Innopolis Open 2022-2023. First qualification round"
rating: 0
weight: 104052
solve_time_s: 101
verified: false
draft: false
---

[CF 104052C - Sliding Dominoes](https://codeforces.com/problemset/problem/104052/C)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 41s  
**Verified:** no  

## Solution
## Correctness

The solution answers all parts, but part (b) is incorrect and breaks subsequent reasoning. The error comes from an incorrect application of the quotient definition: it wrongly assumes that $\alpha \in f/e_2$ must itself belong to $f$, which is not required. This leads to an incorrect result for $f/e_2$, and therefore an incorrect conclusion for $f/(f/e_2)$.

Parts (a), (c), (e) are essentially correct, and (d), (f), (g) are mostly repaired in structure, though (d) still contains informal justification. However, the failure in (b) is decisive.

## Gaps and Errors

### (b) Incorrect computation of $f/e_2$ (Critical error)

The solution asserts that $\alpha \cup \{2\} \in f$ must be checked only against elements whose singleton difference $\alpha$ already lies in $f$, and therefore rejects $\alpha = \{1\}$. This is incorrect.

By definition,

$$\alpha \in f/e_2 \iff \alpha \cap \{2\} = \varnothing \;\text{and}\; \alpha \cup \{2\} \in f.$$

There is no requirement that $\alpha \in f$.

Checking correctly:

- $\alpha = \varnothing$: $\{2\} \in f$, valid.
- $\alpha = \{1\}$: $\{1\} \cap \{2\} = \varnothing$ and $\{1,2\} \in f$, valid.
- $\alpha = \{3\}, \{4\}$: fail since unions with $\{2\}$ are not in $f$.

Thus the correct result is:

$$f/e_2 = \{\varnothing, \{1\}\}.$$

The solution’s omission of $\{1\}$ invalidates all subsequent computations depending on this value.

## Summary

The solution is structurally improved, but part (b) contains a fundamental misinterpretation of the quotient definition, producing an incorrect result.

VERDICT: FAIL - incorrect computation of $f/e_2$ due to an invalid extra constraint requiring $\alpha \in f$.
