---
title: "CF 491B - New York Hotel"
description: "The city is a rectangular grid. Every hotel and every restaurant is located at an intersection with coordinates $(x,y)$."
date: "2026-05-31T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "greedy", "math"]
categories: ["algorithms"]
codeforces_contest: 491
codeforces_index: "B"
codeforces_contest_name: "Testing Round 11"
rating: 2100
weight: 491
solve_time_s: 700
verified: false
draft: false
---

[CF 491B - New York Hotel](https://codeforces.com/problemset/problem/491/B)

**Rating:** 2100  
**Tags:** greedy, math  
**Solve time:** 11m 40s  
**Verified:** no  

## Solution
## Problem Understanding

The city is a rectangular grid. Every hotel and every restaurant is located at an intersection with coordinates $(x,y)$. Moving between neighboring intersections costs one kilometer, so the travel distance between two points is the Manhattan distance

$$|x_1-x_2| + |y_1-y_2|.$$

All friends start from their hotels and travel to the same restaurant. For a chosen restaurant, the cost we care about is not the total distance traveled by all friends, but the largest distance traveled by any single friend.

For every restaurant we must compute

$$\max_{\text{hotel } h}
\left(
|x_h-x_r|+|y_h-y_r|
\right)$$

and choose a restaurant that minimizes this value. We must output both the optimal maximum distance and the index of any restaurant achieving it.

The city dimensions can be as large as $10^9$, but this turns out to be irrelevant because we never need to iterate over grid cells. The important constraints are the numbers of hotels and restaurants, both up to $10^5$.

A direct comparison of every restaurant against every hotel would require

$$10^5 \times 10^5 = 10^{10}$$

distance computations in the worst case, which is completely impossible within a 2 second limit. We need something close to linear or $O(n \log n)$.

Several subtle situations can cause incorrect reasoning.

Consider two hotels:

```
(1,100)
(100,1)
```

and a restaurant:

```
(50,50)
```

A careless solution might try to use the hotel with largest $x$ or largest $y$ independently. The farthest hotel is determined by the Manhattan metric, which combines both coordinates. Looking only at one coordinate loses information.

Another easy mistake is assuming that the city bounds matter. For example:

```
N = M = 10^9
hotel = (1,1)
restaurant = (10^9,10^9)
```

The distance is simply

$$(10^9-1)+(10^9-1),$$

and no grid traversal is required. Any solution depending on the area of the city would fail immediately.

A third trap is handling duplicate locations. Example:

```
Hotels:
(5,5)
(5,5)

Restaurants:
(5,5)
```

The answer is distance $0$. The algorithm must treat duplicate points normally and not assume all coordinates are distinct.

## Approaches

The brute force approach is straightforward. For each restaurant, compute its Manhattan distance to every hotel and keep the maximum. After evaluating all hotels, we know the worst distance for that restaurant. Repeating this for all restaurants gives the optimal answer.

The reason this works is simple. The definition of the objective is exactly the maximum hotel-to-restaurant distance, so explicitly checking every pair produces the correct result.

The problem is the scale. With $10^5$ hotels and $10^5$ restaurants, we would evaluate $10^{10}$ distances. Even if a distance computation took only a few machine instructions, this is far beyond the limit.

To improve this, we need to understand the structure of Manhattan distance.

For any hotel $(a,b)$ and restaurant $(x,y)$,

$$|a-x|+|b-y|.$$

A standard identity for Manhattan geometry is

$$|u|+|v|
=
\max
\{
(u+v),
(u-v),
(-u+v),
(-u-v)
\}.$$

Substituting $u=a-x$ and $v=b-y$,

$$|a-x|+|b-y|
=
\max
\{
(a+b)-(x+y),
(a-b)-(x-y),
(-a+b)-(-x+y),
(-a-b)-(-x-y)
\}.$$

For a fixed restaurant, the maximum over all hotels becomes

$$\max
\left(
\max(a+b)-(x+y),
\max(a-b)-(x-y),
\max(-a+b)-(-x+y),
\max(-a-b)-(-x-y)
\right).$$

The crucial observation is that all hotel information is compressed into four global maxima.

Let

$$M_1=\max(a+b),$$

$$M_2=\max(a-b),$$

$$M_3=\max(-a+b),$$

$$M_4=\max(-a-b).$$

Once these four values are known, the farthest-hotel distance for any restaurant can be computed in constant time.

The brute force works because it explicitly searches for the farthest hotel. The observation above replaces that search with four precomputed extreme values. We spend $O(C)$ time preprocessing hotels and $O(H)$ time evaluating restaurants.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(CH)$ | $O(1)$ | Too slow |
| Optimal | $O(C+H)$ | $O(1)$ | Accepted |

## Algorithm Walkthrough

1. Read all hotel coordinates.
2. Compute four values over all hotels:

$$M_1=\max(x+y)$$

$$M_2=\max(x-y)$$

$$M_3=\max(-x+y)$$

$$M_4=\max(-x-y)$$

These are the only hotel statistics needed later.
3. Process restaurants one by one.
4. For a restaurant $(x,y)$, compute

$$d=
\max(
M_1-(x+y),
M_2-(x-y),
M_3-(-x+y),
M_4-(-x-y)
).$$

This value equals the maximum Manhattan distance from the restaurant to any hotel.
5. Keep the restaurant with the smallest value of $d$.
6. Output the best distance and the corresponding 1-based restaurant index.

### Why it works

For every hotel, Manhattan distance can be rewritten as the maximum of four linear expressions. When we take the maximum over all hotels, each linear expression depends on the largest value attained by a hotel in that direction. Those largest values are exactly $M_1,M_2,M_3,M_4$.

For a fixed restaurant, evaluating the four expressions using these precomputed maxima gives the same result as checking every hotel individually. Since the computed value is exactly the farthest-hotel distance, comparing these values across restaurants selects the restaurant minimizing the worst travel distance. No approximation is involved, so the algorithm is correct.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, m = map(int, input().split())

    c = int(input())

    INF = 10**30

    m1 = -INF
    m2 = -INF
    m3 = -INF
    m4 = -INF

    for _ in range(c):
        x, y = map(int, input().split())

        m1 = max(m1, x + y)
        m2 = max(m2, x - y)
        m3 = max(m3, -x + y)
        m4 = max(m4, -x - y)

    h = int(input())

    best_dist = INF
    best_idx = 1

    for idx in range(1, h + 1):
        x, y = map(int, input().split())

        dist = max(
            m1 - (x + y),
            m2 - (x - y),
            m3 - (-x + y),
            m4 - (-x - y)
        )

        if dist < best_dist:
            best_dist = dist
            best_idx = idx

    print(best_dist)
    print(best_idx)

solve()
```

The first part of the code computes the four extreme transformed coordinates from all hotels. This corresponds to the preprocessing step that compresses all hotel information into four numbers.

The restaurant loop evaluates the farthest-hotel distance in constant time using those four maxima. Since restaurant indices are required in the output, the loop is run with 1-based indexing.

All arithmetic easily fits in 64-bit integers. Coordinates are at most $10^9$, so transformed values are bounded by roughly $2 \cdot 10^9$. Python integers handle this automatically.

A common implementation mistake is forgetting that the restaurant answer is the maximum of the four transformed expressions, not the minimum. Each expression represents one possible sign configuration in the Manhattan distance identity.

## Worked Examples

### Sample 1

Input:

```
10 10
2
1 1
3 3
2
1 10
4 4
```

Hotel preprocessing:

| Hotel | x+y | x-y | -x+y | -x-y |
| --- | --- | --- | --- | --- |
| (1,1) | 2 | 0 | 0 | -2 |
| (3,3) | 6 | 0 | 0 | -6 |

Final maxima:

| M1 | M2 | M3 | M4 |
| --- | --- | --- | --- |
| 6 | 0 | 0 | -2 |

Restaurant evaluation:

| Restaurant Index | Coordinates | Distance |
| --- | --- | --- |
| 1 | (1,10) | 9 |
| 2 | (4,4) | 6 |

The second restaurant has the smaller worst-case distance, so the answer is:

```
6
2
```

This trace shows how every restaurant can be evaluated without revisiting the hotels.

### Example 2

Input:

```
100 100
2
1 100
100 1
2
50 50
1 1
```

Hotel preprocessing:

| Hotel | x+y | x-y | -x+y | -x-y |
| --- | --- | --- | --- | --- |
| (1,100) | 101 | -99 | 99 | -101 |
| (100,1) | 101 | 99 | -99 | -101 |

Maxima:

| M1 | M2 | M3 | M4 |
| --- | --- | --- | --- |
| 101 | 99 | 99 | -101 |

Restaurant evaluation:

| Restaurant Index | Coordinates | Distance |
| --- | --- | --- |
| 1 | (50,50) | 99 |
| 2 | (1,1) | 99 |

Both restaurants achieve the same value. Either index is valid.

This example demonstrates that the farthest hotel is determined by transformed coordinates, not by examining only the largest $x$ or largest $y$.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(C+H)$ | One pass over hotels and one pass over restaurants |
| Space | $O(1)$ | Only a few variables are stored |

The input size can reach $2 \cdot 10^5$ points. A linear scan over all points is easily fast enough within the time limit. Memory usage is constant and far below the available 256 MB.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    input = sys.stdin.readline

    n, m = map(int, input().split())

    c = int(input())

    INF = 10**30
    m1 = m2 = m3 = m4 = -INF

    for _ in range(c):
        x, y = map(int, input().split())
        m1 = max(m1, x + y)
        m2 = max(m2, x - y)
        m3 = max(m3, -x + y)
        m4 = max(m4, -x - y)

    h = int(input())

    best_dist = INF
    best_idx = 1

    for idx in range(1, h + 1):
        x, y = map(int, input().split())

        dist = max(
            m1 - (x + y),
            m2 - (x - y),
            m3 - (-x + y),
            m4 - (-x - y)
        )

        if dist < best_dist:
            best_dist = dist
            best_idx = idx

    return f"{best_dist}\n{best_idx}\n"

# provided sample
assert run(
"""10 10
2
1 1
3 3
2
1 10
4 4
"""
) == "6\n2\n"

# minimum size
assert run(
"""1 1
1
1 1
1
1 1
"""
) == "0\n1\n"

# duplicate hotels
assert run(
"""10 10
2
5 5
5 5
1
5 5
"""
) == "0\n1\n"

# tie between restaurants
assert run(
"""100 100
2
1 100
100 1
2
50 50
1 1
"""
) in ("99\n1\n", "99\n2\n")

# boundary coordinates
assert run(
"""1000000000 1000000000
1
1 1
1
1000000000 1000000000
"""
) == "1999999998\n1\n"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Single hotel and restaurant at same point | 0 | Minimum-size case |
| Duplicate hotel coordinates | 0 | Duplicate points handled correctly |
| Symmetric hotel placement | Either restaurant index | Correct tie handling |
| Coordinates near $10^9$ | 1999999998 | Large values and overflow safety |

## Edge Cases

Consider duplicate locations:

```
10 10
2
5 5
5 5
1
5 5
```

The maxima become:

$$M_1=10,\quad M_2=0,\quad M_3=0,\quad M_4=-10.$$

For the restaurant $(5,5)$,

$$\max(0,0,0,0)=0.$$

The algorithm outputs distance $0$, exactly matching the true answer.

Consider extreme coordinates:

```
1000000000 1000000000
1
1 1
1
1000000000 1000000000
```

The transformed maxima are computed from the single hotel. Evaluating the restaurant yields

$$(10^9-1)+(10^9-1)=1999999998.$$

No iteration over city cells occurs, so the huge grid size causes no difficulty.

Consider a tie:

```
100 100
2
1 100
100 1
2
50 50
1 1
```

Both restaurants produce maximum distance $99$. The algorithm keeps the first one it encounters with the optimal value. Since the statement allows any optimal restaurant, this behavior is correct.
