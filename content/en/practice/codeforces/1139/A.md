---
title: "CF 1139A - Even Substrings"
description: "We are given a string of digits from 1 to 9. Our task is to count how many substrings, defined by any contiguous range of indices, represent even numbers. A substring is even if its last digit is even, since the number’s parity is determined entirely by the last digit."
date: "2026-06-12T03:50:18+07:00"
tags: ["codeforces", "competitive-programming", "implementation", "strings"]
categories: ["algorithms"]
codeforces_contest: 1139
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 548 (Div. 2)"
rating: 800
weight: 1139
solve_time_s: 68
verified: true
draft: false
---

[CF 1139A - Even Substrings](https://codeforces.com/problemset/problem/1139/A)

**Rating:** 800  
**Tags:** implementation, strings  
**Solve time:** 1m 8s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a string of digits from 1 to 9. Our task is to count how many substrings, defined by any contiguous range of indices, represent even numbers. A substring is even if its last digit is even, since the number’s parity is determined entirely by the last digit.

The input size can be up to 65,000 digits. This rules out any solution that explicitly constructs all substrings because the total number of substrings is roughly $n(n+1)/2$, which is over 2 billion for $n = 65,000$. Any algorithm that tries to iterate over all substrings and convert them to integers would be far too slow.

A subtle edge case is a string composed entirely of odd digits. For example, "1357" should produce an output of 0, because no substring ends with an even digit. Another edge case is when every digit is even, like "246", where every substring will be counted. Handling these correctly depends on counting substrings based on the last digit rather than attempting arithmetic on full substrings.

## Approaches

The brute-force approach would iterate over all possible starting and ending indices of substrings, convert the substring into a number, and check if it is divisible by 2. This is correct but too slow because it requires $O(n^2)$ substring extractions and integer conversions. With $n = 65,000$, this is roughly $2 \times 10^9$ operations, which exceeds reasonable limits for a 0-second time constraint.

The key insight is that the parity of a number depends only on its last digit. A substring ending at position $i$ is even if $s[i]$ is one of 2, 4, 6, or 8. Every substring that ends at this position can be counted directly: there are exactly $i$ substrings ending at index $i$. Therefore, instead of generating substrings, we simply iterate through the string and, whenever we see an even digit, we add its position (1-indexed) to our running total. This reduces the time complexity to $O(n)$ and avoids unnecessary string or integer manipulations.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n²) | O(1) | Too slow |
| Optimal | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the input string and its length. We will iterate through the string from left to right using a 1-based index.
2. Initialize a counter to zero. This counter will accumulate the total number of even substrings.
3. For each character at index $i$, convert it to an integer to check its parity.
4. If the digit is even (2, 4, 6, 8), increment the counter by $i$. This works because every substring ending at this position is uniquely identified by its starting index from 1 to $i$.
5. Continue until the end of the string and then print the counter.

Why it works: the invariant is that for each index $i$, the total number of substrings ending at $i$ is exactly $i$, and each substring ending in an even digit contributes to the answer. Since we visit every index exactly once and count all substrings ending with even digits, no valid substring is missed or double-counted.

## Python Solution

```python
import sys
input = sys.stdin.readline

n = int(input())
s = input().strip()

count = 0
for i, c in enumerate(s, start=1):
    if int(c) % 2 == 0:
        count += i

print(count)
```

The solution reads the input string and enumerates it with a 1-based index. For each character, we check if it is even and, if so, add its index to the total count. We do not need to store substrings or convert multiple characters into numbers, which keeps both memory and computation low.

## Worked Examples

**Sample 1:**

Input: "1234"

| i | s[i] | is_even? | count update | total count |
| --- | --- | --- | --- | --- |
| 1 | 1 | no | - | 0 |
| 2 | 2 | yes | +2 | 2 |
| 3 | 3 | no | - | 2 |
| 4 | 4 | yes | +4 | 6 |

This confirms that substrings ending at positions 2 and 4 are counted correctly.

**Sample 2:**

Input: "246"

| i | s[i] | is_even? | count update | total count |
| --- | --- | --- | --- | --- |
| 1 | 2 | yes | +1 | 1 |
| 2 | 4 | yes | +2 | 3 |
| 3 | 6 | yes | +3 | 6 |

All substrings are counted, demonstrating correct handling of consecutive even digits.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Each character is visited once and the parity check is O(1). |
| Space | O(1) | Only a counter is used; no additional storage is needed. |

Given $n \le 65,000$, the algorithm performs at most 65,000 operations, which is well within the limit.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    n = int(input())
    s = input().strip()
    count = 0
    for i, c in enumerate(s, start=1):
        if int(c) % 2 == 0:
            count += i
    return str(count)

# Provided samples
assert run("4\n1234\n") == "6", "sample 1"
assert run("3\n246\n") == "6", "sample 2"

# Custom cases
assert run("1\n1\n") == "0", "single odd digit"
assert run("1\n2\n") == "1", "single even digit"
assert run("5\n11111\n") == "0", "all odd digits"
assert run("5\n22222\n") == "15", "all even digits"
assert run("6\n135792\n") == "6", "mixed digits, only last even matters"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 | 0 | single odd digit, count is zero |
| 2 | 1 | single even digit, minimal non-zero count |
| 11111 | 0 | all odd digits, no substrings counted |
| 22222 | 15 | all even digits, sum of indices 1+2+3+4+5 |
| 135792 | 6 | mixed digits, last even digit counts correctly |

## Edge Cases

For a single-digit string "1", the algorithm correctly outputs 0 because the only substring ends with an odd digit. For a string with all even digits like "22222", each index contributes its 1-based position to the total, yielding 1+2+3+4+5 = 15. For alternating parity like "135792", the only even digits are at positions 2 and 6, contributing 2+6=8 to the total, confirming the algorithm does not miss or double-count substrings.
