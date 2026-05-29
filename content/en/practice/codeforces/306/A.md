---
title: "CF 306A - Candies"
description: "Polycarpus has a certain number of candies and a number of friends. He wants to distribute all the candies among his friends in such a way that every friend gets a positive number of candies, and the difference between the friend who receives the most candies and the friend who…"
date: "2026-05-29T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "implementation"]
categories: ["algorithms"]
codeforces_contest: 306
codeforces_index: "A"
codeforces_contest_name: "Testing Round 6"
rating: 800
weight: 306
solve_time_s: 200
verified: false
draft: false
---

[CF 306A - Candies](https://codeforces.com/problemset/problem/306/A)

**Rating:** 800  
**Tags:** implementation  
**Solve time:** 3m 20s  
**Verified:** no  

## Solution
## Problem Understanding

Polycarpus has a certain number of candies and a number of friends. He wants to distribute all the candies among his friends in such a way that every friend gets a positive number of candies, and the difference between the friend who receives the most candies and the friend who receives the least is as small as possible. The input gives us two integers: the total number of candies `n` and the number of friends `m`. The output should be a sequence of `m` positive integers that sum up to `n`, and the difference between the largest and smallest integers should be minimized.

Given the constraints, `n` and `m` are both at most 100. This is small enough that any straightforward distribution strategy will run efficiently, so we do not have to worry about performance with high-complexity algorithms. The main challenge is reasoning about the distribution itself.

An important edge case is when `n` is not divisible by `m`. For instance, if Polycarpus has 10 candies and 3 friends, a naive approach might try to give each friend `n // m = 3` candies, but then we would have 1 candy leftover. The correct approach is to give some friends one extra candy to balance the distribution: `[4, 3, 3]`. Another edge case is when `n` equals `m`; each friend simply gets one candy. A careless solution that does not handle the remainder correctly will fail for any input where `n % m != 0`.

## Approaches

The brute-force approach would be to try every possible distribution of `n` candies among `m` friends and check the difference between the maximum and minimum values. This is guaranteed to find the optimal solution, but the number of combinations grows exponentially with `n` and `m`. Specifically, the number of partitions of `n` into `m` positive integers is combinatorial and can easily exceed thousands, which is unnecessary given the simple structure of the problem.

The key insight to optimize this is that the fairest distribution is always a nearly uniform distribution. Every friend should receive either `floor(n / m)` or `ceil(n / m)` candies. Let `q = n // m` be the base number of candies per friend and `r = n % m` be the remainder. Exactly `r` friends should get `q + 1` candies, and the remaining `m - r` friends get `q` candies. This guarantees that the maximum difference is 1, which is minimal and cannot be improved because if all values were equal and `n % m != 0`, we would not reach the total sum `n`.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(combinatorial) | O(m) | Too slow |
| Optimal | O(m) | O(m) | Accepted |

## Algorithm Walkthrough

1. Read the integers `n` and `m` from input. These represent the total candies and the number of friends.
2. Compute `q = n // m` as the base number of candies each friend should receive. This ensures everyone gets at least the same minimum amount.
3. Compute `r = n % m` as the remainder candies that still need to be distributed. These extra candies will be given one per friend to minimize the maximum difference.
4. Create a list of size `m` where the first `r` elements are `q + 1` and the remaining `m - r` elements are `q`. This guarantees that exactly `r` friends receive one extra candy, balancing the distribution.
5. Print the list as space-separated integers.

Why it works: The invariant is that each friend receives at least `q` candies, and exactly `r` friends receive one more candy. The sum of all values is `q*(m-r) + (q+1)*r = n`, which ensures correctness. The difference between the largest and smallest value is at most 1, which is minimal because distributing the remainder requires some friends to get an extra candy.

## Python Solution

```python
import sys
input = sys.stdin.readline

n, m = map(int, input().split())
q, r = divmod(n, m)
result = [q + 1] * r + [q] * (m - r)
print(' '.join(map(str, result)))
```

The code first computes the quotient and remainder using `divmod`, which is cleaner than separate division and modulo operations. The list is then constructed by repeating `q + 1` exactly `r` times and `q` exactly `m - r` times. Using `join` converts the integers to strings and prints them in the required format. Off-by-one errors are avoided by carefully handling the remainder `r` and ensuring all friends receive a positive integer.

## Worked Examples

### Example 1

Input: `12 3`

| Step | q | r | Result list |
| --- | --- | --- | --- |
| Compute q,r | 4 | 0 | [] |
| Build list | 4_0 + 4_3 | 0 | [4, 4, 4] |

All friends get the same number of candies. Maximum difference is 0.

### Example 2

Input: `10 3`

| Step | q | r | Result list |
| --- | --- | --- | --- |
| Compute q,r | 3 | 1 | [] |
| Build list | [3+1]*1 + [3]*2 | 1 | [4, 3, 3] |

One friend receives one extra candy to distribute the remainder. Maximum difference is 1.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(m) | We create a list of length `m` and print it. Each operation is linear in `m`. |
| Space | O(m) | We store the resulting list of size `m`. |

Given `m ≤ 100`, this is extremely fast and memory-efficient. The solution easily runs within 1 second and 256 MB.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    n, m = map(int, input().split())
    q, r = divmod(n, m)
    result = [q + 1] * r + [q] * (m - r)
    return ' '.join(map(str, result))

# provided samples
assert run("12 3\n") == "4 4 4", "sample 1"
assert run("10 3\n") == "4 3 3", "remainder distribution"

# custom cases
assert run("1 1\n") == "1", "minimum input"
assert run("100 1\n") == "100", "single friend, all candies"
assert run("100 100\n") == "1 "*100[:-1], "each friend gets one candy"
assert run("7 3\n") == "3 2 2", "small uneven distribution"
assert run("15 4\n") == "4 4 4 3", "uneven with remainder less than half"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 1 | 1 | minimum input |
| 100 1 | 100 | single friend gets all candies |
| 100 100 | 1 1 ... 1 | maximum friends, minimal distribution |
| 7 3 | 3 2 2 | remainder distribution correctness |
| 15 4 | 4 4 4 3 | remainder distribution when remainder < m/2 |

## Edge Cases

When `n` equals `m`, such as `5 5`, each friend receives exactly 1 candy. The algorithm computes `q = 1` and `r = 0`. The result list is `[1, 1, 1, 1, 1]`. When `n` is slightly larger than `m`, such as `7 3`, we compute `q = 2` and `r = 1`. The first `r` friend receives `q + 1 = 3` candies, and the remaining two receive `2` candies each. This ensures that the maximum difference is exactly 1, which cannot be reduced. The algorithm gracefully handles both cases without additional conditions.
