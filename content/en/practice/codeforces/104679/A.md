---
title: "CF 104679A - First Year, Second Year"
description: "We are given two numbers that summarize an unknown pair of positive integers. One number represents their sum, and the other represents their difference, where the difference is taken as first minus second. From these two values, we need to reconstruct the original pair."
date: "2026-06-29T09:00:42+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104679
codeforces_index: "A"
codeforces_contest_name: "Replay of Battle of Brains 2022, University of Dhaka"
rating: 0
weight: 104679
solve_time_s: 48
verified: true
draft: false
---

[CF 104679A - First Year, Second Year](https://codeforces.com/problemset/problem/104679/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 48s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given two numbers that summarize an unknown pair of positive integers. One number represents their sum, and the other represents their difference, where the difference is taken as first minus second. From these two values, we need to reconstruct the original pair.

The task is essentially to invert a simple linear system. Instead of being given the two unknown integers directly, we are given two combined measurements of them and must recover the original values uniquely.

The constraints are minimal in structure since the computation is purely arithmetic. This implies the solution must run in constant time per test case, since any loop over large ranges would be unnecessary overhead. The expected approach should therefore be direct algebraic manipulation.

A subtle issue arises from validity of the reconstructed values. Since the original integers are positive, the computed results must also be positive integers. Another important edge case is parity: if the sum and difference do not produce integer results when divided by two, then the input is inconsistent with any valid integer pair.

For example, if the input is sum 5 and difference 2, the reconstruction works cleanly. But if the input is sum 5 and difference 3, then both reconstructed values become non-integers, which signals invalidity in a strict integer setting.

## Approaches

A brute-force interpretation would try all possible pairs of positive integers and check which pair matches both the given sum and difference. For each candidate x and y, we would verify whether x + y equals the given sum and x − y equals the given difference. This works conceptually because it exhaustively searches the solution space.

However, the number of candidate pairs grows quadratically with the size of the sum. If the sum is on the order of 10^9, the number of pairs to check is proportional to that magnitude squared, which is computationally infeasible.

The key observation is that the two equations already define a linear system. Instead of searching, we can directly solve for the unknowns by eliminating variables. Adding both equations isolates one variable, and subtracting them isolates the other. This reduces the problem from search to constant-time arithmetic.

The structure of the problem is what enables this reduction. The constraints do not introduce any nonlinear behavior or additional conditions that would complicate inversion, so direct algebra fully determines the solution.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(S²) | O(1) | Too slow |
| Optimal | O(1) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the two given values, which represent the sum of the unknown numbers and their difference in a fixed order.

The order matters because the difference determines which variable is larger.
2. Use the relationship between the two equations to isolate the first number. Adding the sum and difference cancels the second variable, leaving twice the first number.
3. Divide the result by two to obtain the first original number. This division is guaranteed to be valid only if the input is consistent with integer solutions.
4. Compute the second number by subtracting the first number from the sum, or equivalently by subtracting the difference from the sum and dividing by two.
5. Output both reconstructed values.

Why it works: the system defines a unique linear intersection point in two dimensions. The transformation from original variables to sum and difference is invertible as long as arithmetic division by two yields integers. Since addition and subtraction are linear operations, reversing them preserves consistency and guarantees that the reconstructed pair satisfies both original equations exactly.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    data = input().split()
    S = int(data[0])
    D = int(data[1])

    x = (S + D) // 2
    y = (S - D) // 2

    print(x, y)

if __name__ == "__main__":
    solve()
```

The solution reads the two input values and immediately applies the algebraic inversion of the system. The expression (S + D) corresponds to twice the first number, while (S − D) corresponds to twice the second number. Integer division is used because the problem guarantees valid inputs where the reconstruction is exact.

A common mistake is reversing the signs or swapping the formulas, which produces correct-looking but incorrect pairs. Another subtle issue is forgetting that both values must be integers, but in standard competitive programming settings for this problem, the input is constructed to avoid fractional outcomes.

## Worked Examples

### Example 1

Input:

S = 10, D = 4

We compute the reconstructed values step by step.

| Step | Expression | Value |
| --- | --- | --- |
| Sum | S | 10 |
| Difference | D | 4 |
| First number | (S + D) / 2 | 7 |
| Second number | (S − D) / 2 | 3 |

This confirms that 7 + 3 = 10 and 7 − 3 = 4, so the reconstruction is consistent. The trace shows that the transformation cleanly separates the two unknowns without ambiguity.

### Example 2

Input:

S = 8, D = 2

| Step | Expression | Value |
| --- | --- | --- |
| Sum | S | 8 |
| Difference | D | 2 |
| First number | (S + D) / 2 | 5 |
| Second number | (S − D) / 2 | 3 |

Here the reconstructed pair is 5 and 3. Verifying back substitution confirms correctness. This example reinforces that the procedure is symmetric and independent of scale.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(1) | Only a fixed number of arithmetic operations are performed |
| Space | O(1) | No additional data structures are used |

The computation remains constant regardless of input size, which fits easily within typical competitive programming limits where even large batches of test cases would not affect performance.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from contextlib import redirect_stdout
    out = io.StringIO()
    with redirect_stdout(out):
        solve()
    return out.getvalue().strip()

def solve():
    import sys
    input = sys.stdin.readline
    S, D = map(int, input().split())
    x = (S + D) // 2
    y = (S - D) // 2
    print(x, y)

assert run("10 4\n") == "7 3", "sample 1"
assert run("8 2\n") == "5 3", "sample 2"

assert run("2 0\n") == "1 1", "minimum equal numbers"
assert run("1000000000 0\n") == "500000000 500000000", "large equal case"
assert run("9 1\n") == "5 4", "odd sum with valid reconstruction"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 2 0 | 1 1 | Minimum symmetric case |
| 1000000000 0 | 500000000 500000000 | Large values stability |
| 9 1 | 5 4 | General odd-sum reconstruction |

## Edge Cases

One edge case is when the difference is zero. For input 2 and 0, the reconstruction yields both values equal. The algorithm computes (2 + 0) / 2 = 1 and (2 − 0) / 2 = 1, producing a valid identical pair. This confirms that the method naturally handles symmetry without special branching.

Another case is when the sum is large but the difference is also large and close to the sum. For input 100 and 98, the computation yields x = 99 and y = 1. The arithmetic remains stable because both expressions still produce non-negative integers, and the subtraction does not introduce overflow or precision issues in Python.

A final edge case is parity consistency. If a hypothetical input such as 5 and 2 were allowed, the formulas would produce fractional values. The algorithm assumes inputs are constructed so that both (S + D) and (S − D) are even, ensuring integer outputs.
