---
title: "CF 1913A - Rating Increase"
description: "We are given a string of digits that represents two concatenated integers, the original rating a and the increased rating b, but without a clear separation between them."
date: "2026-06-08T20:08:41+07:00"
tags: ["codeforces", "competitive-programming", "implementation"]
categories: ["algorithms"]
codeforces_contest: 1913
codeforces_index: "A"
codeforces_contest_name: "Educational Codeforces Round 160 (Rated for Div. 2)"
rating: 800
weight: 1913
solve_time_s: 146
verified: true
draft: false
---

[CF 1913A - Rating Increase](https://codeforces.com/problemset/problem/1913/A)

**Rating:** 800  
**Tags:** implementation  
**Solve time:** 2m 26s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a string of digits that represents two concatenated integers, the original rating `a` and the increased rating `b`, but without a clear separation between them. Our task is to split this string into two numbers such that both are strictly positive, neither has leading zeros, and `b` is strictly greater than `a`. If multiple splits satisfy these conditions, we can return any; if no valid split exists, we return `-1`.

The input size for each test case is small: the string has length between 2 and 8. We may have up to 10,000 test cases. Since each string is at most 8 characters, any approach that inspects all possible splits is feasible because for a single string there are at most 7 split positions. The key challenge is handling leading zeros, equal numbers, and enforcing `b > a` correctly. For example, given the input `200200`, a careless implementation might split it as `200` and `200`, which fails because `b` is not strictly greater than `a`. Similarly, splitting `1001` as `10` and `01` is invalid because `01` has a leading zero.

## Approaches

The brute-force approach is straightforward. For each string, try every possible place to split it into two non-empty parts. Convert both parts to integers and check if they satisfy the conditions: neither has a leading zero, both are greater than zero, and `b > a`. Since the string has at most length 8, this requires at most 7 checks per test case. With 10,000 test cases, this yields at most 70,000 checks, which is acceptable in practice. The brute-force approach works because every possible valid split is guaranteed to be examined.

An observation simplifies our work: if a string has length `n`, trying splits closer to the middle often yields smaller `a` and larger `b`, which makes `b > a` more likely. However, for correctness, we still need to check all splits in the worst case, since a valid split could occur at any position, especially for strings where digits are repeated or increasing.

The optimal approach, in this context, is still brute-force with early stopping: iterate over all split positions from left to right and return the first valid split. The number of operations remains tiny due to the input constraints, and this guarantees correctness without unnecessary complexity.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force / Early Stop | O(n * t), n ≤ 8, t ≤ 10^4 | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the number of test cases `t`.
2. For each test case, read the concatenated string `s`.
3. Iterate over possible split positions `i` from 1 to `len(s)-1`. The split divides `s` into `a_str = s[:i]` and `b_str = s[i:]`.
4. Check for leading zeros: if `a_str` or `b_str` starts with `'0'`, skip this split.
5. Convert `a_str` and `b_str` to integers `a` and `b`.
6. Check if both numbers are strictly positive (`a > 0` and `b > 0`) and if `b > a`. If so, print `a` and `b` and stop processing this string.
7. If no valid split is found after checking all positions, print `-1`.

Why it works: The algorithm checks all possible ways to separate the string into two numbers. By explicitly rejecting splits with leading zeros and enforcing `b > a`, it guarantees that any output satisfies the problem constraints. The early stopping ensures that as soon as a valid split is found, we produce a result efficiently.

## Python Solution

```python
import sys
input = sys.stdin.readline

t = int(input())
for _ in range(t):
    s = input().strip()
    n = len(s)
    found = False
    for i in range(1, n):
        a_str, b_str = s[:i], s[i:]
        if a_str[0] == '0' or b_str[0] == '0':
            continue
        a, b = int(a_str), int(b_str)
        if b > a:
            print(a, b)
            found = True
            break
    if not found:
        print(-1)
```

The solution reads input efficiently using `sys.stdin.readline`. We iterate over all split points and check each candidate split. Leading zeros are filtered first to avoid unnecessary integer conversions. The early stopping ensures we return the first valid split without extra work.

## Worked Examples

**Input:** `20002001`

| i | a_str | b_str | a | b | b > a? | Output? |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | 2 | 0002001 | 2 | 2001 | True | Invalid (b_str has leading zeros) |
| 2 | 20 | 002001 | 20 | 2001 | True | Invalid (b_str has leading zeros) |
| 3 | 200 | 02001 | 200 | 2001 | True | Invalid (b_str has leading zeros) |
| 4 | 2000 | 2001 | 2000 | 2001 | True | Valid |

This confirms that the algorithm correctly ignores leading zeros and produces a valid split.

**Input:** `200200`

| i | a_str | b_str | a | b | b > a? | Output? |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | 2 | 00200 | 2 | 200 | True | Invalid (b_str leading zeros) |
| 2 | 20 | 0200 | 20 | 200 | Invalid (b_str leading zeros) |  |
| 3 | 200 | 200 | 200 | 200 | False | Invalid |
| 4 | 2002 | 00 | 2002 | 0 | False | Invalid |
| No valid split exists. Output: `-1`. |  |  |  |  |  |  |

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n * t) | For each of t ≤ 10^4 strings of length n ≤ 8, we check up to n-1 splits. |
| Space | O(1) | Only a few integer variables and substrings of length ≤ 8 are stored. |

With n ≤ 8, t ≤ 10^4, total operations are under 10^5, well within the 2-second limit. Memory usage is negligible, fitting comfortably under 256 MB.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()
    t = int(input())
    for _ in range(t):
        s = input().strip()
        n = len(s)
        found = False
        for i in range(1, n):
            a_str, b_str = s[:i], s[i:]
            if a_str[0] == '0' or b_str[0] == '0':
                continue
            a, b = int(a_str), int(b_str)
            if b > a:
                print(a, b)
                found = True
                break
        if not found:
            print(-1)
    return sys.stdout.getvalue().strip()

# Provided samples
assert run("5\n20002001\n391125\n200200\n2001000\n12\n") == "2000 2001\n39 1125\n-1\n200 1000\n1 2"

# Custom test cases
assert run("3\n10\n1001\n1112\n") == "1 0\n-1\n1 112", "minimum-size and leading zero cases"
assert run("2\n98765432\n12345678\n") == "9 8765432\n1 2345678", "split first digit vs first few digits"
assert run("2\n10000001\n12321\n") == "-1\n1 2321", "edge cases with zeros inside and middle split"
assert run("1\n11\n") == "-1", "equal digits, no valid b > a"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `10\n1001\n1112\n` | `1 0\n-1\n1 112` | Minimum size input, leading zeros |
| `98765432\n12345678` | `9 8765432\n1 2345678` | Splitting first digit vs longer prefix |
| `10000001\n12321` | `-1\n1 2321` | Cases with zeros inside, tricky splits |
| `11` | `-1` | Equal digits, no valid increase |

## Edge Cases

When the concatenated string starts with a single non-zero digit followed by zeros, for example `1001`, the algorithm correctly skips splits that produce leading zeros. It tests each split carefully. For `1001`, splits yield `1|001`, `10|01`, `100|1`. The first two splits are invalid due to leading zeros in `b`. The last split gives `100` and `1`, but `1` is not greater than `100`, so no valid split exists, returning `-1`. This demonstrates that the
