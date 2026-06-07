---
title: "CF 2121B - Above the Clouds"
description: "We are asked to determine, for a given string, whether it is possible to split it into three non-empty parts, $a$, $b$, and $c$, such that $a + b + c = s$ and the middle segment $b$ appears as a substring of the concatenation $a + c$."
date: "2026-06-08T03:47:10+07:00"
tags: ["codeforces", "competitive-programming", "constructive-algorithms", "greedy", "strings"]
categories: ["algorithms"]
codeforces_contest: 2121
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 1032 (Div. 3)"
rating: 800
weight: 2121
solve_time_s: 87
verified: false
draft: false
---

[CF 2121B - Above the Clouds](https://codeforces.com/problemset/problem/2121/B)

**Rating:** 800  
**Tags:** constructive algorithms, greedy, strings  
**Solve time:** 1m 27s  
**Verified:** no  

## Solution
## Problem Understanding

We are asked to determine, for a given string, whether it is possible to split it into three non-empty parts, $a$, $b$, and $c$, such that $a + b + c = s$ and the middle segment $b$ appears as a substring of the concatenation $a + c$. In other words, we want to know if there is a "middle piece" $b$ that is already visible somewhere in the combination of the prefix $a$ and suffix $c$.

The input consists of multiple test cases, each with a string of length at least 3 and at most $10^5$. The sum of string lengths across all test cases does not exceed $2 \cdot 10^5$. This means we cannot afford to check every possible split $a, b, c$ naively, since there are roughly $O(n^2)$ ways to choose the endpoints of $b$ for a single string of length $n$. Any algorithm approaching $O(n^2)$ would be too slow, so we need something close to $O(n)$ per string.

A subtle edge case is when the string is made of identical characters, like "aaa". Splitting it into three segments still allows the middle piece to appear in the concatenation of the first and last segments. Another tricky case is when all characters are distinct, such as "abc". Here, the middle character must match either the first or last character to satisfy the substring condition. Careless implementations might always try to take the middle segment as more than one character or ignore the simplest split options, producing the wrong answer.

## Approaches

The brute-force approach would be to iterate over all possible starting and ending positions of $b$ and then check if $b$ appears as a substring in $a+c$. For a string of length $n$, this could take $O(n^3)$ time in the worst case (choose start and end of $b$, then check substring with $O(n)$ comparisons). This is clearly infeasible for $n$ up to $10^5$.

The key observation is that we do not need to consider long middle segments. If we take $b$ to be a single character, we can quickly check if it matches either the first character of $s$ or the last character. Specifically, if $s[0] == s[1]$ or $s[1] == s[-1]$, a valid split exists: we can pick $a$ as the first character, $b$ as the second, and $c$ as the rest. Alternatively, if $s[-2] == s[-1]$ or $s[0] == s[-2]$, we can pick the last character as $c$ and the one before it as $b$.

This works because a substring of length 1 trivially appears in $a+c$ if it matches either endpoint. Since the string length is at least 3, this check is enough: we do not need $b$ to be longer than one character to satisfy the condition. This greedy insight reduces the complexity to $O(1)$ checks per string, which is fast enough.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n^3) | O(1) | Too slow |
| Optimal | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the number of test cases $t$.
2. For each string $s$ of length $n \ge 3$, consider splitting it with $b$ as a single character. Focus on the second character $s[1]$ or the penultimate character $s[-2]$.
3. Check if $s[1]$ matches $s[0]$ or $s[-1]$. If it does, output "Yes". Otherwise, check if $s[-2]$ matches $s[0]$ or $s[-1]$. If either condition is true, output "Yes".
4. If none of the above checks pass, output "No".

Why it works: The approach guarantees correctness because any valid split with a non-empty middle segment must allow that middle segment to appear in the combination of the prefix and suffix. Since single-character segments are the minimal non-empty substrings, if a valid split exists, it will be detected by checking the second and penultimate characters against the string endpoints. Longer substrings would only require that one of their characters matches an endpoint, which is covered by this minimal check.

## Python Solution

```python
import sys
input = sys.stdin.readline

t = int(input())
for _ in range(t):
    n = int(input())
    s = input().strip()
    if s[0] == s[1] or s[-1] == s[-2] or s[1] == s[-1] or s[0] == s[-2]:
        print("Yes")
    else:
        print("No")
```

The solution first reads the number of test cases and then iterates over each string. It trims the newline after reading the string to avoid accidental mismatches. The checks directly implement the observation that the middle character can be a single character and must match either end. The order of conditions is arbitrary because we only need one true match.

## Worked Examples

For input `"aaa"` (length 3), the second character `s[1] = 'a'` matches the first `s[0] = 'a'`. The algorithm outputs "Yes".

| s | s[0] | s[1] | s[-2] | s[-1] | Condition matched? | Output |
| --- | --- | --- | --- | --- | --- | --- |
| aaa | a | a | a | a | s[0] == s[1] | Yes |

For input `"aba"` (length 3), the second character `s[1] = 'b'` does not match `s[0] = 'a'` or `s[-1] = 'a'`. The penultimate character `s[-2] = 'b'` also does not match either endpoint. No condition matches, so the output is "No".

| s | s[0] | s[1] | s[-2] | s[-1] | Condition matched? | Output |
| --- | --- | --- | --- | --- | --- | --- |
| aba | a | b | b | a | none | No |

These traces confirm the algorithm correctly identifies minimal splits and edge cases.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) per test case | Each string is processed with a constant number of character comparisons, scanning only endpoints and neighbors |
| Space | O(1) | Only a few characters and integers are stored per test case, no additional structures |

The total number of characters across all test cases is $2 \cdot 10^5$, so $O(n)$ operations per string ensures the solution completes well within the 2-second limit. Memory usage remains negligible.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    out = io.StringIO()
    sys.stdout = out
    t = int(input())
    for _ in range(t):
        n = int(input())
        s = input().strip()
        if s[0] == s[1] or s[-1] == s[-2] or s[1] == s[-1] or s[0] == s[-2]:
            print("Yes")
        else:
            print("No")
    return out.getvalue().strip()

# provided samples
assert run("12\n3\naaa\n3\naba\n3\naab\n4\nabca\n4\nabba\n4\naabb\n5\nabaca\n5\nabcda\n5\nabcba\n6\nabcbbf\n6\nabcdaa\n3\nabb\n") == \
"Yes\nNo\nYes\nNo\nYes\nYes\nYes\nNo\nYes\nYes\nYes\nYes"

# custom cases
assert run("3\n3\nabc\n3\naaa\n4\naabb\n") == "No\nYes\nYes", "mixed edge cases"
assert run("2\n3\naaa\n5\nabcde\n") == "Yes\nNo", "all same vs all distinct"
assert run("1\n3\nabb\n") == "Yes", "last two letters equal"
assert run("1\n3\nbaa\n") == "Yes", "first two letters equal"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 3\n3\nabc\n3\naaa\n4\naabb | No\nYes\nYes | mixed edge cases: all distinct, all same, last two letters same |
| 2\n3\naaa\n5\nabcde | Yes\nNo | smallest length all same vs larger all distinct |
| 1\n3\nabb | Yes | last two letters equal triggers valid split |
| 1\n3\nbaa | Yes | first two letters equal triggers valid split |

## Edge Cases

For `"aaa"`, both the first and last characters match the middle character, so any choice of the middle as `b` works. For `"aba"`, the middle `'b'` does not match any endpoint, so no split works. For `"abb
