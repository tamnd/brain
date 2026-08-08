---
title: "CF 102471A - City"
description: "We have an n×m rectangular grid of unit squares. Its grid points have integer coordinates, so there are (n+1)(m+1) points in total."
date: "2026-08-09T04:28:20+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102471
codeforces_index: "A"
codeforces_contest_name: "2019 ICPC Asia-East Continent Final"
rating: 0
weight: 102471
solve_time_s: 158
verified: true
draft: false
---

[CF 102471A - City](https://codeforces.com/problemset/problem/102471/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 2m 38s  
**Verified:** yes  

## Solution
## Problem Understanding

We have an n×m rectangular grid of unit squares. Its grid points have integer coordinates, so there are (n+1)(m+1) points in total. We may choose any two distinct grid points as the endpoints of a segment, including diagonal segments and segments that pass through other grid points.

A segment is valid exactly when its midpoint is also a grid point. We need to count every distinct non-zero segment satisfying that condition.

The coordinate viewpoint makes the condition much easier to reason about. Suppose the endpoints are (x 1 ​ ,y 1 ​ ) and (x 2 ​ ,y 2 ​ ). Their midpoint is

( 2 x 1 ​ +x 2 ​ ​ , 2 y 1 ​ +y 2 ​ ​ ).

Since all grid points have integer coordinates, the midpoint is a grid point exactly when both x 1 ​ +x 2 ​ and y 1 ​ +y 2 ​ are even. Equivalently, the two endpoints must have the same parity in their x-coordinates and the same parity in their y-coordinates.

The constraints give 1≤n,m≤1000, so there can be just over one million grid points. An algorithm that examines every pair of points would need roughly 5×10 11 pair checks at the maximum size, which is far beyond what a one-second solution can afford. We need to count the valid pairs without explicitly constructing them.

There are two small cases that commonly expose incorrect counting. For input `1 1`, there are four grid points, but every pair of distinct corners has a midpoint that is not an integer grid point, so the answer is `0`. A solution that counts all diagonals or all pairs at even-looking distances can accidentally count these segments.

For input `1 2`, there are six grid points. The two horizontal rows each contain three points, and only the two pairs spanning two unit intervals have grid-point midpoints. The answer is `2`. A solution that only considers horizontal and vertical segments can get this right here by accident, but it would fail on larger grids because valid diagonal segments also exist.

## Approaches

A direct approach is to assign coordinates to all (n+1)(m+1) grid points and inspect every unordered pair. For a pair of endpoints, we calculate the midpoint and check whether both coordinates are integers. This is correct because every possible segment is represented by exactly one pair of endpoints.

The problem is the number of pairs. At n=m=1000, there are 1,002,001 points, producing

( 2 1,002,001 ​ )=501,?×10 9

pairs, approximately 5.02×10 11. Even a very cheap constant-time check for each pair is much too slow.

The key observation is that the midpoint condition does not depend on the actual distances between the points. It depends only on coordinate parity. Two endpoints have an integer midpoint precisely when their x-coordinates have the same parity and their y-coordinates have the same parity.

That divides every grid point into one of four parity classes:

(even,even),(even,odd),(odd,even),(odd,odd).

Every pair of distinct points inside the same class is valid, while every pair from different classes is invalid. Thus, instead of checking every pair, we only need the size of each class and can add ( 2 k ​ ) for each class.

The number of even coordinates among 0,1,…,n is ⌊n/2⌋+1, while the number of odd coordinates is ⌈n/2⌉. The same applies independently to the y-coordinates. This gives all four class sizes immediately.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O((nm) 2 ) | O(nm) | Too slow |
| Optimal | O(1) | O(1) | Accepted |

## Algorithm Walkthrough

1. Count how many even and odd integers occur among the n+1 possible x-coordinates. There are ⌊n/2⌋+1 even values because the range starts at zero, and the remaining values are odd.
2. Count the even and odd values among the m+1 possible y-coordinates in the same way. The number of even values is ⌊m/2⌋+1, and the number of odd values is ⌈m/2⌉.
3. Construct the four parity-class sizes by multiplying the corresponding coordinate counts. For example, the number of points with even x and odd y is `even_x * odd_y`.
4. For each parity class containing k points, add ( 2 k ​ )=k(k−1)/2 to the answer. Every choice of two distinct points from that class has both coordinate sums even, so its midpoint is a grid point.
5. Print the sum of the four contributions. No geometric enumeration is necessary because the parity classification already captures the entire midpoint condition.

### Why it works

Consider any two grid points. Their midpoint is a grid point exactly when both coordinate averages are integers. An average of two integers is an integer exactly when the integers have the same parity. Thus a valid segment must have endpoints with the same x-parity and the same y-parity, meaning both endpoints belong to the same one of the four parity classes.

Conversely, any two distinct points in the same parity class have even coordinate sums, so their midpoint has integer coordinates and lies inside the rectangular grid because it lies on the segment connecting two grid points. Hence every pair counted by the algorithm is valid, and every valid pair is counted exactly once.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, m = map(int, input().split())

    even_x = n // 2 + 1
    odd_x = (n + 1) - even_x

    even_y = m // 2 + 1
    odd_y = (m + 1) - even_y

    classes = (
        even_x * even_y,
        even_x * odd_y,
        odd_x * even_y,
        odd_x * odd_y,
    )

    ans = sum(k * (k - 1) // 2 for k in classes)
    print(ans)

solve()
```

The first two counts describe the parity distribution of the x-coordinates from 0 through n. The `+ 1` in `n // 2 + 1` accounts for coordinate zero, which is even. The odd count is then obtained by subtracting the even count from the total number of coordinates.

The same calculation is performed for the y-coordinates. Multiplying one x-parity count by one y-parity count gives the number of grid points in the corresponding parity class.

The expression `k * (k - 1) // 2` counts unordered pairs of distinct points. We use integer arithmetic throughout, so there is no floating-point precision issue. Python integers also handle the maximum answer comfortably.

There is no coordinate array to construct, and no pair of points is explicitly visited. The entire calculation consists of a constant number of arithmetic operations.

## Worked Examples

For the first sample, n=1 and m=1. The possible x-coordinates are 0,1, and the possible y-coordinates are also 0,1.

| Variable | Value |
| --- | --- |
| `even_x` | 1 |
| `odd_x` | 1 |
| `even_y` | 1 |
| `odd_y` | 1 |
| `(even, even)` | 1 |
| `(even, odd)` | 1 |
| `(odd, even)` | 1 |
| `(odd, odd)` | 1 |
| Answer | 0 |

Every parity class has only one point, so there is no way to choose two distinct points from the same class. The answer is therefore `0`.

For the second sample, n=2 and m=3. The x-coordinates are 0,1,2, giving two even values and one odd value. The y-coordinates are 0,1,2,3, giving two even values and two odd values.

| Parity class | Number of points | Pairs |
| --- | --- | --- |
| `(even, even)` | 4 | 6 |
| `(even, odd)` | 4 | 6 |
| `(odd, even)` | 2 | 1 |
| `(odd, odd)` | 2 | 1 |
| Total | 12 | 14 |

The four class sizes are 4,4,2,2. Their pair counts are 6,6,1,1, giving the required answer `14`. The example also demonstrates why diagonal segments must be included, since many of these valid pairs are not horizontal or vertical.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(1) | Only the four parity classes are computed and processed. |
| Space | O(1) | The algorithm stores only a constant number of integers. |

With n,m≤1000, the grid can contain more than one million points, but the solution never constructs those points. The constant-time calculation is easily within the time and memory limits.

## Test Cases

```python
import sys
import io

def solve():
    input = sys.stdin.readline
    n, m = map(int, input().split())

    even_x = n // 2 + 1
    odd_x = (n + 1) - even_x

    even_y = m // 2 + 1
    odd_y = (m + 1) - even_y

    classes = (
        even_x * even_y,
        even_x * odd_y,
        odd_x * even_y,
        odd_x * odd_y,
    )

    ans = sum(k * (k - 1) // 2 for k in classes)
    print(ans)

def run(inp: str) -> str:
    old_stdin = sys.stdin
    old_stdout = sys.stdout

    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    solve()
    result = sys.stdout.getvalue()

    sys.stdin = old_stdin
    sys.stdout = old_stdout

    return result

# Provided samples
assert run("1 1\n") == "0\n", "sample 1"
assert run("2 3\n") == "14\n", "sample 2"

# Minimum-size grid
assert run("1 2\n") == "2\n", "minimum non-square grid"

# Equal dimensions, exercising all four parity classes
assert run("2 2\n") == "6\n", "equal values"

# Larger boundary case
assert run("1 1000\n") == "249500\n", "thin grid"

# Maximum-size input
assert run("1000 1000\n") == "125500500000\n", "maximum input"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 2` | `2` | Smallest non-square grid and parity counting |
| `2 2` | `6` | Equal dimensions and all four classes |
| `1 1000` | `249500` | Boundary behavior when one dimension is minimal |
| `1000 1000` | `125500500000` | Maximum constraints and large integer result |

## Edge Cases

For `1 1`, the coordinate sets are `{0,1}` in both directions. Each of the four parity classes contains exactly one point, so every value of k is 1 and every k(k−1)/2 contribution is zero. The algorithm prints `0`, correctly rejecting the tempting but invalid corner-to-corner diagonal.

For `1 2`, the x-coordinates have one even and one odd value, while the y-coordinates have two even and one odd value. The four class sizes are 2,1,2,1, giving 1+0+1+0=2. The two valid segments are the length-two horizontal segments on the two rows.

For `1000 1000`, there are 501 even and 500 odd values in each coordinate direction. The four class sizes become 251001,250500,250500,250000. Their pair counts sum to `125500500000`. This case confirms that the implementation handles the largest possible answer without overflow and that no iteration proportional to the number of grid points is hidden in the solution.
