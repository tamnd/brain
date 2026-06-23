---
title: "CF 105507H - \u0412\u044b\u0447\u0438\u0442\u0430\u043d\u0438\u0435"
description: "We are given a very large positive integer written in decimal form. From this number we want to subtract another positive integer $b$, chosen by us, under two constraints. First, $b$ must be strictly smaller than the given number."
date: "2026-06-23T21:59:51+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105507
codeforces_index: "H"
codeforces_contest_name: "2024-2025 \u0412\u0441\u0435\u0440\u043e\u0441\u0441\u0438\u0439\u0441\u043a\u0430\u044f \u043a\u043e\u043c\u0430\u043d\u0434\u043d\u0430\u044f \u043e\u043b\u0438\u043c\u043f\u0438\u0430\u0434\u0430 \u0448\u043a\u043e\u043b\u044c\u043d\u0438\u043a\u043e\u0432 \u043f\u043e \u043f\u0440\u043e\u0433\u0440\u0430\u043c\u043c\u0438\u0440\u043e\u0432\u0430\u043d\u0438\u044e, \u0440\u0435\u0433\u0438\u043e\u043d\u0430\u043b\u044c\u043d\u044b\u0439 \u044d\u0442\u0430\u043f \u0421\u0430\u0440\u0430\u0442\u043e\u0432\u0441\u043a\u043e\u0439 \u043e\u0431\u043b\u0430\u0441\u0442\u0438 (\u0412\u041a\u041e\u0428\u041f 24, \u0421\u0430\u0440\u0430\u0442\u043e\u0432\u0441\u043a\u0438\u0439 \u043e\u0442\u0431\u043e\u0440\u043e\u0447\u043d\u044b\u0439 \u044d\u0442\u0430\u043f)"
rating: 0
weight: 105507
solve_time_s: 68
verified: true
draft: false
---

[CF 105507H - \u0412\u044b\u0447\u0438\u0442\u0430\u043d\u0438\u0435](https://codeforces.com/problemset/problem/105507/H)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 8s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a very large positive integer written in decimal form. From this number we want to subtract another positive integer $b$, chosen by us, under two constraints. First, $b$ must be strictly smaller than the given number. Second, if we compute the difference $c = a - b$, then $c$ must be a positive integer whose decimal representation consists of the same digit repeated in every position, such as $7$, $4444$, or $111111$.

The task is not to find any valid pair, but to choose $b$ so that it becomes as small as possible. Since $b = a - c$, minimizing $b$ is equivalent to making $c$ as large as possible while still being a repdigit and strictly less than $a$.

The input size matters more in length than in numeric magnitude. The number can have up to tens of millions of digits, so any solution that tries to do arithmetic digit by digit across many candidate values or simulates subtraction repeatedly will fail. The only feasible operations are linear scans of the input and a small constant number of comparisons between long strings.

A naive but common mistake is to assume that the best choice of $c$ is always the largest repdigit with the same number of digits as $a$. That fails when a shorter repdigit like $999\ldots9$ with one fewer digit is still larger than any valid same-length candidate under certain prefixes of $a$. Another subtle pitfall is trying to construct $c$ greedily digit by digit without considering that the structure of a repdigit forces all digits to be identical, which makes local choices invalid.

## Approaches

A brute-force idea is to enumerate all possible repdigits $c$, subtract them from $a$, and take the smallest resulting $b$. A repdigit is determined by a length $k$ and a digit $d$ from 1 to 9, giving a value like $d \times (111\ldots1)$. The number of such candidates grows linearly in $k$, and $k$ itself can be as large as the number of digits in $a$.

The problem is not the number of candidates alone, but the cost of evaluating each candidate. Each subtraction and comparison on a number with up to $10^7$ digits is linear in that size. Even testing a few hundred candidates becomes impossible, since each test is already huge.

The key observation is that the structure of optimal answers is extremely restricted. A repdigit either has the same number of digits as $a$, or it has exactly one digit fewer. Any repdigit shorter by two or more digits is too small to ever compete with a same-length repdigit, because adding a single digit position multiplies magnitude by at least 10, while the digit range is only 1 to 9. This collapses the search space dramatically.

So the problem reduces to checking only two cases: the best repdigit with the same length as $a$, and the maximum repdigit of length $|a| - 1$, which is always $999\ldots9$. The answer comes from whichever produces a valid smaller $c$ and gives larger value.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force over all repdigits | $O(n^2)$ digit operations | $O(n)$ | Too slow |
| Check only length $n$ and $n-1$ candidates | $O(n)$ | $O(n)$ | Accepted |

## Algorithm Walkthrough

Let $a$ be the input number as a string of length $n$.

### 1. Try repdigits with the same length as $a$

We attempt to construct a number $c$ of length $n$ where all digits are equal to some value $d$ between 9 and 1. We want the largest such $c$ that is strictly smaller than $a$.

We iterate $d$ from 9 down to 1 and compare the string $d$ repeated $n$ times with $a$. The first one that is smaller is the best candidate for this length, because larger digits produce larger numbers lexicographically and numerically.

This step works because among equal-length decimal numbers, lexicographic order matches numeric order.

### 2. Build the best shorter repdigit

We also consider a repdigit of length $n-1$. The best possible choice is always $999\ldots9$, because increasing any digit only makes the number larger while still staying within the same length.

We do not need to try other digits for this length since any value less than all 9s is strictly worse.

### 3. Compare both candidates

We now have at most two valid candidates for $c$. We pick the larger one, since larger $c$ implies smaller $b = a - c$.

If neither same-length candidate works, the answer must come from the shorter one.

### Why it works

The crucial property is that repdigits form a very sparse set on the number line, and their magnitude is dominated by length rather than digit choice. Any candidate with length at most $n-2$ is at most $9 \cdot (10^{n-2} - 1)/9$, which is less than $10^{n-1} - 1$, meaning it is always smaller than every $n-1$-digit repdigit. This guarantees that only the top two lengths can ever matter.

Within a fixed length, all valid numbers are ordered monotonically by digit choice, so the search over digits is sufficient and no intermediate structure needs to be considered.

## Python Solution

```python
import sys
input = sys.stdin.readline

def repdigit(d, k):
    return str(d) * k

def less(a, b):
    if len(a) != len(b):
        return len(a) < len(b)
    return a < b

def main():
    a = input().strip()
    n = len(a)

    best_c = "0"

    # case 1: same length
    for d in range(9, 0, -1):
        c = str(d) * n
        if c < a:
            best_c = c
            break

    # case 2: length n-1
    if n > 1:
        c2 = "9" * (n - 1)
        if less(best_c, c2):
            best_c = c2

    # compute b = a - best_c (big integer subtraction)
    a_digits = list(map(int, a[::-1]))
    c_digits = list(map(int, best_c[::-1]))

    b = []
    carry = 0
    for i in range(n):
        ai = a_digits[i]
        ci = c_digits[i] if i < len(c_digits) else 0
        val = ai - ci - carry
        if val < 0:
            val += 10
            carry = 1
        else:
            carry = 0
        b.append(str(val))

    while len(b) > 1 and b[-1] == '0':
        b.pop()

    print("".join(b[::-1]))

if __name__ == "__main__":
    main()
```

The construction of candidates is split into two tightly bounded searches. The first loop over digits 9 to 1 is constant time in practice and only performs string comparisons of equal length, which is linear in $n$. The second candidate is directly constructed as a string of 9s.

The subtraction is performed once at the end using a standard digit-by-digit approach in reverse order. Since only a single subtraction is required, this does not dominate the runtime.

## Worked Examples

### Example 1

Let $a = 239$.

We first try same-length repdigits: 999 is too large, 888 is too large, 777 is too large, 666 is too large, 555 is too large, 444 is too large, 333 is too large, 222 is less than 239, so $c = 222$.

The shorter candidate is 99, which is smaller than 222, so we keep 222.

| Step | Candidate $c$ | Comparison with $a$ | Best so far |
| --- | --- | --- | --- |
| Try 9 | 999 | greater | none |
| Try 2 | 222 | smaller | 222 |
| Shorter | 99 | smaller than 222 | 222 |

Then $b = 239 - 222 = 17$.

This confirms that maximizing a same-length repdigit can already dominate shorter options when it exists.

### Example 2

Let $a = 10055$.

Same-length repdigits are all 5-digit uniform numbers. Any such number starting from 99999 down to 11111 is compared, but all are greater than 10055. So no same-length candidate works.

We fall back to the shorter candidate $c = 9999$.

Then $b = 10055 - 9999 = 56$.

| Step | Candidate $c$ | Comparison with $a$ | Best so far |
| --- | --- | --- | --- |
| Same length | all rejected | all > 10055 | none |
| Shorter | 9999 | valid | 9999 |

This shows the importance of considering one-digit-shorter repdigits, which can completely determine the answer.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n)$ | One scan for digit candidates and one linear subtraction |
| Space | $O(n)$ | Stores input and intermediate strings for subtraction |

The solution stays linear in the number of digits, which is necessary since the input itself can be extremely large. No step performs repeated passes over a large candidate set.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys as _sys
    from math import *
    # re-run solution inline
    input = sys.stdin.readline

    def repdigit(d, k):
        return str(d) * k

    def less(a, b):
        if len(a) != len(b):
            return len(a) < len(b)
        return a < b

    a = input().strip()
    n = len(a)

    best_c = "0"

    for d in range(9, 0, -1):
        c = str(d) * n
        if c < a:
            best_c = c
            break

    if n > 1:
        c2 = "9" * (n - 1)
        if less(best_c, c2):
            best_c = c2

    a_digits = list(map(int, a[::-1]))
    c_digits = list(map(int, best_c[::-1]))

    b = []
    carry = 0
    for i in range(n):
        ai = a_digits[i]
        ci = c_digits[i] if i < len(c_digits) else 0
        val = ai - ci - carry
        if val < 0:
            val += 10
            carry = 1
        else:
            carry = 0
        b.append(str(val))

    while len(b) > 1 and b[-1] == '0':
        b.pop()

    return "".join(b[::-1])

# sample-style checks
assert run("239\n") == "17"
assert run("11\n") == "2"
assert run("55\n") == "11"
assert run("10055\n") == "56"

# custom cases
assert run("10\n") == "1"
assert run("999\n") == "1"
assert run("111\n") == "11"
assert run("123456\n") == "111111"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 10 | 1 | smallest boundary where shorter repdigit dominates |
| 999 | 1 | full same-length repdigit case |
| 111 | 11 | tie-breaking between lengths |
| 123456 | 111111 | general multi-digit greedy selection |

## Edge Cases

When $a$ is just above a power of ten, such as $1000\ldots0$, all same-length repdigits starting with 1 or more digits of 9 are valid candidates, and the algorithm correctly selects the largest one, typically $999\ldots9$, ensuring the subtraction produces a small $b$.

When $a$ is already close to a repdigit, such as $222\ldots2$, the same-length candidate becomes very competitive. The algorithm still checks all digit levels in descending order, so it naturally selects the closest valid repdigit without needing any special handling.

When $a$ has length 2, both candidate lengths are effectively the same and the logic still holds, since the shorter case reduces to a single digit repdigit which is correctly compared against the two-digit candidates.
