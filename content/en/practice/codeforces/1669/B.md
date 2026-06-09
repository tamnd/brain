---
title: "CF 1669B - Triple"
description: "The problem asks us to find any number in an array that occurs at least three times. We are given multiple test cases, and for each test case, an array of integers is provided. The integers are guaranteed to be between 1 and the size of the array."
date: "2026-06-10T02:00:49+07:00"
tags: ["codeforces", "competitive-programming", "implementation", "sortings"]
categories: ["algorithms"]
codeforces_contest: 1669
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 784 (Div. 4)"
rating: 800
weight: 1669
solve_time_s: 447
verified: true
draft: false
---

[CF 1669B - Triple](https://codeforces.com/problemset/problem/1669/B)

**Rating:** 800  
**Tags:** implementation, sortings  
**Solve time:** 7m 27s  
**Verified:** yes  

## Solution
## Problem Understanding

The problem asks us to find any number in an array that occurs at least three times. We are given multiple test cases, and for each test case, an array of integers is provided. The integers are guaranteed to be between 1 and the size of the array. Our task is to output one such number if it exists or -1 if no number reaches the frequency of three.

The constraints indicate that the number of test cases can be as high as 10,000 and the total sum of array sizes across all test cases does not exceed 200,000. This means that any solution that iterates over the arrays more than once per test case, or performs nested loops, could become too slow. Therefore, we need an approach with a linear pass per test case, or at most O(n log n) per test case.

Edge cases that could cause naive solutions to fail include arrays with fewer than three elements, where it is impossible for any value to appear three times. For example, an array `[1, 2]` should immediately return -1. Another subtle case is when multiple numbers appear three times; the problem allows any valid number, so we only need to identify one. Arrays where all elements are identical, such as `[5, 5, 5, 5]`, must correctly return that value.

## Approaches

The brute-force approach would iterate through every possible value from 1 to n and count its occurrences in the array. This method is correct because it explicitly checks all elements, but in the worst case, if n is 200,000, counting each number individually leads to O(n^2) operations, which is too slow given the constraints.

The optimal approach uses a frequency counter to count all numbers in a single pass. This leverages the fact that we only need to know whether the count reaches three, not the exact count beyond three. Using a dictionary or a pre-allocated array of size n+1 (since all values are between 1 and n) lets us track frequencies in O(n) time per test case. As soon as any number reaches a count of three, we can immediately print it and stop further processing.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n^2) | O(1) | Too slow |
| Frequency Counter | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Read the number of test cases t.
2. For each test case, read n and the array of n integers.
3. Initialize a frequency counter. If using a list, allocate n+1 zeros to track counts from 1 to n.
4. Iterate through each number in the array. Increment its count in the frequency counter.
5. As soon as a number reaches a count of three, print that number and stop processing the current test case.
6. If the end of the array is reached without any number reaching three, print -1.

The algorithm works because the frequency counter ensures we track exactly how many times each number appears. By checking immediately when a count reaches three, we guarantee that any valid output is printed without unnecessary computation.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        n = int(input())
        arr = list(map(int, input().split()))
        freq = [0] * (n + 1)
        found = False
        for num in arr:
            freq[num] += 1
            if freq[num] == 3:
                print(num)
                found = True
                break
        if not found:
            print(-1)

if __name__ == "__main__":
    solve()
```

The code reads the input efficiently using `sys.stdin.readline` and initializes a list `freq` to count occurrences of each number. By breaking immediately when a number reaches a
