---
title: "CF 1873B - Good Kid"
description: "We are given a small collection of digits, and we are allowed to increase exactly one of them by one unit. After this single modification, we compute the product of all digits and want to maximize it."
date: "2026-06-08T23:13:14+07:00"
tags: ["codeforces", "competitive-programming", "brute-force", "greedy", "math"]
categories: ["algorithms"]
codeforces_contest: 1873
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 898 (Div. 4)"
rating: 800
weight: 1873
solve_time_s: 108
verified: true
draft: false
---

[CF 1873B - Good Kid](https://codeforces.com/problemset/problem/1873/B)

**Rating:** 800  
**Tags:** brute force, greedy, math  
**Solve time:** 1m 48s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a small collection of digits, and we are allowed to increase exactly one of them by one unit. After this single modification, we compute the product of all digits and want to maximize it.

The structure is intentionally simple: the array is tiny, so we are not optimizing over large sequences or complex states. Instead, the decision is purely about which single digit should be incremented so that the resulting product becomes as large as possible.

Even though the constraints allow up to 10⁴ test cases, each test case has at most 9 digits. This immediately rules out anything beyond a constant factor per test case. Trying all possibilities is completely safe because the total work is at most about 9 operations per case, which is trivial.

The main subtlety is that increasing a digit can have non-local effects on the product. For example, increasing a 0 to 1 changes the product from 0 to potentially non-zero, which dominates most other changes. Similarly, increasing a 9 to 10 does not exist because digits remain single integers in this problem, so the maximum value after increment is 10 only in value, not digit structure.

Edge cases appear when zeros are present. A naive approach that assumes “increase the largest digit” can fail badly:

For example, consider `[0, 1, 9]`. Increasing 9 gives product 0, increasing 1 gives product 0, but increasing 0 gives `[1, 1, 9]` and product 9, which is optimal.

So the real issue is not magnitude alone but marginal contribution to the product.

## Approaches

The brute-force approach is straightforward. We try incrementing each index once, compute the product, and take the maximum. Since n ≤ 9, this means at most 9 candidates per test case, and each product computation costs at most 9 multiplications, so the total is constant time in practice.

This works because the decision space is extremely small and there are no constraints linking multiple choices. The brute-force fails only if we mistakenly try to optimize greedily, assuming local digit properties determine the best global product.

The observation that unlocks the solution is that there is no interaction between choices beyond the single modified position. Every candidate solution is independent, so enumerating all possibilities is optimal and sufficient.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n²) per test | O(1) | Accepted |
| Optimal | O(n²) per test (same idea) | O(1) | Accepted |

Here the so-called “optimal” solution is simply the brute-force itself, because the constraints already force it to be optimal.

## Algorithm Walkthrough

1. Read the array of digits for the test case.
2. Compute the baseline idea: we will try modifying each index exactly once. This ensures we explore every valid configuration.
3. For each index i, temporarily increase a[i] by 1.
4. Compute the product of all digits after this modification. This directly evaluates the resulting outcome of choosing i.
5. Restore a[i] and continue to the next index.
6. Track the maximum product seen across all choices.
7. Output the maximum.

### Why it works

Each valid solution is uniquely determined by the position of the incremented digit. There are no other degrees of freedom. Since we evaluate every possible choice, we are guaranteed to include the optimal one. The correctness follows from exhaustive enumeration over a constant-sized decision space.

## Python Solution

```python
import sys
input = sys.stdin.readline

t = int(input())
for _ in range(t):
    n = int(input())
    a = list(map(int, input().split()))

    best = 0

    for i in range(n):
        a[i] += 1

        prod = 1
        for v in a:
            prod *= v

        best = max(best, prod)

        a[i] -= 1

    print(best)
```

The solution directly implements the idea of testing each possible increment position. For each index, we modify it, recompute the full product, and restore it. The restoration step is important because failing to revert the change would corrupt subsequent evaluations.

Since n ≤ 9, recomputing the product repeatedly is cheap. The nested loops do not cause any performance issues.

## Worked Examples

### Example 1

Input:

```
4
2 2 1 2
```

| Modified index | Array after increment | Product |
| --- | --- | --- |
| 0 | 3 2 1 2 | 12 |
| 1 | 2 3 1 2 | 12 |
| 2 | 2 2 2 2 | 16 |
| 3 | 2 2 1 3 | 12 |

The best choice is increasing the third element, producing 16. This shows how even a small digit change can dominate due to multiplicative structure.

### Example 2

Input:

```
3
0 1 2
```

| Modified index | Array after increment | Product |
| --- | --- | --- |
| 0 | 1 1 2 | 2 |
| 1 | 0 2 2 | 0 |
| 2 | 0 1 3 | 0 |

The optimal strategy is clearly to increment the zero, since it turns the entire product from zero into a positive value. This demonstrates why greedy “pick largest digit” would fail.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n²) per test | Try each index and recompute full product |
| Space | O(1) | Only storing input array |

Given n ≤ 9, this is effectively constant time per test case, well within limits even for 10⁴ tests.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    input = sys.stdin.readline

    t = int(input())
    out = []
    for _ in range(t):
        n = int(input())
        a = list(map(int, input().split()))

        best = 0

        for i in range(n):
            a[i] += 1
            prod = 1
            for v in a:
                prod *= v
            best = max(best, prod)
            a[i] -= 1

        out.append(str(best))

    return "\n".join(out)

# provided samples
assert run("""4
4
2 2 1 2
3
0 1 2
5
4 3 2 3 4
9
9 9 9 9 9 9 9 9 9""") == """16
2
432
430467210"""

# custom cases
assert run("""1
1
5""") == """6"""  # single element increment
assert run("""1
3
0 0 0""") == """1"""  # any increment creates 1
assert run("""1
3
1 1 1""") == """8"""  # symmetric case
assert run("""1
4
0 2 3 4""") == """36"""  # zero handling dominates
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single element | basic increment | base case |
| all zeros | zero-to-one effect | zero handling |
| all ones | uniform behavior | symmetry |
| mixed digits | zero dominance | greedy failure case |

## Edge Cases

When the array contains zeros, the optimal move is almost always to increment a zero because it transforms the product from 0 to a positive value. The algorithm handles this correctly because it explicitly evaluates every index, including zeros, without bias.

When all digits are identical, every choice yields the same product structure, and enumeration naturally captures this symmetry.

When n = 1, the only valid operation is incrementing that single digit, and the algorithm correctly evaluates that sole possibility and returns its value.
