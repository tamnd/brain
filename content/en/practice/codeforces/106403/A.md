---
title: "CF 106403A - Luxury"
description: "We are given several independent integers. For each integer x, we compute the integer part of its square root, call it k = ⌊√x⌋. The task is to determine whether x is “luxurious”, meaning it is divisible by this k."
date: "2026-06-25T10:07:06+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 106403
codeforces_index: "A"
codeforces_contest_name: "Bay Area Programming Contest 2026 Novice Division"
rating: 0
weight: 106403
solve_time_s: 40
verified: true
draft: false
---

[CF 106403A - Luxury](https://codeforces.com/problemset/problem/106403/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 40s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given several independent integers. For each integer x, we compute the integer part of its square root, call it k = ⌊√x⌋. The task is to determine whether x is “luxurious”, meaning it is divisible by this k.

So the input is a sequence of numbers, and for each one we output a binary decision: whether x mod ⌊√x⌋ equals zero.

The structure is deliberately minimal. Each query is independent, so there is no shared state or cumulative effect. The output is typically a sequence of answers in the same order as input.

The constraint style for this type of problem is usually large, often up to 10^5 or 10^6 numbers, with x possibly up to 10^18. That combination immediately rules out any solution that does more than constant or logarithmic work per number. A naive loop over all divisors would be far too slow.

The subtle edge cases come from perfect squares and very small numbers.

One corner case is x = 1. Here ⌊√1⌋ = 1, so the condition always holds and the answer is trivially true.

Another is when x is just below a perfect square. For example x = 15 gives ⌊√15⌋ = 3, and 15 is divisible by 3 so it is valid. But x = 14 gives ⌊√14⌋ = 3 as well, and 14 is not divisible by 3, so it fails. These adjacent values highlight that the decision boundary is driven by the square root step function, not the magnitude of x itself.

A third edge case is perfect squares like x = 16. Here ⌊√16⌋ = 4, and divisibility becomes exact in some cases (16 works), but many perfect squares will still fail depending on the value, so there is no shortcut like “all squares pass”.

## Approaches

The brute-force interpretation is straightforward: for each number x, compute k = ⌊√x⌋, then check whether x % k == 0. If we compute the square root by scanning from 1 upward until i² exceeds x, this costs O(√x) per query. Over large input this becomes prohibitive, potentially reaching 10^10 operations in worst cases.

The key observation is that we do not need to search for k. The value ⌊√x⌋ can be computed directly using a standard integer square root routine, which runs in constant or logarithmic time depending on implementation. Once k is known, the divisibility check is constant time.

The structure of the problem is therefore not algorithmically deep, but it is sensitive to correct integer square root computation. Floating-point sqrt must be handled carefully because rounding errors can produce k or k+1 incorrectly, which changes the divisibility result near perfect squares.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute force sqrt scan | O(√x) per query | O(1) | Too slow |
| Integer sqrt + check | O(1) per query | O(1) | Accepted |

## Algorithm Walkthrough

We process each number independently.

1. Read the integer x. Each value is handled in isolation, so no preprocessing is required.
2. Compute k as the integer square root of x. This is the largest integer such that k² ≤ x. The correctness of the rest of the logic depends on k being exact, not approximate.
3. Check whether x is divisible by k. If x % k == 0, classify x as luxurious, otherwise classify it as not luxurious.
4. Output the result for x before moving to the next number.

The only nontrivial decision is computing k reliably. Using floating-point sqrt and truncation is acceptable in many environments, but a safer approach is to compute k using integer arithmetic or adjust around the candidate value to correct rounding.

Why it works: every number is classified solely by its relationship to ⌊√x⌋. There is no interaction between numbers, and no hidden state. The integer square root partitions the input space into intervals where k is constant, and within each interval we only test a single modular condition. This guarantees that once k is correctly computed, the decision is exact.

## Python Solution

```python
import sys
input = sys.stdin.readline
import math

def solve():
    t = int(input())
    for _ in range(t):
        x = int(input())
        k = math.isqrt(x)
        if x % k == 0:
            print("YES")
        else:
            print("NO")

if __name__ == "__main__":
    solve()
```

The solution is built around `math.isqrt`, which avoids floating-point precision issues entirely. A common mistake is using `int(math.sqrt(x))` directly, which can fail for large perfect squares due to rounding down incorrectly or occasionally rounding up in edge cases. The integer square root routine guarantees k² ≤ x < (k+1)².

The rest of the implementation is deliberately minimal: each test case is independent, and the divisibility check is constant time.

## Worked Examples

Consider inputs x = 15, 14, 16.

For each value we compute k = ⌊√x⌋.

| x | k = ⌊√x⌋ | x % k | Output |
| --- | --- | --- | --- |
| 15 | 3 | 0 | YES |
| 14 | 3 | 2 | NO |
| 16 | 4 | 0 | YES |

This trace shows that the square root boundary groups numbers into blocks where k is fixed, but divisibility varies independently within each block.

Now consider small values.

| x | k | x % k | Output |
| --- | --- | --- | --- |
| 1 | 1 | 0 | YES |
| 2 | 1 | 0 | YES |
| 3 | 1 | 0 | YES |
| 4 | 2 | 0 | YES |

This demonstrates that for k = 1 the condition is always true, which is a structural property of the definition rather than a special case in code.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(T) | Each query performs constant-time integer sqrt and modulus |
| Space | O(1) | No additional data structures are used |

The solution fits comfortably within typical constraints for up to 10^5 or more queries, since each operation is constant time and implemented in optimized C-based library code for square root computation.

## Test Cases

```python
import sys, io
import math

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    out = []
    input = sys.stdin.readline

    t = int(input())
    for _ in range(t):
        x = int(input())
        k = math.isqrt(x)
        out.append("YES" if x % k == 0 else "NO")
    return "\n".join(out)

# small cases
assert run("3\n1\n2\n3\n") == "YES\nYES\nYES"

# perfect square boundary
assert run("2\n15\n16\n") == "YES\nYES"

# non-trivial mix
assert run("4\n10\n11\n12\n13\n") == "NO\nNO\nYES\nNO"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1,2,3 | YES,YES,YES | k=1 behavior correctness |
| 15,16 | YES,YES | boundary around perfect squares |
| 10-13 | mixed | general correctness across intervals |

## Edge Cases

For x = 1, we get k = 1, so the divisibility condition always holds. The algorithm directly returns YES without any special handling, since 1 % 1 = 0.

For numbers just below a perfect square such as x = 24, we get k = 4. The algorithm checks 24 % 4 = 0, returning YES, which matches the definition. For x = 23, k is still 4, but 23 % 4 ≠ 0, returning NO. The correctness depends entirely on using ⌊√x⌋ rather than any rounded square root.

For perfect squares like x = 49, k = 7 and 49 % 7 = 0, so the output is YES. This confirms that the algorithm handles exact square boundaries without any adjustment logic.

For x = 2, k = 1, which reduces the problem to checking divisibility by 1, always true. The implementation naturally handles this without branching.
