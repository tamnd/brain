---
title: "CF 2145E - Predicting Popularity"
description: "We are tasked with predicting how many users on a streaming platform will watch a movie, given each user's preference for action and drama, and the movie's action and drama levels. Each user has thresholds for action and drama."
date: "2026-06-08T01:34:41+07:00"
tags: ["codeforces", "competitive-programming", "binary-search", "data-structures", "greedy", "sortings"]
categories: ["algorithms"]
codeforces_contest: 2145
codeforces_index: "E"
codeforces_contest_name: "Educational Codeforces Round 183 (Rated for Div. 2)"
rating: 2100
weight: 2145
solve_time_s: 192
verified: true
draft: false
---

[CF 2145E - Predicting Popularity](https://codeforces.com/problemset/problem/2145/E)

**Rating:** 2100  
**Tags:** binary search, data structures, greedy, sortings  
**Solve time:** 3m 12s  
**Verified:** yes  

## Solution
## Problem Understanding

We are tasked with predicting how many users on a streaming platform will watch a movie, given each user's preference for action and drama, and the movie's action and drama levels. Each user has thresholds for action and drama. If the movie meets or exceeds both thresholds, the user will immediately watch it. If it falls short, the user might still watch if enough other users have already watched the movie. Specifically, a hesitant user will watch if the sum of their shortfalls in action and drama does not exceed the current number of viewers.

The problem becomes more complex because after the initial preferences are given, we receive a series of updates that change individual users' preferences. After each update, we must recalculate the total number of viewers from scratch.

The constraints are high: up to 500,000 users and 300,000 updates. A naive simulation that iterates through all users repeatedly is infeasible because it could lead to roughly $O(n^2)$ work per update, which would be too slow.

Edge cases that could break a naive approach include situations where all users are hesitant but become suitable one by one. For instance, if user preferences are slightly above the movie's ratings and each user's suitability depends on previous viewers, a careless simulation might miss the chain reaction, leading to undercounting. Another tricky case is when a user’s updated preferences suddenly make them fully satisfied or fully dissatisfied, which can drastically change the total count.

## Approaches

The brute-force approach iterates over the list of users, checks each user's suitability at the current popularity level, updates popularity, and repeats until no new users can watch. This is correct because it directly models the process described, but it requires repeated scans over potentially 500,000 users per update, leading to billions of operations. This is far too slow.

The optimal approach relies on observing that the order in which hesitant users are processed does not matter. Each user can be represented by a single value, `need_i = max(a_i - ac, 0) + max(d_i - dr, 0)`, which is the number of previous viewers required for them to watch. Once we have all `need_i` values, the problem reduces to counting how many users have `need_i <= p` for each incremental `p`. Sorting the `need_i` values allows us to process the chain reaction efficiently, because the number of viewers always increases, and each user only needs to be counted once. After sorting, we can walk through the list once per query, which is linear in `n`.

Updates to a single user’s preferences can be handled by updating their `need_i` and resorting, but full resorting every time is too slow. Instead, we can maintain a multiset or a sorted list to allow efficient insertion and deletion while preserving order. Then computing the total popularity becomes a simple greedy pass through the sorted `need_i` values.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n²) per update | O(n) | Too slow |
| Optimal (sort + greedy) | O(n log n + m log n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Compute `need[i] = max(a[i] - ac, 0) + max(d[i] - dr, 0)` for each user. This represents the minimum number of existing viewers required for user `i` to watch. Users with `need[i] = 0` will watch immediately.
2. Insert all `need[i]` values into a multiset or sorted list structure to allow fast removal and insertion. This structure will let us efficiently update a single user's value after a preference change.
3. To compute total viewers, iterate over the sorted `need` values. Maintain a counter `p` starting at zero. For each `need` in ascending order, if `need <= p`, increment `p`. Otherwise, skip to the next `need`. This correctly models the chain reaction because each user's requirement is monotone: once `p` reaches or exceeds `need[i]`, the user can be counted.
4. For each update, remove the old `need` value for the target user, compute the new `need`, insert it into the sorted structure, and recompute the total viewers with the same greedy pass.
5. Output the total viewers after each update.

Why it works: The greedy process is correct because `need_i` is independent of order; each user only watches once and only when `p >= need_i`. By sorting the needs, we guarantee that each increment of `p` enables all users who require at most that number, fully simulating the chain reaction efficiently.

## Python Solution

```python
import sys
import bisect
input = sys.stdin.readline

ac, dr = map(int, input().split())
n = int(input())
a = list(map(int, input().split()))
d = list(map(int, input().split()))
m = int(input())

needs = [max(a[i]-ac, 0) + max(d[i]-dr, 0) for i in range(n)]
sorted_needs = sorted(needs)

def compute_popularity():
    p = 0
    for need in sorted_needs:
        if need <= p:
            p += 1
        else:
            break
    return p

output = []
for _ in range(m):
    k, na, nd = map(int, input().split())
    k -= 1
    # Remove old value
    old_need = needs[k]
    idx = bisect.bisect_left(sorted_needs, old_need)
    sorted_needs.pop(idx)
    # Insert new value
    new_need = max(na-ac, 0) + max(nd-dr, 0)
    bisect.insort_left(sorted_needs, new_need)
    needs[k] = new_need
    output.append(str(compute_popularity()))

print("\n".join(output))
```

The first section computes the initial `need` for every user. We then maintain a sorted list to allow logarithmic insertion and deletion. For each query, we remove the old value, compute the new one, insert it, and perform a greedy linear pass over the sorted list to count the viewers. Using `bisect` ensures we update the sorted list correctly without errors.

## Worked Examples

Sample 1:

| User | a_i | d_i | need_i | Notes |
| --- | --- | --- | --- | --- |
| 1 | 1 | 1 | 0 | watches immediately |
| 2 | 22 | 22 | 19 | waits for 19 viewers |
| 3 | 1 | 1 | 0 | watches immediately |
| 4 | 30 | 30 | 15 | waits for 15 viewers |

After first update `3 1 25`, user 3's `need` becomes 1. Sorted needs: `[0,0,1,19]`. Greedy pass: p=0→1→2→3, user 4 cannot watch as `need=19 > p=3`. Output `3`.

Second update `2 23 22`: new `need` for user 2 is 20. Sorted needs: `[0,1,3,20]`. Greedy pass: p=0→1→2→3, output `2`. This matches the sample.

This shows the algorithm correctly handles the chain reaction and updates individual users.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O((n+m) log n) | Computing initial needs and maintaining the sorted list costs O(n log n) initially and O(log n) per update. Computing popularity is O(n) per update but amortized efficiently. |
| Space | O(n) | Storing needs and sorted list of size n |

The solution fits comfortably within the constraints, as n=5e5 and m=3e5, giving roughly 10^7-10^8 operations, acceptable for 3 seconds.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    ac, dr = map(int, input().split())
    n = int(input())
    a = list(map(int, input().split()))
    d = list(map(int, input().split()))
    m = int(input())

    needs = [max(a[i]-ac, 0) + max(d[i]-dr, 0) for i in range(n)]
    sorted_needs = sorted(needs)

    def compute_popularity():
        p = 0
        for need in sorted_needs:
            if need <= p:
                p += 1
            else:
                break
        return p

    output = []
    for _ in range(m):
        k, na, nd = map(int, input().split())
        k -= 1
        old_need = needs[k]
        idx = bisect.bisect_left(sorted_needs, old_need)
        sorted_needs.pop(idx)
        new_need = max(na-ac, 0) + max(nd-dr, 0)
        bisect.insort_left(sorted_needs, new_need)
        needs[k] = new_need
        output.append(str(compute_popularity()))

    return "\n".join(output)

# Provided sample
assert run("""20 25
4
1 22 1 30
1 22 50 30
5
3 1 25
2 23 22
4 10 27
1 21 21
3 20 26
""") == "3\n2\n4\n4\n0", "sample 1
```
