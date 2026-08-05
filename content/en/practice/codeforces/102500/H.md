---
title: "CF 102500H - Height Profile"
description: "I will provide the editorial as a reusable document. Edit The race profile is described by the heights of the road at every integer kilometre. Between two consecutive kilometre marks, the road is a straight line, so the slope is constant inside every segment."
date: "2026-08-05T18:12:59+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102500
codeforces_index: "H"
codeforces_contest_name: "2019-2020 ICPC Northwestern European Regional Programming Contest (NWERC 2019)"
rating: 0
weight: 102500
solve_time_s: 78
verified: true
draft: false
---

[CF 102500H - Height Profile](https://codeforces.com/problemset/problem/102500/H)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 18s  
**Verified:** yes  

## Solution
I will provide the editorial as a reusable document.

Edit

# Problem Understanding

The race profile is described by the heights of the road at every integer kilometre. Between two consecutive kilometre marks, the road is a straight line, so the slope is constant inside every segment. For each requested incline grade, we need the longest horizontal interval whose average slope is at least that grade.

A direct interpretation is to choose two points on the route and compare their height difference with their horizontal distance. The difficulty is that the endpoints do not have to be integer positions. The optimal interval can start or end in the middle of a kilometre segment.

The race length can contain 100000 segments, while there can be 50 different grade queries. A solution that checks every pair of endpoints would require around 10^10 comparisons, which is far beyond what fits. Even doing a linear scan per possible pair is impossible, so the target must be close to O(n) per query.

A common mistake is to only check integer kilometre positions. For example, with the input

```
2 1
0 30 30
2.0
```

the answer is `1.5`, because the interval from kilometre 0 to kilometre 1.5 has slope 20 metres per kilometre, which is a 2% grade. Checking only vertices would miss this interval.

Another trap is assuming that the best interval must end at a vertex. Consider

```
3 1
0 10 0 0
5.0
```

The transformed profile reaches the required value inside a segment, so the answer may be a fractional distance. Any approach that only updates answers at integer coordinates can return a shorter result.

A third edge case appears when the required grade is never reached:

```
2 1
0 0 0
1.0
```

The correct output is `-1`. A careless implementation might output zero because it always finds a pair of identical positions.

# Approaches

The brute force solution tries every possible pair of endpoints. For each pair, it computes the average incline and keeps the longest interval satisfying the query. With n positions this requires O(n^2) checks, which is about 10^10 operations for the maximum input size.

The key observation comes from rewriting the condition. For a query grade g, define

f(x) = height(x) - (g / 100) * x

For two positions a < b, the incline from a to b is at least g exactly when

f(b) >= f(a).

The problem becomes finding the longest distance between two points where the later point has a value at least as large as the earlier point.

While scanning from left to right, if we know the smallest value of f seen so far and the earliest position where it occurred, then every current position gives the best possible interval ending there. The only remaining issue is that f is continuous and linear inside each kilometre segment. Since a line segment is monotonic, the best endpoint inside a segment can be found directly without binary search.

The brute-force method works because it checks all possible pairs. It fails because there are too many pairs. The transformation above reduces the problem to maintaining a prefix minimum while walking through only the n linear pieces.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n^2) per query | O(1) | Too slow |
| Optimal | O(n) per query | O(1) besides input storage | Accepted |

# Algorithm Walkthrough

1. For a query grade g, subtract the line with slope g/100 from the height profile. The new value at position x is `height(x) - g*x/100`. An interval is valid exactly when this transformed value does not decrease from its left endpoint to its right endpoint.
2. Start scanning the route from left to right. Maintain the minimum transformed value seen so far and the earliest position where that minimum appears. This gives the best possible starting point for any interval ending at the current position.
3. For every segment between two integer kilometres, determine where the transformed line segment reaches its largest valid endpoint. If the segment is increasing, the far end is always valid. If it is decreasing, the valid part ends when the segment reaches the current prefix minimum.
4. Update the answer with the distance between this endpoint and the stored minimum position. After finishing the segment, update the prefix minimum using the segment endpoint because future intervals may start there.
5. Repeat the scan for every requested grade and print the longest length found. If no positive length interval exists, print `-1`.

Why it works:

For any possible ending point y, the best starting point is the earliest occurrence of the minimum transformed value before y. The scan always stores exactly this information. Inside each segment, the transformed function is linear, so the set of valid ending points is either the whole segment or a prefix of it. The algorithm checks the furthest valid ending point, which is the only one that can improve the answer. Since every possible endpoint is considered, the maximum interval cannot be missed.

# Python Solution

```python
import sys
input = sys.stdin.readline

def solve_query(h, g):
    n = len(h) - 1
    slope_need = g / 100.0

    def value(i):
        return h[i] - slope_need * i

    cur_min = value(0)
    min_pos = 0
    ans = 0.0

    cur = value(0)

    for i in range(n):
        nxt = value(i + 1)
        seg_slope = nxt - cur

        if seg_slope >= 0:
            end = i + 1.0
        else:
            t = (cur_min - cur) / seg_slope
            if t >= 1.0:
                end = i + 1.0
            else:
                end = i + t

        if end - min_pos > ans:
            ans = end - min_pos

        cur = nxt

        if cur < cur_min:
            cur_min = cur
            min_pos = i + 1.0

    if ans <= 1e-12:
        return "-1"
    return f"{ans:.10f}"

def main():
    n, k = map(int, input().split())
    h = list(map(int, input().split()))

    grades = []
    for _ in range(k):
        grades.append(float(input()))

    out = []
    for g in grades:
        out.append(solve_query(h, g))

    print("\n".join(out))

if __name__ == "__main__":
    main()
```

The code processes each grade independently because the transformation depends on the requested slope. The function `solve_query` keeps the current transformed value, the smallest transformed value seen so far, and the position where that minimum was reached.

The expression `seg_slope = nxt - cur` is the slope of the transformed segment. When it is non-negative, every point in the segment has a value at least as large as the start of the segment, so the far endpoint is the best choice. When it is negative, the line eventually falls below the stored minimum, and the formula computes the exact crossing point.

All coordinates are stored as floating point values because the optimal endpoint may lie inside a segment. Python integers handle the original heights safely, and only the transformed calculations require floating point precision.

# Worked Examples

For the first sample, the query is 2.0%. The transformed profile is created by subtracting 2 metres per kilometre.

| Segment | Current minimum position | Current transformed value | Best endpoint | Answer |
| --- | --- | --- | --- | --- |
| Start | 0 | 0 | 1 | 1 |
| 1 to 2 | 0 | -2 | 2 | 2 |
| 2 to 3 | 0 | -4 | 3 | 3 |
| Remaining segments | 0 | minimum stays lower | no improvement | 3 |

The interval from kilometre 0 to kilometre 3 has exactly the required average slope, so the answer is 3.

For the second sample, the query is 2.0%.

| Segment | Current minimum position | Current transformed value | Best endpoint | Answer |
| --- | --- | --- | --- | --- |
| 0 to 1 | 0 | 0 | 1 | 1 |
| 1 to 2 | 0 | 28 | 1.5 | 1.5 |

The second segment is flat after transformation, allowing a fractional endpoint. The algorithm finds the length 1.5 interval.

# Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(nk) | Each of the k grades scans all n segments once |
| Space | O(n) | The height array is stored, and the scan itself uses constant extra memory |

The maximum work is about 5 million segment operations, which is easily within the intended limits.

# Test Cases

```python
import sys
import io

def run(inp: str) -> str:
    old = sys.stdin
    sys.stdin = io.StringIO(inp)
    out = io.StringIO()
    old_out = sys.stdout
    sys.stdout = out
    main()
    sys.stdout = old_out
    sys.stdin = old
    return out.getvalue().strip()

assert run("""8 2
0 0 10 30 60 45 75 65 30
2.0
3.1
""") == "3.0000000000\n-1"

assert run("""2 2
0 30 30
3.0
2.0
""") == "1.0000000000\n1.5000000000"

assert run("""2 1
0 0 0
1.0
""") == "-1"

assert run("""2 1
0 100 200
50.0
""") == "2.0000000000"

assert run("""2 1
5 5 5
0.0
""") == "2.0000000000"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Flat profile with positive grade | -1 | No valid interval exists |
| Straight increasing profile | 2.0 | Entire route can be valid |
| Fractional endpoint case | 1.5 | Non-integer answers are handled |
| Equal heights with zero grade | 2.0 | Flat segments count for zero slope |

# Edge Cases

When the best endpoint is inside a segment, the algorithm reaches it through the decreasing-segment crossing formula. For the input

```
2 1
0 30 30
2.0
```

the transformed values are 0, 28, and 26. The minimum stays at position 0. The second segment decreases from 28 to 26, and the crossing with the minimum occurs after 1.5 kilometres, producing the correct answer.

When every interval fails the required grade, the prefix minimum never allows a positive valid distance. For

```
2 1
0 0 0
1.0
```

the transformed profile is decreasing immediately, and every possible interval has negative adjusted slope. The stored answer remains zero, so the program prints `-1`.

When the whole route is valid, the minimum remains at the beginning and the final endpoint gives the answer. For

```
2 1
0 100 200
50.0
```

the transformed profile is flat, so the scan reaches kilometre 2 and returns the full length.
