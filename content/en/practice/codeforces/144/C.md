---
title: "CF 144C - Anagram Search"
description: "We are asked to count the number of substrings of a string s that can be transformed into an anagram of a given string p. The string s can contain question marks ?, which can be replaced by any lowercase letter."
date: "2026-05-29T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "implementation", "strings"]
categories: ["algorithms"]
codeforces_contest: 144
codeforces_index: "C"
codeforces_contest_name: "Codeforces Round 103 (Div. 2)"
rating: 1500
weight: 144
solve_time_s: 83
verified: true
draft: false
---

[CF 144C - Anagram Search](https://codeforces.com/problemset/problem/144/C)

**Rating:** 1500  
**Tags:** implementation, strings  
**Solve time:** 1m 23s  
**Verified:** yes  

## Solution
## Problem Understanding

We are asked to count the number of substrings of a string `s` that can be transformed into an anagram of a given string `p`. The string `s` can contain question marks `?`, which can be replaced by any lowercase letter. A substring is defined as a contiguous segment of `s`, and two substrings starting at different positions are considered distinct even if they are identical.

The input size allows `s` and `p` to each be up to 100,000 characters long. A naive approach that generates all substrings and checks them individually would require roughly `O(n^2 * m)` operations where `n` is the length of `s` and `m` is the length of `p`. With `n` and `m` up to 10^5, this results in about 10^15 operations, which is far too slow for a 2-second time limit. We need an `O(n)` or `O(n * 26)` approach to remain efficient.

Non-obvious edge cases include situations where the substring length of `s` is less than `p`, which should immediately produce zero valid substrings. Another subtle case arises when a substring contains only question marks - it can match any anagram of `p` as long as the length matches. For instance, if `s = "???"` and `p = "abc"`, the substring is valid because the three question marks can be replaced with 'a', 'b', 'c' in some order. A careless solution might miscount or miss such cases.

## Approaches

A brute-force approach iterates over all substrings of `s` of length equal to `p` and checks if they can form an anagram by counting letters and question marks. For each substring, one would compute a frequency array of letters and see if the difference between `p`’s letter counts and the substring’s counts can be covered exactly by the question marks. This works logically but runs in `O(n*m)` time. For the largest inputs, that is about 10^10 operations - far too slow.

The key observation is that checking substrings of fixed length lends itself to a sliding window. By maintaining a frequency count for a window of length `m` (length of `p`), we can efficiently update the counts when the window moves one position to the right. We also maintain the number of question marks in the window. For each shift, we only need to check whether the deficit of letters in the window relative to `p` is exactly equal to the number of question marks. This reduces the per-window check to `O(26)` operations, making the full algorithm `O(n*26)`, which is fast enough.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n*m) | O(26) | Too slow |
| Sliding Window | O(n*26) | O(26) | Accepted |

## Algorithm Walkthrough

1. Compute the frequency array `freq_p` for string `p`, where `freq_p[i]` counts occurrences of letter `'a'+i`.
2. Initialize a sliding window of length `m` over `s`. Compute `freq_window` as the letter counts of the first window and count the number of question marks `q_count`.
3. For each window, compute the total number of missing letters compared to `p` by summing `max(0, freq_p[i] - freq_window[i])` across all letters. If this sum equals `q_count`, the window is good.
4. Slide the window one position to the right. Update `freq_window` and `q_count` by decrementing the count of the character that left the window and incrementing the count of the character that entered the window.
5. Repeat step 3 and 4 until the end of the string is reached.

The reason this works is that each letter deficit must be exactly covered by question marks for a substring to be transformable into an anagram of `p`. Sliding the window ensures we examine every possible substring efficiently without recomputing counts from scratch.

## Python Solution

```python
import sys
input = sys.stdin.readline

s = input().strip()
p = input().strip()

len_s = len(s)
len_p = len(p)

if len_p > len_s:
    print(0)
    sys.exit()

# frequency of letters in p
freq_p = [0] * 26
for ch in p:
    freq_p[ord(ch) - ord('a')] += 1

# frequency of letters in the current window
freq_window = [0] * 26
q_count = 0
for i in range(len_p):
    if s[i] == '?':
        q_count += 1
    else:
        freq_window[ord(s[i]) - ord('a')] += 1

result = 0

def is_good():
    missing = 0
    for i in range(26):
        if freq_p[i] > freq_window[i]:
            missing += freq_p[i] - freq_window[i]
    return missing == q_count

if is_good():
    result += 1

for i in range(len_p, len_s):
    # remove leftmost character
    left = s[i - len_p]
    if left == '?':
        q_count -= 1
    else:
        freq_window[ord(left) - ord('a')] -= 1
    # add new character
    right = s[i]
    if right == '?':
        q_count += 1
    else:
        freq_window[ord(right) - ord('a')] += 1
    if is_good():
        result += 1

print(result)
```

The solution initializes letter counts for both `p` and the first window of `s`. Each shift of the window updates only the characters entering and leaving, keeping the per-window check to constant time (26 letters). Using `max(0, freq_p[i]-freq_window[i])` avoids negative deficits, correctly handling letters that appear more in the window than needed. The `?` count is adjusted incrementally, preventing recomputation.

## Worked Examples

Sample Input 1:

```
s = "bb??x???"
p = "aab"
```

| Window | freq_window | q_count | missing letters | Good? |
| --- | --- | --- | --- | --- |
| "bb?" | b=2 | 1 | missing a=2 → missing=2 | 2 == 1? No |
| "b??" | b=1 | 2 | missing a=2 → missing=2 | 2 == 2? Yes |
| "???" | 0 | 3 | missing a=2, b=1 → missing=3 | 3 == 3? Yes |
| "?x?" | x=1 | 2 | missing a=2, b=1 → missing=3 | 3 != 2? No |
| "x??" | x=1 | 2 | missing a=2, b=1 → missing=3 | 3 != 2? No |
| "???" | 0 | 3 | missing a=2, b=1 → missing=3 | 3 == 3? Yes |

Two substrings counted.

Sample Input 2:

```
s = "ab?c"
p = "abc"
```

| Window | freq_window | q_count | missing | Good? |
| --- | --- | --- | --- | --- |
| "ab?" | a=1, b=1 | 1 | c=1 → missing=1 | 1==1 Yes |
| "b?c" | b=1, c=1 | 1 | a=1 → missing=1 | 1==1 Yes |

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n*26) | Each of the n windows performs a 26-letter deficit check. Sliding window updates are O(1). |
| Space | O(26*2) = O(1) | Two frequency arrays of size 26 and a few counters. |

The solution fits well within the 2-second limit for n up to 100,000.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    s = input().strip()
    p = input().strip()
    len_s = len(s)
    len_p = len(p)
    if len_p > len_s:
        return "0"
    freq_p = [0]*26
    for ch in p:
        freq_p[ord(ch)-ord('a')] += 1
    freq_window = [0]*26
    q_count = 0
    for i in range(len_p):
        if s[i]=='?':
            q_count += 1
        else:
            freq_window[ord(s[i])-ord('a')] +=1
    result=0
    def is_good():
        missing=0
        for i in range(26):
            if freq_p[i]>freq_window[i]:
                missing += freq_p[i]-freq_window[i]
        return missing==q_count
    if is_good():
        result +=1
    for i in range(len_p,len_s):
        left = s[i-len_p]
        if left=='?':
            q_count -=1
        else:
            freq_window[ord(left)-ord('a')]-=1
        right = s[i]
        if
```
