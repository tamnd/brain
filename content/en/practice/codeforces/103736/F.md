---
title: "CF 103736F - Subarrays"
description: "We are given a sequence of integers and asked to count how many contiguous subarrays have a sum divisible by a given integer $k$."
date: "2026-07-02T09:11:24+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 103736
codeforces_index: "F"
codeforces_contest_name: "The 2022 Hangzhou Normal U Summer Trials"
rating: 0
weight: 103736
solve_time_s: 47
verified: true
draft: false
---

[CF 103736F - Subarrays](https://codeforces.com/problemset/problem/103736/F)

**Rating:** -  
**Tags:** -  
**Solve time:** 47s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a sequence of integers and asked to count how many contiguous subarrays have a sum divisible by a given integer $k$. A subarray here means we pick a starting position and an ending position and take everything in between without gaps, then compute the sum of those elements. We want to know how many of these sums are multiples of $k$, including zero.

The array length can go up to $10^5$, and each value can be as large as $10^9$. That immediately rules out any solution that tries to recompute sums from scratch for every subarray, since the number of subarrays itself is about $O(n^2)$, which is far too large. Even a single quadratic loop is already around $10^{10}$ operations in the worst case, which cannot pass in a 1 second limit.

A subtle point is that values can be zero, so a subarray consisting of a single zero must be counted when $k$ divides zero. Another corner case appears when $k = 1$, where every subarray is valid since every integer is divisible by 1, meaning the answer should be $n(n+1)/2$. Any correct solution must handle this naturally without special casing.

A naive prefix-sum check might also look safe but still fail due to overflow concerns in languages with fixed-width integers, since prefix sums can reach $10^{14}$. In Python this is not an issue, but in other contexts it matters conceptually.

## Approaches

The brute-force idea is straightforward. For every pair $(l, r)$, compute the sum of the subarray $a_l \dots a_r$ and check whether it is divisible by $k$. Even if we precompute prefix sums, we still iterate over all pairs of indices, leading to $O(n^2)$ checks.

The reason this fails is not just the number of subarrays, but also that each pair either costs $O(1)$ with prefix sums or $O(n)$ without them. Either way, quadratic scale is unavoidable.

The key observation is that subarray sums become simple when expressed through prefix sums. Let $S_i = a_1 + \dots + a_i$. Then the sum of a subarray $[l, r]$ is $S_r - S_{l-1}$. We want this to be divisible by $k$, meaning:

$$S_r \equiv S_{l-1} \pmod{k}$$

So the problem is not about subarrays anymore, but about counting pairs of prefix sums with equal remainder modulo $k$. Each valid subarray corresponds exactly to a pair of indices whose prefix sums have the same modulo class.

This transforms the problem into counting combinations within groups: for each remainder value $r$, if it appears $c_r$ times among prefix sums, it contributes $c_r(c_r - 1)/2$ valid subarrays.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n²) | O(1) or O(n) | Too slow |
| Optimal (prefix mod counting) | O(n) | O(min(n, k)) | Accepted |

## Algorithm Walkthrough

1. Compute prefix sums while iterating through the array, maintaining the sum modulo $k$ instead of the full sum. This avoids large integer growth and keeps only the relevant equivalence class.
2. Maintain a frequency map that records how many times each remainder has appeared so far. Initialize it with remainder 0 appearing once, representing the empty prefix before any elements are taken.
3. For each element, update the running prefix sum and compute its remainder modulo $k$.
4. Every time we see a remainder $r$, we know that all previous prefix sums with the same remainder can form a valid subarray ending at the current position. So we add the current frequency of $r$ to the answer.
5. Increment the frequency of remainder $r$.

The key decision is step 4. Instead of trying to form subarrays explicitly, we interpret each prefix sum as a “state”, and every repetition of a state creates new valid subarrays ending at the current index.

### Why it works

The correctness comes from the invariant that at any position $i$, the frequency map stores exactly how many prefix sums have each remainder among indices $0 \dots i$. A subarray $[l, r]$ has sum divisible by $k$ if and only if the prefix remainders at $r$ and $l-1$ are equal. Thus every time we encounter a remainder $r$, we are effectively choosing any previous occurrence of the same remainder as the start boundary of a valid subarray ending at the current index. No valid pair is missed, and no invalid pair is counted, since different remainders cannot satisfy the divisibility condition.

## Python Solution

```python
import sys
input = sys.stdin.readline

n, k = map(int, input().split())
arr = list(map(int, input().split()))

freq = {0: 1}
prefix = 0
ans = 0

for x in arr:
    prefix = (prefix + x) % k
    ans += freq.get(prefix, 0)
    freq[prefix] = freq.get(prefix, 0) + 1

print(ans)
```

The implementation tracks the prefix sum modulo $k$ directly, which avoids both overflow and unnecessary full-sum computation. The dictionary `freq` stores counts of each remainder. The initial entry `{0: 1}` is essential because it accounts for subarrays that start from index 1, where the prefix itself is already divisible by $k$.

A common pitfall is updating the frequency before adding to the answer. Doing so would incorrectly count the current prefix with itself, which does not correspond to any valid subarray.

## Worked Examples

### Example 1

Input:

```
6 3
0 1 2 4 7 7
```

We track prefix modulo 3 and frequency updates.

| i | value | prefix mod 3 | freq before | added to ans | freq after | ans |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | 0 | 0 | {0:1} | 1 | {0:2} | 1 |
| 2 | 1 | 1 | {0:2} | 0 | {0:2,1:1} | 1 |
| 3 | 2 | 0 | {0:2,1:1} | 2 | {0:3,1:1} | 3 |
| 4 | 4 | 2 | {0:3,1:1} | 0 | {0:3,1:1,2:1} | 3 |
| 5 | 7 | 0 | {0:3,1:1,2:1} | 3 | {0:4,1:1,2:1} | 6 |
| 6 | 7 | 1 | {0:4,1:1,2:1} | 1 | {0:4,1:2,2:1} | 7 |

This trace shows how repeated prefix remainders directly generate multiple valid subarrays without explicitly enumerating them.

### Example 2

Input:

```
5 2
1 1 1 1 1
```

| i | value | prefix mod 2 | freq before | added to ans | freq after | ans |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | 1 | 1 | {0:1} | 0 | {0:1,1:1} | 0 |
| 2 | 1 | 0 | {0:1,1:1} | 1 | {0:2,1:1} | 1 |
| 3 | 1 | 1 | {0:2,1:1} | 1 | {0:2,1:2} | 2 |
| 4 | 1 | 0 | {0:2,1:2} | 2 | {0:3,1:2} | 4 |
| 5 | 1 | 1 | {0:3,1:2} | 2 | {0:3,1:3} | 6 |

This demonstrates the alternating structure: every pair of equal remainders forms a valid subarray.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Each element is processed once with O(1) dictionary operations on average |
| Space | O(min(n, k)) | We store frequencies of remainders encountered |

The solution fits comfortably within constraints since $n \le 10^5$, and both time and memory usage grow linearly with input size.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    n, k = map(int, input().split())
    arr = list(map(int, input().split()))

    freq = {0: 1}
    prefix = 0
    ans = 0

    for x in arr:
        prefix = (prefix + x) % k
        ans += freq.get(prefix, 0)
        freq[prefix] = freq.get(prefix, 0) + 1

    return str(ans)

# provided sample
assert run("6 3\n0 1 2 4 7 7\n") == "7"

# single element zero
assert run("1 3\n0\n") == "1"

# all ones, k = 2
assert run("5 2\n1 1 1 1 1\n") == "6"

# k = 1, all subarrays valid
assert run("4 1\n1 2 3 4\n") == "10"

# alternating zeros
assert run("5 3\n0 0 0 0 0\n") == "15"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 6 3 … | 7 | sample correctness |
| 1 3 / 0 | 1 | single zero edge case |
| k=2 ones | 6 | repeated prefix structure |
| k=1 | 10 | full combinatorics |
| all zeros | 15 | all prefixes equal |

## Edge Cases

A minimal case like a single element tests whether the initial prefix remainder is handled correctly. With input `1 3` and array `[0]`, the prefix remainder is zero immediately, and since the frequency map starts with `{0:1}`, we count exactly one valid subarray. The algorithm processes this as a single step where `prefix = 0`, adds `freq[0] = 1`, and returns 1.

A case with `k = 1` is more extreme because every prefix has remainder zero. For `n = 4` and `[1,2,3,4]`, every step increases the frequency of remainder zero, producing the total of all subarrays, which is 10. The frequency mechanism naturally accumulates triangular counts without any modification.

An all-zero array behaves similarly but for any `k`. Since every prefix sum is identical modulo `k`, every pair of indices forms a valid subarray. The frequency map repeatedly counts increasing combinations, producing $n(n+1)/2$, matching the expected combinatorial structure.
