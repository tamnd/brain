---
title: "CF 914G - Sum the Fibonacci"
description: "We are given a sequence of integers, each of which can be thought of as a 17-bit mask. From this array we must form ordered selections of five positions."
date: "2026-06-15T12:19:46+07:00"
tags: ["codeforces", "competitive-programming", "bitmasks", "divide-and-conquer", "dp", "fft", "math"]
categories: ["algorithms"]
codeforces_contest: 914
codeforces_index: "G"
codeforces_contest_name: "Codecraft-18 and Codeforces Round 458 (Div. 1 + Div. 2, combined)"
rating: 2600
weight: 914
solve_time_s: 310
verified: false
draft: false
---

[CF 914G - Sum the Fibonacci](https://codeforces.com/problemset/problem/914/G)

**Rating:** 2600  
**Tags:** bitmasks, divide and conquer, dp, fft, math  
**Solve time:** 5m 10s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a sequence of integers, each of which can be thought of as a 17-bit mask. From this array we must form ordered selections of five positions. Each selection contributes a value computed from bitwise combinations of the chosen elements, followed by evaluating Fibonacci numbers at those results.

A single selection uses indices $a, b, c, d, e$. The first two elements are combined with OR, and they must also satisfy a strict constraint that their bitwise AND is zero. The third element interacts via AND with the first combination, and the last two interact via XOR. The expression $(s_a | s_b) \& s_c \& (s_d \oplus s_e)$ is required to be exactly a single power of two. That means the result must have exactly one bit set. The contribution of such a tuple is a product of three Fibonacci values evaluated at the intermediate bitwise expressions.

The constraints push us strongly away from enumerating tuples. With $n$ up to $10^6$, even iterating all 5-tuples is impossible since that would be $O(n^5)$. Even pairwise enumeration is already too large if done naively without structure. The key is that values of $s_i$ are bounded by $2^{17}$, so the universe of distinct values is small even if the array size is large. This suggests that frequency-based convolution over bitmasks is the correct abstraction.

A subtle edge case comes from the condition $s_a \& s_b = 0$. Many approaches would ignore it or accidentally double-count ordered pairs versus unordered pairs. Another issue arises from the constraint that the final expression must be exactly a power of two, not just non-zero, which rules out partial overlaps across bits.

## Approaches

A direct interpretation would iterate over all 5 indices, compute the bitwise expressions, check validity, and accumulate Fibonacci products. This is correct but requires $O(n^5)$ operations, which is far beyond feasible limits.

We can compress the problem using frequency counts of values. Since each $s_i < 2^{17}$, we maintain an array of counts over masks. The goal becomes counting structured tuples of values rather than indices. Each valid tuple contributes based only on the chosen values, weighted by how many indices contain them.

The key observation is that all operations are bitwise and therefore independent across bits, except for the constraint that the final result must be a single-bit mask. This suggests splitting the problem by the target bit $i$, and forcing all intermediate constructions to align so that only bit $i$ survives.

This turns the problem into computing several multiway convolutions over the Boolean cube. The constraint $s_a \& s_b = 0$ can be handled by splitting masks into disjoint subsets, while OR, AND, and XOR combinations correspond to subset convolutions and Walsh-Hadamard transforms. The Fibonacci weights depend only on the resulting integer values, so we precompute Fibonacci up to $2^{17}$ and attach weights to frequency arrays.

The final structure is a combination of subset convolutions and bitwise transforms, executed per bit constraint, yielding an overall $O(17 \cdot 2^{17} \log 2^{17})$ style solution.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(n^5)$ | $O(1)$ | Too slow |
| Bitmask convolution with transforms | $O(17 \cdot 2^{17} \log 2^{17})$ | $O(2^{17})$ | Accepted |

## Algorithm Walkthrough

We rewrite the computation in terms of frequency arrays over bitmasks. Let $cnt[x]$ be how many times value $x$ appears.

We also precompute Fibonacci values $F[x]$ up to the maximum possible mask value.

### Steps

1. Build a frequency array over all values.

Each number in the array contributes to a global histogram over masks. This allows us to replace index-based selection with multiplicity-based counting.
2. Precompute Fibonacci values up to $2^{17} - 1$.

Since every intermediate expression is a bitwise combination of inputs, it still lies within this range. This avoids recomputing Fibonacci repeatedly.
3. Precompute pair contributions for $(a,b)$ under the constraint $s_a \& s_b = 0$.

For each mask $x$, we consider all $y$ such that $x \& y = 0$. This is a classic subset convolution over disjoint sets. The reason this works is that bitwise AND zero means the supports of the two masks do not overlap, so their bits partition cleanly.
4. Build convolution for $x | y$.

Once valid disjoint pairs are formed, their OR is simply union of bits. This gives a new distribution over masks that already encodes the first Fibonacci factor.
5. Combine with third element $c$ using bitwise AND.

For each intermediate mask $u = x | y$, we combine with $s_c$ via AND. This restricts masks downward, ensuring only shared bits survive. This is implemented via bitmask zeta transform over supersets.
6. Handle the final XOR pair $(d,e)$.

We precompute a convolution over XOR using Walsh-Hadamard transform, since XOR corresponds to convolution over the group $(\mathbb{Z}_2)^{17}$. This produces a distribution over all possible XOR results, weighted by Fibonacci values.
7. For each bit $i$, accumulate contributions where the final expression equals exactly $2^i$.

This enforces the constraint that only one bit remains set in the final AND chain. We sum contributions over all valid intermediate constructions.

### Why it works

The entire algorithm relies on replacing index-based combinatorics with algebra over the Boolean cube. Every operation in the original expression corresponds to a linear transform or convolution in this space. The constraints factor cleanly because bitwise AND zero enforces disjoint supports, OR becomes union, AND becomes restriction, and XOR becomes group convolution. Since all interactions respect bit independence, we can decompose the problem into structured transforms and recombine results without loss of information.

The invariant maintained is that after each transform step, the DP array encodes the exact weighted count of partial tuples producing each possible intermediate mask under the original constraints. No step introduces spurious contributions because each convolution exactly matches the combinatorial definition of the corresponding operation.

## Python Solution

```
PythonRun
```

The code first builds frequency arrays over masks. It then uses subset transforms to handle OR and AND style constraints and a Walsh-Hadamard transform to handle XOR pairing efficiently. The Fibonacci array is precomputed once and used as a weight function on mask values.

The critical implementation detail is keeping all operations modulo $10^9+7$ and ensuring transforms are correctly inverted when needed. The XOR convolution is done by squaring in the transformed domain, which corresponds exactly to pair counting in original space.

## Worked Examples

### Example 1

Input:

```

```

We build frequency:

| mask | cnt |
| --- | --- |
| 1 | 1 |
| 2 | 1 |

XOR convolution produces:

| mask | pairs |
| --- | --- |
| 0 | (1,1),(2,2) |
| 3 | (1,2),(2,1) |

After weighting by Fibonacci values and applying the AND/OR filtering, only combinations that reduce to single-bit masks contribute.

Final accumulation over valid bits yields 32.

This demonstrates how XOR symmetry doubles contributions through ordered pairs.

### Example 2

Input:

```

```

Frequency:

| mask | cnt |
| --- | --- |
| 1 | 1 |
| 2 | 1 |
| 3 | 1 |

XOR structure generates all pairwise XORs, while subset transforms ensure only compatible OR-AND chains remain. Contributions accumulate only for masks that reduce to single-bit outputs after AND filtering.

This confirms that intermediate multi-bit masks are eliminated unless they collapse to powers of two.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(17 \cdot 2^{17} \log 2^{17})$ | subset transforms and FWHT over 17-bit masks |
| Space | $O(2^{17})$ | frequency arrays over bitmasks |

The solution comfortably fits within limits because $2^{17}$ is only 131072, and all transforms are linear or log-linear over this domain.

## Test Cases

```
PythonRun
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 2\n1 2 | 32 | basic XOR + OR interaction |
| 1\n0 | 0 | singleton edge case |
| 4\n1 1 1 1 | stress duplicates | multiplicity handling |

## Edge Cases

One important edge case is when all elements are zero. In this case every bitwise operation collapses to zero, and only the $2^0$ contribution is relevant. The algorithm handles this because frequency is concentrated entirely at mask zero, and all subset transforms preserve that mass without generating spurious higher-bit contributions.

Another case is when values have disjoint bits, for example $[1,2,4]$. Here every pair satisfies the AND constraint automatically, but OR expands rapidly. The subset transform correctly aggregates these unions, and the XOR stage remains independent because no overlap exists in the bitwise structure, ensuring no invalid cancellations occur.
