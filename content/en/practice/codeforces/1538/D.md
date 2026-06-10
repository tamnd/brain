---
title: "CF 1538D - Another Problem About Dividing Numbers"
description: "We are given two integers, a and b, and a target number of operations k. In each operation, we can take either a or b, choose a divisor greater than one that divides it, and replace the number with its quotient."
date: "2026-06-10T14:59:31+07:00"
tags: ["codeforces", "competitive-programming", "constructive-algorithms", "math", "number-theory"]
categories: ["algorithms"]
codeforces_contest: 1538
codeforces_index: "D"
codeforces_contest_name: "Codeforces Round 725 (Div. 3)"
rating: 1700
weight: 1538
solve_time_s: 481
verified: false
draft: false
---

[CF 1538D - Another Problem About Dividing Numbers](https://codeforces.com/problemset/problem/1538/D)

**Rating:** 1700  
**Tags:** constructive algorithms, math, number theory  
**Solve time:** 8m 1s  
**Verified:** no  

## Solution
## Problem Understanding

We are given two integers, `a` and `b`, and a target number of operations `k`. In each operation, we can take either `a` or `b`, choose a divisor greater than one that divides it, and replace the number with its quotient. Our goal is to determine whether we can make `a` equal to `b` using exactly `k` operations.

From a practical perspective, each operation reduces a number by factoring out some component. Since we can choose any divisor greater than one, the most granular way to reduce a number is to factor out a prime. This observation immediately connects the problem to prime factorization: the number of times a number can be "divided" corresponds to the total number of prime factors (counted with multiplicity).

Constraints are high: `a` and `b` can go up to `10^9`, and we may have up to `10^4` test cases. We cannot simulate every possible divisor choice, because the number of divisor combinations grows too fast. Instead, we need a method that scales with the logarithmic size of `a` and `b`, which is naturally captured by their prime factorizations.

Edge cases that can trip up a naive approach include situations where `a` and `b` are already equal, or when `k` is one. For example, if `a=2` and `b=2`, `k=1`, it is impossible to make exactly one move and still have equality - a naive check might incorrectly return "Yes" if it only verifies the numbers can be equal without considering the exact number of moves.

## Approaches

The brute-force approach would attempt every sequence of legal operations on `a` and `b`, checking if we reach equality in exactly `k` steps. This is correct in principle but infeasible. For numbers like `10^9`, the number of divisors can reach hundreds, and trying all sequences for `k` up to `10^9` is impossible. Even for small `k`, the combinatorial explosion makes this O((#divisors)^k), which is far too slow.

The key insight is that the operations correspond to splitting numbers into their prime factors. Each prime factor can be removed in one operation, and because we can pick any divisor, we can always choose to remove a prime or a composite of primes in a single move. Therefore, the minimal number of moves is one if `a != b` and one of them is divisible by the other, and the maximal number of moves is the total count of prime factors of `a` and `b` (counted with multiplicity).

With this, we can solve the problem by counting prime factors. Let `min_moves` be 1 if `a != b` and one divides the other, otherwise 2. Let `max_moves` be the sum of prime factors of `a` and `b`. Then `k` is possible if and only if `min_moves <= k <= max_moves`. This observation drastically reduces complexity: counting prime factors is O(sqrt(n)) per number, which is acceptable for numbers up to `10^9` and 10,000 test cases.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O((#divisors)^k) | O(k) | Too slow |
| Prime Factor Counting | O(sqrt(a)+sqrt(b)) | O(1) | Accepted |

## Algorithm Walkthrough

1. For each test case, read `a`, `b`, and `k`. If `a == b`, handle separately since operations are needed to change numbers.
2. Compute `max_moves` as the sum of the counts of prime factors (with multiplicity) for both `a` and `b`. Factorization can be done by trial division up to sqrt(n).
3. Determine `min_moves`. If `a != b` and one divides the other, `min_moves` is 1; otherwise, it is 2.
4. Check if `k` lies between `min_moves` and `max_moves`. If yes, output "Yes", otherwise "No".

Why it works: the algorithm works because the total number of prime factors represents the upper limit of how many division steps are possible. The minimal moves guarantee feasibility in extreme cases: either a single move if we can divide one by the other directly, or two moves if we need to act on both numbers. Every `k` in this range can be realized because we can combine or split moves by choosing different divisors.

## Python Solution

```python
import sys
input = sys.stdin.readline

def count_prime_factors(n):
    count = 0
    i = 2
    while i * i <= n:
        while n % i == 0:
            count += 1
            n //= i
        i += 1
    if n > 1:
        count += 1
    return count

t = int(input())
for _ in range(t):
    a, b, k = map(int, input().split())
    if k == 1:
        print("YES" if (a != b and (a % b == 0 or b % a == 0)) else "NO")
        continue
    max_moves = count_prime_factors(a) + count_prime_factors(b)
    print("YES" if 2 <= k <= max_moves else "NO")
```

The code reads input efficiently for multiple test cases. The prime factor counter is careful to handle `n` greater than 1 after dividing out small factors. Special handling for `k=1` ensures we respect the “exactly k moves” constraint. Forgetting this condition would incorrectly allow "Yes" when only one move cannot equalize `a` and `b`.

## Worked Examples

### Example 1

Input: `36 48 2`

| Step | a | b | Action |
| --- | --- | --- | --- |
| Initial | 36 | 48 | -- |
| Min moves | -- | -- | 2 (neither divides the other) |
| Max moves | -- | -- | 6 (36=2^2_3^2, 48=2^4_3^1, sum=6) |
| Check | k=2 | -- | 2 <= 2 <= 6 → Yes |

This shows that for `k` smaller than total prime factors, we can achieve equality by choosing the right divisors.

### Example 2

Input: `2 8 1`

| Step | a | b | Action |
| --- | --- | --- | --- |
| Initial | 2 | 8 | -- |
| Min moves | 1 | -- | 1 (2 divides 8) |
| Max moves | 2 | -- | 1+3=4 (2=2, 8=2^3) |
| Check | k=1 | -- | 1 <= 1 <= 4 → Yes |

This illustrates the `k=1` special case where one number divides the other.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(t*(sqrt(a)+sqrt(b))) | Each number is factorized in O(sqrt(n)), up to 10^4 test cases |
| Space | O(1) | Only counters and temporary variables are used, no large arrays |

Given the constraints, `t*sqrt(n)` is well below `10^8`, which is feasible under the 2s time limit.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    output = io.StringIO()
    sys.stdout = output
    # copy the solution here
    def count_prime_factors(n):
        count = 0
        i = 2
        while i * i <= n:
            while n % i == 0:
                count += 1
                n //= i
            i += 1
        if n > 1:
            count += 1
        return count

    t = int(input())
    for _ in range(t):
        a, b, k = map(int, input().split())
        if k == 1:
            print("YES" if (a != b and (a % b == 0 or b % a == 0)) else "NO")
            continue
        max_moves = count_prime_factors(a) + count_prime_factors(b)
        print("YES" if 2 <= k <= max_moves else "NO")
    
    return output.getvalue().strip()

# provided samples
assert run("8\n36 48 2\n36 48 3\n36 48 4\n2 8 1\n2 8 2\n1000000000 1000000000 1000000000\n1 2 1\n2 2 1\n") == \
"YES\nYES\nYES\nYES\nYES\nNO\nYES\nNO"

# custom test cases
assert run("3\n1 1 1\n1 1 2\n17 289 2\n") == "NO\nNO\nYES"
assert run("2\n1000000000 500000000 1\n999983 999983 1\n") == "YES\nNO"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 1 |  |  |
