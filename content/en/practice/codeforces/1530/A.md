---
title: "CF 1530A - Binary Decimal"
description: "The problem asks us to break a positive integer $n$ into a sum of numbers whose decimal digits are only 0 or 1. These numbers are called binary decimals, like 1, 10, 11, 101, 1000. The goal is to determine the smallest number of such binary decimals that sum up to $n$."
date: "2026-06-10T16:53:26+07:00"
tags: ["codeforces", "competitive-programming", "greedy", "math"]
categories: ["algorithms"]
codeforces_contest: 1530
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 733 (Div. 1 + Div. 2, based on VK Cup 2021 - Elimination (Engine))"
rating: 800
weight: 1530
solve_time_s: 124
verified: true
draft: false
---

[CF 1530A - Binary Decimal](https://codeforces.com/problemset/problem/1530/A)

**Rating:** 800  
**Tags:** greedy, math  
**Solve time:** 2m 4s  
**Verified:** yes  

## Solution
## Problem Understanding

The problem asks us to break a positive integer $n$ into a sum of numbers whose decimal digits are only 0 or 1. These numbers are called binary decimals, like 1, 10, 11, 101, 1000. The goal is to determine the smallest number of such binary decimals that sum up to $n$. Each test case provides one integer $n$, and we need to output a single number per test case representing this minimal count.

The constraints allow $n$ up to $10^9$ and up to 1000 test cases. This means that any solution must run in roughly linear time per test case at worst. For example, an algorithm that iterates through all numbers less than $n$ would be too slow, as $n$ could be nearly a billion.

Edge cases arise when $n$ is very small, like 1 or 5, or when $n$ is itself a binary decimal. A naive greedy approach that just subtracts the largest binary decimal smaller than $n$ repeatedly could work but might be more complex than necessary. Careless approaches that try to directly build binary decimals without considering each digit separately will fail on numbers like 121 or 1102, producing too many pieces.

## Approaches

The brute-force approach would attempt to generate all binary decimals up to $n$ and try every combination that sums to $n$. This is clearly infeasible: for $n$ around $10^9$, there are thousands of binary decimals, and checking all combinations would require exponential time.

The key insight is that the minimal number of binary decimals needed to sum to $n$ is determined by the largest single decimal digit in $n$. Each digit $d_i$ in $n$ contributes $d_i$ "ones" in that decimal place. For example, the number 121 has digits 1, 2, 1. The maximum digit is 2, meaning we need at least two binary decimals to sum to 121. We can construct these by decomposing each digit vertically: take each digit and assign its value across as many binary decimals as the digit's maximum. This reduces the problem to a simple scan of digits.

This approach is greedy but optimal because each binary decimal can only contribute a 0 or 1 per decimal place. Therefore, no digit's contribution can be combined into fewer than the maximum digit.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(2^k) | O(k) | Too slow |
| Digit Scan Greedy | O(log n) | O(1) | Accepted |

## Algorithm Walkthrough

1. For each test case, read the integer $n$.
2. Convert $n$ to a string so that we can iterate over its decimal digits.
3. Initialize a variable `max_digit` to zero. This will track the largest digit in $n$.
4. Iterate over each character `c` in the string representation of $n$. Convert `c` to an integer `digit`.
5. If `digit` is larger than `max_digit`, update `max_digit` to `digit`.
6. After scanning all digits, `max_digit` represents the minimal number of binary decimals required.
7. Output `max_digit`.

Why it works: each binary decimal can only contribute a 1 or 0 in each decimal position. To reach a digit $d_i$ in position $i$, we need at least $d_i$ ones in that position across all binary decimals. Therefore, the maximal digit anywhere in the number dictates the minimal number of summands. This invariant guarantees correctness.

## Python Solution

```python
import sys
input = sys.stdin.readline

t = int(input())
for _ in range(t):
    n = input().strip()
    max_digit = max(int(c) for c in n)
    print(max_digit)
```

The solution reads the number of test cases, then iterates through each test case. Converting the number to a string avoids repeated division and modulo operations, simplifying digit extraction. Using `max(int(c) for c in n)` succinctly computes the maximum digit in one line. There are no off-by-one issues because digits are always between 0 and 9, and the input guarantees $n \ge 1$.

## Worked Examples

### Sample 1: `121`

| Step | n | Digit | max_digit |
| --- | --- | --- | --- |
| 1 | 121 | 1 | 1 |
| 2 | 121 | 2 | 2 |
| 3 | 121 | 1 | 2 |

The maximum digit is 2, so the answer is 2. This corresponds to the decomposition 110 + 11 or 111 + 10.

### Sample 2: `5`

| Step | n | Digit | max_digit |
| --- | --- | --- | --- |
| 1 | 5 | 5 | 5 |

The maximum digit is 5, so five binary decimals are needed, e.g., 1+1+1+1+1.

These traces show that scanning digits and taking the maximum directly yields the minimal number of summands.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(log n) per test case | Scans each decimal digit of n, which is O(log10 n) |
| Space | O(1) | Only stores `max_digit` and loop variables |

With $n \le 10^9$ and $t \le 1000$, the algorithm performs at most $1000 * 9 = 9000$ operations, well within the 1-second time limit.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    out = io.StringIO()
    sys.stdout = out
    
    t = int(input())
    for _ in range(t):
        n = input().strip()
        max_digit = max(int(c) for c in n)
        print(max_digit)
        
    sys.stdout = sys.__stdout__
    return out.getvalue().strip()

# Provided samples
assert run("3\n121\n5\n1000000000\n") == "2\n5\n1", "sample 1"

# Custom cases
assert run("1\n1\n") == "1", "minimum input"
assert run("1\n999\n") == "9", "maximum single-digit"
assert run("1\n101010\n") == "1", "alternating digits"
assert run("1\n111111111\n") == "1", "all ones"
assert run("1\n1203\n") == "3", "mixed digits, max in middle"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 | 1 | Minimum input |
| 999 | 9 | Maximum single-digit triggers correct max |
| 101010 | 1 | Alternating zeros and ones |
| 111111111 | 1 | All digits are ones |
| 1203 | 3 | Maximum digit in the middle |

## Edge Cases

For `n = 1`, the algorithm scans the single digit 1, sets `max_digit` to 1, and outputs 1. For `n = 1000000000`, the digits are mostly zeros with a leading 1, so the maximum digit is 1, yielding the correct single binary decimal. For `n = 1203`, digits are 1, 2, 0, 3; scanning sets `max_digit` to 3, ensuring the minimal number of summands equals the largest decimal digit. These cases confirm the algorithm handles minimal, maximal, and non-obvious digit placements correctly.
