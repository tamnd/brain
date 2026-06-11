---
title: "CF 1260A - Heating"
description: "We are given a house with n rooms. For each room, we know two numbers: ci, the maximum number of radiators we can install, and sumi, the total number of radiator sections required to adequately heat that room."
date: "2026-06-11T20:43:04+07:00"
tags: ["codeforces", "competitive-programming", "math"]
categories: ["algorithms"]
codeforces_contest: 1260
codeforces_index: "A"
codeforces_contest_name: "Educational Codeforces Round 77 (Rated for Div. 2)"
rating: 1000
weight: 1260
solve_time_s: 142
verified: true
draft: false
---

[CF 1260A - Heating](https://codeforces.com/problemset/problem/1260/A)

**Rating:** 1000  
**Tags:** math  
**Solve time:** 2m 22s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a house with `n` rooms. For each room, we know two numbers: `c_i`, the maximum number of radiators we can install, and `sum_i`, the total number of radiator sections required to adequately heat that room. Each radiator can have an arbitrary number of sections, and the cost of a radiator with `k` sections is `k^2`. Our goal is to assign sections to radiators so that the total sections in a room is at least `sum_i`, we do not exceed `c_i` radiators, and the total cost is minimized.

The key constraints are that `n` can be up to 1000, and each room can need up to 10,000 sections with up to 10,000 radiators. This is small enough to allow `O(n)` operations per room, but anything quadratic in `sum_i` or `c_i` could reach 10^8 operations, which is too slow. Edge cases occur when `c_i` is much smaller than `sum_i` or much larger. For example, if a room requires 100 sections but we can only place 1 radiator, we must put all 100 sections in that single radiator. Conversely, if a room requires 1 section and we can place 10,000 radiators, we should put 1 section in a single radiator.

A careless implementation might try to iterate through all possible distributions of sections across radiators. For instance, for `c_i = 2` and `sum_i = 6`, enumerating `[6,0],[5,1],[4,2]…` works for small numbers, but if `sum_i` and `c_i` are 10,000, this approach would be hopelessly slow.

## Approaches

A naive brute-force approach would try every possible combination of `k` radiators and assign sections in all possible ways. This is correct because it covers every valid allocation, but the number of combinations grows exponentially. For `c_i = 10,000` and `sum_i = 10,000`, even enumerating partitions of 10,000 into 10,000 parts is impossible. This demonstrates that brute-force is infeasible.

The key observation is that the cost function `k^2` is convex. Convexity means that the sum of squares is minimized when the values are as equal as possible. In other words, for a given number of radiators, the minimal cost occurs when we distribute the sections evenly, assigning `floor(sum_i/c_i)` to each radiator and spreading the remainder (`sum_i % c_i`) across a few radiators by adding one extra section. This is a classic trick with convex functions: to minimize sum of squares with a fixed sum, the numbers should be as balanced as possible.

Once we know the number of radiators to use, computing the cost is straightforward. We calculate `x = sum_i // c_i` as the base number of sections per radiator, `r = sum_i % c_i` as the remainder sections, and then compute the cost as `(c_i - r) * x^2 + r * (x + 1)^2`. This formula balances the radiators and accounts for any leftover sections.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O((sum_i choose c_i)) | O(c_i) | Too slow |
| Optimal | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read `n`, the number of rooms.
2. For each room, read `c_i` and `sum_i`.
3. Determine the number of radiators we will actually use. This is `min(c_i, sum_i)`, because we cannot use more radiators than either the maximum allowed or the total number of sections (a radiator with 0 sections is meaningless).
4. Compute the base number of sections per radiator as `x = sum_i // num_radiators`.
5. Compute the remainder `r = sum_i % num_radiators`. These are the extra sections that cannot be evenly distributed.
6. Compute the total cost: `(num_radiators - r) * x^2 + r * (x + 1)^2`. This formula assigns `x` sections to most radiators and distributes the remainder one extra section each to `r` radiators.
7. Output the cost for each room.

Why it works: The invariant is that the sum of assigned sections equals `sum_i` and the number of radiators does not exceed `c_i`. Convexity guarantees that distributing sections as evenly as possible minimizes the sum of squares. Any other distribution where some radiators get significantly more sections than others increases the total cost.

## Python Solution

```python
import sys
input = sys.stdin.readline

n = int(input())
for _ in range(n):
    c_i, sum_i = map(int, input().split())
    num_radiators = min(c_i, sum_i)
    x = sum_i // num_radiators
    r = sum_i % num_radiators
    cost = (num_radiators - r) * x * x + r * (x + 1) * (x + 1)
    print(cost)
```

The solution first reads the number of rooms. For each room, it computes how many radiators to use and divides the required sections evenly. The remainder is distributed one per radiator, ensuring all radiators have integer sections. Multiplying and squaring in this order avoids floating-point errors. Using `min(c_i, sum_i)` handles edge cases where the number of radiators exceeds the number of sections.

## Worked Examples

**Sample Input 1:**

```
4
1 10000
10000 1
2 6
4 6
```

| Room | c_i | sum_i | num_radiators | x | r | Cost Calculation | Result |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 1 | 10000 | 1 | 10000 | 0 | 1*10000^2 | 100000000 |
| 2 | 10000 | 1 | 1 | 1 | 0 | 1*1^2 | 1 |
| 3 | 2 | 6 | 2 | 3 | 0 | 2*3^2 | 18 |
| 4 | 4 | 6 | 4 | 1 | 2 | 2_1^2 + 2_2^2 | 10 |

This confirms that the remainder is distributed correctly and the total sections always meet `sum_i`.

**Custom Input 1:**

```
1
5 3
```

| Room | c_i | sum_i | num_radiators | x | r | Cost Calculation | Result |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 5 | 3 | 3 | 1 | 0 | 3*1^2 | 3 |

This tests that when `c_i > sum_i`, we only use `sum_i` radiators.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Each room is processed independently with a constant number of arithmetic operations. |
| Space | O(1) | We store only temporary variables per room, no large arrays needed. |

With `n <= 1000`, the algorithm performs at most 1000 iterations, each with constant operations. Memory usage is negligible, comfortably within the limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    out = io.StringIO()
    sys.stdout = out
    # solution
    n = int(input())
    for _ in range(n):
        c_i, sum_i = map(int, input().split())
        num_radiators = min(c_i, sum_i)
        x = sum_i // num_radiators
        r = sum_i % num_radiators
        cost = (num_radiators - r) * x * x + r * (x + 1) * (x + 1)
        print(cost)
    return out.getvalue().strip()

# provided samples
assert run("4\n1 10000\n10000 1\n2 6\n4 6\n") == "100000000\n1\n18\n10"

# custom cases
assert run("1\n5 3\n") == "3", "c_i > sum_i"
assert run("2\n1 1\n10 100\n") == "1\n1000", "single radiator vs many radiators"
assert run("1\n3 8\n") == "22", "unequal division"
assert run("1\n10000 10000\n") == "10000", "all ones"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1\n5 3 | 3 | When max radiators exceed sections |
| 2\n1 1\n10 100 | 1\n1000 | Mix of single and many radiators |
| 1\n3 8 | 22 | Uneven section distribution |
| 1\n10000 10000 | 10000 | Each radiator gets exactly 1 section |

## Edge Cases

If `c_i = 1`, we must place all sections in
