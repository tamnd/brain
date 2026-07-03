---
title: "CF 103081E - Cakes"
description: "We are given a recipe that consists of several ingredients, and for each ingredient we know two numbers: how much of it is needed to bake one cake and how much of it is currently available in the kitchen."
date: "2026-07-03T23:17:09+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 103081
codeforces_index: "E"
codeforces_contest_name: "2020-2021 ICPC Southwestern European Regional Contest (SWERC 2020)"
rating: 0
weight: 103081
solve_time_s: 40
verified: true
draft: false
---

[CF 103081E - Cakes](https://codeforces.com/problemset/problem/103081/E)

**Rating:** -  
**Tags:** -  
**Solve time:** 40s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a recipe that consists of several ingredients, and for each ingredient we know two numbers: how much of it is needed to bake one cake and how much of it is currently available in the kitchen. The task is to determine the maximum number of complete cakes we can bake such that no ingredient runs out.

A single cake requires satisfying all ingredient requirements simultaneously, so if any ingredient becomes insufficient, we cannot increase the number of cakes further. Each ingredient independently imposes an upper bound on how many cakes can be produced. The final answer is therefore governed by the most restrictive ingredient.

The constraints are extremely small, with at most 10 ingredients. This immediately suggests that even very direct computations are sufficient, since any solution that does constant work per ingredient will run instantly. There is no need for optimization beyond simple arithmetic.

A subtle edge case appears when an ingredient requirement is large relative to supply. For example, if one ingredient requires 10 units per cake and only 5 units are available, that ingredient alone forces the answer to zero cakes regardless of other abundances. Another case is when all ingredients are abundant except one extremely tight constraint, which becomes the bottleneck.

Example:

Input:

```
2 5
70 1000
```

The first ingredient allows at most 2 // 5 = 0 cakes, so the answer is 0 even though the second ingredient is plentiful. A naive approach that sums or averages ratios would be incorrect.

## Approaches

The brute-force idea is to simulate baking cakes one by one. For each attempted cake count k, we check whether every ingredient has at least k times its required amount available. We increase k until this condition fails. While correct, this approach performs up to O(answer × N) checks, and in pathological cases where ingredient amounts are large, the answer can reach 10^4 or more, making it unnecessarily repetitive compared to what is needed.

The key observation is that each ingredient independently limits the number of cakes. If an ingredient requires r units per cake and we have a units available, then the number of cakes allowed by that ingredient alone is a // r. Since all ingredients must be satisfied simultaneously, the overall answer is the minimum of these per-ingredient limits. This transforms the problem from repeated simulation into a single pass computation.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Simulation | O(N × answer) | O(1) | Too slow |
| Per-ingredient minimum | O(N) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the number of ingredients N, then read each pair of values representing required amount and available amount for each ingredient. This sets up the constraints that will define feasible cake production.
2. For each ingredient, compute how many cakes it can individually support by dividing available quantity by required quantity using integer division. This step converts raw resource constraints into a unified “cake capacity” metric.
3. Maintain a variable initialized to a very large value, representing the current best upper bound on the number of cakes.
4. For each ingredient, update this variable by taking the minimum between its current value and the computed capacity of the ingredient. This ensures that the final result respects the tightest constraint.
5. After processing all ingredients, output the final minimum value, which represents the maximum number of cakes that can be made without violating any constraint.

Why it works: each ingredient imposes an independent upper bound on feasible solutions. Any valid solution must satisfy all bounds simultaneously, so the solution space is the intersection of these constraints. The intersection of upper bounds is determined by the smallest bound, which guarantees that no ingredient is overused while maximizing the number of complete cakes.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    ans = 10**18

    for _ in range(n):
        need, have = map(int, input().split())
        ans = min(ans, have // need)

    print(ans)

if __name__ == "__main__":
    solve()
```

The solution reads input incrementally and maintains a running minimum. The key implementation detail is integer division, which correctly floors the number of possible cakes per ingredient. Initializing the answer to a very large number ensures the first ingredient properly sets the baseline.

A common mistake is reversing the division order. The correct computation is have // need, not need // have. The latter would invert the constraint and produce meaningless results. Another subtle point is ensuring integer division rather than floating point, since fractional cakes are irrelevant.

## Worked Examples

### Example 1

Input:

```
3
100 500
2 5
70 1000
```

| Step | Ingredient | Need | Have | Capacity | Current Min |
| --- | --- | --- | --- | --- | --- |
| 1 | 1 | 100 | 500 | 5 | 5 |
| 2 | 2 | 2 | 5 | 2 | 2 |
| 3 | 3 | 70 | 1000 | 14 | 2 |

The second ingredient is the limiting factor, producing only 2 cakes. This shows how a single tight constraint dominates the result even when others are generous.

### Example 2

Input:

```
2
3 10
4 5
```

| Step | Ingredient | Need | Have | Capacity | Current Min |
| --- | --- | --- | --- | --- | --- |
| 1 | 1 | 3 | 10 | 3 | 3 |
| 2 | 2 | 4 | 5 | 1 | 1 |

The second ingredient reduces the answer to 1. This confirms that even small differences in ratios can determine the final result.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(N) | Each ingredient is processed once with constant-time arithmetic |
| Space | O(1) | Only a single accumulator variable is used |

With N ≤ 10, the solution is trivially fast, and even larger constraints would comfortably fit within limits due to linear complexity.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from __main__ import solve
    import sys
    from io import StringIO
    old_stdout = sys.stdout
    sys.stdout = StringIO()
    solve()
    out = sys.stdout.getvalue()
    sys.stdout = old_stdout
    return out.strip()

# single ingredient
assert run("1\n3 10\n") == "3"

# bottleneck is zero
assert run("2\n5 4\n2 10\n") == "0"

# all equal ratios
assert run("3\n2 10\n3 15\n5 25\n") == "5"

# mixed constraints
assert run("4\n1 7\n2 8\n3 9\n4 10\n") == "2"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 ingredient | direct division | base case |
| one zero-capacity ingredient | 0 | hard bottleneck handling |
| proportional ingredients | consistent scaling | uniform ratios |
| mixed constraints | correct minimum selection | general correctness |

## Edge Cases

One important edge case is when an ingredient has insufficient quantity for even a single cake.

Input:

```
1
5 3
```

The algorithm computes 3 // 5 = 0. Since the running minimum starts large, it becomes 0 immediately and remains 0 until the end. This correctly reflects that no cakes are possible.

Another case is when all ingredients are identical in ratio.

Input:

```
3
2 10
2 10
2 10
```

Each ingredient yields 10 // 2 = 5, so the minimum remains 5 throughout. The algorithm does not mistakenly multiply or sum capacities, which would incorrectly inflate the result.
