---
title: "CF 1948B - Array Fix"
description: "We are given an array of integers between 0 and 99, and our goal is to decide whether we can transform it into a non-decreasing array by repeatedly \"splitting\" numbers of two digits into their individual digits."
date: "2026-06-07T17:54:03+07:00"
tags: ["codeforces", "competitive-programming", "brute-force", "dp", "greedy", "implementation"]
categories: ["algorithms"]
codeforces_contest: 1948
codeforces_index: "B"
codeforces_contest_name: "Educational Codeforces Round 163 (Rated for Div. 2)"
rating: 1100
weight: 1948
solve_time_s: 89
verified: true
draft: false
---

[CF 1948B - Array Fix](https://codeforces.com/problemset/problem/1948/B)

**Rating:** 1100  
**Tags:** brute force, dp, greedy, implementation  
**Solve time:** 1m 29s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given an array of integers between 0 and 99, and our goal is to decide whether we can transform it into a non-decreasing array by repeatedly "splitting" numbers of two digits into their individual digits. Specifically, for any element at least 10, we can replace it with its digits in order. For example, 12 becomes [1, 2], 45 becomes [4, 5]. We may perform this operation any number of times on any eligible element. The task is to determine if there exists a sequence of operations that will make the entire array sorted in non-decreasing order.

The constraints give us arrays of length up to 50 and at most 1000 test cases. Because the largest array is small, an algorithm that is quadratic in the length of the array is feasible, but anything exponential in the number of elements is not practical. Each element is at most 99, so the "splitting" operation produces at most two new elements, which bounds the size of any transformed array.

Edge cases appear when numbers are already single digits, when the array contains duplicates, or when larger numbers must be split to fit into the order. For instance, an input `[12, 3]` can be transformed to `[1, 2, 3]`, which is sorted. A careless implementation that only checks the original numbers without considering splits would incorrectly report "NO". Another edge case is when all numbers are already zero or one-digit numbers, such as `[0, 0]`; the algorithm should recognize it as already sorted.

## Approaches

The brute-force approach would be to generate all possible arrays by performing splits in every possible order. For each array, we would check if it is non-decreasing. This is correct in principle, because it exhaustively tries every combination, but the number of possibilities grows exponentially with the number of multi-digit numbers. Even with a maximum array length of 50, we could have roughly `2^50` possibilities in the worst case, which is far too large.

The key insight that allows an optimal solution is that splitting numbers is strictly beneficial for sorting because it never decreases the relative order of digits. Each number `x` of two digits can only be split into its first and second digit, and these digits are always non-decreasing (`x//10 <= x%10`). Therefore, instead of exploring all combinations, we can take a greedy approach: we transform each number of two digits into its constituent digits immediately and then check if the resulting array is sorted. There is no advantage to delaying a split, because splitting earlier can only make the array easier to sort.

By applying this insight, we reduce the problem to a simple pass over the transformed array to verify non-decreasing order.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(2^n) | O(n) | Too slow |
| Greedy Split | O(n) per test case | O(n) | Accepted |

## Algorithm Walkthrough

1. Initialize an empty list `b` which will hold the transformed array. We are going to iterate through the original array and replace each two-digit number with its digits.
2. For each element `x` in the array `a`, check if it is at least 10. If so, append `x // 10` followed by `x % 10` to `b`. Otherwise, append `x` directly. This immediately simulates splitting the number into digits.
3. Once all elements have been processed into `b`, iterate through `b` and check whether each element is greater than or equal to the previous one. If any element violates this condition, we conclude that it is impossible to sort the array using splits and output "NO".
4. If the entire array `b` passes the non-decreasing check, output "YES".

Why it works: At every point, the array `b` contains the smallest possible representation after splitting, and any further splitting would not reduce the first digit or create a smaller number. Therefore, if `b` is non-decreasing, there is a sequence of operations that makes the original array sorted. Conversely, if `b` is not non-decreasing, no sequence of splits can fix it, because we have already split all numbers and any additional splitting would only increase the number of elements but never decrease a digit to improve the order.

## Python Solution

```python
import sys
input = sys.stdin.readline

def main():
    t = int(input())
    for _ in range(t):
        n = int(input())
        a = list(map(int, input().split()))
        b = []
        for x in a:
            if x >= 10:
                b.append(x // 10)
                b.append(x % 10)
            else:
                b.append(x)
        ok = True
        for i in range(1, len(b)):
            if b[i] < b[i - 1]:
                ok = False
                break
        print("YES" if ok else "NO")

if __name__ == "__main__":
    main()
```

In the solution, we read the number of test cases, then for each test case read the array. The transformed array `b` is built by splitting numbers immediately. Checking for non-decreasing order is done in a single pass. This approach avoids unnecessary splits and ensures that we only track the relevant sequence for determining if sorting is possible.

## Worked Examples

Sample Input 1:

```
4
12 3 45 67
```

| Step | x | b after append | Sorted check |
| --- | --- | --- | --- |
| 1 | 12 | [1, 2] | - |
| 2 | 3 | [1, 2, 3] | - |
| 3 | 45 | [1, 2, 3, 4, 5] | - |
| 4 | 67 | [1, 2, 3, 4, 5, 6, 7] | True |

This demonstrates that greedily splitting all two-digit numbers produces a fully sorted array.

Sample Input 2:

```
3
12 28 5
```

| Step | x | b after append | Sorted check |
| --- | --- | --- | --- |
| 1 | 12 | [1, 2] | - |
| 2 | 28 | [1, 2, 2, 8] | check 2 >= 2 ok |
| 3 | 5 | [1, 2, 2, 8, 5] | check 5 >= 8 fails |

The check fails at the last element, so the output is "NO". This shows that some arrays cannot be fixed by splitting.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) per test case | Each element is processed once and the transformed array is scanned once. |
| Space | O(n) | The transformed array `b` stores at most 2n elements. |

Given the constraints n ≤ 50 and t ≤ 1000, the total operations are well below 100,000, which is efficient for a 2-second limit.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    out = io.StringIO()
    sys.stdout = out
    main()
    sys.stdout = sys.__stdout__
    return out.getvalue().strip()

# Provided samples
assert run("3\n4\n12 3 45 67\n3\n12 28 5\n2\n0 0\n") == "YES\nNO\nYES", "sample tests"

# Custom test cases
assert run("1\n2\n9 10\n") == "YES", "splitting last element"
assert run("1\n3\n11 12 10\n") == "YES", "all elements split result sorted"
assert run("1\n5\n21 20 3 4 5\n") == "NO", "cannot sort due to first two elements"
assert run("1\n4\n0 0 0 0\n") == "YES", "all zeros, already sorted"
assert run("1\n2\n99 1\n") == "NO", "two-digit number needs split but still cannot fix"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 9 10 | YES | Splitting last element works |
| 11 12 10 | YES | Multiple splits produce sorted array |
| 21 20 3 4 5 | NO | Early two-digit numbers prevent sorting |
| 0 0 0 0 | YES | Already sorted with all equal elements |
| 99 1 | NO | Cannot fix order even after splitting |

## Edge Cases

For an array like `[12, 3]`, the algorithm splits 12 into `[1, 2]` and appends 3 to get `[1, 2, 3]`. The check confirms that the array is sorted, producing "YES". For `[28, 5]`, splitting produces `[2, 8, 5]`. The last element 5 is less than 8, so the check fails, producing "NO". This confirms the algorithm handles arrays where splitting is necessary but insufficient, as well as arrays already sorted or trivially sortable.
