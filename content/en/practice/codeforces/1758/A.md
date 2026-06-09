---
title: "CF 1758A - SSeeeeiinngg DDoouubbllee"
description: "We are given a string s. If we \"double\" the string, every character appears twice. For example, \"abc\" becomes the multiset of characters in \"aabbcc\". Our task is not to output the doubled string itself."
date: "2026-06-09T14:37:51+07:00"
tags: ["codeforces", "competitive-programming", "constructive-algorithms", "strings"]
categories: ["algorithms"]
codeforces_contest: 1758
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 836 (Div. 2)"
rating: 800
weight: 1758
solve_time_s: 157
verified: false
draft: false
---

[CF 1758A - SSeeeeiinngg DDoouubbllee](https://codeforces.com/problemset/problem/1758/A)

**Rating:** 800  
**Tags:** constructive algorithms, strings  
**Solve time:** 2m 37s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a string `s`. If we "double" the string, every character appears twice. For example, `"abc"` becomes the multiset of characters in `"aabbcc"`.

Our task is not to output the doubled string itself. We may rearrange those doubled characters in any order, as long as the final string is a palindrome and uses exactly the same characters.

A palindrome reads the same from left to right and from right to left. Since every character in the doubled string appears an even number of times, a palindromic arrangement is always possible.

The constraints are very small. Each string has length at most 100, and there are at most 1000 test cases. Even an $O(n^2)$ solution would be fine here. The real challenge is spotting the simple construction that always works.

One easy mistake is to overthink the rearrangement and start counting character frequencies. For example:

```
s = "abc"
```

The doubled string contains two copies of each letter. A frequency-based solution works, but it is unnecessary.

Another subtle case is when all characters are identical:

```
s = "aaaa"
```

The doubled string is `"aaaaaaaa"`, which is already a palindrome. Any correct construction must still produce a valid palindrome.

A third case is when characters repeat irregularly:

```
s = "abca"
```

A careless approach might output the doubled string directly:

```
aabbccaa
```

This is not a palindrome. We need a construction that guarantees symmetry regardless of the character pattern inside the original string.

## Approaches

A brute-force viewpoint is to generate all rearrangements of the doubled string and check whether any of them is a palindrome.

This is obviously correct because every possible arrangement is examined. The problem is the number of permutations. If the doubled string has length 200, the number of rearrangements is astronomically large, roughly $200!$. Even for length 20, this is already completely infeasible.

The key observation comes from thinking about palindromes directly instead of thinking about rearrangements.

Suppose we place the original string on the left half of the answer:

```
s = abc
```

If we place the reverse of the original string on the right half:

```
abc + cba = abccba
```

the result is automatically a palindrome.

Why does this use exactly the required characters? Every character from `s` appears once in the left half and once in the reversed half. Thus each original character appears exactly twice overall, which is precisely the doubled string's character multiset.

This means we do not need any frequency counting, sorting, or special handling. The answer is always:

```
s + reverse(s)
```

### Comparison

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O((2n)!)$ | $O((2n)!)$ | Too slow |
| Optimal | $O(n)$ | $O(n)$ | Accepted |

## Algorithm Walkthrough

1. Read the string `s`.
2. Compute its reverse.
3. Concatenate the original string and its reverse.
4. Output the resulting string.

The crucial idea is that the first half and second half mirror each other exactly. Since the second half is the reverse of the first half, the entire string reads identically from both directions.

### Why it works

Let the original string be:

```
s = c1 c2 ... cn
```

The algorithm outputs:

```
c1 c2 ... cn cn ... c2 c1
```

For every position from the left, the corresponding position from the right contains the same character. Hence the string is a palindrome.

Each character of the original string appears once in the first half and once in the mirrored second half. Consequently, every character appears exactly twice, matching the doubled string's character multiset. The output is both a palindrome and a valid rearrangement of the doubled string.

## Python Solution

```python
import sys
input = sys.stdin.readline

t = int(input())

for _ in range(t):
    s = input().strip()
    print(s + s[::-1])
```

The solution follows the construction directly.

The expression `s[::-1]` creates the reversed string. Concatenating `s` with its reverse produces a palindrome immediately.

There are no boundary cases requiring special handling. A string of length one becomes two identical characters, which is still a palindrome. Repeated characters work naturally because the construction does not depend on character uniqueness.

The implementation performs only one reversal and one concatenation per test case, making it both simple and efficient.

## Worked Examples

### Example 1

Input string:

```
sururu
```

| Step | Value |
| --- | --- |
| Original string | `sururu` |
| Reverse | `ururus` |
| Output | `sururuururus` |

Checking symmetry:

```
sururuururus
||||||||||||
sururuururus
```

Reading from either direction gives the same string. Every character from the original appears exactly twice.

### Example 2

Input string:

```
errorgorn
```

| Step | Value |
| --- | --- |
| Original string | `errorgorn` |
| Reverse | `nrogrorre` |
| Output | `errorgornnrogrorre` |

The left half is the original string and the right half is its mirror image. This guarantees a palindrome without any frequency analysis.

These examples demonstrate the central invariant: the second half is always the reverse of the first half.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n)$ | Reversing the string and concatenating both require linear time |
| Space | $O(n)$ | The output string and reversed copy each have linear size |

Here, $n$ is the length of the current string. Since $n \le 100$, the running time is tiny. Even across 1000 test cases, the solution easily fits within the limits.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def solve():
    input = sys.stdin.readline

    t = int(input())
    for _ in range(t):
        s = input().strip()
        print(s + s[::-1])

def run(inp: str) -> str:
    old_stdin = sys.stdin
    old_stdout = sys.stdout

    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    solve()

    out = sys.stdout.getvalue()

    sys.stdin = old_stdin
    sys.stdout = old_stdout

    return out

# provided sample
assert run(
"""4
a
sururu
errorgorn
anutforajaroftuna
"""
) == (
"""aa
sururuururus
errorgornnrogrorre
anutforajaroftunaanutforajaroftuna
"""
)

# minimum size
assert run(
"""1
a
"""
) == (
"""aa
"""
), "single character"

# repeated characters
assert run(
"""1
aaaa
"""
) == (
"""aaaaaaaa
"""
), "all characters equal"

# distinct characters
assert run(
"""1
abc
"""
) == (
"""abccba
"""
), "basic palindrome construction"

# boundary length pattern
assert run(
"""1
abca
"""
) == (
"""abcaacba
"""
), "repeated and distinct characters mixed"
```

### Test Coverage Summary

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `a` | `aa` | Minimum length |
| `aaaa` | `aaaaaaaa` | All characters identical |
| `abc` | `abccba` | Basic mirror construction |
| `abca` | `abcaacba` | Mixed repeated and unique characters |

## Edge Cases

Consider the smallest possible input:

```
1
a
```

The algorithm computes:

```
a + a = aa
```

The result is a palindrome and contains exactly two copies of the original character.

Now consider a string where every character is the same:

```
1
aaaa
```

The reverse is still `"aaaa"`, so the output becomes:

```
aaaaaaaa
```

Every position matches its mirrored position automatically.

Finally, consider a mixed string:

```
1
abca
```

The algorithm performs:

| Step | Value |
| --- | --- |
| Original | `abca` |
| Reverse | `acba` |
| Result | `abcaacba` |

Checking mirrored positions:

```
a b c a a c b a
a b c a a c b a
```

Every symmetric pair matches. The output contains exactly two copies of each character from the original string, so it is a valid rearrangement of the doubled string.
