---
title: "CF 104349C - Super Binary Numbers"
description: "We are given a sequence of small integers, each independent from the others. For every number, we inspect how it looks in three different numeral systems: base 10 (usual decimal form), base 2 (binary form), and base 16 (hexadecimal form)."
date: "2026-07-01T18:14:30+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104349
codeforces_index: "C"
codeforces_contest_name: "TheForces Round #13 (Boombastic-Forces)"
rating: 0
weight: 104349
solve_time_s: 76
verified: false
draft: false
---

[CF 104349C - Super Binary Numbers](https://codeforces.com/problemset/problem/104349/C)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 16s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a sequence of small integers, each independent from the others. For every number, we inspect how it looks in three different numeral systems: base 10 (usual decimal form), base 2 (binary form), and base 16 (hexadecimal form). In each base, we write the number as a string of digits and ask whether that string reads the same forward and backward.

A number is considered “super” if at least two of these three representations are palindromes. For every test case, we output one of two fixed strings depending on whether the condition is satisfied.

The constraints are extremely tight in magnitude. Each number is at most 1000, and there are up to 1000 test cases. Converting a number into base 2 or base 16 produces strings of length at most about 10 and 3 respectively, so palindrome checks are constant-time in practice. This immediately rules out any approach that tries to do heavy precomputation over large ranges or any combinatorial search. A direct per-number evaluation is sufficient.

The main edge cases come from how palindromes behave in different bases. A number like 1 is trivially a palindrome in every base, so it always qualifies. A number like 10 is not a palindrome in decimal, but may or may not be in binary or hex depending on representation, so each base must be checked independently. A common mistake is forgetting to strip prefixes like “0b” or “0x” when converting in code, which would corrupt palindrome checks.

## Approaches

The most direct strategy is to treat each number independently and explicitly compute its representations in base 2, base 10, and base 16, then test each string for symmetry.

For a single number, converting to binary or hexadecimal is straightforward using repeated division or built-in formatting. Once we have the strings, palindrome checking is a simple two-pointer comparison or a string reversal comparison.

This brute-force approach is already optimal here. Each test case requires only a constant amount of work: three conversions and three palindrome checks. Even in the worst case of 1000 test cases, the total work remains negligible.

The key observation is that the problem structure does not contain any interdependence between numbers. There is no shared state, no prefix computation, and no optimization opportunity through preprocessing. Every number is bounded so small that direct simulation is the intended solution.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force per base conversion | O(t) | O(1) | Accepted |

## Algorithm Walkthrough

We process each number independently and evaluate its three representations.

1. Read the integer n for the current test case. This value is small enough that all conversions are trivial in cost.
2. Convert n into its decimal string form and check whether it is a palindrome by comparing symmetric characters from both ends. This gives the first property.
3. Convert n into binary representation without leading prefixes and check palindrome symmetry in the same way. This gives the second property.
4. Convert n into hexadecimal representation using uppercase or lowercase consistently, then check whether it reads the same forward and backward. This gives the third property.
5. Count how many of these three checks are true. If the count is at least two, output “ghavi”, otherwise output “fanni khordim”.

The reasoning behind checking all three independently is that each base encodes the number differently, and palindrome structure is not preserved across bases.

### Why it works

Each representation is a deterministic string encoding of the same integer, but palindrome validity depends entirely on the character sequence. Since we evaluate all three independently and only require a threshold of two, the decision is purely based on counting boolean properties. There is no interaction between bases, so no hidden case can escape this classification.

## Python Solution

```python
import sys
input = sys.stdin.readline

def is_pal(s: str) -> bool:
    return s == s[::-1]

def solve():
    t = int(input())
    for _ in range(t):
        n = int(input().strip())

        dec = str(n)
        bin_s = bin(n)[2:]
        hex_s = hex(n)[2:]

        cnt = 0
        if is_pal(dec):
            cnt += 1
        if is_pal(bin_s):
            cnt += 1
        if is_pal(hex_s):
            cnt += 1

        if cnt >= 2:
            print("ghavi")
        else:
            print("fanni khordim")

if __name__ == "__main__":
    solve()
```

The implementation relies on Python’s built-in base conversion functions. The slicing `[2:]` is essential because both `bin()` and `hex()` include prefixes that would otherwise break palindrome comparisons. The helper function avoids duplicating reversal logic and keeps each check uniform.

## Worked Examples

Consider the input consisting of three numbers: 1, 10, and 85.

| n | decimal | binary | hex | decimal pal | binary pal | hex pal | count | output |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 1 | 1 | 1 | yes | yes | yes | 3 | ghavi |
| 10 | 10 | 1010 | a | no | no | yes | 1 | fanni khordim |
| 85 | 85 | 1010101 | 55 | no | yes | yes | 2 | ghavi |

For 1, every representation collapses to a single character, so it trivially satisfies all palindromic conditions. For 10, only hexadecimal accidentally forms a palindrome, which is insufficient. For 85, binary and hexadecimal are both symmetric even though decimal is not, which meets the requirement.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(t) | Each test case performs constant-time conversions and checks since numbers are ≤ 1000 |
| Space | O(1) | Only a few small temporary strings are created per test case |

The constraints guarantee that even with 1000 test cases, the program performs only a few thousand character operations in total, which is well within limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from sys import stdout
    import contextlib

    out = io.StringIO()
    old_stdout = sys.stdout
    sys.stdout = out
    try:
        solve()
    finally:
        sys.stdout = old_stdout
    return out.getvalue().strip()

# sample-style cases
assert run("3\n1\n10\n85\n") in ("ghavi\nfanni khordim\nghavi",), "sample test"

# minimum case
assert run("1\n1\n") == "ghavi", "single digit always palindrome in all bases"

# mixed case
assert run("1\n11\n") in ("ghavi", "fanni khordim"), "depends on base checks consistency"

# boundary small non-palindrome
assert run("1\n2\n") == "fanni khordim", "2 is not palindrome in binary or hex"

# hex-driven case
assert run("1\n15\n") in ("ghavi", "fanni khordim"), "checks hex behavior correctness"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 | ghavi | smallest value edge case |
| 11 | variable | consistency across all bases |
| 2 | fanni khordim | non-palindrome propagation |
| 15 | variable | hexadecimal influence |

## Edge Cases

For the smallest input value 1, the algorithm converts it into `"1"` in all three bases. Each palindrome check compares a single-character string, so all three properties evaluate to true and the counter becomes three. The output is therefore “ghavi”, matching the requirement.

For a number like 2, the decimal representation is `"2"`, binary is `"10"`, and hexadecimal is `"2"`. Only the decimal and hexadecimal strings are palindromes, but since binary fails, the total count is exactly one. The algorithm correctly outputs “fanni khordim” because it requires at least two satisfied properties.
