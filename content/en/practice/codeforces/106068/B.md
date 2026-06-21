---
title: "CF 106068B - SCPC is Typing..."
description: "We are given a list of positions on a number line, each position representing where a person lives. The goal is to choose one of the given positions as a meeting point so that the sum of walking distances from all people to that chosen point is as small as possible."
date: "2026-06-21T15:57:09+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 106068
codeforces_index: "B"
codeforces_contest_name: "2025 Aleppo and Idlib Private Universities Collegiate Programming Contest (APUCPC 2025)"
rating: 0
weight: 106068
solve_time_s: 44
verified: true
draft: false
---

[CF 106068B - SCPC is Typing...](https://codeforces.com/problemset/problem/106068/B)

**Rating:** -  
**Tags:** -  
**Solve time:** 44s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a list of positions on a number line, each position representing where a person lives. The goal is to choose one of the given positions as a meeting point so that the sum of walking distances from all people to that chosen point is as small as possible. Distance is measured in the standard absolute difference on the line.

Although the problem allows choosing any of the given positions, the cost depends only on how the chosen point balances all values on the number line. Intuitively, if the meeting point is too far left, many points lie to the right and contribute large distances; if it is too far right, the symmetric issue happens.

The input size can be as large as 200,000 values, and each value can be up to 10^9. A quadratic solution that evaluates every candidate meeting point against all others would involve up to 4×10^10 distance computations in the worst case, which is far beyond what can run in two seconds in Python or even optimized compiled code with naive implementation patterns.

A linear or linearithmic approach is required, which strongly suggests that we must avoid recomputing distances from scratch for every candidate.

A subtle point is that the answer is not necessarily unique in value if multiple positions yield the same minimum cost. Since the problem asks to print a position Pi from the array, any valid median-like position is acceptable.

Edge cases that matter here include arrays with repeated values, already sorted arrays, and highly skewed distributions such as one extreme outlier. For example, if input is [1, 1, 1, 100], the optimal meeting point must be 1; a naive intuition might incorrectly consider averaging or midpoint logic, which is irrelevant because we are constrained to choose an existing Pi.

## Approaches

The brute-force idea is straightforward. For each candidate position Pi, compute the sum of absolute differences |Pi − Pj| over all j, then pick the Pi with the smallest sum. This is correct because it directly evaluates the objective function defined by the problem.

However, this approach recomputes an O(N) sum for each of N candidates, resulting in O(N^2) total operations. With N up to 2×10^5, this leads to roughly 4×10^10 operations, which is infeasible.

The key observation is that minimizing sum of absolute deviations on a line is a classic median property. If we sort the array, the point that minimizes the sum of distances is the median element. The reason is structural: moving the meeting point slightly left or right changes contributions from elements on each side in opposite directions, and balance is achieved exactly at the median split.

Since N is odd, the median is a single well-defined element after sorting, specifically the element at index N/2 in zero-based indexing.

This transforms the problem from evaluating all candidates to sorting once and selecting a single position.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(N^2) | O(1) | Too slow |
| Optimal (Median after sorting) | O(N log N) | O(1) or O(N) | Accepted |

## Algorithm Walkthrough

1. Read the array of positions. At this stage, the values are in arbitrary order, so no structural property like ordering or prefix balance is available yet.
2. Sort the array in non-decreasing order. Sorting is essential because the median property only becomes meaningful in an ordered sequence. Without sorting, there is no notion of left half versus right half.
3. Select the element at index N // 2. Since N is odd, this index corresponds to the middle element with exactly the same number of elements on both sides.
4. Output this element as the chosen meeting point. This value is guaranteed to be one of the original positions and is optimal under the absolute distance sum objective.

### Why it works

Consider any candidate point x on the number line. Each point to the left of x contributes a distance that decreases if x moves left, and each point to the right contributes a distance that increases if x moves left. The total cost function is piecewise linear and changes slope depending on how many points lie on either side of x. The slope is negative when fewer than half the points are to the left and positive when fewer than half are to the right. The balance point where neither direction improves the cost is exactly when x is a median. Because N is odd, this balance occurs at a single element in the sorted order, guaranteeing that the median element minimizes the total absolute deviation.

## Python Solution

```python
import sys
input = sys.stdin.readline

def main():
    n = int(input())
    p = list(map(int, input().split()))
    
    p.sort()
    print(p[n // 2])

if __name__ == "__main__":
    main()
```

The solution reads all positions, sorts them, and prints the middle element. The only subtle implementation detail is using integer division n // 2, which correctly selects the median index for zero-based arrays when n is odd. No special handling is needed for duplicates or unsorted input because sorting naturally handles both.

## Worked Examples

### Example 1

Input:

[7, 3, 5, 1, 4]

Sorted array:

[1, 3, 4, 5, 7]

Median index is 2.

| Step | Array state | Chosen index | Chosen value |
| --- | --- | --- | --- |
| Sort | [1, 3, 4, 5, 7] | - | - |
| Pick | [1, 3, 4, 5, 7] | 2 | 4 |

This shows that 4 balances three elements on the left side and one on the right side, producing the minimal total absolute distance.

### Example 2

Input:

[10, 2, 8, 9, 2]

Sorted array:

[2, 2, 8, 9, 10]

Median index is 2.

| Step | Array state | Chosen index | Chosen value |
| --- | --- | --- | --- |
| Sort | [2, 2, 8, 9, 10] | - | - |
| Pick | [2, 2, 8, 9, 10] | 2 | 8 |

Here, 8 minimizes total distance because it splits two values on the left and two on the right, giving optimal balance.

The traces confirm that the solution consistently selects the central balancing point after ordering, which is exactly the median behavior required for minimizing absolute deviations.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(N log N) | Sorting dominates, linear scan afterwards |
| Space | O(1) or O(N) | Depending on in-place sort implementation |

The constraints allow up to 2×10^5 elements, and sorting this size comfortably fits within typical time limits in Python. The rest of the computation is constant-time relative to N, so the solution is efficient.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys as _sys
    from types import SimpleNamespace

    # capture output
    from io import StringIO
    backup = sys.stdout
    sys.stdout = StringIO()

    try:
        main()
        return sys.stdout.getvalue().strip()
    finally:
        sys.stdout = backup

# provided sample
assert run("5\n7 3 5 1 4\n") == "4"

# minimum size
assert run("1\n10\n") == "10"

# all equal
assert run("5\n2 2 2 2 2\n") == "2"

# already sorted
assert run("5\n1 2 3 4 5\n") == "3"

# reverse sorted
assert run("5\n5 4 3 2 1\n") == "3"

# skewed distribution
assert run("5\n1 1 1 1 100\n") == "1"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 element | same value | minimum edge case |
| all equal | that value | stability under duplicates |
| sorted input | middle element | no dependence on input order |
| skewed values | 1 | dominance of median over outlier |

## Edge Cases

For a single element input like [10], sorting keeps it unchanged and selecting index 0 returns 10, which is trivially optimal since no movement is required.

For an all-equal array like [2, 2, 2, 2, 2], sorting does nothing and the median is still 2. Any choice would yield zero total distance, and the algorithm consistently returns a valid optimal point.

For a highly skewed array like [1, 1, 1, 1, 100], sorting gives [1, 1, 1, 1, 100], and the median index is 2, yielding value 1. If one attempted to choose based on averaging or intuition about balancing magnitudes rather than counts, one might incorrectly prefer 100 or something closer to it, but the absolute deviation cost depends only on counts on each side, not distances in value space.
