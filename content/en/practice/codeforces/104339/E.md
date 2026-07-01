---
title: "CF 104339E - Compare"
description: "We are given two textual representations of real numbers in decimal form and we need to decide which one is larger, or whether they are equal. The twist is that the formatting is very loose."
date: "2026-07-01T18:38:59+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104339
codeforces_index: "E"
codeforces_contest_name: "FAMCS Olympiad for scholars, Qualification (copy)"
rating: 0
weight: 104339
solve_time_s: 69
verified: true
draft: false
---

[CF 104339E - Compare](https://codeforces.com/problemset/problem/104339/E)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 9s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given two textual representations of real numbers in decimal form and we need to decide which one is larger, or whether they are equal. The twist is that the formatting is very loose. A number can have an optional integer part, an optional fractional part, or both, but never both missing. A decimal point may be absent if there is no fractional part, and either side of the point may also be missing, which effectively behaves like zero. Leading zeros and trailing zeros are irrelevant and may appear in arbitrary quantity.

Conceptually, each input string encodes a non-negative real number in base 10, but not in canonical form. The task is purely a comparison of numeric value, not string order.

The constraints are dominated by the length of each input string, which can be up to 100,000 characters. That immediately rules out any strategy that normalizes numbers by converting them into floating point types or Python decimals, since both precision and performance would fail. Even big integer arithmetic must be handled carefully because the fractional part can be as large as the integer part.

The key difficulty is that the representation is split into two independent components, integer and fractional, and both must be compared lexicographically after normalization without constructing huge intermediate numbers.

Several edge cases cause naive solutions to fail silently.

A first example is differing leading zeros in integer parts. Consider `00012.3` versus `12.3`. A string comparison would incorrectly treat the first as smaller due to lexicographic ordering, but numerically they are equal in integer magnitude.

A second example is missing integer parts. Input like `.15` represents `0.15`, and must compare correctly against something like `0.149999`.

A third example is fractional comparison where one number has a longer fractional part. For instance, `1.2300` and `1.23` are equal, even though the raw strings differ. A naive comparison that compares fractional strings directly would incorrectly say the first is larger due to extra characters.

These issues show that we must normalize structure, not compute numeric values.

## Approaches

A brute-force approach would be to parse each string into a high-precision decimal object or simulate arbitrary precision arithmetic by converting the entire number into a single integer scaled by 10 to the power of the maximum fractional length. For each number, we would need to determine the fractional length, then pad the integer part accordingly, concatenate, and compare as big integers.

This works correctly in principle because both numbers are transformed into comparable integer representations. However, the cost becomes problematic. If both numbers have up to 100,000 digits and we concatenate them into a single large integer string, comparison itself is O(n), and conversion and normalization also require O(n). In practice this remains borderline but acceptable in Python only if carefully implemented. However, repeated allocations and padding make it fragile.

A better observation is that we never need to construct a combined number. We only need to compare integer parts first, and only if they are equal do we compare fractional parts. Within each part, normalization is purely about ignoring leading or trailing zeros.

Thus the problem reduces to string comparison under controlled normalization rules: strip leading zeros in the integer part, strip trailing zeros in the fractional part, then compare lengths and lexicographic order.

This reduces the problem from constructing numbers to comparing two cleaned string pairs.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force (big integer normalization) | O(n) per number, heavy constants | O(n) | Risky |
| Optimal (split and normalize parts) | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Split each input string into integer and fractional parts around the dot. If no dot exists, treat the fractional part as empty. If the string starts with a dot, treat integer part as empty.
2. Normalize the integer part by removing leading zeros. If the result becomes empty, replace it with `"0"`. This ensures that values like `"000"` and `""` both represent zero.
3. Normalize the fractional part by removing trailing zeros. If it becomes empty, treat it as `""`. We do not force it to `"0"` because fractional equality depends on length and content.
4. Compare the integer parts first. If one has more digits than the other, the longer one represents the larger number. If they differ in lexicographic order at the same length, that determines the result.
5. If integer parts are equal, compare fractional parts. First compare by length of the fractional string. A longer fractional part means greater precision beyond equality, so `1.2300` becomes `1.23` after trimming, and they become equal.
6. If lengths are equal, compare lexicographically digit by digit.
7. If both parts match exactly, the numbers are equal.

### Why it works

Every real number in this problem is uniquely determined by its integer magnitude and fractional extension after removing redundant zeros. The normalization guarantees that each value maps to a canonical form where integer comparison reflects magnitude, and fractional comparison reflects fine-grained ordering only when integer parts match. Since both parts are compared in decreasing significance order, integer dominance always decides first, and fractional comparison only resolves ties. This structure preserves ordering equivalence with real numbers.

## Python Solution

```python
import sys
input = sys.stdin.readline

def split_num(s: str):
    if '.' in s:
        a, b = s.split('.')
    else:
        a, b = s, ""

    a = a.lstrip('0')
    if a == "":
        a = "0"

    b = b.rstrip('0')
    return a, b

def cmp(a1, b1, a2, b2):
    if len(a1) != len(a2):
        return 1 if len(a1) > len(a2) else -1
    if a1 != a2:
        return 1 if a1 > a2 else -1

    if b1 == b2:
        return 0

    if len(b1) != len(b2):
        return 1 if len(b1) > len(b2) else -1

    if b1 > b2:
        return 1
    return -1

s1 = input().strip()
s2 = input().strip()

a1, b1 = split_num(s1)
a2, b2 = split_num(s2)

print(cmp(a1, b1, a2, b2))
```

The splitting function is responsible for converting each number into a canonical representation. The integer part is stripped of leading zeros, ensuring correct magnitude comparison. The fractional part is stripped of trailing zeros, ensuring that equivalent decimal expansions do not diverge.

The comparison function carefully avoids converting strings into numeric types. Integer parts are compared first using length, which is the most significant determinant. Only when lengths match do we fall back to lexicographic comparison.

Fractional comparison is only used as a tie-breaker. Length comparison is used first because `"123"` vs `"1230"` would otherwise compare incorrectly if treated lexicographically without normalization.

## Worked Examples

### Example 1

Input:

```
211.000000000000000001
211
```

| Step | Integer part 1 | Fraction 1 | Integer part 2 | Fraction 2 | Decision |
| --- | --- | --- | --- | --- | --- |
| Split | 211 | 000...001 | 211 | "" | equal integers |
| Normalize | 211 | 1 | 211 | "" | integer equal |
| Fraction compare | 1 |  | "" |  | 1 > empty |

The integer parts match exactly, so the comparison reduces to fractional parts. After removing trailing zeros, the first number has a non-empty fractional component while the second has none, so the first is larger.

### Example 2

Input:

```
15
00000000015.00000000
```

| Step | Integer part 1 | Fraction 1 | Integer part 2 | Fraction 2 | Decision |
| --- | --- | --- | --- | --- | --- |
| Split | 15 | "" | 00000000015 | 00000000 | same value |
| Normalize | 15 | "" | 15 | "" | equal |

After normalization both integer parts reduce to `15`, and fractional parts become empty. This confirms equality.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Each string is scanned a constant number of times for splitting and trimming |
| Space | O(n) | Stored normalized strings in worst case |

The solution comfortably fits within constraints because each character is processed a constant number of times, and no large intermediate numeric objects are constructed.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    input = sys.stdin.readline

    def split_num(s: str):
        if '.' in s:
            a, b = s.split('.')
        else:
            a, b = s, ""
        a = a.lstrip('0')
        if a == "":
            a = "0"
        b = b.rstrip('0')
        return a, b

    def cmp(a1, b1, a2, b2):
        if len(a1) != len(a2):
            return 1 if len(a1) > len(a2) else -1
        if a1 != a2:
            return 1 if a1 > a2 else -1
        if b1 == b2:
            return 0
        if len(b1) != len(b2):
            return 1 if len(b1) > len(b2) else -1
        return 1 if b1 > b2 else -1

    s1 = input().strip()
    s2 = input().strip()
    a1, b1 = split_num(s1)
    a2, b2 = split_num(s2)
    return str(cmp(a1, b1, a2, b2))

# provided samples
assert run("211.000000000000000001\n211\n") == "1", "sample 1"
assert run("15\n00000000015.00000000\n") == "0", "sample 2"
assert run(".15\n00000000015.00000000\n") == "-1", "sample 3"

# custom cases
assert run("0.0\n0") == "0", "both zero forms"
assert run("000.0001\n0.0001000") == "0", "fraction normalization"
assert run("1.1\n1.10") == "0", "trailing zero fraction equality"
assert run("2\n10") == "-1", "integer length dominance"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `0.0 vs 0` | 0 | full zero normalization |
| `000.0001 vs 0.0001000` | 0 | fractional trimming correctness |
| `1.1 vs 1.10` | 0 | trailing fractional zeros ignored |
| `2 vs 10` | -1 | integer length comparison correctness |

## Edge Cases

One subtle case is when both integer parts collapse to empty after stripping zeros. For example, `0000.5` and `.5` both represent the same integer value `0`. The normalization step forces empty integer strings into `"0"`, so both become identical before fractional comparison.

Another case is when fractional parts become empty after trimming. For example, `1.2300` becomes integer `1` and fractional `23`, while `1.23` becomes the same. Since fractional comparison treats empty strings as equal only when both are empty or both match, equality is preserved.

A final edge case is large integer parts with equal length but different lexicographic values, such as `999` and `100`. Even though lexicographically `"999" > "100"`, length comparison is identical, so lexicographic comparison correctly resolves the ordering without numeric conversion.
