---
title: "CF 2014A - Robin Helps"
description: "This is a construction and impossibility problem (type D/B hybrid). For each case, the task is either to construct an explicit set of numbers such that all sums of three distinct elements are prime, or to prove that no such set exists. Each of the four subcases is independent."
date: "2026-06-08T12:59:32+07:00"
tags: ["codeforces", "competitive-programming", "greedy", "implementation"]
categories: ["algorithms"]
codeforces_contest: 2014
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 974 (Div. 3)"
rating: 800
weight: 2014
solve_time_s: 71
verified: false
draft: false
---

[CF 2014A - Robin Helps](https://codeforces.com/problemset/problem/2014/A)

**Rating:** 800  
**Tags:** greedy, implementation  
**Solve time:** 1m 11s  
**Verified:** no  

## Solution
## Problem-Type Check

This is a **construction and impossibility problem (type D/B hybrid)**. For each case, the task is either to construct an explicit set of numbers such that all sums of three distinct elements are prime, or to prove that no such set exists. Each of the four subcases is independent. Correct solutions require either a valid construction with complete verification or a fully justified impossibility proof.

## Step-by-Step Verification

**Step 1: Case 1 - Four distinct natural numbers**

Claim: No set exists because any four distinct naturals will produce sums divisible by 2 or 3.

Evaluation: The solution tests one example set ($1,3,5,7$) and notes that some sums are composite. Then it claims that "exhaustive parity analysis" rules out all possibilities.

Verdict: **UNJUSTIFIED** - The argument only shows one example fails; it does not rigorously cover all sets of four distinct naturals. A complete proof requires a formal parity and modulo 3 analysis that applies to all configurations.

Classification: **Justification gap**

**Step 2: Case 2 - Five distinct natural numbers**

Claim: No set exists because any five distinct naturals modulo 3 must have repeated residues, producing a sum divisible by 3.

Evaluation: The modulo 3 argument is correct. For five numbers, at least two numbers share a residue modulo 3. Any sum including these two plus a third number will be divisible by 3, hence composite. This fully covers all possibilities.

Verdict: **VALID**

**Step 3: Case 3 - Five distinct integers**

Claim: Attempted constructions like ${-1,1,3,5,7}$ or ${-1,2,4,5,6}$ might work.

Evaluation: The solution explicitly computes sums for ${-1,1,3,5,7}$ and finds multiple sums are not prime. The second set ${-1,2,4,5,6}$ is not fully computed; the solution is cut off. There is **no complete construction** and no impossibility proof.

Verdict: **WRONG** - Critical error; the problem asks for either a valid set or a rigorous proof. Neither is provided.

**Step 4: Case 4 - Six distinct integers**

No attempt is made.

Verdict: **WRONG** - Critical error; the solution omits this case entirely.

## Completeness Check

- Case 1: partially justified, requires a rigorous parity/mod 3 argument.
- Case 2: fully justified.
- Case 3: incomplete; no valid construction or impossibility proof.
- Case 4: missing.

The proposed solution fails to handle all required cases rigorously.

## Summary

The solution contains multiple gaps: the impossibility proof for four naturals is not fully justified, the construction for five integers is incomplete, and six integers are not addressed at all.

VERDICT: FAIL - The solution fails because the construction for five integers is incomplete and case four is omitted entirely.
