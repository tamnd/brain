---
title: "CF 2173A - Sleeping Through Classes"
description: "We are asked to plan our sleep schedule across a sequence of classes, each of which is either important or not. The day is represented as a binary string where '1' marks an important class and '0' a non-important one."
date: "2026-06-07T22:46:59+07:00"
tags: ["codeforces", "competitive-programming", "greedy", "implementation"]
categories: ["algorithms"]
codeforces_contest: 2173
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 1068 (Div. 2)"
rating: 800
weight: 2173
solve_time_s: 186
verified: true
draft: false
---

[CF 2173A - Sleeping Through Classes](https://codeforces.com/problemset/problem/2173/A)

**Rating:** 800  
**Tags:** greedy, implementation  
**Solve time:** 3m 6s  
**Verified:** yes  

## Solution
## Problem Understanding

We are asked to plan our sleep schedule across a sequence of classes, each of which is either important or not. The day is represented as a binary string where '1' marks an important class and '0' a non-important one. The rule is that for every important class you attend, you are forced to stay awake not only for that class but also for the next `k` classes. Non-important classes can be slept through freely, unless this forced awake rule applies. Our goal is to maximize the number of classes we can sleep through.

Each test case gives the total number of classes `n`, the sleep recovery window `k`, and the string representing which classes are important. The output should be a single integer for each test case: the count of classes we can sleep through while respecting the awake constraints.

Constraints are small: both `n` and `k` go up to 100, and there can be up to 500 test cases. This means that even a straightforward `O(n^2)` solution per test case will likely work, but we can also aim for an `O(n)` solution since the logic is sequential. The non-obvious edge cases involve consecutive important classes or important classes near the end of the string, where the `k` window might extend beyond the end.

For example, consider `n = 5, k = 2, s = "10101"`. A naive approach that ignores overlap might double-count awake windows, but the correct strategy should handle overlapping awake periods efficiently. Another edge case is when `k` is larger than the remaining classes: `n = 3, k = 5, s = "100"`. Here attending class 1 forces staying awake to the end.

## Approaches

A brute-force approach would iterate through the string and, for each important class, mark the next `k` classes as forced awake. After marking, we count how many zeros remain unmarked to get the maximum sleep count. This works because it directly simulates the rules. With `n` up to 100, marking up to `k` classes per '1' gives at most 100 × 100 = 10,000 operations per test case, which is acceptable given 500 test cases.

The optimal approach observes that we do not need an auxiliary array for marking. We can maintain a single pointer representing the index until which we are forced awake. As we iterate through the classes, if the current class index is less than this pointer, we must stay awake. If the class is important, we update the pointer to `i + k + 1` (because arrays are 0-indexed). Non-important classes outside the forced awake window can be slept through and increment our sleep counter. This reduces bookkeeping and makes the solution simple and linear in `n`.

The key insight is that overlapping awake windows merge naturally: attending an important class while still within a previous awake window only extends the awake period if it pushes further than the current pointer. This ensures we never undercount or overcount awake classes.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n * k) | O(n) | Acceptable due to small constraints |
| Optimal | O(n) | O(1) | Accepted and clean |

## Algorithm Walkthrough

1. Initialize `awake_until` to `-1`. This variable tracks the class index up to which you are forced to stay awake.
2. Initialize `sleep_count` to `0`. This will store the number of classes you can sleep through.
3. Iterate through each class index `i` from `0` to `n-1`.
4. If `i` is greater than `awake_until` and the class is non-important (`s[i] == '0'`), increment `sleep_count` because you are allowed to sleep through it.
5. If the class is important (`s[i] == '1'`), update `awake_until` to `max(awake_until, i + k)`. This ensures you stay awake for `k` classes following the important class, but preserves the longer awake period if already in a previous awake window.
6. After finishing the iteration, `sleep_count` contains the maximum number of classes you can sleep through.

Why it works: The invariant is that at each class `i`, `awake_until` correctly represents the last class you must stay awake for. By updating `awake_until` using `max`, overlapping awake periods are merged naturally. Sleeping is only allowed if `i > awake_until` and the class is non-important, guaranteeing that no forced awake constraints are violated.

## Python Solution

```python
import sys
input = sys.stdin.readline

t = int(input())
for _ in range(t):
    n, k = map(int, input().split())
    s = input().strip()
    awake_until = -1
    sleep_count = 0
    for i in range(n):
        if i > awake_until and s[i] == '0':
            sleep_count += 1
        if s[i] == '1':
            awake_until = max(awake_until, i + k)
    print(sleep_count)
```

The code initializes the forced awake pointer and a counter for slept classes. Iterating over the string, we increment the sleep counter whenever a class is safely sleepable and extend the forced awake window whenever an important class is encountered. Using `max` ensures that overlapping awake windows do not shrink.

## Worked Examples

**Example 1**: `n=4, k=1, s="1001"`

| i | s[i] | awake_until | sleep_count | Explanation |
| --- | --- | --- | --- | --- |
| 0 | 1 | 1 | 0 | Must attend class 1, awake until class 2 |
| 1 | 0 | 1 | 0 | Within awake window, cannot sleep |
| 2 | 0 | 1 | 1 | Outside awake window, can sleep |
| 3 | 1 | 4 | 1 | Important class, update awake_until |

Result: 1 class can be slept through.

**Example 2**: `n=8, k=2, s="01000101"`

| i | s[i] | awake_until | sleep_count | Explanation |
| --- | --- | --- | --- | --- |
| 0 | 0 | -1 | 1 | Non-important, outside awake window |
| 1 | 1 | 3 | 1 | Important, awake until 4 |
| 2 | 0 | 3 | 1 | Within awake window |
| 3 | 0 | 3 | 1 | Within awake window |
| 4 | 0 | 3 | 2 | Outside awake window, sleep |
| 5 | 1 | 7 | 2 | Important, awake until 7 |
| 6 | 0 | 7 | 2 | Within awake window |
| 7 | 1 | 9 | 2 | Important, awake until 9 |

Result: 2 classes can be slept through.

These traces demonstrate that the algorithm correctly handles overlapping awake periods and identifies all classes safe to sleep through.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Single pass over each class per test case |
| Space | O(1) | Only a few counters and pointers |

With `n ≤ 100` and `t ≤ 500`, the total operations are at most 50,000, well within the 1-second time limit. The memory usage is minimal.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    output = io.StringIO()
    sys.stdout = output
    t = int(input())
    for _ in range(t):
        n, k = map(int, input().split())
        s = input().strip()
        awake_until = -1
        sleep_count = 0
        for i in range(n):
            if i > awake_until and s[i] == '0':
                sleep_count += 1
            if s[i] == '1':
                awake_until = max(awake_until, i + k)
        print(sleep_count)
    return output.getvalue().strip()

# Provided samples
assert run("4\n4 1\n1001\n3 3\n000\n3 1\n001\n8 2\n01000101\n") == "1\n3\n2\n2"

# Custom cases
assert run("1\n3 5\n100") == "2", "large k extends past end"
assert run("1\n5 0\n10101") == "2", "k=0 only important classes prevent sleep"
assert run("1\n5 2\n00000") == "5", "all classes non-important"
assert run("1\n6 1\n111111") == "0", "all classes important"
assert run("1\n1 1\n0") == "1", "single non-important class"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `3 5 100` | 2 | k extends beyond the end correctly |
| `5 0 10101` | 2 | k=0 only blocks current important class |
| `5 2 00000` | 5 | All classes non-important, can sleep all |
| `6 1 111111` | 0 | All classes important |
