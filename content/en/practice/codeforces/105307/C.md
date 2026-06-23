---
title: "CF 105307C - Chopsticks"
description: "We are given a collection of identical “pairs” of chopsticks, where each pair is characterized by a single integer length. From each pair we can treat the two chopsticks as two equal sides of a rectangle."
date: "2026-06-23T14:46:57+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105307
codeforces_index: "C"
codeforces_contest_name: "ICPC 2024 Thailand - Chulalongkorn University Internal Round"
rating: 0
weight: 105307
solve_time_s: 65
verified: true
draft: false
---

[CF 105307C - Chopsticks](https://codeforces.com/problemset/problem/105307/C)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 5s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a collection of identical “pairs” of chopsticks, where each pair is characterized by a single integer length. From each pair we can treat the two chopsticks as two equal sides of a rectangle. To form a rectangle, we must pick two different pairs: one pair will provide the vertical sides and the other pair will provide the horizontal sides. If we choose a pair with length `a` and another pair with length `b`, the rectangle area becomes `a × b`.

The task is to maximize this product over all choices of two distinct pairs.

The input size is small, with at most 100 pairs. This immediately rules out any concern about higher-order complexity constraints. Even an O(N³) solution would pass comfortably, since the worst case is only around one million operations. However, the presence of large values up to 10⁹ means we must be careful with integer multiplication, though Python handles big integers safely.

A subtle point is that we are selecting pairs, not individual chopsticks. This means each chosen length is taken as-is from the list of pair lengths. There is no need to split or match individual sticks.

Edge cases are mostly about structure rather than performance. If all lengths are equal, any two pairs produce the same rectangle. If there are exactly two pairs, the answer is simply their product. If the maximum values occur multiple times, we must ensure we pick two distinct occurrences of the same maximum value, because using the same pair twice is not allowed even if values match.

## Approaches

The most direct approach is to try every pair of distinct indices. For each pair `(i, j)`, compute `l[i] * l[j]` and track the maximum. This is correct because every valid rectangle corresponds exactly to a choice of two distinct pairs, and we evaluate all such choices.

This brute-force approach runs in O(N²) time. With N ≤ 100, this means at most 4950 multiplications, which is trivial. So strictly speaking, this already passes.

However, we can still simplify the reasoning by noticing what actually matters. Since we are maximizing a product of two numbers chosen from the list, the optimal solution must involve the two largest values in the array. The product of any smaller element with the maximum cannot exceed the product of the second maximum with the maximum. Therefore, sorting or tracking the top two values is sufficient.

This reduces the problem to scanning once and keeping the largest and second-largest values.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Pair Enumeration | O(N²) | O(1) | Accepted |
| Track Top Two Values | O(N) | O(1) | Accepted |

## Algorithm Walkthrough

We focus on the linear solution that extracts the two largest values.

1. Initialize two variables `first` and `second` to zero. These will store the largest and second-largest lengths seen so far. We use zero because all input values are positive.
2. Iterate through each length `x` in the input list.
3. If `x` is greater than or equal to `first`, shift `first` into `second`, then set `first = x`. This ensures the previous maximum is not lost and remains a candidate for second place.
4. Otherwise, if `x` is greater than `second`, update `second = x`. This keeps track of the best value that is not the maximum.
5. After processing all values, compute the answer as `first * second`.

The key subtlety is handling duplicates of the maximum value. If the maximum appears at least twice, this procedure correctly sets both `first` and `second` to that maximum, producing the correct squared result.

### Why it works

At any prefix of the array, `first` and `second` represent the largest and second-largest values encountered so far. Any future element either becomes the new maximum or competes for second place. This invariant guarantees that after processing all elements, no pair of values in the array can have a product larger than `first × second`, since any candidate pair must involve values that are both less than or equal to these two maxima.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input().strip())
    arr = list(map(int, input().split()))
    
    first = 0
    second = 0
    
    for x in arr:
        if x >= first:
            second = first
            first = x
        elif x > second:
            second = x
    
    print(first * second)

if __name__ == "__main__":
    solve()
```

The solution reads the list, then maintains two running maxima. The key implementation detail is the `>=` condition when updating `first`. This ensures that duplicate maximum values correctly propagate into `second`, which is necessary for cases like `[3, 3]`, where both values must be used.

We avoid sorting because it is unnecessary overhead, though it would also be correct. The single-pass update is simpler and avoids extra memory.

## Worked Examples

### Sample 1

Input: `3 1 2 3`

We track `first` and `second`:

| x | first | second | Action |
| --- | --- | --- | --- |
| 1 | 1 | 0 | first updated |
| 2 | 2 | 1 | first updated, old first becomes second |
| 3 | 3 | 2 | first updated, old first becomes second |

Final answer is `3 × 2 = 6`.

This confirms that the algorithm always preserves the top two values seen so far.

### Sample 2

Input: `4 1 2 3 3`

| x | first | second | Action |
| --- | --- | --- | --- |
| 1 | 1 | 0 | first updated |
| 2 | 2 | 1 | first updated |
| 3 | 3 | 2 | first updated |
| 3 | 3 | 3 | duplicate max updates second |

Final answer is `3 × 3 = 9`.

This demonstrates the importance of handling duplicates of the maximum correctly. Without the `>=` condition, `second` would incorrectly remain 2, producing 6 instead of 9.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(N) | Each value is processed once in a single scan |
| Space | O(1) | Only two variables are maintained regardless of input size |

The constraints allow up to 100 values, so this solution is far below the limit. Even a quadratic approach would be safe, but the linear scan is cleaner and more direct.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline
    
    n = int(input().strip())
    arr = list(map(int, input().split()))
    
    first = 0
    second = 0
    
    for x in arr:
        if x >= first:
            second = first
            first = x
        elif x > second:
            second = x
    
    return str(first * second)

# provided samples
assert run("3\n1 2 3\n") == "6"
assert run("4\n1 2 3 3\n") == "9"

# custom cases
assert run("2\n5 7\n") == "35", "simple two elements"
assert run("3\n10 10 1\n") == "100", "duplicate max handling"
assert run("5\n1 1 1 1 1\n") == "1", "all equal values"
assert run("6\n9 8 7 6 5 4\n") == "72", "descending order"
assert run("5\n1 1000000000 2 3 4\n") == "4000000000", "large values"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `2 / 5 7` | 35 | minimal non-trivial case |
| `3 / 10 10 1` | 100 | duplicate maximum handling |
| `5 / 1 1 1 1 1` | 1 | all equal values |
| `6 / 9 8 7 6 5 4` | 72 | descending order stability |
| `5 / 1 1000000000 2 3 4` | 4000000000 | large value multiplication |

## Edge Cases

For the case where the maximum value appears more than once, consider input `3 3 3`. The scan proceeds by setting `first = 3`, `second = 0` on the first element. On the second `3`, the condition `x >= first` triggers again, shifting `first` into `second` and setting both to 3. The final element does not change anything. The result becomes `3 × 3 = 9`, which is correct because we are allowed to pick two different pairs even if their values are identical.

For a strictly increasing sequence like `1 2 3`, the algorithm naturally ends with `first = 3` and `second = 2`. The product `6` corresponds to selecting the two largest available pair lengths, which is optimal because any smaller pairing reduces one factor without increasing the other.
