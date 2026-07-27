---
title: "CF 102800G - Matrix"
description: "The matrix starts filled with zeros. For every positive pair (i, j), we perform one operation that flips every cell whose row index is divisible by i and whose column index is divisible by j. A particular cell does not care about operations that do not reach it."
date: "2026-07-27T17:39:13+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102800
codeforces_index: "G"
codeforces_contest_name: "The 14th Jilin Provincial Collegiate Programming Contest"
rating: 0
weight: 102800
solve_time_s: 78
verified: true
draft: false
---

[CF 102800G - Matrix](https://codeforces.com/problemset/problem/102800/G)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 18s  
**Verified:** yes  

## Solution
## Problem Understanding

The matrix starts filled with zeros. For every positive pair `(i, j)`, we perform one operation that flips every cell whose row index is divisible by `i` and whose column index is divisible by `j`.

A particular cell does not care about operations that do not reach it. For a cell at row `r` and column `c`, the only relevant operations are those where `i` divides `r` and `j` divides `c`. Every such pair flips the cell once. After all operations finish, the cell contains `1` if it has been flipped an odd number of times, otherwise it remains `0`.

Each test case gives the dimensions of one matrix. The task is to count how many cells end as `1`.

The dimensions can be as large as `10^18`, so even iterating over all rows is impossible. Any algorithm proportional to `n`, `m`, or `n × m` is immediately ruled out. The solution must use only a handful of arithmetic operations per test case.

One easy mistake is to think that every divisor contributes independently and forget that the answer depends only on parity.

For example:

```
1
2 2
```

The correct answer is:

```
1
```

Only cell `(1, 1)` becomes `1`. Although other cells are flipped several times, each of them is flipped an even number of times.

Another subtle case is when only one index is a perfect square.

```
1
3 4
```

The correct answer is:

```
2
```

Rows `1` is the only perfect square, while columns `1` and `4` are perfect squares. Only `(1,1)` and `(1,4)` finish as `1`. A careless solution that checks only one dimension would overcount.

A final edge case is the largest possible input.

```
1
1000000000000000000 1000000000000000000
```

The solution must avoid simulation and compute the answer directly from integer square roots.

## Approaches

The brute force idea is straightforward. For every operation `(i, j)`, visit every affected cell and flip it. This is correct because it follows the definition exactly. Unfortunately, there are `n × m` possible operation pairs, and each operation may touch many cells. Even iterating through all cells is impossible when the dimensions reach `10^18`.

The key observation is to analyze one cell independently.

Suppose we look at cell `(r, c)`. It is flipped once for every divisor `i` of `r` and every divisor `j` of `c`. If `d(x)` denotes the number of divisors of `x`, then the total number of flips is

`d(r) × d(c)`.

Only the parity matters. A product is odd only when both factors are odd.

Now we only need one classical number theory fact. The divisor count of an integer is odd exactly when the integer is a perfect square. Every non-square has divisors that appear in pairs `(a, x / a)`, while a perfect square has one unpaired divisor, its square root.

So a cell becomes `1` exactly when both its row index and column index are perfect squares.

The problem reduces to counting perfect squares in each dimension. There are exactly `⌊√n⌋` perfect squares between `1` and `n`, and similarly `⌊√m⌋` between `1` and `m`.

The final answer is simply

`⌊√n⌋ × ⌊√m⌋`.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n × m × average affected cells) | O(n × m) | Too slow |
| Optimal | O(1) per test case | O(1) | Accepted |

## Algorithm Walkthrough

1. Read `n` and `m`.
2. Compute `a = ⌊√n⌋` using the integer square root function. This gives the number of perfect square row indices.
3. Compute `b = ⌊√m⌋` using the integer square root function. This gives the number of perfect square column indices.
4. Output `a × b`, because every combination of a perfect square row and a perfect square column produces a cell that is flipped an odd number of times.

### Why it works

For a fixed cell `(r, c)`, the number of flips equals the number of divisor pairs `(i, j)` with `i | r` and `j | c`, which is `d(r) × d(c)`. The cell ends as `1` if and only if this product is odd. A divisor count is odd exactly for perfect squares, so both `r` and `c` must be perfect squares. Counting such rows and columns independently gives the exact number of cells containing `1`.

## Python Solution

```python
import sys
from math import isqrt

input = sys.stdin.readline

t = int(input())
for _ in range(t):
    n, m = map(int, input().split())
    print(isqrt(n) * isqrt(m))
```

The program directly implements the mathematical result. `math.isqrt` returns the integer square root, which is exactly `⌊√x⌋` without any floating point errors. This is especially important because the input can be as large as `10^18`, where floating point square roots may lose precision.

Each test case performs only two integer square root computations and one multiplication. Python integers comfortably handle the largest possible answer, so there are no overflow concerns.

## Worked Examples

### Sample 1

Input:

```
1
2 3
```

| Variable | Value |
| --- | --- |
| `isqrt(2)` | 1 |
| `isqrt(3)` | 1 |
| Answer | 1 |

Only row `1` is a perfect square, and only column `1` is a perfect square. Their single intersection is the only cell equal to `1`.

### Sample 2

Input:

```
1
9 10
```

| Variable | Value |
| --- | --- |
| `isqrt(9)` | 3 |
| `isqrt(10)` | 3 |
| Answer | 9 |

The perfect square rows are `1, 4, 9`. The perfect square columns are `1, 4, 9`. Every combination of these rows and columns contributes one cell, giving `3 × 3 = 9`.

This example illustrates that the two dimensions are completely independent once the parity argument has been established.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(1) per test case | Two integer square roots and one multiplication |
| Space | O(1) | Only a few integer variables are stored |

The running time is independent of the matrix dimensions, so it easily handles values up to `10^18` within the limits.

## Test Cases

```python
import sys
import io
from math import isqrt

def solve():
    input = sys.stdin.readline
    t = int(input())
    out = []
    for _ in range(t):
        n, m = map(int, input().split())
        out.append(str(isqrt(n) * isqrt(m)))
    sys.stdout.write("\n".join(out))

def run(inp: str) -> str:
    old_stdin = sys.stdin
    old_stdout = sys.stdout
    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()
    solve()
    ans = sys.stdout.getvalue()
    sys.stdin = old_stdin
    sys.stdout = old_stdout
    return ans

# provided sample
assert run("1\n2 3\n") == "1"

# minimum size
assert run("1\n1 1\n") == "1"

# rectangular boundary
assert run("1\n3 4\n") == "2"

# no additional perfect square after 15
assert run("1\n15 15\n") == "9"

# maximum values
assert run("1\n1000000000000000000 1000000000000000000\n") == "1000000000000000000"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 1` | `1` | Smallest possible matrix |
| `3 4` | `2` | Only one dimension contributes multiple perfect squares |
| `15 15` | `9` | Correct floor square root handling |
| `10^18 10^18` | `10^18` | Largest allowed values |

## Edge Cases

Consider the smallest matrix.

```
1
1 1
```

`isqrt(1) = 1` for both dimensions, so the answer is `1 × 1 = 1`. The only cell is flipped once because `1` has exactly one divisor.

Now consider a case where only one dimension contains multiple perfect squares.

```
1
3 4
```

The algorithm computes `isqrt(3) = 1` and `isqrt(4) = 2`, producing `1 × 2 = 2`. The cells `(1,1)` and `(1,4)` are the only ones with odd flip counts.

Finally, consider the largest legal values.

```
1
1000000000000000000 1000000000000000000
```

`isqrt(10^18) = 10^9`, so the answer is `10^9 × 10^9 = 10^18`. The algorithm performs only constant-time arithmetic and never depends on the actual matrix size.
