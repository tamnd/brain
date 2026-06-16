---
title: "CF 1008A - Romaji"
description: "We are given a single lowercase word and asked to verify whether it follows a specific phonetic rule. The rule constrains how consonants and vowels can appear in sequence."
date: "2026-06-16T23:03:26+07:00"
tags: ["codeforces", "competitive-programming", "implementation", "strings"]
categories: ["algorithms"]
codeforces_contest: 1008
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 497 (Div. 2)"
rating: 900
weight: 1008
solve_time_s: 77
verified: true
draft: false
---

[CF 1008A - Romaji](https://codeforces.com/problemset/problem/1008/A)

**Rating:** 900  
**Tags:** implementation, strings  
**Solve time:** 1m 17s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a single lowercase word and asked to verify whether it follows a specific phonetic rule. The rule constrains how consonants and vowels can appear in sequence.

Every consonant must be immediately followed by a vowel, with a single exception: the consonant `'n'` is allowed to be followed by either any letter or by the end of the string. Vowels are fixed as `'a'`, `'e'`, `'i'`, `'o'`, and `'u'`. Any other letter is treated as a consonant.

The task is simply to decide whether the entire string respects this constraint everywhere it applies.

The input length is at most 100, which means a direct scan of the string is sufficient. Even an $O(n^2)$ approach would be trivial here, but the structure suggests a single left-to-right validation is enough.

A few edge cases are easy to miss when thinking informally about the rule. The first is a consonant appearing at the end of the string. For example, `"abc"` ends with `'c'`, which is a consonant, so it immediately violates the rule because there is no following vowel.

Another case is consecutive consonants. For example, `"king"` fails because `'k'` is followed by `'i'` which is fine, but `'n'` is followed by `'g'`, and `'g'` is a consonant that is not `'n'`, so it requires a vowel afterward but none is guaranteed.

Finally, `'n'` itself is special but only locally. A string like `"nbo"` is valid because `'n'` can be followed by a consonant, but that does not grant safety to the next character if it is a non-`n` consonant.

## Approaches

A brute-force interpretation would check every consonant position and scan forward until it finds the next character to verify whether it is a vowel or whether the consonant is `'n'`. This works correctly, but in the worst case it repeatedly rescans suffixes, leading to quadratic behavior.

Since the string is short here, even that would pass, but the structure of the condition suggests a cleaner invariant: the validity of each position depends only on the current character and the next one. There is no long-range dependency, so we do not need to look ahead arbitrarily far.

This reduces the problem to a single linear pass. At each position, we only need to verify whether the current character is a consonant that violates the rule. If it is a vowel, nothing needs to be checked. If it is `'n'`, it is always safe. Otherwise, the next character must exist and must be a vowel.

This observation collapses all redundant checks and makes the validation purely local.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Scan Ahead | O(n²) | O(1) | Accepted but unnecessary |
| Single Pass Check | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

We process the string from left to right, validating each character based on whether it is a vowel, `'n'`, or another consonant.

1. Define a set of vowels `{a, e, i, o, u}` so membership checks are constant time. This avoids repeated string comparisons.
2. Iterate through each index `i` of the string.
3. If the current character is a vowel, continue without restriction because vowels impose no constraints on following letters.
4. If the current character is `'n'`, also continue because `'n'` is exempt from the “must be followed by vowel” rule.
5. If the current character is any other consonant, we must ensure there is a next character. If `i + 1` is out of bounds, the string is invalid immediately.
6. If a next character exists, verify it is a vowel. If not, the rule is violated and we can terminate early.

### Why it works

The key invariant is that every invalid configuration is detectable at the exact position where a non-`n` consonant appears. Such a consonant has a strict local requirement on its immediate successor. If that requirement is violated, no later correction is possible because the rule is not about global structure but adjacency. Therefore, checking only the next character is sufficient to guarantee correctness.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    s = input().strip()
    vowels = set("aeiou")
    
    n = len(s)
    for i, c in enumerate(s):
        if c in vowels:
            continue
        if c == 'n':
            continue
        
        # consonant that must be followed by vowel
        if i + 1 >= n or s[i + 1] not in vowels:
            print("NO")
            return
    
    print("YES")

if __name__ == "__main__":
    solve()
```

The code mirrors the algorithm directly. The vowel set is used for fast membership checks, ensuring constant-time validation per character. The early exit on failure avoids unnecessary scanning after detecting a violation.

A subtle point is the boundary check `i + 1 >= n`. Without it, accessing `s[i + 1]` would raise an error when a consonant appears at the end of the string. This is exactly the case that invalidates words like `"king"`.

## Worked Examples

### Example 1: `sumimasen`

| i | char | type | next char | valid so far |
| --- | --- | --- | --- | --- |
| 0 | s | consonant | u | ok |
| 1 | u | vowel | - | ok |
| 2 | m | consonant | i | ok |
| 3 | i | vowel | - | ok |
| 4 | m | consonant | a | ok |
| 5 | a | vowel | - | ok |
| 6 | s | consonant | e | ok |
| 7 | e | vowel | - | ok |
| 8 | n | special | end | ok |

This confirms that every non-`n` consonant is followed by a vowel and `'n'` appears safely at the end.

### Example 2: `king`

| i | char | type | next char | valid so far |
| --- | --- | --- | --- | --- |
| 0 | k | consonant | i | ok |
| 1 | i | vowel | - | ok |
| 2 | n | special | g | ok |
| 3 | g | consonant | end | fail |

At index 3, `'g'` is a consonant with no following character, violating the rule immediately.

This trace shows that failure is detected exactly at the first invalid adjacency, with no need to examine the remainder of the string.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Each character is processed once with constant-time checks |
| Space | O(1) | Only a fixed vowel set and loop variables are used |

The maximum input size is 100, so this linear scan is effectively instantaneous under the constraints.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    
    from sys import stdout
    backup = stdout
    sys.stdout = io.StringIO()
    
    def solve():
        s = input().strip()
        vowels = set("aeiou")
        
        n = len(s)
        for i, c in enumerate(s):
            if c in vowels:
                continue
            if c == 'n':
                continue
            if i + 1 >= n or s[i + 1] not in vowels:
                print("NO")
                return
        print("YES")
    
    solve()
    out = sys.stdout.getvalue()
    sys.stdout = backup
    return out.strip()

# provided sample
assert run("sumimasen\n") == "YES"

# single vowel
assert run("a\n") == "YES"

# single consonant (invalid)
assert run("b\n") == "NO"

# valid with n at end
assert run("man\n") == "YES"

# invalid consecutive consonants
assert run("king\n") == "NO"

# boundary case: consonant at end
assert run("abc\n") == "NO"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `"a"` | YES | minimal valid string |
| `"b"` | NO | single consonant edge case |
| `"man"` | YES | special handling of `'n'` |
| `"king"` | NO | consecutive consonant failure |
| `"abc"` | NO | consonant at end boundary |

## Edge Cases

A single-character string like `"n"` is valid because `'n'` is explicitly exempt from needing a following vowel. The loop processes it once, classifies it as the special case, and accepts it without any bounds issues.

A string ending in a non-`n` consonant such as `"abc"` fails at the last character. When `i` reaches the final index, the condition `i + 1 >= n` triggers the rejection immediately. This captures the core rule that every non-special consonant must be followed by another character, and that character must be a vowel.

A run of consonants such as `"bcd"` fails at the first character already, since `'b'` is followed by `'c'`, which is not a vowel and also not exempt. The algorithm terminates early, showing that violations are detected at the earliest possible position without needing full traversal.
