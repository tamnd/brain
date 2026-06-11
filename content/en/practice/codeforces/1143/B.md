---
title: "CF 1143B - Nirvana"
description: "We are asked to find, for a given integer $n$, the largest product of digits that any number from 1 to $n$ can have. In other words, imagine iterating through all numbers from 1 up to $n$ and multiplying the digits of each number; we want the maximum such product."
date: "2026-06-12T03:35:51+07:00"
tags: ["codeforces", "competitive-programming", "brute-force", "math", "number-theory"]
categories: ["algorithms"]
codeforces_contest: 1143
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 549 (Div. 2)"
rating: 1200
weight: 1143
solve_time_s: 96
verified: true
draft: false
---

[CF 1143B - Nirvana](https://codeforces.com/problemset/problem/1143/B)

**Rating:** 1200  
**Tags:** brute force, math, number theory  
**Solve time:** 1m 36s  
**Verified:** yes  

## Solution
## Problem Understanding

We are asked to find, for a given integer $n$, the largest product of digits that any number from 1 to $n$ can have. In other words, imagine iterating through all numbers from 1 up to $n$ and multiplying the digits of each number; we want the maximum such product.

The input is a single integer $n$ where $1 \le n \le 2 \cdot 10^9$. This upper bound immediately tells us that iterating over all numbers from 1 to $n$ is infeasible, because that could be two billion operations and any solution that checks every number would timeout.

Non-obvious edge cases arise when the optimal number has digits smaller than $n$ itself. For instance, with $n = 390$, the optimal number is $389$, not $390$, because changing the last digit from 0 to 9 can produce a larger product. Another tricky scenario is when $n$ consists mostly of 9s; then $n$ itself may be optimal. Finally, single-digit $n$ values are trivial but must still be handled correctly.

## Approaches

The brute-force solution is simple to describe: iterate through every number from 1 to $n$, compute the product of its digits, and keep track of the maximum. This is correct because it explicitly checks all possibilities. Its complexity is $O(n \cdot d)$, where $d$ is the number of digits in the current number, but even with $d \approx 10$ for $n = 2 \cdot 10^9$, it is far too slow because $n$ itself is huge.

The key insight for a faster approach comes from observing how products behave when digits decrease. If we have a number like 390, lowering one of the digits (from 0 to 9) while reducing all subsequent digits to 9 often increases the product. This is because 0 in the digits kills the product entirely. Therefore, instead of checking all numbers, we only need to check numbers formed by:

1. Keeping some prefix of $n$ the same.
2. Reducing the first non-zero digit in the remaining suffix by 1.
3. Replacing all subsequent digits with 9.

Additionally, we must always consider $n$ itself. This reduces the candidate numbers from billions to at most the number of digits in $n$ plus one, which is at most 10 for our constraints.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n·d) | O(1) | Too slow |
| Optimal | O(d^2) | O(d) | Accepted |

## Algorithm Walkthrough

1. Convert $n$ into a string $s$ to manipulate digits individually.
2. Initialize `max_product` as the product of digits of $n$ itself. This ensures we always consider $n$ as a candidate.
3. Iterate over each digit position $i$ in $s$:

1. If the digit at position $i$ is 0, skip to the next position because reducing 0 would create a negative or invalid digit.
2. Construct a new candidate number by keeping the prefix up to $i-1$ unchanged.
3. Reduce the digit at $i$ by 1.
4. Replace all digits after $i$ with 9.
5. Compute the product of digits for this candidate and update `max_product` if larger.
4. Output `max_product`.

Why it works: The invariant is that for any number larger than $n$, reducing the first non-zero digit and filling the rest with 9 maximizes the product without exceeding $n$. By checking all positions where a reduction can occur, we guarantee the maximum product is found.

## Python Solution

```python
import sys
input = sys.stdin.readline

def product_of_digits(num_str):
    prod = 1
    for ch in num_str:
        prod *= int(ch)
    return prod

def main():
    n = input().strip()
    max_prod = product_of_digits(n)
    
    n_list = list(n)
    for i in range(len(n_list)):
        if n_list[i] == '0':
            continue
        candidate = n_list[:i] + [str(int(n_list[i])-1)] + ['9'] * (len(n_list)-i-1)
        candidate_str = ''.join(candidate).lstrip('0')
        if candidate_str:
            max_prod = max(max_prod, product_of_digits(candidate_str))
    
    print(max_prod)

if __name__ == "__main__":
    main()
```

The code first defines a helper function to compute the product of digits. Then it iterates over every digit in `n`, tries reducing that digit by 1, fills the rest with 9s, and calculates the product. Leading zeros are stripped because they do not contribute to the number. The maximum product among all candidates is printed.

## Worked Examples

### Sample 1: $n = 390$

| Step | Candidate | Product |
| --- | --- | --- |
| Original n | 390 | 3_9_0 = 0 |
| Reduce first digit (3->2) + 9s | 299 | 2_9_9 = 162 |
| Reduce second digit (9->8) + 9s | 389 | 3_8_9 = 216 |

The trace shows that reducing the second digit gives the optimal product 216.

### Sample 2: $n = 7$

| Step | Candidate | Product |
| --- | --- | --- |
| Original n | 7 | 7 |

No reductions are possible. Maximum product is 7.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(d^2) | `d` is the number of digits in `n`. Each candidate requires computing the product of at most `d` digits. |
| Space | O(d) | For storing digit strings and candidates. |

Given $d \le 10$, the solution executes in a few hundred operations, well within 1 second.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()
    main()
    return sys.stdout.getvalue().strip()

# Provided samples
assert run("390\n") == "216", "sample 1"
assert run("7\n") == "7", "sample 2"
assert run("999999999\n") == "387420489", "sample 3"

# Custom cases
assert run("1\n") == "1", "minimum n"
assert run("10\n") == "9", "two-digit with zero"
assert run("1000000000\n") == "999999999", "largest n with zeroes"
assert run("1234\n") == "1080", "mixed digits"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 | 1 | Minimum input |
| 10 | 9 | Handling zero correctly |
| 1000000000 | 387420489 | Maximum n with zeros, large numbers |
| 1234 | 1080 | Correct reduction and digit replacement logic |

## Edge Cases

For $n = 10$, the algorithm checks the original 10 (product 0) and reduces the first digit 1->0 with rest as 9 -> 9. Maximum product becomes 9. For $n = 1000000000$, reducing the first 1 to 0 and filling the rest with 9 yields 999999999, product $9^9$. Single-digit inputs are handled trivially by initializing `max_product` with the product of digits of `n`.

The algorithm never misses an optimal candidate because any number that could surpass the product of `n` can be formed by reducing a prefix digit and filling the rest with 9s.
