---
title: "CF 1478A - Nezzar and Colorful Balls"
description: "Nezzar has a sequence of balls, each labeled with a number from a non-decreasing array. He wants to color the balls using as few colors as possible with the rule that, if we isolate all balls of the same color, their numbers must strictly increase."
date: "2026-06-10T23:49:52+07:00"
tags: ["codeforces", "competitive-programming", "brute-force", "greedy"]
categories: ["algorithms"]
codeforces_contest: 1478
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 698 (Div. 2)"
rating: 800
weight: 1478
solve_time_s: 117
verified: true
draft: false
---

[CF 1478A - Nezzar and Colorful Balls](https://codeforces.com/problemset/problem/1478/A)

**Rating:** 800  
**Tags:** brute force, greedy  
**Solve time:** 1m 57s  
**Verified:** yes  

## Solution
## Problem Understanding

Nezzar has a sequence of balls, each labeled with a number from a non-decreasing array. He wants to color the balls using as few colors as possible with the rule that, if we isolate all balls of the same color, their numbers must strictly increase. A strictly increasing sequence requires each subsequent number to be larger than the previous. For single balls or isolated elements, this trivially holds.

The input consists of multiple test cases. Each test case gives the length of the array and the array itself. The numbers on the balls range from 1 to $n$, and the array is non-decreasing. The output must be the minimum number of colors required for each test case.

The constraints are small: $n$ goes up to 100, and there are at most 100 test cases. This allows algorithms with $O(n^2)$ complexity to run comfortably within time limits. However, careless handling of repeated numbers can produce wrong answers. For example, in the array `[1,1,2,2,3]`, a naive approach that simply tries to assign colors greedily from left to right without considering overlaps may use more colors than necessary. The correct answer is 2 because we can alternate colors for repeated numbers: `[1,2,1,2,1]`.

Edge cases include arrays where all numbers are identical, arrays with a single element, and arrays with strictly increasing numbers. These scenarios test whether the algorithm correctly counts repeated elements.

## Approaches

The brute-force approach would be to try every possible assignment of colors to each ball and check if the resulting sequences for each color are strictly increasing. While correct, this approach has exponential complexity in $n$ and is infeasible even for $n=20$.

The key observation is that the minimal number of colors required is determined by the maximum frequency of any single number in the array. Each repeated number needs to go into a separate color to maintain the strictly increasing condition for each color. For example, if the number 2 appears three times, we must have at least three colors, because any color can hold at most one occurrence of 2.

Thus, the optimal approach is to count the frequency of each number and take the maximum. This reduces the problem to a simple counting problem with linear time complexity relative to $n$. Since $n$ is small, this approach is extremely efficient.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(k^n) | O(n) | Too slow |
| Optimal | O(n) per test case | O(n) | Accepted |

## Algorithm Walkthrough

1. Read the number of test cases.
2. For each test case, read $n$ and the array of numbers.
3. Initialize a frequency dictionary or array to count how many times each number occurs.
4. Iterate through the array and increment the count for each number.
5. Find the maximum frequency among all numbers.
6. Print this maximum frequency as the minimum number of colors required.

Why it works: the maximum frequency of any number represents the tightest bottleneck. No color can contain more than one occurrence of the same number, so each repeated number must be split across multiple colors. Any less than the maximum frequency would violate the strictly increasing requirement for some number.

## Python Solution

```python
import sys
input = sys.stdin.readline
from collections import Counter

t = int(input())
for _ in range(t):
    n = int(input())
    a = list(map(int, input().split()))
    freq = Counter(a)
    print(max(freq.values()))
```

The code reads input efficiently using `sys.stdin.readline`. `Counter` automatically counts the frequency of each number. Using `max(freq.values())` extracts the highest frequency directly, which corresponds to the minimum number of colors. This avoids manual looping and potential off-by-one errors.

## Worked Examples

**Sample 1:**

Input: `[1, 1, 1, 2, 3, 4]`

| Number | Frequency |
| --- | --- |
| 1 | 3 |
| 2 | 1 |
| 3 | 1 |
| 4 | 1 |

Maximum frequency is 3, so we need 3 colors.

**Sample 2:**

Input: `[1, 1, 2, 2, 3]`

| Number | Frequency |
| --- | --- |
| 1 | 2 |
| 2 | 2 |
| 3 | 1 |

Maximum frequency is 2, so we need 2 colors.

These traces show that the algorithm correctly identifies the color requirement based on repeated numbers.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) per test case | Counting frequency is linear, finding the max is linear in the number of unique numbers, at most n |
| Space | O(n) per test case | Counter dictionary stores frequencies for each unique number, at most n entries |

Given $n \le 100$ and $t \le 100$, the total operations are at most $100*100=10^4$, well within the 1-second limit.

## Test Cases

```python
import sys, io
from collections import Counter

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    output = []
    t = int(input())
    for _ in range(t):
        n = int(input())
        a = list(map(int, input().split()))
        freq = Counter(a)
        output.append(str(max(freq.values())))
    return "\n".join(output)

# provided samples
assert run("5\n6\n1 1 1 2 3 4\n5\n1 1 2 2 3\n4\n2 2 2 2\n3\n1 2 3\n1\n1\n") == "3\n2\n4\n1\n1", "samples"

# custom cases
assert run("2\n3\n1 1 1\n4\n1 2 3 4\n") == "3\n1", "all same / all distinct"
assert run("1\n5\n2 2 2 2 2\n") == "5", "max frequency all same"
assert run("1\n6\n1 1 2 2 3 3\n") == "2", "multiple repeated numbers"
assert run("1\n1\n1\n") == "1", "single element"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `3\n1 1 1\n4\n1 2 3 4` | `3\n1` | Correct handling of all same vs all distinct |
| `5\n2 2 2 2 2` | `5` | Maximum frequency equals array size |
| `6\n1 1 2 2 3 3` | `2` | Multiple numbers with same maximum frequency |
| `1\n1` | `1` | Single element edge case |

## Edge Cases

For `[2,2,2,2]`, the algorithm counts 4 occurrences of 2. Maximum frequency is 4, so it outputs 4. This correctly reflects that we need 4 colors since no two balls with number 2 can share a color.

For `[1]`, frequency of 1 is 1, maximum frequency is 1, output is 1. Single-element arrays always need one color.

For `[1,2,3,4]`, all numbers are distinct, maximum frequency is 1, output is 1. This confirms the algorithm correctly handles strictly increasing sequences without unnecessary colors.

All edge cases demonstrate that the algorithm is robust and aligns exactly with the problem's requirements.
