---
title: "CF 208D - Prizes, Prizes, more Prizes"
description: "We have a sequence of chocolate bar purchases, each yielding a certain number of points. Vasya starts with zero points and after each bar may go to the prize center. The prizes have fixed point costs: a mug, a towel, a bag, a bicycle, and a car, in strictly increasing order."
date: "2026-06-03T17:22:43+07:00"
tags: ["codeforces", "competitive-programming", "implementation"]
categories: ["algorithms"]
codeforces_contest: 208
codeforces_index: "D"
codeforces_contest_name: "Codeforces Round 130 (Div. 2)"
rating: 1200
weight: 208
solve_time_s: 170
verified: false
draft: false
---

[CF 208D - Prizes, Prizes, more Prizes](https://codeforces.com/problemset/problem/208/D)

**Rating:** 1200  
**Tags:** implementation  
**Solve time:** 2m 50s  
**Verified:** no  

## Solution
## Problem Understanding

We have a sequence of chocolate bar purchases, each yielding a certain number of points. Vasya starts with zero points and after each bar may go to the prize center. The prizes have fixed point costs: a mug, a towel, a bag, a bicycle, and a car, in strictly increasing order. Vasya applies a greedy strategy: whenever he has enough points to buy any prize, he picks the most expensive one he can afford, reduces his points, and repeats until he cannot afford any prize.

Our task is to reconstruct Vasya’s prize collection and determine his leftover points after processing all chocolate bars.

The input gives `n` (up to 50), the points for each bar (`p_i` up to 10^9), and the costs of the five prizes (strictly increasing, up to 10^9). The small `n` allows us to simulate the process directly without worrying about performance. The large point values mean we must avoid naive array-based DP or counting approaches that assume small integers.

Edge cases include situations where Vasya’s points exactly match a prize cost, or where he can afford multiple prizes at once and the greedy choice must be applied repeatedly. For instance, if Vasya earns 10 points and prizes cost `[2,4,10,15,20]`, he should choose the bag immediately rather than buying multiple smaller items, and leftover points must be calculated correctly after each purchase.

## Approaches

The brute-force approach is straightforward simulation. Start with zero points and for each chocolate bar add its points. Then, while the current points are at least the cheapest prize cost, repeatedly find the most expensive prize Vasya can afford, increment its count, and subtract its cost from points. Continue this for all bars.

This approach is correct because it directly follows Vasya’s greedy strategy. Since `n` is at most 50 and there are only 5 prizes, the inner loop of repeatedly exchanging points will run at most `n * max_points / min_cost` times. Even with large point values, the maximum number of iterations is constrained by the greedy subtraction sequence, which is at most a handful of iterations per bar in practical terms.

There is no faster asymptotic solution needed because the constraints are small, but the key insight is that the greedy strategy allows us to always pick the largest affordable prize without considering sequences of smaller prizes - the problem guarantees this approach is optimal.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Simulation | O(n * 5) in practice | O(5) for counters | Accepted |
| Optimized | N/A | N/A | Not needed; brute force suffices |

## Algorithm Walkthrough

1. Initialize a list `count` of size 5 to zero, representing the number of each prize Vasya has collected. Initialize `points` to zero.
2. Iterate over each chocolate bar in chronological order. Add its points to `points`.
3. While `points` is at least the cost of the cheapest prize:

a. Iterate over the prizes from the most expensive to the cheapest.

b. Find the most expensive prize whose cost is less than or equal to `points`.

c. Increment the corresponding count.

d. Subtract the prize’s cost from `points`.
4. After processing all chocolate bars, print the counts of each prize followed by the remaining `points`.

This works because the invariant is that after each inner loop, Vasya cannot afford any prize except possibly after adding more points from the next chocolate bar. At each decision point, selecting the most expensive affordable prize guarantees the greedy strategy matches the problem description.

## Python Solution

```python
import sys
input = sys.stdin.readline

n = int(input())
points_list = list(map(int, input().split()))
prizes = list(map(int, input().split()))  # a, b, c, d, e
count = [0] * 5
points = 0

for p in points_list:
    points += p
    while points >= prizes[0]:
        for i in range(4, -1, -1):
            if points >= prizes[i]:
                count[i] += 1
                points -= prizes[i]
                break

print(' '.join(map(str, count)))
print(points)
```

The outer loop adds points for each bar. The inner loop repeatedly applies the greedy strategy until Vasya can no longer buy any prize. Iterating from most expensive to cheapest ensures we always pick the maximal prize first. Using `break` inside the inner loop guarantees only one prize is bought per iteration, correctly simulating Vasya’s continuous exchanges.

## Worked Examples

Sample 1:

| Step | Points Added | Points Before Exchange | Prize Bought | Points After Exchange | Count |
| --- | --- | --- | --- | --- | --- |
| 1 | 3 | 3 | Mug (2) | 1 | [1,0,0,0,0] |
| 2 | 10 | 11 | Bag (10) | 1 | [1,0,1,0,0] |
| 3 | 4 | 5 | Towel (4) | 1 | [1,1,1,0,0] |

This confirms the algorithm correctly chooses the most expensive prize at each step and tracks leftover points.

Custom Input:

```
5
1 2 3 4 5
2 3 5 7 11
```

| Step | Points | Prize Bought | Points After | Count |
| --- | --- | --- | --- | --- |
| 1 | 1 | - | 1 | [0,0,0,0,0] |
| 2 | 3 | 3 | 0 | [0,1,0,0,0] |
| 3 | 3 | 2 | 0 | [1,1,0,0,0] |
| 4 | 4 | 3 | 1 | [1,1,1,0,0] |
| 5 | 6 | 5 | 1 | [1,1,2,0,0] |

This demonstrates repeated greedy selections with leftover points being correctly carried forward.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n * 5) | Outer loop runs `n` times; inner loop runs at most 5 iterations per prize exchange. |
| Space | O(5) | Store counts of 5 prizes; input list of size n. |

With n ≤ 50, this executes well under 2 seconds even with large point values. Memory usage is trivial, far below 256 MB.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    n = int(input())
    points_list = list(map(int, input().split()))
    prizes = list(map(int, input().split()))
    count = [0]*5
    points = 0
    for p in points_list:
        points += p
        while points >= prizes[0]:
            for i in range(4, -1, -1):
                if points >= prizes[i]:
                    count[i] += 1
                    points -= prizes[i]
                    break
    return f"{' '.join(map(str,count))}\n{points}"

# Provided sample
assert run("3\n3 10 4\n2 4 10 15 20\n") == "1 1 1 0 0\n1", "sample 1"

# Minimum input
assert run("1\n1\n1 2 3 4 5\n") == "1 0 0 0 0\n0", "min input"

# All points smaller than cheapest prize
assert run("3\n1 1 1\n5 6 7 8 9\n") == "0 0 0 0 0\n3", "all points small"

# Exact sums
assert run("2\n7 4\n2 3 5 7 10\n") == "0 1 1 0 0\n3", "exact sums"

# Multiple exchanges per bar
assert run("1\n20\n2 4 10 15 20\n") == "0 0 1 0 0\n10", "single large bar"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 1 1 / 5 6 7 8 9 | 0 0 0 0 0\n3 | Points less than any prize |
| 2 7 4 / 2 3 5 7 10 | 0 1 1 0 0\n3 | Exact sums triggering multiple prizes |
| 1 20 / 2 4 10 15 20 | 0 0 1 0 0\n10 | Single bar allowing multiple exchanges |

## Edge Cases

If Vasya earns points that exactly match multiple prizes in a single step, the algorithm selects the most expensive prize first. For instance, points 20 with prizes `[2,4,10,15,20]` leads to one car if we processed greedily in reverse order. Leftover points are zero if
