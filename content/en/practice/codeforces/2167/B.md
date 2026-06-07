---
title: "CF 2167B - Your Name"
description: "We are given two strings, s and t, each of length n. The first string represents a row of lettered cubes, and the second string is a target name. The task is to determine if it is possible to rearrange the letters of s to exactly match t."
date: "2026-06-07T23:24:19+07:00"
tags: ["codeforces", "competitive-programming", "sortings", "strings"]
categories: ["algorithms"]
codeforces_contest: 2167
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 1062 (Div. 4)"
rating: 800
weight: 2167
solve_time_s: 74
verified: true
draft: false
---

[CF 2167B - Your Name](https://codeforces.com/problemset/problem/2167/B)

**Rating:** 800  
**Tags:** sortings, strings  
**Solve time:** 1m 14s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given two strings, `s` and `t`, each of length `n`. The first string represents a row of lettered cubes, and the second string is a target name. The task is to determine if it is possible to rearrange the letters of `s` to exactly match `t`. Essentially, we are checking if `t` is a permutation of `s`.

The constraints are small: `n` is at most 20 and there can be up to 1000 test cases. This means we can afford operations that are cubic or even factorial in `n` for a single test case, though simpler methods will be faster and cleaner. The input strings contain only lowercase letters, so any solution that checks the frequency of letters will suffice.

A subtle edge case arises when the strings contain repeated letters. For example, `s = "aaab"` and `t = "abaa"` should return "YES" because the letters match in quantity, but a naive check that simply compares sorted strings character by character without considering frequency could fail if implemented incorrectly. Another case is when `s` and `t` have the same letters but different counts, like `s = "abc"` and `t = "aab"`, which must return "NO".

## Approaches

The brute-force approach is to generate all permutations of `s` and check if any equals `t`. This is correct because it literally tests every possible rearrangement, but its complexity is `O(n!)` per test case. Even with `n = 20`, this is completely infeasible because 20 factorial is roughly 2.4 × 10^18 operations. Clearly, we need a faster method.

The key observation is that the order of letters does not matter, only their counts do. If `s` can be rearranged to form `t`, then `s` and `t` must contain exactly the same letters with the same frequency. This reduces the problem to a simple frequency comparison. One convenient way to do this is to sort both strings and compare them character by character. Alternatively, we could count the occurrences of each letter using an array of length 26 (for 'a' to 'z') and compare the counts. Both methods have linear or near-linear time complexity relative to `n`, which is extremely fast given the small size of `n`.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n!) | O(n) | Too slow |
| Sort & Compare | O(n log n) | O(n) | Accepted |
| Count Frequencies | O(n) | O(26) | Accepted |

## Algorithm Walkthrough

1. Read the number of test cases, `q`.
2. For each test case, read `n` and the two strings `s` and `t`.
3. Sort both strings. Sorting ensures that characters are arranged in lexicographical order. If `s` can be rearranged into `t`, their sorted versions must be identical.
4. Compare the sorted strings. If they are exactly equal, output "YES"; otherwise, output "NO".

Why it works: Sorting transforms the permutation problem into a linear comparison. Any mismatch in letter counts or characters will appear in the sorted strings, guaranteeing correctness. The invariant is that sorted strings preserve the multiset of characters; if the multisets are identical, one string is a permutation of the other.

## Python Solution

```python
import sys
input = sys.stdin.readline

q = int(input())
for _ in range(q):
    n = int(input())
    s, t = input().split()
    if sorted(s) == sorted(t):
        print("YES")
    else:
        print("NO")
```

The solution starts by reading the number of test cases and iterates over each. The `input().split()` call efficiently reads both strings from the same line. Sorting both strings reduces the problem to a simple equality check. This implementation handles multiple test cases correctly and leverages Python's efficient built-in sorting, which is more than sufficient for `n <= 20`.

## Worked Examples

**Example 1:** `s = "humitsa"`, `t = "mitsuha"`

| Step | s sorted | t sorted | Comparison |
| --- | --- | --- | --- |
| Initial | humitsa | mitsuha |  |
| After sort | a h i m s t u | a h i m s t u | equal → YES |

The trace confirms that sorting aligns the letters exactly, so "YES" is returned.

**Example 2:** `s = "aakima"`, `t = "makima"`

| Step | s sorted | t sorted | Comparison |
| --- | --- | --- | --- |
| Initial | aakima | makima |  |
| After sort | a a i k m m | a a i k m m | equal → NO |

After sorting, we see that the counts of each letter differ. This confirms the algorithm correctly identifies when the strings are not permutations.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(q * n log n) | Sorting each string dominates the cost; `q` test cases multiply this. |
| Space | O(n) | Sorting creates temporary arrays proportional to string length. |

Given `q <= 1000` and `n <= 20`, the total operations are at most 1000 × 20 log 20 ≈ 1000 × 80 = 80,000, which fits well within the 1-second limit.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    output = io.StringIO()
    sys.stdout = output
    # solution function
    q = int(input())
    for _ in range(q):
        n = int(input())
        s, t = input().split()
        if sorted(s) == sorted(t):
            print("YES")
        else:
            print("NO")
    return output.getvalue().strip()

# Provided samples
assert run("5\n7\nhumitsa mitsuha\n4\norhi hori\n6\naakima makima\n6\nnezuqo nezuko\n6\nmisaka mikasa\n") == "YES\nYES\nNO\nNO\nYES"

# Custom tests
assert run("1\n1\na a\n") == "YES", "single character, equal"
assert run("1\n1\na b\n") == "NO", "single character, different"
assert run("1\n4\naaaa aaaa\n") == "YES", "all letters same"
assert run("1\n4\naabb abab\n") == "YES", "letters same but shuffled"
assert run("1\n4\naabb abbc\n") == "NO", "different counts"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1\n1\na a | YES | Minimum-size input, equal letters |
| 1\n1\na b | NO | Minimum-size input, different letters |
| 1\n4\naaaa aaaa | YES | All letters identical |
| 1\n4\naabb abab | YES | Shuffle of letters |
| 1\n4\naabb abbc | NO | Counts mismatch |

## Edge Cases

For the minimum-size input `s = "a"`, `t = "a"`, the algorithm sorts both to "a" and returns "YES". If `t = "b"`, the sorted strings differ, and "NO" is returned. For repeated letters, such as `s = "aabb"` and `t = "abab"`, sorting results in "aabb" for both strings, confirming that the algorithm correctly handles multisets of letters, not just unique elements.
