---
title: "CF 246B - Increase and Decrease"
description: "We have an array of integers, and we are allowed to pick two different elements and simultaneously increase one by 1 and decrease the other by 1. We can perform this operation as many times as we like."
date: "2026-05-29T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "greedy", "math"]
categories: ["algorithms"]
codeforces_contest: 246
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 151 (Div. 2)"
rating: 1300
weight: 246
solve_time_s: 58
verified: true
draft: false
---

[CF 246B - Increase and Decrease](https://codeforces.com/problemset/problem/246/B)

**Rating:** 1300  
**Tags:** greedy, math  
**Solve time:** 58s  
**Verified:** yes  

## Solution
## Problem Understanding

We have an array of integers, and we are allowed to pick two different elements and simultaneously increase one by 1 and decrease the other by 1. We can perform this operation as many times as we like. The task is to determine the largest number of array elements that can be made equal after any sequence of these operations.

The key thing is to interpret what this operation does. Each operation preserves the sum of the array, because increasing one number by 1 and decreasing another by 1 cancels out. So, the sum is invariant. At the same time, this operation allows “redistribution” of values: large numbers can be decreased while smaller numbers increase. This suggests that the maximum number of equal elements will occur when the array is as balanced as possible around some target value.

The array can have up to 100,000 elements and values up to 10,000 in magnitude. This rules out any brute-force simulation of moves because that could take up to $10^9$ steps if we tried to repeatedly apply operations.

Edge cases include arrays with all equal elements, arrays with only one element, or arrays with two elements differing by more than 1. For instance, an array `[2, 1]` cannot be made fully equal because their sum is 3 and there is no integer `x` such that `2x = 3` for both elements. Correctly handling such cases requires considering the sum of the array and integer division properties, not just comparing individual elements.

## Approaches

A naive approach would try to simulate every possible pair of operations, adjusting elements toward equality until no further operations help. This is correct in principle, because the operation preserves sum and moves values toward each other. But in the worst case, each move only changes two elements by 1. If the array contains 100,000 elements with values of order 10,000, this could require billions of operations, which is far too slow.

The insight to simplify the problem comes from observing two things. First, the sum of the array does not change. Second, if we want `k` elements to be equal to some integer `x`, then `k * x` must be less than or equal to the total sum, otherwise there would not be enough total to distribute. From this, we can see that the maximum number of equal elements is closely related to the greatest common divisibility of the sum over the array size, but in practical terms, we only need to check if the sum is divisible by `n` or not. If the sum is divisible by `n`, we can make all elements equal to `sum // n`. If not, the best we can do is `n - 1` elements equal, because one element will have to absorb the remainder.

The story here is that the brute-force works because each operation moves toward equality, but fails because there are too many operations. The observation that the sum is invariant and equality requires integer values lets us reduce this to a simple check based on divisibility.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Simulation | O(n * max(a)) | O(n) | Too slow |
| Optimal Math-based | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

1. Compute the sum of all elements in the array. This represents the total “resource” that we can redistribute.
2. Check if the sum is divisible by the number of elements `n`. If it is, then we can make all elements equal to `sum // n`. This works because each operation preserves the sum, and integer division ensures an exact target value exists.
3. If the sum is not divisible by `n`, then it is impossible to make all elements equal. In this case, the best we can do is to make `n - 1` elements equal. The remaining element will absorb the remainder. This follows from the pigeonhole principle: the sum of `n-1` elements can be balanced exactly, leaving one extra element.
4. Print the result based on the divisibility check.

Why it works: the invariant is the sum of the array. Any sequence of valid operations preserves this sum, so the target value for equal elements must satisfy `k * x <= sum` for integer `x`. Divisibility ensures the sum can be evenly split; otherwise, one element must take the leftover. No other configuration can produce more equal elements because increasing beyond `n - 1` elements would violate the sum constraint.

## Python Solution

```python
import sys
input = sys.stdin.readline

n = int(input())
a = list(map(int, input().split()))

total = sum(a)

if total % n == 0:
    print(n)
else:
    print(n - 1)
```

The code first reads the number of elements and the array. It computes the total sum and then checks divisibility by `n`. Using integer division directly is unnecessary because we only need to know whether the sum divides evenly. The `n - 1` fallback handles cases where a single remainder prevents full equality. There are no boundary issues since Python handles large integers automatically.

## Worked Examples

**Example 1**

Input:

```
2
2 1
```

| Step | total | total % n | Result |
| --- | --- | --- | --- |
| Compute sum | 3 | 3 % 2 = 1 | sum not divisible |
| Output | - | - | n - 1 = 1 |

Explanation: The sum is 3. Two equal integers cannot sum to 3, so only one element can match another.

**Example 2**

Input:

```
3
4 4 2
```

| Step | total | total % n | Result |
| --- | --- | --- | --- |
| Compute sum | 10 | 10 % 3 = 1 | sum not divisible |
| Output | - | - | n - 1 = 2 |

Explanation: Total sum 10 cannot divide evenly among 3, so maximum equal elements is 2.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Single pass to compute sum of array |
| Space | O(1) | Only total sum and a few integers stored |

This complexity easily fits the problem constraints. With `n` up to 100,000, a single linear scan executes well under 2 seconds. Memory usage is minimal and far below 256 MB.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    n = int(input())
    a = list(map(int, input().split()))
    total = sum(a)
    return str(n if total % n == 0 else n - 1)

# Provided sample
assert run("2\n2 1\n") == "1", "sample 1"

# Custom tests
assert run("1\n100\n") == "1", "single element"
assert run("3\n1 1 1\n") == "3", "all equal"
assert run("4\n2 2 2 3\n") == "3", "one remainder"
assert run("5\n5 5 5 5 5\n") == "5", "all equal large n"
assert run("2\n-100 100\n") == "2", "sum divisible with negatives"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1\n100` | 1 | Single-element array |
| `3\n1 1 1` | 3 | Already all equal |
| `4\n2 2 2 3` | 3 | One element differs |
| `5\n5 5 5 5 5` | 5 | All equal, larger n |
| `2\n-100 100` | 2 | Negative values, sum divisible |

## Edge Cases

If the array has only one element, the sum is trivially divisible by `n=1`, and the algorithm correctly outputs 1. For arrays with two elements differing by 1, like `[2, 1]`, the sum 3 is not divisible by 2, so the algorithm outputs 1, which is correct. For arrays with all equal elements, the sum divides evenly, so the output is `n`. The algorithm naturally handles negative numbers and zeros because the sum logic applies uniformly to integers.
