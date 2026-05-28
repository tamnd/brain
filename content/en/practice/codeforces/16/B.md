---
title: "CF 16B - Burglar and Matches"
description: "We have a burglar who can carry exactly n matchboxes. In the warehouse, there are m containers. Each container i has a_i matchboxes, and every matchbox in that container contains b_i matches."
date: "2026-05-28T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "greedy", "implementation", "sortings"]
categories: ["algorithms"]
codeforces_contest: 16
codeforces_index: "B"
codeforces_contest_name: "Codeforces Beta Round 16 (Div. 2 Only)"
rating: 900
weight: 16
solve_time_s: 73
verified: true
draft: false
---
[CF 16B - Burglar and Matches](https://codeforces.com/problemset/problem/16/B)

**Rating:** 900  
**Tags:** greedy, implementation, sortings  
**Solve time:** 1m 13s  
**Verified:** yes  

## Solution
## Problem Understanding

We have a burglar who can carry exactly `n` matchboxes. In the warehouse, there are `m` containers. Each container `i` has `a_i` matchboxes, and every matchbox in that container contains `b_i` matches. The goal is to pick up to `n` matchboxes such that the total number of matches is maximized.

The inputs are two integers `n` and `m` followed by `m` pairs `(a_i, b_i)`. The output is a single integer: the maximum total matches the burglar can take.

The constraints are telling. `n` can be as large as 2·10^8. This is huge for iterating over individual matchboxes, so any solution that examines each matchbox individually would be too slow. `m` is at most 20, so the number of containers is tiny. That hints that sorting or a greedy choice over containers is feasible. `a_i` can be large, so the number of matchboxes in a container can exceed `n`. `b_i` is small, 1 to 10, so the matches per box are easy to handle with regular integers.

Edge cases to watch out for include containers that have more matchboxes than the burglar can carry. For example, if `n = 5` and a container has `a_i = 10` boxes with `b_i = 3` matches, the burglar can only take 5 of them. A careless implementation that adds all `10*3 = 30` matches would be wrong. Another edge case is when `n` is larger than the total number of matchboxes in all containers. In that case, the burglar should just take everything.

## Approaches

The brute-force approach would iterate through every possible combination of matchboxes from the containers, summing the total matches and picking the best. With `m` up to 20, each container having up to 10^8 matchboxes, the number of combinations is astronomical. Even if we only considered containers as whole units, the number of subsets is `2^m = 2^20 ≈ 1 million`, which is feasible for subset sums but unnecessary here. Going down to the individual matchboxes is clearly impossible because `n` can be 2·10^8.

The key observation is that the problem is greedy: to maximize the number of matches, the burglar should first take matchboxes with the largest `b_i` (matches per box). The order of containers is irrelevant except for `b_i`. Once containers are sorted by `b_i` descending, the burglar takes as many boxes as possible from the first container, then the next, until the rucksack is full. This works because each matchbox is indivisible and the boxes with more matches are always strictly better than those with fewer.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(2^m * m) | O(m) | Too slow |
| Greedy / Sort by `b_i` | O(m log m) | O(m) | Accepted |

## Algorithm Walkthrough

1. Read `n` (capacity) and `m` (number of containers). Initialize `total_matches = 0`.
2. Read each container's `(a_i, b_i)` and store as a list of tuples.
3. Sort the list of containers in descending order of `b_i`. Sorting ensures we always consider the most valuable boxes first.
4. Iterate through the sorted containers:

a. Let `take = min(a_i, n)`. This is the number of boxes we can take from this container without exceeding capacity.

b. Add `take * b_i` to `total_matches`.

c. Decrease `n` by `take`. If `n` becomes 0, break the loop because the rucksack is full.
5. Print `total_matches`.

Why it works: At every step, we are taking the available matchboxes with the highest matches per box first. Because matchboxes are indivisible, there is no advantage to leaving a high-value box for a lower-value box. The greedy choice is safe, and by iterating until `n` boxes are taken, we guarantee that the total matches are maximized.

## Python Solution

```python
import sys
input = sys.stdin.readline

n, m = map(int, input().split())
containers = []

for _ in range(m):
    a, b = map(int, input().split())
    containers.append((b, a))  # store as (matches per box, number of boxes)

# Sort by matches per box descending
containers.sort(reverse=True)

total_matches = 0
for b, a in containers:
    if n == 0:
        break
    take = min(a, n)
    total_matches += take * b
    n -= take

print(total_matches)
```

We store `(b, a)` instead of `(a, b)` because sorting is easier on `b` descending. During iteration, `take = min(a, n)` ensures we never exceed capacity. The loop terminates early if the rucksack is full. These details prevent off-by-one or overflow issues.

## Worked Examples

Sample 1:

Input:

```
7 3
5 10
2 5
3 6
```

Step-by-step trace:

| Container (b, a) | n before | take | total_matches after | n after |
| --- | --- | --- | --- | --- |
| (10, 5) | 7 | 5 | 50 | 2 |
| (6, 3) | 2 | 2 | 50 + 12 = 62 | 0 |
| (5, 2) | 0 | 0 | 62 | 0 |

Explanation: First container is richest, take 5 boxes. Next container, only 2 boxes fit in remaining capacity. Total matches = 62.

Another test case:

Input:

```
10 2
3 10
5 20
```

| Container (b, a) | n before | take | total_matches after | n after |
| --- | --- | --- | --- | --- |
| (20, 5) | 10 | 5 | 100 | 5 |
| (10, 3) | 5 | 3 | 100 + 30 = 130 | 2 |

The remaining capacity (2) is more than any remaining boxes, so we stop. Total matches = 130.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(m log m) | Sorting `m` containers dominates; iteration is O(m) |
| Space | O(m) | Storing the container list |

Given `m ≤ 20`, sorting is trivial, and the algorithm easily fits within the 0s time limit and 64 MB memory limit. Handling `n` up to 2·10^8 works because we never iterate per matchbox, only per container.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline
    n, m = map(int, input().split())
    containers = []
    for _ in range(m):
        a, b = map(int, input().split())
        containers.append((b, a))
    containers.sort(reverse=True)
    total_matches = 0
    for b, a in containers:
        if n == 0:
            break
        take = min(a, n)
        total_matches += take * b
        n -= take
    return str(total_matches)

# Provided sample
assert run("7 3\n5 10\n2 5\n3 6\n") == "62", "sample 1"

# Minimum input
assert run("1 1\n1 1\n") == "1", "minimum input"

# Large n, all containers smaller
assert run("10 2\n3 5\n2 10\n") == "35", "capacity larger than total boxes"

# All boxes same b
assert run("5 2\n3 7\n4 7\n") == "35", "all boxes same value"

# Single rich container exceeds n
assert run("4 1\n10 100\n") == "400", "single container larger than capacity"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 1\n1 1 | 1 | minimum input edge case |
| 10 2\n3 5\n2 10 | 35 | capacity larger than total boxes |
| 5 2\n3 7\n4 7 | 35 | all boxes equal value |
| 4 1\n10 100 | 400 | container larger than capacity, only take n boxes |

## Edge Cases

Case where the richest container has more boxes than `n`:

```
n = 4, m = 1
10 100
```

`take = min(10, 4) = 4`, `total_matches = 4*100 = 400`. Correct, no overcounting.

Case where total boxes < n:

```
n = 10, m = 2
3 5
2
```
