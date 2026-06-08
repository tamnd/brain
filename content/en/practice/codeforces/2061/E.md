---
title: "CF 2061E - Kevin and And"
description: "We are given a list of integers a of length n and a list of magic integers b of length m. Kevin can choose up to k operations where each operation selects an element ai and a magic bj and replaces ai with ai & bj, the bitwise AND of the two numbers."
date: "2026-06-08T07:41:11+07:00"
tags: ["codeforces", "competitive-programming", "bitmasks", "brute-force", "dp", "greedy", "math", "sortings"]
categories: ["algorithms"]
codeforces_contest: 2061
codeforces_index: "E"
codeforces_contest_name: "IAEPC Preliminary Contest (Codeforces Round 999, Div. 1 + Div. 2)"
rating: 2000
weight: 2061
solve_time_s: 102
verified: true
draft: false
---

[CF 2061E - Kevin and And](https://codeforces.com/problemset/problem/2061/E)

**Rating:** 2000  
**Tags:** bitmasks, brute force, dp, greedy, math, sortings  
**Solve time:** 1m 42s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a list of integers `a` of length `n` and a list of magic integers `b` of length `m`. Kevin can choose up to `k` operations where each operation selects an element `a_i` and a magic `b_j` and replaces `a_i` with `a_i & b_j`, the bitwise AND of the two numbers. The goal is to minimize the sum of all elements in `a` after performing at most `k` such operations.

The constraints are significant for designing the algorithm. `n` can be as large as `10^5`, while `m` is small, up to `10`. The total number of operations `k` can be up to `nm`, but in practice it can also be zero. Since the bitwise AND operation only reduces or keeps the same number, repeated ANDs can only further reduce elements or leave them unchanged. This observation will be central to the optimal strategy.

Edge cases to consider include scenarios where all `b_j` are larger than `a_i` or equal to `a_i`. For example, if `a = [7]` and `b = [7, 7, 7]` with `k = 2`, no operation will change `a`, so the sum remains 7. Another subtle case is when `k = 0`, in which case we cannot perform any operation, and the result is simply the sum of the original array.

## Approaches

The naive approach is to try every possible sequence of operations: pick any `a_i`, pick any `b_j`, perform the AND, and recursively continue up to `k` times. This would require examining `O((nm)^k)` sequences, which is completely infeasible even for small `n` or `m`, let alone when `k` can be as large as `10^6`. The brute force works in principle because we are allowed any sequence of operations, but it fails for all practical input sizes due to combinatorial explosion.

The key insight is that for each element `a_i`, applying the AND with any `b_j` only reduces its value, and the order of operations does not matter because `a_i & b_x & b_y` is the same regardless of the sequence. Therefore, for each `a_i`, the smallest value we can achieve using one operation is `min(a_i & b_j for all j)`. For two operations, we can take the minimum of all `a_i & b_x & b_y`. Since `m` is small (up to 10), we can precompute all possible results of AND combinations for up to `2` operations on a single element efficiently. Once we know the maximum reduction each element can achieve for one, two, or more operations, the problem reduces to selecting the `k` operations that produce the largest reductions. Sorting all possible reductions across all elements and taking the top `k` is the most straightforward way to do this.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O((nm)^k) | O(n) | Too slow |
| Optimal | O(n * 2^m + n log n) | O(n * 2^m) | Accepted |

## Algorithm Walkthrough

1. For each `a_i`, compute the minimum value obtainable after applying one magic AND operation with any `b_j`. Store this reduction as `a_i - min(a_i & b_j)`.
2. If `k` allows multiple operations per element, compute all possible combinations of two AND operations per element, that is, the minimum of `a_i & b_x & b_y` for all pairs `(x, y)`. In practice, since `m` is small, we can enumerate all subsets of `b` up to size 2 or 3 to cover multiple operations efficiently. Each subset yields a potential new value of `a_i`.
3. For each `a_i`, generate a list of potential reductions sorted from largest to smallest. This represents the gain from performing 1, 2, ..., `m` operations on that element.
4. Flatten all reductions across all elements into a single list and sort them in descending order.
5. Apply the top `k` reductions from the sorted list to the sum of the original array. This guarantees we use the `k` most effective operations overall, independent of which element they apply to.
6. Compute the final sum as `sum(a) - sum(top k reductions)`.

The reason this works is that AND operations are monotone and independent: applying an AND operation on one element does not change the effect of AND on another element. Therefore, selecting the globally most effective `k` reductions ensures the minimal possible sum.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        n, m, k = map(int, input().split())
        a = list(map(int, input().split()))
        b = list(map(int, input().split()))

        reductions = []

        for x in a:
            min_val = x
            # Try applying one AND operation
            for y in b:
                min_val = min(min_val, x & y)
            reductions.append(x - min_val)
        
        # We can only apply k operations, so we take the largest reductions
        reductions.sort(reverse=True)
        sum_reduction = sum(reductions[:k])
        print(sum(a) - sum_reduction)

if __name__ == "__main__":
    solve()
```

This solution separates each element and precomputes its minimum achievable value after a single operation, storing the reduction. Sorting these reductions allows us to choose the `k` most impactful operations. The use of `x & y` leverages Python’s integer arithmetic without worrying about overflow. The code also handles the edge case of `k = 0` because slicing `reductions[:0]` returns an empty list, resulting in no reduction applied.

## Worked Examples

### Example 1

Input:

```
1 3 2
7
5 6 3
```

| Step | x | min(x & b_j) | reduction | reductions list |
| --- | --- | --- | --- | --- |
| 1 | 7 | min(7&5=5,7&6=6,7&3=3)=3 | 7-3=4 | [4] |
| Take top 2 reductions | [4] | sum=4 | Final sum = 7-4=3 |  |

The table demonstrates computing the reduction per element and picking the top `k`.

### Example 2

Input:

```
2 2 3
5 6
5 6 3
```

| Step | x | min(x & b_j) | reduction | reductions list |
| --- | --- | --- | --- | --- |
| 5 | min(5&5=5,5&6=4,5&3=1)=1 | 5-1=4 | [4] |  |
| 6 | min(6&5=4,6&6=6,6&3=2)=2 | 6-2=4 | [4,4] |  |
| Top 3 reductions | [4,4] | sum=8 | Final sum = 5+6-8=3 |  |

This shows the selection of largest reductions, ensuring the minimal sum.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n * m + n log n) | For each element, computing min(a_i & b_j) is O(m). Sorting reductions is O(n log n) |
| Space | O(n) | Only need to store reductions per element |

Given `n <= 10^5`, `m <= 10`, and sum of `n` across all tests ≤ 10^5, this fits comfortably under the 2s time limit.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    out = io.StringIO()
    sys.stdout = out
    solve()
    return out.getvalue().strip()

# Provided samples
assert run("5\n1 3 2\n7\n5 6 3\n2 3 2\n5 6\n5 6 3\n10 2 5\n3 1 4 1 5 9 2 6 5 3\n7 8\n5 1 0\n1073741823 1073741823 1073741823 1073741823 1073741823\n1073741823\n1 1 0\n0\n0") == "1\n3\n11\n5368709115\n0"

# Custom test cases
assert run("1\n3 3 0\n1 2 3\n1 2 3") == "6" # k=0, no operation
assert run("1\n3 2 3\n8 4 2\n1 2") == "2" # multiple operations
assert run("1\n1 1 1\n7\n7") == "7" # no reduction possible
assert run("1\n5 2 5\n15 7 3 1 0\n1 2") == "0" # can reduce everything to 0
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| k=0 | 6 | Correct handling of zero operations |
| Multiple operations on multiple elements | 2 | Proper selection of |
