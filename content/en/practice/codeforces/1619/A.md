---
title: "CF 1619A - Square String?"
description: "We are given several strings, and we need to determine for each whether it is a square string. A string is square if it can be expressed as some substring concatenated with itself."
date: "2026-06-10T06:09:18+07:00"
tags: ["codeforces", "competitive-programming", "implementation", "strings"]
categories: ["algorithms"]
codeforces_contest: 1619
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 762 (Div. 3)"
rating: 800
weight: 1619
solve_time_s: 99
verified: false
draft: false
---

[CF 1619A - Square String?](https://codeforces.com/problemset/problem/1619/A)

**Rating:** 800  
**Tags:** implementation, strings  
**Solve time:** 1m 39s  
**Verified:** no  

## Solution
## Problem Understanding

We are given several strings, and we need to determine for each whether it is a square string. A string is square if it can be expressed as some substring concatenated with itself. For example, "abab" is square because it is "ab" repeated twice, while "abcab" is not square because no substring repeated twice produces the original string.

The input consists of an integer `t` followed by `t` strings. Each string has length between 1 and 100. The output is simply "YES" if the string is square, "NO" otherwise.

The constraints are small: up to 100 strings of length up to 100. This allows us to use algorithms that are quadratic in the string length, but ideally we aim for linear or near-linear checks per string.

Edge cases to watch for include strings of odd length. For example, "aaa" has length 3, which cannot be split evenly into two equal halves. Any odd-length string is automatically not square. Another subtle case is a string like "aa" or "aaaa", which are perfectly square, but a naive substring search might overcomplicate the solution if not careful. A string of length 1, like "a", is never square.

## Approaches

The brute-force approach is to consider all possible substrings of length `n/2` and check if repeating them produces the original string. For a string of length `n`, there is only one candidate substring of length `n/2` (the first half). The naive check would slice the string into the first half and the second half and compare them. Each comparison takes O(n/2) time. Since there are up to 100 strings of length up to 100, this approach is acceptable, but we can reason further.

The key observation is that a string is square if and only if its length is even and the first half is identical to the second half. This observation immediately reduces our problem to a simple check: if the length is odd, output "NO"; if the length is even, compare the two halves directly. This is linear per string and uses only O(1) extra space.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force substring repeat check | O(n) per string | O(n) | Accepted |
| Half-split comparison | O(n) per string | O(1) | Accepted |

The half-split method is optimal here and simple to implement.

## Algorithm Walkthrough

1. Read the number of test cases `t`.
2. Loop over each string input.
3. For each string, compute its length `n`.
4. If `n` is odd, print "NO" immediately because an odd-length string cannot be square.
5. If `n` is even, split the string into two halves: the first half contains characters `s[0:n//2]`, the second half `s[n//2:n]`.
6. Compare the two halves. If they are equal, print "YES"; otherwise, print "NO".

Why it works: the only way a string can be square is if it is composed of two identical halves. Checking length first ensures we do not attempt to split an odd-length string, and directly comparing halves guarantees correctness because any mismatch in the halves immediately invalidates the square property.

## Python Solution

```python
import sys
input = sys.stdin.readline

t = int(input())
for _ in range(t):
    s = input().strip()
    n = len(s)
    if n % 2 == 1:
        print("NO")
    else:
        mid = n // 2
        if s[:mid] == s[mid:]:
            print("YES")
        else:
            print("NO")
```

This solution reads all inputs efficiently using `sys.stdin.readline`. Stripping the newline is important to ensure the string length is correct. We check the length parity first to catch the obvious "NO" cases and then compare the two halves directly.

## Worked Examples

**Example 1: "abab"**

| Variable | Value |
| --- | --- |
| s | "abab" |
| n | 4 |
| mid | 2 |
| s[:mid] | "ab" |
| s[mid:] | "ab" |
| comparison | equal → YES |

The algorithm correctly identifies "abab" as square.

**Example 2: "abcab"**

| Variable | Value |
| --- | --- |
| s | "abcab" |
| n | 5 |
| parity | odd → NO |

The odd-length check immediately produces "NO", correctly handling this edge case.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n * t) | Each string comparison is O(n), with t strings total |
| Space | O(1) | We only store string slices and integers for indexing |

With `t ≤ 100` and `n ≤ 100`, the total work is at most 10,000 character comparisons, well within the 1-second limit.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    output = io.StringIO()
    sys.stdout = output
    t = int(input())
    for _ in range(t):
        s = input().strip()
        n = len(s)
        if n % 2 == 1:
            print("NO")
        else:
            mid = n // 2
            if s[:mid] == s[mid:]:
                print("YES")
            else:
                print("NO")
    return output.getvalue().strip()

# provided sample
assert run("10\na\naa\naaa\naaaa\nabab\nabcabc\nabacaba\nxxyy\nxyyx\nxyxy\n") == \
"NO\nYES\nNO\nYES\nYES\nYES\nNO\nNO\nNO\nYES"

# custom cases
assert run("3\nb\ncc\ndd\n") == "NO\nYES\nYES", "single and double letters"
assert run("2\nabcdabcd\nabcabc\n") == "YES\nYES", "multiple repeated substrings"
assert run("1\na"*100+"\n") == "YES", "max size even repeated char"
assert run("1\na"*99+"\n") == "NO", "max size odd repeated char"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| b, cc, dd | NO, YES, YES | single-letter edge and double-letter correctness |
| abcdabcd, abcabc | YES, YES | multiple-character repeats |
| 'a'*100 | YES | max-size even repeated char |
| 'a'*99 | NO | max-size odd repeated char |

## Edge Cases

For a string of length 1 like "a", the algorithm detects odd length and outputs "NO". For a string of length 2 like "aa", it splits into "a" and "a", finds them equal, and outputs "YES". For strings like "xxyy", it splits into "xx" and "yy", detects inequality, and outputs "NO". The algorithm handles all minimal, maximal, and non-uniform repetitions correctly.
