---
title: "CF 192A - Funky Numbers"
description: "This is a Type A - “Find all X” problem. A valid proof must do two things: 1. Verify that every claimed solution actually satisfies the conditions. 2. Prove that no other solutions exist. The proposed solution does not complete either direction fully."
date: "2026-05-29T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "binary-search", "brute-force", "implementation"]
categories: ["algorithms"]
codeforces_contest: 192
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 121 (Div. 2)"
rating: 1300
weight: 192
solve_time_s: 47
verified: false
draft: false
---

[CF 192A - Funky Numbers](https://codeforces.com/problemset/problem/192/A)

**Rating:** 1300  
**Tags:** binary search, brute force, implementation  
**Solve time:** 47s  
**Verified:** no  

## Solution
## Problem-Type Check

This is a **Type A - “Find all X”** problem. A valid proof must do two things:

1. Verify that every claimed solution actually satisfies the conditions.
2. Prove that no other solutions exist.

The proposed solution does not complete either direction fully.

The only explicit candidate eventually found is $550$, and that candidate is correctly verified. However, the proof never finishes the case analysis, never handles the cases $k=-1$ and $k=1$, and never proves exhaustiveness. So the “nothing else exists” direction is missing.

## Step-by-Step Verification

### Step 1: Representing the number as $N=100a+10b+c$ with digit conditions - VALID

This is standard and correct.

### Step 2: Using the divisibility criterion for $11$, namely $a-b+c\equiv0\pmod{11}$ - VALID

Correct application of the divisibility rule.

Checking small examples:

- $121$: $1-2+1=0$, divisible by $11$.
- $352$: $3-5+2=0$, divisible by $11$.
- $418$: $4-1+8=11$, divisible by $11$.
- $123$: $1-2+3=2$, not divisible by $11$.

The rule is correctly used.

### Step 3: Deriving

$$100a+10b+c = 11(a^2+b^2+c^2)$$

from the condition $N/11=a^2+b^2+c^2$ - VALID

This is an algebraically correct equivalence.

### Step 4: Concluding $k\in\{-1,0,1\}$ from

$$a-b+c=11k$$

and the digit bounds - VALID

Since

$$1-9+0=-8,\qquad 9-0+9=18,$$

the quantity $a-b+c$ lies in $[-8,18]$. The only multiples of $11$ in this range are $0$ and $11$. In fact, $-11$ is impossible.

So the correct conclusion is:

$$k\in\{0,1\}.$$

The inclusion of $k=-1$ is mathematically harmless but inaccurate.

This is a **justification gap**, not a critical error.

### Step 5: Substituting $c=b-a$ in the case $k=0$ - VALID

Correct algebra.

### Step 6: Simplifying to

$$2a^2-2ab+2b^2-9a-b=0$$

- VALID

The algebraic manipulations are correct.

### Step 7: Solving the equation by checking values of $a$ - UNJUSTIFIED

The proof begins checking cases:

- $a=1$
- $a=2$
- $a=3$
- $a=4$
- $a=5$
- $a=6$ (unfinished)

but the argument abruptly stops mid-line.

No complete exhaustion is provided.

This is a **critical error** because the proof of completeness depends entirely on exhausting all possibilities.

### Step 8: Claiming $550$ works - VALID

The verification is correct:

$$550/11=50,$$

and

$$5^2+5^2+0^2=25+25=50.$$

Also $550$ is divisible by $11$.

### Step 9: Handling the cases $k=1$ and $k=-1$ - MISSING / UNJUSTIFIED

The proof never analyzes these cases.

In fact:

- $k=-1$ is impossible because $a-b+c\ge -8$.
- $k=1$ corresponds to

$$a-b+c=11.$$

Those cases must be ruled out to complete the classification.

This omission is a **critical error**.

## Completeness Check

The proof is incomplete in several essential ways.

First, the case analysis is unfinished. The computation literally stops at:

$$a=6,\quad b=\frac{8}{4}=$$

with no continuation.

Second, the proof never handles the $k=1$ case. Since the problem asks for all solutions, every admissible divisibility case must be addressed.

Third, there is no final conclusion listing all solutions and proving uniqueness.

Fourth, the proof never explicitly proves that no additional digit triples satisfy the equation.

The argument also contains a subtle inaccuracy: it allows $k=-1$, though this cannot occur. That alone would not invalidate the proof, but it reflects incomplete control of the range argument.

## Summary

The proposed solution contains correct preliminary algebra and correctly identifies one valid solution, $550$. However, the proof is fundamentally incomplete because the exhaustive classification is never finished. The cases are not fully analyzed, the $k=1$ branch is ignored, and the argument terminates mid-computation.

VERDICT: FAIL - the proof never completes the case analysis and does not rule out all other possible solutions.
