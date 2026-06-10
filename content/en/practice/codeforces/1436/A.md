---
title: "CF 1436A - Reorder"
description: "The problem presents an array of integers and asks whether it can be reordered so that a specific weighted sum matches a given target value."
date: "2026-06-11T04:52:08+07:00"
tags: ["codeforces", "competitive-programming", "math"]
categories: ["algorithms"]
codeforces_contest: 1436
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 678 (Div. 2)"
rating: 800
weight: 1436
solve_time_s: 206
verified: true
draft: false
---

[CF 1436A - Reorder](https://codeforces.com/problemset/problem/1436/A)

**Rating:** 800  
**Tags:** math  
**Solve time:** 3m 26s  
**Verified:** yes  

## Solution
## Problem Understanding

The problem presents an array of integers and asks whether it can be reordered so that a specific weighted sum matches a given target value. The sum is defined as the sum over all starting positions $i$ of the sum from that position to the end of each element divided by its one-based index. Conceptually, each element contributes to multiple terms of the overall sum, with earlier elements affecting more terms than later elements.

The input consists of multiple test cases. Each test case gives the length of the array, the target sum, and the array itself. The output should be "YES" if there exists any permutation of the array that produces the exact sum and "NO" otherwise.

With the constraints $1 \le n \le 100$ and $0 \le a_i, m \le 10^6$, we can safely perform computations in $O(n \log n)$ or $O(n^2)$ per test case, since $100^2$ operations is acceptable. A naive solution attempting all $n!$ permutations is infeasible. Edge cases to watch include arrays of zeros, arrays with a single element, or targets smaller than the smallest element. For instance, with array $[0, 0, 0]$ and target $1$, the correct output is "NO". If the array is $[5]$ and the target is $5$, the answer is "YES".

## Approaches

A brute-force approach would generate all $n!$ permutations and compute the sum for each. While correct, this is impractical because even for $n = 10$, the number of permutations exceeds 3 million.

The key observation is that the sum is linear in the array elements. Rewriting the formula gives:

$$\sum_{i=1}^{n}\sum_{j=i}^{n} \frac{a_j}{j} = \sum_{j=1}^{n} a_j \sum_{i=1}^{j} \frac{1}{j} = \sum_{j=1}^{n} a_j$$

since $\sum_{i=1}^{j} \frac{1}{j} = 1$. Therefore, the weighted sum reduces to the simple sum of the array elements. This remarkable simplification means that the sum is invariant under reordering. The problem then reduces to checking whether the sum of all elements equals the target. This insight transforms a seemingly complex combinatorial problem into a simple arithmetic check.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force (all permutations) | O(n! * n) | O(n) | Too slow |
| Sum Check (optimal) | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the number of test cases $t$.
2. For each test case, read $n$ and $m$, then read the array of length $n$.
3. Compute the sum of all array elements.
4. Compare this sum to $m$. If they are equal, print "YES"; otherwise, print "NO".

Why it works: the formula given in the problem collapses to the sum of the array elements regardless of their order. Therefore, if the sum matches the target, any permutation trivially satisfies the condition. If not, no permutation can satisfy the condition.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        n, m = map(int, input().split())
        a = list(map(int, input().split()))
        if sum(a) == m:
            print("YES")
        else:
            print("NO")

if __name__ == "__main__":
    solve()
```

The solution reads inputs efficiently with `sys.stdin.readline`, computes the sum in linear time, and directly compares it to the target. The variables are scoped inside the loop to avoid reuse across test cases. The sum check is exact because all numbers are integers, avoiding floating-point issues.

## Worked Examples

**Sample 1**

| Variable | Value |
| --- | --- |
| n | 3 |
| m | 8 |
| a | [2, 5, 1] |
| sum(a) | 8 |
| Comparison | 8 == 8 → YES |

**Sample 2**

| Variable | Value |
| --- | --- |
| n | 4 |
| m | 4 |
| a | [0, 1, 2, 3] |
| sum(a) | 6 |
| Comparison | 6 != 4 → NO |

These traces demonstrate that the only requirement is the sum of the array. The inner and outer summations are invariant under reordering.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n * t) | Each test case sums at most 100 elements. |
| Space | O(n) | Array storage per test case. |

With $t \le 100$ and $n \le 100$, the worst-case operations are 10,000, well within limits.

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

# provided samples
assert run("2\n3 8\n2 5 1\n4 4\n0 1 2 3\n") == "YES\nNO", "sample 1"

# custom cases
assert run("1\n1 5\n5\n") == "YES", "single element equal"
assert run("1\n1 5\n4\n") == "NO", "single element not equal"
assert run("1\n3 0\n0 0 0\n") == "YES", "all zeros target zero"
assert run("1\n3 1\n0 0 1\n") == "YES", "sum equals target with zero elements"
assert run("1\n3 2\n1 0 0\n") == "NO", "sum does not equal target"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1\n1 5\n5\n | YES | Single-element array where element equals target |
| 1\n1 5\n4\n | NO | Single-element array where element differs from target |
| 1\n3 0\n0 0 0\n | YES | All zeros, target zero |
| 1\n3 1\n0 0 1\n | YES | Sum matches target with zeros present |
| 1\n3 2\n1 0 0\n | NO | Sum does not match target |

## Edge Cases

A minimal edge case is an array of length one. The sum check trivially handles this since the single element must match the target. Arrays of all zeros work as long as the target is zero, and arrays with mixed zeros behave correctly because the sum of all elements is exactly what matters, ignoring order. No floating-point arithmetic is needed because all operations are integer sums.
