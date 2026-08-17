---
title: "CF 102203D - \u041f\u0440\u043e \u043a\u044b\u0440\u0442"
description: "We have a fixed point (O), representing the factory, and (n) collection points in the plane. We need to choose four collection points and split them into two pairs. The segment connecting the points of each pair must pass through (O), and the four points must lie on one circle."
date: "2026-08-18T00:42:29+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102203
codeforces_index: "D"
codeforces_contest_name: "\u0427\u0435\u0442\u0432\u0435\u0440\u0442\u0430\u044f \u041b\u0438\u043f\u0435\u0446\u043a\u0430\u044f \u043a\u043e\u043c\u0430\u043d\u0434\u043d\u0430\u044f \u043e\u043b\u0438\u043c\u043f\u0438\u0430\u0434\u0430 \u0448\u043a\u043e\u043b\u044c\u043d\u0438\u043a\u043e\u0432 \u043f\u043e \u043f\u0440\u043e\u0433\u0440\u0430\u043c\u043c\u0438\u0440\u043e\u0432\u0430\u043d\u0438\u044e (8-11 \u043a\u043b\u0430\u0441\u0441\u044b)"
rating: 0
weight: 102203
solve_time_s: 361
verified: true
draft: false
---

[CF 102203D - \u041f\u0440\u043e \u043a\u044b\u0440\u0442](https://codeforces.com/problemset/problem/102203/D)

**Rating:** -  
**Tags:** -  
**Solve time:** 6m 1s  
**Verified:** yes  

## Solution
## Problem Understanding

We have a fixed point (O), representing the factory, and (n) collection points in the plane. We need to choose four collection points and split them into two pairs. The segment connecting the points of each pair must pass through (O), and the four points must lie on one circle.

Because every line through (O) contains at most two collection points, once we choose a valid pair, those two points must lie on opposite sides of (O). Thus every useful pair corresponds to one line through (O) containing exactly two collection points.

The coordinates of (O) and all collection points are integers with absolute value at most (10^4), while (n) is at most (2000). An (O(n^2)) solution would already perform about four million iterations, which is comfortable in Python. An (O(n^3)) or (O(n^4)) solution is not realistic under a one second limit. The main goal is consequently to reduce the search to essentially one pass over the points.

There are several geometric details that can make a seemingly correct implementation fail. A pair of points on the same ray from (O) does not form a segment containing (O). For example,

```
0 0
4
1 0
2 0
0 1
0 -2
```

has two points on the positive (x)-ray, so the first two cannot be a valid pair. The only valid pair is ((0,1),(0,-2)), which is not enough to form the required four points, so the answer is `NO`. An implementation that groups points only by an undirected slope and forgets which side of (O) they occupy could incorrectly treat the first two points as a pair.

A point coinciding with (O) must also be handled separately. For example,

```
0 0
3
0 0
1 0
-1 0
```

has only one non-degenerate pair, so the answer is `NO`. A point at (O) has zero distance from (O), and it cannot participate in one of the required two-point segments in a useful four-point configuration.

Duplicate coordinates are another reason not to assume that every normalized direction automatically represents a valid pair. For example,

```
0 0
2
1 1
1 1
```

contains two collection points at the same location. They do not lie on opposite sides of (O), so they cannot form the required segment through (O). The answer is `NO`.

Finally, exact arithmetic matters. The relevant geometric quantity is a product of squared distances, and using floating point values for it can introduce unnecessary equality errors. All coordinates are integral, so the entire computation can be performed with integers.

## Approaches

The direct approach is to enumerate every set of four collection points, try all three ways to split the four points into two pairs, check whether the corresponding segments pass through (O), and then check whether the four points are concyclic. This is correct because every possible answer is explicitly examined. However, with (n=2000), merely enumerating the four-point subsets requires

[
\binom{2000}{4}=664,668,499,500
]

iterations in the worst case. That is far beyond the available time.

The useful geometric observation is that the two chosen segments are secants of the same circle passing through (O). For any point pair (A,B) on one such line, define

[
P(A,B)=OA\cdot OB.
]

For any two secants through the same point (O) of a circle, the power-of-a-point theorem gives

[
OA\cdot OB=OC\cdot OD.
]

So instead of examining four points at once, we can examine each line through (O) that contains a pair of points and calculate its product of distances. Two different valid lines give the required answer exactly when their products are equal.

There is no need to use actual distances. If

[
r_A^2=OA^2,\qquad r_B^2=OB^2,
]

then equality of products of distances is equivalent to

[
r_A^2r_B^2=r_C^2r_D^2.
]

All these values are integers.

The remaining task is to identify opposite points on the same line. For a point (P), translate it by (O), reduce the vector by the gcd of its coordinates, and keep its sign. For example, ((6,4)) becomes ((3,2)), while its opposite ray is ((-3,-2)). A pair exists exactly when both normalized vectors occur.

The input guarantees that there are at most two points on any line through (O), so each ray can contain at most one relevant point. We can store one point for every normalized directed vector, then look for its negation.

The brute-force approach works because it explicitly checks every possible four-point configuration, but fails when (n=2000). The observation that every valid configuration is determined by two opposite-ray pairs, and that a circle makes their distance products equal, lets us reduce the problem to hashing one integer value per valid line.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | (O(n^4)) | (O(1)) | Too slow |
| Optimal | (O(n\log C)) | (O(n)) | Accepted |

Here (C) is the maximum absolute translated coordinate. Since (C\le 2\cdot10^4), the gcd computation is effectively constant time for these constraints.

## Algorithm Walkthrough

1. Translate every collection point by subtracting the coordinates of (O). A point with translated coordinates ((0,0)) is ignored because it cannot form a non-degenerate pair with another point across (O).
2. Normalize the direction of every remaining point. If its translated vector is ((x,y)), divide both coordinates by (\gcd(|x|,|y|)). Keep the sign unchanged, so opposite rays produce opposite keys.
3. Store for each normalized directed vector the point index and its squared distance
[
r^2=x^2+y^2.
]
The condition about at most two points on every line guarantees that a ray cannot contain two different collection points.
4. For every direction (v=(x,y)), look for the opposite direction (-v). If it does not exist, those points cannot form a segment through (O).
5. Process each undirected line only once. A simple way is to process only the direction satisfying (v< -v) in lexicographical tuple order. For the two points (A,B) on that line, calculate
[
value=OA^2\cdot OB^2.
]
6. Store the first pair found for every `value`. If another different line produces the same value, output the two stored endpoints followed by the two endpoints of the current line. Their two segments both contain (O), and the equal product condition guarantees that all four points lie on one circle.
7. If no product is repeated, output `NO`.

### Why it works

Consider any valid answer with pairs (A,B) and (C,D). Since both segments pass through (O), (A,B) are on opposite rays of one line and (C,D) are on opposite rays of another line. Since the four points lie on one circle, the power of (O) with respect to that circle gives

[
OA\cdot OB=OC\cdot OD.
]

Squaring both sides gives exactly the equality checked by the algorithm.

For the converse, suppose two distinct lines through (O) have opposite-ray pairs (A,B) and (C,D) with equal products. Take the circle through (A,B,C). Its power at (O) is determined by the first secant and equals (OA\cdot OB). The second line intersects this circle at (C) and at another point whose distance from (O) must make the same product. Since (OC\cdot OD) is equal to that value, (D) is precisely that second intersection. Thus all four points lie on the same circle.

The invariant is that every processed valid line is represented by exactly one integer, the squared power magnitude of its pair with respect to (O). Equal integers correspond exactly to two secants that can belong to the same circle.

## Python Solution

```python
import sys
import math

input = sys.stdin.readline

def solve():
    ox, oy = map(int, input().split())
    n = int(input())

    rays = {}

    for idx in range(1, n + 1):
        x, y = map(int, input().split())
        x -= ox
        y -= oy

        if x == 0 and y == 0:
            continue

        g = math.gcd(abs(x), abs(y))
        x //= g
        y //= g

        rays[(x, y)] = (idx, x * x + y * y)

    seen_value = {}

    for direction, data in rays.items():
        x, y = direction
        opposite = (-x, -y)

        if opposite not in rays:
            continue

        # Process each undirected line only once.
        if direction > opposite:
            continue

        idx1, r1 = data
        idx2, r2 = rays[opposite]

        value = r1 * r2

        if value in seen_value:
            a, b = seen_value[value]
            print("YES")
            print(a, b, idx1, idx2)
            return

        seen_value[value] = (idx1, idx2)

    print("NO")

if __name__ == "__main__":
    solve()
```

The first part of the code translates every point so that the factory becomes the origin. This makes both the direction test and the distance calculation independent of the original position of (O).

The gcd normalization turns vectors on the same ray into the same dictionary key. For instance, ((10,6)) and ((5,3)) both become ((5,3)). Their opposite ray is represented by ((-5,-3)). We deliberately preserve the sign because an undirected line alone is not enough to tell whether the segment between two points contains (O).

The squared distance is computed after normalization in the code. This is valid because the normalized vector still points in the same direction, but there is a subtle point here: the stored squared distance must be the actual squared distance of the original point, not the squared length of the normalized direction. The code as written above would consequently be incorrect.

The correct implementation must retain the original translated coordinates for the distance calculation while using the normalized vector only as the dictionary key. Here is the corrected complete solution.

```python
import sys
import math

input = sys.stdin.readline

def solve():
    ox, oy = map(int, input().split())
    n = int(input())

    rays = {}

    for idx in range(1, n + 1):
        x, y = map(int, input().split())
        x -= ox
        y -= oy

        if x == 0 and y == 0:
            continue

        dist2 = x * x + y * y

        g = math.gcd(abs(x), abs(y))
        dx = x // g
        dy = y // g

        rays[(dx, dy)] = (idx, dist2)

    seen_value = {}

    for direction, (idx1, r1) in rays.items():
        dx, dy = direction
        opposite = (-dx, -dy)

        if opposite not in rays:
            continue

        if direction > opposite:
            continue

        idx2, r2 = rays[opposite]
        value = r1 * r2

        if value in seen_value:
            a, b = seen_value[value]
            print("YES")
            print(a, b, idx1, idx2)
            return

        seen_value[value] = (idx1, idx2)

    print("NO")

if __name__ == "__main__":
    solve()
```

The second version is the one to submit. The distinction between the normalized direction and the original vector is essential. Normalization removes the distance information, so using the normalized vector to compute (OA^2) would make unrelated points on the same ray appear to have the same distance.

Python integers have arbitrary precision, so the product causes no overflow. With the original coordinate differences bounded by (2\cdot10^4), each squared distance is at most (8\cdot10^8), and the product is below roughly (6.4\cdot10^{17}).

The lexicographical comparison `direction > opposite` prevents processing the same line twice. It does not affect the geometry, it only avoids storing the same pair in the power map twice.

The order of the final four indices is also deliberate. The first two indices come from one opposite-ray pair, while the last two come from another. Consequently, the first segment and the second segment both pass through (O), exactly as required by the output format.

## Worked Examples

Only one sample is provided in the statement, so the second trace uses a small custom configuration.

### Sample 1

The factory is at (O=(1,1)). After translating by (O), the relevant points are:

| Index | Translated vector | Normalized direction | Squared distance | Opposite | Pair value
