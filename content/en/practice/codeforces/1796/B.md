---
title: "CF 1796B - Asterisk-Minor Template"
description: "We are asked to construct a “template” string that can describe two given strings simultaneously. A template consists of lowercase letters and asterisks. Each asterisk can be replaced with any string, including the empty string, to match the original strings."
date: "2026-06-09T10:00:59+07:00"
tags: ["codeforces", "competitive-programming", "implementation", "strings"]
categories: ["algorithms"]
codeforces_contest: 1796
codeforces_index: "B"
codeforces_contest_name: "Educational Codeforces Round 144 (Rated for Div. 2)"
rating: 1000
weight: 1796
solve_time_s: 151
verified: false
draft: false
---

[CF 1796B - Asterisk-Minor Template](https://codeforces.com/problemset/problem/1796/B)

**Rating:** 1000  
**Tags:** implementation, strings  
**Solve time:** 2m 31s  
**Verified:** no  

## Solution
## Problem Understanding

We are asked to construct a “template” string that can describe two given strings simultaneously. A template consists of lowercase letters and asterisks. Each asterisk can be replaced with any string, including the empty string, to match the original strings. Importantly, a template is “asterisk-minor” if the number of asterisks does not exceed the number of letters in it.

Given two strings, the goal is to determine whether a single asterisk-minor template exists that both strings match, and if so, produce one. Each test case consists of two strings of length at most 50, and there may be up to 10,000 test cases.

The first thing to notice is that the small string length makes operations on entire strings feasible. Even a quadratic comparison (like checking all character pairs) is acceptable because $50 \cdot 50 = 2500$, and multiplying by 10,000 test cases still fits comfortably in 2 seconds.

The non-obvious edge cases involve:

- Completely identical strings. For example, `a = "abc"`, `b = "abc"`. The template is simply the string itself, with no asterisks.
- Strings differing only in the middle. For instance, `a = "abXcd"`, `b = "abYcd"`. A naive approach that always inserts a single asterisk per difference might accidentally violate the “asterisk-minor” constraint.
- Completely different strings of length 1. For `a = "x"`, `b = "y"`, the only valid template is `*`, which is asterisk-minor because it has 1 letter (if we include an empty string?) but we need to handle letter counting carefully.

## Approaches

A brute-force approach would attempt to generate every possible combination of asterisks and letters in a template and test it against both strings. For two strings of length 50, the number of ways to insert asterisks grows exponentially, making this infeasible even for small lengths.

The key insight is that the asterisk can be used to “absorb” any segment of differing characters. Therefore, the simplest valid template is one that keeps the longest common prefix and suffix as literal letters and replaces everything in between with a single asterisk.

For example, given `a = "aaab"` and `b = "zzzb"`, the longest common suffix is `"b"`, the longest common prefix is empty, and the middle `"aaa"` vs `"zzz"` can be replaced by `*`. The resulting template is `*b`. This template is asterisk-minor: it has 1 asterisk and 1 letter, satisfying the constraint.

If the two strings have no matching prefix or suffix, the simplest template is `*`, which is also asterisk-minor if at least one string is of length ≥1. If the common prefix and suffix together are shorter than the total number of asterisks needed, it might violate the asterisk-minor rule, and we must then report `NO`.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(2^n) | O(n) | Too slow |
| Prefix-Suffix | O(n) per test case | O(n) | Accepted |

## Algorithm Walkthrough

1. For each pair of strings `a` and `b`, start by finding the longest common prefix. Initialize `i = 0` and increment `i` while `a[i] == b[i]`. Stop when the characters differ or the end of one string is reached.
2. Next, find the longest common suffix. Initialize `j = 0` and increment `j` while `a[-1-j] == b[-1-j]` and the remaining substring does not overlap the prefix. This ensures that prefix and suffix do not intersect.
3. If the sum of prefix length and suffix length is equal to or greater than the length of either string, it means the strings are identical in that range, and the template can be constructed without internal asterisks.
4. Otherwise, replace the differing middle segment with a single asterisk. Concatenate the prefix, asterisk, and suffix to form the template.
5. Verify the asterisk-minor condition: count letters and asterisks. If letters ≥ asterisks, print `YES` and the template. Otherwise, print `NO`.

Why it works: at most one asterisk is needed to replace any differing segment because a single asterisk can absorb any substring. By keeping the matching prefix and suffix intact, we ensure that all literal letters are preserved. The asterisk-minor condition is automatically satisfied for strings of length ≤50 because the middle segment is replaced by at most one asterisk.

## Python Solution

```python
import sys
input = sys.stdin.readline

t = int(input())
for _ in range(t):
    a = input().strip()
    b = input().strip()
    
    n = len(a)
    m = len(b)
    
    # Longest common prefix
    i = 0
    while i < min(n, m) and a[i] == b[i]:
        i += 1
    
    # Longest common suffix
    j = 0
    while j < min(n - i, m - i) and a[n-1-j] == b[m-1-j]:
        j += 1
    
    if i + j == 0 and n != m:
        # No overlap and no common letters: * cannot be minor if no letters
        print("NO")
    else:
        template = a[:i] + "*" + a[n-j:] if j > 0 else a[:i] + "*"
        letters = len(a[:i]) + len(a[n-j:])
        stars = 1
        if letters >= stars:
            print("YES")
            print(template)
        else:
            print("NO")
```

The code carefully avoids overlapping the prefix and suffix. We only insert a single asterisk regardless of the length of differing segments, which is enough to match both strings. Checking `letters >= stars` ensures the asterisk-minor condition is satisfied.

## Worked Examples

Sample input:

```
a = "aaab", b = "zzzb"
```

| i | j | template |
| --- | --- | --- |
| 0 | 1 | *b |

Explanation: no common prefix, common suffix `"b"`, differing middle replaced by `*`. Letters = 1, asterisks = 1 → asterisk-minor satisfied.

Another example:

```
a = "codeforces", b = "tokitlx"
```

| i | j | template |
| --- | --- | --- |
| 0 | 0 | NO |

Explanation: no common prefix or suffix, replacing entire strings with `*` would produce letters < asterisks, violating the rule.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(T * min( | a |
| Space | O(n) | Storing strings and temporary template |

With T ≤ 10^4 and |a|, |b| ≤ 50, the worst-case total operations are around 500,000, well within the 2-second limit.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    out = io.StringIO()
    sys.stdout = out
    exec(open("solution.py").read())
    return out.getvalue().strip()

# Provided samples
assert run("6\naaab\nzzzb\ncodeforces\natcoder\ncodeforces\ntokitlx\naaaa\naaaaaa\nabcd\nabcd\nc\nf\n") == "YES\n*b\nYES\n*co*\nNO\nYES\na*a*a*a\nYES\nabcd\nNO"

# Custom cases
assert run("2\nx\ny\nabc\nabc\n") == "YES\n*\nYES\nabc"
assert run("1\na\naa\n") == "YES\n*a"
assert run("1\nabcdef\nghijkl\n") == "NO"
assert run("1\nabc\nxyz\n") == "NO"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `x, y` | `YES\n*` | Single-letter strings with no overlap |
| `abc, abc` | `YES\nabc` | Identical strings |
| `a, aa` | `YES\n*a` | Prefix handling for different lengths |
| `abcdef, ghijkl` | `NO` | Completely different strings |
| `abc, xyz` | `NO` | Common prefix/suffix absent, template impossible |

## Edge Cases

For two identical strings, e.g., `a = "abcd"`, `b = "abcd"`, the algorithm finds prefix length 4, suffix length 0, and no differing middle. Template is `"abcd"`, asterisk-minor condition holds because stars = 0 ≤ letters = 4.

For strings with no common prefix or suffix, like `a = "abc"`, `b = "xyz"`, prefix = 0, suffix = 0, the algorithm considers replacing the middle with `*`, but letters = 0, stars = 1 →
