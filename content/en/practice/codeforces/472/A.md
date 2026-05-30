---
title: "CF 472A - Design Tutorial: Learn from Math"
description: "We are given a single integer n, where n ≥ 12. The task is to find any two composite numbers whose sum is exactly n. A composite number is an integer greater than 1 that has at least one divisor other than 1 and itself."
date: "2026-05-30T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "math", "number-theory"]
categories: ["algorithms"]
codeforces_contest: 472
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 270"
rating: 800
weight: 472
solve_time_s: 82
verified: true
draft: false
---

[CF 472A - Design Tutorial: Learn from Math](https://codeforces.com/problemset/problem/472/A)

**Rating:** 800  
**Tags:** math, number theory  
**Solve time:** 1m 22s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a single integer `n`, where `n ≥ 12`. The task is to find any two composite numbers whose sum is exactly `n`.

A composite number is an integer greater than 1 that has at least one divisor other than 1 and itself. For example, 4, 6, 8, and 9 are composite, while 2, 3, 5, and 7 are prime.

The input contains only one value, so there is no need to process multiple test cases. The upper bound is `10^6`, which is small enough that even algorithms involving a few million operations are easily fast enough within a one-second time limit.

The interesting part of the problem is not efficiency but finding a guaranteed construction. Since the statement promises that every integer at least 12 can be represented as a sum of two composite numbers, we only need a method that always produces one valid pair.

A common mistake is to focus on primality testing and search exhaustively for a valid decomposition. While that works, it is unnecessary.

One edge case is the smallest allowed value.

For input:

```
12
```

a valid answer is:

```
4 8
```

Both numbers are composite. Any solution must handle this lower boundary correctly.

Another subtle case is an odd value such as:

```
15
```

A decomposition like `4 + 11` is invalid because 11 is prime. The correct output could be:

```
6 9
```

Both numbers are composite.

A careless construction such as always printing `4` and `n - 4` fails for odd numbers. For example, with `n = 15`, it would produce `4 + 11`, which is not allowed.

## Approaches

The most direct approach is brute force. We can try every possible first number `x` from 4 to `n - 4`, let `y = n - x`, and check whether both numbers are composite. A number up to `10^6` can be tested for compositeness in roughly `O(√n)` time.

This approach is correct because it explicitly searches all possible decompositions and returns the first valid one. The problem is that in the worst case we may examine nearly one million candidates, and each candidate may require square-root primality checks. That pushes the complexity toward `O(n√n)`, which is far more work than necessary.

The key observation comes from parity.

If `n` is even, then:

```
4 + (n - 4)
```

always works.

The number 4 is composite. Since `n` is even, `n - 4` is also even. Because `n ≥ 12`, we have `n - 4 ≥ 8`. Every even number greater than 2 is composite or at least not prime? More specifically, every even number at least 4 is composite. Thus both numbers are composite.

If `n` is odd, then:

```
9 + (n - 9)
```

always works.

The number 9 is composite. Since `n` is odd, `n - 9` is even. Because `n ≥ 13` for any odd valid input, we have `n - 9 ≥ 4`. Every even number at least 4 is composite, so the second number is composite as well.

This observation removes all searching. We can construct the answer immediately.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n√n) | O(1) | Too slow and unnecessary |
| Optimal | O(1) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the integer `n`.
2. Check whether `n` is even.
3. If `n` is even, output `4` and `n - 4`.

The first number is composite. The second number is an even integer at least 8, which is also composite.
4. Otherwise, `n` is odd. Output `9` and `n - 9`.

The first number is composite. The second number is an even integer at least 4, which is composite.

### Why it works

The algorithm relies entirely on parity.

For even `n`, the decomposition `4 + (n - 4)` is valid because 4 is composite and `n - 4` is an even number at least 8. Any even integer greater than 2 has a divisor 2, so it is composite.

For odd `n`, the decomposition `9 + (n - 9)` is valid because 9 is composite and `n - 9` is an even number at least 4. Again, every even integer greater than 2 is composite.

One of these two cases always applies, so the algorithm always outputs two composite numbers whose sum is exactly `n`.

## Python Solution

```python
import sys
input = sys.stdin.readline

n = int(input())

if n % 2 == 0:
    print(4, n - 4)
else:
    print(9, n - 9)
```

The program begins by reading the single input value.

The parity of `n` determines which construction to use. For even numbers, the pair `(4, n - 4)` is produced. For odd numbers, the pair `(9, n - 9)` is produced.

The only boundary condition is ensuring the second number remains composite. The constraints guarantee this automatically. For the smallest even input, `n = 12`, the second value is `8`. For the smallest odd input, `n = 13`, the second value is `4`. Both are composite.

No loops, primality tests, or additional data structures are needed.

## Worked Examples

### Example 1

Input:

```
12
```

| n | n % 2 | Output Pair |
| --- | --- | --- |
| 12 | 0 | (4, 8) |

Since 12 is even, the algorithm chooses `4` and `12 - 4 = 8`. Both numbers are composite, and their sum is 12.

### Example 2

Input:

```
15
```

| n | n % 2 | Output Pair |
| --- | --- | --- |
| 15 | 1 | (9, 6) |

Since 15 is odd, the algorithm chooses `9` and `15 - 9 = 6`. Both numbers are composite, and their sum is 15.

This example demonstrates why using `4` for all inputs would fail. The decomposition `4 + 11` would contain a prime number, while `9 + 6` is always valid.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(1) | Only a parity check and arithmetic operations |
| Space | O(1) | Uses a constant amount of memory |

The running time does not depend on the size of `n`. Even for the maximum value `10^6`, the algorithm performs the same fixed number of operations, which is comfortably within the limits.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def solve():
    n = int(input())

    if n % 2 == 0:
        print(4, n - 4)
    else:
        print(9, n - 9)

def run(inp: str) -> str:
    backup_stdin = sys.stdin
    backup_stdout = sys.stdout

    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    global input
    input = sys.stdin.readline

    solve()

    out = sys.stdout.getvalue()

    sys.stdin = backup_stdin
    sys.stdout = backup_stdout

    return out.strip()

# provided sample
assert run("12\n") == "4 8", "sample"

# custom cases
assert run("13\n") == "9 4", "smallest odd valid input"
assert run("14\n") == "4 10", "small even input"
assert run("15\n") == "9 6", "odd input"
assert run("1000000\n") == "4 999996", "maximum constraint"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 13 | 9 4 | Smallest odd valid value |
| 14 | 4 10 | Small even value |
| 15 | 9 6 | Odd-number construction |
| 1000000 | 4 999996 | Maximum constraint |

## Edge Cases

For the minimum input:

```
12
```

the algorithm enters the even branch and outputs:

```
4 8
```

The second number is exactly 8, which is composite. This confirms that the lower boundary works without special handling.

For the smallest odd valid input:

```
13
```

the algorithm enters the odd branch and outputs:

```
9 4
```

Both numbers are composite. This is the smallest case where the `9 + (n - 9)` construction is used.

For an odd value such as:

```
15
```

the algorithm outputs:

```
9 6
```

The second value is an even number greater than 2, so it is composite. This demonstrates why the odd-number construction avoids the pitfall of producing a prime second term.

For the maximum input:

```
1000000
```

the algorithm outputs:

```
4 999996
```

The second number is even and greater than 2, so it is composite. The algorithm performs the same constant amount of work as for any other input.
