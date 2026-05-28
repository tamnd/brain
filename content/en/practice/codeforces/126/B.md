---
title: "CF 126B - Password"
description: "We are given a single lowercase string and need to find the longest string that satisfies three conditions at the same time. The chosen string must be a prefix of the original string, a suffix of the original string, and also appear somewhere strictly inside the string."
date: "2026-05-28T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "binary-search", "dp", "hashing", "string-suffix-structures", "strings"]
categories: ["algorithms"]
codeforces_contest: 126
codeforces_index: "B"
codeforces_contest_name: "Codeforces Beta Round 93 (Div. 1 Only)"
rating: 1700
weight: 126
solve_time_s: 124
verified: true
draft: false
---

[CF 126B - Password](https://codeforces.com/problemset/problem/126/B)

**Rating:** 1700  
**Tags:** binary search, dp, hashing, string suffix structures, strings  
**Solve time:** 2m 4s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a single lowercase string and need to find the longest string that satisfies three conditions at the same time.

The chosen string must be a prefix of the original string, a suffix of the original string, and also appear somewhere strictly inside the string. The internal occurrence cannot use the entire prefix or the entire suffix position.

For example, in `fixprefixsuffix`, the string `fix` appears at the beginning, at the end, and also inside the word `prefix`, so it is a valid answer.

The string length can reach one million characters. That immediately rules out anything quadratic. Even an `O(n^2)` algorithm would require around `10^12` operations in the worst case, which is far beyond what fits in two seconds. We need a linear or near-linear solution.

The tricky part is not checking whether a string is both a prefix and suffix. That can be done with standard string techniques. The real difficulty is verifying that the same string also appears somewhere in the middle.

Several edge cases are easy to mishandle.

Consider the input:

```
aaaa
```

The correct answer is:

```
aa
```

The prefix `aaa` is also a suffix, but it does not appear strictly inside the string. Its two occurrences are exactly the prefix and suffix positions. A careless implementation might incorrectly return `aaa`.

Another dangerous case is:

```
abcdabc
```

The prefix `abc` is also the suffix, but there is no middle occurrence. The correct output is:

```
Just a legend
```

An implementation that only checks prefix-suffix equality would fail here.

A minimal case also matters:

```
a
```

No non-empty substring can simultaneously be a proper prefix, proper suffix, and middle substring. The answer must be:

```
Just a legend
```

Repeated-character strings create another subtle situation:

```
aaaaa
```

The correct answer is:

```
aaa
```

The string `aaaa` is both prefix and suffix, but again it does not occur strictly inside. We must distinguish between overlapping occurrences and valid internal occurrences.

## Approaches

The brute-force approach is straightforward. Enumerate every possible prefix of the string. For each prefix, check whether it is also a suffix and whether it appears somewhere in the middle.

Suppose the string length is `n`. There are `n` possible prefixes. Comparing a prefix against the suffix costs up to `O(n)`, and searching for another occurrence inside the string also costs up to `O(n)`. The total complexity becomes `O(n^2)` or worse depending on the search method.

With `n = 10^6`, even `O(n^2)` is completely infeasible.

The key observation is that the problem only cares about borders of the string. A border is a substring that is both a prefix and a suffix. Instead of testing all substrings, we only need to examine borders.

This naturally leads to the prefix function from the Knuth-Morris-Pratt algorithm. The prefix function `pi[i]` stores the length of the longest proper prefix of the string that is also a suffix ending at position `i`.

For the full string, `pi[n - 1]` gives the longest border length. If that border also appears somewhere earlier in the prefix-function array, then it occurs in the middle and is a valid answer.

If not, we can jump to the next smaller border using the prefix-function links themselves. This is the elegant part of KMP: borders form a chain. Instead of recomputing anything, we repeatedly move from one border to the next smaller border in constant time.

This transforms the problem into a linear scan plus a few border jumps, giving `O(n)` complexity.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n²) | O(1) | Too slow |
| Optimal | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Compute the prefix function array `pi` for the entire string.

The prefix function tells us, for every position, the length of the longest border ending there.
2. Look at `pi[n - 1]`.

This value is the length of the longest prefix that is also a suffix of the whole string.
3. Record every prefix-function value that appears before the last position.

We only care about positions `0` through `n - 2` because the final position corresponds to the entire string suffix itself, not a middle occurrence.
4. Let `x = pi[n - 1]`.

This is our current candidate answer length.
5. While `x > 0`, check whether `x` appeared somewhere earlier in the prefix-function array.

If it did, then the prefix of length `x` occurs in the middle, so we have found the longest valid answer.
6. If `x` does not appear earlier, move to the next smaller border using:

```
x = pi[x - 1]
```

This works because the border of a border is also a border.
7. If the loop finishes with `x = 0`, no valid substring exists.

### Why it works

The prefix function captures all border relationships in the string.

Every valid answer must be a border of the full string, so starting from `pi[n - 1]` guarantees we examine candidates from longest to shortest.

If a border length appears somewhere earlier in the prefix-function array, that means the same prefix ended at some internal position, which proves the substring occurs in the middle.

The transition `x = pi[x - 1]` correctly moves to the next possible border because any smaller valid border of the full string must also be a border of the current border.

Since we examine borders in decreasing order, the first valid one is automatically the longest.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    s = input().strip()
    n = len(s)

    pi = [0] * n

    j = 0
    for i in range(1, n):
        while j > 0 and s[i] != s[j]:
            j = pi[j - 1]

        if s[i] == s[j]:
            j += 1

        pi[i] = j

    seen = [False] * (n + 1)

    for i in range(n - 1):
        seen[pi[i]] = True

    x = pi[n - 1]

    while x > 0:
        if seen[x]:
            print(s[:x])
            return
        x = pi[x - 1]

    print("Just a legend")

solve()
```

The first part computes the KMP prefix function in linear time.

The variable `j` stores the current matched prefix length. Whenever characters mismatch, we jump backward using previously computed prefix-function values instead of restarting from zero. This is the reason KMP stays linear.

The `seen` array records which border lengths appeared before the final position. Using a boolean array instead of a set avoids hashing overhead on very large inputs.

The search loop starts from the longest border of the whole string. If that border appeared internally, we immediately print it because we are examining candidates from largest to smallest.

The line:

```
x = pi[x - 1]
```

is the most important transition. It walks through the border chain without recomputing anything.

A common mistake is checking all positions including `n - 1` when filling `seen`. That would incorrectly accept borders that only occur as the full suffix.

Another common off-by-one bug happens with `pi[x - 1]`. The prefix function stores information by ending position, so the border of a prefix of length `x` is found at index `x - 1`.

## Worked Examples

### Example 1

Input:

```
fixprefixsuffix
```

The prefix-function array becomes:

| Index | Character | pi[i] |
| --- | --- | --- |
| 0 | f | 0 |
| 1 | i | 0 |
| 2 | x | 0 |
| 3 | p | 0 |
| 4 | r | 0 |
| 5 | e | 0 |
| 6 | f | 1 |
| 7 | i | 2 |
| 8 | x | 3 |
| 9 | s | 0 |
| 10 | u | 0 |
| 11 | f | 1 |
| 12 | f | 1 |
| 13 | i | 2 |
| 14 | x | 3 |

Now:

| Step | x | seen[x] | Action |
| --- | --- | --- | --- |
| Initial | 3 | True | Output prefix length 3 |

The answer is:

```
fix
```

This trace shows the ideal situation where the longest border already appears in the middle.

### Example 2

Input:

```
abcdabc
```

Prefix-function array:

| Index | Character | pi[i] |
| --- | --- | --- |
| 0 | a | 0 |
| 1 | b | 0 |
| 2 | c | 0 |
| 3 | d | 0 |
| 4 | a | 1 |
| 5 | b | 2 |
| 6 | c | 3 |

Now:

| Step | x | seen[x] | Next x |
| --- | --- | --- | --- |
| Initial | 3 | False | pi[2] = 0 |

No candidate remains, so the output is:

```
Just a legend
```

This demonstrates why checking only prefix and suffix equality is insufficient.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Prefix function computation and border traversal are linear |
| Space | O(n) | Arrays `pi` and `seen` each store `n` integers/booleans |

With `n` up to one million, linear complexity is necessary. The solution performs only a few passes over the string and comfortably fits within both the time and memory limits.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def solve():
    input = sys.stdin.readline

    s = input().strip()
    n = len(s)

    pi = [0] * n

    j = 0
    for i in range(1, n):
        while j > 0 and s[i] != s[j]:
            j = pi[j - 1]

        if s[i] == s[j]:
            j += 1

        pi[i] = j

    seen = [False] * (n + 1)

    for i in range(n - 1):
        seen[pi[i]] = True

    x = pi[n - 1]

    while x > 0:
        if seen[x]:
            print(s[:x])
            return

        x = pi[x - 1]

    print("Just a legend")

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    out = io.StringIO()
    sys.stdout = out

    solve()

    sys.stdout = sys.__stdout__
    return out.getvalue().strip()

# provided sample
assert run("fixprefixsuffix\n") == "fix", "sample 1"

# minimum size
assert run("a\n") == "Just a legend", "single character"

# repeated characters
assert run("aaaaa\n") == "aaa", "overlapping borders"

# border exists but no middle occurrence
assert run("abcdabc\n") == "Just a legend", "no internal occurrence"

# multiple nested borders
assert run("ababa\n") == "a", "fallback to smaller border"

# all equal large-style pattern
assert run("aaaaaaaa\n") == "aaaaaa", "largest valid middle border"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `a` | `Just a legend` | Minimum-size input |
| `aaaaa` | `aaa` | Overlapping occurrences handled correctly |
| `abcdabc` | `Just a legend` | Prefix-suffix alone is insufficient |
| `ababa` | `a` | Correct fallback through border chain |
| `aaaaaaaa` | `aaaaaa` | Deep border hierarchy |

## Edge Cases

Consider the input:

```
aaaa
```

The prefix-function array is:

| Index | Character | pi[i] |
| --- | --- | --- |
| 0 | a | 0 |
| 1 | a | 1 |
| 2 | a | 2 |
| 3 | a | 3 |

The longest border has length `3`, corresponding to `aaa`.

We check whether `3` appears before the last position. It does not. The algorithm falls back to:

```
x = pi[2] = 2
```

Now `2` does appear earlier, so the answer becomes `aa`.

This correctly rejects borders that only occur as prefix and suffix.

Now consider:

```
abcdabc
```

The longest border length is `3`, corresponding to `abc`.

The value `3` never appears before the last position in the prefix-function array, so there is no middle occurrence. The algorithm falls back to `0` and prints:

```
Just a legend
```

This prevents falsely accepting a substring that appears only twice.

Finally, consider:

```
ababa
```

The longest border is `aba`, length `3`.

That border does not occur internally. The algorithm falls back using:

```
x = pi[2] = 1
```

Now the border `a` is valid because it appears multiple times inside the string.

The output becomes:

```
a
```

This example shows why traversing the border chain is necessary. The longest border may fail, while a smaller border still succeeds.
