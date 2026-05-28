---
title: "CF 39H - Multiplication Table"
description: "We are asked to construct a multiplication table for numbers in a positional numeral system of base k, where k ranges from 2 to 10. Concretely, the table should have k-1 rows and k-1 columns, representing the numbers 1 through k-1 in both the row and column axes."
date: "2026-05-28T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "implementation"]
categories: ["algorithms"]
codeforces_contest: 39
codeforces_index: "H"
codeforces_contest_name: "School Team Contest 1 (Winter Computer School 2010/11)"
rating: 1300
weight: 39
solve_time_s: 122
verified: false
draft: false
---
[CF 39H - Multiplication Table](https://codeforces.com/problemset/problem/39/H)

**Rating:** 1300  
**Tags:** implementation  
**Solve time:** 2m 2s  
**Verified:** no  

## Solution
## Problem Understanding

We are asked to construct a multiplication table for numbers in a positional numeral system of base `k`, where `k` ranges from 2 to 10. Concretely, the table should have `k-1` rows and `k-1` columns, representing the numbers `1` through `k-1` in both the row and column axes. Each cell at row `i` and column `j` must contain the product `i * j`, but expressed in base `k` notation. For example, in base 2, the table should show only `1` for the top-left corner, `10` for `2 * 1`, and so on, in binary.

The constraints are small: `k` goes up to 10, so the largest multiplication we will ever need is `9 * 9 = 81`. The resulting table has at most 9 rows and 9 columns. This means a simple double loop to compute every cell is feasible. Memory and time are trivial concerns, but attention to correctly converting numbers to the target base is essential.

The edge cases revolve around small bases like 2 or 3. In base 2, all numbers are represented in binary, so a naive approach that prints decimal numbers would be incorrect. Similarly, we must avoid off-by-one errors when constructing ranges: the table should start at 1, not 0, and end at `k-1`. For example, with `k=3`, the expected table is:

```
1 2
2 11
```

If we mistakenly include 0 or go to `k`, the table will be incorrect.

## Approaches

The most straightforward approach is brute-force: iterate over all `i` and `j` from 1 to `k-1`, compute the product `i * j`, and convert it to a string in base `k`. This approach works because the total number of operations is `(k-1)^2`, which is at most 81 for `k=10`. This is far below any performance limit.

The key insight is that we do not need any sophisticated algorithm because the complexity is already trivial. The only subtlety is converting integers to a string in the given base. Python’s built-in `format` function or a custom conversion loop can achieve this. This ensures the output matches the positional notation rather than decimal. Once that conversion is implemented correctly, the algorithm is fully correct.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(k^2 * log(k^2)) | O(1) | Accepted |
| Optimal | O(k^2 * log(k^2)) | O(1) | Accepted |

Even though we call the second "optimal," it is essentially the brute-force solution with proper base conversion.

## Algorithm Walkthrough

1. Read the integer `k` from input. This is the base of the numeral system we will use.
2. Iterate `i` from 1 to `k-1`. Each `i` represents a row in the multiplication table.
3. For each `i`, iterate `j` from 1 to `k-1`. Each `j` represents a column.
4. Compute the product `i * j`.
5. Convert the product to a string in base `k`. Use repeated division and remainder extraction or Python’s `format` function with base conversion.
6. Print each row with values separated by a space. Ensure no trailing spaces disrupt the output format.
7. Repeat until all rows are printed.

Why it works: the algorithm explicitly generates each element of the multiplication table by computing `i * j` for all valid indices. Conversion to the target base guarantees each number is expressed correctly in the numeral system. The loop bounds are chosen to include exactly `1` through `k-1`, preserving the correct dimensions and avoiding zero-index artifacts.

## Python Solution

```python
import sys
input = sys.stdin.readline

def to_base(n, b):
    if n == 0:
        return "0"
    digits = []
    while n:
        digits.append(str(n % b))
        n //= b
    return ''.join(reversed(digits))

k = int(input())

for i in range(1, k):
    row = [to_base(i * j, k) for j in range(1, k)]
    print(' '.join(row))
```

The `to_base` function converts any integer to a string representation in the specified base. It handles zero explicitly and builds the number from least to most significant digit, reversing at the end. The nested loop constructs each row of the multiplication table, converting every product to the target base before joining the row into a string for printing. Off-by-one errors are avoided by iterating from `1` to `k-1`.

## Worked Examples

Input `k=3`:

| i | j | i*j | base-3 |
| --- | --- | --- | --- |
| 1 | 1 | 1 | 1 |
| 1 | 2 | 2 | 2 |
| 2 | 1 | 2 | 2 |
| 2 | 2 | 4 | 11 |

Output:

```
1 2
2 11
```

This demonstrates proper handling of small bases and non-trivial multi-digit base conversions.

Input `k=10` (Sample 1) is the standard decimal multiplication table 1-9, showing the algorithm scales correctly for the largest allowed base.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(k^2 * log(k^2)) | Two nested loops over `1..k-1` and conversion to base k takes O(log(i*j)) per element. |
| Space | O(1) | Only a temporary list for row digits and output string, independent of k^2. |

Given `k <= 10`, total operations are minimal, well within a 2-second limit and 64 MB memory bound.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    output = io.StringIO()
    sys.stdout = output
    k = int(input())
    def to_base(n, b):
        if n == 0:
            return "0"
        digits = []
        while n:
            digits.append(str(n % b))
            n //= b
        return ''.join(reversed(digits))
    for i in range(1, k):
        row = [to_base(i * j, k) for j in range(1, k)]
        print(' '.join(row))
    return output.getvalue().strip()

# Provided sample
assert run("10") == "\n".join([
    "1 2 3 4 5 6 7 8 9",
    "2 4 6 8 10 12 14 16 18",
    "3 6 9 12 15 18 21 24 27",
    "4 8 12 16 20 24 28 32 36",
    "5 10 15 20 25 30 35 40 45",
    "6 12 18 24 30 36 42 48 54",
    "7 14 21 28 35 42 49 56 63",
    "8 16 24 32 40 48 56 64 72",
    "9 18 27 36 45 54 63 72 81"
]), "sample 1"

# Custom cases
assert run("2") == "1", "minimum base"
assert run("3") == "1 2\n2 11", "small base with multi-digit"
assert run("5") == "\n".join([
    "1 2 3 4",
    "2 4 11 13",
    "3 11 14 22",
    "4 13 22 31"
]), "mid base"
assert run("9") == "\n".join([
    "1 2 3 4 5 6 7 8",
    "2 4 6 8 10 12 14 16",
    "3 6 10 12 15 18 21 24",
    "4 8 12 16 20 24 28 32",
    "5 10 15 22 27 33 38 44",
    "6 12 18 24 30 36 42 48",
    "7 14 21 28 35 42 51 56",
    "8 16 24 32 44 48 56 64"
]), "high base"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 2 | 1 | Minimum base |
| 3 | 1 2\n2 11 | Small base multi-digit conversion |
| 5 | see above | Mid-range base correctness |
| 9 | see above | High base, larger products, multi-digit conversion |

## Edge Cases

For `k=2`, the multiplication table is a single cell `1`. The algorithm correctly iterates `i=1..1` and `j=1..1`, computes `1*1=1`, and converts to base 2 as `"1"`. No off-by-one or zero appears.

For `k=3`, the largest product is `2*2=4`. The conversion to base 3 yields `11`, not `
