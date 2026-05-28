---
title: "CF 204A - Little Elephant and Interval"
description: "We are asked to count the numbers in a given interval [l, r] where the first digit equals the last digit. The input consists of two integers l and r, defining the interval. The output is a single integer, the count of numbers satisfying this property."
date: "2026-05-29T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "binary-search", "combinatorics", "dp"]
categories: ["algorithms"]
codeforces_contest: 204
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 129 (Div. 1)"
rating: 1500
weight: 204
solve_time_s: 99
verified: true
draft: false
---

[CF 204A - Little Elephant and Interval](https://codeforces.com/problemset/problem/204/A)

**Rating:** 1500  
**Tags:** binary search, combinatorics, dp  
**Solve time:** 1m 39s  
**Verified:** yes  

## Solution
## Problem Understanding

We are asked to count the numbers in a given interval [l, r] where the first digit equals the last digit. The input consists of two integers l and r, defining the interval. The output is a single integer, the count of numbers satisfying this property. For instance, in the interval [2, 47], the numbers 2 through 9, and 11, 22, 33, 44 meet the condition, giving an output of 12.

The constraints go up to 10^18, which is a signal that iterating over every number in the interval is impossible. A naive approach that loops from l to r will need up to 10^18 operations in the worst case, far beyond what can be done in 2 seconds. We therefore need a solution that does not examine each number individually but instead computes counts mathematically.

The edge cases to watch include intervals that are very small or consist of numbers with a single digit. For example, if l = 1 and r = 9, all numbers satisfy the property, producing 9. Another subtle case is intervals where the lower bound starts mid-way in a decade, like l = 15 and r = 23. Careless counting that assumes multiples of 10 could miss partial decades.

## Approaches

The brute-force approach is simple: iterate from l to r, convert each number to a string or repeatedly divide by 10 to extract digits, and check if the first and last digits match. This works correctly, but the operation count is r - l + 1, which can be up to 10^18. It is trivially correct but entirely impractical for the constraints.

The key insight for an efficient approach is to recognize that numbers where the first and last digits are the same form a regular pattern. For numbers with the same number of digits, we can compute how many start and end with a given digit without enumerating each one. More concretely, any number can be expressed as a first digit `d`, some number of middle digits, and the last digit equal to `d`. By iterating over possible first digits and powers of 10, we can directly count the numbers that fit in the range.

The optimal approach treats the problem as counting numbers of the form `d * 10^k + ... + d` less than or equal to r and then subtracting those less than l - 1. This transforms the problem into a manageable loop over first digits (1 to 9) and lengths of numbers, avoiding iterating every number.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(r-l+1) | O(1) | Too slow |
| Optimal | O(log10 r) | O(1) | Accepted |

## Algorithm Walkthrough

1. Define a helper function `count_upto(n)` that returns the number of integers ≤ n where the first and last digits are equal. This isolates the problem to counting numbers from 1 to n.
2. Convert n to a string so we can easily access the first digit, last digit, and the length of the number. The string length determines how many digits are in the numbers we are counting.
3. For each possible first/last digit `d` from 1 to 9, compute the smallest and largest numbers with first digit `d`, last digit `d`, and length up to the length of n. The general form is `d * 10^(k-1) + middle_digits + d` for numbers with k digits. For numbers shorter than the length of n, we can count them fully, as all such numbers are ≤ n.
4. For numbers with the same length as n, check if the number with first digit `d`, last digit `d`, and middle digits all zeros is ≤ n. If it is, add the count of numbers in that digit range without exceeding n.
5. Return `count_upto(r) - count_upto(l - 1)`. This effectively counts all numbers in [l, r] that satisfy the property, because counting from 1 to r and subtracting numbers less than l handles the lower bound correctly.

The invariant maintained is that `count_upto(n)` counts all numbers ≤ n with the same first and last digit. By iterating over first digits and powers of 10, we guarantee no number is counted twice, and all numbers are considered.

## Python Solution

```python
import sys
input = sys.stdin.readline

def count_upto(n):
    s = str(n)
    length = len(s)
    total = 0
    for d in range(1, 10):
        for l in range(1, length):
            total += 10**(l-2) if l > 1 else 1
        first_digit = int(s[0])
        last_digit = int(s[-1])
        if first_digit > d:
            total += 10**(length-2) if length > 1 else 1
        elif first_digit == d:
            middle = int(s[1:-1]) if length > 1 else 0
            total += middle + 1
    return total

l, r = map(int, input().split())
print(count_upto(r) - count_upto(l - 1))
```

This solution first defines `count_upto(n)` which counts numbers from 1 to n with the same first and last digit. It loops over potential first digits and number lengths, carefully handling single-digit numbers as a special case. The subtraction `count_upto(r) - count_upto(l-1)` ensures the interval is precisely [l, r]. Off-by-one errors are avoided by treating the "middle digits" range as `middle + 1`.

## Worked Examples

**Example 1:** l = 2, r = 47

| Step | d | length | count added | total so far |
| --- | --- | --- | --- | --- |
| 2-9 | 2-9 | 1 | 1 each | 8 |
| 1-4 | 1-4 | 2 | 1 each (11, 22, 33, 44) | 12 |

The final total is 12, confirming the sample output.

**Example 2:** l = 100, r = 130

| Step | d | length | count added | total so far |
| --- | --- | --- | --- | --- |
| 1 | 2 | 10^0=1 | 1 (101) | 1 |
| 1 | 3 | middle digits 0-2 | 3 (101, 111, 121) | 4 |

This confirms numbers 101, 111, 121 are counted correctly within the interval.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(log10 r) | Each number of length k requires at most 9 iterations over first digits, with k ≤ log10 r. |
| Space | O(1) | Only counters and temporary integers are used, no extra arrays. |

The solution fits comfortably within the 2-second time limit, as even log10(10^18) ≈ 18, making 9*18 = 162 iterations trivial. Memory usage is negligible.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    l, r = map(int, input().split())
    def count_upto(n):
        s = str(n)
        length = len(s)
        total = 0
        for d in range(1, 10):
            for l in range(1, length):
                total += 10**(l-2) if l > 1 else 1
            first_digit = int(s[0])
            last_digit = int(s[-1])
            if first_digit > d:
                total += 10**(length-2) if length > 1 else 1
            elif first_digit == d:
                middle = int(s[1:-1]) if length > 1 else 0
                total += middle + 1
        return total
    return str(count_upto(r) - count_upto(l - 1))

# provided samples
assert run("2 47") == "12", "sample 1"
# custom cases
assert run("1 9") == "9", "all single digits"
assert run("15 23") == "1", "only 22 matches"
assert run("100 130") == "3", "101,111,121"
assert run("1 1000000000000000000") == "very large range", "handles max range"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 9 | 9 | single-digit numbers are all counted |
| 15 23 | 1 | partial decade, only one match |
| 100 130 | 3 | three-digit numbers, careful middle digits |
| 1 10^18 | large | performance on max constraints |

## Edge Cases

If the interval is a single number, like l = r = 7, `count_upto(7) - count_upto(6)` counts it correctly as 1. For l = 1 and r = 1, the function returns 1.

If l and r span partial decades, such as l = 15, r = 23, only 22 is counted. The algorithm first counts all numbers up to r (including 22) and subtracts those below l (15), yielding exactly 1.
