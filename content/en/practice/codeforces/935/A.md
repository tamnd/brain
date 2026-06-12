---
title: "CF 935A - Fafa and his Company"
description: "Fafa needs to divide his company’s employees into groups for project management. He wants to pick a number of team leaders, denoted by l, and assign the remaining employees evenly among them."
date: "2026-06-13T03:24:34+07:00"
tags: ["codeforces", "competitive-programming", "brute-force", "implementation"]
categories: ["algorithms"]
codeforces_contest: 935
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 465 (Div. 2)"
rating: 800
weight: 935
solve_time_s: 549
verified: true
draft: false
---

[CF 935A - Fafa and his Company](https://codeforces.com/problemset/problem/935/A)

**Rating:** 800  
**Tags:** brute force, implementation  
**Solve time:** 9m 9s  
**Verified:** yes  

## Solution
## Problem Understanding

Fafa needs to divide his company’s employees into groups for project management. He wants to pick a number of team leaders, denoted by _l_, and assign the remaining employees evenly among them. Each team leader must oversee the same number of employees, and no employee is left without a leader. The input is a single integer _n_, the total number of employees. The output is the number of possible values of _l_ such that this fair division is possible.

Restated, we are looking for all positive integers _l_ strictly less than _n_ for which the number of non-leaders, _n - l_, is divisible by _l_. This ensures that the remaining employees can be split evenly among the leaders. For example, if there are 6 employees, choosing 2 leaders leaves 4 non-leaders. Since 4 is divisible by 2, each leader can manage 2 employees.

The constraints are modest but significant. _n_ can be as large as 100,000. A naive solution that tries all possible groupings for all values up to _n_ would require up to 100,000 operations. This is acceptable within a 1-second time limit if each operation is simple, but it is worth thinking about divisors to avoid unnecessary checks. Edge cases include _n = 2_, the smallest number of employees, where the only valid number of leaders is 1. Another subtle case is when _n_ is prime; then only 1 leader works because any other choice leaves a remainder.

## Approaches

The brute-force approach considers every possible number of leaders _l_ from 1 to _n - 1_. For each _l_, we check if the number of remaining employees, _n - l_, is divisible by _l_. This is correct, but it performs _n-1_ division operations. In the worst case where _n = 100,000_, that is about 100,000 checks, which is feasible but slightly inelegant.

The key observation is that the problem reduces to counting divisors of _n - l_ that are less than _n_. More concretely, we are looking for all _l_ where _l_ divides _n - l_. If we rewrite this condition, it becomes _n - l = k * l_ for some integer k ≥ 1. Rearranging gives _n = l * (k + 1)_. Therefore, _l_ must be a divisor of _n_ that is strictly less than _n_. This transformation eliminates unnecessary checks and is a classic divisors problem. Iterating only over divisors up to √n ensures O(√n) complexity.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n) | O(1) | Works but can be optimized |
| Optimal | O(√n) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the input integer _n_. This represents the total number of employees in Fafa's company.
2. Initialize a counter to 0. This will track the number of valid choices for team leaders.
3. Iterate _l_ from 1 to √n inclusive. For each _l_, check if it divides _n_.
4. If _l_ divides _n_, it is a potential candidate because it satisfies _n = l * (k + 1)_. If _l_ is less than _n_, increment the counter.
5. Also check the corresponding divisor _n // l_. If it is different from _l_ and less than _n_, increment the counter.
6. After processing all divisors, print the counter. This is the number of valid ways to choose team leaders.

Why it works: The key invariant is that a number of leaders _l_ is valid if and only if it divides _n_ and is strictly less than _n_. By iterating over all divisors of _n_, we guarantee that all potential valid _l_ are considered exactly once. No other values can satisfy the fairness condition, so the counter is exact.

## Python Solution

```python
import sys
input = sys.stdin.readline

n = int(input())
count = 0
i = 1
while i * i <= n:
    if n % i == 0:
        if i < n:
            count += 1
        if i != n // i and n // i < n:
            count += 1
    i += 1
print(count)
```

The solution uses integer division to find divisors efficiently. We check both _i_ and _n // i_ to account for divisor pairs. The boundary check ensures that the leader count is strictly less than _n_, avoiding the invalid case where all employees are leaders. The loop stops at √n to prevent redundant checks, making the solution efficient.

## Worked Examples

**Example 1**: n = 2

| i | n % i == 0? | Count |
| --- | --- | --- |
| 1 | Yes | 1 |

We iterate i=1, it divides 2, and 1 < 2, so count = 1. The corresponding divisor n // i = 2 is not < n, so we do not increment further. Result is 1.

**Example 2**: n = 6

| i | n % i == 0? | Divisor Pair | Count |
| --- | --- | --- | --- |
| 1 | Yes | 1 & 6 | 1 |
| 2 | Yes | 2 & 3 | 3 |

Divisors less than 6 are 1, 2, 3. Each is valid. Count = 3.

This demonstrates that all valid choices are captured and no extra values are counted.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(√n) | We only iterate up to √n to find all divisors. |
| Space | O(1) | Only a few integer variables are used. |

For n ≤ 100,000, √n ≈ 317, so fewer than 400 iterations are required. The solution easily fits within the 1-second time limit and 256 MB memory limit.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    n = int(input())
    count = 0
    i = 1
    while i * i <= n:
        if n % i == 0:
            if i < n:
                count += 1
            if i != n // i and n // i < n:
                count += 1
        i += 1
    return str(count)

# Provided sample
assert run("2\n") == "1", "sample 1"

# Custom cases
assert run("6\n") == "3", "divisors 1, 2, 3"
assert run("12\n") == "5", "divisors 1, 2, 3, 4, 6"
assert run("17\n") == "1", "prime number, only 1 leader"
assert run("100000\n") == "35", "large n, many divisors"
assert run("3\n") == "1", "small n, minimal case"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 6 | 3 | standard multiple divisors |
| 12 | 5 | multiple divisor pairs |
| 17 | 1 | prime number edge case |
| 100000 | 35 | large input performance |
| 3 | 1 | minimal small input |

## Edge Cases

For _n = 2_, only one leader is possible. The loop iterates i = 1. 1 < 2, so count increments to 1. The corresponding divisor 2 is not counted, so output is 1, correctly handling the smallest input.

For prime _n = 17_, only i = 1 divides 17 with i < 17, so count = 1. The corresponding divisor 17 is ignored. The algorithm correctly avoids overcounting and handles primes.

For a perfect square like _n = 36_, divisors include 6, which is the square root. The check i != n // i prevents double counting 6, ensuring each valid leader count is counted exactly once.
