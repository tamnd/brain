---
title: "CF 102788A - Normal Magic Square"
description: "A normal magic square of order n is an n × n arrangement containing every number from 1 to n² exactly once. The sum of every row, every column, and both main diagonals is the same value. The task is not to build the square."
date: "2026-07-27T18:19:57+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102788
codeforces_index: "A"
codeforces_contest_name: "2017-2018 ICPC Central Quarter Final of Northeastern European Regional Collegiate Programming Contest"
rating: 0
weight: 102788
solve_time_s: 39
verified: true
draft: false
---

[CF 102788A - Normal Magic Square](https://codeforces.com/problemset/problem/102788/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 39s  
**Verified:** yes  

## Solution
## Problem Understanding

A normal magic square of order `n` is an `n × n` arrangement containing every number from `1` to `n²` exactly once. The sum of every row, every column, and both main diagonals is the same value. The task is not to build the square. We only need the sum of the numbers in the first row of such a square. The input is the side length of the square, and the output is this common magic sum.

The order can be as large as `1000`, so constructing the whole square would require storing up to one million cells. That is still possible in some languages, but it is unnecessary. The intended solution should use only the mathematical property of the square and finish in constant time. Any simulation that tries to place values or verify rows and columns performs work proportional to `n²`, while the answer can be derived directly.

The main edge cases come from small orders and parity. For `n = 1`, the square contains only the number `1`, so the answer is `1`. A program that blindly applies a construction formula without handling this case may fail. For example:

```
Input:
1

Output:
1
```

The order `2` never appears because a normal magic square of that size does not exist. A careless implementation that assumes every positive `n` is valid may attempt to construct an impossible square. The constraints exclude this case, so the program only needs to read the valid input range.

## Approaches

A direct approach would be to actually create a normal magic square and calculate the first row. For odd orders, one could use the Siamese construction, while other orders require more complicated constructions. After building the `n × n` grid, reading the first row takes another `O(n)` operations. The problem with this approach is that it solves a harder problem than required. The worst case with `n = 1000` creates one million cells and performs a large amount of unnecessary work.

The key observation is that the first row has the same sum as every other row. The entire square contains the numbers `1` through `n²`, so the total of all cells is the arithmetic series:

$$1 + 2 + \dots + n^2 = \frac{n^2(n^2+1)}{2}$$

There are exactly `n` rows, and every row has the same sum. Dividing the total sum by the number of rows gives the magic sum:

$$\frac{n^2(n^2+1)}{2n} = \frac{n(n^2+1)}{2}$$

The answer is therefore determined entirely by `n`. The actual arrangement of the square is irrelevant.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n²) | O(n²) | Too slow and unnecessary |
| Optimal | O(1) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the order `n` of the magic square.
2. Compute the total sum of all numbers from `1` to `n²` using the arithmetic progression formula:

$$\frac{n^2(n^2+1)}{2}$$

This works because a normal magic square contains each of these numbers exactly once.

1. Divide the total sum by `n`, because the square has `n` rows and all rows have the same sum.
2. Output the resulting value, which is the sum of the first row.

Why it works:

The defining property of a magic square is that every row has an identical sum. Since all numbers from `1` to `n²` appear once, the sum of all cells is fixed regardless of how the numbers are arranged. Splitting this fixed total evenly among the `n` rows gives the value of every row, including the first one. The formula cannot depend on the construction because all valid normal magic squares have the same total and the same number of rows.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    print(n * (n * n + 1) // 2)

if __name__ == "__main__":
    solve()
```

The program only keeps the value of `n`, so it never allocates the square itself. The expression `n * (n * n + 1) // 2` follows directly from the derived formula.

Python integers handle the intermediate multiplication safely. The largest value is reached when `n = 1000`, where the result is still far below Python's integer limits. Integer division is exact because the magic sum is always an integer for the valid orders in the problem.

## Worked Examples

For the first sample:

| Step | n | n² | Formula value | Output |
| --- | --- | --- | --- | --- |
| Start | 3 | 9 | 3 × (9 + 1) / 2 | 15 |

The formula gives `15`, which matches the first row sum of any `3 × 3` normal magic square. This example demonstrates the general odd-order case.

For the second sample:

| Step | n | n² | Formula value | Output |
| --- | --- | --- | --- | --- |
| Start | 1 | 1 | 1 × (1 + 1) / 2 | 1 |

The calculation naturally handles the trivial square. No special construction is required.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(1) | Only a few arithmetic operations are performed |
| Space | O(1) | The algorithm stores only the input value |

The solution easily fits the limits because it avoids building a square of size `n²`. Even the maximum allowed order only requires constant-time arithmetic.

## Test Cases

```python
import sys
import io

def solve(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    input = sys.stdin.readline
    n = int(input())
    return str(n * (n * n + 1) // 2)

# provided samples
assert solve("3\n") == "15", "sample 1"
assert solve("1\n") == "1", "sample 2"

# custom cases
assert solve("5\n") == "65", "odd order magic sum"
assert solve("1000\n") == "500000500", "maximum size input"
assert solve("7\n") == "175", "larger odd order"
assert solve("9\n") == "369", "off-by-one formula check"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `5` | `65` | Checks a normal odd order |
| `1000` | `500000500` | Checks the maximum allowed value |
| `7` | `175` | Checks the formula on a larger square |
| `9` | `369` | Catches incorrect arithmetic formulas |

## Edge Cases

For `n = 1`, the algorithm calculates:

$$\frac{1(1^2+1)}{2} = 1$$

The output is:

```
Input:
1

Output:
1
```

The formula works because the only row contains the only cell in the square.

For the largest allowed order:

```
Input:
1000
```

The algorithm does not try to create one million cells. It directly computes:

$$\frac{1000(1000^2+1)}{2}=500000500$$

and outputs:

```
500000500
```

This confirms why using the mathematical property is necessary: the amount of work stays the same even when the square becomes very large.
