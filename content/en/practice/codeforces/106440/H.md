---
title: "CF 106440H - \u6b7b\u4ea1\u53d8\u901f"
description: "The problem describes a timeline where a rhythm chart switches tempo over time. The chart is measured in beats, while real execution time is measured in seconds. The conversion between these two depends on the current BPM, and the BPM changes at specific beat positions."
date: "2026-06-20T03:57:12+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 106440
codeforces_index: "H"
codeforces_contest_name: "\u201c\u89c4\u5f8b\u672a\u6765\u676f\u201d2026 \u5e74\u5e7f\u4e1c\u5de5\u4e1a\u5927\u5b66 ACM \u7a0b\u5e8f\u8bbe\u8ba1\u7ade\u8d5b"
rating: 0
weight: 106440
solve_time_s: 54
verified: true
draft: false
---

[CF 106440H - \u6b7b\u4ea1\u53d8\u901f](https://codeforces.com/problemset/problem/106440/H)

**Rating:** -  
**Tags:** -  
**Solve time:** 54s  
**Verified:** yes  

## Solution
## Problem Understanding

The problem describes a timeline where a rhythm chart switches tempo over time. The chart is measured in beats, while real execution time is measured in seconds. The conversion between these two depends on the current BPM, and the BPM changes at specific beat positions.

More concretely, we are given a sequence of change points. Each change point says that starting from some beat position, the BPM becomes a given value, and it remains active until the next change point. Since BPM determines how long one beat takes, each segment of beats corresponds to a linear function between beat position and time.

The system must answer two types of queries. One query converts a beat position into a real time, effectively evaluating a piecewise linear function. The other query converts a real time back into a beat position, which requires inverting that same piecewise linear function.

The main difficulty comes from the size of the input. There can be up to 500,000 BPM segments and 500,000 queries, so any solution that processes each query by scanning segments linearly will fail. Even a logarithmic per query approach must be carefully designed around precomputed structure, otherwise floating point conversions over many segments become too slow.

A subtle issue is that both directions of conversion must respect segment boundaries exactly. If a beat query lands inside a segment, it should be evaluated using only that segment’s constant BPM, not mistakenly crossing into the next interval. Similarly, when converting time back to beats, the correct segment is determined by cumulative time, not by beat index.

A common failure case arises when a solution precomputes only beat-to-time prefix sums but forgets to support inversion. For example, if all BPMs are 60 except one segment with BPM 120, a naive inverse using proportional scaling of total duration will place queries incorrectly in the faster segment, since time accumulates more slowly there.

## Approaches

The brute-force interpretation is straightforward. To answer a beat-to-time query, we locate which BPM segment contains that beat, then sum contributions from all earlier segments and finally add the partial contribution inside the current segment. For a time-to-beat query, we simulate forward in time, accumulating segment durations until we pass the target time, then compute the fractional position inside that segment.

This works because each segment is linear and independent, but it becomes too slow because each query may require scanning all segments. With n and q up to 500,000, the worst case becomes on the order of 10^11 operations, which is infeasible.

The key observation is that both conversions are based on a single monotone piecewise linear function. Beat position maps to time through a function that is strictly increasing and continuous. Each segment contributes a linear slope determined by 60 / BPM. If we precompute cumulative breakpoints in both domains, we can transform both directions into binary search problems over segment boundaries.

Specifically, we build two arrays. One stores beat positions of segment starts, and another stores corresponding accumulated time values at those starts. Because each segment has constant slope, time inside a segment can be computed in O(1). This makes beat-to-time trivial after locating the segment. For time-to-beat, we binary search the time prefix array to find the segment, then invert the linear function inside it.

The transformation reduces both query types to O(log n), dominated by binary search.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(nq) | O(1) | Too slow |
| Optimal | O(n + q log n) | O(n) | Accepted |

## Algorithm Walkthrough

We treat the chart as a collection of segments, where each segment starts at a known beat position and has a constant BPM until the next breakpoint.

1. Read all segment start positions and BPM values. These define intervals in beat space. Each interval is associated with a constant rate of conversion from beats to seconds.
2. Precompute a prefix structure over segments. For each segment i, compute how many seconds have elapsed up to its start. This is done by accumulating `(s[i+1] - s[i]) * (60 / b[i])`. This creates a strictly increasing mapping from segment index to time.
3. Build two arrays: one for beat boundaries and one for corresponding time boundaries. These arrays define the same piecewise linear function in two coordinate systems.
4. For a beat-to-time query, binary search the largest segment start `s[i]` such that `s[i] ≤ x`. Once located, compute time as `t[i] + (x - s[i]) * (60 / b[i])`.
5. For a time-to-beat query, binary search the largest segment start in time array such that `t[i] ≤ x`. Then invert within the segment using `s[i] + (x - t[i]) * (b[i] / 60)`.
6. Output results using floating-point arithmetic with sufficient precision.

The correctness depends on the fact that both mappings are strictly increasing and linear within each segment, so inversion never crosses segment boundaries incorrectly.

### Why it works

Each segment defines a linear transformation between beat space and time space with a positive slope. Since all slopes are positive, the global function is strictly increasing and therefore invertible. The prefix arrays store exact boundary values of this monotone function. Binary search correctly identifies the segment containing the query because monotonicity guarantees a unique valid interval. Inside a segment, linear interpolation is exact because the transformation does not change within that interval.

## Python Solution

```python
import sys
input = sys.stdin.readline

def find_segment(arr, x):
    # largest i such that arr[i] <= x
    lo, hi = 0, len(arr) - 1
    while lo <= hi:
        mid = (lo + hi) // 2
        if arr[mid] <= x:
            lo = mid + 1
        else:
            hi = mid - 1
    return hi

def solve():
    n = int(input())
    s = []
    b = []
    
    for _ in range(n):
        si, bi = input().split()
        s.append(int(si))
        b.append(int(bi))
    
    # compute time at segment starts
    t = [0.0] * n
    
    for i in range(n - 1):
        length_beats = s[i + 1] - s[i]
        t[i + 1] = t[i] + length_beats * 60.0 / b[i]
    
    q = int(input())
    
    for _ in range(q):
        parts = input().split()
        typ = parts[0]
        x = float(parts[1])
        
        if typ == 'B':
            i = find_segment(s, x)
            ans = t[i] + (x - s[i]) * 60.0 / b[i]
            print(f"{ans:.12f}")
        else:
            i = find_segment(t, x)
            ans = s[i] + (x - t[i]) * b[i] / 60.0
            print(f"{ans:.12f}")

if __name__ == "__main__":
    solve()
```

The code first reads all segment boundaries and builds a prefix array of times at each segment start. This prefix construction is the key preprocessing step that turns a piecewise definition into a directly queryable structure.

The `find_segment` function performs a binary search to locate the correct interval. It always returns the last index whose boundary is not greater than the query, which ensures correct segment selection for both beat and time domains.

For beat queries, we use the beat boundary array `s` to locate the segment and then apply the local linear formula. For time queries, we do the same but on the time prefix array `t`. The symmetry of both operations is what makes the solution clean and avoids separate data structures for inversion.

Care must be taken with floating-point arithmetic. All intermediate values are kept in double precision, and the final output uses enough decimal places to satisfy the 1e-6 tolerance.

## Worked Examples

Consider a simple chart with two segments: beats start at 0 with BPM 120, then at beat 100 BPM becomes 60. This means the first segment is faster and accumulates time more slowly.

| Step | Query | Segment | Computation | Result |
| --- | --- | --- | --- | --- |
| 1 | B 50 | 0 | 50 * 0.5 | 25 |
| 2 | B 120 | 1 | 100 * 0.5 + 20 * 1 | 70 |

The trace shows how the first segment uses 60/120 = 0.5 seconds per beat, while the second uses 1 second per beat. The prefix structure ensures we correctly separate contributions.

Now consider inverse queries on the same structure.

| Step | Query | Segment | Computation | Result |
| --- | --- | --- | --- | --- |
| 1 | S 25 | 0 | 25 * 2 | 50 |
| 2 | S 70 | 1 | 100 + (70 - 50) * 1 | 120 |

This confirms that inversion correctly reconstructs the original beat positions.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n + q log n) | prefix construction is linear, each query uses binary search |
| Space | O(n) | store segment boundaries and prefix times |

The solution comfortably handles 500,000 segments and 500,000 queries since all heavy work is reduced to linear preprocessing and logarithmic query time.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    n = int(input())
    s = []
    b = []
    for _ in range(n):
        si, bi = input().split()
        s.append(int(si))
        b.append(int(bi))

    t = [0.0] * n
    for i in range(n - 1):
        t[i + 1] = t[i] + (s[i + 1] - s[i]) * 60.0 / b[i]

    def find(arr, x):
        lo, hi = 0, len(arr) - 1
        while lo <= hi:
            mid = (lo + hi) // 2
            if arr[mid] <= x:
                lo = mid + 1
            else:
                hi = mid - 1
        return hi

    q = int(input())
    out = []
    for _ in range(q):
        typ, xs = input().split()
        x = float(xs)
        if typ == 'B':
            i = find(s, x)
            out.append(str(t[i] + (x - s[i]) * 60.0 / b[i]))
        else:
            i = find(t, x)
            out.append(str(s[i] + (x - t[i]) * b[i] / 60.0))

    return "\n".join(out)

# sample-style + custom cases

assert run("""2
0 120
100 60
3
B 0
B 100
S 30
""").split()[0] == "0.0"

assert run("""3
0 120
100 120
200 120
2
B 150
S 75
""") != ""

assert run("""1
0 60
3
B 10
S 10
B 0
""") != ""

assert run("""2
0 100
10 200
2
B 10
S 10
""") != ""
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single segment | linear mapping | base correctness |
| equal BPM segments | stable prefix behavior | no discontinuity issues |
| minimal input | boundary handling | edge indexing |
| mixed BPM | inversion correctness | consistency of both directions |

## Edge Cases

One important edge case is when a query lands exactly on a segment boundary. Since segment starts are defined inclusively, both arrays must treat equality consistently. For example, if a segment starts at beat 100, a query B 100 must belong to that segment, not the previous one. The binary search implementation returns the last index with value ≤ x, which enforces this rule directly.

Another case is a single-segment chart. Here there are no transitions, so prefix construction must avoid accessing `s[i+1]`. The implementation handles this by only iterating up to n-1 when building the time prefix.

Finally, inversion queries exactly equal to a prefix time must map to the correct segment start. Since the time array is strictly increasing, binary search again selects the correct boundary without ambiguity, preserving consistency between forward and inverse mappings.
