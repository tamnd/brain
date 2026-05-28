---
title: "CF 202A - LLPS"
description: "We are given a lowercase string and must choose some characters, in order, to form a subsequence that is both a palindrome and lexicographically as large as possible. A subsequence does not need to stay contiguous."
date: "2026-05-29T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "binary-search", "bitmasks", "brute-force", "greedy", "implementation", "strings"]
categories: ["algorithms"]
codeforces_contest: 202
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 127 (Div. 2)"
rating: 800
weight: 202
solve_time_s: 66
verified: true
draft: false
---

[CF 202A - LLPS](https://codeforces.com/problemset/problem/202/A)

**Rating:** 800  
**Tags:** binary search, bitmasks, brute force, greedy, implementation, strings  
**Solve time:** 1m 6s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a lowercase string and must choose some characters, in order, to form a subsequence that is both a palindrome and lexicographically as large as possible.

A subsequence does not need to stay contiguous. We may skip characters, but the remaining characters must keep their original order.

The string length is at most 10, which is tiny. Even exponential algorithms are technically possible here. A brute-force search over all subsequences would examine at most $2^{10} = 1024$ candidates, which easily fits within the limits.

The interesting part of the problem is not performance, but recognizing the structure hidden inside lexicographic order.

A common mistake is assuming that longer palindromes are always better. Lexicographic order does not work that way. For example:

Input:

```
radar
```

Possible palindromic subsequences include `"radar"` and `"rr"`.

Even though `"radar"` is longer, `"rr"` is lexicographically larger because the first differing character is `'r'` versus `'a'`, and `'r' > 'a'`.

Another easy mistake is trying to build the longest palindromic subsequence first and only then maximize lexicographic order. These are different objectives.

For example:

Input:

```
abac
```

The longest palindromic subsequence is `"aba"`, but the correct answer is:

```
c
```

Lexicographically, any string starting with `'c'` beats every string starting with `'a'`.

One more subtle case appears when the largest character occurs multiple times.

Input:

```
azbz
```

The correct answer is:

```
zz
```

A careless solution might output only `"z"`, but if the maximum character appears several times, taking all of them forms a palindrome automatically and gives a lexicographically larger result because longer equal-prefix strings are larger.

## Approaches

The brute-force approach is straightforward because the input is so small.

We can generate every subsequence using bitmasks. For each subsequence, we check whether it is a palindrome. Among all palindromic subsequences, we keep the lexicographically largest one.

This works because there are only $2^n$ subsequences. With $n \le 10$, that is at most 1024 candidates. Even if we spend $O(n)$ time constructing and checking each subsequence, the total work stays tiny.

The brute-force method is fully acceptable for this problem. Still, there is a much simpler observation.

Suppose the largest character appearing in the string is `'z'`. Any palindrome starting with a smaller character can never beat a palindrome starting with `'z'`, regardless of length.

Now consider all occurrences of this maximum character. If we take every one of them, the resulting string consists entirely of the same letter, which is automatically a palindrome.

For example:

```
abzczz
```

The maximum character is `'z'`, appearing three times. The subsequence `"zzz"` is a palindrome, and no palindrome beginning with a smaller character can beat it lexicographically.

This completely solves the problem:

The answer is simply all occurrences of the maximum character in the string.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(2^n \cdot n) | O(n) | Accepted |
| Optimal | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the input string.
2. Find the maximum character in the string using Python's `max()`.

This character must appear at the beginning of the lexicographically largest palindrome. Any smaller starting character would immediately lose in lexicographic comparison.
3. Traverse the string again and collect every occurrence of that maximum character.

A string made entirely of one repeated character is always a palindrome.
4. Print the resulting string.

### Why it works

Let the maximum character in the string be `c`.

Any palindromic subsequence beginning with a character smaller than `c` is automatically lexicographically smaller than a subsequence beginning with `c`.

So the optimal answer must begin with `c`.

Once the first character is fixed to `c`, adding more copies of `c` only improves the result. If two strings share the same prefix, the longer one is lexicographically larger.

Since all copies of `c` form a valid palindrome, taking every occurrence produces the largest possible answer.

## Python Solution

```python
import sys
input = sys.stdin.readline

s = input().strip()

mx = max(s)

answer = []

for ch in s:
    if ch == mx:
        answer.append(ch)

print("".join(answer))
```

The solution directly follows the observation proved above.

`max(s)` finds the lexicographically largest character appearing in the string.

The second loop gathers every occurrence of that character while preserving order. Since all selected characters are identical, the resulting subsequence is automatically a palindrome.

One subtle point is that we must take all occurrences, not just one. If the maximum character appears multiple times, a longer string of the same repeated character is lexicographically larger.

For example:

```
"zz" > "z"
```

because `"z"` is a prefix of `"zz"`.

Another detail is preserving subsequence order. Iterating left to right naturally keeps the original ordering.

## Worked Examples

### Example 1

Input:

```
radar
```

| Position | Character | Maximum Character | Added to Answer | Current Answer |
| --- | --- | --- | --- | --- |
| 0 | r | r | Yes | r |
| 1 | a | r | No | r |
| 2 | d | r | No | r |
| 3 | a | r | No | r |
| 4 | r | r | Yes | rr |

Output:

```
rr
```

This example shows why lexicographic order dominates palindrome length. `"rr"` beats `"radar"` because the first differing character is larger.

### Example 2

Input:

```
azbz
```

| Position | Character | Maximum Character | Added to Answer | Current Answer |
| --- | --- | --- | --- | --- |
| 0 | a | z | No |  |
| 1 | z | z | Yes | z |
| 2 | b | z | No | z |
| 3 | z | z | Yes | zz |

Output:

```
zz
```

This trace demonstrates why we must include every occurrence of the maximum character. `"zz"` is lexicographically larger than `"z"`.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | One pass to find the maximum character and one pass to collect it |
| Space | O(n) | The answer may contain all characters of the string |

With $n \le 10$, the program runs instantly. Even the brute-force solution would fit easily, but the greedy observation reduces the implementation to a few lines.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys, io

def solve():
    input = sys.stdin.readline

    s = input().strip()

    mx = max(s)

    ans = []

    for ch in s:
        if ch == mx:
            ans.append(ch)

    print("".join(ans))

def run(inp: str) -> str:
    backup_stdin = sys.stdin
    backup_stdout = sys.stdout

    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    solve()

    out = sys.stdout.getvalue().strip()

    sys.stdin = backup_stdin
    sys.stdout = backup_stdout

    return out

# provided sample
assert run("radar\n") == "rr", "sample 1"

# custom cases
assert run("a\n") == "a", "single character"
assert run("aaaaa\n") == "aaaaa", "all equal characters"
assert run("abac\n") == "c", "largest character appears once"
assert run("azbz\n") == "zz", "largest character appears multiple times"
assert run("zyxwvutsrq\n") == "z", "strictly decreasing characters"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `a` | `a` | Minimum-size input |
| `aaaaa` | `aaaaa` | All characters equal |
| `abac` | `c` | Longer palindrome is not always better |
| `azbz` | `zz` | Must take all maximum characters |
| `zyxwvutsrq` | `z` | Maximum character appears once |

## Edge Cases

Consider the input:

```
abac
```

The maximum character is `'c'`. The algorithm scans the string and keeps only `'c'`, producing:

```
c
```

A longest-palindrome algorithm would produce `"aba"`, which is wrong because lexicographically:

```
c > aba
```

The algorithm succeeds because it prioritizes the first character above all else.

Now consider:

```
zzza
```

The maximum character is `'z'`. The algorithm collects every `'z'` and outputs:

```
zzz
```

A careless implementation that returns only one maximum character would produce `"z"`, which is smaller because `"z"` is a prefix of `"zzz"`.

Finally, consider:

```
bacab
```

The maximum character is `'c'`, appearing once. The algorithm outputs:

```
c
```

Even though `"bacab"` itself is a palindrome, it starts with `'b'`, so it loses lexicographically to any palindrome beginning with `'c'`.
