---
title: "CF 102726E - Headquarters"
description: "The problem asks us to locate a new headquarters at the average position of all users. Each city contributes a certain number of users, and every user in that city is considered to be standing at the city's coordinates."
date: "2026-08-01T22:12:16+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102726
codeforces_index: "E"
codeforces_contest_name: "UTPC Contest 9-11-20 Div. 1"
rating: 0
weight: 102726
solve_time_s: 52
verified: true
draft: false
---

[CF 102726E - Headquarters](https://codeforces.com/problemset/problem/102726/E)

**Rating:** -  
**Tags:** -  
**Solve time:** 52s  
**Verified:** yes  

## Solution
## Problem Understanding

The problem asks us to locate a new headquarters at the average position of all users. Each city contributes a certain number of users, and every user in that city is considered to be standing at the city's coordinates. The final location is the weighted average of all city coordinates, where the population value is the weight.

The input describes several cities. A city has an x coordinate, a y coordinate, and a population count. The output is the coordinate of the headquarters, meaning the average x position and average y position of every individual user.

The number of cities is below 1000, and the coordinate and population values are also small. This means even a straightforward O(n) scan is easily fast enough. More complicated approaches such as sorting, searching, or geometry algorithms are unnecessary. The main challenge is not performance, but translating the real world description into the correct mathematical formula.

A common mistake is to compute the average of the city coordinates without considering population. For example, if one city has one user and another city has one thousand users, treating both cities equally gives the wrong center. Another mistake is dividing the x and y sums separately by the number of cities instead of the total population.

For example, consider:

```
2
0 0 1
10 0 9
```

The correct output is:

```
9.0000 0.0000
```

because nine tenths of the users are at x = 10. A careless solution averaging cities would output x = 5.

Another edge case is when all cities have the same position.

```
3
5 7 1
5 7 100
5 7 50
```

The answer must still be:

```
5.0000 7.0000
```

because every user is already at that location. A solution using integer division or unnecessary rounding may lose precision.

## Approaches

The brute force interpretation is to imagine every user individually and average all their coordinates. This is correct because the headquarters is defined as the center of all users. However, expanding the populations is unnecessary. If a city has 999 users, storing 999 identical points only increases work without adding information. The total number of users can also be much larger than the number of cities, so this approach is the wrong representation.

The key observation is that many identical points can be compressed into one weighted point. A city contributes x times its population to the total x coordinate and y times its population to the total y coordinate. After processing all cities, dividing those sums by the total population gives exactly the same result as averaging every user separately.

The brute force works because every user contributes equally, but it fails because it repeats identical work for users from the same city. The observation that cities can be treated as weighted points reduces the entire task to one linear pass.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(total users) | O(total users) | Too slow if populations are expanded |
| Optimal | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the number of cities and initialize three accumulators: the total population, the weighted x coordinate sum, and the weighted y coordinate sum.

The weighted sums represent the combined contribution of every user without explicitly creating separate entries for them.

1. For each city, multiply its x coordinate by its population and add the result to the x sum. Do the same for the y coordinate. Add the population to the total population.

A city with population p is equivalent to p identical users, so its contribution is exactly p copies of its coordinates.

1. After all cities are processed, divide the weighted coordinate sums by the total population.

The resulting values are the coordinates of the center of all users.

1. Print the coordinates with enough decimal precision to satisfy the required error margin.

The calculation uses floating point only at the final division, which avoids unnecessary precision loss.

Why it works:

Every user contributes exactly one copy of their coordinates to the average. A city with population p contributes the same as p separate users at the same location. The algorithm replaces those p identical contributions with one multiplication by p, so the weighted sums are identical to the sums from the expanded list of users. Dividing by the total number of users therefore produces exactly the required average position.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    
    sum_x = 0
    sum_y = 0
    total = 0
    
    for _ in range(n):
        x, y, p = map(int, input().split())
        sum_x += x * p
        sum_y += y * p
        total += p
    
    ans_x = sum_x / total
    ans_y = sum_y / total
    
    print(f"{ans_x:.10f} {ans_y:.10f}")

if __name__ == "__main__":
    solve()
```

The three variables `sum_x`, `sum_y`, and `total` store the complete mathematical information needed for the answer. No city data needs to be saved after it is processed.

Multiplication is performed before addition because each coordinate contribution must be scaled by the population of that city. Python integers handle large intermediate values safely, so there is no overflow concern.

The final division converts the integer weighted sums into floating point coordinates. Printing ten digits after the decimal point gives much more precision than the required margin.

## Worked Examples

For the first example:

```
3
-10 6 4
1 -9 3
8 8 3
```

The trace is:

| City | sum_x | sum_y | total population |
| --- | --- | --- | --- |
| Start | 0 | 0 | 0 |
| -10, 6, 4 | -40 | 24 | 4 |
| 1, -9, 3 | -37 | -3 | 7 |
| 8, 8, 3 | -13 | 21 | 10 |

The final coordinates are:

```
-13 / 10 = -1.3
21 / 10 = 2.1
```

This demonstrates that populations affect the result through the weighted sums.

For a second example:

```
2
0 0 1
10 10 1
```

The trace is:

| City | sum_x | sum_y | total population |
| --- | --- | --- | --- |
| Start | 0 | 0 | 0 |
| 0, 0, 1 | 0 | 0 | 1 |
| 10, 10, 1 | 10 | 10 | 2 |

The answer becomes:

```
5.0000000000 5.0000000000
```

This confirms that when all weights are equal, the formula becomes the normal arithmetic average.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Every city is processed once |
| Space | O(1) | Only three running totals are stored |

The constraints allow a linear scan easily. The algorithm does not depend on the total number of users, only on the number of cities, so it remains efficient even when population values are large.

## Test Cases

```python
import sys
import io

def solve():
    input = sys.stdin.readline
    n_line = input().strip()
    if not n_line:
        return
    n = int(n_line)
    
    sx = sy = total = 0
    for _ in range(n):
        x, y, p = map(int, input().split())
        sx += x * p
        sy += y * p
        total += p
    
    print(f"{sx / total:.10f} {sy / total:.10f}")

def run(inp: str) -> str:
    old = sys.stdin
    sys.stdin = io.StringIO(inp)
    out = io.StringIO()
    old_out = sys.stdout
    sys.stdout = out
    solve()
    sys.stdin = old
    sys.stdout = old_out
    return out.getvalue()

assert run("""3
-10 6 4
1 -9 3
8 8 3
""") == "-1.3000000000 2.1000000000\n", "sample 1"

assert run("""2
0 0 1
10 10 1
""") == "5.0000000000 5.0000000000\n", "sample 2"

assert run("""1
7 -3 100
""") == "7.0000000000 -3.0000000000\n", "single city"

assert run("""2
0 0 1
10 0 9
""") == "9.0000000000 0.0000000000\n", "population weighting"

assert run("""3
5 7 1
5 7 100
5 7 50
""") == "5.0000000000 7.0000000000\n", "all equal positions"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Single city | The same city coordinates | Minimum size handling |
| Two cities with different populations | Weighted position | Population must affect the answer |
| Multiple identical locations | Same location | Avoiding precision and division mistakes |

## Edge Cases

A single city is the smallest possible input:

```
1
7 -3 100
```

The algorithm computes weighted sums of 700 and -300 with total population 100, producing exactly `(7, -3)`. There is no special case because the general formula already handles it.

When one city has a much larger population than another:

```
2
0 0 1
10 0 9
```

the weighted sums become x = 90 and population = 10, so the result is x = 9. This catches implementations that average cities instead of users.

When every city shares the same coordinates:

```
3
5 7 1
5 7 100
5 7 50
```

the weighted sums are simply the same coordinate multiplied by the total population. Dividing returns the original point, so the algorithm naturally handles this case without additional conditions.
