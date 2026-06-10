---
title: "CF 1472B - Fair Division"
description: "We have a collection of candies where each candy weighs either 1 or 2 grams. Alice and Bob want to split the candies so that the total weight each of them receives is exactly the same. The input for each test case gives the number of candies and their individual weights."
date: "2026-06-11T00:33:46+07:00"
tags: ["codeforces", "competitive-programming", "dp", "greedy", "math"]
categories: ["algorithms"]
codeforces_contest: 1472
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 693 (Div. 3)"
rating: 800
weight: 1472
solve_time_s: 325
verified: true
draft: false
---

[CF 1472B - Fair Division](https://codeforces.com/problemset/problem/1472/B)

**Rating:** 800  
**Tags:** dp, greedy, math  
**Solve time:** 5m 25s  
**Verified:** yes  

## Solution
## Problem Understanding

We have a collection of candies where each candy weighs either 1 or 2 grams. Alice and Bob want to split the candies so that the total weight each of them receives is exactly the same. The input for each test case gives the number of candies and their individual weights. The output is simply "YES" if a fair split is possible and "NO" otherwise.

The problem constraints tell us that the number of candies per test case, \(n\), is at most 100, but there can be up to 10,000 test cases. The total number of candies across all test cases does not exceed 100,000. This means we cannot afford anything worse than O(n) per test case if we want to fit in the 2-second time limit, since operations in the range of \(10^8\) are typically fine but \(10^9\) may be tight in Python.

A subtle point arises because candies cannot be split. Even if the total sum of weights is even, it is not always enough to guarantee a fair split. For example, with three candies weighing 2, 1, and 2 grams, the total sum is 5, which is odd and therefore immediately impossible. A careless solution might just check for total sum being even, which would fail in some edge cases like having only one candy of weight 2 or combinations where the sum is even but the distribution cannot be balanced using the available 1-gram and 2-gram candies.

Edge cases include having only 1-gram candies, only 2-gram candies, an odd total weight, and combinations where the total weight is even but there is an odd number of 1-gram candies. These affect the ability to form two equal subsets, so we must reason carefully about both the parity of the total sum and the counts of each candy type.

## Approaches

The brute-force approach is to try every possible subset of candies and check whether any subset sums to half the total weight. This is equivalent to the subset-sum problem. For a single test case with n=100, the number of subsets is \(2^{100}\), which is astronomically large and therefore completely impractical. Even using a dynamic programming approach that checks for sums up to total weight divided by two would take O(n * sum(weights)), which could be up to 200 per test case. That is acceptable, but we can do even better with simple arithmetic reasoning.

The key observation is that there are only two candy types. Let \(c_1\) be the number of 1-gram candies and \(c_2\) be the number of 2-gram candies. The total weight is \(c_1 + 2 c_2\). For a fair split, this total must be even. Moreover, if the total weight is even, the challenge reduces to forming a subset with sum equal to half of the total. Because we can only choose integer numbers of 1-gram and 2-gram candies, half the total weight, call it \(S\), must be achievable using a combination of \(c_1\) ones and \(c_2\) twos. This is only impossible if S is odd and there are no 1-gram candies to adjust parity. In other words, if the total weight is odd, the answer is "NO". If the total weight is even, the answer is "YES" unless S is odd and there are no 1-gram candies to make it odd, in which case the answer is "NO".

This insight allows a very simple O(1) check per test case using counts of 1s and 2s. We no longer need to iterate over subsets or use dynamic programming.

| Approach | Time Complexity | Space Complexity | Verdict |
|---|---|---|---|
| Brute Force | O(2^n) | O(n) | Too slow |
| Optimal | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

1. For each test case, read n and the list of candy weights.
2. Count the number of 1-gram candies, \(c_1\), and the number of 2-gram candies, \(c_2\). This step gives us the key data for reasoning about sum distribution.
3. Compute the total weight \(T = c_1 + 2 c_2\). If \(T\) is odd, output "NO" because no fair split is possible.
4. If \(T\) is even, compute half the total, \(S = T / 2\). This is the target sum for one of the two subsets.
5. Check if S is achievable using the available 2-gram candies. Let k be the minimum of S // 2 and c_2, the maximum number of 2-gram candies we can use without exceeding S.
6. Subtract the weight contributed by the 2-gram candies, \(2 k\), from S. If the remaining weight can be covered exactly by the 1-gram candies, that is, if S - 2 k ≤ c_1, output "YES". Otherwise, output "NO".

Why it works: the algorithm guarantees correctness because we always choose as many 2-gram candies as possible without exceeding half the total, which reduces the remaining sum to be covered by 1-gram candies. Because the weights are only 1 and 2, any achievable sum is a combination of these two, so this greedy selection is sufficient. The parity check ensures that we never attempt an impossible split when the total sum is odd.

## Python Solution

```python
import sys
input = sys.stdin.readline

def can_divide(weights):
    c1 = weights.count(1)
    c2 = weights.count(2)
    total = c1 + 2 * c2
    if total % 2 != 0:
        return "NO"
    half = total // 2
    # use as many 2s as possible without exceeding half
    max_twos = min(c2, half // 2)
    remaining = half - 2 * max_twos
    if remaining <= c1:
        return "YES"
    return "NO"

t = int(input())
for _ in range(t):
    n = int(input())
    weights = list(map(int, input().split()))
    print(can_divide(weights))
```

The code counts the number of 1s and 2s in each test case. It immediately rejects odd total sums. For even totals, it greedily fills half of the sum with as many 2-gram candies as possible and checks if the remaining sum can be made with 1-gram candies. Using min(c2, half // 2) avoids overshooting the target sum. The solution handles multiple test cases efficiently and avoids unnecessary iteration.

## Worked Examples

Trace Sample 1, first and fourth test cases.

| n | weights | c1 | c2 | total | half | max_twos | remaining | output |
|---|---|---|---|---|---|---|---|---|
| 2 | [1,1] | 2 | 0 | 2 | 1 | 0 | 1 | YES |
| 3 | [2,2,2] | 0 | 3 | 6 | 3 | 1 | 1 | NO |

The first trace shows that with two 1-gram candies, the total is 2, half is 1, and we need 1 candy of weight 1 to reach the target, which exists, giving "YES". The fourth trace has total 6, half 3, we can take one 2-gram candy contributing 2, but then need 1 more to reach 3, and since there are no 1-gram candies, we cannot, giving "NO".

## Complexity Analysis

| Measure | Complexity | Explanation |
|---|---|---|
| Time | O(n) | Counting 1s and 2s requires one pass through the weights per test case |
| Space | O(n) | Storing the weights array per test case |

This fits comfortably within the limits since total n across all test cases is ≤ 10^5 and we perform only one pass per test case with O(1) extra memory.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    out = []
    t = int(input())
    for _ in range(t):
        n = int(input())
        weights = list(map(int, input().split()))
        out.append(can_divide(weights))
    return "\n".join(out)

# provided samples
assert run("5\n2\n1 1\n2\n1 2\n4\n1 2 1 2\n3\n2 2 2\n3\n2 1 2\n") == "YES\nNO\nYES\nNO\nNO", "sample 1"

# custom cases
assert run("2\n1\n2\n2\n2 2\n") == "NO\nYES", "single candy and two equal twos"
assert run("2\n3\n1 1 1\n4\n2 2 2 2\n") == "NO\nYES", "odd number of 1s and all twos"
assert run("2\n4\n1 1 2 2\n3\n1 2 2\n") == "YES\nNO", "mixed combinations"
assert run("1\n5\n1 1 1 1 2\n") == "YES", "uneven but fair split possible"
```

| Test input | Expected output | What it validates |
|---|---|---|
|
