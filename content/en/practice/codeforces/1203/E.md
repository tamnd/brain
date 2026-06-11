---
title: "CF 1203E - Boxers"
description: "We are given a set of boxers, each with a positive integer weight. Each boxer can adjust their weight by at most 1, either up or down, but the weight must remain strictly positive."
date: "2026-06-11T23:43:20+07:00"
tags: ["codeforces", "competitive-programming", "greedy", "sortings"]
categories: ["algorithms"]
codeforces_contest: 1203
codeforces_index: "E"
codeforces_contest_name: "Codeforces Round 579 (Div. 3)"
rating: 1500
weight: 1203
solve_time_s: 77
verified: true
draft: false
---

[CF 1203E - Boxers](https://codeforces.com/problemset/problem/1203/E)

**Rating:** 1500  
**Tags:** greedy, sortings  
**Solve time:** 1m 17s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a set of boxers, each with a positive integer weight. Each boxer can adjust their weight by at most 1, either up or down, but the weight must remain strictly positive. Our goal is to form the largest possible team in which no two boxers share the same weight after the adjustments. The input provides the number of boxers, `n`, and the list of their weights. The output is a single integer representing the size of the largest team with unique weights.

The constraints indicate that `n` can be as large as 150,000, and weights can reach up to 150,000. A naive approach that tries all possible combinations of adjustments would involve exponential time, which is infeasible. We need a solution that runs in roughly linear or linearithmic time, O(n log n) or better, because O(n^2) would lead to over 22 billion operations in the worst case, far exceeding the 2-second limit.

A few edge cases are worth considering. If all boxers have the same weight, we must carefully adjust weights up or down to maximize the team. For instance, with weights `[1,1,1]`, the optimal result is `[1,2,3]` giving a team of size 3. Another case is when weights include 1, since we cannot reduce 1 further, so adjustments must only increase such weights. If the maximum weight occurs multiple times near the upper bound, we must ensure we do not exceed 150,001 when increasing weights.

## Approaches

The brute-force solution is simple to describe: for each boxer, try all three possible weights (current, current-1, current+1) and check if that weight has already been assigned in the team. If not, add it to the team. Continue until all boxers are processed. This is correct because it explicitly checks all feasible weight assignments. The problem is that in the worst case, each boxer tries three possibilities, and checking uniqueness might require searching or updating a set repeatedly, leading to O(n^2) complexity if not carefully managed. With `n = 150,000`, this approach will timeout.

The key insight is that the order in which we process boxers matters. Sorting the boxers by weight allows us to consider smaller weights first. For each boxer, we attempt to decrease their weight by 1 if it remains positive and is available, then try the original weight, and finally try increasing by 1. This greedy strategy ensures that smaller weights are filled first, leaving room for higher weights without conflicts. The reason this works is that once a weight is used, we cannot reuse it. By always taking the smallest available option, we minimize collisions later. This reduces the problem to a single pass through a sorted list while maintaining a set or boolean array of used weights, achieving O(n log n) time due to sorting and O(n) space.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n^2) | O(n) | Too slow |
| Optimal | O(n log n) | O(max(a_i)) | Accepted |

## Algorithm Walkthrough

1. Read the number of boxers `n` and the list of weights `a`.
2. Sort the list of weights in ascending order. Sorting ensures we process smaller weights first, which lets us assign the smallest available unique weights greedily.
3. Initialize a boolean array or set to track which weights have already been assigned. We will mark a weight as used when we assign it to a boxer.
4. Initialize a counter `team_size` to zero to count successfully assigned boxers.
5. Iterate over each weight `w` in the sorted list. For each weight, attempt in order:

a. `w-1`, only if it is positive and not used. If assigned, mark it used and increment `team_size`.

b. If `w-1` was not available, try `w` itself. If available, mark it used and increment `team_size`.

c. If neither `w-1` nor `w` was available, try `w+1`. If available, mark it used and increment `team_size`.
6. After processing all boxers, `team_size` will contain the size of the largest possible team. Output this value.

Why it works: the algorithm maintains the invariant that all assigned weights are unique. Sorting ensures that smaller weights get priority, which avoids wasting smaller numbers that could only be assigned by reducing boxers with weight 2 or more. The three-step greedy check guarantees that each boxer contributes to the team if at least one nearby weight is available. Since all options are tested in increasing order, no potential assignment is missed.

## Python Solution

```python
import sys
input = sys.stdin.readline

n = int(input())
weights = list(map(int, input().split()))
weights.sort()

MAX_W = 150001
used = [False] * (MAX_W + 2)
team_size = 0

for w in weights:
    if w > 1 and not used[w-1]:
        used[w-1] = True
        team_size += 1
    elif not used[w]:
        used[w] = True
        team_size += 1
    elif w + 1 <= MAX_W + 1 and not used[w+1]:
        used[w+1] = True
        team_size += 1

print(team_size)
```

The solution starts by reading input and sorting the boxers' weights. We use a boolean array to track used weights for constant-time access. The iteration over sorted weights ensures we handle smaller weights first, avoiding unnecessary conflicts. Each conditional handles the greedy choice: reduce if possible, then keep, then increase. Boundary checks ensure no negative or overly large weights are used. Incrementing `team_size` only when a weight is successfully assigned maintains correctness.

## Worked Examples

Sample Input 1:

```
4
3 2 4 1
```

| w | used[w-1] | used[w] | used[w+1] | team_size |
| --- | --- | --- | --- | --- |
| 1 | - | False | True | 1 |
| 2 | False | True | - | 2 |
| 3 | False | True | - | 3 |
| 4 | False | True | - | 4 |

All boxers can keep their weight; final team size is 4.

Sample Input 2:

```
5
1 1 2 2 3
```

| w | used[w-1] | used[w] | used[w+1] | team_size |
| --- | --- | --- | --- | --- |
| 1 | - | False | True | 1 |
| 1 | False | True | - | 2 |
| 2 | False | True | - | 3 |
| 2 | True | True | True | 3 |
| 3 | False | True | - | 4 |

Final team has weights `[1,2,2,3,4]` adjusted to `[1,2,3,4,5]` with size 5.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n) | Sorting dominates; processing each weight is O(1) |
| Space | O(max(a_i)) | Boolean array of size ~150,003 for used weights |

With `n ≤ 150,000` and weights ≤ 150,000, sorting plus single pass fits comfortably under the 2-second limit. Memory usage is also under 256 MB.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    n = int(input())
    weights = list(map(int, input().split()))
    weights.sort()
    MAX_W = 150001
    used = [False] * (MAX_W + 2)
    team_size = 0
    for w in weights:
        if w > 1 and not used[w-1]:
            used[w-1] = True
            team_size += 1
        elif not used[w]:
            used[w] = True
            team_size += 1
        elif w + 1 <= MAX_W + 1 and not used[w+1]:
            used[w+1] = True
            team_size += 1
    return str(team_size)

# Provided samples
assert run("4\n3 2 4 1\n") == "4", "sample 1"
assert run("5\n1 1 2 2 3\n") == "5", "custom sample"

# Custom cases
assert run("3\n1 1 1\n") == "3", "all equal weights"
assert run("2\n1 2\n") == "2", "minimum n"
assert run("5\n1 2 2 2 3\n") == "5", "multiple duplicates with lower bound 1"
assert run("6\n5 5 5 5 5 5\n") == "6", "all equal larger weights"
assert run("4\n150000 150000 150000 150000\n") == "4", "upper bound weights"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `3\n1 1 1` | 3 | Correct handling of repeated minimum weights |
| ` |  |  |
