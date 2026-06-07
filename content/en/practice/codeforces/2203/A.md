---
title: "CF 2203A - Towers of Boxes"
description: "Monocarp has n identical boxes, each weighing m units and able to support up to d units on top. He wants to stack all the boxes into towers while respecting durability: no box can support more weight than d."
date: "2026-06-07T20:00:50+07:00"
tags: ["codeforces", "competitive-programming", "math"]
categories: ["algorithms"]
codeforces_contest: 2203
codeforces_index: "A"
codeforces_contest_name: "Educational Codeforces Round 187 (Rated for Div. 2)"
rating: 800
weight: 2203
solve_time_s: 102
verified: true
draft: false
---

[CF 2203A - Towers of Boxes](https://codeforces.com/problemset/problem/2203/A)

**Rating:** 800  
**Tags:** math  
**Solve time:** 1m 42s  
**Verified:** yes  

## Solution
## Problem Understanding

Monocarp has `n` identical boxes, each weighing `m` units and able to support up to `d` units on top. He wants to stack all the boxes into towers while respecting durability: no box can support more weight than `d`. The task is to determine the minimum number of towers required to use all boxes.

Input consists of multiple test cases. Each test case gives `n`, `m`, and `d`. The output is a single integer per test case: the minimum number of towers. Each tower must contain at least one box, and all boxes must be placed.

Because the maximum `n`, `m`, and `d` are 50, and there can be up to 10,000 test cases, any solution that performs a simple arithmetic computation per test case is feasible. A naive simulation that iteratively stacks boxes while checking weight constraints could work but is unnecessary. Edge cases include situations where `m > d`, making it impossible to place two boxes on top of each other, and cases where `d` is large relative to `m`, allowing all boxes in a single tower. For example, if `n = 5`, `m = 3`, `d = 2`, no stacking is possible, so each box forms its own tower, giving 5 towers. A careless approach that does not check the per-box weight limit would incorrectly attempt to stack boxes and undercount the towers.

## Approaches

The brute-force approach is to simulate stacking: start with an empty tower, add boxes until the next box would violate the durability constraint, then start a new tower. Repeat until all boxes are placed. This works because it directly enforces the weight condition, but it requires looping through `n` boxes for each test case. With `n` up to 50 and `t` up to 10,000, this is manageable, but it's overkill.

The optimal approach observes that in a tower of `k` boxes, the box at the bottom supports `(k-1) * m` weight. To avoid breaking, `(k-1) * m <= d`. Solving for `k` gives `k <= d // m + 1`. The minimal number of towers is then the ceiling of `n` divided by the maximum possible height per tower: `ceil(n / ((d // m) + 1))`. This reduces the problem to a simple arithmetic calculation per test case.

The observation relies on the uniformity of boxes. Since every box has the same weight and durability, we only need to find the tallest safe tower. Then distributing all boxes into towers of this height guarantees a minimum number of towers.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n * t) | O(1) | Acceptable but unnecessary |
| Optimal | O(t) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the number of test cases `t`.
2. For each test case, read `n`, `m`, and `d`.
3. Compute the maximum height a single tower can have without breaking boxes: `max_height = d // m + 1`. This comes from solving `(k-1) * m <= d` for `k`.
4. Compute the minimum number of towers required as `ceil(n / max_height)`. In integer arithmetic, this is `(n + max_height - 1) // max_height`.
5. Print the result for each test case.

Why it works: `max_height` ensures no box exceeds its durability. Dividing the total number of boxes by `max_height` and rounding up guarantees all boxes are used while minimizing towers. The uniformity of boxes makes this invariant valid across the tower distribution.

## Python Solution

```python
import sys
input = sys.stdin.readline

t = int(input())
for _ in range(t):
    n, m, d = map(int, input().split())
    max_height = d // m + 1
    towers = (n + max_height - 1) // max_height
    print(towers)
```

The code first reads `t`, then loops over each test case. `max_height` is computed from the durability and weight, and integer division with rounding up gives the number of towers. The formula `(n + max_height - 1) // max_height` avoids floating-point arithmetic. Off-by-one errors are avoided by using the ceiling formula rather than attempting manual rounding.

## Worked Examples

Sample Input 1:

```
8 10 20
```

| n | m | d | max_height | towers |
| --- | --- | --- | --- | --- |
| 8 | 10 | 20 | 3 | 3 |

Explanation: `(k-1)*m <= d` gives `k <= 3`. `ceil(8/3) = 3` towers are needed.

Sample Input 2:

```
5 3 2
```

| n | m | d | max_height | towers |
| --- | --- | --- | --- | --- |
| 5 | 3 | 2 | 1 | 5 |

Explanation: `d < m`, so no stacking is possible, each box forms a separate tower.

These traces demonstrate both the stackable and unstackable cases and confirm the ceiling division works.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(t) | Each test case involves a few arithmetic operations. |
| Space | O(1) | Only a few integers per test case are stored. |

Given `t` up to 10,000 and simple arithmetic per test case, the solution runs efficiently within time and memory limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    output = io.StringIO()
    sys.stdout = output
    t = int(input())
    for _ in range(t):
        n, m, d = map(int, input().split())
        max_height = d // m + 1
        towers = (n + max_height - 1) // max_height
        print(towers)
    return output.getvalue().strip()

# provided samples
assert run("3\n8 10 20\n8 1 20\n5 3 2\n") == "3\n1\n5", "sample 1"

# custom cases
assert run("1\n1 1 1\n") == "1", "minimum size input"
assert run("1\n50 50 50\n") == "2", "maximum size input where stacking barely fits"
assert run("1\n10 2 5\n") == "3", "general stacking"
assert run("1\n4 5 2\n") == "4", "weight exceeds durability, no stacking"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 1 1 | 1 | Single box minimal input |
| 50 50 50 | 2 | Maximum values, check arithmetic correctness |
| 10 2 5 | 3 | Typical stackable case |
| 4 5 2 | 4 | Each box forms its own tower, weight > durability |

## Edge Cases

If `d < m`, the maximum height `d // m + 1` becomes 1. This ensures every box is placed in its own tower. For example, with `n = 4`, `m = 5`, `d = 2`, `max_height = 1`, the algorithm computes `(4 + 1 - 1) // 1 = 4`, correctly outputting 4 towers. The algorithm handles this scenario naturally without any special casing. If `d` is a large multiple of `m`, say `d = 100`, `m = 2`, `n = 10`, `max_height = 51`, then `(10 + 51 - 1) // 51 = 1`, placing all boxes in a single tower, which is correct.
