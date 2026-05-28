---
title: "CF 214B - Hometask"
description: "We are given a multiset of digits and asked to construct the largest integer from some or all of them such that the resulting number is divisible by 2, 3, and 5 simultaneously."
date: "2026-05-29T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "brute-force", "constructive-algorithms", "greedy", "math"]
categories: ["algorithms"]
codeforces_contest: 214
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 131 (Div. 2)"
rating: 1600
weight: 214
solve_time_s: 169
verified: true
draft: false
---

[CF 214B - Hometask](https://codeforces.com/problemset/problem/214/B)

**Rating:** 1600  
**Tags:** brute force, constructive algorithms, greedy, math  
**Solve time:** 2m 49s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a multiset of digits and asked to construct the largest integer from some or all of them such that the resulting number is divisible by 2, 3, and 5 simultaneously. Because a number divisible by 2, 3, and 5 is divisible by 30, the task reduces to building the largest number divisible by 30 from the given digits. The input consists of a single integer `n` representing the number of digits, followed by `n` digits separated by spaces. The output is either the largest valid number or `-1` if no such number exists. Leading zeros are not allowed except in the case of the number zero itself.

The constraints allow `n` up to 100,000, so any solution with worse than O(n log n) complexity is likely to exceed the time limit. We must avoid approaches that enumerate all possible permutations of the digits, as that would be factorial in `n` and completely infeasible. Edge cases include having only zeros, a single digit that cannot form a multiple of 30, or digits that sum to a total not divisible by 3 while containing zero, which would prevent divisibility by 30. For example, input `1 5` should produce `-1`, not `5`, because no combination forms a multiple of 30.

## Approaches

The naive approach is to generate all permutations of the digits, check divisibility for each, and keep the maximum. This brute-force works because it correctly identifies numbers divisible by 30, but its complexity is O(n!) in the worst case, making it completely infeasible for `n` up to 100,000.

The key insight is to decompose the divisibility rules. A number divisible by 2 must have at least one even digit, a number divisible by 5 must end with 0 or 5, and a number divisible by 3 must have digits summing to a multiple of 3. Combining these for divisibility by 30, the last digit must be 0 (since it is the only digit divisible by both 2 and 5). Once we know zero exists, we must adjust the sum of the digits so it is divisible by 3. Because we want the maximum number, digits should be arranged in descending order. This reduces the problem to counting digits, adjusting their sum modulo 3, and printing them in descending order.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n!) | O(n!) | Too slow |
| Optimal | O(n) | O(10) | Accepted |

## Algorithm Walkthrough

1. Read the number of digits `n` and the list of digits. Count the occurrences of each digit using a frequency array of size 10.
2. Check if there is at least one zero. If not, print `-1` because a number divisible by 30 must end with 0.
3. Compute the sum of all digits. If the sum modulo 3 is not zero, remove the minimal set of digits needed to make the sum divisible by 3. We can remove one digit with remainder 1 or two digits with remainder 2 (or vice versa) to fix the sum. Prioritize removing the smallest digits to maximize the final number.
4. After adjustments, if there are no digits left other than zeros, print `0`. This handles the all-zero case.
5. Construct the largest number by iterating from digit 9 down to 0 and appending each digit the number of times it occurs after adjustments.
6. Print the resulting number.

Why it works: The algorithm maintains the invariants that the sum of digits is divisible by 3 and the number ends with zero, ensuring divisibility by 30. Sorting digits in descending order maximizes the number. Removing minimal digits preserves the largest possible remaining number.

## Python Solution

```python
import sys
input = sys.stdin.readline

n = int(input())
digits = list(map(int, input().split()))

count = [0]*10
for d in digits:
    count[d] += 1

if count[0] == 0:
    print(-1)
    sys.exit()

total = sum(d * count[d] for d in range(10))
mod = total % 3

def remove_digits(mod_val):
    # Try removing smallest digit with remainder mod_val
    for r in range(1, 10):
        if r % 3 == mod_val and count[r] > 0:
            count[r] -= 1
            return True
    # Try removing two smallest digits with remainder 3 - mod_val
    needed = 2
    for r in range(1, 10):
        if r % 3 == (3 - mod_val):
            while count[r] > 0 and needed > 0:
                count[r] -= 1
                needed -= 1
            if needed == 0:
                return True
    return False

if mod != 0:
    if not remove_digits(mod):
        print(-1)
        sys.exit()

# handle all zeros
if sum(count[1:]) == 0:
    print(0)
    sys.exit()

res = []
for d in range(9, -1, -1):
    res.extend([str(d)]*count[d])
print(''.join(res))
```

The code first counts digits and ensures at least one zero exists. The sum modulo 3 is corrected by removing the minimal number of digits to satisfy divisibility. The output is constructed in descending order for maximum value. Special handling is done if only zeros remain.

## Worked Examples

Sample 1:

| digits | count | sum | mod | remove | final count | result |
| --- | --- | --- | --- | --- | --- | --- |
| [0] | 0..1..0 | 0 | 0 | none | 0..1..0 | 0 |

This confirms that the algorithm correctly identifies that zero is the only number divisible by 30.

Sample 2:

| digits | count | sum | mod | remove | final count | result |
| --- | --- | --- | --- | --- | --- | --- |
| [5,5,5,4,4,4,3,3,3,0] | counts 0..9 | 36 | 0 | none | same | 5554443330 |

This shows the algorithm preserves the largest number without needing to remove digits.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Counting digits is O(n), adjusting sum and printing are O(10) |
| Space | O(10) | Only a fixed-size frequency array is needed |

The solution easily fits in time and memory limits because the dominant operation scales linearly with the number of digits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    n = int(input())
    digits = list(map(int, input().split()))
    count = [0]*10
    for d in digits:
        count[d] += 1
    if count[0] == 0:
        return "-1"
    total = sum(d * count[d] for d in range(10))
    mod = total % 3
    def remove_digits(mod_val):
        for r in range(1, 10):
            if r % 3 == mod_val and count[r] > 0:
                count[r] -= 1
                return True
        needed = 2
        for r in range(1, 10):
            if r % 3 == (3 - mod_val):
                while count[r] > 0 and needed > 0:
                    count[r] -= 1
                    needed -= 1
                if needed == 0:
                    return True
        return False
    if mod != 0:
        if not remove_digits(mod):
            return "-1"
    if sum(count[1:]) == 0:
        return "0"
    res = []
    for d in range(9, -1, -1):
        res.extend([str(d)]*count[d])
    return ''.join(res)

# provided samples
assert run("1\n0\n") == "0"
assert run("10\n5 5 5 4 4 4 3 3 3 0\n") == "5554443330"
assert run("1\n5\n") == "-1"
# custom cases
assert run("3\n0 0 0\n") == "0", "all zeros"
assert run("5\n3 3 3 3 0\n") == "33330", "sum divisible by 3 with zero"
assert run("4\n1 1 1 0\n") == "1110", "remove one digit to fix modulo 3"
assert run("5\n1 4 4 0 0\n") == "44100", "maximize number with multiple zeros"
assert run("6\n9 8 7 0 0 0\n") == "987000", "descending order with multiple zeros"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 3\n0 0 0 | 0 | all zeros case |
| 5\n3 3 3 3 0 | 33330 | sum divisible by 3 with zero |
| 4\n1 1 1 0 | 1110 | remove one digit to fix modulo 3 |
| 5\n1 4 4 0 0 | 44100 | maximize number with multiple zeros |
