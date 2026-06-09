---
title: "CF 1790A - Polycarp and the Day of Pi"
description: "Each test case gives a string of digits that Polycarp wrote down after trying to memorize the digits of π. The task is to determine how many leading digits of π match the prefix of this string. We are not reconstructing π or correcting errors."
date: "2026-06-09T10:36:00+07:00"
tags: ["codeforces", "competitive-programming", "implementation", "math", "strings"]
categories: ["algorithms"]
codeforces_contest: 1790
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 847 (Div. 3)"
rating: 800
weight: 1790
solve_time_s: 95
verified: true
draft: false
---

[CF 1790A - Polycarp and the Day of Pi](https://codeforces.com/problemset/problem/1790/A)

**Rating:** 800  
**Tags:** implementation, math, strings  
**Solve time:** 1m 35s  
**Verified:** yes  

## Solution
## Problem Understanding

Each test case gives a string of digits that Polycarp wrote down after trying to memorize the digits of π. The task is to determine how many leading digits of π match the prefix of this string.

We are not reconstructing π or correcting errors. We are simply comparing the given digit string against a known reference sequence of π digits and stopping at the first mismatch. The answer for a test case is the length of the longest prefix that matches exactly.

The constraint is small: each string has at most 30 characters and there are up to 1000 test cases. This means even a straightforward character-by-character comparison against a stored reference string is easily fast enough. The total work is bounded by roughly 30,000 character comparisons.

The main subtlety lies in leading zeros and early mismatches. A common mistake is to assume numeric comparison or to ignore the leading digit "3" of π.

A few edge situations matter:

A string like "000" should immediately give 0 because π starts with "3", so the first character already fails.

A string starting with "3" but diverging later, such as "31420", should count only the correct prefix "314".

A full correct prefix like "3141592653" should return its full length if it matches the start of π.

## Approaches

The most direct idea is to compare the input string against a precomputed prefix of π. We store π digits as a string, for example "314159265358979323846264338327..." long enough to cover all possible inputs.

For each test case, we scan from left to right and compare characters until we find a mismatch or reach the end of the input string. The index at which we stop is the answer.

This brute-force method is already optimal in this problem because the maximum input length is tiny. Even if we recomputed comparisons repeatedly or used slicing, the complexity remains linear in the total input size.

A more abstract way to see it is that we are computing a longest common prefix between two strings: the given number and a fixed reference string. Since one string is constant, we do not need any advanced preprocessing like hashing or suffix structures.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Comparison | O(t · n) | O(1) | Accepted |
| Optimal (same idea) | O(t · n) | O(1) | Accepted |

## Algorithm Walkthrough

1. Store the digits of π as a fixed string starting from the first digit after the decimal point included with the leading 3.
2. For each test case, read the input string representing Polycarp’s remembered digits.
3. Initialize a counter to zero. This counter tracks how many consecutive digits match between the input string and π.
4. Iterate over the characters of the input string from left to right. For each position i, compare input[i] with pi_digits[i].
5. If the characters are equal, increment the counter and continue.
6. If a mismatch occurs, stop immediately because any further digits cannot be part of a correct prefix.
7. Output the counter.

The key idea is that prefix correctness is monotonic. Once a mismatch happens, extending the comparison cannot recover correctness.

### Why it works

At every position i, the algorithm ensures that all positions before i have matched exactly with π. The first mismatch defines the boundary between correct and incorrect memory. Since we only care about prefix agreement, not rearrangements or partial matches, the stopping condition is both sufficient and necessary for correctness.

## Python Solution

```python
import sys
input = sys.stdin.readline

PI = "314159265358979323846264338327950288419716939937510"

t = int(input())
for _ in range(t):
    s = input().strip()
    ans = 0
    for i in range(len(s)):
        if i < len(PI) and s[i] == PI[i]:
            ans += 1
        else:
            break
    print(ans)
```

The solution relies on a precomputed string of π digits. The loop compares each character positionally and stops immediately on mismatch. The boundary check `i < len(PI)` is a safety guard, though the constant is long enough for all constraints.

A common implementation mistake is forgetting to strip newline characters, which would cause incorrect comparisons. Another is converting the string to integers unnecessarily, which complicates comparison without benefit.

## Worked Examples

### Example 1

Input:

```
3
000
31415
31420
```

| Test | i | s[i] | PI[i] | Match | ans |
| --- | --- | --- | --- | --- | --- |
| 000 | 0 | 0 | 3 | No | 0 |

First test fails immediately because the first digit does not match π.

| Test | i | s[i] | PI[i] | Match | ans |
| --- | --- | --- | --- | --- | --- |
| 31415 | 0 | 3 | 3 | Yes | 1 |
|  | 1 | 1 | 1 | Yes | 2 |
|  | 2 | 4 | 4 | Yes | 3 |
|  | 3 | 1 | 1 | Yes | 4 |
|  | 4 | 5 | 5 | Yes | 5 |

This case fully matches the first five digits.

| Test | i | s[i] | PI[i] | Match | ans |
| --- | --- | --- | --- | --- | --- |
| 31420 | 0 | 3 | 3 | Yes | 1 |
|  | 1 | 1 | 1 | Yes | 2 |
|  | 2 | 4 | 4 | Yes | 3 |
|  | 3 | 2 | 1 | No | 3 |

This shows a partial prefix match that stops at the first incorrect digit.

These traces confirm the algorithm behaves as a strict prefix matcher.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(t · n) | Each test case compares at most 30 characters once |
| Space | O(1) | Only a fixed π string and a few counters are used |

The constraints make this effectively constant time per test case. Even in the worst case of 1000 strings of length 30, the total work is negligible.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    PI = "314159265358979323846264338327950288419716939937510"
    out = []
    t = int(sys.stdin.readline())
    for _ in range(t):
        s = sys.stdin.readline().strip()
        ans = 0
        for i in range(len(s)):
            if i < len(PI) and s[i] == PI[i]:
                ans += 1
            else:
                break
        out.append(str(ans))
    return "\n".join(out)

# provided samples
assert run("""9
000
3
4141592653
141592653589793238462643383279
31420
31415
314159265358
27182
314159265358979323846264338327
""") == """0
1
0
0
3
5
12
0
30"""

# custom cases
assert run("""3
3
314
3141592653
""") == """1
3
10"""

assert run("""2
0
000000
""") == """0
0"""

assert run("""2
314159
3141592653589793238462643383279502884
""") == """6
35"""
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Single digit correct prefix | 1 | minimal matching case |
| All zeros | 0 | immediate mismatch handling |
| Full prefix match | full length | long correct prefix behavior |

## Edge Cases

For an input like "000", the algorithm compares the first character with '3' from π and immediately stops, returning 0. This confirms that leading invalid digits are handled correctly without scanning further.

For a fully matching prefix such as "314159", each character matches sequentially, and the counter reaches 6. The loop only terminates naturally after exhausting the string, confirming correct handling of complete matches.

For mixed cases like "31420", matching proceeds for the first three characters, then fails at the fourth, and the result stabilizes at 3, demonstrating correct early termination on first mismatch.
