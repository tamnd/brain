---
title: "CF 105230E - Great Product"
description: "We are given a single integer $n$, and we want to express it as a product of integers greater than 1. The twist is that among all possible factorizations, we are not optimizing for simplicity or minimal number of terms, but for the opposite: we want to maximize how many factors…"
date: "2026-06-24T15:59:25+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105230
codeforces_index: "E"
codeforces_contest_name: "2024-2025 ICPC Bolivia Pre-National Contest"
rating: 0
weight: 105230
solve_time_s: 69
verified: true
draft: false
---

[CF 105230E - Great Product](https://codeforces.com/problemset/problem/105230/E)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 9s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a single integer $n$, and we want to express it as a product of integers greater than 1. The twist is that among all possible factorizations, we are not optimizing for simplicity or minimal number of terms, but for the opposite: we want to maximize how many factors appear in the product.

Each factor must be at least 2, since using 1 is explicitly forbidden even though it would trivially allow infinite length representations. The output is a sequence of integers in non-decreasing order whose product equals $n$, and among all valid decompositions, we choose the one with the maximum number of terms.

The constraint $2 \le n \le 10^5$ is small enough that we can afford methods that factorize $n$ in roughly $O(\sqrt{n})$, or even $O(n)$ precomputation ideas. What we cannot afford is enumerating all factorizations or doing exponential recursion over partitions of factors, since the number of multiplicative decompositions grows very quickly even for moderate values.

A key edge case is when $n$ is prime. In that situation, no non-trivial factorization exists, so the only valid representation is the number itself.

Another subtle case appears when multiple factorization paths exist but differ in depth. For example, $12$ can be written as $3 \times 4$ or $2 \times 6$, but only the decomposition that keeps splitting until all factors are prime achieves the maximum length. A naive greedy choice like always taking the smallest divisor first does not automatically guarantee the best global factor count unless we justify it properly.

## Approaches

The brute-force approach is to recursively try every possible split of $n$ into $a \times b$, then continue factorizing both $a$ and $b$, tracking the decomposition with the maximum number of terms. This is correct because it explores the full state space of multiplicative partitions. However, even for moderate $n$, this becomes infeasible. Many numbers have dozens of divisors, and each branch leads to further branching, creating an exponential explosion. In the worst case, such as highly composite numbers, the recursion tree grows extremely large.

The key observation is that we are not asked for arbitrary factors, but for the decomposition that maximizes the number of terms. To maximize the number of factors, we want to split numbers as much as possible, and splitting any composite number into smaller factors always increases or preserves the total count of factors. This suggests that the optimal strategy is to decompose $n$ completely into prime factors, since primes are the minimal indivisible building blocks under multiplication.

Once we reach prime factorization, no further splitting is possible, so the number of factors is maximized exactly when every composite is broken down fully. This turns the problem into standard prime factorization, followed by sorting the resulting primes in non-decreasing order, which is already naturally satisfied if we collect them in increasing divisor order.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force recursion over all factorizations | exponential | O(log n) stack | Too slow |
| Prime factorization (trial division) | O(\sqrt{n}) | O(log n) | Accepted |

## Algorithm Walkthrough

1. Start with the number $n$ and attempt to extract all factors starting from the smallest possible divisor $2$. We begin with small divisors because splitting by smaller numbers increases the total count of factors more aggressively than using larger composite splits.
2. For each integer $d$ from 2 up to $\sqrt{n}$, repeatedly divide $n$ by $d$ while it is divisible. Every time we divide, we record $d$ as one factor. This ensures that we fully extract all occurrences of $d$ before moving on.
3. Once a divisor no longer divides $n$, increment $d$ and continue. This guarantees that every composite structure is eventually broken down into prime components because any composite factor must have a prime divisor not exceeding its square root.
4. After finishing the loop, if the remaining value of $n$ is greater than 1, it must be prime. We append it as the final factor.
5. Output all collected factors in order, joined by the character 'x'. The order is naturally non-decreasing because we iterate divisors in increasing order.

### Why it works

The core property is that any composite factorization can be refined into prime factors without decreasing the number of terms, and in fact strictly increasing it unless the factor was already prime. Any factor $a \times b$ with $a, b > 1$ contributes two terms instead of one, so repeatedly breaking composites always improves or preserves the count. Therefore, the maximal-length decomposition is exactly the prime factorization of $n$, and no alternative grouping can produce more factors.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input().strip())
    res = []
    
    d = 2
    while d * d <= n:
        while n % d == 0:
            res.append(d)
            n //= d
        d += 1
    
    if n > 1:
        res.append(n)
    
    print("x".join(map(str, res)))

if __name__ == "__main__":
    solve()
```

The implementation directly mirrors the factor extraction process. The outer loop advances possible divisors, while the inner loop removes all occurrences of the current divisor, ensuring multiplicity is fully captured. The final check handles the case where a large prime remains after division, which is standard in trial division.

The key implementation detail is using $d \times d \le n$ as the stopping condition, which ensures correctness even as $n$ shrinks during division. This avoids unnecessary iterations beyond the current reduced value.

## Worked Examples

### Example 1: $n = 12$

We track how factors are extracted.

| Step | d | n before | Action | Factors |
| --- | --- | --- | --- | --- |
| 1 | 2 | 12 | divide | 2 |
| 2 | 2 | 6 | divide | 2, 2 |
| 3 | 2 | 3 | stop | 2, 2 |
| 4 | 3 | 3 | divide | 2, 2, 3 |

Final output is `2x2x3`.

This trace shows that repeated division naturally decomposes composites fully, producing the maximum number of factors.

### Example 2: $n = 5$

| Step | d | n before | Action | Factors |
| --- | --- | --- | --- | --- |
| 1 | 2 | 5 | skip |  |
| 2 | 3 | 5 | skip |  |
| 3 | 4 | 5 | skip |  |
| 4 | final | 5 | append | 5 |

Output is `5`.

This demonstrates the prime case where no decomposition increases the factor count.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(\sqrt{n}) | each divisor is tested up to sqrt(n), with constant-time divisions per hit |
| Space | O(log n) | storing prime factors of n |

The constraints allow this comfortably, since $\sqrt{10^5} \approx 316$, making the solution extremely fast even in Python.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from sys import stdout
    out = []
    
    def input():
        return sys.stdin.readline()
    
    n = int(input().strip())
    res = []
    d = 2
    while d * d <= n:
        while n % d == 0:
            res.append(d)
            n //= d
        d += 1
    if n > 1:
        res.append(n)
    return "x".join(map(str, res))

assert run("12\n") == "2x2x3"
assert run("5\n") == "5"
assert run("2\n") == "2"
assert run("16\n") == "2x2x2x2"
assert run("30\n") == "2x3x5"
assert run("49\n") == "7x7"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 2 | 2 | minimum input size |
| 16 | 2x2x2x2 | repeated prime factors |
| 30 | 2x3x5 | distinct primes ordering |
| 49 | 7x7 | repeated large prime square |

## Edge Cases

For a prime input like $n = 13$, the algorithm tries divisors 2 and 3, finds none, and directly appends 13 as the only factor. The trace shows no divisions happen, so the output remains a single-element list.

For a power of two like $n = 16$, repeated division by 2 continues until the value becomes 1, producing four occurrences of 2. Each division strictly increases the factor count, demonstrating the optimality condition directly.

For mixed composites like $n = 30$, the algorithm extracts 2, then 3, then 5 in increasing order. Since each is prime, no further splitting is possible, and any alternative grouping such as $6 \times 5$ or $3 \times 10$ would yield fewer total factors, confirming why full factorization is necessary.
