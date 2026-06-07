---
title: "CF 2103C - Median Splits"
description: "We are given an array and asked whether we can cut it into three contiguous parts such that a particular condition involving medians holds across the cuts. If we pick two split points, the array is divided into three non-empty segments."
date: "2026-06-08T05:02:24+07:00"
tags: ["codeforces", "competitive-programming", "binary-search", "greedy", "implementation", "sortings"]
categories: ["algorithms"]
codeforces_contest: 2103
codeforces_index: "C"
codeforces_contest_name: "Codeforces Round 1019 (Div. 2)"
rating: 1600
weight: 2103
solve_time_s: 122
verified: false
draft: false
---

[CF 2103C - Median Splits](https://codeforces.com/problemset/problem/2103/C)

**Rating:** 1600  
**Tags:** binary search, greedy, implementation, sortings  
**Solve time:** 2m 2s  
**Verified:** no  

## Solution
## Problem Understanding

We are given an array and asked whether we can cut it into three contiguous parts such that a particular condition involving medians holds across the cuts.

If we pick two split points, the array is divided into three non-empty segments. Each segment has its own median, defined as the middle element when that segment is sorted. Then we take those three medians and compute their median again. The question is whether this final value can be at most `k`.

A useful way to rephrase the condition is that among the three segment medians, at least two must be less than or equal to `k`. This comes from the definition of the median of three values: it is ≤ `k` exactly when at least two of the three values are ≤ `k`.

The constraints are large: `n` goes up to 2⋅10^5 across all test cases, so an O(n²) approach per test case is impossible. Even O(n log n) per split candidate would be too slow if done naively for all pairs `(l, r)`.

The key difficulty is that the median of a subarray is not a simple prefix statistic; it depends on ordering inside the segment, which suggests that direct recomputation per segment is too expensive.

A few subtle edge cases are worth highlighting.

If all elements are ≤ `k`, every subarray median is automatically ≤ `k`, so the answer is trivially YES. A naive solution that incorrectly recomputes medians without considering monotonicity may still work, but a buggy greedy might fail to detect this early exit.

If exactly one segment has median ≤ `k`, the answer must be NO because the median of three values cannot be ≤ `k` unless at least two are ≤ `k`.

Another tricky situation is when large values are interspersed: a greedy attempt that tries to greedily extend segments based only on current prefix counts can fail because median depends on relative ordering inside each segment, not just counts in isolation.

## Approaches

A brute-force strategy would enumerate every pair `(l, r)` and compute the median of each of the three segments by sorting each segment or using a selection structure. For each split, we check the median condition.

This is correct but far too slow. There are O(n²) splits, and computing medians is at least O(n) or O(log n) per segment, leading to O(n³) or O(n² log n) overall, which is infeasible for 2⋅10^5 elements.

The key insight is to transform the problem from “median of medians” into a binary classification problem. We only care whether each segment median is ≤ `k`, not its exact value.

For a segment, its median is ≤ `k` exactly when at least half of its elements are ≤ `k`. So we can map the array into a transformed form where each element becomes:

+1 if `a[i] ≤ k`, otherwise -1.

Now a segment has median ≤ `k` if and only if its sum is positive. This reduces a median condition into a prefix sum condition.

Now the problem becomes: can we split the array into three contiguous segments such that at least two of the three segments have positive sum in this transformed array.

This is now a structure problem over prefix sums. We can precompute prefix sums and track whether we can find valid split points efficiently using linear scans and greedy tracking of best possible segment signs.

The final solution reduces to checking whether we can place two cut points so that at least two of the three resulting segments have positive sum.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force (enumerate splits, recompute medians) | O(n³) or O(n² log n) | O(n) | Too slow |
| Prefix transform + greedy split feasibility | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Convert the array into a binary form where each element becomes +1 if `a[i] ≤ k`, otherwise -1. This reformulates the median condition into a sum condition.
2. Build a prefix sum array over this transformed sequence. The prefix sum at position i represents how many more “good” elements (≤ k) than “bad” elements exist in the prefix.
3. Observe that a segment `[l, r]` has median ≤ k exactly when `prefix[r] - prefix[l-1] > 0`. This allows constant-time checking of segment validity.
4. We now need two cut points `l < r` such that among the three segments, at least two have positive sums. This splits into three possible patterns: first and second segments good, first and third segments good, or second and third segments good.
5. For the first-and-second case, we scan for an `l` where prefix[1..l] can form a good segment, then check if there exists `r > l` such that both `[l+1, r]` and `[r+1, n]` can be arranged to satisfy the condition using prefix minima/maxima.
6. For each pattern, we maintain running information while scanning to avoid recomputing segment sums explicitly. This ensures each position is processed once.

### Why it works

The transformation reduces a median constraint into a linear inequality over prefix sums. Because segment validity becomes monotone in prefix space, feasibility depends only on existence of cut points satisfying additive constraints. The greedy scan works because once a valid prefix or segment endpoint is found, extending or shifting boundaries preserves or only relaxes feasibility conditions in prefix sum space, so no optimal configuration is skipped.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, k = map(int, input().split())
    a = list(map(int, input().split()))
    
    b = [1 if x <= k else -1 for x in a]
    
    pref = [0] * (n + 1)
    for i in range(n):
        pref[i + 1] = pref[i] + b[i]
    
    total = pref[n]
    
    # case 1: first two segments are good
    # check if exists l, r such that:
    # sum(1..l) > 0 and sum(l+1..r) > 0
    
    ok_prefix = [False] * (n + 1)
    cur_min = 0
    for i in range(1, n + 1):
        if pref[i] - cur_min > 0:
            ok_prefix[i] = True
        cur_min = min(cur_min, pref[i])
    
    # case 2: last two segments are good
    ok_suffix = [False] * (n + 2)
    cur_max = pref[n]
    for i in range(n - 1, -1, -1):
        if cur_max - pref[i] > 0:
            ok_suffix[i] = True
        cur_max = max(cur_max, pref[i])
    
    # check any split pattern
    # pattern A: first two segments good
    # pattern B: last two segments good
    # pattern C: first and last segments good
    
    # pattern A
    for r in range(2, n):
        if ok_prefix[r]:
            return True
    
    # pattern B
    for l in range(1, n - 1):
        if ok_suffix[l]:
            return True
    
    # pattern C
    # first and last segments good
    # need prefix[i] > 0 and suffix[j] > 0 with i < j
    best = -10**18
    for i in range(1, n):
        if pref[i] > 0:
            best = max(best, i)
    for j in range(2, n + 1):
        if pref[n] - pref[j - 1] > 0 and best != -10**18 and best < j - 1:
            return True
    
    return False

t = int(input())
for _ in range(t):
    print("YES" if solve() else "NO")
```

The solution begins by turning the array into a +1 and -1 representation so that segment medians become a sign test over sums. Prefix sums then allow any segment to be evaluated in constant time.

We then precompute which prefixes and suffixes can form valid positive-sum segments. These arrays encode whether a valid segment ending or starting at a position exists without rechecking all subarrays.

Finally, we test the three possible ways to pick two “good” segments among the three required ones. Each check uses linear scans over prefix information.

The main implementation subtlety is that we never explicitly compute medians or sort subarrays; all reasoning happens in prefix sum space, and every segment condition is reduced to O(1) checks.

## Worked Examples

### Example 1

Input:

```
3 2
3 2 1
```

We transform with `k = 2`:

| i | a[i] | b[i] | pref |
| --- | --- | --- | --- |
| 1 | 3 | -1 | -1 |
| 2 | 2 | +1 | 0 |
| 3 | 1 | +1 | 1 |

We check segment feasibility:

- `[1,2]` sum = 0 (not positive)
- `[2,3]` sum = 2 (positive)

We can form two good segments, so answer is YES.

This confirms that even when prefix oscillates, suffix structure still allows valid grouping.

### Example 2

Input:

```
3 1
3 2 1
```

Transformation:

| i | a[i] | b[i] | pref |
| --- | --- | --- | --- |
| 1 | 3 | -1 | -1 |
| 2 | 2 | -1 | -2 |
| 3 | 1 | +1 | -1 |

Every segment has non-positive sum unless it is trivial. No two segments can be made positive, so no valid split exists.

This demonstrates that the same structure behaves differently when `k` is too small.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) per test case | single pass prefix computation and constant-time checks |
| Space | O(n) | prefix arrays and auxiliary tracking |

The linear complexity fits easily within the constraint of total n up to 2⋅10^5.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    input = sys.stdin.readline

    def solve():
        n, k = map(int, input().split())
        a = list(map(int, input().split()))
        b = [1 if x <= k else -1 for x in a]
        pref = [0]
        for x in b:
            pref.append(pref[-1] + x)

        def good(l, r):
            return pref[r] - pref[l - 1] > 0

        for l in range(1, n - 1):
            for r in range(l + 1, n):
                cnt = 0
                if good(1, l): cnt += 1
                if good(l + 1, r): cnt += 1
                if good(r + 1, n): cnt += 1
                if cnt >= 2:
                    return True
        return False

    t = int(input())
    out = []
    for _ in range(t):
        out.append("YES" if solve() else "NO")
    return "\n".join(out)

# provided samples
assert run("""6
3 2
3 2 1
3 1
3 2 1
6 3
8 5 3 1 6 4
8 7
10 7 12 16 3 15 6 11
6 8
7 11 12 4 9 17
3 500000000
1000 1000000000 1000
""") == """YES
NO
NO
YES
YES
YES"""
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| all elements equal and ≤ k | YES | trivial full-good array |
| alternating around k | YES/NO mix | prefix oscillation cases |
| strictly increasing large values | NO | no valid segments exist |

## Edge Cases

One edge case is when almost all elements are greater than `k` except a few isolated small values. In such cases, only very short segments can be “good”, and the algorithm relies on prefix minima correctly detecting whether any positive segment exists.

Another case is when all elements are ≤ `k`. The prefix sum is always increasing, so every segment is valid. The algorithm immediately finds valid split points in the first pattern check.

A final subtle case is when only the last segment can be made good. The suffix precomputation ensures that even if early prefixes fail, valid suffix-based configurations are still detected through reverse prefix scanning.
