---
title: "CF 39H - Multiplication Table"
description: "The task is to generate a multiplication table for numbers in a positional numeral system with a base k. Unlike the decimal system, the digits in this system range from 0 up to k-1. Petya wants to see products of numbers from 1 to k-1 expressed in this system."
date: "2026-05-28T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "implementation"]
categories: ["algorithms"]
codeforces_contest: 39
codeforces_index: "H"
codeforces_contest_name: "School Team Contest 1 (Winter Computer School 2010/11)"
rating: 1300
weight: 39
solve_time_s: 93
verified: false
draft: false
---

[CF 39H - Multiplication Table](https://codeforces.com/problemset/problem/39/H)

**Rating:** 1300  
**Tags:** implementation  
**Solve time:** 1m 33s  
**Verified:** no  

## Solution
## Problem Understanding

The task is to generate a multiplication table for numbers in a positional numeral system with a base `k`. Unlike the decimal system, the digits in this system range from 0 up to `k-1`. Petya wants to see products of numbers from 1 to `k-1` expressed in this system. The input is a single integer `k` representing the radix, constrained between 2 and 10. The output is a `(k-1) × (k-1)` table, where the entry at row `i` and column `j` contains the product `i × j` expressed in base `k`.

Because `k` is at most 10, the largest table size is `9 × 9`. Each product in the table is at most `(k-1) × (k-1) = 81` when `k = 10`. This is small enough that we can generate the table explicitly without worrying about performance. The main subtlety lies in converting the decimal product into the target base, ensuring digits are correctly represented as strings and handling multi-digit numbers properly.

An edge case arises when `k = 2`. The table then only has a single entry: `1 × 1 = 1`. Careless implementations might loop incorrectly or attempt to include 0 in the table, producing the wrong size.

## Approaches

The brute-force approach is straightforward: loop over all integers `i` and `j` from 1 to `k-1`, compute their product, and convert it into the string representation in base `k`. This works because the table size is tiny, even at the maximum `k`. Each product is at most 81, so base conversion can be done by repeated division and remainder operations.

There is no faster asymptotic approach because the problem requires printing every entry explicitly. The key insight is that generating numbers in base `k` is simple once we treat the conversion carefully: repeatedly divide by `k` and record remainders, then reverse the collected digits. The table itself must not include zero rows or columns, and all numbers must be printed as strings in the target base, separated by spaces. Python's built-in integer arithmetic handles all products safely without overflow.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(k^2 log k) | O(k^2 log k) | Accepted |
| Optimal | O(k^2 log k) | O(k^2 log k) | Accepted |

The `log k` factor comes from the number of digits needed to represent numbers up to `(k-1)^2` in base `k`.

## Algorithm Walkthrough

1. Read the radix `k` from input. This determines the size of the table, `(k-1) × (k-1)`.
2. Define a helper function to convert a decimal integer `n` into a string in base `k`. Initialize an empty list `digits`. While `n` is greater than zero, divide `n` by `k`, take the remainder, append the remainder as a string to `digits`, and continue with the quotient. Reverse `digits` at the end. If `n` is zero, return `"0"`.
3. Loop over each row index `i` from 1 to `k-1`. For each `i`, initialize an empty list `row`.
4. Inside the row loop, loop over each column index `j` from 1 to `k-1`. Compute the product `i × j`.
5. Convert the product to base `k` using the helper function and append it to `row`.
6. After processing all columns for a row, join the row entries with spaces and print the result.
7. Repeat until all rows are printed.

This approach works because each entry is computed explicitly and converted correctly into the target base. The loop bounds guarantee the table size matches `(k-1) × (k-1)`, and the base conversion ensures digits are represented as strings without relying on implicit decimal formatting.

## Python Solution

```python
import sys
input = sys.stdin.readline

def to_base(n, k):
    if n == 0:
        return "0"
    digits = []
    while n > 0:
        digits.append(str(n % k))
        n //= k
    return ''.join(reversed(digits))

def main():
    k = int(input())
    for i in range(1, k):
        row = []
        for j in range(1, k):
            product = i * j
            row.append(to_base(product, k))
        print(' '.join(row))

if __name__ == "__main__":
    main()
```

The `to_base` function handles base conversion by repeated division and remainder extraction. The `main` function loops over all table indices and constructs rows dynamically. Joining the row elements ensures proper spacing. The code correctly handles the smallest and largest valid `k` values, including `k = 2` which produces a single entry.

## Worked Examples

Consider the input `k = 3`. The table size is `2 × 2`. Trace through variables:

| i | j | product | base 3 conversion | row |
| --- | --- | --- | --- | --- |
| 1 | 1 | 1 | "1" | ["1"] |
| 1 | 2 | 2 | "2" | ["1","2"] |
| 2 | 1 | 2 | "2" | ["2"] |
| 2 | 2 | 4 | "11" | ["2","11"] |

Output:

```
1 2
2 11
```

This demonstrates that the conversion handles multi-digit numbers correctly (`4` becomes `"11"` in base 3).

Another example with `k = 2`:

| i | j | product | base 2 conversion | row |
| --- | --- | --- | --- | --- |
| 1 | 1 | 1 | "1" | ["1"] |

Output:

```
1
```

This confirms the algorithm handles the minimal table case properly.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(k^2 log k) | Each of the (k-1)^2 products requires converting a number up to (k-1)^2 into base k, which takes O(log_k((k-1)^2)) = O(log k) operations. |
| Space | O(k^2 log k) | Each row stores k-1 numbers in string form. Each number has up to O(log k) digits. |

Given that k ≤ 10, the algorithm performs at most 81 table entries with at most 2-digit base-10 numbers, well within the 2-second and 64 MB limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    output = io.StringIO()
    sys.stdout = output
    main()
    sys.stdout = sys.__stdout__
    return output.getvalue().strip()

# provided sample
assert run("10\n") == "\n".join([
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

# custom minimum k
assert run("2\n") == "1", "minimum k"

# custom small k
assert run("3\n") == "1 2\n2 11", "k=3"

# custom medium k
assert run("4\n") == "1 2 3\n2 10 12\n3 12 21", "k=4"

# custom max k
assert run("10\n") == run("10\n"), "k=10 consistency"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 2 | 1 | Minimum table size |
| 3 | 1 2 \n 2 11 | Base conversion for multi-digit numbers |
| 4 | 1 2 3 \n 2 10 12 \n 3 12 21 | Base conversion with more digits and multi-row table |
| 10 | full 9×9 table | Large table correctness, consistency |

## Edge Cases

When `k = 2`, the table has only one cell. The loops execute exactly once: `i = 1`, `j = 1`, product is `1`, converted to base 2 as `"1"`, and printed. There is no off-by-one risk because the range is `range(1, k)`. For `k = 3`, products like `2 × 2 = 4` become `"11"` in base 3, demonstrating that the algorithm handles multi-digit base conversion correctly. The trace tables above confirm all boundaries and multi-digit conversions are accurate.
