---
title: "CF 64A - Factorial"
description: "We are asked to compute the factorial of a given integer $n$. Factorial is the product of all positive integers up to $n$, so for $n = 3$, the factorial is $1 times 2 times 3 = 6$. The input is a single integer, and the output is the single integer result of this product."
date: "2026-05-28T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "*special", "implementation"]
categories: ["algorithms"]
codeforces_contest: 64
codeforces_index: "A"
codeforces_contest_name: "Unknown Language Round 1"
rating: 1300
weight: 64
solve_time_s: 73
verified: true
draft: false
---

[CF 64A - Factorial](https://codeforces.com/problemset/problem/64/A)

**Rating:** 1300  
**Tags:** *special, implementation  
**Solve time:** 1m 13s  
**Verified:** yes  

## Solution
## Problem Understanding

We are asked to compute the factorial of a given integer $n$. Factorial is the product of all positive integers up to $n$, so for $n = 3$, the factorial is $1 \times 2 \times 3 = 6$. The input is a single integer, and the output is the single integer result of this product.

The constraints are very tight: $n$ is guaranteed to be between 1 and 10. This is extremely small, which simplifies the problem significantly. Even a naive implementation that multiplies numbers in a loop is trivially fast, since computing $10!$ only involves 10 multiplications, well below any concern for performance. Memory usage is negligible because the factorial of 10 fits easily within a standard 32-bit integer.

Despite the simplicity, we should be careful with boundary cases. The smallest input is $n = 1$, which should return 1. Any implementation that initializes a product variable incorrectly or starts a loop at 2 instead of 1 could miscompute this. Similarly, the largest input is $n = 10$, which is $3628800$. This is small enough to fit in standard integers, but if the problem were scaled up, naive implementations could overflow.

## Approaches

The brute-force approach is also the optimal approach here due to the tiny input range. It consists of initializing a variable to hold the product, then iteratively multiplying it by each integer from 1 up to $n$. This works because multiplication is associative and commutative, so we can safely build the product in any order.

There is no need for memoization or recursion here because the numbers are so small that neither stack depth nor repeated computation is an issue. One could implement factorial recursively as well, defining $factorial(n) = n \times factorial(n-1)$ with the base case $factorial(1) = 1$. Both iterative and recursive methods compute the exact same result, but the iterative method avoids the minor overhead of recursive calls, which is trivial for such small numbers but is still good practice.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Iterative | O(n) | O(1) | Accepted |
| Recursive | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Read the input integer $n$. This is the number whose factorial we need to compute.
2. Initialize a variable `fact` to 1. This will hold the cumulative product. Starting at 1 ensures correct handling for $n = 1$.
3. Loop over integers $i$ from 2 to $n$ inclusive. Multiply `fact` by $i$ at each iteration. Starting at 2 is an optimization because multiplying by 1 does not change the result.
4. After the loop finishes, `fact` contains the factorial of $n$. Print the value.

Why it works: Each iteration multiplies `fact` by the next integer in sequence. By the end of the loop, `fact` is exactly $1 \times 2 \times \dots \times n$. The invariant is that after processing integer $i$, `fact` equals the factorial of $i$.

## Python Solution

```python
import sys
input = sys.stdin.readline

n = int(input())
fact = 1
for i in range(2, n + 1):
    fact *= i
print(fact)
```

We read the integer using fast I/O to match competitive programming conventions, though for such small input, standard `input()` is also fine. We start the loop at 2 to avoid unnecessary multiplication by 1. The final print outputs the factorial. No special handling is required because Python integers can grow beyond 32-bit limits automatically.

## Worked Examples

Sample Input 1:

```
3
```

| i | fact before | fact after |
| --- | --- | --- |
| 2 | 1 | 2 |
| 3 | 2 | 6 |

Output: `6`

This demonstrates that the cumulative product correctly computes the factorial, starting with 1 and multiplying up to 3.

Sample Input 2:

```
5
```

| i | fact before | fact after |
| --- | --- | --- |
| 2 | 1 | 2 |
| 3 | 2 | 6 |
| 4 | 6 | 24 |
| 5 | 24 | 120 |

Output: `120`

This shows that as we increase $n$, the algorithm scales linearly and maintains the invariant: `fact` always equals the factorial of the current `i`.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | We perform one multiplication per integer from 2 to n. For $n = 10$, this is 9 multiplications. |
| Space | O(1) | We use only a single integer variable to store the cumulative product. |

Given $n \le 10$, the algorithm runs in negligible time and requires trivial memory, so it easily fits within the constraints.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    n = int(sys.stdin.readline())
    fact = 1
    for i in range(2, n + 1):
        fact *= i
    return str(fact)

# provided sample
assert run("3\n") == "6", "sample 1"

# minimum input
assert run("1\n") == "1", "minimum n"

# maximum input
assert run("10\n") == "3628800", "maximum n"

# medium input
assert run("4\n") == "24", "4 factorial"

# another input
assert run("7\n") == "5040", "7 factorial"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 | 1 | minimum input |
| 10 | 3628800 | maximum input |
| 4 | 24 | normal computation |
| 7 | 5040 | larger middle-range input |

## Edge Cases

For $n = 1$, the loop from 2 to $n$ does not execute, leaving `fact = 1`. This matches the definition of $1!$. For $n = 10$, the loop performs exactly 9 multiplications, resulting in `fact = 3628800`, which is correct and within integer limits. Every other input between 1 and 10 behaves similarly, and there are no hidden failure modes.

This editorial gives a clear path from understanding factorial, recognizing constraints, choosing an iterative approach, and carefully handling boundary cases.
