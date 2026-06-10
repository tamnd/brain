---
title: "CF 1562B - Scenes From a Memory"
description: "We are given a number n without zeros in its decimal representation, and the task is to remove some digits to obtain a number that is not prime, either a composite number or 1. The goal is to remove as many digits as possible while still ensuring the result is not prime."
date: "2026-06-10T12:07:52+07:00"
tags: ["codeforces", "competitive-programming", "brute-force", "constructive-algorithms", "implementation", "math", "number-theory"]
categories: ["algorithms"]
codeforces_contest: 1562
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 741 (Div. 2)"
rating: 1000
weight: 1562
solve_time_s: 155
verified: true
draft: false
---

[CF 1562B - Scenes From a Memory](https://codeforces.com/problemset/problem/1562/B)

**Rating:** 1000  
**Tags:** brute force, constructive algorithms, implementation, math, number theory  
**Solve time:** 2m 35s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a number `n` without zeros in its decimal representation, and the task is to remove some digits to obtain a number that is **not prime**, either a composite number or `1`. The goal is to remove as many digits as possible while still ensuring the result is not prime. The input includes multiple test cases, each specifying the number of digits `k` and the number `n` itself. The output for each test case is the length of the remaining number and the number itself after deletion.

The constraints are moderate: `k` is at most 50, and the sum of `k` over all test cases is at most 10,000. This means we cannot afford algorithms that enumerate all subsequences of digits, because the number of subsequences grows exponentially with `k`. We need an approach that is mostly linear in `k` per test case.

The edge cases that could break a naive solution are small numbers where single digits or pairs are prime. For example, if `n = 53`, no single digit is non-prime, but the pair `53` itself is prime, so the solution must consider pairs or other short subsequences. Another subtle case is numbers made entirely of the same digit, like `4444`, where removing all but one digit still yields a composite.

## Approaches

The brute-force approach is to generate all subsequences of digits from length 1 to `k-1` and check if each number is not prime. This works in principle, but the number of subsequences is `2^k - 1`, which is astronomically large for `k = 50`. Even a linear primality test per number is far too slow.

The key observation that simplifies the problem is that we only need to find a **small non-prime number**, ideally of length 1 or 2. This works because there is always a single-digit composite (`4, 6, 8, 9`) or a pair of digits forming a two-digit non-prime. Since `n` has no zeros, any digit `1, 4, 6, 8, 9` immediately gives a valid answer of length 1. If no single digit works, checking all pairs of digits is feasible: there are at most `k*(k-1)/2` pairs, which is at most 1,225 for `k = 50`, and verifying if a two-digit number is non-prime is constant time.

The optimal solution is thus: first scan for a single-digit composite. If none exists, scan all two-digit numbers. The problem guarantees that at least one solution exists, so we will always find one.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(2^k * k) | O(k) | Too slow |
| Optimal | O(k^2) | O(1) | Accepted |

## Algorithm Walkthrough

1. For each test case, read `k` and `n`. Convert `n` into a list of digits for easier manipulation.
2. Scan the digits from left to right, checking if any digit is in the set `{1, 4, 6, 8, 9}`. These are single-digit numbers that are not prime. If one is found, output `1` and that digit, then continue to the next test case.
3. If no single-digit composite is found, generate all two-digit numbers by taking every pair of digits `(i, j)` with `i < j`.
4. For each two-digit number, check if it is **not prime**. Since the largest two-digit number is 99, a simple lookup in a precomputed small prime set or a constant-time check suffices.
5. Output the length `2` and the first two-digit number found that is non-prime. Move on to the next test case.

**Why it works**: By construction, the algorithm first prioritizes single-digit composites, which are the maximal deletions we can make to reduce the number. If none exist, any two-digit non-prime is guaranteed to exist according to the problem constraints. This ensures correctness and minimal computation.

## Python Solution

```python
import sys
input = sys.stdin.readline

# Helper: check if 2-digit number is prime
def is_prime_2digit(x):
    if x < 2: return False
    for p in [2, 3, 5, 7]:
        if x == p: return True
        if x % p == 0: return False
    return True

t = int(input())
for _ in range(t):
    k = int(input())
    n = input().strip()
    
    # Step 1: check single-digit non-prime
    for d in n:
        if d in '14689':
            print(1)
            print(d)
            break
    else:
        # Step 2: check two-digit non-prime
        found = False
        for i in range(k):
            for j in range(i+1, k):
                num = int(n[i] + n[j])
                if not is_prime_2digit(num):
                    print(2)
                    print(n[i] + n[j])
                    found = True
                    break
            if found:
                break
```

The code starts by checking digits that are immediately non-prime. The `else` after the `for` loop ensures we only enter two-digit search if no single-digit solution exists. For two-digit numbers, we check each combination with a small constant-time primality check, which is safe since the numbers are all at most 99.

## Worked Examples

### Sample Input 1

| n | Single-digit composite found | Two-digit pair found | Output |
| --- | --- | --- | --- |
| 237 | 2,3,7 → none | 23, 27 → 27 is composite | 2 / 27 |
| 44444 | 4 exists | - | 1 / 4 |

The trace shows that for 237, no single-digit solution exists, so the first non-prime pair `27` is selected. For 44444, the single-digit 4 suffices.

### Sample Input 2

| n | Single-digit composite | Two-digit pair | Output |
| --- | --- | --- | --- |
| 773 | none | 77 → 77 is composite | 2 / 77 |
| 35 | none | 35 → 35 is composite | 2 / 35 |

Here, scanning for single-digit composites fails. Generating pairs produces the first non-prime number.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(k^2) per test case | Checking all pairs if no single-digit composite is found |
| Space | O(1) | Only a few variables and the input string |

With `k <= 50` and `sum(k) <= 10^4`, the algorithm easily runs under the 1-second limit.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    output = io.StringIO()
    sys.stdout = output
    exec(open('solution.py').read())  # Assuming solution is saved as solution.py
    return output.getvalue().strip()

# Provided samples
assert run("7\n3\n237\n5\n44444\n3\n221\n2\n35\n3\n773\n1\n4\n30\n626221626221626221626221626221\n") == \
"2\n27\n1\n4\n1\n1\n2\n35\n2\n77\n1\n4\n1\n6", "sample 1"

# Cu
```
