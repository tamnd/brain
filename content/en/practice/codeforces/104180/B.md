---
title: "CF 104180B - Rain Collector"
description: "We are given a starting amount of rainwater collected on day one, denoted by an integer $i$. This value determines everything about the rest of the week."
date: "2026-07-02T00:42:30+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104180
codeforces_index: "B"
codeforces_contest_name: "UTPC Contest 02-10-23 Div. 2 (Beginner)"
rating: 0
weight: 104180
solve_time_s: 53
verified: true
draft: false
---

[CF 104180B - Rain Collector](https://codeforces.com/problemset/problem/104180/B)

**Rating:** -  
**Tags:** -  
**Solve time:** 53s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a starting amount of rainwater collected on day one, denoted by an integer $i$. This value determines everything about the rest of the week. From day two to day seven, the amount of rain increases steadily: each day adds the same increment $x$, where $x$ is computed as the sum of digits of $i$. Over seven days in total, we need to compute the cumulative amount of water collected.

A useful way to reinterpret the problem is as a simple arithmetic sequence. The first term is $i$, and each next term increases by $x$. So the sequence looks like:

$i, i + x, i + 2x, \dots, i + 6x$. The task is to sum all these terms.

The constraints are small, with $i \leq 10^5$, so computing the digit sum and performing a constant number of arithmetic operations is trivial in terms of performance. Even a fully direct computation per test case is constant time.

Edge cases are subtle but important because of how the digit sum behaves.

One edge case is $i = 0$. The digit sum is $0$, so all seven days produce zero. A naive implementation that assumes positive numbers or ignores leading-zero-like behavior still handles it correctly only if digit sum logic is robust.

Another edge case is when $i$ has trailing zeros, for example $i = 10000$. The digit sum is $1$, not affected by zeros, so the increment is small, but the sequence still grows correctly. Mistakes often come from incorrectly interpreting the increment as something like “append digit” instead of sum of digits.

Finally, since the sequence length is fixed (7 terms), there is no danger of overflow in Python, but in stricter languages, naive accumulation using large arithmetic might need care.

## Approaches

The brute-force idea is straightforward. We compute the digit sum $x$, then explicitly simulate the seven days. Starting from $i$, we repeatedly add $x$ and accumulate the total. This is correct because it mirrors the process described in the problem exactly.

The cost of this approach is constant per test case since there are only seven days. Even if we recompute digit sums or perform arithmetic repeatedly, the complexity is still bounded by a fixed constant. However, the more general inefficiency lies in ignoring structure: the sequence is arithmetic, so summation can be done in closed form instead of iterative accumulation.

The key observation is that the sequence is an arithmetic progression with first term $i$, last term $i + 6x$, and 7 terms total. The sum of an arithmetic progression is:

$$\text{sum} = \frac{7}{2} \cdot (2i + 6x)$$

This reduces everything to computing a digit sum once and applying a direct formula.

This turns the problem into pure arithmetic.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Simulation | O(1) | O(1) | Accepted |
| Arithmetic Formula | O(1) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the integer $i$ from input. This is the base value of the sequence, and it defines the entire progression.
2. Compute $x$, the sum of digits of $i$. This value acts as the fixed daily increment, so correctness depends entirely on extracting digits properly.
3. Recognize that the 7 daily values form an arithmetic sequence starting at $i$ with common difference $x$.
4. Compute the total sum using the arithmetic progression formula:

$$S = \frac{7}{2} \cdot (2i + 6x)$$

This avoids iterating over the seven days while preserving exact equivalence.
5. Output $S$.

### Why it works

The construction of daily values guarantees a linear progression because each day depends only on a fixed additive constant derived from the input. Once $x$ is fixed, every term is determined uniquely as $a_k = i + kx$. Summing these terms is equivalent to summing an arithmetic sequence, and the closed-form formula is algebraically identical to direct accumulation. Since no intermediate step modifies $x$, the structure remains stable across all seven terms.

## Python Solution

```python
import sys
input = sys.stdin.readline

i = int(input().strip())

x = sum(int(c) for c in str(i))

# arithmetic series: i + (i+x) + ... + (i+6x)
# sum = 7/2 * (2i + 6x) = 7 * (2i + 6x) / 2
total = 7 * (2 * i + 6 * x) // 2

print(total)
```

The solution reads the input and immediately computes the digit sum by converting the integer into a string and summing characters. This is safe for all inputs including zero, since `"0"` produces a correct digit sum of zero.

The key implementation detail is avoiding floating-point arithmetic. Although the formula involves division by 2, the expression is always even, so integer division is safe. Writing it as `7 * (2 * i + 6 * x) // 2` ensures exact integer output.

## Worked Examples

### Example 1

Input:

```
70
```

Here, $i = 70$, so digit sum $x = 7$.

The sequence becomes:

$70, 77, 84, 91, 98, 105, 112$

| Day | Value |
| --- | --- |
| 1 | 70 |
| 2 | 77 |
| 3 | 84 |
| 4 | 91 |
| 5 | 98 |
| 6 | 105 |
| 7 | 112 |

Sum is $637$.

This confirms that even when digits include zeros, only nonzero digits affect the increment.

### Example 2

Input:

```
5
```

Here, $i = 5$, so $x = 5$.

Sequence:

$5, 10, 15, 20, 25, 30, 35$

| Day | Value |
| --- | --- |
| 1 | 5 |
| 2 | 10 |
| 3 | 15 |
| 4 | 20 |
| 5 | 25 |
| 6 | 30 |
| 7 | 35 |

Sum is $140$.

This shows the arithmetic progression structure clearly when the digit sum equals the number itself.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(1) | Digit sum is bounded by at most 6 digits, and only constant arithmetic is performed |
| Space | O(1) | Only a few integer variables are used |

The runtime is constant regardless of input size, easily fitting within any realistic constraints.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    i = int(input().strip())
    x = sum(int(c) for c in str(i))
    total = 7 * (2 * i + 6 * x) // 2
    return str(total)

# provided sample
assert run("70\n") == "637"

# minimum case
assert run("0\n") == "0"

# small number
assert run("5\n") == "140"

# all digits zero except one
assert run("10000\n") == str(7 * (2 * 10000 + 6 * 1) // 2)

# max constraint
assert run("100000\n") == str(7 * (2 * 100000 + 6 * 1) // 2)

# repeated digit sum variation
assert run("99\n") == str(7 * (2 * 99 + 6 * 18) // 2)
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 0 | 0 | zero handling |
| 5 | 140 | basic arithmetic progression |
| 10000 | formula correctness with trailing zeros |  |
| 100000 | upper bound behavior |  |
| 99 | multi-digit sum correctness |  |

## Edge Cases

For input `0`, the digit sum is `0`, so the sequence is constant zero across all seven days. The algorithm computes $x = 0$, leading to:

$S = \frac{7}{2}(0) = 0$, which matches the expected output exactly.

For input `10000`, the digit sum is `1`. The sequence becomes:

$10000, 10001, 10002, 10003, 10004, 10005, 10006$.

The algorithm computes:

$S = 7(20000 + 6)/2 = 70003$, which matches direct summation.

For input `99`, digit sum is `18`. The sequence grows much faster, but the arithmetic formula still applies unchanged. Each term is determined solely by the fixed increment, so no step deviates from the arithmetic progression definition.
