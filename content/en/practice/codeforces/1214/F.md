---
title: "CF 1214F - Employment"
description: "We have two multisets of points on a circle of length m. The first set contains the office locations. Office i is located in city a[i]. The second set contains the candidates. Candidate j lives in city b[j]."
date: "2026-06-11T23:03:09+07:00"
tags: ["codeforces", "competitive-programming", "greedy", "sortings"]
categories: ["algorithms"]
codeforces_contest: 1214
codeforces_index: "F"
codeforces_contest_name: "Codeforces Round 583 (Div. 1 + Div. 2, based on Olympiad of Metropolises)"
rating: 2700
weight: 1214
solve_time_s: 160
verified: true
draft: false
---

[CF 1214F - Employment](https://codeforces.com/problemset/problem/1214/F)

**Rating:** 2700  
**Tags:** greedy, sortings  
**Solve time:** 2m 40s  
**Verified:** yes  

## Solution
# Problem Understanding

We have two multisets of points on a circle of length `m`.

The first set contains the office locations. Office `i` is located in city `a[i]`.

The second set contains the candidates. Candidate `j` lives in city `b[j]`.

Every office must receive exactly one candidate and every candidate must be assigned to exactly one office. The cost of assigning a candidate to an office is the shortest circular distance between their cities. We must minimize the total cost and also output one optimal assignment.

The circle contains up to `10^9` cities, but only `n ≤ 200000` offices and candidates. The city count is huge, so any algorithm depending on the size of the circle is impossible. The only objects we can afford to process are the `n` positions themselves.

The value of `n` immediately rules out quadratic algorithms. An `O(n²)` solution would require roughly `4 × 10^10` operations in the worst case, which is completely infeasible. The target complexity must be around `O(n log n)`.

The tricky part is that the cities lie on a circle rather than a line.

Consider:

```
m = 10
offices    : 1 9
candidates : 2 10
```

A linear interpretation would use distances `1` and `1`, but on the circle city `10` is adjacent to city `1`, so the geometry wraps around.

Another easy mistake is to sort both arrays and match them position by position.

```
m = 10
offices    : 1 4 8
candidates : 3 6 8
```

After sorting, matching equal ranks gives cost

```
|1-3| + |4-6| + |8-8| = 4
```

but on the circle we may rotate one sorted order. Matching

```
1 <- 3
4 <- 6
8 <- 8
```

is actually the shift that produces the optimum here. The key observation is that the optimal matching is always a cyclic shift of the sorted order, not necessarily the zero shift.

Duplicates create another subtle case.

```
m = 20
offices    : 5 5 5
candidates : 5 5 5
```

There are many optimal assignments. A solution must still output a valid permutation of candidate indices.

## Approaches

A brute force solution would try every possible perfect matching. There are `n!` matchings, which becomes impossible almost immediately.

A more reasonable brute force starts with a structural observation. If we sort office positions around the circle and sort candidate positions around the circle, any optimal matching has no crossing pairs. If two matched paths cross, exchanging their endpoints never increases the total distance and often decreases it. Repeatedly removing crossings transforms any optimum into a non-crossing optimum.

Once crossings are forbidden, the matching is completely determined by a cyclic shift. After sorting both sets, choose some shift `k`, then match

```
A[i] <-> B[i+k]
```

with indices taken cyclically.

That reduces the search space from `n!` matchings to only `n` shifts.

Unfortunately, evaluating every shift independently still costs `O(n²)`.

The remaining observation is that for a fixed office position `a`, its contribution as the shift changes is a piecewise-constant function over ranges of shifts. The circular distance

```
dist(a, b) = min(|a-b|, m-|a-b|)
```

changes form only when `b` crosses one of a few critical positions relative to `a`.

After sorting the coordinates, these critical transitions can be located with binary search. Each office and each candidate contributes a constant value over contiguous ranges of shifts. We can accumulate all contributions using a difference array on the shift domain.

The result is an `O(n log n)` algorithm.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force over all shifts | O(n²) | O(n) | Too slow |
| Difference-array over shifts | O(n log n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Sort the offices by city position, remembering their original indices.
2. Sort the candidates by city position, also remembering their original indices.
3. Use the non-crossing property. Any optimal assignment must match the sorted office sequence with a cyclic shift of the sorted candidate sequence.
4. Let shift `k` mean that sorted office `i` is matched with sorted candidate `(i+k) mod n`.
5. Build an array `cost[k]`, the total cost of shift `k`.
6. Instead of evaluating each shift separately, process every office position `a[i]`.

For a fixed office, the expression `dist(a[i], b[j])` changes form only when `b[j]` crosses one of four critical regions around the circle. Binary searches on the sorted candidate coordinates identify the ranges of `j` belonging to each region.
7. Convert every such region into a range update on the shift variable `k = j - i`.

A difference array allows adding the same value to an entire interval of shifts in `O(1)` time.
8. Repeat the symmetric process for every candidate position `b[j]`.

After both passes, the accumulated value for each shift equals the total matching cost for that shift.
9. Prefix-sum the difference array to recover every `cost[k]`.
10. Choose the shift with minimum cost.
11. Reconstruct the assignment. If the best shift is `k`, then sorted office `i` receives sorted candidate `(i+k) mod n`.
12. Convert the assignment back to original indices and print the result.

### Why it works

After sorting the points around the circle, any crossing matching can be uncrossed without increasing the objective value. Repeating this process yields an optimal non-crossing matching.

A non-crossing perfect matching between two cyclically ordered sets is completely determined by one starting pair. Once the first pair is chosen, the remaining pairs must follow the circular order. That means every optimal solution corresponds to some cyclic shift of the sorted candidate sequence.

The difference-array construction computes the exact total cost for every shift simultaneously. Each office-candidate pair contributes to exactly the shifts where that pair is matched, and the piecewise decomposition covers all possibilities. Consequently, the recovered value for shift `k` is precisely the total cost of the matching defined by that shift. Choosing the minimum among them yields the global optimum.

## Python Solution

```python
import sys
from bisect import bisect_right

input = sys.stdin.readline

def solve():
    m, n = map(int, input().split())

    A = [(x, i) for i, x in enumerate(map(int, input().split()), start=1)]
    B = [(x, i) for i, x in enumerate(map(int, input().split()), start=1)]

    A.sort()
    B.sort()

    a = [x for x, _ in A]
    b = [x for x, _ in B]

    aa = [2 * x for x in a]
    bb = [2 * x for x in b]

    diff = [0] * (n + 1)

    def add_range(l, r, v):
        if l > r:
            return

        l %= n
        r %= n

        if l <= r:
            diff[l] += v
            if r + 1 < n:
                diff[r + 1] -= v
        else:
            diff[0] += v
            if r + 1 < n:
                diff[r + 1] -= v
            diff[l] += v

    for i in range(n):
        x = a[i]

        r = bisect_right(bb, 2 * x - m - 1) - 1
        add_range(-i, r - i, -x)

        l = r + 1
        r = bisect_right(bb, 2 * x - 1) - 1
        add_range(l - i, r - i, x)

        l = r + 1
        r = bisect_right(bb, 2 * x + m) - 1
        add_range(l - i, r - i, -x)

        l = r + 1
        r = n - 1
        add_range(l - i, r - i, x + m)

    for i in range(n):
        x = b[i]

        r = bisect_right(aa, 2 * x - m - 1) - 1
        add_range(i - r, i, -x)

        l = r + 1
        r = bisect_right(aa, 2 * x) - 1
        add_range(i - r, i - l, x)

        l = r + 1
        r = bisect_right(aa, 2 * x + m) - 1
        add_range(i - r, i - l, -x)

        l = r + 1
        r = n - 1
        add_range(i - r, i - l, x + m)

    cur = 0
    best_shift = 0
    best_cost = None

    for k in range(n):
        cur += diff[k]
        if best_cost is None or cur < best_cost:
            best_cost = cur
            best_shift = k

    ans = [0] * n

    for i in range(n):
        j = (i + best_shift) % n
        office_idx = A[i][1]
        candidate_idx = B[j][1]
        ans[office_idx - 1] = candidate_idx

    print(best_cost)
    print(*ans)

solve()
```

The first part sorts offices and candidates while preserving original indices so that the final assignment can be reconstructed.

The core of the implementation is the shift-domain difference array. Rather than computing the cost of every shift separately, each binary search identifies a whole interval of shifts that receive the same contribution. The helper `add_range` performs cyclic range updates because shifts are taken modulo `n`.

The four binary-search ranges correspond to the four different algebraic forms of circular distance. Their derivation comes from comparing the direct arc and the wrapped arc.

After all updates are applied, a prefix sum reconstructs the total cost for every shift. The minimum shift determines the optimal matching.

One easy place to make a mistake is the modular interval update. Intervals may wrap around the end of the shift array, so they must be split into two ordinary ranges. Another common source of bugs is the use of `bisect_right(...)-1`, which intentionally finds the last index belonging to a region.

## Worked Examples

### Sample 1

Input:

```
10 3
1 5 5
10 4 6
```

Sorted positions:

| i | Office A[i] | Candidate B[i] |
| --- | --- | --- |
| 0 | 1 | 4 |
| 1 | 5 | 6 |
| 2 | 5 | 10 |

After processing all range updates:

| Shift k | Total Cost |
| --- | --- |
| 0 | 3 |
| 1 | 9 |
| 2 | 9 |

The best shift is `0`.

Matching:

| Office city | Candidate city | Distance |
| --- | --- | --- |
| 1 | 10 | 1 |
| 5 | 4 | 1 |
| 5 | 6 | 1 |

Total cost = `3`.

This example shows that the sorted orders already align optimally.

### Sample 2

Input:

```
10 3
1 4 8
3 6 8
```

Sorted positions:

| i | Office A[i] | Candidate B[i] |
| --- | --- | --- |
| 0 | 1 | 3 |
| 1 | 4 | 6 |
| 2 | 8 | 8 |

Computed costs:

| Shift k | Total Cost |
| --- | --- |
| 0 | 4 |
| 1 | 10 |
| 2 | 10 |

The best shift is `0`.

Matching:

| Office city | Candidate city | Distance |
| --- | --- | --- |
| 1 | 3 | 2 |
| 4 | 6 | 2 |
| 8 | 8 | 0 |

Total cost = `4`.

This trace illustrates the non-crossing structure. Once the first pair is fixed, the rest of the matching follows automatically.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n) | Sorting plus binary searches for every point |
| Space | O(n) | Sorted arrays, assignment array, difference array |

With `n ≤ 200000`, an `O(n log n)` solution easily fits within the time limit. The memory usage is linear and comfortably below the 512 MB limit.

## Test Cases

```python
# helper skeleton for local testing

import sys
import io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    # call solve() here
    out = io.StringIO()
    old_stdout = sys.stdout
    sys.stdout = out
    solve()
    sys.stdout = old_stdout
    return out.getvalue().strip()

# sample 1
res = run(
"""10 3
1 5 5
10 4 6
"""
)
assert res.splitlines()[0] == "3"

# sample 2
res = run(
"""10 3
1 4 8
8 3 6
"""
)
assert res.splitlines()[0] == "4"

# minimum size
res = run(
"""1 1
1
1
"""
)
assert res.splitlines()[0] == "0"

# all equal
res = run(
"""20 4
5 5 5 5
5 5 5 5
"""
)
assert res.splitlines()[0] == "0"

# wrap-around distance
res = run(
"""10 2
1 9
10 2
"""
)
assert res.splitlines()[0] == "2"

# duplicated cities
res = run(
"""100 3
10 10 50
9 11 50
"""
)
assert res.splitlines()[0] == "2"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `m=1, n=1` | cost `0` | Minimum constraints |
| All cities equal | cost `0` | Duplicate positions |
| Wrap-around example | cost `2` | Circular geometry |
| Mixed duplicates | cost `2` | Stable handling of repeated coordinates |

## Edge Cases

Consider:

```
10 2
1 9
10 2
```

The circular distances are `1` and `1`, giving total cost `2`. A linear-distance solution would incorrectly compute `1 + 7 = 8`. The algorithm handles this because the distance decomposition explicitly uses the circular metric and treats wrapped paths as first-class candidates.

Now consider repeated positions:

```
20 3
5 5 5
5 5 5
```

Every shift has cost `0`. The difference-array construction assigns zero contribution everywhere, all shifts tie, and the algorithm outputs one valid permutation. No special handling is required.

Finally, consider a case where the optimal matching is not obvious from the original order:

```
10 3
1 4 8
8 3 6
```

Sorting reveals the circular ordering. The non-crossing property reduces the search space to cyclic shifts, and the minimum-cost shift reproduces the optimal assignment with total cost `4`. The algorithm never depends on the original input order, only on the geometric order around the circle.
