---
title: "CF 1504A -  D\u00e9j\u00e0 Vu"
description: "We are given several strings. For each string, we must insert exactly one character 'a' at some position. The new string must have length The input contains up to 10^4 test cases, and the sum of all string lengths is at most 3·10^5."
date: "2026-06-10T20:40:31+07:00"
tags: ["codeforces", "competitive-programming", "constructive-algorithms", "strings"]
categories: ["algorithms"]
codeforces_contest: 1504
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 712 (Div. 2)"
rating: 800
weight: 1504
solve_time_s: 358
verified: false
draft: false
---

[CF 1504A -  D\u00e9j\u00e0 Vu](https://codeforces.com/problemset/problem/1504/A)

**Rating:** 800  
**Tags:** constructive algorithms, strings  
**Solve time:** 5m 58s  
**Verified:** no  

## Solution
## Problem Understanding

We are given several strings. For each string, we must insert exactly one character `'a'` at some position. The new string must have length `|s|+1`, and it must not be a palindrome. If every possible insertion produces a palindrome, we have to report that no solution exists.

The input contains up to `10^4` test cases, and the sum of all string lengths is at most `3·10^5`. Since the total amount of data is moderate, an algorithm whose running time is linear in the total length is easily fast enough. Quadratic work per string would still pass for short strings, but a cubic approach would become unnecessary overhead.

Several edge cases are easy to mishandle.

The first one is a string consisting entirely of `'a'`.

Input:

```
a
```

The only possible insertion creates `"aa"`, which is still a palindrome. The correct answer is:

```
NO
```

A careless solution that always puts an `'a'` at the front would incorrectly output `"aa"`.

Another case is when one insertion position gives a palindrome but another position works.

Input:

```
ab
```

Inserting at the end gives `"aba"`, which is a palindrome, but inserting at the beginning gives `"aab"`, which is not. The correct answer is:

```
YES
aab
```

A solution that checks only one position may miss valid constructions.

There are also strings that are already palindromes but still admit a valid answer.

Input:

```
aba
```

Adding `'a'` to the front gives `"aaba"`, which is not a palindrome. Being a palindrome initially does not imply impossibility.

## Approaches

A straightforward brute-force method tries all `n+1` insertion positions. For each position, it constructs the resulting string and checks whether that string is a palindrome. The method is correct because every possible insertion is examined.

The problem is that a string of length `n` has `n+1` candidate positions, and checking whether a candidate is a palindrome takes `O(n)` time. Constructing the string itself also costs `O(n)`. The total complexity becomes `O(n²)`.

With the given constraints, even quadratic time is acceptable in practice because the total length is only `3·10^5`. Still, the problem has a much simpler structure.

The key observation is that if the original string contains some character other than `'a'`, then one of two constructions must work.

We can prepend `'a'`, producing

```
a + s
```

or append `'a'`, producing

```
s + a
```

Suppose both were palindromes. Since

```
a+s
```

is a palindrome, removing its first and last characters shows that the remaining part of the string must be symmetric. Doing the same with

```
s+a
```

leads to the same conclusion. Combining these conditions forces every character of `s` to be `'a'`.

So whenever the string contains at least one non-`'a'` character, at least one of these two constructions is guaranteed to be non-palindromic. We only need to test the two possibilities.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n²) | O(n) | Accepted |
| Optimal | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Read a string `s`.
2. Construct the string obtained by adding `'a'` at the front.
3. Check whether this new string is a palindrome. If it is not, output `"YES"` and this string.
4. Otherwise, construct the string obtained by adding `'a'` at the end.
5. Check whether this second string is a palindrome. If it is not, output `"YES"` and this string.
6. If both candidates are palindromes, output `"NO"`.

The reason only two positions are examined is that any string containing a character different from `'a'` must make at least one of these candidates non-palindromic.

### Why it works

The algorithm explicitly checks the two candidate strings `a+s` and `s+a`. If either one is not a palindrome, it is a valid answer.

Suppose both candidates are palindromes. In `a+s`, the first and last characters are equal, so the last character of `s` must be `'a'`. Removing these matching characters leaves a palindrome. Repeating this argument shows that every character of `s` is `'a'`. For such a string, every insertion of `'a'` produces another all-`'a'` string, which is always a palindrome. Hence no solution exists.

Since the algorithm outputs a valid string whenever one exists, and reports `"NO"` exactly when no solution exists, it is correct.

## Python Solution

```python
import sys
input = sys.stdin.readline

def is_palindrome(s):
    return s == s[::-1]

t = int(input())
ans = []

for _ in range(t):
    s = input().strip()

    front = 'a' + s
    if not is_palindrome(front):
        ans.append("YES")
        ans.append(front)
        continue

    back = s + 'a'
    if not is_palindrome(back):
        ans.append("YES")
        ans.append(back)
    else:
        ans.append("NO")

print("\n".join(ans))
```

The helper function checks whether a string equals its reverse. Python slicing makes this operation concise and runs in linear time.

For each test case, the code first tries putting `'a'` at the front. If that string is not a palindrome, it immediately records the answer and moves to the next test case.

If the first attempt fails, the code tries placing `'a'` at the end. Only when both candidates are palindromes does it print `"NO"`.

The order matters because once a valid construction is found, there is no reason to test anything else.

Boundary conditions are simple. Strings of length one are handled naturally. For example, `"a"` leads to `"aa"` in both attempts, so the answer becomes `"NO"`.

## Worked Examples

### Example 1

Input string:

```
ab
```

| Step | Candidate | Palindrome? | Action |
| --- | --- | --- | --- |
| 1 | `"aab"` | No | Output answer |

The algorithm stops immediately and prints:

```
YES
aab
```

This example shows that the first candidate may already work, even though adding `'a'` elsewhere could produce a palindrome.

### Example 2

Input string:

```
zza
```

| Step | Candidate | Palindrome? | Action |
| --- | --- | --- | --- |
| 1 | `"azza"` | Yes | Continue |
| 2 | `"zzaa"` | No | Output answer |

The output becomes:

```
YES
zzaa
```

This example demonstrates why both ends must be checked. One insertion position can fail while the other succeeds.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Two palindrome checks, each linear |
| Space | O(n) | Temporary strings and reversed copies |

Here `n` denotes the length of one string. Since the sum of all lengths is at most `3·10^5`, the total amount of work is linear in the input size and comfortably fits within the limits.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    input = sys.stdin.readline

    def is_palindrome(s):
        return s == s[::-1]

    t = int(input())
    ans = []

    for _ in range(t):
        s = input().strip()

        front = 'a' + s
        if not is_palindrome(front):
            ans.append("YES")
            ans.append(front)
            continue

        back = s + 'a'
        if not is_palindrome(back):
            ans.append("YES")
            ans.append(back)
        else:
            ans.append("NO")

    return "\n".join(ans)

# provided sample
assert run(
"""6
cbabc
ab
zza
ba
a
nutforajaroftuna
"""
) == (
"""YES
acbabc
YES
aab
YES
zzaa
YES
aba
NO
YES
anutforajaroftuna"""
)

# minimum size
assert run(
"""1
a
"""
) == "NO", "single a"

# single non-a character
assert run(
"""1
b
"""
) == "YES\nab", "length one, solvable"

# all equal characters
assert run(
"""1
aaaa
"""
) == "NO", "all characters are a"

# off-by-one case
assert run(
"""1
zza
"""
) == "YES\nzzaa", "front insertion fails, back works"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `a` | `NO` | Minimum size and impossible case |
| `b` | `YES ab` | Length one with a valid answer |
| `aaaa` | `NO` | All characters equal to `'a'` |
| `zza` | `YES zzaa` | One end fails, the other succeeds |

## Edge Cases

Consider the input

```
1
a
```

The algorithm forms `"aa"` by prepending and `"aa"` by appending. Both are palindromes, so it outputs:

```
NO
```

This matches the fact that every insertion produces the same string.

Now consider

```
1
ab
```

The first candidate is `"aab"`.

```
aab ≠ baa
```

so it is not a palindrome. The algorithm immediately outputs

```
YES
aab
```

No additional work is required.

Finally, consider

```
1
aba
```

The candidates are:

```
aaba
abaa
```

Neither string equals its reverse, so the first one is accepted:

```
YES
aaba
```

This confirms that an original palindrome can still have a valid construction.
