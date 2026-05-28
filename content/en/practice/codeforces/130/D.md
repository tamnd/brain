---
title: "CF 130D - Exponentiation"
description: "We need to compute the remainder when $a^b$ is divided by $c$. The input gives three integers, one per line. The first value is the base, the second is the exponent, and the third is the modulus. The direct interpretation is straightforward."
date: "2026-05-28T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "*special"]
categories: ["algorithms"]
codeforces_contest: 130
codeforces_index: "D"
codeforces_contest_name: "Unknown Language Round 4"
rating: 1500
weight: 130
solve_time_s: 111
verified: true
draft: false
---

[CF 130D - Exponentiation](https://codeforces.com/problemset/problem/130/D)

**Rating:** 1500  
**Tags:** *special  
**Solve time:** 1m 51s  
**Verified:** yes  

## Solution
## Problem Understanding

We need to compute the remainder when $a^b$ is divided by $c$. The input gives three integers, one per line. The first value is the base, the second is the exponent, and the third is the modulus.

The direct interpretation is straightforward. If the input is:

```
2
5
40
```

then we calculate $2^5 = 32$, and then compute $32 \bmod 40 = 32$.

The constraints are tiny. Every value is between 1 and 100. Even the largest possible exponent is only 100, which means the raw value $100^{100}$ is enormous mathematically, but Python handles arbitrarily large integers automatically. A simple loop multiplying the number 100 times is completely safe within the limits.

Because the exponent is at most 100, even an $O(b)$ solution is trivial in practice. There is no risk of timeout with a straightforward implementation. Still, this problem is a good opportunity to discuss modular exponentiation, because the same idea scales to exponents as large as $10^{18}$.

The main edge case is forgetting to apply the modulus at the correct time. Consider:

```
10
2
7
```

The correct answer is:

```
2
```

because $10^2 = 100$, and $100 \bmod 7 = 2$.

A careless implementation in languages with fixed-size integers could overflow before taking the modulus. Python avoids overflow, but the modular approach is still the mathematically correct technique.

Another subtle case is when the modulus is 1:

```
5
7
1
```

The correct answer is:

```
0
```

Every integer modulo 1 equals 0. Forgetting this property can lead to incorrect assumptions about the result staying positive.

## Approaches

The brute-force approach computes $a^b$ directly by multiplying $a$ by itself $b$ times, then taking the remainder modulo $c$.

For these constraints, that solution is perfectly acceptable. The exponent is at most 100, so the loop performs at most 100 multiplications. Even direct exponentiation using `a ** b` works comfortably in Python.

The weakness of the brute-force method appears when the exponent becomes very large. If $b$ were $10^9$, a loop performing one billion multiplications would be impossible within the time limit.

The key observation is that modular arithmetic allows us to reduce intermediate values immediately:

$$(x \cdot y) \bmod c = ((x \bmod c) \cdot (y \bmod c)) \bmod c$$

This means we never need to store the full value of $a^b$. We can keep every intermediate result smaller than $c$.

From there, binary exponentiation becomes natural. Instead of multiplying $a$ exactly $b$ times, we repeatedly square the base and process the exponent bit by bit. Every step cuts the exponent in half, reducing the complexity from $O(b)$ to $O(\log b)$.

Even though the constraints do not require this optimization, it is the standard and scalable solution.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(b)$ | $O(1)$ | Accepted |
| Optimal | $O(\log b)$ | $O(1)$ | Accepted |

## Algorithm Walkthrough

1. Read the integers `a`, `b`, and `c`.
2. Initialize `result = 1`.

This variable stores the accumulated value of the exponentiation modulo `c`.
3. Reduce the base immediately with `a %= c`.

Any larger multiple of `c` behaves identically under modulo arithmetic, so keeping the base small avoids unnecessary growth.
4. While `b > 0`, process the exponent one bit at a time.
5. If `b` is odd, multiply the current result by the current base:

$$result = (result \cdot a) \bmod c$$

An odd exponent means the current power contributes to the final answer.
6. Square the base:

$$a = (a \cdot a) \bmod c$$

Squaring moves from powers like $a^1$ to $a^2$, then $a^4$, $a^8$, and so on.
7. Divide the exponent by 2 using integer division.

This removes the bit that was just processed.
8. After the loop finishes, print `result`.

### Why it works

At every iteration, the algorithm maintains this invariant:

$$result \cdot a^b \equiv \text{original } a^{\text{original } b} \pmod c$$

When the exponent is odd, one copy of the current base must contribute to the final answer, so we multiply it into `result`. Then we square the base and halve the exponent, which preserves the same mathematical value in a compressed form.

Because the exponent loses one binary digit each iteration, the loop eventually reaches zero. At that moment, all required powers have been incorporated into `result`, so it equals the correct value of $a^b \bmod c$.

## Python Solution

```python
import sys
input = sys.stdin.readline

a = int(input())
b = int(input())
c = int(input())

result = 1
a %= c

while b > 0:
    if b % 2 == 1:
        result = (result * a) % c

    a = (a * a) % c
    b //= 2

print(result)
```

The program starts by reading the three integers from standard input.

The variable `result` begins as 1 because multiplication identities start from 1. The line `a %= c` immediately reduces the base into the valid modular range. This keeps intermediate values small and matches the mathematical property of modular multiplication.

The loop processes the exponent in binary form. When `b` is odd, the lowest binary bit is 1, meaning the current power of `a` must be included in the answer. After that, the base is squared to move to the next power of two.

The line `b //= 2` shifts the exponent right by one bit. This is the heart of binary exponentiation.

The order of operations matters. We must check whether `b` is odd before halving it, otherwise we would lose information about the current bit.

Python integers never overflow, but keeping the modulo inside the loop is still the correct implementation strategy and is essential in languages with fixed-size integer types.

## Worked Examples

### Example 1

Input:

```
2
5
40
```

We want to compute $2^5 \bmod 40$.

| Step | b | result | a |
| --- | --- | --- | --- |
| Start | 5 | 1 | 2 |
| b odd, multiply | 5 | 2 | 2 |
| Square and halve | 2 | 2 | 4 |
| Square and halve | 1 | 2 | 16 |
| b odd, multiply | 1 | 32 | 16 |
| Square and halve | 0 | 32 | 16 |

Final answer:

```
32
```

This trace shows how the algorithm only multiplies into `result` when the current exponent bit is 1. The powers used are $2^1$ and $2^4$, whose product is $2^5$.

### Example 2

Input:

```
10
2
7
```

We want to compute $10^2 \bmod 7$.

| Step | b | result | a |
| --- | --- | --- | --- |
| Start | 2 | 1 | 3 |
| Square and halve | 1 | 1 | 2 |
| b odd, multiply | 1 | 2 | 2 |
| Square and halve | 0 | 2 | 4 |

Final answer:

```
2
```

This example demonstrates why reducing the base early is useful. Since $10 \bmod 7 = 3$, the algorithm never works with unnecessarily large values.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(\log b)$ | The exponent is halved every iteration |
| Space | $O(1)$ | Only a few integer variables are stored |

The exponent is at most 100, so the loop executes only a handful of times. The solution easily fits within the 2 second time limit and 64 MB memory limit.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys, io

def solve():
    input = sys.stdin.readline

    a = int(input())
    b = int(input())
    c = int(input())

    result = 1
    a %= c

    while b > 0:
        if b % 2 == 1:
            result = (result * a) % c

        a = (a * a) % c
        b //= 2

    print(result)

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    out = io.StringIO()
    sys.stdout = out

    solve()

    sys.stdout = sys.__stdout__
    return out.getvalue()

# provided sample
assert run("2\n5\n40\n") == "32\n", "sample 1"

# minimum values
assert run("1\n1\n1\n") == "0\n", "minimum values"

# modulus equals 1
assert run("5\n7\n1\n") == "0\n", "modulo 1"

# all equal values
assert run("7\n7\n7\n") == "0\n", "all equal"

# larger exponent
assert run("3\n10\n13\n") == "3\n", "binary exponentiation correctness"

# maximum bounds
assert run("100\n100\n100\n") == "0\n", "maximum bounds"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 1 1` | `0` | Smallest possible inputs |
| `5 7 1` | `0` | Every number modulo 1 equals 0 |
| `7 7 7` | `0` | Base divisible by modulus |
| `3 10 13` | `3` | Correct handling of repeated squaring |
| `100 100 100` | `0` | Maximum constraints |

## Edge Cases

Consider the case where the modulus is 1:

```
5
7
1
```

The algorithm begins with:

```
a %= c
```

so `a` becomes `0`.

Every multiplication afterward stays `0` modulo `1`. The loop eventually produces:

```
0
```

which is mathematically correct because every integer leaves remainder 0 when divided by 1.

Now consider a case where the base is already divisible by the modulus:

```
7
7
7
```

The line `a %= c` again turns the base into `0`.

The first time the algorithm encounters an odd exponent bit, it computes:

$$result = (1 \cdot 0) \bmod 7 = 0$$

After that, the result can never change. The final answer is:

```
0
```

This demonstrates why reducing the base before entering the loop is both correct and efficient.

Finally, consider:

```
10
2
7
```

A naive implementation might first compute `10 * 10 = 100` and only later apply the modulus. Our algorithm instead reduces immediately:

$$10 \bmod 7 = 3$$

Then it works entirely with small values:

$$3^2 \bmod 7 = 2$$

The output is:

```
2
```

The invariant remains valid because modular multiplication preserves equivalence at every step.
