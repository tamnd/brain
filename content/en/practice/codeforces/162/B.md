---
title: "CF 162B - Binary notation"
description: "We are given a single positive integer and must print its representation in base 2. In other words, instead of expressing the number as powers of 10, we express it as powers of 2 using only digits 0 and 1."
date: "2026-05-29T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "*special"]
categories: ["algorithms"]
codeforces_contest: 162
codeforces_index: "B"
codeforces_contest_name: "VK Cup 2012 Wild-card Round 1"
rating: 1800
weight: 162
solve_time_s: 80
verified: true
draft: false
---

[CF 162B - Binary notation](https://codeforces.com/problemset/problem/162/B)

**Rating:** 1800  
**Tags:** *special  
**Solve time:** 1m 20s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a single positive integer and must print its representation in base 2. In other words, instead of expressing the number as powers of 10, we express it as powers of 2 using only digits `0` and `1`.

For example, the decimal number `5` becomes `101` because:

$$5 = 1 \cdot 2^2 + 0 \cdot 2^1 + 1 \cdot 2^0$$

The constraint is very small. The value of `n` is at most `10^6`, which means its binary representation contains fewer than 20 bits because:

$$2^{20} = 1,\!048,\!576$$

Even inefficient solutions would run comfortably within the limits. A linear scan over all possible bit positions is already trivial here.

The main source of mistakes is formatting the output correctly. Binary notation must not contain leading zeros.

Consider the input:

```
1
```

The correct output is:

```
1
```

A careless implementation that always prints a fixed number of bits, such as 32 bits, would produce:

```
00000000000000000000000000000001
```

which is wrong.

Another subtle case appears when repeatedly dividing by two. The remainders are generated from least significant bit to most significant bit, so they must be reversed before printing.

For example:

```
6
```

Division sequence:

| Current number | Remainder |
| --- | --- |
| 6 | 0 |
| 3 | 1 |
| 1 | 1 |

Collected bits are `011`, but the correct answer is:

```
110
```

Printing the bits in collection order would silently produce the reversed binary number.

## Approaches

The most direct brute-force idea is to test every power of two and determine whether that bit is present in the number. Since the maximum value is below `2^20`, we could iterate from the highest bit down to zero and print `1` or `0` depending on whether the corresponding power contributes to the number.

This works because every integer has a unique binary decomposition. For each position, we ask whether the remaining value contains that power of two.

Even if we checked all 32 or 64 bit positions, the runtime would still be effectively constant. The problem is not performance, but implementation clarity. We must also carefully skip leading zeros.

Another classic approach repeatedly divides the number by two and records the remainder. Each remainder becomes one binary digit. The first remainder corresponds to the least significant bit, the next remainder to the next bit, and so on.

The reason this works is tied directly to positional notation. When dividing by two:

$$n = 2q + r$$

where `r` is either `0` or `1`. That remainder is exactly the current binary digit.

The division approach is simpler because it naturally extracts the binary representation digit by digit without manually reasoning about powers of two.

Since every division cuts the number roughly in half, the number of iterations equals the number of bits in the answer.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(log n) | O(1) | Accepted |
| Optimal | O(log n) | O(log n) | Accepted |

## Algorithm Walkthrough

1. Read the integer `n`.
2. Create an empty list `bits` to store binary digits.
3. While `n` is greater than zero, compute `n % 2` and append the result to `bits`.

The remainder tells us whether the current least significant bit is `0` or `1`.
4. Replace `n` with `n // 2`.

Integer division removes the least significant binary digit we already processed.
5. After the loop finishes, reverse the collected digits.

The first extracted remainder corresponds to the least significant bit, but binary notation is written from most significant bit to least significant bit.
6. Join the digits into a string and print the result.

### Why it works

Each iteration decomposes the current number into:

$$n = 2q + r$$

where `r` is either `0` or `1`. That remainder is exactly the lowest binary digit of `n`.

After removing that digit with integer division, the same logic applies to the quotient. Repeating this process extracts every binary digit exactly once.

The algorithm stops when the quotient becomes zero, meaning all binary positions have been processed. Reversing the collected digits restores the correct left-to-right order.

## Python Solution

```python
import sys
input = sys.stdin.readline

n = int(input())

bits = []

while n > 0:
    bits.append(str(n % 2))
    n //= 2

bits.reverse()

print("".join(bits))
```

The program starts by reading the integer from standard input.

The `while` loop repeatedly extracts the least significant bit using `n % 2`. Since `% 2` can only produce `0` or `1`, each remainder is a valid binary digit.

After recording the digit, the code performs integer division by two. This discards the processed bit and shifts the number right by one binary position.

The digits are collected in reverse order because the least significant bit appears first during repeated division. Reversing the list before printing restores the correct representation.

Using strings inside the list avoids repeated integer-to-string conversions during joining.

The loop condition `while n > 0` works because the problem guarantees `n` is positive. If zero were allowed, we would need a special case to print `"0"`.

## Worked Examples

### Example 1

Input:

```
5
```

Execution trace:

| Current n | n % 2 | bits after append |
| --- | --- | --- |
| 5 | 1 | [1] |
| 2 | 0 | [1, 0] |
| 1 | 1 | [1, 0, 1] |

After reversing:

| Reversed bits | Output |
| --- | --- |
| [1, 0, 1] | 101 |

This example shows a symmetric binary representation where reversing does not visibly change the sequence. The invariant still holds: every remainder corresponds to the current least significant bit.

### Example 2

Input:

```
6
```

Execution trace:

| Current n | n % 2 | bits after append |
| --- | --- | --- |
| 6 | 0 | [0] |
| 3 | 1 | [0, 1] |
| 1 | 1 | [0, 1, 1] |

After reversing:

| Reversed bits | Output |
| --- | --- |
| [1, 1, 0] | 110 |

This trace demonstrates why reversal is necessary. Without reversing, we would incorrectly print `011`.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(log n) | Each iteration divides the number by 2 |
| Space | O(log n) | The binary representation stores one digit per bit |

The maximum input is below `2^20`, so the loop executes at most 20 times. Both runtime and memory usage are tiny compared to the problem limits.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys, io

def solve():
    import sys
    input = sys.stdin.readline

    n = int(input())

    bits = []

    while n > 0:
        bits.append(str(n % 2))
        n //= 2

    bits.reverse()

    print("".join(bits))

def run(inp: str) -> str:
    backup_stdin = sys.stdin
    backup_stdout = sys.stdout

    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    solve()

    out = sys.stdout.getvalue()

    sys.stdin = backup_stdin
    sys.stdout = backup_stdout

    return out.strip()

# provided sample
assert run("5\n") == "101", "sample 1"

# minimum input
assert run("1\n") == "1", "minimum value"

# power of two
assert run("8\n") == "1000", "single set bit"

# mixed bits
assert run("13\n") == "1101", "general binary conversion"

# maximum constraint region
assert run("1000000\n") == "11110100001001000000", "large value"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1` | `1` | Minimum valid input |
| `8` | `1000` | Correct handling of powers of two |
| `13` | `1101` | General conversion with mixed bits |
| `1000000` | `11110100001001000000` | Large input near the upper bound |

## Edge Cases

The first important edge case is the smallest valid number.

Input:

```
1
```

Execution:

| Current n | n % 2 | bits |
| --- | --- | --- |
| 1 | 1 | [1] |

After reversal, the output remains:

```
1
```

This confirms the algorithm does not introduce leading zeros.

Another subtle case is a power of two.

Input:

```
8
```

Execution:

| Current n | n % 2 | bits |
| --- | --- | --- |
| 8 | 0 | [0] |
| 4 | 0 | [0, 0] |
| 2 | 0 | [0, 0, 0] |
| 1 | 1 | [0, 0, 0, 1] |

After reversal:

```
1000
```

This verifies that trailing zeros in the reversed collection become valid ending zeros in the final binary representation.

A third edge case is a number whose reversed remainder sequence differs visibly from the answer.

Input:

```
6
```

Collected remainders:

```
011
```

After reversal:

```
110
```

This demonstrates why reversing the digit list is necessary for correctness.
