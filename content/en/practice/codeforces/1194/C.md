---
title: "CF 1194C - From S To T"
description: "We are given three strings s, t, and p. We can repeatedly take any character from p and insert it anywhere in s. The goal is to determine if, after some sequence of such insertions, s can become exactly equal to t."
date: "2026-06-12T00:17:09+07:00"
tags: ["codeforces", "competitive-programming", "implementation", "strings"]
categories: ["algorithms"]
codeforces_contest: 1194
codeforces_index: "C"
codeforces_contest_name: "Educational Codeforces Round 68 (Rated for Div. 2)"
rating: 1300
weight: 1194
solve_time_s: 101
verified: true
draft: false
---

[CF 1194C - From S To T](https://codeforces.com/problemset/problem/1194/C)

**Rating:** 1300  
**Tags:** implementation, strings  
**Solve time:** 1m 41s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given three strings `s`, `t`, and `p`. We can repeatedly take any character from `p` and insert it anywhere in `s`. The goal is to determine if, after some sequence of such insertions, `s` can become exactly equal to `t`. Each query is independent, and we must answer `YES` or `NO` for each one.

The first observation is that the order of the existing characters in `s` matters. If `s` contains characters in an order that does not match a subsequence of `t`, no amount of inserting extra characters from `p` can fix the relative positions. Therefore, `s` must already be a subsequence of `t`. Second, for every character that is in `t` but not in `s`, there must be enough of that character in `p` to fill the gap.

The string lengths are small: up to 100 characters each, and there are at most 100 queries. This allows for simple linear scans per query, because even a naive O(|t| + |p|) check per query is at most around 10,000 operations, which is well within 1 second.

A subtle edge case occurs when `s` is already longer than `t`, or when `s` has characters in the wrong order. For example, `s = "ba"`, `t = "ab"`, `p = "a"`. `s` is not a subsequence of `t`, so the answer must be `NO`, even though `p` has characters that exist in `t`. A careless approach might only check character counts and mistakenly report `YES`.

## Approaches

A brute-force approach would try every possible way to insert characters from `p` into `s` to match `t`. We could generate all permutations of insertions, but even for length 100, this is completely infeasible because the number of possibilities grows factorially with the number of insertions.

The key insight is to separate the problem into two simpler checks. First, verify that `s` is a subsequence of `t`. This guarantees that the relative order of characters already in `s` is correct. Second, count the number of each character needed in `t` that is not present in `s`. If `p` contains at least that many of each needed character, the answer is `YES`; otherwise, it is `NO`. This approach works because the insertion operations are flexible in position, so order does not constrain characters from `p`.

The brute-force approach is correct in theory but impractical, while the two-step check uses the problem's structure to reduce it to a linear-time solution.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(factorial( | t | )) |
| Subsequence + Count Check | O( | t | + |

## Algorithm Walkthrough

1. Start by checking if `s` is a subsequence of `t`. Initialize two pointers, `i` for `s` and `j` for `t`. Scan through `t`, advancing `i` whenever `t[j] == s[i]`. At the end, if `i` equals the length of `s`, then `s` is a subsequence of `t`.
2. If `s` is not a subsequence of `t`, immediately return `NO`. This is because the relative order of characters in `s` cannot be altered by inserting characters from `p`.
3. Count the frequency of each character in `s`, `t`, and `p`. For each character in `t`, compute how many additional occurrences are needed beyond what `s` already provides. This is simply `needed = count_t[char] - count_s.get(char, 0)`.
4. Check if `p` has enough of each required character. If for any character the count in `p` is less than `needed`, return `NO`. Otherwise, return `YES`.

Why it works: The first step guarantees that `s` aligns correctly with `t`. The counting step guarantees that the extra characters required to fill `s` into `t` are available in `p`. Since insertion is allowed anywhere, no additional constraints exist, so these two checks are both necessary and sufficient.

## Python Solution

```python
import sys
input = sys.stdin.readline

from collections import Counter

def can_transform(s, t, p):
    # Check if s is a subsequence of t
    i = 0
    for ch in t:
        if i < len(s) and s[i] == ch:
            i += 1
    if i != len(s):
        return "NO"
    
    # Count characters
    count_s = Counter(s)
    count_t = Counter(t)
    count_p = Counter(p)
    
    # Check if p can supply the missing characters
    for ch in count_t:
        if count_t[ch] > count_s.get(ch, 0) + count_p.get(ch, 0):
            return "NO"
    
    return "YES"

def main():
    q = int(input())
    for _ in range(q):
        s = input().strip()
        t = input().strip()
        p = input().strip()
        print(can_transform(s, t, p))

if __name__ == "__main__":
    main()
```

The function `can_transform` first checks the subsequence property using a pointer scan. This avoids complicated logic with string insertions. Next, `Counter` is used for character counts, which simplifies checking if `p` can provide the needed letters. The order of operations is important: the subsequence check must happen before counting, because if `s` is not a subsequence of `t`, the counts alone are insufficient.

## Worked Examples

Using the first sample input:

| s | t | p | i pointer | decision |
| --- | --- | --- | --- | --- |
| ab | acxb | cax | 0→1→2 | s is subsequence of t, counts check passes → YES |
| a | aaaa | aaabbcc | 0→1 | subsequence passes, t needs 3 extra a's, p has enough → YES |
| aaaa | aabbcc | aabbcc | 0→1→2→3 | subsequence passes, t needs 2 b's and 2 c's, p has only 2 b's, 2 c's → YES or NO? |

Second trace confirms subsequence check works, counts check ensures all letters needed are available in p.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O( | s |
| Space | O(26) = O(1) | Counter dictionaries store at most 26 lowercase letters |

Since |s|, |t|, |p| ≤ 100 and q ≤ 100, worst-case operations are around 30,000, which is acceptable.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    output = io.StringIO()
    sys.stdout = output
    main()
    sys.stdout = sys.__stdout__
    return output.getvalue().strip()

# Provided samples
assert run("4\nab\nacxb\ncax\na\naaaa\naaabbcc\naaaa\naabbcc\nab\nbaaa\naaaaa\n") == "YES\nYES\nNO\nNO", "sample 1"

# Custom cases
assert run("1\na\nb\na\n") == "NO", "s not subsequence of t"
assert run("1\na\nab\nb\n") == "YES", "s can be extended by p"
assert run("1\nabc\nabc\n\n") == "YES", "s equals t, p empty"
assert run("1\nabc\nacb\nabc\n") == "NO", "s subsequence fails due to order"
assert run("1\na"*100 + "\n" + "a"*100 + "\n" + "" + "\n") == "YES", "maximum-length equal strings"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| a / b / a | NO | s not a subsequence of t |
| a / ab / b | YES | s can be extended by p to match t |
| abc / abc / empty | YES | s equals t, p empty |
| abc / acb / abc | NO | order mismatch prevents subsequence |
| 100×a / 100×a / empty | YES | maximum-length strings handled |

## Edge Cases

For `s = "ba"`, `t = "ab"`, `p =
