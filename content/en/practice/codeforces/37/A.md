---
title: "CF 37A - Towers"
description: "We are given a set of wooden bars, each with a positive integer length. Vasya wants to build towers by stacking bars of"
date: "2026-05-28T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "sortings"]
categories: ["algorithms"]
codeforces_contest: 37
codeforces_index: "A"
codeforces_contest_name: "Codeforces Beta Round 37"
rating: 1000
weight: 37
solve_time_s: 53
verified: true
draft: false
---

[CF 37A - Towers](https://codeforces.com/problemset/problem/37/A)

**Rating:** 1000  
**Tags:** sortings  
**Solve time:** 53s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a set of wooden bars, each with a positive integer length. Vasya wants to build towers by stacking bars of the same length. Each tower must consist of bars that are identical in length, but different towers can have different lengths. The goal is to construct all the bars into towers while minimizing the number of towers and reporting the height of the tallest tower.

The input consists of the number of bars $N$ (1 ≤ N ≤ 1000) and a list of their lengths. The output requires two integers: the maximum number of bars stacked in a single tower and the total number of towers.

The constraints are moderate. $N$ can be up to 1000, which allows algorithms with time complexity up to $O(N^2)$ comfortably. However, since the lengths are integers bounded by 1000, we can exploit this to compute counts efficiently without iterating through all pairs of bars. This hints at a frequency-counting approach rather than a nested-loop construction.

Non-obvious edge cases include:

1. All bars have unique lengths. For example, input `5\n1 2 3 4 5` results in 5 towers each of height 1. A careless approach that tries to "combine" bars would fail.
2. All bars have the same length. Input `4\n7 7 7 7` should yield a single tower of height 4.
3. Mixed repetitions. Input `6\n1 2 2 3 3 3` should produce towers of heights 1, 2, and 3, with the tallest tower height 3. Naive sorting without counting could make it less obvious how to compute the number of towers efficiently.

## Approaches

The brute-force approach would be to simulate building towers explicitly. We could iterate over each bar and try to place it on an existing tower of the same length, or start a new tower. For $N = 1000$, this involves checking every existing tower for every bar, potentially leading to $O(N^2)$ operations. While this is feasible here, it is unnecessarily complicated and error-prone when the heights and counts can be derived more directly.

The key insight is that the height of the tallest tower is determined by the maximum frequency of any bar length, and the total number of towers is determined by the number of distinct lengths. Counting frequencies turns the problem into a simple pass through the data. By storing how many bars of each length exist, the tallest tower is simply the maximum count, and the number of towers is the number of unique lengths.

The observation that "we only need counts, not explicit tower structures" transforms the problem from a simulation to a counting problem, reducing complexity from $O(N^2)$ to $O(N)$.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(N^2) | O(N) | Works but overkill |
| Optimal | O(N) | O(L) where L ≤ 1000 | Accepted |

## Algorithm Walkthrough

1. Initialize a dictionary (or array of size 1001) to count the frequency of each bar length. This structure maps each length to the number of bars of that length.
2. Iterate through all bar lengths. For each length, increment its count in the frequency dictionary. This step gives the full distribution of bar lengths.
3. Determine the height of the tallest tower by finding the maximum value in the frequency dictionary. The largest number of identical bars directly corresponds to the tallest tower.
4. Count the total number of towers by computing the number of unique lengths present in the dictionary. Each unique length forms exactly one tower.
5. Output the height of the tallest tower and the total number of towers.

Why it works: At each point, the algorithm keeps a complete count of each bar length. The tallest tower cannot exceed the count of the most frequent length, and each distinct length must contribute at least one tower. No information is lost, so the final answer is exact.

## Python Solution

```python
import sys
input = sys.stdin.readline

N = int(input())
lengths = list(map(int, input().split()))

# count frequencies
freq = {}
for l in lengths:
    if l in freq:
        freq[l] += 1
    else:
        freq[l] = 1

max_height = max(freq.values())
num_towers = len(freq)

print(max_height, num_towers)
```

The solution first reads input efficiently using `sys.stdin.readline`. The frequency dictionary `freq` stores counts of each length, and we directly compute the maximum value for the tallest tower. The number of keys in the dictionary gives the number of distinct towers. This avoids any off-by-one errors or unnecessary loops.

## Worked Examples

**Sample 1**

Input:

```
3
1 2 3
```

| Step | freq | max_height | num_towers |
| --- | --- | --- | --- |
| initial | {} | - | - |
| after counting 1 | {1:1} | 1 | 1 |
| after counting 2 | {1:1,2:1} | 1 | 2 |
| after counting 3 | {1:1,2:1,3:1} | 1 | 3 |

This confirms that each bar forms its own tower. Tallest tower is 1, total towers 3.

**Custom Example**

Input:

```
6
1 2 2 3 3 3
```

| Step | freq | max_height | num_towers |
| --- | --- | --- | --- |
| after counting all | {1:1,2:2,3:3} | 3 | 3 |

This shows that repeated lengths stack correctly. Maximum frequency determines tallest tower, distinct keys determine number of towers.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(N) | One pass to read input and one pass to build counts. |
| Space | O(L) where L ≤ 1000 | Frequency dictionary stores at most 1000 keys, one per possible length. |

With N ≤ 1000 and lengths ≤ 1000, the solution runs comfortably within 2 seconds and uses minimal memory.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    N = int(input())
    lengths = list(map(int, input().split()))
    freq = {}
    for l in lengths:
        freq[l] = freq.get(l, 0) + 1
    return f"{max(freq.values())} {len(freq)}"

# provided sample
assert run("3\n1 2 3\n") == "1 3"

# all equal
assert run("4\n7 7 7 7\n") == "4 1"

# mixed repetitions
assert run("6\n1 2 2 3 3 3\n") == "3 3"

# minimum input
assert run("1\n5\n") == "1 1"

# maximum input with distinct values
assert run("1000\n" + " ".join(map(str, range(1,1001))) + "\n") == "1 1000"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 4\n7 7 7 7 | 4 1 | All bars identical, single tower |
| 6\n1 2 2 3 3 3 | 3 3 | Mixed counts, tallest tower computation |
| 1\n5 | 1 1 | Minimum-size input |
| 1000\n1 2 3 ... 1000 | 1 1000 | Maximum-size input, all distinct |

## Edge Cases

For input `4\n7 7 7 7`, the frequency dictionary becomes `{7:4}`. `max(freq.values())` correctly returns 4 for tallest tower, and `len(freq)` returns 1. No iteration over individual bars beyond counting is needed.

For input `6\n1 2 2 3 3 3`, the dictionary `{1:1,2:2,3:3}` produces a tallest tower height 3, number of towers 3. This confirms that the algorithm correctly handles varying repetitions without additional logic for stacking.
