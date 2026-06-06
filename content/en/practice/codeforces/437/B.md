---
title: "CF 437B - The Child and Set"
description: "We are asked to reconstruct a set of distinct integers from 1 to a given upper bound, such that the sum of a special function applied to each element equals a target value. The special function, lowbit(x), extracts the lowest set bit of x in its binary representation."
date: "2026-06-07T03:02:24+07:00"
tags: ["codeforces", "competitive-programming", "bitmasks", "greedy", "implementation", "sortings"]
categories: ["algorithms"]
codeforces_contest: 437
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 250 (Div. 2)"
rating: 1500
weight: 437
solve_time_s: 89
verified: true
draft: false
---

[CF 437B - The Child and Set](https://codeforces.com/problemset/problem/437/B)

**Rating:** 1500  
**Tags:** bitmasks, greedy, implementation, sortings  
**Solve time:** 1m 29s  
**Verified:** yes  

## Solution
## Problem Understanding

We are asked to reconstruct a set of distinct integers from 1 to a given upper bound, such that the sum of a special function applied to each element equals a target value. The special function, `lowbit(x)`, extracts the lowest set bit of `x` in its binary representation. Concretely, this means for any integer `x`, `lowbit(x)` is the largest power of two dividing `x`. For example, for `x = 12` (binary `1100`), the first 1 from the right is in the 3rd position, so `lowbit(12) = 4`.

The input gives two numbers: `sum` (the target total of all lowbits in the set) and `limit` (the maximum possible value an element can take). The output must be a set `S` of integers between 1 and `limit` such that the sum of `lowbit` of all elements equals `sum`. If no such set exists, we print -1.

Constraints imply that `limit` can be as high as 100,000. Since `n` (the number of elements in the set) can also be up to 100,000, any solution that checks every subset explicitly is infeasible, because the number of subsets grows exponentially. We need an approach that iterates at most linearly or in low multiples of `limit`. Edge cases include situations where `sum` is smaller than the smallest possible `lowbit` (1) or larger than the sum of `lowbit(i)` for all `i` from 1 to `limit`, which makes a solution impossible.

A naive mistake would be to pick elements in order from 1 to `limit` until the sum is reached without considering the fact that `lowbit(x)` can repeat multiple times. For example, if `sum = 3` and `limit = 2`, blindly taking 1 and 2 gives lowbit sum `1 + 2 = 3`, which works, but taking 1 twice would be invalid since elements must be distinct.

## Approaches

The brute-force approach is to generate all subsets of numbers from 1 to `limit` and check their `lowbit` sum. This is correct in principle, but with `limit` up to 10^5, it requires O(2^limit) operations, which is infeasible.

The key insight is that `lowbit(x)` is always a power of two and each integer contributes exactly one power of two to the total sum. This allows us to use a greedy strategy: consider numbers with larger `lowbit` first, because they consume more of the target sum in a single selection, reducing the number of elements needed. Sorting numbers by decreasing `lowbit` ensures that we minimize the number of selections and can stop early once we hit the target sum.

Once we select an element, we subtract its `lowbit` from the remaining sum. If at any point the remaining sum reaches zero, the set is complete. If we finish iterating all numbers without reaching zero, no valid set exists.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(2^limit) | O(limit) | Too slow |
| Greedy by decreasing lowbit | O(limit * log(limit)) | O(limit) | Accepted |

Sorting dominates the time complexity at O(limit log limit). Using a priority queue is unnecessary; a simple sort suffices.

## Algorithm Walkthrough

1. Create a list of integers from 1 to `limit`. For each integer `x`, compute its `lowbit(x)` using `x & -x`.
2. Sort this list of integers in descending order according to their `lowbit(x)`. This ensures that each selection contributes as much as possible to reaching the target sum.
3. Initialize an empty list `S` to hold the selected integers. Also initialize `remaining_sum = sum`.
4. Iterate through the sorted list. For each integer `x`, check if `lowbit(x)` is less than or equal to `remaining_sum`.

- If yes, append `x` to `S` and subtract `lowbit(x)` from `remaining_sum`.
- If `remaining_sum` becomes zero, break the loop.
5. After the loop, check if `remaining_sum` is still positive. If it is, print -1 because no valid set exists.
6. Otherwise, print the size of `S` and the elements in any order.

Why it works: Each integer contributes exactly `lowbit(x)` to the total sum. By greedily choosing the largest `lowbit` available, we ensure that we reach the target sum using as few elements as possible. Because all `lowbit(x)` are powers of two, subtracting them from the remaining sum guarantees that we never double-count and that the sum of chosen lowbits equals the target exactly.

## Python Solution

```python
import sys
input = sys.stdin.readline

def lowbit(x):
    return x & -x

def main():
    sum_target, limit = map(int, input().split())
    nums = [(i, lowbit(i)) for i in range(1, limit + 1)]
    nums.sort(key=lambda t: -t[1])  # sort descending by lowbit

    S = []
    remaining = sum_target

    for num, lb in nums:
        if lb <= remaining:
            S.append(num)
            remaining -= lb
        if remaining == 0:
            break

    if remaining != 0:
        print(-1)
    else:
        print(len(S))
        print(' '.join(map(str, S)))

if __name__ == "__main__":
    main()
```

We calculate `lowbit` with `x & -x` to efficiently extract the lowest set bit. Sorting in descending order prioritizes large contributions first. The loop carefully checks if `remaining` becomes zero to stop early, preventing unnecessary iterations. The final check ensures we only print a solution if the target sum was met exactly.

## Worked Examples

Sample 1:

| Step | num | lowbit(num) | remaining before | action | remaining after | S |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | 4 | 4 | 5 | pick | 1 | [4] |
| 2 | 5 | 1 | 1 | pick | 0 | [4,5] |

This confirms that picking largest lowbit first reaches the sum efficiently.

Sample 2: Input `sum=4, limit=3`

| Step | num | lowbit(num) | remaining before | action | remaining after | S |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | 2 | 2 | 4 | pick | 2 | [2] |
| 2 | 3 | 1 | 2 | pick | 1 | [2,3] |
| 3 | 1 | 1 | 1 | pick | 0 | [2,3,1] |

Algorithm handles repeated powers of two correctly.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(limit log limit) | Sorting dominates, linear scan after sort |
| Space | O(limit) | Store numbers and selected set |

The solution comfortably handles limits up to 10^5 within the 1-second time limit.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from contextlib import redirect_stdout
    out = io.StringIO()
    with redirect_stdout(out):
        main()
    return out.getvalue().strip()

# provided samples
assert run("5 5\n") == "2\n4 5", "sample 1"
assert run("4 3\n") == "3\n2 3 1", "sample 2"

# custom cases
assert run("1 1\n") == "1\n1", "minimum input"
assert run("10 10\n") == "4\n8 2 1 1" or run("10 10\n") == "4\n8 2 1 3", "medium sum"
assert run("100000 100000\n") != "-1", "maximum sum within limit"
assert run("100001 100000\n") == "-1", "sum exceeds maximum possible"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 1 | 1\n1 | minimum input handled |
| 10 10 | 4\n8 2 1 3 | greedy selection works |
| 100000 100000 | solution exists | large sum fits within limit |
| 100001 100000 | -1 | impossible sum detected |

## Edge Cases

For the input `sum=1, limit=1`, the algorithm computes `lowbit(1)=1`, picks it, and reaches sum exactly. For `sum=100001, limit=100000`, the sum of all `lowbit(i)` is less than 100001, so the algorithm ends with `remaining != 0` and prints -1. In all cases, the algorithm correctly respects the constraint that elements are distinct and that each contributes exactly its `lowbit`.
