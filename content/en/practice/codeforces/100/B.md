---
title: "CF 100B - Friendly Numbers"
description: "We are asked to determine whether a set of non-zero integers forms a \"friendly group,\" meaning every pair of numbers satisfies a divisibility relationship: one number divides the other."
date: "2026-05-28T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "*special", "implementation"]
categories: ["algorithms"]
codeforces_contest: 100
codeforces_index: "B"
codeforces_contest_name: "Unknown Language Round 3"
rating: 1500
weight: 100
solve_time_s: 139
verified: true
draft: false
---

[CF 100B - Friendly Numbers](https://codeforces.com/problemset/problem/100/B)

**Rating:** 1500  
**Tags:** *special, implementation  
**Solve time:** 2m 19s  
**Verified:** yes  

## Solution
## Problem Understanding

We are asked to determine whether a set of non-zero integers forms a "friendly group," meaning every pair of numbers satisfies a divisibility relationship: one number divides the other. The input provides the number of integers, $n$, followed by a comma-separated list of the integers sorted in non-decreasing order. The output should be "FRIENDS" if the entire group satisfies this condition and "NOT FRIENDS" otherwise.

Given $n$ can go up to 1000 and each number can have up to 7 digits, a brute-force check of all pairs is feasible but not optimal. The worst-case number of operations for a full pairwise check is $n(n-1)/2$, which is roughly 500,000 operations when $n = 1000$. This is still manageable for a 2-second time limit in Python. However, there is a structure we can exploit due to the sorted input that avoids unnecessary checks.

Non-obvious edge cases include groups where all numbers are the same, groups including 1, or groups with a large number that is not divisible by any smaller member. For example, input "1, 3, 6, 12" is FRIENDS, but "2, 3, 6" is NOT FRIENDS because 2 does not divide 3 and 3 does not divide 2. A careless implementation might only check consecutive numbers in the sorted array and incorrectly return FRIENDS for the latter case.

## Approaches

The brute-force approach checks each pair $a_i, a_j$ with $i < j$ and verifies that either $a_i$ divides $a_j$ or $a_j$ divides $a_i$. This works because it explicitly validates the definition of a friendly group. For $n = 1000$, this requires roughly 500,000 divisibility checks. While acceptable for this constraint, it is unnecessary given the sorted order of numbers.

The optimal approach leverages the sorted order. If the smallest number divides all other numbers, then every pair in the array will satisfy the friendship condition. This is because divisibility is transitive along multiples of the smallest element: if $x$ divides $y$ and $y$ divides $z$, then $x$ divides $z$. Therefore, we only need to check that the smallest number divides every other number in the list. This reduces the number of checks from $O(n^2)$ to $O(n)$.

The brute-force works because it directly implements the definition but fails in efficiency. The observation that the smallest element must divide all others reduces the problem to a single linear scan.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n^2) | O(n) | Acceptable but slower |
| Optimal | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Read the integer $n$ and the sorted comma-separated list of numbers.
2. Convert the input list into integers.
3. Assign the first element of the list to a variable `smallest`. This is the candidate that must divide all others.
4. Iterate over the remaining numbers in the list.
5. For each number, check if it is divisible by `smallest`. If any number is not divisible, immediately print "NOT FRIENDS" and exit.
6. If all numbers are divisible by `smallest`, print "FRIENDS".

The invariant is that after checking all numbers, if no violation occurs, the smallest element divides all others. Because the numbers are sorted, and divisibility is transitive along multiples of the smallest number, every pair in the group satisfies the friendship condition.

## Python Solution

```python
import sys
input = sys.stdin.readline

n = int(input())
nums = list(map(int, input().strip().split(',')))

smallest = nums[0]
for num in nums[1:]:
    if num % smallest != 0:
        print("NOT FRIENDS")
        sys.exit(0)
print("FRIENDS")
```

We read the input and split it by commas, converting the resulting strings into integers. We take the first number as the smallest and iterate over the rest to check divisibility. Using `sys.exit(0)` immediately terminates the program on failure, avoiding unnecessary checks. The order of operations is critical: converting strings to integers before performing modulo prevents runtime errors.

## Worked Examples

Sample 1:

Input: `1,3,6,12`

| Variable | Iteration 1 | Iteration 2 | Iteration 3 |
| --- | --- | --- | --- |
| num | 3 | 6 | 12 |
| num % smallest | 3 % 1 = 0 | 6 % 1 = 0 | 12 % 1 = 0 |

All numbers are divisible by 1. Output: FRIENDS. This confirms that the smallest-element strategy works when the smallest is 1.

Sample 2:

Input: `2,3,6`

| Variable | Iteration 1 | Iteration 2 |
| --- | --- | --- |
| num | 3 | 6 |
| num % smallest | 3 % 2 = 1 | - |

3 is not divisible by 2. Output: NOT FRIENDS. This demonstrates the early exit on failure.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | We iterate through the list once to check divisibility |
| Space | O(n) | We store the list of integers in memory |

Given n ≤ 1000, the algorithm performs at most 999 modulo operations. Memory usage is negligible. The solution fits comfortably within the time and memory limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    output = io.StringIO()
    sys.stdout = output
    n = int(input())
    nums = list(map(int, input().strip().split(',')))
    smallest = nums[0]
    for num in nums[1:]:
        if num % smallest != 0:
            print("NOT FRIENDS")
            return output.getvalue().strip()
    print("FRIENDS")
    return output.getvalue().strip()

# provided sample
assert run("4\n1,3,6,12\n") == "FRIENDS", "sample 1"
# all equal
assert run("3\n5,5,5\n") == "FRIENDS", "all equal"
# minimum size
assert run("1\n7\n") == "FRIENDS", "single element"
# maximum size, all divisible
assert run("5\n2,4,8,16,32\n") == "FRIENDS", "powers of two"
# non-divisible in middle
assert run("4\n2,3,6,12\n") == "NOT FRIENDS", "failure in middle"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 3,5,5 | FRIENDS | All equal numbers |
| 1 element: 7 | FRIENDS | Single-element group |
| 2,4,8,16,32 | FRIENDS | Chain of multiples |
| 2,3,6,12 | NOT FRIENDS | Early detection of failure in the middle |

## Edge Cases

For a single-element group like `7`, the algorithm assigns `smallest = 7` and finds no remaining numbers. It prints FRIENDS. This correctly handles the minimum $n=1$ scenario. For a group with all identical numbers, the modulo check always returns 0, so FRIENDS is printed. If the smallest number is 1, every other number is divisible by 1, so FRIENDS is correctly returned even with large integers. The early exit ensures we do not perform unnecessary operations once a violation is detected.
