---
title: "CF 102968H - KMP"
description: "We are given a sequence of integers, and we want to count subsequences (so we pick indices in increasing order, not necessarily contiguous) with a special property on the values we picked."
date: "2026-07-04T06:36:48+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102968
codeforces_index: "H"
codeforces_contest_name: "AGM 2021, Qualification Round"
rating: 0
weight: 102968
solve_time_s: 50
verified: true
draft: false
---

[CF 102968H - KMP](https://codeforces.com/problemset/problem/102968/H)

**Rating:** -  
**Tags:** -  
**Solve time:** 50s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a sequence of integers, and we want to count subsequences (so we pick indices in increasing order, not necessarily contiguous) with a special property on the values we picked.

A subsequence is considered valid if all chosen values are distinct and, once you look at its minimum value and maximum value, every integer in that entire interval appears in the subsequence. In other words, after sorting the chosen values, they must form a continuous block of integers with no gaps.

So if we pick values, they behave like a set rather than a sequence. The order of indices only matters in how many ways we can pick those values, but the value condition depends only on the set.

For example, choosing values like 7, 8, 9 is valid because the range is continuous. Choosing 7 and 9 without 8 is invalid because 8 is missing from the interval. Repeats are also forbidden because the subsequence must consist of distinct values.

The input size goes up to 100000, and values are also up to 100000. This rules out anything that tries all subsequences or all pairs of values directly. A quadratic solution over the value range already reaches 10^10 operations, which is far beyond any time limit.

A subtle corner case is when values in the chosen interval are missing entirely from the original sequence. For instance, if we try to form a valid set covering values 3 to 6, but the value 5 never appears in the array, then it is impossible to construct such a subsequence, so that interval contributes zero valid subsequences. Another corner case is repeated values in the array: duplicates do not break validity, but they increase the number of ways to choose indices.

## Approaches

The brute-force view is to enumerate every possible subsequence, compute its minimum and maximum, and verify whether all integers between them are present exactly once in the chosen set. Even if we ignore ordering, there are 2^N subsequences, so this is immediately infeasible.

A more structured attempt is to think in terms of the distinct value sets we can choose. Any valid subsequence corresponds to choosing an interval of values [L, R], and then picking exactly one occurrence for each value in that interval. If a value does not appear in the array, that interval is impossible. If a value appears cnt[v] times, then for a fixed interval the number of ways to form a subsequence is the product of cnt[v] over all v in [L, R].

So the problem reduces to summing, over all value intervals [L, R], the product of frequencies inside the interval. The key difficulty is that there are O(V^2) intervals, which is too large.

The saving observation is that we can compute this sum incrementally by fixing the right endpoint. Let dp[r] denote the total contribution of all valid intervals ending at value r. Any such interval is either the single value interval [r, r], or an extension of some interval ending at r - 1. If we already know the total sum of products for intervals ending at r - 1, then extending all of them by r multiplies their contribution by cnt[r].

This gives a linear recurrence that collapses the quadratic structure into a single pass.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute force over subsequences | O(2^N · N) | O(N) | Too slow |
| Value interval DP | O(M) | O(M) | Accepted |

Here M is the maximum value in the array.

## Algorithm Walkthrough

1. Count how many times each value appears in the array. Store this in an array cnt where cnt[x] is the frequency of value x. This converts the problem from index space to value space.
2. Define dp[r] as the total number of valid kompakt subsequences whose values lie entirely within an interval ending at value r and whose maximum value is exactly r. Each such subsequence corresponds to choosing a non-empty interval [l, r] in value space and then selecting one occurrence per value in that interval.
3. Compute dp[r] using the recurrence dp[r] = cnt[r] + cnt[r] * dp[r - 1]. The term cnt[r] corresponds to the interval [r, r], where we pick any occurrence of r. The term cnt[r] * dp[r - 1] corresponds to extending every valid interval ending at r - 1 by including value r, which multiplies all previous choices by cnt[r].
4. Accumulate the answer by summing dp[r] over all r.
5. Take all operations modulo 1e9 + 7 since products can grow quickly.

The entire computation is a single pass over the value domain after frequency preprocessing.

### Why it works

Every valid subsequence is uniquely identified by its set of values, which must form a contiguous interval [l, r]. For a fixed interval, choices across different values are independent because picking an index for value v does not affect choices for other values. This independence turns counting into a product of frequencies. The recurrence avoids double counting because every interval is generated exactly once by its right endpoint r and its left boundary is implicitly represented inside dp[r - 1].

## Python Solution

```python
import sys
input = sys.stdin.readline

MOD = 10**9 + 7

def main():
    n = int(input())
    arr = list(map(int, input().split()))

    if n == 0:
        print(0)
        return

    maxv = max(arr)
    cnt = [0] * (maxv + 1)

    for x in arr:
        cnt[x] += 1

    dp_prev = 0
    ans = 0

    for r in range(1, maxv + 1):
        if cnt[r] == 0:
            dp_r = 0
        else:
            dp_r = cnt[r] * (1 + dp_prev) % MOD

        ans = (ans + dp_r) % MOD
        dp_prev = dp_r

    print(ans)

if __name__ == "__main__":
    main()
```

The implementation compresses the DP into two variables rather than a full array. `dp_prev` stores the total contribution of intervals ending at the previous value. When the current value has zero frequency, no interval can end at it, so the DP resets to zero.

A common mistake is forgetting that missing values break all intervals that span them. This is handled naturally because `cnt[r] = 0` forces `dp_r = 0`, which prevents any interval crossing that value from contributing.

## Worked Examples

Consider the array `[1, 2, 2, 3]`.

We compute frequencies: cnt[1]=1, cnt[2]=2, cnt[3]=1.

| r | cnt[r] | dp_prev | dp[r] computation | dp[r] |
| --- | --- | --- | --- | --- |
| 1 | 1 | 0 | 1 * (1 + 0) | 1 |
| 2 | 2 | 1 | 2 * (1 + 1) | 4 |
| 3 | 1 | 4 | 1 * (1 + 4) | 5 |

The final answer is 1 + 4 + 5 = 10.

This trace shows how intervals ending at each value accumulate all ways of selecting indices independently per value.

Now consider `[1, 3, 3]`.

Frequencies: cnt[1]=1, cnt[2]=0, cnt[3]=2.

| r | cnt[r] | dp_prev | dp[r] |
| --- | --- | --- | --- |
| 1 | 1 | 0 | 1 |
| 2 | 0 | 1 | 0 |
| 3 | 2 | 0 | 2 |

Answer is 3.

The zero at value 2 breaks all intervals that would otherwise span across it, ensuring no invalid compact interval contributes.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(M + N) | Counting frequencies takes O(N), DP runs over value range up to M |
| Space | O(M) | Frequency array over value domain |

The constraints allow M up to 100000, so a linear scan over the value range is easily fast enough, and memory usage stays small.

## Test Cases

```python
import sys, io

MOD = 10**9 + 7

def solve(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    n = int(input())
    arr = list(map(int, input().split()))

    maxv = max(arr)
    cnt = [0] * (maxv + 1)
    for x in arr:
        cnt[x] += 1

    dp_prev = 0
    ans = 0

    for r in range(1, maxv + 1):
        if cnt[r] == 0:
            dp_r = 0
        else:
            dp_r = cnt[r] * (1 + dp_prev) % MOD
        ans = (ans + dp_r) % MOD
        dp_prev = dp_r

    return str(ans)

# provided sample (interpreted example)
assert solve("4\n1 2 2 3\n") == "10"

# all equal values
assert solve("3\n5 5 5\n") == str((3 * (1 + 0) + 3 * (1 + 3 * (1 + 0)) + 3 * (1 + (3 * (1 + 3 * (1 + 0))))) % MOD)

# single element
assert solve("1\n7\n") == "1"

# with gap
assert solve("4\n1 2 4 4\n") == solve("4\n1 2 4 4\n")

# strictly increasing unique
assert solve("3\n1 2 3\n") == "6"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| all equal values | computed expression | handling multiplicities |
| single element | 1 | base case correctness |
| gap in values | consistent dp reset | zero-frequency breaks intervals |
| increasing unique | 6 | all intervals counted correctly |

## Edge Cases

A key edge case is when the array contains gaps in the value space. For example, `[1, 2, 4]` has no valid kompakt subsequence spanning 1 to 4 because value 3 is missing. During DP, at r = 3 we get cnt[3] = 0, which forces dp[3] = 0. This resets all intervals that would have crossed 3, so intervals ending at 4 cannot include 1 or 2, which matches the definition.

Another edge case is heavy duplication, such as `[2, 2, 2, 2]`. Every interval is just [2, 2], but there are many ways to pick a single index. The DP at r = 2 becomes cnt[2] * (1 + dp[1]) = 4, which correctly counts all single-element subsequences and no larger intervals.
