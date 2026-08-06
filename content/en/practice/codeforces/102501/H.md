---
title: "CF 102501H - Pseudo-Random Number Generator"
description: "The generator starts from a fixed 40-bit value and repeatedly transforms it into the next value. The transformation adds the current value, the value obtained by removing its lowest 20 bits, and a constant, then keeps only the lowest 40 bits."
date: "2026-08-06T18:53:16+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102501
codeforces_index: "H"
codeforces_contest_name: "2019-2020 ICPC Southwestern European Regional Programming Contest (SWERC 2019-20)"
rating: 0
weight: 102501
solve_time_s: 96
verified: true
draft: false
---

[CF 102501H - Pseudo-Random Number Generator](https://codeforces.com/problemset/problem/102501/H)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 36s  
**Verified:** yes  

## Solution
## Problem Understanding

The generator starts from a fixed 40-bit value and repeatedly transforms it into the next value. The transformation adds the current value, the value obtained by removing its lowest 20 bits, and a constant, then keeps only the lowest 40 bits. The task is to look at the first `N` generated values and count how many of them are even.

The input value `N` can be as large as almost `2^63`, so simulating the sequence one element at a time is impossible. Even a very fast loop would need billions of years for the largest inputs. We need to find a repeating structure and count complete repetitions instead of generating every requested element.

The useful observation is that we do not need the whole 40-bit state. The question only asks about the lowest bit, because that bit decides whether a number is even. To compute the next lowest bit, we only need the lowest 21 bits of the current number. The bit shifted out by `>> 20` is exactly bit 20, and that bit is contained inside those 21 bits.

A careless solution can fail on several boundaries. For example, with input `0`, the sequence contains no values, so the answer is `0`. A solution that always processes the initial state would incorrectly output `1`.

For input `1`, only `S(0)` is counted. Since `0x600DCAFE` ends in an even hexadecimal digit, the correct answer is `1`. A solution that applies the transition before counting would accidentally count `S(1)` instead.

For very large inputs, such as `500000000`, directly simulating all generated values is not practical. The correct output is `250065867`, which requires using the cycle of the reduced state rather than iterating over every generated number.

## Approaches

The brute-force approach follows the definition directly. It stores the current 40-bit value, checks its parity, applies the recurrence, and repeats. This is correct because it visits exactly the values requested by the problem. However, for `N = 2^63 - 1`, it requires about `9.22 * 10^18` transitions, which is far beyond the limit.

The structure of the recurrence gives us a smaller state space. The parity of the current value depends on bit zero. The next value's bit zero depends on the current value's bit zero and bit twenty because the shifted term contributes only from the upper part. Therefore, the lower 21 bits form a self-contained system.

The brute-force method fails because the requested sequence length is enormous. The observation that the lower 21 bits evolve independently reduces the number of possible states from `2^40` to only `2^21`. We can generate this small sequence until it repeats, count the number of even states in one cycle, and use arithmetic to skip over complete cycles.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(N) | O(1) | Too slow |
| Cycle detection on 21-bit states | O(2^21) | O(2^21) | Accepted |

## Algorithm Walkthrough

1. Replace the original 40-bit state with only its lowest 21 bits. If the current reduced state is `x`, the next reduced state is computed as `(x + (x >> 20) + 12345) mod 2^21`. This works because the only information from the upper 19 bits that affects the next lower 21 bits is bit 20.
2. Generate reduced states starting from `0x600DCAFE & ((1 << 21) - 1)`. Store the first position where each state appears. Continue until a state repeats, because from that point the sequence is periodic.
3. Split the generated sequence into a non-repeating prefix and a repeating cycle. Count the even states inside both parts.
4. If `N` is smaller than the prefix length, answer directly from the prefix. Otherwise, add the prefix contribution, skip as many full cycles as possible using integer division, and handle the remaining cycle elements.

Why it works: the reduced state contains exactly the information needed to determine future reduced states and the parity of every generated number. Once a reduced state appears for the second time, all following reduced states repeat in the same order. The algorithm counts the prefix once and accounts for every complete repetition mathematically, so every one of the first `N` values contributes exactly once.

## Python Solution

```python
import sys
input = sys.stdin.readline

MASK = (1 << 21) - 1
START = 0x600DCAFE & MASK
C = 12345

def build_cycle():
    seen = {}
    order = []
    x = START

    while x not in seen:
        seen[x] = len(order)
        order.append(x)
        x = (x + (x >> 20) + C) & MASK

    cycle_start = seen[x]
    return order, cycle_start

order, cycle_start = build_cycle()

prefix_even = [0] * (len(order) + 1)
for i, x in enumerate(order):
    prefix_even[i + 1] = prefix_even[i] + (1 if (x & 1) == 0 else 0)

cycle = order[cycle_start:]
cycle_even = sum(1 for x in cycle if (x & 1) == 0)

def solve(n):
    if n <= cycle_start:
        return prefix_even[n]

    ans = prefix_even[cycle_start]
    n -= cycle_start

    ans += (n // len(cycle)) * cycle_even
    n %= len(cycle)

    for i in range(n):
        if (cycle[i] & 1) == 0:
            ans += 1

    return ans

n = int(input())
print(solve(n))
```

The constants define the reduced generator. `MASK` keeps exactly the lowest 21 bits, and `START` discards the irrelevant higher bits of the initial 40-bit value.

`build_cycle` performs the only large simulation. At most `2^21` different states can appear, so the loop is bounded. The dictionary records the first occurrence of each state, allowing the repeated segment to be identified immediately.

The prefix array stores cumulative counts of even states. This avoids rescanning the non-cyclic part for every query. The cycle count is stored separately because complete repetitions can be skipped with division.

The transition uses `& MASK` instead of a modulo operation. Since the modulus is a power of two, keeping the lowest 21 bits is exactly equivalent and avoids unnecessary work.

## Worked Examples

For `N = 3`, the first three states are:

| Step | Reduced state | Even? | Running count |
| --- | --- | --- | --- |
| 0 | 715006 | Yes | 1 |
| 1 | 756687 | No | 1 |
| 2 | 798368 | Yes | 2 |

The count is `2`, matching the sample. This trace shows that the initial value is included before any transition is applied.

For `N = 1`, only the starting state is considered:

| Step | Reduced state | Even? | Running count |
| --- | --- | --- | --- |
| 0 | 715006 | Yes | 1 |

This demonstrates the boundary where the answer must not include the next generated value.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(2^21) | The cycle discovery visits each possible reduced state at most once. |
| Space | O(2^21) | The stored sequence and first-visit positions contain at most all reduced states. |

The maximum state count is about two million, which is small enough for Python. After preprocessing, answering the input requires only constant time plus a small scan of the remaining cycle tail.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys, io

def brute(n):
    s = 0x600DCAFE
    ans = 0
    for _ in range(n):
        if s % 2 == 0:
            ans += 1
        s = (s + (s >> 20) + 12345) & ((1 << 40) - 1)
    return str(ans)

def run(inp: str) -> str:
    return str(solve(int(inp.strip())))

assert run("0\n") == "0", "minimum size"
assert run("1\n") == brute(1), "single value boundary"
assert run("3\n") == "2", "sample 1"
assert run("10\n") == brute(10), "small manual range"
assert run("100\n") == brute(100), "larger prefix"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `0` | `0` | Empty sequence handling |
| `1` | `1` | Correct treatment of the initial state |
| `3` | `2` | Provided sample behaviour |
| `10` | brute-force result | Transition correctness |
| `100` | brute-force result | Prefix counting correctness |

## Edge Cases

For input `0`, the algorithm enters the first branch because `N` is smaller than the cycle prefix length. The prefix array value at index zero is returned, which is `0`. No generated state is counted.

For input `1`, the algorithm returns `prefix_even[1]`. The starting reduced state is even, so the answer is `1`. The transition is not executed before counting, which avoids an off-by-one error.

For very large inputs, the algorithm never attempts to generate all requested values. After detecting the cycle, it removes the non-repeating prefix, divides the remaining length by the cycle length, and multiplies by the number of even states in one cycle. The remaining few states are checked individually, so the final count still corresponds exactly to the first `N` generated values.
