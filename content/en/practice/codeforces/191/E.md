---
title: "CF 191E - Thwarting Demonstrations"
description: "We have an array of soldier reliabilities. Every contiguous subarray represents one possible police group. The general always chooses the strongest unused group first, meaning all subarray sums are sorted in descending order and picked one by one."
date: "2026-05-29T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "binary-search", "data-structures", "trees"]
categories: ["algorithms"]
codeforces_contest: 191
codeforces_index: "E"
codeforces_contest_name: "Codeforces Round 121 (Div. 1)"
rating: 2200
weight: 191
solve_time_s: 106
verified: true
draft: false
---

[CF 191E - Thwarting Demonstrations](https://codeforces.com/problemset/problem/191/E)

**Rating:** 2200  
**Tags:** binary search, data structures, trees  
**Solve time:** 1m 46s  
**Verified:** yes  

## Solution
## Problem Understanding

We have an array of soldier reliabilities. Every contiguous subarray represents one possible police group. The general always chooses the strongest unused group first, meaning all subarray sums are sorted in descending order and picked one by one.

We need the reliability of the group chosen on day `k`. In other words, among all `n(n+1)/2` subarray sums, we must find the `k`-th largest value.

The array may contain negative numbers, so longer subarrays are not always better. A maximum-sum subarray technique alone is not enough because we need the entire ranking of subarray sums, not only the best one.

The constraints are what force the real difficulty here. The number of subarrays is quadratic, roughly `n^2 / 2`. For `n = 10^5`, this becomes about `5 * 10^9` subarrays, far too many to enumerate explicitly. Even storing all sums would require tens of gigabytes of memory. Any solution around `O(n^2)` is immediately impossible.

The time limit is generous at 6 seconds, which usually signals that an `O(n log^2 n)` or `O(n log n)` solution with advanced data structures is expected.

The tricky part is that we are not asked to construct the top `k` sums directly. The correct approach is to binary search the answer and repeatedly count how many subarrays have sum at least some threshold `x`.

Several edge cases silently break naive implementations.

Consider an array where all numbers are negative.

Input:

```
3 2
-5 -2 -7
```

All subarray sums are:

`[-5, -7, -14, -2, -9, -7]`

Sorted descending:

`[-2, -5, -7, -7, -9, -14]`

The answer is `-5`.

A careless implementation that assumes larger subarrays are always stronger would fail immediately.

Another subtle case appears with duplicate sums.

Input:

```
3 4
1 1 1
```

Subarray sums are:

`[1,2,3,1,2,1]`

Sorted descending:

`[3,2,2,1,1,1]`

The 4th largest value is `1`.

If we binary search for the first value with count strictly greater than `k`, instead of greater than or equal to `k`, duplicates produce off-by-one errors.

Large values also matter.

Input:

```
2 1
1000000000 1000000000
```

The best subarray sum is `2000000000`.

Using 32-bit integers overflows here. Python handles this automatically, but in lower-level languages this requires 64-bit arithmetic everywhere.

## Approaches

The brute-force idea is straightforward. Generate every contiguous subarray, compute its sum, store all sums in a list, sort the list descending, and take the `k`-th element.

Prefix sums reduce subarray-sum computation from `O(length)` to `O(1)`, so generating all sums costs `O(n^2)`. Sorting then costs `O(n^2 log n)`.

This works for small arrays, but for `n = 10^5` the number of subarrays is about five billion. Even iterating over them once is impossible.

The key observation is that we do not actually need the exact ordering of all sums. We only need one value, the `k`-th largest. Problems of this form often become much easier if we can answer the question:

"How many subarrays have sum at least `x`?"

Suppose we can compute this count efficiently. Then binary search becomes possible.

If at least `k` subarrays have sum at least `x`, then the answer is at least `x`.

If fewer than `k` subarrays reach `x`, then `x` is too large.

Now the task becomes counting subarrays with sum at least `x`.

Let prefix sums be:

`pref[i] = a[1] + ... + a[i]`

A subarray `(l, r)` has sum:

`pref[r] - pref[l-1]`

We want:

`pref[r] - pref[l-1] >= x`

Rearranging:

`pref[l-1] <= pref[r] - x`

So while scanning prefixes from left to right, for each `pref[r]` we need the number of earlier prefix sums not exceeding `pref[r] - x`.

This is a classic order-statistics problem.

Because prefix sums can be very large and negative, we coordinate-compress them and use a Fenwick tree to maintain frequencies of previous prefix sums.

Each counting pass costs `O(n log n)`. Binary search over the answer range adds another logarithmic factor.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n² log n) | O(n²) | Too slow |
| Optimal | O(n log² n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Build prefix sums.

Define:

`pref[0] = 0`

and:

`pref[i] = pref[i-1] + a[i]`

Every subarray sum can now be written as a difference of two prefix sums.
2. Binary search the answer.

The smallest possible subarray sum is at least `-10^14`, and the largest is at most `10^14`, because `n ≤ 10^5` and `|a[i]| ≤ 10^9`.

We binary search for the largest value `x` such that at least `k` subarrays have sum at least `x`.
3. For a fixed threshold `x`, count valid subarrays.

For each position `r`, we need the number of earlier indices `l-1` satisfying:

`pref[l-1] <= pref[r] - x`

This becomes a prefix-frequency query.
4. Coordinate-compress all prefix sums.

Fenwick trees work on indices, not arbitrary large integers.

Collect all prefix sums, sort them, and remove duplicates.
5. Scan prefixes from left to right.

Initially insert `pref[0]`.

For each `pref[r]`:

Find how many inserted prefix sums are `<= pref[r] - x`.

Add this count to the answer.

Then insert `pref[r]` into the Fenwick tree.
6. Use the count result inside binary search.

If the count is at least `k`, then `x` is feasible and we try larger values.

Otherwise, `x` is too large and we search smaller values.
7. After binary search finishes, output the largest feasible value.

### Why it works

For every right endpoint `r`, the algorithm counts exactly the left endpoints producing subarray sums at least `x`. Every valid subarray corresponds to one pair of prefix sums satisfying:

`pref[r] - pref[l-1] >= x`

The Fenwick tree maintains all earlier prefix sums, so every subarray is counted exactly once.

Binary search is valid because feasibility is monotonic. If at least `k` subarrays have sum at least `x`, then the same is true for every smaller threshold. This monotonicity guarantees that binary search converges to the exact `k`-th largest subarray sum.

## Python Solution

```python
import sys
from bisect import bisect_right

input = sys.stdin.readline

class Fenwick:
    def __init__(self, n):
        self.n = n
        self.bit = [0] * (n + 1)

    def add(self, idx, val):
        while idx <= self.n:
            self.bit[idx] += val
            idx += idx & -idx

    def sum(self, idx):
        res = 0
        while idx > 0:
            res += self.bit[idx]
            idx -= idx & -idx
        return res

def solve():
    n, k = map(int, input().split())
    a = list(map(int, input().split()))

    pref = [0]
    for x in a:
        pref.append(pref[-1] + x)

    coords = sorted(set(pref))

    def count_ge(x):
        fw = Fenwick(len(coords))
        total = 0

        pos0 = bisect_right(coords, pref[0])
        fw.add(pos0, 1)

        for i in range(1, n + 1):
            need = pref[i] - x

            cnt = bisect_right(coords, need)
            total += fw.sum(cnt)

            pos = bisect_right(coords, pref[i])
            fw.add(pos, 1)

        return total

    lo = -10**15
    hi = 10**15

    while lo < hi:
        mid = (lo + hi + 1) // 2

        if count_ge(mid) >= k:
            lo = mid
        else:
            hi = mid - 1

    print(lo)

solve()
```

The first section computes prefix sums so every subarray sum becomes a difference of two values. This is the core transformation that makes counting possible.

The Fenwick tree stores frequencies of previously seen prefix sums. Since prefix sums can be negative and extremely large, coordinate compression maps them into a compact index range.

The function `count_ge(x)` performs the counting step for binary search. For each current prefix sum `pref[i]`, it counts how many earlier prefix sums satisfy:

```
pref[j] <= pref[i] - x
```

The call to `bisect_right` is subtle but critical. We need values less than or equal to the threshold, not strictly less. Using `bisect_left` here produces incorrect answers when duplicate prefix sums exist.

The binary search looks for the largest feasible value. The midpoint formula:

```
mid = (lo + hi + 1) // 2
```

avoids infinite loops by biasing upward.

The search range uses `±10^15`, safely covering every possible subarray sum.

## Worked Examples

### Example 1

Input:

```
3 4
1 4 2
```

All subarray sums are:

`[1,5,7,4,6,2]`

Sorted descending:

`[7,6,5,4,2,1]`

The answer is `4`.

Suppose binary search checks `x = 4`.

Prefix sums:

`[0,1,5,7]`

| i | pref[i] | need = pref[i] - 4 | Earlier pref ≤ need | Count added |
| --- | --- | --- | --- | --- |
| 1 | 1 | -3 | 0 | 0 |
| 2 | 5 | 1 | 2 | 2 |
| 3 | 7 | 3 | 2 | 2 |

Total valid subarrays: `4`.

Since at least `4` subarrays have sum at least `4`, the answer is at least `4`.

This trace demonstrates the core counting invariant. At each step, the Fenwick tree contains exactly the earlier prefix sums.

### Example 2

Input:

```
3 2
-5 -2 -7
```

Sorted subarray sums:

`[-2,-5,-7,-7,-9,-14]`

The answer is `-5`.

Suppose binary search checks `x = -5`.

Prefix sums:

`[0,-5,-7,-14]`

| i | pref[i] | need | Earlier pref ≤ need | Count added |
| --- | --- | --- | --- | --- |
| 1 | -5 | 0 | 1 | 1 |
| 2 | -7 | -2 | 1 | 1 |
| 3 | -14 | -9 | 0 | 0 |

Total valid subarrays: `2`.

Exactly two subarrays have sum at least `-5`.

This example shows why negative values must be handled carefully. The algorithm never assumes positivity.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log² n) | Binary search performs O(log range) iterations, each counting pass costs O(n log n) |
| Space | O(n) | Prefix sums, compressed coordinates, and Fenwick tree |

The logarithm of the numeric range is about 50 because subarray sums fit within roughly `[-10^14, 10^14]`. With `n = 10^5`, the total number of Fenwick operations remains well within the time limit.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io
from bisect import bisect_right

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    input = sys.stdin.readline

    class Fenwick:
        def __init__(self, n):
            self.n = n
            self.bit = [0] * (n + 1)

        def add(self, idx, val):
            while idx <= self.n:
                self.bit[idx] += val
                idx += idx & -idx

        def sum(self, idx):
            res = 0
            while idx > 0:
                res += self.bit[idx]
                idx -= idx & -idx
            return res

    n, k = map(int, input().split())
    a = list(map(int, input().split()))

    pref = [0]
    for x in a:
        pref.append(pref[-1] + x)

    coords = sorted(set(pref))

    def count_ge(x):
        fw = Fenwick(len(coords))
        total = 0

        fw.add(bisect_right(coords, pref[0]), 1)

        for i in range(1, n + 1):
            need = pref[i] - x
            total += fw.sum(bisect_right(coords, need))
            fw.add(bisect_right(coords, pref[i]), 1)

        return total

    lo = -10**15
    hi = 10**15

    while lo < hi:
        mid = (lo + hi + 1) // 2

        if count_ge(mid) >= k:
            lo = mid
        else:
            hi = mid - 1

    return str(lo) + "\n"

# provided sample
assert run(
"""3 4
1 4 2
"""
) == "4\n", "sample 1"

# minimum size
assert run(
"""1 1
5
"""
) == "5\n", "single element"

# all negative
assert run(
"""3 2
-5 -2 -7
"""
) == "-5\n", "all negative"

# duplicate sums
assert run(
"""3 4
1 1 1
"""
) == "1\n", "duplicate sums"

# off-by-one around ranking
assert run(
"""2 2
5 -1
"""
) == "4\n", "ranking boundary"

# large values
assert run(
"""2 1
1000000000 1000000000
"""
) == "2000000000\n", "64-bit range"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 1 / 5` | `5` | Minimum-size input |
| `3 2 / -5 -2 -7` | `-5` | All-negative handling |
| `3 4 / 1 1 1` | `1` | Duplicate subarray sums |
| `2 2 / 5 -1` | `4` | Correct k-th ranking |
| `2 1 / 1e9 1e9` | `2000000000` | Large integer handling |

## Edge Cases

Consider again the all-negative case.

Input:

```
3 2
-5 -2 -7
```

Prefix sums become:

`[0,-5,-7,-14]`

When checking `x = -5`, the algorithm counts exactly two valid subarrays:

`[-5]` and `[-2]`.

The Fenwick tree logic still works because it only compares prefix sums. No assumption about positivity appears anywhere.

Now consider duplicate sums.

Input:

```
3 4
1 1 1
```

Subarray sums sorted descending:

`[3,2,2,1,1,1]`

The answer is `1`.

During counting, multiple prefix sums may map to the same compressed coordinate. Using `bisect_right` guarantees that all equal values are included in the query. Replacing it with `bisect_left` incorrectly excludes equal prefix sums and undercounts the number of valid subarrays.

Finally, consider a ranking boundary case.

Input:

```
2 2
5 -1
```

Subarray sums are:

`[5,4,-1]`

The second-largest sum is `4`.

Binary search checks whether at least two subarrays reach a threshold. At `x = 4`, the count is exactly two:

`[5]` and `[5,-1]`.

At `x = 5`, only one subarray qualifies.

This demonstrates why the binary search condition must be:

```
count >= k
```

Using `count > k` would incorrectly move past the correct answer.
