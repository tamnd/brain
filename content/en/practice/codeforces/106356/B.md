---
title: "CF 106356B - Easy Composite"
description: "We are given several prime numbers. For each prime $p$, we may place one or more decimal digits in front of its decimal representation. The resulting number is the concatenation of the chosen prefix and $p$."
date: "2026-06-19T14:56:08+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 106356
codeforces_index: "B"
codeforces_contest_name: "Replay of BUET IUPC 2026, Powered By Phitron"
rating: 0
weight: 106356
solve_time_s: 52
verified: true
draft: false
---

[CF 106356B - Easy Composite](https://codeforces.com/problemset/problem/106356/B)

**Rating:** -  
**Tags:** -  
**Solve time:** 52s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given several prime numbers. For each prime $p$, we may place one or more decimal digits in front of its decimal representation. The resulting number is the concatenation of the chosen prefix and $p$.

Our goal is to produce a prefix that makes the resulting number composite, while using as few prepended digits as possible. If several prefixes of the minimum length work, any of them is acceptable.

The key observation comes from the constraints on $p$. Every input number is a prime between 10 and $10^8$, so $p$ is never equal to 2, 3, or 5. In particular, $p \bmod 3$ is always either 1 or 2.

A careless approach might try many prefixes and test primality of the resulting number. That would work for small inputs, but it completely ignores the structure of the problem.

Consider $p = 11$.

If we prepend the digit 1, we obtain 111. Since $111 = 3 \times 37$, the result is composite.

The answer uses only one prepended digit, so it is already optimal.

Another example is $p = 13$.

Prepending 2 gives 213, and $213 = 3 \times 71$.

Again, one digit is enough.

The most important edge case is realizing that zero prepended digits are not allowed. Even though the original number is prime, we must prepend at least one digit. The minimum possible answer length is therefore 1, not 0.

## Approaches

A brute-force solution would try all one-digit prefixes, then all two-digit prefixes, and so on until a composite number is found. For each candidate, it would construct the concatenated number and run a primality test.

This works because eventually some prefix must produce a composite number. The problem is that primality testing would be repeated many times across up to $10^5$ test cases. Even though the resulting numbers are not extremely large, doing repeated primality checks is unnecessary.

The crucial observation is that we do not actually need to search.

Let $k$ be the number of digits of $p$. If we prepend a single digit $d$, the new number is

$$N = d \cdot 10^k + p.$$

Since $10 \equiv 1 \pmod 3$,

$$10^k \equiv 1 \pmod 3.$$

Thus

$$N \equiv d + p \pmod 3.$$

Because $p$ is a prime greater than 3, $p \bmod 3$ is either 1 or 2.

If $p \bmod 3 = 1$, choose $d = 2$.

Then

$$N \equiv 2 + 1 \equiv 0 \pmod 3.$$

If $p \bmod 3 = 2$, choose $d = 1$.

Then

$$N \equiv 1 + 2 \equiv 0 \pmod 3.$$

The resulting number is divisible by 3 and is larger than 3, so it must be composite.

Since a single digit always works, the minimum possible number of prepended digits is always 1.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | Depends on repeated primality tests | O(1) | Unnecessarily slow |
| Optimal | O(1) per test case | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the prime number $p$.
2. Compute $p \bmod 3$.
3. If $p \bmod 3 = 1$, output the digit `2`.

The concatenated number will be divisible by 3 because $2 + 1 \equiv 0 \pmod 3$.
4. Otherwise, $p \bmod 3 = 2$, so output the digit `1`.

The concatenated number will be divisible by 3 because $1 + 2 \equiv 0 \pmod 3$.

### Why it works

Let $k$ be the number of digits of $p$. After prepending digit $d$, the new number is

$$N = d \cdot 10^k + p.$$

Since $10^k \equiv 1 \pmod 3$,

$$N \equiv d + p \pmod 3.$$

Our choice of $d$ guarantees $d + p \equiv 0 \pmod 3$. Hence $N$ is divisible by 3.

Because $N$ contains at least two digits and is larger than 3, divisibility by 3 implies that $N$ is composite.

A one-digit prefix always exists, and no solution can use fewer than one digit because prepending zero digits is not allowed. Thus the produced answer is always optimal.

## Python Solution

```python
import sys
input = sys.stdin.readline

t = int(input())

for _ in range(t):
    p = int(input())

    if p % 3 == 1:
        print(2)
    else:
        print(1)
```

The solution only uses the residue of $p$ modulo 3.

When $p \equiv 1 \pmod 3$, the digit `2` makes the concatenated number divisible by 3.

When $p \equiv 2 \pmod 3$, the digit `1` does the same.

No construction of the final number is necessary. The number of digits of $p$ never needs to be computed because the congruence

$$10^k \equiv 1 \pmod 3$$

holds for every $k$.

The implementation runs in constant time per test case and avoids all primality testing.

## Worked Examples

### Example 1

Input:

```
1
11
```

| Variable | Value |
| --- | --- |
| p | 11 |
| p % 3 | 2 |
| chosen digit | 1 |

The constructed number would be 111.

| Check | Value |
| --- | --- |
| 111 % 3 | 0 |
| Composite? | Yes |

This example shows the case $p \equiv 2 \pmod 3$. A single digit immediately produces a composite number.

### Example 2

Input:

```
1
13
```

| Variable | Value |
| --- | --- |
| p | 13 |
| p % 3 | 1 |
| chosen digit | 2 |

The constructed number would be 213.

| Check | Value |
| --- | --- |
| 213 % 3 | 0 |
| Composite? | Yes |

This example shows the case $p \equiv 1 \pmod 3$. The same argument works with a different digit.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(1) per test case | Only one modulo operation and one comparison |
| Space | O(1) | No auxiliary data structures |

Even with $10^5$ test cases, the total work is tiny. The solution easily fits within the given limits.

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
        p = int(input())
        ans.append("2" if p % 3 == 1 else "1")

    return "\n".join(ans) + "\n"

# basic examples
assert run("1\n11\n") == "1\n"
assert run("1\n13\n") == "2\n"

# smallest valid prime
assert run("1\n11\n") == "1\n"

# p % 3 = 1
assert run("1\n31\n") == "2\n"

# p % 3 = 2
assert run("1\n17\n") == "1\n"

# multiple test cases
assert run("4\n11\n13\n17\n31\n") == "1\n2\n1\n2\n"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `11` | `1` | Case where $p \equiv 2 \pmod 3$ |
| `13` | `2` | Case where $p \equiv 1 \pmod 3$ |
| `17` | `1` | Another residue-2 prime |
| `31` | `2` | Another residue-1 prime |
| Multiple inputs | Alternating answers | Correct handling of many test cases |

## Edge Cases

Consider the smallest valid prime:

```
1
11
```

The algorithm computes $11 \bmod 3 = 2$ and outputs `1`. The resulting number is 111, which is divisible by 3. Since one digit is used, the answer is optimal.

Consider a prime with $p \equiv 1 \pmod 3$:

```
1
97
```

The algorithm outputs `2`. The constructed number is 297. Since $297 = 3 \times 99$, it is composite. No shorter prefix is possible because at least one digit must be prepended.

Consider a large prime near the upper limit:

```
1
99999989
```

Only $p \bmod 3$ matters. The algorithm still performs a single modulo operation and outputs either `1` or `2`. The size of the prime has no effect on the running time, which remains constant.
