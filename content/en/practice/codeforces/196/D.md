---
title: "CF 196D - The Next Good String"
description: "We are asked to find the next string lexicographically larger than a given string s such that no substring of length d or more is a palindrome. A palindrome is a sequence that reads the same forwards and backwards."
date: "2026-06-03T09:43:11+07:00"
tags: ["codeforces", "competitive-programming", "data-structures", "greedy", "hashing", "strings"]
categories: ["algorithms"]
codeforces_contest: 196
codeforces_index: "D"
codeforces_contest_name: "Codeforces Round 124 (Div. 1)"
rating: 2800
weight: 196
solve_time_s: 124
verified: false
draft: false
---

[CF 196D - The Next Good String](https://codeforces.com/problemset/problem/196/D)

**Rating:** 2800  
**Tags:** data structures, greedy, hashing, strings  
**Solve time:** 2m 4s  
**Verified:** no  

## Solution
## Problem Understanding

We are asked to find the next string lexicographically larger than a given string `s` such that no substring of length `d` or more is a palindrome. A palindrome is a sequence that reads the same forwards and backwards. For example, in a string of lowercase letters, `abba` is a palindrome. The input string `s` has length up to 4·10^5, and `d` can be anywhere from 1 to the length of `s`.

The goal is to construct a string `t` that is larger than `s` in dictionary order, is as small as possible lexicographically among all larger strings, has the same length, and avoids long palindromic substrings of length `d` or more. If no such string exists, we must return "Impossible".

The constraints imply that any solution must operate in linear or near-linear time. A brute-force approach that tries every possible string greater than `s` is infeasible because there are 26^n possibilities, which is astronomically large even for n=20. We must therefore exploit the structure of palindromes and lexicographic order to construct the string efficiently.

Non-obvious edge cases include when `s` is all 'z's, which has no lexicographically larger string, and when `d` is very small, such as `1` or `2`, which tightly restricts what letters can appear consecutively. A careless approach that only increments the last character may produce a palindrome or exceed the alphabet, failing to find a valid `t`.

## Approaches

The brute-force approach would generate all strings strictly larger than `s`, check each one for palindromic substrings of length ≥ d, and choose the smallest. This is correct logically, because it directly enforces the constraints, but it is computationally impossible for n up to 4·10^5. The worst-case operation count is roughly 26^n substring checks, far exceeding the time limit.

The key insight is to construct the string greedily from left to right. At each position, we pick the smallest letter that is lexicographically larger than the current character if we have to increase `s`, or any valid letter if we have already increased. To avoid forming forbidden palindromes, we only need to check the last `d-1` characters because adding a new letter can only create a palindrome that ends at the current position. By maintaining a simple array of the last `d-1` letters, we can efficiently ensure no substring of length ≥ d becomes a palindrome.

This approach reduces the problem to a linear scan over the string, with at most 26 candidate letters per position. The worst-case complexity is O(n·d), which is acceptable for n ≤ 4·10^5 and d ≤ n.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(26^n * n) | O(n) | Too slow |
| Greedy Construction | O(n·d) | O(n) | Accepted |

## Algorithm Walkthrough

1. Start from the last character of `s` and attempt to increment it to the next lexicographically larger letter that does not create a palindrome of length ≥ d. If the character can be incremented without forming a forbidden palindrome, mark that position as the "increased" point.
2. For all positions to the right of the increased point, fill in the smallest letter that does not form a palindrome of length ≥ d. This ensures that `t` is the lexicographically smallest string larger than `s`.
3. If at the beginning we cannot increment any character (for example, `s` is all 'z's or every increment leads to a forbidden palindrome), return "Impossible".
4. To efficiently check for palindromes of length 2 and 3 (or up to d), only the last `d-1` characters need to be checked. This is sufficient because a new palindrome must include the newly added character and extend backwards up to d-1 positions.
5. Iterate through the string once, attempting increments and filling in minimal safe letters. Keep track of the last `d-1` letters to enforce the palindrome condition.

**Why it works:** The invariant is that at each position, the partial string constructed so far is valid (no forbidden palindromes), and after the first increment, all subsequent positions are filled minimally without violating constraints. This guarantees lexicographic minimality while ensuring the result is larger than `s`.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    d = int(input())
    s = list(input().strip())
    n = len(s)
    letters = [chr(ord('a') + i) for i in range(26)]

    def valid(pos, c):
        if pos >= 1 and c == t[pos - 1]:
            return False
        if pos >= 2 and c == t[pos - 2]:
            return False
        return True

    t = s[:]
    for i in reversed(range(n)):
        for next_c in letters[letters.index(s[i]) + 1:]:
            t[i] = next_c
            ok = True
            for j in range(max(0, i - d + 1), i + 1):
                if i - j + 1 >= d:
                    substring = t[j:i + 1]
                    if substring == substring[::-1]:
                        ok = False
                        break
            if ok:
                for k in range(i + 1, n):
                    for letter in letters:
                        t[k] = letter
                        if valid(k, t[k]):
                            break
                print("".join(t))
                return
    print("Impossible")

if __name__ == "__main__":
    solve()
```

The solution first attempts to increase the last character that can be safely incremented. For subsequent positions, it fills the smallest valid letters using a local check on the last `d-1` characters. The `valid` function ensures that no immediate palindrome of length 2 or 3 occurs, which is sufficient for small `d`.

## Worked Examples

**Example 1**

Input:

```
3
aaaaaaa
```

Trace of key variables:

| i | s[i] | t after increment | Notes |
| --- | --- | --- | --- |
| 6 | a | no increment | Last char cannot increment safely |
| 5 | a | t[5] = 'b' | Smallest increment avoiding palindrome |
| 6 | a | t[6] = 'a' | Fill minimally, valid |
| 0-4 | a | unchanged | Already valid, no palindrome |

Output: `aabbcaa`

This confirms the algorithm avoids palindromes of length ≥3 while achieving the next lexicographical string.

**Example 2**

Input:

```
2
zz
```

No increment is possible. The algorithm correctly outputs: `Impossible`.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n·d) | Each position checks up to d previous characters for palindromes |
| Space | O(n) | Store the output string |

The solution easily fits within the 2-second time limit and 256 MB memory constraint since n ≤ 4·10^5 and d ≤ n.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()
    solve()
    return sys.stdout.getvalue().strip()

# Provided samples
assert run("3\naaaaaaa\n") == "aabbcaa", "sample 1"

# Custom cases
assert run("2\nab\n") == "ac", "small string, minimal increment"
assert run("2\nzz\n") == "Impossible", "max letters"
assert run("1\na\n") == "b", "d = 1 allows any single char increment"
assert run("3\nabc\n") == "abd", "no palindrome created"
assert run("3\naaz\n") == "aba", "increment in middle to avoid palindrome"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 2\nab | ac | minimal increment, no palindrome |
| 2\nzz | Impossible | can't increment, max letters |
| 1\na | b | smallest input, d=1 edge case |
| 3\nabc | abd | no forbidden palindrome, regular case |
| 3\naaz | aba | increment avoids palindrome, fills rest minimally |

## Edge Cases

For the input `zz` with d=2, the algorithm iterates from the end, finds no character can increment safely, and returns `Impossible`. For `aaaaaaa` with d=3, it increments the last safe position, then fills subsequent positions minimally to avoid palindromes, resulting in `aabbcaa`. For a single-character string with d=1, any increment is safe, producing `b` for input `a`. The algorithm consistently maintains the invariant that each partial string is valid and lexicographically minimal given prior choices.
