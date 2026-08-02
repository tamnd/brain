---
title: "CF 102623B - Bamboo Leaf Rhapsody"
description: "The task is to find how quickly a message sent from the origin can reach at least one star. The stars are points in three-dimensional space, and the message travels in a straight line at speed one unit of distance per year."
date: "2026-08-02T14:06:18+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102623
codeforces_index: "B"
codeforces_contest_name: "2020 Lenovo Cup USST Campus Online Invitational Contest"
rating: 0
weight: 102623
solve_time_s: 191
verified: true
draft: false
---

[CF 102623B - Bamboo Leaf Rhapsody](https://codeforces.com/problemset/problem/102623/B)

**Rating:** -  
**Tags:** -  
**Solve time:** 3m 11s  
**Verified:** yes  

## Solution
## Problem Understanding

The task is to find how quickly a message sent from the origin can reach at least one star. The stars are points in three-dimensional space, and the message travels in a straight line at speed one unit of distance per year. Since the destination can be any one of the given stars, the answer is simply the smallest distance from the origin to any star.

Each input point describes one possible destination. For a star at coordinates `(x, y, z)`, the required travel time is the Euclidean distance from `(0, 0, 0)` to that point, which is `sqrt(x^2 + y^2 + z^2)`. The output is the minimum of these distances, rounded to three digits after the decimal point.

The number of stars is at most 1000. This is small enough that we can inspect every star once. An algorithm with quadratic behavior would already perform around one million operations, which is acceptable here, but the structure of the problem allows an even simpler linear scan. The coordinate values are limited to 1000 in absolute value, so squared distances fit comfortably inside normal integer ranges in Python.

Several implementation details can cause wrong answers. A common mistake is comparing distances after taking square roots, which is unnecessary and can introduce precision work that does not help. Another mistake is printing too few digits. For example:

```
1
1 1 1
```

The correct output is:

```
1.732
```

The distance is approximately `1.73205`, so rounding is required. A program that truncates instead of rounding would print `1.732` only accidentally for this case and can fail on values where the fourth decimal digit changes the answer.

Another edge case is a star at the origin:

```
1
0 0 0
```

The correct output is:

```
0.000
```

If an implementation initializes the minimum distance to zero instead of a very large value, every positive distance will be ignored incorrectly. The initial value must allow the first star to replace it.

Duplicate stars are also possible:

```
2
5 0 0
5 0 0
```

The answer is:

```
5.000
```

A solution must treat every star as a candidate but does not need to store any extra information because only the smallest distance matters.

## Approaches

The direct approach is to compute the distance for every star and keep the smallest value found. This works because every star is independent. There is no interaction between destinations, so checking all candidates is enough to guarantee that the best one is found.

A more complicated brute force interpretation might compare every pair of stars or build unnecessary geometric structures, but none of those operations contribute to the answer. The only relevant relationship is between each star and the origin. The useful computation count is therefore exactly one distance calculation per star.

The key observation is that the problem asks for the nearest point to a fixed point. Because the origin never changes, there is no need for sorting or searching. A single pass is sufficient. We can also compare squared distances instead of actual distances because the square root function is increasing. If `a < b`, then `sqrt(a) < sqrt(b)`, so the star with the smallest squared distance also has the smallest real distance.

The brute force works because checking every destination guarantees correctness, but it becomes wasteful if the number of stars grows much larger. The observation that the answer depends only on each point's distance to the origin reduces the solution to a linear scan.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n) | O(1) | Accepted, if implemented as a scan |
| Optimal | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the number of stars and prepare a variable containing a very large squared distance. This value represents the best answer found so far before examining any star.
2. For each star, compute `x * x + y * y + z * z`. This is the squared travel distance from the origin. Comparing squared values avoids unnecessary square root calculations while preserving the ordering of distances.
3. If the current squared distance is smaller than the stored minimum, replace the stored minimum with this value. The stored value always represents the closest star among all stars processed so far.
4. After all stars have been processed, take the square root of the minimum squared distance and print it with exactly three digits after the decimal point.

Why it works: after processing any prefix of the input, the stored minimum is the smallest squared distance among all stars in that prefix. The next star either becomes the new closest star or leaves the current answer unchanged. This invariant remains true until every star has been checked, so the final stored value corresponds to the nearest star overall. Taking the square root only at the end converts the squared distance back into the required travel time.

## Python Solution

```python
import sys
import math

input = sys.stdin.readline

def solve():
    n_line = input().strip()
    if not n_line:
        return

    n = int(n_line)
    best = float('inf')

    for _ in range(n):
        x, y, z = map(int, input().split())
        dist2 = x * x + y * y + z * z
        if dist2 < best:
            best = dist2

    print(f"{math.sqrt(best):.3f}")

if __name__ == "__main__":
    solve()
```

The program keeps only one value, `best`, because the identity of the closest star is irrelevant. The loop updates it whenever a better candidate appears, matching the invariant from the algorithm walkthrough.

The comparison uses squared distances. This avoids repeated floating point square root calculations and keeps the decision process exact because all squared distances are integers. The square root operation happens once, after the minimum has already been found.

The output format uses `:.3f`, which performs the required rounding to three decimal places. The initialization with infinity handles the case where the first star has any possible distance, including zero.

## Worked Examples

For the sample input:

```
3
0 1 1
2 0 0
0 -2 0
```

the execution is:

| Step | Star | Squared distance | Current minimum |
| --- | --- | --- | --- |
| Start | none | none | infinity |
| 1 | (0,1,1) | 2 | 2 |
| 2 | (2,0,0) | 4 | 2 |
| 3 | (0,-2,0) | 4 | 2 |

The minimum squared distance is 2, so the final distance is `sqrt(2)`, which rounds to `1.414`. This demonstrates that the algorithm keeps the best candidate and ignores farther stars.

A second example:

```
2
0 0 0
10 10 10
```

| Step | Star | Squared distance | Current minimum |
| --- | --- | --- | --- |
| Start | none | none | infinity |
| 1 | (0,0,0) | 0 | 0 |
| 2 | (10,10,10) | 300 | 0 |

The closest star is the origin itself, so the output is `0.000`. This confirms that zero distance is handled correctly.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Every star is visited exactly once and requires constant-time arithmetic. |
| Space | O(1) | Only the current minimum value is stored. |

With at most 1000 stars, the linear scan easily fits within the given limits. The algorithm also scales well because its memory usage does not depend on the number of stars.

## Test Cases

```python
import sys
import io
import math

def solution(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    input = sys.stdin.readline

    n = int(input())
    best = float('inf')

    for _ in range(n):
        x, y, z = map(int, input().split())
        best = min(best, x * x + y * y + z * z)

    return f"{math.sqrt(best):.3f}"

assert solution("""3
0 1 1
2 0 0
0 -2 0
""") == "1.414", "sample 1"

assert solution("""1
0 0 0
""") == "0.000", "origin case"

assert solution("""3
1000 1000 1000
-1000 -1000 -1000
1 1 1
""") == "1.732", "large coordinates and minimum selection"

assert solution("""4
5 0 0
0 5 0
0 0 5
5 0 0
""") == "5.000", "duplicate equal distances"

assert solution("""2
-1000 0 0
0 999 0
""") == "999.000", "boundary coordinate values"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Single star at `(0,0,0)` | `0.000` | Minimum distance can be zero |
| Coordinates at `1000` and `-1000` | `1.732` | Large values and correct comparison |
| Several identical nearest distances | `5.000` | Duplicate candidates do not affect the result |
| Negative and boundary coordinates | `999.000` | Absolute position matters through squared distance |

## Edge Cases

For the zero-distance case:

```
1
0 0 0
```

the algorithm starts with infinity, computes a squared distance of zero, and replaces the stored minimum. The final square root is zero, so the printed answer is `0.000`.

For duplicate stars:

```
2
5 0 0
5 0 0
```

the first star sets the minimum squared distance to 25. The second star also has squared distance 25, so the minimum remains unchanged. The final answer is `5.000`.

For rounding precision:

```
1
1 1 1
```

the algorithm stores the squared distance `3` and computes `sqrt(3)` only once at the end. The formatted output rounds the value correctly to `1.732`.

For negative coordinates:

```
1
-1000 0 0
```

the squared distance is `1000000`, the same as for `(1000,0,0)`. The sign of a coordinate does not affect distance because the value is squared before comparison.

This version can also be adapted into a shorter Codeforces submission note or a more formal contest editorial format if needed.
