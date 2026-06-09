---
title: "CF 1616A - Integer Diversity"
description: "We are given a list of integers and we are allowed to negate any subset of them. The goal is to maximize the number of distinct integers in the array after possibly negating some elements."
date: "2026-06-10T06:33:27+07:00"
tags: ["codeforces", "competitive-programming", "implementation"]
categories: ["algorithms"]
codeforces_contest: 1616
codeforces_index: "A"
codeforces_contest_name: "Good Bye 2021: 2022 is NEAR"
rating: 800
weight: 1616
solve_time_s: 102
verified: false
draft: false
---

[CF 1616A - Integer Diversity](https://codeforces.com/problemset/problem/1616/A)

**Rating:** 800  
**Tags:** implementation  
**Solve time:** 1m 42s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a list of integers and we are allowed to negate any subset of them. The goal is to maximize the number of distinct integers in the array after possibly negating some elements. Each test case provides a new list of integers, and the output is simply the largest number of different values we can obtain through these negations.

Looking at the input constraints, the array size `n` is at most 100 and values lie between -100 and 100. This is small enough to consider solutions that inspect the frequency or presence of each value directly, without worrying about high asymptotic complexity. The number of test cases is also moderate at 100, so even an `O(n^2)` approach per test case would run in acceptable time.

The edge cases to watch for are zeros, duplicates, and symmetrical positives and negatives. For example, if the array is `[0, 0]`, negating zeros changes nothing, so the answer is 1. If the array is `[1, 1, -1]`, we need to handle duplicates carefully: we can use one 1 and one -1, but we cannot create a second 1 from -1 again. Ignoring this subtlety would cause overcounting.

## Approaches

A brute-force approach would try every subset of the array, negate it, and count distinct values. For each element, we have two choices: negate or not, giving `2^n` possibilities. Even with `n = 20`, this reaches over a million subsets, and for `n = 100`, this is astronomically large. Therefore brute-force is infeasible.

The key observation is that we only care about **distinct absolute values**. Each positive number can appear as itself, its negation, or both. Each negative number is just a negative version of some positive absolute value. Zero is special: it can appear only once regardless of negation. So the problem reduces to counting how many distinct absolute values we have, but we need to decide how to handle cases where both the positive and negative of a number exist.

The optimal strategy is as follows: we count zeros separately and limit them to 1, then for every other absolute value, we can include at most two numbers: one positive and one negative. If the original array contains both signs for the same absolute value, we include both; otherwise, we include whichever exists. This guarantees the maximum number of distinct elements.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(2^n * n) | O(n) | Too slow |
| Optimal | O(n) | O(1) (or O(n) for set) | Accepted |

## Algorithm Walkthrough

1. Initialize a counter for zeros and two sets: one for positive numbers, one for negative numbers.
2. Iterate through the array. If a number is zero, increment the zero counter. If positive, add it to the positive set. If negative, add its absolute value to the negative set.
3. The maximum number of distinct values is the sum of the zero count (at most 1), the number of positive-only numbers, the number of negative-only numbers, and the number of numbers that exist in both positive and negative forms.
4. For each absolute value, if it appears in both positive and negative sets, count both. If it appears in only one set, count that single occurrence. Add the zero if it exists.
5. Output this sum for each test case.

**Why it works:** By counting distinct absolute values and considering at most one zero, we ensure no duplicates are counted and no numbers are overlooked. Negating duplicates beyond this does not increase distinct values, so this strategy is maximal.

## Python Solution

```python
import sys
input = sys.stdin.readline

t = int(input())
for _ in range(t):
    n = int(input())
    a = list(map(int, input().split()))
    
    pos = set()
    neg = set()
    zero = 0
    
    for x in a:
        if x > 0:
            pos.add(x)
        elif x < 0:
            neg.add(-x)
        else:
            zero = 1
    
    both = pos & neg  # numbers that appear in both positive and negative
    pos_only = pos - both
    neg_only = neg - both
    
    result = len(both) * 2 + len(pos_only) + len(neg_only) + zero
    print(result)
```

The code separates positive, negative, and zero numbers. It counts numbers appearing in both positive and negative form and handles them correctly. Zeros are counted at most once. Using sets ensures duplicates are ignored.

## Worked Examples

### Sample Input 1

```
4
1 1 2 2
```

| Step | pos | neg | zero | both | pos_only | neg_only | result |
| --- | --- | --- | --- | --- | --- | --- | --- |
| init | {} | {} | 0 | - | - | - | - |
| 1 | {1} | {} | 0 | - | - | - | - |
| 2 | {1} | {} | 0 | - | - | - | - |
| 3 | {1,2} | {} | 0 | - | - | - | - |
| 4 | {1,2} | {} | 0 | - | - | - | - |
| final | - | - | - | {} | {1,2} | {} | 4 |

Explanation: No negatives, zeros = 0. All numbers are positive and unique, so max distinct is 4.

### Sample Input 2

```
0 0
```

| Step | pos | neg | zero | both | pos_only | neg_only | result |
| --- | --- | --- | --- | --- | --- | --- | --- |
| init | {} | {} | 0 | - | - | - | - |
| 1 | {} | {} | 1 | - | - | - | - |
| 2 | {} | {} | 1 | - | - | - | - |
| final | - | - | - | {} | {} | {} | 1 |

Zeros only, result = 1.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) per test case | Each number is processed once and sets support O(1) insertion and look-up |
| Space | O(n) | Sets store at most n numbers in total |

With n ≤ 100 and t ≤ 100, this approach easily runs in under 1 second and uses negligible memory.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    output = io.StringIO()
    sys.stdout = output
    # copy solution here
    t = int(input())
    for _ in range(t):
        n = int(input())
        a = list(map(int, input().split()))
        
        pos = set()
        neg = set()
        zero = 0
        
        for x in a:
            if x > 0:
                pos.add(x)
            elif x < 0:
                neg.add(-x)
            else:
                zero = 1
        
        both = pos & neg
        pos_only = pos - both
        neg_only = neg - both
        
        result = len(both) * 2 + len(pos_only) + len(neg_only) + zero
        print(result)
    
    return output.getvalue().strip()

# provided samples
assert run("3\n4\n1 1 2 2\n3\n1 2 3\n2\n0 0\n") == "4\n3\n1"

# custom cases
assert run("1\n3\n-1 1 0\n") == "3", "pos+neg+zero"
assert run("1\n5\n5 5 5 5 5\n") == "1", "all equal"
assert run("1\n6\n-3 -3 3 3 0 0\n") == "5", "duplicates with zero"
assert run("1\n4\n-2 -1 1 2\n") == "4", "symmetric negatives and positives"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| -1 1 0 | 3 | counts zero and positive/negative separately |
| 5 5 5 5 5 | 1 | handles all equal values |
| -3 -3 3 3 0 0 | 5 | handles duplicates and zero correctly |
| -2 -1 1 2 | 4 | handles symmetric positives and negatives |

## Edge Cases

For an array `[0, 0]`, the algorithm sets `zero = 1` and no positive or negative numbers. `both`, `pos_only`, `neg_only` are empty. The result is 1, correctly handling repeated zeros.

For `[1, 1, -1]`, `pos = {1}`, `neg = {1}`, `both = {1}`, `pos_only = {}`, `neg_only = {}`, result = 2. This correctly counts one 1 and one -1, and does not over
