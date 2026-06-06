---
title: "CF 440A - Forgotten Episode"
description: "We are asked to determine which episode Polycarpus has not watched in a season of a TV show. He has watched n - 1 episodes out of a total of n, each numbered consecutively from 1 to n."
date: "2026-06-07T03:19:27+07:00"
tags: ["codeforces", "competitive-programming", "implementation"]
categories: ["algorithms"]
codeforces_contest: 440
codeforces_index: "A"
codeforces_contest_name: "Testing Round 10"
rating: 800
weight: 440
solve_time_s: 61
verified: true
draft: false
---

[CF 440A - Forgotten Episode](https://codeforces.com/problemset/problem/440/A)

**Rating:** 800  
**Tags:** implementation  
**Solve time:** 1m 1s  
**Verified:** yes  

## Solution
## Problem Understanding

We are asked to determine which episode Polycarpus has not watched in a season of a TV show. He has watched _n_ - 1 episodes out of a total of _n_, each numbered consecutively from 1 to _n_. The input gives us _n_, the total number of episodes, and a list of _n_ - 1 integers representing the episodes he has already seen. The task is to find the missing episode number.

Given that _n_ can be as large as 100,000, any solution that scales worse than O(n) could become too slow. For example, repeatedly scanning the list for each number from 1 to _n_ would be O(n²) in the worst case, which is unacceptably slow for n ≈ 10⁵. We need a solution that performs a linear pass or uses a mathematical property to reduce the work.

A non-obvious edge case occurs when the missing episode is either the first episode (1) or the last episode (n). For example, if n = 3 and the watched episodes are [2, 3], the missing episode is 1. Any solution that assumes the missing episode is somewhere in the middle of the list would fail. Similarly, if the watched episodes are [1, 2] for n = 3, the missing episode is 3, which could be overlooked if array bounds are mishandled.

## Approaches

The brute-force method would iterate through numbers 1 to _n_, checking for each number whether it exists in the watched list. This works because the list contains distinct integers in the range 1 to _n_, so any missing number is the answer. However, checking membership in a list of size _n_ - 1 is O(n), so this naive approach would perform O(n²) operations. For n = 100,000, this is roughly 10¹⁰ operations, which is far too slow for a 1-second time limit.

The optimal approach relies on a simple mathematical property. The sum of the first n natural numbers is n*(n+1)/2. If we compute this total sum and subtract the sum of all watched episodes, the difference must be the missing episode. This works because the watched episodes cover every other number exactly once. The sum computation and subtraction are both O(n), so the total runtime is linear and fits comfortably within the constraints.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n²) | O(1) | Too slow |
| Sum Difference | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the total number of episodes, n. This tells us the range of valid episode numbers.
2. Read the list of n - 1 watched episodes. Each number is guaranteed to be distinct and within 1 to n.
3. Compute the total sum of all n episode numbers using the formula n*(n+1)//2. This gives the sum we would have if no episodes were missing.
4. Compute the sum of the watched episodes. This captures all the numbers we have seen.
5. Subtract the sum of the watched episodes from the total sum. The result is the number of the episode Polycarpus forgot to watch.
6. Print this missing episode number.

The key property that ensures correctness is that the sum of all distinct numbers from 1 to n minus the sum of any n - 1 of them leaves exactly the one missing number. This works regardless of which episode is missing, including the first or last episode.

## Python Solution

```python
import sys
input = sys.stdin.readline

n = int(input())
watched = list(map(int, input().split()))

total_sum = n * (n + 1) // 2
watched_sum = sum(watched)

missing_episode = total_sum - watched_sum
print(missing_episode)
```

The code reads n and the list of watched episodes. It computes the total sum of the first n natural numbers using integer division to avoid floating-point issues. Then it computes the sum of the watched episodes and subtracts it from the total sum. Finally, it prints the missing episode. A common mistake is to forget integer division or use floating-point division, which could give incorrect results.

## Worked Examples

**Sample 1**

Input:

```
10
3 8 10 1 7 9 6 5 2
```

| Variable | Value |
| --- | --- |
| n | 10 |
| watched | [3, 8, 10, 1, 7, 9, 6, 5, 2] |
| total_sum | 55 |
| watched_sum | 51 |
| missing_episode | 4 |

The table shows that the missing episode 4 is exactly the difference between the total sum 55 and the watched sum 51.

**Custom Example**

Input:

```
3
2 3
```

| Variable | Value |
| --- | --- |
| n | 3 |
| watched | [2, 3] |
| total_sum | 6 |
| watched_sum | 5 |
| missing_episode | 1 |

This confirms that the algorithm correctly identifies the first episode as missing.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | We compute the sum of n numbers using a formula, then sum n - 1 elements of the list. |
| Space | O(n) | The list of watched episodes uses O(n) memory. |

Linear time and space are well within the 1-second and 256 MB limits for n up to 100,000.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    n = int(input())
    watched = list(map(int, input().split()))
    total_sum = n * (n + 1) // 2
    watched_sum = sum(watched)
    return str(total_sum - watched_sum)

# provided sample
assert run("10\n3 8 10 1 7 9 6 5 2\n") == "4", "sample 1"

# custom cases
assert run("3\n2 3\n") == "1", "missing first episode"
assert run("3\n1 2\n") == "3", "missing last episode"
assert run("5\n1 2 3 4\n") == "5", "small sequence, last missing"
assert run("2\n1\n") == "2", "minimum size"
assert run("4\n1 3 4\n") == "2", "missing middle episode"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 3\n2 3 | 1 | first episode missing |
| 3\n1 2 | 3 | last episode missing |
| 5\n1 2 3 4 | 5 | small sequence, last missing |
| 2\n1 | 2 | minimum size input |
| 4\n1 3 4 | 2 | missing middle episode |

## Edge Cases

If the missing episode is the first one, e.g., n = 3, watched = [2, 3], total_sum = 6, watched_sum = 5, the algorithm returns 1, which is correct. If the missing episode is the last one, e.g., n = 3, watched = [1, 2], total_sum = 6, watched_sum = 3, the algorithm returns 3. In all cases, the sum difference captures the exact missing number regardless of its position in the list.
