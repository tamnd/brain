---
title: "CF 102307B - Boring Non-Palindrome"
description: "We have one non-empty string s. The only allowed operation is appending characters to its right end. The goal is to append as few characters as possible so that the entire resulting string becomes a palindrome."
date: "2026-08-13T07:12:54+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102307
codeforces_index: "B"
codeforces_contest_name: "2019 ICPC Universidad Nacional de Colombia Programming Contest"
rating: 0
weight: 102307
solve_time_s: 364
verified: true
draft: false
---

[CF 102307B - Boring Non-Palindrome](https://codeforces.com/problemset/problem/102307/B)

**Rating:** -  
**Tags:** -  
**Solve time:** 6m 4s  
**Verified:** yes  

## Solution
## Problem Understanding

We have one non-empty string `s`. The only allowed operation is appending characters to its right end. The goal is to append as few characters as possible so that the entire resulting string becomes a palindrome.

The key restriction is that we cannot modify or remove any character already present. Suppose some suffix of `s` is already a palindrome. If we keep that suffix as the central part of the final palindrome, everything before it can be mirrored by appending its reverse. For example, for `helloworld`, the longest palindromic suffix is just `d`. The prefix before it is `helloworl`, whose reverse is `lrowolleh`, so the answer becomes `helloworldlrowolleh`.

The input length is at most 5000. That is small enough that an `O(n^2)` algorithm is potentially practical, but it also makes a linear solution straightforward and removes the need to rely on the relatively generous constant factors of Python string operations. An `O(n^3)` approach would be clearly unsuitable because 5000 characters would already imply billions of operations. The target solution will use `O(n)` time and `O(n)` memory.

There are several boundary cases that can make an otherwise reasonable implementation wrong. For a one-character input such as `a`, the string is already a palindrome, so the correct output is `a`. An implementation that always appends at least one character would incorrectly produce a longer string.

For an already palindromic string such as `anitalavalatina`, nothing should be appended. The correct output is exactly `anitalavalatina`. An implementation that searches only for proper palindromic suffixes can accidentally append unnecessary characters.

A suffix does not have to be only one character. For `aace`, the longest palindromic suffix is `e`, so the answer is `aacecaa`. A careless approach that checks only whether the whole string is a palindrome, and otherwise appends the entire reverse string, would produce `aaceecaa`, which is valid but not minimal.

The longest palindromic suffix can also be quite long without being the whole string. For `abac`, the suffix `c` is the only palindromic suffix longer than one character, so the answer is `abacaba`. The algorithm must find the longest such suffix rather than simply stopping at the first convenient palindrome unless the candidates are examined in the correct order.

## Approaches

The direct approach is to try every suffix, starting with the entire string, and check whether that suffix is a palindrome. The first palindromic suffix found is the longest one. If its length is `k`, the prefix of length `n-k` is not part of that suffix, so we append its reverse. This is correct because the existing suffix is already symmetric, while every character in the prefix needs a matching character added on the right.

A palindrome check for a suffix of length `k` takes at most `floor(k/2)` character comparisons. If every candidate has to be checked and every check reaches its midpoint, the total number of comparisons is

`sum(floor(k/2))` for `k = 1 ... n`.

For `n = 5000`, this is exactly `6,250,000` comparisons. Creating and reversing candidate substrings also introduces additional `O(n^2)` character copying. The approach is therefore quadratic in the worst case. With this particular bound it can be made to pass in many languages, but it does not exploit the structure of the problem.

The faster observation is that finding the longest palindromic suffix can be converted into a standard prefix-matching problem. Reverse the string and call it `r`. A suffix of `s` is a palindrome exactly when the corresponding prefix of `r` is the same string.

For example, consider `s = abac`. Its reverse is `r = caba`. The suffix `c` of `s` corresponds to the prefix `c` of `r`. If a longer suffix of `s` were palindromic, that longer prefix of `r` would match the suffix of `s` itself.

We can encode this comparison using the KMP prefix function. Construct

`r + '#' + s`.

The separator is a character that does not occur in the input, so a prefix cannot accidentally cross from `r` into `s`. The final value of the KMP prefix function gives the length of the longest prefix of `r` that is also a suffix of `s`. Because a prefix of `r` is the reverse of a suffix of `s`, equality between them means that this suffix reads identically in both directions. It is exactly the longest palindromic suffix we need.

Once that length is known, the rest is immediate. If the longest palindromic suffix has length `k`, append `reverse(s[:n-k])`.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n²) | O(n) | Accepted for n ≤ 5000, but less efficient |
| KMP Prefix Function | O(n) | O(n) | Accepted and optimal |

## Algorithm Walkthrough

1. Read the string `s` and construct its reverse `r`. We are interested in palindromic suffixes of `s`, and those become prefixes when viewed from the reversed direction.
2. Build the combined string `t = r + '#' + s`. The separator must not occur in `s`, because the KMP prefix function must never treat characters on opposite sides of the separator as part of one candidate match.
3. Compute the KMP prefix function `pi` for `t`. For every position, `pi[i]` stores the length of the longest proper prefix of `t` that is also a suffix ending at position `i`.
4. Take `k = pi[-1]`. This is the longest prefix of `r` that is also a suffix of `s`. Since the prefix of `r` is the reverse of the corresponding suffix of `s`, equality means that this suffix is a palindrome.
5. Keep the first `n-k` characters of `s` as the part that still needs a mirror image. Append their reverse, `s[:n-k][::-1]`. The resulting string is a palindrome.
6. Print the resulting string. If `s` was already a palindrome, then `k = n`, so `s[:n-k]` is empty and nothing is appended.

### Why it works

Let `P` be the longest palindromic suffix of `s`, with length `k`. Because `P` is a palindrome, its reverse is still `P`. Reversing the whole string turns this suffix into a prefix of `r`, so `P` is simultaneously a prefix of `r` and a suffix of `s`. The KMP prefix function finds the longest such overlap, giving exactly `k`.

The remaining prefix `s[:n-k]` is placed at the beginning of the final string. Appending its reverse gives matching characters on the opposite side, while the middle part `P` is already a palindrome. Thus the constructed string is a palindrome.

Minimality follows from the choice of the longest palindromic suffix. Any valid final palindrome must leave some suffix of the original string as its central palindromic part, because only new characters can be added to the right. Using a shorter palindromic suffix would leave more original characters to be mirrored and would require more insertions. The longest palindromic suffix therefore gives the minimum possible number of appended characters.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve_string(s):
    r = s[::-1]
    t = r + '#' + s

    pi = [0] * len(t)

    for i in range(1, len(t)):
        j = pi[i - 1]

        while j > 0 and t[i] != t[j]:
            j = pi[j - 1]

        if t[i] == t[j]:
            j += 1

        pi[i] = j

    k = pi[-1]
    return s + s[:len(s) - k][::-1]

def main():
    s = input().strip()
    print(solve_string(s))

if __name__ == "__main__":
    main()
```

The `solve_string` function first creates `r`, the reverse of the input. The combined string `t` contains the information needed by KMP to compare prefixes of `r` with suffixes of `s`.

The prefix array `pi` is computed in the standard way. The variable `j` represents the length of the current candidate match. When `t[i]` does not match `t[j]`, following `pi[j - 1]` jumps directly to the next possible border instead of restarting the comparison from zero. That is what makes the prefix computation linear.

The final value `pi[-1]` is the length of the longest palindromic suffix. If `k` is that length, the number of characters that must be appended is `len(s) - k`. Python slicing makes the required prefix `s[:len(s) - k]`, and `[::-1]` supplies exactly the characters needed on the right side.

The separator `#` is safe because the problem's input is a string without spaces, but the statement does not explicitly restrict the alphabet to lowercase letters. A more defensive implementation can choose a separator not present in the input. The code above assumes the usual character set for this problem. To make the implementation completely independent of the alphabet, the separator can instead be chosen with a short loop.

There is no integer overflow issue because Python integers are arbitrary precision, and the only indices involved are bounded by the string length.

## Worked Examples

For Sample 1, `s = helloworld`. Its reverse is `dlrowolleh`. The KMP computation finds only one character of overlap, corresponding to the palindromic suffix `d`.

| Variable | State |
| --- | --- |
| `s` | `helloworld` |
| `r` | `dlrowolleh` |
| Longest palindromic suffix | `d` |
| `k` | `1` |
| Prefix to mirror | `helloworl` |
| Appended text | `lrowolleh` |
| Result | `helloworldlrowolleh` |

The suffix `d` is already symmetric, so the first nine characters must be mirrored. The appended text is the reverse of `helloworl`, producing the required palindrome.

For Sample 2, `s = anitalavalatina`. The entire string is already a palindrome, so the complete string matches its reverse.

| Variable | State |
| --- | --- |
| `s` | `anitalavalatina` |
| `r` | `anitalavalatina` |
| Longest palindromic suffix | `anitalavalatina` |
| `k` | `16` |
| Prefix to mirror | empty |
| Appended text | empty |
| Result | `anitalavalatina` |

Here the KMP overlap reaches the full length of the string. Consequently, there are zero characters left to mirror, which is exactly the desired behavior for an already palindromic input.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | The combined string has length `2n + 1`, and KMP processes every position with amortized constant work. |
| Space | O(n) | The reversed string, combined string, and prefix-function array all require linear space. |

With `n ≤ 5000`, the combined string contains at most 10001 characters. The prefix-function computation therefore performs only a small linear number of operations, comfortably within the 2-second limit and far below the 256 MB memory limit.

## Test Cases

```python
import sys
import io

def solve_string(s):
    r = s[::-1]
    t = r + '#' + s

    pi = [0] * len(t)

    for i in range(1, len(t)):
        j = pi[i - 1]

        while j > 0 and t[i] != t[j]:
            j = pi[j - 1]

        if t[i] == t[j]:
            j += 1

        pi[i] = j

    k = pi[-1]
    return s + s[:len(s) - k][::-1]

def run(inp: str) -> str:
    return solve_string(inp.strip())

assert run("helloworld") == "helloworldlrowolleh", "sample 1"
assert run("anitalavalatina") == "anitalavalatina", "sample 2"

assert run("a") == "a", "minimum-size input"
assert run("aaaaaa") == "aaaaaa", "all-equal characters"
assert run("aace") == "aacecaa", "single-character palindromic suffix"
assert run("abac") == "abacaba", "nontrivial boundary overlap"

max_input = "a" * 4999 + "b"
max_expected = max_input + "a" * 4999
assert run(max_input) == max_expected, "maximum-size input"

print("All tests passed.")
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `a` | `a` | Minimum length and already-palindromic input |
| `aaaaaa` | `aaaaaa` | Entire string is a palindrome and the longest overlap reaches `n` |
| `aace` | `aacecaa` | Only a one-character suffix can remain, catching unnecessary insertions |
| `abac` | `abacaba` | Nontrivial palindromic-suffix detection and prefix reversal |
| `aaaa...aaab` with length 5000 | `aaaa...aaabaaaa...aaa` | Maximum input size and linear-time behavior |

## Edge Cases

For the one-character input `a`, the reversed string is also `a`. The longest prefix-suffix match has length `1`, so `k = n`. The prefix `s[:0]` is empty, and the algorithm returns `a` without adding anything.

For an already-palindromic input such as `anitalavalatina`, the reversed string is identical to the original. KMP discovers an overlap of the full length, so `k = n`. This makes the appended prefix empty and prevents the common mistake of adding an unnecessary copy of the string.

For `aace`, the suffix `e` is palindromic, while the longer suffixes are not. KMP finds `k = 1`. The prefix `aac` is reversed to `caa`, giving `aacecaa`. The central character `e` is matched by itself, while the original prefix is mirrored around it.

For `abac`, the longest palindromic suffix is `c`, so `k = 1`. The algorithm takes the prefix `aba`, reverses it to `aba`, and produces `abacaba`. This case is useful because the prefix itself happens to be a palindrome, but the full input is not. An implementation that simply reverses the whole input would add too many characters.

For the maximum-length input consisting of 4999 copies of `a` followed by `b`, the final `b` is the longest palindromic suffix. KMP still processes only the `2n + 1` characters in the combined string. The algorithm appends 4999 copies of `a`, producing a palindrome of length 9999. This exercises the largest allowed input while also checking that the implementation handles a very small palindromic suffix without scanning candidate suffixes repeatedly.
