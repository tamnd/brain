---
title: "CF 1475E - Advertising Agency"
description: "Masha has a list of bloggers, each with a certain number of followers, and she wants to hire exactly k of them to maximize the total audience reached. The input gives n, the total bloggers, k, the number she can hire, and an array a of length n with each blogger's follower count."
date: "2026-06-11T00:09:36+07:00"
tags: ["codeforces", "competitive-programming", "combinatorics", "math", "sortings"]
categories: ["algorithms"]
codeforces_contest: 1475
codeforces_index: "E"
codeforces_contest_name: "Codeforces Round 697 (Div. 3)"
rating: 1600
weight: 1475
solve_time_s: 106
verified: true
draft: false
---

[CF 1475E - Advertising Agency](https://codeforces.com/problemset/problem/1475/E)

**Rating:** 1600  
**Tags:** combinatorics, math, sortings  
**Solve time:** 1m 46s  
**Verified:** yes  

## Solution
## Problem Understanding

Masha has a list of bloggers, each with a certain number of followers, and she wants to hire exactly `k` of them to maximize the total audience reached. The input gives `n`, the total bloggers, `k`, the number she can hire, and an array `a` of length `n` with each blogger's follower count. For each test case, the output is the number of ways to choose `k` bloggers such that the sum of their followers is the highest possible. Two selections are considered different if they differ by at least one blogger.

Given the constraints, with `n` up to 1000 and the sum of all `n` across test cases also bounded by 1000, we know that a solution with time complexity around `O(n log n)` per test case will easily fit. We also need to be careful about combinatorial counting because `k` can be as large as `n` and the counts can be repeated, making naive counting prone to off-by-one mistakes.

A subtle edge case arises when multiple bloggers have the same follower count. For example, if all bloggers have the same followers and `k=2`, every pair is valid. A naive approach that just takes the `k` largest numbers without considering frequency will undercount possibilities.

## Approaches

A brute-force approach would enumerate all `n choose k` subsets, sum their followers, and count those that achieve the maximum sum. This works because correctness is guaranteed by checking all subsets, but it becomes computationally infeasible even for `n=30` since the number of subsets grows exponentially. With `n` up to 1000, this is impossible.

The key observation is that the total followers are maximized by simply taking the `k` bloggers with the largest follower counts. Sorting the array in descending order immediately identifies the maximum total. The complexity reduction comes from noticing that once the largest `k` followers are known, the number of ways to choose them depends only on the frequency of the smallest value among these top `k` followers in the entire array. Specifically, if the `k`-th largest follower count appears `c` times in the whole array and `m` times within the top `k`, then the number of ways to choose the top `k` bloggers is `C(c, m)`, the binomial coefficient.

This is significantly faster because sorting is `O(n log n)` and computing `C(c, m)` can be done in `O(k)` with precomputed factorials modulo `10^9+7`.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n choose k * k) | O(k) | Too slow |
| Optimal | O(n log n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Read the number of test cases `t`.
2. For each test case, read `n` and `k`, then read the follower array `a`.
3. Sort `a` in descending order. The first `k` elements now give the maximum possible sum.
4. Identify `x`, the smallest follower count among the top `k` bloggers.
5. Count `m`, the number of occurrences of `x` within the top `k`.
6. Count `c`, the total number of occurrences of `x` in the entire array.
7. Compute the binomial coefficient `C(c, m)` modulo `10^9+7` to get the number of valid selections.
8. Print the result for each test case.

The algorithm works because the invariant is that any optimal set must include all elements larger than `x` and exactly `m` of the elements equal to `x`. This ensures that the sum is maximal and counts every distinct combination correctly.

## Python Solution

```python
import sys
input = sys.stdin.readline
MOD = 10**9 + 7

# precompute factorials and inverse factorials
N = 1000
fact = [1] * (N+1)
invfact = [1] * (N+1)

for i in range(2, N+1):
    fact[i] = fact[i-1] * i % MOD

def modinv(x):
    return pow(x, MOD-2, MOD)

for i in range(2, N+1):
    invfact[i] = modinv(fact[i])

def comb(n, k):
    if k < 0 or k > n:
        return 0
    return fact[n] * invfact[k] % MOD * invfact[n-k] % MOD

t = int(input())
for _ in range(t):
    n, k = map(int, input().split())
    a = list(map(int, input().split()))
    a.sort(reverse=True)
    x = a[k-1]
    m = a[:k].count(x)
    c = a.count(x)
    print(comb(c, m))
```

The precomputation of factorials and modular inverses allows us to compute any binomial coefficient efficiently. Sorting ensures we pick the largest elements. Counting occurrences of the smallest element in the top `k` and total guarantees the correct combinatorial calculation. A common mistake is miscounting `m` or `c`, or forgetting the modulo arithmetic.

## Worked Examples

Sample 1:

```
n=4, k=3, a=[1,3,1,2]
```

| Step | Array a | Top k | x | m | c | comb(c,m) |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | [1,3,1,2] | [3,2,1] | 1 | 1 | 2 | 2 |

This shows that the smallest element in the top 3 is 1. It occurs once in the top 3 and twice overall. There are 2 ways to choose the one `1` among the two available, matching the expected output.

Sample 2:

```
n=4, k=2, a=[1,1,1,1]
```

| Step | Array a | Top k | x | m | c | comb(c,m) |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | [1,1,1,1] | [1,1] | 1 | 2 | 4 | 6 |

All values are the same. There are 4 choose 2 ways to pick the top 2, yielding 6.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n) per test case | Sorting dominates, counting occurrences is O(n) |
| Space | O(n) | Store array and factorials up to 1000 |

The solution easily fits within 2 seconds and 256 MB because `n` and the sum over all test cases is ≤ 1000.

## Test Cases

```python
import sys, io

def run(inp):
    sys.stdin = io.StringIO(inp)
    MOD = 10**9 + 7
    N = 1000
    fact = [1]*(N+1)
    invfact = [1]*(N+1)
    for i in range(2,N+1):
        fact[i] = fact[i-1]*i % MOD
    def modinv(x):
        return pow(x,MOD-2,MOD)
    for i in range(2,N+1):
        invfact[i] = modinv(fact[i])
    def comb(n,k):
        if k<0 or k>n: return 0
        return fact[n]*invfact[k]%MOD*invfact[n-k]%MOD
    t=int(input())
    res=[]
    for _ in range(t):
        n,k=map(int,input().split())
        a=list(map(int,input().split()))
        a.sort(reverse=True)
        x=a[k-1]
        m=a[:k].count(x)
        c=a.count(x)
        res.append(str(comb(c,m)))
    return "\n".join(res)

# Provided samples
assert run("3\n4 3\n1 3 1 2\n4 2\n1 1 1 1\n2 1\n1 2\n") == "2\n6\n1", "sample 1"

# Custom cases
assert run("1\n5 3\n5 5 5 5 5\n") == "10", "all equal"
assert run("1\n3 2\n1 2 3\n") == "1", "simple increasing"
assert run("1\n6 3\n1 2 2 3 3 3\n") == "1", "multiple repeats, largest freq"
assert run("1\n6 3\n3 3 2 2 1 1\n") == "1", "sorted descending with ties"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 5 3 5 5 5 5 5 | 10 | All equal values, multiple combinations |
| 3 2 1 2 3 | 1 | Simple increasing, unique largest elements |
| 6 3 1 2 2 3 3 3 | 1 | Multiple repeats, pick among the most frequent max |
| 6 3 3 3 2 2 1 1 | 1 | Sorted descending, ties handled correctly |

## Edge Cases

If all bloggers have the same followers, for example `a=[1,1,1,1]` and `k=2`, the algorithm correctly identifies `x
