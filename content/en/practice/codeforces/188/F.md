---
title: "CF 188F - Binary Notation"
description: "We are given a single positive integer and must print its representation in base 2. In other words, instead of writing the number using decimal digits from 0 to 9, we must write it using only binary digits, 0 and 1."
date: "2026-05-29T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "*special", "implementation"]
categories: ["algorithms"]
codeforces_contest: 188
codeforces_index: "F"
codeforces_contest_name: "Surprise Language Round 6"
rating: 1400
weight: 188
solve_time_s: 92
verified: true
draft: false
---

[CF 188F - Binary Notation](https://codeforces.com/problemset/problem/188/F)

**Rating:** 1400  
**Tags:** *special, implementation  
**Solve time:** 1m 32s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a single positive integer and must print its representation in base 2. In other words, instead of writing the number using decimal digits from 0 to 9, we must write it using only binary digits, 0 and 1.

For example, the decimal number 5 becomes `101` in binary because:

$$5 = 1 \cdot 2^2 + 0 \cdot 2^1 + 1 \cdot 2^0$$

The input contains only one integer, and the upper bound is $10^6$. That limit is very small for modern computers. Even an algorithm that repeatedly divides the number by 2 will finish almost instantly because the number of binary digits is only about $\log_2(n)$. For $10^6$, that is roughly 20 bits.

The main danger in this problem is not performance, but formatting mistakes.

One common mistake is producing the bits in reverse order. If we repeatedly take `n % 2`, we obtain bits from least significant to most significant. For example:

Input:

```
6
```

If we collect remainders directly, we get `011`, which is reversed. The correct output is:

```
110
```

Another easy mistake is printing leading zeros. Binary notation should start from the highest set bit. For example:

Input:

```
1
```

Correct output:

```
1
```

A careless implementation that pads to a fixed length might print something like `0001`, which is invalid for this problem.

The smallest possible input also matters because some implementations stop immediately when the number becomes zero and accidentally print nothing.

Input:

```
1
```

Correct output:

```
1
```

If the loop condition is written incorrectly, the result may become an empty string.

## Approaches

The most direct approach is to repeatedly test every power of two from large to small and decide whether that power contributes to the number. For each position, we can check whether the corresponding bit is set.

For example, for `13`:

$$13 = 8 + 4 + 1$$

So the bits are:

```
1101
```

This method works because every integer has a unique binary decomposition. Since the maximum value is only $10^6$, even scanning all 20 possible bit positions is trivial.

Another straightforward method repeatedly divides the number by 2. Each remainder becomes the next binary digit. The remainder is either 0 or 1, exactly matching a binary bit.

For `13`:

| Current n | n % 2 | Next n |
| --- | --- | --- |
| 13 | 1 | 6 |
| 6 | 0 | 3 |
| 3 | 1 | 1 |
| 1 | 1 | 0 |

The remainders appear in reverse order, so we reverse them at the end and obtain `1101`.

The key observation is that binary notation is literally built from repeated division by 2. Every division removes the lowest binary digit, and the remainder tells us what that digit was.

Both approaches are fast enough here, but repeated division is simpler and naturally matches the mathematical definition of binary representation.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force over bit positions | O(log n) | O(1) | Accepted |
| Repeated division by 2 | O(log n) | O(log n) | Accepted |

## Algorithm Walkthrough

1. Read the integer `n`.
2. Create an empty list called `bits`.
3. While `n` is greater than 0, compute `n % 2` and append the result to `bits`.

The remainder after division by 2 is always either 0 or 1, which directly gives the current least significant binary digit.
4. Replace `n` with `n // 2`.

Integer division removes the least significant binary digit that we just processed.
5. After the loop finishes, reverse the list of collected bits.

The first remainder corresponds to the lowest bit, so the digits were collected backward.
6. Join the reversed digits into a string and print the result.

### Why it works

At every iteration, the algorithm extracts the least significant binary digit using `n % 2`. Then integer division by 2 shifts the binary representation one position to the right.

This process continues until the number becomes zero, meaning all binary digits have been extracted. Since the remainders are generated from least significant to most significant, reversing them restores the correct order.

Because every integer has a unique binary representation, the constructed string must be correct.

## Python Solution

```python
import sys
input = sys.stdin.readline

n = int(input())

bits = []

while n > 0:
    bits.append(str(n % 2))
    n //= 2

print("".join(reversed(bits)))
```

The program begins by reading the integer from standard input.

The `bits` list stores the binary digits as strings. During each iteration, `n % 2` extracts the current least significant bit. We immediately convert it to a string because the final output is textual.

After extracting the bit, the code updates `n` using integer division by 2. This removes the processed bit from the number.

The digits are collected in reverse order. For example, for `13`, the collected sequence becomes:

```
1, 0, 1, 1
```

Reversing it produces:

```
1, 1, 0, 1
```

Finally, `"".join(...)` concatenates the digits into one binary string.

One subtle detail is the loop condition. The loop runs while `n > 0`. Since the problem guarantees `n >= 1`, the list always receives at least one digit.

## Worked Examples

### Example 1

Input:

```
5
```

| Current n | n % 2 | bits after append |
| --- | --- | --- |
| 5 | 1 | `["1"]` |
| 2 | 0 | `["1", "0"]` |
| 1 | 1 | `["1", "0", "1"]` |

After reversing:

```
101
```

This example shows how remainders are collected from right to left. Reversing restores the proper binary order.

### Example 2

Input:

```
10
```

| Current n | n % 2 | bits after append |
| --- | --- | --- |
| 10 | 0 | `["0"]` |
| 5 | 1 | `["0", "1"]` |
| 2 | 0 | `["0", "1", "0"]` |
| 1 | 1 | `["0", "1", "0", "1"]` |

After reversing:

```
1010
```

This trace demonstrates alternating bits and confirms that integer division correctly removes processed digits one by one.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(log n) | Each iteration divides the number by 2 |
| Space | O(log n) | The binary representation contains O(log n) digits |

For $n \le 10^6$, the binary representation has at most 20 bits. The algorithm performs only a tiny number of operations and easily fits within the time and memory limits.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys, io

def solve():
    input = sys.stdin.readline

    n = int(input())

    bits = []

    while n > 0:
        bits.append(str(n % 2))
        n //= 2

    print("".join(reversed(bits)))

def run(inp: str) -> str:
    backup_stdin = sys.stdin
    backup_stdout = sys.stdout

    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    solve()

    output = sys.stdout.getvalue()

    sys.stdin = backup_stdin
    sys.stdout = backup_stdout

    return output

# provided sample
assert run("5\n") == "101\n", "sample 1"

# minimum input
assert run("1\n") == "1\n", "minimum value"

# power of two
assert run("8\n") == "1000\n", "single set bit"

# alternating bits
assert run("10\n") == "1010\n", "alternating pattern"

# maximum constraint
assert run("1000000\n") == bin(1000000)[2:] + "\n", "maximum constraint"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1` | `1` | Smallest valid input |
| `8` | `1000` | Correct handling of powers of two |
| `10` | `1010` | Proper bit ordering |
| `1000000` | `11110100001001000000` | Maximum constraint handling |

## Edge Cases

The smallest valid number is easy to mishandle if the loop logic is incorrect.

Input:

```
1
```

Execution trace:

| Current n | n % 2 | bits |
| --- | --- | --- |
| 1 | 1 | `["1"]` |

Then `n` becomes `0`, the loop stops, and the output is:

```
1
```

This confirms the algorithm never produces an empty string.

Another important case is a power of two.

Input:

```
8
```

Execution trace:

| Current n | n % 2 | bits |
| --- | --- | --- |
| 8 | 0 | `["0"]` |
| 4 | 0 | `["0", "0"]` |
| 2 | 0 | `["0", "0", "0"]` |
| 1 | 1 | `["0", "0", "0", "1"]` |

After reversing:

```
1000
```

This confirms that leading zeros are not printed. The representation starts from the highest set bit and contains only meaningful digits.

The reversed-order issue also deserves attention.

Input:

```
6
```

Collected remainders:

```
0, 1, 1
```

If printed directly, the result would incorrectly become:

```
011
```

The algorithm reverses the digits first, producing the correct output:

```
110
```
