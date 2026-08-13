---
title: "CF 102307I - Integer Prefix"
description: "We are given one text string with no spaces. The task is to find the longest prefix of that string whose characters are all decimal digits. The prefix must be non-empty. If the very first character is not a digit, then no valid prefix exists and we print -1."
date: "2026-08-13T07:23:41+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102307
codeforces_index: "I"
codeforces_contest_name: "2019 ICPC Universidad Nacional de Colombia Programming Contest"
rating: 0
weight: 102307
solve_time_s: 65
verified: true
draft: false
---

[CF 102307I - Integer Prefix](https://codeforces.com/problemset/problem/102307/I)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 5s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given one text string with no spaces. The task is to find the longest prefix of that string whose characters are all decimal digits. The prefix must be non-empty. If the very first character is not a digit, then no valid prefix exists and we print `-1`.

For example, in `23082019UNAL`, the initial characters `23082019` are digits, while the next character `U` is not. The answer is consequently `23082019`. In `ABC123`, the first character already breaks the digit-only condition, so the answer is `-1`.

The string contains at most `2 * 10^5` characters. That size is large enough that a quadratic algorithm is inappropriate, especially under a one-second time limit. A solution performing roughly `n^2` character checks could reach about `4 * 10^10` operations at the maximum length, far beyond what can fit in the limit. We need to inspect the string essentially once, giving an `O(n)` solution.

There are a few boundary cases that can cause an otherwise simple implementation to fail. If the input is `7`, the entire string is a valid numeric prefix, so the output is `7`. An implementation that expects a non-digit terminator would incorrectly miss this case.

If the input is `A123`, the correct output is `-1`, because the valid prefix must start at the first character. A careless solution that searches for any run of digits could incorrectly return `123`.

If the input is `123A456`, the answer is `123`, not `123456`. Once the first non-digit appears, no later characters can belong to the required prefix.

If the input is `0000X`, the answer is `0000`. The prefix is a string, not an integer, so leading zeroes must be preserved. Converting the prefix to an integer before printing would incorrectly produce `0`.

## Approaches

A direct brute-force approach can consider every possible prefix and check whether every character inside that prefix is a digit. For a string of length `n`, there are `n` possible non-empty prefixes. If we check a prefix ending at position `i` from its beginning every time, the total number of character inspections is

`1 + 2 + 3 + ... + n = n(n + 1)/2`.

At `n = 200000`, this is about `2 * 10^10` inspections. The brute-force method is logically correct because it explicitly verifies the definition of a valid prefix, but it repeatedly checks characters that were already known to be digits.

The structure of the problem gives us a much simpler observation. A prefix is valid exactly while every character encountered from the beginning is a digit. The first non-digit character permanently ends the answer. There is no reason to reconsider an earlier character after reaching it, because a prefix cannot skip characters.

That lets us scan from left to right once. At each position, if the character is a digit, we continue. At the first non-digit, we stop and output everything before that position. If the scan reaches the end, the whole string is the answer. This reduces the work from quadratic to linear.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n²) | O(n) | Too slow |
| Optimal | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Read the complete input string and remove the trailing newline. We keep it as a string rather than converting it to a number, because leading zeroes are part of the required output.
2. Start scanning from the first character toward the end of the string. The scan represents the longest prefix that has been confirmed to contain only digits so far.
3. When the current character is a digit, continue scanning. Every character before the current position has already been verified, so extending the prefix by another digit remains valid.
4. When the current character is not a digit, stop immediately and print the substring before this position. This is the longest possible answer because every longer prefix would contain this same non-digit character.
5. If the scan reaches the end without finding a non-digit, print the entire string. Every character has been verified as a digit, so the complete string is the longest valid prefix.
6. If the first character is non-numeric, the stopping position is zero and the prefix before it is empty. Since the problem requires a non-empty prefix, print `-1` instead.

### Why it works

Maintain the invariant that before position `i`, every character in the prefix `T[0:i]` is a digit. If `T[i]` is also a digit, extending the prefix preserves the invariant. If `T[i]` is not a digit, every prefix longer than `T[0:i]` contains `T[i]`, so none of those prefixes can be valid. Thus the first non-digit position uniquely determines the longest numeric prefix. If no such position exists, every character is a digit and the whole string is the answer.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    s = input().strip()

    for i, ch in enumerate(s):
        if not ch.isdigit():
            if i == 0:
                print(-1)
            else:
                print(s[:i])
            return

    print(s)

if __name__ == "__main__":
    solve()
```

The input line is read once, and `strip()` removes the newline added by standard input. The string itself is never converted to an integer, which preserves leading zeroes such as those in `000123`.

The loop examines characters in their original order. As soon as `isdigit()` returns false, the loop has found the exact boundary between the numeric prefix and the rest of the text. The slice `s[:i]` contains precisely the characters before that boundary.

The `i == 0` check handles the non-empty requirement. If the first character is not a digit, `s[:0]` would be an empty string, so the required output is `-1` instead.

There is no integer arithmetic in the solution, so integer overflow is irrelevant. The only boundary that matters is whether the first invalid character occurs at index zero, somewhere in the middle, or not at all.

## Worked Examples

### Sample 1

For `23082019UNAL`, the scan continues through all eight initial digits and stops at `U`.

| Index | Character | Is digit? | Prefix confirmed |
| --- | --- | --- | --- |
| 0 | `2` | Yes | `2` |
| 1 | `3` | Yes | `23` |
| 2 | `0` | Yes | `230` |
| 3 | `8` | Yes | `2308` |
| 4 | `2` | Yes | `23082` |
| 5 | `0` | Yes | `230820` |
| 6 | `1` | Yes | `2308201` |
| 7 | `9` | Yes | `23082019` |
| 8 | `U` | No | Stop |

The first non-digit is at index `8`, so the answer is `s[:8]`, which is `23082019`. The remaining characters do not matter because every longer prefix would contain `U`.

### Sample 2

For `UNAL`, the very first character is not a digit.

| Index | Character | Is digit? | Action |
| --- | --- | --- | --- |
| 0 | `U` | No | Stop and print `-1` |

There is no non-empty prefix consisting only of digits. This trace exercises the boundary where the first invalid character occurs at position zero.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Each character is examined at most once. |
| Space | O(n) | The input string requires O(n) memory, and the output slice can also require O(n) memory. |

With at most `2 * 10^5` characters, a single linear scan performs only a few hundred thousand character checks. This is comfortably within the stated one-second time limit, while the quadratic brute-force approach could require around `2 * 10^10` checks.

## Test Cases

```python
import sys
import io

def solve_string(s: str) -> str:
    for i, ch in enumerate(s):
        if not ch.isdigit():
            return "-1" if i == 0 else s[:i]
    return s

def run(inp: str) -> str:
    return solve_string(inp.strip())

# Provided samples
assert run("23082019UNAL") == "23082019", "sample 1"
assert run("UNAL") == "-1", "sample 2"

# Minimum-size inputs
assert run("7") == "7", "single digit"
assert run("A") == "-1", "single non-digit"

# Leading zeroes must be preserved
assert run("0000X") == "0000", "leading zeroes"

# Non-digit immediately after the numeric prefix
assert run("123A456") == "123", "prefix boundary"

# All characters are digits
assert run("999999") == "999999", "all digits"

# Maximum-size input, with the first non-digit at the very end
maximum = "7" * (2 * 10**5 - 1) + "X"
assert run(maximum) == "7" * (2 * 10**5 - 1), "maximum-size input"

# Maximum-size input with no valid prefix
maximum_invalid = "X" + "7" * (2 * 10**5 - 1)
assert run(maximum_invalid) == "-1", "maximum-size invalid prefix"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `7` | `7` | Minimum size and a prefix that reaches the end |
| `A` | `-1` | Minimum size with no numeric prefix |
| `0000X` | `0000` | Preservation of leading zeroes |
| `123A456` | `123` | Correct stopping boundary |
| `999999` | `999999` | Entire string is numeric |
| `777...7X` with length `200000` | All but final `X` | Maximum input size and final-character boundary |
| `X777...7` with length `200000` | `-1` | Maximum input size with no valid prefix |

## Edge Cases

For `A123`, the algorithm examines index `0`, sees that `A` is not a digit, and immediately returns `-1`. It never searches for a later numeric segment, because the required object is a prefix beginning at the first character.

For `123A456`, indices `0`, `1`, and `2` are accepted. At index `3`, the character `A` fails the digit test, so the algorithm returns `s[:3]`, which is `123`. The suffix `456` is deliberately ignored because a prefix cannot skip over `A`.

For `0000X`, every zero passes the digit test, and the scan stops only at `X`. The returned substring is `0000`, preserving all four zeroes. Treating the answer as an integer would lose information that the problem requires us to print.

For `7`, the loop never encounters a non-digit. It reaches the end and returns the complete string `7`. This handles the case where there is no terminating non-digit character.

For a string of length `200000` consisting entirely of digits, every character is processed once and the complete string is returned. The algorithm does not need a special maximum-length branch, so the upper constraint is handled naturally.

For a string whose first character is non-numeric and whose remaining `199999` characters are digits, the algorithm still stops after one character and returns `-1`. This demonstrates why the answer depends only on the first uninterrupted run of digits, not on the presence of digits later in the text.
