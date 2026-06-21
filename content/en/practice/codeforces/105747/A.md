---
title: "CF 105747A - Fahim Hates Juice"
description: "The task describes a very simple production process: each glass of mixed fruit juice consumes exactly one mango and one orange."
date: "2026-06-22T04:41:06+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105747
codeforces_index: "A"
codeforces_contest_name: "Bangladesh Olympiad in Informatics 2025 Preliminary Round"
rating: 0
weight: 105747
solve_time_s: 45
verified: true
draft: false
---

[CF 105747A - Fahim Hates Juice](https://codeforces.com/problemset/problem/105747/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 45s  
**Verified:** yes  

## Solution
## Problem Understanding

The task describes a very simple production process: each glass of mixed fruit juice consumes exactly one mango and one orange. We are given two quantities, the number of mangoes available and the number of oranges available, and we must determine how many complete glasses of juice can be made.

Each glass is constrained by both ingredients simultaneously. Even if one fruit is abundant, a glass cannot be formed without the other, so the limiting factor is always whichever fruit runs out first during pairing.

The input consists of two integers representing the available counts of mangoes and oranges. The output is a single integer representing the maximum number of full juice glasses that can be produced.

The constraints allow values up to 10^9. This immediately rules out any approach that simulates consumption one glass at a time. A linear simulation would require up to 10^9 iterations in the worst case, which is far beyond typical time limits. The problem therefore requires reasoning in constant time.

A subtle edge case appears when the two quantities are extremely unbalanced. For example, if the input is 1 1000000000, only one glass can be produced even though there is a huge surplus of oranges. A naive greedy loop that repeatedly subtracts until one value reaches zero would still produce the correct answer logically, but would be computationally infeasible.

## Approaches

A brute-force strategy would repeatedly form a glass by decrementing both mango and orange counts until one of them becomes zero. Each iteration corresponds to producing one glass, so the number of iterations equals the answer.

This approach is correct because it directly simulates the problem statement. However, in the worst case, when both M and O are 10^9, it would require 10^9 iterations. Each iteration performs constant work, so the total complexity becomes O(min(M, O)), which is too slow for typical execution constraints.

The key observation is that each operation consumes exactly one unit from both resources. Therefore, the process stops precisely when one resource is exhausted. The number of complete operations is entirely determined by the smaller of the two initial values. Instead of simulating step-by-step consumption, we can compute the result directly as the minimum of the two numbers.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(min(M, O)) | O(1) | Too slow |
| Optimal | O(1) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the two integers representing the available quantities of mangoes and oranges. These values define how many times we can perform the pairing operation.
2. Observe that each operation consumes exactly one mango and one orange, so the total number of operations is limited by whichever resource is smaller.
3. Compute the minimum of the two values. This directly corresponds to the number of full glasses that can be formed before one ingredient runs out.
4. Output this computed minimum as the final answer.

### Why it works

At every step of making juice, both resources decrease by exactly one unit. This means the difference between the two quantities remains constant throughout the process. Eventually, one of them reaches zero first, and at that moment no further full pairs can be formed. The total number of successful operations is therefore exactly the initial count of the smaller resource, since it is the bottleneck from the start.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    data = input().strip().split()
    m = int(data[0])
    o = int(data[1])
    return str(min(m, o))

if __name__ == "__main__":
    sys.stdout.write(solve())
```

The solution reads the two integers from input, converts them into numeric form, and directly computes their minimum. The result is returned as a string for output. The logic is fully contained in a single computation, avoiding loops entirely. The key implementation detail is to ensure correct parsing of input and handling of whitespace, since the input is provided on a single line.

## Worked Examples

### Example 1: Input `3 5`

| Step | Mangoes | Oranges | Action |
| --- | --- | --- | --- |
| Start | 3 | 5 | Initial state |
| 1 | 2 | 4 | Form 1 glass |
| 2 | 1 | 3 | Form 1 glass |
| 3 | 0 | 2 | Form 1 glass |

At this point mangoes are exhausted, so no further glasses can be made. The process stops at 3 glasses. This confirms that the limiting resource is mangoes.

### Example 2: Input `4 4`

| Step | Mangoes | Oranges | Action |
| --- | --- | --- | --- |
| Start | 4 | 4 | Initial state |
| 1 | 3 | 3 | Form 1 glass |
| 2 | 2 | 2 | Form 1 glass |
| 3 | 1 | 1 | Form 1 glass |
| 4 | 0 | 0 | Form 1 glass |

Both resources deplete simultaneously, so all 4 possible pairs are formed. This demonstrates the balanced case where neither resource is wasted.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(1) | Only a constant-time minimum operation is performed |
| Space | O(1) | No additional data structures are used |

The solution easily fits within the constraints since it performs a fixed number of operations regardless of input size, even for values up to 10^9.

## Test Cases

```python
import sys, io

def solve():
    data = sys.stdin.readline().strip().split()
    m = int(data[0])
    o = int(data[1])
    return str(min(m, o))

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    return solve().strip()

# provided samples
assert run("3 5\n") == "3", "sample 1"
assert run("4 4\n") == "4", "sample 2"

# custom cases
assert run("1 1000000000\n") == "1", "single mango limits output"
assert run("1000000000 1\n") == "1", "single orange limits output"
assert run("0 0\n") == "0", "both zero edge case"
assert run("7 2\n") == "2", "unequal small values"
assert run("10 10\n") == "10", "equal values"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 1000000000 | 1 | extreme imbalance, small first value |
| 1000000000 1 | 1 | symmetric imbalance |
| 0 0 | 0 | degenerate case with no resources |
| 7 2 | 2 | general unequal case |
| 10 10 | 10 | balanced equality case |

## Edge Cases

For extremely skewed inputs such as `1 1000000000`, a naive loop would attempt one billion iterations. The optimal solution instead directly computes `min(1, 1000000000)` and returns 1 immediately, avoiding any simulation.

For balanced large inputs like `1000000000 1000000000`, both resources deplete together. The algorithm correctly returns the full value without any risk of overflow or iterative error, since it relies only on a constant-time comparison rather than repeated subtraction.
