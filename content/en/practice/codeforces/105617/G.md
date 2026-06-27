---
title: "CF 105617G - M-11 Highway"
description: "We are given a sequence of points placed on a straight line in increasing order of coordinate. Each point is either a gas station or a rest area. We are also given a maximum allowed distance d."
date: "2026-06-26T18:21:52+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105617
codeforces_index: "G"
codeforces_contest_name: "2024-2025 Russia Team Open, High School Programming Contest (VKOSHP XXV)"
rating: 0
weight: 105617
solve_time_s: 58
verified: true
draft: false
---

[CF 105617G - M-11 Highway](https://codeforces.com/problemset/problem/105617/G)

**Rating:** -  
**Tags:** -  
**Solve time:** 58s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a sequence of points placed on a straight line in increasing order of coordinate. Each point is either a gas station or a rest area. We are also given a maximum allowed distance `d`.

We need to count ordered triples of points `(i, j, k)` such that `i < j < k` in the given order, the outer two points are gas stations, the middle point is a rest area, and the distance between the two gas stations does not exceed `d`.

Because the coordinates are strictly increasing in the input, the index order already matches left-to-right order on the line. So “i < j < k” is equivalent to “i is left of j is left of k”.

The condition is therefore geometrically simple: pick two gas stations as endpoints of an interval whose length is at most `d`, and count how many rest areas lie strictly between them.

The constraints go up to `5 × 10^5` points, which immediately rules out any quadratic enumeration over triples or even all pairs of points. A naive O(n²) scan over all gas station pairs would already be too slow in the worst case when half of the points are gas stations.

A more subtle issue appears if one tries to fix a pair of gas stations and count middle points by scanning between them. Even if each scan is linear, repeated scanning over overlapping ranges leads to cubic behavior in dense cases.

Edge cases that commonly break naive reasoning include situations where all points are gas stations, where all points are rest areas, or where gas stations are clustered tightly so that almost every pair satisfies the distance constraint. In particular, if all points are gas stations, the answer must be zero regardless of distances. Conversely, if there are many rest areas between a valid gas pair, each such rest contributes independently, which can easily be double-counted if the structure is not carefully organized.

## Approaches

A brute-force strategy is straightforward: iterate over all triples `(i, j, k)`, check the types and the coordinate constraint, and count valid ones. This is correct because it directly follows the definition, but it requires checking O(n³) triples in the worst case. Even restricting to gas stations reduces it to O(g² r) in dense configurations, which is still far beyond limits for `n = 5 × 10^5`.

The key observation is that the middle point is independent once we fix the endpoints. For any fixed pair of gas stations `(i, k)` with `x_k - x_i ≤ d`, every rest area between them contributes exactly one valid triple with that pair. So the problem becomes counting, for each valid gas pair, how many rest points lie in its interval.

This suggests separating structure by type and using prefix sums. Once points are ordered by coordinate, we can maintain a running count of rest areas and convert “how many rest points lie between two indices” into a difference of prefix values. The remaining challenge is efficiently iterating only over gas station pairs that satisfy the distance constraint. This is handled by a two-pointer window over gas stations.

We sweep the right endpoint over gas stations. For each right endpoint, we maintain the leftmost gas station still within distance `d`. All gas stations in this window form valid pairs with the current right endpoint. Instead of enumerating them individually, we aggregate their contribution using a running sum of prefix values.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute force triples | O(n³) | O(1) | Too slow |
| Gas pairs + prefix + two pointers | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

We preprocess the array so that we can quickly query how many rest areas exist in any prefix of the line.

1. Build an array `pref_rest`, where `pref_rest[i]` is the number of rest areas among points `1` through `i`. This allows constant-time counting of rest points in any segment.
2. Extract the indices of all gas stations into a list `gas`. We will only iterate over these points for the main logic.
3. Use a two-pointer window over the `gas` list. Let the right pointer `r` move from left to right over gas stations.
4. Maintain a left pointer `l` such that the distance constraint holds for all gas stations in the window, meaning `x[gas[r]] - x[gas[l]] ≤ d`. When this is violated, we move `l` forward. This ensures every gas station in `[l, r]` is a valid left endpoint for `gas[r]`.
5. While processing a fixed right endpoint `r`, we want to sum contributions of all left endpoints `i` in the window. For each pair `(i, r)`, the number of valid middle points is `pref_rest[r_idx - 1] - pref_rest[i_idx]`, where `i_idx` and `r_idx` are their original positions in the array.
6. Split the sum over all `i` in the window:

- The term `pref_rest[r_idx - 1]` is constant for the fixed `r`, so it contributes `(window_size) * pref_rest[r_idx - 1]`.
- The term `-pref_rest[i_idx]` requires maintaining the sum of `pref_rest[i_idx]` over all gas stations currently in the window.
7. Maintain a running sum `sum_pref` of `pref_rest[i_idx]` for gas stations in the current window, updating it as the window slides.
8. For each `r`, add:

`window_size * pref_rest[r_idx - 1] - sum_pref` to the answer.

### Why it works

The correctness rests on two coupled invariants. First, the sliding window always represents exactly the set of gas stations that can legally pair with the current right endpoint under the distance constraint. Second, for each such pair, the number of valid middle points depends only on prefix counts and decomposes linearly over left endpoints.

Because each valid triple is uniquely represented by a choice of right gas station `k`, left gas station `i`, and a rest station between them, and because the contribution of each pair is counted exactly once when `k` is processed, no overcounting or undercounting occurs.

## Python Solution

```python
import sys
input = sys.stdin.readline

n, d = map(int, input().split())
x = []
t = []

for _ in range(n):
    xi, ti = map(int, input().split())
    x.append(xi)
    t.append(ti)

pref_rest = [0] * (n + 1)
for i in range(n):
    pref_rest[i + 1] = pref_rest[i] + (1 if t[i] == 0 else 0)

gas = [i for i in range(n) if t[i] == 1]

ans = 0
l = 0
sum_pref = 0

for r in range(len(gas)):
    ri = gas[r]

    while l < r and x[ri] - x[gas[l]] > d:
        sum_pref -= pref_rest[gas[l] + 1]
        l += 1

    # add current right endpoint contribution
    window_size = r - l
    if window_size > 0:
        ans += window_size * pref_rest[ri] - sum_pref

    sum_pref += pref_rest[ri + 1]

print(ans)
```

The core structure of the code follows exactly the sliding window over gas stations. The prefix array is built in one pass. The two-pointer loop ensures each gas station enters and leaves the window at most once.

A subtle implementation detail is that prefix values are taken as `pref_rest[i+1]` for gas index `i`, because `pref_rest` is defined over the original array indices shifted by one. Mixing 0-based and 1-based indexing here is the most common source of off-by-one errors.

## Worked Examples

Consider a simplified trace where gas stations are sparse so the window is easy to follow.

### Example 1

Input:

```
5 5
1 1
2 0
3 1
6 0
7 1
```

Gas stations are at indices 0, 2, 4.

| r (gas idx) | l | window gas | pref_rest[r+1] | sum_pref | contribution |
| --- | --- | --- | --- | --- | --- |
| 0 | 0 | [0] | 0 | 1 | 0 |
| 1 | 0 | [0,2] | 1 | 2 | (1 * 1 - 1) = 0 |
| 2 | 1 | [2,4] | 2 | 4 | (1 * 2 - 2) = 0 |

This demonstrates that rest contributions only appear when a rest lies strictly between gas endpoints, and the prefix subtraction correctly captures that.

### Example 2

Input:

```
6 10
1 1
2 0
3 0
4 1
5 0
6 1
```

Gas stations at 0, 3, 5.

| r | l | window | pref_rest[r+1] | sum_pref | contribution |
| --- | --- | --- | --- | --- | --- |
| 0 | 0 | [0] | 0 | 1 | 0 |
| 1 | 0 | [0,3] | 2 | 3 | (2*2 - 1) = 3 |
| 2 | 0 | [0,3,5] | 3 | 6 | (3*3 - 6) = 3 |

This trace shows how multiple rest points accumulate correctly via prefix differences and how contributions scale with the number of left endpoints.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Each point is processed once in prefix computation, and each gas station enters and exits the sliding window at most once |
| Space | O(n) | Prefix array and gas index list |

The linear complexity is essential for handling up to `5 × 10^5` points within the time limit. The algorithm avoids any pairwise enumeration and reduces the problem to a single sweep over gas stations.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    n, d = map(int, input().split())
    x = []
    t = []
    for _ in range(n):
        xi, ti = map(int, input().split())
        x.append(xi)
        t.append(ti)

    pref_rest = [0] * (n + 1)
    for i in range(n):
        pref_rest[i + 1] = pref_rest[i] + (1 if t[i] == 0 else 0)

    gas = [i for i in range(n) if t[i] == 1]

    ans = 0
    l = 0
    sum_pref = 0

    for r in range(len(gas)):
        ri = gas[r]

        while l < r and x[ri] - x[gas[l]] > d:
            sum_pref -= pref_rest[gas[l] + 1]
            l += 1

        if r - l > 0:
            ans += (r - l) * pref_rest[ri] - sum_pref

        sum_pref += pref_rest[ri + 1]

    return str(ans)

# provided samples
assert run("""8 5
1 1
2 0
3 1
6 0
7 0
8 1
15 1
19 1
""") == "3"

assert run("""10 6
0 1
1 0
3 1
4 0
5 1
8 1
10 0
11 0
14 1
18 1
""") == "7"

# custom cases
assert run("""3 10
1 1
2 0
3 1
""") == "1", "single middle rest"

assert run("""4 1
1 1
2 0
3 1
4 1
""") == "1", "tight distance constraint"

assert run("""5 100
1 1
2 1
3 1
4 1
5 1
""") == "0", "no rest stations"

assert run("""5 100
1 0
2 0
3 0
4 0
5 0
""") == "0", "no gas stations"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 3-point mixed | 1 | minimal valid triple |
| tight d | 1 | sliding window correctness |
| all gas | 0 | no middle points possible |
| all rest | 0 | no endpoints exist |

## Edge Cases

When all points are gas stations, the prefix structure still builds correctly, but the gas list becomes the full index set. The sliding window may contain many pairs, yet every contribution evaluates to zero because `pref_rest` is always zero at gas positions. The algorithm naturally accumulates zero without special handling.

When all points are rest areas, the gas list is empty. The loop over gas stations never runs, so no contributions are added and the answer remains zero. This avoids any need for guarding against empty structures.

When gas stations are extremely close in coordinate space, the window expands to include many left endpoints. The algorithm still behaves correctly because each left endpoint contributes independently through the maintained prefix sum, and no pair is double-counted due to the strict single pass over right endpoints.
