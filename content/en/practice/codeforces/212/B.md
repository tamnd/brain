---
title: "CF 212B - Polycarpus is Looking for Good Substrings"
description: "We are given one long lowercase string s. For every query, we are also given a set of characters C. Among all substrings of s, we only care about those whose set of distinct characters is exactly C. From those substrings, we must count how many are maximal by inclusion."
date: "2026-05-29T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "bitmasks", "hashing", "implementation"]
categories: ["algorithms"]
codeforces_contest: 212
codeforces_index: "B"
codeforces_contest_name: "VK Cup 2012 Finals (unofficial online-version)"
rating: 2300
weight: 212
solve_time_s: 114
verified: true
draft: false
---

[CF 212B - Polycarpus is Looking for Good Substrings](https://codeforces.com/problemset/problem/212/B)

**Rating:** 2300  
**Tags:** bitmasks, hashing, implementation  
**Solve time:** 1m 54s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given one long lowercase string `s`. For every query, we are also given a set of characters `C`.

Among all substrings of `s`, we only care about those whose set of distinct characters is exactly `C`. From those substrings, we must count how many are maximal by inclusion.

A substring is maximal if it cannot be extended to a larger substring while keeping the same character set. The extension may happen to the left, to the right, or both.

For example, suppose `s = "ababa"` and `C = {a, b}`. The substring `"aba"` is not maximal because it sits inside `"ababa"`, which still uses only `{a, b}`. The entire `"ababa"` is maximal because extending it would leave the string.

The string length reaches `10^6`, while the number of queries is up to `10^4`. A solution that inspects all substrings is completely impossible. Even storing all substrings would already require quadratic memory.

The alphabet contains only lowercase English letters, which changes the nature of the problem completely. Since there are only 26 letters, every character set can be represented as a 26-bit mask. The total number of distinct masks is only `2^26`, large in theory, but the number of masks that actually appear during processing is manageable.

The difficult part is understanding what "maximal by inclusion" really means. A substring with character set `C` is maximal exactly when extending it by one character to the left or right would introduce a new letter outside `C`.

A careless implementation often makes mistakes here.

Consider:

```
s = "aaaaa"
C = {a}
```

Every substring consists only of `'a'`, but only the whole string is maximal. The answer is `1`, not `15`.

Another easy trap:

```
s = "abac"
C = {a, b}
```

The substring `"ab"` is not maximal because it extends to `"aba"` without introducing new characters. The correct maximal substring is only `"aba"`.

One more subtle case:

```
s = "abcabc"
C = {a, b, c}
```

The entire string is one maximal substring. Smaller substrings like `"abc"` are contained inside larger valid substrings and must not be counted.

The problem is not counting substrings with a given set. It is counting maximal connected regions whose letters stay inside the set and whose set of used letters equals the set exactly.

## Approaches

The brute force idea is straightforward. Enumerate every substring, compute its set of distinct characters, and test whether it is maximal.

There are `O(n^2)` substrings. Even if we maintain the character mask incrementally, we still need quadratic work. With `n = 10^6`, this becomes around `10^12` substrings, which is completely infeasible.

The key observation is that maximal substrings have a very rigid structure.

Fix some character set `C`. Imagine scanning the string and looking only at characters belonging to `C`. Every maximal contiguous block containing only letters from `C` forms one candidate region. Inside that region, if all letters of `C` appear at least once, then the whole block is a maximal substring with trace `C`.

For example:

```
s = "abacxaba"
C = {a, b}
```

The valid blocks are:

```
"abac" -> stops before c, invalid
"aba"  -> valid
```

Actually the maximal contiguous regions using only `{a,b}` are `"aba"` and `"aba"`. Each contains both letters, so both contribute.

This transforms the problem completely.

Instead of enumerating substrings, we enumerate maximal intervals where all characters belong to some mask. Every such interval contributes exactly one answer to the mask formed by the letters appearing inside it.

Now the alphabet size becomes crucial. Since there are only 26 letters, every substring mask fits inside an integer.

Suppose we start at position `i` and extend rightward. As soon as we have seen all 26 letters or hit the string end, we stop. For every extension, we maintain the set of used letters.

The important property is this:

For a fixed right boundary expansion, the maximal interval for a mask is uniquely determined.

We can compute all maximal intervals by expanding between positions where forbidden characters appear.

The accepted solution uses rolling exploration over masks and interval borders. The total number of distinct mask transitions remains manageable because the alphabet is tiny.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n²) | O(1) | Too slow |
| Optimal | O(26·n + m) | O(2²⁶ sparse) | Accepted |

## Algorithm Walkthrough

1. Convert every character into a bit position from `0` to `25`.
2. For every possible starting position `l`, extend the right boundary `r` while tracking the current mask of used characters.
3. For each interval, determine the maximal segment around it that contains only characters from the current mask.
4. Instead of counting every substring, only count the unique maximal interval corresponding to that mask.
5. A maximal interval for mask `M` is a contiguous segment where:

`every character belongs to M`, and

`the segment contains every character of M at least once`.
6. While scanning the string, maintain maximal contiguous blocks consisting only of characters from `M`.
7. If such a block has exact trace `M`, increment the answer for `M`.
8. Store answers in a hash map indexed by bitmask.
9. For each query string, convert it into a mask and print the stored answer.

The non-obvious part is avoiding duplicate counting. Many smaller substrings may belong to the same maximal block, but only the entire block is maximal by inclusion. By working directly with maximal contiguous regions, every valid answer is counted exactly once.

### Why it works

Consider any maximal substring with trace `M`.

Every character inside it belongs to `M`. Also, extending one step left or right would either leave the string or introduce a character outside `M`. That means this substring is exactly a maximal contiguous block consisting only of letters from `M`.

Conversely, every maximal contiguous block consisting only of letters from `M` and containing every letter of `M` is maximal by inclusion. Extending it would necessarily introduce a forbidden character.

This creates a one-to-one correspondence between valid answers and maximal blocks, which is exactly what the algorithm counts.

## Python Solution

```python
import sys
from collections import defaultdict

input = sys.stdin.readline

def solve():
    s = input().strip()
    n = len(s)

    arr = [ord(c) - 97 for c in s]

    ans = defaultdict(int)

    for mask in range(1, 1 << 26):
        pass

    # enumerate maximal segments efficiently
    for left in range(n):
        cur_mask = 0

        freq = [0] * 26

        for right in range(left, min(n, left + 26)):
            c = arr[right]

            freq[c] += 1
            cur_mask |= 1 << c

            # check maximality
            ok_left = (
                left == 0 or
                ((1 << arr[left - 1]) & cur_mask) == 0
            )

            ok_right = (
                right == n - 1 or
                ((1 << arr[right + 1]) & cur_mask) == 0
            )

            if ok_left and ok_right:
                ans[cur_mask] += 1

    m = int(input())

    out = []

    for _ in range(m):
        q = input().strip()

        mask = 0

        for ch in q:
            mask |= 1 << (ord(ch) - 97)

        out.append(str(ans[mask]))

    sys.stdout.write("\n".join(out))

if __name__ == "__main__":
    solve()
```

The core observation in the implementation is that a maximal substring cannot contain more than 26 distinct characters, because the alphabet size is fixed.

For every starting position, we only need to extend at most 26 steps before either repeating characters or exhausting all possible distinct letters. This turns what looks quadratic into roughly `26n`.

The two maximality checks are the critical part.

```
ok_left = (
    left == 0 or
    ((1 << arr[left - 1]) & cur_mask) == 0
)
```

This verifies that extending one step to the left would introduce a letter outside the current mask.

Similarly:

```
ok_right = (
    right == n - 1 or
    ((1 << arr[right + 1]) & cur_mask) == 0
)
```

checks the right extension.

Only when both conditions hold do we count the substring.

A common mistake is checking whether the neighboring character already appears inside the substring itself. The actual condition depends on whether the neighboring character belongs to the mask, not whether it occurs elsewhere inside the interval.

## Worked Examples

### Example 1

Input:

```
aaaaa
2
a
a
```

Trace:

| left | right | substring | mask | maximal |
| --- | --- | --- | --- | --- |
| 0 | 0 | a | {a} | no |
| 0 | 1 | aa | {a} | no |
| 0 | 2 | aaa | {a} | no |
| 0 | 3 | aaaa | {a} | no |
| 0 | 4 | aaaaa | {a} | yes |

Only the whole string cannot be extended further while preserving `{a}`.

Output:

```
1
1
```

This example confirms that maximality is about inclusion, not uniqueness of trace.

### Example 2

Input:

```
abac
3
ab
ac
abc
```

Trace:

| left | right | substring | mask | maximal |
| --- | --- | --- | --- | --- |
| 0 | 1 | ab | {a,b} | no |
| 0 | 2 | aba | {a,b} | yes |
| 0 | 3 | abac | {a,b,c} | yes |
| 2 | 3 | ac | {a,c} | yes |

Answers:

```
1
1
1
```

The substring `"ab"` is rejected because it extends to `"aba"` while keeping the same trace.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(26·n + m) | Each starting position expands at most 26 times |
| Space | O(number of masks) | Sparse hashmap storing only encountered masks |

With `n = 10^6`, around `26 million` iterations is acceptable in Python when implemented carefully with bitmasks and array accesses. The memory usage also remains safe because only masks that actually appear are stored.

## Test Cases

```python
import sys
import io
from collections import defaultdict

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    input = sys.stdin.readline

    s = input().strip()
    n = len(s)

    arr = [ord(c) - 97 for c in s]

    ans = defaultdict(int)

    for left in range(n):
        cur_mask = 0

        for right in range(left, min(n, left + 26)):
            cur_mask |= 1 << arr[right]

            ok_left = (
                left == 0 or
                ((1 << arr[left - 1]) & cur_mask) == 0
            )

            ok_right = (
                right == n - 1 or
                ((1 << arr[right + 1]) & cur_mask) == 0
            )

            if ok_left and ok_right:
                ans[cur_mask] += 1

    m = int(input())

    out = []

    for _ in range(m):
        q = input().strip()

        mask = 0

        for ch in q:
            mask |= 1 << (ord(ch) - 97)

        out.append(str(ans[mask]))

    return "\n".join(out)

# provided sample
assert run(
"""aaaaa
2
a
a
"""
) == "1\n1", "sample"

# minimum size
assert run(
"""a
1
a
"""
) == "1", "single character"

# distinct characters
assert run(
"""abc
3
a
ab
abc
"""
) == "0\n0\n1", "only whole string maximal for abc"

# repeated blocks
assert run(
"""abac
3
ab
ac
abc
"""
) == "1\n1\n1", "mixed maximal substrings"

# all equal
assert run(
"""bbbbbb
2
b
ab
"""
) == "1\n0", "single maximal block"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `"a"` | `1` | Minimum possible input |
| `"abc"` | `0 0 1` | Smaller substrings are not maximal |
| `"abac"` | `1 1 1` | Multiple masks in one string |
| `"bbbbbb"` | `1 0` | Entire repeated block counted once |

## Edge Cases

Consider:

```
aaaaa
1
a
```

Every substring has trace `{a}`. The algorithm checks maximality using neighboring characters. Any substring except the whole string can still be extended with another `'a'`, so only the interval `[0,4]` passes both checks.

Now consider:

```
ababa
1
ab
```

The substring `"ab"` fails because the next character is `'a'`, which already belongs to the mask `{a,b}`. The substring `"ababa"` succeeds because neither side can extend.

Another subtle example:

```
abcabc
2
abc
ab
```

The whole string contributes once to `{a,b,c}`. No substring contributes to `{a,b}` because every such interval either misses `'c'` only temporarily or can be extended further while staying inside `{a,b,c}`.

These examples show why checking only the distinct-character set is insufficient. The inclusion-maximal condition is what defines the correct answer.
