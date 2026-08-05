---
title: "CF 102498A - \u041f\u0435\u0440\u0435\u0440\u044b\u0432 \u043d\u0430 \u043e\u0431\u0435\u0434"
description: "We have a starting point, a destination point, and several possible restaurants placed on a coordinate plane. The traveler moves at a constant speed of one unit of distance per second and must visit exactly one restaurant before reaching the destination."
date: "2026-08-05T18:19:29+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102498
codeforces_index: "A"
codeforces_contest_name: "\u0418\u043d\u0442\u0435\u0440\u043d\u0435\u0442-\u043e\u043b\u0438\u043c\u043f\u0438\u0430\u0434\u044b, \u0421\u0435\u0437\u043e\u043d 2019-2020, \u041f\u0435\u0440\u0432\u0430\u044f \u043b\u0438\u0447\u043d\u0430\u044f \u043e\u043b\u0438\u043c\u043f\u0438\u0430\u0434\u0430"
rating: 0
weight: 102498
solve_time_s: 199
verified: true
draft: false
---

[CF 102498A - \u041f\u0435\u0440\u0435\u0440\u044b\u0432 \u043d\u0430 \u043e\u0431\u0435\u0434](https://codeforces.com/problemset/problem/102498/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 3m 19s  
**Verified:** yes  

## Solution
## Problem Understanding

We have a starting point, a destination point, and several possible restaurants placed on a coordinate plane. The traveler moves at a constant speed of one unit of distance per second and must visit exactly one restaurant before reaching the destination. Visiting a restaurant adds a fixed waiting time, because eating takes a known number of seconds. The task is to choose the restaurant that gives the smallest total travel time.

For a restaurant at `(x_i, y_i)`, the total time is the distance from the start to that restaurant, plus the eating time, plus the distance from that restaurant to the destination. Since movement speed is one, Euclidean distance directly represents travel time. The answer is the minimum of this value over all restaurants.

The coordinates are bounded by 1000 in absolute value, so distances are at most a few thousand units. The number of restaurants can reach 1000. This is a small enough input size that checking every restaurant once is easily possible. A solution that tries every pair of restaurants would already be unnecessary because the only choice is which single restaurant to visit.

A common mistake is to compare only the direct distance to the destination and ignore the eating time. A farther restaurant with a shorter waiting time can be the best choice.

For example:

```
0 0 10 0
2
5 0 100
8 0 1
```

The first restaurant gives `5 + 100 + 5 = 110`, while the second gives `8 + 1 + 2 = 11`. Choosing the closest restaurant would give the wrong result.

Another edge case is when the best restaurant is not between the starting point and destination. A route can move away first if the restaurant has a sufficiently small eating time.

```
0 0 5 0
1
0 5 1
```

The time is `sqrt(25) + 1 + sqrt(50) = 8.071067811865476`. A solution that only considers restaurants lying on the direct segment would incorrectly reject the only possible restaurant.

Precision also matters. Coordinates are integers, but distances are usually irrational. Printing with normal floating point formatting is enough as long as the calculation uses floating point numbers and enough digits are printed.

## Approaches

The straightforward approach is to examine every restaurant independently. For each one, calculate the distance from the starting point to the restaurant, add the restaurant's eating time, then add the distance from the restaurant to the destination. The smallest value among all restaurants is the answer. This method is correct because every valid journey must choose exactly one restaurant, so checking every possible choice covers the whole solution space.

The brute-force approach already has the same structure as the optimal solution because there is no hidden interaction between restaurants. There is no reason to visit two restaurants, and the cost of visiting one restaurant does not depend on the others. With `n = 1000`, this requires only 1000 distance calculations, which is trivial.

The observation that every restaurant can be evaluated independently lets us reduce the problem to a simple minimum search. The important part is recognizing that there is no pathfinding problem here. The city coordinates do not contain obstacles or restrictions, so the shortest path between any two points is always the straight line segment.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n) | O(1) | Accepted |
| Optimal | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the start point and destination point. Store them because every restaurant calculation needs the same two endpoints.
2. Initialize the answer with a very large value. This represents the best route found so far before any restaurant has been checked.
3. For each restaurant, compute the distance from the start to the restaurant using the Euclidean distance formula. Add the restaurant's eating duration and the distance from the restaurant to the destination.
4. Compare this route length with the current answer and replace the answer if this restaurant gives a smaller total time.
5. Print the final minimum value with enough decimal places to satisfy the precision requirement.

The reason this works is that the only decision in the entire problem is the choice of restaurant. Once a restaurant is chosen, the optimal way to reach it and then leave it is always a straight line because movement is unrestricted. The algorithm checks every possible choice exactly once, so the smallest value it keeps is the true optimal route.

## Python Solution

```python
import sys
import math

input = sys.stdin.readline

def solve():
    xs, ys, xt, yt = map(int, input().split())
    n = int(input())

    ans = float("inf")

    for _ in range(n):
        x, y, t = map(int, input().split())

        first = math.hypot(xs - x, ys - y)
        second = math.hypot(xt - x, yt - y)

        ans = min(ans, first + t + second)

    print("{:.15f}".format(ans))

if __name__ == "__main__":
    solve()
```

The solution directly follows the algorithm. `math.hypot` is used instead of manually computing a square root because it expresses the Euclidean distance formula clearly and avoids unnecessary intermediate code.

The answer starts as infinity so that the first restaurant always replaces it. Every restaurant is processed independently, and no restaurant information needs to be stored after its value has been calculated, which keeps memory usage constant.

The eating time is an integer, but it is added to floating point distances. Python automatically converts the result to a floating point value, preserving the required precision. There is no overflow risk because the coordinate limits make all squared distances very small.

## Worked Examples

For the first sample:

```
0 0 10 0
1
5 0 3
```

| Restaurant | Start distance | Eat time | End distance | Total | Best answer |
| --- | --- | --- | --- | --- | --- |
| (5, 0) | 5 | 3 | 5 | 13 | 13 |

The only possible route goes to the restaurant in the middle, spends three seconds there, and continues to the destination. The trace shows that the algorithm only needs to evaluate one independent option.

For the second sample:

```
0 -5 0 -3
1
0 5 10
```

| Restaurant | Start distance | Eat time | End distance | Total | Best answer |
| --- | --- | --- | --- | --- | --- |
| (0, 5) | 10 | 10 | 8 | 28 | 28 |

The restaurant is not between the start and destination. The algorithm still evaluates it because it does not assume anything about the restaurant location. This confirms that the shortest route may involve moving in any direction before reaching the destination.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Every restaurant is visited once and requires a constant amount of arithmetic. |
| Space | O(1) | Only the current restaurant and the current best answer are stored. |

With at most 1000 restaurants, a linear scan is far below the available limits. The solution performs only a few thousand arithmetic operations and uses a fixed amount of memory.

## Test Cases

```python
import sys
import io
import math

def solve_data(inp: str) -> str:
    old_stdin = sys.stdin
    sys.stdin = io.StringIO(inp)

    import math
    input = sys.stdin.readline

    xs, ys, xt, yt = map(int, input().split())
    n = int(input())

    ans = float("inf")

    for _ in range(n):
        x, y, t = map(int, input().split())
        ans = min(ans,
                  math.hypot(xs - x, ys - y) +
                  t +
                  math.hypot(xt - x, yt - y))

    result = "{:.15f}".format(ans)
    sys.stdin = old_stdin
    return result

assert abs(float(solve_data("""0 0 10 0
1
5 0 3
""")) - 13.0) < 1e-9

assert abs(float(solve_data("""0 -5 0 -3
1
0 5 10
""")) - 28.0) < 1e-9

assert abs(float(solve_data("""0 0 5 5
2
3 3 2
3 4 1
""")) - 8.23606797749979) < 1e-9

assert abs(float(solve_data("""0 0 0 0
1
0 0 1
""")) - 1.0) < 1e-9

assert abs(float(solve_data("""0 0 10 0
2
5 0 100
8 0 1
""")) - 11.0) < 1e-9

assert abs(float(solve_data("""1000 1000 -1000 -1000
1
1000 -1000 1000
""")) - (2000 * math.sqrt(2) + 1000)) < 1e-9
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Start equals destination and restaurant is the same point | 1 | Handles zero travel distance correctly. |
| Two restaurants where the farther one is better | 11 | Prevents choosing only by geometric distance. |
| Coordinates at maximum limits | Large floating point value | Confirms precision handling at boundary coordinates. |

## Edge Cases

The first edge case from the problem understanding is the presence of a nearby but slow restaurant. For:

```
0 0 10 0
2
5 0 100
8 0 1
```

the algorithm evaluates both choices. The first gives `110`, the second gives `11`, so the stored minimum becomes `11`. Since the eating time is included in the same expression as the distances, the algorithm does not fall into the trap of selecting the closest restaurant.

The second edge case is a restaurant outside the direct path:

```
0 0 5 0
1
0 5 1
```

The algorithm computes the distance to the restaurant as `5`, adds the eating time `1`, and adds the final distance `sqrt(50)`. It never filters restaurants by their location, so it correctly returns approximately `8.071067811865476`.

The final edge case is when distances are not integers. For example, the sample with diagonal movement contains square roots. The algorithm keeps all calculations as floating point values and prints fifteen digits after the decimal point, which is enough to satisfy the required error tolerance.
