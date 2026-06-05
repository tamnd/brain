---
title: "CF 283A - Cows and Sequence"
description: "We start with a sequence containing a single element, 0, and perform a sequence of n operations. Operations can modify the sequence in three ways: increasing the first a elements by some value x, appending a new number to the end, or removing the last element."
date: "2026-06-05T09:38:42+07:00"
tags: ["codeforces", "competitive-programming", "constructive-algorithms", "data-structures", "implementation"]
categories: ["algorithms"]
codeforces_contest: 283
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 174 (Div. 1)"
rating: 1600
weight: 283
solve_time_s: 106
verified: true
draft: false
---

[CF 283A - Cows and Sequence](https://codeforces.com/problemset/problem/283/A)

**Rating:** 1600  
**Tags:** constructive algorithms, data structures, implementation  
**Solve time:** 1m 46s  
**Verified:** yes  

## Solution
## Problem Understanding

We start with a sequence containing a single element, `0`, and perform a sequence of `n` operations. Operations can modify the sequence in three ways: increasing the first `a` elements by some value `x`, appending a new number to the end, or removing the last element. After each operation, we need the average of all elements in the sequence. The output is a floating-point number with at least six digits of precision.

The key constraints are that `n` can be up to 2·10⁵ and the sequence can grow by appending elements. Any naive approach that explicitly modifies all first `a` elements during an addition operation could take up to O(n²) in total because each type-1 operation could touch O(n) elements. This is far too slow given the 2-second time limit. The integers involved are small (absolute values ≤ 10³), so numerical overflow is not a concern in Python, but we need care when computing floating-point averages.

Edge cases that a naive implementation might mishandle include: performing a type-3 operation (removing the last element) when there are exactly two elements, and performing type-1 additions on elements that were appended dynamically rather than part of the original sequence. For example, if the sequence is `[0, 2]` and we perform `1 2 3` (add 3 to the first 2 elements), the result must be `[3, 5]`. A careless approach that only updates the first element or does not account for appended values would produce a wrong average.

## Approaches

The brute-force approach is simple: maintain the entire sequence as a list. For each type-1 operation, iterate over the first `a` elements and add `x`. For type-2, append `k`. For type-3, remove the last element. After each operation, sum the sequence and divide by its length. This works for small `n`, but for `n ≈ 2·10⁵` with repeated type-1 operations affecting O(n) elements, the operation count becomes O(n²), which is roughly 4·10¹⁰, far exceeding the allowed time.

The key insight is that we do not need to know the exact value of every element individually; we only need the average. Type-1 operations always affect a prefix of the sequence. We can track these updates efficiently using a secondary array that stores incremental increases per prefix length. Let `increment[i]` represent the total additional value applied to the first `i+1` elements. By keeping a running sum of the sequence (`total_sum`), we can update this sum in O(1) for type-1 operations, because adding `x` to the first `a` elements increases the sum by `a * x`. Type-2 and type-3 operations can be handled by storing the last element separately and maintaining the sum accordingly. This reduces the total complexity to O(n), suitable for the input bounds.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n²) | O(n) | Too slow |
| Prefix Increment + Running Sum | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Initialize `seq` as `[0]`, `increments` as `[0]`, and `total_sum` as 0. `increments[i]` will store the extra value applied to `seq[i]` due to type-1 operations.
2. For each operation, read its type `t`.
3. If `t` is 1, read `a` and `x`. Update `increments[a-1]` by adding `x`. Update `total_sum` by adding `a * x`. This captures the effect of adding `x` to the first `a` elements without modifying each element individually.
4. If `t` is 2, read `k`. Append `k` to `seq` and append `0` to `increments`. Update `total_sum` by adding `k`.
5. If `t` is 3, remove the last element `last_val` from `seq`. Retrieve its incremental value from `increments[-1]` and subtract it from the second-to-last element in `increments` so that the prefix sum remains consistent. Update `total_sum` by subtracting `last_val + increments[-1]`. Remove the last element from `increments`.
6. After each operation, compute the average as `total_sum / len(seq)` and print it with 6 decimal digits.

**Why it works**

The `increments` array ensures that each prefix of the sequence accurately tracks accumulated additions from type-1 operations. Type-2 and type-3 operations update the sum explicitly, maintaining a correct running total. The average computed from `total_sum` divided by the length of `seq` always reflects the current sequence, even though the sequence is never fully reconstructed. This preserves correctness in O(1) per operation.

## Python Solution

```python
import sys
input = sys.stdin.readline

n = int(input())
seq = [0]
increments = [0]
total_sum = 0

for _ in range(n):
    op = list(map(int, input().split()))
    t = op[0]
    
    if t == 1:
        a, x = op[1], op[2]
        increments[a-1] += x
        total_sum += a * x
    elif t == 2:
        k = op[1]
        seq.append(k)
        increments.append(0)
        total_sum += k
    else:
        last_val = seq.pop()
        inc = increments.pop()
        total_sum -= last_val + inc
        if increments:
            increments[-1] += inc
    print(total_sum / len(seq))
```

The solution initializes `seq` with 0. The `increments` array mirrors `seq` in length. Type-1 operations update the last affected prefix in `increments` and `total_sum`. Type-2 appends a new value and a corresponding 0 in `increments`. Type-3 pops the last element, adjusts the prefix increment to propagate its value correctly, and updates the sum. Using `total_sum` guarantees that the average is computed in O(1) time.

## Worked Examples

**Sample Input 1**

```
5
2 1
3
2 3
2 1
3
```

| Step | Operation | seq | increments | total_sum | avg |
| --- | --- | --- | --- | --- | --- |
| 0 | init | [0] | [0] | 0 | 0 |
| 1 | 2 1 | [0,1] | [0,0] | 1 | 0.5 |
| 2 | 3 | [0] | [0] | 0 | 0.0 |
| 3 | 2 3 | [0,3] | [0,0] | 3 | 1.5 |
| 4 | 2 1 | [0,3,1] | [0,0,0] | 4 | 1.333333 |
| 5 | 3 | [0,3] | [0,0] | 3 | 1.5 |

This trace confirms that prefix increments propagate correctly when elements are removed.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Each operation is handled in O(1) using prefix increments and running sum |
| Space | O(n) | `seq` and `increments` arrays each store at most n elements |

Given `n ≤ 2·10⁵`, the O(n) solution completes comfortably under 2 seconds.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    output = io.StringIO()
    sys.stdout = output
    # paste the solution here
    n = int(input())
    seq = [0]
    increments = [0]
    total_sum = 0
    for _ in range(n):
        op = list(map(int, input().split()))
        t = op[0]
        if t == 1:
            a, x = op[1], op[2]
            increments[a-1] += x
            total_sum += a * x
        elif t == 2:
            k = op[1]
            seq.append(k)
            increments.append(0)
            total_sum += k
        else:
            last_val = seq.pop()
            inc = increments.pop()
            total_sum -= last_val + inc
            if increments:
                increments[-1] += inc
        print(total_sum / len(seq))
    return output.getvalue().strip()

# Provided samples
assert run("5\n2 1\n3\n2 3\n2 1\n3\n") == "0.5\n0.0\n1.5\n1.3333333333333333\n1.5", "sample 1"

# Custom cases
assert run("1\n2 1000\n") == "500.0", "single append"
assert run("3\n2 1\n1 2 5\n3\n") == "0.5\n5.5\n5.0", "type-1 then remove"
assert run("2\n1 1 10\n3\n") == "10.0\n0.0", "
```
