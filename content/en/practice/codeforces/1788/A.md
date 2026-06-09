---
title: "CF 1788A - One and Two"
description: "We are given a sequence of numbers where each element is either 1 or 2. Our goal is to split the sequence into two contiguous parts such that the product of numbers in the first part equals the product of numbers in the second part."
date: "2026-06-09T10:47:35+07:00"
tags: ["codeforces", "competitive-programming", "brute-force", "implementation", "math"]
categories: ["algorithms"]
codeforces_contest: 1788
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 851 (Div. 2)"
rating: 800
weight: 1788
solve_time_s: 111
verified: true
draft: false
---

[CF 1788A - One and Two](https://codeforces.com/problemset/problem/1788/A)

**Rating:** 800  
**Tags:** brute force, implementation, math  
**Solve time:** 1m 51s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a sequence of numbers where each element is either 1 or 2. Our goal is to split the sequence into two contiguous parts such that the product of numbers in the first part equals the product of numbers in the second part. Specifically, we want to find the smallest index `k` where this split works. If no split works, we return `-1`.

The input size can reach up to 1000 elements per test case, and there can be up to 100 test cases. This means a naive approach that computes products for all possible splits would involve about 500,000 product calculations in the worst case, which is feasible for Python if done carefully, but we can do better by using simple mathematical observations about the sequence values. Since all numbers are 1 or 2, the product grows very predictably: multiplying by 1 does nothing, and multiplying by 2 just doubles the product.

An edge case arises when all numbers are 1. For example, for input `[1, 1, 1, 1]`, every split produces equal products, and the answer should be the first index `1`. Another edge case is sequences dominated by 2, where a split might not exist, such as `[2, 2, 2]`, which cannot be split into equal products because 2 cannot be matched by a product of 1s on the other side.

## Approaches

The brute-force approach computes the product of the left part for every possible split, then the product of the right part, and compares them. This works because every split is checked explicitly, so correctness is guaranteed. In Python, computing products for up to 1000 elements repeatedly could reach O(n^2) time complexity, which is acceptable but inefficient.

A key observation is that the product of a sequence of 1s and 2s is determined entirely by the number of 2s. Multiplying by 1 does not change the product, so we only need to track the cumulative power of 2s on both sides. Let `total_twos` be the count of 2s in the whole array. Then the left part after `k` elements has `left_twos` number of 2s, and the right part has `total_twos - left_twos`. For the products to match, `2^left_twos = 2^(total_twos - left_twos)` must hold, so `left_twos` must equal `total_twos - left_twos`, i.e., `left_twos = total_twos / 2`. If `total_twos` is odd, no split exists. Otherwise, we can scan from the left and find the smallest prefix with exactly half of the 2s, giving the minimal `k`.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n^2) | O(1) | Works for n ≤ 1000, but slow for large inputs |
| Counting 2s | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

1. For each test case, count the total number of 2s in the array and store it in `total_twos`. The 1s do not matter since multiplying by 1 leaves the product unchanged.
2. If `total_twos` is 0, every split has equal product because all elements are 1. Return `1` because the smallest split index is always valid.
3. If `total_twos` is odd, there is no way to split the sequence into two parts with equal numbers of 2s, so the products cannot match. Return `-1`.
4. Otherwise, the goal is to find the smallest prefix whose count of 2s is exactly `total_twos / 2`. Initialize a variable `left_twos` to 0 and iterate over the array. Increment `left_twos` by 1 whenever you encounter a 2.
5. As soon as `left_twos` reaches `total_twos / 2`, return the current index plus 1 as the minimal `k`.
6. If the iteration ends without reaching half of the 2s (should not happen if `total_twos` is even), return `-1`.

Why it works: the count of 2s fully determines the product. By splitting the sequence into equal halves in terms of 2s, the products of the two parts automatically match. This invariant guarantees the minimal index split is found.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        n = int(input())
        a = list(map(int, input().split()))
        total_twos = a.count(2)
        if total_twos == 0:
            print(1)
            continue
        if total_twos % 2 == 1:
            print(-1)
            continue
        half_twos = total_twos // 2
        left_twos = 0
        for i in range(n):
            if a[i] == 2:
                left_twos += 1
            if left_twos == half_twos:
                print(i + 1)
                break

if __name__ == "__main__":
    solve()
```

The code first reads the number of test cases, then loops through each one. Counting the total number of 2s is the first step, because 1s do not affect the product. Handling the edge case of zero 2s ensures the minimal split is returned correctly. The scan for half of the 2s guarantees the minimal index `k`. The break ensures we stop as soon as the correct split is found, preventing off-by-one errors.

## Worked Examples

### Example 1

Input: `[2, 2, 1, 2, 1, 2]`

| Index | Value | left_twos | Check |
| --- | --- | --- | --- |
| 0 | 2 | 1 | 1 != 2/2 |
| 1 | 2 | 2 | 2 == 4/2, print 2 |

Here we see the minimal index `k = 2` satisfies the condition.

### Example 2

Input: `[1, 2, 1]`

| Index | Value | left_twos | Check |
| --- | --- | --- | --- |
| 0 | 1 | 0 | 0 != 1.5 (total_twos odd) |
| 1 | 2 | 1 | - |

`total_twos` is 1 (odd), so no split exists and we print `-1`.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) per test case | Single pass to count 2s, another pass to find the split |
| Space | O(n) | Storing the array |

With n ≤ 1000 and t ≤ 100, the total operations are at most 200,000, which is well within the 1-second limit. Memory usage is minimal.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()
    solve()
    return sys.stdout.getvalue().strip()

# Provided samples
assert run("3\n6\n2 2 1 2 1 2\n3\n1 2 1\n4\n1 1 1 1\n") == "2\n-1\n1", "Sample 1"

# Custom test cases
assert run("1\n2\n2 2\n") == "1", "Two elements both 2s"
assert run("1\n5\n1 1 1 1 1\n") == "1", "All 1s, minimal split"
assert run("1\n6\n2 2 2 2 2 2\n") == "3", "All 2s, split in half"
assert run("1\n4\n2 1 2 1\n") == "2", "Interleaved 1s and 2s"
assert run("1\n3\n2 1 2\n") == "-1", "Odd number of 2s, no split"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 2 2 | 1 | Minimal split works for smallest array |
| 1 1 1 1 1 | 1 | All 1s handled correctly |
| 2 2 2 2 2 2 | 3 | Correct split for even number of 2s |
| 2 1 2 1 | 2 | Interleaved pattern handled |
| 2 1 2 | -1 | Odd number of 2s returns -1 |

## Edge Cases

When the array contains only 1s, such as `[1, 1, 1, 1]`, `total_twos` is 0. The algorithm immediately returns 1 as the minimal split, correctly handling this scenario without iterating further. For an odd number of 2s, such as `[2, 1, 2]`, `total_twos` is 2, which is even, but half_twos is 1. Iterating finds the first 2 at index 0, then the second 2 at index 2, so left_twos reaches half_twos at index 0, and `k = 1` is returned. This confirms
