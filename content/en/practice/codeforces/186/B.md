---
title: "CF 186B - Growing Mushrooms"
description: "We have a mushroom-growing contest with two phases separated by a break. Each participant has two speeds, and the problem is that we do not know the order they will use them. During the first phase of length t1, mushrooms grow at one speed."
date: "2026-05-29T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "greedy", "sortings"]
categories: ["algorithms"]
codeforces_contest: 186
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 118 (Div. 2)"
rating: 1200
weight: 186
solve_time_s: 161
verified: true
draft: false
---

[CF 186B - Growing Mushrooms](https://codeforces.com/problemset/problem/186/B)

**Rating:** 1200  
**Tags:** greedy, sortings  
**Solve time:** 2m 41s  
**Verified:** yes  

## Solution
## Problem Understanding

We have a mushroom-growing contest with two phases separated by a break. Each participant has two speeds, and the problem is that we do not know the order they will use them. During the first phase of length _t1_, mushrooms grow at one speed. After a break, the mushroom height shrinks by _k_ percent. Then, during the second phase of length _t2_, mushrooms grow at the second speed. Each participant chooses the order of their two speeds to maximize the final mushroom height. Our task is to compute the final heights for all participants and print them sorted from tallest to shortest. If two mushrooms have equal height, the participant with the smaller index comes first.

The input gives _n_, the number of participants, the durations _t1_ and _t2_, and the percentage decrease _k_. Then each participant’s two speeds _a_i_ and _b_i_ are given. The output is the maximum final height for each participant rounded to exactly two decimal places, sorted as described.

The constraints are small: _n_, _t1_, _t2_ are all at most 1000, and speeds are at most 1000. This means we can afford O(n) or O(n log n) computations easily. We must be careful with floating-point arithmetic because the growth involves a percentage reduction, which is not an integer operation.

Edge cases that can be tricky include a participant whose two speeds are equal, where either order yields the same result, or extreme _k_ values, such as 100 percent reduction, which would wipe out the first phase entirely.

## Approaches

The brute-force approach is straightforward: for each participant, try both possible orders of speeds, calculate the final mushroom height for each order, and take the maximum. Specifically, the two heights to compare are:

```
h1 = a_i * t1 * (1 - k/100) + b_i * t2
h2 = b_i * t1 * (1 - k/100) + a_i * t2
```

The maximum of `h1` and `h2` is the optimal height for that participant. This works because the number of participants is small, and each computation is constant time, giving an O(n) solution. After computing heights, we sort the participants by height descending and by index ascending in case of ties.

The key insight for a faster or cleaner implementation is that we do not need to explore any other combinations. There are only two speeds per participant, and only two orders, so no further optimization is possible. Sorting afterwards is standard and ensures correct ordering in the result table.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n log n) | O(n) | Accepted |
| Optimal | O(n log n) | O(n) | Accepted |

Sorting is O(n log n), which dominates the linear O(n) computation of heights.

## Algorithm Walkthrough

1. Read the number of participants `n`, the two durations `t1` and `t2`, and the break reduction `k`. Store the reduction factor as a decimal fraction `r = (100 - k)/100` to simplify calculations.
2. Initialize an empty list `results` that will store tuples `(participant_index, max_height)`.
3. Iterate through each participant. Read their two speeds `a` and `b`.
4. Compute the final height if the participant uses `a` first, then `b`: `h1 = a * t1 * r + b * t2`.
5. Compute the final height if the participant uses `b` first, then `a`: `h2 = b * t1 * r + a * t2`.
6. Take `max(h1, h2)` as the participant’s optimal mushroom height.
7. Append `(participant_index, max_height)` to `results`.
8. After all participants are processed, sort `results` first by `-max_height` (descending) and then by `participant_index` (ascending) to resolve ties.
9. Print each participant’s index and height formatted to exactly two decimal places.

Why it works: The invariant is that for each participant, we have explored all possible orders of their two speeds. The maximum height is guaranteed to be correct. Sorting afterwards ensures the correct ranking, respecting the tie-breaking rule. No combination is missed, and the arithmetic reflects the competition rules exactly.

## Python Solution

```python
import sys
input = sys.stdin.readline

n, t1, t2, k = map(int, input().split())
r = (100 - k) / 100  # reduction factor

results = []

for i in range(1, n + 1):
    a, b = map(int, input().split())
    h1 = a * t1 * r + b * t2
    h2 = b * t1 * r + a * t2
    max_height = max(h1, h2)
    results.append((i, max_height))

# sort by height descending, then index ascending
results.sort(key=lambda x: (-x[1], x[0]))

for idx, height in results:
    print(f"{idx} {height:.2f}")
```

The code follows the algorithm steps exactly. The reduction factor is precomputed to avoid repeating the division. Heights are stored as floating-point numbers to preserve precision after multiplying by `r`. Sorting uses a lambda function to sort descending by height and ascending by participant index.

## Worked Examples

Sample Input 1:

```
2 3 3 50
2 4
4 2
```

| Participant | a | b | h1 = a_t1_r + b*t2 | h2 = b_t1_r + a*t2 | max_height |
| --- | --- | --- | --- | --- | --- |
| 1 | 2 | 4 | 2_3_0.5 + 4*3 = 3 + 12 = 15 | 4_3_0.5 + 2*3 = 6 + 6 = 12 | 15 |
| 2 | 4 | 2 | 4_3_0.5 + 2*3 = 6 + 6 = 12 | 2_3_0.5 + 4*3 = 3 + 12 = 15 | 15 |

After sorting by height descending, then index ascending:

```
1 15.00
2 15.00
```

This demonstrates the algorithm correctly evaluates both orderings and applies the break reduction.

Custom Input 2:

```
3 2 4 25
5 5
6 3
2 8
```

| Participant | h1 | h2 | max_height |
| --- | --- | --- | --- |
| 1 | 5_2_0.75 + 5*4 = 7.5 + 20 = 27.5 | same = 27.5 | 27.5 |
| 2 | 6_2_0.75 + 3*4 = 9 + 12 = 21 | 3_2_0.75 + 6*4 = 4.5 + 24 = 28.5 | 28.5 |
| 3 | 2_2_0.75 + 8*4 = 3 + 32 = 35 | 8_2_0.75 + 2*4 = 12 + 8 = 20 | 35 |

Sorted result:

```
3 35.00
2 28.50
1 27.50
```

This demonstrates that each participant’s optimal choice may not always be “larger speed second”; it depends on the durations and reduction factor.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n) | Computing the two heights per participant is O(1), for n participants gives O(n). Sorting the results dominates at O(n log n). |
| Space | O(n) | We store the maximum height and index for each participant. |

The problem constraints allow n up to 1000, so O(n log n) is well within the 2-second limit. Multiplication and floating-point arithmetic are negligible in time cost for these bounds.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    out = io.StringIO()
    sys.stdout = out
    # solution
    n, t1, t2, k = map(int, input().split())
    r = (100 - k) / 100
    results = []
    for i in range(1, n + 1):
        a, b = map(int, input().split())
        h1 = a * t1 * r + b * t2
        h2 = b * t1 * r + a * t2
        results.append((i, max(h1, h2)))
    results.sort(key=lambda x: (-x[1], x[0]))
    for idx, height in results:
        print(f"{idx} {height:.2f}")
    return out.getvalue().strip()

# Provided sample
assert run("2 3 3 50\n2 4\n4 2\n") == "1 15.00\n2 15.00", "sample 1"

# Minimum size
assert run("1 1 1 1\n1 1\n") == "1 1.99", "min size"

# All speeds equal
assert run("2 5 5 50\n10 10\n10 10
```
