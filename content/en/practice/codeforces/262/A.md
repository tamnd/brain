---
title: "CF 262A - Roma and Lucky Numbers"
description: "Roma has a collection of positive integers, and he is fascinated with numbers whose decimal digits consist only of 4 and 7. These are called lucky numbers. The task is to determine, from his collection, how many numbers have at most k lucky digits."
date: "2026-05-29T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "implementation"]
categories: ["algorithms"]
codeforces_contest: 262
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 160 (Div. 2)"
rating: 800
weight: 262
solve_time_s: 186
verified: false
draft: false
---

[CF 262A - Roma and Lucky Numbers](https://codeforces.com/problemset/problem/262/A)

**Rating:** 800  
**Tags:** implementation  
**Solve time:** 3m 6s  
**Verified:** no  

## Solution
## Problem Understanding

Roma has a collection of positive integers, and he is fascinated with numbers whose decimal digits consist only of 4 and 7. These are called lucky numbers. The task is to determine, from his collection, how many numbers have at most _k_ lucky digits. The input gives the size of the collection _n_, the maximum allowed count of lucky digits _k_, and then the _n_ numbers themselves. The output is a single integer: the count of numbers that meet the lucky digit constraint.

The constraints are moderate: both _n_ and _k_ can be at most 100, and each number can be up to 10^9. This means that we can afford to process each number individually and examine every digit without performance concerns. A naive digit-by-digit inspection is feasible because, in the worst case, 100 numbers with up to 10 digits each results in roughly 1,000 operations. Edge cases include numbers with no lucky digits, numbers that consist entirely of lucky digits, or situations where _k_ is larger than the number of digits in the largest number. For example, if _n_ = 3, _k_ = 1 and the numbers are 4, 7, 47, the correct output is 2 because 47 has two lucky digits and exceeds _k_. A careless implementation might miscount digits or forget to compare against _k_, giving the wrong total.

## Approaches

A brute-force approach is straightforward. Iterate through each of Roma’s numbers and for each number, count how many digits are lucky. If the count does not exceed _k_, increment a running total. This works because each number has at most 10 digits and there are at most 100 numbers, yielding roughly 1,000 digit inspections. The algorithm is correct by construction, as we explicitly count lucky digits and compare them to the threshold. Performance is not a concern due to the small input limits.

There is no faster asymptotic solution needed, because the brute-force approach already meets the constraints. The only optimization possible is stylistic: we could convert numbers to strings and use a generator expression to count lucky digits in one line instead of using loops, but the underlying logic does not change. This problem is essentially about careful iteration and counting, not algorithmic complexity.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n * d) where d is number of digits ≤ 10 | O(1) | Accepted |
| Optimal | O(n * d) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the integers _n_ and _k_ from input, and read the list of numbers.
2. Initialize a counter `result` to zero. This will hold the count of numbers satisfying the lucky digit condition.
3. Iterate over each number in the list.
4. For each number, initialize a local counter `lucky_count` to zero.
5. Examine each digit of the current number. If the digit is 4 or 7, increment `lucky_count`.
6. After examining all digits, compare `lucky_count` to _k_. If `lucky_count` ≤ _k_, increment `result`.
7. After all numbers have been processed, output the value of `result`.

Why it works: At each step, we explicitly count lucky digits per number and check if they stay within the allowed threshold. The invariant is that `result` always accurately reflects the count of numbers processed so far that satisfy the condition. Since every digit is examined and the comparison to _k_ is exact, no number can be miscounted.

## Python Solution

```python
import sys
input = sys.stdin.readline

n, k = map(int, input().split())
numbers = list(map(int, input().split()))
result = 0

for num in numbers:
    lucky_count = sum(1 for digit in str(num) if digit == '4' or digit == '7')
    if lucky_count <= k:
        result += 1

print(result)
```

The solution reads input efficiently using `sys.stdin.readline` to handle standard competitive programming input speeds. Each number is converted to a string so we can inspect digits individually. The generator expression `sum(1 for digit in str(num) if digit == '4' or digit == '7')` counts lucky digits cleanly and avoids manual loops. The comparison to `k` ensures only numbers meeting the condition contribute to the final result. Using integers avoids any risk of overflow, and the small size of numbers guarantees no performance bottleneck.

## Worked Examples

**Sample 1:**

Input:

```
3 4
1 2 4
```

| num | digits inspected | lucky_count | lucky_count <= k? | result |
| --- | --- | --- | --- | --- |
| 1 | '1' | 0 | True | 1 |
| 2 | '2' | 0 | True | 2 |
| 4 | '4' | 1 | True | 3 |

All numbers have at most 4 lucky digits, so the final output is 3.

**Sample 2:**

Input:

```
3 2
447 4 77
```

| num | digits inspected | lucky_count | lucky_count <= k? | result |
| --- | --- | --- | --- | --- |
| 447 | '4','4','7' | 3 | False | 0 |
| 4 | '4' | 1 | True | 1 |
| 77 | '7','7' | 2 | True | 2 |

Only 4 and 77 satisfy the condition, yielding an output of 2.

These traces confirm the algorithm correctly counts lucky digits and compares them against the threshold _k_. Edge cases like numbers exactly on the boundary of _k_ are handled correctly.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n * d) ≤ O(1000) | Each of the n numbers is at most 10 digits. |
| Space | O(1) | Only counters and a temporary list of numbers are stored. |

Given the constraints, this runs well within the 1-second limit and uses negligible memory.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    n, k = map(int, input().split())
    numbers = list(map(int, input().split()))
    result = 0
    for num in numbers:
        lucky_count = sum(1 for digit in str(num) if digit == '4' or digit == '7')
        if lucky_count <= k:
            result += 1
    return str(result)

# provided samples
assert run("3 4\n1 2 4\n") == "3", "sample 1"
assert run("3 2\n447 4 77\n") == "2", "sample 2"

# custom cases
assert run("1 0\n4\n") == "0", "single number exceeds k"
assert run("1 1\n4\n") == "1", "single number equals k"
assert run("5 3\n4 7 44 77 447\n") == "4", "mixed small numbers"
assert run("3 10\n4444 7777 4747\n") == "3", "all numbers below high k"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 0\n4 | 0 | single number exceeds k |
| 1 1\n4 | 1 | single number equals k |
| 5 3\n4 7 44 77 447 | 4 | mixed small numbers, some exceed k |
| 3 10\n4444 7777 4747 | 3 | all numbers under high k |

## Edge Cases

For a single number exceeding _k_, such as `n=1, k=0, numbers=[4]`, the algorithm correctly counts 1 lucky digit, compares it to 0, and skips incrementing the result, producing output 0. For maximum size numbers like `n=100, k=100, numbers=[777777777]*100`, each number has 9 digits, all lucky. The sum for each number is 9, which is ≤ 100, so all numbers are counted, giving output 100. The algorithm handles zero, boundary, and maximum input correctly without off-by-one errors.
