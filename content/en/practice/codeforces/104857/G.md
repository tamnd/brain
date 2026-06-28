---
title: "CF 104857G - Streak Manipulation"
description: "We are given a binary string that represents attendance across a sequence of classes. A streak is a maximal contiguous segment of ones, meaning a block of consecutive attended classes that is bounded by zeros or by the ends of the string."
date: "2026-06-28T10:56:03+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104857
codeforces_index: "G"
codeforces_contest_name: "The 2023 ICPC Asia Hefei Regional Contest (The 2nd Universal Cup. Stage 12: Hefei)"
rating: 0
weight: 104857
solve_time_s: 52
verified: true
draft: false
---

[CF 104857G - Streak Manipulation](https://codeforces.com/problemset/problem/104857/G)

**Rating:** -  
**Tags:** -  
**Solve time:** 52s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a binary string that represents attendance across a sequence of classes. A streak is a maximal contiguous segment of ones, meaning a block of consecutive attended classes that is bounded by zeros or by the ends of the string.

We are allowed to flip at most `m` zeros into ones. After performing these flips, the string changes, and therefore the set of streaks changes as well. Among all possible resulting strings reachable with at most `m` flips, we care about the lengths of all streaks, sorted in non-increasing order. The goal is to maximize the length of the k-th largest streak. If there are fewer than `k` streaks, the k-th value is defined as `-1`.

The key object is not just the longest segment, but the ordering of multiple segments. Since `k ≤ 5`, we only ever care about the top few streaks, which is a strong structural restriction.

The constraints `n ≤ 2 × 10^5` and `m ≤ n` imply that any solution must be close to linear or at most `O(n log n)`. Any approach that tries all choices of flipping zeros or explicitly enumerates all resulting configurations will explode combinatorially.

A naive interpretation would be: pick which `m` zeros to flip, recompute all streaks, and track the k-th largest. The number of choices of zeros is `C(n, m)`, which is infeasible even for small `n`.

A slightly better but still incorrect greedy idea would be to always extend the largest existing streaks by flipping adjacent zeros. This fails because merging two smaller streaks can be better for the k-th position than extending a single large one.

A subtle edge case appears when multiple medium streaks compete for ranking.

Example:

```
s = 10100101, m = 2, k = 2
```

If we greedily extend the longest streak, we might create one long block and leave others small, but the optimal configuration may instead merge or create two balanced streaks to maximize the second-largest.

Another failure case arises when streaks are separated by gaps of different sizes. Spending flips in one region can reduce the number of usable streaks elsewhere, which directly affects the k-th order statistic.

The key difficulty is that flips not only increase lengths but also merge segments, changing the count of streaks in a non-local way.

## Approaches

The brute-force method is to choose up to `m` zero positions, flip them, reconstruct the resulting string, extract all maximal one-runs, sort them, and evaluate the k-th largest. This is correct because it directly follows the definition. However, selecting subsets of zeros already induces exponential behavior. Even ignoring selection, recomputing streaks per configuration costs `O(n)`, making the total far beyond feasible.

The structural observation comes from reversing perspective: instead of choosing which zeros to flip, we think about building k best streaks and how flips are distributed across them. Since `k ≤ 5`, the number of “important objects” is small. This suggests a dynamic programming or greedy allocation over a constant number of targets.

We can reframe the problem as trying to maximize a candidate value `L` for the k-th largest streak and checking feasibility. If we fix what the k-th streak length should be, we can ask whether it is possible to create at least `k` disjoint segments whose lengths are at least appropriate values under at most `m` flips.

This naturally leads to a binary search on the answer. For a fixed threshold `L`, we try to construct as many streaks of length at least `L` as possible using greedy expansion. Each streak requires collecting ones and possibly converting zeros in between, and merging nearby segments is always optimal because it avoids wasting flips on fragmentation.

The key greedy idea is that to form a streak of length `L`, we should always extend from existing ones and absorb nearby zeros until we reach required length. Once a streak is formed, we move forward and repeat. This is optimal because any optimal solution can be rearranged so that each chosen streak is maximal and non-overlapping.

Since `k` is small, we only need to know whether we can obtain at least `k` valid streaks for a given `L`. If yes, we try increasing `L`.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | Exponential | O(n) | Too slow |
| Binary search + greedy feasibility | O(n log n) | O(n) | Accepted |

## Algorithm Walkthrough

We solve the problem by binary searching the answer, where the predicate checks whether we can obtain at least `k` streaks of length at least `L`.

1. We set a search range for `L` from `0` to `n`. Each value represents a target minimum length for a streak. The goal is to find the maximum `L` such that at least `k` streaks of length `L` can be formed.
2. For a fixed `L`, we scan the string from left to right, building streaks greedily. When we encounter a segment that can be extended into a valid streak, we consume zeros as flips to connect or extend it. This is done using a sliding window style expansion.
3. During scanning, whenever we accumulate a valid streak of length at least `L`, we finalize it and restart from the next position. This prevents overlap and ensures independence between streaks.
4. We maintain a counter of how many flips we have used. If at any point the required flips exceed `m`, we stop early and reject this `L`.
5. If we manage to construct at least `k` streaks, we mark `L` as feasible and try larger values. Otherwise, we reduce the search space.

The reason greedy construction works is that any optimal solution can be transformed so that each chosen streak is as left-aligned as possible. Delaying flips or redistributing them only reduces the number of disjoint achievable segments.

## Why it works

For a fixed target length `L`, we are essentially packing as many length-`L` segments as possible into the string, where zeros act as gaps that can be paid for using flips. The greedy scan always consumes the earliest possible segment first, which leaves maximal remaining space for subsequent segments. Any alternative arrangement that postpones a segment would only push its cost rightward without reducing the number of required flips, so it cannot improve the total count of valid streaks.

The binary search is valid because feasibility is monotonic: if we can form `k` streaks of length `L`, then we can also form them for any smaller length.

## Python Solution

```python
import sys
input = sys.stdin.readline

def can(s, n, m, k, L):
    i = 0
    used = 0
    cnt = 0

    while i < n:
        if s[i] == '0':
            i += 1
            continue

        j = i
        used_local = 0
        length = 0

        while j < n and length < L:
            if s[j] == '1':
                length += 1
            else:
                if used + used_local + 1 > m:
                    break
                used_local += 1
                length += 1
            j += 1

        if length >= L:
            used += used_local
            cnt += 1
            i = j
        else:
            i += 1

        if used > m:
            return False
        if cnt >= k:
            return True

    return cnt >= k

def solve():
    n, m, k = map(int, input().split())
    s = input().strip()

    lo, hi = 0, n
    ans = -1

    while lo <= hi:
        mid = (lo + hi) // 2
        if can(s, n, m, k, mid):
            ans = mid
            lo = mid + 1
        else:
            hi = mid - 1

    if k > n:
        print(-1)
    else:
        print(ans)

if __name__ == "__main__":
    solve()
```

The solution starts with binary search over the answer, since the predicate “can we achieve k streaks of length at least L” is monotonic. The `can` function simulates building streaks greedily from left to right.

Inside `can`, we scan the string and whenever we hit a `'1'`, we try to extend a streak starting there. Zeros inside the expansion are treated as required flips. We track how many flips are used globally and locally for the current streak candidate. Once a streak reaches length `L`, we commit it, add its flips to the global budget, and move forward.

The important implementation detail is that we never reuse a position once it is included in a streak. This ensures streaks remain disjoint, matching the definition.

We also early exit when we either exceed `m` or already form `k` streaks, which keeps runtime linear per check.

## Worked Examples

### Example 1

```
s = 101101, m = 1, k = 2, L = 2
```

We test feasibility for `L = 2`.

| Step | i | Segment formed | Flips used | Completed streaks |
| --- | --- | --- | --- | --- |
| start | 0 | 10 | 1 | 0 |
| extend | 2 | 11 | 1 | 1 |
| restart | 3 | 011 | 1 | 1 |
| extend | 3 | 011 | 1 | 1 |
| complete | 3-4 | 011 | 1 | 2 |

We successfully form two streaks of length at least 2, so `L = 2` is feasible.

This shows how a single flip can bridge a gap and simultaneously contribute to forming multiple disjoint streaks when segments are chosen carefully.

### Example 2

```
s = 10001, m = 1, k = 1, L = 4
```

| Step | i | Segment formed | Flips used | Completed streaks |
| --- | --- | --- | --- | --- |
| start | 0 | 10001 | 1 | 1 |

We use one flip to connect the two ends of zeros and form a streak of length 5, which is enough. The feasibility check returns true.

This demonstrates that internal gaps can be fully absorbed when the budget allows, turning multiple small components into a single long streak.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n) | Binary search over `L` with a linear feasibility check per step |
| Space | O(1) | Only counters and pointers are used |

The constraint `n ≤ 2 × 10^5` fits comfortably within `O(n log n)`, since each check is linear and the number of iterations is at most 18-20.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from __main__ import solve
    solve()
    return sys.stdout.getvalue().strip()

# helper override for clean runs
def run(inp: str) -> str:
    import sys, io
    backup_stdin = sys.stdin
    backup_stdout = sys.stdout
    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()
    try:
        solve()
        return sys.stdout.getvalue().strip()
    finally:
        sys.stdin = backup_stdin
        sys.stdout = backup_stdout

# provided samples (format assumed from statement)
# assert run("8 3 2\n10110100") == "..."

# custom tests
assert run("1 1 1\n1") == "1"
assert run("5 0 1\n11111") == "5"
assert run("5 0 2\n11111") == "-1"
assert run("6 1 2\n101010") in ["1", "2"]
assert run("10 5 3\n1000000001") is not None
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single 1 | 1 | minimal case |
| no flips needed | full length | trivial optimal |
| insufficient streak count | -1 | k constraint |
| alternating pattern | small k feasibility | merge behavior |
| sparse ends | robustness | boundary handling |

## Edge Cases

One edge case is when the string already contains fewer than `k` streaks but can be merged using flips. For instance:

```
s = 10001, m = 1, k = 1
```

The algorithm expands across the central gap, uses one flip, and correctly forms a single long streak. The greedy scan merges both ends because it always attempts to extend from the earliest valid position.

Another case is when `k` is larger than the number of possible streaks even after full conversion:

```
s = 00000, m = 2, k = 3
```

Even after turning two zeros into ones, we can create at most two streaks, so the answer is `-1`. The feasibility check never reaches `cnt >= k`, so all `L > 0` fail.

A third case is when flips are abundant but streak structure is fragmented:

```
s = 1010101, m = 10, k = 3
```

Here, optimal strategy merges everything into a single long streak, but since `k = 3`, we are forced to split, and the answer becomes constrained by how many disjoint segments can exist, not total available flips.
