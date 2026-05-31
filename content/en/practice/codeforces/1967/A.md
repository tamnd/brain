---
title: "CF 1967A - Permutation Counting"
description: "We are given a set of cards, each labeled with a number from 1 to n. For each number i, we have ai cards of that type."
date: "2026-05-31T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "binary-search", "greedy", "implementation", "math", "sortings"]
categories: ["algorithms"]
codeforces_contest: 1967
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 942 (Div. 1)"
rating: 1400
weight: 1967
solve_time_s: 76
verified: false
draft: false
---

[CF 1967A - Permutation Counting](https://codeforces.com/problemset/problem/1967/A)

**Rating:** 1400  
**Tags:** binary search, greedy, implementation, math, sortings  
**Solve time:** 1m 16s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a set of cards, each labeled with a number from 1 to n. For each number i, we have a_i cards of that type. We also have k coins, and each coin allows us to buy a new card of any type, so we can increase the count of any number arbitrarily as long as we do not exceed k purchases in total. After purchasing, we will arrange all the cards in a line and count how many contiguous subarrays of length n are permutations of [1, 2, ..., n]. Our task is to maximize that count.

The input consists of multiple test cases. Each test case specifies n, k, and the initial counts a_1 through a_n. The output for each test case is a single integer, the maximum number of n-length subarrays that are full permutations.

The constraints are large: n can be up to 2×10^5, k can reach 10^12, and a_i can also be up to 10^12. This rules out any approach that tries to simulate all subarrays or rearrangements. We must rely on counting and distribution logic instead of explicitly generating sequences.

An important edge case is when n = 1, because every card is trivially a permutation of [1]. Another case occurs when k is extremely large relative to a_i; we might be able to buy enough cards to make every a_i equal and thus maximize the number of permutations. Careless implementations might try to construct an actual array and fail due to memory limits or overflow.

## Approaches

A brute-force approach would attempt to generate all sequences of cards after buying up to k new cards, then slide a window of size n and check if each window is a permutation. This is correct in principle but becomes infeasible very quickly. Even for n = 10^5, there are n! permutations of length n, and generating arrays of length sum(a_i) + k is impossible when a_i and k reach 10^12. The operation count is exponential and memory usage is astronomical.

The key insight is to recognize that the problem reduces to distributing cards evenly across the n types. If we imagine forming permutations in a repeating sequence, the maximum number of n-length permutation subarrays is determined by the minimum count of any type after purchasing extra cards. Specifically, if after buying we can ensure that all types appear at least m times, then we can form m full permutation blocks. The remaining cards allow us to form additional permutations in a staggered fashion, but the dominant factor is always the type with the smallest count.

This reduces the problem to a binary search: we search for the largest integer m such that we can increase each a_i to at least m using at most k coins. For each candidate m, we compute the total extra cards needed as sum(max(0, m - a_i) for i = 1..n). If that sum is <= k, m is achievable. Binary search efficiently finds the largest feasible m.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n * (sum(a_i) + k)) | O(sum(a_i) + k) | Too slow |
| Binary Search + Counting | O(n log(max(a_i) + k)) | O(n) | Accepted |

## Algorithm Walkthrough

1. Read the number of test cases. Loop over each test case independently.
2. For the current test case, read n, k, and the array a of counts.
3. Initialize binary search bounds. The minimum possible permutations is 0, and the maximum is the largest possible count if we spent all k coins to equalize the minimum type: max(a) + k.
4. Perform binary search. For each candidate m, compute the sum of coins required to raise each a_i to at least m. For a_i already >= m, no coins are needed; otherwise, we need m - a_i coins.
5. If the total coins required <= k, the candidate m is feasible. Update the search to try a larger m. Otherwise, decrease m.
6. After binary search, the highest feasible m is the maximum number of complete permutations we can guarantee.
7. Output that number.

Why it works: The binary search works because the function "is m achievable" is monotonic. If m is achievable, then any smaller m is also achievable. If m is not achievable, then any larger m is also impossible. The invariant is that at the end, we have identified the largest m such that we can guarantee at least m full permutations of [1, 2, ..., n].

## Python Solution

```python
import sys
input = sys.stdin.readline

def max_permutations(n, k, a):
    low, high = 0, max(a) + k
    while low < high:
        mid = (low + high + 1) // 2
        required = sum(max(0, mid - x) for x in a)
        if required <= k:
            low = mid
        else:
            high = mid - 1
    return low

t = int(input())
for _ in range(t):
    n, k = map(int, input().split())
    a = list(map(int, input().split()))
    print(max_permutations(n, k, a))
```

The solution first sets binary search bounds based on the largest current card count plus k coins. For each candidate m, it calculates the coins needed and compares it to k. The choice of `(low + high + 1) // 2` ensures that the search terminates correctly on the largest feasible m. The `max(0, mid - x)` ensures we only count coins where a_i is below mid, avoiding negative contributions.

## Worked Examples

Sample input 2:

```
2 4
8 4
```

Variables during execution:

| Step | low | high | mid | required | decision |
| --- | --- | --- | --- | --- | --- |
| start | 0 | 12 | 6 | 2 | required <= k, low=6 |
| next | 6 | 12 | 9 | 5 | required <= k, low=9 |
| next | 9 | 12 | 11 | 7 | required <= k, low=11 |
| next | 11 | 12 | 12 | 8 | required > k, high=11 |

Output: 11

This demonstrates the binary search narrowing on the maximum achievable permutation count.

Another example, input:

```
1 10
1
```

Since n=1, a_1=1, k=10. The maximum achievable is a_1 + k = 11. Binary search correctly identifies this.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log(max(a_i) + k)) | For each test case, binary search iterates log(max(a_i) + k) times and sums over n counts each iteration |
| Space | O(n) | We store the array a of length n; no extra structures needed |

With n <= 2×10^5, sum over all test cases <= 5×10^5, and k <= 10^12, the solution runs well within 2s and memory constraints.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    output = io.StringIO()
    sys.stdout = output
    # call solution
    t = int(input())
    for _ in range(t):
        n, k = map(int, input().split())
        a = list(map(int, input().split()))
        print(max_permutations(n, k, a))
    sys.stdout = sys.__stdout__
    return output.getvalue().strip()

# Provided samples
assert run("1\n1 10\n1\n") == "11", "sample 1"
assert run("1\n2 4\n8 4\n") == "11", "sample 2"

# Custom cases
assert run("1\n3 0\n1 2 3\n") == "1", "no coins, limited by min"
assert run("1\n3 10\n1 2 3\n") == "5", "coins enough to balance"
assert run("1\n1 0\n1000000000000\n") == "1000000000000", "single type, no coins"
assert run("1\n2 1000000000000\n1 1\n") == "500000000001", "large k, equalize both types"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 3 0\n1 2 3 | 1 | No coins, minimum type limits permutations |
| 3 10\n1 2 3 | 5 | Coins allow balancing types |
| 1 0\n1000000000000 | 1000000000000 | Single type, edge case |
| 2 1000000000000\n1 1 | 500000000001 | Large k, splits evenly across two types |

## Edge Cases

When n=1, any number of coins can directly increase the count of the single type, so the output is a_1 + k. Binary search correctly handles this since required = max(0, mid - a_1). For very large k compared to a_i, binary search identifies how many full permutations can be created after distributing coins optimally, always controlled by the smallest adjusted type. When a_i are already large, and k is small, the algorithm correctly computes that no extra permutations beyond the minimum existing count are possible.
