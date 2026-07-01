---
title: "CF 104091C - \u0411\u0443\u0434\u044c \u043d\u0430\u0447\u0435\u043a\u0443!"
description: "We need to count how many decimal numbers with exactly n digits satisfy a special adjacency rule. A number is called beautiful if every pair of neighboring digits forms a two digit number divisible by 3."
date: "2026-07-02T02:27:54+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104091
codeforces_index: "C"
codeforces_contest_name: "\u041c\u0443\u043d\u0438\u0446\u0438\u043f\u0430\u043b\u044c\u043d\u044b\u0439 \u044d\u0442\u0430\u043f \u0412\u041e\u0428 \u043f\u043e \u0438\u043d\u0444\u043e\u0440\u043c\u0430\u0442\u0438\u043a\u0435 \u0432 \u041f\u0435\u0442\u0440\u043e\u0437\u0430\u0432\u043e\u0434\u0441\u043a\u0435 \u0438 \u041a\u0430\u0440\u0435\u043b\u0438\u0438 2022-2023"
rating: 0
weight: 104091
solve_time_s: 41
verified: true
draft: false
---

[CF 104091C - \u0411\u0443\u0434\u044c \u043d\u0430\u0447\u0435\u043a\u0443!](https://codeforces.com/problemset/problem/104091/C)

**Rating:** -  
**Tags:** -  
**Solve time:** 41s  
**Verified:** yes  

## Solution
## Problem Understanding

We need to count how many decimal numbers with exactly `n` digits satisfy a special adjacency rule.

A number is called beautiful if every pair of neighboring digits forms a two digit number divisible by `3`. For example, `12754` is beautiful because `12`, `27`, `75`, and `54` are all divisible by `3`. On the other hand, `1221` is not beautiful because `22` is not divisible by `3`.

The first digit cannot be zero because the number must have exactly `n` digits. Every remaining digit may be zero if the divisibility condition is satisfied.

The input contains a single integer `n`, where `2 ≤ n ≤ 27`. The output is the total number of beautiful `n` digit numbers.

The value of `n` is extremely small. Even an algorithm with complexity proportional to `n × 100` or `n × 1000` easily fits within the limits. Exhaustively checking every `n` digit number is impossible because there are `9 × 10^(n-1)` candidates. For the largest value, `n = 27`, this is roughly `9 × 10^26` numbers, far beyond any realistic computation.

One subtle case is the first digit. For example, when `n = 2`, the number `03` satisfies the adjacency rule because `03 = 3` is divisible by `3`, but it is not a valid two digit number. The algorithm must forbid leading zeros.

Another easy mistake is misunderstanding the condition. The pair `75` is divisible by `3`, but neither digit individually has any special property. For example, `12` is valid because `12` is divisible by `3`, while `13` is not because `13 % 3 = 1`.

A more interesting observation comes from divisibility by `3`. Since

```
10a + b ≡ a + b (mod 3),
```

a pair is divisible by `3` exactly when the two digits have residues whose sum is divisible by `3`. The actual decimal value never needs to be computed.

## Approaches

The most direct solution is to generate every `n` digit number, test every adjacent pair, and count the valid ones. This is obviously correct because every candidate is examined independently. Unfortunately, the running time is proportional to `9 × 10^(n-1)`, which becomes roughly `10^27` operations in the worst case.

The condition only relates neighboring digits. Once the previous digit is fixed, earlier digits no longer matter. This is exactly the situation where dynamic programming over the last digit is effective.

The key observation is that divisibility by `3` depends only on the residues of two neighboring digits. We can build the number from left to right while remembering only the final digit. If we already know how many valid prefixes end with digit `d`, then every digit `x` satisfying `(10d + x) % 3 == 0` can extend those prefixes.

There are only ten possible last digits, so every layer of the dynamic program contains only ten states. Each state tries at most ten transitions, giving only about one hundred operations per digit.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(10ⁿ × n) | O(1) | Too slow |
| Optimal DP | O(n × 100) | O(10) | Accepted |

## Algorithm Walkthrough

1. Create an array `dp` of size `10`, where `dp[d]` stores the number of valid prefixes ending with digit `d`.
2. Initialize the first digit. Digits `1` through `9` each form one valid prefix of length `1`, so set `dp[1]` through `dp[9]` to `1`. Leave `dp[0]` equal to `0` because leading zeros are forbidden.
3. Repeat `n - 1` times, once for every remaining position.
4. Create a fresh array `next_dp` filled with zeros.
5. For every possible previous digit `a` and every possible next digit `b`, check whether `(10 * a + b) % 3 == 0`. If it is, every valid prefix ending in `a` can be extended by `b`, so add `dp[a]` to `next_dp[b]`.
6. Replace `dp` with `next_dp`.
7. After processing all positions, sum every value in `dp`. Each state represents valid numbers ending in a different final digit, so their sum is the required answer.

### Why it works

The dynamic programming invariant is that after processing `k` digits, `dp[d]` equals the number of valid `k` digit prefixes whose final digit is `d`.

The initialization is correct because every nonzero digit forms exactly one valid prefix of length one.

During a transition, every extension is considered exactly once. A transition is allowed precisely when the newly created adjacent pair is divisible by `3`. No invalid extension is added, and no valid extension is omitted.

By induction on the processed length, the invariant remains true after every iteration. After all `n` digits have been processed, every beautiful `n` digit number belongs to exactly one state according to its last digit, so summing all states gives the correct answer.

## Python Solution

```python
import sys
input = sys.stdin.readline

n = int(input())

dp = [0] * 10
for d in range(1, 10):
    dp[d] = 1

for _ in range(n - 1):
    ndp = [0] * 10
    for a in range(10):
        if dp[a] == 0:
            continue
        for b in range(10):
            if (10 * a + b) % 3 == 0:
                ndp[b] += dp[a]
    dp = ndp

print(sum(dp))
```

The initialization represents all possible one digit prefixes. Digit zero is excluded because the final number must contain exactly `n` digits.

Each iteration extends the prefixes by one digit. A fresh array is used because transitions for the current position must not affect other transitions within the same layer.

Skipping states whose count is zero is not required for correctness, but it avoids unnecessary work.

Python integers automatically grow to arbitrary size, so the answer fits even though it may exceed the range of a 32 bit integer.

## Worked Examples

### Example 1

Input

```
2
```

Initialization:

| Length | dp (nonzero entries) |
| --- | --- |
| 1 | 1:1 2:1 3:1 4:1 5:1 6:1 7:1 8:1 9:1 |

After processing the second digit:

| Previous digit | Allowed next digits |
| --- | --- |
| 1 | 2, 5, 8 |
| 2 | 1, 4, 7 |
| 3 | 0, 3, 6, 9 |
| 4 | 2, 5, 8 |
| 5 | 1, 4, 7 |
| 6 | 0, 3, 6, 9 |
| 7 | 2, 5, 8 |
| 8 | 1, 4, 7 |
| 9 | 0, 3, 6, 9 |

The final counts sum to `30`.

This example shows that every extension depends only on the previous digit, not on the entire
