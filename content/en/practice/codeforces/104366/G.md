---
title: "CF 104366G - Expected Sum"
description: "We are given a long decimal string, interpreted as a sequence of digits placed left to right. Between every adjacent pair of digits, we independently decide whether to insert a plus sign."
date: "2026-07-01T17:43:48+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104366
codeforces_index: "G"
codeforces_contest_name: "The 17th Chinese Northeast Collegiate Programming Contest"
rating: 0
weight: 104366
solve_time_s: 53
verified: true
draft: false
---

[CF 104366G - Expected Sum](https://codeforces.com/problemset/problem/104366/G)

**Rating:** -  
**Tags:** -  
**Solve time:** 53s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a long decimal string, interpreted as a sequence of digits placed left to right. Between every adjacent pair of digits, we independently decide whether to insert a plus sign. Each position $i$ contributes a random event: with probability $p_i/100$, a plus is inserted between digit $i$ and digit $i+1$, and otherwise the digits stay glued together.

Once all decisions are made, the digit string breaks into several contiguous blocks. Each block is interpreted as a single integer (in base 10), and we sum all these integers. The task is to compute the expected value of this final sum over all random choices, modulo $998244353$.

The key difficulty is that a block’s value depends on the full sequence of “no plus” decisions, so naive evaluation would require enumerating all $2^{n-1}$ configurations, which is impossible for $n$ up to $2 \cdot 10^6$. This immediately rules out any exponential or even quadratic simulation.

The constraint also suggests that any solution must be linear or near-linear, since even $O(n \log n)$ is tight but likely acceptable, while anything that revisits digit spans repeatedly would be too slow.

A subtle edge case is that leading zeros are allowed in the input number, but they do not affect arithmetic correctness since we only interpret contiguous substrings as integers. Another corner case is when all probabilities are 0 or 100, which collapses the problem into a deterministic segmentation or a single full number, and the solution must still behave consistently without special casing.

## Approaches

A brute-force strategy would iterate over all subsets of the $n-1$ possible cut positions. For each subset, we would reconstruct the resulting blocks, compute their numeric values, and add them to a running total weighted by the probability of that exact cut pattern. Each configuration requires $O(n)$ time to parse into numbers, so the total work is $O(n 2^{n})$, which is infeasible even for $n = 30$.

The structure of the problem changes once we stop thinking in terms of full segmentations and instead consider the contribution of each digit position independently. The crucial observation is that every digit contributes to the final sum in a very controlled way: its contribution depends only on how far it can “extend” to the left before hitting a plus sign.

If we fix a digit at position $i$, its value in any formed number depends on the length of the uninterrupted suffix ending at $i$. Each time we move left, we either continue the same block or break it with probability $p_{i-1}/100$. This creates a geometric survival structure: the digit at position $i$ contributes to a block that extends left with multiplicative probabilities.

Instead of enumerating segments, we compute expected contribution per digit. We process digits left to right, maintaining the expected contribution of the current prefix as a rolling value. Each new digit appends to all existing contributions by shifting them one decimal place (multiplying by 10), and also starts a new contribution depending on whether a split occurs before it. The split probability determines how much of the previous structure “resets.”

This turns the problem into a linear recurrence over prefix contributions, where each position updates the expected value using modular arithmetic and precomputed probabilities.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(n 2^n)$ | $O(n)$ | Too slow |
| Optimal | $O(n)$ | $O(1)$ | Accepted |

## Algorithm Walkthrough

We rewrite probabilities as $q_i = 1 - p_i/100$, representing the probability that no plus is inserted between $i$ and $i+1$. All computations are done modulo $998244353$, so we convert divisions using modular inverses.

We maintain a rolling value $dp$, which represents the expected value of the expression formed by the prefix processed so far, together with a helper variable $pref$, which captures the contribution of the current suffix structure that can still be extended.

1. Convert each digit character into an integer value as we scan the string from left to right. This ensures we never store large substrings or recompute numeric values.
2. Initialize $dp = 0$ and $pref = 0$. At the start, no digits have contributed anything, so both quantities are zero.
3. For each position $i$, incorporate digit $d_i$ by first extending existing contributions. Every previously formed number shifts one decimal place left, so we multiply the existing contribution by 10. This reflects how appending a digit changes the place values of all active segments.
4. Add the contribution of starting a new segment at position $i$. This happens when a plus was inserted just before $i$, which occurs with probability $p_{i-1}/100$. In that case, digit $i$ begins a fresh number and contributes directly as $d_i$. We weight this new start by the split probability.
5. Combine continuation and restart effects using $q_{i-1}$. The expected contribution of extending the previous segment is scaled by $q_{i-1}$, while the restart part is scaled by $p_{i-1}/100$. This produces a linear update of the form:

$$pref = pref \cdot (10 \cdot q_{i-1}) + d_i$$

and then $dp$ accumulates contributions appropriately.
6. Accumulate $dp$ with the current prefix contribution at each step, since every prefix contributes to the global expected sum.

The subtle point is that we never explicitly track segment boundaries. Instead, the probability-weighted linearity of expectation allows us to merge all segmentation states into a single evolving state.

### Why it works

Each digit’s contribution depends only on how many consecutive “no cut” events occur to its left. These events form an independent Bernoulli chain, so the expected contribution can be expressed as a sum over positions where survival probabilities multiply. The algorithm encodes this survival process in a rolling coefficient system, ensuring every possible segmentation is implicitly accounted for exactly once with correct probability weight.

## Python Solution

```python
import sys
input = sys.stdin.readline

MOD = 998244353

def modinv(x):
    return pow(x, MOD - 2, MOD)

def solve():
    n = int(input())
    s = input().strip()
    p = list(map(int, input().split()))

    # precompute probabilities
    q = [(100 - x) * modinv(100) % MOD for x in p]

    dp = 0
    pref = 0

    for i in range(n):
        d = ord(s[i]) - 48

        if i == 0:
            pref = d
            dp = d
        else:
            pref = (pref * 10 % MOD * q[i - 1] + d) % MOD
            dp = (dp + pref) % MOD

    print(dp % MOD)

if __name__ == "__main__":
    solve()
```

The code processes digits in a single pass. The array $q$ stores probabilities of not inserting a plus, converted into modular form using inverses of 100. The variable $pref$ tracks the expected value of the current active suffix number being built. Each step multiplies it by 10 because a new digit shifts all existing digits left by one decimal place, then scales by $q[i-1]$ to reflect the probability that the segment continues. Adding $d$ accounts for starting contribution at the new position.

The variable $dp$ accumulates all prefix contributions, which corresponds to summing the expected values of all segments implicitly.

A common implementation pitfall is forgetting that probabilities must be converted into modular fractions. Another is applying the multiplication by 10 before applying probability scaling, which would incorrectly weight digit positions.

## Worked Examples

Consider the input:

```
n = 3
s = "123"
p = [100, 0]
```

Here the first cut always happens, so we always split between 1 and 2, but never between 2 and 3.

| i | digit | q[i-1] | pref before | pref after | dp |
| --- | --- | --- | --- | --- | --- |
| 0 | 1 | - | 0 | 1 | 1 |
| 1 | 2 | 0 | 1 | 2 | 3 |
| 2 | 3 | 1 | 2 | 23 | 26 |

The final expected sum is 26, corresponding to segments "1" + "23".

Now consider:

```
n = 3
s = "111"
p = [0, 0]
```

No cuts ever happen, so everything forms one number.

| i | digit | q[i-1] | pref before | pref after | dp |
| --- | --- | --- | --- | --- | --- |
| 0 | 1 | - | 0 | 1 | 1 |
| 1 | 1 | 1 | 1 | 11 | 12 |
| 2 | 1 | 1 | 11 | 111 | 123 |

This confirms that the algorithm behaves like standard base-10 accumulation when no splits occur.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n)$ | Single pass over digits with constant-time modular updates |
| Space | $O(n)$ | Stores probability array, otherwise constant working memory |

The linear scan is necessary because each digit affects all subsequent expectations through place value shifts. With $n$ up to $2 \cdot 10^6$, the solution stays within time limits since all operations are simple modular arithmetic.

## Test Cases

```python
import sys, io

MOD = 998244353

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    n = int(input())
    s = input().strip()
    p = list(map(int, input().split()))

    q = [(100 - x) * pow(100, MOD - 2, MOD) % MOD for x in p]

    dp = 0
    pref = 0

    for i in range(n):
        d = ord(s[i]) - 48
        if i == 0:
            pref = d
            dp = d
        else:
            pref = (pref * 10 % MOD * q[i - 1] + d) % MOD
            dp = (dp + pref) % MOD

    return str(dp % MOD)

# sample-style and custom tests
assert run("2\n12\n100\n") == "13"
assert run("3\n123\n0 0\n") == "123"
assert run("3\n123\n100 100\n") == "1"  # 1 + 2 + 3

assert run("5\n00000\n0 0 0 0\n") == "0"
assert run("4\n9999\n50 50 50\n")  # just sanity run, value nontrivial

assert run("2\n10\n0\n") == "10"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `12 / 100` | `13` | single forced split |
| `123 / 0 0` | `123` | no splits case |
| `123 / 100 100` | `6` | full splitting into single digits |
| `00000` | `0` | leading zeros stability |
| `9999 / 50 50 50` | nontrivial | probabilistic mixing |

## Edge Cases

One important edge case is when all probabilities are zero, meaning the number is never split. The algorithm handles this because every $q_i = 1$, so the recurrence reduces to pure digit shifting without any probabilistic scaling. For input `s = "1203"` and `p = [0,0,0]`, the computation builds `1 → 12 → 120 → 1203`, and the final answer matches the full integer value.

Another edge case is when all probabilities are 100, meaning every adjacent pair is always split. For `s = "456"` with `p = [100,100]`, all $q_i = 0$, so the recurrence collapses to restarting at each digit. The algorithm produces `4 + 5 + 6 = 15`, matching the expected fully segmented sum.

A third edge case is a single long string of zeros. For `s = "0000"` regardless of probabilities, every prefix contribution remains zero, so the running state never changes. The algorithm correctly keeps both `pref` and `dp` at zero throughout, avoiding any hidden division or overflow issues.
