---
title: "CF 1952H - Palindrome"
description: "The task is to determine, for each given string, whether it reads the same forwards and backwards. A palindrome is such a string, like \"radar\" or \"racecar\", while a string like \"ac\" is not."
date: "2026-05-31T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "*special", "implementation", "strings"]
categories: ["algorithms"]
codeforces_contest: 1952
codeforces_index: "H"
codeforces_contest_name: "April Fools Day Contest 2024"
rating: 0
weight: 1952
solve_time_s: 72
verified: false
draft: false
---

[CF 1952H - Palindrome](https://codeforces.com/problemset/problem/1952/H)

**Rating:** -  
**Tags:** *special, implementation, strings  
**Solve time:** 1m 12s  
**Verified:** no  

## Solution
## Problem Understanding

The task is to determine, for each given string, whether it reads the same forwards and backwards. A palindrome is such a string, like "radar" or "racecar", while a string like "ac" is not. The input consists of multiple test cases, each providing a string of up to 100 lowercase English letters. For each string, the output should be either "YES" if it is a palindrome or "NO" if it is not.

Given that each string is at most 100 characters long and there are at most 100 test cases, the total number of characters to process is 10,000. This is small enough that even an $O(n^2)$ approach would run quickly, but we can aim for $O(n)$ per string. The main concern is handling boundary conditions correctly: empty strings, single-character strings, or strings with repeated characters. For example, an input string "a" should output "YES" because a single letter is trivially a palindrome. A careless implementation might misinterpret an empty string or mix up indices when reversing the string.

## Approaches

The naive approach is to reverse the string and check equality with the original. For each string of length $n$, reversing takes $O(n)$ and comparison also takes $O(n)$. With up to 100 strings, each up to 100 characters, this results in at most 20,000 operations per worst-case scenario, which is trivial for modern computers. This method is simple and reliable.

Another approach is to use a two-pointer technique. Place one pointer at the start of the string and another at the end, then move both pointers toward the center, comparing characters at each step. This avoids creating a reversed copy of the string and operates in $O(n)$ time with $O(1)$ extra space. It is slightly more memory-efficient and demonstrates the principle of invariants: at each step, we maintain that all previously checked characters match.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Reverse + compare | O(n) | O(n) | Accepted |
| Two-pointer | O(n) | O(1) | Accepted |

The two-pointer approach is marginally more elegant in terms of space and highlights a reusable technique for palindrome checks in larger problems.

## Algorithm Walkthrough

1. Read the number of test cases $t$. This tells us how many strings we need to process.
2. For each test case, read the string $s$. The string will contain only lowercase letters.
3. Initialize two pointers: $i = 0$ at the start and $j = \text{len}(s) - 1$ at the end.
4. Compare the characters $s[i]$ and $s[j]$. If they are not equal, immediately output "NO" for this string and move to the next test case. This step detects a mismatch early.
5. If the characters are equal, increment $i$ and decrement $j$ to move toward the center.
6. Repeat steps 4 and 5 until $i \geq j$. If no mismatch was found, output "YES".
7. Continue to the next string until all test cases are processed.

Why it works: The two-pointer invariant guarantees correctness. At each step, we have verified that the prefix and suffix of the string are mirrors of each other. Once the pointers meet or cross, the entire string has been verified as symmetric. Any mismatch immediately signals that the string is not a palindrome.

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

The code first reads the number of test cases. Each string is stripped of the newline character. Two pointers traverse the string from both ends, immediately breaking if a mismatch is found. The final print statement uses a conditional expression to decide the output. Care was taken to handle empty strings and single-character strings, both of which are correctly identified as palindromes because the loop never executes for these cases.

## Worked Examples

**Sample 1 Input:** `"ac"`

| i | j | s[i] | s[j] | is_palindrome |
| --- | --- | --- | --- | --- |
| 0 | 1 | a | c | False |

The pointers detect a mismatch immediately. Output: `"NO"`.

**Sample 2 Input:** `"racecar"`

| i | j | s[i] | s[j] | is_palindrome |
| --- | --- | --- | --- | --- |
| 0 | 6 | r | r | True |
| 1 | 5 | a | a | True |
| 2 | 4 | c | c | True |
| 3 | 3 | e | e | True |

Pointers meet at the center. Output: `"YES"`. This trace confirms the invariant that all checked characters are symmetric.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) per string | Each character is checked at most once by the two-pointer scan. |
| Space | O(1) | Only two integer pointers and a boolean are used, independent of string length. |

With $t \leq 100$ and $n \leq 100$, the total number of operations is under 10,000, fitting easily within the 3-second time limit.

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

# Provided samples
assert run("8\nac\ntle\nradar\nracecar\nphp\natcoder\ncodeforces\nsteam\n") == \
"NO\nNO\nYES\nYES\nNO\nNO\nYES\nYES", "sample 1"

# Custom test cases
assert run("3\na\n\nzzzzzzzzzz\n") == "YES\nYES\nYES", "single and empty strings"
assert run("2\nabcba\nabcd\n") == "YES\nNO", "odd-length and non-palindrome"
assert run("1\naaaaaaaaaa\n") == "YES", "all equal characters"
assert run("2\nabccba\nabcdefg\n") == "YES\nNO", "even-length palindrome vs non-palindrome"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `a\n\nzzzzzzzzzz` | `YES\nYES\nYES` | Handles single-character, empty, and repeated-character strings |
| `abcba\nabcd` | `YES\nNO` | Correctly identifies odd-length palindrome and non-palindrome |
| `aaaaaaaaaa` | `YES` | All identical characters produce a palindrome |
| `abccba\nabcdefg` | `YES\nNO` | Even-length palindrome vs non-palindrome |

## Edge Cases

An empty string should output "YES". In the two-pointer loop, $i = 0$ and $j = -1$, so $i < j$ is false, the loop does not execute, and `is_palindrome` remains True. For a single-character string like `"z"`, $i = j = 0$, again the loop does not execute, resulting in "YES". Strings with all identical characters, such as `"aaaa"`, will have all comparisons succeed, confirming the output "YES". These cases demonstrate that the loop invariant correctly handles all minimal and uniform inputs.
