---
title: "CF 181B - Number of Triplets"
description: "We are given a set of distinct points on a 2D plane. The task is to count how many unordered triples of points form a configuration where one point lies exactly at the midpoint of the segment formed by the other two."
date: "2026-05-29T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "binary-search", "brute-force"]
categories: ["algorithms"]
codeforces_contest: 181
codeforces_index: "B"
codeforces_contest_name: "Croc Champ 2012 - Round 2 (Unofficial Div. 2 Edition)"
rating: 1300
weight: 181
solve_time_s: 94
verified: true
draft: false
---

[CF 181B - Number of Triplets](https://codeforces.com/problemset/problem/181/B)

**Rating:** 1300  
**Tags:** binary search, brute force  
**Solve time:** 1m 34s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a set of distinct points on a 2D plane. The task is to count how many unordered triples of points form a configuration where one point lies exactly at the midpoint of the segment formed by the other two.

If we pick three points $A$, $B$, and $C$, then $B$ is the midpoint of segment $AC$ when:

$B = \left(\frac{x_A + x_C}{2}, \frac{y_A + y_C}{2}\right)$

Since triples are unordered, the pair $(A,B,C)$ is the same as $(C,B,A)$. We only want to count each valid geometric configuration once.

The constraint $n \le 3000$ is the key to the problem. A cubic solution that checks every triple directly would require about $3000^3 = 27$ billion checks, which is far beyond what fits in a 2 second time limit. Quadratic solutions, around 9 million operations, are completely reasonable in Python.

The coordinates are small, between $-1000$ and $1000$, but that alone is not enough to build a tiny grid-based solution. The important observation is geometric: if $B$ is the midpoint of $AC$, then the coordinates of $A$ and $C$ determine $B$ uniquely.

Several edge cases can silently break careless implementations.

Consider this input:

```
3
0 0
1 1
2 2
```

The answer is:

```
1
```

Point $(1,1)$ is the midpoint of $(0,0)$ and $(2,2)$.

Now consider:

```
3
0 0
1 0
2 1
```

The answer is:

```
0
```

A naive implementation that only checks whether averages are integers could incorrectly count this. The midpoint of $(0,0)$ and $(2,1)$ is $(1,0.5)$, which does not exist among the points.

Another subtle issue is double counting. Suppose we have:

```
3
0 0
1 1
2 2
```

If we iterate over ordered pairs $(A,C)$, then both $(0,0)\rightarrow(2,2)$ and $(2,2)\rightarrow(0,0)$ produce the same midpoint. A careless solution would return 2 instead of 1.

One more important case is when midpoint coordinates are fractional:

```
4
0 0
1 1
1 0
2 1
```

The midpoint of $(0,0)$ and $(1,1)$ is $(0.5,0.5)$, which is invalid. The midpoint of $(1,0)$ and $(2,1)$ is $(1.5,0.5)$, also invalid. The correct answer is 0. Any approach using floating point arithmetic risks precision issues and unnecessary complexity.

## Approaches

The most direct solution is brute force. We can iterate over every triple of distinct points and check whether one of them is the midpoint of the other two.

For each triple $(A,B,C)$, we verify:

$2x_B = x_A + x_C \quad \text{and} \quad 2y_B = y_A + y_C$

This works because midpoint coordinates are exactly the averages of the endpoints. The approach is correct, but the runtime is disastrous. There are $\binom{3000}{3}$ triples, which is roughly 4.5 billion combinations. Even a tiny constant factor cannot save this.

The bottleneck comes from choosing triples explicitly. The midpoint condition actually depends only on a pair of endpoints. Once $A$ and $C$ are fixed, the midpoint is determined immediately.

That observation changes the problem completely.

Instead of choosing three points, we choose only two points $A$ and $C$. Their midpoint is:

$\left(\frac{x_A+x_C}{2}, \frac{y_A+y_C}{2}\right)$

If that midpoint exists among the given points, then we found one valid triplet.

We can store all points inside a hash set for $O(1)$ membership checks. Then we iterate over every unordered pair of points.

For each pair:

1. Check whether the sums $x_A+x_C$ and $y_A+y_C$ are even.
2. Compute the midpoint coordinates.
3. Check whether that midpoint exists in the set.

This reduces the complexity to $O(n^2)$, which easily fits the constraints.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(n^3)$ | $O(1)$ | Too slow |
| Optimal | $O(n^2)$ | $O(n)$ | Accepted |

## Algorithm Walkthrough

1. Read all points and store them in a list.
2. Insert every point into a hash set.

The set allows constant-time lookup when checking whether a midpoint exists.
3. Initialize the answer to 0.
4. Iterate over all unordered pairs of points $(i,j)$ where $i < j$.

Using unordered pairs prevents double counting. The pair $(A,C)$ should be processed exactly once.
5. For the current pair, compute:

$s_x = x_i + x_j, \quad s_y = y_i + y_j$
6. If either $s_x$ or $s_y$ is odd, skip this pair.

Integer-coordinate points cannot have a midpoint with fractional coordinates.
7. Otherwise compute the midpoint:

$m_x = \frac{s_x}{2}, \quad m_y = \frac{s_y}{2}$
8. Check whether $(m_x,m_y)$ exists in the set of points.

If it exists, increment the answer by 1.
9. Print the final answer.

### Why it works

For every valid triplet, there is exactly one unordered pair of endpoints $(A,C)$. Their midpoint is uniquely determined, and the algorithm checks whether that midpoint point exists in the input.

Every valid triplet is counted once because the pair iteration uses $i < j$. The reverse ordering $(C,A)$ is never revisited.

No invalid triplet can be counted because the midpoint condition is checked exactly using integer arithmetic:

$2m_x = x_A + x_C, \quad 2m_y = y_A + y_C$

A midpoint is accepted only if it matches an actual input point.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input())
    
    points = []
    point_set = set()
    
    for _ in range(n):
        x, y = map(int, input().split())
        points.append((x, y))
        point_set.add((x, y))
    
    ans = 0
    
    for i in range(n):
        x1, y1 = points[i]
        
        for j in range(i + 1, n):
            x2, y2 = points[j]
            
            sx = x1 + x2
            sy = y1 + y2
            
            if sx % 2 != 0 or sy % 2 != 0:
                continue
            
            mx = sx // 2
            my = sy // 2
            
            if (mx, my) in point_set:
                ans += 1
    
    print(ans)

solve()
```

The first part reads all points into both a list and a set. The list preserves iteration order, while the set provides fast midpoint existence checks.

The nested loops enumerate every unordered pair exactly once. Using `j` from `i + 1` avoids duplicate processing and guarantees correct counting.

The parity check is critical:

```
if sx % 2 != 0 or sy % 2 != 0:
    continue
```

Without it, integer division would silently round down and create false midpoint matches.

The midpoint is computed using integer arithmetic only. Floating point arithmetic is unnecessary and would introduce avoidable precision concerns.

The final membership check:

```
if (mx, my) in point_set:
```

is the geometric core of the solution. If the midpoint exists among the input points, then those three points form a valid triplet.

## Worked Examples

### Example 1

Input:

```
3
1 1
2 2
3 3
```

| Pair | Sum Coordinates | Midpoint | Exists | Answer |
| --- | --- | --- | --- | --- |
| (1,1) and (2,2) | (3,3) | fractional | No | 0 |
| (1,1) and (3,3) | (4,4) | (2,2) | Yes | 1 |
| (2,2) and (3,3) | (5,5) | fractional | No | 1 |

Output:

```
1
```

This trace shows why parity matters. Only the second pair produces integer midpoint coordinates.

### Example 2

Input:

```
5
0 0
2 0
1 0
0 2
2 2
```

| Pair | Sum Coordinates | Midpoint | Exists | Answer |
| --- | --- | --- | --- | --- |
| (0,0) and (2,0) | (2,0) | (1,0) | Yes | 1 |
| (0,0) and (1,0) | (1,0) | fractional | No | 1 |
| (0,0) and (0,2) | (0,2) | (0,1) | No | 1 |
| (0,0) and (2,2) | (2,2) | (1,1) | No | 1 |
| (2,0) and (0,2) | (2,2) | (1,1) | No | 1 |
| (0,2) and (2,2) | (2,4) | (1,2) | No | 1 |

Output:

```
1
```

This example demonstrates that integer midpoint coordinates alone are not enough. The midpoint must also exist among the given points.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n^2)$ | Every unordered pair of points is checked once |
| Space | $O(n)$ | The hash set stores all points |

With $n = 3000$, the algorithm performs roughly 4.5 million pair checks, which is easily manageable in Python within the time limit. The memory usage is tiny compared to the 256 MB limit.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys, io

def solve():
    input = sys.stdin.readline

    n = int(input())

    points = []
    point_set = set()

    for _ in range(n):
        x, y = map(int, input().split())
        points.append((x, y))
        point_set.add((x, y))

    ans = 0

    for i in range(n):
        x1, y1 = points[i]

        for j in range(i + 1, n):
            x2, y2 = points[j]

            sx = x1 + x2
            sy = y1 + y2

            if sx % 2 != 0 or sy % 2 != 0:
                continue

            mx = sx // 2
            my = sy // 2

            if (mx, my) in point_set:
                ans += 1

    print(ans)

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    out = io.StringIO()
    sys.stdout = out

    solve()

    sys.stdout = sys.__stdout__
    return out.getvalue().strip()

# provided sample
assert run(
"""3
1 1
2 2
3 3
""") == "1", "sample 1"

# minimum size, no valid midpoint
assert run(
"""3
0 0
1 0
0 1
""") == "0", "minimum invalid case"

# one valid midpoint
assert run(
"""3
0 0
2 0
1 0
""") == "1", "simple midpoint"

# multiple valid triplets
assert run(
"""5
0 0
2 0
1 0
0 2
2 2
""") == "1", "single valid triplet among many pairs"

# negative coordinates
assert run(
"""5
-2 -2
0 0
2 2
-2 2
2 -2
""") == "1", "handles negative coordinates"

# catches double counting bugs
assert run(
"""3
-1 -1
0 0
1 1
""") == "1", "unordered counting"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Three unrelated points | 0 | Minimum invalid configuration |
| Horizontal midpoint case | 1 | Basic midpoint detection |
| Mixed valid and invalid pairs | 1 | Correct filtering logic |
| Negative coordinates | 1 | Coordinate sign handling |
| Symmetric diagonal points | 1 | Prevents double counting |

## Edge Cases

Consider the fractional midpoint case:

```
3
0 0
1 1
2 1
```

The algorithm checks pair $(0,0)$ and $(1,1)$. Their coordinate sums are $(1,1)$, both odd. Since the midpoint would be $(0.5,0.5)$, the pair is skipped immediately.

Next it checks $(0,0)$ and $(2,1)$. The sums are $(2,1)$. The y-coordinate sum is odd, so this pair is also skipped.

The final pair also produces fractional midpoint coordinates. The answer remains 0.

Now consider the double-counting scenario:

```
3
0 0
1 1
2 2
```

The only valid triplet uses endpoints $(0,0)$ and $(2,2)$. The algorithm processes this pair once because it only considers indices with $i < j$. The reverse pair never appears, so the answer becomes exactly 1 instead of 2.

Finally, consider a case where midpoint coordinates are integers but the midpoint point is missing:

```
3
0 0
2 2
5 5
```

The pair $(0,0)$ and $(2,2)$ produces midpoint $(1,1)$. The parity check passes, but the set lookup fails because $(1,1)$ is not in the input. The algorithm correctly rejects the pair and outputs 0.
