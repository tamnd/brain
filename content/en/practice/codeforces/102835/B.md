---
title: "CF 102835B - Make Numbers"
description: "The task is to take four given digits and create as many different non-negative integers as possible. Each valid expression must use all four digits exactly once."
date: "2026-07-26T15:06:11+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102835
codeforces_index: "B"
codeforces_contest_name: "The 2020 ICPC Asia Taipei-Hsinchu Site Programming Contest"
rating: 0
weight: 102835
solve_time_s: 56
verified: true
draft: false
---

[CF 102835B - Make Numbers](https://codeforces.com/problemset/problem/102835/B)

**Rating:** -  
**Tags:** -  
**Solve time:** 56s  
**Verified:** yes  

## Solution
## Problem Understanding

The task is to take four given digits and create as many different non-negative integers as possible. Each valid expression must use all four digits exactly once. The digits can be rearranged, combined into multi-digit numbers, and connected with the basic arithmetic operations addition, subtraction, and multiplication. The goal is not to find one expression, but to count how many distinct final values can be produced.

For example, with digits `1 1 2 1`, the expression `21 + 11` creates `32`, while `111 - 2` creates `109`. Different expressions that produce the same value only contribute once. The output is the size of the set of all reachable non-negative results.

The input contains only four digits, so the search space is small. A normal problem with `n = 10^5` would require near-linear time, but here the fixed size changes the strategy completely. We can afford exponential enumeration over the four positions because there are only `2^4 = 16` subsets. The challenge is not the amount of data, but making sure every possible expression form is represented.

The tricky part is handling all ways digits can be grouped. A careless solution might only try the original order of digits and miss rearrangements. For input `1 1 2 1`, a program that never forms `21` will miss values such as `32`, even though they are valid.

Another common mistake is ignoring repeated results. For input `1 1 1 1`, the expressions `11 + 1 - 1` and `1 * 111` are different expressions, but the answer only counts each produced integer once. The correct output is `15`.

A final edge case is subtraction producing negative values. The problem only asks for non-negative integers, so negative intermediate or final results must not be inserted into the answer set. For example, an expression like `1 - 2 - 1 - 1` should not contribute `-3`.

## Approaches

The direct approach is to generate every possible expression. One way is to arrange the four digits, decide where concatenation happens, insert operations between the resulting pieces, and evaluate the expression. This is correct because every legal expression can be described by those choices.

However, writing this enumeration manually is error-prone. The number of expression shapes grows because operations can be nested in different ways. A recursive generation method is cleaner. It treats every subset of digits as a smaller independent expression problem.

The brute-force idea becomes much more manageable after the key observation: there are only sixteen subsets of the four digit positions. For every subset, we can store all values that can be made using exactly those digits. A subset can produce values by concatenating its digits in every possible order, or by splitting into two smaller non-empty subsets and combining their values with `+`, `-`, or `*`.

The brute-force version repeatedly rebuilds the same smaller expressions, while the subset dynamic programming version computes each subset once and reuses it. The final answer comes from the values stored for the full set of four digits.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(number of expressions) | O(number of expressions) | Works conceptually, but easy to miss cases |
| Optimal | O(3^4 * V^2) | O(2^4 * V) | Accepted |

Here `V` is the maximum number of values stored for one subset. Since the number of digits is fixed at four, this is easily within limits.

## Algorithm Walkthrough

1. Read the four digits and represent them by positions from `0` to `3`. Positions are used because equal digits still represent different available tiles.
2. Build a recursive function that returns all numbers obtainable from a subset of positions. The returned collection represents every possible expression using exactly those digits.
3. For a subset, first add all numbers created by concatenating its digits in every possible order. This handles values such as `21`, `112`, and `1112`.
4. Try every way to divide the subset into two non-empty disjoint parts. Compute all values for the left and right parts, then combine every pair using addition, subtraction, and multiplication.
5. Store the result set for the full subset containing all four digits. Remove negative values because only non-negative integers are valid answers, then output the number of remaining distinct values.

The reason this works is that the last operation of any valid expression is either a concatenation or one of the three arithmetic operations. If it is arithmetic, the expression naturally splits into two smaller expressions. The recursion follows this structure exactly, so every valid expression is generated. Since every generated expression is valid, no incorrect values are added.

## Python Solution

```python
import sys
from functools import lru_cache
from itertools import permutations

input = sys.stdin.readline

def solve():
    digits = list(map(int, input().split()))

    @lru_cache(None)
    def dp(mask):
        res = set()
        ids = [i for i in range(4) if mask & (1 << i)]

        for p in permutations(ids):
            value = 0
            for i in p:
                value = value * 10 + digits[i]
            res.add(value)

        sub = (mask - 1) & mask
        while sub:
            other = mask ^ sub
            if other and sub < other:
                for a in dp(sub):
                    for b in dp(other):
                        res.add(a + b)
                        res.add(a - b)
                        res.add(a * b)
                        res.add(b - a)
            sub = (sub - 1) & mask

        return res

    ans = sum(1 for x in dp(15) if x >= 0)
    print(ans)

if __name__ == "__main__":
    solve()
```

The recursive function `dp(mask)` is the core of the solution. The bitmask describes which digit positions are available. Using positions rather than digit values prevents equal digits from being merged accidentally.

The permutation loop adds every possible concatenated number. This is necessary because the order of digits is flexible. For a subset containing digits `1` and `2`, both `12` and `21` must be considered.

The subset splitting loop tries every partition exactly once by requiring `sub < other`. This avoids doing the same split twice. The arithmetic combinations include both subtraction directions because the left and right parts of an expression are ordered.

Python integers do not overflow, so multiplication is safe. The memoization decorator ensures that each subset is evaluated once instead of being recomputed many times.

## Worked Examples

For input `1 1 1 1`, the important state is the set of values produced from the complete mask.

| Step | Current subset | Action | Result size |
| --- | --- | --- | --- |
| 1 | single digits | Store possible one-digit values | 1 |
| 2 | pairs | Add concatenations and arithmetic combinations | several values |
| 3 | triples | Combine previously computed pairs and singles | larger set |
| 4 | all digits | Combine all partitions | 15 non-negative values |

This example confirms that duplicate expressions do not matter. The algorithm keeps a set, so repeated values disappear automatically.

For input `1 1 2 1`, the final combination step includes expressions such as `21 + 11`.

| Step | Current subset | Example generated value | Reason |
| --- | --- | --- | --- |
| 1 | digits `2` and `1` | 21 | concatenation is allowed |
| 2 | remaining digits `1` and `1` | 11 | second concatenation |
| 3 | full set | 32 | combine `21 + 11` |
| 4 | full set | 109 | combine `111 - 2` |

The trace demonstrates why storing intermediate subsets is useful. Larger expressions reuse smaller building blocks instead of trying every complete expression separately.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(3^4 * V^2) | Each subset is split into smaller subsets and values are combined |
| Space | O(2^4 * V) | Sixteen masks are stored, each containing reachable values |

The number of digits never changes, so the exponential part is a constant-size search. The solution comfortably fits the one second limit because it performs only a small number of recursive states and set operations.

## Test Cases

```python
import sys
import io
from functools import lru_cache
from itertools import permutations

def solve_case(inp):
    digits = list(map(int, inp.split()))

    @lru_cache(None)
    def dp(mask):
        res = set()
        ids = [i for i in range(4) if mask & (1 << i)]

        for p in permutations(ids):
            x = 0
            for i in p:
                x = x * 10 + digits[i]
            res.add(x)

        sub = (mask - 1) & mask
        while sub:
            other = mask ^ sub
            if other and sub < other:
                for a in dp(sub):
                    for b in dp(other):
                        res.add(a + b)
                        res.add(a - b)
                        res.add(b - a)
                        res.add(a * b)
            sub = (sub - 1) & mask

        return res

    return str(sum(x >= 0 for x in dp(15)))

assert solve_case("1 1 1 1") == "15"
assert solve_case("1 1 2 1") == "32"

assert solve_case("0 0 0 0") == "1"
assert solve_case("9 9 9 9") != "0"
assert solve_case("0 1 2 3") != "0"
assert solve_case("5 5 5 5") != "0"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 1 1 1` | `15` | Provided sample and duplicate handling |
| `1 1 2 1` | `32` | Provided sample and digit rearrangement |
| `0 0 0 0` | `1` | Repeated zero digits and zero result |
| `9 9 9 9` | Non-zero answer | Large digit values |
| `0 1 2 3` | Non-zero answer | Concatenation involving zero |

## Edge Cases

For `1 1 1 1`, the algorithm builds many identical values through different expressions. Because every subset result is stored in a set, expressions like `1+1+1+1` and `11-7` style duplicates cannot inflate the answer.

For `0 0 0 0`, concatenation creates only zero, and every arithmetic operation also stays at zero. The final set contains exactly one valid non-negative number, so the output is `1`.

For cases where subtraction creates negative values, such as using digits `1 2 3 4`, expressions that end below zero are generated internally but filtered before counting. This prevents invalid negative integers from affecting the answer.
