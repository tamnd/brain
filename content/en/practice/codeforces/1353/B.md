---
title: "CF 1353B - Two Arrays And Swaps"
description: "The problem gives two arrays of equal length, which we can think of as two sets of numbers on separate shelves. We are allowed to swap numbers between the shelves, but only up to a maximum of k swaps."
date: "2026-06-11T14:08:31+07:00"
tags: ["codeforces", "competitive-programming", "greedy", "sortings"]
categories: ["algorithms"]
codeforces_contest: 1353
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 642 (Div. 3)"
rating: 800
weight: 1353
solve_time_s: 554
verified: true
draft: false
---

[CF 1353B - Two Arrays And Swaps](https://codeforces.com/problemset/problem/1353/B)

**Rating:** 800  
**Tags:** greedy, sortings  
**Solve time:** 9m 14s  
**Verified:** yes  

## Solution
## Problem Understanding

The problem gives two arrays of equal length, which we can think of as two sets of numbers on separate shelves. We are allowed to swap numbers between the shelves, but only up to a maximum of `k` swaps. Our goal is to make the sum of the first shelf as large as possible after performing these swaps. Each test case provides the lengths of the arrays, the maximum allowed swaps, and the arrays themselves. The output is simply the largest sum of the first array achievable under the swap constraint.

The constraints are small: `n` can be at most 30 and `k` at most `n`, while the number of test cases `t` is up to 200. This means we do not need to worry about scaling to millions of operations, so any solution that is quadratic or sorts the arrays will be efficient enough. Each number is small as well, up to 30, so integer overflow is not a concern. Non-obvious edge cases include situations where the optimal number of swaps is zero, for instance when all elements of the first array are already larger than all elements of the second. Another tricky case is when `k` exceeds the number of advantageous swaps; performing unnecessary swaps could reduce the sum if done carelessly.

## Approaches

The naive approach is to try all possible sequences of swaps. For each move, we would pick a pair `(i, j)` and swap, recursively exploring the next move until we either reach `k` swaps or exhaust possibilities. This is correct because it enumerates all possible outcomes, but the number of sequences grows extremely fast - up to `(n^2)^k` - which is far too slow even for `n = 30` and `k = 30`.

The key insight is to notice that we want to increase the sum of the first array. To do this optimally, we should swap its smallest elements with the largest elements of the second array, but only if the element from the second array is larger. Swapping anything else would not help. Sorting the first array in ascending order and the second in descending order allows us to pair the best candidates for swapping. Then we iterate over the first `k` elements, performing a swap only if the element from the second array is strictly greater than the element from the first. This greedy approach guarantees that every swap we perform contributes positively to the sum of the first array.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O((n^2)^k) | O(n) | Too slow |
| Optimal (Greedy with Sorting) | O(n log n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Read the number of test cases `t`.
2. For each test case, read `n` and `k`, and then read arrays `a` and `b`.
3. Sort `a` in ascending order to identify the smallest elements.
4. Sort `b` in descending order to identify the largest elements.
5. Iterate over the first `k` elements, considering `a[i]` and `b[i]`. If `b[i]` is larger than `a[i]`, swap them. Otherwise, break the loop because no further swaps can improve the sum.
6. Compute the sum of the modified array `a`.
7. Output this sum for each test case.

Why it works: Sorting guarantees that we always compare the smallest available element in `a` with the largest available element in `b`, which is exactly the swap that maximizes the immediate increase in `a`'s sum. The greedy decision to stop swapping when `b[i] <= a[i]` is valid because no later elements of `b` will be larger than earlier elements due to the descending order, and no later elements of `a` will be smaller than earlier elements due to ascending order. This preserves optimality.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        n, k = map(int, input().split())
        a = list(map(int, input().split()))
        b = list(map(int, input().split()))
        
        a.sort()
        b.sort(reverse=True)
        
        for i in range(min(k, n)):
            if b[i] > a[i]:
                a[i], b[i] = b[i], a[i]
            else:
                break
        
        print(sum(a))

solve()
```

The code first sorts the two arrays to make the greedy swaps straightforward. The loop runs for at most `k` iterations and only performs a swap if it strictly improves the sum of `a`. The use of `min(k, n)` ensures we do not access indices out of range, which is a subtle point that can be overlooked. Calculating `sum(a)` after the swaps gives the final answer.

## Worked Examples

Consider the first sample input:

```
2 1
1 2
3 4
```

| i | a (sorted) | b (sorted desc) | swap? | a after swap |
| --- | --- | --- | --- | --- |
| 0 | 1 | 4 | yes | 4,2 |

We swap 1 with 4. Sum of `a` is 6.

Another example:

```
5 3
1 2 3 4 5
10 9 10 10 9
```

Sorting gives `a = [1,2,3,4,5]` and `b = [10,10,10,9,9]`.

| i | a[i] | b[i] | swap? | a after swap |
| --- | --- | --- | --- | --- |
| 0 | 1 | 10 | yes | 10,2,3,4,5 |
| 1 | 2 | 10 | yes | 10,10,3,4,5 |
| 2 | 3 | 10 | yes | 10,10,10,4,5 |

After 3 swaps, sum of `a` is 10+10+10+4+5 = 39.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(t * n log n) | Sorting both arrays dominates the computation; loop of k is O(n) and negligible. |
| Space | O(n) | Arrays `a` and `b` are stored per test case. |

The solution fits comfortably within the constraints, as `n` is at most 30 and `t` at most 200, so sorting per test case is trivial in terms of runtime.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    output = io.StringIO()
    sys.stdout = output
    solve()
    return output.getvalue().strip()

# Provided samples
assert run("5\n2 1\n1 2\n3 4\n5 5\n5 5 6 6 5\n1 2 5 4 3\n5 3\n1 2 3 4 5\n10 9 10 10 9\n4 0\n2 2 4 3\n2 4 2 3\n4 4\n1 2 2 1\n4 4 5 4") == "6\n27\n39\n11\n17", "provided samples"

# Custom test cases
assert run("1\n3 2\n1 2 3\n3 2 1") == "8", "swaps limited by k"
assert run("1\n3 3\n5 5 5\n1 1 1") == "15", "no swaps needed"
assert run("1\n4 4\n1 2 3 4\n4 3 2 1") == "14", "max swaps used"
assert run("1\n1 1\n1\n100") == "100", "single element swap"
assert run("1\n2 0\n1 2\n3 4") == "3", "zero swaps allowed"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 3 2 / 1 2 3 / 3 2 1 | 8 | Only beneficial swaps are performed, limited by k |
| 3 3 / 5 5 5 / 1 1 1 | 15 | No swaps needed because `a` already optimal |
| 4 4 / 1 2 3 4 / 4 3 2 1 | 14 | All swaps used correctly to maximize sum |
| 1 1 / 1 / 100 | 100 | Single element swap scenario |
| 2 0 / 1 2 / 3 4 | 3 | Zero swaps allowed, algorithm respects k |

## Edge Cases

For a case where swaps do not increase the sum, such as:

```
2 2
5 6
1 2
```

The algorithm sorts `a` ascending `[5,6]` and `b` descending `[2,1]`. On iteration `i=0`, `b[0]=2` is not greater than `a[0]=5`, so the loop breaks immediately. No swaps occur and sum remains 11. This confirms the algorithm correctly handles scenarios where swaps would be counterproductive.
