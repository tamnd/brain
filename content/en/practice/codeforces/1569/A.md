---
title: "CF 1569A - Balanced Substring"
description: "We are given a binary string consisting only of the characters a and b. For each test case, we must find any contiguous segment whose number of a characters is exactly equal to its number of b characters."
date: "2026-06-10T11:36:40+07:00"
tags: ["codeforces", "competitive-programming", "implementation"]
categories: ["algorithms"]
codeforces_contest: 1569
codeforces_index: "A"
codeforces_contest_name: "Educational Codeforces Round 113 (Rated for Div. 2)"
rating: 800
weight: 1569
solve_time_s: 167
verified: false
draft: false
---

[CF 1569A - Balanced Substring](https://codeforces.com/problemset/problem/1569/A)

**Rating:** 800  
**Tags:** implementation  
**Solve time:** 2m 47s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a binary string consisting only of the characters `a` and `b`. For each test case, we must find any contiguous segment whose number of `a` characters is exactly equal to its number of `b` characters.

The output is not asking for the longest balanced substring or the number of balanced substrings. Any valid answer is acceptable. If no balanced substring exists, we print `-1 -1`.

The constraints are extremely small. Each string has length at most 50, and there can be at most 1000 test cases. Even an algorithm that checks every possible substring would comfortably fit within the time limit because there are only about 2500 substrings in a length-50 string.

The interesting part of the problem is that a much simpler observation exists.

Consider a string of length 1.

```
a
```

No non-empty substring can be balanced because every substring contains only one character. The correct answer is `-1 -1`.

A common mistake is to assume that every string contains a balanced substring of length at least 2.

Consider a string where all characters are identical.

```
aaaaa
```

Every substring contains only `a`, so none can have equal counts of `a` and `b`. The correct answer is `-1 -1`.

A careless implementation might search only for even-length substrings and incorrectly assume one must exist.

Another subtle case is a string such as:

```
aba
```

The whole string is not balanced because it contains two `a` and one `b`. However, the substring `"ab"` is balanced. Since the problem accepts any balanced substring, we should stop as soon as we find one.

## Approaches

The brute-force solution is straightforward. Enumerate every pair `(l, r)`, count the number of `a` and `b` inside that substring, and check whether the counts match. Since there are `O(n²)` substrings and counting characters naively takes `O(n)` time, the total complexity is `O(n³)`.

With `n ≤ 50`, even `50³ = 125000` operations per test case is perfectly manageable. So brute force would already be accepted.

The real trick comes from looking at the smallest possible balanced substring.

A balanced substring must contain the same number of `a` and `b`. The shortest non-empty balanced substring has length 2, and its only possible forms are:

```
ab
ba
```

Now suppose a balanced substring exists somewhere in the string. Let us examine its first two characters that differ. Since the string contains only `a` and `b`, any adjacent unequal pair is either `"ab"` or `"ba"`, which is already balanced.

This means we never need to search for long substrings. We only need to find two neighboring characters that are different.

If such a pair exists at positions `i` and `i+1`, then substring `[i, i+1]` is balanced and can be returned immediately.

If every adjacent pair is equal, the entire string consists of only one repeated character. In that situation no balanced substring can exist.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n³) | O(1) | Accepted |
| Optimal | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the string.
2. Scan all adjacent pairs of characters.
3. For each position `i`, check whether `s[i] != s[i + 1]`.
4. If such a pair is found, output `i + 1` and `i + 2` using 1-based indexing.
5. Stop processing the current test case immediately because `"ab"` and `"ba"` are both balanced substrings.
6. If the scan finishes without finding any differing adjacent characters, output `-1 -1`.

The reason step 6 is correct is that a binary string with no adjacent differing characters must be entirely composed of the same character. Such a string cannot contain equal numbers of `a` and `b` in any non-empty substring.

### Why it works

The key property is that every adjacent unequal pair forms a balanced substring of length 2.

If the algorithm returns positions `(i, i+1)`, the substring is either `"ab"` or `"ba"`. Both contain one `a` and one `b`, so the answer is valid.

If the algorithm finds no adjacent unequal pair, then every character in the string is identical. Every non-empty substring also consists of identical characters, so it cannot contain both `a` and `b`. Hence no balanced substring exists.

The algorithm can never output an invalid substring, and it can never miss an existing balanced substring.

## Python Solution

```python
import sys
input = sys.stdin.readline

t = int(input())

for _ in range(t):
    n = int(input())
    s = input().strip()

    found = False

    for i in range(n - 1):
        if s[i] != s[i + 1]:
            print(i + 1, i + 2)
            found = True
            break

    if not found:
        print(-1, -1)
```

The implementation follows the observation directly.

The loop examines every adjacent pair once. When two neighboring characters differ, the corresponding length-2 substring is balanced, so the answer is printed immediately.

The indices inside the string are 0-based, but the problem expects 1-based positions. That is why the output uses `i + 1` and `i + 2`.

The variable `found` tracks whether a valid substring has already been reported. If the loop finishes without setting it to `True`, the string contains only one repeated character and the answer must be `-1 -1`.

There are no overflow concerns because the algorithm performs only simple index operations.

## Worked Examples

### Example 1

Input string:

```
abbaba
```

| i | s[i] | s[i+1] | Different? | Action |
| --- | --- | --- | --- | --- |
| 0 | a | b | Yes | Output 1 2 |

The first adjacent pair is `"ab"`, which contains one `a` and one `b`. The algorithm immediately returns positions `(1, 2)`.

This example shows that we do not need to search for longer balanced substrings. The first valid pair is already enough.

### Example 2

Input string:

```
aaaaa
```

| i | s[i] | s[i+1] | Different? | Action |
| --- | --- | --- | --- | --- |
| 0 | a | a | No | Continue |
| 1 | a | a | No | Continue |
| 2 | a | a | No | Continue |
| 3 | a | a | No | Continue |

No differing adjacent pair is found.

Output:

```
-1 -1
```

This trace demonstrates the case where the entire string is made of one character. Since every substring also contains only `a`, no balanced substring exists.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | One scan through the string |
| Space | O(1) | Only a few variables are used |

With `n ≤ 50`, the algorithm performs at most 49 comparisons per test case. Even with 1000 test cases, the total work is tiny compared to the limits.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    input = sys.stdin.readline
    t = int(input())
    out = []

    for _ in range(t):
        n = int(input())
        s = input().strip()

        found = False

        for i in range(n - 1):
            if s[i] != s[i + 1]:
                out.append(f"{i + 1} {i + 2}")
                found = True
                break

        if not found:
            out.append("-1 -1")

    return "\n".join(out)

# provided sample
assert run(
"""4
1
a
6
abbaba
6
abbaba
9
babbabbaa
"""
) == """-1 -1
1 2
1 2
1 2""", "sample"

# minimum size, no answer
assert run(
"""1
1
b
"""
) == "-1 -1", "single character"

# smallest balanced substring
assert run(
"""1
2
ab
"""
) == "1 2", "length two balanced"

# all equal characters
assert run(
"""1
5
aaaaa
"""
) == "-1 -1", "all a"

# difference appears at the end
assert run(
"""1
5
aaaab
"""
) == "4 5", "boundary pair"

# maximum length style case
assert run(
"""1
50
aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaab
"""
) == "49 50", "near maximum length"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `b` | `-1 -1` | Minimum length string |
| `ab` | `1 2` | Smallest possible balanced substring |
| `aaaaa` | `-1 -1` | All characters identical |
| `aaaab` | `4 5` | Adjacent differing pair at the end |
| `a...ab` (length 50) | `49 50` | Boundary handling near maximum size |

## Edge Cases

Consider the input:

```
1
a
```

The loop over adjacent pairs never executes because there is no pair of neighboring characters. The algorithm reaches the end and prints `-1 -1`. This is correct because a single character cannot contain equal counts of `a` and `b`.

Consider the input:

```
5
aaaaa
```

The scan checks `(a,a)` four times. Every comparison is equal, so no answer is found. The algorithm prints `-1 -1`. Every substring contains only `a`, so no balanced substring exists.

Consider the input:

```
3
aba
```

At `i = 0`, the algorithm compares `a` and `b`. They differ, so it outputs `1 2`. The substring `"ab"` contains one `a` and one `b`, making it balanced. The fact that the whole string is not balanced does not matter because any valid balanced substring is acceptable.

Consider the input:

```
5
bbbba
```

The first three adjacent pairs are `(b,b)`. At `i = 3`, the pair is `(b,a)`, which differs. The algorithm outputs `4 5`. The substring `"ba"` is balanced, so the answer is correct. This case confirms that pairs near the end of the string are handled correctly.
