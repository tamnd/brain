---
title: "CF 1509A - Average Height"
description: "We are asked to arrange a set of students in a line so that the number of photogenic consecutive pairs is maximized. A pair is photogenic if the average of their heights is an integer. The input consists of multiple test cases."
date: "2026-06-10T19:47:05+07:00"
tags: ["codeforces", "competitive-programming", "constructive-algorithms"]
categories: ["algorithms"]
codeforces_contest: 1509
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 715 (Div. 2)"
rating: 800
weight: 1509
solve_time_s: 181
verified: false
draft: false
---

[CF 1509A - Average Height](https://codeforces.com/problemset/problem/1509/A)

**Rating:** 800  
**Tags:** constructive algorithms  
**Solve time:** 3m 1s  
**Verified:** no  

## Solution
## Problem Understanding

We are asked to arrange a set of students in a line so that the number of photogenic consecutive pairs is maximized. A pair is photogenic if the average of their heights is an integer. The input consists of multiple test cases. Each test case gives a list of integers representing the heights of the students. The output must be a permutation of these heights for each test case that maximizes the number of photogenic pairs.

The main observation is that a pair of numbers has an integer average if both numbers are either even or odd. This immediately reduces the problem to a simple classification: we want consecutive numbers to share the same parity. The sum of heights across all test cases is bounded by 2000, so an algorithm that runs in linear time with respect to the number of heights per test case is sufficient.

Edge cases that can be tricky include when all numbers are even, all numbers are odd, or there is only a single number of one parity. For example, if the heights are `[2, 4, 6]`, any order produces all photogenic pairs. If the heights are `[1, 2, 3]`, careful arrangement is needed to maximize consecutive pairs.

## Approaches

The brute-force approach would be to generate all permutations of the list of heights, count the number of photogenic consecutive pairs for each permutation, and select the one with the maximum count. For `n` up to 2000, this is clearly infeasible since it has factorial time complexity. Even for `n=10`, there are 3.6 million permutations.

The key insight is that the photogenic property depends solely on parity. By separating the numbers into two groups, odd and even, we can ensure that every pair of consecutive numbers in the same group will be photogenic. This reduces the problem to a simple sorting or grouping task. The simplest approach is to output all even numbers followed by all odd numbers (or vice versa). Any two consecutive numbers within the same parity group will be photogenic, and there is no way to create additional photogenic pairs between numbers of opposite parity. This guarantees an optimal arrangement.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n!) | O(n) | Too slow |
| Parity Grouping | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

1. For each test case, read the number of students `n` and the list of their heights.
2. Initialize two empty lists: one for odd heights and one for even heights.
3. Iterate through the list of heights. If a height is odd, append it to the odd list. If it is even, append it to the even list.
4. Concatenate the even list and the odd list. This ordering ensures that all consecutive numbers within each group have the same parity, maximizing the number of photogenic pairs.
5. Output the concatenated list.

Why it works: Consecutive pairs of the same parity always produce an integer average. By grouping all even numbers together and all odd numbers together, we guarantee the maximum number of such pairs. Any attempt to interleave numbers of different parity cannot increase the number of photogenic pairs, so this strategy is optimal.

## Python Solution

```python
import sys
input = sys.stdin.readline

t = int(input())
for _ in range(t):
    n = int(input())
    heights = list(map(int, input().split()))
    odd = []
    even = []
    for h in heights:
        if h % 2 == 0:
            even.append(h)
        else:
            odd.append(h)
    result = even + odd
    print(" ".join(map(str, result)))
```

The solution reads input efficiently using `sys.stdin.readline`. It separates heights by parity and concatenates the lists. This ordering guarantees the optimal number of photogenic consecutive pairs. Boundary conditions, such as all numbers being even or odd, are handled naturally.

## Worked Examples

### Example 1

Input: `[1, 1, 2]`

| Step | Even List | Odd List | Result |
| --- | --- | --- | --- |
| Initial | [] | [] | [] |
| 1 | [] | [1] | [] |
| 2 | [] | [1, 1] | [] |
| 3 | [2] | [1, 1] | [2, 1, 1] |

Output: `[2, 1, 1]` (or `[1, 1, 2]`). The photogenic pair is `(1,1)`.

### Example 2

Input: `[10, 9, 13, 15, 3, 16, 9, 13]`

| Step | Even List | Odd List | Result |
| --- | --- | --- | --- |
| Initial | [] | [] | [] |
| 10 | [10] | [] | [] |
| 9 | [10] | [9] | [] |
| 13 | [10] | [9,13] | [] |
| 15 | [10] | [9,13,15] | [] |
| 3 | [10] | [9,13,15,3] | [] |
| 16 | [10,16] | [9,13,15,3] | [] |
| 9 | [10,16] | [9,13,15,3,9] | [] |
| 13 | [10,16] | [9,13,15,3,9,13] | [] |
| Concatenate | [10,16] | [9,13,15,3,9,13] | [10,16,9,13,15,3,9,13] |

Output maximizes photogenic pairs within each group.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) per test case | One pass to separate heights by parity, one pass to concatenate and print |
| Space | O(n) | Two additional lists for odd and even heights |

The sum of `n` over all test cases is ≤ 2000, so total operations are well within limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    output = io.StringIO()
    sys.stdout = output
    t = int(input())
    for _ in range(t):
        n = int(input())
        heights = list(map(int, input().split()))
        odd = []
        even = []
        for h in heights:
            if h % 2 == 0:
                even.append(h)
            else:
                odd.append(h)
        result = even + odd
        print(" ".join(map(str, result)))
    return output.getvalue().strip()

# Provided samples
assert run("4\n3\n1 1 2\n3\n1 1 1\n8\n10 9 13 15 3 16 9 13\n2\n18 9\n") == "2 1 1\n1 1 1\n10 16 9 13 15 3 9 13\n18 9"

# Custom test cases
assert run("1\n2\n2 4\n") == "2 4", "all even numbers"
assert run("1\n3\n1 3 5\n") == "1 3 5", "all odd numbers"
assert run("1\n4\n1 2 3 4\n") == "2 4 1 3", "mix of odd and even"
assert run("1\n5\n5 4 3 2 1\n") == "4 2 5 3 1", "descending mix"
assert run("1\n2\n1 2\n") == "2 1", "minimum size input"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `2 4` | `2 4` | all even numbers produce all photogenic pairs |
| `1 3 5` | `1 3 5` | all odd numbers produce all photogenic pairs |
| `1 2 3 4` | `2 4 1 3` | mixed parity arrangement maximizes photogenic pairs |
| `5 4 3 2 1` | `4 2 5 3 1` | descending input with mixed parity |
| `1 2` | `2 1` | minimum size edge case |

## Edge Cases

If all heights are of the same parity, the algorithm will place them in their original group, producing the maximum number of photogenic pairs automatically. For example, input `[2, 4, 6]` results in `[2,4,6]`, with two photogenic pairs `(2,4)` and `(4,6)`.

If only one height of a certain parity exists, it is placed at the end of the concatenation, which is optimal. For `[1,2,4]`, the even numbers `[2,4]` are placed first, followed by the single odd `1`. The photogenic pairs `(2,4)` is counted, and no additional pairs are possible with the odd number.
