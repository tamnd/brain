---
title: "CF 1634A - Reverse and Concatenate"
description: "We are given a string s of length n and a number k. We can perform exactly k operations on s, where each operation is either appending the reverse of the string to itself (s + rev(s)) or prepending the reverse (rev(s) + s)."
date: "2026-06-10T04:44:16+07:00"
tags: ["codeforces", "competitive-programming", "greedy", "strings"]
categories: ["algorithms"]
codeforces_contest: 1634
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 770 (Div. 2)"
rating: 800
weight: 1634
solve_time_s: 85
verified: false
draft: false
---

[CF 1634A - Reverse and Concatenate](https://codeforces.com/problemset/problem/1634/A)

**Rating:** 800  
**Tags:** greedy, strings  
**Solve time:** 1m 25s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a string `s` of length `n` and a number `k`. We can perform exactly `k` operations on `s`, where each operation is either appending the reverse of the string to itself (`s + rev(s)`) or prepending the reverse (`rev(s) + s`). The task is to count how many distinct strings can result after performing all `k` operations. The output for each test case is a single integer representing this count.

The constraints are small: `n` is up to 100, `k` is up to 1000, and there are at most 100 test cases. This rules out simulating all `2^k` sequences of operations explicitly, because even for `k = 1000`, the number of possible sequences is astronomical. We need an approach that reasons about the structure of the strings rather than constructing each string.

A subtle case occurs when the original string is a palindrome. For example, if `s = "aba"`, then `rev(s) = "aba"` as well. After any number of operations, prepending or appending `rev(s)` produces the same string. This collapses multiple operation sequences into a single string. Another edge case is when `k = 0`, in which case we simply return 1 because no operations change the string.

## Approaches

The brute-force approach would simulate every operation sequence: for each operation, either prepend or append the reverse, and keep a set of all distinct results. This works for small `k`, but for `k = 1000` it would require storing and generating strings of length up to `n * 2^k`, which is completely infeasible.

The key observation is that the number of distinct strings after `k` operations depends only on whether the original string is a palindrome. If the string is a palindrome, prepending or appending its reverse produces the same result, so no new distinct strings appear. If the string is not a palindrome, the first operation produces two distinct results, and each subsequent operation will continue doubling in principle. However, because of symmetry, all subsequent operations produce only two unique strings: one starting with the original string and one starting with the reversed string. Therefore, for non-palindromes with `k > 0`, the answer is always 2. For `k = 0`, the answer is 1.

This insight reduces the problem to a simple check for palindromes and the value of `k`. The brute-force approach fails because it attempts to construct strings of exponential length, while the optimal approach leverages the symmetry in reversals.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(2^k * n * k) | O(2^k * n * k) | Too slow |
| Optimal | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the number of test cases.
2. For each test case, read `n`, `k`, and the string `s`.
3. If `k = 0`, immediately return 1 because no operations are performed.
4. Check if `s` is a palindrome by comparing it to its reverse.
5. If `s` is a palindrome, return 1 because every sequence of operations produces the same string.
6. If `s` is not a palindrome, return 2 because the first operation generates two distinct strings and every subsequent operation preserves these two distinct forms.
7. Print the result for each test case.

Why it works: The invariant is that once the first operation is applied to a non-palindrome, it produces exactly two distinct strings: one that starts with the original string and one that starts with the reversed string. Subsequent operations cannot create new distinct strings because prepending or appending reversals only swaps between these two forms. Palindromes remain invariant under reversal, so only a single string ever exists.

## Python Solution

```python
import sys
input = sys.stdin.readline

def main():
    t = int(input())
    for _ in range(t):
        n, k = map(int, input().split())
        s = input().strip()
        if k == 0:
            print(1)
        elif s == s[::-1]:
            print(1)
        else:
            print(2)

if __name__ == "__main__":
    main()
```

The solution begins by reading the number of test cases. Each test case reads the length, the number of operations, and the string. The special case `k = 0` is handled first. The palindrome check uses Python slicing, which is O(n), sufficient for `n <= 100`. The logic for non-palindromes directly outputs 2, based on the first operation producing two distinct strings.

## Worked Examples

Sample 1: `s = "aab"`, `k = 2`.

| Operation | String(s) |
| --- | --- |
| Initial | aab |
| First | aabbaa, baaaab |
| Second | aabbaaaabbaa, baaaabbaaaab |

After 2 operations, two distinct strings exist. Our algorithm outputs 2, which matches the trace.

Sample 2: `s = "abacaba"`, `k = 1`.

| Operation | String(s) |
| --- | --- |
| Initial | abacaba |
| First | abacabaabacaba |

Since `s` is a palindrome, the first operation yields only one string. Algorithm outputs 1.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n * t) | Each string of length n is checked once for palindrome, repeated for t test cases |
| Space | O(1) | No extra data structures beyond input reading and temporary variables |

This is well within the constraints, as `n * t <= 100 * 100 = 10^4`.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    output = io.StringIO()
    sys.stdout = output
    main()
    return output.getvalue().strip()

# Provided samples
assert run("4\n3 2\naab\n3 3\naab\n7 1\nabacaba\n2 0\nab") == "2\n2\n1\n1", "Sample tests"

# Custom tests
assert run("1\n1 5\na") == "1", "single character palindrome"
assert run("1\n2 0\nab") == "1", "k=0 case"
assert run("1\n3 1\nabc") == "2", "non-palindrome short string"
assert run("1\n5 100\nabcba") == "1", "palindrome with large k"
assert run("1\n4 10\nabca") == "2", "non-palindrome with large k"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| "1\n1 5\na" | 1 | Single character palindrome |
| "1\n2 0\nab" | 1 | k = 0 produces one string |
| "1\n3 1\nabc" | 2 | Non-palindrome short string first operation |
| "1\n5 100\nabcba" | 1 | Palindrome with large k remains one string |
| "1\n4 10\nabca" | 2 | Non-palindrome with many operations |

## Edge Cases

When `k = 0`, the algorithm correctly outputs 1. For `s = "aba"`, a palindrome, and `k > 0`, the algorithm outputs 1, because every sequence of operations produces the same string `aba...aba`. For `s = "abc"`, a non-palindrome, and `k = 1`, the output is 2 because the two possible strings after one operation are `"abccba"` and `"cbaabc"`. All these scenarios are correctly handled by the palindrome check and the `k == 0` condition.
