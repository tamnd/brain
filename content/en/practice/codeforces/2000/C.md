---
title: "CF 2000C - Numeric String Template"
description: "The problem asks us to check whether a string matches a numeric template. The template is an array of integers where the same number should correspond to the same letter in a string, and the same letter should correspond to the same number."
date: "2026-06-08T14:11:26+07:00"
tags: ["codeforces", "competitive-programming", "data-structures", "strings"]
categories: ["algorithms"]
codeforces_contest: 2000
codeforces_index: "C"
codeforces_contest_name: "Codeforces Round 966 (Div. 3)"
rating: 1000
weight: 2000
solve_time_s: 156
verified: true
draft: false
---

[CF 2000C - Numeric String Template](https://codeforces.com/problemset/problem/2000/C)

**Rating:** 1000  
**Tags:** data structures, strings  
**Solve time:** 2m 36s  
**Verified:** yes  

## Solution
## Problem Understanding

The problem asks us to check whether a string matches a numeric template. The template is an array of integers where the same number should correspond to the same letter in a string, and the same letter should correspond to the same number. In other words, there must be a one-to-one mapping between the distinct elements of the array and the distinct letters of the string. Each test case provides a numeric template and a set of strings, and we need to determine for each string whether it satisfies this correspondence.

The constraints tell us that the total sum of array lengths and the total sum of string lengths across all test cases is at most 200,000. This implies we need a solution that processes each element or character in linear time; any solution with quadratic complexity on string length would be too slow. Edge cases include arrays with repeated numbers, strings with repeated letters, single-element arrays, or arrays with negative numbers. A naive approach might miss inconsistencies where two letters map to the same number or two numbers map to the same letter.

For example, for an array `[3,5,2,1,3]` and string `"abfda"`, `3` appears twice and maps to `'a'` both times, and all other numbers map to distinct letters, so it matches. But `"afbfa"` fails because `'f'` appears in positions corresponding to both `5` and `1`, breaking the one-to-one mapping.

## Approaches

The brute-force approach would be to try all possible mappings between numbers and letters for each string, but this is clearly infeasible because the number of permutations of mappings grows exponentially with the number of distinct numbers or letters. The key insight is that we do not need to try mappings; we just need to check consistency. We can maintain two dictionaries: one mapping numbers to letters and one mapping letters to numbers. While iterating through the template and the string simultaneously, we check that every mapping is consistent with previous mappings. If we ever encounter a mismatch, the string does not match the template. If we reach the end without inconsistencies, it matches. This works in linear time relative to the length of the string.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(k!) where k = number of distinct numbers | O(k) | Too slow |
| Mapping Check | O(n) per string | O(n) per string | Accepted |

## Algorithm Walkthrough

1. Read the number of test cases `t`.
2. For each test case, read `n` and the array `a`.
3. Read the number of strings `m`.
4. For each string `s`:

a. If the length of `s` does not match `n`, immediately output `"NO"`.

b. Initialize two empty dictionaries: `num_to_char` for mapping numbers to letters, and `char_to_num` for letters to numbers.

c. Iterate over each index `i` from `0` to `n-1`. For the current number `a[i]` and character `s[i]`:

i. If `a[i]` already has a mapping in `num_to_char`, check that it matches `s[i]`. If not, output `"NO"` and stop checking this string.

ii. If `s[i]` already has a mapping in `char_to_num`, check that it matches `a[i]`. If not, output `"NO"` and stop.

iii. If both mappings are consistent or new, update the dictionaries.

d. If the loop completes without inconsistency, output `"YES"`.

**Why it works**: The dictionaries maintain the invariant that each number maps to exactly one letter and each letter maps to exactly one number. Any violation of this invariant immediately identifies a mismatch, ensuring correctness.

## Python Solution

```python
import sys
input = sys.stdin.readline

t = int(input())
for _ in range(t):
    n = int(input())
    a = list(map(int, input().split()))
    m = int(input())
    for _ in range(m):
        s = input().strip()
        if len(s) != n:
            print("NO")
            continue
        
        num_to_char = {}
        char_to_num = {}
        valid = True
        for ai, ci in zip(a, s):
            if ai in num_to_char and num_to_char[ai] != ci:
                valid = False
                break
            if ci in char_to_num and char_to_num[ci] != ai:
                valid = False
                break
            num_to_char[ai] = ci
            char_to_num[ci] = ai
        print("YES" if valid else "NO")
```

The solution reads input efficiently using `sys.stdin.readline` and iterates through each string, checking mapping consistency using two dictionaries. The use of `zip(a, s)` ensures that we compare corresponding positions directly. Using dictionaries avoids repeated scanning, maintaining linear complexity per string.

## Worked Examples

**Example 1**

Input:

Array `a = [3,5,2,1,3]`, string `s = "abfda"`

| Index | a[i] | s[i] | num_to_char | char_to_num | Valid? |
| --- | --- | --- | --- | --- | --- |
| 0 | 3 | a | {3: a} | {a: 3} | Yes |
| 1 | 5 | b | {3: a,5: b} | {a:3,b:5} | Yes |
| 2 | 2 | f | {3:a,5:b,2:f} | {a:3,b:5,f:2} | Yes |
| 3 | 1 | d | {3:a,5:b,2:f,1:d} | {a:3,b:5,f:2,d:1} | Yes |
| 4 | 3 | a | consistent | consistent | Yes |

Output: `"YES"`

**Example 2**

Input: Array `[3,5,2,1,3]`, string `"afbfa"`

At index 2, `s[2] = f` corresponds to `a[2]=2`, but later `f` at a position corresponds to a different number, violating the mapping, so `"NO"`.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(sum of n + sum of lengths of all strings) | Each element of the array and each character of each string is processed once. |
| Space | O(n) | For each string, dictionaries may contain up to `n` entries. |

Given constraints, this solution is efficient and will run well within limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    output = []
    t = int(input())
    for _ in range(t):
        n = int(input())
        a = list(map(int, input().split()))
        m = int(input())
        for _ in range(m):
            s = input().strip()
            if len(s) != n:
                output.append("NO")
                continue
            num_to_char = {}
            char_to_num = {}
            valid = True
            for ai, ci in zip(a, s):
                if ai in num_to_char and num_to_char[ai] != ci:
                    valid = False
                    break
                if ci in char_to_num and char_to_num[ci] != ai:
                    valid = False
                    break
                num_to_char[ai] = ci
                char_to_num[ci] = ai
            output.append("YES" if valid else "NO")
    return "\n".join(output)

# Provided sample
assert run("""3
5
3 5 2 1 3
2
abfda
afbfa
2
1 2
3
ab
abc
aa
4
5 -3 5 -3
4
aaaa
bcbc
aba
cbcb
""") == """YES
NO
YES
NO
NO
NO
YES
NO
YES""", "sample 1"

# Custom cases
assert run("""1
3
1 1 2
2
aab
aba
""") == """YES
NO""", "duplicate mapping check"

assert run("""1
4
1 2 1 2
2
abab
aabb
""") == """YES
NO""", "two-to-two mapping"

assert run("""1
1
100
1
x
""") == "YES", "single element mapping"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| [1,1,2], ["aab","aba"] | YES, NO | Ensures duplicate numbers map consistently |
| [1,2,1,2], ["abab","aabb"] | YES, NO | Checks alternating pattern mapping |
| [100], ["x"] | YES | Handles single-element arrays correctly |

## Edge Cases

For arrays with a single element, any single-character string matches, producing `"YES"`. For arrays with length 1 but strings longer than 1, the output is `"NO"`. For strings where a character is mapped to multiple numbers, the code detects inconsistency immediately and outputs `"NO"`. Negative numbers and large numbers are treated the same as any integers because Python dictionaries handle arbitrary keys efficiently. The solution correctly handles all such edge cases.
