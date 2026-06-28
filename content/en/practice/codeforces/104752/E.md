---
title: "CF 104752E - Exotic island"
description: "The shop has a single fixed bill denomination, and every item has a price in dollars. A tourist wants to pay for an item, but Juan can only use bills of that one denomination."
date: "2026-06-28T22:57:49+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104752
codeforces_index: "E"
codeforces_contest_name: "Concurso de programaci\u00f3n ANIEI 2023"
rating: 0
weight: 104752
solve_time_s: 80
verified: true
draft: false
---

[CF 104752E - Exotic island](https://codeforces.com/problemset/problem/104752/E)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 20s  
**Verified:** yes  

## Solution
## Problem Understanding

The shop has a single fixed bill denomination, and every item has a price in dollars. A tourist wants to pay for an item, but Juan can only use bills of that one denomination. The task is to determine how many such bills are needed so that their total value reaches the item price.

Since each bill contributes exactly $A$ dollars, we are effectively decomposing the price $B$ into multiples of $A$. If the price is not exactly divisible, we still need enough bills to cover it completely, because underpaying is not allowed in this interpretation. That turns the problem into computing the smallest integer $k$ such that $k \cdot A \ge B$.

The constraints go up to $10^9$, so any solution must run in constant time per test case. Iterating or simulating addition of bills would require up to $10^9$ steps in the worst case, which is far beyond a 1 second limit. This immediately suggests that the answer must be derived using arithmetic rather than simulation.

A subtle edge case is when $B$ is exactly divisible by $A$. For example, if $A = 5$ and $B = 10$, the answer is exactly 2. If $A = 5$ and $B = 11$, the answer becomes 3, not 2, because two bills only give 10 which is insufficient.

Another corner case appears when $A > B$. For instance, $A = 10$, $B = 3$. One bill is required because fractional payment is not possible and zero bills would not cover the price.

## Approaches

A brute-force approach would repeatedly subtract $A$ from $B$ until the remainder becomes non-positive. This is correct because each subtraction corresponds to using one bill. However, in the worst case where $A = 1$ and $B = 10^9$, this requires $10^9$ iterations, which is too slow.

The key observation is that we are computing how many full blocks of size $A$ fit into $B$, plus possibly one extra block if there is a remainder. This is exactly the ceiling of the division $B / A$. Once we recognize this, the problem reduces to a single integer arithmetic operation.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force subtraction | $O(B/A)$ | $O(1)$ | Too slow |
| Ceiling division | $O(1)$ | $O(1)$ | Accepted |

## Algorithm Walkthrough

### Optimal Strategy

1. Read integers $A$ and $B$. These represent the fixed bill value and the required payment amount.
2. Compute whether $B$ is divisible by $A$. If it is, the answer is exactly $B / A$, since bills fit perfectly without waste.
3. If $B$ is not divisible by $A$, compute $B // A + 1$. The integer division gives the number of full bills that fit, and the extra one covers the remaining unpaid amount.
4. Output the computed value.

The key decision point is the handling of the remainder. If we ignore it, we underpay; if we overcompensate by exactly one additional bill, we always reach or exceed the target with minimal excess.

### Why it works

Any solution corresponds to choosing an integer $k$ such that $kA \ge B$. The set of such integers starts at $\lceil B/A \rceil$. Any smaller value $k < \lceil B/A \rceil$ implies $kA < B$, which fails to cover the price. Any larger value increases cost unnecessarily. Therefore the ceiling division is the unique minimal valid choice.

## Python Solution

```python
import sys
input = sys.stdin.readline

A = int(input().strip())
B = int(input().strip())

# compute ceiling of B / A
ans = (B + A - 1) // A

print(ans)
```

The solution relies on the classic integer ceiling trick. Instead of explicitly checking divisibility, it uses the identity $\lceil B/A \rceil = (B + A - 1) // A$. This avoids branching and keeps the computation in a single arithmetic expression.

The subtraction by 1 inside the numerator ensures that exact multiples do not get incorrectly rounded up. For example, when $B = 10$ and $A = 5$, we get $(10 + 4) // 5 = 2$, while when $B = 11$, we get $(11 + 4) // 5 = 3$.

## Worked Examples

### Example 1

Input:

$A = 2$, $B = 10$

| Step | A | B | Computation | Result |
| --- | --- | --- | --- | --- |
| Start | 2 | 10 |  |  |
| Apply formula | 2 | 10 | (10 + 1) // 2 | 5 |

The result is 5, meaning five bills of value 2 exactly reach 10. This confirms the formula works cleanly when division is exact.

### Example 2

Input:

$A = 5$, $B = 5$

| Step | A | B | Computation | Result |
| --- | --- | --- | --- | --- |
| Start | 5 | 5 |  |  |
| Apply formula | 5 | 5 | (5 + 4) // 5 | 1 |

Here one bill is sufficient because the price matches the denomination exactly. The computation does not overcount.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(1)$ | Only a few arithmetic operations are performed regardless of input size |
| Space | $O(1)$ | No auxiliary data structures are used |

The constraints allow values up to $10^9$, but the solution does not depend on iteration or recursion. It remains constant time and easily fits within limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    A = int(input().strip())
    B = int(input().strip())
    ans = (B + A - 1) // A
    return str(ans)

# provided samples (interpreted as A then B per statement)
assert run("2\n10\n") == "5", "sample 1"
assert run("5\n5\n") == "1", "sample 2"
assert run("3\n10\n") == "4", "sample 3"

# custom cases
assert run("1\n1000000000\n") == "1000000000", "unit denomination"
assert run("1000000000\n1\n") == "1", "large A small B"
assert run("7\n49\n") == "7", "exact division"
assert run("7\n50\n") == "8", "off-by-one remainder"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1, 1e9 | 1e9 | minimal denomination edge |
| 1e9, 1 | 1 | large divisor case |
| 7, 49 | 7 | exact division correctness |
| 7, 50 | 8 | ceiling behavior |

## Edge Cases

When $A = 1$, every dollar requires one bill. The algorithm computes $(B + 0) // 1 = B$, producing the correct linear result without special handling.

When $A > B$, say $A = 10$, $B = 3$, the formula gives $(3 + 9) // 10 = 1$. This matches the requirement that at least one bill must be used even though it overpays.

When $B$ is exactly a multiple of $A$, such as $A = 5$, $B = 20$, the expression yields $(20 + 4) // 5 = 4$, avoiding unnecessary rounding up and confirming the tightness of the ceiling formulation.
