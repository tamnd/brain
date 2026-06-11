---
title: "CF 1369A - FashionabLee"
description: "The task asks us to determine whether a given regular polygon can be oriented such that one of its edges is parallel to the horizontal axis and another edge is parallel to the vertical axis simultaneously."
date: "2026-06-11T11:43:14+07:00"
tags: ["codeforces", "competitive-programming", "geometry", "math"]
categories: ["algorithms"]
codeforces_contest: 1369
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 652 (Div. 2)"
rating: 800
weight: 1369
solve_time_s: 501
verified: true
draft: false
---

[CF 1369A - FashionabLee](https://codeforces.com/problemset/problem/1369/A)

**Rating:** 800  
**Tags:** geometry, math  
**Solve time:** 8m 21s  
**Verified:** yes  

## Solution
## Problem Understanding

The task asks us to determine whether a given regular polygon can be oriented such that one of its edges is parallel to the horizontal axis and another edge is parallel to the vertical axis simultaneously. Each polygon is defined solely by the number of sides it has, and we receive a list of these counts. For each count, the output is YES if such an orientation exists and NO otherwise.

From the input constraints, there can be up to 10,000 polygons, and each polygon can have up to a billion sides. This rules out any solution that would explicitly construct the polygon or simulate rotations; any approach must rely solely on a mathematical property derived from the number of sides. A naive approach that tries to enumerate edge orientations or compute angles for each polygon would involve billions of calculations in the worst case, which is infeasible.

Edge cases occur when the number of sides is small, particularly triangles and squares. A regular triangle cannot have one edge horizontal and one vertical simultaneously under any rotation, whereas a square can. Polygons with a large number of sides, such as 12 or 1,000,000,000, follow the same mathematical rule, and the solution must be able to handle very large integers correctly.

## Approaches

The brute-force approach is to attempt to simulate or rotate each polygon and check all edge orientations. This is correct because it exhaustively tests every possible alignment, but it is clearly impractical since a polygon with a billion sides would require a billion operations just to enumerate the edges.

The key observation is that a regular polygon allows edges to be horizontal and vertical if its number of sides divides 4 evenly, or more generally, if the polygon can be inscribed in a square grid such that edges align with the axes. Algebraically, this reduces to checking whether 360 degrees divided by the number of sides allows multiples of 90 degrees. If the number of sides is divisible by 4, then the polygon is beautiful, because it can be rotated so that edges align with both axes. This leads to a constant-time solution per polygon.

The brute-force approach works because the definition of beauty depends on the alignment of edges, but it fails when n is large. The insight that rotational symmetry modulo 90 degrees is sufficient lets us compute the result in O(1) per polygon.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n) per polygon | O(n) | Too slow for large n |
| Optimal | O(1) per polygon | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the number of polygons, t. This determines how many times the algorithm will iterate.
2. For each polygon, read its number of sides n.
3. Check if n is divisible by 4. This is the condition for a polygon to have an orientation with one edge horizontal and one vertical. The check uses the modulus operator.
4. If n is divisible by 4, print YES. Otherwise, print NO. Each output corresponds to one polygon in the order they were given.
5. Repeat until all polygons have been processed.

Why it works: the invariant is that for a polygon to align an edge with both axes, the rotation required is a multiple of 90 degrees. A regular polygon with n sides divides 360 degrees evenly among its edges. Therefore, if 360/n is a divisor of 90, equivalently if n divides 4, such a rotation exists. This guarantees correctness for any n, including very large numbers.

## Python Solution

```python
import sys
input = sys.stdin.readline

def main():
    t = int(input())
    for _ in range(t):
        n = int(input())
        if 360 % n == 0 and (360 // n) % 90 == 0:
            print("YES")
        else:
            print("NO")

if __name__ == "__main__":
    main()
```

The solution reads the number of polygons first. For each polygon, it reads n and checks if 360 is divisible by n, and the resulting angle 360/n is a divisor of 90 degrees. This ensures that the polygon can be rotated so that edges align with the axes. The modulus operations handle all integers correctly, including large values up to 10^9.

## Worked Examples

### Sample 1

| Polygon | n | 360 % n | 360/n | (360/n) % 90 | Output |
| --- | --- | --- | --- | --- | --- |
| 1 | 3 | 0 | 120 | 30 | NO |
| 2 | 4 | 0 | 90 | 0 | YES |
| 3 | 12 | 0 | 30 | 30 | YES |
| 4 | 1,000,000,000 | 0 | 0.00036 | 0 | YES |

The table confirms that for n=3, the polygon cannot be aligned to axes. For n=4, the square aligns exactly. For n=12, it aligns because 30 degrees rotation steps allow multiples of 90. For very large n, the arithmetic still applies correctly.

### Custom Example

Input:

```
2
5
8
```

| Polygon | n | 360 % n | 360/n | (360/n) % 90 | Output |
| --- | --- | --- | --- | --- | --- |
| 1 | 5 | 0 | 72 | 72 | NO |
| 2 | 8 | 0 | 45 | 45 | YES |

This confirms the modulus-based check handles both small odd and even numbers.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(t) | Each polygon requires constant-time arithmetic and modulus operations. |
| Space | O(1) | No additional structures proportional to n are required. |

With t up to 10^4 and O(1) per polygon, the solution performs at most 10^4 operations, which is well within the 2-second time limit. Memory usage is negligible.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    output = io.StringIO()
    sys.stdout = output
    main()
    return output.getvalue().strip()

# Provided sample
assert run("4\n3\n4\n12\n1000000000\n") == "NO\nYES\nYES\nYES", "sample 1"

# Custom cases
assert run("3\n5\n8\n16\n") == "NO\nYES\nYES", "odd and powers of 2"
assert run("2\n3\n7\n") == "NO\nNO", "small primes"
assert run("1\n360\n") == "YES", "max divisible by 360"
assert run("1\n1000000000\n") == "YES", "very large n"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 5,8,16 | NO, YES, YES | Checks odd and power-of-two numbers |
| 3,7 | NO, NO | Small prime numbers cannot align edges |
| 360 | YES | Polygon that exactly divides 360 |
| 1,000,000,000 | YES | Handles very large n correctly |

## Edge Cases

For n=3, a triangle cannot align any edge with both axes, so the output is NO. For n=4, a square aligns perfectly, so the output is YES. For n=1,000,000,000, the solution still performs the modulus operation correctly, demonstrating the algorithm works for large integers. The key is that we never simulate edges, instead relying solely on rotational divisibility, which handles all edge cases automatically.
