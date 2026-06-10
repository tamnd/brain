---
title: "CF 1562E - Rescue Niwen!"
description: "Program M computes a double-precision product by expanding each normalized operand into high and low halves, forming four partial products, then discarding all terms that lie strictly to the right of the retained word boundary."
date: "2026-06-10T12:10:59+07:00"
tags: ["codeforces", "competitive-programming", "dp", "greedy", "string-suffix-structures", "strings"]
categories: ["algorithms"]
codeforces_contest: 1562
codeforces_index: "E"
codeforces_contest_name: "Codeforces Round 741 (Div. 2)"
rating: 2500
weight: 1562
solve_time_s: 177
verified: false
draft: false
---

[CF 1562E - Rescue Niwen!](https://codeforces.com/problemset/problem/1562/E)

**Rating:** 2500  
**Tags:** dp, greedy, string suffix structures, strings  
**Solve time:** 2m 57s  
**Verified:** no  

## Solution
## Solution

Program M computes a double-precision product by expanding each normalized operand into high and low halves, forming four partial products, then discarding all terms that lie strictly to the right of the retained word boundary. The only arithmetic operations that combine values are additions of aligned partial results inside fixed byte fields.

Overflow in MIX double-precision arithmetic refers to a carry propagating beyond the most significant retained byte of a word, thereby corrupting the sign or exponent fields stored in that word. In Program M, every addition step is structured so that any potential carry either remains within the designated byte field or is absorbed into a higher-order partial product that has already been positioned to account for it.

The structure of the multiplication is such that each operand is decomposed into two parts, a most significant part $u_m$ and a least significant part $u_l$, and similarly $v_m$ and $v_l$. The product expands into four contributions:

$$u_m v_m,\quad u_m v_l,\quad u_l v_m,\quad u_l v_l.$$

These terms are aligned in memory so that their byte boundaries correspond exactly to their positional significance in the final double-precision word. The least significant product $u_l v_l$ is placed entirely to the right of the retained region and is discarded without being added into the result, so it cannot induce overflow.

The mixed products $u_m v_l$ and $u_l v_m$ are shifted so that their highest possible contribution still fits strictly below the highest retained byte boundary. Since each operand is normalized, each fraction component lies in a bounded interval determined by the base $b$ representation, so each partial product is strictly less than $b^2$ times a normalized digit. The alignment in Program M ensures that when these shifted values are added, their sum cannot exceed one byte of carry beyond the allocated field.

The most significant term $u_m v_m$ is added last. Both $u_m$ and $v_m$ are normalized leading parts, so their product lies strictly below the overflow threshold of the floating-point representation used for the leading word. The program relies on the fact that multiplication of normalized fractions produces a result whose leading byte is strictly less than the base, so no carry can propagate beyond the exponent-adjusted boundary.

The only additions performed in Program M are additions of aligned byte fields that were constructed so that any carry from a lower byte is absorbed into the immediately higher byte of the same double-precision word. Since no addition ever places a carry into a field outside the allocated exponent-plus-fraction structure, and since the highest-order field has no higher field into which a carry could propagate, no overflow can occur.

This completes the proof. ∎
