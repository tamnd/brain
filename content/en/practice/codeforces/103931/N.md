---
title: "CF 103931N - Nine Is Greater Than Ten"
description: "We are given two positive integers written in plain decimal form, each without leading zeros, and we need to compare them using a deliberately odd rule inspired by the story."
date: "2026-07-02T07:20:03+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 103931
codeforces_index: "N"
codeforces_contest_name: "2022 Shanghai Collegiate Programming Contest"
rating: 0
weight: 103931
solve_time_s: 42
verified: true
draft: false
---

[CF 103931N - Nine Is Greater Than Ten](https://codeforces.com/problemset/problem/103931/N)

**Rating:** -  
**Tags:** -  
**Solve time:** 42s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given two positive integers written in plain decimal form, each without leading zeros, and we need to compare them using a deliberately odd rule inspired by the story. Despite the humorous “Koji comparison”, the actual task still reduces to determining whether the first number is smaller than, equal to, or greater than the second number, and printing the corresponding relationship in the exact format `a>b`, `a<b`, or `a=b`.

The key detail is that the integers can be very large, up to about $2 \cdot 10^{10}$, so they may not safely fit into standard fixed-width integer types in some languages. In Python this is less of a concern, but the intent of the constraint is clearly that we should treat them as strings or use arbitrary precision logic rather than relying on naive integer parsing assumptions in stricter languages.

A naive but common mistake is to convert both inputs into integers and compare them directly. That is correct in Python, but in other environments it risks overflow. Another subtle pitfall is attempting to compare lexicographically as strings without handling length differences properly. For example, `"9"` and `"10"`: lexicographically `"9" > "10"` is false because `'9' < '1'` is false only if we compare incorrectly; but actually string comparison works by lexicographic order, so `"9" > "10"` would incorrectly evaluate as `True` in some naive implementations because `'9' > '1'`. The correct ordering must consider numeric length first.

Edge cases that matter here include single-digit versus multi-digit numbers, equal strings, and numbers where the first digit differs immediately versus cases where they share prefixes.

## Approaches

The brute-force approach is straightforward: parse both inputs as integers and compare them directly. In Python this is effectively constant time for comparison after parsing, but parsing itself is linear in the number of digits. Since each number can have up to around 11 digits in this problem, this is trivial and safe. In a stricter language context, this approach might still be acceptable because the bounds are small, but the conceptual issue is that it relies on built-in big integer support.

A more universal approach that works in any language is to treat the numbers as strings and compare them as numeric strings. The key observation is that integer comparison can be reduced to two rules. First, if the lengths differ, the longer number is larger because it has more digits in base 10. Second, if lengths are equal, then standard lexicographic comparison works because both strings represent aligned digit sequences.

The brute-force mental model works because we simulate actual integer values implicitly. It fails conceptually when relying on raw lexicographic comparison without length normalization, since digit ordering in ASCII is not aligned with numeric magnitude across different lengths. The observation that digit length determines magnitude removes the need for full numeric parsing and gives a direct comparison rule.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force (integer parsing) | O(d) | O(d) | Accepted |
| String length + lexicographic compare | O(d) | O(1) extra | Accepted |

Here $d$ is the number of digits in the larger number.

## Algorithm Walkthrough

1. Read the two input strings `a` and `b`. We keep them as strings because their digit structure encodes their magnitude directly.
2. Compare the lengths of `a` and `b`. If `len(a) > len(b)`, we immediately conclude `a > b`. This works because any number with more digits is necessarily larger in base 10.
3. If `len(a) < len(b)`, we immediately conclude `a < b` for the same reason.
4. If the lengths are equal, compare `a` and `b` character by character from left to right. The first position where they differ determines the ordering: the string with the larger digit at that position corresponds to the larger number.
5. If no differing position exists, the numbers are identical and we output equality.

### Why it works

The algorithm relies on the fact that decimal representation is positional. A number with more digits always exceeds any number with fewer digits because the smallest k-digit number is $10^{k-1}$, which is strictly larger than the largest $(k-1)$-digit number $10^{k-1}-1$. When digit counts match, each prefix comparison preserves numeric order because both numbers share the same positional weights. The first differing digit determines which number has a larger contribution at the highest differing place value, and all later digits cannot compensate for that difference.

## Python Solution

```python
import sys
input = sys.stdin.readline

a, b = input().split()

if len(a) > len(b):
    print(f"{a}>{b}")
elif len(a) < len(b):
    print(f"{a}<{b}")
else:
    if a > b:
        print(f"{a}>{b}")
    elif a < b:
        print(f"{a}<{b}")
    else:
        print(f"{a}={b}")
```

The solution separates comparison into two logically distinct stages: length comparison first, then lexicographic comparison only when necessary. The formatting requirement is handled directly via f-strings, preserving the exact output structure.

A subtle implementation detail is that we never convert the strings into integers. This keeps the solution safe in any language and avoids unnecessary overhead. The lexicographic comparison is valid only because we already guaranteed equal length.

## Worked Examples

### Example 1: `9 10`

| Step | a | b | len(a) | len(b) | Decision |
| --- | --- | --- | --- | --- | --- |
| 1 | "9" | "10" | 1 | 2 | Compare lengths |

Since `len(a) < len(b)`, we immediately output `9<10`.

This demonstrates that magnitude is dominated by digit count rather than character comparison.

### Example 2: `114514 1919`

| Step | a | b | len(a) | len(b) | Decision |
| --- | --- | --- | --- | --- | --- |
| 1 | "114514" | "1919" | 6 | 4 | Compare lengths |

Since `len(a) > len(b)`, we output `114514>1919` without digit-by-digit comparison.

This shows why length comparison alone is sufficient in most cases and avoids unnecessary scanning.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(d) | We read input and possibly compare strings once digit-by-digit |
| Space | O(1) | Only storing two input strings and constant extra variables |

The digit length $d$ is at most about 11 in the constraints, so the solution runs effectively in constant time and trivially fits within limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    a, b = input().split()

    if len(a) > len(b):
        return f"{a}>{b}"
    elif len(a) < len(b):
        return f"{a}<{b}"
    else:
        if a > b:
            return f"{a}>{b}"
        elif a < b:
            return f"{a}<{b}"
        else:
            return f"{a}={b}"

# provided samples
assert run("9 10") == "9<10"
assert run("114514 1919") == "114514>1919"
assert run("9 999") == "9<999"
assert run("99 99") == "99=99"

# custom cases
assert run("1 2") == "1<2", "single digit increasing"
assert run("10 2") == "10>2", "different digit lengths reversal"
assert run("123 123") == "123=123", "exact equality"
assert run("1000 999") == "1000>999", "power of ten boundary"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 2 | 1<2 | smallest single-digit comparison |
| 10 2 | 10>2 | length dominance over lexicographic intuition |
| 123 123 | 123=123 | equality handling |
| 1000 999 | 1000>999 | boundary between digit lengths |

## Edge Cases

A key edge case is when numbers differ only by digit count, such as `10` versus `9`. The algorithm handles this immediately via length comparison and avoids incorrect lexicographic reasoning.

Another case is identical numbers like `999` and `999`, where neither length nor lexicographic comparison finds a difference. The algorithm correctly falls through to equality.

Finally, cases where prefixes match but lengths differ, such as `100` and `99`, are correctly resolved because length comparison dominates before any digit inspection.
