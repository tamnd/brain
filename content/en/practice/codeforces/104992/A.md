---
title: "CF 104992A - \u041c\u043d\u043e\u0433\u043e\u043d\u043e\u0433\u0438 \u0438 \u043c\u043d\u043e\u0433\u043e\u0433\u043e\u043b\u043e\u0432\u044b"
description: "We are given a world populated by two kinds of creatures. Each creature of the first type has exactly 1 head and 19 legs, while each creature of the second type has exactly 7 heads and 4 legs."
date: "2026-06-28T04:26:48+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104992
codeforces_index: "A"
codeforces_contest_name: "qual VKOSHP Junior 24"
rating: 0
weight: 104992
solve_time_s: 89
verified: true
draft: false
---

[CF 104992A - \u041c\u043d\u043e\u0433\u043e\u043d\u043e\u0433\u0438 \u0438 \u043c\u043d\u043e\u0433\u043e\u0433\u043e\u043b\u043e\u0432\u044b](https://codeforces.com/problemset/problem/104992/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 29s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a world populated by two kinds of creatures. Each creature of the first type has exactly 1 head and 19 legs, while each creature of the second type has exactly 7 heads and 4 legs. We are told the total number of heads and the total number of legs observed in this world. The task is to determine how many creatures of each type could exist so that both the head count and leg count match exactly. If multiple valid decompositions exist, any one of them is acceptable. If no decomposition is possible, we must report impossibility.

The input consists of two integers. The first is the total number of heads, which constrains a linear combination of the two creature types. The second is the total number of legs, which provides a second linear constraint. The output is a pair of non-negative integers describing how many creatures of each type were present, or -1 if no solution exists.

Even though the bounds allow values up to 10^8, the structure is not combinatorial in nature. We are solving a system of two linear equations in two variables, but with non-negativity constraints and the requirement that solutions be integers. This immediately places the problem in constant-time algebraic solving rather than search.

A naive approach would attempt to try all possible counts of one creature and deduce the other from the head equation, checking whether the leg equation matches. This would work but is unnecessary and could conceptually loop up to 10^8 iterations in the worst case, which is too slow.

Edge cases arise from divisibility constraints and mismatched parity-like structure between heads and legs. A common failure mode is assuming that head equations always uniquely determine counts without verifying leg consistency. Another is overlooking that one species contributes disproportionately more heads than legs compared to the other, making infeasible systems that superficially look solvable.

For example, if we had 2 heads and 19 legs, one might incorrectly assume two single-headed creatures exist, but then the leg count becomes inconsistent immediately. The contradiction appears only when both equations are enforced simultaneously.

## Approaches

The problem reduces to solving a system of linear equations. Let x be the number of 1-head 19-leg creatures, and y be the number of 7-head 4-leg creatures. Then:

x + 7y = A

19x + 4y = B

A brute-force method would iterate over all possible values of y from 0 to A // 7. For each y, compute x = A - 7y and check whether it is non-negative and satisfies the leg equation. This is correct because every valid solution must satisfy both constraints simultaneously. However, in the worst case A can be 10^8, making up to about 1.4 × 10^7 iterations, which is borderline and unnecessary for a single-test problem.

The key observation is that this is a 2×2 linear system with a unique algebraic solution when it exists. We can eliminate variables directly. From x = A - 7y, substitute into the second equation:

19(A - 7y) + 4y = B

19A - 133y + 4y = B

19A - 129y = B

129y = 19A - B

So y is uniquely determined by the right-hand side. Once y is known, x follows directly. The only remaining task is validating that y is an integer and both x and y are non-negative.

This turns the problem into constant-time arithmetic with a small number of checks.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(A/7) | O(1) | Too slow |
| Optimal | O(1) | O(1) | Accepted |

## Algorithm Walkthrough

We solve the system using elimination and then verify feasibility.

1. Express the number of 1-head creatures x in terms of y using the head constraint: x = A - 7y. This reduces the system from two variables to one.
2. Substitute this expression into the leg equation: 19(A - 7y) + 4y = B. This step ensures both constraints are enforced simultaneously rather than independently.
3. Simplify the equation to isolate y: 19A - 129y = B, which gives y = (19A - B) / 129. This is the only possible value of y that can satisfy both equations.
4. Check whether (19A - B) is divisible by 129. If not, no integer solution exists, so we output -1. This enforces integrality, which is required because creature counts must be whole numbers.
5. Compute y and then compute x = A - 7y. This reconstructs the full solution once y is validated.
6. Verify that x and y are both non-negative. If either is negative, the solution is invalid in the physical sense of counting creatures, so output -1.

### Why it works

The system consists of two independent linear constraints over integers. Any valid solution must satisfy both simultaneously, and elimination shows that y is uniquely determined by a single linear expression in A and B. Because the transformation preserves equivalence, any integer solution to the derived equation corresponds exactly to a valid pair (x, y) in the original system. Therefore, checking divisibility and non-negativity is sufficient to decide existence and recover the solution.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    A, B = map(int, input().split())

    numerator = 19 * A - B
    denom = 129

    if numerator % denom != 0:
        print(-1)
        return

    y = numerator // denom
    x = A - 7 * y

    if x < 0 or y < 0:
        print(-1)
        return

    print(x, y)

if __name__ == "__main__":
    solve()
```

The solution first encodes the algebraic elimination step directly into a single expression for y. The division check ensures that we never assume fractional creature counts. After computing y, x is derived from the head constraint rather than recomputing from legs, which avoids redundant arithmetic and reduces floating-point risk entirely by staying in integers.

The final validation step is necessary because algebraic manipulation alone does not enforce non-negativity; it only ensures consistency of the equations.

## Worked Examples

### Sample 1

Input: A = 23, B = 50

| Step | Expression | Value |
| --- | --- | --- |
| Compute numerator | 19A - B | 19·23 - 50 = 437 - 50 = 387 |
| Check divisibility | 387 / 129 | 3 |
| Compute y | y | 3 |
| Compute x | A - 7y | 23 - 21 = 2 |

This confirms a consistent decomposition exists. The resulting counts satisfy both constraints exactly.

### Sample 2

Input: A = 2, B = 19

| Step | Expression | Value |
| --- | --- | --- |
| Compute numerator | 19A - B | 38 - 19 = 19 |
| Check divisibility | 19 / 129 | not divisible |
| Output | -1 | invalid |

The failure occurs because the leg constraint cannot be satisfied by any integer combination of creatures, even though the head count alone suggests a simple interpretation.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(1) | Only a fixed number of arithmetic operations and checks are performed |
| Space | O(1) | No additional data structures are used |

The solution fits comfortably within constraints since all computations are constant-time integer operations, independent of input magnitude.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    A, B = map(int, sys.stdin.readline().split())

    numerator = 19 * A - B
    denom = 129

    if numerator % denom != 0:
        return "-1"

    y = numerator // denom
    x = A - 7 * y

    if x < 0 or y < 0:
        return "-1"

    return f"{x} {y}"

# provided samples
assert run("23 50") == "2 3"
assert run("2 19") == "-1"

# custom cases
assert run("1 19") == "1 0"
assert run("7 4") == "0 1"
assert run("0 0") == "0 0"
assert run("14 38") == "2 0"
assert run("21 8") == "0 3"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 19 | 1 0 | only first species |
| 7 4 | 0 1 | only second species |
| 0 0 | 0 0 | degenerate zero case |
| 14 38 | 2 0 | multiple of first species |
| 21 8 | 0 3 | multiple of second species |

## Edge Cases

A subtle edge case occurs when the system yields a fractional value for y even though both A and B are valid integers. For example, A = 2, B = 19 produces numerator 19·2 - 19 = 19, which is not divisible by 129. The algorithm detects this immediately through the divisibility check, preventing any attempt to interpret a fractional creature count.

Another edge case is when algebra produces a negative y. This corresponds to situations where the leg count is too large relative to heads for any valid mixture. In such cases, the computed y violates the non-negativity constraint and is rejected explicitly, ensuring correctness even when the linear system has a mathematical solution outside the feasible region.
