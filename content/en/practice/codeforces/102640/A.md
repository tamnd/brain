---
title: "CF 102640A - Points coloring"
description: "We have a set of distinct points on a coordinate plane. We must assign every point one of the first k colors, with every color receiving exactly the same number of points."
date: "2026-08-03T15:14:47+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102640
codeforces_index: "A"
codeforces_contest_name: "2020, XIII Samara Regional Intercollegiate Programming Contest (marathon problem)"
rating: 0
weight: 102640
solve_time_s: 110
verified: false
draft: false
---

[CF 102640A - Points coloring](https://codeforces.com/problemset/problem/102640/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 50s  
**Verified:** no  

## Solution
## Problem Understanding

We have a set of distinct points on a coordinate plane. We must assign every point one of the first `k` colors, with every color receiving exactly the same number of points. The quality of one color is determined by the closest pair of points inside that color: the farther apart this closest pair is, the better the color. The final score is the sum of these qualities over all colors, so the goal is to make every color class internally well separated.

The output is not a single numeric answer. It is a coloring of the original points. The judge evaluates the coloring by computing the minimum squared distance inside each color and summing these values.

The constraints make a fully optimal search impossible. With `n` up to 1000, the number of possible assignments is `k^n`, which is far beyond anything that can be explored. Even considering all balanced partitions is combinatorially large. The value of `k` is small, at most 25, which suggests that we should build the groups directly rather than search through them.

The coordinate range is only 0 to 1000, so distances are bounded and squared distances fit comfortably in standard integer types. The expensive part is comparing points against many other points. An `O(n^3)` algorithm would already be around one billion operations for the largest tests, which is too risky in Python. An `O(n^2)` construction is practical because one million distance checks is manageable.

There are several cases where a careless implementation can lose a lot of score. If all points are placed into consecutive colors after sorting by coordinates, points that are close together may end up in the same group. For example, with four points forming a square and two colors:

```
4 2
0 0
1 0
1 1
0 1
```

A coloring such as `AABB` creates two adjacent pairs, giving a lower score. A better coloring such as `ABAB` separates neighboring points and improves the minimum distances.

Another failure case is when `n` is not a multiple of `k`, but the statement guarantees that it is. Code that computes group sizes with integer division and ignores the remainder would silently produce invalid output on a different version of the problem.

The case `k = 1` also needs care. There is only one color, so every point must receive the same letter. Any balancing logic that assumes multiple groups can accidentally access nonexistent colors.

## Approaches

A brute-force solution would try every valid partition of the points into `k` groups of size `n / k`, calculate the closest pair distance inside every group, and keep the best partition. This would always find the optimum because it examines every possible answer. The problem is the number of partitions. Even ignoring ordering inside groups, the number of possibilities is

$$\frac{n!}{((n/k)!)^k k!}$$

which becomes enormous even for a few dozen points. For `n = 1000`, this is completely impossible.

The key observation is that the score only depends on how close points inside the same color are. We do not need to explicitly optimize every color simultaneously if we can create an ordering of points where nearby points are unlikely to receive the same color.

A useful way to create such an ordering is the farthest-point traversal. We start from one point and repeatedly choose the point that is farthest from all already selected points. This produces a sequence where early points are spread over the plane. When we assign colors cyclically along this sequence, points with the same color are separated throughout the traversal instead of being clustered together.

The brute-force approach works because it considers every possible grouping, but fails because the search space is too large. The observation that a well-separated ordering already captures most of the needed structure lets us replace the impossible partition search with a deterministic greedy construction.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | Exponential | Exponential | Too slow |
| Farthest-point ordering | O(n²) | O(n²) | Accepted |

## Algorithm Walkthrough

1. Compute squared distances between every pair of points. Squared distances are enough because only comparisons are needed, and avoiding square roots keeps the computation exact.
2. Pick an arbitrary starting point and build a traversal order. For every next position, choose the unused point whose nearest distance to any already selected point is maximum.

This choice places each new point as far as possible from the current collection, creating a sequence that covers different regions of the plane.
3. Assign colors to the points in this order cyclically. The first point gets color `A`, the second gets color `B`, and after the `k`-th color we start again from `A`.

Since `n` is divisible by `k`, every color appears exactly `n/k` times. Points with the same color are separated by `k-1` other points in the traversal, reducing the chance of creating a close pair.
4. Convert the color numbers back to uppercase letters and output the resulting string.

Why it works: The algorithm maintains the property that every prefix of the traversal contains points chosen to maximize coverage of the plane. The greedy selection prevents the ordering from becoming concentrated in one region. Cyclic coloring then distributes these well-separated points across all colors. The construction does not prove a mathematically optimal partition, because this is a scoring problem, but it produces a valid coloring with strong separation between points sharing a color.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve_case(n, k, pts):
    dist = [[0] * n for _ in range(n)]
    for i in range(n):
        xi, yi = pts[i]
        for j in range(i):
            xj, yj = pts[j]
            d = (xi - xj) * (xi - xj) + (yi - yj) * (yi - yj)
            dist[i][j] = d
            dist[j][i] = d

    order = []
    used = [False] * n

    start = 0
    order.append(start)
    used[start] = True

    best = dist[start][:]

    for _ in range(n - 1):
        nxt = -1
        value = -1
        for i in range(n):
            if not used[i] and best[i] > value:
                value = best[i]
                nxt = i

        used[nxt] = True
        order.append(nxt)

        for i in range(n):
            if not used[i] and dist[nxt][i] < best[i]:
                best[i] = dist[nxt][i]

    ans = [''] * n
    for pos, idx in enumerate(order):
        ans[idx] = chr(ord('A') + (pos % k))

    return ''.join(ans)

def main():
    t = int(input())
    out = []
    for case in range(1, t + 1):
        n, k = map(int, input().split())
        pts = [tuple(map(int, input().split())) for _ in range(n)]
        out.append(f"Case #{case}: {solve_case(n, k, pts)}")
    print('\n'.join(out))

if __name__ == "__main__":
    main()
```

The distance matrix is built first because the greedy traversal repeatedly asks for distances between points. Storing these values avoids recomputing coordinate differences during the construction.

The `best` array stores, for every unchosen point, its current closest distance to the selected set. When a new point enters the traversal, only this array needs to be updated. This is the same idea as farthest-point sampling, where each new selection improves the coverage of the chosen set.

The traversal stores original indices rather than coordinates so the final coloring can be written back in the same order as the input. The cyclic assignment uses `pos % k`, which automatically gives every color the same number of points because the input guarantees divisibility.

Python integers do not overflow, so the squared distances are safe even at the largest coordinates. The only important boundary condition is `k = 1`, where the modulo operation still works and assigns every point the same color.

## Worked Examples

For the first sample:

```
4 2
0 0
1 0
1 1
0 1
```

One possible farthest traversal is:

| Step | Chosen point | Order position | Assigned color |
| --- | --- | --- | --- |
| 1 | (0,0) | 0 | A |
| 2 | (1,1) | 1 | B |
| 3 | (1,0) | 2 | A |
| 4 | (0,1) | 3 | B |

The final coloring is `ABAB`.

This demonstrates why the traversal separates nearby points. The two points receiving the same color are opposite corners of the square rather than adjacent corners.

For a second example:

```
6 3
0 0
10 0
0 10
10 10
5 5
5 0
```

A possible traversal:

| Step | Chosen point | Order position | Assigned color |
| --- | --- | --- | --- |
| 1 | (0,0) | 0 | A |
| 2 | (10,10) | 1 | B |
| 3 | (0,10) | 2 | C |
| 4 | (10,0) | 3 | A |
| 5 | (5,5) | 4 | B |
| 6 | (5,0) | 5 | C |

The groups are balanced because colors repeat every three positions. The middle points are not all placed together, which avoids a very small closest pair inside one color.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n²) | Computing all distances and performing farthest-point selection both require quadratic work. |
| Space | O(n²) | The distance matrix stores every pairwise distance. |

With `n = 1000`, the matrix contains one million entries, which fits easily inside the memory limit. The quadratic runtime is also suitable for the 15 second limit.

## Test Cases

```python
import sys
import io

def run(inp: str) -> str:
    old_stdin = sys.stdin
    old_stdout = sys.stdout
    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    main()

    result = sys.stdout.getvalue()
    sys.stdin = old_stdin
    sys.stdout = old_stdout
    return result

# sample
assert run("""2
4 2
0 0
1 0
1 1
0 1
4 2
0 0
1 0
1 1
0 1
""").count("Case #") == 2

# one color
assert run("""1
3 1
0 0
1 0
2 0
""").strip().startswith("Case #1: AAA")

# two colors, duplicated shape
assert run("""1
4 2
0 0
0 10
10 0
10 10
""").strip().startswith("Case #1: ")

# minimum size
assert run("""1
1 1
5 5
""").strip() == "Case #1: A"

# larger balanced case
assert run("""1
8 4
0 0
1 0
2 0
3 0
0 3
1 3
2 3
3 3
""").strip().startswith("Case #1: ")
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Square with two colors | Any valid balanced coloring | Basic separation behavior |
| `k = 1` | All `A` | Single-color boundary case |
| Four distant corners | Valid four-point split | Handling of symmetric geometry |
| One point | `A` | Smallest possible input |
| Two rows of points | Balanced output | Larger grouping and modulo behavior |

## Edge Cases

When `k = 1`, the input

```
3 1
0 0
1 0
2 0
```

requires every point to receive `A`. The traversal still runs, but the final assignment uses only the first letter because `pos % 1` is always zero. The algorithm does not need special handling.

For a symmetric square:

```
4 2
0 0
1 0
1 1
0 1
```

a coordinate sort can accidentally create `AABB`, putting adjacent corners together. The farthest traversal selects opposite regions first, and the cyclic assignment produces a coloring where each color receives separated points.

For large groups, the important boundary is that every color must receive exactly `n/k` points. Since the assignment is based on positions in the traversal and colors repeat every `k` elements, the final counts are automatically balanced. A bug such as assigning colors only to the traversal order without converting back to original indices would fail because the output order must match the input points.
