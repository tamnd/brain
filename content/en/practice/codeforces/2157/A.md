---
title: "CF 2157A - Dungeon Equilibrium"
description: "We are given an array of integers, and the goal is to make it \"balanced.\" An array is balanced if each number x that appears in it does so exactly x times. So if a number appears too few or too many times, we need to remove some elements to fix it."
date: "2026-06-08T00:18:15+07:00"
tags: ["codeforces", "competitive-programming", "greedy", "implementation", "sortings"]
categories: ["algorithms"]
codeforces_contest: 2157
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 1066 (Div. 1 + Div. 2)"
rating: 800
weight: 2157
solve_time_s: 188
verified: true
draft: false
---

[CF 2157A - Dungeon Equilibrium](https://codeforces.com/problemset/problem/2157/A)

**Rating:** 800  
**Tags:** greedy, implementation, sortings  
**Solve time:** 3m 8s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given an array of integers, and the goal is to make it "balanced." An array is balanced if each number `x` that appears in it does so exactly `x` times. So if a number appears too few or too many times, we need to remove some elements to fix it. For instance, `[1, 4, 2, 4, 4, 4, 2]` is balanced because `1` appears once, `2` appears twice, and `4` appears four times. In contrast, `[2, 2, 2]` is not balanced because `2` appears three times but should appear exactly twice.

The input contains multiple test cases, each with an array of size `n` and values between `0` and `n`. Our task is to find the minimum number of deletions needed to reach a balanced array.

The constraints are fairly small: `n` is at most 100 and there are up to 500 test cases. That means even a quadratic approach in `n` per test case is acceptable, because `100^2 * 500 = 5*10^6` operations, which fits comfortably within one second.

Some non-obvious edge cases arise when numbers appear more than once but cannot reach their "balanced count," or when `0` occurs. For example, an array `[0, 0, 0]` should be reduced to remove all zeros since `0` can appear zero times, giving a minimum deletion of 3. Similarly, a number appearing more times than its value, like `[3, 3, 3, 3]`, requires deletions to reduce its count to exactly 3.

## Approaches

A brute-force approach would enumerate all possible subsets of the array and check whether they are balanced. This works in theory because we can remove elements freely, but the number of subsets is exponential, making it infeasible even for `n=20`.

The key insight for a faster solution is that the array only has `n` distinct values at most, and we can focus on the frequency of each number. For each number `x`, if it appears `f` times, there are only two sensible options: remove all occurrences of `x` or leave exactly `x` of them. Choosing the better of these two minimizes deletions locally. Since the choices for each distinct number are independent, we can calculate the minimum deletions by summing the optimal deletions for each distinct number.

We can implement this efficiently by counting frequencies with a dictionary or a `Counter` and iterating over all unique values in the array. If the value is zero, we always delete all zeros because a balanced array cannot include zero. If the frequency exceeds the value, we delete the excess; if the frequency is smaller than the value, we delete all occurrences because we cannot "create" more of that number.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(2^n * n) | O(n) | Too slow |
| Optimal | O(n) per test case | O(n) | Accepted |

## Algorithm Walkthrough

1. Read the number of test cases. For each test case, read the array size `n` and the array itself.
2. Count the occurrences of each number using a dictionary or `Counter`. This gives us the frequency `f` for each unique number `x`.
3. Initialize a counter for deletions. Iterate through each unique number:

- If `x` is zero, add its full frequency to deletions, because zeros cannot appear in a balanced array.
- If `f < x`, add `f` to deletions, because we cannot increase occurrences; the only option is to remove them all.
- If `f >= x`, add `f - x` to deletions, removing the excess occurrences to match the desired count exactly.
4. After processing all unique numbers, output the total deletions for this test case.

Why it works: For each number, either we match its value exactly or remove all instances. This local optimal choice guarantees a globally minimal deletion count because the numbers' occurrences are independent and cannot affect one another’s validity.

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
    deletions = 0
    for x, f in freq.items():
        if x == 0:
            deletions += f
        elif f < x:
            deletions += f
        else:
            deletions += f - x
    print(deletions)
```

This solution first counts the occurrences of each number with `Counter`. Then it iterates through the unique numbers and applies the deletion logic described in the algorithm walkthrough. Using `Counter` guarantees O(n) counting, and iterating over at most `n` keys is efficient.

## Worked Examples

### Example 1

Input: `[1, 2, 2]`

| x | f | Action | Deletions so far |
| --- | --- | --- | --- |
| 1 | 1 | f >= x → remove f-x = 0 | 0 |
| 2 | 2 | f >= x → remove f-x = 0 | 0 |

Output: 0. The array is already balanced.

### Example 2

Input: `[1, 1, 2, 2, 3]`

| x | f | Action | Deletions so far |
| --- | --- | --- | --- |
| 1 | 2 | f >= x → remove f-x = 1 | 1 |
| 2 | 2 | f >= x → remove f-x = 0 | 1 |
| 3 | 1 | f < x → remove all f = 1 | 2 |

Output: 2. Remove one `1` and the single `3` to balance.

These traces confirm that the deletion count is computed independently per number and matches the intended balance.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) per test case | Counting with `Counter` and iterating over keys is linear in the array size. |
| Space | O(n) | The `Counter` stores frequency for each unique element, at most `n`. |

With n ≤ 100 and t ≤ 500, the total operations are ≤ 50,000, which fits easily under the time limit.

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
        deletions = 0
        for x, f in freq.items():
            if x == 0:
                deletions += f
            elif f < x:
                deletions += f
            else:
                deletions += f - x
        output.append(str(deletions))
    return "\n".join(output)

# provided samples
assert run("4\n3\n1 2 2\n5\n1 1 2 2 3\n10\n1 2 3 2 4 4 4 4 5 2\n1\n0\n") == "0\n2\n3\n1", "sample 1"

# custom cases
assert run("2\n3\n0 0 0\n4\n3 3 3 3\n") == "3\n1", "zeros and overcount"
assert run("1\n5\n5 5 5 5 5\n") == "0", "perfect balance"
assert run("1\n6\n1 1 1 2 2 3\n") == "3", "mixed under and over counts"
assert run("1\n1\n0\n") == "1", "single zero"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `0 0 0` | 3 | Correct handling of zeros |
| `3 3 3 3` | 1 | Reduces to exactly 3 occurrences |
| `5 5 5 5 5` | 0 | Already balanced, no deletions |
| `1 1 1 2 2 3` | 3 | Mixed under-counts and over-counts |
| `0` | 1 | Single zero handled correctly |

## Edge Cases

For the array `[0, 0, 0]`, `Counter` gives `{0: 3}`. The algorithm adds all three to deletions because zeros cannot remain, yielding 3. For `[3, 3, 3, 3]`, `Counter` gives `{3: 4}`. The algorithm removes one to reduce count to 3, which is correct. For a perfectly balanced array like `[5, 5, 5, 5, 5]`, no deletions are needed. The solution consistently handles zeros, over-counts, and under-counts.
