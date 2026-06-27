---
title: "CF 105020A - Mood"
description: "We are given multiple independent scenarios where a person has a fixed amount of money and wants to buy a drink with a known price. For each scenario, we need to determine how much additional money is required so that the available amount is enough to cover the cost."
date: "2026-06-28T01:56:22+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105020
codeforces_index: "A"
codeforces_contest_name: "TCPC Tunisian Collegiate Programming Contest 2022"
rating: 0
weight: 105020
solve_time_s: 77
verified: false
draft: false
---

[CF 105020A - Mood](https://codeforces.com/problemset/problem/105020/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 17s  
**Verified:** no  

## Solution
## Problem Understanding

We are given multiple independent scenarios where a person has a fixed amount of money and wants to buy a drink with a known price. For each scenario, we need to determine how much additional money is required so that the available amount is enough to cover the cost. If the current money already covers or exceeds the price, then nothing needs to be borrowed.

Each test case contains two integers. The first is the current amount of money available, and the second is the cost of the drink. The output for each case is the shortfall between cost and available money, but never negative.

The input size can be as large as 100,000 test cases, and each value can be up to 100,000. This immediately rules out any approach that does extra work per test case beyond constant time. Any nested loop or simulation per test case would exceed the time limit, since even O(t log t) is unnecessary overhead here and O(t) is the target.

The key edge behavior happens when the available money is already enough. For example, if x = 10 and y = 7, the answer is 0, not -3. A naive implementation that directly prints y - x without guarding the sign would produce incorrect negative outputs. Another subtle case is when x equals y exactly, where the answer must also be 0.

## Approaches

The most direct way to think about the problem is to imagine repeatedly borrowing one pound at a time until the total reaches the required cost. If x is less than y, we would need to add 1 repeatedly until equality is reached. This brute-force interpretation is conceptually correct but inefficient: in the worst case, when x = 0 and y = 100,000, it would require 100,000 steps per test case, leading to 10^10 operations in the worst input size.

The structure of the problem removes any need for simulation because the final answer depends only on the difference between two numbers. Instead of incrementally borrowing, we can compute the exact deficit directly. If the current amount is already sufficient, the deficit is zero. Otherwise, it is exactly y - x. This observation reduces the entire process to a single arithmetic comparison per test case.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(t · | y − x | ) |
| Optimal | O(t) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the number of test cases t, since each case is independent and can be processed in isolation.
2. For each test case, read the pair (x, y), representing available money and required cost.
3. Compare x with y to determine whether there is a deficit.
4. If x is greater than or equal to y, output 0 because no borrowing is required and borrowing cannot be negative.
5. Otherwise, output y - x, which directly measures the missing amount needed to reach the cost.

### Why it works

For each test case, the result depends only on whether x covers y. If x ≥ y, the requirement is already satisfied, so the minimal additional amount is zero. If x < y, any valid solution must increase x up to at least y, and the smallest such increase is exactly y - x. There is no alternative combination or hidden constraint, so this difference uniquely determines the answer.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        x, y = map(int, input().split())
        if x >= y:
            print(0)
        else:
            print(y - x)

if __name__ == "__main__":
    solve()
```

The solution reads all test cases using fast input to handle up to 100,000 lines efficiently. Each case is processed independently in constant time. The conditional check ensures that we never output negative values, which is the most common implementation mistake for this problem.

The subtraction y - x is only performed when x < y, guaranteeing correctness and avoiding unnecessary computation. This separation also makes the logic explicit and safe against edge cases like equality.

## Worked Examples

### Example 1

Input:

```
3
7 10
5 3
45 45
```

| x | y | x ≥ y | Output |
| --- | --- | --- | --- |
| 7 | 10 | No | 3 |
| 5 | 3 | Yes | 0 |
| 45 | 45 | Yes | 0 |

The first case shows a deficit of 3. The second and third cases show that when the available money is sufficient or equal, no borrowing is needed.

### Example 2

Input:

```
4
1 100
100 1
0 50
20 25
```

| x | y | x ≥ y | Output |
| --- | --- | --- | --- |
| 1 | 100 | No | 99 |
| 100 | 1 | Yes | 0 |
| 0 | 50 | No | 50 |
| 20 | 25 | No | 5 |

This example stresses both extremes: large deficits, zero money, and cases where no borrowing is needed.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(t) | Each test case is handled with a constant number of operations: one read, one comparison, and one subtraction. |
| Space | O(1) | No extra data structures are used beyond input variables. |

The linear scan over test cases is optimal because every input pair must be read at least once. The constraints allow up to 100,000 operations, which is comfortably within limits for Python with fast I/O.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from collections import deque
    output = []

    def solve():
        t = int(input())
        for _ in range(t):
            x, y = map(int, input().split())
            if x >= y:
                output.append("0")
            else:
                output.append(str(y - x))

    solve()
    return "\n".join(output)

# provided sample
assert run("3\n7 10\n5 3\n45 45\n") == "3\n0\n0"

# minimum values
assert run("2\n1 1\n1 2\n") == "0\n1"

# large deficit
assert run("1\n1 100000\n") == "99999"

# already enough money
assert run("3\n100 50\n50 50\n60 10\n") == "0\n0\n0"

# mixed cases
assert run("4\n0 5\n5 0\n10 20\n20 10\n") == "5\n0\n10\n0"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 1 / 1 2 | 0 / 1 | equality and small deficit |
| 1 100000 | 99999 | maximum difference handling |
| mixed | 0 / positive | correct branching |
| zeros | 5 / 0 / 10 / 0 | boundary and reversal cases |

## Edge Cases

One important edge case is equality, where x equals y. For input `10 10`, the algorithm checks `x >= y` and directly outputs 0. This confirms that no borrowing is needed when the amount exactly matches the cost.

Another case is when x is zero. For `0 50`, the condition `x >= y` fails and the algorithm computes `50 - 0 = 50`. This ensures correct handling of missing initial funds without special casing.

A reversed case like `100 1` tests that the subtraction is not mistakenly applied in all cases. Since `x >= y` holds, the output is correctly clamped to 0 rather than producing a negative value.
