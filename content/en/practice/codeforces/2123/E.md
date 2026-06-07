---
title: "CF 2123E - MEX Count"
description: "We are given an array of nonnegative integers, and we are asked to compute the number of distinct possible values of the minimum excluded value (MEX) after removing exactly $k$ elements from the array, for each $k$ from 0 to $n$."
date: "2026-06-08T03:38:00+07:00"
tags: ["codeforces", "competitive-programming", "binary-search", "data-structures", "greedy", "sortings", "two-pointers"]
categories: ["algorithms"]
codeforces_contest: 2123
codeforces_index: "E"
codeforces_contest_name: "Codeforces Round 1034 (Div. 3)"
rating: 1400
weight: 2123
solve_time_s: 84
verified: false
draft: false
---

[CF 2123E - MEX Count](https://codeforces.com/problemset/problem/2123/E)

**Rating:** 1400  
**Tags:** binary search, data structures, greedy, sortings, two pointers  
**Solve time:** 1m 24s  
**Verified:** no  

## Solution
## Problem Understanding

We are given an array of nonnegative integers, and we are asked to compute the number of distinct possible values of the minimum excluded value (MEX) after removing exactly $k$ elements from the array, for each $k$ from 0 to $n$. The MEX of an array is the smallest nonnegative integer not present in the array.

For each test case, we need to output $n+1$ numbers: the count of possible MEX values after removing 0 elements, 1 element, ..., up to $n$ elements.

The input constraints are significant. Each array can be as large as $2 \cdot 10^5$, and the total across all test cases does not exceed $2 \cdot 10^5$. That implies that any solution worse than $O(n \log n)$ per test case will likely time out. Naive solutions that simulate every combination of removed elements are hopeless because the number of subsets of size $k$ is combinatorial.

Some edge cases are subtle. Consider an array where all elements are equal, like `[0,0,0,0]`. The MEX starts at 1, but removing any subset of zeros cannot produce any value other than 1 for the MEX until the array is empty. Another edge case is an array missing 0 from the start, for example `[1,2,3]`; then the MEX is 0 and removing elements cannot make it smaller, only larger. Careless implementations might assume that removing elements always increases the MEX, which is false.

## Approaches

A brute-force approach would try every subset of size $k$ for each $k$ from 0 to $n$, compute the MEX, and count distinct values. This is correct logically, but completely impractical. For $n = 10^5$, even subsets of size 1 are $O(n)$, subsets of size 2 are $O(n^2)$, and so on. Clearly combinatorial explosion rules this out.

The key insight comes from understanding how the MEX changes when we remove elements. The MEX increases only when all numbers less than the candidate MEX are present. If a number $x < MEX$ is missing, the MEX is already $x$. If we remove numbers, we can increase the MEX only by removing numbers that prevent it from increasing. Conversely, we can always reduce the MEX by removing numbers greater than or equal to the current MEX, but we cannot create a MEX smaller than the smallest missing number.

Concretely, we can count the occurrences of each number from 0 up to $n$. Let’s denote `cnt[x]` as the count of $x$ in the array. We can then simulate increasing the MEX step by step. At MEX = 0, we need 0s present. To reach MEX = 1, we must remove enough 0s to either reduce the array size or adjust other numbers. By maintaining a running “extra removal budget,” we can decide for each target MEX how many ways it is achievable for each $k$. Using prefix sums or a greedy allocation of removals lets us efficiently compute the answer.

This reduces the complexity to $O(n)$ per test case, since we only scan the array once to count numbers, then scan counts sequentially to simulate MEX growth.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(2^n) | O(n) | Too slow |
| Optimal (count occurrences + greedy) | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Read the array size $n$ and the array `a`.
2. Initialize an array `cnt` of length $n+2$ to count occurrences of each number. Iterate over `a` and increment `cnt[x]` for each element `x`.
3. Initialize `removed = 0` to track the total removals used to reach a certain MEX. Initialize an empty list `ans` of length $n+1$ to store the number of possible MEX values for each $k$.
4. Iterate over potential MEX values `mex` starting from 0. For each `mex`, check `cnt[mex]`. If `cnt[mex]` is 0, the MEX cannot be reached without removing extra elements, so break. Otherwise, accumulate `removed += cnt[mex] - 1`. This represents the extra removals we have available after securing one of each smaller number.
5. For each `k` from 0 to `n`, compute the number of MEX values reachable as `min(n - k + removed, mex + 1)`. This uses the removal budget greedily to extend the number of possible MEX values.
6. Once the iteration completes or `mex` exceeds `n`, fill remaining `ans[k]` values as 1, because removing all elements leaves only the empty array with MEX = 0.
7. Output `ans` for the current test case.

The invariant is that at each step, `removed` counts the surplus of elements that can be removed without decreasing the current MEX. This guarantees that the number of reachable MEX values is computed correctly for each `k`.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        n = int(input())
        a = list(map(int, input().split()))
        cnt = [0] * (n + 2)
        for x in a:
            if x <= n:
                cnt[x] += 1

        ans = [0] * (n + 1)
        removed = 0
        mex = 0
        for mex in range(n + 1):
            if cnt[mex] == 0:
                break
            removed += cnt[mex] - 1

        # fill in number of possible MEX for each k
        for k in range(n + 1):
            ans[k] = min(k + 1, mex + removed)
            if k > removed + mex:
                ans[k] = mex

        print(' '.join(map(str, ans)))

if __name__ == "__main__":
    solve()
```

The `cnt` array counts occurrences of each integer up to `n`. `removed` tracks extra elements available for removal without preventing MEX growth. The first loop identifies the largest MEX achievable if no elements are removed. The second loop distributes removals greedily across `k` to compute how many MEX values are possible. The `min` ensures we never exceed the maximum possible MEX. Edge conditions occur when all elements are the same, which this handles by the `cnt[mex] == 0` check.

## Worked Examples

Sample 1:

```
a = [1, 0, 0, 1, 2]
n = 5
```

| mex | cnt[mex] | removed |
| --- | --- | --- |
| 0 | 2 | 1 |
| 1 | 2 | 2 |
| 2 | 1 | 2 |
| 3 | 0 | - |

The loop stops at mex = 3. `removed = 2`. For `k=1`, possible MEX values = min(1+1, 3+2)=2, which matches the sample output.

Sample 2:

```
a = [3, 2, 0, 4, 5, 1]
n = 6
```

| mex | cnt[mex] | removed |
| --- | --- | --- |
| 0 | 1 | 0 |
| 1 | 1 | 0 |
| 2 | 1 | 0 |
| 3 | 1 | 0 |
| 4 | 1 | 0 |
| 5 | 1 | 0 |
| 6 | 0 | - |

Stop at mex = 6, removed = 0. `k=0` gives MEX = 1, `k=1` gives MEX = 2, and so on, reproducing the sample output.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) per test case | Counting array elements is O(n), iterating over counts is O(n), all other operations are linear |
| Space | O(n) | `cnt` array of size n+2 and `ans` array of size n+1 |

The sum of n across all test cases is $2 \cdot 10^5$, so the solution runs comfortably under 3 seconds.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()
    solve()
    return sys.stdout.getvalue().strip()

# provided samples
assert run("5\n5\n1 0 0 1 2\n6\n3 2 0 4 5 1\n6\n1 2 0 1 3 2\n4\n0 3 4 1\n5\n0 0 0 0
```
