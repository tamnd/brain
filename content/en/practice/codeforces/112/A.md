---
title: "CF 112A - Petya and Strings"
description: "We are given two strings made of English letters. Both strings have the same length, but letters may appear in either uppercase or lowercase form. The task is to compare the two strings lexicographically while completely ignoring letter case."
date: "2026-05-28T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "implementation", "strings"]
categories: ["algorithms"]
codeforces_contest: 112
codeforces_index: "A"
codeforces_contest_name: "Codeforces Beta Round 85 (Div. 2 Only)"
rating: 800
weight: 112
solve_time_s: 97
verified: true
draft: false
---

[CF 112A - Petya and Strings](https://codeforces.com/problemset/problem/112/A)

**Rating:** 800  
**Tags:** implementation, strings  
**Solve time:** 1m 37s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given two strings made of English letters. Both strings have the same length, but letters may appear in either uppercase or lowercase form. The task is to compare the two strings lexicographically while completely ignoring letter case.

Ignoring case means that `'A'` and `'a'` must be treated as identical characters. After comparison, we print:

- `-1` if the first string is lexicographically smaller
- `1` if the first string is lexicographically larger
- `0` if both strings are equal

The strings are very small, at most length 100. Even an inefficient character-by-character solution easily fits within the limits. The real challenge is not performance, it is handling case conversion correctly before comparison.

A common mistake is to compare the original strings directly. Python compares uppercase and lowercase letters using ASCII values, where uppercase letters come before lowercase letters. That produces incorrect answers for this problem.

Consider this input:

```
aaaa
aaaA
```

The correct output is:

```
0
```

A direct comparison without converting case would incorrectly treat `'a'` and `'A'` as different.

Another easy mistake is converting only one string to lowercase.

Example:

```
aBc
ABC
```

The correct output is:

```
0
```

If only the first string is converted, the comparison becomes `"abc"` vs `"ABC"`, which still fails because uppercase and lowercase ASCII values differ.

One more edge case appears when the strings differ only near the end.

Example:

```
abcz
abca
```

The correct output is:

```
1
```

A careless implementation that stops too early or compares only prefixes would miss the final differing character.

## Approaches

The most direct solution is to compare the strings character by character. For each position, we can manually convert both characters to the same case and then decide which string is larger. The first differing position determines the answer.

This brute-force method is already fast enough. Each string has at most 100 characters, so we perform at most 100 comparisons. That is effectively instant.

We can simplify the implementation further by observing that Python already supports lexicographical string comparison. The only issue is case sensitivity. Once both strings are converted entirely to lowercase, the built-in comparison behaves exactly as required.

The brute-force version works because lexicographical order depends only on the first differing character. The cleaner solution works because converting both strings to the same case preserves their relative alphabetical order while removing case differences completely.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n) | O(1) | Accepted |
| Optimal | O(n) | O(n) | Accepted |

Here, `n` is the string length.

## Algorithm Walkthrough

1. Read the first string from input.
2. Read the second string from input.
3. Convert both strings to lowercase.

This removes all differences caused only by uppercase versus lowercase letters.
4. Compare the lowercase strings lexicographically.
5. If the first string is smaller, print `-1`.
6. If the first string is larger, print `1`.
7. Otherwise, print `0`.

### Why it works

Lexicographical comparison depends on the relative order of characters from left to right. Converting both strings to lowercase preserves alphabetical ordering while making uppercase and lowercase versions of the same letter identical. After conversion, a normal string comparison produces exactly the required result.

## Python Solution

```python
import sys
input = sys.stdin.readline

s1 = input().strip().lower()
s2 = input().strip().lower()

if s1 < s2:
    print(-1)
elif s1 > s2:
    print(1)
else:
    print(0)
```

The first step reads both strings and immediately converts them to lowercase using `.lower()`. Doing the conversion early keeps the rest of the logic simple and avoids repeated character handling later.

Using `.strip()` is important because `input()` includes the trailing newline character. Without removing it, the comparison would include `'\n'`, producing incorrect results.

Python already performs lexicographical string comparison correctly. It compares characters from left to right and stops at the first mismatch. That matches the exact definition required by the problem.

The three comparison branches directly map to the required outputs. No manual loops are necessary because Python handles the comparison internally.

## Worked Examples

### Example 1

Input:

```
aaaa
aaaA
```

After lowercase conversion:

| Variable | Value |
| --- | --- |
| `s1` | `"aaaa"` |
| `s2` | `"aaaa"` |

Comparison result:

| Check | Result |
| --- | --- |
| `s1 < s2` | False |
| `s1 > s2` | False |
| Final output | `0` |

This example demonstrates why case normalization is necessary. The original strings differ in capitalization only, so they must compare as equal.

### Example 2

Input:

```
abs
Abz
```

After lowercase conversion:

| Variable | Value |
| --- | --- |
| `s1` | `"abs"` |
| `s2` | `"abz"` |

Character comparison:

| Position | `s1[i]` | `s2[i]` | Result |
| --- | --- | --- | --- |
| 0 | `a` | `a` | equal |
| 1 | `b` | `b` | equal |
| 2 | `s` | `z` | `s < z` |

Final output:

```
-1
```

This trace shows how lexicographical comparison depends on the first differing character.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Each character is processed once during lowercase conversion and comparison |
| Space | O(n) | Lowercase string copies are created |

The constraints are extremely small, with strings of length at most 100. An O(n) solution easily fits within both the time and memory limits.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys, io

def solve():
    input = sys.stdin.readline

    s1 = input().strip().lower()
    s2 = input().strip().lower()

    if s1 < s2:
        print(-1)
    elif s1 > s2:
        print(1)
    else:
        print(0)

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    solve()

    return sys.stdout.getvalue()

# provided sample
assert run("aaaa\naaaA\n") == "0\n", "sample 1"

# custom cases
assert run("a\nb\n") == "-1\n", "single character smaller"
assert run("Z\na\n") == "1\n", "uppercase handling"
assert run("Codeforces\ncodeforces\n") == "0\n", "all equal ignoring case"
assert run("abcz\nabca\n") == "1\n", "difference at last character"

# maximum-size style case
s1 = "A" * 100
s2 = "a" * 100
assert run(f"{s1}\n{s2}\n") == "0\n", "maximum equal strings"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `a / b` | `-1` | Minimum-size comparison |
| `Z / a` | `1` | Correct uppercase normalization |
| `Codeforces / codeforces` | `0` | Equality ignoring case |
| `abcz / abca` | `1` | Difference at final position |
| 100 identical letters with mixed case | `0` | Maximum-length handling |

## Edge Cases

Consider strings that differ only by capitalization.

Input:

```
ABC
abc
```

The algorithm converts both strings to lowercase:

```
abc
abc
```

The strings become identical, so the output is:

```
0
```

Without normalization, ASCII comparison would incorrectly treat uppercase letters differently.

Now consider a mismatch at the final character.

Input:

```
abcy
abcz
```

After conversion:

```
abcy
abcz
```

The first three positions match. At the final position, `'y' < 'z'`, so the algorithm prints:

```
-1
```

This confirms that the comparison continues until the first actual difference appears.

Finally, consider single-character strings.

Input:

```
B
a
```

After lowercase conversion:

```
b
a
```

Since `'b' > 'a'`, the output becomes:

```
1
```

This validates that the algorithm works correctly even for the minimum input size.
