---
title: "CF 1517A - Sum of 2050"
description: "We are asked to take a number $n$ and express it as a sum of numbers that are multiples of 2050 scaled by powers of ten. Concretely, the numbers we can use are 2050, 20500, 205000, 2050000, and so on. Each number in this sequence is exactly 2050 multiplied by a power of ten."
date: "2026-06-10T18:17:24+07:00"
tags: ["codeforces", "competitive-programming", "greedy", "math"]
categories: ["algorithms"]
codeforces_contest: 1517
codeforces_index: "A"
codeforces_contest_name: "Contest 2050 and Codeforces Round 718 (Div. 1 + Div. 2)"
rating: 800
weight: 1517
solve_time_s: 126
verified: true
draft: false
---

[CF 1517A - Sum of 2050](https://codeforces.com/problemset/problem/1517/A)

**Rating:** 800  
**Tags:** greedy, math  
**Solve time:** 2m 6s  
**Verified:** yes  

## Solution
## Problem Understanding

We are asked to take a number $n$ and express it as a sum of numbers that are multiples of 2050 scaled by powers of ten. Concretely, the numbers we can use are 2050, 20500, 205000, 2050000, and so on. Each number in this sequence is exactly 2050 multiplied by a power of ten. The task is to find the minimum number of such numbers that sum to $n$, or report that it is impossible.

The input consists of multiple test cases, each with a single number $n$. $n$ can be as large as $10^{18}$, which rules out any brute-force enumeration of all possible combinations. This bound tells us we need a method that works with large integers efficiently, ideally in logarithmic or linear time relative to the number of digits of $n$.

A subtle edge case occurs when $n$ is not divisible by 2050 at all. For example, $n = 205$ cannot be written as a sum of 2050-numbers. A careless implementation that always attempts division or subtraction would either give a non-integer result or incorrectly try to construct a sum that does not exist. Another edge case is when $n$ is exactly a single 2050-number with a large power of ten, such as $2050 \cdot 10^{15}$. Our solution must handle these without iterating over all smaller multiples.

## Approaches

The naive approach is to generate all 2050-numbers up to $n$ and try all combinations. For each 2050-number, you could repeatedly subtract it from $n$ until you reach zero. This is essentially a brute-force greedy approach. It works for small $n$ but fails for large inputs because the number of possible 2050-numbers scales with the number of digits of $n$ and the subtraction loops could reach $10^{18}/2050 \approx 5 \cdot 10^{14}$ operations in the worst case.

The key insight is that every valid $n$ must be divisible by 2050, because all allowed numbers are multiples of 2050. Once we divide $n$ by 2050, the problem reduces to representing the resulting number $m = n / 2050$ as a sum of powers of 10. Since powers of 10 only have one non-zero digit, the minimum number of terms is simply the sum of the digits of $m$. This avoids iterating over every possible combination and reduces the problem to a simple digit sum calculation. This approach works because any number $m$ in base 10 can be uniquely represented as a sum of powers of 10 multiplied by single-digit coefficients, and each coefficient corresponds to the count of a 2050-number with a specific power of 10.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n / 2050) | O(1) | Too slow for large n |
| Optimal | O(log10 n) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the number of test cases $T$.
2. For each test case, read the number $n$.
3. Check if $n$ is divisible by 2050. If it is not, print -1 and continue to the next test case. This step immediately filters impossible cases.
4. Divide $n$ by 2050 to get $m$. This transforms the problem into counting digits.
5. Initialize a counter for the number of 2050-numbers needed.
6. While $m > 0$, extract the last digit of $m$ using modulo 10, add it to the counter, and integer-divide $m$ by 10. This effectively sums the digits of $m$.
7. Print the counter. This is the minimum number of 2050-numbers required.

The correctness is guaranteed because each digit of $m$ corresponds to the count of a 2050-number multiplied by a specific power of 10. Summing the digits gives the minimal number of terms since each digit can be realized directly with the corresponding 2050-number.

## Python Solution

```python
import sys
input = sys.stdin.readline

T = int(input())
for _ in range(T):
    n = int(input())
    if n % 2050 != 0:
        print(-1)
        continue
    m = n // 2050
    count = 0
    while m > 0:
        count += m % 10
        m //= 10
    print(count)
```

We first read the number of test cases, then iterate through each $n$. The divisibility check prevents unnecessary computation for impossible cases. Dividing by 2050 converts the problem into a digit sum problem. We then loop through the digits of $m$, summing them to get the final count. Using integer division ensures that no floating point precision issues arise.

## Worked Examples

### Example 1: n = 4100

| Step | n | n % 2050 | m | count |
| --- | --- | --- | --- | --- |
| Initial | 4100 | 0 | 2 | 0 |
| Loop 1 | 4100 | 0 | 2 | 2 |
| Loop 2 | 4100 | 0 | 0 | 2 |

The digit sum of 2 gives 2, which corresponds to 4100 = 2050 + 2050.

### Example 2: n = 25308639900

| Step | n | n % 2050 | m | count |
| --- | --- | --- | --- | --- |
| Initial | 25308639900 | 0 | 12345678 | 0 |
| Loop 1 | 12345678 | 8 | 1234567 | 8 |
| Loop 2 | 1234567 | 7 | 123456 | 15 |
| Loop 3 | 123456 | 6 | 12345 | 21 |
| Loop 4 | 12345 | 5 | 1234 | 26 |
| Loop 5 | 1234 | 4 | 123 | 30 |
| Loop 6 | 123 | 3 | 12 | 33 |
| Loop 7 | 12 | 2 | 1 | 35 |
| Loop 8 | 1 | 1 | 0 | 36 |

The sum of digits gives 36, which is the minimum number of 2050-numbers needed.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(log10 n) | We divide by 2050 once and then sum the digits of the resulting number, which takes time proportional to the number of digits. |
| Space | O(1) | Only a few integer variables are used, no extra data structures. |

Given $n \le 10^{18}$, the maximum number of digits is 18, so our algorithm performs at most 18 operations per test case, which easily fits in 1 second for up to 1000 test cases.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    output = []
    T = int(input())
    for _ in range(T):
        n = int(input())
        if n % 2050 != 0:
            output.append("-1")
            continue
        m = n // 2050
        count = 0
        while m > 0:
            count += m % 10
            m //= 10
        output.append(str(count))
    return "\n".join(output)

# provided samples
assert run("6\n205\n2050\n4100\n20500\n22550\n25308639900\n") == "-1\n1\n2\n1\n2\n36", "sample 1"

# custom cases
assert run("3\n2050\n20500\n205000\n") == "1\n1\n1", "single terms"
assert run("1\n2049\n") == "-1", "not divisible"
assert run("1\n2050000000000000000\n") == "1", "large power of ten"
assert run("1\n6150\n") == "3", "sum of three 2050s"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 2050, 20500, 205000 | 1, 1, 1 | Minimal representation with one 2050-number |
| 2049 | -1 | Divisibility check |
| 2050000000000000000 | 1 | Handling very large numbers |
| 6150 | 3 | Correct counting of multiple same 2050-numbers |

## Edge Cases

If $n$ is smaller than 2050, the divisibility check ensures that the algorithm outputs -1. For $n$ that is exactly a 2050-number multiplied by a power of ten, the digit sum of $m$ will be 1, giving the correct minimal count. For very large $n$, using integer division and modulo avoids any floating-point errors and ensures accurate counting. The algorithm correctly handles numbers with multiple digits in $m$, summing them to produce the minimum number of terms.
