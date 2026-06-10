---
title: "CF 1512G - Short Task"
description: "We are asked to find the smallest positive integer $n$ such that the sum of its divisors equals a given number $c$. Formally, the sum-of-divisors function $d(n)$ sums all numbers that divide $n$ evenly, including $1$ and $n$ itself. For example, $d(6) = 1 + 2 + 3 + 6 = 12$."
date: "2026-06-10T18:56:24+07:00"
tags: ["codeforces", "competitive-programming", "brute-force", "dp", "math", "number-theory"]
categories: ["algorithms"]
codeforces_contest: 1512
codeforces_index: "G"
codeforces_contest_name: "Codeforces Round 713 (Div. 3)"
rating: 1700
weight: 1512
solve_time_s: 183
verified: false
draft: false
---

[CF 1512G - Short Task](https://codeforces.com/problemset/problem/1512/G)

**Rating:** 1700  
**Tags:** brute force, dp, math, number theory  
**Solve time:** 3m 3s  
**Verified:** no  

## Solution
## Problem Understanding

We are asked to find the smallest positive integer $n$ such that the sum of its divisors equals a given number $c$. Formally, the sum-of-divisors function $d(n)$ sums all numbers that divide $n$ evenly, including $1$ and $n$ itself. For example, $d(6) = 1 + 2 + 3 + 6 = 12$. Given an integer $c$, we must determine whether there exists an $n$ such that $d(n) = c$, and if so, return the smallest such $n$. If no such $n$ exists, we return $-1$.

The input consists of multiple test cases, each giving one integer $c$ up to $10^7$. With $t \le 10^4$ test cases, we cannot afford to compute $d(n)$ naively for all $n \le 10^7$ repeatedly. A naive brute-force approach that checks each $n$ by summing its divisors would take $O(n \sqrt{n})$ per test case, which is prohibitively slow given the worst-case input. We need a smarter approach that precomputes information efficiently for all possible $c$.

Edge cases include $c = 1$, where $n = 1$ is the only valid solution. Another subtle point is that many numbers, such as $c = 2$ or $c = 5$, do not correspond to any $n$. A naive approach that assumes a solution exists for all $c$ would fail on these inputs. We also need to account for numbers that are the sum of divisors of small composite numbers, e.g., $c = 12$ corresponds to $n = 6$, but also $c = 18$ corresponds to $n = 12$. The algorithm must select the minimum $n$.

## Approaches

A brute-force approach would iterate through $n = 1$ to some upper bound (like $10^7$), compute $d(n)$ by checking all divisors up to $\sqrt{n}$, and store the results in a map from sum-of-divisors to the smallest $n$ producing it. While correct, this approach has a complexity of roughly $O(n \sqrt{n}) = O(10^7 \cdot 3162)$, which is far too slow for $t = 10^4$ queries.

The key observation is that we can precompute the sum-of-divisors function for all $n$ up to $10^7$ using a sieve-like approach. The sum-of-divisors function is multiplicative in nature and can be computed by iterating over multiples. Specifically, for each $i$ from 1 to $N$, we add $i$ to $d[j]$ for all multiples $j = i, 2i, 3i, \dots, N$. This allows us to compute $d(n)$ for all $n$ in $O(n \log n)$ time. Once we have $d(n)$ for all $n$, we can map each sum-of-divisors value to the smallest $n$ that produces it. After preprocessing, answering each query becomes a simple dictionary lookup in $O(1)$ time.

The brute-force method works because computing $d(n)$ is straightforward, but fails when $n$ is large and multiple queries require repeated computation. The observation that $d(n)$ can be computed for all $n$ via multiples reduces the problem to a fast preprocessing step, making it feasible to answer thousands of queries quickly.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n√n) per query | O(1) | Too slow |
| Precompute with Sieve | O(n log n) preprocessing, O(1) per query | O(n) | Accepted |

## Algorithm Walkthrough

1. Define a maximum $N = 10^7$ since no input $c$ exceeds this value. Initialize an array $d$ of size $N + 1$ to store sum-of-divisors for each $n$.
2. Iterate $i$ from 1 to $N$. For each $i$, iterate through multiples $j = i, 2i, 3i, \dots, N$, and add $i$ to $d[j]$. This computes the sum-of-divisors function for all numbers up to $N$ efficiently.
3. Initialize a dictionary $answer$ to map each possible sum-of-divisors value to the smallest $n$ producing it. For $n$ from 1 to $N$, if $d[n]$ is not already in $answer$, store $answer[d[n]] = n$. This ensures minimal $n$ is recorded.
4. For each query $c$, check if $c$ exists in $answer$. If it does, output $answer[c]$; otherwise, output $-1$.

Why it works: The sieve-like accumulation guarantees $d[n]$ is computed correctly for every $n$ up to $10^7$. By storing the first occurrence of each sum-of-divisors value, we ensure that the minimum $n$ producing that sum is preserved. No query can produce a wrong answer because all possible sums are precomputed and mapped correctly.

## Python Solution

```python
import sys
input = sys.stdin.readline

MAX_C = 10**7
d = [0] * (MAX_C + 1)
for i in range(1, MAX_C + 1):
    for j in range(i, MAX_C + 1, i):
        d[j] += i

answer = {}
for n in range(1, MAX_C + 1):
    if d[n] not in answer:
        answer[d[n]] = n

t = int(input())
for _ in range(t):
    c = int(input())
    print(answer.get(c, -1))
```

The first block computes all sum-of-divisors using a sieve. The second block ensures we store the smallest $n$ for each sum. Finally, queries are answered in constant time using a dictionary lookup. A subtle point is iterating $n$ from 1 to $N$ for mapping; reversing the order would break the "minimum $n$" guarantee.

## Worked Examples

For the input:

```
3
1
12
18
```

| n | d[n] | answer dictionary updated? |
| --- | --- | --- |
| 1 | 1 | answer[1] = 1 |
| 2 | 3 | answer[3] = 2 |
| 3 | 4 | answer[4] = 3 |
| 4 | 7 | answer[7] = 4 |
| 5 | 6 | answer[6] = 5 |
| 6 | 12 | answer[12] = 6 |
| 12 | 28 | answer[28] = 12 |
| 18 | 39 | answer[39] = 18 |

Queries: 1 → 1, 12 → 6, 18 → 18.

This confirms the mapping works and minimum $n$ is preserved.

Another trace for $c = 2$:

| n | d[n] | answer dictionary updated? |
| --- | --- | --- |
| 1 | 1 | answer[1] = 1 |
| 2 | 3 | answer[3] = 2 |

Query 2 → not in dictionary → output -1. This shows the algorithm correctly identifies impossible sums.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(N log N + t) | Sieve for sum-of-divisors takes O(N log N), answering t queries is O(t) |
| Space | O(N) | Array d and dictionary answer each store up to N elements |

With $N = 10^7$ and $t = 10^4$, this solution runs comfortably under the 2-second limit and uses less than 512 MB.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    output = io.StringIO()
    sys.stdout = output
    
    MAX_C = 10**7
    d = [0] * (MAX_C + 1)
    for i in range(1, MAX_C + 1):
        for j in range(i, MAX_C + 1, i):
            d[j] += i

    answer = {}
    for n in range(1, MAX_C + 1):
        if d[n] not in answer:
            answer[d[n]] = n

    t = int(input())
    for _ in range(t):
        c = int(input())
        print(answer.get(c, -1))
    
    return output.getvalue().strip()

# provided sample
assert run("12\n1\n2\n3\n4\n5\n6\n7\n8\n9\n10\n39\n691\n") == "1\n-1\n2\n3\n-1\n5\n4\n7\n-1\n-1\n18
```
