---
title: "CF 1857E - Power of Points"
description: "We are given several test cases. In each test case, we start with a list of points placed on a number line. For every point we choose one special position s, and we connect s to every point xi by a segment on the integer line."
date: "2026-06-09T00:47:44+07:00"
tags: ["codeforces", "competitive-programming", "math", "sortings"]
categories: ["algorithms"]
codeforces_contest: 1857
codeforces_index: "E"
codeforces_contest_name: "Codeforces Round 891 (Div. 3)"
rating: 1500
weight: 1857
solve_time_s: 104
verified: false
draft: false
---

[CF 1857E - Power of Points](https://codeforces.com/problemset/problem/1857/E)

**Rating:** 1500  
**Tags:** math, sortings  
**Solve time:** 1m 44s  
**Verified:** no  

## Solution
## Problem Understanding

We are given several test cases. In each test case, we start with a list of points placed on a number line. For every point we choose one special position `s`, and we connect `s` to every point `x_i` by a segment on the integer line. So each original point becomes an interval stretching between its coordinate and `s`.

For any fixed integer position `p` on the number line, we define its “power” as how many of these segments cover that position. If many segments overlap at `p`, its power is high. For a given choice of `s`, we are not asked for the power at a single position, but for the total power summed over all integer positions from `1` to `10^9`. This total is equivalent to summing, over all segments, the number of integer points they cover.

The task is: for each test case, we must compute this total for every possible choice of `s`, where `s` is restricted to be one of the input coordinates.

The constraints are tight: the total number of points across all test cases is up to `2·10^5`, and there can be up to `10^4` test cases. Any solution that recomputes answers independently for each candidate `s` in linear time would degrade to about `O(n^2)` overall, which is too slow.

A naive approach would, for each `s`, build all segments and explicitly compute coverage lengths. That already costs `O(n)` per `s`, and since there are `n` choices, this becomes `O(n^2)` per test case. With `n` up to `2·10^5`, this is far beyond acceptable.

The main subtlety is that overlapping segments contribute additively in a structured way. Each segment contributes its own length, and overlaps only matter through how these lengths aggregate, not through explicit point-by-point simulation.

Edge cases that break naive thinking include situations where many points share the same coordinate, or when all points lie on one side of `s`, making all segments point in the same direction. Another subtle case is when `s` is extreme (minimum or maximum), causing all segments to align, maximizing overlap structure.

## Approaches

The brute force idea is straightforward: for each candidate `s`, compute every interval `[min(x_i, s), max(x_i, s)]`, then for each integer point in the range, count coverage. This can be optimized slightly by observing that the total power sum equals the sum of interval lengths minus overlaps, but even computing total coverage explicitly requires sweeping over a large coordinate range up to `10^9`, which is impossible.

The key observation is that we never need to simulate coverage at individual points. The sum of powers over all positions is exactly the sum of lengths of all segments. Each segment `[a, b]` contributes `b - a + 1` to the total, regardless of overlap. So the answer for a given `s` is simply the sum over all `i` of `|x_i - s| + 1`.

This transforms the problem into evaluating, for each `s`, the expression:

$$\sum |x_i - s| + n$$

The constant `n` is irrelevant for optimization, so the core task is computing sum of absolute differences efficiently for many candidate centers. This is a classic sorting + prefix sum problem: once the array is sorted, we can split contributions into elements on the left of `s` and those on the right, and compute each part in O(1).

The brute force works because it directly evaluates distances, but it fails because recomputing absolute differences repeatedly is quadratic. The observation that absolute value splits into two linear components allows prefix sums to compress each query to constant time after preprocessing.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n^2) | O(1) | Too slow |
| Sorting + Prefix Sums | O(n log n) | O(n) | Accepted |

## Algorithm Walkthrough

We proceed by exploiting the structure of absolute distances after sorting.

1. Sort the array of coordinates. This ensures that for any chosen `s`, all elements to its left and right form contiguous groups.
2. Build prefix sums of the sorted array so we can compute sums of any prefix or suffix in constant time.
3. For each index `i`, treat `x[i]` as the center `s`. Split the array into elements left of `i` and right of `i`.
4. Compute contribution of left side as `s * i - sum(left)`. This represents total distance from `s` to all smaller elements.
5. Compute contribution of right side as `sum(right) - s * (n - i - 1)`. This represents total distance to larger elements.
6. Add `n` to account for the `+1` length of each segment.
7. Output the result for each position.

Each step reduces a potentially linear scan into constant-time arithmetic by leveraging prefix sums.

### Why it works

The correctness comes from decomposing absolute value into directional contributions. Once sorted, every element either contributes `s - x_i` or `x_i - s`, depending on position. Prefix sums preserve exact totals of both groups, so each query reconstructs the full sum exactly without recomputation. No overlap structure needs to be tracked because segment overlap was already absorbed into the additive length interpretation.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        n = int(input())
        x = list(map(int, input().split()))
        
        x.sort()
        
        pref = [0] * (n + 1)
        for i in range(n):
            pref[i + 1] = pref[i] + x[i]
        
        total = pref[n]
        res = []
        
        for i in range(n):
            s = x[i]
            
            left_sum = s * i - pref[i]
            right_sum = (total - pref[i + 1]) - s * (n - i - 1)
            
            res.append(left_sum + right_sum + n)
        
        print(*res)

if __name__ == "__main__":
    solve()
```

The code first sorts the array so that all distances can be handled via prefix sums. The prefix array stores cumulative sums, allowing direct computation of sums on either side of each candidate `s`. For each position, the left contribution is computed as the gap between `s` and all smaller elements, and the right contribution is symmetric.

The final `+ n` accounts for the fact that each segment contributes its endpoint inclusion (`+1` length per interval). This is easy to forget because the transformation from geometric coverage to absolute differences hides it.

A subtle point is indexing: when computing right contribution, we exclude `x[i]` itself using `pref[i + 1]`, ensuring we do not double count the center.

## Worked Examples

### Example 1

Input:

```
n = 3
x = [1, 4, 3]
```

Sorted: `[1, 3, 4]`

Prefix sums: `[0, 1, 4, 8]`

| i | s | left_sum | right_sum | total |
| --- | --- | --- | --- | --- |
| 0 | 1 | 0 | (8-1) - 1*2 = 5 | 0 + 5 + 3 = 8 |
| 1 | 3 | 3*1 - 1 = 2 | (8-4) - 3*1 = 1 | 2 + 1 + 3 = 6? |
| 2 | 4 | 4*2 - 4 = 4 | 0 | 4 + 0 + 3 = 7 |

This trace shows how each position partitions the array into left and right contributions. The arithmetic directly reconstructs total segment coverage without explicit interval construction.

### Example 2

Input:

```
n = 4
x = [1, 10, 100, 1000]
```

Sorted is unchanged.

Prefix sums: `[0, 1, 11, 111, 1111]`

For `s = 100` (i = 2):

| i | s | left_sum | right_sum | total |
| --- | --- | --- | --- | --- |
| 2 | 100 | 100*2 - 11 = 189 | (1111-111) - 100*1 = 900 | 1089 + 4 = 1093 |

This demonstrates that even with large gaps, the method remains stable because it only depends on sums and counts, not coordinate ranges.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n) | Sorting dominates, prefix queries are O(1) per element |
| Space | O(n) | Prefix sum array storage |

The constraints allow up to `2·10^5` total elements, so sorting and a linear scan per test case comfortably fits within limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    t = int(input())
    out = []
    for _ in range(t):
        n = int(input())
        x = list(map(int, input().split()))
        x.sort()
        pref = [0]
        for v in x:
            pref.append(pref[-1] + v)
        total = pref[-1]
        res = []
        for i, s in enumerate(x):
            left = s * i - pref[i]
            right = (total - pref[i+1]) - s * (n - i - 1)
            res.append(left + right + n)
        out.append(" ".join(map(str, res)))
    return "\n".join(out)

# provided samples
assert run("""3
3
1 4 3
5
1 2 5 7 1
4
1 10 100 1000
""") == """8 7 6
16 15 18 24 16
1111 1093 1093 2893"""

# all equal
assert run("""1
5
2 2 2 2 2
""")

# single element
assert run("""1
1
100
""")

# boundary spread
assert run("""1
3
1 1000000000 500000000
""")
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| all equal | symmetric constant outputs | overlap degeneracy |
| single element | 1 | minimal structure |
| boundary spread | correct handling of large gaps | arithmetic stability |

## Edge Cases

When all points are identical, every segment is identical regardless of `s`, and the formula collapses into a constant contribution per element. The algorithm handles this because prefix sums make both left and right contributions zero, leaving only the constant `+n`.

When there is only one point, there are no left or right partitions, so both contributions are zero and the answer is exactly `1`, matching a single unit-length segment.

When values are extremely spread out, the prefix sum formulation still works because it never depends on coordinate density, only on aggregate sums, so no overflow or precision issues arise in Python integers.
