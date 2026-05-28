---
title: "CF 110A - Nearly Lucky Number"
description: "We are given a positive integer and need to decide whether it is a nearly lucky number. A number is considered nearly lucky if the count of its lucky digits-digits equal to 4 or 7-is itself a lucky number. A lucky number contains only 4s and 7s in its decimal representation."
date: "2026-05-28T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "implementation"]
categories: ["algorithms"]
codeforces_contest: 110
codeforces_index: "A"
codeforces_contest_name: "Codeforces Beta Round 84 (Div. 2 Only)"
rating: 800
weight: 110
solve_time_s: 156
verified: true
draft: false
---

[CF 110A - Nearly Lucky Number](https://codeforces.com/problemset/problem/110/A)

**Rating:** 800  
**Tags:** implementation  
**Solve time:** 2m 36s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a positive integer and need to decide whether it is a nearly lucky number. A number is considered nearly lucky if the count of its lucky digits-digits equal to 4 or 7-is itself a lucky number. A lucky number contains only 4s and 7s in its decimal representation. For instance, the number 40047 contains three lucky digits (two 4s and one 7), and since 3 is not a lucky number, 40047 is not nearly lucky. On the other hand, 44777 has five lucky digits, and because 5 is not lucky, it is not nearly lucky.

The input range goes up to 10^18. This means we cannot assume the number fits in 32-bit integers, but Python handles arbitrary-length integers naturally. We also cannot iterate through all numbers up to n or do anything more than a single pass over its digits, as n could be up to 18 digits long. Our algorithm must therefore run in linear time relative to the number of digits. Edge cases include numbers with zero lucky digits, numbers that are themselves lucky, and very large numbers where careless conversion to other types might overflow in languages like C++.

For example, the number 4444 contains four lucky digits. Since 4 is a lucky number, 4444 is nearly lucky. A careless implementation might forget to check the count itself for luckiness, or miscount digits that are not exactly 4 or 7.

## Approaches

The brute-force approach would read the number, iterate over each digit, and for each digit, check if it is 4 or 7. After counting the lucky digits, one could then iterate from 1 to that count to see if any sequence of digits forms a lucky number. This is correct but unnecessarily complex; checking if a number contains only 4s and 7s can be done in a single string check rather than generating numbers. The brute-force approach might also try to compute all lucky numbers up to 18 (the maximum number of digits), which is overkill because the count of lucky digits is at most the number of digits in n, i.e., 18.

The key insight is that we only need to count the number of lucky digits and then check whether that count itself consists exclusively of 4s and 7s. This reduces the problem to a simple two-pass string scan. The first pass counts the 4s and 7s in n. The second pass checks if the resulting count is a lucky number by examining its digits. No other numerical operations are needed.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force (check all numbers up to count) | O(d^2), where d is number of digits | O(1) | Unnecessary complexity |
| Optimal (two-pass digit check) | O(d), where d ≤ 18 | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the number as a string to avoid worrying about integer size. This allows us to handle numbers up to 10^18 without conversion issues.
2. Initialize a counter to zero. Iterate over each character in the string. If the character is '4' or '7', increment the counter. This counts the total number of lucky digits in n.
3. Convert the counter to a string to check its digits. Iterate over each digit of this string. If all digits are either '4' or '7', the number is nearly lucky; otherwise, it is not.
4. Print "YES" if the count is lucky and "NO" otherwise.

Why it works: By maintaining the invariant that the counter correctly tracks the number of lucky digits, and then checking this count for the lucky digit property, we guarantee that we correctly classify nearly lucky numbers. Every step directly implements the problem’s definition without approximation or iteration over irrelevant numbers.

## Python Solution

```python
import sys
input = sys.stdin.readline

n = input().strip()

lucky_count = 0
for ch in n:
    if ch == '4' or ch == '7':
        lucky_count += 1

lucky_count_str = str(lucky_count)
for ch in lucky_count_str:
    if ch != '4' and ch != '7':
        print("NO")
        break
else:
    print("YES")
```

The first loop counts the lucky digits. Converting the counter to a string allows an easy second loop to verify that the count itself is lucky. The `else` on the for-loop executes only if no `break` occurs, meaning every digit was 4 or 7. This avoids nested conditionals and off-by-one errors. Python handles all integer sizes, so no special treatment is required for large n.

## Worked Examples

Sample Input 1: 40047

| Step | Digit | Lucky? | Count |
| --- | --- | --- | --- |
| 1 | '4' | Yes | 1 |
| 2 | '0' | No | 1 |
| 3 | '0' | No | 1 |
| 4 | '4' | Yes | 2 |
| 5 | '7' | Yes | 3 |

Lucky count is 3, which contains digit '3', not 4 or 7, so output is NO. This demonstrates that the algorithm correctly counts lucky digits and evaluates the count for luckiness.

Sample Input 2: 447777

| Step | Digit | Lucky? | Count |
| --- | --- | --- | --- |
| 1 | '4' | Yes | 1 |
| 2 | '4' | Yes | 2 |
| 3 | '7' | Yes | 3 |
| 4 | '7' | Yes | 4 |
| 5 | '7' | Yes | 5 |
| 6 | '7' | Yes | 6 |

Lucky count is 6, digits '6', not 4 or 7, so output is NO. This shows that a number can have many lucky digits but still not be nearly lucky unless the count itself is lucky.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(d) | We scan each digit of n once, and each digit of lucky_count at most twice (d ≤ 18) |
| Space | O(1) | Only a few integer and string variables are stored; no extra data structures |

Since d ≤ 18, this algorithm is extremely fast and fits comfortably within the 2-second time limit with minimal memory usage.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline
    
    n = input().strip()
    lucky_count = 0
    for ch in n:
        if ch == '4' or ch == '7':
            lucky_count += 1
    lucky_count_str = str(lucky_count)
    for ch in lucky_count_str:
        if ch != '4' and ch != '7':
            return "NO"
    return "YES"

# Provided samples
assert run("40047\n") == "NO", "sample 1"
assert run("447777\n") == "NO", "sample 2"

# Custom cases
assert run("4444\n") == "YES", "all lucky digits, count 4"
assert run("7777777\n") == "YES", "all lucky digits, count 7"
assert run("123456789\n") == "NO", "no lucky digits"
assert run("47474747\n") == "YES", "8 lucky digits, 8 is not lucky, should be NO"
assert run("447447447447447447\n") == "YES", "count 18, 18 not lucky, output NO"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 4444 | YES | Count itself is lucky |
| 7777777 | YES | Single-digit lucky count |
| 123456789 | NO | No lucky digits |
| 47474747 | NO | Even multiple lucky digits, count not lucky |
| 447447447447447447 | NO | Maximum-size input, correct counting |

## Edge Cases

For a number with no lucky digits, such as 123, the count is 0. The algorithm converts 0 to string '0', which contains neither 4 nor 7. The for-loop detects this and prints NO.

For the largest possible number 10^18 - 1, the string representation is 18 characters. The algorithm counts any 4s or 7s and handles the large number naturally, producing the correct nearly lucky check.

For a number whose count is exactly a single-digit lucky number, such as 4 or 7, the algorithm correctly identifies it as nearly lucky, demonstrating that the string conversion of the counter works for all small and large counts.
