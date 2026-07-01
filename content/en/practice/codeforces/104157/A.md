---
title: "CF 104157A - Printing Papers"
description: "We are given a weekly supply limit, and Michael is allowed to make exactly one purchase. The restriction is that the quantity he buys must be a power of two. Among all valid purchase amounts that do not exceed the available supply, we need to choose the largest one."
date: "2026-07-02T01:14:23+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104157
codeforces_index: "A"
codeforces_contest_name: "UTPC Contest 01-27-23 Div. 2 (Beginner)"
rating: 0
weight: 104157
solve_time_s: 57
verified: true
draft: false
---

[CF 104157A - Printing Papers](https://codeforces.com/problemset/problem/104157/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 57s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a weekly supply limit, and Michael is allowed to make exactly one purchase. The restriction is that the quantity he buys must be a power of two. Among all valid purchase amounts that do not exceed the available supply, we need to choose the largest one.

In other words, we are looking for the greatest number of the form $2^k$ such that it does not exceed $n$. The input $n$ represents the maximum number of papers available in a week, and the output is the largest purchasable bundle size under the power-of-two restriction.

The constraint $n \le 10^5$ is small enough that even iterating through all powers of two up to this limit is trivial. The number of powers of two up to $10^5$ is bounded by $\log_2(10^5) \approx 16.6$, so even a linear scan over powers is constant-time in practice.

A naive mistake here is to misinterpret the task as needing to partition $n$ or maximize some combination of powers of two. For example, given $n = 5$, one might incorrectly think $4 + 1$ is allowed because both are powers of two, but the problem explicitly restricts Michael to a single purchase. So the output must be a single number, not a decomposition.

Another subtle failure case is stopping at the first power of two greater than or equal to $n$. For $n = 5$, the next power of two is $8$, which is invalid because it exceeds the limit, but a careless implementation that rounds up would return an invalid answer.

## Approaches

The brute-force idea is straightforward: enumerate all powers of two starting from 1 and keep track of the largest one that does not exceed $n$. This works because powers of two form a strictly increasing sequence, so scanning them in order guarantees we do not miss any candidate. The issue with this approach is not correctness but generality: if implemented inefficiently or if the range were much larger, repeatedly generating powers could become unnecessary overhead.

However, the structure of the problem makes optimization immediate. Every number in this sequence doubles the previous one, so we can simply keep multiplying by 2 until the next value would exceed $n$. The last valid value is the answer. This reduces the problem to a single loop with logarithmic length.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force (scan powers sequentially) | O(log n) | O(1) | Accepted |
| Optimal (iterative doubling) | O(log n) | O(1) | Accepted |

In practice, both are equivalent here, but the iterative doubling version is the cleanest and least error-prone.

## Algorithm Walkthrough

1. Start from the smallest valid power of two, which is 1. This is always safe because the minimum input constraint guarantees $n \ge 1$, so at least one valid answer exists.
2. Repeatedly compute the next power of two by doubling the current value. Each step explores the next candidate in strictly increasing order, ensuring we never skip a valid possibility.
3. Stop when doubling would produce a value greater than $n$. At that point, the current value is the largest valid power of two that fits within the constraint.
4. Output the last valid value obtained before exceeding $n$.

The key idea is that powers of two form a monotonic sequence, so the optimal value can be found by walking this sequence until it breaks feasibility.

### Why it works

At every step, we maintain the invariant that the current value is the largest power of two not exceeding the most recently checked threshold. Since the sequence of powers of two is strictly increasing and unbroken, the first value that exceeds $n$ immediately implies the previous value is the maximum feasible candidate. There is no alternative candidate between two consecutive powers of two, so no valid solution can be skipped.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input().strip())
    x = 1
    while x * 2 <= n:
        x *= 2
    print(x)

if __name__ == "__main__":
    solve()
```

The solution reads the input value, then iteratively doubles a running variable starting from 1. The loop condition `x * 2 <= n` ensures we only advance while the next power of two remains valid. Once the condition fails, `x` is guaranteed to be the largest valid power of two.

A common implementation pitfall is using `x <= n` inside the loop condition while updating first, which can accidentally overshoot and require backtracking. The chosen condition avoids that entirely by checking before updating.

## Worked Examples

### Example 1

Input:

```
5
```

| Step | x | x * 2 <= n |
| --- | --- | --- |
| 1 | 1 | True |
| 2 | 2 | True |
| 3 | 4 | True |
| 4 | 8 | False |

The loop stops when doubling 4 would produce 8, which exceeds 5. The last valid value is 4, so the output is 4. This confirms the algorithm correctly selects the largest power of two not exceeding the limit.

### Example 2

Input:

```
1
```

| Step | x | x * 2 <= n |
| --- | --- | --- |
| 1 | 1 | False |

The loop never runs because even doubling 1 would exceed the limit. The answer remains 1, which is correct since it is the only power of two within the constraint.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(log n) | Each iteration doubles the value, so the number of steps is proportional to the number of bits in n |
| Space | O(1) | Only a single integer variable is maintained |

The constraint $n \le 10^5$ guarantees at most around 17 iterations, which is effectively constant time in practice and easily within limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    n = int(input().strip())
    x = 1
    while x * 2 <= n:
        x *= 2
    return str(x)

# provided samples
assert run("5\n") == "4", "sample 1"
assert run("1\n") == "1", "sample 2"

# custom cases
assert run("2\n") == "2", "exact power of two"
assert run("3\n") == "2", "just above power of two"
assert run("16\n") == "16", "exact upper power"
assert run("17\n") == "16", "just above upper power"
assert run("100000\n") == "65536", "large boundary"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 2 | 2 | exact power of two handling |
| 3 | 2 | correct floor behavior between powers |
| 16 | 16 | boundary exact match |
| 17 | 16 | transition across power boundary |
| 100000 | 65536 | upper constraint correctness |

## Edge Cases

For $n = 1$, the algorithm starts at $x = 1$ and immediately fails the condition $x \cdot 2 \le n$, so it returns 1 without entering the loop. This confirms correctness at the smallest boundary.

For values just above a power of two, such as $n = 33$, the sequence goes 1, 2, 4, 8, 16, 32, and stops before 64. The algorithm naturally returns 32, demonstrating that it always selects the greatest feasible power without overshooting.
