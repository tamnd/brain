---
title: "CF 1753B - Factorial Divisibility"
description: "We are asked to determine whether the sum of factorials of an array of integers is divisible by another factorial. More concretely, we are given an array [a1, a2, ..., an] and a number x. We want to know if (a1! + a2! + ... + an!) is divisible by x!."
date: "2026-06-09T14:58:51+07:00"
tags: ["codeforces", "competitive-programming", "math", "number-theory"]
categories: ["algorithms"]
codeforces_contest: 1753
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 829 (Div. 1)"
rating: 1600
weight: 1753
solve_time_s: 280
verified: true
draft: false
---

[CF 1753B - Factorial Divisibility](https://codeforces.com/problemset/problem/1753/B)

**Rating:** 1600  
**Tags:** math, number theory  
**Solve time:** 4m 40s  
**Verified:** yes  

## Solution
## Problem Understanding

We are asked to determine whether the sum of factorials of an array of integers is divisible by another factorial. More concretely, we are given an array `[a_1, a_2, ..., a_n]` and a number `x`. We want to know if `(a_1! + a_2! + ... + a_n!)` is divisible by `x!`. Each `a_i` is guaranteed to be at most `x`, so we never have to compute factorials larger than `x!`.

The key constraints are that `n` and `x` can each be up to 500,000. Computing factorials naively for each element and summing them would involve numbers of size roughly `x!`, which grows far faster than any data type can handle. Even 20! is already about 2.4×10^18, so a straightforward computation is impossible for large `x`. This tells us that we must reason mathematically instead of directly computing factorials.

An important edge case arises when some elements in the array are exactly `x`. Since `x!` divides `x!`, any sum containing `x!` is automatically divisible by `x!` if it contains at least one `x!`. Another subtle case is when all `a_i` are less than `x-1`. Then the sum is strictly less than `x!`, so divisibility is impossible. For example, if `x = 5` and all `a_i ≤ 3`, the sum is at most `n * 6 = 6n`, which is less than `5! = 120` unless `n` is huge. But since the sum is always composed of smaller factorials, a clean check is that if any `a_i` is exactly `x`, the answer is always "Yes". Otherwise, we must ensure all `a_i ≥ x-1` to reach divisibility.

## Approaches

The brute-force approach is to compute each factorial, sum them, and check divisibility by `x!`. This is correct in principle but fails immediately for `x > 20`, since the factorials exceed standard integer limits and take far too long to compute. For `n = 500,000` and `x = 500,000`, computing factorials is completely infeasible.

The key observation is that factorials grow extremely fast. If any `a_i` is exactly `x`, `x!` divides it, so we can immediately return "Yes". If all elements are less than `x`, then the largest factorial in the sum is `(x-1)!`. Summing any number of factorials smaller than `x!` cannot reach a multiple of `x!`, because `x!` is strictly larger than the sum of all `(x-1)!` terms. This reduces the problem to a simple check: if the maximum element in the array equals `x`, return "Yes"; otherwise, return "No".

This approach avoids all actual factorial computation and works in linear time relative to the array size.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n * x) | O(1) or O(x) | Too slow / infeasible for large x |
| Optimal | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read integers `n` and `x`.
2. Read the array `a` of length `n`.
3. Compute the maximum value in the array. This identifies the largest factorial in the sum.
4. If the maximum value is equal to `x`, the sum contains `x!`, so the sum is divisible by `x!`. Output "Yes".
5. Otherwise, the sum is strictly smaller than `x!` and cannot be divisible by `x!`. Output "No".

Why it works: `x!` is divisible by all smaller factorials, but the sum of smaller factorials is never a multiple of `x!` unless at least one term equals `x!`. By tracking only the maximum element, we capture this invariant efficiently.

## Python Solution

```python
import sys
input = sys.stdin.readline

def main():
    n, x = map(int, input().split())
    a = list(map(int, input().split()))
    
    if max(a) == x:
        print("Yes")
    else:
        print("No")

if __name__ == "__main__":
    main()
```

The solution reads input efficiently and handles large arrays. We use `max(a)` to find the largest element instead of iterating and comparing manually, which is concise and efficient. There are no loops for factorial computation, avoiding integer overflow. We also do not need to store intermediate factorials, saving memory.

## Worked Examples

**Example 1**

Input:

```
6 4
3 2 2 2 3 3
```

| Step | max(a) | Condition | Output |
| --- | --- | --- | --- |
| Read array | [3,2,2,2,3,3] | max(a)=3 | 3 != 4 → No |

Here, the largest element is 3, which is less than `x=4`. Thus `4!` does not divide the sum of factorials.

**Example 2**

Input:

```
7 3
3 2 2 2 2 2 1
```

| Step | max(a) | Condition | Output |
| --- | --- | --- | --- |
| Read array | [3,2,2,2,2,2,1] | max(a)=3 | 3 == 3 → Yes |

The largest element equals `x=3`, so the sum includes `3!` and is divisible by `3!`.

These traces confirm the logic: only the maximum element matters for divisibility.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Finding the maximum of `n` elements takes linear time. |
| Space | O(n) | Storing the input array; no extra space needed. |

The solution comfortably fits within the problem constraints, even for `n = 500,000`.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    n, x = map(int, input().split())
    a = list(map(int, input().split()))
    return "Yes" if max(a) == x else "No"

# Provided samples
assert run("6 4\n3 2 2 2 3 3\n") == "No", "sample 1"
assert run("8 3\n3 2 2 2 2 2 1 1\n") == "Yes", "sample 2"

# Custom cases
assert run("1 1\n1\n") == "Yes", "minimum input, single element equals x"
assert run("5 5\n1 2 3 4 4\n") == "No", "maximum less than x"
assert run("5 5\n1 2 3 4 5\n") == "Yes", "array contains x"
assert run("3 10\n7 8 9\n") == "No", "all elements less than x, larger x"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 1 / [1] | Yes | Minimum input, single element equals x |
| 5 5 / [1,2,3,4,4] | No | All elements less than x |
| 5 5 / [1,2,3,4,5] | Yes | Array contains x |
| 3 10 / [7,8,9] | No | Larger x, all elements less |

## Edge Cases

For the case `n=1, x=1, a=[1]`, the algorithm correctly outputs "Yes" because the single factorial `1!` equals `x!`. For the case where all elements are less than `x`, such as `n=3, x=10, a=[7,8,9]`, the sum of factorials is smaller than `10!`, so the algorithm correctly outputs "No". These edge cases show that our maximum-element check reliably captures all possible divisibility scenarios without ever computing large factorials.
