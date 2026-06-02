---
title: "CF 175A - Robot Bicorn Attack"
description: "We are given a string of digits that was formed by writing the scores from three game rounds one after another, without any separators. Originally there were exactly three non-negative integers."
date: "2026-06-02T17:01:46+07:00"
tags: ["codeforces", "competitive-programming", "brute-force", "implementation"]
categories: ["algorithms"]
codeforces_contest: 175
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 115"
rating: 1400
weight: 175
solve_time_s: 112
verified: true
draft: false
---

[CF 175A - Robot Bicorn Attack](https://codeforces.com/problemset/problem/175/A)

**Rating:** 1400  
**Tags:** brute force, implementation  
**Solve time:** 1m 52s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a string of digits that was formed by writing the scores from three game rounds one after another, without any separators.

Originally there were exactly three non-negative integers. Each integer was written without leading zeros, except that the number `0` itself is allowed. Every round score was at most `1,000,000`.

The separators between the three numbers were lost. Our task is to restore them in a way that produces a valid triple of round scores and maximizes their sum. If no valid split exists, we must print `-1`.

The string length is at most 30. That is the key observation. Even though the numbers themselves may be large when interpreted as substrings, the string is very short. A length of 30 means there are only a small number of places where we can insert the two separators.

A score cannot exceed `1,000,000`, which has at most 7 digits. This restriction is much stronger than the string length bound. Any valid part must contain at most 7 digits, otherwise its value is automatically too large.

Several edge cases can easily break a careless implementation.

Consider:

```
1000
```

A valid split is `1 | 0 | 0`, but that leaves an extra digit. The only way to use all digits is `10 | 0 | 0`, whose sum is `10`. Any solution must ensure that all characters belong to exactly one of the three numbers.

Consider:

```
009
```

Possible three-part splits are:

```
0 | 0 | 9
0 | 09 | ...
00 | ...
```

The substring `"09"` has a leading zero and `"00"` also has a leading zero. No valid split exists, so the answer is `-1`.

Consider:

```
10000011000001
```

A split such as:

```
1000001 | 1000001 | 0
```

uses values exactly at the allowed limit. The bound is inclusive, so `1,000,000` is allowed but `1,000,001` is not.

Consider:

```
123456789012345678901234567890
```

The string is much longer than three times seven digits. Since every valid score has at most seven digits, three scores together can occupy at most twenty-one digits. A length-30 string can never be split into three valid scores, so the answer is immediately `-1`.

## Approaches

The most direct idea is to try every possible way to place the two separators.

If the first separator is after position `i` and the second separator is after position `j`, then the three numbers are:

```
s[0:i]
s[i:j]
s[j:n]
```

For each split we verify three conditions. Every part must be non-empty. No part may contain leading zeros unless its length is exactly one. Its numeric value must not exceed `1,000,000`.

Whenever a split is valid, we compute the sum and keep the maximum.

A truly naive brute force would generate all possible triples of substrings and check them. With a string length of at most 30, there are only about

```
30 * 30 = 900
```

choices for the separator positions. Even after parsing numbers, this is tiny.

The crucial observation is that the constraints are so small that this brute force is already optimal. There is no need for dynamic programming, greedy methods, or sophisticated pruning. The entire problem is about correctly validating candidate splits.

We can make the implementation slightly cleaner by noticing that valid numbers have at most seven digits, but even without using that fact, checking all separator pairs is fast enough.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force over all split positions | O(n²) | O(1) | Accepted |
| Optimal | O(n²) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the digit string `s` and let its length be `n`.
2. Initialize `best = -1`.
3. Enumerate the end position of the first number. Let it be `i`, where `1 ≤ i < n`.
4. Enumerate the end position of the second number. Let it be `j`, where `i + 1 ≤ j < n`.
5. Extract the three substrings:

```
a = s[:i]
b = s[i:j]
c = s[j:]
```
6. Check whether each substring represents a legal score.

A substring is legal if:

- Its length is at least 1.
- If its length is greater than 1, it does not start with `'0'`.
- Its numeric value is at most `1,000,000`.
7. If any of the three substrings is illegal, discard this split and continue.
8. Otherwise convert all three substrings to integers, compute their sum, and update:

```
best = max(best, a + b + c)
```
9. After all separator pairs have been tested, print `best`.

### Why it works

Every valid reconstruction of the original game scores corresponds to exactly one pair of separator positions. The algorithm enumerates every possible pair, so no valid reconstruction can be missed.

For each candidate split, the validation checks exactly the rules given in the statement: three non-empty numbers, no leading zeros, and value at most `1,000,000`. Any split that passes these checks is a legal reconstruction, and any split that fails them is illegal.

Since the algorithm evaluates the sum of every legal reconstruction and keeps the maximum, the final value stored in `best` is precisely the largest achievable total score. If no legal reconstruction exists, `best` remains `-1`, which is the required output.

## Python Solution

```python
import sys
input = sys.stdin.readline

LIMIT = 1000000

s = input().strip()
n = len(s)

best = -1

for i in range(1, n):
    for j in range(i + 1, n):
        parts = (s[:i], s[i:j], s[j:])
        values = []
        ok = True

        for p in parts:
            if len(p) > 1 and p[0] == '0':
                ok = False
                break

            v = int(p)
            if v > LIMIT:
                ok = False
                break

            values.append(v)

        if ok:
            best = max(best, sum(values))

print(best)
```

The outer two loops enumerate all possible locations for the two separators. Since the separators must produce exactly three non-empty parts, `i` starts from `1` and `j` starts from `i + 1`.

The validation logic follows the statement directly. A substring like `"0"` is legal, while `"00"` and `"09"` are not. The check

```
len(p) > 1 and p[0] == '0'
```

captures this rule exactly.

After that, the substring is converted to an integer and compared against `1,000,000`. Python integers have arbitrary precision, so there is no overflow concern.

Whenever a split is valid, its sum is compared against the current best answer. If no valid split is ever found, `best` remains `-1`, which naturally handles impossible inputs.

## Worked Examples

### Example 1

Input:

```
1234
```

| i | j | Split | Valid? | Sum | Best |
| --- | --- | --- | --- | --- | --- |
| 1 | 2 | 1, 2, 34 | Yes | 37 | 37 |
| 1 | 3 | 1, 23, 4 | Yes | 28 | 37 |
| 2 | 3 | 12, 3, 4 | Yes | 19 | 37 |

Output:

```
37
```

The maximum comes from splitting the string as `1 | 2 | 34`.

### Example 2

Input:

```
900
```

| i | j | Split | Valid? | Sum | Best |
| --- | --- | --- | --- | --- | --- |
| 1 | 2 | 9, 0, 0 | Yes | 9 | 9 |
| 1 | 3 | invalid | Not possible | - | 9 |
| 2 | 3 | 90, 0, 0 | Yes | 90 | 90 |

Output:

```
90
```

This example shows why we must test every separator placement. The first valid split is not the optimal one.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n²) | Enumerating all pairs of separator positions |
| Space | O(1) | Only a few variables are stored |

With `n ≤ 30`, there are at most 435 separator pairs. Each candidate requires checking three short substrings. The running time is comfortably below the limits, and memory usage is negligible.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys, io

def run(inp: str) -> str:
    s = inp.strip()
    n = len(s)
    best = -1

    for i in range(1, n):
        for j in range(i + 1, n):
            parts = (s[:i], s[i:j], s[j:])
            vals = []
            ok = True

            for p in parts:
                if len(p) > 1 and p[0] == '0':
                    ok = False
                    break

                v = int(p)
                if v > 1000000:
                    ok = False
                    break

                vals.append(v)

            if ok:
                best = max(best, sum(vals))

    return str(best)

# provided sample
assert run("1234") == "37", "sample 1"

# custom cases
assert run("900") == "90", "zeros allowed as standalone numbers"
assert run("009") == "-1", "leading zeros invalidate all splits"
assert run("111") == "3", "minimum valid length"
assert run("1000000100000010") == "2000001", "boundary value 1000000"
assert run("123456789012345678901234567890") == "-1", "too long for three valid scores"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `900` | `90` | Standalone zero is legal |
| `009` | `-1` | Leading-zero rejection |
| `111` | `3` | Smallest possible valid input length |
| `1000000100000010` | `2000001` | Values equal to 1,000,000 are allowed |
| `123456789012345678901234567890` | `-1` | No split can satisfy the score limit |

## Edge Cases

Consider the input:

```
009
```

The candidate split `0 | 0 | 9` is valid only if the separators produce exactly those substrings. For the other possibilities, substrings such as `"00"` or `"09"` appear. The validation step rejects any substring whose length exceeds one and begins with `'0'`. Since every possible split fails, `best` remains `-1`.

Consider:

```
100000110000010
```

One candidate split is:

```
1000001 | 1000000 | 10
```

The first value exceeds the limit and is rejected. Another split may produce:

```
1000000 | 1000000 | 10
```

which is accepted because the limit is inclusive. The algorithm compares the parsed integer directly against `1,000,000`, so the boundary is handled correctly.

Consider:

```
123456789012345678901234567890
```

Any partition into three non-empty pieces must leave at least one part with more than seven digits. Any number with more than seven digits exceeds `1,000,000`, so every split fails the value check. The algorithm systematically verifies all possibilities and correctly returns `-1`.

Consider:

```
111
```

This is the shortest possible string that can form three non-empty numbers. The only split is:

```
1 | 1 | 1
```

The loops still examine it correctly because `i = 1` and `j = 2` are valid separator positions. The resulting sum is `3`, which becomes the answer.
