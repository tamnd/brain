---
title: "CF 104262C - Calibration Complications"
description: "The five-letter word pairing scheme in Section 7.2.1.1 relies on masking a packed bitstring so that each mask isolates the lower portion of a word consisting of an integral number of fixed-size letter fields."
date: "2026-07-01T21:35:13+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104262
codeforces_index: "C"
codeforces_contest_name: "UTPC Contest 03-24-23 Div. 1 (Advanced)"
rating: 0
weight: 104262
solve_time_s: 62
verified: false
draft: false
---

[CF 104262C - Calibration Complications](https://codeforces.com/problemset/problem/104262/C)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 2s  
**Verified:** no  

## Solution
## Solution

The five-letter word pairing scheme in Section 7.2.1.1 relies on masking a packed bitstring so that each mask isolates the lower portion of a word consisting of an integral number of fixed-size letter fields. In the standard construction each letter occupies $5$ bits, so a word is partitioned into blocks of size $5$, and the $j$th mask is designed to extract exactly the lowest $5(j+1)$ bits.

In that setting the correct masks have the form

$$m_j = z \,\&\, (2^{5j+5}-1),$$

since the binary number $2^{5j+5}-1$ consists of $5(j+1)$ consecutive $1$ bits, and therefore preserves exactly the lowest $5(j+1)$ bits of $z$ while clearing all higher bits.

The proposed modification replaces this by

$$m_j = z \,\&\, (25j+5 - 1).$$

Interpreting this in the intended bit-manipulation sense requires reading $25j+5$ as $2^{5j+5}$, since only a power of two produces a mask consisting of a contiguous block of low-order $1$ bits. Under this interpretation,

$$25j+5 - 1 = 2^{5j+5}-1,$$

so each $m_j$ extracts exactly the same set of low-order bits as in the original scheme.

The correctness of the pairing scheme depends only on the nesting property of the masks,

$$m_0 \subset m_1 \subset m_2 \subset \cdots,$$

meaning that each successive mask retains all bits retained by the previous one and adds a fixed additional block of $5$ bits. Both the original masks and the modified masks satisfy this property because

$$2^{5(j+1)}-1 = (2^{5j+5}-1) + 2^{5j+5},$$

which appends a disjoint higher block of $5$ bits.

Since all subsequent steps in the scheme depend only on consistent isolation of successive 5-bit fields and not on any arithmetic identity beyond these bit partitions, replacing the original masks by the modified ones leaves every intermediate extraction unchanged. Every grouped 5-bit letter remains aligned, and no cross-field interference occurs.

Therefore the algorithm produces exactly the same decomposition of the packed word into five-letter blocks and yields the same pairing results as the original construction.

This completes the proof. ∎
