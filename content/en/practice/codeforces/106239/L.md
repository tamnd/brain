---
title: "CF 106239L - \u6c14\u7403\u91c7\u8d2d"
description: "We are given a set of $n$ different problem types, each associated with an expected probability ratio $pi / qi$ that models how many participants are expected to solve that problem."
date: "2026-06-19T16:27:51+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 106239
codeforces_index: "L"
codeforces_contest_name: "2025\u5e7f\u4e1c\u5de5\u4e1a\u5927\u5b66\u65b0\u751f\u8d5b(\u51b3\u8d5b)"
rating: 0
weight: 106239
solve_time_s: 49
verified: true
draft: false
---

[CF 106239L - \u6c14\u7403\u91c7\u8d2d](https://codeforces.com/problemset/problem/106239/L)

**Rating:** -  
**Tags:** -  
**Solve time:** 49s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a set of $n$ different problem types, each associated with an expected probability ratio $p_i / q_i$ that models how many participants are expected to solve that problem. There are $m$ participants in total, so for each problem type we estimate how many balloons of that color are needed by scaling this probability by $m$ and rounding up to the nearest integer.

Each problem type already has some number of balloons prepared. If the prepared amount is not enough for the estimated requirement, we buy the missing amount. If it is sufficient, we do nothing for that type. The task is to compute the total number of balloons that must be additionally purchased across all problem types.

The input sizes are very small, with at most 14 problem types and up to 200 participants. This immediately tells us that any solution even doing straightforward arithmetic per item is easily fast enough. The only real subtlety is correctness of the rounding step, since floating-point computation would be risky and unnecessary.

A common pitfall is computing $m \cdot p_i / q_i$ using floating-point arithmetic and then applying a cast or round. That can introduce precision errors, especially when values are close to an integer boundary. Another subtle issue is forgetting to apply ceiling correctly, for example using integer division directly which truncates instead of rounding up.

A concrete failure example is when $m = 10$, $p = 1$, $q = 11$. The true value is $10/11$, which should become 1 after ceiling. Integer division would give 0, which underestimates the requirement and leads to an incorrect shortage calculation.

## Approaches

The brute-force approach is already essentially optimal. For each problem type, we directly compute the required number of balloons using the definition and then compare it with what is already available. The cost per item is constant, so the total runtime is linear in $n$, which is at most 14.

If one were to interpret the computation literally using floating-point arithmetic, the implementation would still be trivial, but correctness becomes fragile. The key insight is that the required value is a ceiling of a rational number $m \cdot p_i / q_i$, and this can be computed exactly using integer arithmetic without any division precision issues.

The transformation comes from rewriting the ceiling operation in a way that avoids fractions entirely. Instead of computing a real number and rounding, we compute $\lceil x/y \rceil = (x + y - 1) // y$, which guarantees correctness for all positive integers. This removes floating-point entirely and makes the computation both exact and safe.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Direct floating-point computation | O(n) | O(1) | Risky |
| Integer ceiling formula | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

1. For each problem type, compute the total expected requirement numerator as $m \cdot p_i$. This represents the total expected number of solved instances scaled by participants.
2. Convert the ratio into an integer ceiling using the formula $(m \cdot p_i + q_i - 1) // q_i$. This ensures we always round up when there is any remainder after division.
3. Compare the computed requirement with the already available balloons $w_i$. If the requirement is larger, compute the difference.
4. Accumulate all positive differences into a running total. This sum represents the total number of balloons that must be purchased.
5. Output the final accumulated value after processing all problem types.

### Why it works

Each problem type is independent, so the total requirement is simply the sum of individual shortages. The ceiling formula guarantees that each $need_i$ is the smallest integer not less than the true fractional expectation. Since we only buy when supply is insufficient, each contribution to the answer is exactly the deficit for that type, and no interaction exists between categories that could invalidate summation.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, m = map(int, input().split())
    ans = 0

    for _ in range(n):
        p, q, w = map(int, input().split())
        need = (m * p + q - 1) // q
        if need > w:
            ans += need - w

    print(ans)

if __name__ == "__main__":
    solve()
```

The implementation directly follows the derived formula. The key line is the integer ceiling computation, which avoids any floating-point arithmetic entirely. The multiplication $m * p$ is safe because constraints are small, and Python handles large integers natively anyway. The subtraction step is guarded so we only accumulate shortages, ensuring we never incorrectly add surplus as negative values.

## Worked Examples

Consider a case with three problem types where $m = 10$. Suppose the inputs are $(p, q, w)$ as $(1, 1, 0)$, $(50, 100, 10)$, and $(1, 11, 0)$.

For the first type, the requirement is $\lceil 10 \cdot 1 / 1 \rceil = 10$, so the shortage is $10$.

For the second type, the requirement is $\lceil 10 \cdot 50 / 100 \rceil = \lceil 5 \rceil = 5$, and since $w = 10$, no purchase is needed.

For the third type, the requirement is $\lceil 10 \cdot 1 / 11 \rceil = 1$, so the shortage is $1$.

| i | p | q | m·p | need | w | deficit |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | 1 | 1 | 10 | 10 | 0 | 10 |
| 2 | 50 | 100 | 500 | 5 | 10 | 0 |
| 3 | 1 | 11 | 10 | 1 | 0 | 1 |

The table shows that each row is handled independently, and the final answer is the sum of deficits.

A second example can stress the ceiling behavior. Take $m = 7$, and a single problem with $p = 2$, $q = 3$, $w = 4$. The requirement is $\lceil 14/3 \rceil = 5$, so we need to buy 1 additional balloon. This confirms that truncation-based division would incorrectly give 4 and miss the required extra unit.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Each problem type is processed once with constant-time arithmetic |
| Space | O(1) | Only a running sum is maintained |

The constraints cap $n$ at 14, so even more expensive solutions would pass comfortably. This solution is well within limits and effectively constant time in practice.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    from math import ceil

    input = sys.stdin.readline

    def solve():
        n, m = map(int, input().split())
        ans = 0
        for _ in range(n):
            p, q, w = map(int, input().split())
            need = (m * p + q - 1) // q
            if need > w:
                ans += need - w
        print(ans)

    from io import StringIO
    out = io.StringIO()
    old_stdout = sys.stdout
    sys.stdout = out
    solve()
    sys.stdout = old_stdout
    return out.getvalue().strip()

# provided sample (first example described)
assert run("3 10\n1 1 0\n50 100 10\n1 11 0\n") == "11"

# minimum case
assert run("1 1\n1 1 0\n") == "1"

# already sufficient inventory
assert run("2 10\n1 1 10\n1 2 10\n") == "0"

# ceiling edge case
assert run("1 7\n2 3 4\n") == "1"

# large ratio check
assert run("1 200\n100 100 0\n") == "200"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single underflow | 1 | basic ceiling and deficit |
| all sufficient | 0 | no negative contribution |
| fractional rounding | 1 | correct ceiling behavior |
| max ratio | 200 | large multiplication correctness |

## Edge Cases

One important edge case is when the computed requirement is already exactly satisfied by existing balloons. For an input like $m = 10$, $p = 50$, $q = 100$, $w = 5$, the requirement becomes $\lceil 5 \rceil = 5$. The algorithm computes a deficit of zero because the comparison `need > w` fails. This confirms that equality does not trigger unnecessary purchases.

Another case is when the true fractional value is just above an integer boundary. For $m = 7$, $p = 2$, $q = 3$, we get $14/3$. The formula $(14 + 2)/3$ ensures correct rounding to 5, not 4. A naive integer division would produce 4 and silently undercount by one, which directly breaks correctness.
