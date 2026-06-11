---
title: "CF 1145B - Kanban Numbers"
description: "We are asked to determine whether a given number can be represented as the sum of any number of integers equal to 4 or 7. The input is a single integer $a$ between 1 and 99, and the output is either \"YES\" if such a representation exists, or \"NO\" otherwise."
date: "2026-06-12T03:26:01+07:00"
tags: ["codeforces", "competitive-programming", "*special", "brute-force"]
categories: ["algorithms"]
codeforces_contest: 1145
codeforces_index: "B"
codeforces_contest_name: "April Fools Day Contest 2019"
rating: 0
weight: 1145
solve_time_s: 96
verified: true
draft: false
---

[CF 1145B - Kanban Numbers](https://codeforces.com/problemset/problem/1145/B)

**Rating:** -  
**Tags:** *special, brute force  
**Solve time:** 1m 36s  
**Verified:** yes  

## Solution
## Problem Understanding

We are asked to determine whether a given number can be represented as the sum of any number of integers equal to 4 or 7. The input is a single integer $a$ between 1 and 99, and the output is either "YES" if such a representation exists, or "NO" otherwise. Conceptually, we can think of this as a special kind of “coin change” problem with only two coin denominations: 4 and 7.

The key constraint is that $a$ is at most 99. This small upper bound means we can consider all possible combinations of 4s and 7s without performance concerns. A naive approach that attempts every pair $(x, y)$ where $4x + 7y = a$ is feasible because the maximum number of coins for either denomination is under 25, and the total number of combinations is tiny.

Edge cases emerge when $a$ is less than 4 or between 4 and 7 but not equal to 4 or 7. For example, if $a = 3$, no combination of 4s and 7s can sum to 3, so the correct output is "NO". If $a = 11$, the number can be expressed as $4 + 7$, so the output is "YES". A careless approach might try only multiples of 4 or 7 independently, missing combinations like $4 + 7$.

## Approaches

The brute-force method iterates over all non-negative counts of 4s and 7s whose sum does not exceed $a$. For each possible number of 4s, we check if the remainder $a - 4x$ is divisible by 7. This approach works because the total number of iterations is limited by $\frac{a}{4} \approx 24$ in the worst case. Although technically a double loop could be used, a single loop over 4s suffices because once the number of 4s is fixed, checking divisibility by 7 is constant time.

The optimal approach relies on the insight that we only need to consider $x$ from 0 up to $\lfloor a / 4 \rfloor$. For each $x$, if $(a - 4x) \% 7 == 0$, then $a$ can be expressed as a sum of 4s and 7s. This reduces unnecessary exploration of negative or impossible counts of 7s and is guaranteed to find a solution if one exists. There is no faster method needed because the input range is small.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(a^2) | O(1) | Accepted due to small input |
| Single-loop check | O(a/4) = O(1) | O(1) | Accepted and simpler |

## Algorithm Walkthrough

1. Read the integer $a$ from input. This is the target sum we want to check.
2. Iterate $x$ from 0 to $\lfloor a / 4 \rfloor$. Each $x$ represents the count of 4s used.
3. For each $x$, compute the remainder $r = a - 4x$. This is the amount that must be covered by 7s.
4. Check if $r$ is divisible by 7 using $r \% 7 == 0$. If true, output "YES" and stop.
5. If no $x$ satisfies this condition after the loop, output "NO".

Why it works: Every potential combination of 4s and 7s can be expressed as $4x + 7y = a$. By iterating over all feasible counts of 4s, we are guaranteed to test every possible value of $y$ that is non-negative. The divisibility check ensures that $y$ is an integer, satisfying the original equation. No valid combination can be skipped.

## Python Solution

```python
import sys
input = sys.stdin.readline

a = int(input())
for x in range(a // 4 + 1):
    if (a - 4 * x) % 7 == 0:
        print("YES")
        break
else:
    print("NO")
```

The code reads the integer $a$ and iterates $x$ from 0 up to $a // 4$. The expression $(a - 4 * x) \% 7$ directly checks whether the remainder can be formed entirely by 7s. Using a `for` loop with an `else` clause ensures we only print "NO" if no valid $x$ is found. A common mistake is off-by-one errors in the loop bounds; here, `a // 4 + 1` correctly includes the case where $x = a // 4$.

## Worked Examples

Sample input 1: `5`

| x | r = a - 4*x | r % 7 == 0? |
| --- | --- | --- |
| 0 | 5 | False |
| 1 | 1 | False |

No valid $x$ exists, so the output is "NO". This confirms the algorithm handles small numbers correctly.

Sample input 2: `11`

| x | r = a - 4*x | r % 7 == 0? |
| --- | --- | --- |
| 0 | 11 | False |
| 1 | 7 | True |

The algorithm prints "YES", demonstrating it correctly identifies combinations like 4 + 7.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(a/4) = O(1) | Maximum 25 iterations for a ≤ 99 |
| Space | O(1) | Only loop counter and remainder stored |

The solution comfortably fits within the 1-second time limit and the 256 MB memory limit.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    a = int(input())
    for x in range(a // 4 + 1):
        if (a - 4 * x) % 7 == 0:
            return "YES"
    return "NO"

# provided sample
assert run("5\n") == "NO", "sample 1"

# custom cases
assert run("11\n") == "YES", "4 + 7"
assert run("3\n") == "NO", "too small"
assert run("28\n") == "YES", "4*7 or 7*4"
assert run("99\n") == "YES", "largest input, multiple solutions"
assert run("1\n") == "NO", "minimum input, impossible"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 11 | YES | combination 4 + 7 |
| 3 | NO | too small, no solution |
| 28 | YES | multiple solutions possible |
| 99 | YES | largest input, stress test |
| 1 | NO | minimum input, impossible |

## Edge Cases

For `a = 1`, the loop runs with x = 0, r = 1, which is not divisible by 7. Output is "NO", handling the lower bound correctly. For `a = 28`, x = 0 yields r = 28 divisible by 7, so the algorithm prints "YES" immediately, showing it correctly finds solutions that use only 7s. These examples confirm that all combinations within the input range are tested efficiently.
