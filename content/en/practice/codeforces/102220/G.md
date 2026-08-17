---
title: "CF 102220G - Radar Scanner"
description: "We have (n) axis-aligned rectangular scanners. Scanner (i) currently covers every grid square whose coordinates lie inside [ [ai,ci]times[bi,di]."
date: "2026-08-17T22:42:46+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102220
codeforces_index: "G"
codeforces_contest_name: "The 13th Chinese Northeast Collegiate Programming Contest"
rating: 0
weight: 102220
solve_time_s: 108
verified: true
draft: false
---

[CF 102220G - Radar Scanner](https://codeforces.com/problemset/problem/102220/G)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 48s  
**Verified:** yes  

## Solution
## Problem Understanding

We have (n) axis-aligned rectangular scanners. Scanner (i) currently covers every grid square whose coordinates lie inside

[
[a_i,c_i]\times[b_i,d_i].
]

A move shifts one entire scanner by exactly one square horizontally or vertically, so moving a scanner by ((\Delta x,\Delta y)) costs (|\Delta x|+|\Delta y|). We want to reposition the scanners so that at least one grid square belongs to every scanner, while minimizing the total number of moves.

The first useful simplification is to forget about the final scanner positions and instead choose the square that all scanners will cover. Once that square is fixed, every scanner can be optimized independently. The remaining question is how to choose the best common square.

There are up to (10^5) scanners in one test case, and the total number of scanners over all test cases is at most (10^6). The coordinates can reach (10^9), so algorithms that enumerate possible positions are immediately impossible. With a two second time limit, even an (O(n^2)) method is far too expensive at (n=10^5), and a method depending on the coordinate range would be even worse. We need essentially (O(n\log n)) total work, or better.

There are several edge cases that are easy to mishandle. A single scanner already has a common covered square with itself, so

```
1
1
5 7 9 11
```

must produce

```
0
```

A careless implementation that always moves toward a chosen global coordinate could produce a positive answer even though no movement is necessary.

Two rectangles may already overlap even when neither rectangle is contained in the other. For example,

```
1
2
1 1 5 5
3 3 7 7
```

has answer `0`, because the square ((3,3)) is covered by both. An approach based only on rectangle centers can miss this.

Touching at a boundary also counts because the covered squares are integer squares and the endpoints are included. For

```
1
2
1 1 1 1
2 1 2 1
```

the answer is `1`: move either scanner one square horizontally. Treating intervals as open would incorrectly reject the boundary positions.

A rectangle can be much wider than the others. Consider

```
1
2
1 1 10 10
5 5 5 5
```

The answer is `0`, because the second scanner lies inside the first. A method that replaces each rectangle by its center would lose exactly the information that makes the answer zero.

Finally, the coordinates can be as large as (10^9). For

```
1
2
1 1 1 1
1000000000 1000000000 1000000000 1000000000
```

the answer is

```
1999999998
```

because one scanner must move (999999999) squares in each direction. Python integers handle this safely, but fixed-width implementations need a sufficiently large integer type.

## Approaches

A direct brute-force solution can choose a candidate square ((x,y)), compute how far every scanner has to move so that it covers that square, and keep the minimum total cost. This is correct because every valid final configuration has some common covered square, so considering every possible common square considers an optimal configuration as well.

The problem is the number of candidates. Since all useful coordinates lie inside the bounding box of the input rectangles, there can still be (10^9) possible (x)-coordinates and (10^9) possible (y)-coordinates. That gives as many as (10^{18}) candidate squares. Evaluating all (n) scanners for each candidate would require up to (10^{23}) distance computations when (n=10^5). The brute force is conceptually simple, but it is nowhere close to feasible.

The key observation is that the two coordinates are completely independent. Suppose the common square has (x)-coordinate (x). For scanner (i), its horizontal interval is ([a_i,c_i]). If (x) already belongs to this interval, no horizontal movement is needed. If (x<a_i), the scanner must move left or right so that its left boundary reaches (x), costing (a_i-x). Similarly, if (x>c_i), the cost is (x-c_i).

Thus the horizontal cost for scanner (i) is exactly the distance from (x) to the interval ([a_i,c_i]):

[
\operatorname{dist}(x,[a_i,c_i]).
]

The total horizontal cost is consequently

[
F(x)=\sum_i \operatorname{dist}(x,[a_i,c_i]).
]

The vertical coordinate gives an identical problem with intervals ([b_i,d_i]). We can solve the two one-dimensional problems independently and add their answers.

The remaining question is how to minimize the sum of distances to intervals. The useful identity is

(r-l)+2\operatorname{dist}(x,[l,r]).
]

Rearranging,

\frac{|x-l|+|x-r|-(r-l)}{2}.
]

After summing this over all intervals, the terms involving (x) become the sum of absolute distances from (x) to all (2n) endpoints. A sum of absolute distances is minimized at a median. So we only need the median of all left and right endpoints.

The brute-force works because it explicitly searches for the common square. It fails because the search space is enormous. The observation that the movement cost separates by coordinate turns the problem into two one-dimensional interval problems, and the endpoint identity reduces each of those to finding a median.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | (O(n\cdot 10^{18})) | (O(1)) | Too slow |
| Optimal | (O(n\log n)) | (O(n)) | Accepted |

## Algorithm Walkthrough

1. For every scanner, collect its horizontal endpoints (a_i,c_i) into one array and its vertical endpoints (b_i,d_i) into another array. Also accumulate the total horizontal width (\sum(c_i-a_i)) and vertical height (\sum(d_i-b_i)). The two axes can be processed independently because a horizontal move never changes the vertical coverage.
2. Sort the (2n) horizontal endpoints. Choose the element at index (n-1), using zero-based indexing, as the horizontal target coordinate (x). This is one of the two middle endpoints, so it is a valid median of all (2n) endpoints.
3. Compute the sum of absolute differences between (x) and every horizontal endpoint. If the sorted endpoints are (e_1,\ldots,e_{2n}), the horizontal movement cost is

[
\frac{\sum_j |e_j-x|-\sum_i(c_i-a_i)}{2}.
]

The subtraction of the total widths removes the movement that is already free because a target coordinate can lie inside a rectangle rather than forcing both endpoints toward it.

1. Repeat the same calculation for the vertical endpoints, using (y) equal to the middle vertical endpoint and subtracting the total rectangle heights.
2. Add the horizontal and vertical costs. This is the minimum number of individual scanner moves because every unit of horizontal or vertical displacement corresponds to exactly one allowed operation.

### Why it works

For any fixed target square ((x,y)), scanner (i) needs exactly

[
\operatorname{dist}(x,[a_i,c_i])
+
\operatorname{dist}(y,[b_i,d_i])
]

moves. Summing over scanners separates the objective into an (x)-only part and a (y)-only part, so minimizing the two coordinates independently is optimal.

For one interval ([l,r]),

\frac{|x-l|+|x-r|-(r-l)}{2}.
]

After summing over all intervals, the only part depending on (x) is the sum of absolute distances from (x) to all (2n) endpoints. Every median minimizes such a sum. Hence the selected middle endpoint gives the minimum possible horizontal cost, and the same argument gives the minimum vertical cost. Since the two costs are independent, their sum is globally optimal.

## Python Solution

```python
import sys
input = sys.stdin.readline

def axis_cost(endpoints, span_sum, n):
    endpoints.sort()
    median = endpoints[n - 1]

    distance_sum = sum(abs(x - median) for x in endpoints)
    return (distance_sum - span_sum) // 2

def solve():
    t = int(input())
    out = []

    for _ in range(t):
        n = int(input())

        xs = []
        ys = []
        x_span = 0
        y_span = 0

        for _ in range(n):
            a, b, c, d = map(int, input().split())

            xs.append(a)
            xs.append(c)
            ys.append(b)
            ys.append(d)

            x_span += c - a
            y_span += d - b

        answer = axis_cost(xs, x_span, n)
        answer += axis_cost(ys, y_span, n)

        out.append(str(answer))

    sys.stdout.write("\n".join(out))

if __name__ == "__main__":
    solve()
```

The input loop stores exactly the two endpoints needed for each axis. There is no need to retain the original rectangles after their endpoints and widths have been recorded.

`axis_cost` first sorts the (2n) endpoints and selects `endpoints[n - 1]`. Because there are (2n) values, both middle positions are valid medians. Choosing the lower middle value avoids any need for floating point arithmetic and is especially convenient with zero-based indexing.

The expression

```
distance_sum - span_sum
```

implements the identity from the proof. For every interval ([l,r]), its two endpoint contributions are (|x-l|+|x-r|), while its width (r-l) is subtracted. The result is exactly twice the required distance to the interval. Integer division by two is safe because the resulting quantity is an integer.

The input coordinates are at most (10^9), but the total answer can be around (2\cdot10^{14}), so Python's arbitrary-precision integers are convenient. There is no risk of overflow.

The division must happen after the entire sum is formed. Dividing individual endpoint contributions first would be incorrect because the two endpoint terms and the interval width must be combined before dividing by two.

## Worked Examples

For the official sample,

```
1
2
2 2 3 3
4 4 5 5
```

the horizontal and vertical calculations are identical.

| Axis | Endpoints | Median | Sum of endpoint distances | Total widths | Cost |
| --- | --- | --- | --- | --- | --- |
| X | 2, 3, 4, 5 | 3 | 4 | 2 | 1 |
| Y | 2, 3, 4, 5 | 3 | 4 | 2 | 1 |

The first rectangle already covers ((3,3)). The second rectangle must move one square left and one square down, so the total is (1+1=2). The median calculation produces exactly the same result.

For a case where one rectangle contains another,

```
1
2
1 1 10 10
5 5 5 5
```

the endpoints and calculations are:

| Axis | Endpoints | Median | Sum of endpoint distances | Total widths | Cost |
| --- | --- | --- | --- | --- | --- |
| X | 1, 5, 5, 10 | 5 | 9 | 9 | 0 |
| Y | 1, 5, 5, 10 | 5 | 9 | 9 | 0 |

The target square can be ((5,5)), which is already covered by both scanners. The width subtraction is what makes the cost zero for the large rectangle rather than incorrectly charging for the distance to its endpoints.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | (O(n\log n)) | Each axis sorts (2n) endpoints, followed by a linear scan |
| Space | (O(n)) | Two arrays contain (2n) endpoints each |

The total number of scanners over all test cases is at most (10^6), so the total sorting work is bounded by the corresponding sum of (O(n\log n)) terms. The implementation never enumerates coordinates, target squares, or scanner movements, so the coordinate bound of (10^9) does not affect the running time.

The memory usage is linear in the number of scanners. With the given 512 MB memory limit, storing the endpoint arrays is feasible.

## Test Cases

```python
import sys
import io

input = sys.stdin.readline

def axis_cost(endpoints, span_sum, n):
    endpoints.sort()
    median = endpoints[n - 1]
    distance_sum = sum(abs(x - median) for x in endpoints)
    return (distance_sum - span_sum) // 2

def solve():
    t = int(input())
    out = []

    for _ in range(t):
        n = int(input())

        xs = []
        ys = []
        x_span = 0
        y_span = 0

        for _ in range(n):
            a, b, c, d = map(int, input().split())
            xs.append(a)
            xs.append(c)
            ys.append(b)
            ys.append(d)
            x_span += c - a
            y_span += d - b

        ans = axis_cost(xs, x_span, n)
        ans += axis_cost(ys, y_span, n)
        out.append(str(ans))

    sys.stdout.write("\n".join(out))

def run(inp: str) -> str:
    global input

    old_stdin = sys.stdin
    old_stdout = sys.stdout

    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()
    input = sys.stdin.readline

    try:
        solve()
        return sys.stdout.getvalue()
    finally:
        sys.stdin = old_stdin
        sys.stdout = old_stdout
        input = sys.stdin.readline

assert run(
    "1\n"
    "2\n"
    "2 2 3 3\n"
    "4 4 5 5\n"
) == "2\n", "provided sample"

assert run(
    "1\n"
    "1\n"
    "5 7 9 11\n"
) == "0\n", "single scanner needs no movement"

assert run(
    "1\n"
    "2\n"
    "1 1 5 5\n"
    "3 3 7 7\n"
) == "0\n", "already overlapping rectangles"

assert run(
    "1\n"
    "2\n"
    "1 1 1 1\n"
    "2 1 2 1\n"
) == "1\n", "touching boundary and off-by-one case"

assert run(
    "1\n"
    "2\n"
    "1 1 1 1\n"
    "1000000000 1000000000 1000000000 1000000000\n"
) == "1999999998\n", "maximum coordinate distance"

n = 100000
maximum_size = (
    "1\n"
    f"{n}\n"
    + ("1000000000 1000000000 1000000000 1000000000\n" * n)
)
assert run(maximum_size) == "0\n", "maximum n with identical rectangles"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 / 1 / 5 7 9 11` | `0` | Minimum-size input and zero movement |
| `1 / 2 / 1 1 5 5 / 3 3 7 7` | `0` | Existing intersection |
| `1 / 2 / 1 1 1 1 / 2 1 2 1` | `1` | Inclusive boundaries and median indexing |
| `1 / 2 / 1 1 1 1 / 1000000000 1000000000 1000000000 1000000000` | `1999999998` | Maximum coordinate values and large answer |
| `1 / 100000 / identical maximum-coordinate rectangles` | `0` | Maximum (n), repeated values, and performance |

## Edge Cases

For a single scanner,

```
1
1
5 7 9 11
```

the horizontal endpoints are (5,9), so the chosen median is (5). Their absolute-distance sum is (4), exactly equal to the rectangle width (9-5=4), giving horizontal cost zero. The vertical calculation behaves identically, so the final answer is `0`. The algorithm never assumes that at least two scanners are present.

For already overlapping rectangles,

```
1
2
1 1 5 5
3 3 7 7
```

the horizontal endpoints are (1,3,5,7), and choosing (x=3) gives an endpoint-distance sum of (8), while the total width is (4+4=8). The horizontal cost is zero. The vertical axis is identical, so the final answer is zero. The rectangle interiors do not need to have the same boundaries, only a common covered square.

For boundary contact,

```
1
2
1 1 1 1
2 1 2 1
```

the horizontal endpoints are (1,1,2,2). The selected median is (1), giving an endpoint-distance sum of (2). Both rectangles have zero width, so the horizontal cost is (2/2=1). Vertically, every endpoint is (1), giving cost zero. Thus the answer is `1`. The use of the closed intervals ([a_i,c_i]) and ([b_i,d_i]) is reflected directly in the distance-to-interval formula.

For a rectangle containing another,

```
1
2
1 1 10 10
5 5 5 5
```

the horizontal endpoints are (1,5,5,10). Choosing the lower median (5) gives distances (4,0,0,5), whose sum is (9). The large rectangle has width (9), so the horizontal movement is ((9-9)/2=0). The same calculation applies vertically. This demonstrates why the full interval, rather than only its center or one endpoint, must be represented.

For the largest coordinate separation,

```
1
2
1 1 1 1
1000000000 1000000000 1000000000 1000000000
```

the horizontal endpoints are (1,1,10^9,10^9). A median can be (1) or (10^9), and the horizontal cost is (999999999). The vertical cost is the same, giving (1999999998). Python's integer arithmetic handles the result directly, and the formula avoids any coordinate iteration.

The most subtle implementation edge case is the even number of endpoints. There are always exactly (2n) endpoints, so there are two middle values. Any point between them minimizes the sum of absolute deviations. Choosing `endpoints[n - 1]` is sufficient, and because every endpoint is an integer, the chosen target coordinate is also a valid grid coordinate. There is no need to average the two middle values, which could introduce an unnecessary fractional coordinate.
