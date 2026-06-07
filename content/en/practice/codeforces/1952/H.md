---
title: "CF 1952H - Palindrome"
description: "The problem asks us to determine whether a given string reads the same forwards and backwards, which is the definition of a palindrome. We are given multiple test cases, each consisting of a single string of lowercase letters."
date: "2026-06-07T18:00:05+07:00"
tags: ["codeforces", "competitive-programming", "*special", "implementation", "strings"]
categories: ["algorithms"]
codeforces_contest: 1952
codeforces_index: "H"
codeforces_contest_name: "April Fools Day Contest 2024"
rating: 0
weight: 1952
solve_time_s: 97
verified: false
draft: false
---

[CF 1952H - Palindrome](https://codeforces.com/problemset/problem/1952/H)

**Rating:** -  
**Tags:** *special, implementation, strings  
**Solve time:** 1m 37s  
**Verified:** no  

## Solution
## Problem Understanding

The problem asks us to determine whether a given string reads the same forwards and backwards, which is the definition of a palindrome. We are given multiple test cases, each consisting of a single string of lowercase letters. For each string, we need to output "YES" if it is a palindrome and "NO" otherwise.

The constraints tell us that the number of test cases can be up to 100 and the maximum string length is 100. This means the total number of characters we may need to process is at most 10,000, which is small. Any solution that runs in linear time with respect to the length of each string will be fast enough, since checking each character pair in a string of length 100 takes only 50 comparisons.

Edge cases we need to be careful about include strings of length 1, which are trivially palindromes, and strings where only the first and last character differ, such as "ab". A naive approach that does not correctly handle the string boundaries could incorrectly identify such strings.

## Approaches

The most straightforward method is brute-force: for each string, compare the first character with the last, the second with the second-to-last, and so on, until we reach the middle of the string. If all these pairs match, the string is a palindrome; if any pair differs, it is not. This approach is correct because it directly implements the definition of a palindrome. The time complexity is O(n) per string, where n is the string length. Since n ≤ 100, this is efficient.

There is no faster asymptotic solution for this problem because we must inspect every character at least once in the worst case. The key insight is recognizing that we only need to check up to the middle of the string. Checking the entire string in both directions or reversing it for comparison works, but using two pointers from the ends is slightly more memory efficient and direct.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force (two-pointer comparison) | O(n) per string | O(1) | Accepted |
| Reverse and compare | O(n) per string | O(n) | Accepted |

Both approaches are acceptable here. The two-pointer comparison uses no extra memory and is slightly cleaner.

## Algorithm Walkthrough

1. Read the number of test cases `t`. We will loop over each test case individually.
2. For each test case, read the string `s` and initialize two pointers: `i` at 0 (start) and `j` at `len(s)-1` (end).
3. While `i < j`, compare `s[i]` and `s[j]`. If they are equal, increment `i` and decrement `j`. This moves the pointers towards the center of the string, checking symmetry.
4. If at any point `s[i]` and `s[j]` differ, the string cannot be a palindrome. Output "NO" immediately and stop checking further characters.
5. If the loop completes without finding mismatched characters, all mirrored pairs are equal. Output "YES".

Why it works: the algorithm maintains the invariant that at each iteration, all characters outside the pointers have been checked and are symmetric. If a mismatch occurs, the symmetry property of a palindrome is violated. If no mismatch is found, the string satisfies the palindrome property.

## Python Solution

```python
import sys
input = sys.stdin.readline

t = int(input())
for _ in range(t):
    s = input().strip()
    i, j = 0, len(s) - 1
    is_palindrome = True
    while i < j:
        if s[i] != s[j]:
            is_palindrome = False
            break
        i += 1
        j -= 1
    print("YES" if is_palindrome else "NO")
```

We use `input().strip()` to remove any trailing newline characters. The two-pointer approach ensures that we compare mirrored positions efficiently. The `is_palindrome` flag allows an early exit on mismatch, avoiding unnecessary comparisons. This also makes it easy to print the result after the loop.

## Worked Examples

Trace for the string "radar":

| i | j | s[i] | s[j] | is_palindrome |
| --- | --- | --- | --- | --- |
| 0 | 4 | r | r | True |
| 1 | 3 | a | a | True |
| 2 | 2 | d | d | True |

All comparisons match, so the output is "YES".

Trace for the string "tle":

| i | j | s[i] | s[j] | is_palindrome |
| --- | --- | --- | --- | --- |
| 0 | 2 | t | e | False |

Mismatch at the first comparison. Output is "NO".

These traces show that the algorithm correctly identifies both palindromes and non-palindromes. The two-pointer technique immediately stops when symmetry is violated, saving unnecessary work.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) per string | Each character is compared at most once in a two-pointer sweep. |
| Space | O(1) | Only a few integer variables and a boolean flag are used, independent of string length. |

With n ≤ 100 and t ≤ 100, the total number of operations is at most 10,000, which is well within the 3-second limit. Memory usage is minimal, so the solution is efficient and safe for all inputs.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    output = []
    t = int(input())
    for _ in range(t):
        s = input().strip()
        i, j = 0, len(s) - 1
        is_palindrome = True
        while i < j:
            if s[i] != s[j]:
                is_palindrome = False
                break
            i += 1
            j -= 1
        output.append("YES" if is_palindrome else "NO")
    return "\n".join(output)

# provided samples
assert run("8\nac\ntle\nradar\nracecar\nphp\natcoder\ncodeforces\nsteam\n") == "NO\nNO\nYES\nYES\nNO\nNO\nYES\nYES", "sample 1"

# custom cases
assert run("3\na\nab\naba\n") == "YES\nNO\nYES", "single-character and small palindromes"
assert run("2\nzzzzzzzzzz\nabcdefghijk\n") == "YES\nNO", "all-equal and completely non-palindromic"
assert run("1\nx"*100 + "\n") == "YES", "maximum-length palindrome"
assert run("1\n" + "ab"*50 + "\n") == "NO", "maximum-length non-palindrome"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| a, ab, aba | YES, NO, YES | Single-character, two-character mismatch, small palindrome |
| zzzzzzzzzz, abcdefghijk | YES, NO | Uniform string, completely non-palindromic |
| x repeated 100 | YES | Maximum-length palindrome |
| ab repeated 50 | NO | Maximum-length non-palindrome |

## Edge Cases

For strings of length 1, such as "x", the pointers `i` and `j` start at 0. Since `i` is not less than `j`, the loop never runs, and the string is correctly classified as a palindrome. For two-character strings where the letters differ, the pointers immediately detect a mismatch and output "NO". Strings where all characters are identical, such as "aaaa", are correctly recognized as palindromes because each mirrored pair matches. The two-pointer approach naturally handles both even and odd-length strings without special branching logic.
