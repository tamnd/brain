---
title: "CF 102163K - Masaoud LOVES PIZZAS"
description: "We have an array of positive integers, where A[i] is the number of pizza slices on the plate of the i-th student. Masaoud must choose a contiguous group of students, so every valid choice corresponds to a subarray of A."
date: "2026-08-19T07:52:41+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102163
codeforces_index: "K"
codeforces_contest_name: "NCD 2019"
rating: 0
weight: 102163
solve_time_s: 112
verified: false
draft: false
---

[CF 102163K - Masaoud LOVES PIZZAS](https://codeforces.com/problemset/problem/102163/K)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 52s  
**Verified:** no  

## Solution
## Problem Understanding

We have an array of positive integers, where `A[i]` is the number of pizza slices on the plate of the `i`-th student. Masaoud must choose a contiguous group of students, so every valid choice corresponds to a subarray of `A`. A choice is valid when the sum of that subarray is strictly smaller than `X`.

For example, with `A = [1, 2, 3]`, the group containing positions `1..2` has sum `1 + 2 = 3`. If `X = 4`, that group is valid, while the group `1..3`, whose sum is `6`, is not. The required output is the total number of contiguous subarrays whose sum is less than `X`.

The values of `A[i]` and `X` can be as large as `10^9`, while `N` can reach `10^5`. A quadratic algorithm may inspect about `N(N+1)/2`, which is roughly `5 * 10^9` subarrays at the maximum size. That is far beyond what a one-second Codeforces time limit can handle. We need an algorithm whose work grows essentially linearly with the array size. Since all `A[i]` are positive, adding another element always increases a subarray sum, which gives us exactly the monotonicity needed for a sliding-window solution.

There are several boundary cases that can make an otherwise reasonable implementation wrong. The first is the strict inequality. For the input

```
1
1 3
3
```

the answer is `0`, because the only subarray has sum `3`, and `3 < 3` is false. A careless implementation using `while sum > X` would incorrectly count it.

Another edge case occurs when no non-empty subarray can satisfy the condition. For

```
1
2 1
5 6
```

the answer is `0`. Every individual element already has a sum greater than or equal to `X`. The window must be allowed to become empty after removing elements.

The opposite case is when every subarray is valid. For

```
1
3 10
1 2 3
```

all `3 * 4 / 2 = 6` non-empty subarrays have sum below `10`. The algorithm must count every possible starting position, not only the longest window ending at each position.

## Approaches

The direct solution is to enumerate every possible pair of endpoints. For each starting position, we can extend the ending position and maintain the current sum. Because every contiguous group is uniquely determined by its left and right endpoints, this examines every possible group and is completely correct.

The problem is the number of such groups. An array of length `10^5` has `10^5 * 100001 / 2 = 5,000,050,000` non-empty subarrays. Even if each sum were maintained in constant time, processing several billion candidates is much too slow for a one-second limit. Computing each sum from scratch would be even worse, at `O(N^3)` if implemented literally.

The key observation is that every array element is positive. Fix a right endpoint `r` and suppose we have found the smallest left endpoint `l` such that the window `[l, r]` has sum less than `X`. Because all elements are positive, every shorter suffix ending at `r`, namely `[l+1, r]`, `[l+2, r]`, and so on, also has sum less than `X`. There are exactly `r - l + 1` such subarrays.

Even better, when we move `r` one position to the right, the previous window can be reused. We add `A[r]` to the sum, and if the sum becomes too large, we repeatedly remove elements from the left until the window is valid again. Since an element is added once and removed at most once, the total number of pointer movements is linear.

The brute-force method works because it explicitly checks every contiguous group, but fails because there are too many groups. The observation that positive values make the window sum monotonic lets us discard all invalid or redundant choices at once, reducing the computation to a single pass.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(N²) | O(1) | Too slow |
| Sliding Window | O(N) | O(1) auxiliary | Accepted |

## Algorithm Walkthrough

1. Initialize a left pointer `left = 0`, a running window sum `current_sum = 0`, and the answer `answer = 0`. The window `[left, right]` will represent the current contiguous group under consideration.
2. Move the right endpoint from left to right through the array. Add `A[right]` to `current_sum` because the new right endpoint is now included in the window.
3. While `current_sum >= X`, remove `A[left]` from the window and increment `left`. The condition is `>=`, rather than `>`, because the problem requires the sum to be strictly less than `X`.
4. Once the loop stops, the current window `[left, right]` has sum less than `X`. Since all values are positive, every subarray ending at `right` and starting anywhere from `left` through `right` also has sum less than `X`. There are `right - left + 1` such subarrays, so add that number to `answer`.
5. After processing every right endpoint, print `answer`. Every non-empty contiguous subarray has exactly one right endpoint, so it has been counted exactly once.

### Why it works

The central invariant is that after the shrinking loop finishes, `[left, right]` is the shortest valid suffix of the prefix ending at `right` with respect to the current left boundary. More precisely, every starting position from `left` through `right` gives a valid subarray, while any position before `left` would produce a sum at least `X`, because adding positive elements can only increase the sum. Thus exactly `right - left + 1` valid subarrays end at `right`. As every subarray has one unique right endpoint, summing this quantity over all `right` counts every valid group once and no invalid group.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())

    for _ in range(t):
        n, x = map(int, input().split())
        a = list(map(int, input().split()))

        left = 0
        current_sum = 0
        answer = 0

        for right in range(n):
            current_sum += a[right]

            while left <= right and current_sum >= x:
                current_sum -= a[left]
                left += 1

            answer += right - left + 1

        print(answer)

if __name__ == "__main__":
    solve()
```

The input is read with `sys.stdin.readline` so that multiple large test cases can be processed efficiently. The entire array is stored because the input naturally provides it as one line, although the algorithm itself only needs the elements in their original order.

For each `right`, `a[right]` is first added to the current sum. Only after adding it do we shrink the window, because the new element may have made an otherwise valid window invalid.

The `while` condition uses `current_sum >= x`. If the sum is exactly `X`, the group is not allowed, so at least one element must be removed. This strict boundary is one of the most common sources of wrong answers for this problem.

The expression `right - left + 1` counts the valid subarrays ending at `right`. For example, if `left = 2` and `right = 5`, the valid starts are `2, 3, 4, 5`, giving four subarrays.

The check `left <= right` prevents the implementation from attempting to remove an element from an already empty window. When a single element is itself at least `X`, that element is removed immediately and `left` becomes `right + 1`. The contribution then becomes zero, correctly reflecting that no valid subarray ends at that position.

Python integers have arbitrary precision, so there is no overflow issue. In languages with fixed-width integer types, a 64-bit integer is required for the answer because there can be about `N(N+1)/2` valid subarrays, which is around `5 * 10^9` for `N = 10^5`.

## Worked Examples

The first sample contains the single-element array `[3]` with `X = 4`.

| right | added value | current_sum before shrinking | left after shrinking | current_sum after shrinking | added to answer | answer |
| --- | --- | --- | --- | --- | --- | --- |
| 0 | 3 | 3 | 0 | 3 | 1 | 1 |

The only window is `[3]`, whose sum is `3 < 4`. There is one valid subarray, so the answer is `1`. This trace demonstrates the simplest case where the window remains unchanged and contributes exactly one subarray.

For the second sample, `A = [1, 5]` and `X = 4`.

| right | added value | current_sum before shrinking | left after shrinking | current_sum after shrinking | added to answer | answer |
| --- | --- | --- | --- | --- | --- | --- |
| 0 | 1 | 1 | 0 | 1 | 1 | 1 |
| 1 | 5 | 6 | 2 | 0 | 0 | 1 |

At `right = 0`, the subarray `[1]` is valid. At `right = 1`, adding `5` gives a sum of `6`, so the algorithm removes `1`, leaving `[5]`, which is still invalid. It then removes `5`, leaving an empty window. Consequently there are no valid subarrays ending at position `1`. The final answer remains `1`, corresponding only to `[1]`.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(N) per test case | Each element enters the window once and leaves it at most once |
| Space | O(N) | The input array is stored; the sliding-window state itself uses O(1) auxiliary space |

Across all test cases, the total time is linear in the total number of input elements. With `N <= 10^5`, this is comfortably within the intended complexity for the one-second limit. The stored array uses well below the 256 MB memory limit for the stated input size.

## Test Cases

```python
import sys
import io

def solve():
    input = sys.stdin.readline
    t = int(input())

    for _ in range(t):
        n, x = map(int, input().split())
        a = list(map(int, input().split()))

        left = 0
        current_sum = 0
        answer = 0

        for right in range(n):
            current_sum += a[right]

            while left <= right and current_sum >= x:
                current_sum -= a[left]
                left += 1

            answer += right - left + 1

        print(answer)

def run(inp: str) -> str:
    old_stdin = sys.stdin
    old_stdout = sys.stdout

    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    try:
        solve()
        return sys.stdout.getvalue()
    finally:
        sys.stdin = old_stdin
        sys.stdout = old_stdout

# Provided sample
assert run("""\
2
1 4
3
2 4
1 5
""") == """\
1
1
""", "provided sample"

# Minimum-size input, and equality with X must not be counted.
assert run("""\
2
1 1
1
1 2
1
""") == """\
0
1
""", "minimum size and strict inequality"

# All subarrays are valid.
assert run("""\
1
3 10
1 2 3
""") == """\
6
""", "all subarrays valid"

# All equal values.
# Valid subarrays have length 1 or 2 because 2 + 2 < 5,
# while a length-3 subarray has sum 6.
assert run("""\
1
4 5
2 2 2 2
""") == """\
7
""", "all equal values"

# Boundary case where a sum exactly equal to X must be excluded.
assert run("""\
1
3 6
1 2 3
""") == """\
4
""", "exact equality must be excluded"

# Maximum-size input.
# X = 1 and every element is 1, so no non-empty subarray is valid.
n = 100000
max_case = "1\n{} 1\n{}\n".format(n, " ".join(["1"] * n))
assert run(max_case) == "0\n", "maximum N"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 1 / [1]` and `1 2 / [1]` | `0`, `1` | Minimum size and strict inequality |
| `3 10 / [1,2,3]` | `6` | Every possible subarray is valid |
| `4 5 / [2,2,2,2]` | `7` | Equal values and counting multiple valid lengths |
| `3 6 / [1,2,3]` | `4` | A sum exactly equal to `X` must not be counted |
| `N=100000, X=1, all values 1` | `0` | Maximum input size and empty-window behavior |

## Edge Cases

When the only element is exactly `X`, the input

```
1
1 3
3
```

has answer `0`. The algorithm adds `3`, sees that `current_sum >= X`, removes the only element, and advances `left` to `1`. The contribution is `right - left + 1 = 0`, so the equality case is correctly excluded.

When every element is already too large, consider

```
1
2 1
5 6
```

At the first position, the sum becomes `5`, so the element is immediately removed and the contribution is zero. At the second position, the same thing happens with `6`. The final answer is `0`. The `left <= right` condition allows the window to become empty without accessing outside the array.

When every subarray is valid, consider

```
1
3 10
1 2 3
```

At `right = 0`, there is one valid subarray. At `right = 1`, both `[2]` and `[1,2]` are valid, contributing two more. At `right = 2`, all three suffixes `[3]`, `[2,3]`, and `[1,2,3]` are valid, contributing three. The total is `1 + 2 + 3 = 6`, which is every possible non-empty subarray.

The positivity of `A[i]` is what makes the sliding window valid. If negative numbers were allowed, removing an element from the left could increase the sum, and extending the right endpoint could decrease it. The monotonic relationship used by the algorithm would disappear, so this exact technique could no longer be justified.
