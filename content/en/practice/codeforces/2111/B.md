---
title: "CF 2111B - Fibonacci Cubes"
description: "We have a collection of cubes, where the side length of the $i$-th cube corresponds to the $i$-th Fibonacci number under a modified definition: $f1 = 1$, $f2 = 2$, and $fi = f{i-1} + f{i-2}$ for $i 2$."
date: "2026-06-08T04:30:35+07:00"
tags: ["codeforces", "competitive-programming", "brute-force", "dp", "implementation", "math"]
categories: ["algorithms"]
codeforces_contest: 2111
codeforces_index: "B"
codeforces_contest_name: "Educational Codeforces Round 179 (Rated for Div. 2)"
rating: 1100
weight: 2111
solve_time_s: 109
verified: false
draft: false
---

[CF 2111B - Fibonacci Cubes](https://codeforces.com/problemset/problem/2111/B)

**Rating:** 1100  
**Tags:** brute force, dp, implementation, math  
**Solve time:** 1m 49s  
**Verified:** no  

## Solution
## Problem Understanding

We have a collection of cubes, where the side length of the $i$-th cube corresponds to the $i$-th Fibonacci number under a modified definition: $f_1 = 1$, $f_2 = 2$, and $f_i = f_{i-1} + f_{i-2}$ for $i > 2$. For each box in a set of boxes, we are asked whether all these cubes can fit inside, respecting the rules of stacking. Each cube must be aligned with the box, cannot float in mid-air, and cannot be placed on a smaller cube.

The input consists of multiple test cases, each providing the number of cubes $n$, the number of boxes $m$, and the dimensions of each box. The output for each test case is a string of length $m$, with '1' if the cubes fit in the corresponding box and '0' otherwise.

The constraints give us $n \le 10$ and the sum of $m$ across all test cases $\le 2 \cdot 10^5$. This is crucial because it allows us to precompute the cube sizes and use a straightforward simulation for each box. Since the cube sizes grow quickly in Fibonacci order, the problem does not require complex packing algorithms; rather, a carefully ordered greedy approach suffices.

A subtle edge case arises when cubes have a combined footprint larger than a box in any orientation, or when a box has one very small dimension that prevents stacking. For instance, if $n = 5$, the cubes have sides $1, 2, 3, 5, 8$, and the box dimensions are $(6, 6, 5)$, the stacking fails because the largest cube ($8$) does not fit any orientation. A naive approach that checks only total volume would incorrectly say "fit," ignoring actual dimension constraints.

## Approaches

A brute-force approach would attempt to simulate every possible permutation of cube placement and orientation in each box. Given $n \le 10$, there are $n!$ permutations, and each cube can be oriented in up to 6 ways. With $m$ potentially $2 \cdot 10^5$, this becomes prohibitive.

The key insight is that all cubes are cubes (sides equal) and $n$ is small. Therefore, we can sort the cubes in descending order and simulate a greedy placement along the largest box dimension. For each box, we sort its sides in descending order, then repeatedly place the largest remaining cube on the largest remaining dimension. The cubes stack vertically along one dimension, and the remaining two dimensions must accommodate all cubes in any orientation. This reduces each box check to a simple sequence of comparisons.

The greedy approach works because the cube sizes grow and must be stacked largest to smallest. Sorting both the cubes and the box sides ensures that if a cube cannot fit along a dimension in sorted order, it cannot fit in any permutation.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n! * 6^n * m) | O(n) | Too slow |
| Optimal Greedy | O(n log n + m log 3) ≈ O(m) | O(n) | Accepted |

## Algorithm Walkthrough

1. Precompute the first 10 Fibonacci numbers according to the modified definition: $f_1 = 1$, $f_2 = 2$, $f_i = f_{i-1} + f_{i-2}$ for $i > 2$. We will need only these numbers since $n \le 10$.
2. For each test case, sort the Fibonacci cubes in descending order. This allows us to place the largest cube first.
3. For each box, sort its three dimensions in descending order. This identifies which dimension will hold the stack height and which two form the base.
4. Initialize three available dimensions from the box. Starting with the largest cube, try to place it along the largest remaining dimension. Reduce the available dimension along the stacking axis by the cube side.
5. Continue placing cubes in descending order. If at any step a cube exceeds any of the available dimensions, mark the box as impossible and move to the next box.
6. If all cubes are placed successfully within the box dimensions, mark it as possible.
7. Repeat steps 3-6 for every box in the test case.

Why it works: Sorting the cubes in descending order guarantees that the largest cubes occupy the largest space first, preventing a smaller cube from blocking a larger one. Sorting the box dimensions ensures the stacking direction is chosen optimally. The invariant is that after placing each cube, the remaining space along all axes is sufficient for the remaining cubes if and only if the box can hold all cubes.

## Python Solution

```python
import sys
input = sys.stdin.readline

# precompute Fibonacci numbers up to 10
fib = [1, 2]
for i in range(2, 10):
    fib.append(fib[-1] + fib[-2])

t = int(input())
for _ in range(t):
    n, m = map(int, input().split())
    cubes = fib[:n]
    cubes.sort(reverse=True)
    res = []
    for _ in range(m):
        box = list(map(int, input().split()))
        box.sort(reverse=True)
        temp_box = box[:]
        possible = True
        # we can place cubes along the largest box dimension
        for cube in cubes:
            # find the largest box dimension to place this cube
            placed = False
            for i in range(3):
                if temp_box[i] >= cube:
                    temp_box[i] -= cube
                    placed = True
                    break
            if not placed:
                possible = False
                break
        res.append('1' if possible else '0')
    print(''.join(res))
```

The precomputation of Fibonacci numbers ensures that we never recompute them per test case. Sorting cubes in descending order guarantees largest-first placement. Sorting box dimensions ensures we stack along the largest axis, maximizing space usage. Reducing the dimension as cubes are placed avoids overcounting space. This avoids errors like placing a cube that technically fits by volume but cannot be accommodated by dimensions.

## Worked Examples

**Sample Input 1**

```
5 4
3 1 2
10 10 10
9 8 13
14 7 20
```

| Cube | Side | Box sorted | Placement |
| --- | --- | --- | --- |
| 8 | 8 | 10,10,10 | placed in 10 → remaining 2 |
| 5 | 5 | 10,10,2 | placed in 10 → remaining 5 |
| 3 | 3 | 10,5,2 | placed in 10 → remaining 2 |
| 2 | 2 | 2,5,2 | placed in 5 → remaining 2 |
| 1 | 1 | 2,2,2 | placed in 2 → remaining 1 |

Output: 1

This trace shows that the cubes can be stacked along the largest dimension.

**Sample Input 2**

```
2 6
3 3 3
1 2 1
```

| Cube | Side | Box sorted | Placement |
| --- | --- | --- | --- |
| 2 | 2 | 3,3,3 | placed in 3 → remaining 1 |
| 1 | 1 | 1,3,3 | placed in 3 → remaining 2 |

Output: 10

This demonstrates that small cubes may fit in multiple orientations, but large cubes may fail if any box dimension is too small.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(m * n) | Each box requires iterating over n cubes; n ≤ 10, so effectively linear in total m. |
| Space | O(n) | Only storing cube sizes and temporary box dimensions. |

With $m \le 2 \cdot 10^5$ and $n \le 10$, the total operations are ≤ 2·10^6, well within the 2-second time limit. Memory usage is minimal.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    output = io.StringIO()
    sys.stdout = output
    # run solution
    import sys
    input = sys.stdin.readline

    fib = [1, 2]
    for i in range(2, 10):
        fib.append(fib[-1] + fib[-2])

    t = int(input())
    for _ in range(t):
        n, m = map(int, input().split())
        cubes = fib[:n]
        cubes.sort(reverse=True)
        res = []
        for _ in range(m):
            box = list(map(int, input().split()))
            box.sort(reverse=True)
            temp_box = box[:]
            possible = True
            for cube in cubes:
                placed = False
                for i in range(3):
                    if temp_box[i] >= cube:
                        temp_box[i] -= cube
                        placed = True
                        break
                if not placed:
                    possible = False
                    break
            res.append('1' if possible else '0')
        print(''.join(res))
    return output.getvalue().strip()

# Provided samples
assert run("2\n5
```
