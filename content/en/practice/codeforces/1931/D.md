---
title: "CF 1931D - Divisible Pairs"
description: "We are given an array of integers and two numbers, $x$ and $y$. A pair of indices $(i, j)$ with $i < j$ is considered \"beautiful\" if the sum of the two elements $ai + aj$ is divisible by $x$ and the difference $ai - aj$ is divisible by $y$."
date: "2026-06-08T18:28:04+07:00"
tags: ["codeforces", "competitive-programming", "combinatorics", "math", "number-theory"]
categories: ["algorithms"]
codeforces_contest: 1931
codeforces_index: "D"
codeforces_contest_name: "Codeforces Round 925 (Div. 3)"
rating: 1300
weight: 1931
solve_time_s: 210
verified: true
draft: false
---

[CF 1931D - Divisible Pairs](https://codeforces.com/problemset/problem/1931/D)

**Rating:** 1300  
**Tags:** combinatorics, math, number theory  
**Solve time:** 3m 30s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given an array of integers and two numbers, $x$ and $y$. A pair of indices $(i, j)$ with $i < j$ is considered "beautiful" if the sum of the two elements $a_i + a_j$ is divisible by $x$ and the difference $a_i - a_j$ is divisible by $y$. For each test case, we need to count how many such pairs exist.

The constraints are important to interpret correctly. Each array can be up to $2 \cdot 10^5$ elements, and there can be up to $10^4$ test cases. The total sum of $n$ across all test cases does not exceed $2 \cdot 10^5$, so we can treat $n$ as effectively $2 \cdot 10^5$ per batch. A brute-force approach that checks all pairs directly would require $O(n^2)$ operations, which could be as large as $4 \cdot 10^{10}$ and is far too slow for a 2-second limit. We need a solution that scales linearly or near-linearly with $n$.

An edge case that can break naive solutions is when all numbers are equal or when $x$ or $y$ divide the differences trivially. For instance, if $x = y = 1$, every pair is beautiful. A careless implementation might attempt modulo operations without considering negative numbers, leading to subtle off-by-one or sign errors.

## Approaches

The naive approach iterates over every pair $(i, j)$ and checks the two divisibility conditions. This is correct because it directly implements the problem statement, but it requires $O(n^2)$ checks. For $n \approx 2 \cdot 10^5$, this would produce roughly $2 \cdot 10^10$ iterations, which is far beyond the feasible computation limit.

The key insight for optimization comes from looking at the congruence conditions modulo $x$ and $y$. Let $a_i + a_j \equiv 0 \pmod{x}$ and $a_i - a_j \equiv 0 \pmod{y}$. We can solve these two congruences simultaneously. Adding and subtracting them shows that $2a_i \equiv 0 \pmod{\text{lcm}(x, y)}$ and $2a_j \equiv 0 \pmod{\text{lcm}(x, y)}$ up to some shifts. Concretely, we can transform the problem to counting how many previous numbers $a_j$ satisfy a linear congruence relative to the current number $a_i$, which can be done with a hash map (dictionary) of residues modulo a derived modulus. This reduces the pair-checking from quadratic to linear in the array length.

The story here is that the sum and difference conditions look complicated at first, but by rephrasing them in terms of modular arithmetic, they become a problem of counting matching residues. Using a dictionary to store frequency of each residue allows us to incrementally count beautiful pairs as we iterate over the array exactly once.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n^2) | O(1) | Too slow |
| Modular Hash Map | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Precompute the greatest common divisor (gcd) of $x$ and $y$, which will help in reducing the two congruences to a single modulus. Let $g = \gcd(x, y)$.
2. Iterate over the array from left to right. For each element $a_i$, compute two values: $r_i = a_i \bmod x$ and $s_i = a_i \bmod y$. These represent the current element's remainder relative to $x$ and $y$.
3. Construct a combined residue key $(r_i, s_i)$ and store a frequency map of how many times each such key has appeared. This allows checking how many previous elements satisfy the modular conditions required to form a beautiful pair with $a_i$.
4. For each element $a_i$, compute the corresponding complementary residue $(r_j, s_j)$ that would make the pair $(a_j, a_i)$ beautiful, using the formula derived from the congruences. Add the frequency of that key in the map to the answer.
5. After processing $a_i$, increment its key in the frequency map so that future elements can form pairs with it.

Why it works: At each step, the map stores counts of all previously seen elements grouped by their residues modulo $x$ and $y$. Every time we encounter a new element, we compute exactly which residues it can pair with to satisfy the sum and difference conditions. Because we iterate only once and the map tracks all relevant previous elements, we count every valid pair exactly once without checking redundant pairs.

## Python Solution

```python
import sys
input = sys.stdin.readline
from collections import defaultdict
from math import gcd

def count_beautiful_pairs(n, x, y, a):
    freq = defaultdict(int)
    ans = 0
    g = gcd(x, y)
    lcm = x * y // g
    
    for val in a:
        # target residues for previous elements
        target = ((-val) % x, (val) % y)
        ans += freq[target]
        # current residue key
        key = (val % x, val % y)
        freq[key] += 1
    return ans

t = int(input())
for _ in range(t):
    n, x, y = map(int, input().split())
    a = list(map(int, input().split()))
    print(count_beautiful_pairs(n, x, y, a))
```

The solution builds a frequency dictionary keyed by pairs of residues modulo $x$ and $y$. For each element, we compute the residues that would satisfy the sum and difference constraints with previous elements. Incrementing the frequency after counting ensures that no pair is double-counted. The use of `%` ensures correct handling of negative numbers, which is subtle because Python's modulo operator always returns a non-negative result.

## Worked Examples

Take the input `6 5 2; 1 2 7 4 9 6`. Iterating through the array:

| i | a[i] | val%x | val%y | target | freq map | ans |
| --- | --- | --- | --- | --- | --- | --- |
| 0 | 1 | 1 | 1 | (4,1) | {} | 0 |
| 1 | 2 | 2 | 0 | (3,0) | {(1,1):1} | 0 |
| 2 | 7 | 2 | 1 | (3,1) | {(1,1):1,(2,0):1} | 0 |
| 3 | 4 | 4 | 0 | (1,0) | ... | 0 |
| 4 | 9 | 4 | 1 | (1,1) | ... | 1 |
| 5 | 6 | 1 | 0 | (4,0) | ... | 1 |

Final answer is 2. This table shows that only when the target key exists in the frequency map does the count increment, confirming the modular mapping captures exactly the valid pairs.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Each element is processed once, and dictionary operations are O(1) amortized |
| Space | O(n) | Frequency dictionary stores up to n distinct residue pairs |

With $n$ up to $2 \cdot 10^5$ and a linear pass per test case, the solution runs comfortably under 2 seconds.

## Test Cases

```python
import io, sys

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    output = io.StringIO()
    sys.stdout = output
    exec(open("solution.py").read())
    return output.getvalue().strip()

# provided samples
assert run("7\n6 5 2\n1 2 7 4 9 6\n7 9 5\n1 10 15 3 8 12 15\n9 4 10\n14 10 2 2 11 11 13 5 6\n9 5 6\n10 7 6 7 9 7 7 10 10\n9 6 2\n4 9 7 1 2 2 13 3 15\n9 2 3\n14 6 1 15 12 15 8 2 15\n10 5 7\n13 3 3 2 12 11 3 7 13 14") == "2\n0\n1\n3\n5\n7\n0"

# minimum input
assert run("1\n2 1 1\n1 1") == "1"

# all equal
assert run("1\n5 2 3\n6 6 6 6 6") == "10"

# no valid pairs
assert run("1\n3 7 5\n1 2 3") == "0"

# large numbers
assert run("1\n3 1000000000 999999
```
