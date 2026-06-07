---
title: "CF 2209B - Array"
description: "We are given an array of integers, and for each element, we need to determine how many elements to its right can be “dominated” by it, in a specific sense."
date: "2026-06-07T19:21:48+07:00"
tags: ["codeforces", "competitive-programming", "greedy"]
categories: ["algorithms"]
codeforces_contest: 2209
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 1087 (Div. 2)"
rating: 900
weight: 2209
solve_time_s: 87
verified: true
draft: false
---

[CF 2209B - Array](https://codeforces.com/problemset/problem/2209/B)

**Rating:** 900  
**Tags:** greedy  
**Solve time:** 1m 27s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given an array of integers, and for each element, we need to determine how many elements to its right can be “dominated” by it, in a specific sense. For an element `a[i]`, we want to count the maximum number of indices `j > i` such that there exists some integer `k` for which the absolute difference `|a[i] - k|` is strictly greater than `|a[j] - k|`. The key is that `k` can be chosen independently for each `i`, and we want the count to be maximal.

This is equivalent to asking: for each element `a[i]`, how many later elements `a[j]` are strictly between `a[i]` and some chosen `k`? Intuitively, choosing `k` either very large or very small allows `a[i]` to dominate all elements either less than or greater than itself. The optimal `k` is always just outside the range of two elements to maximize the count.

The constraints indicate that the array can have up to 5000 elements in total across all test cases. A naive approach that examines every pair `(i, j)` for all potential `k` would take O(n²) operations, which is acceptable because n ≤ 5000, but there may be a simpler method using the properties of numbers rather than brute-force iteration over `k`.

Edge cases include arrays of size 1, arrays with repeated elements, and arrays where the largest or smallest element appears at the start or end. For example, an array `[5, 5, 5]` must produce `[0, 0, 0]`, because no matter the choice of `k`, no element is strictly “closer” to `k` than another when the values are equal.

## Approaches

The brute-force approach would iterate over each element `a[i]`, then for each `i`, check every element `a[j]` for `j > i`. For each pair `(i, j)`, we would try to find an integer `k` such that `|a[i] - k| > |a[j] - k|`. This inequality reduces to a simple check: `k` should be outside the interval between `a[i]` and `a[j]`. Concretely, either `k < min(a[i], a[j])` or `k > max(a[i], a[j])`. Since such a `k` always exists for any `i ≠ j`, the condition reduces to checking `a[i] ≠ a[j]`. The naive complexity is O(n²) per test case, which is tolerable given the constraints.

The optimal approach exploits the observation that for any `a[i]`, the maximal count of dominated elements is achieved by choosing `k` far to the left or far to the right, so that `a[i]` is further from `k` than `a[j]` if `a[j]` lies between `a[i]` and `k`. This reduces the problem to counting the number of elements to the right of `i` that are either strictly smaller or strictly larger than `a[i]`, and taking the maximum of these two counts. We no longer need to compute or iterate over `k`.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n²) | O(1) | Acceptable for n ≤ 5000 |
| Optimized Greedy | O(n²) | O(1) | Accepted, simpler logic |

## Algorithm Walkthrough

1. For each test case, read the array `a` of length `n`.
2. Initialize a result array `res` of length `n` with zeros.
3. Iterate over each index `i` from `0` to `n-1`.
4. For `i`, initialize two counters `count_less` and `count_greater` to zero.
5. Iterate over each index `j` from `i+1` to `n-1`. If `a[j] < a[i]`, increment `count_less`. If `a[j] > a[i]`, increment `count_greater`.
6. Set `res[i]` to the maximum of `count_less` and `count_greater`.
7. After processing all indices, output the result array for the test case.

Why it works: For each `i`, the number of elements that can be dominated depends only on the relative values of `a[i]` and `a[j]`. Choosing `k` far to the left will dominate all smaller elements, and choosing `k` far to the right will dominate all larger elements. Since we want the maximum, taking the larger of these two counts gives the correct answer. No element is ever double-counted because domination is independent for each `i`.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        n = int(input())
        a = list(map(int, input().split()))
        res = [0] * n
        for i in range(n):
            count_less = 0
            count_greater = 0
            for j in range(i + 1, n):
                if a[j] < a[i]:
                    count_less += 1
                elif a[j] > a[i]:
                    count_greater += 1
            res[i] = max(count_less, count_greater)
        print(" ".join(map(str, res)))
```

The code directly implements the algorithm steps. Each `i` is compared only with indices after it. Using `max(count_less, count_greater)` ensures we select the optimal `k` implicitly. The approach avoids unnecessary computation of actual `k` values, relying only on relative ordering.

## Worked Examples

For the array `[1, 2, 93, 84, 2]`:

| i | a[i] | Elements after i | count_less | count_greater | res[i] |
| --- | --- | --- | --- | --- | --- |
| 0 | 1 | [2, 93, 84, 2] | 0 | 4 | 4 |
| 1 | 2 | [93, 84, 2] | 1 | 2 | 2 |
| 2 | 93 | [84, 2] | 2 | 0 | 2 |
| 3 | 84 | [2] | 1 | 0 | 1 |
| 4 | 2 | [] | 0 | 0 | 0 |

This confirms that taking the max of counts of larger and smaller elements after `i` correctly computes the solution.

For the array `[105, -105]`:

| i | a[i] | Elements after i | count_less | count_greater | res[i] |
| --- | --- | --- | --- | --- | --- |
| 0 | 105 | [-105] | 1 | 0 | 1 |
| 1 | -105 | [] | 0 | 0 | 0 |

This demonstrates that the algorithm handles negative numbers and small arrays correctly.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n²) | Each element is compared with all elements to its right |
| Space | O(n) | Result array of length n; no extra structures |

Given the sum of `n` across all test cases is ≤ 5000, the worst-case number of comparisons is around 25 million, which is acceptable under a 2-second time limit. Memory usage is minimal.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    out = io.StringIO()
    sys.stdout = out
    solve()
    sys.stdout = sys.__stdout__
    return out.getvalue().strip()

# Provided samples
assert run("6\n1\n1092\n2\n105 -105\n5\n1 2 93 84 2\n7\n2 9 38 4 7 1 6\n10\n1 9 20 9 829 3 87 1 283 7\n11\n9 18 29817 283 3 3928 5726 1942 1000000000 -1000000000 19\n") == \
"0\n1 0\n4 2 2 1 0\n5 4 4 2 2 1 0\n8 4 4 3 5 3 2 2 1 0\n8 7 7 4 5 3 3 2 2 1 0"

# Custom cases
assert run("1\n1\n42\n") == "0", "single element"
assert run("1\n3\n5 5 5\n") == "0 0 0", "all equal"
assert run("1\n4\n1 2 3 4\n") == "3 2 1 0", "strictly increasing"
assert run("1\n4\n4 3 2 1\n") == "3 2 1 0", "strictly decreasing"
assert run("1\n5\n1 -1 2 -2 0\n") == "3 2 2 1 0", "mixed signs"
```

| Test input | Expected output
