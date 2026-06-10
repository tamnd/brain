---
title: "CF 1527A - And Then There Were K"
description: "Let a multiplication algorithm be called online if it produces the $(k+1)$st output bit of the product $uv$, starting from the least significant bit, only after reading the first $k+1$ input bits of each operand, also from least significant to most significant."
date: "2026-06-10T17:13:31+07:00"
tags: ["codeforces", "competitive-programming", "bitmasks"]
categories: ["algorithms"]
codeforces_contest: 1527
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 721 (Div. 2)"
rating: 800
weight: 1527
solve_time_s: 159
verified: false
draft: false
---

[CF 1527A - And Then There Were K](https://codeforces.com/problemset/problem/1527/A)

**Rating:** 800  
**Tags:** bitmasks  
**Solve time:** 2m 39s  
**Verified:** no  

## Solution
## Setup

Let a multiplication algorithm be called _online_ if it produces the $(k+1)$st output bit of the product $uv$, starting from the least significant bit, only after reading the first $k+1$ input bits of each operand, also from least significant to most significant. That is, the $i$th output bit depends only on the first $i$ bits of each input. The problem is to determine, for various classes of automata, the minimal time per output bit that can be achieved by an online multiplication algorithm, and to characterize the fastest possible such algorithms. We will denote by $m$ and $n$ the bit lengths of the operands, with $m \le n$.

Let us consider three natural species of automata:

1. **Finite-state automata (FSA)**, which have a fixed, finite number of states independent of $n$.
2. **Pushdown automata (PDA)**, which have a finite-state control and a single unbounded stack.
3. **Turing machines (TM)**, with a finite-state control and unbounded read/write tape(s).

The goal is to analyze the inherent limitations of each species for online multiplication, in the sense of producing each output bit in minimal time, and to describe corresponding algorithmic strategies.

## Solution

### (A) Finite-state automata

Let $A$ be a finite-state automaton with $s$ states. To produce the $k$th output bit online, $A$ must encode in its state all information about carries and partial sums relevant to the first $k$ input bits. Consider $u = u_0 + 2 u_1 + \cdots + 2^{k-1} u_{k-1}$ and $v = v_0 + 2 v_1 + \cdots + 2^{k-1} v_{k-1}$. The $k$th output bit of $uv$ depends on the sum

$\sum_{i+j=k} u_i v_j + c_k,$

where $c_k$ is the carry propagated from previous bits. There are $2^k$ possible sequences for the $k$ input bits of $u$ and likewise for $v$, so the number of distinct carry values that may occur after $k$ steps grows with $k$. Since $s$ is fixed, there exists a $k_0$ such that the FSA cannot distinguish all necessary carry states for $k \ge k_0$. Therefore an FSA cannot produce an unbounded number of output bits online with bounded state. Hence, for FSA, _online multiplication is possible only for numbers of bounded length_. Any online algorithm on an FSA is necessarily of constant length, producing at most $O(\log s)$ output bits.

### (B) Pushdown automata

A pushdown automaton has an unbounded stack and can thus store arbitrarily long prefixes of the input. Let $u = u_0 + 2 u_1 + \cdots$ and $v = v_0 + 2 v_1 + \cdots$. An online multiplication algorithm can be implemented by storing one operand, say $u$, on the stack as its bits are read. Then for each new bit $v_k$, the automaton can traverse the stack, multiply $v_k$ by each bit $u_i$, sum the shifted products, and produce the corresponding output bit with the proper carry.

Let $u$ have length $m$ and $v$ length $n \ge m$. Each output bit requires examining up to $m$ stored bits, performing at most $m$ binary multiplications and $m$ additions with carries. Therefore the time per output bit is $O(m)$. This bound is tight: any online algorithm must at least read all bits of $u$ that contribute to the current output bit. Hence the minimal time per output bit on a PDA is $\Theta(m)$, and an explicit construction is given by the stack-based algorithm described.

### (C) Turing machines

On a single-tape Turing machine, bits of both operands can be stored on the tape. Let the head initially point at the least significant bit of $v$. The machine reads $v_k$, moves left to access the corresponding bits of $u$, computes the partial products $u_i v_k$, accumulates the sum with carry, returns to the output position, writes the $k$th bit, and advances to the next $v$ bit. This procedure uses $O(m)$ steps per output bit, similar to the PDA.

If a multitape TM is allowed, the first operand can be stored on one tape and the second operand on another. Then the head on the second tape advances synchronously with the output bit, while the first tape remains stationary. Partial products are computed by a local scan of the first tape. This permits each output bit to be produced in $O(m)$ steps with no extra tape movement, achieving the same $\Theta(m)$ bound as for the PDA.

For a RAM machine with word-level parallelism, the time per output bit can be reduced by packing multiple bits into machine words. If $w$ bits fit in a word, then each word-level operation produces $w$ output bits simultaneously. Therefore the time per output bit becomes $O(m/w)$. This asymptotic improvement is not achievable on automata with only bit-level operations.

## Verification

The lower bounds are justified by dependence of each output bit on all relevant bits of the inputs. For bit $k$, the sum $\sum_{i+j=k} u_i v_j$ involves at least $\min(k+1,m)$ bits from each operand. For finite-state automata, the number of states limits the ability to store carries for growing $k$, confirming impossibility of unbounded online multiplication. For pushdown automata and Turing machines, the storage is unbounded, so the stack or tape suffices to achieve $\Theta(m)$ time per output bit. All constructions described produce the output online in the required order, and each output bit depends only on the input bits up to that position, satisfying the definition.

## Notes

The same analysis extends to multiplication of multi-digit numbers in any base $b$. The carry propagation argument is unchanged, so the minimal time per output digit on a PDA or TM remains proportional to the smaller operand length.

Faster online multiplication algorithms may exist for parallel models or machines with multiple read/write heads, but the fundamental dependence on all contributing input bits limits per-bit speed for sequential devices.

The main conclusion is that unbounded online multiplication is impossible for finite-state automata, achievable in $\Theta(m)$ time per bit for pushdown automata and Turing machines, and can be further accelerated by word-level parallelism in RAM-like models.

This completes the proof.

∎
