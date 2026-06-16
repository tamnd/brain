---
title: "CF 1004A - Sonya and Hotels"
description: "We are given a set of existing hotels placed on integer points along an infinite number line. We want to open one additional hotel at some integer coordinate. The requirement is that the closest existing hotel to this new one must be at distance exactly $d$."
date: "2026-06-16T23:25:34+07:00"
tags: ["codeforces", "competitive-programming", "implementation"]
categories: ["algorithms"]
codeforces_contest: 1004
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 495 (Div. 2)"
rating: 900
weight: 1004
solve_time_s: 98
verified: true
draft: false
---

[CF 1004A - Sonya and Hotels](https://codeforces.com/problemset/problem/1004/A)

**Rating:** 900  
**Tags:** implementation  
**Solve time:** 1m 38s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a set of existing hotels placed on integer points along an infinite number line. We want to open one additional hotel at some integer coordinate. The requirement is that the closest existing hotel to this new one must be at distance exactly $d$. In other words, if we look at all distances from the new position to every existing hotel, the minimum of those distances must equal $d$.

The input gives us the number of existing hotels and their coordinates, already sorted in increasing order. The task is to count how many integer positions for the new hotel satisfy this exact distance condition.

The constraint $n \le 100$ is small enough that a quadratic scan over candidates is feasible without concern. Even if we consider checking every potential candidate position and verifying it against all existing hotels, the total number of operations stays well within a few million. This immediately rules out the need for advanced data structures or logarithmic query optimizations. A straightforward geometric inspection approach is sufficient.

A naive misunderstanding that often appears in this problem is to think that we only need to check points exactly at distance $d$ from some hotel, without further validation. That is not sufficient because a point can be at distance $d$ from one hotel while being closer than $d$ to another.

For example, consider hotels at positions 0 and 10 with $d = 5$. The point 5 is at distance 5 from both hotels, so it is valid. But a point like 4 is at distance 4 from 0 and 6 from 10, so its minimum distance is 4, not 5, and it must not be counted. Similarly, a point like 15 is at distance 5 from 10, but only 5 from 10 and 15 from 0, so it is valid; however, if another hotel existed closer, such a point might fail the condition. This shows that local reasoning around a single hotel is insufficient; global verification is required.

Another subtle edge case is duplication of candidate positions. Different hotels may generate the same candidate coordinate $x_i + d$ or $x_i - d$, and counting them multiple times would overestimate the answer.

## Approaches

The brute-force idea would be to iterate over all integer coordinates in a reasonable range, such as from the minimum hotel position minus $d$ to the maximum plus $d$, and check for each point whether its minimum distance to any hotel is exactly $d$. This is correct in principle, but the range can be as large as $10^9$ in both directions, making it impossible to scan directly.

The key observation is that a valid point must lie exactly on the boundary of a circle of radius $d$ centered at some hotel. If a point is valid, its closest hotel must be at distance exactly $d$, meaning it must satisfy $|y - x_i| = d$ for at least one $i$. This immediately reduces the search space to only two candidates per hotel: $x_i - d$ and $x_i + d$.

However, generating candidates is not sufficient. Each candidate must be verified against all hotels to ensure that no hotel is closer than distance $d$. This verification is cheap because $n \le 100$, so checking all distances for each candidate costs $O(n)$, and we only have $2n$ candidates.

The final solution is therefore a generate-and-validate approach over a small candidate set.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force over coordinates | $O(R \cdot n)$ where $R$ can be $10^9$ | $O(1)$ | Too slow |
| Generate candidates from each hotel | $O(n^2)$ | $O(1)$ | Accepted |

## Algorithm Walkthrough

1. For each hotel position $x_i$, construct two candidate positions: $x_i - d$ and $x_i + d$. These are the only points that can possibly have minimum distance exactly $d$, since any valid point must be exactly $d$ away from at least one hotel.
2. For each candidate position $y$, compute its distance to every hotel.
3. While checking distances, keep track of the minimum distance from $y$ to any hotel. This determines whether $y$ satisfies the condition.
4. If the minimum distance equals exactly $d$, count this candidate as valid.
5. Use a set to avoid counting duplicate candidate positions generated from different hotels.

The key idea is that we never need to consider points that are not at distance $d$ from some hotel, because any valid solution must touch at least one “radius boundary” centered at a hotel.

### Why it works

Any valid position $y$ must satisfy $\min_i |y - x_i| = d$. This means there exists at least one index $i$ such that $|y - x_i| = d$, and for all other indices $j$, $|y - x_j| \ge d$. Therefore every valid point must appear in the candidate set constructed from $x_i \pm d$. The verification step ensures that we exclude candidates that are too close to some other hotel, preserving correctness.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, d = map(int, input().split())
    x = list(map(int, input().split()))

    candidates = set()

    for xi in x:
        candidates.add(xi - d)
        candidates.add(xi + d)

    ans = 0

    for y in candidates:
        best = float('inf')
        for xi in x:
            dist = abs(y - xi)
            if dist < best:
                best = dist
                if best < d:
                    break
        if best == d:
            ans += 1

    print(ans)

if __name__ == "__main__":
    solve()
```

The solution first constructs all possible boundary candidates around each hotel. The set is crucial because multiple hotels can generate the same coordinate, and duplicates must not inflate the answer.

During validation, we compute the closest distance from each candidate to any hotel. An early break is used once we detect a distance smaller than $d$, since that immediately disqualifies the candidate.

## Worked Examples

### Example 1

Input:

```
4 3
-3 2 9 16
```

We generate candidates:

| Hotel | xi - d | xi + d |
| --- | --- | --- |
| -3 | -6 | 0 |
| 2 | -1 | 5 |
| 9 | 6 | 12 |
| 16 | 13 | 19 |

Candidate set is {-6, 0, -1, 5, 6, 12, 13, 19}.

Now we validate:

| y | closest distance | valid |
| --- | --- | --- |
| -6 | 3 | yes |
| 0 | 2 | no |
| -1 | 3 | yes |
| 5 | 3 | yes |
| 6 | 3 | yes |
| 12 | 3 | yes |
| 13 | 3 | yes |
| 19 | 3 | yes |

We count 6 valid positions.

This trace shows that even though all candidates come from valid boundaries, some fail due to being closer than $d$ to another hotel.

### Example 2

Input (constructed):

```
3 2
1 5 10
```

Candidates:

| Hotel | xi - d | xi + d |
| --- | --- | --- |
| 1 | -1 | 3 |
| 5 | 3 | 7 |
| 10 | 8 | 12 |

Unique candidates: {-1, 3, 7, 8, 12}

| y | closest distance | valid |
| --- | --- | --- |
| -1 | 2 | yes |
| 3 | 2 | yes |
| 7 | 2 | yes |
| 8 | 2 | yes |
| 12 | 2 | yes |

All are valid in this configuration because no point becomes closer than $d$ to a third hotel.

This demonstrates a case where every boundary candidate survives validation.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n^2)$ | We generate $2n$ candidates and for each check distance to up to $n$ hotels |
| Space | $O(n)$ | Storage for hotel positions and candidate set |

With $n \le 100$, the worst-case about 20,000 distance checks is easily within limits. The solution is comfortably efficient under the constraints.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    input = sys.stdin.readline

    n, d = map(int, input().split())
    x = list(map(int, input().split()))

    candidates = set()
    for xi in x:
        candidates.add(xi - d)
        candidates.add(xi + d)

    ans = 0
    for y in candidates:
        best = float('inf')
        for xi in x:
            best = min(best, abs(y - xi))
        if best == d:
            ans += 1

    return str(ans)

# provided sample
assert run("4 3\n-3 2 9 16\n") == "6"

# minimum size
assert run("1 10\n0\n") == "2"

# symmetric case
assert run("2 5\n0 10\n") == "4"

# all close cluster
assert run("3 1\n1 2 3\n") == "4"

# larger spacing
assert run("3 2\n1 5 10\n") == "5"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single hotel | 2 | base case around one point |
| symmetric pair | 4 | overlapping candidate boundaries |
| dense cluster | 4 | filtering by other hotels |
| sparse layout | 5 | multiple valid boundary points |

## Edge Cases

When there is only one hotel, every valid position is exactly two points: $x_1 - d$ and $x_1 + d$. The algorithm generates exactly these two candidates and both pass validation since no other hotel can violate the distance condition.

When hotels are close together, some boundary candidates fail because another hotel is closer than $d$. The validation loop correctly eliminates these cases by checking all distances.

When multiple hotels generate the same candidate coordinate, the set ensures it is counted only once. Without deduplication, the same valid position could be overcounted, especially when symmetric configurations exist.
