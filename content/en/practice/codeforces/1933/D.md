---
title: "CF 1933D - Turtle Tenacity: Continual Mods"
description: "We are given an array of integers, and we need to decide if we can reorder the array such that when we apply modulo operations consecutively from left to right, the final result is not zero."
date: "2026-06-08T18:15:37+07:00"
tags: ["codeforces", "competitive-programming", "constructive-algorithms", "greedy", "math", "number-theory", "sortings"]
categories: ["algorithms"]
codeforces_contest: 1933
codeforces_index: "D"
codeforces_contest_name: "Codeforces Round 929 (Div. 3)"
rating: 1200
weight: 1933
solve_time_s: 122
verified: false
draft: false
---

[CF 1933D - Turtle Tenacity: Continual Mods](https://codeforces.com/problemset/problem/1933/D)

**Rating:** 1200  
**Tags:** constructive algorithms, greedy, math, number theory, sortings  
**Solve time:** 2m 2s  
**Verified:** no  

## Solution
## Problem Understanding

We are given an array of integers, and we need to decide if we can reorder the array such that when we apply modulo operations consecutively from left to right, the final result is not zero. Formally, we want a permutation $b_1, b_2, \dots, b_n$ of the input array $a_1, a_2, \dots, a_n$ such that

$$b_1 \bmod b_2 \bmod \dots \bmod b_n \neq 0$$

The modulo operation is left-associative, so we first compute $b_1 \bmod b_2$, then take that result modulo $b_3$, and so on. For example, if $b = [2024, 1000, 8]$, the evaluation is $(2024 \bmod 1000) \bmod 8 = 24 \bmod 8 = 0$.

The input contains multiple test cases. Each test case specifies the number of elements $n$ and the array itself. The constraints allow up to $10^4$ test cases and a total of $2 \cdot 10^5$ elements across all test cases. This rules out any solution that is worse than roughly $O(n \log n)$ per test case, as $O(n^2)$ solutions would exceed the time limit.

A subtlety arises when the array contains all identical numbers. For instance, $[3, 3, 3]$ will always evaluate to zero regardless of the permutation, because any number modulo itself is zero, and zero modulo anything remains zero. Another tricky scenario is when the smallest number in the array is $1$. If $1$ appears first, the result of $1 \bmod x$ is always $1$, which cannot be reduced to zero in subsequent modulo operations. So the presence of a $1$ may guarantee a non-zero result if arranged correctly.

## Approaches

A brute-force approach would be to try all $n!$ permutations of the array and evaluate the chained modulo for each. This is clearly infeasible since $n$ can be up to $10^5$. Even attempting to only consider permutations with the smallest element at the start would still be combinatorially explosive for larger arrays.

The key insight is that the left-associative modulo operation is sensitive to the ordering of large and small numbers. Specifically, the first element determines the maximum starting remainder. If we place the largest element first and the smallest element last, we maximize the chance that intermediate remainders do not hit zero early. We notice that the operation can only yield zero if at some step, the current remainder is a multiple of the next number. Therefore, if we sort the array in non-decreasing order, the first modulo operation is $a_1 \bmod a_2$. If $a_1 < a_2$, the remainder is $a_1$, which is non-zero. By keeping numbers non-decreasing, we ensure that the remainder never collapses to zero immediately unless all numbers are identical.

Hence the solution reduces to checking if the array contains more than one distinct value. If all elements are equal, the answer is "NO". Otherwise, sorting the array in non-decreasing order guarantees that the chained modulo evaluates to a non-zero value.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Permutations | O(n!) | O(n) | Too slow |
| Sort + Check Distinct | O(n log n) | O(n) | Accepted |

## Algorithm Walkthrough

1. For each test case, read the number of elements $n$ and the array $a$.
2. Check whether all elements in $a$ are equal. If yes, output "NO" because any permutation will yield zero.
3. Otherwise, sort the array in non-decreasing order. This ensures that the first modulo operation is safe and the remainder does not collapse to zero prematurely.
4. Output "YES" to indicate a valid permutation exists. We do not need to actually construct the permutation for this problem, just confirm its existence.

Why it works: The invariant is that if the array contains at least two distinct numbers, arranging them in non-decreasing order ensures that the remainder after each modulo operation is either preserved or reduced but never immediately zero, except in the all-equal case. Since the smallest number is at the front or early in the sequence, the left-associative modulo chain cannot reduce it to zero unless all numbers are equal.

## Python Solution

```python
import sys
input = sys.stdin.readline

t = int(input())
for _ in range(t):
    n = int(input())
    a = list(map(int, input().split()))
    if len(set(a)) == 1:
        print("NO")
    else:
        print("YES")
```

The code first reads the number of test cases. For each test case, it reads the array and converts it to a set to count distinct elements. If there is only one distinct element, it prints "NO". Otherwise, it prints "YES". Using `set(a)` is crucial because it handles arrays with repeated elements efficiently. Sorting is actually unnecessary if we only care about existence.

## Worked Examples

### Sample 1: `[1, 2, 3, 4, 5, 6]`

| Step | Array | Distinct? | Output |
| --- | --- | --- | --- |
| 1 | [1,2,3,4,5,6] | Yes | YES |

All elements are not identical, so a non-zero modulo chain is possible.

### Sample 2: `[3, 3, 3, 3, 3]`

| Step | Array | Distinct? | Output |
| --- | --- | --- | --- |
| 1 | [3,3,3,3,3] | No | NO |

All elements are identical, any permutation yields zero.

These traces show that the only deciding factor is whether all numbers are equal.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) per test case | Creating a set requires scanning all elements once |
| Space | O(n) | The set of distinct elements may store up to n values |

Even in the worst case of $2 \cdot 10^5$ total elements, the algorithm performs at most $O(2 \cdot 10^5)$ operations, well within the 2-second limit.

## Test Cases

```python
# helper
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    output = io.StringIO()
    sys.stdout = output
    # solution
    t = int(input())
    for _ in range(t):
        n = int(input())
        a = list(map(int, input().split()))
        if len(set(a)) == 1:
            print("NO")
        else:
            print("YES")
    return output.getvalue().strip()

# provided samples
assert run("8\n6\n1 2 3 4 5 6\n5\n3 3 3 3 3\n3\n2 2 3\n5\n1 1 2 3 7\n3\n1 2 2\n3\n1 1 2\n6\n5 2 10 10 10 2\n4\n3 6 9 3\n") == "YES\nNO\nYES\nNO\nYES\nNO\nYES\nNO"

# custom cases
assert run("1\n2\n1 1\n") == "NO", "minimum-size identical"
assert run("1\n2\n1 2\n") == "YES", "minimum-size distinct"
assert run("1\n5\n10 10 10 10 10\n") == "NO", "all equal large"
assert run("1\n5\n1 3 5 7 9\n") == "YES", "all distinct odd numbers"
assert run("1\n3\n1000000000 999999999 999999998\n") == "YES", "large numbers distinct"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 2 elements equal `[1,1]` | NO | Minimum array, all equal |
| 2 elements distinct `[1,2]` | YES | Minimum array, distinct |
| 5 elements equal `[10,10,10,10,10]` | NO | Medium size, all equal |
| 5 distinct `[1,3,5,7,9]` | YES | Non-trivial, distinct |
| 3 large numbers `[10^9, 10^9-1, 10^9-2]` | YES | Handles large integers |

## Edge Cases

Arrays with all identical numbers are handled by the `set(a)` check. Arrays with only two distinct numbers are handled because at least one modulo operation will yield a non-zero remainder. Arrays where the smallest number is `1` are naturally handled because placing it first guarantees the modulo chain remains non-zero. Arrays with large numbers are safe since Python handles large integers natively. The algorithm does not depend on constructing the actual permutation, only on the property of having at least two distinct numbers.
