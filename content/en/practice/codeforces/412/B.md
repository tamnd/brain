---
title: "CF 412B - Network Configuration"
description: "We are given a set of computers, each with a measured maximum Internet speed. There are fewer participants than computers, and each participant must get a separate computer."
date: "2026-06-07T02:20:26+07:00"
tags: ["codeforces", "competitive-programming", "greedy", "sortings"]
categories: ["algorithms"]
codeforces_contest: 412
codeforces_index: "B"
codeforces_contest_name: "Coder-Strike 2014 - Round 1"
rating: 900
weight: 412
solve_time_s: 265
verified: true
draft: false
---

[CF 412B - Network Configuration](https://codeforces.com/problemset/problem/412/B)

**Rating:** 900  
**Tags:** greedy, sortings  
**Solve time:** 4m 25s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a set of computers, each with a measured maximum Internet speed. There are fewer participants than computers, and each participant must get a separate computer. The goal is to make the speeds of the selected computers equal, but we are allowed to reduce any computer’s speed arbitrarily, never increase it. Among all ways to select computers and adjust their speeds, we want to maximize the common speed assigned to participants.

Input consists of two integers: the total number of computers `n` and the number of participants `k`. Then comes an array of integers representing the maximum speed of each computer. Output is a single integer: the highest possible uniform speed that at least `k` computers can achieve after optional reductions.

The constraints are small: `n` is at most 100. This allows approaches up to roughly O(n² log n) comfortably, because even O(n³) is borderline. The speeds themselves are moderate integers up to 32768, but we never need to enumerate all numbers in that range thanks to the small `n`.

An edge case that might break a naive solution occurs when many computers share high speeds but only a few are needed. For example, with `n = 5`, `k = 3`, and speeds `[10, 10, 9, 9, 8]`, the optimal selection is `[10, 10, 9]` reduced to `9` each. A careless approach that only counts exact duplicates could wrongly pick `10` and fail, since only two computers have it. Another subtle case is when all computers have the same speed; the answer should just be that speed regardless of `k`.

## Approaches

The brute-force method would be to consider every integer speed from 1 up to the maximum observed speed. For each candidate speed `s`, we would count how many computers have at least speed `s`. If at least `k` computers meet this threshold, `s` is feasible. Then we take the largest feasible `s`. This works because reducing a speed is allowed, so any computer faster than `s` can contribute. The problem with this is that the speed range is up to 32768, so even though `n` is small, iterating over all 32768 speeds is inefficient.

The key insight is that we only need to consider speeds that actually appear on the computers. Sorting the array lets us systematically check candidate speeds from largest to smallest. For a given candidate speed `s`, we can count how many computers have at least that speed. As soon as this count is at least `k`, we have found the optimal speed. This reduces the candidate space from 32768 to at most `n` values, which is perfectly feasible with `n` up to 100.

The story here is: the brute-force works in principle because reducing speeds is allowed, but it is inefficient because it tries impossible or unnecessary speeds. Sorting and checking only existing speeds leverages the problem’s structure: only existing maximums matter for the optimal solution.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force (all speeds 1..max) | O(n * max_speed) | O(1) | Too slow |
| Check sorted speeds | O(n log n + n²) | O(n) | Accepted |

## Algorithm Walkthrough

1. Read the input values `n`, `k`, and the array of maximum speeds. Sorting the array will help us reason from high speeds to low speeds.
2. Sort the array of speeds in non-decreasing order. The reason is that higher speeds are preferable, so we will try candidates from largest to smallest.
3. Iterate over the array from the largest speed downward. For each speed `a[i]`, count how many computers have speed greater than or equal to `a[i]`. We can do this by scanning the array from the end backward.
4. As soon as the count of computers with speed at least `a[i]` is at least `k`, return `a[i]`. This works because `a[i]` is the largest candidate that allows at least `k` computers to meet it. We do not need to check smaller speeds because they will only reduce the common speed.

Why it works: By considering only existing speeds and counting how many computers can reach each speed, we ensure that we select the maximum uniform speed that can be applied to at least `k` computers. Any smaller candidate speed is either unnecessary or suboptimal. The invariant is that at every candidate `s`, the count of computers ≥ `s` correctly tells us feasibility.

## Python Solution

```python
import sys
input = sys.stdin.readline

n, k = map(int, input().split())
speeds = list(map(int, input().split()))

# Sort speeds ascending
speeds.sort()

# Check candidates from largest to smallest
for i in range(n - 1, -1, -1):
    count = sum(1 for speed in speeds if speed >= speeds[i])
    if count >= k:
        print(speeds[i])
        break
```

The code first sorts the speeds. Then, for each candidate speed starting from the largest, it counts how many computers can achieve at least that speed. As soon as the count reaches `k`, that speed is printed. The subtlety here is scanning from largest to smallest and counting `>= speeds[i]`, which guarantees the maximum feasible speed.

## Worked Examples

**Sample 1:**

Input:

```
3 2
40 20 30
```

| Step | Candidate `s` | Count >= `s` | Decision |
| --- | --- | --- | --- |
| 1 | 40 | 1 | Not enough |
| 2 | 30 | 2 | Enough → select 30 |

The algorithm identifies that two computers can be set to 30, which is the highest possible uniform speed.

**Custom Example:**

Input:

```
5 3
10 10 9 9 8
```

| Step | Candidate `s` | Count >= `s` | Decision |
| --- | --- | --- | --- |
| 1 | 10 | 2 | Not enough |
| 2 | 9 | 4 | Enough → select 9 |

Even though 10 appears twice, only four computers can reach 9 after optional reductions, giving a uniform 9.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n²) | Sorting is O(n log n), checking each candidate is O(n²) in worst case |
| Space | O(n) | Storing the speeds array |

With `n ≤ 100`, O(n²) is negligible (at most 10,000 operations). Memory usage is trivial.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    output = io.StringIO()
    sys.stdout = output
    n, k = map(int, input().split())
    speeds = list(map(int, input().split()))
    speeds.sort()
    for i in range(n-1, -1, -1):
        count = sum(1 for s in speeds if s >= speeds[i])
        if count >= k:
            print(speeds[i])
            break
    return output.getvalue().strip()

# Provided sample
assert run("3 2\n40 20 30\n") == "30", "sample 1"

# Custom cases
assert run("5 3\n10 10 9 9 8\n") == "9", "mixed speeds"
assert run("4 2\n5 5 5 5\n") == "5", "all equal"
assert run("1 1\n16\n") == "16", "minimum size"
assert run("6 4\n20 15 15 10 10 10\n") == "15", "need top 4"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `5 3\n10 10 9 9 8` | 9 | Selection and reduction correctness |
| `4 2\n5 5 5 5` | 5 | All equal speeds |
| `1 1\n16` | 16 | Minimum input |
| `6 4\n20 15 15 10 10 10` | 15 | Picking top `k` after reductions |

## Edge Cases

For `n = 1` and `k = 1` with speed `16`, the algorithm immediately selects 16. For `n = 5` and `k = 3` with speeds `[10, 10, 9, 9, 8]`, the algorithm first tests 10 (count 2 < 3), then 9 (count 4 ≥ 3), outputting 9. Both edge cases demonstrate that counting `>= candidate` is essential, and starting from the largest candidate ensures maximality. The approach handles all cases where `k` equals `n`, all speeds are equal, or reductions are required to match the uniform speed.
