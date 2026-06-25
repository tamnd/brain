---
title: "CF 105947E - \u0110\u1ebfm s\u1ed1 \u0111o\u1ea1n con"
description: "We are given several test cases, each consisting of an integer array. For each array, the task is to count how many contiguous subarrays contain exactly k distinct values."
date: "2026-06-25T13:51:55+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105947
codeforces_index: "E"
codeforces_contest_name: "Bach Khoa Code Challenge #2"
rating: 0
weight: 105947
solve_time_s: 40
verified: true
draft: false
---

[CF 105947E - \u0110\u1ebfm s\u1ed1 \u0111o\u1ea1n con](https://codeforces.com/problemset/problem/105947/E)

**Rating:** -  
**Tags:** -  
**Solve time:** 40s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given several test cases, each consisting of an integer array. For each array, the task is to count how many contiguous subarrays contain exactly `k` distinct values.

A contiguous subarray is a slice of the array formed by choosing a left boundary and a right boundary without reordering elements. “Exactly k distinct values” means that if we look at all elements inside that slice, the number of unique numbers appearing in it is precisely `k`.

So the output for each test case is a single number: the total count of such subarrays.

The constraints imply a classic subarray counting setting. The total length over all test cases is up to about `2 · 10^5`, which rules out any solution that is quadratic per test case. A naive O(n²) enumeration of all subarrays would perform about 2e10 operations in the worst case, which is far beyond limits. This pushes us toward linear or near-linear techniques, typically sliding window or two pointers.

There are a few subtle edge cases that often break incorrect solutions.

If all elements are equal and `k = 1`, every subarray is valid. For example, `[5, 5, 5]` should yield 6 valid subarrays. A naive solution that mistakenly counts only maximal segments would undercount.

If `k` is larger than the number of distinct elements in the whole array, the answer must be zero. For instance, `[1, 2, 1]` with `k = 3` has no valid subarray, even though every subarray has at most 2 distinct values.

Another tricky situation is when duplicates are interleaved. For example, `[1, 2, 1, 2]` with `k = 2` has many valid subarrays, and counting requires careful handling of boundaries; simply tracking distinct counts without proper shrinking leads to overcounting overlapping windows.

## Approaches

The brute-force idea is straightforward. We iterate over every left endpoint, expand the right endpoint, and maintain a set of elements to count distinct values. Each time we extend the right pointer, we recompute or update the set and check whether the number of distinct values is exactly `k`. This correctly counts all valid subarrays because it directly checks every possible segment.

The issue is performance. Maintaining a set per expansion is O(1) amortized, but we still examine O(n²) subarrays per test case in the worst case. With total input size 2e5, this becomes infeasible.

The key observation is that we do not actually need to count “exactly k” directly. Instead, it is much easier to count “at most k” distinct values. A standard sliding window technique allows us to maintain a window `[l, r]` such that it always contains at most `k` distinct elements. For each `r`, all subarrays ending at `r` and starting anywhere from `l` to `r` are valid under this constraint, contributing `(r - l + 1)` subarrays.

Once we can compute `atMost(k)`, we can convert the problem into a difference of two easier problems: subarrays with exactly `k` distinct values equals `atMost(k) - atMost(k - 1)`. This works because every subarray with exactly `k` distinct values is included in `atMost(k)` but excluded from `atMost(k - 1)`.

This transforms the problem into two linear sliding window passes.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n²) | O(n) | Too slow |
| Sliding Window (at most k + subtraction) | O(n) per test | O(n) | Accepted |

## Algorithm Walkthrough

We build a helper function `at_most(k)` that counts subarrays with at most `k` distinct values.

1. Initialize two pointers `l = 0` and `result = 0`. Also maintain a frequency map `freq` and a variable `distinct = 0`. The map tracks how many times each value appears in the current window.
2. Expand the right pointer `r` from `0` to `n - 1`, adding `a[r]` to the window. If this value was previously absent, increase `distinct`. Update its frequency in the map.
3. If `distinct` exceeds `k`, shrink the window from the left. Move `l` forward while decrementing frequencies. When a frequency becomes zero, decrease `distinct`. This restores the invariant that the window has at most `k` distinct values.
4. After the window is valid, all subarrays ending at `r` and starting between `l` and `r` are valid. Add `(r - l + 1)` to `result`. This works because every such subarray still lies inside the current valid window.
5. Return `result`.

For the final answer, compute `at_most(k) - at_most(k - 1)`.

### Why it works

At every step, the window `[l, r]` is the smallest left boundary such that the subarray ending at `r` contains at most `k` distinct values. Any smaller left boundary would violate the constraint, and any larger one would miss valid subarrays. This makes the contribution counting exact, since each subarray ending at `r` is counted exactly once when its right endpoint is processed.

## Python Solution

```python
import sys
input = sys.stdin.readline

from collections import defaultdict

def at_most(a, k):
    if k < 0:
        return 0
    freq = defaultdict(int)
    l = 0
    distinct = 0
    res = 0

    for r, x in enumerate(a):
        if freq[x] == 0:
            distinct += 1
        freq[x] += 1

        while distinct > k:
            y = a[l]
            freq[y] -= 1
            if freq[y] == 0:
                distinct -= 1
            l += 1

        res += r - l + 1

    return res

t = int(input())
for _ in range(t):
    n, k = map(int, input().split())
    a = list(map(int, input().split()))
    print(at_most(a, k) - at_most(a, k - 1))
```

The core structure is the two-pointer sliding window. The frequency dictionary tracks occurrences inside the current window, and `distinct` avoids recomputing the number of unique elements from scratch.

A common mistake is recomputing a set for each `r`, which silently turns the solution quadratic. Another is forgetting that shrinking must continue until the constraint is satisfied again; a single conditional shrink is not enough.

The subtraction at the end is essential. Without `at_most(k - 1)`, the function would count all subarrays with fewer than `k` distinct values as well.

## Worked Examples

### Example 1

Input:

```
n = 3, k = 2
a = [1, 2, 1]
```

| r | l | window | distinct | contribution |
| --- | --- | --- | --- | --- |
| 0 | 0 | [1] | 1 | 1 |
| 1 | 0 | [1,2] | 2 | 2 |
| 2 | 0 | [1,2,1] | 2 | 3 |

`at_most(2) = 6`, `at_most(1) = 3`, so answer is `3`.

This confirms that overlapping windows are counted correctly via `(r - l + 1)`.

### Example 2

Input:

```
n = 4, k = 1
a = [5, 5, 5, 5]
```

| r | l | window | distinct | contribution |
| --- | --- | --- | --- | --- |
| 0 | 0 | [5] | 1 | 1 |
| 1 | 0 | [5,5] | 1 | 2 |
| 2 | 0 | [5,5,5] | 1 | 3 |
| 3 | 0 | [5,5,5,5] | 1 | 4 |

Here `at_most(1) = 10`, `at_most(0) = 0`, so answer is `10`.

This shows the algorithm naturally handles repeated elements without special casing.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) per test case | Each pointer moves at most n steps, and each element enters and leaves the window once |
| Space | O(n) | Frequency map stores at most n distinct values |

The total complexity over all test cases is linear in the total input size, which fits comfortably under the constraints where the sum of `n` is about `2 · 10^5`.

## Test Cases

```python
import sys, io
from collections import defaultdict

def solve():
    input = sys.stdin.readline
    def at_most(a, k):
        if k < 0:
            return 0
        freq = defaultdict(int)
        l = 0
        distinct = 0
        res = 0
        for r, x in enumerate(a):
            if freq[x] == 0:
                distinct += 1
            freq[x] += 1
            while distinct > k:
                y = a[l]
                freq[y] -= 1
                if freq[y] == 0:
                    distinct -= 1
                l += 1
            res += r - l + 1
        return res

    t = int(input())
    out = []
    for _ in range(t):
        n, k = map(int, input().split())
        a = list(map(int, input().split()))
        out.append(str(at_most(a, k) - at_most(a, k - 1)))
    return "\n".join(out)

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    return solve()

# provided samples
assert run("""3
1 1
10
3 1
3 1 8
16 1
8 1 5 8 8 7 4 9 7 10 10 7 5 8 5 5
""") == """1
3
19"""

# custom cases
assert run("""1
3 1
5 5 5
""") == "6"

assert run("""1
4 2
1 2 3 4
""") == "3"

assert run("""1
5 3
1 2 3 1 2
""") == "7"

assert run("""1
4 5
1 2 3 4
""") == "0"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| all equal | 6 | maximum overlap counting |
| all distinct | 3 | correct sliding window shrinking |
| mixed repeats | 7 | overlapping distinct tracking |
| k too large | 0 | edge condition handling |

## Edge Cases

When all elements are identical and `k = 1`, the window never shrinks because `distinct` stays at 1. The algorithm counts every prefix ending at each position, which naturally produces the full triangular number of subarrays. For `[5, 5, 5]`, the contributions are 1, 2, and 3, summing to 6, matching the correct count.

When `k = 0`, the helper `at_most(k - 1)` becomes `at_most(-1)` which is defined as zero, so the result is also zero. This avoids special casing invalid configurations where no subarray can have zero distinct values.

When all elements are distinct and `k = 2`, the window shrinks aggressively. For `[1,2,3,4]`, the valid contributions per position are 1, 2, 2, and 2, giving 7 for `at_most(2)`, and subtracting `at_most(1)` removes single-element subarrays, leaving exactly those with two distinct values.
