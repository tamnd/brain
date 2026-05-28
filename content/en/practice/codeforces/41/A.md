---
title: "CF 41A - Translation"
description: "We are given two lowercase strings. The first string is a word in one language, and the second string is supposed to be"
date: "2026-05-28T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "implementation", "strings"]
categories: ["algorithms"]
codeforces_contest: 41
codeforces_index: "A"
codeforces_contest_name: "Codeforces Beta Round 40 (Div. 2)"
rating: 800
weight: 41
solve_time_s: 74
verified: true
draft: false
---

[CF 41A - Translation](https://codeforces.com/problemset/problem/41/A)

**Rating:** 800  
**Tags:** implementation, strings  
**Solve time:** 1m 14s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given two lowercase strings. The first string is a word in one language, and the second string is supposed to be its translation into another language where every word is written backwards.

The task is simply to check whether the second string is exactly the reverse of the first one. If it is, we print `YES`. Otherwise, we print `NO`.

The maximum length of each string is only 100 characters. With such a small limit, even inefficient approaches would run comfortably within the time limit. A solution that scans the strings once is already more than enough. There is no need for advanced data structures or optimization tricks.

The main danger in this problem is not performance, but correctness. A careless implementation can accidentally accept invalid cases.

One easy mistake is forgetting to compare the full reversed string. For example:

```
abc
ab
```

The correct output is:

```
NO
```

The second string is shorter, so it cannot possibly be the reverse of the first. Any implementation that only compares matching positions until one string ends would incorrectly accept this case.

Another common mistake is reversing incorrectly by comparing characters in the same direction. Consider:

```
abc
cba
```

The correct output is:

```
YES
```

If we compare `s[i]` with `t[i]` directly instead of `t[n - 1 - i]`, we would reject a valid translation.

A final edge case is a single-character string:

```
a
a
```

The correct output is:

```
YES
```

A one-character string is equal to its own reverse, so the answer must still be accepted.

## Approaches

The brute-force idea is to manually build the reversed version of the first string. We can iterate from the last character of `s` to the first and append each character into a new string. After constructing the reversed string, we compare it with `t`.

This works because a reversed word is uniquely defined. If every character appears in the opposite order, the translation is correct.

The drawback of this approach is that repeated string concatenation can become inefficient in languages where strings are immutable. Each append may create a new string, which can lead to quadratic behavior in the worst case. With a maximum length of only 100, this still passes easily, but it is not the cleanest implementation.

The key observation is that the problem already matches a built-in operation directly. Instead of rebuilding the reverse manually, we can reverse the string in one step and compare the result immediately.

In Python, `s[::-1]` creates the reversed string. Once we compute it, the problem reduces to a single equality check.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n²) | O(n) | Accepted |
| Optimal | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Read the first string `s`.
2. Read the second string `t`.
3. Reverse `s` using slicing.
4. Compare the reversed string with `t`.
5. If they are equal, print `YES`. Otherwise, print `NO`.

The comparison works because reversing preserves every character while changing only the order. Two strings match exactly if and only if the translation was performed correctly.

### Why it works

The algorithm checks the defining property of the translation directly. A valid translated word must contain exactly the same characters as the original word, but in reverse order.

If `reverse(s) == t`, every position matches the required reversed character, so the translation is correct.

If even one character differs, or the lengths differ, the equality check fails automatically, so the translation is invalid.

## Python Solution

```python
import sys
input = sys.stdin.readline

s = input().strip()
t = input().strip()

if s[::-1] == t:
    print("YES")
else:
    print("NO")
```

The program starts by reading both strings from standard input. Using `.strip()` removes the trailing newline character produced by input reading.

The expression `s[::-1]` creates a reversed copy of the string. Python slicing handles the reversal internally, so we do not need a manual loop.

The equality check compares both length and character order automatically. This avoids subtle bugs where partial matches might incorrectly pass.

The implementation is short because the problem itself is fundamentally simple. The main idea is recognizing that reversing a string is the exact operation required.

## Worked Examples

### Example 1

Input:

```
code
edoc
```

| Step | Value |
| --- | --- |
| Original string `s` | `code` |
| Reversed `s` | `edoc` |
| Target string `t` | `edoc` |
| Comparison result | Equal |
| Output | `YES` |

The reversed version of `code` is exactly `edoc`, so the translation is valid.

### Example 2

Input:

```
hello
ollehh
```

| Step | Value |
| --- | --- |
| Original string `s` | `hello` |
| Reversed `s` | `olleh` |
| Target string `t` | `ollehh` |
| Comparison result | Not equal |
| Output | `NO` |

This example demonstrates that matching prefixes are not enough. The strings must match completely, including length.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Reversing and comparing both scan the string once |
| Space | O(n) | The reversed string is stored temporarily |

The maximum string length is only 100, so this solution easily fits within both the time and memory limits.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys, io

def solve():
    import sys
    input = sys.stdin.readline

    s = input().strip()
    t = input().strip()

    if s[::-1] == t:
        print("YES")
    else:
        print("NO")

def run(inp: str) -> str:
    backup_stdin = sys.stdin
    backup_stdout = sys.stdout

    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    solve()

    output = sys.stdout.getvalue()

    sys.stdin = backup_stdin
    sys.stdout = backup_stdout

    return output.strip()

# provided sample
assert run("code\nedoc\n") == "YES", "sample 1"

# minimum-size input
assert run("a\na\n") == "YES", "single character"

# different lengths
assert run("abc\nab\n") == "NO", "length mismatch"

# same letters but wrong order
assert run("abcd\nabdc\n") == "NO", "incorrect reversal"

# maximum-size style case
s = "a" * 100
t = "a" * 100
assert run(f"{s}\n{t}\n") == "YES", "maximum equal strings"

# palindrome
assert run("level\nlevel\n") == "YES", "palindrome case"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `a / a` | `YES` | Minimum-size input |
| `abc / ab` | `NO` | Length mismatch handling |
| `abcd / abdc` | `NO` | Incorrect character order |
| 100 `'a'` characters | `YES` | Maximum allowed length |
| `level / level` | `YES` | Palindrome remains unchanged when reversed |

## Edge Cases

Consider the case where the strings have different lengths:

```
abc
ab
```

The algorithm computes:

```
reverse("abc") = "cba"
```

Then it compares `"cba"` with `"ab"`.

The strings are different, so the output becomes:

```
NO
```

This confirms that the algorithm does not accidentally accept partial matches.

Now consider a palindrome:

```
level
level
```

The algorithm computes:

```
reverse("level") = "level"
```

Since the reversed string is identical to the original, the comparison succeeds and the output is:

```
YES
```

This verifies that strings equal to their own reverse are handled correctly.

Finally, consider a case where the characters match but the order does not:

```
abcd
abdc
```

The algorithm computes:

```
reverse("abcd") = "dcba"
```

Comparing `"dcba"` with `"abdc"` fails immediately, producing:

```
NO
```

This shows that the solution checks the exact reversed ordering, not just the set of characters.
