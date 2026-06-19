---
title: "CF 106194A - A + B Problem"
description: "We are given two very large integers, each representing a number written on a separate record card. The task is not to compute the full sum in its entirety, but only to determine the last digit of their sum."
date: "2026-06-19T18:35:30+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 106194
codeforces_index: "A"
codeforces_contest_name: "2025 Winter China Unversity of Geosciences (Wuhan) Freshman Contest"
rating: 0
weight: 106194
solve_time_s: 55
verified: true
draft: false
---

[CF 106194A - A + B Problem](https://codeforces.com/problemset/problem/106194/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 55s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given two very large integers, each representing a number written on a separate record card. The task is not to compute the full sum in its entirety, but only to determine the last digit of their sum. This value is then used as a one-digit access code for a mechanical bookshelf lock.

In more concrete terms, the input consists of two integers $A$ and $B$, each of which can be extremely large, up to $10^{100}$. The output is a single digit, corresponding to $(A + B) \bmod 10$.

The size constraint is the key signal here. Numbers up to $10^{100}$ cannot be stored in standard 64-bit integer types, and even arbitrary-length integer addition would be unnecessary overkill if we only care about the last digit. Any solution that tries to parse the full integers and compute their sum directly using native integer arithmetic will either fail or be unnecessarily heavy.

A subtle edge case arises when thinking about input formatting. Since the numbers can be very large, they may include leading digits far beyond any standard numeric type capacity. For example:

Input:

```
99999999999999999999999999999999999999999999999999 1
```

Correct output:

```
0
```

A naive implementation that attempts conversion to integer types would fail here. Even using big integers, computing the full sum is unnecessary work when only the last digit matters.

Another edge case is when one or both numbers are single-digit values, where the logic should still behave uniformly:

Input:

```
7 8
```

Output:

```
5
```

The simplicity of the output hides the fact that the same logic must work uniformly across all magnitudes.

## Approaches

A brute-force approach would interpret both numbers as full integers, convert them into a big integer type, compute the sum, and then extract the last digit. This is correct conceptually, since the problem reduces to modular arithmetic. However, in languages without arbitrary precision support, this immediately fails due to overflow. Even in languages that support big integers, this approach is wasteful because it processes all digits even though only the last digit matters.

The key observation is that the last digit of a sum depends only on the last digits of the addends. This follows from modular arithmetic:

$$(A + B) \bmod 10 = ((A \bmod 10) + (B \bmod 10)) \bmod 10$$

So instead of parsing the entire numbers, we only need to read their final characters, convert them to integers, and compute their sum modulo 10.

This reduces the problem from arbitrary-length arithmetic to constant-time computation.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force (full big integer addition) | O(n) | O(n) | Accepted but unnecessary |
| Optimal (use last digit only) | O(1) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read both numbers as strings rather than integers. This avoids any risk of overflow and preserves all digits exactly as given. The structure of the problem guarantees that we do not need numeric parsing beyond character inspection.
2. Extract the last character of the first string and convert it into an integer digit. This represents $A \bmod 10$, since the last digit of a decimal number fully determines its remainder modulo 10.
3. Extract the last character of the second string and convert it into an integer digit. This represents $B \bmod 10$ for the same reason.
4. Compute the sum of these two digits.
5. Take the result modulo 10 to handle any carry beyond a single digit, since the output must also be a single digit.
6. Output the resulting digit.

Why it works: decimal representation preserves modular structure with respect to 10, meaning every digit except the last contributes a multiple of 10 and therefore vanishes under modulo 10. The algorithm relies on the invariant that for any integer written in base 10, all prefixes ending before the last digit are divisible by 10, so they do not affect the final remainder.

## Python Solution

```python
import sys
input = sys.stdin.readline

a, b = input().split()

da = ord(a[-1]) - ord('0')
db = ord(b[-1]) - ord('0')

print((da + db) % 10)
```

The solution reads the two values as strings and avoids any numeric conversion beyond single characters. The expression `a[-1]` and `b[-1]` safely accesses the last digit regardless of length. Using `ord(...)-ord('0')` is a fast and explicit way to convert a character digit into an integer without invoking slower parsing routines.

The final modulo operation ensures correctness even when the sum of the two digits exceeds 9, which would otherwise produce a two-digit intermediate result.

## Worked Examples

### Example 1

Input:

```
114514 1919810
```

We track only last digits:

| Step | a[-1] | b[-1] | da | db | da + db | (da + db) % 10 |
| --- | --- | --- | --- | --- | --- | --- |
| Initial | 4 | 0 | 4 | 0 | - | - |
| Computation | - | - | 4 | 0 | 4 | 4 |

Output:

```
4
```

This demonstrates that the entire large numbers are irrelevant beyond their final digit.

### Example 2

Input:

```
99999999999999999999 99999999999999999999
```

| Step | a[-1] | b[-1] | da | db | da + db | (da + db) % 10 |
| --- | --- | --- | --- | --- | --- | --- |
| Initial | 9 | 9 | 9 | 9 | - | - |
| Computation | - | - | 9 | 9 | 18 | 8 |

Output:

```
8
```

This confirms that carry propagation beyond the last digit does not matter for modulo 10.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(1) | Only constant-time character access and arithmetic |
| Space | O(1) | No storage beyond two input strings |

The solution comfortably fits within all constraints since it performs a fixed number of operations regardless of input size, making it optimal even when inputs reach the maximum length of $10^{100}$.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    a, b = sys.stdin.readline().split()
    return str((int(a[-1]) + int(b[-1])) % 10)

assert run("1 1") == "2"
assert run("114514 1919810") == "4"
assert run("0 0") == "0"
assert run("99999999999999999999 1") == "0"
assert run("123456789 987654321") == "0"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 1 | 2 | basic correctness |
| 114514 1919810 | 4 | sample-style large input |
| 0 0 | 0 | minimal boundary case |
| 999...9 1 | 0 | carry across many digits |
| 123456789 987654321 | 0 | symmetric large-digit cancellation |

## Edge Cases

For inputs where both numbers end in 9, the carry could suggest full addition is needed, but the algorithm ignores all higher digits safely.

Input:

```
9 9
```

Execution:

```
da = 9, db = 9
sum = 18
output = 8
```

Even though the true sum is 18, only the last digit is required, and the method directly produces it without computing full addition.

For zero-heavy cases like:

```
0 99999999999999999999
```

Only the last digit of the second number matters:

```
da = 0, db = 9
output = 9
```

The algorithm correctly ignores the long prefix of zeros and large digits because they are irrelevant under modulo 10 arithmetic.
