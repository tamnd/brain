---
title: "CF 1679A - AvtoBus"
description: "We are asked to determine how many buses a fleet could have given the total number of wheels. Each bus comes in one of two types: two-axle buses with 4 wheels and three-axle buses with 6 wheels."
date: "2026-06-10T00:40:07+07:00"
tags: ["codeforces", "competitive-programming", "brute-force", "greedy", "math", "number-theory"]
categories: ["algorithms"]
codeforces_contest: 1679
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 791 (Div. 2)"
rating: 900
weight: 1679
solve_time_s: 97
verified: true
draft: false
---

[CF 1679A - AvtoBus](https://codeforces.com/problemset/problem/1679/A)

**Rating:** 900  
**Tags:** brute force, greedy, math, number theory  
**Solve time:** 1m 37s  
**Verified:** yes  

## Solution
## Problem Understanding

We are asked to determine how many buses a fleet could have given the total number of wheels. Each bus comes in one of two types: two-axle buses with 4 wheels and three-axle buses with 6 wheels. The input consists of a number of test cases, each specifying the total number of wheels, and the output must be the minimum and maximum number of buses that could sum to this wheel total. If no combination of buses can produce that total, the output is `-1`.

The constraints are generous for arithmetic but restrictive for naive enumeration. The number of wheels `n` can be as large as 10^18, meaning that any solution that tries to enumerate all combinations of buses is infeasible. The time limit of 1 second with up to 1,000 test cases implies that we need an O(1) or O(log n) solution per test case. Edge cases include small totals like `1`, `2`, or `3`, which are impossible to form with 4- and 6-wheeled buses, and very large totals, which must be handled using precise integer arithmetic without overflow.

A naive approach might fail on totals that are odd or otherwise not divisible into sums of 4s and 6s. For example, 7 wheels cannot be formed because 4+4=8 exceeds it, and 6+4=10 exceeds it as well. Small inputs like `4` or `6` require the algorithm to detect that only a single bus is possible, which is the minimum and maximum simultaneously.

## Approaches

The brute-force approach tries all combinations of two-axle and three-axle buses whose wheels sum to `n`. For each `a` in `[0, n//4]`, it checks if `n - 4*a` is divisible by 6. This is correct because it considers all valid partitions, but it requires up to n/4 iterations per test case. For `n = 10^18`, this is completely infeasible.

The key insight comes from simple integer arithmetic. Let `x` be the number of 2-axle buses and `y` the number of 3-axle buses. Then we have the linear Diophantine equation `4*x + 6*y = n`. Dividing both sides by 2 gives `2*x + 3*y = n/2`. We can now solve for `x` and `y` as non-negative integers. The minimum number of buses occurs when we maximize `y`, since 3-axle buses have more wheels per bus. This leads to `y = floor(n/6)` if `n` is divisible by 2, and then `x` is the remaining wheels divided by 4. The maximum number of buses occurs when we maximize `x`, leading to `x = floor(n/4)` and `y` adjusted accordingly. If `n` is odd, or the remainder is not divisible by 2 after dividing by 2, no solution exists.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n) | O(1) | Too slow |
| Optimal | O(1) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the number of test cases `t`. For each test case, read the total wheel count `n`.
2. Check if `n` is less than 4. If so, output `-1` because no combination of buses can have fewer than 4 wheels.
3. Compute the minimum number of buses by taking as many 3-axle buses as possible. Set `min_buses = ceil(n/6)` because each 3-axle bus contributes 6 wheels. If `n` is divisible by 2, integer arithmetic suffices.
4. Compute the maximum number of buses by taking as many 2-axle buses as possible. Set `max_buses = n // 4` because each 2-axle bus contributes 4 wheels.
5. Check if `n` is divisible by 2. If not, print `-1` because 4 and 6 are both even, so odd totals are impossible. Otherwise, print `min_buses` and `max_buses`.

The correctness relies on the invariant that every valid combination of 4- and 6-wheeled buses must sum to an even number. Maximizing the number of 3-axle buses minimizes the total bus count, and maximizing 2-axle buses maximizes the total bus count. The floor and ceiling arithmetic ensures we do not miss feasible integer solutions.

## Python Solution

```python
import sys
input = sys.stdin.readline

t = int(input())
for _ in range(t):
    n = int(input())
    if n < 4 or n % 2 != 0:
        print(-1)
        continue
    min_buses = (n + 5) // 6  # ceil(n / 6)
    max_buses = n // 4         # floor(n / 4)
    print(min_buses, max_buses)
```

The code reads input efficiently using `sys.stdin.readline`. We immediately filter out totals that are too small or odd. The minimum number of buses uses ceiling division to guarantee enough wheels are covered with 3-axle buses. The maximum number of buses uses floor division to maximize 2-axle buses. Both divisions work correctly with very large integers in Python.

## Worked Examples

For input `n = 4`, `(4+5)//6 = 1` for minimum buses and `4//4 = 1` for maximum. The output is `1 1`, which matches expectations. For `n = 24`, `(24+5)//6 = 29//6 = 4` for minimum and `24//4 = 6` for maximum, producing `4 6`, which matches the sample explanation.

| n | min_buses | max_buses |
| --- | --- | --- |
| 4 | 1 | 1 |
| 24 | 4 | 6 |
| 7 | - | - |
| 998244353998244352 | 166374058999707392 | 249561088499561088 |

These traces confirm that the algorithm handles small, medium, and very large inputs and correctly rejects impossible cases like 7.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(t) | One arithmetic calculation per test case |
| Space | O(1) | Only a few integer variables are used per test case |

Even with t = 1,000 and n up to 10^18, these O(1) operations per test case fit well within the 1-second limit. Python handles arbitrarily large integers efficiently for these calculations.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    out = io.StringIO()
    sys.stdout = out
    t = int(input())
    for _ in range(t):
        n = int(input())
        if n < 4 or n % 2 != 0:
            print(-1)
            continue
        min_buses = (n + 5) // 6
        max_buses = n // 4
        print(min_buses, max_buses)
    return out.getvalue().strip()

# provided samples
assert run("4\n4\n7\n24\n998244353998244352\n") == "1 1\n-1\n4 6\n166374058999707392 249561088499561088"

# custom cases
assert run("3\n1\n2\n3\n") == "-1\n-1\n-1", "too small numbers"
assert run("2\n6\n10\n") == "1 1\n2 2", "small valid numbers"
assert run("1\n1000000000000000000\n") == "166666666666666667 250000000000000000", "very large number"
assert run("1\n5\n") == "-1", "odd number less than 6"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1,2,3 | -1,-1,-1 | rejects impossible small totals |
| 6,10 | 1 1, 2 2 | small valid numbers |
| 10^18 | 166666666666666667 250000000000000000 | very large numbers correctness |
| 5 | -1 | odd numbers detection |

## Edge Cases

When `n` is smaller than 4, the algorithm immediately returns `-1`. For odd numbers like `7`, `5`, or `1`, the algorithm returns `-1` because 4 and 6 cannot sum to an odd total. For multiples of 2 but not multiples of 4 or 6, such as `10`, the algorithm correctly computes minimum and maximum by distributing the remainder appropriately. For extremely large numbers, Python handles integer arithmetic without overflow, ensuring correctness even when `n` approaches 10^18.
