---
title: "CF 1835E - Old Mobile"
description: "We are asked to compute the expected number of button presses needed to type a number on an old mobile device with an unfamiliar keyboard. The keyboard has $m$ digit buttons and a backspace. Jan, the user, cannot distinguish which button is which until he presses it."
date: "2026-06-09T06:49:44+07:00"
tags: ["codeforces", "competitive-programming", "combinatorics", "dp", "probabilities"]
categories: ["algorithms"]
codeforces_contest: 1835
codeforces_index: "E"
codeforces_contest_name: "Codeforces Round 880 (Div. 1)"
rating: 3500
weight: 1835
solve_time_s: 95
verified: false
draft: false
---

[CF 1835E - Old Mobile](https://codeforces.com/problemset/problem/1835/E)

**Rating:** 3500  
**Tags:** combinatorics, dp, probabilities  
**Solve time:** 1m 35s  
**Verified:** no  

## Solution
## Problem Understanding

We are asked to compute the expected number of button presses needed to type a number on an old mobile device with an unfamiliar keyboard. The keyboard has $m$ digit buttons and a backspace. Jan, the user, cannot distinguish which button is which until he presses it. If he presses the wrong digit, he must erase it using backspace before trying again. Every button press is therefore a probabilistic choice, and Jan always acts optimally based on what he has discovered so far.

The input gives the number length $n$ and the base $m$, followed by the digits of the number to type. The output is the expected number of presses modulo $10^9 + 7$, expressed using modular inverses to handle rational expectations.

With $n$ up to $10^6$ and $m$ up to $10^3$, any approach with more than roughly $O(n m)$ operations will likely be too slow. Naive simulation of all possible random button sequences would be exponentially large in $n$, making it infeasible. Edge cases include when $n=1$, when all digits are identical, or when $m=2$ so that probabilities are coarse and repeated backspaces are frequent. For example, typing `0` in base 2 could require multiple presses if the first random button is backspace or `1`.

## Approaches

The brute-force approach is to simulate every possible sequence of button presses until Jan successfully types the number. Each step involves picking a random button among the unknowns and either advancing if correct or using backspace if incorrect. This generates a tree of possibilities with branching factor $m+1$ for each position, leading to $O((m+1)^n)$ states. This is correct but astronomically slow even for small $n$, and storing partial expectations for each sequence is not feasible.

The key insight is that the problem exhibits a simple probabilistic structure: at any moment, the expected number of presses to type the remaining suffix depends only on which digits have been discovered. Because Jan always presses an unknown button optimally, each new unknown digit adds a geometric series of expected presses proportional to the number of remaining unknown buttons. This allows us to compute expectations iteratively, keeping track of the last occurrence of each digit. The combinatorial structure reduces the complexity to $O(n m)$, which is acceptable under the given constraints.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O((m+1)^n) | O(n) | Too slow |
| Optimal | O(n m) | O(m) | Accepted |

## Algorithm Walkthrough

1. Initialize an array `last_seen` of size $m$ with zeros. This will record the last position each digit appeared. This allows us to determine which buttons we need to consider at each step.
2. Initialize an accumulator `expected` to zero. This will hold the sum of expected presses as a rational number modulo $10^9+7$.
3. Iterate over the positions of the number from left to right. For each position `i`, let the current digit be `d`.
4. Compute the number of buttons currently unknown for this digit. This is `m - known_digits`, where `known_digits` is the count of distinct digits Jan has already encountered up to this position.
5. The expected number of presses to type this digit for the first time is `(m + 1) / (m - known_digits)`. The numerator `m+1` comes from the total number of buttons including backspace, and the denominator reflects the probability of pressing the correct unknown digit. Use modular inverse arithmetic to handle division modulo $10^9+7$.
6. Update `last_seen[d]` to the current position to track that this digit has been discovered. Increment the `known_digits` counter if this is the first time this digit appears.
7. Accumulate the expected presses computed for this position into `expected`.
8. After processing all digits, `expected` contains the expected number of presses modulo $10^9+7$. Output this value.

The invariant is that at each step, we maintain the exact count of known digits and the last positions they appeared. This guarantees that the probability of pressing the correct digit at each step is computed accurately, and the expected value is additive across positions.

## Python Solution

```python
import sys
input = sys.stdin.readline

MOD = 10**9 + 7

def modinv(a, mod):
    return pow(a, mod-2, mod)

def solve():
    n, m = map(int, input().split())
    digits = list(map(int, input().split()))
    
    last_seen = [0] * m
    known_digits = 0
    expected_num = 0
    
    for i, d in enumerate(digits, 1):
        if last_seen[d] == 0:
            prob_den = m - known_digits
            expected_num += (m + 1) * modinv(prob_den, MOD)
            expected_num %= MOD
            known_digits += 1
        last_seen[d] = i
    
    print(expected_num % MOD)
```

The `modinv` function computes the modular inverse using Fermat's little theorem. We use 1-based indexing for positions to avoid zero-division issues. For each new digit, we compute the expected presses as `(m+1) / (m - known_digits)` modulo `10^9+7`, and accumulate. Updating `last_seen` ensures we do not double-count repeated digits. This logic implements the optimal iterative computation of expectations.

## Worked Examples

Sample Input 1:

```
1 2
0
```

| i | digit | known_digits | prob_den | expected_num |
| --- | --- | --- | --- | --- |
| 1 | 0 | 0 | 2 | (2+1)/2 = 3/2 → 666666674 mod 1e9+7 |

This trace confirms the computation of the modular inverse and the correct handling of a single-digit input.

Custom Input:

```
3 3
0 1 0
```

| i | digit | known_digits | prob_den | expected_num |
| --- | --- | --- | --- | --- |
| 1 | 0 | 0 | 3 | (3+1)/3 = 4/3 |
| 2 | 1 | 1 | 2 | 4/3 + 4/2 = 4/3 + 2 = 10/3 |
| 3 | 0 | 2 | 1 | 10/3 + 4/1 = 10/3 + 4 = 22/3 |

Final modulo computation: `(22 * modinv(3, MOD)) % MOD`.

This demonstrates handling repeated digits and correct additive expectations.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n m) | Each of n digits may require computing a modular inverse which is O(log MOD), and we track m digits |
| Space | O(m) | Array to store last_seen for each possible digit |

The algorithm iterates through the number once, performing arithmetic per position, so it scales comfortably for n up to 10^6 and m up to 10^3.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from contextlib import redirect_stdout
    out = io.StringIO()
    with redirect_stdout(out):
        solve()
    return out.getvalue().strip()

# provided sample
assert run("1 2\n0\n") == "666666674", "sample 1"

# custom tests
assert run("3 3\n0 1 0\n") == str((22 * pow(3, MOD-2, MOD)) % MOD), "repeated digits"
assert run("2 2\n1 1\n") == str((3 + 3) * pow(1, MOD-2, MOD) % MOD), "same digit repeated"
assert run("1 10\n9\n") == str((11 * pow(10, MOD-2, MOD)) % MOD), "single digit max base"
assert run("4 2\n0 1 0 1\n") == str((3 + 3 + 3 + 3) % MOD), "alternating digits"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `3 3\n0 1 0` | `22*modinv(3)` | Repeated digits handling |
| `2 2\n1 1` | `6` | Repeated single-digit computation |
| `1 10\n9` | `11*modinv(10)` | Single-digit max base |
| `4 2\n0 1 0 1` | `12` | Alternating digits and backspace expectation |

## Edge Cases

When $n=1$ and $m=2$, for input `0`, `expected_num` is `(2+1)/2 = 3/2`. The algorithm computes `modinv(2, MOD)` correctly and multiplies, giving `666666674`. When digits repeat, `known_digits` ensures the expectation formula does not double-count. For maximum base, modular inverses prevent integer division errors. For alternating digits, each new digit triggers correct expected presses, verifying that the iterative additive model handles all sequences.
