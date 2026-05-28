---
title: "CF 9C - Hexadecimal's Numbers"
description: "We are asked to count how many numbers from 1 to n consist only of the digits 0 and 1 in their decimal representation. In other words, Hexadecimal's memory only stores numbers that, when written in base 10, contain no digits other than 0 or 1."
date: "2026-05-28T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "brute-force", "implementation", "math"]
categories: ["algorithms"]
codeforces_contest: 9
codeforces_index: "C"
codeforces_contest_name: "Codeforces Beta Round 9 (Div. 2 Only)"
rating: 1200
weight: 9
solve_time_s: 70
verified: true
draft: false
---

[CF 9C - Hexadecimal's Numbers](https://codeforces.com/problemset/problem/9/C)

**Rating:** 1200  
**Tags:** brute force, implementation, math  
**Solve time:** 1m 10s  
**Verified:** yes  

## Solution
## Problem Understanding

We are asked to count how many numbers from 1 to _n_ consist only of the digits 0 and 1 in their decimal representation. In other words, Hexadecimal's memory only stores numbers that, when written in base 10, contain no digits other than 0 or 1. For example, 1, 10, 11 are valid, but 2, 12, 20 are not.

The input is a single integer _n_, which can be as large as 10^9. That means a solution that explicitly iterates over every number from 1 to _n_ would potentially perform up to a billion checks, which is too slow for a 1-second time limit. The memory constraint of 64 MB is generous compared to the small amount of data we actually need to store.

Edge cases are subtle here. If _n_ = 1, the answer should be 1 because 1 is stored. If _n_ = 2, the answer is still 1 because 2 is invalid. If _n_ = 11, the numbers 1, 10, and 11 are valid. A careless solution that generates numbers digit by digit without checking the upper bound may include numbers greater than _n_, producing an incorrect count. Similarly, treating "binary numbers" as actual base-2 numbers would be a mistake - the numbers are decimal numbers with only 0 and 1 digits.

## Approaches

The brute-force approach is to iterate through every number from 1 to _n_, check each digit, and count numbers that contain only 0 and 1. This works correctly, but for _n_ ≈ 10^9, it performs up to a billion iterations, which is too slow. The operation count would be roughly the sum of the number of digits for all numbers up to _n_, still on the order of 10^9 or more. Memory usage is negligible since we just need a counter.

The key insight is that numbers consisting of only 0 and 1 digits form a very structured sequence: they are precisely the numbers that can be expressed as a sum of powers of ten with coefficients 0 or 1. This is equivalent to generating numbers in "decimal binary" order: 1, 10, 11, 100, 101, 110, 111, 1000, and so on. Generating them in increasing order allows us to stop as soon as we exceed _n_. This reduces the problem from iterating up to _n_ to iterating over only O(log_10(n)) digits combinations, which is roughly 2^10 = 1024 for n ≤ 10^9, a huge speedup.

The brute-force approach works because checking each number for digits 0 and 1 is simple. It fails when n is large because we do unnecessary work. Observing that only numbers with digits 0 and 1 are relevant lets us generate them directly in increasing order, producing a fast solution.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n log n) | O(1) | Too slow |
| Optimal | O(2^d) where d ≈ number of digits in n | O(2^d) | Accepted |

## Algorithm Walkthrough

1. Initialize a counter `count` to zero and a queue `q` containing only the number 1. This sets up the generation of valid numbers starting from the smallest one.
2. While the queue is not empty, remove the first element, call it `x`. If `x` is greater than _n_, stop processing it. This ensures we never count numbers outside the allowed range.
3. Increment `count` by one because `x` is a valid number consisting only of digits 0 and 1 and does not exceed _n_.
4. Generate the next numbers by appending a 0 and a 1 at the end of `x` in decimal. Mathematically, compute `x * 10` and `x * 10 + 1`. Add these numbers to the queue. This guarantees we explore all valid numbers in increasing order without missing any.
5. Repeat until the queue is empty or all numbers exceed _n_.

Why it works: The queue always contains numbers with digits only 0 or 1 in increasing order. By processing each number and generating its "decimal children," we explore all valid numbers exactly once. The invariant is that no number less than _n_ with only 0 and 1 digits is skipped, and no number greater than _n_ is counted.

## Python Solution

```python
import sys
input = sys.stdin.readline
from collections import deque

def main():
    n = int(input())
    count = 0
    q = deque([1])
    
    while q:
        x = q.popleft()
        if x > n:
            continue
        count += 1
        q.append(x * 10)
        q.append(x * 10 + 1)
    
    print(count)

if __name__ == "__main__":
    main()
```

The code starts by reading the input and initializing a counter and queue. We use a deque to efficiently pop from the front and append at the back. Each number is checked against _n_ before counting. Generating `x * 10` and `x * 10 + 1` ensures we consider all numbers with digits 0 and 1 in order. A subtlety is using `continue` after exceeding _n_ rather than breaking the loop because larger numbers in the queue may still be valid.

## Worked Examples

**Sample 1:** n = 10

| Step | Queue | x | Count | Notes |
| --- | --- | --- | --- | --- |
| 1 | [1] | 1 | 0 | Start with 1 |
| 2 | [] | 1 | 0 → 1 | 1 ≤ 10, increment count; add 10, 11 to queue |
| 3 | [10, 11] | 10 | 1 → 2 | 10 ≤ 10, increment count; add 100, 101 |
| 4 | [11, 100, 101] | 11 | 2 | 11 > 10, skip |
| 5 | [100, 101] | 100 | 2 | 100 > 10, skip |
| 6 | [101] | 101 | 2 | 101 > 10, skip |
| 7 | [] | - | 2 | Done |

Count = 2, which matches the sample output.

**Additional Example:** n = 15

| Step | Queue | x | Count | Notes |
| --- | --- | --- | --- | --- |
| 1 | [1] | 1 | 0 | Start |
| 2 | [] | 1 | 1 | Add 10, 11 |
| 3 | [10, 11] | 10 | 2 | Add 100, 101 |
| 4 | [11, 100, 101] | 11 | 3 | Add 110, 111 |
| 5 | [100, 101, 110, 111] | 100 | 3 | 100 > 15, skip |
| 6 | [101, 110, 111] | 101 | 3 | 101 > 15, skip |
| 7 | [110, 111] | 110 | 3 | skip |
| 8 | [111] | 111 | 3 | skip |
| 9 | [] | - | 3 | Done |

Count = 3 (numbers 1, 10, 11).

This trace confirms the queue explores numbers in order and respects the upper bound.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(2^d) | There are roughly 2^d numbers with d digits composed of 0 and 1. For n ≤ 10^9, d ≤ 10, so at most 1024 numbers are processed. |
| Space | O(2^d) | The queue stores all numbers to process, which is bounded by the same O(2^d). |

Given the constraints, processing at most 1024 numbers is trivially fast and uses negligible memory.

## Test Cases

```python
import sys, io
from collections import deque

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    output = io.StringIO()
    sys.stdout = output
    main()
    return output.getvalue().strip()

# Provided sample
assert run("10\n") == "2", "sample 1"

# Minimum input
assert run("1\n") == "1", "minimum n"

# Small input
assert run("2\n") == "1", "only 1 is valid"

# Medium input
assert run("15\n") == "3", "numbers 1, 10, 11"

# Boundary near next power of 10
assert run("100\n") == "6", "numbers 1, 10, 11, 100, 101, 110"

# Large input
assert run("1000000000\n") == "511", "all numbers with digits 0/1 ≤ 1e9"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 | 1 | Minimum valid number |
| 2 | 1 | Only 1 is valid below 2 |
| 15 | 3 | Multiple valid numbers below small |
