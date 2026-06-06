---
title: "CF 347A - Difference Row"
description: "We are given a list of n integers and need to arrange them in a row such that the sum of differences between consecutive numbers is maximized. Concretely, if the arrangement is $x1, x2, dots, xn$, the value is calculated as $(x1 - x2) + (x2 - x3) + dots + (x{n-1} - xn)$."
date: "2026-06-06T18:28:56+07:00"
tags: ["codeforces", "competitive-programming", "constructive-algorithms", "implementation", "sortings"]
categories: ["algorithms"]
codeforces_contest: 347
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 201 (Div. 2)"
rating: 1300
weight: 347
solve_time_s: 74
verified: true
draft: false
---

[CF 347A - Difference Row](https://codeforces.com/problemset/problem/347/A)

**Rating:** 1300  
**Tags:** constructive algorithms, implementation, sortings  
**Solve time:** 1m 14s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a list of _n_ integers and need to arrange them in a row such that the sum of differences between consecutive numbers is maximized. Concretely, if the arrangement is $x_1, x_2, \dots, x_n$, the value is calculated as $(x_1 - x_2) + (x_2 - x_3) + \dots + (x_{n-1} - x_n)$. Observing the formula, the intermediate terms cancel, leaving the total value as $x_1 - x_n$. This means the maximum value is obtained by placing the largest number first and the smallest number last. The challenge, however, is that the problem also requires the lexicographically smallest sequence among all arrangements that produce this maximum value.

The constraints are moderate: $n$ goes up to 100, and integers range from -1000 to 1000. This allows solutions up to $O(n^2)$ comfortably, but naive permutations, which scale as $O(n!)$, are impractical. Edge cases include sequences where multiple elements have the same maximum or minimum, sequences with only two elements, and sequences where all numbers are equal. A naive approach might choose any order without ensuring lexicographical minimality, producing a correct maximum value but the wrong output sequence.

## Approaches

The brute-force method would generate all permutations of the input array, calculate the value for each permutation, and select the one with the highest value, breaking ties by lexicographical comparison. For $n = 100$, this approach is impossible because $100!$ permutations is astronomically large.

The key insight comes from observing the cancellation in the difference sum. The sum simplifies to $x_1 - x_n$. Maximizing this requires placing the largest number first and the smallest number last. Once the first and last positions are fixed, the remaining numbers do not influence the sum. To obtain the lexicographically smallest sequence, the middle numbers should be arranged in ascending order. This guarantees the smallest possible sequence for the given first and last numbers.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n!) | O(n) | Too slow |
| Optimal | O(n log n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Sort the array in ascending order. This allows easy identification of the smallest and largest numbers and simplifies constructing a lexicographically minimal sequence.
2. Place the largest number at the first position. This maximizes $x_1$ in the simplified sum $x_1 - x_n$.
3. Place the smallest number at the last position. This minimizes $x_n$ in the sum.
4. Take the remaining numbers (all numbers except the largest and smallest) and place them in ascending order between the first and last positions. This ensures the sequence is lexicographically minimal while maintaining the maximum value.
5. Print the resulting sequence.

Why it works: By fixing the largest and smallest numbers at the ends, we guarantee the maximum difference. Ordering the middle numbers ascending ensures the smallest possible sequence lexicographically. Any other order of middle numbers would not change the sum but would result in a larger lexicographical sequence.

## Python Solution

```python
import sys
input = sys.stdin.readline

n = int(input())
a = list(map(int, input().split()))

a.sort()
largest = a[-1]
smallest = a[0]
middle = a[1:-1]

result = [largest] + middle + [smallest]
print(' '.join(map(str, result)))
```

The code first sorts the input array. `largest` takes the last element, `smallest` takes the first, and `middle` contains all elements in between. Concatenating them as `[largest] + middle + [smallest]` produces the desired output. Sorting the middle ensures lexicographical minimality. The approach carefully avoids modifying the original array in a way that would break the order.

## Worked Examples

**Sample 1**

Input: `5\n100 -100 50 0 -50\n`

| Step | Array | Action | Result |
| --- | --- | --- | --- |
| 1 | [-100, -50, 0, 50, 100] | Sorted | [-100, -50, 0, 50, 100] |
| 2 | 100 | Pick largest | largest = 100 |
| 3 | -100 | Pick smallest | smallest = -100 |
| 4 | [-50, 0, 50] | Middle | middle = [-50, 0, 50] |
| 5 | Concatenate | [100] + [-50, 0, 50] + [-100] | [100, -50, 0, 50, -100] |

This sequence produces the sum `(100 - (-50)) + (-50 - 0) + (0 - 50) + (50 - (-100)) = 200`.

**Sample 2**

Input: `4\n1 2 3 4\n`

| Step | Array | Action | Result |
| --- | --- | --- | --- |
| 1 | [1, 2, 3, 4] | Sorted | [1, 2, 3, 4] |
| 2 | 4 | Pick largest | largest = 4 |
| 3 | 1 | Pick smallest | smallest = 1 |
| 4 | [2, 3] | Middle | middle = [2, 3] |
| 5 | Concatenate | [4] + [2, 3] + [1] | [4, 2, 3, 1] |

Sum: `(4 - 2) + (2 - 3) + (3 - 1) = 3 + (-1) + 2 = 4`, which is maximal.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n) | Sorting dominates the runtime, all other operations are O(n) |
| Space | O(n) | Storing the array and constructing the result sequence |

With $n \le 100$, $O(n \log n)$ is negligible and fits well within the 2-second time limit.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    n = int(input())
    a = list(map(int, input().split()))
    a.sort()
    largest = a[-1]
    smallest = a[0]
    middle = a[1:-1]
    result = [largest] + middle + [smallest]
    return ' '.join(map(str, result))

# Provided samples
assert run("5\n100 -100 50 0 -50\n") == "100 -50 0 50 -100", "sample 1"
assert run("4\n1 2 3 4\n") == "4 2 3 1", "sample 2"

# Custom cases
assert run("2\n10 -10\n") == "10 -10", "two elements"
assert run("3\n5 5 5\n") == "5 5 5", "all equal"
assert run("5\n-1 -2 -3 -4 -5\n") == "-1 -4 -3 -2 -5", "negative numbers"
assert run("6\n0 100 -100 50 -50 25\n") == "100 -50 0 25 50 -100", "mixed numbers"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 2\n10 -10 | 10 -10 | Minimum size input |
| 3\n5 5 5 | 5 5 5 | All elements equal |
| 5\n-1 -2 -3 -4 -5 | -1 -4 -3 -2 -5 | Negative numbers handling |
| 6\n0 100 -100 50 -50 25 | 100 -50 0 25 50 -100 | Mixed numbers, lexicographical order |

## Edge Cases

For `n = 2`, the array `[10, -10]` directly yields `[10, -10]` with sum `20`. There are no middle elements, so lexicographical choice is trivial. When all numbers are equal, for instance `[5, 5, 5]`, the maximum sum is zero, and any permutation is valid. Sorting and following the algorithm still yields `[5, 5, 5]`, which is lexicographically minimal. For sequences with negative numbers or mixed signs, the same logic applies, and sorting ensures the middle numbers maintain lexicographical minimality while preserving the maximum difference sum.
