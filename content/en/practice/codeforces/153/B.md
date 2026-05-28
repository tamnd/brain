---
title: "CF 153B - Binary notation"
description: "We are given a single positive integer and must print its representation in base 2. In other words, we want to express the number as powers of two and output the corresponding sequence of bits."
date: "2026-05-29T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "*special"]
categories: ["algorithms"]
codeforces_contest: 153
codeforces_index: "B"
codeforces_contest_name: "Surprise Language Round 5"
rating: 1800
weight: 153
solve_time_s: 89
verified: true
draft: false
---

[CF 153B - Binary notation](https://codeforces.com/problemset/problem/153/B)

**Rating:** 1800  
**Tags:** *special  
**Solve time:** 1m 29s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a single positive integer and must print its representation in base 2. In other words, we want to express the number as powers of two and output the corresponding sequence of bits.

For example, the decimal number 13 is equal to:

$13 = 1\cdot2^3 + 1\cdot2^2 + 0\cdot2^1 + 1\cdot2^0$

so its binary notation is `1101`.

The limit is very small. The value of `n` is at most one million, which means its binary representation contains at most 20 bits because:

$2^{20}=1048576$

Any reasonable algorithm easily fits within the time limit. Even an approach that repeatedly divides the number by two performs only about 20 iterations.

The tricky part is not performance, it is correctness around formatting.

One common mistake is printing the bits in reverse order. When we repeatedly divide by two, we obtain bits from least significant to most significant. If we print them immediately, the answer becomes reversed.

For example:

Input:

```
5
```

The remainders appear in this order:

| Current n | n % 2 |

|---|---|---|

| 5 | 1 |

| 2 | 0 |

| 1 | 1 |

If we print them directly, we get `101` from bottom to top, not from top to bottom.

Another mistake is producing leading zeros. Binary notation should begin with the highest set bit.

For example:

Input:

```
1
```

Correct output:

```
1
```

A careless fixed-width implementation might print something like `00000001`, which is not allowed.

A third edge case is handling the smallest number correctly. If the loop condition is written incorrectly, the program may produce an empty string for `n = 1`.

Input:

```
1
```

Correct output:

```
1
```

The algorithm must guarantee that at least one bit is printed.

## Approaches

The most direct idea is to simulate the definition of binary notation. Every binary digit tells whether a certain power of two participates in the decomposition of the number.

A brute-force approach checks powers of two from large to small. For each position, we determine whether that power fits into the remaining value. If it does, we output `1` and subtract it. Otherwise, we output `0`.

For example, for `13`:

$13 = 8 + 4 + 0 + 1$

so the bits become `1101`.

This method is correct because binary notation is exactly the decomposition into powers of two. The issue is that we first need to determine the largest relevant power. If implemented naively with repeated exponentiation or scanning many unnecessary positions, the code becomes clumsy for such a simple task.

A cleaner observation comes from how binary numbers are formed. The least significant bit equals the remainder when dividing by two.

$n = 2q + r,\quad r\in\{0,1\}$

The remainder `r` is exactly the current binary digit. After extracting it, we divide the number by two and continue with the quotient.

For example, starting from `13`:

| n | n % 2 | n // 2 |
| --- | --- | --- |
| 13 | 1 | 6 |
| 6 | 0 | 3 |
| 3 | 1 | 1 |
| 1 | 1 | 0 |

The bits appear in reverse order: `1011`. Reversing them gives `1101`.

This approach is optimal because each iteration removes one binary digit. Since a number up to one million has only about 20 bits, the algorithm finishes almost instantly.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(log n) | O(1) | Accepted |
| Optimal | O(log n) | O(log n) | Accepted |

## Algorithm Walkthrough

1. Read the integer `n`.
2. Create an empty list `bits` to store binary digits.
3. While `n > 0`, do the following:

1. Compute `n % 2`.
2. Append this remainder to `bits`.
3. Replace `n` with `n // 2`.

The remainder gives the current least significant binary digit. Integer division removes that digit and shifts the number right by one bit.
4. Reverse the list `bits`.

The digits were generated from least significant to most significant, so reversing restores the proper order.
5. Join the digits into a string and print the result.

### Why it works

At every iteration, the algorithm maintains the invariant that the original number can be reconstructed from the collected remainders and the current value of `n`.

Suppose the current value is `n`. We write:

$n = 2\left\lfloor\frac{n}{2}\right\rfloor + (n\bmod 2)$

The remainder is always either `0` or `1`, which matches a binary digit exactly. After recording this digit, we continue with the quotient. Repeating this process extracts every binary digit from right to left. Reversing the collected digits restores the standard left-to-right binary notation.

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

The list `bits` stores the binary digits as strings. Storing them as strings immediately avoids an extra conversion step during output construction.

Inside the loop, `n % 2` extracts the current least significant bit. Then `n //= 2` removes that bit from the number. The loop continues until the number becomes zero.

The order of operations matters. We must record the remainder before dividing. Reversing these two lines would lose the current bit.

After the loop, the digits are reversed because they were collected from right to left. Finally, `"".join(bits)` constructs the output efficiently.

The condition `while n > 0` works correctly because the problem guarantees `n ≥ 1`. If zero were allowed, we would need special handling since the loop would never execute.

## Worked Examples

### Example 1

Input:

```
5
```

| Current n | n % 2 | bits after append |
| --- | --- | --- |
| 5 | 1 | [1] |
| 2 | 0 | [1, 0] |
| 1 | 1 | [1, 0, 1] |

After reversing:

| bits |
| --- |
| [1, 0, 1] |

Output:

```
101
```

This example shows that the digits are naturally generated from least significant to most significant. Reversing restores the correct order.

### Example 2

Input:

```
13
```

| Current n | n % 2 | bits after append |
| --- | --- | --- |
| 13 | 1 | [1] |
| 6 | 0 | [1, 0] |
| 3 | 1 | [1, 0, 1] |
| 1 | 1 | [1, 0, 1, 1] |

After reversing:

| bits |
| --- |
| [1, 1, 0, 1] |

Output:

```
1101
```

This trace demonstrates the decomposition into powers of two:

$13 = 1\cdot2^3 + 1\cdot2^2 + 0\cdot2^1 + 1\cdot2^0$

The algorithm extracts exactly these coefficients.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(log n) | Each iteration divides the number by 2 |
| Space | O(log n) | The binary representation contains O(log n) digits |

Since `n ≤ 10^6`, the loop runs at most about 20 times. Both the running time and memory usage are tiny compared to the contest limits.

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

    return out

# provided sample
assert run("5\n") == "101\n", "sample 1"

# minimum value
assert run("1\n") == "1\n", "minimum input"

# power of two
assert run("8\n") == "1000\n", "single leading 1"

# alternating bits
assert run("10\n") == "1010\n", "checks ordering of bits"

# maximum constraint neighborhood
assert run("1000000\n") == bin(1000000)[2:] + "\n", "large input"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1` | `1` | Smallest valid input |
| `8` | `1000` | Correct handling of powers of two |
| `10` | `1010` | Digits must appear in the correct order |
| `1000000` | `11110100001001000000` | Large input near the constraint limit |

## Edge Cases

Consider the smallest possible input:

Input:

```
1
```

Execution trace:

| Current n | n % 2 | bits |
| --- | --- | --- |
| 1 | 1 | [1] |

After division, `n` becomes `0`, so the loop stops. Reversing a single-element list changes nothing, and the output becomes:

```
1
```

This confirms the algorithm never produces an empty string.

Now consider a power of two:

Input:

```
8
```

Execution trace:

| Current n | n % 2 | bits |
| --- | --- | --- |
| 8 | 0 | [0] |
| 4 | 0 | [0, 0] |
| 2 | 0 | [0, 0, 0] |
| 1 | 1 | [0, 0, 0, 1] |

After reversing:

| bits |
| --- |
| [1, 0, 0, 0] |

Output:

```
1000
```

This verifies that leading zeros are not introduced. The representation begins exactly at the highest set bit.

Finally, consider a number whose bits alternate:

Input:

```
10
```

Execution trace:

| Current n | n % 2 | bits |
| --- | --- | --- |
| 10 | 0 | [0] |
| 5 | 1 | [0, 1] |
| 2 | 0 | [0, 1, 0] |
| 1 | 1 | [0, 1, 0, 1] |

Reversing produces `1010`.

This catches the common mistake of printing remainders immediately without reversing them.
