---
title: "CF 1177B - Digits Sequence (Hard Edition)"
description: "We are asked to consider the infinite string formed by writing all positive integers consecutively without any separators: \"1234567891011121314…\". Given a position $k$, we must determine which digit occupies that place."
date: "2026-06-12T01:43:28+07:00"
tags: ["codeforces", "competitive-programming", "binary-search", "divide-and-conquer", "implementation"]
categories: ["algorithms"]
codeforces_contest: 1177
codeforces_index: "B"
codeforces_contest_name: "Testing Round 15 (Unrated)"
rating: 1800
weight: 1177
solve_time_s: 92
verified: true
draft: false
---

[CF 1177B - Digits Sequence (Hard Edition)](https://codeforces.com/problemset/problem/1177/B)

**Rating:** 1800  
**Tags:** binary search, divide and conquer, implementation  
**Solve time:** 1m 32s  
**Verified:** yes  

## Solution
## Problem Understanding

We are asked to consider the infinite string formed by writing all positive integers consecutively without any separators: "1234567891011121314…". Given a position $k$, we must determine which digit occupies that place. The input is a single integer $k$ up to $10^{12}$, and the output is the corresponding digit.

The first observation is that the sequence is implicitly structured by the length of the numbers. Single-digit numbers occupy positions 1 through 9. Two-digit numbers occupy positions 10 through 189, three-digit numbers occupy positions 190 through 2889, and so on. This layering by digit length is essential for efficiency. A naive approach that constructs the string up to $k$ would require storing up to $10^{12}$ digits, which is infeasible in memory and too slow to generate in a reasonable time.

An important edge case occurs near boundaries between digit lengths. For example, if $k = 10$, the digit belongs to "10", the first two-digit number. A naive implementation that counts digits without considering length groups may miscount and select the wrong digit.

Another subtle case occurs when $k$ lands exactly on the last digit of a length group, for instance $k = 9$ or $k = 189$. These positions correspond to the last digit of 1-digit or 2-digit numbers. Handling boundaries carefully prevents off-by-one errors.

## Approaches

The brute-force approach is straightforward: start from 1 and append each number as a string until the total length reaches $k$. Then return the $k$-th character. This is correct, because we literally simulate the sequence. The problem arises in performance. For $k$ near $10^{12}$, generating digits one by one would require at least $10^{12}$ operations, far beyond practical limits for a 1-second time limit.

The key insight for an optimal solution is that the sequence is structured in blocks of numbers with equal digit lengths. Numbers with $d$ digits occupy a contiguous block of length $d \times 9 \times 10^{d-1}$. By computing the lengths of these blocks cumulatively, we can determine which block contains the $k$-th digit without generating the entire sequence. Once the block is identified, integer division and modulo arithmetic locate the exact number and digit within that number. This reduces the problem from linear in $k$ to logarithmic in the number of digit lengths, which is acceptable for $k$ up to $10^{12}$.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(k) | O(k) | Too slow |
| Optimal | O(log k) | O(1) | Accepted |

## Algorithm Walkthrough

1. Initialize a digit length counter `d = 1` and the starting number for this length `start = 1`. Initialize a cumulative length counter `count = 0` to track total digits processed so far.
2. Compute the length of the current block of `d`-digit numbers as `block_len = 9 * 10^(d-1) * d`. If adding `block_len` to `count` keeps `count < k`, increment `d` and update `count += block_len`. Repeat until the block containing `k` is found.
3. Once the correct digit length `d` is found, compute the offset of `k` within the block: `offset = k - count - 1`. The `-1` converts the position to zero-based indexing within the block.
4. Determine which number within the block contains the desired digit using integer division: `number_index = offset // d`. The actual number is `number = 10^(d-1) + number_index`.
5. Determine which digit within this number is the target using modulo: `digit_index = offset % d`. Extract the digit by converting the number to a string and indexing: `str(number)[digit_index]`.
6. Output the digit as the answer.

Why it works: At each step, we maintain the invariant that `count` tracks the total number of digits covered by all smaller blocks. By identifying the block length `d` that contains `k`, and using integer division and modulo, we precisely map the global position `k` to a number and digit within that number. There is no ambiguity because numbers in each block are consecutive and uniformly sized.

## Python Solution

```python
import sys
input = sys.stdin.readline

k = int(input())

d = 1
count = 0

while True:
    block_len = 9 * (10 ** (d - 1)) * d
    if count + block_len >= k:
        break
    count += block_len
    d += 1

offset = k - count - 1
number_index = offset // d
digit_index = offset % d
number = 10 ** (d - 1) + number_index
print(str(number)[digit_index])
```

The code follows the algorithm exactly. The `while` loop searches for the correct digit length block by accumulating `count`. The zero-based indexing `offset = k - count - 1` ensures that integer division and modulo correctly locate the number and digit. Conversion to string is safe because numbers have at most 12 digits (since `k ≤ 10^12`) and fits comfortably in Python integers.

## Worked Examples

Sample 1: `k = 7`

| Variable | Value |
| --- | --- |
| d | 1 |
| count | 0 |
| block_len | 9 |
| offset | 6 |
| number_index | 6 |
| number | 7 |
| digit_index | 0 |
| output | 7 |

The trace confirms that `k=7` falls within the 1-digit numbers, precisely mapping to number 7, digit 0.

Sample 2: `k = 12`

| Variable | Value |
| --- | --- |
| d | 2 |
| count | 9 |
| block_len | 180 |
| offset | 2 |
| number_index | 1 |
| number | 10 + 1 = 11 |
| digit_index | 0 |
| output | 1 |

This trace demonstrates handling the transition from 1-digit to 2-digit numbers correctly. The offset calculation maps the global position to the proper number and digit.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(log k) | Each iteration multiplies the starting number by 10, so the number of digit lengths considered is at most 12 for `k ≤ 10^12`. All subsequent calculations are constant time. |
| Space | O(1) | Only integer variables are stored, no large arrays or strings. |

Given the constraints, this fits comfortably within the 1-second time limit and 256 MB memory limit.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    k = int(input())
    d = 1
    count = 0
    while True:
        block_len = 9 * (10 ** (d - 1)) * d
        if count + block_len >= k:
            break
        count += block_len
        d += 1
    offset = k - count - 1
    number_index = offset // d
    digit_index = offset % d
    number = 10 ** (d - 1) + number_index
    return str(number)[digit_index]

# provided samples
assert run("7") == "7", "sample 1"

# custom cases
assert run("1") == "1", "first digit"
assert run("10") == "1", "transition from 1-digit to 2-digit"
assert run("190") == "1", "
```
