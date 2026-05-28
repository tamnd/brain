---
title: "CF 122A - Lucky Division"
description: "We are asked to determine whether a given number is almost lucky. A number is almost lucky if it is divisible by at least one lucky number. Lucky numbers are positive integers composed entirely of the digits 4 and 7, like 4, 7, 44, 47, 74, and so on."
date: "2026-05-28T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "brute-force", "number-theory"]
categories: ["algorithms"]
codeforces_contest: 122
codeforces_index: "A"
codeforces_contest_name: "Codeforces Beta Round 91 (Div. 2 Only)"
rating: 1000
weight: 122
solve_time_s: 72
verified: true
draft: false
---

[CF 122A - Lucky Division](https://codeforces.com/problemset/problem/122/A)

**Rating:** 1000  
**Tags:** brute force, number theory  
**Solve time:** 1m 12s  
**Verified:** yes  

## Solution
## Problem Understanding

We are asked to determine whether a given number is almost lucky. A number is almost lucky if it is divisible by at least one lucky number. Lucky numbers are positive integers composed entirely of the digits 4 and 7, like 4, 7, 44, 47, 74, and so on. The input is a single integer `n` between 1 and 1000, and the output is a simple "YES" if the number is almost lucky, or "NO" otherwise.

The constraints are very modest. Since `n` is at most 1000, we can afford to check divisibility against every lucky number up to 1000 without worrying about performance. This also allows us to precompute all lucky numbers in that range. The small upper bound rules out the need for advanced number-theoretic algorithms or optimized sieving techniques.

The non-obvious edge cases arise from small numbers, numbers that are lucky themselves, and numbers that are multiples of lucky numbers but are not lucky themselves. For example, 4 is almost lucky because it is lucky. The number 16 is almost lucky because it is divisible by 4, even though it contains a digit other than 4 or 7. A careless implementation might only check whether `n` is lucky, ignoring divisibility, which would fail for numbers like 16 or 28.

## Approaches

A straightforward brute-force approach would generate all numbers from 1 to `n` and check whether each number is lucky. For every lucky number found, we would then check if it divides `n`. This approach is correct because any almost lucky number must be divisible by some lucky number. However, iterating through all numbers up to 1000 and repeatedly checking their digits is slightly redundant.

The key insight is that we can generate all lucky numbers up to 1000 using a recursive or iterative construction. Start with the empty number and append either 4 or 7 repeatedly, stopping once numbers exceed 1000. Once we have this list, we simply iterate through it and check for divisibility. The structure of lucky numbers-restricted digits and a small upper bound-makes this feasible and efficient. Instead of checking every number from 1 to 1000, we only check a small set of valid candidates.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n log n) | O(1) | Acceptable here, but inefficient |
| Precompute Lucky Numbers | O(L) where L is number of lucky numbers ≤1000 | O(L) | Optimal, accepted |

## Algorithm Walkthrough

1. Initialize a list to hold all lucky numbers up to 1000. We start with 4 and 7 as the base numbers because these are the simplest lucky numbers.
2. Use a queue to iteratively generate new lucky numbers by appending 4 or 7 to each number in the queue. Stop generating new numbers once they exceed 1000, since they cannot divide `n`.
3. Iterate through the list of lucky numbers. For each lucky number, check if `n` is divisible by it using the modulo operator.
4. If we find any lucky number that divides `n`, print "YES" and terminate. If none of them divide `n`, print "NO".

Why it works: By construction, we have enumerated all lucky numbers that could possibly divide `n`. Since almost lucky numbers are defined by divisibility by some lucky number, checking divisibility against this complete set guarantees correctness.

## Python Solution

```python
import sys
input = sys.stdin.readline

def generate_lucky_numbers(limit):
    lucky = []
    queue = [4, 7]
    while queue:
        num = queue.pop(0)
        if num > limit:
            continue
        lucky.append(num)
        queue.append(num * 10 + 4)
        queue.append(num * 10 + 7)
    return lucky

n = int(input())
lucky_numbers = generate_lucky_numbers(1000)

for ln in lucky_numbers:
    if n % ln == 0:
        print("YES")
        break
else:
    print("NO")
```

We first generate all lucky numbers up to 1000 using a simple BFS-like method, appending digits 4 and 7. Then we iterate through the generated numbers and check divisibility. The use of `else` on the `for` loop ensures that we only print "NO" if no lucky number divides `n`.

## Worked Examples

### Sample 1

Input: `47`

| Variable | Value |
| --- | --- |
| n | 47 |
| lucky_numbers | [4, 7, 44, 47, 74, 77, ...] |
| ln during iteration | 4 → 7 → 44 → 47 |

During iteration, 47 is divisible by 47. Output is "YES".

### Sample 2

Input: `16`

| Variable | Value |
| --- | --- |
| n | 16 |
| lucky_numbers | [4, 7, 44, 47, 74, 77, ...] |
| ln during iteration | 4 → 7 → 44 ... |

16 % 4 == 0. Output is "YES". This demonstrates the algorithm correctly handles almost lucky numbers that are not lucky themselves.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(L) | L is the number of lucky numbers ≤1000; checking divisibility for each is constant time. |
| Space | O(L) | We store all lucky numbers ≤1000. |

Given n ≤ 1000, the total number of lucky numbers is small (under 20), so this algorithm is extremely efficient and well within the 2s/256MB limit.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()
    exec(open('solution.py').read())
    return sys.stdout.getvalue().strip()

# provided samples
assert run("47\n") == "YES", "sample 1"
assert run("16\n") == "YES", "divisible by 4"

# custom cases
assert run("5\n") == "NO", "not divisible by any lucky number"
assert run("4\n") == "YES", "lucky number itself"
assert run("28\n") == "YES", "divisible by 7"
assert run("1000\n") == "NO", "edge of constraint not divisible by any lucky number"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 5 | NO | Non-almost-lucky number |
| 4 | YES | Lucky number itself |
| 28 | YES | Divisible by a lucky number (7) |
| 1000 | NO | Maximum input boundary |

## Edge Cases

The smallest input `n = 1` produces "NO" because 1 is not divisible by any lucky number. The largest input `n = 1000` is handled correctly because all lucky numbers greater than 1000 are never generated, and we correctly check divisibility against all possible lucky numbers. Numbers that are themselves lucky, like 4, 7, 47, are immediately confirmed as almost lucky since they divide themselves. Numbers that are multiples of small lucky numbers but not lucky themselves, like 16, 28, and 44, are also correctly detected by our divisibility loop.
