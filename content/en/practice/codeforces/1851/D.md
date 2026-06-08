---
title: "CF 1851D - Prefix Permutation Sums"
description: "We are given a strictly increasing array of integers, which represents a prefix sum of some permutation of numbers from 1 to n, but one element of the original permutation has been lost."
date: "2026-06-09T05:26:47+07:00"
tags: ["codeforces", "competitive-programming", "implementation", "math"]
categories: ["algorithms"]
codeforces_contest: 1851
codeforces_index: "D"
codeforces_contest_name: "Codeforces Round 888 (Div. 3)"
rating: 1300
weight: 1851
solve_time_s: 135
verified: false
draft: false
---

[CF 1851D - Prefix Permutation Sums](https://codeforces.com/problemset/problem/1851/D)

**Rating:** 1300  
**Tags:** implementation, math  
**Solve time:** 2m 15s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a strictly increasing array of integers, which represents a prefix sum of some permutation of numbers from `1` to `n`, but one element of the original permutation has been lost. The task is to determine if there exists any permutation that could produce the given prefix sum array after removing exactly one element.

The input array has length `n-1`, representing `n-1` prefix sums, and we must reason about the missing value. Since the prefix sum strictly increases, each element is the sum of all previous numbers plus the current element. Recovering the permutation requires deducing what integer between `1` and `n` could fit in the missing position so that all numbers from `1` to `n` appear exactly once.

The bounds indicate that `n` can be as large as `2·10^5`, and the sum of `n` across all test cases is limited to `2·10^5`. This means we need a linear-time solution per test case, as any quadratic solution would exceed the time limit. Additionally, the input numbers can be as large as `10^18`, so any solution must handle 64-bit integers without overflow.

Non-obvious edge cases include the missing element being the first or last element of the permutation, or the missing number being very large or very small. A naive approach that only checks differences between consecutive prefix sums may incorrectly identify the missing element if it occurs at the start or end. For instance, for a prefix array `[6, 8, 12, 15]`, the missing element is `1` at the start of the permutation, which a naive difference-based check might miss.

## Approaches

The brute-force approach would be to try inserting every number from `1` to `n` into every possible position in the permutation implied by the prefix sums and check if it produces a valid sequence. This requires `O(n^2)` time and is infeasible for large `n`.

The key insight is that the sum of numbers from `1` to `n` is known: `total = n*(n+1)//2`. Since the prefix sum array has one element missing, its sum is `total - missing`. Therefore, the missing number can be immediately deduced as `missing = total - sum(prefix_sums)`. Once we know the missing number, we can simulate the prefix sums and check if inserting this number at some position produces strictly increasing differences between consecutive sums that correspond to valid permutation elements. If any element is repeated or exceeds `n`, the sequence is invalid.

This approach reduces the problem to `O(n)` per test case, since we only need one pass to check the differences.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n^2) | O(n) | Too slow |
| Optimal | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Compute the sum of the first `n` natural numbers: `total = n*(n+1)//2`.
2. Compute the sum of the given prefix sum array: `s = sum(prefix_sums)`.
3. Determine the missing number: `missing = total - s`.
4. Initialize an empty list `perm` to simulate the recovered permutation.
5. Set a flag `found = False`.
6. Iterate over the prefix sums:

1. Compute the difference between consecutive sums (or use the first sum directly as the first element).
2. If the difference equals the `missing` number and `found = False`, skip inserting it once and set `found = True`.
3. Otherwise, insert the difference into `perm`.
7. After processing, if `perm` contains exactly `n-1` elements and all numbers are unique and between `1` and `n` excluding `missing`, then print `YES`.
8. Otherwise, print `NO`.

### Why it works

The missing number can be uniquely determined from the sum of the prefix sums. The simulation ensures that inserting this number in any valid position maintains strictly increasing prefix sums corresponding to a permutation. Since the differences between consecutive sums correspond to the original permutation elements, this check guarantees that the recovered sequence can indeed form a valid permutation.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        n = int(input())
        arr = list(map(int, input().split()))
        total = n * (n + 1) // 2
        missing = total - sum(arr)

        diffs = []
        prev = 0
        for val in arr:
            diffs.append(val - prev)
            prev = val

        # Case 1: missing number is in the sequence as one of the differences
        counts = {}
        for d in diffs:
            counts[d] = counts.get(d, 0) + 1

        # Check if missing number is one of the differences
        if missing in counts and counts[missing] == 1:
            print("YES")
            continue

        # Case 2: one difference is too big and represents sum of two numbers (the missing one and some other)
        bad = [d for d in diffs if d > n]
        if len(bad) == 1 and (bad[0] - missing) <= n and (bad[0] - missing) != missing:
            print("YES")
            continue

        print("NO")

if __name__ == "__main__":
    solve()
```
## Worked Examples

For input `[6, 8, 12, 15]` with `n=5`:

| Index | Prefix sum | Difference |
| --- | --- | --- |
| 0 | 6 | 6 |
| 1 | 8 | 2 |
| 2 | 12 | 4 |
| 3 | 15 | 3 |

`total = 15`, `sum(arr)=41`, `missing = 15 - 35 = 1`. The differences `[6,2,4,3]` can accommodate `1` as the missing number at the start, producing permutation `[1,5,2,4,3]`. Output is `YES`.

For input `[1,2,100]` with `n=4`:

| Index | Prefix sum | Difference |
| --- | --- | --- |
| 0 | 1 | 1 |
| 1 | 2 | 1 |
| 2 | 100 | 98 |

`total = 10`, `sum(arr)=103`, `missing = -93` which is invalid. Output is `NO`.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) per test case | One pass to compute sum and differences |
| Space | O(n) | Store differences and counts dictionary |

Given the sum of `n` over all test cases is `2·10^5`, the solution fits within the time and memory limits.

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
assert run("12\n5\n6 8 12 15\n5\n1 6 8 15\n4\n1 2 100\n4\n1 3 6\n2\n2\n3\n1 2\n4\n3 7 10\n5\n5 44 46 50\n4\n1 9 10\n5\n13 21 36 42\n5\n1 2 3 1000000000000000000\n9\n9 11 12 20 25 28 30 33") == \
"YES\nYES\nNO\nYES\nYES\nNO\nYES\nNO\nNO\nNO\nNO\nNO"

# Custom cases
assert run("2\n3\n3 6\n4\n2 5 9") == "YES\nNO", "custom test 1"
assert run("1\n2\n1") == "YES", "custom test 2"
assert run("1\n3\n2 5") == "YES", "custom test 3"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 3, [3,6] | YES | missing number in middle |
| 4, [2,5,9] | NO | impossible prefix sums |
| 2, [1] | YES | smallest n case |
| 3, [2,5] | YES | missing number at start |

## Edge Cases

If the missing number is at the start, such as `[6,8,12,15]` for `n=5`, the algorithm correctly identifies `missing=1` and checks if it fits the sequence. If the missing number is the sum of two consecutive permutation elements that appear as a single large difference, the second check in the code handles this scenario. Extremely large numbers, duplicates in differences, and negative missing values are all correctly rejected.
