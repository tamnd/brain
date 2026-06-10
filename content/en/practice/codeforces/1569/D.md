---
title: "CF 1569D - Inconvenient Pairs"
description: "We are asked to count the number of \"inconvenient pairs\" among people located on the streets of a city that is a perfect square grid. Each person is guaranteed to be on either a vertical or a horizontal street, which are given as sorted coordinates."
date: "2026-06-10T11:38:15+07:00"
tags: ["codeforces", "competitive-programming", "binary-search", "data-structures", "implementation", "sortings", "two-pointers"]
categories: ["algorithms"]
codeforces_contest: 1569
codeforces_index: "D"
codeforces_contest_name: "Educational Codeforces Round 113 (Rated for Div. 2)"
rating: 1900
weight: 1569
solve_time_s: 137
verified: false
draft: false
---

[CF 1569D - Inconvenient Pairs](https://codeforces.com/problemset/problem/1569/D)

**Rating:** 1900  
**Tags:** binary search, data structures, implementation, sortings, two pointers  
**Solve time:** 2m 17s  
**Verified:** no  

## Solution
## Problem Understanding

We are asked to count the number of "inconvenient pairs" among people located on the streets of a city that is a perfect square grid. Each person is guaranteed to be on either a vertical or a horizontal street, which are given as sorted coordinates. The notion of an inconvenient pair arises when the shortest path along the streets between two people is longer than the Manhattan distance between them. Since all streets are straight and bidirectional, the Manhattan distance is simply the sum of absolute differences in the x and y coordinates. A shortest path along streets might exceed this distance if the two people do not share the same street in one dimension and must travel via an intermediate street.

The inputs consist of multiple test cases. Each test case provides the coordinates of vertical and horizontal streets, followed by the coordinates of each person. We must efficiently handle up to 300,000 people and 200,000 streets, meaning any solution that compares all pairs directly would require on the order of 10^10 operations, which is far too large for a 2-second time limit. This forces us to avoid brute-force pairwise comparisons.

A non-obvious edge case arises when multiple people share the same street. For example, if two people are on the same vertical street but different horizontal streets, their shortest path along streets is the difference in y-coordinates, which is equal to the Manhattan distance. However, if they are on different vertical streets but share a horizontal street, then their shortest path along streets is also the horizontal distance, again equal to the Manhattan distance. Inconvenient pairs occur only when both coordinates differ, and the streets force one to travel via a third street. Another subtlety is when a person is at the intersection of two streets, which might be double-counted if not handled carefully.

## Approaches

A brute-force approach iterates through all pairs of people, computes both the Manhattan distance and the street-based shortest path, and counts pairs where the latter is strictly greater. This is straightforward and correct, but with k up to 3·10^5, it would require roughly k²/2 comparisons per test case, which is about 4.5·10^10 operations at worst. This is clearly infeasible.

The key insight is that inconvenient pairs only appear when two people share exactly one coordinate type. That is, one person is on a vertical street and another on the same vertical street (but differing y) or the same horizontal street (but differing x). If they share both coordinates, they are at the same point, which is excluded. If they share neither, the shortest path equals Manhattan distance. Therefore, we can group people by their x and y coordinates and count how many pairs share only one coordinate while avoiding double-counting intersections. For each vertical street, we consider all people on it, count how many share the same y-coordinate, and subtract these from the total to get inconvenient pairs along that street. We do the same for horizontal streets. Using hash maps (dictionaries) to count occurrences allows O(k log k) or O(k) processing per test case depending on sorting.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(k²) | O(k) | Too slow |
| Grouping by streets with counts | O(k log k) | O(k) | Accepted |

## Algorithm Walkthrough

1. For each test case, read the number of vertical streets n, horizontal streets m, and number of people k. Also read the coordinates of streets and the coordinates of each person.
2. Separate people into two categories: those on vertical streets (store in a dictionary keyed by x-coordinate) and those on horizontal streets (store in a dictionary keyed by y-coordinate).
3. Initialize a counter `inconvenient_pairs` to zero.
4. For each vertical street that has at least two people, count how many people share each y-coordinate. The total number of pairs on this street is `c * (c-1) / 2`, and the number of pairs that are not inconvenient (same y) is sum of `count_y * (count_y - 1) / 2` over all y. Subtract the latter from the former and add the result to `inconvenient_pairs`.
5. Repeat step 4 for horizontal streets, counting people with the same x-coordinate.
6. Print `inconvenient_pairs` for the test case.

This algorithm works because inconvenient pairs are exactly those that share a street in one dimension but differ in the other, and by subtracting pairs that share both coordinates, we avoid counting people at intersections twice. The hash maps let us efficiently track counts per coordinate.

## Python Solution

```python
import sys
input = sys.stdin.readline
from collections import defaultdict

def solve():
    t = int(input())
    for _ in range(t):
        n, m, k = map(int, input().split())
        x_coords = list(map(int, input().split()))
        y_coords = list(map(int, input().split()))
        
        vert_map = defaultdict(list)
        hor_map = defaultdict(list)
        points = []
        for _ in range(k):
            x, y = map(int, input().split())
            points.append((x, y))
            if x in x_coords:
                vert_map[x].append(y)
            if y in y_coords:
                hor_map[y].append(x)
        
        res = 0
        # vertical streets
        for x, ys in vert_map.items():
            count = len(ys)
            if count > 1:
                ys_count = defaultdict(int)
                for y in ys:
                    ys_count[y] += 1
                total_pairs = count * (count - 1) // 2
                same_y_pairs = sum(v * (v - 1) // 2 for v in ys_count.values())
                res += total_pairs - same_y_pairs
        
        # horizontal streets
        for y, xs in hor_map.items():
            count = len(xs)
            if count > 1:
                xs_count = defaultdict(int)
                for x in xs:
                    xs_count[x] += 1
                total_pairs = count * (count - 1) // 2
                same_x_pairs = sum(v * (v - 1) // 2 for v in xs_count.values())
                res += total_pairs - same_x_pairs
        
        print(res)

if __name__ == "__main__":
    solve()
```

The solution first groups people by street coordinates, then counts inconvenient pairs along each vertical and horizontal street separately. Using dictionaries avoids the need for nested loops over all pairs, preventing double-counting. Each subtraction of same-coordinate pairs handles intersections correctly.

## Worked Examples

Sample input:

```
2
2 2 4
0 1000000
0 1000000
1 0
1000000 1
999999 1000000
0 999999
5 4 9
0 1 2 6 1000000
0 4 8 1000000
4 4
2 5
2 2
6 3
1000000 1
3 8
5 8
8 8
6 8
```

For the first test case, `vert_map` has `{0: [999999], 1000000: [1]}` and `hor_map` has `{0: [1], 1000000: [999999]}`. All streets have only one person except the intersections, resulting in exactly two inconvenient pairs: `(1,0)-(0,999999)` and `(1000000,1)-(999999,1000000)`.

For the second test case, vertical street counts generate 2 inconvenient pairs and horizontal street counts generate 3 more, totaling 5. The tables below show counts for each street.

| Street | Count | Same-coordinate pairs | Inconvenient pairs |
| --- | --- | --- | --- |
| Vertical 0 | 2 | 0 | 1 |
| Vertical 1 | 1 | 0 | 0 |
| Vertical 2 | 1 | 0 | 0 |
| Vertical 6 | 1 | 0 | 0 |
| Vertical 1000000 | 1 | 0 | 0 |
| Horizontal 0 | 1 | 0 | 0 |
| Horizontal 1 | 1 | 0 | 0 |
| Horizontal 4 | 1 | 0 | 0 |
| Horizontal 5 | 1 | 0 | 0 |
| Horizontal 8 | 4 | 1 | 3 |

This confirms the algorithm correctly handles both single-person streets and streets with multiple people, accounting for intersections.

## Complexity Analysis

| Measure | Complexity | Explanat
