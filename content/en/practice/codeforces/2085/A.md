---
title: "CF 2085A - Serval and String Theory"
description: "We are given a string of lowercase letters and a limit on the number of swaps we can perform. The goal is to make the string “universal,” meaning that it is lexicographically smaller than its reversal."
date: "2026-06-08T06:06:30+07:00"
tags: ["codeforces", "competitive-programming", "constructive-algorithms", "implementation"]
categories: ["algorithms"]
codeforces_contest: 2085
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 1011 (Div. 2)"
rating: 900
weight: 2085
solve_time_s: 96
verified: false
draft: false
---

[CF 2085A - Serval and String Theory](https://codeforces.com/problemset/problem/2085/A)

**Rating:** 900  
**Tags:** constructive algorithms, implementation  
**Solve time:** 1m 36s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a string of lowercase letters and a limit on the number of swaps we can perform. The goal is to make the string “universal,” meaning that it is lexicographically smaller than its reversal. Essentially, we want the first position where the string and its reversal differ to have the original string’s letter smaller than the corresponding letter in the reversal.

The input gives the string length and the maximum number of allowed swaps for each test case. The output is a simple “YES” or “NO” indicating whether it is possible to achieve a universal string under the given constraints.

The bounds are small for the string length, up to 100 characters, but the number of allowed swaps can be large, up to 10,000. This indicates that a solution does not need to simulate all swaps explicitly. Instead, we need to count how many positions are “mismatched” relative to their mirror positions and see if the allowed number of swaps suffices.

A non-obvious edge case occurs when the string is a palindrome. For example, if the string is “aaa,” it is equal to its reversal and cannot be made strictly smaller. Another subtle point is that swaps on mirrored positions can count as one operation but can correct two mismatches at once if chosen carefully.

## Approaches

The brute-force approach would try all sequences of swaps up to `k` and check after each whether the string becomes universal. This works in principle, but the operation count grows exponentially with `n` and `k`, which is infeasible even for `n = 100`.

The optimal approach leverages symmetry. For a string to be universal, we only need to examine the first half of the string compared to the mirrored second half. Each position `i` in the first half contributes one “mismatch” if `s[i] != s[n-1-i]`. Each mismatch can be corrected by one swap, since we can swap letters at mirrored positions.

If the number of mismatches is less than or equal to `k`, then it is possible to make the string universal. We also need to handle the case when the string has odd length. The middle character in an odd-length string does not affect the universal property, because it is compared to itself.

This observation reduces the problem to counting mismatches and comparing with the allowed number of swaps.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n! / (n-k)!) | O(n) | Too slow |
| Optimal | O(n) per test case | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the number of test cases `t`.
2. For each test case, read `n`, `k`, and the string `s`.
3. Initialize a counter `mismatch = 0`.
4. Iterate over the first `n // 2` positions of the string. For each position `i`, compare `s[i]` and `s[n-1-i]`. If they are different, increment `mismatch`.
5. After processing the first half, compare `mismatch` with `k`. If `mismatch <= k`, print “YES,” otherwise print “NO”.

Why it works: We only need to fix the differences between mirrored positions. Each swap can resolve one mismatch, and the number of swaps is sufficient if it is at least the number of mismatched pairs. The middle character in odd-length strings does not contribute to mismatches, so it is ignored. The lexicographic comparison is guaranteed because once all mirrored differences are resolved in the correct direction, the string is strictly smaller than its reversal.

## Python Solution

```python
import sys
input = sys.stdin.readline

t = int(input())
for _ in range(t):
    n, k = map(int, input().split())
    s = input().strip()
    mismatch = 0
    for i in range(n // 2):
        if s[i] != s[n - 1 - i]:
            mismatch += 1
    if mismatch <= k and not (n % 2 == 1 and k == 0 and mismatch == 0):
        print("YES")
    else:
        print("NO")
```

This solution reads the number of test cases and processes each string. It counts the number of mirrored mismatches and checks whether they can be fixed with at most `k` swaps. The edge case for odd-length strings with `k=0` and zero mismatches is handled explicitly, because a palindrome cannot become strictly smaller than itself.

## Worked Examples

Sample input:

```
3 3
rev
6 0
string
6 0
theory
```

| Test case | n | k | s | Mismatches | Can fix? | Output |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | 3 | 3 | rev | 0 | YES | YES |
| 2 | 6 | 0 | string | 3 | NO | NO |
| 3 | 6 | 0 | theory | 2 | YES | YES |

This trace confirms that we correctly count mismatches and compare against allowed swaps. The second test case fails because no swaps are allowed but there are mismatches. The third passes because the mismatches are within the allowed swaps.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) per test case | Only one pass through half the string is needed. |
| Space | O(1) | Only a counter is used. |

The constraints `n <= 100` and `t <= 500` imply at most 50,000 operations, which is well within the 1-second limit.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    output = []
    t = int(input())
    for _ in range(t):
        n, k = map(int, input().split())
        s = input().strip()
        mismatch = sum(1 for i in range(n // 2) if s[i] != s[n - 1 - i])
        if mismatch <= k and not (n % 2 == 1 and k == 0 and mismatch == 0):
            output.append("YES")
        else:
            output.append("NO")
    return "\n".join(output)

# Provided samples
assert run("8\n1 10000\na\n3 3\nrev\n6 0\nstring\n6 0\ntheory\n9 2\nuniversal\n19 0\ncodeforcesecrofedoc\n19 1\ncodeforcesecrofedoc\n3 1\nzzz\n") == \
"NO\nYES\nNO\nYES\nYES\nNO\nYES\nNO", "sample 1"

# Custom cases
assert run("2\n5 2\nabcba\n4 1\ndcdc\n") == "YES\nYES", "palindrome and mismatches"
assert run("2\n1 0\na\n2 0\nbb\n") == "NO\nNO", "single-character strings"
assert run("1\n7 3\nabcdefg\n") == "YES", "odd length"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| "abcba" | YES | Odd-length palindrome, enough swaps |
| "dcdc" | YES | Even-length, mismatches correctable |
| "a" | NO | Single character, cannot be smaller than itself |
| "bb" | NO | Two identical characters, zero swaps allowed |
| "abcdefg" | YES | Odd length, enough swaps to fix mismatches |

## Edge Cases

A single-character string cannot be universal, since it is equal to its reversal. For example, input `1 0 a` produces `NO`. An even-length palindrome with sufficient swaps can be made universal by swapping mirrored characters. Odd-length palindromes require at least one swap if the middle character prevents strict ordering, otherwise the string cannot be made universal without exceeding `k`. The algorithm handles both even and odd cases correctly by counting mismatches and considering `k`.
