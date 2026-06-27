---
title: "CF 105129D - Two Triangles"
description: "Each test case describes a right-angled triangle using its base and height. The task is not to compute the actual geometric area, but instead to output twice that area. A right triangle’s area is computed as half of the product of its base and height."
date: "2026-06-27T18:53:20+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105129
codeforces_index: "D"
codeforces_contest_name: "Shorouk Academy 2024 Collegiate Programming Contest"
rating: 0
weight: 105129
solve_time_s: 38
verified: true
draft: false
---

[CF 105129D - Two Triangles](https://codeforces.com/problemset/problem/105129/D)

**Rating:** -  
**Tags:** -  
**Solve time:** 38s  
**Verified:** yes  

## Solution
## Problem Understanding

Each test case describes a right-angled triangle using its base and height. The task is not to compute the actual geometric area, but instead to output twice that area.

A right triangle’s area is computed as half of the product of its base and height. Since the problem explicitly asks for double the area, the fraction disappears and each test case reduces to a simple multiplication of the two given integers.

The input begins with a number indicating how many triangles we will process. Then each subsequent line provides the base and height of one triangle. For every pair, we must output a single integer representing $b \times h$.

The constraints are small, with both dimensions up to 500. Even if there are many test cases, the operation per case is constant time arithmetic on small integers. This means any correct solution runs comfortably within limits as long as it avoids unnecessary overhead.

The main failure mode in similar problems usually comes from misreading the input format or forgetting that the requested quantity is twice the area rather than the area itself. Another subtle issue is treating the computation as floating point division by two and then multiplying again, which is unnecessary and may introduce precision handling that is not needed here.

## Approaches

The most direct way to think about the problem is to apply the definition of triangle area literally for each test case. For a given base and height, compute $\frac{b \cdot h}{2}$, then multiply by 2 as requested. This immediately simplifies to $b \cdot h$, so the intermediate division step serves no purpose.

A brute-force implementation might still follow the formula exactly: compute the product, divide by two, then multiply by two. This is correct mathematically, but it introduces redundant operations and potential floating-point use if implemented carelessly. The computational cost remains trivial since each test case requires only a few arithmetic operations, so performance is never the limiting factor.

The key observation is that the problem is designed to test whether the solver recognizes algebraic simplification. The structure of the formula cancels out the only nontrivial operation, leaving a direct multiplication.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Literal formula evaluation | O(T) | O(1) | Accepted but unnecessary |
| Direct simplification | O(T) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the number of test cases $T$, which determines how many independent computations must be performed.
2. For each test case, read two integers $b$ and $h$, representing the dimensions of a right triangle.
3. Compute the product $b \times h$, which corresponds to twice the triangle’s area after simplification.
4. Output the computed value immediately for each test case.

### Why it works

The area of a right triangle is defined as $\frac{b \cdot h}{2}$. The problem requests twice this value, so the factor of $\frac{1}{2}$ cancels exactly with the multiplication by 2. This leaves a direct equality between the required output and the product $b \cdot h$. Since each test case is independent and involves only constant-time arithmetic, processing them sequentially preserves correctness without requiring any additional state or preprocessing.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    out = []
    for _ in range(t):
        b, h = map(int, input().split())
        out.append(str(b * h))
    sys.stdout.write("\n".join(out))

if __name__ == "__main__":
    solve()
```

The solution reads all test cases sequentially and stores results in a list before printing them at once. This avoids repeated I/O calls, which is a standard optimization in Python competitive programming.

The only computation inside the loop is a single integer multiplication. No floating-point arithmetic is used, which avoids precision issues entirely. The use of buffered output ensures that even large values of $T$ are handled efficiently.

## Worked Examples

Consider an input with two triangles:

Input:

```
2
4 8
10 12
```

For each test case, we track the computation.

| Test Case | b | h | b × h | Output |
| --- | --- | --- | --- | --- |
| 1 | 4 | 8 | 32 | 32 |
| 2 | 10 | 12 | 120 | 120 |

The first triangle produces 32, and the second produces 120. Each output is independent, confirming that no shared state is involved across test cases.

This trace shows that the algorithm directly transforms each input pair into its product without intermediate steps, matching the simplified mathematical form.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(T) | Each test case requires one multiplication and constant-time parsing |
| Space | O(1) | Aside from output storage, no auxiliary data structures are used |

The constraints allow up to a moderate number of test cases with small integer values, so a linear scan over the input is easily sufficient.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()
    
    import sys as _sys
    input = _sys.stdin.readline

    t = int(input())
    out = []
    for _ in range(t):
        b, h = map(int, input().split())
        out.append(str(b * h))
    return "\n".join(out)

# provided sample
assert run("2\n4 8\n10 12\n") == "32\n120"

# minimum input
assert run("1\n1 1\n") == "1"

# all equal values
assert run("3\n5 5\n5 5\n5 5\n") == "25\n25\n25"

# boundary values
assert run("2\n500 1\n500 500\n") == "500\n250000"

# mixed pattern
assert run("4\n2 3\n3 4\n4 5\n5 6\n") == "6\n12\n20\n30"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single minimal pair | 1 | smallest valid case |
| repeated identical pairs | constant repetition | consistency across cases |
| maximum base cases | large products | boundary arithmetic correctness |
| increasing pattern | sequential correctness | general correctness over multiple inputs |

## Edge Cases

The smallest possible triangle occurs when both base and height are 1. The algorithm reads the pair, multiplies them, and returns 1. No special handling is required since multiplication behaves correctly at this scale.

At the upper bound, both values can be 500, producing 250000. This still fits comfortably within standard 32-bit integer range, so no overflow concerns arise in Python. The algorithm simply computes the product and outputs it directly.

When all test cases are identical, the algorithm still processes each independently without relying on cached values. Each multiplication is recomputed, which preserves correctness even though optimization is unnecessary at this scale.
