---
title: "CF 1177A - Digits Sequence (Easy Edition)"
description: "We are given a single positive integer $k$, and we imagine writing all positive integers in order, starting from 1, directly next to each other without spaces or separators. This produces one continuous digit stream like 12345678910111213... and so on."
date: "2026-06-13T10:23:58+07:00"
tags: ["codeforces", "competitive-programming", "implementation"]
categories: ["algorithms"]
codeforces_contest: 1177
codeforces_index: "A"
codeforces_contest_name: "Testing Round 15 (Unrated)"
rating: 1000
weight: 1177
solve_time_s: 303
verified: true
draft: false
---

[CF 1177A - Digits Sequence (Easy Edition)](https://codeforces.com/problemset/problem/1177/A)

**Rating:** 1000  
**Tags:** implementation  
**Solve time:** 5m 3s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a single positive integer $k$, and we imagine writing all positive integers in order, starting from 1, directly next to each other without spaces or separators. This produces one continuous digit stream like 12345678910111213... and so on. The task is to determine which digit appears at position $k$ in this infinite stream when counting from the left starting at 1.

The key challenge is that the sequence grows very quickly in length, but in a structured way. Numbers with one digit contribute 9 digits, numbers with two digits contribute 90 numbers times 2 digits each, numbers with three digits contribute 900 numbers times 3 digits each, and so on. This structure means we never actually need to construct the full string.

The constraint $k \le 10000$ is small enough that even a naive simulation up to that many digits might pass, but the intended reasoning scales to much larger inputs and avoids constructing strings entirely. Any approach that explicitly builds the concatenated string risks unnecessary overhead and confusion around indexing.

A subtle edge case arises around boundaries between digit-length blocks. For example, when $k = 9$, the answer is 9, but when $k = 10$, we move to the number 10 and must correctly extract the first digit of a multi-digit number. A naive incremental string builder can easily misalign indices at these transitions.

## Approaches

A brute-force approach directly constructs the sequence by repeatedly converting integers to strings and appending them until the length exceeds $k$. Once the full string is built, we simply index into it. This works because Python string concatenation and integer-to-string conversion are correct operations for this problem. However, the cost comes from repeatedly growing a string, which leads to total work proportional to the final constructed length. While $k \le 10000$ keeps this manageable here, the method becomes inefficient if $k$ grows.

The more principled approach avoids building the string entirely. Instead, we reason in blocks of numbers with the same digit length. We first determine whether the $k$-th digit lies in the block of 1-digit numbers, 2-digit numbers, 3-digit numbers, and so on. Each block contributes a known number of digits, so we subtract block sizes until we locate the correct range. Once we know the correct block, we identify the exact number and then extract the required digit using arithmetic rather than string concatenation.

This works because the sequence is structured in contiguous, uniform segments where digit counts are predictable.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(k)$ | $O(k)$ | Accepted for this constraint |
| Optimal | $O(\log k)$ | $O(1)$ | Accepted |

## Algorithm Walkthrough

We build the solution by progressively narrowing down where the $k$-th digit lies.

1. Start with digit length $d = 1$, representing numbers from 1 to 9. We compute how many digits this block contributes as $9 \cdot d$. If $k$ is larger than this, we subtract it and move to the next block.
2. Increase $d$ to 2, then consider numbers from 10 to 99. This block contributes $90 \cdot 2$ digits. If $k$ is still larger than this block, subtract again and continue.
3. Repeat this process for increasing digit lengths. At each step, we are effectively skipping entire uniform layers of the number system, which avoids examining individual numbers.
4. Once we find the first block where $k$ is within its total digit contribution, we identify the exact number inside that block. We compute how many full numbers into the block we need to go using integer division, and then locate the exact digit inside that number using modulo.
5. Convert the identified number to a string and extract the correct character.

The key reason this works is that each block is contiguous and has constant digit width, so we can map global digit positions into local coordinates inside a specific range of integers.

### Why it works

At every step, we maintain the invariant that $k$ represents the offset into a suffix of the digit sequence starting at some digit-length block. Each subtraction removes an entire complete and correctly accounted prefix. Because blocks do not overlap and fully partition the sequence, once we stop, $k$ must lie within a single digit-length region. Inside that region, each number contributes exactly $d$ digits, so arithmetic mapping from index to number is exact and lossless.

## Python Solution

```python
import sys
input = sys.stdin.readline

k = int(input().strip())

digit_len = 1
count = 9
start = 1

while k > digit_len * count:
    k -= digit_len * count
    digit_len += 1
    count *= 10
    start *= 10

num = start + (k - 1) // digit_len
idx = (k - 1) % digit_len

print(str(num)[idx])
```

The implementation mirrors the block-by-block reasoning. The variables `digit_len`, `count`, and `start` track the current segment of numbers we are analyzing. `digit_len * count` gives the total number of digits in the current block. We subtract entire blocks until we find the correct range.

Once inside the correct block, `(k - 1) // digit_len` gives the offset in terms of full numbers, and `(k - 1) % digit_len` gives the position inside that number. Subtracting 1 before division and modulo is essential to correctly handle 1-based indexing.

## Worked Examples

### Example 1: k = 7

| Step | digit_len | count | block_size | remaining k |
| --- | --- | --- | --- | --- |
| initial | 1 | 9 | 9 | 7 |

We do not subtract anything since 7 lies in the first block of 1-digit numbers. The number is 7 itself, and the digit is 7. This confirms that early positions map directly to single-digit integers without transformation.

### Example 2: k = 12

| Step | digit_len | count | block_size | remaining k |
| --- | --- | --- | --- | --- |
| 1-digit | 1 | 9 | 9 | 3 |
| 2-digit | 2 | 90 | 180 | 3 |

After removing the 9 digits from the 1-digit block, we have $k = 3$ inside the 2-digit block starting at 10. The third digit in the sequence 101112... corresponds to number 11, and within it we take the first digit, which is 1.

This trace shows how the algorithm cleanly transitions across digit-length boundaries without constructing the sequence.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(\log k)$ | We iterate over digit lengths, and each step skips an exponentially growing block of numbers |
| Space | $O(1)$ | We only store a constant number of counters and compute digits on demand |

The constraints allow up to $k = 10000$, and the algorithm runs in constant time relative to that range because the number of digit-length blocks is at most 5. This is far below any time limit concerns.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    return solution()

def solution():
    import sys
    input = sys.stdin.readline
    k = int(input().strip())

    digit_len = 1
    count = 9
    start = 1

    while k > digit_len * count:
        k -= digit_len * count
        digit_len += 1
        count *= 10
        start *= 10

    num = start + (k - 1) // digit_len
    idx = (k - 1) % digit_len
    return str(num)[idx]

# provided sample
assert run("7\n") == "7"

# boundary: end of first block
assert run("9\n") == "9"

# transition into two-digit numbers
assert run("10\n") == "1"

# within two-digit block
assert run("12\n") == "1"

# larger position
assert run("15\n") == "2"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 9 | 9 | boundary of 1-digit block |
| 10 | 1 | first digit of 10 |
| 12 | 1 | correct indexing inside 2-digit block |
| 15 | 2 | mid-block correctness |

## Edge Cases

One edge case occurs exactly at block transitions, such as $k = 9$ or $k = 10$. For $k = 9$, the algorithm stays in the 1-digit block and returns 9 directly. For $k = 10$, we subtract the full 1-digit block, leaving $k = 1$ in the 2-digit block. The computed number becomes 10, and index 0 is extracted, correctly producing 1.

Another subtle case is when $k$ lands on the last digit of a multi-digit number, such as $k = 11$, which corresponds to the second digit of 10, yielding 0. The arithmetic indexing ensures that modulo computation correctly selects the last character of the string representation without any off-by-one error.
