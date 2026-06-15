---
title: "CF 1057B - DDoS"
description: "We are given a timeline split into seconds. For each second, we know how many requests hit a server. This gives us an array where each position represents request volume in that second."
date: "2026-06-15T13:06:02+07:00"
tags: ["codeforces", "competitive-programming", "*special", "brute-force"]
categories: ["algorithms"]
codeforces_contest: 1057
codeforces_index: "B"
codeforces_contest_name: "Mail.Ru Cup 2018 - Practice Round"
rating: 1400
weight: 1057
solve_time_s: 265
verified: true
draft: false
---

[CF 1057B - DDoS](https://codeforces.com/problemset/problem/1057/B)

**Rating:** 1400  
**Tags:** *special, brute force  
**Solve time:** 4m 25s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a timeline split into seconds. For each second, we know how many requests hit a server. This gives us an array where each position represents request volume in that second.

We need to find the longest contiguous time interval such that the total number of requests inside that interval is strictly larger than 100 times the length of the interval. In other words, if we pick a segment of length `t`, and the sum of requests in it exceeds `100 * t`, that segment is considered an attack period, and we want the maximum possible length of such a segment.

The input size goes up to 5000 seconds, and each value can also go up to 5000. This immediately suggests that an O(n^2) solution is acceptable since n^2 is about 25 million operations, which fits comfortably in 2 seconds in Python with prefix sums.

A key observation is that the condition depends only on sums over intervals. This makes prefix sums a natural tool, because it allows constant time range sum queries.

The main difficulty is not computing sums, but efficiently checking all candidate intervals and extracting the maximum valid length.

A subtle edge case arises when no interval satisfies the condition. For example, if all values are 0, then every interval has sum 0, which is never greater than `100 * t`. In this case the answer must be 0, not a negative number or -1.

Another edge case is when only single elements qualify. For instance, if `r[i] = 101`, then a length-1 interval is valid, but longer intervals might fail. The solution must still correctly detect and compare all valid lengths.

Finally, note that the condition is strict: `sum > 100 * length`. Using `>=` instead would incorrectly include borderline cases like exactly `100 * t`.

## Approaches

A direct approach checks every possible subarray. For each starting index `i`, we extend to every ending index `j`, compute the sum of `r[i..j]`, and check whether it exceeds `100 * (j - i + 1)`. This is correct because it explicitly evaluates every possible interval.

However, recomputing sums from scratch for each interval leads to O(n^3) complexity if done naively. Even with partial reuse, a double loop with incremental sum updates gives O(n^2), which is the best we can hope for in brute force form.

The key improvement is to precompute prefix sums so that any interval sum can be computed in O(1). This reduces the check for each pair `(i, j)` to constant time. We still enumerate all pairs, but now each check is cheap.

The structure of the problem does not allow better than O(n^2) because we are explicitly asked for the longest valid interval without monotonic constraints that would enable two pointers or binary search. The condition is not monotone in interval length, so sliding window techniques do not apply.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force (nested + recompute) | O(n^3) | O(1) | Too slow |
| Prefix Sum + O(n^2) enumeration | O(n^2) | O(n) | Accepted |

## Algorithm Walkthrough

1. Build a prefix sum array where `pref[i]` stores the sum of the first `i` elements. This allows fast computation of any segment sum later.
2. Iterate over all possible left endpoints `l` from 0 to n - 1.
3. For each `l`, extend the right endpoint `r` from `l` to n - 1.
4. Compute the sum of the segment `[l, r]` using `pref[r+1] - pref[l]`.
5. Compute the length of the segment as `r - l + 1`.
6. Check whether `segment_sum > 100 * length`.
7. If the condition holds, update the answer with the maximum length seen so far.

The reason we scan all `(l, r)` pairs is that any valid interval must appear somewhere in this enumeration. Prefix sums ensure that we do not recompute overlapping sums repeatedly.

### Why it works

The algorithm evaluates every possible contiguous interval exactly once. For each interval, correctness of the check depends only on an exact arithmetic comparison between its sum and a linear threshold based on its length. Since prefix sums give exact interval sums, no approximation or heuristic is involved. Therefore, any interval that satisfies the condition will be detected, and the maximum length among them is tracked.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    r = list(map(int, input().split()))

    pref = [0] * (n + 1)
    for i in range(n):
        pref[i + 1] = pref[i] + r[i]

    ans = 0

    for l in range(n):
        for rgt in range(l, n):
            total = pref[rgt + 1] - pref[l]
            length = rgt - l + 1
            if total > 100 * length:
                if length > ans:
                    ans = length

    print(ans)

if __name__ == "__main__":
    solve()
```
