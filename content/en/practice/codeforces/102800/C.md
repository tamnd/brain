---
title: "CF 102800C - String Game"
description: "The game revolves around two strings. Clair has a longer string, and Bob chooses another string as the target word."
date: "2026-07-28T22:51:31+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102800
codeforces_index: "C"
codeforces_contest_name: "The 14th Jilin Provincial Collegiate Programming Contest"
rating: 0
weight: 102800
solve_time_s: 55
verified: true
draft: false
---

[CF 102800C - String Game](https://codeforces.com/problemset/problem/102800/C)

**Rating:** -  
**Tags:** -  
**Solve time:** 55s  
**Verified:** yes  

## Solution
## Problem Understanding

The game revolves around two strings. Clair has a longer string, and Bob chooses another string as the target word. Bob’s chosen string may contain mistakes, so the task is to check how many different ways it can still be formed by deleting some characters from Clair’s string while keeping the remaining characters in order.

A way of forming the target string is a subsequence match. For example, from `eeettt`, the string `et` can be formed by choosing any one of the three `e` characters and any one of the three `t` characters after it, giving nine possible matches. The required output is the total number of such choices modulo (10^9+7).

The first string can have length up to 5000, while the target string can have length up to 1000. A quadratic solution is usually around 25 million operations for the largest input, which is comfortable in Python. A solution that tries every possible subset of positions would require checking up to (2^{5000}) choices, which is impossible. The constraints suggest that the positions of the target string must be processed with dynamic programming rather than explicit enumeration.

Several details can break a naive implementation. If the target string is longer than the original string, no subsequence can exist. For input:

```
abc
abcd
```

the correct answer is `0`. A method that only counts matching characters without considering order and length could incorrectly produce a positive value.

Repeated characters create another common mistake. For:

```
ee
e
```

the answer is `2`, because either `e` in the first string can be selected. Counting only distinct resulting strings would incorrectly return `1`.

The order of characters also matters. For:

```
abc
ba
```

the answer is `0`, because although both characters appear, the `b` comes after the `a` in the source string and cannot be chosen before it. A method based only on character frequencies would fail here.

## Approaches

The direct approach is to choose positions in Clair’s string for every character in Bob’s string. For each possible selection of positions, we verify whether the chosen characters match the target string in order. This is correct because every valid subsequence corresponds to exactly one set of chosen positions.

The problem is the number of choices. If Clair’s string has length 5000, the number of possible subsequences is (2^{5000}). Even generating a tiny fraction of them is far beyond the time limit, so the brute-force idea cannot be used.

The useful observation is that every partial match has the same structure. While scanning Clair’s string from left to right, we only need to know how many ways each prefix of Bob’s string has already been formed. The future only depends on these counts, not on the exact positions used before.

Suppose we have processed some prefix of Clair’s string. Let `dp[j]` represent the number of ways to create the first `j` characters of Bob’s string from the processed prefix. When a new character from Clair is read, it can extend every already-existing match whose next required character is the same. It can also start a match for the first character of Bob’s string.

This turns the exponential search into a dynamic programming process. Each character from Clair updates all possible prefix lengths of Bob’s string once.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(2^n) | O(n) | Too slow |
| Optimal | O(nm) | O(m) | Accepted |

Here, `n` is the length of Clair’s string and `m` is the length of Bob’s string.

## Algorithm Walkthrough

1. Create a dynamic programming array where `dp[j]` stores the number of ways to form the first `j` characters of Bob’s string using the part of Clair’s string processed so far. Initially, `dp[0] = 1` because there is exactly one way to form an empty string: choose nothing.
2. Scan Clair’s string character by character. For the current character, examine Bob’s string positions from the end toward the beginning.
3. If the current character of Clair matches the `j`-th character of Bob, add `dp[j-1]` into `dp[j]`. This represents taking the current character as the final character of a newly formed subsequence. The reverse direction is necessary because the current character can only be used once in the current update.
4. After all characters from Clair have been processed, `dp[m]` contains the number of complete ways to form Bob’s entire string. Output this value modulo (10^9+7).

Why it works: the invariant is that after processing any prefix of Clair’s string, `dp[j]` is exactly the number of ways to form the first `j` characters of Bob’s string from that prefix. When a new character is considered, every existing subsequence either ignores it or uses it as the next matching character. The backward update counts the second case while preserving the first case in the existing values. Since every valid subsequence has a unique last chosen character, every possibility is counted exactly once.

## Python Solution

```python
import sys
input = sys.stdin.readline

MOD = 10 ** 9 + 7

def solve():
    s = input().strip()
    t = input().strip()

    m = len(t)
    dp = [0] * (m + 1)
    dp[0] = 1

    for ch in s:
        for j in range(m, 0, -1):
            if ch == t[j - 1]:
                dp[j] += dp[j - 1]
                if dp[j] >= MOD:
                    dp[j] -= MOD

    print(dp[m])

if __name__ == "__main__":
    solve()
```

The array `dp` represents all prefix lengths of Bob’s string. Its size is only the length of the target string, because the processed part of Clair’s string does not need to be stored.

The outer loop processes Clair’s string in the same order as subsequences are built. The inner loop goes backwards through Bob’s string so that one occurrence of a character from Clair contributes only once during this step. If the loop went forward, an updated value could immediately be reused and the same character could incorrectly fill multiple positions in Bob’s string.

The modulo operation is applied after every addition because the number of subsequences grows very quickly. Python integers do not overflow, but keeping values reduced avoids unnecessary growth and matches the required output.

## Worked Examples

For the first sample:

```
eeettt
et
```

the target has length two, so `dp[1]` counts ways to make `e` and `dp[2]` counts ways to make `et`.

| Current character | dp after processing |
| --- | --- |
| start | `[1, 0, 0]` |
| e | `[1, 1, 0]` |
| e | `[1, 2, 0]` |
| e | `[1, 3, 0]` |
| t | `[1, 3, 3]` |
| t | `[1, 3, 6]` |
| t | `[1, 3, 9]` |

The final value is `9`. The trace shows that every `e` can pair with every later `t`.

For the second sample:

```
eeettt
te
```

the order of the target is reversed.

| Current character | dp after processing |
| --- | --- |
| start | `[1, 0, 0]` |
| e | `[1, 0, 0]` |
| e | `[1, 0, 0]` |
| e | `[1, 0, 0]` |
| t | `[1, 1, 0]` |
| t | `[1, 2, 0]` |
| t | `[1, 3, 0]` |

The answer stays zero because no `e` appears after a selected `t`. The dynamic programming state naturally enforces ordering.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(nm) | Each character of Clair’s string updates every possible prefix length of Bob’s string once. |
| Space | O(m) | Only the counts for Bob’s prefixes are stored. |

With `n = 5000` and `m = 1000`, the algorithm performs about five million state updates, which fits comfortably within the limits.

## Test Cases

```python
import sys
import io

MOD = 10 ** 9 + 7

def solve():
    s = input().strip()
    t = input().strip()

    dp = [0] * (len(t) + 1)
    dp[0] = 1

    for ch in s:
        for j in range(len(t), 0, -1):
            if ch == t[j - 1]:
                dp[j] = (dp[j] + dp[j - 1]) % MOD

    print(dp[-1])

def run(inp: str) -> str:
    old_stdin = sys.stdin
    old_stdout = sys.stdout
    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    solve()

    result = sys.stdout.getvalue()
    sys.stdin = old_stdin
    sys.stdout = old_stdout
    return result

assert run("eeettt\net\n") == "9\n", "sample 1"
assert run("eeettt\nte\n") == "0\n", "sample 2"

assert run("a\na\n") == "1\n", "single matching character"
assert run("abc\nabcd\n") == "0\n", "target longer than source"
assert run("aaaa\naa\n") == "6\n", "all equal characters"
assert run("abab\nab\n") == "4\n", "multiple ordered matches"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `a` and `a` | `1` | Minimum valid subsequence |
| `abc` and `abcd` | `0` | Target longer than source |
| `aaaa` and `aa` | `6` | Combinations with repeated characters |
| `abab` and `ab` | `4` | Multiple valid ordered selections |

## Edge Cases

For the case where the target is longer than the source:

```
abc
abcd
```

the algorithm creates a dynamic programming array of length five. During the scan, only the first three target positions can receive contributions, because the fourth target character never has a matching source character. The final value remains `0`, which is correct.

For repeated characters:

```
ee
e
```

the initial state is `[1, 0]`. The first `e` changes it to `[1, 1]`, and the second `e` changes it to `[1, 2]`. The final answer is `2`, counting both possible choices of position.

For ordering:

```
abc
ba
```

the first character `a` does not help because the first required target character is `b`. After processing `b`, there is one way to form `b`, but when `a` is processed it cannot extend that match because the target requires `a` after `b`. The final answer is `0`.

The algorithm handles these cases because the state stores prefixes of the target string, not just character counts. A character contributes only when it appears in the correct position relative to the already matched prefix.

I can also adapt this editorial into a shorter Codeforces-style version if you want a more contest-submission format.
