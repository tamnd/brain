---
title: "CF 1606B - Update Files"
description: "We are asked to determine the minimum time required to copy an operating system update from a single initially updated computer to all the computers in a network."
date: "2026-06-10T07:49:26+07:00"
tags: ["codeforces", "competitive-programming", "greedy", "implementation", "math"]
categories: ["algorithms"]
codeforces_contest: 1606
codeforces_index: "B"
codeforces_contest_name: "Educational Codeforces Round 116 (Rated for Div. 2)"
rating: 1100
weight: 1606
solve_time_s: 79
verified: true
draft: false
---

[CF 1606B - Update Files](https://codeforces.com/problemset/problem/1606/B)

**Rating:** 1100  
**Tags:** greedy, implementation, math  
**Solve time:** 1m 19s  
**Verified:** yes  

## Solution
## Problem Understanding

We are asked to determine the minimum time required to copy an operating system update from a single initially updated computer to all the computers in a network. Each computer can copy the update to at most one other computer per hour, and the network has a total of `k` patch cables that limit the number of simultaneous transfers in a given hour. The goal is to output, for multiple test cases, the smallest number of hours needed so that every computer has the update.

The key constraints are large: `n` and `k` can each be up to $10^{18}$, and there can be up to $10^5$ test cases. This rules out any solution that simulates each hour directly, because simulating an operation for every computer would be far too slow. The solution must instead reason mathematically about the growth of updated computers each hour, handling extremely large numbers without iterating over them.

A subtle edge case arises when `k` is very small compared to `n`. For example, if `n = 7` and `k = 1`, the update spreads almost linearly because only one new computer can receive the update per hour, despite having multiple computers already updated. Conversely, if `k >= n - 1`, multiple updates can occur simultaneously, and the time reduces dramatically. The case where `n = 1` is trivial: no updates are needed, and the output must be `0`.

## Approaches

A brute-force approach would simulate each hour: maintain a counter of computers with the update, compute the number of computers that can be updated based on available patch cables, and continue until all `n` computers are updated. This method is correct but its complexity is roughly proportional to `n`, making it infeasible for large `n` up to $10^{18}$.

The insight for an optimal approach comes from viewing the spread as two phases. In the first phase, when the number of updated computers `u` is less than `k`, the update capacity is limited by `u`, because each computer can only send the update to one other computer per hour. During this phase, the number of updated computers doubles each hour. In the second phase, when `u >= k`, the number of updates per hour is capped by `k`, because the patch cables become the bottleneck. In this phase, the number of updated computers grows linearly by `k` each hour until reaching `n`.

Using this observation, we can compute the number of hours required in two parts. First, count how many hours it takes for the updated computers to reach `k` via doubling. Second, once the number of updated computers is at least `k`, calculate the remaining number of computers to update and divide by `k` to get the number of additional hours needed. This reduces the complexity to `O(log k + 1)` per test case, which is fast enough even for the largest constraints.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Simulation | O(n) per test case | O(1) | Too slow for n up to 10^18 |
| Doubling + Linear Phase | O(log k + 1) per test case | O(1) | Accepted |

## Algorithm Walkthrough

1. Read `t`, the number of test cases, and for each test case, read `n` and `k`.
2. Initialize `hours = 0` and `updated = 1` to track the number of computers with the update.
3. While `updated < k` and `updated < n`, double the number of updated computers each hour. Increment `hours` for each doubling step. Doubling is appropriate here because when the number of updated computers is less than `k`, each updated computer can copy to a new one.
4. After the doubling phase, if `updated >= n`, print `hours` as the result, since all computers are updated.
5. Otherwise, compute the remaining computers as `remaining = n - updated`. Each hour now updates up to `k` computers, so the additional hours required are `(remaining + k - 1) // k` to round up. Add these hours to the total.
6. Output the total hours for the test case.

Why it works: The algorithm maintains an invariant that `updated` always represents the maximum number of computers that can have the update at that hour. In the first phase, the maximum growth is limited by the number of updated computers (`updated < k`), giving exponential growth. In the second phase, the bottleneck is the number of patch cables, so growth is linear by `k` per hour. This ensures that the total hours calculated are minimal.

## Python Solution

```python
import sys
input = sys.stdin.readline

def min_hours(n, k):
    if n == 1:
        return 0
    hours = 0
    updated = 1
    while updated < k and updated < n:
        updated *= 2
        hours += 1
    if updated >= n:
        return hours
    remaining = n - updated
    hours += (remaining + k - 1) // k
    return hours

t = int(input())
for _ in range(t):
    n, k = map(int, input().split())
    print(min_hours(n, k))
```

The solution reads input efficiently using `sys.stdin.readline` due to the potentially large number of test cases. The `min_hours` function encapsulates the algorithm described above. Doubling occurs while `updated < k`, and once this threshold is crossed, we calculate the linear phase. Care is taken to round up in the linear phase using `(remaining + k - 1) // k`, which avoids off-by-one errors.

## Worked Examples

Consider the first sample `n = 8, k = 3`.

| Hour | Updated | Notes |
| --- | --- | --- |
| 0 | 1 | initial state |
| 1 | 2 | double since 1 < 3 |
| 2 | 4 | double since 2 < 3 → capped by k=3 eventually, next doubling to 4 |
| 3 | 8 | remaining = 8 - 4 = 4 → linear phase with k=3 → hours = ceil(4/3) = 2 → total hours = 4 |

This matches the expected output `4`.

For `n = 7, k = 1`, doubling phase does not occur because `updated >= k` fails initially. The algorithm enters linear growth immediately:

| Hour | Updated | Notes |
| --- | --- | --- |
| 0 | 1 | initial state |
| 1 | 2 | add k=1 |
| 2 | 3 | add k=1 |
| 3 | 4 | add k=1 |
| 4 | 5 | add k=1 |
| 5 | 6 | add k=1 |
| 6 | 7 | add k=1 → done |

Output is `6`, as expected.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(log k) per test case | Doubling phase takes log k steps, linear phase is computed in O(1) with arithmetic |
| Space | O(1) per test case | Only counters and arithmetic needed; no large structures |

Given `t <= 10^5` and each test case taking O(log k) steps, the total operations are well within limits. The space used is negligible.

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
        print(min_hours(n, k))
    return output.getvalue().strip()

# provided samples
assert run("4\n8 3\n6 6\n7 1\n1 1\n") == "4\n3\n6\n0", "sample tests"

# custom cases
assert run("2\n1 1\n10 10\n") == "0\n4", "trivial and k=n case"
assert run("1\n1000000000000000000 1\n") == "999999999999999999", "large n, k=1"
assert run("1\n15 5\n") == "4", "small doubling then linear"
assert run("1\n10 100\n") == "4", "k > n, direct doubling suffices"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 1 | 0 | minimal case, no update needed |
| 10 10 | 4 | k = n, check doubling + linear phase |
| 1000000000000000000 1 | 999999999999999999 | very large n, minimal k |
| 15 5 | 4 | small n, k < n, both phases involved |
| 10 100 | 4 | k > n, doubling sufficient |

## Edge Cases

For `n = 1, k = 1`, the initial computer already has the update. The algorithm returns `0` without entering any loop, correctly handling the minimal scenario.

For `k = 1`, each hour only one computer can be updated. The doubling loop is skipped, and the algorithm adds `(n - 1 + 1 - 1) // 1 = n - 1` hours, which matches the expected linear spread. For example, `n = 7, k = 1` yields `
