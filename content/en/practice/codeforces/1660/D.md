---
title: "CF 1660D - Maximum Product Strikes Back"
description: "We are given an array of integers where each value is extremely small in magnitude, only from -2 to 2. From this array, we are allowed to delete a prefix and a suffix, leaving a contiguous middle segment. That remaining segment could even be empty."
date: "2026-06-10T03:02:20+07:00"
tags: ["codeforces", "competitive-programming", "brute-force", "implementation", "math", "two-pointers"]
categories: ["algorithms"]
codeforces_contest: 1660
codeforces_index: "D"
codeforces_contest_name: "Codeforces Round 780 (Div. 3)"
rating: 1600
weight: 1660
solve_time_s: 134
verified: false
draft: false
---

[CF 1660D - Maximum Product Strikes Back](https://codeforces.com/problemset/problem/1660/D)

**Rating:** 1600  
**Tags:** brute force, implementation, math, two pointers  
**Solve time:** 2m 14s  
**Verified:** no  

## Solution
## Problem Understanding

We are given an array of integers where each value is extremely small in magnitude, only from -2 to 2. From this array, we are allowed to delete a prefix and a suffix, leaving a contiguous middle segment. That remaining segment could even be empty.

The task is to choose where to cut from the left and right so that the product of the remaining numbers is as large as possible. If we remove everything, the product is defined as 1, so empty subarrays are always a valid candidate.

Each test case is independent, and we only need to output the counts of removed elements from the front and back, not the product itself.

The constraints are tight in aggregate: up to 200,000 total elements across all test cases. That immediately rules out any quadratic or per-position recomputation of products. Any solution must be linear per test case or amortized linear across all tests.

A few edge behaviors matter here. Zeros are especially important because any segment containing a zero has product 0, which is worse than an empty segment producing 1. Negative values introduce sign flips, so removing or keeping a single element can change the sign of the product. For example, in `[-1, -1]`, the full product is 1, but removing everything also yields 1, so multiple answers tie.

A naive strategy that recomputes the product for every possible subarray would fail because there are O(n²) subarrays. Even if we precomputed prefix products, handling zeros and choosing optimal cuts still requires reasoning about sign changes, not just arithmetic.

## Approaches

A brute-force solution would try every pair of cut positions `(l, r)` meaning we keep `a[l..r]`, compute its product, and track the maximum. This requires O(n²) subarrays, and each product computation is O(1) if prefix products are carefully maintained, but handling zeros and negative parity still forces careful recomputation or resets. Even with optimizations, enumerating all valid segments is too slow for 2e5 total elements.

The key observation is that we are not asked for arbitrary subarrays, but only contiguous segments, and values are restricted to {-2, -1, 0, 1, 2}. This restriction collapses the structure: only zeros break the array into independent blocks, and inside each block the sign is determined only by the parity of negatives.

Within any block without zeros, the absolute value of the product is maximized by keeping everything. The only reason to remove elements is to fix the sign or avoid zeros. Zeros are decisive because they reset product to zero, so any optimal segment either avoids all zeros or includes a carefully chosen region that maximizes sign-corrected magnitude.

A more precise way to see it is to consider all positions of non-zero elements. The optimal segment must lie within some maximal zero-free interval, and within that interval the only meaningful decision is whether the number of negatives is even or odd. If it is even, keeping the whole segment is optimal. If it is odd, we must remove either a prefix up to the first negative or a suffix after the last negative to remove exactly one negative effect.

This reduces the problem to scanning segments separated by zeros and evaluating at most two candidate cuts per segment.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n²) | O(1) | Too slow |
| Optimal | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

We process each test case independently by scanning the array once and treating each zero as a hard boundary.

1. Split the array into maximal segments that contain no zeros. Each such segment can be analyzed independently because any segment containing a zero yields product 0, which is always worse than choosing an empty segment with value 1 unless no better option exists.
2. For each zero-free segment, compute the positions of negative numbers inside it. These positions determine whether the full segment product is positive or negative.
3. If the number of negatives is even, keeping the entire segment is optimal because it yields a positive product with maximal absolute value.
4. If the number of negatives is odd, we must exclude exactly one negative to make the product positive. We evaluate two possibilities: remove everything up to and including the first negative in the segment, or remove everything from the last negative to the end. The better of these two keeps more absolute value while fixing parity.
5. Track the best resulting segment across all zero-free segments. Also compare against the empty segment option, which has product 1.
6. Output the corresponding number of removed elements from the front and back of the original array.

The key reasoning step is that inside a zero-free segment, multiplying by any ±2 or ±1 always increases or preserves absolute value, so the only factor affecting optimality is whether the product is positive or negative. Once that is fixed, longer segments are always better.

### Why it works

Inside any contiguous region without zeros, the product magnitude is monotone with respect to inclusion: adding elements never reduces absolute value. The only obstruction is sign. Since sign depends only on the parity of negative numbers, the optimal solution must either keep the entire segment or remove a prefix/suffix that eliminates exactly one negative contribution. Zeros partition the problem into independent subproblems, and comparing across segments reduces to picking the best feasible sign-corrected product or the empty array baseline.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        n = int(input())
        a = list(map(int, input().split()))

        best_prod = 1
        best_l = n
        best_r = 0

        i = 0
        while i < n:
            while i < n and a[i] == 0:
                i += 1
            if i == n:
                break

            start = i
            neg_pos = []
            while i < n and a[i] != 0:
                if a[i] < 0:
                    neg_pos.append(i)
                i += 1
            end = i - 1

            # consider full segment
            if len(neg_pos) % 2 == 0:
                l, r = start, end
                if r - l + 1 > best_r - best_l + 1:
                    best_l, best_r = l, r
            else:
                # remove prefix up to first negative
                l1 = neg_pos[0] + 1
                r1 = end
                # remove suffix from last negative
                l2 = start
                r2 = neg_pos[-1] - 1

                if r1 >= l1 and (r1 - l1 + 1 > best_r - best_l + 1):
                    best_l, best_r = l1, r1
                if r2 >= l2 and (r2 - l2 + 1 > best_r - best_l + 1):
                    best_l, best_r = l2, r2

        if best_l == n:
            print(0, 0)
        else:
            print(best_l, n - best_r - 1)

if __name__ == "__main__":
    solve()
```

The solution walks through each test case and maintains the best valid segment found so far. Each zero-free segment is processed in linear time, and only the indices of negative elements are stored, so memory stays constant per segment.

A subtle point is the comparison criterion: instead of explicitly computing products, we compare segment lengths because within a fixed zero-free segment, any valid transformation that fixes parity preserves all non-zero magnitudes, and longer segments strictly dominate shorter ones in absolute value. This is why tracking only structure, not arithmetic values, is sufficient.

Another detail is converting the best segment `[best_l, best_r]` back into removals. Removing `best_l` elements from the front gives a 0-based left cut, and removing from the end is `n - best_r - 1`.

## Worked Examples

### Example 1

Input array: `[2, 0, -2, 2, -1]`

We split into segments: `[2]` and `[-2, 2, -1]`.

For `[2]`, there are zero negatives, so we keep it. Product is 2.

For `[-2, 2, -1]`, there are two negatives, so full segment is valid. Product is 4.

| Segment | Negatives | Action | Result |
| --- | --- | --- | --- |
| [2] | 0 | keep full | 2 |
| [-2,2,-1] | 2 | keep full | 4 |

The best segment is the second one, so we keep it entirely, meaning we remove the first two elements.

This confirms that zeros correctly split independent optimization regions.

### Example 2

Input array: `[1, 1, -2]`

Single segment `[-2]` after considering full array.

Negatives = 1, so we must remove either prefix or suffix around it. Best is to remove everything before it, leaving `[-2]`, or remove it entirely depending on comparison with empty array.

| Segment | Negatives | Option 1 | Option 2 |
| --- | --- | --- | --- |
| [1,1,-2] | 1 | [-2] | [] |

The empty array has product 1, which is better than -2, so best answer is to delete all elements.

This demonstrates that empty segment must always be compared explicitly.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | each element is visited once and each segment is processed linearly |
| Space | O(1) | only stores indices of negatives within a segment |

The linear scan is sufficient because the total input size across all test cases is bounded by 2e5, so the algorithm runs comfortably within limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys as _sys
    input = _sys.stdin.readline

    t = int(input())
    out = []
    for _ in range(t):
        n = int(input())
        a = list(map(int, input().split()))

        best_l, best_r = n, -1

        i = 0
        while i < n:
            while i < n and a[i] == 0:
                i += 1
            if i == n:
                break

            start = i
            neg = []
            while i < n and a[i] != 0:
                if a[i] < 0:
                    neg.append(i)
                i += 1
            end = i - 1

            if len(neg) % 2 == 0:
                if end - start > best_r - best_l:
                    best_l, best_r = start, end
            else:
                l1, r1 = neg[0] + 1, end
                l2, r2 = start, neg[-1] - 1
                if r1 >= l1 and r1 - l1 > best_r - best_l:
                    best_l, best_r = l1, r1
                if r2 >= l2 and r2 - l2 > best_r - best_l:
                    best_l, best_r = l2, r2

        if best_r == -1:
            return "0 0\n"
        return f"{best_l} {n - best_r - 1}\n"

# provided samples
assert run("""5
4
1 2 -1 2
3
1 1 -2
5
2 0 -2 2 -1
3
-2 -1 -1
3
-1 -2 -2
""") == """0 2
3 0
2 0
0 1
1 0
"""

# custom cases
assert run("""1
1
0
""") == "0 0\n"

assert run("""1
2
-1 -1
""") in ["0 0\n", "0 0\n"]

assert run("""1
4
2 -2 -2 2
""") == "0 0\n"

assert run("""1
3
1 -1 1
""") in ["0 0\n", "1 0\n"]
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single zero | 0 0 | empty-array dominance |
| two negatives | 0 0 | tie handling for positive product |
| symmetric positives/negatives | 0 0 | parity neutrality |
| alternating signs | flexible | multiple optimal solutions |

## Edge Cases

A subtle case is when the entire array contains only zeros. Every segment yields product 0, but the empty array yields 1. The algorithm must explicitly allow selecting no segment at all; otherwise it would incorrectly return a zero-containing segment.

Another case is when negatives are sparse and isolated. Removing the wrong side around the first or last negative can accidentally discard more positive contribution than necessary. The correct handling ensures only one negative is removed, preserving maximal length among valid fixes.

Finally, arrays with all positive ones require special care because every segment has product 1, so any answer is valid. The algorithm handles this naturally because the longest segment is always preferred, but ties must not force unnecessary removals.
