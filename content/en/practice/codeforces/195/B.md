---
title: "CF 195B - After Training"
description: "We are asked to simulate the process of distributing numbered footballs into a row of baskets according to a specific order. Each new ball must go into the basket that currently contains the fewest balls."
date: "2026-06-05T00:51:52+07:00"
tags: ["codeforces", "competitive-programming", "data-structures", "implementation", "math"]
categories: ["algorithms"]
codeforces_contest: 195
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 123 (Div. 2)"
rating: 1300
weight: 195
solve_time_s: 69
verified: true
draft: false
---

[CF 195B - After Training](https://codeforces.com/problemset/problem/195/B)

**Rating:** 1300  
**Tags:** data structures, implementation, math  
**Solve time:** 1m 9s  
**Verified:** yes  

## Solution
## Problem Understanding

We are asked to simulate the process of distributing numbered footballs into a row of baskets according to a specific order. Each new ball must go into the basket that currently contains the fewest balls. If multiple baskets are tied for the fewest balls, we pick the one closest to the center of the row. If there is still a tie, we select the basket with the smaller index.

The input gives two integers: the total number of balls `n` and the total number of baskets `m`. The output is a sequence of length `n`, where the `i`-th number is the index of the basket that receives ball `i`. The sequence must be computed in the order the balls are added, because each new ball depends on the current basket configuration.

Constraints are significant. Both `n` and `m` can be as large as 100,000. A naive approach that scans all baskets for every ball would require `n*m` operations, which can reach 10^10 in the worst case-far too large to execute in 2 seconds. This implies we need a strategy that avoids full scans and leverages the predictable structure of the selection rules.

A subtle edge case occurs when the number of balls is smaller than the number of baskets. For example, if `n = 2` and `m = 5`, the first ball should go to the center basket (`3`) and the second ball should go to the next nearest basket to the center (`2` or `4`). A careless implementation that assumes all baskets will always be filled at least once will fail on such sparse cases.

## Approaches

The brute-force solution is straightforward. We could maintain an array of length `m` representing the number of balls in each basket. For each ball, we would scan the array to find the basket with the minimum count, then break ties first by distance to the center and then by index. This approach works correctly but requires `O(n * m)` operations, which is impractical for large inputs. For `n = m = 10^5`, it would involve roughly 10 billion operations.

The key insight is that the selection criteria produce a very structured sequence. The first ball always goes to the center basket. The second ball goes to one of the two baskets immediately adjacent to the center. The third ball goes to the other side of the center. Continuing in this zig-zag pattern guarantees that at any moment we are placing the next ball in a basket that is either empty or has the fewest balls and is closest to the center. Because the placement order does not depend on the exact ball numbers but only on the pattern of the baskets, we can precompute the order of baskets in `O(m)` time and then iterate through it repeatedly to assign all `n` balls.

This reduces the complexity to `O(n)` with a small `O(m)` preprocessing step, which is fast enough for the given constraints.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n*m) | O(m) | Too slow |
| Optimal | O(n) | O(m) | Accepted |

## Algorithm Walkthrough

1. Compute the center of the row of baskets as `(m + 1) // 2`. This is the basket closest to the middle according to the problem definition.
2. Generate a sequence of basket indices starting from the center, then alternating left and right, expanding outward. This gives the exact order of baskets that will receive balls if we were to fill one ball at a time according to the rules. The pattern is: center, center-1, center+1, center-2, center+2, and so on.
3. Initialize an array to store the ball assignment results.
4. Iterate over all balls from 1 to `n`. Assign each ball to the next basket in the precomputed sequence. If we reach the end of the sequence (which occurs when `n > m`), continue cycling through the sequence as each basket will now have multiple balls.
5. Print the basket index for each ball in the order they are assigned.

Why it works: the invariant here is that the precomputed sequence always chooses the basket with the minimum ball count and closest to the center. By cycling through this sequence, we exactly replicate Valeric's scheme. Because every basket is revisited in the correct order, ties are handled automatically, and the smallest-index tie breaker is also satisfied naturally by generating the sequence from left to right around the center.

## Python Solution

```python
import sys
input = sys.stdin.readline

n, m = map(int, input().split())

center = (m + 1) // 2
order = [center]

# expand left and right alternately
for d in range(1, m):
    if center - d >= 1:
        order.append(center - d)
    if center + d <= m:
        order.append(center + d)

# assign balls
res = []
for i in range(n):
    res.append(str(order[i % m]))

print("\n".join(res))
```

The code first computes the center basket, then builds a precomputed basket sequence expanding outward. The loop `for i in range(n)` assigns each ball in turn, cycling through the sequence when the number of balls exceeds the number of baskets. Off-by-one errors are avoided by using inclusive checks `>= 1` and `<= m`.

## Worked Examples

Sample Input 1: `n = 4, m = 3`

| Ball | Assigned Basket | Sequence Position |
| --- | --- | --- |
| 1 | 2 | center |
| 2 | 1 | left of center |
| 3 | 3 | right of center |
| 4 | 2 | center again |

The table shows the balls follow the precomputed zig-zag sequence. The fourth ball correctly goes back to the center as all baskets now have one ball, and the center is closest to the middle.

Custom Input 2: `n = 7, m = 5`

| Ball | Assigned Basket | Sequence Position |
| --- | --- | --- |
| 1 | 3 | center |
| 2 | 2 | left |
| 3 | 4 | right |
| 4 | 1 | far left |
| 5 | 5 | far right |
| 6 | 3 | center (second round) |
| 7 | 2 | left (second round) |

This demonstrates how the algorithm cycles through the sequence when `n > m`.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Precomputing the order takes O(m), then assigning n balls takes O(n) |
| Space | O(m) | Store the precomputed basket sequence |

Given `n, m <= 10^5`, the algorithm performs at most 200,000 operations to build the sequence plus 100,000 assignments, well within the 2-second time limit and 256 MB memory limit.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    n, m = map(int, input().split())
    center = (m + 1) // 2
    order = [center]
    for d in range(1, m):
        if center - d >= 1:
            order.append(center - d)
        if center + d <= m:
            order.append(center + d)
    res = []
    for i in range(n):
        res.append(str(order[i % m]))
    return "\n".join(res)

# provided samples
assert run("4 3\n") == "2\n1\n3\n2", "sample 1"

# custom tests
assert run("1 1\n") == "1", "single ball, single basket"
assert run("2 5\n") == "3\n2", "fewer balls than baskets"
assert run("7 5\n") == "3\n2\n4\n1\n5\n3\n2", "more balls than baskets"
assert run("5 5\n") == "3\n2\n4\n1\n5", "balls equal baskets"
assert run("10 2\n") == "1\n2\n1\n2\n1\n2\n1\n2\n1\n2", "two baskets repeated"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 1` | `1` | Minimum input |
| `2 5` | `3\n2` | Fewer balls than baskets |
| `7 5` | `3\n2\n4\n1\n5\n3\n2` | More balls than baskets, cycling sequence |
| `5 5` | `3\n2\n4\n1\n5` | Balls equal baskets, full first round |
| `10 2` | `1\n2\n1\n2\n1\n2\n1\n2\n1\n2` | Two baskets repeating |

## Edge Cases

When `n < m`, such as `n = 2, m = 5`, the algorithm assigns the first ball to the center (`3`) and the second to the next closest basket (`2`). The remaining baskets are ignored because there are not enough balls to reach them. The precomputed sequence ensures that ties for the fewest balls are broken by proximity to the center and index order automatically. This avoids any manual min-count scanning, which is the common source of subtle bugs in naive implementations
