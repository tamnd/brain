---
title: "CF 1946B - Maximum Sum"
description: "We start with an integer array. Each operation allows us to choose any contiguous subarray, including the empty subarray, compute its sum, and insert that sum as a new element anywhere in the array. The key observation is that inserting a value changes the total sum of the array."
date: "2026-06-07T17:50:36+07:00"
tags: ["codeforces", "competitive-programming", "dp", "greedy", "math"]
categories: ["algorithms"]
codeforces_contest: 1946
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 936 (Div. 2)"
rating: 1100
weight: 1946
solve_time_s: 74
verified: true
draft: false
---

[CF 1946B - Maximum Sum](https://codeforces.com/problemset/problem/1946/B)

**Rating:** 1100  
**Tags:** dp, greedy, math  
**Solve time:** 1m 14s  
**Verified:** yes  

## Solution
## Problem Understanding

We start with an integer array. Each operation allows us to choose any contiguous subarray, including the empty subarray, compute its sum, and insert that sum as a new element anywhere in the array.

The key observation is that inserting a value changes the total sum of the array. If the chosen subarray has sum `x`, then after inserting `x`, the array sum increases by exactly `x`.

The task is to perform exactly `k` operations and maximize the final array sum. Since the answer can become enormous, we output it modulo `10^9 + 7`.

The constraints are large enough that we need a nearly linear solution. Across all test cases, the total value of `n + k` is at most `2·10^5`, which rules out any approach that simulates subarrays repeatedly or explores operation sequences. We need something around `O(n)` or `O(n log n)` per test case.

Several edge cases are easy to mishandle.

Consider an array whose every subarray has non-positive sum:

```
n = 2, k = 2
a = [-4, -7]
```

The best choice is the empty subarray, whose sum is `0`. Any non-empty subarray would decrease the final answer. The correct result is `-11`, which becomes `999999996` modulo `10^9+7`.

Consider an array with a positive maximum subarray:

```
n = 3, k = 2
a = [2, 2, 8]
```

The maximum subarray sum is `12`. After inserting `12`, that new element can become part of an even larger subarray. A solution that adds `12` twice would obtain `36`, but the optimal process produces `12 + 24`, giving a final sum of `48`.

Another subtle case is when the total array sum is negative but a positive subarray exists:

```
n = 3, k = 1
a = [100, -200, 150]
```

The total sum is `50`, but the best operation inserts the maximum subarray sum `150`, yielding `200`. Looking only at the total sum misses the real source of gain.

## Approaches

A brute-force viewpoint is to treat each operation as a choice among all subarrays. There are `O(n²)` subarrays at every step, and the array length grows after each insertion. Even for one operation this is expensive, and for up to `2·10^5` operations it becomes completely infeasible.

The brute-force idea is correct because every operation contributes exactly the chosen subarray sum to the global total. The difficulty is determining which sequence of choices maximizes the accumulated gain.

The breakthrough comes from understanding what happens after we insert a positive sum.

Suppose the maximum subarray sum of the original array is `M`.

If `M ≤ 0`, no non-empty subarray is worth taking. Since the empty subarray is allowed, every operation can contribute `0`. The answer is simply the original array sum.

Now assume `M > 0`.

During the first operation we insert a value equal to `M`. Since that value is now present in the array, we can choose a subarray containing both the original maximum-sum segment and the newly inserted `M`. Its sum becomes `2M`.

After inserting `2M`, we can repeat the same idea and obtain `4M`, then `8M`, and so on.

The sequence of gains is

```
M, 2M, 4M, ..., 2^(k-1)M
```

whose total contribution is

```
M(2^k - 1)
```

No strategy can do better, because every inserted value ultimately originates from the maximum subarray sum available so far, and this doubling strategy always realizes the largest possible growth.

Thus the problem reduces to two quantities:

```
S = sum of all array elements
M = maximum subarray sum, but at least 0
```

The final answer is

```
S + M(2^k - 1)
```

computed modulo `10^9 + 7`.

The maximum subarray sum is obtained with Kadane's algorithm in linear time.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | Exponential / worse than O(k·n²) | O(n) | Too slow |
| Optimal | O(n) per test case | O(1) | Accepted |

## Algorithm Walkthrough

1. Compute the total array sum `S`.
2. Run Kadane's algorithm to find the maximum subarray sum.
3. Replace that value by `max(0, maximum_subarray_sum)`.

If every subarray is negative, we can always choose the empty subarray and gain `0`.
4. Compute `pow2 = 2^k mod MOD`.
5. Compute the extra contribution:

```
M(2^k - 1)
```

modulo `MOD`.
6. Convert the original sum `S` into modulo form.

Since `S` may be negative, use Python's modulo operation.
7. Add the two parts modulo `MOD` and output the result.

### Why it works

Let `M` be the maximum non-negative subarray sum currently achievable.

After inserting a value equal to `M`, that inserted value can be placed adjacent to the segment producing `M`. The next maximum achievable subarray sum becomes `2M`. Repeating this argument shows that the optimal gains form the sequence

```
M, 2M, 4M, ..., 2^(k-1)M.
```

Their sum is exactly `M(2^k-1)`.

Any inserted value originates from some subarray sum. No subarray can exceed the current maximum achievable subarray sum, so no operation can gain more than the doubling strategy gains at that step. Since the strategy achieves the maximum possible gain every time, it is optimal.

## Python Solution

```python
import sys
input = sys.stdin.readline

MOD = 1000000007

def solve():
    t = int(input())

    for _ in range(t):
        n, k = map(int, input().split())
        a = list(map(int, input().split()))

        total = sum(a)

        best = 0
        cur = 0

        for x in a:
            cur = max(0, cur + x)
            best = max(best, cur)

        extra = best * ((pow(2, k, MOD) - 1) % MOD)
        ans = (total % MOD + extra) % MOD

        print(ans)

solve()
```

The variable `total` stores the original array sum.

Kadane's algorithm is implemented using `cur` and `best`. The expression

```
cur = max(0, cur + x)
```

maintains the maximum subarray sum ending at the current position, while allowing the empty subarray. As a result, `best` automatically becomes `max(0, maximum_subarray_sum)`.

The value `2^k` can be enormous, so modular exponentiation is required. Python's built-in `pow(2, k, MOD)` computes it in `O(log k)` time.

A common mistake is forgetting that `total` may be negative. Using

```
total % MOD
```

converts it into the correct modular representation before adding the extra contribution.

## Worked Examples

### Example 1

Input:

```
n = 3, k = 3
a = [2, 2, 8]
```

Kadane's trace:

| Element | cur | best |
| --- | --- | --- |
| 2 | 2 | 2 |
| 2 | 4 | 4 |
| 8 | 12 | 12 |

Now:

| Variable | Value |
| --- | --- |
| S | 12 |
| M | 12 |
| 2^k - 1 | 7 |
| Extra | 84 |
| Answer | 96 |

The gains are `12`, `24`, and `48`, whose sum is `84`.

### Example 2

Input:

```
n = 2, k = 2
a = [-4, -7]
```

Kadane's trace:

| Element | cur | best |
| --- | --- | --- |
| -4 | 0 | 0 |
| -7 | 0 | 0 |

Now:

| Variable | Value |
| --- | --- |
| S | -11 |
| M | 0 |
| Extra | 0 |
| Answer | 999999996 |

This demonstrates why allowing the empty subarray is essential. Every non-empty choice wou
