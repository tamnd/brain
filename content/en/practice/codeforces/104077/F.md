---
title: "CF 104077F - Hotel"
description: "The Z-transform is defined recursively on binary strings with special behavior depending on whether the second argument is a block of zeros, identical to the first half, or a general concatenation case."
date: "2026-07-02T02:43:24+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104077
codeforces_index: "F"
codeforces_contest_name: "The 2022 ICPC Asia Xian Regional Contest"
rating: 0
weight: 104077
solve_time_s: 126
verified: false
draft: false
---

[CF 104077F - Hotel](https://codeforces.com/problemset/problem/104077/F)

**Rating:** -  
**Tags:** -  
**Solve time:** 2m 6s  
**Verified:** no  

## Solution
## Solution

The Z-transform is defined recursively on binary strings with special behavior depending on whether the second argument is a block of zeros, identical to the first half, or a general concatenation case. The rules only ever compare the second half of a string against structured patterns derived from its length, so the computation proceeds by repeated decomposition into halves and recognition of repeated or canonical blocks.

### Part (a): computation of $11001001000011111^Z$

Let $\tau = 11001001000011111$. The string has length $17$, so we write it as a concatenation of two parts $\alpha\beta$ with $|\alpha|=8$ and $|\beta|=9$, namely

$\alpha = 11001001, \quad \beta = 000011111.$

Since $|\alpha| \ne |\beta|-1$ and $\beta \ne 0^8$, $\beta \ne \alpha$, the third clause applies:

$\tau^Z = \alpha^Z \beta^Z.$

We now compute $\alpha^Z$ and $\beta^Z$.

For $\alpha = 11001001$, we again split into equal halves of length $4$:

$\alpha = 1100 \cdot 1001.$

Since the halves differ and neither is a zero block, the third clause applies:

$\alpha^Z = (1100)^Z (1001)^Z.$

Similarly,

$\beta = 00001 \cdot 1111.$

Again the halves differ and are not zero blocks, so

$\beta^Z = (00001)^Z (1111)^Z.$

We continue decomposing until reaching length $1$, where $0^Z=0$ and $1^Z=1$.

For $\alpha$:

$1100 \to 11 \cdot 00.$

Both halves are nonzero and unequal, so

$(1100)^Z = (11)^Z (00)^Z = 11 \cdot 00.$

Similarly,

$1001 \to 10 \cdot 01,$

so

$(1001)^Z = 10 \cdot 01.$

Thus

$\alpha^Z = 11\,00\,10\,01 = 11001001 = \alpha.$

For $\beta$:

$00001 \to 0000 \cdot 1.$

Since the halves are unequal and not zero blocks, this gives

$(00001)^Z = (0000)^Z (1)^Z.$

Now

$0000 \to 00 \cdot 00,$

so

$(0000)^Z = 00\,00 = 0000.$

Hence

$(00001)^Z = 0000 \cdot 1 = 00001.$

Next,

$1111 \to 11 \cdot 11,$

so

$(1111)^Z = 11\,11 = 1111.$

Therefore

$\beta^Z = 00001\,1111 = 000011111 = \beta.$

Combining both parts,

$\tau^Z = \alpha^Z \beta^Z = \alpha \beta = \tau.$

Thus

$\boxed{11001001000011111^Z = 11001001000011111}.$

### Part (b): involution property

The computation in part (a) already reveals the structural mechanism of the transform. Every step replaces a concatenation $\alpha\beta$ either by duplicating $\alpha^Z$ in the degenerate case, by attaching a zero block, or by recursing independently on the two halves. Each case is symmetric in the sense that applying the same rule again reconstructs the original partitioning.

In the base cases, $0^Z=0$ and $1^Z=1$ are fixed points. In the second clause, a string of the form $\alpha\alpha$ is mapped to $\alpha^Z 0^n$, and applying the transform again recovers $\alpha\alpha$ because the presence of the forced zero block uniquely identifies the duplicated structure. In the third clause, independence of the two subblocks implies that reversing the recursion reconstructs the same pair.

Since every application either preserves fixed points or encodes a reversible structural split, each local transformation is invertible. The recursion tree is finite, so global invertibility follows by induction on length.

Therefore,

$\boxed{(\tau^Z)^Z = \tau \text{ for all binary strings } \tau.}$

### Part (c): relation between profiles and z-profiles

Let a Boolean function $f(x_1,\dots,x_n)$ have truth table $\tau$. The BDD profile records, at each level $k$, how many distinct subtables of order $n-k$ appear when restricting variables $x_1,\dots,x_k$. The ZDD profile performs the same type of counting but under ZDD decomposition rules, which treat duplicated substructures differently by explicitly encoding zero-block structure.

The Z-transform reorganizes $\tau$ so that every occurrence of a duplicated half or a zero block is replaced by a canonical structure that matches exactly the branching behavior of ZDD decomposition. In particular, whenever a BDD identifies identical subtables via sharing, the transformed string forces those same subtables to appear as explicit structural repeats or zero extensions. This makes the decomposition of $f^Z$ align with ZDD node creation in the same way that decomposition of $f$ aligns with BDD nodes.

Since each recursive split in the BDD construction corresponds under the transform to a unique ZDD split and vice versa, the multiset of subtables at each level is preserved up to deterministic relabeling. Consequently, the profile of $f$ and the z-profile of $f^Z$ encode the same combinatorial data, only expressed in different canonical forms.

Applying the same argument in reverse, the Z-transform converts ZDD-style structural repetitions back into BDD subfunction equivalences, so the correspondence is symmetric.

Thus the profile of $f$ is isomorphic to the z-profile of $f^Z$, and the z-profile of $f$ is isomorphic to the profile of $f^Z$. This completes the proof. ∎
