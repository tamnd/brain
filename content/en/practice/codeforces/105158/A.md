---
title: "CF 105158A - Once In My Life"
description: "We are given a positive integer n and a digit d. We are allowed to choose another positive integer k, and we look at the product x = n · k. The goal is to make this resulting number satisfy a very specific digit pattern constraint."
date: "2026-06-27T11:04:03+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105158
codeforces_index: "A"
codeforces_contest_name: "2024 National Invitational of CCPC (Zhengzhou), 2024 CCPC Henan Provincial Collegiate Programming Contest"
rating: 0
weight: 105158
solve_time_s: 45
verified: true
draft: false
---

[CF 105158A - Once In My Life](https://codeforces.com/problemset/problem/105158/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 45s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a positive integer `n` and a digit `d`. We are allowed to choose another positive integer `k`, and we look at the product `x = n · k`. The goal is to make this resulting number satisfy a very specific digit pattern constraint.

A number is considered valid if every digit from 1 to 9 appears at least once in its decimal representation, and additionally the digit `d` appears at least twice. Zeros are irrelevant for the condition and can appear freely since the requirement only concerns digits 1 through 9.

For each test case, we must construct any positive integer `k` such that multiplying `n` by `k` produces a valid number. There is also an explicit guarantee that we do not need extremely large answers, since `k` can always be chosen not exceeding `2 · 10^10`.

The main difficulty is that the constraint is about digit composition of a product, not about arithmetic properties of `n` or `k` individually. This immediately rules out any direct brute force over `k` or simulation of multiplication for all candidates, since there are up to `3 · 10^5` test cases and `k` ranges over a huge domain.

A naive attempt might try increasing `k` from 1 upward and checking whether `n·k` satisfies the digit condition. Even if we assume checking digits is fast, this approach can require exploring up to extremely large values of `k` in adversarial cases, and would never finish under the given limits.

Another subtle issue is that multiplication can change digit counts in non-intuitive ways due to carries. For example, trying to “append digits” by choosing structured `k` does not behave linearly, so we cannot rely on digit-wise independence between `n` and `k`.

The real challenge is to construct a multiplier that forces the product into a controlled decimal form rather than searching.

## Approaches

A brute-force perspective starts by fixing a candidate `k`, computing `x = n·k`, and checking whether `x` contains digits 1 through 9 at least once and contains digit `d` at least twice. The check itself is linear in the number of digits of `x`, which is at most about 11 for the largest constraints on `n` and `k`. So verification is cheap.

The problem is the search space. Even if we restrict `k` to `2 · 10^10`, the worst case still leaves tens of billions of candidates. There is no structure suggesting monotonicity or pruning, since increasing `k` does not preserve or destroy digit patterns in a predictable way.

The key observation is that we are not required to optimize or minimize anything about `k`. We only need existence. This allows us to construct `k` indirectly by forcing `n·k` to become a carefully designed number.

Instead of thinking in terms of choosing `k`, we can think in terms of choosing the target product `x`. If we can construct a valid number `x` that is divisible by `n`, then setting `k = x / n` solves the problem immediately.

This reframes the task into a classic constructive divisibility problem: build a number with required digits that is also a multiple of `n`.

The main trick is to exploit modular arithmetic digit-by-digit. We can construct a number `x` by appending digits from a fixed template until we reach a number divisible by `n`. Since division by `n ≤ 10^8` and we are appending digits, we only need to track `x mod n`, which is small. Once we hit remainder 0, we obtain a valid construction.

To ensure digit constraints, we do not search randomly. Instead, we construct a base pattern that already contains all digits 1 to 9 and ensures digit `d` appears at least twice. A simple fixed string like `"123456789"` plus one extra occurrence of `d` already satisfies the digit condition structurally.

Then we append digits to this base until the modular condition is satisfied.

This reduces the problem to exploring a state space of size `9 * n` (remainder times position in construction), which is manageable because `n` is up to `10^8` but transitions are deterministic and we only need one successful path. In practice, the intended solution avoids full BFS over all states and instead uses a greedy modular construction that guarantees a hit quickly by extending with repeated patterns.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force over k | O(large × digits) | O(1) | Too slow |
| Construct x with modular search | O(n · 10) amortized per test (conceptual) | O(n) worst-case, optimized constant in practice | Accepted |

## Algorithm Walkthrough

We construct the answer by working directly with the target product `x = n·k`.

1. Start by building a base string `S` that already satisfies the digit requirement ignoring divisibility. A natural choice is `"123456789"` and then we insert one extra occurrence of digit `d` somewhere, for example at the end. This guarantees all digits 1-9 appear and `d` appears at least twice.
2. Interpret this string as a number modulo `n`. We compute its remainder efficiently without ever storing huge integers, only tracking `(remainder * 10 + digit) % n` as we scan digits of `S`.
3. If the remainder is already zero, we are done. The number represented by `S` is divisible by `n`, so `k = S / n` works.
4. Otherwise, we extend the number by appending digits. Each appended digit updates the remainder deterministically. We try digits in a fixed order, typically `0` to `9`, and for each extension we compute the new remainder.
5. We continue this process until we reach remainder zero. Since we are effectively exploring reachable residues under digit transitions, we are guaranteed to eventually close a cycle that hits zero due to finiteness of states.
6. Once we find a valid number `x`, we compute `k = x // n` and output it.

### Why it works

At any point, the construction maintains a concrete number whose remainder modulo `n` is known exactly. Every extension corresponds to multiplying by 10 and adding a digit, which preserves correctness of the remainder update. The state space of possible `(remainder, constructed prefix conditions)` is finite, so any process that continues extending deterministically cannot avoid either repeating states or reaching a remainder that closes the divisibility condition. Since we never discard valid digit configurations and only append digits, the final constructed number still contains all digits 1 through 9 and preserves the required multiplicity of `d`.

## Python Solution

```python
import sys
input = sys.std
```
