---
title: "CF 1950A - Stair, Peak, or Neither?"
description: "We are given three digits, a, b, and c, and must classify their relationship. A sequence is called a stair when the values strictly increase from left to right, meaning a < b < c."
date: "2026-05-31T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "implementation"]
categories: ["algorithms"]
codeforces_contest: 1950
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 937 (Div. 4)"
rating: 800
weight: 1950
solve_time_s: 64
verified: true
draft: false
---

[CF 1950A - Stair, Peak, or Neither?](https://codeforces.com/problemset/problem/1950/A)

**Rating:** 800  
**Tags:** implementation  
**Solve time:** 1m 4s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given three digits, `a`, `b`, and `c`, and must classify their relationship.

A sequence is called a **stair** when the values strictly increase from left to right, meaning `a < b < c`.

A sequence is called a **peak** when the middle value is strictly larger than both neighbors, meaning `a < b` and `b > c`.

If neither condition is satisfied, we print `"NONE"`.

Each test case contains only three numbers, and there are at most 1000 test cases. Since every classification requires only a few comparisons, the amount of work per test case is constant. Even a straightforward implementation performs only a handful of operations, so efficiency is never a concern.

The main challenge is correctly handling strict inequalities. Equal values do not satisfy either definition.

Consider the input:

```
1
1 1 2
```

The correct answer is:

```
NONE
```

A careless implementation that checks only whether the sequence is non-decreasing might incorrectly classify it as a stair.

Another easy mistake is treating a local maximum as a peak without verifying the left side rises:

```
1
3 2 1
```

The correct answer is:

```
NONE
```

Although `2 > 1`, the condition `3 < 2` is false, so this is not a peak.

A third edge case occurs when all values are equal:

```
1
0 0 0
```

The correct output is:

```
NONE
```

Neither strict increase nor strict peak conditions hold.

## Approaches

The most direct approach is to examine all three numbers and test whether they satisfy the definitions. Since the problem itself defines a stair and a peak using inequalities, we can simply evaluate those inequalities.

A brute-force solution would check every possible pattern and compare the values accordingly. Because each test case contains exactly three digits, this already runs in constant time. Even with 1000 test cases, the total work remains tiny.

The key observation is that there is no hidden structure to discover. The problem is purely an implementation exercise. The definitions can be translated directly into code.

First, check whether `a < b < c`. If true, the answer is `"STAIR"`.

Otherwise, check whether `a < b > c`. If true, the answer is `"PEAK"`.

If neither condition matches, the answer must be `"NONE"`.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(1) per test case | O(1) | Accepted |
| Optimal | O(1) per test case | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the number of test cases.
2. For each test case, read `a`, `b`, and `c`.
3. Check whether `a < b < c`.

This exactly matches the definition of a stair.
4. If the previous condition is false, check whether `a < b > c`.

This exactly matches the definition of a peak.
5. If neither condition is true, output `"NONE"`.

### Why it works

The problem provides complete definitions for both valid classifications.

A sequence is a stair if and only if `a < b < c`. A sequence is a peak if and only if `a < b > c`. These conditions are mutually exclusive because a value cannot simultaneously satisfy `b < c` and `b > c`.

The algorithm tests the stair definition directly, then tests the peak definition directly. Any remaining sequence satisfies neither definition and must be classified as `"NONE"`. Since every possible input falls into exactly one of these cases, the algorithm is correct.

## Python Solution

```python
import sys
input = sys.stdin.readline

t = int(input())

for _ in range(t):
    a, b, c = map(int, input().split())

    if a < b < c:
        print("STAIR")
    elif a < b > c:
        print("PEAK")
    else:
        print("NONE")
```

The first part reads the number of test cases.

For each test case, the three digits are read and stored in `a`, `b`, and `c`.

The condition `a < b < c` uses Python's chained comparison syntax. It is equivalent to checking both `a < b` and `b < c`.

If that condition fails, the code tests `a < b > c`, which is equivalent to checking both `a < b` and `b > c`.

The order matters only because we want to print a single answer. In practice, the two conditions cannot both be true at the same time.

Any case involving equal values automatically falls through to `"NONE"` because both definitions require strict inequalities.

## Worked Examples

### Example 1

Input:

```
1 5 3
```

| a | b | c | a < b < c | a < b > c | Output |
| --- | --- | --- | --- | --- | --- |
| 1 | 5 | 3 | False | True | PEAK |

The sequence rises from `1` to `5` and then falls to `3`. The middle value is strictly larger than both sides, so the answer is `"PEAK"`.

### Example 2

Input:

```
4 5 7
```

| a | b | c | a < b < c | a < b > c | Output |
| --- | --- | --- | --- | --- | --- |
| 4 | 5 | 7 | True | False | STAIR |

The values increase strictly from left to right. This matches the stair definition exactly.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(1) per test case | Only a constant number of comparisons are performed |
| Space | O(1) | No additional data structures are used |

With at most 1000 test cases, the program performs only a few thousand comparisons. This is far below the available limits for both time and memory.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    input = sys.stdin.readline

    t = int(input())
    ans = []

    for _ in range(t):
        a, b, c = map(int, input().split())

        if a < b < c:
            ans.append("STAIR")
        elif a < b > c:
            ans.append("PEAK")
        else:
            ans.append("NONE")

    return "\n".join(ans) + "\n"

# provided sample
assert run(
"""7
1 2 3
3 2 1
1 5 3
3 4 1
0 0 0
4 1 7
4 5 7
"""
) == (
"""STAIR
NONE
PEAK
PEAK
NONE
NONE
STAIR
"""
), "sample 1"

# minimum values
assert run(
"""1
0 0 0
"""
) == (
"""NONE
"""
), "all equal"

# simple stair
assert run(
"""1
0 1 2
"""
) == (
"""STAIR
"""
), "strictly increasing"

# simple peak
assert run(
"""1
0 9 0
"""
) == (
"""PEAK
"""
), "strict peak"

# equality blocks stair and peak
assert run(
"""1
1 1 2
"""
) == (
"""NONE
"""
), "strict inequality required"

# boundary digits
assert run(
"""1
8 9 8
"""
) == (
"""PEAK
"""
), "largest digit in middle"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `0 0 0` | `NONE` | All values equal |
| `0 1 2` | `STAIR` | Strictly increasing sequence |
| `0 9 0` | `PEAK` | Valid peak structure |
| `1 1 2` | `NONE` | Equality does not satisfy strict comparisons |
| `8 9 8` | `PEAK` | Boundary digit values |

## Edge Cases

Consider:

```
1
1 1 2
```

The algorithm checks `1 < 1 < 2`, which is false because `1 < 1` is false. It then checks `1 < 1 > 2`, which is also false. The output is `"NONE"`. This correctly handles equality.

Consider:

```
1
3 2 1
```

The stair condition fails because `3 < 2` is false. The peak condition also fails because `3 < 2` is false. The output becomes `"NONE"`. This prevents incorrectly labeling a decreasing sequence as a peak.

Consider:

```
1
0 0 0
```

Neither `0 < 0 < 0` nor `0 < 0 > 0` is true. The algorithm prints `"NONE"`, which matches the definitions requiring strict inequalities.

Consider:

```
1
2 5 5
```

The stair condition fails because `5 < 5` is false. The peak condition fails because `5 > 5` is false. The result is `"NONE"`. This catches a common mistake where equal neighboring values are accidentally treated as valid.
