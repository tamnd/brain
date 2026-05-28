---
title: "CF 58A - Chat room"
description: "The problem asks whether Vasya, who typed a string of lowercase letters, effectively managed to say \"hello\". The goal is not to check if the typed string is exactly \"hello\", but whether we can remove some letters (possibly zero) to produce the sequence h, e, l, l, o in order."
date: "2026-05-28T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "greedy", "strings"]
categories: ["algorithms"]
codeforces_contest: 58
codeforces_index: "A"
codeforces_contest_name: "Codeforces Beta Round 54 (Div. 2)"
rating: 1000
weight: 58
solve_time_s: 80
verified: true
draft: false
---

[CF 58A - Chat room](https://codeforces.com/problemset/problem/58/A)

**Rating:** 1000  
**Tags:** greedy, strings  
**Solve time:** 1m 20s  
**Verified:** yes  

## Solution
## Problem Understanding

The problem asks whether Vasya, who typed a string of lowercase letters, effectively managed to say "hello". The goal is not to check if the typed string is exactly "hello", but whether we can remove some letters (possibly zero) to produce the sequence `h`, `e`, `l`, `l`, `o` in order.

The input is a single string of length between 1 and 100. The output is either "YES" if it is possible to extract the word "hello" from it or "NO" otherwise.

The constraints are very relaxed. With `n ≤ 100` and a time limit of 1 second, even a naive solution that looks at all subsequences could theoretically work, but the problem's essence is really about scanning the string for the target sequence. Edge cases that can trick a naive approach include strings where letters are present but out of order, such as `hlelo`, which contains all the letters of "hello" but does not preserve their order. Another edge case is minimal input, e.g., `h`, which should clearly output "NO".

## Approaches

The brute-force approach would try every possible subsequence of the input string to see if it matches "hello". For a string of length `n`, there are `2^n` subsequences, which is infeasible even for `n = 100`, producing roughly `10^30` checks. Clearly, this approach is correct in principle but not practical.

The key insight is that we do not need to consider all subsequences explicitly. We only care about whether we can match each character of "hello" in order as we scan the string. This suggests a greedy scan: keep an index `j` for the target word "hello". Traverse the input string `s` from left to right. Each time a character matches `hello[j]`, increment `j`. If `j` reaches the length of "hello" (5), we have successfully found the word. This is linear in the length of the string and directly encodes the problem's sequential requirement.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(2^n) | O(1) | Too slow |
| Greedy Scan | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

1. Initialize `target = "hello"` and an index `j = 0` to track which character of "hello" we are currently looking for.
2. Iterate through each character `c` in the input string `s`.
3. If `c` equals `target[j]`, increment `j`. This moves us to the next character we need to match. We skip all other characters automatically because they cannot disrupt the order.
4. After scanning the string, check if `j` equals 5. If it does, print "YES", otherwise print "NO".

Why it works: The greedy approach relies on the invariant that `j` always points to the next character of "hello" that needs to be matched. Every time a character matches, it advances the index. Any characters in between are ignored because they do not prevent forming the subsequence. This guarantees that if `j` reaches 5, all letters have been matched in the correct order.

## Python Solution

```python
import sys
input = sys.stdin.readline

s = input().strip()
target = "hello"
j = 0

for c in s:
    if c == target[j]:
        j += 1
        if j == len(target):
            break

print("YES" if j == len(target) else "NO")
```

The code reads the input and strips any trailing newline. We maintain a pointer `j` to track our progress through "hello". As we iterate over `s`, we increment `j` whenever we match the current target character. If we reach the end of `target`, we stop early for efficiency. Finally, we print "YES" if all letters were matched, otherwise "NO".

## Worked Examples

### Example 1

Input: `ahhellllloou`

| s[i] | c | target[j] | j |
| --- | --- | --- | --- |
| 0 | a | h | 0 |
| 1 | h | h | 1 |
| 2 | h | e | 1 |
| 3 | e | e | 2 |
| 4 | l | l | 3 |
| 5 | l | l | 4 |
| 6 | l | o | 4 |
| 7 | l | o | 4 |
| 8 | l | o | 4 |
| 9 | o | o | 5 |

All target letters are matched in order. Output: `YES`.

### Example 2

Input: `hlelo`

| s[i] | c | target[j] | j |
| --- | --- | --- | --- |
| 0 | h | h | 1 |
| 1 | l | e | 1 |
| 2 | e | e | 2 |
| 3 | l | l | 3 |
| 4 | o | l | 3 |

`j` never reaches 5. Output: `NO`.

These traces confirm that the algorithm correctly tracks sequential matches and rejects out-of-order letters.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | We scan each character once, performing at most one comparison and pointer increment per character |
| Space | O(1) | Only a few variables are used regardless of input length |

With `n ≤ 100`, this is comfortably within time and memory limits. Even if `n` were larger, this linear scan scales well.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    s = input().strip()
    target = "hello"
    j = 0
    for c in s:
        if c == target[j]:
            j += 1
            if j == len(target):
                break
    return "YES" if j == len(target) else "NO"

# Provided sample
assert run("ahhellllloou") == "YES", "sample 1"

# Custom cases
assert run("hlelo") == "NO", "letters out of order"
assert run("h") == "NO", "single letter"
assert run("helicopterlo") == "YES", "interleaved extra letters"
assert run("aaaaa") == "NO", "no relevant letters"
assert run("hhheeellllooo") == "YES", "duplicates before matches"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| hlelo | NO | sequence order enforcement |
| h | NO | minimum input handling |
| helicopterlo | YES | skips irrelevant letters |
| aaaaa | NO | absence of target letters |
| hhheeellllooo | YES | multiple consecutive matches handled |

## Edge Cases

For `s = "h"`, the algorithm iterates once, sees `h` matches `target[0]`, increments `j = 1`. There are no further characters, `j < 5`, so output is `NO`. For `s = "hhheeellllooo"`, the algorithm increments `j` only when the next required letter matches, skipping duplicates. After all characters, `j = 5`, correctly outputting `YES`. These confirm the greedy scan handles both insufficient and repetitive input correctly.
