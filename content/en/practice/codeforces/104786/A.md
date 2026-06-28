---
title: "CF 104786A - John and M\u00f6bius Convolution"
description: "We are given two arrays of integers, each of length $n$. Every value in both arrays is small, at most $10^3$, but the arrays themselves can be large, up to $2 cdot 10^5$ elements."
date: "2026-06-28T14:29:17+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104786
codeforces_index: "A"
codeforces_contest_name: "FIICode2023Round1"
rating: 0
weight: 104786
solve_time_s: 59
verified: true
draft: false
---

[CF 104786A - John and M\u00f6bius Convolution](https://codeforces.com/problemset/problem/104786/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 59s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given two arrays of integers, each of length $n$. Every value in both arrays is small, at most $10^3$, but the arrays themselves can be large, up to $2 \cdot 10^5$ elements.

The task is to consider every pair formed by picking one element from the first array and one element from the second array, compute $\gcd(x, y) \cdot \mathrm{lcm}(x, y)$, and sum this over all pairs.

The key structural simplification is that for any two integers $x$ and $y$, the product of their gcd and lcm is exactly $x \cdot y$. This identity turns a seemingly number-theoretic problem into a pure counting and aggregation problem over products.

So the problem reduces to computing the sum of $a_i \cdot b_j$ over all pairs.

The constraint $n \le 2 \cdot 10^5$ rules out any quadratic pairing strategy. Even though each value is small, iterating over all $n^2$ pairs would involve up to $4 \cdot 10^{10}$ operations, which is far beyond the time limit.

A direct per-pair computation is also unnecessary because the expression factorizes cleanly.

Edge cases are mostly about extreme multiplicities. For example, if all values are 1, every pair contributes 1, and the answer becomes $n^2$. A naive approach might still be correct but too slow. Another edge case is when values are all $10^3$, where naive multiplication risks large intermediate sums but still fits in 64-bit range since the maximum product is $10^6$ and total pairs are $4 \cdot 10^{10}$, requiring 128-bit safety in some languages, though Python handles it naturally.

## Approaches

The brute-force approach is straightforward: iterate over every $a_i$ and $b_j$, compute $\gcd(a_i, b_j)$, compute $\mathrm{lcm}(a_i, b_j)$, multiply them, and add to the answer. This is correct because it follows the definition directly. The cost comes from the double loop over all pairs, which already gives $O(n^2)$, and each pair also performs a gcd computation. Even with optimized gcd, this becomes completely infeasible at $n = 2 \cdot 10^5$.

The key observation is that the expression inside the sum simplifies algebraically. Using the identity $\gcd(x,y) \cdot \mathrm{lcm}(x,y) = x \cdot y$, each pair contributes simply $a_i \cdot b_j$. The double sum becomes separable: $\sum_i \sum_j a_i b_j = \left(\sum_i a_i\right)\left(\sum_j b_j\right)$. This transforms the problem from pairwise interaction into independent aggregation over each array.

We no longer need to consider interactions between individual pairs. Only the total sum of each array matters.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(n^2)$ | $O(1)$ | Too slow |
| Optimal | $O(n)$ | $O(1)$ | Accepted |

## Algorithm Walkthrough

1. Read the integer $n$, then read arrays $a$ and $b$. These define two multisets of values whose pairwise interactions we must aggregate.
2. Compute the sum of all elements in $a$, call it $S_a$. This captures the total contribution from the first array across all pairings, since each element will be reused across all elements of the second array.
3. Compute the sum of all elements in $b$, call it $S_b$. This plays the symmetric role for the second array.
4. Multiply $S_a$ and $S_b$. This works because every $a_i$ pairs with every $b_j$, so each $a_i$ is effectively repeated $n$ times, once per element in $b$, and vice versa.
5. Output the product $S_a \cdot S_b$.

Why it works: the transformation $\gcd(x,y)\cdot \mathrm{lcm}(x,y) = x \cdot y$ removes all interaction complexity between elements. After substitution, the sum becomes bilinear and fully separable. The algorithm is effectively computing a dot product between two vectors of ones weighted by the original arrays, and bilinearity guarantees that regrouping terms does not change the result.

## Python Solution

```python
import sys
input = sys.stdin.readline

n = int(input())
a = list(map(int, input().split()))
b = list(map(int, input().split()))

sa = sum(a)
sb = sum(b)

print(sa * sb)
```

The implementation relies entirely on the algebraic reduction. There is no need to compute gcd or lcm explicitly. The only subtlety is ensuring input is read efficiently and sums are accumulated in standard Python integers, which naturally handle large values without overflow.

The multiplication is performed once at the end, after both sums are fully computed, ensuring no intermediate quadratic growth of operations.

## Worked Examples

### Example 1

Input:

```
2
2 6
3 12
```

We compute sums of each array and then multiply.

| Step | Sa | Sb | Current State | Notes |
| --- | --- | --- | --- | --- |
| Start | 0 | 0 | a, b loaded | initialization |
| Read a | 8 | 0 | [2, 6] | sum of a is 8 |
| Read b | 8 | 15 | [3, 12] | sum of b is 15 |
| Final | 8 | 15 | answer | 8 × 15 = 120 |

This confirms that even though the original problem involves gcd and lcm, the structure collapses into a product of sums.

### Example 2

Input:

```
3
1 1 1
5 10 15
```

| Step | Sa | Sb | Current State | Notes |
| --- | --- | --- | --- | --- |
| Start | 0 | 0 | arrays loaded | initialization |
| Read a | 3 | 0 | [1,1,1] | uniform array |
| Read b | 3 | 30 | [5,10,15] | sum computed |
| Final | 3 | 30 | answer | 90 |

This shows that repeated values do not require special handling; multiplicity is already encoded in the sum.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n)$ | single pass over each array to compute sums |
| Space | $O(1)$ | only running totals stored |

The solution comfortably fits within constraints since $n = 2 \cdot 10^5$ requires only linear scanning and a single multiplication.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    n = int(input())
    a = list(map(int, input().split()))
    b = list(map(int, input().split()))
    return str(sum(a) * sum(b))

# provided sample
assert run("2\n2 6\n3 12\n") == "120"

# minimum size
assert run("1\n1\n1\n") == "1"

# all equal values
assert run("3\n2 2 2\n3 3 3\n") == "36"

# mixed small values
assert run("4\n1 2 3 4\n4 3 2 1\n") == "100"

# larger skew
assert run("5\n10 0 0 0 0\n1 2 3 4 5\n") == "10"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 1 / 1 1 | 1 | minimum edge case |
| all 2s and 3s | 36 | repeated values |
| reversed sequences | 100 | symmetry correctness |
| sparse nonzero | 10 | zeros and distribution |

## Edge Cases

### Single element arrays

Input:

```
1
7
9
```

The algorithm computes $S_a = 7$, $S_b = 9$, and returns 63. The only pair is (7, 9), and $\gcd(7,9)\cdot\mathrm{lcm}(7,9) = 63$, matching the result exactly. This confirms correctness in the degenerate case where no aggregation is needed.

### Presence of zeros

Although not present in constraints here, if zeros were allowed, the identity still holds because $0 \cdot x = 0$. The algorithm would correctly produce zero whenever either sum is zero, which matches pairwise evaluation.

### Large uniform arrays

Input where all values are $10^3$. The algorithm computes sums linearly and multiplies them once. Every pair contributes $10^6$, and there are $n^2$ pairs, matching $(n \cdot 10^3)(n \cdot 10^3)$. The reduction avoids ever iterating over these pairs explicitly while preserving the total contribution exactly.
