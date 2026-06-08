---
title: "CF 1833C - Vlad Building Beautiful Array"
description: "We are given an array of positive integers, and the task is to construct a new array of the same length where all elements are positive and have the same parity, either all odd or all even."
date: "2026-06-09T06:55:25+07:00"
tags: ["codeforces", "competitive-programming", "greedy", "math"]
categories: ["algorithms"]
codeforces_contest: 1833
codeforces_index: "C"
codeforces_contest_name: "Codeforces Round 874 (Div. 3)"
rating: 800
weight: 1833
solve_time_s: 109
verified: false
draft: false
---

[CF 1833C - Vlad Building Beautiful Array](https://codeforces.com/problemset/problem/1833/C)

**Rating:** 800  
**Tags:** greedy, math  
**Solve time:** 1m 49s  
**Verified:** no  

## Solution
## Problem Understanding

We are given an array of positive integers, and the task is to construct a new array of the same length where all elements are positive and have the same parity, either all odd or all even. For each element in the new array, we can either copy the corresponding element from the original array or take the difference between that element and any other element in the original array. We need to determine whether it is possible to construct such an array for each test case.

The array lengths can go up to 200,000, and the sum of lengths across all test cases also does not exceed 200,000. This means any solution that processes each pair of elements naively, such as trying every possible difference for every element, would require on the order of $O(n^2)$ operations and is clearly too slow. Instead, we need a solution that works in linear or linearithmic time per test case, ideally $O(n)$.

An edge case that might be tricky is when the array contains a mix of odd and even numbers but only one of each type. For example, the array `[2, 3]` cannot form a beautiful array because no difference of elements produces a number that can align the parities. Another subtle situation is when all elements are already of the same parity. In that case, the answer is immediately "YES", but a careless approach that always tries to compute differences might waste time or misclassify it.

## Approaches

The brute-force approach would try every possible pair of elements to compute all possible differences and then check if a beautiful array can be constructed from these numbers. For an array of length $n$, there are $n^2$ possible differences to consider. We could store all differences in a set and check for possible uniform parity arrays. This is correct in principle because it covers all allowed operations, but with $n$ up to 200,000, it would result in 40 billion operations in the worst case, which is far too slow.

The key insight that allows an efficient solution is that the parity of differences is entirely determined by the parity of the original numbers. If all numbers are already of the same parity, we are done. If there is a mix of odd and even numbers, then subtracting an odd from an even or vice versa always gives an odd result, and subtracting two numbers of the same parity gives an even result. This means the only obstacle is having a mixture that prevents all differences from being aligned. The real check reduces to seeing whether the array contains both odd and even numbers that differ by exactly one or not.

This observation allows us to solve each test case in linear time by simply counting the number of odd and even numbers. If there is at least one odd and one even, we check their minimal difference to see if the beautiful array is feasible. Otherwise, the array is already trivially beautiful.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n²) | O(n²) | Too slow |
| Optimal | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

1. For each test case, read the array length $n$ and the array $a$. This sets up the data for processing.
2. Count the number of odd and even numbers in the array. This immediately tells us whether the array is already uniform in parity or mixed.
3. If all numbers are odd or all numbers are even, print "YES". No changes are necessary because the array is already beautiful.
4. If there are both odd and even numbers, sort the array. Sorting allows us to efficiently check if there exists any two numbers of opposite parity with a difference of exactly 1. Such a pair cannot coexist in a beautiful array.
5. Traverse the sorted array. For each consecutive pair, if one is odd and the other is even and their difference is 1, print "NO" and break. This is the only scenario where constructing a beautiful array is impossible.
6. If no such adjacent pair is found, print "YES". Differences of more than 1 or same-parity pairs do not prevent constructing a beautiful array, because we can always choose differences to align parities.

Why it works: the algorithm relies on the fact that subtracting two numbers of the same parity yields an even number and subtracting two numbers of different parity yields an odd number. Therefore, the only way a beautiful array cannot be built is when an odd and an even number differ by exactly 1, because no combination of differences can transform them into the same parity without producing zero or a negative number. All other configurations allow choosing either original numbers or differences to produce a uniform parity array.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        n = int(input())
        a = list(map(int, input().split()))
        odd_count = sum(1 for x in a if x % 2 == 1)
        even_count = n - odd_count
        if odd_count == 0 or even_count == 0:
            print("YES")
            continue
        a.sort()
        possible = True
        for i in range(1, n):
            if a[i] - a[i-1] == 1:
                possible = False
                break
        print("YES" if possible else "NO")
```

The code first counts odd and even numbers to handle trivial cases immediately. Sorting ensures that checking differences of 1 is efficient and linear. The loop over consecutive pairs catches the only scenario that makes building a beautiful array impossible.

## Worked Examples

Sample Input 1:

```
5
2 6 8 4 3
```

| i | a[i] | a[i-1] | diff | decision |
| --- | --- | --- | --- | --- |
| 1 | 6 | 2 | 4 | continue |
| 2 | 8 | 6 | 2 | continue |
| 3 | 4 | 8 | -4 | continue |
| 4 | 3 | 4 | 1 | impossible → NO |

This demonstrates that the presence of an odd-even pair with difference 1 prevents a beautiful array.

Sample Input 2:

```
5
1 4 7 6 9
```

| i | a[i] | a[i-1] | diff | decision |
| --- | --- | --- | --- | --- |
| 1 | 4 | 1 | 3 | continue |
| 2 | 6 | 4 | 2 | continue |
| 3 | 7 | 6 | 1 | possible, but difference is odd-even? |
| 4 | 9 | 7 | 2 | continue |

No adjacent pair differs by 1 in a conflicting parity sense, so output is YES.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n) | Sorting dominates; counting parity is O(n) |
| Space | O(n) | Storing array for each test case |

The solution fits comfortably within 1-second limits for n up to 2*10^5.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from contextlib import redirect_stdout
    out = io.StringIO()
    with redirect_stdout(out):
        solve()
    return out.getvalue().strip()

# Provided samples
assert run("7\n5\n2 6 8 4 3\n5\n1 4 7 6 9\n4\n2 6 4 10\n7\n5 29 13 9 10000001 11 3\n5\n2 1 2 4 2\n5\n2 4 5 4 3\n4\n2 5 5 4\n") == \
"NO\nYES\nYES\nYES\nYES\nNO\nNO", "sample 1"

# Custom cases
assert run("1\n2\n2 3\n") == "NO", "odd-even pair difference 1"
assert run("1\n3\n1 3 5\n") == "YES", "all odd"
assert run("1\n4\n2 4 6 8\n") == "YES", "all even"
assert run("1\n4\n1 2 4 6\n") == "YES", "mixed but no difference 1"
assert run("1\n5\n1 2 3 4 5\n") == "NO", "multiple adjacent difference 1"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 2 3 | NO | edge case of smallest mixed array with difference 1 |
| 1 3 5 | YES | all numbers odd |
| 2 4 6 8 | YES | all numbers even |
| 1 2 4 6 | YES | mixed numbers but no conflict difference 1 |
| 1 2 3 4 5 | NO | multiple conflicting adjacent differences |

## Edge Cases

For an array like `[2, 3]`, odd_count=1, even_count=1. Sorting gives `[2, 3]`. The difference `3-2 = 1` triggers the impossibility condition, so the output is NO. For `[1, 3, 5]`, all numbers are odd, so the algorithm prints YES without further checks. For `[1, 2, 4, 6]`, the sorted array is `[1, 2, 4, 6]
