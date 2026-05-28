---
title: "CF 162J - Brackets"
description: "We are given a string consisting solely of opening and closing round brackets. The task is to determine whether this sequence is balanced, meaning it could represent a correct arrangement of parentheses in a mathematical expression."
date: "2026-05-29T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "*special"]
categories: ["algorithms"]
codeforces_contest: 162
codeforces_index: "J"
codeforces_contest_name: "VK Cup 2012 Wild-card Round 1"
rating: 1800
weight: 162
solve_time_s: 64
verified: true
draft: false
---

[CF 162J - Brackets](https://codeforces.com/problemset/problem/162/J)

**Rating:** 1800  
**Tags:** *special  
**Solve time:** 1m 4s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a string consisting solely of opening and closing round brackets. The task is to determine whether this sequence is balanced, meaning it could represent a correct arrangement of parentheses in a mathematical expression. In other words, every opening bracket must have a matching closing bracket, and brackets must be properly nested. For instance, "(())()" is balanced because each "(" is closed in the correct order, whereas "(()" is not, since one opening bracket remains unmatched, and ")(" is not because a closing bracket appears before any matching opening bracket.

The input string length is guaranteed to be between 1 and 100 characters. This small upper bound implies that any algorithm with linear time complexity or better is acceptable. Quadratic or more complex solutions would also run fast enough due to the low limit, but simplicity and clarity are preferred. Edge cases to be aware of include sequences that start with a closing bracket, sequences that end with an opening bracket, sequences with unmatched brackets in the middle, and sequences consisting entirely of one type of bracket. For example, the string ")" should return "NO" because a closing bracket cannot appear without a preceding opening bracket. Similarly, "(((" should return "NO" because the extra opening brackets remain unmatched.

## Approaches

A brute-force approach would attempt to check every possible substring to see if it forms a valid bracket sequence. This involves recursively or iteratively pairing each opening bracket with a closing bracket and verifying all nested sequences. While correct, this approach has exponential time complexity, O(2^n) in the worst case, and is unnecessary given the constraints. It becomes clearly overkill even for a string of length 20 or more, as the number of checks grows explosively.

The optimal approach leverages a simple counting mechanism using a single integer as a balance counter. We iterate through the string from left to right, increasing the counter for each opening bracket and decreasing it for each closing bracket. If the counter ever goes negative, it indicates that a closing bracket appeared without a matching opening bracket, so the sequence is immediately invalid. After processing the entire string, the sequence is balanced only if the counter is zero, meaning all opening brackets have been matched by closing brackets. This approach works in O(n) time and O(1) space because we only need a single integer to maintain the balance.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(2^n) | O(n) | Too slow |
| Optimal | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

1. Initialize a counter variable to zero. This counter will track the net number of unmatched opening brackets as we scan the sequence.
2. Iterate through each character in the string. If the character is an opening bracket "(", increment the counter because we have one more unmatched opening bracket. If the character is a closing bracket ")", decrement the counter because one unmatched opening bracket has been matched.
3. If at any point during iteration the counter becomes negative, immediately print "NO" and terminate. This indicates that a closing bracket occurred before a corresponding opening bracket, making the sequence unbalanced.
4. After iterating through the entire string, check the counter. If it is exactly zero, print "YES" because every opening bracket has a matching closing bracket. Otherwise, print "NO" because some opening brackets remain unmatched.

Why it works: the counter maintains an invariant that represents the number of currently unmatched opening brackets. A negative value signals an invalid state, and a zero value at the end confirms that every bracket has been properly matched and nested. This invariant guarantees correctness.

## Python Solution

```python
import sys
input = sys.stdin.readline

s = input().strip()
balance = 0

for char in s:
    if char == '(':
        balance += 1
    else:  # char == ')'
        balance -= 1
    if balance < 0:
        print("NO")
        sys.exit()

print("YES" if balance == 0 else "NO")
```

The solution reads the input and removes trailing newlines. The balance counter starts at zero. For each character, we adjust the counter according to the bracket type. If balance goes negative at any point, we immediately print "NO" and terminate, reflecting that the sequence cannot be balanced. After the loop, checking whether balance equals zero ensures that all brackets are matched.

## Worked Examples

Sample Input 1: "(()(()))()"

| Step | Char | Balance | Action |
| --- | --- | --- | --- |
| 1 | ( | 1 | Increment for '(' |
| 2 | ( | 2 | Increment for '(' |
| 3 | ) | 1 | Decrement for ')' |
| 4 | ( | 2 | Increment for '(' |
| 5 | ( | 3 | Increment for '(' |
| 6 | ) | 2 | Decrement for ')' |
| 7 | ) | 1 | Decrement for ')' |
| 8 | ) | 0 | Decrement for ')' |
| 9 | ( | 1 | Increment for '(' |
| 10 | ) | 0 | Decrement for ')' |

Balance ends at 0, so output is "YES". This confirms the algorithm correctly tracks nested pairs and matches.

Sample Input 2: "(()"

| Step | Char | Balance | Action |
| --- | --- | --- | --- |
| 1 | ( | 1 | Increment for '(' |
| 2 | ( | 2 | Increment for '(' |
| 3 | ) | 1 | Decrement for ')' |

Balance ends at 1, indicating one unmatched '('. Output is "NO", correctly identifying an unbalanced sequence.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | We iterate through each character once. |
| Space | O(1) | Only a single integer counter is used. |

Given n ≤ 100, the O(n) solution runs comfortably within the 3-second limit, and the O(1) space ensures memory efficiency.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from contextlib import redirect_stdout
    out = io.StringIO()
    with redirect_stdout(out):
        s = input().strip()
        balance = 0
        for char in s:
            if char == '(':
                balance += 1
            else:
                balance -= 1
            if balance < 0:
                print("NO")
                return
        print("YES" if balance == 0 else "NO")
    return out.getvalue().strip()

# Provided sample
assert run("(()(()))()") == "YES", "sample 1"

# Custom cases
assert run("(") == "NO", "single opening"
assert run(")") == "NO", "single closing"
assert run("()()()") == "YES", "repeated balanced pairs"
assert run("((()))") == "YES", "nested balanced"
assert run("((())") == "NO", "unmatched opening inside"
assert run("())(") == "NO", "early closing unmatched"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| "(" | NO | Single unmatched opening |
| ")" | NO | Single unmatched closing |
| "()()()" | YES | Multiple balanced pairs |
| "((()))" | YES | Nested balanced brackets |
| "((())" | NO | Unmatched opening inside |
| "())(" | NO | Closing before opening |

## Edge Cases

For a string starting with a closing bracket, e.g., ")", the balance immediately becomes negative at step 1, triggering "NO". For a string ending with unmatched openings like "(((", the balance is positive at the end, resulting in "NO". In a perfectly nested sequence like "((()))", the counter increments and decrements correctly, ending at zero, confirming "YES". The algorithm correctly handles all scenarios with early termination and final balance check.
