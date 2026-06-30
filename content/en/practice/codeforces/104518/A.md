---
title: "CF 104518A - Sum of Odds"
description: "We are given a single integer $n$, and we are asked to compute the sum of the first $n$ odd numbers. In other words, we conceptually build a sequence starting from 1, increasing by 2 each time, and stopping after $n$ terms. The task is to return the total of that sequence."
date: "2026-06-30T10:36:50+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104518
codeforces_index: "A"
codeforces_contest_name: "UNICAMP Selection Contest 2023"
rating: 0
weight: 104518
solve_time_s: 51
verified: true
draft: false
---

[CF 104518A - Sum of Odds](https://codeforces.com/problemset/problem/104518/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 51s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a single integer $n$, and we are asked to compute the sum of the first $n$ odd numbers. In other words, we conceptually build a sequence starting from 1, increasing by 2 each time, and stopping after $n$ terms. The task is to return the total of that sequence.

So if we imagine generating the numbers explicitly, we would form a list like 1, 3, 5, 7, and so on up to the $n$-th term, which is $2n - 1$, and then sum everything.

The input size constraint $n \le 10^7$ is small enough that we could in principle generate the numbers, but large enough that we must be careful about efficiency and, more importantly, about integer growth. A direct summation loop of length ten million is borderline in interpreted languages if done repeatedly or inside multiple test cases, but still feasible once. However, the real constraint pressure is not time complexity but recognizing the mathematical structure so we avoid unnecessary work entirely.

A naive implementation might also fail in languages with fixed-width integers. The sum grows as $n^2$, so for $n = 10^7$, the result is around $10^{14}$, which exceeds 32-bit limits but comfortably fits in 64-bit or Python integers.

A subtle edge case arises if someone assumes arithmetic progression formulas incorrectly or forgets that the sequence starts at 1 rather than 0. For example, incorrectly using $n \cdot (2n) / 2$ instead of the correct formula leads to outputs that are consistently too large.

## Approaches

A brute-force approach constructs each odd number one by one and accumulates the sum. We start at 1 and repeatedly add 2 until we reach the $n$-th term. This is straightforward and guarantees correctness because it directly mirrors the definition of the sequence.

However, this requires $n$ iterations and each iteration does constant work. For $n = 10^7$, this is about ten million additions, which is still borderline but unnecessary. More importantly, it hides the mathematical structure of the sequence.

The key observation is that the sequence of odd numbers forms an arithmetic progression. Instead of summing term-by-term, we can recognize a classical identity: the sum of the first $n$ odd numbers equals $n^2$. This can be derived either from pairing arguments or by using the arithmetic series formula:

$$\frac{n}{2} \cdot (2 \cdot 1 + (n-1)\cdot 2)$$

which simplifies directly to $n^2$.

This transforms the problem from linear time computation into constant time arithmetic.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(n)$ | $O(1)$ | Too slow for large $n$ |
| Optimal | $O(1)$ | $O(1)$ | Accepted |

## Algorithm Walkthrough

1. Read the integer $n$ from input. This represents how many odd numbers we are summing.
2. Recognize that the $i$-th odd number is $2i - 1$, so the full sum is $\sum_{i=1}^{n} (2i - 1)$.
3. Use the known simplification of this summation, which reduces to $n^2$.
4. Compute $n \times n$ using a 64-bit safe or arbitrary precision integer type.
5. Output the result directly.

The key step is the transformation from a summation problem into a closed-form expression. Without this, we would be forced into iterative computation, but once recognized, the solution becomes a single multiplication.

### Why it works

Each term $2i - 1$ contributes linearly increasing structure, but the cumulative effect forms a perfect square. One way to see this is inductively: assume the sum of the first $n$ odd numbers is $n^2$, then adding the next odd number $2(n+1)-1 = 2n+1$ gives:

$$n^2 + (2n+1) = (n+1)^2$$

so the property holds for all $n$. This invariant guarantees that at every step, the sum remains a perfect square, ensuring correctness of the final expression.

## Python Solution

```python
import sys
input = sys.stdin.readline

n = int(input().strip())
print(n * n)
```

The implementation directly encodes the closed-form formula. The input is read once, stripped of whitespace, and converted to an integer. The computation is a single multiplication, which is safe in Python due to its arbitrary-precision integer arithmetic.

A common mistake here is attempting to construct the sequence explicitly in a loop, which is unnecessary and slower. Another mistake is using floating-point arithmetic for large $n$, which can introduce precision issues. Sticking to integer multiplication avoids both problems.

## Worked Examples

### Example 1: $n = 3$

We compute the sum of 1, 3, 5.

| Step | Value of i | Odd number | Running sum |
| --- | --- | --- | --- |
| 1 | 1 | 1 | 1 |
| 2 | 2 | 3 | 4 |
| 3 | 3 | 5 | 9 |

Final output is 9, which matches $3^2 = 9$.

This trace confirms that the recurrence builds perfect squares incrementally.

### Example 2: $n = 5$

We compute 1 + 3 + 5 + 7 + 9.

| Step | Value of i | Odd number | Running sum |
| --- | --- | --- | --- |
| 1 | 1 | 1 | 1 |
| 2 | 2 | 3 | 4 |
| 3 | 3 | 5 | 9 |
| 4 | 4 | 7 | 16 |
| 5 | 5 | 9 | 25 |

Final result is 25, matching $5^2$. This demonstrates that the structure persists uniformly across all prefixes.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(1)$ | Only a single arithmetic operation is performed |
| Space | $O(1)$ | No auxiliary data structures are used |

The solution fits easily within constraints because even the largest possible input only triggers one multiplication. Memory usage is constant and independent of input size.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys as _sys
    input = _sys.stdin.readline
    n = int(input().strip())
    return str(n * n)

# provided samples (conceptual, since samples are implicit)
assert run("1\n") == "1"
assert run("2\n") == "4"
assert run("3\n") == "9"

# minimum edge case
assert run("1\n") == "1"

# small even case
assert run("4\n") == "16"

# large case
assert run("10000000\n") == str(10000000 * 10000000)

# square boundary behavior
assert run("99999\n") == str(99999 * 99999)
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 | 1 | minimal case correctness |
| 4 | 16 | correctness for small even n |
| 10^7 | 10^14 | large constraint handling |
| 99999 | 9999800001 | non-trivial large square correctness |

## Edge Cases

The smallest input $n = 1$ is important because it checks whether the implementation correctly handles trivial sequences. The algorithm computes $1 \times 1 = 1$, matching the only odd number in the sequence.

For large $n$, such as $n = 10^7$, the computation reduces to $10^{14}$. Since Python supports arbitrary precision integers, there is no overflow risk. A step-by-step mental trace shows that no iteration occurs, only a single multiplication, so performance remains stable regardless of input size.

A potential incorrect implementation would try to construct the sequence explicitly. For $n = 10^7$, this would attempt ten million iterations, which is unnecessary overhead. The optimized approach avoids this entirely by relying on the structural identity of odd numbers forming perfect squares.
