---
title: "CF 104687B - \u041e\u0442\u0441\u043e\u0440\u0442\u0438\u0440\u043e\u0432\u0430\u0442\u044c \u043c\u0430\u0441\u0441\u0438\u0432"
description: "We are given a sequence of integers and are allowed to rearrange it by sorting. After sorting, we compute the total “adjacent difference cost”, which is the sum of absolute differences between every pair of consecutive elements in the sorted sequence."
date: "2026-06-29T14:43:13+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104687
codeforces_index: "B"
codeforces_contest_name: "\u041e\u0442\u0431\u043e\u0440 \u0432 \u0426\u0420\u041e\u0414 2022"
rating: 0
weight: 104687
solve_time_s: 69
verified: false
draft: false
---

[CF 104687B - \u041e\u0442\u0441\u043e\u0440\u0442\u0438\u0440\u043e\u0432\u0430\u0442\u044c \u043c\u0430\u0441\u0441\u0438\u0432](https://codeforces.com/problemset/problem/104687/B)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 9s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a sequence of integers and are allowed to rearrange it by sorting. After sorting, we compute the total “adjacent difference cost”, which is the sum of absolute differences between every pair of consecutive elements in the sorted sequence. The task is to output this final value.

In other words, we take the array, reorder it into nondecreasing order, then measure how much it “stretches” from one element to the next when walked left to right. This is a single pass computation after sorting.

The constraint on $n$ is small, at most 100, and values can go up to $10^5$. This immediately tells us that any $O(n^2)$ or $O(n \log n)$ solution is easily fast enough. Even a straightforward sort dominates runtime and is acceptable.

A subtle point is that the absolute value sum depends heavily on ordering. Without sorting, adjacent differences could be arbitrarily large or small depending on arrangement. A naive approach that skips sorting would clearly produce incorrect results.

A typical mistake is to compute differences on the original array instead of the sorted one. For example, given input `[3, 1, 2]`, the original sum is `|3-1| + |1-2| = 2 + 1 = 3`, while the correct sorted computation gives `|1-2| + |2-3| = 1 + 1 = 2`. This mismatch shows that sorting is not optional.

Another edge case is when all values are equal. The sorted array remains constant and the result must be zero. Any implementation that accidentally uses signed differences instead of absolute values could still pass some tests but fail in mixed-sign cases.

## Approaches

A brute-force interpretation would be to try all permutations of the array, compute the adjacent difference sum for each permutation, and possibly take the minimum or some required value depending on interpretation. In this problem, since sorting is explicitly required, the brute-force view becomes unnecessary, but it is still useful as a mental model: we are searching for an ordering that makes the sequence structured enough to evaluate easily.

Enumerating all permutations costs $n!$ configurations, and each evaluation costs $O(n)$, which becomes completely infeasible even for $n = 10$. This leads to factorial explosion.

The key observation is that the problem does not ask us to optimize over permutations. It explicitly tells us to sort first. Once the array is sorted, the structure becomes monotonic. In a sorted array, the best way to compute total adjacent differences is simply to walk through once. There is no alternative ordering to consider, so the combinatorial explosion disappears.

Thus the solution reduces to two operations: sorting and linear accumulation.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force (all permutations) | $O(n! \cdot n)$ | $O(n)$ | Too slow |
| Sort + scan | $O(n \log n)$ | $O(1)$ or $O(n)$ | Accepted |

## Algorithm Walkthrough

### Steps

1. Read the integer $n$ and the array $a$. This is a single test case, so we process it once.
2. Sort the array in nondecreasing order. This ensures adjacent elements are as close as possible in value in a global sense, removing arbitrary ordering effects.
3. Initialize an accumulator variable `ans = 0`. This will store the sum of adjacent absolute differences.
4. Iterate from index `1` to `n - 1`. For each position, compute `a[i] - a[i-1]`. Because the array is sorted, this difference is always non-negative, so the absolute value is unnecessary.
5. Add each difference to `ans`.
6. Output `ans`.

### Why it works

After sorting, the sequence is monotonic nondecreasing, so every adjacent difference equals the true gap between consecutive order statistics. Any other ordering would either introduce larger jumps or duplicate small local differences multiple times. The sorted order makes every element participate exactly in the minimal necessary transitions between consecutive values, so the sum of adjacent differences is uniquely determined and directly computable from the sorted array.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input().strip())
    a = list(map(int, input().split()))
    
    a.sort()
    
    ans = 0
    for i in range(1, n):
        ans += a[i] - a[i - 1]
    
    print(ans)

if __name__ == "__main__":
    solve()
```

The implementation is straightforward. Sorting is done in-place, which keeps memory usage minimal. The loop starts from index 1 to avoid boundary checks for index 0. Since the array is sorted, we replace absolute difference with a direct subtraction, which avoids unnecessary function calls and simplifies the logic.

A common mistake would be to forget sorting or to compute `abs(a[i] - a[i-1])` on the original array. Both would violate the intended transformation described in the problem.

## Worked Examples

### Example 1

Input:

```
3
3 1 2
```

Sorted array is `[1, 2, 3]`.

| i | a[i-1] | a[i] | diff | ans |
| --- | --- | --- | --- | --- |
| 1 | 1 | 2 | 1 | 1 |
| 2 | 2 | 3 | 1 | 2 |

Output is `2`.

This confirms that sorting changes adjacency relationships and reduces arbitrary large jumps.

### Example 2

Input:

```
5
4 4 4 4 4
```

Sorted array is `[4, 4, 4, 4, 4]`.

| i | a[i-1] | a[i] | diff | ans |
| --- | --- | --- | --- | --- |
| 1 | 4 | 4 | 0 | 0 |
| 2 | 4 | 4 | 0 | 0 |
| 3 | 4 | 4 | 0 | 0 |
| 4 | 4 | 4 | 0 | 0 |

Output is `0`.

This confirms the algorithm handles uniform arrays correctly and produces no artificial contributions.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n \log n)$ | sorting dominates, single linear scan afterward |
| Space | $O(1)$ extra | sorting in place, only accumulator used |

With $n \le 100$, the solution runs far below any reasonable time limit. Even if multiple test cases were added, the same complexity would remain easily sufficient.

The memory usage is constant apart from input storage, which is negligible for this constraint range.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from contextlib import redirect_stdout
    import io as sio

    out = sio.StringIO()
    with redirect_stdout(out):
        solve()
    return out.getvalue().strip()

def solve():
    n = int(input().strip())
    a = list(map(int, input().split()))
    a.sort()
    ans = 0
    for i in range(1, n):
        ans += a[i] - a[i - 1]
    print(ans)

# provided sample
assert run("3\n3 1 2\n") == "2"

# minimum size
assert run("2\n5 1\n") == "4"

# all equal
assert run("4\n7 7 7 7\n") == "0"

# already sorted
assert run("5\n1 2 3 4 5\n") == "4"

# reverse order
assert run("5\n5 4 3 2 1\n") == "4"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 2 5 1 | 4 | minimum size correctness |
| 4 7 7 7 7 | 0 | uniform values |
| 5 1 2 3 4 5 | 4 | already sorted case |
| 5 5 4 3 2 1 | 4 | reverse order stability |

## Edge Cases

One important edge case is when all elements are identical. For input `[7, 7, 7, 7]`, sorting does nothing, and every adjacent difference is zero. The algorithm produces `0` because each subtraction yields zero, confirming no accidental accumulation.

Another case is when the input is already sorted. For `[1, 2, 3, 4, 5]`, the algorithm performs no structural change, and the scan directly computes the sum of consecutive gaps, which is correct by construction.

A third case is reverse ordering. For `[5, 4, 3, 2, 1]`, sorting transforms it into `[1, 2, 3, 4, 5]`, after which the computation proceeds identically to the already sorted case. This shows that the algorithm is invariant to initial ordering and depends only on multiset structure.
