---
title: "CF 1342B - Binary Period"
description: "We are given a binary string t and must construct another binary string s. The constructed string must contain t as a subsequence, its length must not exceed 2 The period of a string is the smallest positive integer k such that every character matches the character k positions…"
date: "2026-06-11T15:34:58+07:00"
tags: ["codeforces", "competitive-programming", "constructive-algorithms", "strings"]
categories: ["algorithms"]
codeforces_contest: 1342
codeforces_index: "B"
codeforces_contest_name: "Educational Codeforces Round 86 (Rated for Div. 2)"
rating: 1100
weight: 1342
solve_time_s: 532
verified: false
draft: false
---

[CF 1342B - Binary Period](https://codeforces.com/problemset/problem/1342/B)

**Rating:** 1100  
**Tags:** constructive algorithms, strings  
**Solve time:** 8m 52s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a binary string `t` and must construct another binary string `s`.

The constructed string must contain `t` as a subsequence, its length must not exceed `2 * |t|`, and among all valid choices it must have the smallest possible period.

The period of a string is the smallest positive integer `k` such that every character matches the character `k` positions later whenever both positions exist.

The interesting part of the problem is that we are not trying to minimize the length of `s`. We are trying to minimize its period. Once the minimum achievable period is determined, any string with that period is acceptable.

The constraints are tiny. There are at most 100 test cases and each string has length at most 100. Even quadratic algorithms would be completely fine. The challenge is not performance, it is discovering the correct construction.

A subtle edge case appears when the string contains only one type of character.

For example:

```text
t = "0000"
```

The string itself already has period 1. Any valid answer must have period at least 1, so period 1 is optimal. Returning `"0000"` is correct.

Another important case is when both digits appear.

For example:

```text
t = "110"
```

A careless approach might return `"110"` itself. However `"110"` has period 3, because no smaller period works. We can do better. The string:

```text
1010
```

has period 2 and still contains `"110"` as a subsequence.

The entire problem revolves around understanding when period 1 is possible and when period 2 is the best achievable value.

## Approaches

A brute-force mindset would start by searching through all binary strings of length up to `2|t|`, checking whether `t` is a subsequence and computing the period of each candidate. This is correct in principle because it directly follows the definition.

Unfortunately, even for length 100 the number of binary strings is astronomical. A search space of roughly

```text
2^200
```

is completely infeasible.

The key observation comes from the structure of binary strings with very small periods.

A binary string with period 1 must be entirely zeros or entirely ones.

Therefore period 1 is achievable if and only if `t` itself contains only one distinct character. In that situation we can simply choose `s = t`.

What happens when both `0` and `1` appear?

Period 1 becomes impossible because a period-1 string cannot contain both digits, and every subsequence of such a string also contains only one digit.

The next possible period is 2.

A binary string with period 2 can be written as an alternating sequence:

```text
010101...
```

or

```text
101010...
```

Every binary string is a subsequence of a sufficiently long alternating string. Since the length limit allows up to `2|t|`, we can simply build an alternating string of length exactly `2|t|`.

This immediately gives the smallest possible period.

| Approach | Time Complexity | Space Complexity | Verdict |
|---|---|---|---|
| Brute Force Search | Exponential | Exponential | Too slow |
| Alternating Construction | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Read the string `t`.

2. Check whether all characters are the same.

3. If `t` contains only `0`s or only `1`s, output `t` itself.

   The string already has period 1, and no smaller period exists.

4. Otherwise, build a string by repeating `"01"` exactly `|t|` times.

5. Output the resulting alternating string.

   Its period is 2, which is the smallest possible period once both digits appear.

### Why it works

If `t` contains only one type of character, a period-1 string exists, namely `t` itself. Since period 1 is the minimum possible period, this is optimal.

If `t` contains both `0` and `1`, period 1 is impossible. Any period-1 string consists entirely of a single character, so it cannot contain both digits as a subsequence.

The string

```text
010101...
```

has period 2. Because it alternates forever between the two digits, we can greedily match every character of `t` from left to right. Using `|t|` copies of `"01"` gives length `2|t|`, which is exactly within the allowed limit. Thus `t` is always a subsequence of the constructed string.

Since period 1 is impossible and period 2 is achieved, the construction is optimal.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())

    for _ in range(t):
        s = input().strip()

        if s.count('0') == 0 or s.count('1') == 0:
            print(s)
        else:
            print("01" * len(s))

solve()
```

The solution begins by checking whether one of the two digits is absent.

If every character is identical, the original string is already optimal because it has period 1.

Otherwise we generate `"01" * len(s)`. This creates an alternating string of length exactly `2|s|`, satisfying the length restriction automatically.

No explicit subsequence check is required. The proof above shows that every mixed binary string can be embedded into a sufficiently long alternating sequence.

There are no overflow concerns because the maximum output length is only 200 characters.

## Worked Examples

### Example 1

Input:

```text
01
```

The string contains both digits.

| Step | Value |
|---|---|
| t | 01 |
| Contains both digits? | Yes |
| Construction | "01" * 2 |
| Output | 0101 |

The output has period 2 and clearly contains `"01"` as a subsequence.

### Example 2

Input:

```text
110
```

| Step | Value |
|---|---|
| t | 110 |
| Contains both digits? | Yes |
| Construction | "01" * 3 |
| Output | 010101 |

Subsequence matching:

| Character of t | Matched Position in Output |
|---|---|
| 1 | 2 |
| 1 | 4 |
| 0 | 5 |

Thus `"110"` is a subsequence of `"010101"`.

This example demonstrates why returning the original string is not optimal. `"110"` has period 3, while the constructed answer has period 2.

## Complexity Analysis

| Measure | Complexity | Explanation |
|---|---|---|
| Time | O(n) | Scan the string once and build at most 2n characters |
| Space | O(n) | Store the output string |
| 

The maximum total work is tiny. Even in the largest test case we manipulate strings of length at most 200, so the solution easily fits within the limits.

## Test Cases

```python
import sys
import io

def solve_io(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    out = []

    t = int(input())
    for _ in range(t):
        s = input().strip()

        if s.count('0') == 0 or s.count('1') == 0:
            out.append(s)
        else:
            out.append("01" * len(s))

    return "\n".join(out)

# provided sample
assert solve_io("""4
00
01
111
110
""") == """00
0101
111
010101"""

# minimum size
assert solve_io("""1
0
""") == "0"

# single one
assert solve_io("""1
1
""") == "1"

# mixed string
assert solve_io("""1
10
""") == "0101"

# all zeros
assert solve_io("""1
000000
""") == "000000"

# all ones
assert solve_io("""1
111111
""") == "111111"
```

| Test input | Expected output | What it validates |
|---|---|---|
| `0` | `0` | Minimum length, period 1 |
| `1` | `1` | Minimum length, period 1 |
| `10` | `0101` | Mixed digits require period 2 |
| `000000` | `000000` | All zeros stay unchanged |
| `111111` | `111111` | All ones stay unchanged |

## Edge Cases

Consider:

```text
t = "000"
```

The algorithm detects that there are no `1`s and outputs:

```text
000
```

The period is 1, which is optimal.

Consider:

```text
t = "111"
```

The algorithm outputs:

```text
111
```

Again the period is 1.

Consider:

```text
t = "01"
```

Both digits appear. Period 1 is impossible because no constant string can contain both digits as a subsequence. The algorithm outputs:

```text
0101
```

whose period is 2.

Consider:

```text
t = "101001"
```

Both digits appear, so the algorithm outputs:

```text
010101010101
```

The output length is exactly `2|t| = 12`. By scanning left to right we can match every character of `t`, so it is a valid subsequence. Since period 1 is impossible and period 2 is achieved, the answer is optimal.
