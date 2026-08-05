---
title: "CF 102700K - Katastrophic sort"
description: "Each input string has a very specific structure. It begins with a non-empty sequence of lowercase letters, followed immediately by a non-empty sequence of digits. We are given two such strings and must compare them using a custom ordering."
date: "2026-08-05T12:31:55+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102700
codeforces_index: "K"
codeforces_contest_name: "2020 ICPC Universidad Nacional de Colombia Programming Contest"
rating: 0
weight: 102700
solve_time_s: 57
verified: true
draft: false
---

[CF 102700K - Katastrophic sort](https://codeforces.com/problemset/problem/102700/K)

**Rating:** -  
**Tags:** -  
**Solve time:** 57s  
**Verified:** yes  

## Solution
## Problem Understanding

Each input string has a very specific structure. It begins with a non-empty sequence of lowercase letters, followed immediately by a non-empty sequence of digits. We are given two such strings and must compare them using a custom ordering.

The comparison behaves exactly like ordinary lexicographical order until the numeric suffix is reached. The difference is that the entire numeric suffix is treated as a single integer instead of a sequence of characters. For example, `"z2"` should come before `"z11"` because the integers satisfy `2 < 11`, even though the character `'2'` is lexicographically greater than `'1'`.

The strings can each be as long as $10^5$ characters. Since there are only two strings, reading the input already requires linear time. Any solution that repeatedly scans the strings or performs quadratic work would be unnecessary. A single pass through each string is easily fast enough. The numeric suffix may contain up to $10^5$ digits, so converting it into an integer is a bad idea in languages with fixed-size integer types because it would overflow. Even in Python, constructing such a huge integer is slower than necessary. Comparing the numeric parts as digit strings is sufficient.

Several edge cases deserve attention.

Suppose the alphabetic prefixes differ.

```
abd14
abc14
```

The correct answer is `>` because `"abd"` is lexicographically greater than `"abc"`. A careless implementation that always compares the numeric parts first would incorrectly report equality.

Suppose the prefixes are equal but the numbers have different lengths.

```
x9
x10
```

The correct answer is `<`. Comparing the numeric strings lexicographically would incorrectly conclude `"9" > "10"`. For integers without leading zeroes, the longer digit string always represents the larger number.

Suppose both strings are identical.

```
asgfsd4213456
asgfsd4213456
```

The correct answer is `=`. After both the prefixes and numeric parts match, the comparison must report equality instead of falling through to an arbitrary result.

## Approaches

A direct brute-force idea is to split each string into its alphabetic and numeric parts, convert the numeric suffix into an integer, then compare the prefixes first and the integers second. This produces the correct ordering because it matches the problem definition exactly.

The weakness is the integer conversion. The numeric suffix may contain up to $10^5$ digits, far beyond the capacity of standard integer types in most languages. Even languages with arbitrary precision integers must allocate and process an enormous integer object, which is unnecessary work.

The key observation is that the numeric parts never contain leading zeroes. That gives a very convenient property. If two positive integers have different numbers of digits, the one with more digits is larger. Only when the digit counts are equal do we need a lexicographical comparison of the digit strings, because equal-length decimal representations preserve numeric order.

This lets us compare the numbers without ever parsing them as integers. We only split each string once, compare the alphabetic prefixes, compare the lengths of the numeric suffixes if necessary, and finally compare the digit strings when the lengths match.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n) | O(n) | Accepted in Python, unsafe because of huge integer conversion |
| Optimal | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Read the two input strings.
2. For each string, scan from the beginning until the first digit appears. Everything before that position is the alphabetic prefix, and everything from that position onward is the numeric suffix.
3. Compare the alphabetic prefixes lexicographically. If they differ, output `<` or `>` according to their lexicographical order and stop. The numeric part is irrelevant once the prefixes differ.
4. Compare the lengths of the numeric suffixes. If one suffix has more digits, it represents the larger integer because leading zeroes are forbidden.
5. If the numeric suffixes have the same length, compare them lexicographically as strings. Equal-length decimal strings have the same ordering as their corresponding integers.
6. Output `<`, `>`, or `=` according to the result.

### Why it works

The comparison always follows the same order as the Katastrophic ordering. The alphabetic prefixes determine the result whenever they differ because they appear before the numeric suffixes. When the prefixes are equal, only the represented integers matter. Without leading zeroes, integer comparison is equivalent to comparing digit counts first and lexicographical order second. Every decision made by the algorithm exactly matches these rules, so the produced ordering is always correct.

## Python Solution

```python
import sys
input = sys.stdin.readline

def split_parts(s):
    i = 0
    while i < len(s) and s[i].isalpha():
        i += 1
    return s[:i], s[i:]

a = input().strip()
b = input().strip()

pa, na = split_parts(a)
pb, nb = split_parts(b)

if pa < pb:
    print("<")
elif pa > pb:
    print(">")
else:
    if len(na) < len(nb):
        print("<")
    elif len(na) > len(nb):
        print(">")
    else:
        if na < nb:
            print("<")
        elif na > nb:
            print(">")
        else:
            print("=")
```

The helper function performs exactly one scan until the first digit, producing the two required pieces of each string. Since the input format guarantees that every string consists of letters followed by digits, no additional validation is necessary.

The first comparison is between the alphabetic prefixes because they have higher priority in the ordering. Only when they are identical does the algorithm continue to the numeric suffixes.

Instead of converting the numeric suffixes into integers, the implementation first compares their lengths. This avoids overflow and unnecessary big integer construction. Only when the lengths match does it compare the digit strings directly, which is mathematically equivalent to integer comparison for equal-length decimal representations without leading zeroes.

The implementation carefully preserves the comparison order. Swapping the numeric comparison before the prefix comparison would produce incorrect results whenever the alphabetic prefixes differ.

## Worked Examples

### Sample 1

Input:

```
z2
z11
```

| Step | Prefix 1 | Prefix 2 | Number 1 | Number 2 | Decision |
| --- | --- | --- | --- | --- | --- |
| Split | z | z | 2 | 11 | Prefixes equal |
| Length comparison | z | z | 1 | 2 | First number is smaller |

Output:

```
<
```

This example shows why numeric length matters. A character-by-character comparison of `"2"` and `"11"` would produce the wrong ordering.

### Sample 2

Input:

```
abd14
abc14
```

| Step | Prefix 1 | Prefix 2 | Number 1 | Number 2 | Decision |
| --- | --- | --- | --- | --- | --- |
| Split | abd | abc | 14 | 14 | Prefixes differ |
| Prefix comparison | abd | abc | 14 | 14 | `abd > abc` |

Output:

```
>
```

This example demonstrates that the numeric suffix is ignored once the alphabetic prefixes determine the ordering.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Each string is scanned once, followed by linear string comparisons |
| Space | O(n) | The sliced prefix and suffix strings together contain all original characters |

The running time is linear in the total input size, which is optimal because every character must be read at least once. The memory usage is also linear due to the created substrings, comfortably fitting within the given limits.

## Test Cases

```python
import sys
import io

def solve():
    input = sys.stdin.readline

    def split_parts(s):
        i = 0
        while i < len(s) and s[i].isalpha():
            i += 1
        return s[:i], s[i:]

    a = input().strip()
    b = input().strip()

    pa, na = split_parts(a)
    pb, nb = split_parts(b)

    if pa < pb:
        print("<")
    elif pa > pb:
        print(">")
    else:
        if len(na) < len(nb):
            print("<")
        elif len(na) > len(nb):
            print(">")
        else:
            if na < nb:
                print("<")
            elif na > nb:
                print(">")
            else:
                print("=")

def run(inp: str) -> str:
    backup_stdin = sys.stdin
    backup_stdout = sys.stdout
    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()
    solve()
    out = sys.stdout.getvalue()
    sys.stdin = backup_stdin
    sys.stdout = backup_stdout
    return out

assert run("z2\nz11\n") == "<\n", "sample 1"
assert run("abd14\nabc14\n") == ">\n", "sample 2"
assert run("asgfsd4213456\nasgfsd4213456\n") == "=\n", "sample 3"

assert run("a1\na2\n") == "<\n", "minimum numeric comparison"
assert run("b999\nb1000\n") == "<\n", "different digit counts"
assert run("zzz5\nzza999\n") == ">\n", "prefix comparison dominates"
assert run("abc12345678901234567890\nabc12345678901234567891\n") == "<\n", "very large numbers without integer conversion"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `a1`, `a2` | `<` | Smallest valid comparison |
| `b999`, `b1000` | `<` | Numeric comparison by digit count |
| `zzz5`, `zza999` | `>` | Prefix comparison has priority |
| Very long equal-length numbers | `<` | No integer conversion is required |

## Edge Cases

Consider the input

```
abd14
abc14
```

The algorithm splits the strings into `"abd"` and `"14"`, and `"abc"` and `"14"`. The prefixes differ immediately, so it compares `"abd"` with `"abc"` and outputs `>`. The numeric suffixes are never examined because they cannot affect the result once the prefixes differ.

Consider the input

```
x9
x10
```

The prefixes are both `"x"`, so the algorithm continues to the numeric comparison. The suffixes have lengths `1` and `2`, making `"10"` the larger integer. The algorithm correctly outputs `<` without converting either number into an integer.

Consider the input

```
asgfsd4213456
asgfsd4213456
```

The prefixes match exactly, the numeric suffixes have the same length, and the digit strings are identical. Every comparison reports equality, so the final output is `=`. This confirms that the algorithm does not incorrectly report one string as larger when every component matches.
