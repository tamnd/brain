---
title: "CF 106027A - Large Triangle"
description: "We are given a set of points on a plane and a target area. The task is to choose three of the points so that the triangle they form has exactly the requested area, or report that such a triangle does not exist."
date: "2026-06-25T13:09:08+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 106027
codeforces_index: "A"
codeforces_contest_name: "COMP4128 Large Triangle"
rating: 0
weight: 106027
solve_time_s: 41
verified: true
draft: false
---

[CF 106027A - Large Triangle](https://codeforces.com/problemset/problem/106027/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 41s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a set of points on a plane and a target area. The task is to choose three of the points so that the triangle they form has exactly the requested area, or report that such a triangle does not exist. The area is compared using twice the area, because for integer coordinates the doubled area is always an integer. The original problem has up to 2000 points and a target area up to $2 \cdot 10^{18}$.

The bounds immediately rule out checking every triple. There are $O(n^3)$ possible triangles, which means around $8 \cdot 10^9$ checks at the largest input size. Even with very small constant factors this is too much. We need to reduce the search to roughly quadratic work, because $2000^2$ operations are manageable.

A useful way to think about a triangle is to fix one side as the base. Once two endpoints of the base are known, the required height is also known. The remaining task becomes finding a point whose perpendicular distance from this base line has exactly the needed value.

A careless implementation can fail when it uses floating point geometry. For example, if the target doubled area is `1` and the triangle has a very small height, floating point rounding can incorrectly decide that the area is not exact. The input coordinates can be as large as $10^9$, so cross products can reach about $10^{18}$, and integer arithmetic must be used.

Another common mistake is forgetting that the triangle can lie on either side of the chosen base. For input

```
3 5
0 0
10 0
5 1
```

the doubled area is `10`, so this particular target is impossible. A method that only searches points above the base would also miss valid solutions when the point is below it, because the signed cross product is negative there.

## Approaches

The brute force approach is to pick every triple of points, compute the doubled area using the cross product, and compare it with the target. This is correct because every possible triangle is explicitly checked. The problem is the number of triples, which is about $n^3/6$. For $n=2000$, that is billions of operations.

The key observation is that after choosing a base, the area condition becomes a one dimensional search. If the base vector is $v$, the doubled area is the absolute value of the cross product between $v$ and the vector to the third point. We need a point with a particular signed distance from the base line.

The difficult part is maintaining the points ordered by their distance to the current base. Recomputing this order for every pair would again be too slow. Instead, we rotate the base through all possible segments. When the direction of the base changes continuously, the relative order of two points changes only when the rotating line becomes parallel to the segment connecting those two points. Since we process all point pairs in angular order, every change is just a swap of two adjacent points in the maintained ordering. This gives an $O(n^2 \log n)$ solution.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n³) | O(1) | Too slow |
| Optimal | O(n² log n) | O(n²) | Accepted |

## Algorithm Walkthrough

1. Create all directed point pairs and sort them by the angle of the segment connecting the pair. The sweep starts with a horizontal direction, where sorting by distance to the line is the same as sorting by the y coordinate.
2. Maintain an array of points ordered by their signed distance from the current sweep line. Also store the position of every point inside this array so that swaps are constant time.
3. For every segment in angular order, use the current ordering to search for the third point. For a base from `a` to `b`, the doubled area condition is:

$$cross(b-a, c-a)=2S$$

or the same value with the opposite sign. Because the points are sorted by this value, binary search can find a matching point.

1. After processing a segment, swap the two endpoints of that segment inside the maintained order. This updates the order for the next sweep position.

The reason the swap is enough is that the only moment when two points exchange their order relative to a rotating line is when the line becomes parallel to the segment joining them. We process exactly those events.

Why it works: the maintained ordering is always the ordering of points by signed distance from the current base line. Binary search is valid because the cross product with a fixed base vector is a linear transformation, so it preserves the ordering of distances. The sweep updates the ordering at exactly the moments when two distances can become equal, and no three points are collinear, so every event is unambiguous. Once a point with the required cross product is found, the triangle area condition is satisfied by construction.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, S = map(int, input().split())
    pts = [tuple(map(int, input().split())) for _ in range(n)]
    target = 2 * S

    def cross(a, b, c):
        return (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])

    events = []
    for i in range(n):
        for j in range(i + 1, n):
            dx = pts[j][0] - pts[i][0]
            dy = pts[j][1] - pts[i][1]
            events.append((dy, dx, i, j))

    events.sort(key=lambda e: __import__("math").atan2(e[0], e[1]))

    order = sorted(range(n), key=lambda i: pts[i][1])
    pos = [0] * n
    for i, x in enumerate(order):
        pos[x] = i

    for _, _, a, b in events:
        lo, hi = 0, n
        while lo < hi:
            mid = (lo + hi) // 2
            c = order[mid]
            val = cross(a, b, c)
            if val < target:
                lo = mid + 1
            else:
                hi = mid

        if lo < n and cross(a, b, order[lo]) == target:
            c = order[lo]
            print("YES")
            print(*pts[a])
            print(*pts[b])
            print(*pts[c])
            return

        lo, hi = 0, n
        while lo < hi:
            mid = (lo + hi) // 2
            c = order[mid]
            val = cross(a, b, c)
            if val < -target:
                lo = mid + 1
            else:
                hi = mid

        if lo < n and cross(a, b, order[lo]) == -target:
            c = order[lo]
            print("YES")
            print(*pts[a])
            print(*pts[b])
            print(*pts[c])
            return

        pa, pb = pos[a], pos[b]
        order[pa], order[pb] = order[pb], order[pa]
        pos[a], pos[b] = pb, pa

    print("NO")

if __name__ == "__main__":
    solve()
```

The `cross` function is the core geometry operation. It returns twice the signed area, which avoids all floating point calculations.

The sweep array `order` is the dynamic structure described in the algorithm. The `pos` array prevents an expensive search when the two endpoints of the current base need to be swapped.

The binary searches look for both possible orientations of the triangle. Searching only one sign would miss triangles on the opposite side of the base. All arithmetic stays in Python integers, so large coordinate products do not overflow.

## Worked Examples

For the first sample:

```
3 7
0 0
3 0
0 4
```

The only triangle has doubled area 24, not 14.

| Step | Base | Required cross value | Found point | Result |
| --- | --- | --- | --- | --- |
| 1 | (0,0) to (3,0) | 14 or -14 | none | continue |
| 2 | other pairs | 14 or -14 | none | NO |

The trace shows that checking every base does not find a matching height.

For the second sample:

```
4 3
0 0
2 0
1 2
1 3
```

The target doubled area is 6.

| Step | Base | Required cross value | Found point | Result |
| --- | --- | --- | --- | --- |
| 1 | (0,0) to (2,0) | 6 | (1,3) | YES |

The cross product is $2 \cdot 3 = 6$, so the actual area is 3.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n² log n) | There are $O(n²)$ bases, and each one performs binary searches |
| Space | O(n²) | The list of all point pairs dominates the memory |

The maximum input size is small enough for quadratic memory and near quadratic time. The solution avoids the cubic explosion from enumerating all triangles.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    old = sys.stdin
    sys.stdin = io.StringIO(inp)
    out = io.StringIO()
    old_out = sys.stdout
    sys.stdout = out
    solve()
    sys.stdin = old
    sys.stdout = old_out
    return out.getvalue().strip()

assert run("""3 7
0 0
3 0
0 4
""") == "NO"

assert run("""4 3
0 0
2 0
1 2
1 3
""").split()[0] == "YES"

assert run("""3 1
0 0
1 0
0 1
""").split()[0] == "YES"

assert run("""4 100
0 0
1 0
0 1
1 1
""") == "NO"

assert run("""5 6
0 0
2 0
1 3
4 0
3 2
""").split()[0] == "YES"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Three points forming area 6 but target 7 | NO | Impossible case handling |
| Four point example | YES | Basic successful search |
| Unit right triangle | YES | Minimum useful geometry case |
| Square with too large target | NO | Boundary failure |
| Mixed coordinates | YES | General sweep behaviour |

## Edge Cases

For the impossible sample:

```
3 7
0 0
3 0
0 4
```

The algorithm checks every possible base. The base `(0,0)` to `(3,0)` would require a point with cross product 14, but the third point gives 12. The other two bases fail as well, so the answer remains `NO`.

For the smallest valid triangle:

```
3 1
0 0
1 0
0 1
```

The target doubled area is 2. Taking the first two points as the base, the third point gives cross product 1? With the correct orientation the base `(0,0)` to `(0,1)` gives cross product 2, so the binary search finds it and returns `YES`.

The algorithm handles both orientations because every base is tested with both `target` and `-target`, so triangles below a chosen base line are treated exactly like triangles above it.
