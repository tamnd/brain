---
title: "CF 106063K - Kilometric Intersection"
description: "The problem asks us to measure how much two road segments on a number line overlap. Each segment is a closed interval, so it includes both endpoints, but the answer is based on length, meaning a single touching point contributes zero."
date: "2026-06-25T12:15:30+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 106063
codeforces_index: "K"
codeforces_contest_name: "2025 ICPC Gran Premio de Mexico 3ra Fecha"
rating: 0
weight: 106063
solve_time_s: 34
verified: true
draft: false
---

[CF 106063K - Kilometric Intersection](https://codeforces.com/problemset/problem/106063/K)

**Rating:** -  
**Tags:** -  
**Solve time:** 34s  
**Verified:** yes  

## Solution
## Problem Understanding

The problem asks us to measure how much two road segments on a number line overlap. Each segment is a closed interval, so it includes both endpoints, but the answer is based on length, meaning a single touching point contributes zero. Given two intervals `[a, b]` and `[c, d]`, we need to output the length of their common part, or zero when the common part has no positive length.

The input contains many independent test cases. The number of cases can reach `10^5`, and coordinates can be as large as `10^18` in absolute value. This immediately rules out anything more than constant or logarithmic work per case, because `10^5` cases only leave room for roughly a few million simple operations. The coordinate size also means the implementation must use integer arithmetic that can handle 64-bit values.

The main edge cases come from confusing intersection as a set of points with intersection as a length. For example:

```
1
0 1 1 2
```

The intervals meet at coordinate `1`, but the common part is only the point `{1}`. Its length is zero, so the answer is:

```
0
```

A solution that only checks whether the intervals overlap might incorrectly return `1`.

Another case is when one interval is completely inside another:

```
1
0 10 3 7
```

The intersection is `[3,7]`, whose length is `4`. A careless implementation that only checks one endpoint can miss this situation.

A final tricky case is when both intervals are points:

```
1
5 5 5 5
```

The intervals are identical, but their length is still zero because there is no distance between the endpoints.

## Approaches

The direct approach is to compare the intervals and find every possible overlap situation. We could check whether one interval starts inside the other, whether one contains the other, or whether they are disjoint. This works because every possible relationship between two intervals falls into one of these categories. However, this creates unnecessary branching and is easy to get wrong around touching endpoints.

The structure of intervals gives us a simpler observation. The left boundary of the intersection must be the later of the two left endpoints, because both intervals must have reached that coordinate. Similarly, the right boundary must be the earlier of the two right endpoints. If the resulting left boundary is smaller than the right boundary, there is a positive-length intersection. Otherwise, the intersection has length zero.

The brute force style of case analysis works in constant time too, but the minimum and maximum observation reduces the logic to a single formula. The problem is not about searching or simulation, it is only about identifying the two boundaries of the shared region.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(1) | O(1) | Accepted, but easier to make mistakes |
| Optimal | O(1) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the four endpoints of the two intervals.

We only need the endpoints because the intersection of two intervals is completely determined by their boundaries.
2. Compute the left side of the intersection as `max(a, c)`.

Any point in the intersection must belong to both intervals, so it cannot be before either interval begins.
3. Compute the right side of the intersection as `min(b, d)`.

Any point in the intersection must end before either interval ends.
4. If the left side is smaller than the right side, output the difference between them. Otherwise output zero.

Strict inequality is required because equal boundaries mean the intersection is only a single point.

Why it works: the algorithm maintains the exact possible range where both intervals can simultaneously contain a point. The maximum starting point removes every position that is unavailable in one of the intervals, and the minimum ending point removes every position that is outside one of the intervals. The remaining segment is precisely the intersection. If it has no positive width, its length is zero.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    ans = []

    for _ in range(t):
        a, b, c, d = map(int, input().split())

        left = max(a, c)
        right = min(b, d)

        if left < right:
            ans.append(str(right - left))
        else:
            ans.append("0")

    print("\n".join(ans))

if __name__ == "__main__":
    solve()
```

The solution reads all test cases and processes each one independently. The variables `left` and `right` represent the only two values needed to describe the intersection.

The comparison uses `<` instead of `<=`. This handles the endpoint-touching case correctly, because an intersection like `[2,2]` has zero length. Python integers have arbitrary precision, so the large coordinates do not require any special handling.

## Worked Examples

For the input:

```
3 7 1 5
```

the execution looks like this:

| Step | left | right | action |
| --- | --- | --- | --- |
| Initial intervals | - | - | `[3,7]` and `[1,5]` |
| Find intersection start | 3 | - | max(3,1) |
| Find intersection end | 3 | 5 | min(7,5) |
| Final check | 3 | 5 | output 5-3 = 2 |

The intersection is `[3,5]`, so the answer is `2`. This demonstrates the normal overlapping case.

For the input:

```
0 1 1 2
```

the execution is:

| Step | left | right | action |
| --- | --- | --- | --- |
| Initial intervals | - | - | `[0,1]` and `[1,2]` |
| Find intersection start | 1 | - | max(0,1) |
| Find intersection end | 1 | 1 | min(1,2) |
| Final check | 1 | 1 | output 0 |

The two intervals touch but do not share any distance. This confirms why equality must produce zero.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(T) | Each test case uses a fixed number of comparisons |
| Space | O(T) | Stored output strings, or O(1) extra besides output |

With up to `10^5` test cases, the linear scan is easily within limits because each case is reduced to a few integer operations.

## Test Cases

```python
import sys, io

def solve():
    input = sys.stdin.readline
    t = int(input())
    ans = []

    for _ in range(t):
        a, b, c, d = map(int, input().split())
        left = max(a, c)
        right = min(b, d)
        ans.append(str(right - left if left < right else 0))

    return "\n".join(ans)

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    return solve()

assert run("""6
3 7 1 5
0 0 0 0
-5 -1 2 8
1 10 3 6
-1 4 4 10
-10 -2 -7 0
""") == """2
0
0
3
0
0
5""", "sample"

assert run("""1
5 5 5 5
""") == "0", "point intervals"

assert run("""1
0 10 3 7
""") == "4", "contained interval"

assert run("""1
-1000000000000000000 1000000000000000000 -999999999999999999 0
""") == "999999999999999999", "large coordinates"

assert run("""1
0 5 6 10
""") == "0", "disjoint intervals"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `[5,5]` and `[5,5]` | `0` | Degenerate intervals |
| `[0,10]` and `[3,7]` | `4` | One interval fully contains another |
| Very large endpoints | Large valid length | 64-bit boundary handling |
| `[0,5]` and `[6,10]` | `0` | No overlap |

## Edge Cases

For the touching endpoint case:

```
1
0 1 1 2
```

the algorithm computes `left = max(0,1) = 1` and `right = min(1,2) = 1`. Since the two values are equal, the condition fails and the answer becomes zero. The algorithm correctly treats the shared point as having no length.

For a contained interval:

```
1
0 10 3 7
```

the computed intersection is from `3` to `7`, because the later start is `3` and the earlier end is `7`. The answer is `7 - 3 = 4`, showing that no special containment logic is needed.

For negative coordinates:

```
1
-10 -2 -7 0
```

the intersection is `[-7,-2]`. The algorithm finds `left = -7` and `right = -2`, giving `5`. Negative positions behave exactly like positive ones because only ordering matters.
