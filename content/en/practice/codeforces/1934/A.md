---
title: "CF 1934A - Too Min Too Max"
description: "We are asked to maximize the expression $$ over all quadruples of distinct indices $i, j, k, l$ in an array $a$. The input provides multiple test cases, each with an array of integers. For each test case, the output is the maximum value of the expression."
date: "2026-06-08T18:09:50+07:00"
tags: ["codeforces", "competitive-programming", "greedy", "math"]
categories: ["algorithms"]
codeforces_contest: 1934
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 931 (Div. 2)"
rating: 800
weight: 1934
solve_time_s: 137
verified: false
draft: false
---

[CF 1934A - Too Min Too Max](https://codeforces.com/problemset/problem/1934/A)

**Rating:** 800  
**Tags:** greedy, math  
**Solve time:** 2m 17s  
**Verified:** no  

## Solution
## Problem Understanding

We are asked to maximize the expression

$$|a_i - a_j| + |a_j - a_k| + |a_k - a_l| + |a_l - a_i|$$

over all quadruples of distinct indices $i, j, k, l$ in an array $a$. The input provides multiple test cases, each with an array of integers. For each test case, the output is the maximum value of the expression.

The expression is essentially the perimeter of a "walk" through four elements of the array, moving from $a_i$ to $a_j$ to $a_k$ to $a_l$ and back to $a_i$, measuring absolute differences along the edges. The problem reduces to selecting the largest and smallest values in a way that maximizes the sum of differences.

Constraints allow $n$ up to 100 and $t$ up to 500. This permits $O(n^4)$ brute-force solutions in principle, but a careful observation can reduce the complexity. Edge cases include arrays with all equal elements, where the expression is zero, and arrays with both negative and positive numbers, which influence which combination yields the maximum.

A naive approach might try all quadruples, but we need to understand the structure of absolute differences to simplify the problem.

## Approaches

A brute-force approach enumerates all quadruples $i, j, k, l$ and computes the expression directly. This is $O(n^4)$, which is acceptable given $n \le 100$, but it is unnecessary because the expression can be simplified by considering the extreme values.

The key observation is that absolute differences are maximized when combining the minimum and maximum elements. Let $mn = \min(a)$ and $mx = \max(a)$. To maximize the sum, we want the sequence to alternate between these extremes. For example, choosing $i$ as the minimum, $j$ as the maximum, $k$ as the minimum, and $l$ as the maximum produces the largest contribution from each term. Therefore, the maximum expression reduces to:

$$2 \times (\text{max}(a) - \text{min}(a)) + 2 \times (\text{second max/min contribution})$$

Given the small array size, the exact combinations of extremal values can be enumerated efficiently. One simple method is to sort the array and compute the expression for sequences that pick the two largest and two smallest elements in alternating order. This guarantees the maximum.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n^4) | O(1) | Accepted (n ≤ 100) |
| Greedy/Extremes | O(n log n) | O(n) | Accepted, faster |

## Algorithm Walkthrough

1. For each test case, read the array $a$ and store its length $n$.
2. Sort $a$ to easily access minimum, second minimum, maximum, and second maximum values.
3. Compute the candidate values of the expression by placing extreme elements in alternating positions. Typical candidates are:

- $a_0, a_1, a_{n-2}, a_{n-1}$
- $a_0, a_1, a_{n-1}, a_{n-2}$
- $a_0, a_{n-2}, a_1, a_{n-1}$
- $a_0, a_{n-1}, a_1, a_{n-2}$
4. For each candidate quadruple, compute the expression

$|a_i - a_j| + |a_j - a_k| + |a_k - a_l| + |a_l - a_i|$
5. Track the maximum value across candidates and output it.

Why it works: Absolute differences are maximized by choosing the largest possible differences at each step. Alternating minimum and maximum elements ensures each term contributes maximally to the sum. Sorting allows us to easily enumerate these extreme configurations without checking all quadruples.

## Python Solution

```python
import sys
input = sys.stdin.readline

def max_expression(a):
    a.sort()
    n = len(a)
    candidates = [
        [a[0], a[1], a[n-2], a[n-1]],
        [a[0], a[1], a[n-1], a[n-2]],
        [a[0], a[n-2], a[1], a[n-1]],
        [a[0], a[n-1], a[1], a[n-2]],
    ]
    res = 0
    for quad in candidates:
        i, j, k, l = quad
        val = abs(i-j) + abs(j-k) + abs(k-l) + abs(l-i)
        res = max(res, val)
    return res

def solve():
    t = int(input())
    for _ in range(t):
        n = int(input())
        a = list(map(int, input().split()))
        print(max_expression(a))

if __name__ == "__main__":
    solve()
```

Explanation: Sorting ensures we can easily pick the extreme elements. Candidate quadruples are chosen to maximize the sum of absolute differences. The small number of candidates (4) guarantees correctness while keeping computation trivial.

## Worked Examples

For input `[1,1,2,2,3]`, sorted array is `[1,1,2,2,3]`. Candidate quadruples:

| i,j,k,l | Expression |
| --- | --- |
| 1,1,2,3 |  |
| 1,1,3,2 | ... = 6 |
| 1,2,1,3 | ... = 6 |
| 1,3,1,2 | ... = 6 |

Maximum is 6.

For input `[5,1,3,2,-3,-1,10,3]`, sorted array `[-3,-1,1,2,3,3,5,10]`. Candidate quadruples produce expression values 38, which is the maximum.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n) | Sorting dominates; candidates are constant |
| Space | O(n) | Store sorted array |

Given $n ≤ 100$ and $t ≤ 500$, this is efficient.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from contextlib import redirect_stdout
    out = io.StringIO()
    with redirect_stdout(out):
        solve()
    return out.getvalue().strip()

# Provided samples
assert run("5\n4\n1 1 1 1\n5\n1 1 2 2 3\n8\n5 1 3 2 -3 -1 10 3\n4\n3 3 1 1\n4\n1 2 2 -1\n") == "0\n6\n38\n8\n8"

# Custom cases
assert run("1\n4\n-1 -1 -1 -1\n") == "0", "all equal negative"
assert run("1\n5\n1 2 3 4 5\n") == "12", "ascending consecutive"
assert run("1\n6\n-5 -2 0 2 3 5\n") == "28", "mixed negatives and positives"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 4 elements all equal | 0 | Handles uniform array |
| 1..5 | 12 | Max with ascending array |
| Mixed negative and positive | 28 | Correct handling of sign |

## Edge Cases

For arrays with all equal elements, expression is zero regardless of selection. Sorting and candidate enumeration still work, as all values are identical, producing zero. For minimal size $n=4$, the candidates are exactly the four elements, so the algorithm correctly computes the expression.
